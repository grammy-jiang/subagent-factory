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


def _build_test(principle: dict, cell_type: str, test_id: str, prompt: str) -> dict:
    pid = str(principle.get("principle_id", ""))
    stmt = _clause(principle.get("statement", ""))
    test: dict = {"test_id": test_id, "prompt": prompt, "principle_coverage": [pid]}
    if cell_type == "golden":
        test["expected_route"] = "invoke"
        test["minimum_output"] = stmt
    elif cell_type == "negative-routing":
        test["expected_route"] = "do_not_invoke"
        test["must_not_do"] = ["Answer as if the request were in scope when it is not"]
    else:  # missing-context
        test["expected_route"] = "invoke"
        test["must_ask_for"] = ["the decision-relevant specifics the request leaves unstated"]
    return test


def gen_behaviour_tests(
    principles: list[dict],
    subagent_slug: str,
    *,
    ideator: Ideator | None = None,
    embedder: Embedder | None = None,
    cos_threshold: float = 0.92,
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
