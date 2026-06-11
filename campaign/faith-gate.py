#!/usr/bin/env python3
"""Deterministic gate for one faithfulness-campaign round (no LLM).

Decides on GROUND TRUTH, not the agent's word: the package must now have a
``reports/faithfulness-report.yaml`` that passes ``validate_faithfulness_report``.
Writes a per-run summary, appends to campaign/faith-runs.md, prints the verdict:
``ok | review | error | usage-limit``.

Env: REPO, LOG, SUMM, RUN, SLUG, RC, START, VERIFY.
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
RUNS = REPO / "campaign" / "faith-runs.md"

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


def report_valid() -> bool:
    from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report

    rep = REPO / "subagents" / SLUG / "reports" / "faithfulness-report.yaml"
    if not rep.exists():
        return False
    try:
        return not validate_faithfulness_report(rep)  # [] == valid
    except Exception:
        return False


def main() -> int:
    res = read_result(LOG)
    valid = report_valid()
    hard_limit = RC != 0 and (bool(res["is_error"]) or bool(_LIMIT_RE.search(res["result"])))
    block = re.search(r"===FAITH_SUMMARY===(.*?)===END===", res["result"], re.S)

    if valid and VERIFY == "green":
        gate = "ok"
    elif hard_limit:
        gate = "usage-limit"
    elif res["is_error"] or RC != 0 or not block:
        gate = "error"
    else:
        gate = "review"

    fields = {}
    if block:
        for ln in block.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                fields[k.strip().lower()] = v.strip()

    dur = res["duration_ms"] / 1000.0
    SUMM.write_text(
        f"# Faith run {RUN} — {SLUG} — {gate}\n"
        f"- when: {START}  ({dur:.0f}s, {res['num_turns']} turns, ${res['cost']:.2f})\n"
        f"- report valid (ground truth): {valid}   make_verify: {VERIFY}\n"
        f"- rules_checked: {fields.get('rules_checked', '?')}  verdicts: {fields.get('verdicts', '?')}\n"
        f"- contradicted_unresolved: {fields.get('contradicted_unresolved', '?')}\n"
        f"- finding: {fields.get('finding', '')}\n"
        f"- usage_limit: {'yes' if gate == 'usage-limit' else 'no'} (rc={RC})\n"
        f"- gate: {gate}\n- log: {LOG.name}\n",
        encoding="utf-8",
    )

    if not RUNS.exists():
        RUNS.write_text(
            "# Faithfulness Campaign Runs\n\n"
            "| run | gate | slug | rules | verdicts | contra | finding |\n"
            "|--|--|--|--|--|--|--|\n",
            encoding="utf-8",
        )
    with open(RUNS, "a", encoding="utf-8") as fh:
        fh.write(
            f"| {RUN} | {gate} | {SLUG} | {fields.get('rules_checked', '?')} "
            f"| {fields.get('verdicts', '?')} | {fields.get('contradicted_unresolved', '?')} "
            f"| {fields.get('finding', '')[:60].replace('|', '/')} |\n"
        )

    print(gate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
