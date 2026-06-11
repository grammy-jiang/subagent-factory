#!/usr/bin/env python3
"""Deterministic gate for one authoring-campaign round (no LLM).

Reads the claude stream-json log, parses the agent's ``===AUTHOR_SUMMARY===``
block, then decides the round outcome on **ground truth, not the agent's word**:
the package must actually validate AND be ``status: ready``. Writes a per-run
summary, appends to campaign/author-runs.md, and prints the gate verdict:
``ok | review | error | usage-limit``.

Inputs via env: REPO, LOG, SUMM, RUN, SLUG, RC, START, VERIFY.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(os.environ["REPO"])
LOG = Path(os.environ["LOG"])
SUMM = Path(os.environ["SUMM"])
RUN = os.environ["RUN"]
SLUG = os.environ["SLUG"]
RC = int(os.environ.get("RC", "1"))
START = os.environ.get("START", "")
VERIFY = os.environ.get("VERIFY", "red")
RUNS = REPO / "campaign" / "author-runs.md"

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

_LIMIT_RE = re.compile(r"usage limit|rate limit|exceeded your|Overloaded|insufficient.*quota", re.I)


def read_result(p: Path) -> dict:
    res = {"is_error": None, "result": "", "duration_ms": 0, "num_turns": 0, "cost": 0.0}
    if not p.exists():
        return res
    last = None
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "result":
            last = ev
    if last:
        res.update(
            is_error=last.get("is_error"),
            result=last.get("result") or "",
            duration_ms=last.get("duration_ms") or 0,
            num_turns=last.get("num_turns") or 0,
            cost=last.get("total_cost_usd") or 0.0,
        )
    return res


def parse_block(text: str) -> dict[str, str]:
    m = re.search(r"===AUTHOR_SUMMARY===(.*?)===END===", text, re.S)
    d: dict[str, str] = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                d[k.strip().lower()] = v.strip()
    return d


def ground_truth() -> tuple[bool, str]:
    """(validate_passed, profile_status) — the authority, not the agent's claim."""
    from tools.subagent_factory.validate_generated_package import validate_generated_package

    base = REPO / "subagents" / SLUG
    try:
        import yaml

        status = str(
            (yaml.safe_load((base / "profile.yaml").read_text(encoding="utf-8")) or {}).get(
                "status", ""
            )
        ).lower()
    except Exception:
        status = ""
    try:
        passed = bool(validate_generated_package(base).get("passed"))
    except Exception:
        passed = False
    return passed, status


def main() -> int:
    res = read_result(LOG)
    block = parse_block(res["result"])
    passed, status = ground_truth()

    hard_limit = RC != 0 and (bool(res["is_error"]) or bool(_LIMIT_RE.search(res["result"])))
    if passed and status == "ready" and VERIFY == "green":
        gate = "ok"
    elif hard_limit:
        gate = "usage-limit"
    elif res["is_error"] or RC != 0 or not block:
        gate = "error"
    else:
        gate = "review"  # still draft, validate fail, or verify red

    dur = res["duration_ms"] / 1000.0
    SUMM.write_text(
        f"# Author run {RUN} — {SLUG} — {gate}\n"
        f"- when: {START}  ({dur:.0f}s, {res['num_turns']} turns, ${res['cost']:.2f})\n"
        f"- skills_authored: {block.get('skills_authored', '?')}   "
        f"refs_authored: {block.get('refs_authored', '?')}\n"
        f"- ground truth: validate={'pass' if passed else 'fail'}  status={status or '?'}  "
        f"make_verify={VERIFY}\n"
        f"- agent_said: status={block.get('status', '?')} validate={block.get('validate', '?')} "
        f"quote_scan={block.get('quote_scan', '?')}\n"
        f"- finding: {block.get('finding', '')}\n"
        f"- usage_limit: {'yes' if gate == 'usage-limit' else 'no'} (rc={RC})\n"
        f"- gate: {gate}\n"
        f"- log: {LOG.name}\n",
        encoding="utf-8",
    )

    if not RUNS.exists():
        RUNS.write_text(
            "# Authoring Campaign Runs\n\n"
            "| run | gate | slug | skills | refs | validate | status | finding |\n"
            "|--|--|--|--|--|--|--|--|\n",
            encoding="utf-8",
        )
    with open(RUNS, "a", encoding="utf-8") as fh:
        fh.write(
            f"| {RUN} | {gate} | {SLUG} | {block.get('skills_authored', '?')} "
            f"| {block.get('refs_authored', '?')} | {'pass' if passed else 'fail'} "
            f"| {status or '?'} | {block.get('finding', '')[:70].replace('|', '/')} |\n"
        )

    print(gate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
