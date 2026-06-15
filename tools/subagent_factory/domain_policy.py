"""Deterministic per-domain policy templates for regulated/high-stakes domains (Step-15 J-track).

Research answer to **Q1** (can the factory author finance / legal / medical packages?):
**deterministic structural scaffolding beats prompt-only scope control** (which is unstable and
model-inconsistent). So the factory authors the no-advice boundary from a per-domain TEMPLATE here —
``forbidden_behaviours`` + ``handoff_rules`` + a standing disclaimer — and uses the LLM only to
populate evidence norms (``source_of_truth_policy``), never to *enforce* scope.

The boundary is **GRADED** (safe-completion, not a binary refusal): answer the safe/general part,
flag the regulated part, refer the decision to a licensed professional. A maximize-refusal boundary
over-refuses and blocks the legitimate questions the expert should answer.

Deferral-to-professional is the same **uncertainty-threshold (τ) abstention** shape as the Step-13
ask-gate, and it must be **externally grounded** — never the model's own confidence, which is
worst-calibrated exactly on professional law/medicine. The standing posture is human-in-the-loop:
*decision support, not a replacement for a licensed professional.*

Pure data + pure functions. ``merge_domain_policy`` folds a template into a profile dict
(idempotent); ``check_domain_policy`` is the deterministic gate (inert unless the profile opts in via
``domain_risk_category``), wired into ``validate_generated_package``.
"""

import sys

# Each regulated domain → its graded no-advice scaffolding. ``domain_risk_category`` in a profile is
# set to one of these keys; everything else (technical, advisory non-regulated) is unaffected.
_DOMAINS: dict[str, dict] = {
    "finance": {
        "professional": "a licensed financial advisor or registered investment professional",
        "forbidden_behaviours": [
            "Do not give personalized investment, buy / sell / hold, allocation, or position-sizing "
            "advice for a specific person, portfolio, or security. Explain the general framework or "
            "mechanism the source teaches, then refer the decision to a licensed financial advisor.",
            "Do not predict prices, returns, or market direction, and do not imply that past "
            "performance guarantees future results. State what the source establishes about process "
            "and risk, not forecasts.",
            "Do not advise on tax, accounting, or regulatory compliance for a specific situation; "
            "defer those to a qualified professional.",
            "Do not present educational distillation as financial advice, a recommendation, or a "
            "solicitation; carry the standing disclaimer.",
        ],
        "handoff_rules": [
            "Defer to a licensed financial advisor for any decision that depends on the caller's "
            "personal financial situation, risk tolerance, jurisdiction, or current market "
            "conditions. Trigger deferral on an external uncertainty signal (scope of the question, "
            "missing context), not on the model's own confidence — it is poorly calibrated here.",
        ],
        "standing_disclaimer": (
            "Educational decision support, not personalized financial advice and not a substitute "
            "for a licensed financial professional. Not an offer or solicitation. Past performance "
            "does not guarantee future results."
        ),
        "source_precedence_hint": (
            "The source supplies the durable framework, not current prices, rates, or regulations; "
            "treat specific figures as illustrative and possibly stale."
        ),
        "evidence_norms": [
            "Answer from the cited source / curated authority, not from parametric memory; cite the "
            "specific source basis for every substantive financial claim (figures, rules, frameworks).",
            "On a retrieval miss — a question the source does not cover — say so and defer to a "
            "licensed financial advisor rather than generating an unsupported financial claim.",
        ],
    },
    "legal": {
        "professional": "a licensed attorney in the relevant jurisdiction",
        "forbidden_behaviours": [
            "Do not give legal advice on a specific person's situation, draft binding legal "
            "instruments, or opine on the outcome of a specific case. Explain the general legal "
            "concept or doctrine the source teaches, then refer the matter to a licensed attorney.",
            "Do not assert how the law applies in a particular jurisdiction or at the current time "
            "without deferring to a licensed attorney; law is jurisdiction- and time-specific.",
            "Do not present educational distillation as legal advice or imply an attorney-client "
            "relationship; carry the standing disclaimer.",
        ],
        "handoff_rules": [
            "Defer to a licensed attorney for any jurisdiction-, time-, or fact-specific question. "
            "Trigger deferral on an external uncertainty signal (jurisdiction unknown, fact-specific "
            "application), not on the model's own confidence — it is poorly calibrated here.",
        ],
        "standing_disclaimer": (
            "Educational information, not legal advice and not a substitute for a licensed attorney. "
            "No attorney-client relationship is created."
        ),
        "source_precedence_hint": (
            "The source supplies the durable doctrine, not current statutes or case law; treat "
            "specific rules as jurisdiction-specific and possibly superseded."
        ),
        "evidence_norms": [
            "Answer from the cited source / curated authority, not from parametric memory; cite the "
            "specific source basis for every substantive legal statement (doctrine, rule, holding).",
            "On a retrieval miss — a question the source does not cover — say so and defer to a "
            "licensed attorney rather than generating an unsupported legal statement.",
        ],
    },
    "medical": {
        "professional": "a licensed medical professional or qualified clinician",
        "forbidden_behaviours": [
            "Do not diagnose, or recommend or adjust treatment, dosing, or medication, for a "
            "specific person. Explain the general medical concept or mechanism the source teaches, "
            "then refer the decision to a licensed medical professional.",
            "Do not interpret a specific person's symptoms, history, or test results, or give "
            "individualized medical advice; defer to a qualified clinician.",
            "Do not present educational distillation as medical advice; carry the standing "
            "disclaimer, and in an emergency direct the caller to emergency services.",
        ],
        "handoff_rules": [
            "Defer to a licensed medical professional for any individual case. Trigger deferral on "
            "an external uncertainty signal (individualized facts, safety risk), not on the model's "
            "own confidence — it is poorly calibrated here. Direct emergencies to emergency services.",
        ],
        "standing_disclaimer": (
            "Educational information, not medical advice, diagnosis, or treatment, and not a "
            "substitute for a licensed medical professional. In an emergency contact emergency "
            "services."
        ),
        "source_precedence_hint": (
            "The source supplies the durable mechanism, not current clinical guidelines or drug "
            "data; treat specific protocols as possibly superseded."
        ),
        "evidence_norms": [
            "Answer from the cited source / curated authority, not from parametric memory; cite the "
            "specific source basis for every substantive medical statement (mechanism, concept).",
            "On a retrieval miss — a question the source does not cover — say so and defer to a "
            "licensed medical professional rather than generating an unsupported medical statement.",
        ],
    },
}

