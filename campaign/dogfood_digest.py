#!/usr/bin/env python3
"""Digest one dogfood-review round: compute NEW findings (vs earlier rounds), print a fix-list for
the in-session fixer, record the seen titles, and DROP any reviewer that produced nothing new from
the active set — so the next round only runs reviewers still finding issues.

A finding's identity = sha1(reviewer + '\\x1f' + normalized(title)); it is NEW if that signature is
not in the cumulative seen-titles file. A reviewer is dropped iff it REPORTED this round (appears in
findings.json) and produced nothing that keeps it alive; a reviewer absent from findings.json (never
got to report, e.g. the session timed out) is KEPT active for another chance.

What "keeps it alive" is `--drop-when`:
  no-new         (default) any NEW finding, at any severity, keeps the reviewer active.
  no-actionable  only a NEW must-fix/should keeps it; a reviewer whose new findings are all nits is
                 dropped (its nits are still printed and recorded). Cheaper convergence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _sig(reviewer: str, title: str) -> str:
    return hashlib.sha1(f"{reviewer}\x1f{_norm(title)}".encode()).hexdigest()


def _load_json(text: str) -> dict:
    """Parse the findings JSON, tolerating an LLM that wrapped it in a ```json fence or prose."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    i, j = text.find("{"), text.rfind("}")  # last resort: first '{' … last '}'
    if 0 <= i < j:
        return json.loads(text[i : j + 1])
    raise json.JSONDecodeError("no JSON object found", text, 0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--findings", required=True)
    ap.add_argument("--seen", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--active", required=True, help="comma-separated reviewers run this round")
    ap.add_argument("--label", default="DOGFOOD REVIEW", help="digest header label")
    ap.add_argument(
        "--drop-when",
        choices=("no-new", "no-actionable"),
        default="no-new",
        help="no-new: any new finding keeps a reviewer; no-actionable: only new must-fix/should does",
    )
    a = ap.parse_args()

    actionable = {"must-fix", "should"}

    active = [r for r in a.active.split(",") if r.strip()]
    fpath = Path(a.findings)
    try:
        data = _load_json(fpath.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"[digest] findings file unreadable/invalid ({e}); state unchanged.", file=sys.stderr)
        return 2

    # Seen store is a TSV (sig \t reviewer \t title): exact-signature dedup for the drop-converged
    # logic, plus a readable title the shell shows the next round's instance as "already reported".
    seen_path = Path(a.seen)
    seen_rows: list[str] = []
    seen_sigs: set[str] = set()
    if seen_path.exists():
        for line in seen_path.read_text(encoding="utf-8").splitlines():
            sig = line.split("\t", 1)[0].strip()
            if sig:
                seen_sigs.add(sig)
                seen_rows.append(line)

    reported = {
        r["reviewer"]: (r.get("findings") or [])
        for r in data.get("reviewers", [])
        if isinstance(r, dict) and r.get("reviewer")
    }

    per: dict[str, dict] = {}
    kept: list[str] = []
    dropped: list[str] = []
    for rv in active:
        if rv not in reported:
            per[rv] = {"status": "absent", "new": [], "total": 0}
            kept.append(rv)  # never reported → keep for another round
            continue
        finds = reported[rv]
        fresh = []
        for f in finds:
            if not isinstance(f, dict):
                continue
            title = str(f.get("title", "")).strip()
            s = _sig(rv, title)
            if s not in seen_sigs:
                seen_sigs.add(s)
                seen_rows.append(f"{s}\t{rv}\t{title}")
                fresh.append(f)
        if a.drop_when == "no-actionable":
            alive = [f for f in fresh if str(f.get("severity", "")).strip() in actionable]
        else:
            alive = fresh
        per[rv] = {"status": "reported", "new": fresh, "total": len(finds), "alive": len(alive)}
        (kept if alive else dropped).append(rv)

    # ── digest ──────────────────────────────────────────────────────────────
    print(f"\n===== {a.label} — round {a.round} digest =====")
    total_new = 0
    for rv in active:
        p = per[rv]
        n = len(p["new"])
        total_new += n
        if p["status"] == "absent":
            print(f"\n## {rv}: (did not report this round — kept active)")
            continue
        if p["alive"]:
            tail = ""
        elif n:
            tail = "   <-- nothing actionable (nits only); DROPPED from next round"
        else:
            tail = "   <-- nothing new; DROPPED from next round"
        print(f"\n## {rv}: {n} new / {p['total']} total  ({p['alive']} actionable){tail}")
        for f in sorted(
            p["new"], key=lambda x: {"must-fix": 0, "should": 1, "nit": 2}.get(x.get("severity"), 3)
        ):
            print(f"  [{f.get('severity', '?')}] {f.get('area', '?')}")
            print(f"      {f.get('title', '').strip()}")
            if f.get("suggestion"):
                print(f"      fix: {str(f['suggestion']).strip()}")

    seen_path.write_text(("\n".join(seen_rows) + "\n") if seen_rows else "", encoding="utf-8")
    Path(a.state).write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")

    print(f"\n[digest] {total_new} new finding(s) this round.")
    if dropped:
        print(f"[digest] converged (dropped): {', '.join(dropped)}")
    print(f"[digest] active next round: {', '.join(kept) if kept else '(none — fully converged)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
