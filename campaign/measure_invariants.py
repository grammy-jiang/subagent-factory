#!/usr/bin/env python3
"""Measure the no-invariant replay baseline on a SUBSAMPLE (the flaky endpoint can't do 157 serial).

Strips the invariant layer from the adapter, replays a stratified sample of behaviour-tests with a
semantic LLM grader, and prints the baseline + the should_attach_invariants decision. Error-scored
tests (runner/grader timeout) are dropped from the mean and reported, so a mid-run timeout doesn't
falsely depress the baseline.

Usage: python3 campaign/measure_invariants.py <slug> [n_per_section]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from tools.subagent_factory.behaviour_replay import (  # noqa: E402
    load_behaviour_tests,
    make_llm_grader,
    replay_suite,
    shell_runner,
)
from tools.subagent_factory.compile_invariants import strip_invariant_section  # noqa: E402
from tools.subagent_factory.invariant_policy import should_attach_invariants  # noqa: E402

RUNNER = "examples/replay-runner.sh"


def llm(prompt: str) -> str:
    # Judge via the same replay runner shell (codex-judge is a separate family; keep it simple +
    # on the working endpoint). One sample — we subsample tests, not judges.
    result = subprocess.run(
        [str(REPO / RUNNER)],
        input=prompt,
        capture_output=True,
        text=True,
        env={**os.environ, "ADAPTER_TEXT": "You are a strict grader. Reply only JSON."},
        timeout=300,
    )
    return result.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("n_per_section", nargs="?", type=int, default=6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base = REPO / "subagents" / args.slug
    adapter = (base / "adapters" / "claude-code" / f"{args.slug}.md").read_text(encoding="utf-8")
    if "## Operating invariants" not in adapter:
        print("no invariant section to gate — adapter already lean")
        return 0

    tests = load_behaviour_tests(base)
    by_section: dict[str, list] = defaultdict(list)
    for test in tests:
        by_section[test["section"]].append(test)
    sample = [test for section in by_section.values() for test in section[: args.n_per_section]]
    section_sizes = {section: len(items) for section, items in by_section.items()}
    print(f"tests total={len(tests)}  sample={len(sample)}  sections={section_sizes}")

    stripped = strip_invariant_section(adapter)
    grader = make_llm_grader(llm, samples=1)
    result = replay_suite(stripped, sample, shell_runner(RUNNER), grader)

    per_test = result["per_test"]
    ok = {name: grade for name, grade in per_test.items() if "error" not in grade}
    errored = {name: grade["error"] for name, grade in per_test.items() if "error" in grade}
    clean_mean = round(sum(grade["score"] for grade in ok.values()) / len(ok), 4) if ok else 0.0
    print(
        f"\nbaseline (no invariants): raw_mean={result['mean_score']}  "
        f"clean_mean={clean_mean}  ok={len(ok)}/{len(sample)}  errored={len(errored)}"
    )
    if errored:
        print(f"  errored tests (dropped from clean_mean): {list(errored)[:10]}")

    decision = should_attach_invariants(clean_mean)
    print(f"\nDECISION: attach_invariants={decision['attach']}  ({decision['reason']})")
    print(
        "→ keep FULL (attach_invariants: true)"
        if decision["attach"]
        else "→ keep LEAN (attach_invariants: false)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