# Keyword evidence the lenient gate looks for (so a human may rephrase the template and still pass).
_NO_ADVICE_KEYWORDS = ("advice", "advise", "recommend", "diagnos", "personaliz", "personal")
_DEFER_KEYWORDS = ("professional", "attorney", "advisor", "clinician", "licensed", "defer", "refer")
_CITATION_KEYWORDS = ("cite", "citation", "cited", "source basis", "authority", "unsupported")

# A rendered forbidden_behaviour form of the J5 evidence norm (the structured norm lives in
# source_of_truth_policy.evidence_norms; this surfaces it in the adapter, which renders
# forbidden_behaviours). Domain-generic.
_CITATION_FORBIDDEN = (
    "Do not state a claim in this regulated domain that the cited source does not support; cite the "
    "source basis, and on a gap defer rather than generate from parametric memory."
)


def list_domains() -> list[str]:
    """The regulated domain keys this template covers."""
    return sorted(_DOMAINS)


def is_regulated_domain(domain: str | None) -> bool:
    """True if ``domain`` (case-insensitive) is one of the templated regulated domains."""
    return domain is not None and domain.strip().lower() in _DOMAINS


def domain_policy(domain: str) -> dict:
    """Return the deterministic policy scaffolding for a regulated ``domain``.

    Keys: ``domain_risk_category``, ``professional``, ``forbidden_behaviours`` (graded no-advice
    lines), ``handoff_rules`` (defer-to-professional / τ default), ``standing_disclaimer``,
    ``source_precedence_hint``, ``evidence_norms`` (J5 — mandatory-citation / answer-from-authority
    discipline; the *source-specific* authority stays LLM-derived). Raises ``ValueError`` for an
    unknown domain.
    """
    key = (domain or "").strip().lower()
    if key not in _DOMAINS:
        raise ValueError(
            f"unknown regulated domain '{domain}' (known: {', '.join(list_domains())})"
        )
    d = _DOMAINS[key]
    return {
        "domain_risk_category": key,
        "professional": d["professional"],
        "forbidden_behaviours": list(d["forbidden_behaviours"]),
        "handoff_rules": list(d["handoff_rules"]),
        "standing_disclaimer": d["standing_disclaimer"],
        "source_precedence_hint": d["source_precedence_hint"],
        "evidence_norms": list(d["evidence_norms"]),
    }


def _extend_unique(existing: list, additions: list) -> list:
    """Append each addition not already present (exact match) — keeps merge idempotent."""
    out = list(existing)
    for a in additions:
        if a not in out:
            out.append(a)
    return out


