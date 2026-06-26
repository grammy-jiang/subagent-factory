"""Deterministic patch-validation ladder (Step-6 I-track, automated-program-repair research).

A patch-capable subagent (``produce`` / ``patch-suggest`` mode — e.g. ``legacy-code-change-advisor``)
proposes a unified diff; this ladder **decides** whether it may be suggested/applied. Rungs run in a
fixed order and short-circuit at the first hard failure:

  1. ``parse``     — well-formed unified diff; at least one file with hunks (I1).
  2. ``scope``     — diff stays inside its allowed blast radius: file allow/deny lists (never touch
                     canonical artifacts) + max files / hunks / changed-lines. Bound the diff *by
                     construction* and reject over-edits even when tests pass (I5).
  3. ``reproduce`` — the RED bug-reproduction test FAILS without the patch and PASSES with it (I4, I1).
  4. ``regress``   — the existing suite still PASSES with the patch (I1).
  5. ``ci``        — an optional final command (lint / CI) passes (I1).

**Principle (I3): the deterministic ladder produces the verdict.** An LLM may only *rank* candidates
that already pass this ladder and raise abstain / needs-human — it can never override a deterministic
``fail`` nor resurrect a failed candidate. ``select_patch`` encodes exactly that.

The structural rungs (parse, scope) are pure and fully unit-testable. The execution rungs (3-5) are
delegated to an injectable ``runner`` so the core stays pure; ``shell_runner`` is the real subprocess
adapter (mirrors ``behaviour_replay.shell_runner``). Verdicts:
  - ``fail``        — a rung failed (``stopped_at`` names it).
  - ``pass``        — parse + scope + reproduce + regress all *ran* and passed (ci optional).
  - ``needs_human`` — nothing failed, but a required rung was skipped (no scope bound, or the
                      execution rungs could not run) → deterministic verification is incomplete.
"""

import shlex
import subprocess  # nosec B404 — used only with explicit argv lists, never shell=True
import sys
from collections.abc import Callable, Iterator
from fnmatch import fnmatch
from pathlib import Path
from typing import NamedTuple


class FilePatch(NamedTuple):
    """One file's contribution to a diff."""

    path: str
    added: int
    removed: int
    hunks: int


class RunResult(NamedTuple):
    """Outcome of one execution rung from a ``runner``."""

    ok: bool
    detail: str = ""


# runner(phase) -> RunResult, phase in {"reproduce", "regress", "ci"}.
Runner = Callable[[str], RunResult]

_RUNG_ORDER = ("parse", "scope", "reproduce", "regress", "ci")
# A full ``pass`` needs each of these to have *run* and passed. ``ci`` stays optional.
_REQUIRED_FOR_PASS = ("parse", "scope", "reproduce", "regress")


def _strip_ab(p: str) -> str:
    """Drop a leading ``a/`` or ``b/`` git diff prefix; leave ``/dev/null`` and bare paths alone."""
    p = p.strip()
    for pre in ("a/", "b/"):
        if p.startswith(pre):
            return p[len(pre) :]
    return p


def _classify(line: str, next_line: str | None) -> str:
    """Classify one diff line by the event it begins. ``next_line`` enables one-token lookahead.

    Kinds:
      - ``git_header``  — a ``diff --git`` line (starts a new file).
      - ``file_header`` — an adjacent ``--- ``/``+++ `` pair (this line is the ``--- ``, the next is
        the ``+++ ``). The pair is one event, consumed together. Adjacency is what disambiguates a
        real header from a removed *content* line that merely starts with ``--- ``.
      - ``hunk``        — a ``@@`` hunk header.
      - ``added`` / ``removed`` — a content line inside a hunk (``+``/``-``), explicitly excluding
        ``+++``/``---`` so header-marker tokens are never miscounted as content.
      - ``other``       — context lines, indices, blank lines, anything else.
    """
    if line.startswith("diff --git"):
        return "git_header"
    if line.startswith("--- ") and next_line is not None and next_line.startswith("+++ "):
        return "file_header"
    if line.startswith("@@"):
        return "hunk"
    if line.startswith("+") and not line.startswith("+++"):
        return "added"
    if line.startswith("-") and not line.startswith("---"):
        return "removed"
    return "other"


