#!/usr/bin/env python3
"""Spec-driven round runner — automate the deterministic prep the LLM used to do by hand.

The LLM only curates a small YAML spec (which topic, which books). This script does the rest:
resolve book title-hints to corpus PDF paths, stage them to Markdown (pymupdf4llm, keeps
headings), write campaign/<slug>.sources, and launch the staggered dual-engine chains to
status: ready.

Spec (campaign/rounds/<name>.yaml):
    stagger: 75            # optional, seconds between engine launches
    packages:
      - slug: networking-advisor
        topic: "networking advisor"
        engine: claude      # claude (full) | copilot (2a generate; 2b finish always on claude)
        books:
          - "Computer Networking A Top-Down Approach"   # title hint, resolved against corpus
          - "Network Warrior"
          - path: "Software Architecture/Some Exact File.pdf"   # explicit (awesome-relative or /abs)

Usage:
    prep-round.py <spec.yaml> --resolve     # resolve + print table, no side effects
    prep-round.py <spec.yaml> --stage       # resolve + convert + write .sources
    prep-round.py <spec.yaml> --launch      # stage (if needed) + launch the staggered chains
    prep-round.py <spec.yaml> --launch --dry-run   # print the orchestrator, run nothing
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
PROJECTS = REPO.parent
AWESOME = PROJECTS / "awesome-book-collection"
README_COLLECTIONS = ["999-Computer-Books", "Computer-Science-Reference-Books"]
EXTS = (".pdf", ".epub", ".mobi")
_STOP = {"the", "a", "an", "of", "and", "to", "in", "for", "with", "on", "by", "is", "as", "ed", "edition"}


# ---------- normalization / corpus index ----------
def _tokens(s: str) -> list[str]:
    s = re.sub(r"\.(pdf|epub|mobi)$", "", s, flags=re.I).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return [t for t in s.split() if t not in _STOP and len(t) > 2]


def _norm(s: str) -> str:
    return " ".join(_tokens(s))


def _corpus_index() -> list[tuple[Path, str]]:
    """(path, normalized-name) for every awesome book + every manjunath README entry."""
    idx: list[tuple[Path, str]] = []
    for f in AWESOME.rglob("*"):
        if f.is_file() and f.suffix.lower() in EXTS:
            idx.append((f, _norm(f.name)))
    rx = re.compile(r'href="[^"]*/([^"/]+\.(?:pdf|epub))"[^>]*>(.*?)</a>', re.S | re.I)
    for coll in README_COLLECTIONS:
        readme = PROJECTS / coll / "README.md"
        if not readme.exists():
            continue
        text = readme.read_text(encoding="utf-8", errors="ignore")
        for m in rx.finditer(text):
            fid, title = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
            path = PROJECTS / coll / fid
            if path.exists():
                idx.append((path, _norm(title)))
    return idx


def resolve(hint: str, idx: list[tuple[Path, str]]) -> tuple[Path | None, float, list[Path]]:
    """Best corpus path for a title hint by token-overlap. Returns (best|None, score, ties)."""
    want = set(_tokens(hint))
    if not want:
        return None, 0.0, []
    scored = []
    for path, name in idx:
        have = set(name.split())
        score = len(want & have) / len(want)
        scored.append((score, path))
    scored.sort(key=lambda x: (-x[0], len(x[1].name)))
    best_score = scored[0][0]
    if best_score < 0.5:
        return None, best_score, []
    ties = [p for s, p in scored if abs(s - best_score) < 1e-9]
    return scored[0][1], best_score, ties


def _book_path(entry, idx) -> tuple[Path | None, str, float, list[Path]]:
    """Resolve one spec book entry (str hint or {path: ...}) -> (path, label, score, ties)."""
    if isinstance(entry, dict) and "path" in entry:
        raw = entry["path"]
        p = Path(raw) if raw.startswith("/") else AWESOME / raw
        return (p if p.is_file() else None), raw, (1.0 if p.is_file() else 0.0), []
    path, score, ties = resolve(str(entry), idx)
    return path, str(entry), score, ties


# ---------- staging ----------
def _slug_name(name: str) -> str:
    s = re.sub(r"\.(pdf|epub|mobi)$", "", name, flags=re.I).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:60]


def _heading_count(md: str) -> int:
    return sum(1 for ln in md.splitlines() if re.match(r"#{1,6}\s+\S", ln))


def stage(slug: str, paths: list[Path]) -> int:
    import pymupdf4llm

    out_dir = REPO / "campaign" / "staging" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    staged, rc = [], 0
    for src in paths:
        dst = out_dir / f"{_slug_name(src.name)}.md"
        try:
            md = pymupdf4llm.to_markdown(str(src))
        except Exception as e:  # noqa: BLE001
            print(f"  FAILED {src.name}: {e}")
            rc = 1
            continue
        hc = _heading_count(md)
        dst.write_text(md, encoding="utf-8")
        staged.append(dst)
        print(f"  ok  {dst.name}  ({len(md)} chars, {hc} headings)" + ("  <-- WARN 0 headings" if not hc else ""))
        if not hc:
            rc = 1
    (REPO / "campaign" / f"{slug}.sources").write_text("".join(f"{p}\n" for p in staged), encoding="utf-8")
    print(f"  -> campaign/{slug}.sources ({len(staged)} sources)")
    return rc


# ---------- launch ----------
def build_orchestrator(spec: dict) -> str:
    camp = "$CAMP"
    stagger = int(spec.get("stagger", 75))
    chains = []
    for pkg in spec["packages"]:
        slug, topic, engine = pkg["slug"], pkg["topic"], pkg.get("engine", "claude")
        gen = (
            f'bash {camp}/generate-subagent.sh --fg --slug {slug} --topic "{topic}"'
            if engine == "claude"
            else f'bash {camp}/generate-subagent-copilot.sh --fg --slug {slug} --topic "{topic}"'
        )
        chains.append(
            f'(\n  echo "[{slug}] generate ({engine})"\n  {gen}\n'
            f'  echo "[{slug}] finish-skills (claude)"\n'
            f'  bash {camp}/finish-skills.sh --engine claude --slug {slug}\n'
            f'  echo "[{slug}] DONE"\n) >>"$PAIR" 2>&1 &'
        )
    body = [
        "#!/usr/bin/env bash",
        "set -uo pipefail",
        f'REPO="{REPO}"',
        'CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; mkdir -p "$LOGS"',
        'PAIR="$LOGS/round-$(date +%Y%m%d-%H%M%S).log"',
        'echo "[round] start $(date) log: $PAIR"',
        "pids=()",
    ]
    for i, ch in enumerate(chains):
        body.append(ch)
        body.append("pids+=($!)")
        if i < len(chains) - 1:
            body.append(f'echo "[round] stagger {stagger}s"; sleep {stagger}')
    body.append('for p in "${pids[@]}"; do wait "$p"; done')
    body.append('echo "[round] $(date) ALL DONE"')
    # Auto-review: write review-<slug>.md for every package once both chains finish.
    slugs = " ".join(p["slug"] for p in spec["packages"])
    body.append('VENV_PY="$REPO/.venv/bin/python"; [ -x "$VENV_PY" ] || VENV_PY=python3')
    body.append(f'echo "[round] auto-review"; "$VENV_PY" "$CAMP/review-run.py" {slugs} || true')
    return "\n".join(body) + "\n"


# ---------- main ----------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--resolve", action="store_true")
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--launch", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    spec = yaml.safe_load(Path(args.spec).read_text(encoding="utf-8"))
    idx = _corpus_index()
    print(f"corpus index: {len(idx)} entries\n")

    resolved: dict[str, list[Path]] = {}
    ok = True
    for pkg in spec["packages"]:
        slug = pkg["slug"]
        print(f"=== {slug}  ({pkg.get('engine', 'claude')}) ===")
        paths: list[Path] = []
        for entry in pkg["books"]:
            path, label, score, ties = _book_path(entry, idx)
            if path is None:
                print(f"  UNRESOLVED  ({score:.2f})  {label}")
                ok = False
            elif len(ties) > 1:
                print(f"  AMBIGUOUS   ({score:.2f})  {label}  -> {[p.name for p in ties][:3]}")
                ok = False
            else:
                print(f"  ok ({score:.2f})  {label}\n              -> {path}")
                paths.append(path)
        resolved[slug] = paths

    if not ok:
        print("\nUnresolved/ambiguous entries — fix the spec (add explicit `path:`) and retry.")
        return 1
    if args.resolve:
        return 0

    if (args.stage or args.launch) and not args.dry_run:
        for slug, paths in resolved.items():
            print(f"\n--- staging {slug} ---")
            if stage(slug, paths) != 0:
                print(f"staging produced a flat/failed source for {slug} — aborting.")
                return 1

    if args.launch:
        script = build_orchestrator(spec)
        out = REPO / "campaign" / "logs" / "round-orchestrator.sh"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(script, encoding="utf-8")
        out.chmod(0o755)
        if args.dry_run:
            print(f"\n[dry-run] orchestrator written to {out}:\n")
            print(script)
            return 0
        print(f"\n[launch] running {out} (background it with the Bash tool)")
        subprocess.run(["bash", str(out)], cwd=REPO, check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