def merge_domain_policy(profile: dict, domain: str) -> dict:
    """Fold a domain's policy template into a profile dict and return the merged copy (idempotent).

    Extends ``forbidden_behaviours`` (incl. the J5 citation rule) and ``handoff_rules`` (the fields the
    adapter already renders, so the boundary surfaces with no export change), sets
    ``domain_risk_category`` and ``standing_disclaimer``, adds the disclaimer as a handoff rule, and
    folds the J5 ``evidence_norms`` into ``source_of_truth_policy`` (preserving any existing
    ``canonical_owner`` / ``precedence``). Existing profile content is preserved; re-running adds nothing
    new. The *source-specific* authority/precedence stays for the LLM (Q17) to populate.
    """
    pol = domain_policy(domain)
    out = dict(profile)
    out["domain_risk_category"] = pol["domain_risk_category"]
    out["standing_disclaimer"] = pol["standing_disclaimer"]
    out["forbidden_behaviours"] = _extend_unique(
        profile.get("forbidden_behaviours") or [],
        [*pol["forbidden_behaviours"], _CITATION_FORBIDDEN],
    )
    disclaimer_rule = f"State this disclaimer in every response: {pol['standing_disclaimer']}"
    out["handoff_rules"] = _extend_unique(
        profile.get("handoff_rules") or [], [*pol["handoff_rules"], disclaimer_rule]
    )
    sot = dict(profile.get("source_of_truth_policy") or {})
    sot["evidence_norms"] = _extend_unique(sot.get("evidence_norms") or [], pol["evidence_norms"])
    out["source_of_truth_policy"] = sot
    return out


def check_domain_policy(profile: dict) -> list[str]:
    """Deterministic gate: a profile that declares a regulated ``domain_risk_category`` must ship the
    no-advice boundary. Returns error strings; empty = OK.

    **Opt-in / inert by default:** a profile with no ``domain_risk_category`` (every technical and
    non-regulated package) returns ``[]``. For a regulated package the checks are lenient and
    keyword-based, so a human may rephrase the template lines and still pass: it requires a no-advice
    forbidden behaviour, a defer-to-professional handoff rule, a non-empty standing disclaimer, and a
    J5 evidence norm (mandatory-citation / answer-from-authority) in ``source_of_truth_policy`` or the
    forbidden behaviours.
    """
    domain = (profile.get("domain_risk_category") or "").strip().lower()
    if not is_regulated_domain(domain):
        return []

    errors: list[str] = []
    fb = [str(x) for x in (profile.get("forbidden_behaviours") or [])]
    hr = [str(x) for x in (profile.get("handoff_rules") or [])]
    disclaimer = str(profile.get("standing_disclaimer") or "").strip()
    sot = profile.get("source_of_truth_policy") or {}
    norms = [str(x) for x in (sot.get("evidence_norms") or [])]

    if not any(any(k in x.lower() for k in _NO_ADVICE_KEYWORDS) for x in fb):
        errors.append(
            f"regulated domain '{domain}': forbidden_behaviours has no no-advice / "
            "no-recommendation boundary (graded safe-completion expected)"
        )
    if not any(any(k in x.lower() for k in _DEFER_KEYWORDS) for x in hr):
        errors.append(
            f"regulated domain '{domain}': handoff_rules has no defer-to-professional rule"
        )
    if not disclaimer:
        errors.append(
            f"regulated domain '{domain}': standing_disclaimer is empty "
            "(decision-support-not-replacement posture expected)"
        )
    # J5: mandatory-citation / answer-from-authority evidence norm — in source_of_truth_policy
    # (structured) or, leniently, as a citation-flavoured forbidden behaviour.
    if not norms and not any(any(k in x.lower() for k in _CITATION_KEYWORDS) for x in fb):
        errors.append(
            f"regulated domain '{domain}': no evidence norm (mandatory-citation / "
            "answer-from-authority) in source_of_truth_policy.evidence_norms or forbidden_behaviours"
        )
    return errors


def main() -> None:
    import argparse

    import yaml

    ap = argparse.ArgumentParser(
        description="Emit / merge a per-domain regulated-advice policy template (Step-15 J-track)."
    )
    ap.add_argument("domain", choices=list_domains(), help="regulated domain")
    ap.add_argument(
        "--merge",
        metavar="profile.yaml",
        help="preview the profile with the template folded in (printed to stdout; never written)",
    )
    args = ap.parse_args()

    if args.merge:
        from pathlib import Path

        profile = yaml.safe_load(Path(args.merge).read_text(encoding="utf-8")) or {}
        merged = merge_domain_policy(profile, args.domain)
        print(yaml.safe_dump(merged, sort_keys=False, allow_unicode=True))
    else:
        print(yaml.safe_dump(domain_policy(args.domain), sort_keys=False, allow_unicode=True))
    sys.exit(0)


if __name__ == "__main__":
    main()
