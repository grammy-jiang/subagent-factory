#!/usr/bin/env python3
"""Measure the no-invariant replay baseline on a SUBSAMPLE (the flaky endpoint can't do 157 serial).

Strips the invariant layer from the adapter, replays a stratified sample of behaviour-tests with a
semantic LLM grader, and prints the baseline + the should_attach_invariants decision. Error-scored
tests (runner/grader timeout) are dropped from the mean and reported, so a mid-run timeout doesn't
falsely depress the baseline.

Usage: python3 campaign/measure_invariants.py <slug> [n_per_section]
"""
from __future__ import annotations

import sys
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


def llm(prompt: str) -> str:
    # Judge via the same replay runner shell (codex-judge is a separate family; keep it simple +
    # on the working endpoint). One sample — we subsample tests, not judges.
    import subprocess

    r = subprocess.run(
        [str(REPO / "examples" / "replay-runner.sh")],
        input=prompt,
        capture_output=True,
        text=True,
        env={**__import__("os").environ, "ADAPTER_TEXT": "You are a strict grader. Reply only JSON."},
        timeout=300,
    )
    return r.stdout


def main() -> int:
    slug = sys.argv[1]
    n_per = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    base = REPO / "subagents" / slug
    adapter = (base / "adapters" / "claude-code" / f"{slug}.md").read_text(encoding="utf-8")
    if "## Operating invariants" not in adapter:
        print("no invariant section to gate — adapter already lean")
        return 0
    tests = load_behaviour_tests(base)
    # stratified subsample: first n_per of each section
    by_sec: dict[str, list] = {}
    for t in tests:
        by_sec.setdefault(t["section"], []).append(t)
    sample = [t for sec in by_sec.values() for t in sec[:n_per]]
    print(f"tests total={len(tests)}  sample={len(sample)}  sections={ {k: len(v) for k, v in by_sec.items()} }")

    stripped = strip_invariant_section(adapter)
    grader = make_llm_grader(llm, samples=1)
    res = replay_suite(stripped, sample, shell_runner("examples/replay-runner.sh"), grader)

    ok = {k: v for k, v in res["per_test"].items() if "error" not in v}
    errs = {k: v.get("error") for k, v in res["per_test"].items() if "error" in v}
    clean_mean = round(sum(g["score"] for g in ok.values()) / len(ok), 4) if ok else 0.0
    print(f"\nbaseline (no invariants): raw_mean={res['mean_score']}  "
          f"clean_mean={clean_mean}  ok={len(ok)}/{len(sample)}  errored={len(errs)}")
    if errs:
        print(f"  errored tests (dropped from clean_mean): {list(errs)[:10]}")
    dec = should_attach_invariants(clean_mean)
    print(f"\nDECISION: attach_invariants={dec['attach']}  ({dec['reason']})")
    print("→ keep LEAN (attach_invariants: false)" if not dec["attach"]
          else "→ keep FULL (attach_invariants: true)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
