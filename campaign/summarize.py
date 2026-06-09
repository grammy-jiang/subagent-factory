#!/usr/bin/env python3
"""Deterministic post-processing for one campaign round (no LLM).

Reads the claude stream-json log, extracts the final ``result`` event and the
agent's ``===CAMPAIGN_SUMMARY===`` block, merges the bash-supplied envelope
(git delta, make-verify result, timing, exit code), then:
  - writes campaign/logs/run-NNN.summary.md  (~12-line digest),
  - appends a row to campaign/runs.md         (one line per round),
  - updates the queue row for this sha256,
  - prints the gate verdict on stdout: ok | blocked | error | review | usage-limit

All inputs arrive via environment variables set by run.sh.
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
from pathlib import Path

REPO = Path(os.environ["REPO"])
CAMPAIGN = REPO / "campaign"
QUEUE = CAMPAIGN / "pdf-queue.tsv"
RUNS = CAMPAIGN / "runs.md"
LOG = Path(os.environ["LOG"])
SUMM = Path(os.environ["SUMM"])

RUN = os.environ["RUN"]
RELPATH = os.environ["RELPATH"]
SHA = os.environ["SHA"]
SIZE = int(os.environ.get("SIZE", "0"))
VERIFY = os.environ.get("VERIFY", "red")
RC = int(os.environ.get("RC", "1"))
HEAD_BEFORE = os.environ.get("HEAD_BEFORE", "")
HEAD_AFTER = os.environ.get("HEAD_AFTER", "")
START = os.environ.get("START", "")

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
        res["is_error"] = last.get("is_error")
        res["result"] = last.get("result") or ""
        res["duration_ms"] = last.get("duration_ms") or 0
        res["num_turns"] = last.get("num_turns") or 0
        res["cost"] = last.get("total_cost_usd") or 0.0
    return res


def parse_block(text: str) -> dict[str, str]:
    m = re.search(r"===CAMPAIGN_SUMMARY===(.*?)===END===", text, re.S)
    d: dict[str, str] = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                d[k.strip().lower()] = v.strip()
    return d


def git_commits(before: str, after: str) -> str:
    if not before or before == after:
        return ""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "log", "--oneline", f"{before}..{after}"],
            capture_output=True, text=True, check=False,
        ).stdout.strip()
        return out.replace("\n", "; ")
    except Exception:
        return ""


def update_queue(status: str, slug: str) -> None:
    if not QUEUE.exists():
        return
    with open(QUEUE, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    for r in rows[1:]:
        if len(r) >= 6 and r[4] == SHA:
            r[2] = status
            if slug:
                r[3] = slug
    with open(QUEUE, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(rows)


def main() -> int:
    res = read_result(LOG)
    raw = LOG.read_text(encoding="utf-8", errors="replace") if LOG.exists() else ""
    block = parse_block(res["result"])

    advanced = bool(HEAD_AFTER) and HEAD_AFTER != HEAD_BEFORE
    commits = git_commits(HEAD_BEFORE, HEAD_AFTER)
    slug = block.get("slug", "") or ""
    if slug.lower() in {"none", "n/a", ""}:
        slug = ""
    finding = block.get("finding", "") or ""
    bstatus = (block.get("status", "") or "").lower()
    usage_limit = block.get("usage_limit", "no").lower() == "yes" or bool(_LIMIT_RE.search(raw))

    # Gate decision (deterministic).
    if usage_limit:
        gate = "usage-limit"
    elif bstatus == "blocked":
        gate = "blocked"
    elif bstatus == "ok" and VERIFY == "green" and advanced:
        gate = "ok"
    elif res["is_error"] or RC != 0 or not block:
        gate = "error"
    else:
        # ok-but-no-commit, verify red, or a status the agent could not classify.
        gate = "review"

    # Persist queue status (leave PENDING on usage-limit so the PDF is retried).
    store = {"ok": "done", "blocked": "blocked", "error": "error", "review": "review"}.get(gate)
    if store:
        update_queue(store, slug)

    dur = res["duration_ms"] / 1000.0
    SUMM.write_text(
        f"# Run {RUN} — {slug or '(no slug)'} — {gate}\n"
        f"- pdf: {RELPATH} ({SIZE // 1024} KB)\n"
        f"- when: {START}  ({dur:.0f}s, {res['num_turns']} turns, ${res['cost']:.2f})\n"
        f"- conversion: {block.get('conversion', '?')}\n"
        f"- selfcheck: {block.get('selfcheck', '?')}   validate: {block.get('validate', '?')}"
        f"   make_verify: {VERIFY}\n"
        f"- fix_commit: {block.get('fix_commit', 'none')}   (commits: {commits or 'none'})\n"
        f"- head: {HEAD_BEFORE[:9]} -> {HEAD_AFTER[:9]} ({'advanced' if advanced else 'no change'})\n"
        f"- finding: {finding}\n"
        f"- usage_limit: {'yes' if usage_limit else 'no'}   (exit rc={RC})\n"
        f"- gate: {gate}\n"
        f"- log: {LOG.name}\n",
        encoding="utf-8",
    )

    if not RUNS.exists():
        RUNS.write_text(
            "# Campaign Runs\n\n"
            "| run | gate | slug | conv | verify | fix commit | finding |\n"
            "|--|--|--|--|--|--|--|\n",
            encoding="utf-8",
        )
    with open(RUNS, "a", encoding="utf-8") as fh:
        fh.write(
            f"| {RUN} | {gate} | {slug or '-'} | {block.get('conversion', '?')} | {VERIFY} "
            f"| {block.get('fix_commit', 'none')} | {finding[:80].replace('|', '/')} |\n"
        )

    print(gate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