def _events(lines: list[str]) -> Iterator[tuple[str, str, str | None]]:
    """Walk ``lines`` and yield one ``(kind, raw, nxt)`` event per diff event.

    The single source of index motion for the parser: each iteration classifies the current line via
    ``_classify`` (with one-token lookahead) and advances. A ``file_header`` is the only multi-line
    event — its adjacent ``+++ `` line is carried in ``nxt`` and consumed here, so it is never
    re-emitted as a separate event. Every other kind advances one line. ``nxt`` is the lookahead line
    (``None`` at end of input).
    """
    n = len(lines)
    i = 0
    while i < n:
        raw = lines[i]
        nxt = lines[i + 1] if i + 1 < n else None
        kind = _classify(raw, nxt)
        yield kind, raw, nxt
        # A file_header consumes its adjacent '+++ ' line (two lines, one event); all else, one line.
        i += 2 if kind == "file_header" else 1


def parse_unified_diff(diff_text: str) -> list[FilePatch]:
    """Parse a unified diff into per-file add/remove/hunk counts. Raise ``ValueError`` if malformed.

    Handles ``git diff`` (``diff --git`` + ``a/``/``b/`` prefixes), plain ``diff -u``, file creation
    (``--- /dev/null``) and deletion (``+++ /dev/null``). A ``--- ``/``+++ `` pair is treated as a file
    header only when they are adjacent — so a removed *content* line that happens to start with
    ``--- `` inside a hunk is not mistaken for a header.

    Implemented as a single pass over ``(kind, raw, nxt)`` events from ``_events`` (which owns all
    index motion), with one pure handler per kind. A ``file_header`` event already has its adjacent
    ``+++ `` line consumed by the generator, so each branch here is index-free.
    """
    if not diff_text or not diff_text.strip():
        raise ValueError("empty diff")

    files: list[dict] = []
    cur: dict | None = None
    saw_hunk = False

    def _new(path: str) -> dict:
        return {"path": path, "added": 0, "removed": 0, "hunks": 0}

    def _flush() -> None:
        nonlocal cur
        if cur is not None:
            files.append(cur)
            cur = None

    for kind, raw, nxt in _events(diff_text.splitlines()):
        if kind == "git_header":
            _flush()
            parts = raw.split()
            cur = _new(_strip_ab(parts[-1]) if len(parts) >= 3 else "")
        elif kind == "file_header":
            # nxt is the adjacent '+++ ' line (consumed by _events; not re-emitted).
            old = _strip_ab(raw[4:])
            new = _strip_ab(nxt[4:])  # type: ignore[index]  # guaranteed non-None by _classify
            path = new if new != "/dev/null" else old
            if cur is None or cur["hunks"] > 0:
                _flush()
                cur = _new(path)
            else:
                cur["path"] = path or cur["path"]
        elif kind == "hunk":
            if cur is None:
                raise ValueError("hunk header before any file header")
            cur["hunks"] += 1
            saw_hunk = True
        elif kind in ("added", "removed") and cur is not None and cur["hunks"] > 0:
            cur["added" if kind == "added" else "removed"] += 1
    _flush()

    fps = [FilePatch(f["path"], f["added"], f["removed"], f["hunks"]) for f in files if f["hunks"]]
    if not saw_hunk or not fps:
        raise ValueError("no hunks found in diff")
    if any(not f.path for f in fps):
        raise ValueError("a file patch has hunks but no resolvable path")
    return fps


