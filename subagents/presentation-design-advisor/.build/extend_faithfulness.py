"""One-shot: extend reports/faithfulness-report.yaml to cover knowledge_partition.always_on
and examples (review finding F3), and re-grade the two rules whose citations changed (F5).

Each always_on finding was checked paragraph-by-paragraph against the exact wording and
``applies_when`` of every principle it cites, with the numeric and mechanical claims
(28 points, 120-140 wpm, four-item groupings, two-to-four-item lists, twenty-or-thirty
seconds, over 2,000 words, within an hour) verified against the principle that carries them.
"""

from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
REPORT = BASE / "reports" / "faithfulness-report.yaml"


def f(ref, note, verdict="WITHIN_SCOPE", distortion=("none",), severity="low",
      action="accept_with_note"):
    return {
        "rule_ref": ref,
        "verdict": verdict,
        "distortion": list(distortion),
        "severity": severity,
        "action": action,
        "note": note,
    }


NEW = [
    f(
        "quality_bar[7]",
        "Restates P036; within the source's scope, no strengthening. The four critique perspectives "
        "(speech, structure, visual aids, delivery), the offsetting-strength caveat and the "
        "distraction test are all carried over, and none is turned into a scoring rule the "
        "principle does not state.",
    ),
    f(
        "inputs.required[0]",
        "Authored intake rule, not a domain claim: it names the artifact plus the audience as the "
        "only gating context. Narrower than the sources, never stronger; P061's persona work and "
        "P075's understand/interest test remain available once the extra context arrives.",
    ),
    f(
        "inputs.required[1]",
        "Authored intake rule. The occasion, post-talk action, slot length, preparation time and "
        "room conditions are marked recommended rather than mandatory, which weakens rather than "
        "strengthens the claim that P065/P066/P088 attach to each of them.",
    ),
    f(
        "inputs.required[2]",
        "Authored operating instruction about reading a caller-supplied file. It asserts nothing "
        "about presentation design and therefore carries no source claim to over-state; recorded "
        "here so the section has no unaudited rule.",
    ),
    f(
        "knowledge_partition.always_on[0]",
        "Assertion-evidence paragraph. Restates P014/P015/P021/P044/P045/P046/P047/P069/P070/"
        "P071/P077/P096. Mechanical claims verified against P015 word for word: two lines maximum, "
        "left justified, sentence capitalisation with the period optional, upper-left start, "
        "28 points, phrase-preserving line breaks. The three evidence-first situations (teaching, "
        "complex assertion, skeptical audience) match P046's own list, and the paragraph keeps "
        "P069's prohibition on an assertion with no visual evidence rather than generalising it "
        "into a ban on the evidence-first order.",
    ),
    f(
        "knowledge_partition.always_on[1]",
        "Density paragraph. Restates P012/P018/P019/P025/P026/P033/P073/P080/P081/P084/P097/P101. "
        "Numbers verified: the 120-to-140-words-a-minute comparison is P025's own, the "
        "four-items-or-fewer grouping limit is P084's. P073's qualifier survives intact — "
        "splitting without sequencing does not by itself solve density — and P081's TED-style "
        "simplicity keeps its 'engineered, costs more preparation' framing rather than becoming "
        "a recommendation to imitate the style.",
    ),
    f(
        "knowledge_partition.always_on[2]",
        "Visual-evidence paragraph. Restates P001/P002/P034/P042/P078/P091/P100/P102/P103. The "
        "evidence-type mapping is P034's own list; P078's boundary is preserved in both "
        "directions (analogy for how something works, how large, how likely — never as evidence "
        "in an argument); P100's 'never from an empty body' and P103's cost caveat are carried; "
        "P102's reference requirement stays scoped to slides carrying another group's work.",
    ),
    f(
        "knowledge_partition.always_on[3]",
        "Typography paragraph. Restates P004/P007/P008/P011/P017/P023/P049/P098/P099. P007 is "
        "restated as 'a large minimum type size' with no invented point figure (the 28-point "
        "number belongs to P015's headline rule and is not reused here). The two-line block and "
        "two-to-four-item list limits are P023's; pure black and pure white affording the "
        "greatest contrast is P099's; the palette-verified-by-projecting requirement is P011's.",
    ),
    f(
        "knowledge_partition.always_on[4]",
        "Story paragraph. Restates P005/P035/P041/P059/P060/P064/P087/P116/P118. The "
        "third-or-fourth-round expectation for genuinely clever ideas is P118's own; the "
        "what-is opening and its justification are P087's; P041 keeps stories confined to the "
        "two jobs it names rather than becoming a general instruction to tell stories.",
    ),
    f(
        "knowledge_partition.always_on[5]",
        "Audience paragraph. Restates P013/P056/P057/P058/P061/P063/P074/P075/P114/P119/P120. "
        "P061's persona slide is stated with its condition (front of deck, private working "
        "context, never projected). P013's mixed-audience claim keeps its 'no design achieves "
        "it' shape — satisfied by the end rather than throughout. P074 is cited here from "
        "version 1.1.0, where it states what it states: the message outranks the polish.",
    ),
    f(
        "knowledge_partition.always_on[6]",
        "Persuasion paragraph. Restates P006/P030/P038/P040/P068/P092/P113/P115/P117/P120. "
        "Version 1.0.0 generalised P006's 'science / scientists' to 'technical work' without "
        "carrying a principle for the wider domain; 1.1.0 keeps the domain wording of P006 "
        "('scientific and technical presenters') and grounds the broader reach in the "
        "Duarte-derived P120, whose claim is that analytical audiences also decide partly on "
        "emotion. P030's 'stacking more proof does not convert a determined skeptic' and P038's "
        "override caveat are carried unweakened.",
    ),
    f(
        "knowledge_partition.always_on[7]",
        "Organisation paragraph. Restates P037/P039/P043/P067/P076/P082/P083/P086/P089/P090. The "
        "four structural levers and four pitfalls are P083's own enumeration, the three ways "
        "audiences get lost are P039's, and the three transition-signalling channels with their "
        "three placements are P043's — none is expanded into a general rule about structure.",
    ),
    f(
        "knowledge_partition.always_on[8]",
        "Framing-slides paragraph. Restates P022/P024/P032/P050/P085/P112. The 'more than twenty "
        "or thirty seconds' figure is P085's own; the 'In closing' / 'In summary' headline, the "
        "pause for applause and the animated Questions word are P022's sequence; P024's ranking "
        "of an empty slide, a Thank You slide and a Questions slide is reproduced without "
        "extension; P032 keeps its 'only where they earn their place' hedge; P112 stays "
        "conditional on the talk being covered or filmed.",
    ),
    f(
        "knowledge_partition.always_on[9]",
        "Rehearsal paragraph (split out of the fused delivery paragraph in 1.1.0). Restates "
        "P020/P052/P054/P072/P094/P095/P105. The arithmetic is P095's: at roughly 130 to 140 "
        "words a minute a fifteen-minute talk means over 2,000 words. P054's exception for short "
        "high-stakes fragments is preserved, so the rejection of memorisation is not stated as "
        "absolute; P105 keeps 'costly by default' rather than becoming a prohibition.",
    ),
    f(
        "knowledge_partition.always_on[10]",
        "In-room delivery paragraph (split out in 1.1.0). Restates P016/P066/P079/P106/P107/"
        "P108/P110/P111. P111's condition is now stated explicitly — several deliberate "
        "delivery-mode changes within an hour wherever the slot runs beyond about ten minutes, "
        "which is P111's own `applies_when` and the point at which its squirm claim begins. "
        "P016's 'no single delivery style is correct' and P066's audience-and-room caveat are "
        "carried as stated, so no prescriptive style rule is created.",
    ),
    f(
        "knowledge_partition.always_on[11]",
        "Question-and-challenge paragraph. Restates P029/P055/P093/P109. P109's ordered sequence "
        "and P055's three tested responses are reproduced as options rather than as a single "
        "mandated script, and P093's concession rule keeps its condition (where the challenger "
        "is right).",
    ),
    f(
        "knowledge_partition.always_on[12]",
        "Format-and-preparation paragraph. Restates P009/P010/P027/P031/P051/P062/P065/P088. "
        "P031's five advantages and five disadvantages are reproduced as the weighing, not as a "
        "verdict. P027 and P051 keep their stated occasions (Lessig for keynotes and "
        "after-dinner talks reused on multiple occasions; pecha kucha where a manager must raise "
        "a group's presentations quickly). P065 is narrowed to scaling and booking preparation "
        "without asserting its 36-to-90-hour range. P048, whose own "
        "`operational_mapping.profile_rule` is false, was cited here as an operative 'plan for "
        "slow adoption' instruction in 1.0.0 and is removed in 1.1.0.",
    ),
    f(
        "knowledge_partition.always_on[13]",
        "Equipment-and-contingency paragraph. Restates P003/P028/P053/P104. P028's own hedge is "
        "carried explicitly — rehearsal guarantees nothing, since practised demonstrations still "
        "fail, but greatly increases the odds — so the rehearsal requirement is not stated as a "
        "guarantee. P053's compound-failure reasoning and handout fallback are reproduced with "
        "their condition (once structure and slides are set; where the equipment is unproven).",
    ),
    f(
        "examples[0]",
        "Bullet-deck conversion example. Every step cites the principle it applies (P014, P045, "
        "P071, P034, P002, P025, P073, P015, P070) and closes on P070's preparation trade-off "
        "rather than promising a better reception. The advice-only boundary is stated in the "
        "final sentence, so the example does not model doing the caller's work.",
    ),
    f(
        "examples[1]",
        "Failed-pitch diagnosis. P006's three appeals, P030's evidence-plus-desire pairing, "
        "P119's few-proof-points-for-an-emotionally-driven-audience claim, P038's prior bias, "
        "P117's proportional reward and P113's signal path are each cited where used, and the "
        "response explicitly declines to predict the funding outcome — matching P038's own claim "
        "that prior bias can override the argument.",
    ),
    f(
        "examples[2]",
        "Refusal to inflate a weak result. Grounded in P068 (build up, never deceive) and the "
        "forbidden-behaviour boundary, then redirects to P001/P077, P029, P055/P093, P009 and "
        "P006/P117. No principle is used to justify the refusal beyond what P068 states.",
    ),
    f(
        "examples[3]",
        "Added in 1.1.0 to demonstrate the two refusal categories no example previously covered "
        "(declining to rule on the underlying result, and declining to guarantee approval). The "
        "refusal of the outcome guarantee is grounded in P038 and P028 exactly as they are "
        "stated; the refusal to rule on the data is the authored scope boundary and is labelled "
        "as such rather than attributed to a principle.",
    ),
]

