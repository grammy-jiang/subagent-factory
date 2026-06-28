"""Cap-resilient, cross-engine MAP orchestrator for per-book authoring.

`map_books.sh` drains many books but on ONE fixed engine — if that engine hits its usage cap the
whole batch stalls. This orchestrator drives the same per-book `map_book.sh` step but **fails over
across engines** (claude / copilot / codex): when an engine is blocked, the next available engine
resumes the book from its per-chunk partials, so a single pool's cap never blocks generation.

Design notes
------------
* **Resume is engine-agnostic.** `map_book.sh` persists per-chunk partials and reports real success
  by `principles.yaml` (a cap-kill never reads as done). Any engine continues another's partials.
* **The cap signal is progress-delta, not log text.** After a run we compare the partial count: more
  partials → the engine worked (continue); zero new partials → it is blocked (cool it down, rotate).
  A log regex (`cap_signal`) is used only to DISAMBIGUATE a cap (sleep helps) from a genuine content
  error (sleep will not help) and to keep the run from being mislabelled — never as the primary
  failover trigger, so it does not depend on brittle per-engine cap wording.
* **Everything is injected** (engine runner, clock, sleeper, state) so the loop is fully unit-testable
  without spending a token or sleeping a second.
* **Resumable / Ctrl-C safe.** Built on `map_book.sh`'s `.claim` + partials + `principles.yaml`;
  re-running skips done books and continues partial ones. Engine cooldowns persist to JSON.

Generic: pass any package's book list (a `.sources` file or explicit `--book` paths); nothing here
is specific to one subagent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess  # nosec B404 - invokes the in-repo map_book.sh driver with a fixed argv (no shell)
import time
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_ENGINES: tuple[str, ...] = ("claude", "copilot", "codex")
# Cooldown after an engine is found capped, before it is retried (seconds). Tunable per observation.
DEFAULT_COOLDOWNS: dict[str, float] = {
    "claude": 5 * 3600,
    "copilot": 2 * 3600,
    "codex": 5 * 3600,
}
# Size routing (word counts): big -> claude (1M ctx), small -> codex (smallest budget), else copilot.
LARGE_WORDS = 60_000
SMALL_WORDS = 30_000

# Engine-agnostic cap/rate-limit signal. Only disambiguates cap (sleep) from content error (fail);
# never the primary failover trigger (that is the partial-count delta).
_CAP_RE = re.compile(
    r"rate.?limit|quota|usage limit|\b429\b|overloaded|resets? in|too many requests|"
    r"capacity|insufficient_quota|try again later|out of (?:credit|tokens)",
    re.IGNORECASE,
)


def cap_signal(text: str | None) -> bool:
    """True if the engine output looks like a usage-cap / rate-limit refusal."""
    return bool(text) and bool(_CAP_RE.search(text))  # type: ignore[arg-type]


# --- module-dir filesystem facts (mirror map_book.sh's content-addressing) ----------------------


def book_sha(book: Path) -> str:
    return hashlib.sha256(Path(book).read_bytes()).hexdigest()


def module_dir(cache: Path, book: Path) -> Path:
    return Path(cache) / book_sha(book)


def is_done(mdir: Path) -> bool:
    """map_book.sh's real-success contract: principles.yaml AND module.json both present."""
    return (mdir / "principles.yaml").is_file() and (mdir / "module.json").is_file()


def count_partials(mdir: Path) -> int:
    """Per-chunk progress: number of written partials (the resume granularity)."""
    p = mdir / "partials"
    return sum(1 for _ in p.glob("*.jsonl")) if p.is_dir() else 0


def book_words(book: Path) -> int:
    try:
        return len(Path(book).read_text(encoding="utf-8", errors="replace").split())
    except OSError:
        return 0


# --- engine cooldown state ----------------------------------------------------------------------


