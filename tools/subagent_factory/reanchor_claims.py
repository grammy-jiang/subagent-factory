"""Surgical LLM re-anchoring of claims (+ inherited evidence) — faithful provenance repair.

When a package's distilled claims are good but their ``source_anchors`` are a stale convention
(concept slugs like ``ch1-tactical-empathy``) that no longer resolve, deterministic content-match is
not safe: a claim anchor asserts *support*, and lexical overlap (or a length-biased window) points at
spans that merely share words. This tool keeps the deterministic part where it is sound — **narrowing
candidates** — and uses an LLM only for the **support judgement**:

1. For each claim, rank the source's anchors by token overlap of the claim against each anchor's own
   (short) text and take the top-K. Short per-anchor text is used on purpose: a length-normalised
   window collapses onto one giant summary span; the short text keeps candidates diverse.
2. Show the LLM the claim plus each candidate's real passage **window** (md between consecutive
   anchors) and ask which candidate id(s) actually state/support the claim — or none.
3. Accept only ids the LLM returns **from the candidate set** (it cannot invent), set them as the
   claim's anchors, and propagate to the 1:1 evidence record by ``claim_id``.

The LLM is an injected ``Callable[[str], str]`` (real ``claude -p`` in ``main``, a fake in tests), so
orchestration is deterministic and testable. A claim the LLM cannot support resolves to an empty
anchor list (valid, honest) rather than a guessed one.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from pathlib import Path

import yaml

from tools.subagent_factory.claim_recall import _content_tokens

_WINDOW_CHARS = 320


def _load_source(base: Path, sid: str) -> tuple[list[tuple[str, set[str]]], dict[str, str]]:
    """Return (ranked anchors [(id, text_tokens)], window snippet per anchor) for a source."""
    af = base / "sources" / "anchors" / f"{sid}.anchors.jsonl"
    if not af.exists():
        return [], {}
    recs = [
        json.loads(line) for line in af.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    recs = [r for r in recs if r.get("anchor_id") and r.get("line_number")]
    recs.sort(key=lambda r: r["line_number"])
    md = base / "sources" / "markdown" / f"{sid}.md"
    lines = md.read_text(encoding="utf-8").splitlines() if md.exists() else []
    ranked: list[tuple[str, set[str]]] = []
    window: dict[str, str] = {}
    for i, r in enumerate(recs):
        aid = str(r["anchor_id"])
        ranked.append((aid, _content_tokens(r.get("text", ""))))
        start = int(r["line_number"]) - 1
        end = int(recs[i + 1]["line_number"]) - 1 if i + 1 < len(recs) else len(lines)
        window[aid] = " ".join(" ".join(lines[start:end]).split())[:_WINDOW_CHARS]
    return ranked, window


def _candidates(statement: str, ranked: list[tuple[str, set[str]]], k: int) -> list[str]:
    bt = _content_tokens(statement)
    scored = sorted(((len(bt & at), aid) for aid, at in ranked), reverse=True)
    return [aid for n, aid in scored[:k] if n > 0]


def build_reanchor_prompt(statement: str, candidates: list[str], window: dict[str, str]) -> str:
    head = (
        "Match a distilled CLAIM to the source passage(s) that actually STATE or SUPPORT it.\n"
        'Return ONLY a JSON object: {"anchors": ["<id>", ...]} with the candidate id(s) whose '
        "passage supports the claim (usually one or two). If none truly support it, return "
        '{"anchors": []}. Never invent an id outside the candidates.\n\n'
        f"CLAIM: {statement}\n\nCANDIDATES:"
    )
    body = "\n".join(f"- {aid}: {window.get(aid, '')}" for aid in candidates)
    return head + "\n" + body


def parse_reanchor(output: str, allowed: set[str]) -> list[str]:
    """Extract the ``anchors`` list from the LLM JSON; keep only ids in ``allowed`` (no invention)."""
    for m in reversed(re.findall(r"\{[^{}]*\"anchors\"[^{}]*\}", output)):
        try:
            ids = json.loads(m).get("anchors")
        except json.JSONDecodeError:
            continue
        if isinstance(ids, list):
            seen: dict[str, None] = {}
            for i in ids:
                if isinstance(i, str) and i in allowed:
                    seen[i] = None
            return list(seen)
    return []


def reanchor_claims(
    subagent_dir: str | Path, llm: Callable[[str], str], *, top_k: int = 12, write: bool = True
) -> dict:
    """Re-anchor every claim whose current anchors don't resolve; propagate to evidence. Summary out."""
    base = Path(subagent_dir)
    claims_path = base / "analysis" / "claims.jsonl"
    claims = [
        json.loads(line)
        for line in claims_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    cache: dict[str, tuple[list[tuple[str, set[str]]], dict[str, str]]] = {}

    def source(sid: str) -> tuple[list[tuple[str, set[str]]], dict[str, str]]:
        if sid not in cache:
            cache[sid] = _load_source(base, sid)
        return cache[sid]

    chosen_by_claim: dict[str, list[str]] = {}
    n_fixed = n_empty = 0
    for c in claims:
        sid = c.get("source_id", "")
        ranked, window = source(sid)
        allowed = {aid for aid, _ in ranked}
        current = c.get("source_anchors") or []
        if current and all(a in allowed for a in current):
            continue  # already resolves — leave it
        cands = _candidates(c.get("statement", ""), ranked, top_k)
        chosen = (
            parse_reanchor(llm(build_reanchor_prompt(c["statement"], cands, window)), set(cands))
            if cands
            else []
        )
        c["source_anchors"] = chosen
        chosen_by_claim[c["claim_id"]] = chosen
        n_fixed += bool(chosen)
        n_empty += not chosen

    if write and chosen_by_claim:
        claims_path.write_text(
            "\n".join(json.dumps(c, ensure_ascii=False) for c in claims) + "\n", encoding="utf-8"
        )
        ev_path = base / "evidence" / "evidence-records.yaml"
        if ev_path.exists():
            ev = yaml.safe_load(ev_path.read_text(encoding="utf-8")) or {}
            for r in ev.get("evidence_records", []) or []:
                cid = r.get("claim_id")
                if cid in chosen_by_claim:
                    r["source_anchors"] = chosen_by_claim[cid]
            ev_path.write_text(
                yaml.safe_dump(ev, sort_keys=False, allow_unicode=True), encoding="utf-8"
            )
    return {
        "n_claims": len(claims),
        "n_fixed": n_fixed,
        "n_empty": n_empty,
        "chosen": chosen_by_claim,
    }


def _claude_llm(prompt: str) -> str:
    import subprocess

    claude = str(Path.home() / ".local" / "bin" / "claude")
    # check=True so a crashed claude call raises instead of returning "" that the caller would treat
    # as "model found no anchor" — a swallowed infra failure masquerading as a real empty result.
    return subprocess.run(
        [claude, "-p", "--model", "claude-opus-4-8", "--dangerously-skip-permissions", prompt],
        text=True,
        capture_output=True,
        timeout=180,
        check=True,
    ).stdout


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.reanchor_claims subagents/<slug>")
        sys.exit(1)
    rep = reanchor_claims(sys.argv[1], _claude_llm)
    print(f"re-anchored {rep['n_fixed']}/{rep['n_claims']} claims ({rep['n_empty']} left empty)")


if __name__ == "__main__":
    main()
