"""Full-coverage tests for the cap-resilient cross-engine MAP orchestrator.

The engine runner, clock, and sleeper are all injected, so every failover path is exercised
deterministically without spending a token or sleeping a real second. A `FakeRunner` simulates the
four things an engine attempt can do to a module dir: finish (write principles.yaml + module.json),
make progress (add a partial), hit a cap (nothing + cap signal), or error (nothing + no cap signal).
"""

from __future__ import annotations

import json

import pytest

from tools.subagent_factory import map_corpus as mc
from tools.subagent_factory.map_corpus import (
    EngineRun,
    EngineState,
    book_sha,
    book_words,
    cap_signal,
    count_partials,
    is_done,
    map_book_cmd,
    module_dir,
    route_engine,
    run_corpus,
)

# --- fakes --------------------------------------------------------------------------------------


class Clock:
    def __init__(self, start: float = 1000.0) -> None:
        self.t = start
        self.sleeps: list[float] = []

    def now(self) -> float:
        return self.t

    def sleep(self, s: float) -> None:
        self.sleeps.append(s)
        self.t += s


class FakeRunner:
    """Programmable engine runner. `behavior(book, engine, mdir, n_prior_calls) -> action|EngineRun`.

    Actions: 'done', 'progress', 'cap', 'error', 'progress+cap'.
    """

    def __init__(self, cache, behavior):
        self.cache = cache
        self.behavior = behavior
        self.calls: list[tuple[str, str]] = []
        self._n: dict[str, int] = {}

    def __call__(self, book, engine) -> EngineRun:
        from pathlib import Path

        mdir = module_dir(self.cache, Path(book))
        n = self._n.get(str(book), 0)
        self._n[str(book)] = n + 1
        self.calls.append((Path(book).stem, engine))
        action = self.behavior(Path(book), engine, mdir, n)
        return self._apply(action, mdir)

    @staticmethod
    def _add_partial(mdir):
        pd = mdir / "partials"
        pd.mkdir(parents=True, exist_ok=True)
        (pd / f"c{len(list(pd.glob('*.jsonl'))):04d}.jsonl").write_text("{}\n", encoding="utf-8")

    def _apply(self, action, mdir) -> EngineRun:
        if isinstance(action, EngineRun):
            return action
        mdir.mkdir(parents=True, exist_ok=True)
        if action == "done":
            (mdir / "principles.yaml").write_text("principles: []\n", encoding="utf-8")
            (mdir / "module.json").write_text("{}", encoding="utf-8")
            return EngineRun(rc=0, capped=False)
        if action == "progress":
            self._add_partial(mdir)
            return EngineRun(rc=0, capped=False)
        if action == "progress+cap":
            self._add_partial(mdir)
            return EngineRun(rc=1, capped=True)
        if action == "cap":
            return EngineRun(rc=1, capped=True)
        if action == "error":
            return EngineRun(rc=2, capped=False)
        raise ValueError(f"unknown action {action!r}")


def mkbook(tmp_path, name: str, words: int = 100):
    # content is the name repeated `words` times: distinct per name (distinct sha/module dir) with an
    # exact word count, so two books never collide on the same content-addressed module.
    p = tmp_path / "src" / f"{name}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(" ".join([name] * words), encoding="utf-8")
    return p


def corpus(books, runner, cache, **kw):
    clock = kw.pop("clock", Clock())
    return (
        run_corpus(
            books,
            cache=cache,
            run_book=runner,
            now_fn=clock.now,
            sleep_fn=clock.sleep,
            log=lambda _m: None,
            **kw,
        ),
        clock,
    )


# --- cap_signal ---------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "Error: rate limit exceeded",
        "rate-limit hit",
        "HTTP 429 Too Many Requests",
        "quota exceeded for this org",
        "usage limit reached",
        "model is overloaded",
        "your limit resets in 3h",
        "insufficient_quota",
        "please try again later",
        "you are out of credits",
    ],
)
def test_cap_signal_true(text):
    assert cap_signal(text)


@pytest.mark.parametrize("text", ["", None, "all good", "wrote principles.yaml (11 claims)"])
def test_cap_signal_false(text):
    assert not cap_signal(text)


# --- filesystem facts ---------------------------------------------------------------------------


def test_book_sha_and_module_dir(tmp_path):
    import hashlib

    b = mkbook(tmp_path, "a")
    assert book_sha(b) == hashlib.sha256(b.read_bytes()).hexdigest()
    assert module_dir(tmp_path / "cache", b) == tmp_path / "cache" / book_sha(b)


def test_is_done_requires_both_files(tmp_path):
    m = tmp_path / "m"
    m.mkdir()
    assert not is_done(m)
    (m / "principles.yaml").write_text("x")
    assert not is_done(m)  # module.json still missing
    (m / "module.json").write_text("{}")
    assert is_done(m)