def _path_matches(path: str, pattern: str) -> bool:
    """True if ``path`` matches ``pattern`` under any of three semantics (OR-combined).

    This is the security-relevant predicate behind the deny/allow scope rung, so its three
    semantics are spelled out and pinned by tests:

      1. **exact** — ``path == pattern`` (e.g. ``"src/calc.py"`` matches ``"src/calc.py"``).
      2. **directory prefix** — ``path`` lives under the directory named by ``pattern``: the
         pattern's trailing ``/`` is normalized, then a ``"<pattern>/"`` prefix is required, so
         ``"subagents/"`` matches ``"subagents/foo/profile.yaml"`` but not ``"subagents-x/y"``.
      3. **fnmatch glob** — shell-style wildcards (e.g. ``"src/*.py"`` matches ``"src/calc.py"``).

    A match under *any* semantic returns True; deny wins (a denied path is rejected even if it
    would also satisfy an allow pattern).
    """
    pre = pattern.rstrip("/") + "/"
    return path == pattern or path.startswith(pre) or fnmatch(path, pattern)


def check_scope(files: list[FilePatch], scope: dict) -> tuple[bool, str]:
    """Enforce the diff's blast radius (I5). Returns ``(ok, detail)``.

    ``scope`` keys (all optional): ``allow_paths`` (every changed file must match one),
    ``deny_paths`` (no changed file may match any — e.g. canonical artifacts), ``max_files``,
    ``max_hunks``, ``max_changed_lines``.
    """
    paths = [f.path for f in files]
    n_files = len(paths)
    n_hunks = sum(f.hunks for f in files)
    changed = sum(f.added + f.removed for f in files)

    deny = scope.get("deny_paths") or []
    for p in paths:
        hit = next((d for d in deny if _path_matches(p, d)), None)
        if hit is not None:
            return False, f"path '{p}' matches denied scope '{hit}' (canonical/out-of-bounds edit)"

    allow = scope.get("allow_paths")
    if allow:
        for p in paths:
            if not any(_path_matches(p, a) for a in allow):
                return False, f"path '{p}' is outside allow_paths {allow}"

    for key, val, label in (
        ("max_files", n_files, "files"),
        ("max_hunks", n_hunks, "hunks"),
        ("max_changed_lines", changed, "changed lines"),
    ):
        cap = scope.get(key)
        if cap is not None and val > cap:
            return False, f"{label} {val} exceeds {key}={cap} (over-edit)"

    return True, f"{n_files} file(s), {n_hunks} hunk(s), {changed} changed line(s) within bounds"


def _rec(rung: str, status: str, detail: str) -> dict:
    return {"rung": rung, "status": status, "detail": detail}


def _verdict(records: list[dict], stopped_at: str | None, metrics: dict) -> dict:
    """Fold the recorded rung statuses into the final verdict dict.

    A single ``fail`` → ``fail``; every ``_REQUIRED_FOR_PASS`` rung ``pass`` → ``pass``; otherwise
    (a required rung was skipped) → ``needs_human``.
    """
    status = {r["rung"]: r["status"] for r in records}
    if any(v == "fail" for v in status.values()):
        verdict = "fail"
    elif all(status.get(r) == "pass" for r in _REQUIRED_FOR_PASS):
        verdict = "pass"
    else:
        verdict = "needs_human"
    return {"verdict": verdict, "stopped_at": stopped_at, "rungs": records, "metrics": metrics}


def _scope_rung(files: list[FilePatch], scope: dict | None) -> dict:
    """Produce the ``scope`` rung record (I5). Omitted scope → ``skip`` (→ ``needs_human``)."""
    if scope is None:
        return _rec("scope", "skip", "no scope bound configured — bound the diff to allow pass")
    ok, detail = check_scope(files, scope)
    return _rec("scope", "pass" if ok else "fail", detail)


def _execution_rung(phase: str, runner: Runner | None, request: tuple[str, ...]) -> dict:
    """Produce one execution-rung record (``reproduce``/``regress``/``ci``).

    Not requested or no runner → ``skip``. A runner exception is caught and reported as ``fail`` so a
    flaky harness surfaces as a rung failure, not a crash.
    """
    if phase not in request:
        return _rec(phase, "skip", "not requested")
    if runner is None:
        return _rec(phase, "skip", "no runner provided")
    try:
        res = runner(phase)
    except Exception as e:  # a flaky harness must surface as a rung failure, not a crash
        return _rec(phase, "fail", f"runner error: {e}")
    return _rec(phase, "pass" if res.ok else "fail", res.detail)


