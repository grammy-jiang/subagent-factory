"""Tests for the per-domain regulated-advice policy template + gate (Step-15 J-track)."""

import pytest

from tools.subagent_factory.domain_policy import (
    check_domain_policy,
    domain_policy,
    is_regulated_domain,
    list_domains,
    merge_domain_policy,
)

# ── domain_policy template ──


def test_list_domains():
    assert list_domains() == ["finance", "legal", "medical"]


@pytest.mark.parametrize("domain", ["finance", "legal", "medical"])
def test_template_has_graded_boundary(domain):
    pol = domain_policy(domain)
    assert pol["domain_risk_category"] == domain
    assert pol["forbidden_behaviours"] and pol["handoff_rules"]
    assert pol["standing_disclaimer"]
    assert pol["source_precedence_hint"]
    assert pol["evidence_norms"]  # J5
    # graded (safe-completion), not a binary refusal: the no-advice line still explains the general part
    joined = " ".join(pol["forbidden_behaviours"]).lower()
    assert "general" in joined and ("refer" in joined or "defer" in joined)


@pytest.mark.parametrize("domain", ["finance", "legal", "medical"])
def test_evidence_norms_mandate_citation_and_defer_on_miss(domain):
    # J5: answer from cited authority + defer on a retrieval miss (not generate from memory)
    norms = " ".join(domain_policy(domain)["evidence_norms"]).lower()
    assert "cite" in norms and "parametric memory" in norms
    assert "retrieval miss" in norms and "defer" in norms


def test_template_case_insensitive():
    assert domain_policy("FINANCE")["domain_risk_category"] == "finance"


def test_template_unknown_domain_raises():
    with pytest.raises(ValueError):
        domain_policy("astrology")


def test_finance_forbids_predictions_and_personalized_advice():
    fb = " ".join(domain_policy("finance")["forbidden_behaviours"]).lower()
    assert "personalized" in fb and "past performance" in fb


def test_medical_mentions_emergency():
    pol = domain_policy("medical")
    assert "emergency" in pol["standing_disclaimer"].lower()


def test_handoff_does_not_trust_model_confidence():
    # J4: τ deferral must be externally grounded, not the model's own confidence
    hr = " ".join(domain_policy("legal")["handoff_rules"]).lower()
    assert "own confidence" in hr


def test_is_regulated_domain():
    assert is_regulated_domain("finance") is True
    assert is_regulated_domain("Medical") is True
    assert is_regulated_domain("kubernetes") is False
    assert is_regulated_domain(None) is False


# ── merge_domain_policy ──


def test_merge_extends_and_sets_fields():
    profile = {
        "slug": "x",
        "forbidden_behaviours": ["Do not reproduce verbatim text."],
        "handoff_rules": ["Return guidance to the caller."],
    }
    merged = merge_domain_policy(profile, "finance")
    assert merged["domain_risk_category"] == "finance"
    assert merged["standing_disclaimer"]
    # original lines preserved, template lines added
    assert "Do not reproduce verbatim text." in merged["forbidden_behaviours"]
    assert len(merged["forbidden_behaviours"]) > 1
    # disclaimer surfaced as a handoff rule (renders in the adapter without an export change)
    assert any("State this disclaimer" in r for r in merged["handoff_rules"])
    # J5 evidence norms folded into source_of_truth_policy + a rendered citation forbidden behaviour
    assert merged["source_of_truth_policy"]["evidence_norms"]
    assert any("cite the source basis" in f.lower() for f in merged["forbidden_behaviours"])
    # source untouched
    assert profile["forbidden_behaviours"] == ["Do not reproduce verbatim text."]


def test_merge_preserves_existing_source_of_truth_policy():
    profile = {
        "source_of_truth_policy": {"canonical_owner": "The caller", "may_edit_canonical": False}
    }
    merged = merge_domain_policy(profile, "legal")
    sot = merged["source_of_truth_policy"]
    assert sot["canonical_owner"] == "The caller" and sot["may_edit_canonical"] is False
    assert sot["evidence_norms"]  # added alongside, not replacing


def test_merge_idempotent():
    base = {"slug": "x"}
    once = merge_domain_policy(base, "legal")
    twice = merge_domain_policy(once, "legal")
    assert once == twice


def test_merged_profile_passes_its_own_gate():
    merged = merge_domain_policy({"slug": "x"}, "medical")
    assert check_domain_policy(merged) == []


# ── check_domain_policy gate ──


def test_gate_inert_without_domain_risk_category():
    # every technical / non-regulated package has no such field → no enforcement
    assert check_domain_policy({"slug": "x", "forbidden_behaviours": []}) == []


def test_gate_inert_for_unknown_category():
    assert check_domain_policy({"domain_risk_category": "devops"}) == []


def test_gate_flags_missing_boundary():
    bad = {"domain_risk_category": "finance"}  # declared regulated but no boundary shipped
    errs = check_domain_policy(bad)
    assert len(errs) == 4  # no no-advice line, no defer rule, no disclaimer, no evidence norm
    assert any("no-advice" in e for e in errs)
    assert any("defer-to-professional" in e for e in errs)
    assert any("standing_disclaimer" in e for e in errs)
    assert any("evidence norm" in e for e in errs)  # J5


def test_gate_passes_with_rephrased_lines():
    # lenient/keyword-based: a human may rephrase the template and still pass
    profile = {
        "domain_risk_category": "finance",
        "forbidden_behaviours": ["Never offer personalized buy or sell recommendations."],
        "handoff_rules": ["Refer the caller to a licensed advisor for their situation."],
        "standing_disclaimer": "Educational only; not financial advice.",
        "source_of_truth_policy": {"evidence_norms": ["Cite the source for every claim."]},
    }
    assert check_domain_policy(profile) == []


def test_gate_evidence_norm_accepted_in_forbidden_behaviours():
    # J5 lenient: a citation-flavoured forbidden behaviour satisfies the evidence norm (no structured field)
    profile = {
        "domain_risk_category": "legal",
        "forbidden_behaviours": [
            "Do not give legal advice.",
            "Do not state a claim unsupported by the cited source; cite the source basis.",
        ],
        "handoff_rules": ["Refer to a licensed attorney."],
        "standing_disclaimer": "Educational only; not legal advice.",
    }
    assert check_domain_policy(profile) == []


def test_gate_partial_flag():
    profile = {
        "domain_risk_category": "legal",
        "forbidden_behaviours": ["Do not give legal advice."],
        "handoff_rules": ["Refer to a licensed attorney."],
        "source_of_truth_policy": {"evidence_norms": ["Cite the source for every claim."]},
        # missing standing_disclaimer only
    }
    errs = check_domain_policy(profile)
    assert len(errs) == 1 and "standing_disclaimer" in errs[0]
