"""Detect stale authored skill/reference bodies (Step 9 — process-cycle Phase 12).

An authored doc (``status: ready``) records ``provenance.authored_from_digest``: a sha256 over
the **current statements** of the principles + claims it was authored from. When those upstream
statements change — e.g. a source is re-ingested and principles re-derived — the digest no
longer matches, so the body is stale and must be re-authored (Step 8 treats ``stale`` like a
stub). Deterministic and git-safe: it compares content digests, not mtimes.

Modes (CLI):
  (default)  check  — report STALE / WARN / INFO / OK; exit 0 (advisory).
  --stamp           — write authored_from_digest into every *ready* doc from current upstream
                      (no LLM; called by author-skills as its final step).
  --mark            — flip drifted *ready* docs to status: stale (write).

``detect_stale(base) -> list[(level, artifact, reason)]`` with
``level in {"STALE", "WARN", "INFO", "OK"}`` — the gate maps STALE/WARN → warn.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

from tools.subagent_factory.generate_stubs import planned_slugs
from tools.subagent_factory.validate_skill_authoring import _parse_frontmatter

_US = "\x1f"  # unit separator: id ↔ statement
_RS = "\x1e"  # record separator: between cited items


def _load_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _principle_statements(base: Path) -> dict[str, str]:
    data = _load_yaml(base / "principles" / "principles.yaml")
    return {
        str(p.get("principle_id")): str(p.get("statement", ""))
        for p in (data.get("principles") or [])
        if p.get("principle_id")
    }


def _claim_statements(base: Path) -> dict[str, str]:
    cp = base / "analysis" / "claims.jsonl"
    out: dict[str, str] = {}
    if not cp.exists():
        return out
    for line in cp.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            c = json.loads(line)
            out[str(c["claim_id"])] = str(c.get("statement", ""))
        except (json.JSONDecodeError, KeyError):
            continue
    return out


def _digest(
    prov: dict, principles: dict[str, str], claims: dict[str, str]
) -> tuple[str, list[str]]:
    """sha256 over cited principle + claim statements (sorted, canonical). Returns (digest,
    missing_ids) where missing_ids are cited IDs absent from the current upstream."""
    parts: list[str] = []
    missing: list[str] = []
    for pid in sorted(str(x) for x in (prov.get("principles") or [])):
        st = principles.get(pid)
        if st is None:
            missing.append(pid)
            st = "<MISSING>"
        parts.append(f"P:{pid}{_US}{st}")
    for cid in sorted(str(x) for x in (prov.get("claims") or [])):
        st = claims.get(cid)
        if st is None:
            missing.append(cid)
            st = "<MISSING>"
        parts.append(f"C:{cid}{_US}{st}")
    h = hashlib.sha256(_RS.join(parts).encode("utf-8")).hexdigest()
    return h, missing


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _doc_paths(base: Path) -> list[tuple[str, str, Path]]:
    """(kind, slug, path) for every declared skill + reference doc."""
    profile = _load_yaml(base / "profile.yaml")
    skills, refs = planned_slugs(profile)
    out: list[tuple[str, str, Path]] = []
    for _entry, slug in skills:
        out.append(("skill", slug, base / "skills" / slug / "SKILL.md"))
    for _entry, slug in refs:
        out.append(("reference", slug, base / "references" / f"{slug}.md"))
    return out


def _body_of(text: str) -> str:
    end = text.find("\n---", 3)
    return text[end + 4 :] if end != -1 else ""


def _rewrite(path: Path, fm: dict, body: str) -> None:
    """Re-emit the frontmatter block (key order preserved), body verbatim."""
    dump = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
    body = body.lstrip("\n")
    path.write_text(f"---\n{dump}---\n\n{body}", encoding="utf-8")


def _source_drift(base: Path) -> list[tuple[str, str, str]]:
    manifest = _load_yaml(base / "source-pack.manifest.yaml")
    out: list[tuple[str, str, str]] = []
    for s in manifest.get("sources") or []:
        sid, sha = s.get("source_id"), s.get("sha256")
        if not sid or not sha:
            continue
        od = base / "sources" / "original" / str(sid)
        files = sorted(od.glob("original.*")) if od.exists() else []
        files = [f for f in files if f.is_file()]
        if not files:
            continue
        if _sha256_file(files[0]) != sha:
            out.append(
                (
                    "WARN",
                    f"source:{sid}",
                    "original file sha differs from manifest (replaced in place)",
                )
            )
    return out


def detect_stale(
    subagent_dir: str | Path, *, stamp: bool = False, mark: bool = False
) -> list[tuple[str, str, str]]:
    """Return ``[(level, artifact, reason)]``. With ``stamp``/``mark`` it also writes."""
    base = Path(subagent_dir)
    if not (base / "profile.yaml").exists():
        return []
    principles = _principle_statements(base)
    claims = _claim_statements(base)
    out: list[tuple[str, str, str]] = list(_source_drift(base))

    for kind, slug, path in _doc_paths(base):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if not fm:
            continue
        status = str(fm.get("status", "")).lower()
        if status not in ("ready", "stale"):
            continue  # stubs are Step 8's concern, not maintenance
        aid = f"{kind}:{slug}"
        prov = fm.get("provenance") or {}
        current, missing = _digest(prov, principles, claims)

        if not (prov.get("principles") or prov.get("claims")):
            out.append(("OK", aid, "no principle/claim provenance (not drift-tracked)"))
            continue

        if stamp:
            if status != "ready":
                out.append(("OK", aid, "skipped stamp (not ready — re-author first)"))
                continue
            prov["authored_from_digest"] = current
            fm["provenance"] = prov
            _rewrite(path, fm, _body_of(text))
            out.append(("OK", aid, "stamped"))
            continue

        stored = prov.get("authored_from_digest")
        if stored is None:
            out.append(
                (
                    "INFO",
                    aid,
                    "no baseline digest (authored before drift-tracking); re-stamp to enable",
                )
            )
            continue

        if missing:
            level, reason = "STALE", f"cited IDs no longer present: {', '.join(missing)}"
        elif stored != current:
            level, reason = "STALE", "grounding changed since authoring (digest mismatch)"
        else:
            level, reason = "OK", "grounding unchanged"

        if status == "stale" and level == "OK":
            out.append(
                (
                    "WARN",
                    aid,
                    "marked stale but grounding now matches; re-author or --stamp to clear",
                )
            )
            continue
        if level == "STALE" and mark and status != "stale":
            fm["status"] = "stale"
            _rewrite(path, fm, _body_of(text))
            reason += " [marked stale]"
        out.append((level, aid, reason))

    return out


def main() -> None:
    args = sys.argv[1:]
    flags = {a for a in args if a.startswith("--")}
    positional = [a for a in args if not a.startswith("--")]
    if not positional:
        print("Usage: python -m tools.subagent_factory.detect_stale <pkg> [--stamp|--mark]")
        sys.exit(1)
    findings = detect_stale(positional[0], stamp="--stamp" in flags, mark="--mark" in flags)
    for level, artifact, reason in findings:
        print(f"[{level:5s}] {artifact}: {reason}")
    if not findings:
        print("no authored docs to check")
    sys.exit(0)  # advisory; the validate gate is the enforcement surface


if __name__ == "__main__":
    main()
