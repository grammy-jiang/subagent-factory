"""PROV-O provenance records for Step-7 graph/cluster artifacts (C2).

The principle-graph/cluster artifacts already carry ``cluster_id``/``method``/``confidence`` — a
*subset* of provenance. C2 adds the W3C PROV-O core relations (in snake_case JSON, not RDF) so each
seeded edge/cluster is fully traceable:

- ``was_derived_from`` (prov:wasDerivedFrom) — the entity ids it came from (cluster_id, principle /
  claim / source ids).
- ``was_attributed_to`` (prov:wasAttributedTo) — the responsible agent (the producing tool module,
  or ``"llm"`` for the LLM-confirm step).
- ``was_generated_by`` (prov:wasGeneratedBy) — the activity that produced it.

Deterministic, dependency-free. ``prov_record`` is the single builder used by the seeders so the
agent/activity strings stay consistent across artifacts.
"""

from __future__ import annotations

# Activity → responsible agent (the module that performs it). "llm-confirm" is the LLM step.
_AGENT = {
    "cluster-seed": "tools.subagent_factory.seed_principle_clusters",
    "hearst-isa": "tools.subagent_factory.hearst_isa",
    "llm-confirm": "llm",
}


def prov_record(activity: str, derived_from: object, *, agent: str | None = None) -> dict:
    """Build the PROV-O subset for one edge/cluster.

    ``activity`` is the generating activity (``cluster-seed`` / ``hearst-isa`` / ``llm-confirm``).
    ``derived_from`` is an id or iterable of ids the artifact derives from (deduped, sorted, stringd).
    ``agent`` overrides the activity→agent default.
    """
    items: list[object]
    if isinstance(derived_from, str):
        items = [derived_from]
    elif isinstance(derived_from, list | tuple | set):
        items = list(derived_from)
    else:
        items = [derived_from]
    return {
        "was_derived_from": sorted({str(d) for d in items if d}),
        "was_attributed_to": agent or _AGENT.get(activity, activity),
        "was_generated_by": activity,
    }