@dataclass
class EngineState:
    """Per-engine cooldown: an engine is unavailable until `capped_until[engine]`."""

    capped_until: dict[str, float] = field(default_factory=dict)

    def available(self, engine: str, now: float) -> bool:
        return now >= self.capped_until.get(engine, 0.0)

    def mark_capped(self, engine: str, now: float, cooldown: float) -> None:
        self.capped_until[engine] = now + cooldown

    def next_available(self, engines: Iterable[str], now: float) -> float:
        """Earliest time some engine is usable: `now` if any already is, else the soonest cooldown end."""
        times = [self.capped_until.get(e, 0.0) for e in engines]
        if not times or any(t <= now for t in times):
            return now
        return min(times)

    def to_dict(self) -> dict[str, float]:
        return dict(self.capped_until)

    @classmethod
    def load(cls, path: Path) -> EngineState:
        p = Path(path)
        if p.is_file():
            try:
                return cls(capped_until=dict(json.loads(p.read_text(encoding="utf-8"))))
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                return cls()
        return cls()

    def save(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")


# --- engine routing -----------------------------------------------------------------------------


def route_engine(words: int, available: Sequence[str]) -> str | None:
    """Pick the best AVAILABLE engine for a book of `words`. None iff nothing is available.

    Preference is a soft size routing — big books favour claude (largest context), small books favour
    codex (smallest budget, cheap on a small book), mid books favour copilot — but it always degrades
    to whatever is available rather than stalling, so a capped first choice still makes progress.
    """
    if not available:
        return None
    if words >= LARGE_WORDS:
        order = ("claude", "copilot", "codex")
    elif words <= SMALL_WORDS:
        order = ("codex", "copilot", "claude")
    else:
        order = ("copilot", "claude", "codex")
    for e in order:
        if e in available:
            return e
    return available[0]


# --- the engine runner (injected; real impl shells out to map_book.sh) --------------------------


@dataclass
class EngineRun:
    """Result of one engine attempt. `capped` = a cap signal was seen in this run's output."""

    rc: int
    capped: bool


RunBook = Callable[[Path, str], EngineRun]


def map_book_cmd(repo: Path, book: Path, engine: str, timeout: int) -> list[str]:
    """The argv for one book's MAP on one engine (pure — unit-tested)."""
    return [
        "bash",
        str(Path(repo) / "campaign" / "map_book.sh"),
        "--book",
        str(book),
        "--engine",
        engine,
        "--timeout",
        str(timeout),
        "--max-attempts",
        "1",
        "--fg",
    ]


def make_map_book_runner(
    repo: Path, *, timeout: int = 7200, env: dict[str, str] | None = None
) -> RunBook:
    """Real runner: invoke map_book.sh once and detect a cap signal in its output."""

    def run(book: Path, engine: str) -> EngineRun:
        proc = subprocess.run(  # nosec B603 - fixed argv (map_book_cmd), no shell, trusted inputs
            map_book_cmd(repo, book, engine, timeout),
            cwd=str(repo),
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        return EngineRun(
            rc=proc.returncode, capped=cap_signal(proc.stdout) or cap_signal(proc.stderr)
        )

    return run


# --- the orchestrator ---------------------------------------------------------------------------


@dataclass
class CorpusResult:
    done: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.failed


def run_corpus(
    books: Sequence[str | Path],
    *,
    cache: str | Path,
    run_book: RunBook,
    engines: Sequence[str] = DEFAULT_ENGINES,
    cooldowns: dict[str, float] | None = None,
    state: EngineState | None = None,
    now_fn: Callable[[], float] = time.time,
    sleep_fn: Callable[[float], None] = time.sleep,
    max_attempts_per_book: int = 50,
    max_total_sleep_s: float = 24 * 3600,
    on_state_change: Callable[[EngineState], None] | None = None,
    log: Callable[[str], None] = print,
) -> CorpusResult:
    """Drain `books` to completion, failing over across `engines` on cap. Returns done/failed.

    Sequential (one engine job at a time). For each not-yet-done book it picks an available engine
    (cooldown- and size-aware), runs one MAP attempt, then classifies by partial-count delta:
    done -> next book; progressed -> keep going; zero progress + cap signal -> cool the engine down
    and rotate; zero progress + no cap on every engine since the last progress -> a genuine content
    error (fail fast, do not loop). When all engines are cooling down it sleeps to the soonest wake.
    """
    cooldowns = {**DEFAULT_COOLDOWNS, **(cooldowns or {})}
    state = state or EngineState()
    cache = Path(cache)
    engines = tuple(engines)
    result = CorpusResult()

    def _save() -> None:
        if on_state_change:
            on_state_change(state)

    for raw in books:
        book = Path(raw)
        mdir = module_dir(cache, book)
        if is_done(mdir):
            result.done.append(str(book))
            continue
        words = book_words(book)
        attempts = 0
        zero_progress_engines: set[str] = set()
        slept = 0.0
        failure: str | None = None

        while not is_done(mdir):
            avail = [e for e in engines if state.available(e, now_fn())]
            # Prefer engines that have NOT already errored on this book (zero progress, no cap) since
            # the last progress, so an error rotates to a different pool instead of re-picking the
            # same one; fall back to the full available set once every engine has been tried.
            fresh = [e for e in avail if e not in zero_progress_engines]
            eng = route_engine(words, fresh or avail)
            if eng is None:  # every engine is cooling down — wait for the soonest to free up
                delay = max(0.0, state.next_available(engines, now_fn()) - now_fn())
                if slept + delay > max_total_sleep_s:
                    failure = f"engines stayed capped beyond {max_total_sleep_s:.0f}s budget"
                    break
                log(f"[corpus] {book.name}: all engines cooling down; sleep {delay:.0f}s")
                sleep_fn(delay)
                slept += delay
                continue

            if attempts >= max_attempts_per_book:
                failure = f"exceeded {max_attempts_per_book} attempts"
                break

            p0 = count_partials(mdir)
            attempts += 1
            log(f"[corpus] {book.name} -> {eng} (attempt {attempts}, partials={p0})")
            run = run_book(book, eng)

            if is_done(mdir):
                break
            if count_partials(mdir) > p0:  # made progress — keep draining this book
                zero_progress_engines.clear()
                if run.capped:
                    state.mark_capped(eng, now_fn(), cooldowns[eng])
                    _save()
                continue
            # zero progress this attempt
            if run.capped:
                state.mark_capped(eng, now_fn(), cooldowns[eng])
                _save()
                zero_progress_engines.clear()  # a cap is not a content error
                continue
            # zero progress AND no cap signal -> this engine errored on the book
            zero_progress_engines.add(eng)
            if zero_progress_engines.issuperset(engines):
                failure = "every engine made zero progress with no cap signal — likely a content/schema error"
                break

        if is_done(mdir):
            result.done.append(str(book))
        else:
            result.failed[str(book)] = failure or "incomplete"

    return result


# --- CLI ----------------------------------------------------------------------------------------


def _read_sources(path: Path, repo: Path) -> list[Path]:
    books: list[Path] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        books.append(Path(line) if line.startswith("/") else repo / line)
    return books


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Cap-resilient cross-engine MAP orchestrator.")
    ap.add_argument("--sources", type=Path, help="newline file of book markdown paths")
    ap.add_argument("--book", action="append", default=[], type=Path, help="explicit book path(s)")
    ap.add_argument("--cache", type=Path, default=Path("cache/book-extracts"))
    ap.add_argument(
        "--engines", default=",".join(DEFAULT_ENGINES), help="comma list, in preference"
    )
    ap.add_argument("--state", type=Path, default=Path("campaign/.engine-state.json"))
    ap.add_argument("--timeout", type=int, default=7200)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    args = ap.parse_args(argv)

    repo = args.repo.resolve()
    books: list[Path] = list(args.book)
    if args.sources:
        books += _read_sources(args.sources, repo)
    if not books:
        ap.error("no books (use --sources or --book)")

    engines = tuple(e.strip() for e in args.engines.split(",") if e.strip())
    state = EngineState.load(args.state)
    runner = make_map_book_runner(repo, timeout=args.timeout)
    result = run_corpus(
        books,
        cache=args.cache if args.cache.is_absolute() else repo / args.cache,
        run_book=runner,
        engines=engines,
        state=state,
        on_state_change=lambda s: s.save(args.state),
    )
    print(f"[corpus] done={len(result.done)} failed={len(result.failed)}")
    for b, why in result.failed.items():
        print(f"  FAIL {Path(b).name}: {why}")
    return 0 if result.ok else 1


if __name__ == "__main__":  # pragma: no cover - script entry, exercised via main() in tests
    raise SystemExit(main())