def validate_patch(
    diff_text: str,
    *,
    scope: dict | None = None,
    runner: Runner | None = None,
    request: tuple[str, ...] = ("reproduce", "regress", "ci"),
) -> dict:
    """Run the deterministic validation ladder over one unified diff. Returns a verdict dict.

    ``scope`` bounds the diff (skipped, → ``needs_human``, when omitted). ``runner`` runs the
    execution rungs named in ``request``; without it those rungs are skipped (→ ``needs_human``).
    Short-circuits at the first failing rung (``stopped_at``). See the module docstring for verdicts.

    The ladder is a list of ``(name, step)`` rungs iterated once through one short-circuiting loop:
    each ``step`` returns a record dict; the first ``fail`` stops the ladder and names ``stopped_at``.
    The ``parse`` rung runs first (outside the loop) because it produces the ``files``/``metrics`` the
    later rungs consume and short-circuits on a malformed diff.
    """
    records: list[dict] = []
    metrics: dict = {}

    try:
        files = parse_unified_diff(diff_text)
    except ValueError as e:
        records.append(_rec("parse", "fail", str(e)))
        return _verdict(records, "parse", metrics)
    metrics = {
        "files": [f.path for f in files],
        "n_files": len(files),
        "n_hunks": sum(f.hunks for f in files),
        "changed_lines": sum(f.added + f.removed for f in files),
    }
    records.append(
        _rec("parse", "pass", f"{metrics['n_files']} file(s), {metrics['n_hunks']} hunk(s)")
    )

    # Remaining rungs as uniform record-producing steps; one loop, short-circuit on first fail.
    rungs: list[tuple[str, Callable[[], dict]]] = [
        ("scope", lambda: _scope_rung(files, scope)),
        ("reproduce", lambda: _execution_rung("reproduce", runner, request)),
        ("regress", lambda: _execution_rung("regress", runner, request)),
        ("ci", lambda: _execution_rung("ci", runner, request)),
    ]
    for name, step in rungs:
        record = step()
        records.append(record)
        if record["status"] == "fail":
            return _verdict(records, name, metrics)

    return _verdict(records, None, metrics)


def select_patch(
    candidates: list[str],
    *,
    scope: dict | None = None,
    runner_for: Callable[[int], Runner] | None = None,
    ranker: Callable[[list[int]], int] | None = None,
    request: tuple[str, ...] = ("reproduce", "regress"),
) -> dict:
    """Pick the patch to suggest from several candidates — deterministic gate first, LLM rank last (I3).

    Validates every candidate, keeps only those with verdict ``pass``, then lets ``ranker`` *order*
    the passing ones. The ranker receives the list of passing candidate indices and returns the chosen
    index; a return value outside that set is ignored (falls back to the first passing candidate). So a
    hallucinating or adversarial ranker can never select a candidate the deterministic ladder rejected.

    ``runner_for(i)`` builds the execution runner for candidate ``i`` (None → execution rungs skip, so
    those candidates land in ``needs_human`` rather than ``pass``). Returns ``selected`` (candidate
    index or None), ``passing``, ``needs_human``, ``verdict_per``, and a ``reason``.
    """
    results = [
        validate_patch(
            diff,
            scope=scope,
            runner=(runner_for(i) if runner_for else None),
            request=request,
        )
        for i, diff in enumerate(candidates)
    ]
    verdict_per = [r["verdict"] for r in results]
    passing = [i for i, v in enumerate(verdict_per) if v == "pass"]
    needs_human = any(v == "needs_human" for v in verdict_per)

    if not passing:
        return {
            "selected": None,
            "passing": [],
            "needs_human": needs_human,
            "verdict_per": verdict_per,
            "reason": "no candidate passed the deterministic ladder",
        }

    chosen = passing[0]
    reason = "first passing candidate"
    if ranker is not None:
        try:
            pick = ranker(list(passing))
        except Exception:
            pick = None
        if pick in passing:
            chosen, reason = pick, "ranked among passing candidates"
        else:
            reason = "ranker out of range — fell back to first passing candidate"
    return {
        "selected": chosen,
        "passing": passing,
        "needs_human": needs_human,
        "verdict_per": verdict_per,
        "reason": reason,
    }


