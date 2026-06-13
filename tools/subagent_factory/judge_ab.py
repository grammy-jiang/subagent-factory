"""Pairwise A/B judging harness for two subagent reviews (Phase 10) — judge is injectable.

Implements the budget-feasible subset of the agent-benchmarking harness for comparing two versions
(e.g. 1-source vs 2-source) on the SAME document: **blind position-swapping** (cancels position
bias) over M passes, outcomes fed to ``rank_versions`` for a Bradley-Terry + bootstrap-CI verdict.
The judge is a ``Callable[[str], str]`` injected by the caller — a real LLM in production, a mock in
tests — so the orchestration is deterministic and testable. Caller note: use a judge that is not a
base model of either candidate where possible; for two same-family candidates the self-preference
bias is roughly symmetric (see agent-benchmarking-findings.md).
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path

from tools.subagent_factory.rank_versions import rank_versions

_TMPL = Path(__file__).parent.parent.parent / "examples" / "judge-ab-prompt.tmpl"


def build_judge_prompt(label_a: str, text_a: str, label_b: str, text_b: str) -> str:
    t = _TMPL.read_text(encoding="utf-8")
    return (
        t.replace("{{A_LABEL}}", label_a)
        .replace("{{A_TEXT}}", text_a)
        .replace("{{B_LABEL}}", label_b)
        .replace("{{B_TEXT}}", text_b)
    )


def parse_winner(judge_output: str) -> str | None:
    """Extract ``winner`` from the judge's JSON line (last JSON object wins; tolerant of preamble)."""
    matches = re.findall(r"\{[^{}]*\"winner\"[^{}]*\}", judge_output)
    for m in reversed(matches):
        try:
            w = json.loads(m).get("winner")
        except json.JSONDecodeError:
            continue
        if w:
            return str(w)
    return None


def run_ab(
    ver_a: str,
    text_a: str,
    ver_b: str,
    text_b: str,
    judge: Callable[[str], str],
    passes: int = 6,
    seed: int = 0,
) -> dict:
    """Run ``passes`` position-swapped pairwise judgements; return outcomes + rank_versions verdict.

    Even passes show A as "Review-1"; odd passes show B as "Review-1" — so a judge that always
    prefers position 1 splits its votes evenly and `rank_versions` reports no separation.
    """
    outcomes: list[dict] = []
    for i in range(passes):
        if i % 2 == 0:
            (l1, t1, v1), (l2, t2, v2) = ("Review-1", text_a, ver_a), ("Review-2", text_b, ver_b)
        else:
            (l1, t1, v1), (l2, t2, v2) = ("Review-1", text_b, ver_b), ("Review-2", text_a, ver_a)
        w = parse_winner(judge(build_judge_prompt(l1, t1, l2, t2)))
        if w == "Review-1":
            outcomes.append({"winner": v1, "loser": v2})
        elif w == "Review-2":
            outcomes.append({"winner": v2, "loser": v1})
        # unparseable verdict → skipped (recorded as no outcome)
    return {
        "passes": passes,
        "outcomes": outcomes,
        "n_decided": len(outcomes),
        "ranking": rank_versions(outcomes, seed=seed),
    }