def test_count_partials(tmp_path):
    m = tmp_path / "m"
    assert count_partials(m) == 0  # no partials dir
    (m / "partials").mkdir(parents=True)
    assert count_partials(m) == 0
    (m / "partials" / "c0.jsonl").write_text("{}")
    (m / "partials" / "c1.jsonl").write_text("{}")
    (m / "partials" / "ignore.txt").write_text("x")  # only *.jsonl count
    assert count_partials(m) == 2


def test_book_words(tmp_path):
    assert book_words(mkbook(tmp_path, "a", words=42)) == 42
    assert book_words(tmp_path / "missing.md") == 0


# --- EngineState --------------------------------------------------------------------------------


def test_state_available_default_and_cooldown():
    s = EngineState()
    assert s.available("claude", now=100.0)  # unknown -> available
    s.mark_capped("claude", now=100.0, cooldown=50.0)
    assert not s.available("claude", now=120.0)
    assert not s.available("claude", now=149.0)
    assert s.available("claude", now=150.0)


def test_state_next_available():
    s = EngineState()
    assert s.next_available(["claude", "copilot"], now=100.0) == 100.0  # all free
    s.mark_capped("claude", now=100.0, cooldown=50.0)
    assert s.next_available(["claude"], now=100.0) == 150.0  # only capped -> its end
    assert s.next_available(["claude", "copilot"], now=100.0) == 100.0  # copilot free -> now
    assert s.next_available([], now=100.0) == 100.0  # no engines -> now


def test_state_load_save_roundtrip(tmp_path):
    s = EngineState()
    s.mark_capped("codex", now=0.0, cooldown=10.0)
    path = tmp_path / "state.json"
    s.save(path)
    assert json.loads(path.read_text()) == {"codex": 10.0}
    assert EngineState.load(path).capped_until == {"codex": 10.0}


def test_state_load_missing_and_corrupt(tmp_path):
    assert EngineState.load(tmp_path / "nope.json").capped_until == {}
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert EngineState.load(bad).capped_until == {}
    notobj = tmp_path / "notobj.json"
    notobj.write_text("[1, 2]")  # valid json, wrong shape
    assert EngineState.load(notobj).capped_until == {}


# --- route_engine -------------------------------------------------------------------------------


def test_route_size_preferences():
    big, mid, small = mc.LARGE_WORDS + 1, (mc.SMALL_WORDS + mc.LARGE_WORDS) // 2, mc.SMALL_WORDS - 1
    all3 = ["claude", "copilot", "codex"]
    assert route_engine(big, all3) == "claude"
    assert route_engine(small, all3) == "codex"
    assert route_engine(mid, all3) == "copilot"


def test_route_degrades_when_preferred_unavailable():
    big = mc.LARGE_WORDS + 1
    assert route_engine(big, ["copilot", "codex"]) == "copilot"  # claude gone
    assert route_engine(big, ["codex"]) == "codex"  # last resort
    small = mc.SMALL_WORDS - 1
    assert route_engine(small, ["claude"]) == "claude"  # codex+copilot gone


def test_route_none_when_empty():
    assert route_engine(100, []) is None


def test_route_unlisted_engine_falls_through():
    # an engine not in the preference order is still returned if it is the only one available
    assert route_engine(mc.LARGE_WORDS + 1, ["mystery"]) == "mystery"


# --- run_corpus: core scenarios -----------------------------------------------------------------


def test_all_books_already_done(tmp_path):
    b = mkbook(tmp_path, "a")
    m = module_dir(tmp_path / "cache", b)
    m.mkdir(parents=True)
    (m / "principles.yaml").write_text("x")
    (m / "module.json").write_text("{}")
    runner = FakeRunner(tmp_path / "cache", lambda *a: pytest.fail("must not run"))
    res, _ = corpus([b], runner, tmp_path / "cache")
    assert res.ok and res.done == [str(b)] and runner.calls == []


def test_single_engine_success_first_try(tmp_path):
    b = mkbook(tmp_path, "a")
    runner = FakeRunner(tmp_path / "cache", lambda *_a: "done")
    res, _ = corpus([b], runner, tmp_path / "cache")
    assert res.ok and res.done == [str(b)]
    assert len(runner.calls) == 1


def test_cap_then_failover_succeeds(tmp_path):
    b = mkbook(tmp_path, "a", words=mc.LARGE_WORDS + 1)  # big -> claude first

    def behave(book, engine, mdir, n):
        return "cap" if engine == "claude" else "done"

    runner = FakeRunner(tmp_path / "cache", behave)
    state = EngineState()
    res, _ = corpus([b], runner, tmp_path / "cache", state=state)
    assert res.ok
    # claude tried first (capped, zero progress) then failed over to copilot which finished.
    assert runner.calls[0] == ("a", "claude")
    assert runner.calls[1][1] == "copilot"
    assert not state.available("claude", now=1000.0)  # claude is cooling down
    assert state.available("copilot", now=1000.0)