REGRADE = {
    "forbidden_behaviours[2]": (
        "Authored scope boundary, no principle citation. Version 1.0.0 cited P001/P091 for the "
        "certification prohibition; neither principle states or implies one — P001 fixes the "
        "assertion before graphing it and P091 builds a chain of evidenced sub-assertions. The "
        "rule is sound policy but its grounding was invented, so the citation is removed rather "
        "than re-attached to principles that do not carry it."
    ),
    "source_of_truth_policy.precedence": (
        "Restates P027/P051/P103/P016 (occasion-bound techniques are adaptable guides) and "
        "P028/P046/P047 (carry the source's own hedging); within scope, no strengthening. The "
        "conflict tie-breaker — audience comprehension decides — cited P012/P056 in 1.0.0, "
        "neither of which states a rule for arbitrating between principles; in 1.1.0 it is "
        "labelled an authored tie-breaker with no principle citation."
    ),
}


def main() -> None:
    report = yaml.safe_load(REPORT.read_text(encoding="utf-8"))
    by_ref = {x["rule_ref"]: x for x in report["findings"]}
    for ref, note in REGRADE.items():
        by_ref[ref]["note"] = note
    known = set(by_ref)
    report["findings"].extend(x for x in NEW if x["rule_ref"] not in known)
    REPORT.write_text(
        yaml.safe_dump(report, sort_keys=False, width=100, allow_unicode=True), encoding="utf-8"
    )
    print(f"findings: {len(report['findings'])}")


if __name__ == "__main__":
    main()