def shell_runner(
    repo_root: str | Path,
    *,
    patch_file: str | Path,
    repro_cmd: str | list[str] | None = None,
    regress_cmd: str | list[str] | None = None,
    ci_cmd: str | list[str] | None = None,
    apply_cmd: tuple[str, ...] = ("git", "apply"),
    revert_cmd: tuple[str, ...] = ("git", "apply", "-R"),
    timeout: int = 600,
) -> Runner:
    """Build a real ``runner`` that executes each rung against ``repo_root`` via subprocess.

    Each phase is hermetic: ``reproduce`` runs the RED test at baseline (must fail), applies the patch,
    re-runs it (must pass), then reverts; ``regress``/``ci`` apply the patch, run their command, then
    revert. So a clean tree is restored after every rung regardless of outcome. Commands may be a
    string (``shlex``-split) or an argv list — never run through a shell. Tests inject a fake runner.
    """
    repo = str(repo_root)
    cmds: dict[str, str | list[str] | None] = {
        "reproduce": repro_cmd,
        "regress": regress_cmd,
        "ci": ci_cmd,
    }

    def _sh(cmd: str | list[str]) -> tuple[int, str]:
        argv = shlex.split(cmd) if isinstance(cmd, str) else list(cmd)
        p = subprocess.run(  # nosec B603 — explicit argv, no shell
            argv, cwd=repo, text=True, capture_output=True, timeout=timeout
        )
        return p.returncode, (p.stdout + p.stderr)[-2000:]

    def _patch(revert: bool = False) -> bool:
        base = list(revert_cmd if revert else apply_cmd)
        rc, _ = _sh(base + [str(patch_file)])
        return rc == 0

    def _run(phase: str) -> RunResult:
        cmd = cmds.get(phase)
        if not cmd:
            return RunResult(False, f"{phase}: no command configured")
        if phase == "reproduce":
            rc0, _ = _sh(cmd)
            if rc0 == 0:
                return RunResult(False, "RED test passed pre-patch — bug not reproduced")
        if not _patch():
            return RunResult(False, "patch did not apply cleanly")
        try:
            rc, out = _sh(cmd)
        finally:
            _patch(revert=True)
        if rc == 0:
            return RunResult(True, f"{phase} passed on patched tree")
        return RunResult(False, f"{phase} failed on patched tree: {out}")

    return _run


def main() -> None:
    import argparse
    import json

    ap = argparse.ArgumentParser(
        description="Deterministic patch-validation ladder (Step-6 I-track)."
    )
    ap.add_argument("patch", help="path to the unified-diff patch file")
    ap.add_argument("--repo", default=".", help="repo root the patch applies to (default: cwd)")
    ap.add_argument("--scope", help="path to a JSON file with the scope bound")
    ap.add_argument("--repro-cmd", help="RED bug-reproduction test command")
    ap.add_argument("--regress-cmd", help="regression suite command")
    ap.add_argument("--ci-cmd", help="optional final CI/lint command")
    args = ap.parse_args()

    diff = Path(args.patch).read_text(encoding="utf-8")
    scope = json.loads(Path(args.scope).read_text(encoding="utf-8")) if args.scope else None
    request = tuple(
        p
        for p, c in (
            ("reproduce", args.repro_cmd),
            ("regress", args.regress_cmd),
            ("ci", args.ci_cmd),
        )
        if c
    )
    runner = None
    if request:
        runner = shell_runner(
            args.repo,
            patch_file=args.patch,
            repro_cmd=args.repro_cmd,
            regress_cmd=args.regress_cmd,
            ci_cmd=args.ci_cmd,
        )
    result = validate_patch(
        diff, scope=scope, runner=runner, request=request or ("reproduce", "regress", "ci")
    )
    print(json.dumps(result, indent=2))
    sys.exit({"pass": 0, "fail": 1, "needs_human": 2}[result["verdict"]])


if __name__ == "__main__":
    main()