def test_progress_then_cap_continues_from_partials(tmp_path):
    b = mkbook(tmp_path, "a", words=mc.LARGE_WORDS + 1)

    def behave(book, engine, mdir, n):
        if engine == "claude":
            return "progress+cap"  # extracts one chunk, then caps
        return "done"  # copilot finishes from the partial

    runner = FakeRunner(tmp_path / "cache", behave)
    state = EngineState()
    res, _ = corpus([b], runner, tmp_path / "cache", state=state)
    assert res.ok
    assert runner.calls[0] == ("a", "claude")  # made a partial before capping
    assert not state.available("claude", now=1000.0)
    assert count_partials(module_dir(tmp_path / "cache", b)) >= 1


def test_all_capped_sleeps_then_succeeds(tmp_path):
    b = mkbook(tmp_path, "a")

    # Every engine caps (zero progress) on its first call; after one sleep, the next call succeeds.
    state_calls = {"n": 0}

    def behave(book, engine, mdir, n):
        state_calls["n"] += 1
        return "cap" if state_calls["n"] <= 3 else "done"  # 3 engines cap, then done

    runner = FakeRunner(tmp_path / "cache", behave)
    clock = Clock()
    res, clk = corpus(
        [b],
        runner,
        tmp_path / "cache",
        clock=clock,
        cooldowns={"claude": 100.0, "copilot": 200.0, "codex": 300.0},
    )
    assert res.ok
    # all three capped, then it slept to the SOONEST cooldown (claude, 100s) and retried.
    assert clk.sleeps and clk.sleeps[0] == pytest.approx(100.0)


def test_genuine_error_all_engines_no_cap_fails(tmp_path):
    b = mkbook(tmp_path, "a")
    runner = FakeRunner(tmp_path / "cache", lambda *_a: "error")  # zero progress, no cap, forever
    res, _ = corpus([b], runner, tmp_path / "cache")
    assert not res.ok
    assert "content" in res.failed[str(b)] or "error" in res.failed[str(b)]
    # tried each of the three engines exactly once, then declared a content error.
    assert len(runner.calls) == 3
    assert {e for _b, e in runner.calls} == {"claude", "copilot", "codex"}


def test_resume_skips_done_book_runs_other(tmp_path):
    cache = tmp_path / "cache"
    done_book = mkbook(tmp_path, "done", words=10)
    m = module_dir(cache, done_book)
    m.mkdir(parents=True)
    (m / "principles.yaml").write_text("x")
    (m / "module.json").write_text("{}")
    todo = mkbook(tmp_path, "todo", words=10)

    seen = []

    def behave(book, engine, mdir, n):
        seen.append(book.stem)
        return "done"

    runner = FakeRunner(cache, behave)
    res, _ = corpus([done_book, todo], runner, cache)
    assert res.ok and res.done == [str(done_book), str(todo)]
    assert seen == ["todo"]  # the done book was skipped


def test_max_attempts_safety_caps_runaway(tmp_path):
    b = mkbook(tmp_path, "a")
    # always progresses but never finishes -> would loop forever without the attempt cap
    runner = FakeRunner(tmp_path / "cache", lambda *_a: "progress")
    res, _ = corpus([b], runner, tmp_path / "cache", max_attempts_per_book=5)
    assert not res.ok
    assert "exceeded 5 attempts" in res.failed[str(b)]
    assert len(runner.calls) == 5


def test_max_total_sleep_budget_gives_up(tmp_path):
    b = mkbook(tmp_path, "a")
    runner = FakeRunner(tmp_path / "cache", lambda *_a: "cap")  # always capped, never frees
    res, _ = corpus(
        [b],
        runner,
        tmp_path / "cache",
        cooldowns={"claude": 1000.0, "copilot": 1000.0, "codex": 1000.0},
        max_total_sleep_s=1500.0,
    )
    assert not res.ok
    assert "stayed capped" in res.failed[str(b)]


def test_multi_book_mixed(tmp_path):
    cache = tmp_path / "cache"
    b1, b2 = mkbook(tmp_path, "b1", words=10), mkbook(tmp_path, "b2", words=mc.LARGE_WORDS + 1)

    def behave(book, engine, mdir, n):
        if book.name == "b2" and engine == "claude":
            return "cap"  # b2 caps on claude, fails over
        return "done"

    runner = FakeRunner(cache, behave)
    res, _ = corpus([b1, b2], runner, cache)
    assert res.ok and res.done == [str(b1), str(b2)]


