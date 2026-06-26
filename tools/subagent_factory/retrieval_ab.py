"""Step-14 G1 — local in-prompt-vs-retrieval A/B (closes the distill-vs-retrieve gap per package).

The G1 academic gap — *no paper compares an agent's own distilled principle store vs runtime
retrieval* — cannot be closed by more reading, but it **can** be closed *locally* for one package: run
that package's behaviour-test suite under two conditions and compare the mean score.

- **DISTILLED** (baseline): the current adapter (distilled principles as the system prompt) answers —
  exactly what ``behaviour_replay.replay_suite`` already does.
- **RETRIEVAL**: at query time, deterministically retrieve the top-k source passages — the package's
  **full source** (``sources/markdown/*.md``, paragraph-segmented) — most relevant to the prompt and
  prepend them as grounded context, then answer. The corpus is the *whole* source (not the distilled
  anchor spans, which are ~what distillation already kept → biased toward "suffices"), so retrieval can
  surface long-tail content the adapter dropped — the fair test.

Retrieval is **deterministic — NO LLM** (the factory determinism boundary): BM25-lite lexical scoring
over the source passages, with the same tokenizer family as the rest of the factory.

Pure core (injected ``runner``/``grader`` → unit-tested with fakes); the CLI wires the live shell
runner over a real package. The output is a **measurement, not a gate**: a positive ``delta`` says
retrieval helps *this* package; a flat/negative delta is the (valuable, design-affirming) finding that
in-prompt distillation already suffices — don't build the Step-14 retrieval engine for it.

CLI:
    python -m tools.subagent_factory.retrieval_ab subagents/<slug> --runner <answer.sh> [-k 5]
        [--grader coarse|llm --judge <judge.sh> --judge-samples N]
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from tools.subagent_factory.behaviour_replay import (
    Grader,
    Runner,
    grade_output,
    load_behaviour_tests,
    make_llm_grader,
    replay_suite,
    shell_llm,
    shell_runner,
)
from tools.subagent_factory.claim_recall import _STOPWORDS

_WORD = re.compile(r"[a-z][a-z0-9]+")
# Anchor texts that carry no retrievable content (chunk_source emits "(preamble)" for the pre-heading
# span); skip them so they can't crowd a top-k slot.
_TRIVIAL_TEXT = frozenset({"", "(preamble)"})


@dataclass(frozen=True)
class Passage:
    """One retrievable source passage (a source paragraph, or an anchor span in fallback mode), keyed
    by a citable id (``<sid>#<n>`` for source paragraphs, ``anchor_id`` for anchors)."""

    id: str
    text: str


def _tokens(text: str) -> list[str]:
    """Content tokens **with** repeats (BM25 needs term frequencies). Same regex + stopword filter as
    ``claim_recall._content_tokens``, which returns a *set* — kept consistent, duplicates retained."""
    return [t for t in _WORD.findall(str(text).lower()) if len(t) > 2 and t not in _STOPWORDS]


def load_passages(
    subagent_dir: str | Path, *, min_tokens: int = 4, max_passage_chars: int = 2000
) -> tuple[list[Passage], str]:
    """Build the retrieval corpus from the package's **full source** (``sources/markdown/*.md``,
    paragraph-segmented) — the fair distill-vs-retrieve test: retrieval must be able to surface
    long-tail content the adapter dropped, so the corpus is the whole source, not the sparse distilled
    anchor spans. Falls back to the citable anchor spans only if no source markdown is present.
    Paragraphs below ``min_tokens`` (headings, list stubs) are dropped; each is capped at
    ``max_passage_chars``.

    Returns ``(passages, source_kind)`` where ``source_kind`` is the corpus actually used —
    ``"markdown"`` (the fair full-source corpus), ``"anchors"`` (the distilled-span fallback), or
    ``"none"`` (no corpus found). Callers report this so a silent degrade to the anchor fallback is
    visible and an empty-corpus message names the right candidate dirs."""
    base = Path(subagent_dir)
    md_dir = base / "sources" / "markdown"
    if md_dir.is_dir():
        passages = _passages_from_markdown(md_dir, min_tokens, max_passage_chars)
        if passages:
            return passages, "markdown"
    anchors = _passages_from_anchors(base / "sources" / "anchors", min_tokens)
    return (anchors, "anchors") if anchors else ([], "none")


def _passages_from_markdown(md_dir: Path, min_tokens: int, max_chars: int) -> list[Passage]:
    out: list[Passage] = []
    for f in sorted(md_dir.glob("*.md")):
        sid = f.stem
        text = f.read_text(encoding="utf-8", errors="replace")
        for i, para in enumerate(re.split(r"\n\s*\n", text)):
            p = para.strip()
            if not p or len(_tokens(p)) < min_tokens:
                continue
            out.append(Passage(f"{sid}#{i}", p[:max_chars]))
    return out


def _passages_from_anchors(anchors_dir: Path, min_tokens: int) -> list[Passage]:
    out: list[Passage] = []
    seen: set[str] = set()
    for f in sorted(anchors_dir.glob("*.anchors.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            aid = rec.get("anchor_id")
            text = str(rec.get("text", "")).strip()
            if not aid or aid in seen or text in _TRIVIAL_TEXT:
                continue
            if len(_tokens(text)) < min_tokens:
                continue
            seen.add(aid)
            out.append(Passage(str(aid), text))
    return out


def _bm25_index(passages: list[Passage]) -> tuple[list[list[str]], dict[str, float], float]:
    docs = [_tokens(p.text) for p in passages]
    n = len(docs)
    df: dict[str, int] = {}
    for d in docs:
        for t in set(d):
            df[t] = df.get(t, 0) + 1
    idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
    avgdl = (sum(len(d) for d in docs) / n) if n else 0.0
    return docs, idf, (avgdl or 1.0)


def _bm25_score(
    q: list[str],
    doc: list[str],
    idf: dict[str, float],
    avgdl: float,
    *,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    if not doc:
        return 0.0
    tf = Counter(doc)
    dl = len(doc)
    score = 0.0
    for t in q:
        f = tf.get(t, 0)
        if not f:
            continue
        score += idf.get(t, 0.0) * (f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / avgdl))
    return score


def build_retriever(passages: list[Passage], k: int = 5) -> Callable[[str], list[Passage]]:
    """Index the corpus once; return ``retrieve(query) -> top-k passages`` (deterministic: score desc,
    original order on ties; zero-score passages dropped)."""
    docs, idf, avgdl = _bm25_index(passages)

    def _retrieve(query: str) -> list[Passage]:
        if not passages:
            return []
        q = _tokens(query)
        ranked = sorted(
            ((_bm25_score(q, docs[i], idf, avgdl), i) for i in range(len(passages))),
            key=lambda s: (-s[0], s[1]),
        )
        return [passages[i] for sc, i in ranked[:k] if sc > 0]

    return _retrieve


def _format_context(hits: list[Passage], max_chars: int) -> str:
    """Render the retrieved passages as a citable context block within a ``max_chars`` budget.

    The budget counts *all* emitted characters — the header line and each ``[id] `` citation prefix,
    not just the passage bodies — so the returned block never exceeds ``max_chars`` (modulo the join
    newlines between the lines kept)."""
    if not hits:
        return ""
    header = "Relevant source passages (cite by [id]):"
    lines = [header]
    used = len(header)
    for p in hits:
        prefix = f"[{p.id}] "
        used += len(prefix)
        if used >= max_chars:
            break
        t = p.text.strip()
        if used + len(t) > max_chars:
            t = t[: max(0, max_chars - used)]
        lines.append(f"{prefix}{t}")
        used += len(t)
        if used >= max_chars:
            break
    return "\n".join(lines)


def retrieval_runner(
    base: Runner, retrieve: Callable[[str], list[Passage]], *, max_chars: int = 2000
) -> Runner:
    """Wrap a runner so each prompt is prepended with its retrieved passages (the RETRIEVAL arm)."""

    def _run(adapter_text: str, prompt: str) -> str:
        block = _format_context(retrieve(prompt), max_chars)
        return base(adapter_text, f"{block}\n\n{prompt}" if block else prompt)

    return _run


def retrieval_ab(
    adapter_text: str,
    tests: list[dict],
    runner: Runner,
    passages: list[Passage],
    *,
    grader: Grader = grade_output,
    k: int = 5,
    margin: float = 0.02,
    max_chars: int = 2000,
) -> dict:
    """Score the suite twice — distilled vs retrieval-augmented — and report the delta + per-test
    deltas. ``verdict`` bands the mean delta by ``margin`` (a measurement, never a gate)."""
    distilled = replay_suite(adapter_text, tests, runner, grader)
    retrieve = build_retriever(passages, k)
    augmented = replay_suite(
        adapter_text, tests, retrieval_runner(runner, retrieve, max_chars=max_chars), grader
    )

    d_pt, r_pt = distilled["per_test"], augmented["per_test"]
    per_test_delta = {
        key: round(r_pt[key]["score"] - d_pt[key]["score"], 4) for key in d_pt if key in r_pt
    }
    delta = round(augmented["mean_score"] - distilled["mean_score"], 4)
    verdict = (
        "retrieval-helps"
        if delta > margin
        else "retrieval-hurts"
        if delta < -margin
        else "distillation-suffices"
    )
    return {
        "distilled_mean": distilled["mean_score"],
        "retrieval_mean": augmented["mean_score"],
        "delta": delta,
        "verdict": verdict,
        "n_tests": distilled["n_tests"],
        "n_passages": len(passages),
        "k": k,
        "per_test_delta": per_test_delta,
    }


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="In-prompt-vs-retrieval A/B on one package (Step-14 G1)."
    )
    ap.add_argument("subagent", help="path to subagents/<slug>")
    ap.add_argument(
        "--runner", required=True, help="shell script that answers (adapter = system prompt)"
    )
    ap.add_argument("-k", type=int, default=5, help="top-k passages to retrieve")
    ap.add_argument("--grader", choices=["coarse", "llm"], default="coarse")
    ap.add_argument("--judge", help="shell script for the LLM grader (with --grader llm)")
    ap.add_argument("--judge-samples", type=int, default=1)
    args = ap.parse_args()

    base = Path(args.subagent)
    adapter = base / "adapters" / "claude-code" / f"{base.name}.md"
    if not adapter.is_file():
        print(f"adapter not found: {adapter}")
        return 2
    tests = load_behaviour_tests(base)
    passages, source_kind = load_passages(base)
    if not tests:
        print(f"no behaviour-tests under {base / 'tests'}")
        return 2
    if not passages:
        md_dir = base / "sources" / "markdown"
        anchors_dir = base / "sources" / "anchors"
        print(f"no retrievable passages under {md_dir} or {anchors_dir}")
        return 2
    if source_kind == "anchors":
        print(
            f"note: no source markdown under {base / 'sources' / 'markdown'}; "
            f"degraded to the distilled anchor-span fallback ({len(passages)} passages) — "
            "this is not the fair full-source distill-vs-retrieve test"
        )

    runner = shell_runner(args.runner)
    grader = (
        grade_output
        if args.grader == "coarse"
        else make_llm_grader(shell_llm(args.judge), samples=args.judge_samples)
    )
    res = retrieval_ab(
        adapter.read_text(encoding="utf-8"), tests, runner, passages, grader=grader, k=args.k
    )

    print(
        f"distilled {res['distilled_mean']:.3f}  vs  retrieval(k={res['k']}) {res['retrieval_mean']:.3f}"
        f"  → delta {res['delta']:+.3f}  [{res['verdict']}]"
        f"  ({res['n_tests']} tests, {res['n_passages']} passages)"
    )
    movers = sorted(res["per_test_delta"].items(), key=lambda kv: kv[1])
    for key, d in [*movers[:3], *movers[-3:]]:
        if d:
            print(f"  {d:+.3f}  {key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
