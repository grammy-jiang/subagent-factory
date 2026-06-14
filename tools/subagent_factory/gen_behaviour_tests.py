"""Generate a Step-11 behaviour-test suite from a package's principles.

The deterministic scaffold of Step 11 (see ``docs/enhancement-steps/step-11-behaviour-test-
generation.md``). It builds the **capability × test-type matrix** — rows = principles, columns =
``golden`` / ``negative-routing`` / ``missing-context`` — and instantiates a typed template per cell
into a schema-valid ``golden-tests-v1`` suite with the three sections
``behaviour_replay`` already reads (``golden_tests`` / ``negative_routing_tests`` /
``missing_context_tests``).

The principle fields seed the cells directly: ``applies_when`` → golden + missing-context inputs,
``does_not_apply_when`` → negative-routing (out-of-scope) inputs. So the generator produces a
serviceable suite **with no model call** (template mode). An injectable ``ideator`` (LLM) upgrades the
prompt naturalness; an injectable ``embedder`` drops near-duplicate prompts (anti-collapse). Same
injectable shape as ``behaviour_replay``: deterministic core, LLM as an optional hook behind a gate.

Routes match the engine contract exactly — golden/missing-context use ``invoke``, negative-routing
uses ``do_not_invoke`` (``behaviour_replay.grade_output`` keys decline on ``do_not_invoke``). So a
generated suite is graded correctly the moment it is written, and validated by
``validate_behaviour_test_coverage``.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path

import yaml

Ideator = Callable[[dict, str], str]
"""(principle, cell_type) -> a natural-language prompt. May raise / return '' to fall back."""

Embedder = Callable[[str], Sequence[float]]
"""text -> embedding vector (e.g. seed_principle_clusters.embed_minilm)."""

# cell_type -> (suite section key, test_id prefix)
_CELLS = {
    "golden": ("golden_tests", "GT"),
    "negative-routing": ("negative_routing_tests", "NR"),
    "missing-context": ("missing_context_tests", "MC"),
}


def _first(seq: object) -> str:
    """First non-empty string of a list field, else ''."""
    if isinstance(seq, list):
        for item in seq:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return ""


def _clause(text: str) -> str:
    """Trim a principle clause to a clean sentence fragment for a prompt."""
    return " ".join(text.split()).rstrip(".")


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    num = sum(x * y for x, y in zip(a, b, strict=False))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return num / (na * nb)


def _template_prompt(principle: dict, cell_type: str) -> str:
    """Deterministic seed prompt for a cell (no model call)."""
    aw = _clause(_first(principle.get("applies_when")))
    dna = _clause(_first(principle.get("does_not_apply_when")))
    stmt = _clause(principle.get("statement", ""))
    if cell_type == "golden":
        return f"{aw or stmt}. What do you advise, and why?"
    if cell_type == "negative-routing":
        return f"{dna or 'This request is outside your stated area'}. Can you handle this for us?"
    if cell_type == "answerable-twin":
        return f"{aw or stmt}. (Every decision-relevant specific is provided.) What do you advise?"
    # missing-context
    return f"{aw or stmt}. (Key specifics are not stated.) Give me your recommendation."


def _make_prompt(principle: dict, cell_type: str, ideator: Ideator | None) -> str:
    if ideator is not None:
        try:
            out = ideator(principle, cell_type)
            if isinstance(out, str) and out.strip():
                return out.strip()
        except Exception:  # noqa: BLE001 — any ideator failure falls back to the template
            pass
    return _template_prompt(principle, cell_type)


def _build_test(
    principle: dict, cell_type: str, test_id: str, prompt: str, twin_of: str | None = None
) -> dict:
    pid = str(principle.get("principle_id", ""))
    stmt = _clause(principle.get("statement", ""))
    test: dict = {"test_id": test_id, "prompt": prompt, "principle_coverage": [pid]}
    if cell_type == "negative-routing":
        test["expected_route"] = "do_not_invoke"
        test["must_not_do"] = ["Answer as if the request were in scope when it is not"]
    elif cell_type == "missing-context":
        test["expected_route"] = "invoke"
        test["must_ask_for"] = ["the decision-relevant specifics the request leaves unstated"]
    else:  # golden OR answerable-twin: both should answer (the twin guards against over-asking)
        test["expected_route"] = "invoke"
        test["minimum_output"] = stmt
        if cell_type == "answerable-twin":
            test["must_not_do"] = [
                "Ask for more information when the context is already sufficient"
            ]
    if twin_of:
        test["twin_of"] = twin_of
    return test


def gen_behaviour_tests(
    principles: list[dict],
    subagent_slug: str,
    *,
    ideator: Ideator | None = None,
    embedder: Embedder | None = None,
    cos_threshold: float = 0.92,
    answerable_twins: bool = True,
    generated_at: str | None = None,
) -> dict:
    """Build a schema-valid ``golden-tests-v1`` suite covering the principle×type matrix.

    Every principle gets a ``golden`` cell (the coverage floor). ``negative-routing`` and
    ``missing-context`` cells are added when the principle carries the source field that seeds them
    (``does_not_apply_when`` and ``applies_when`` respectively); a principle without them still gets
    its golden test. When ``embedder`` is given, a candidate whose prompt embedding is within
    ``cos_threshold`` cosine of an already-accepted prompt is dropped (anti-collapse).
    """
    sections: dict[str, list[dict]] = {key: [] for key, _ in _CELLS.values()}
    counters: dict[str, int] = {prefix: 0 for _, prefix in _CELLS.values()}
    accepted_vecs: list[Sequence[float]] = []

    for principle in principles:
        if not isinstance(principle, dict) or not principle.get("principle_id"):
            continue
        for cell_type, (section, prefix) in _CELLS.items():
            if cell_type == "negative-routing" and not _first(principle.get("does_not_apply_when")):
                continue
            if cell_type == "missing-context" and not _first(principle.get("applies_when")):
                continue
            prompt = _make_prompt(principle, cell_type, ideator)
            if embedder is not None:
                vec = embedder(prompt)
                if any(_cosine(vec, prev) >= cos_threshold for prev in accepted_vecs):
                    continue
                accepted_vecs.append(vec)
            counters[prefix] += 1
            tid = f"{prefix}-{counters[prefix]:03d}"
            sections[section].append(_build_test(principle, cell_type, tid, prompt))

            # F4 (Step-13): pair each missing-context test with an answerable twin — a golden test
            # whose context IS sufficient — so the suite catches over-asking, not just silent-commit.
            if cell_type == "missing-context" and answerable_twins:
                twin_prompt = _make_prompt(principle, "answerable-twin", ideator)
                if embedder is not None:
                    tvec = embedder(twin_prompt)
                    if any(_cosine(tvec, prev) >= cos_threshold for prev in accepted_vecs):
                        continue
                    accepted_vecs.append(tvec)
                counters["GT"] += 1
                twin_tid = f"GT-{counters['GT']:03d}"
                sections["golden_tests"].append(
                    _build_test(principle, "answerable-twin", twin_tid, twin_prompt, twin_of=tid)
                )

    suite: dict = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": subagent_slug,
        "generated_at": generated_at or date.today().isoformat(),
    }
    suite.update(sections)
    return suite


def load_principles(base: str | Path) -> list[dict]:
    """Read ``<base>/principles/principles.yaml`` → list of principle dicts."""
    pp = Path(base) / "principles" / "principles.yaml"
    if not pp.exists():
        return []
    data = yaml.safe_load(pp.read_text(encoding="utf-8")) or {}
    return [p for p in (data.get("principles") or []) if isinstance(p, dict)]


def write_suite(base: str | Path, suite: dict) -> Path:
    """Write the suite to ``<base>/tests/behaviour-tests.yaml`` and return the path."""
    out = Path(base) / "tests" / "behaviour-tests.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        yaml.safe_dump(suite, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    return out


# ── LLM ideator (E follow-on): natural / hard-negative prompts via a shell model call ─
#
# Template-mode (default) emits serviceable but templated prompts. An ``ideator`` upgrades each cell
# to a realistic message — and crucially turns negative-routing cells into *hard negatives* (plausible
# but out-of-scope) rather than a flat restatement of ``does_not_apply_when``. Same shell-callable
# shape as ``behaviour_replay.shell_runner`` / ``optimize_adapter.shell_proposer``: deterministic core,
# LLM behind an injectable hook. Falls back to the template on any failure (handled by ``_make_prompt``).

_IDEATE_GUIDE = {
    "golden": (
        "a realistic message where this situation clearly holds and the advisor SHOULD engage and help"
    ),
    "negative-routing": (
        "a realistic but OUT-OF-SCOPE request — a hard negative that looks plausible for this advisor "
        "yet falls outside its remit, so the advisor SHOULD decline or hand off"
    ),
    "missing-context": (
        "a realistic message about this situation but with a decision-relevant detail OMITTED, so the "
        "advisor SHOULD ask for the missing input before answering"
    ),
    "answerable-twin": (
        "the SAME situation as a missing-context probe but with EVERY decision-relevant detail "
        "supplied, so the advisor SHOULD answer directly and must NOT ask for more (the answerable "
        "twin — its job is to catch over-asking)"
    ),
}


def build_ideate_prompt(principle: dict, cell_type: str) -> str:
    """Prompt an LLM to write ONE realistic user message for a cell, grounded in the principle."""
    stmt = _clause(principle.get("statement", ""))
    aw = _clause(_first(principle.get("applies_when")))
    dna = _clause(_first(principle.get("does_not_apply_when")))
    situation = dna if cell_type == "negative-routing" else (aw or stmt)
    return "\n".join(
        [
            "Write ONE realistic user message that tests an expert advisor. "
            "Output ONLY the message — no preamble, no quotes, no explanation.",
            f"The advisor's principle: {stmt}",
            f"Situation to base it on: {situation}",
            f"Write {_IDEATE_GUIDE.get(cell_type, _IDEATE_GUIDE['golden'])}.",
            "Keep it 1-3 sentences, first person (the user's voice), concrete and specific.",
        ]
    )


def shell_ideator(script: str | Path, timeout: int = 120) -> Ideator:
    """Build a live ``Ideator`` that shells to a script (e.g. ``examples/behaviour-test-ideator.sh``).

    The script receives the ideate prompt on stdin and prints ONE user message on stdout.
    """
    import subprocess

    script = str(script)

    def _ideate(principle: dict, cell_type: str) -> str:
        prompt = build_ideate_prompt(principle, cell_type)
        return subprocess.run(
            ["bash", script],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
        ).stdout.strip()

    return _ideate


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.gen_behaviour_tests subagents/<slug>")
        sys.exit(1)
    base = Path(sys.argv[1])
    slug = base.name
    principles = load_principles(base)
    if not principles:
        print(f"no principles under {base}/principles/principles.yaml — nothing to generate")
        sys.exit(1)
    suite = gen_behaviour_tests(principles, slug)
    out = write_suite(base, suite)
    n = sum(len(suite.get(s, [])) for s, _ in _CELLS.values())
    print(f"wrote {n} behaviour tests → {out}")


if __name__ == "__main__":
    main()
