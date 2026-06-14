"""Tests for the PROV-O provenance record builder (C2) + its presence in seeded artifacts."""

import json
from pathlib import Path

import jsonschema
import yaml

from tools.subagent_factory.prov import prov_record

_SCHEMAS = Path(__file__).parent.parent.parent / "schemas"


def _schema(name):
    return json.loads((_SCHEMAS / name).read_text())


# ---- prov_record --------------------------------------------------------------------------------


def test_cluster_seed_agent_and_activity():
    r = prov_record("cluster-seed", ["P2", "P1", "srcA"])
    assert r["was_generated_by"] == "cluster-seed"
    assert r["was_attributed_to"] == "tools.subagent_factory.seed_principle_clusters"
    assert r["was_derived_from"] == ["P1", "P2", "srcA"]  # sorted + deduped


def test_hearst_agent():
    assert (
        prov_record("hearst-isa", ["x"])["was_attributed_to"] == "tools.subagent_factory.hearst_isa"
    )


def test_llm_confirm_agent():
    assert prov_record("llm-confirm", ["pc001"])["was_attributed_to"] == "llm"


def test_string_derived_from_becomes_single_item():
    assert prov_record("cluster-seed", "pc001")["was_derived_from"] == ["pc001"]


def test_dedupes_and_drops_empty():
    assert prov_record("cluster-seed", ["P1", "P1", "", None])["was_derived_from"] == ["P1"]


def test_agent_override():
    assert prov_record("x", ["a"], agent="custom")["was_attributed_to"] == "custom"


def test_unknown_activity_defaults_agent_to_activity():
    assert prov_record("mystery", ["a"])["was_attributed_to"] == "mystery"


# ---- PROV-O lands in seeded artifacts + satisfies the schemas ----------------------------------


def test_cluster_seed_emits_schema_valid_provenance(tmp_path):
    from tools.subagent_factory.seed_principle_clusters import seed_clusters

    base = tmp_path / "pkg"
    (base / "principles").mkdir(parents=True)
    (base / "analysis").mkdir(parents=True)
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(
            json.dumps(c)
            for c in [
                {"claim_id": "c1", "source_id": "bookA", "statement": "x"},
                {"claim_id": "c2", "source_id": "bookB", "statement": "y"},
            ]
        ),
        encoding="utf-8",
    )
    stmt = "deep modules reduce complexity through information hiding"
    (base / "principles" / "principles.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": "principles-v1",
                "principles": [
                    {
                        "principle_id": "P1",
                        "statement": stmt,
                        "derived_from_claims": ["c1"],
                        "confidence": "high",
                    },
                    {
                        "principle_id": "P2",
                        "statement": stmt + " always",
                        "derived_from_claims": ["c2"],
                        "confidence": "high",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    out = seed_clusters(base, 0.15)
    jsonschema.Draft202012Validator(_schema("principle-clusters-v1.schema.json")).validate(out)
    prov = out["clusters"][0]["provenance"]
    assert prov["was_generated_by"] == "cluster-seed"
    assert "P1" in prov["was_derived_from"] and "bookA" in prov["was_derived_from"]


def test_hearst_edge_emits_schema_valid_provenance():
    from tools.subagent_factory.hearst_isa import seed_specializes

    principles = [
        {"principle_id": "P1", "statement": "Use an authentication method such as OAuth for calls"},
        {"principle_id": "P2", "statement": "Configure OAuth tokens carefully for delegation"},
    ]
    g = seed_specializes(principles)
    g["subagent_slug"] = "x"
    jsonschema.Draft202012Validator(_schema("principle-graph-v1.schema.json")).validate(g)
    prov = g["edges"][0]["provenance"]
    assert prov["was_generated_by"] == "hearst-isa"
    assert prov["was_attributed_to"].endswith("hearst_isa")
    assert prov["was_derived_from"]