def test_on_state_change_called_on_cap(tmp_path):
    b = mkbook(tmp_path, "a", words=mc.LARGE_WORDS + 1)

    def behave(book, engine, mdir, n):
        return "cap" if engine == "claude" else "done"

    runner = FakeRunner(tmp_path / "cache", behave)
    saved: list[dict] = []
    run_corpus(
        [b],
        cache=tmp_path / "cache",
        run_book=runner,
        now_fn=Clock().now,
        sleep_fn=lambda _s: None,
        on_state_change=lambda s: saved.append(s.to_dict()),
        log=lambda _m: None,
    )
    assert saved and "claude" in saved[-1]


def test_result_ok_property():
    assert mc.CorpusResult(done=["a"]).ok
    assert not mc.CorpusResult(failed={"a": "x"}).ok


def test_progress_resets_error_rotation(tmp_path):
    # error on claude+copilot (zero progress), THEN codex progresses, THEN done. The interleaved
    # progress must reset the "all engines errored" counter so it is not declared a content error.
    b = mkbook(tmp_path, "a", words=mc.LARGE_WORDS + 1)
    script = iter(["error", "error", "progress", "done"])

    def behave(book, engine, mdir, n):
        return next(script)

    runner = FakeRunner(tmp_path / "cache", behave)
    res, _ = corpus([b], runner, tmp_path / "cache")
    assert res.ok
    assert len(runner.calls) == 4


# --- runner construction / CLI ------------------------------------------------------------------


def test_map_book_cmd_shape(tmp_path):
    cmd = map_book_cmd(tmp_path, tmp_path / "b.md", "copilot", 1234)
    assert cmd[0] == "bash" and cmd[1].endswith("campaign/map_book.sh")
    assert "--engine" in cmd and cmd[cmd.index("--engine") + 1] == "copilot"
    assert cmd[cmd.index("--timeout") + 1] == "1234"
    assert "--fg" in cmd and cmd[cmd.index("--max-attempts") + 1] == "1"


def test_make_runner_detects_cap_and_rc(tmp_path, monkeypatch):
    import subprocess

    class P:
        def __init__(self, rc, out, err):
            self.returncode, self.stdout, self.stderr = rc, out, err

    calls = {}

    def fake_run(cmd, **kw):
        calls["cmd"] = cmd
        return P(1, "boom: rate limit exceeded", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    runner = mc.make_map_book_runner(tmp_path, timeout=10)
    out = runner(tmp_path / "b.md", "claude")
    assert out.rc == 1 and out.capped is True
    assert calls["cmd"][0] == "bash"

    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: P(0, "ok 12 claims", ""))
    assert mc.make_map_book_runner(tmp_path)(tmp_path / "b.md", "claude") == EngineRun(0, False)


def test_read_sources(tmp_path):
    f = tmp_path / "s.sources"
    f.write_text("# comment\n\nrel/one.md\n/abs/two.md\n", encoding="utf-8")
    books = mc._read_sources(f, tmp_path / "repo")
    assert books == [tmp_path / "repo" / "rel/one.md", __import__("pathlib").Path("/abs/two.md")]


def test_main_happy_path_done_book(tmp_path, monkeypatch, capsys):
    repo = tmp_path
    (repo / "campaign").mkdir()
    b = mkbook(repo, "a")
    cache = repo / "cache" / "book-extracts"
    m = module_dir(cache, b)
    m.mkdir(parents=True)
    (m / "principles.yaml").write_text("x")
    (m / "module.json").write_text("{}")
    rc = mc.main(["--book", str(b), "--repo", str(repo), "--cache", str(cache)])
    assert rc == 0
    assert "done=1 failed=0" in capsys.readouterr().out


def test_main_with_sources_file(tmp_path, capsys):
    repo = tmp_path
    (repo / "campaign").mkdir()
    b = mkbook(repo, "a")
    cache = repo / "cache" / "book-extracts"
    m = module_dir(cache, b)
    m.mkdir(parents=True)
    (m / "principles.yaml").write_text("x")
    (m / "module.json").write_text("{}")
    src = repo / "books.sources"
    src.write_text(str(b) + "\n", encoding="utf-8")  # absolute path line
    rc = mc.main(["--sources", str(src), "--repo", str(repo), "--cache", str(cache)])
    assert rc == 0
    assert "done=1 failed=0" in capsys.readouterr().out


def test_main_reports_failure(tmp_path, monkeypatch, capsys):
    repo = tmp_path
    (repo / "campaign").mkdir()
    b = mkbook(repo, "a")
    # force the real runner to "error" so the book fails, without shelling out
    monkeypatch.setattr(
        mc, "make_map_book_runner", lambda *a, **k: lambda book, eng: EngineRun(2, False)
    )
    rc = mc.main(["--book", str(b), "--repo", str(repo), "--cache", str(repo / "c")])
    assert rc == 1
    assert "FAIL" in capsys.readouterr().out


def test_main_requires_books(tmp_path):
    with pytest.raises(SystemExit):
        mc.main(["--repo", str(tmp_path)])
