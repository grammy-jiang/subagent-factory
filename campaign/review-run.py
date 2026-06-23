#!/usr/bin/env python3
"""Post-run review for a generated subagent package (engine-agnostic).

Collects what a generation/finish run produced and writes campaign/logs/review-<slug>.md:
  - the ===GENERATE_SUMMARY=== / ===FINISH_SUMMARY=== machine blocks (if the run emitted them),
  - the authoritative `cli validate` verdict + WARN/FAIL lines,
  - profile status / version, skill+reference authored vs stub counts,
  - faithfulness findings (real over-claims, not the report's prose),
  - known failure signatures seen in the logs (copilot request cap, startup collision,
    flat-conversion, usage-limit, timeout).

Usage: python3 campaign/review-run.py <slug> [<slug> ...]
The `cli validate` call is read-only; this never mutates a package.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
LOGS = REPO / "campaign" / "logs"

SIGNATURES = [
    ("copilot request cap", re.compile(r"\b27 Premium\b")),
    ("usage limit hit", re.compile(r"usage_limit:\s*yes", re.I)),
    ("blocked status", re.compile(r"status:\s*blocked", re.I)),
    ("timeout kill", re.compile(r"\btimeout\b.*\b(124|killed)\b", re.I)),
    ("flat conversion (0 headings)", re.compile(r"headings?\s*[=:]\s*0\b", re.I)),
    ("empty/rc=1 startup", re.compile(r"exited rc=1\b")),
]
SUMMARY_RX = re.compile(r"===(?:GENERATE|FINISH)_SUMMARY===(.*?)===END===", re.S)


def _logs_for(slug: str) -> list[Path]:
    return sorted(p for p in LOGS.glob(f"*{slug}*") if p.is_file() and p.suffix != ".sh")


def _summaries(text: str) -> list[str]:
    return [m.group(1).strip() for m in SUMMARY_RX.finditer(text)]


def _validate(slug: str) -> tuple[str, list[str], list[str]]:
    # Use the repo venv python (it has the factory deps, e.g. slugify); falling back to sys.executable
    # only if the venv is absent. Running under a bare system python yields a ModuleNotFoundError and a
    # bogus verdict "?", which the READY gate then reads as a false NO.
    venv_py = REPO / ".venv" / "bin" / "python"
    py = str(venv_py) if venv_py.exists() else sys.executable
    proc = subprocess.run(
        [py, "-m", "tools.subagent_factory.cli", "validate", slug],
        cwd=REPO,
        capture_output=True,
        text=True,
        env={**os.environ, "SUBAGENT_FACTORY_USE_VENV": "1"},
    )
    out = proc.stdout + proc.stderr
    verdict = "PASSED" if "VALIDATION PASSED" in out else ("FAILED" if "VALIDATION FAILED" in out else "?")
    warns = [ln.strip() for ln in out.splitlines() if "[WARN" in ln or "│ WARN" in ln]
    fails = [ln.strip() for ln in out.splitlines() if "[FAIL" in ln or "│ FAIL" in ln]
    return verdict, warns, fails


def _faithfulness(slug: str) -> int:
    rpt = REPO / "subagents" / slug / "reports" / "faithfulness-report.yaml"
    if not rpt.exists():
        return -1
    try:
        data = yaml.safe_load(rpt.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return -1
    findings = data.get("findings") or []
    if not isinstance(findings, list):
        return -1
    over = {"CONTRADICTED", "HEDGING_REMOVED", "SCOPE_BROADENED"}
    return sum(
        1
        for f in findings
        if isinstance(f, dict) and (f.get("verdict") or f.get("claim_strength") or f.get("level")) in over
    )


def _profile(slug: str) -> dict:
    p = REPO / "subagents" / slug / "profile.yaml"
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def review(slug: str) -> Path:
    prof = _profile(slug)
    verdict, warns, fails = _validate(slug)
    faith = _faithfulness(slug)
    sig_hits: dict[str, list[str]] = {}
    summaries: list[tuple[str, str]] = []
    for log in _logs_for(slug):
        try:
            text = log.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for s in _summaries(text):
            summaries.append((log.name, s))
        for label, rx in SIGNATURES:
            if rx.search(text):
                sig_hits.setdefault(label, []).append(log.name)

    ready = prof.get("status") == "ready" and verdict == "PASSED" and not fails
    lines = [
        f"# Review — {slug}",
        f"_generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}_",
        "",
        f"- **READY: {'YES' if ready else 'NO'}**",
        f"- status: `{prof.get('status')}`  version: `{prof.get('agent_version')}`  tier: `{prof.get('tier')}`",
        f"- validate: **{verdict}**  (FAIL={len(fails)}, WARN={len(warns)})",
        f"- faithfulness findings (real over-claims): {faith if faith >= 0 else 'no report'}",
        "",
        "## Failure signatures in logs",
    ]
    lines += [f"- ⚠️ {k}: {', '.join(sorted(set(v)))}" for k, v in sig_hits.items()] or ["- none"]
    if fails:
        lines += ["", "## Validate FAIL lines", *[f"- {f}" for f in fails]]
    if warns:
        lines += ["", "## Validate WARN lines", *[f"- {w}" for w in warns]]
    lines += ["", "## Run summary blocks"]
    for name, s in summaries:
        lines += [f"### {name}", "```", s, "```"]
    if not summaries:
        lines += ["- (no ===*_SUMMARY=== block emitted)"]

    out = LOGS / f"review-{slug}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: review-run.py <slug> [<slug> ...]", file=sys.stderr)
        return 2
    for slug in sys.argv[1:]:
        path = review(slug)
        print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
