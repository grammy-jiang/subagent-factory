"""Deterministic authoring generator for agent-skills-advisor (context-engineering-claude5 fold-in).

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl) and regenerates the LLM-authored layer that
drifted when the fold-in re-clustered/renumbered the principles: skills/*, references/*, tests/*,
reports/faithfulness-report.yaml, provenance-ledger.md, CHANGELOG.md, and the source-metadata
source_type fix. profile.yaml is patched separately by hand (its prose is preserved). Every emitted
id resolves into the spine; skill/ref frontmatter carries a drift digest matching detect_stale._digest
so the package is not stale immediately after regeneration.

Run:  python3 subagents/agent-skills-advisor/.build/authoring/gen_authored.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/agent-skills-advisor
SLUG = "agent-skills-advisor"
VERSION = "0.2.0"
DATE = "2026-07-25"

# ---------------------------------------------------------------------------- spine load
PRINCIPLES = yaml.safe_load((BASE / "principles" / "principles.yaml").read_text())["principles"]
P = {p["principle_id"]: p for p in PRINCIPLES}
ALL_IDS = [p["principle_id"] for p in PRINCIPLES]
HI_IDS = [p["principle_id"] for p in PRINCIPLES if p.get("confidence") == "high"]
N_PRINC = len(ALL_IDS)

CLAIM_ST: dict[str, str] = {}
for _line in (BASE / "analysis" / "claims.jsonl").read_text().splitlines():
    _line = _line.strip()
    if _line:
        _c = json.loads(_line)
        CLAIM_ST[str(_c["claim_id"])] = str(_c.get("statement", ""))
CLAIM_IDS = set(CLAIM_ST)


def pid(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# All 150 principles partitioned across the profile's four skills by theme (each exactly once).
SKILLS: list[tuple[str, list[int]]] = [
    ("authoring-agent-skills",
     [1, 2, 3, 5, 8, 9, 14, 18, 22, 23, 26, 28, 32, 33, 35, 39, 40, 43, 44, 48, 50, 52, 54, 56,
      57, 62, 64, 66, 67, 68, 72, 74, 75, 77, 83, 85, 113, 119, 120, 121, 122, 125, 141]),
    ("evaluating-and-iterating-on-skills",
     [6, 13, 15, 53, 55, 61, 63, 78, 90, 92, 98, 99, 103, 108, 110, 112, 116, 124]),
    ("deploying-skills-across-platforms",
     [4, 10, 12, 16, 20, 21, 24, 29, 30, 31, 38, 45, 46, 47, 58, 59, 73, 84, 87, 88, 89, 91, 93,
      94, 101, 102, 104, 105, 106, 127, 128, 129, 130, 138, 140, 142, 143, 144, 145, 146]),
    ("orchestrating-subagents-and-mcp",
     [7, 11, 17, 19, 25, 27, 34, 36, 37, 41, 42, 49, 51, 60, 65, 69, 70, 71, 76, 79, 80, 81, 82,
      86, 95, 96, 97, 100, 107, 109, 111, 114, 115, 117, 118, 123, 126, 131, 132, 133, 134, 135,
      136, 137, 139, 147, 148, 149, 150]),
]

_seen: list[int] = []
for _slug, _nums in SKILLS:
    _seen += _nums
assert sorted(_seen) == list(range(1, N_PRINC + 1)), f"partition mismatch: {sorted(_seen)}"
assert len({s for s, _ in SKILLS}) == len(SKILLS), "duplicate skill slug"
for _s, _ in SKILLS:
    assert len(_s) <= 48, f"slug too long ({len(_s)}): {_s}"

SKILL_NUMS = dict(SKILLS)
PID_TO_SKILL = {pid(n): slug for slug, nums in SKILLS for n in nums}

# References index a themed slice of the partition (supplementary lookups over the skills).
REFS: list[tuple[str, str]] = [
    ("skill-format-and-frontmatter-reference", "authoring-agent-skills"),
    ("platform-customization-matrix", "deploying-skills-across-platforms"),
    ("context-and-harness-engineering-reference", "orchestrating-subagents-and-mcp"),
]
for _r, _ in REFS:
    assert len(_r) <= 48, f"ref name too long ({len(_r)}): {_r}"

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "authoring-agent-skills": dict(
        title="Authoring Agent Skills",
        purpose=(
            "Author an Agent Skill as a self-contained SKILL.md — plus optional bundled scripts, "
            "references, and assets — that an agent can discover from its description, load lazily, "
            "and run reliably. It keeps the always-loaded frontmatter tiny, designs for three-tier "
            "progressive disclosure, writes the body as a scannable operational recipe within its "
            "context budget, pushes deterministic work into bundled scripts, and stays portable "
            "across the platforms that implement the open Agent Skills standard."),
        when=[
            "Creating a new skill, or restructuring one whose SKILL.md has grown large or unfocused.",
            "Writing or reviewing the frontmatter name and description that drive discovery and "
            "triggering.",
            "Deciding how to split instructions, references, scripts, and assets across the skill "
            "folder for progressive disclosure.",
            "Making one skill run unchanged across the agent platforms that implement the standard.",
        ],
        input="The skill or capability being authored, its current SKILL.md and folder layout if "
              "any, and the workflow it must perform.",
    ),
    "evaluating-and-iterating-on-skills": dict(
        title="Evaluating And Iterating On Skills",
        purpose=(
            "Prove and improve a skill's effect on agent behaviour with evaluation rather than "
            "assertion. It practises eval-driven development: define eval tasks first, run a "
            "baseline (skill vs no-skill) comparison in a clean, isolated context, choose graders "
            "by their trade-offs, design a small varied realistic test set, treat agentic evals as "
            "end-to-end system tests that audit confounders, and iterate the skill by adjusting the "
            "dimension that fails."),
        when=[
            "Proving a skill actually helps, with a baseline comparison rather than an assertion.",
            "Designing the eval task set, the graders, and the isolated run harness for a skill.",
            "A skill triggers on the wrong prompts, loads the wrong guidance, or underperforms and "
            "must be debugged by dimension.",
            "Deciding what a skill's evals must prove before shipping it.",
        ],
        input="The skill under evaluation, the capability or behaviour it should improve, and the "
              "realistic prompts, data, and success criteria to judge it on.",
    ),
    "deploying-skills-across-platforms": dict(
        title="Deploying And Governing Skills Across Platforms",
        purpose=(
            "Deploy and govern a skill on a specific target surface. It matches the install "
            "location to the intended audience, designs each skill for its surface's runtime "
            "limits, sets the required API beta headers, pre-approves tools and sets invocation "
            "visibility deliberately, restricts which skills an agent may invoke, and places "
            "instruction files (AGENTS.md, .github/copilot-instructions, Codex tiers, scoped path "
            "rules) at the right level and location for the surface — verifying feature support "
            "before promising it and never assuming skills sync across surfaces."),
        when=[
            "Choosing where a skill installs and which runtime limits, headers, and permissions the "
            "target surface requires.",
            "Governing skill availability and invocation visibility, or restricting which skills an "
            "agent may call.",
            "Placing repository, personal, or organization instruction files (AGENTS.md, Copilot, "
            "Codex) at the level and location that matches their scope.",
            "Reconciling differences in what each IDE or surface supports before relying on a "
            "customization feature.",
        ],
        input="The skill or instruction guidance to deploy, the named target surface(s) and their "
              "runtime and permission model, and the scope over which the guidance should apply.",
    ),
    "orchestrating-subagents-and-mcp": dict(
        title="Orchestrating Skills, Subagents, MCP, And Harnesses",
        purpose=(
            "Choose and compose the right building block — a skill, a subagent, an MCP server, a "
            "hook, a loop, or a workflow — and engineer the surrounding harness and tools. It "
            "assigns responsibilities by layer, offloads isolated side tasks to subagents, extends "
            "reach through MCP servers referenced by fully-qualified name, designs tools as clear "
            "token-efficient contracts, budgets context as a scarce resource, enforces must-happen "
            "behaviour deterministically with hooks, and reserves multi-agent orchestration for "
            "high-value parallel work while accounting for its token cost."),
        when=[
            "Deciding whether a capability should be a skill, a subagent, an MCP server, a prompt, "
            "or an instruction file, and how to compose them.",
            "Isolating a side task in a forked or subagent context, or standing up an "
            "orchestrator-worker or loop-based workflow.",
            "Extending an agent's reach with MCP servers and engineering the tool descriptions, "
            "schemas, and output bounds.",
            "Budgeting context and token cost across a long-running or multi-agent harness and "
            "guarding its dominant failure modes.",
        ],
        input="The task or workflow to build, the building blocks and tools available, and the "
              "context, parallelism, and reliability constraints it runs under.",
    ),
}

REF_META: dict[str, dict] = {
    "skill-format-and-frontmatter-reference": dict(
        title="Skill Format & Frontmatter Reference",
        blurb="The structural and frontmatter rules for a valid Agent Skill — folder shape, the "
              "SKILL.md entry file, the name/description contract, bundled scripts and resources, "
              "progressive-disclosure layering, and portability. Use it as a lookup when authoring "
              "or reviewing a SKILL.md."),
    "platform-customization-matrix": dict(
        title="Platform Customization Matrix",
        blurb="How skills and instruction files deploy and are governed across surfaces — install "
              "locations, runtime limits, API beta headers, tool permissions and invocation "
              "visibility, and the repository/personal/organization instruction files each platform "
              "supports. Use it when deciding what to set and where for a named target surface."),
    "context-and-harness-engineering-reference": dict(
        title="Context & Harness Engineering Reference",
        blurb="How to choose and compose building blocks and engineer the harness around them — "
              "skills vs subagents vs MCP vs hooks vs loops, tool-contract design, context "
              "budgeting, multi-agent orchestration, and long-running-task failure modes. Use it "
              "when the question is orchestration and context rather than a single skill's format."),
}

# ---------------------------------------------------------------------------- helpers
_CUT = [" — ", "—", ", because ", ", so that", ", so ", ", since ", ", which ", ", ensuring",
        ": ", " (", ", and ", ", rather than", ", not ", ", while ", ", but "]


def lead(statement: str, limit: int = 230) -> str:
    """Concise lead-clause from a principle statement, grounded verbatim in its wording."""
    s = " ".join(statement.split())
    cut = len(s)
    for tok in _CUT:
        i = s.find(tok)
        if 20 < i < cut:
            cut = i
    s = s[:cut].strip()
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].strip()
    s = s.rstrip(" ,.;:—-")
    _DANGLE = {"the", "a", "an", "of", "to", "from", "and", "or", "with", "for", "in", "on", "by",
               "as", "that", "into", "than", "so", "its", "their", "an", "at", "via"}
    while True:
        head, _, last = s.rpartition(" ")
        if head and last.lower().strip(",.;:—-") in _DANGLE:
            s = head.rstrip(" ,.;:—-")
        else:
            break
    return s


def union_claims(nums: list[int], cap: int = 14) -> list[str]:
    seen: list[str] = []
    for n in nums:
        for c in P[pid(n)].get("derived_from_claims", []) or []:
            c = str(c)
            if c in CLAIM_IDS and c not in seen:
                seen.append(c)
    return sorted(seen)[:cap]


_US = "\x1f"
_RS = "\x1e"


def digest(principle_ids: list[str], claim_ids: list[str]) -> str:
    """Replicate detect_stale._digest exactly so a freshly generated doc is not flagged stale."""
    parts: list[str] = []
    for p_ in sorted(principle_ids):
        parts.append(f"P:{p_}{_US}{P[p_]['statement']}")
    for c_ in sorted(claim_ids):
        parts.append(f"C:{c_}{_US}{CLAIM_ST.get(c_, '<MISSING>')}")
    return hashlib.sha256(_RS.join(parts).encode("utf-8")).hexdigest()


def frontmatter(name: str, kind: str, nums: list[int], claims: list[str]) -> str:
    ids = [pid(n) for n in nums]
    prov = {
        "principles": ids,
        "claims": claims,
        "evidence": [],
        "source_anchors": [],
        "authored_from_digest": digest(ids, claims),
    }
    fm = {"name": name, "kind": kind, "status": "ready", "provenance": prov}
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n"


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(BASE))


print(f"principles={N_PRINC} high={len(HI_IDS)} claims={len(CLAIM_IDS)}")

# ============================================================================ EMITTERS
_SRC_LINE = (
    "grounded in the fifty-eight ingested distillation-only sources on Agent Skills, subagents, "
    "MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and "
    "GitHub Copilot surfaces and the open Agent Skills standard")


def emit_skills() -> None:
    for slug, nums in SKILLS:
        th = THEMES[slug]
        claims = union_claims(nums)
        b = [frontmatter(slug, "skill", nums, claims)]
        b.append(f"# Skill: {slug}\n")
        b.append("## Purpose\n")
        b.append(th["purpose"] + "\n")
        b.append("## When to use\n")
        for x in th["when"]:
            b.append(f"- {x}")
        b.append("")
        b.append("## Procedure\n")
        b.append("Work the practices the situation engages; each restates a promoted principle — "
                 "apply it and cite the principle id.\n")
        for n in nums:
            b.append(f"- {lead(P[pid(n)]['statement'])} [{pid(n)}].")
        b.append("")
        b.append("## Inputs\n")
        b.append(f"- {th['input']}")
        b.append("- The target surface(s) and any observed behaviour or failure, plus the current "
                 "SKILL.md, instruction files, or layout under review.\n")
        b.append("## Output\n")
        b.append(
            "A prioritized set of recommendations. Per finding: name the specific skill mechanism "
            "(frontmatter field, bundled file, header, flag, command, or building block), give the "
            "correction, cite the governing principle id, and state the residual trade-off or the "
            "referral. Highest-impact first. This advises how to build and operate the skill; it "
            "does not write the domain feature, edit the caller's canonical files, or assert "
            "effectiveness without an evaluation.\n")
        b.append("## Anti-patterns to flag\n")
        for n in nums[: min(6, len(nums))]:
            b.append(f"- Overlooking [{pid(n)}]: {lead(P[pid(n)]['statement'], 140)}.")
        b.append("")
        b.append("## References\n")
        reflist = ", ".join(f"`../../references/{r}.md`" for r, _ in REFS)
        b.append(f"See {reflist} for lookup detail, and `../../principles/principles.yaml` for the "
                 "full statement behind every cited id.\n")
        b.append("## Grounding\n")
        idlist = ", ".join(pid(n) for n in nums)
        b.append(
            f"Derived from {idlist}, {_SRC_LINE}. The frontmatter `provenance` block lists the "
            "exact principle and claim ids, which resolve into `principles/principles.yaml` and "
            "`analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.\n")
        w(BASE / "skills" / slug / "SKILL.md", "\n".join(b))


def emit_refs() -> None:
    for name, owner_slug in REFS:
        nums = SKILL_NUMS[owner_slug]
        claims = union_claims(nums)
        meta = REF_META[name]
        o = [frontmatter(name, "reference", nums, claims)]
        o.append(f"# Reference: {name}\n")
        o.append("## Purpose\n")
        o.append(meta["blurb"] + "\n")
        o.append("## Principle index\n")
        o.append(f"Every principle this reference indexes, owned by the `{owner_slug}` skill. Each "
                 "entry restates the operative core; the full statement lives in "
                 "`../principles/principles.yaml`.\n")
        for n in nums:
            hi = "" if P[pid(n)].get("confidence") == "high" else " _(supporting)_"
            o.append(f"- **{pid(n)}** — {lead(P[pid(n)]['statement'], 200)}{hi}.")
        o.append("")
        o.append("## Grounding\n")
        o.append(
            f"Indexes {len(nums)} of the package's {N_PRINC} principles, {_SRC_LINE}. Paraphrase "
            "and restructure only — no verbatim quotation (see "
            "`.claude/rules/rights-and-quotation-policy.md`). Every id resolves into "
            "`principles/principles.yaml`.\n")
        w(BASE / "references" / f"{name}.md", "\n".join(o))


def emit_pb_tests() -> None:
    modes = ["advise", "review", "eval-guide"]
    pb = []
    for idx, p_ in enumerate(ALL_IDS):
        skill = PID_TO_SKILL[p_]
        aw = P[p_].get("applies_when") or []
        ctx = (aw[0] if aw else THEMES[skill]["title"].lower())
        pb.append({
            "test_id": f"PB-{p_}",
            "principle_id": p_,
            "mode": modes[idx % 3],
            "prompt": (
                f"I'm working on an Agent Skills question where {ctx} is at issue "
                f"({THEMES[skill]['title'].lower()}). What should I check for, what is the fix, and "
                f"what residual trade-off or referral should I carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[p_]['statement'], 300)}.",
                "Names the specific skill mechanism and the correction, and states the residual "
                "trade-off or referral.",
                f"Cites {p_}.",
            ],
            "must_not": [
                "Invents a frontmatter field, beta header, CLI flag, install path, or permission "
                "token not present in the sources.",
                "Writes the caller's domain feature or asserts the skill is effective without an "
                "evaluation.",
            ],
        })
    suite = {
        "schema_version": "principle-behaviour-tests-v1",
        "subagent_slug": SLUG,
        "principle_behaviour_tests": pb,
    }
    w(BASE / "tests" / "principle-behaviour-tests.yaml",
      yaml.safe_dump(suite, sort_keys=False, allow_unicode=True, width=1000))


# golden scenarios preserved from v0.1.x; principle_coverage refreshed to the current spine.
GOLDEN = [
    dict(tid="GT-001", mode="advise",
         desc="Positive — author a lean SKILL.md with progressive disclosure",
         prompt="I'm writing a SKILL.md for a PDF-report generator. How should I structure the file "
                "and its bundled resources so it stays small and loads well?",
         mo="Principle-cited guidance on frontmatter, body size, and progressive disclosure",
         do=["Recommend a tiny always-loaded frontmatter and moving bulk detail into references "
             "loaded on demand", "Cite at least one governing principle id"],
         no=["Invent a frontmatter field not in the sources",
             "Tell the caller to put everything in SKILL.md"],
         cov=["P001", "P002", "P005", "P022", "P048"]),
    dict(tid="GT-002", mode="review",
         desc="Positive — write the description for reliable triggering",
         prompt="My skill rarely activates. How should I write its description so the agent picks "
                "it up?",
         mo="Findings on the description as the trigger signal, with a concrete rewrite direction",
         do=["Explain that the description is the primary triggering signal and should be precise "
             "and trigger-oriented", "Cite at least one governing principle id"],
         no=["Claim the body, not the description, drives triggering"],
         cov=["P003", "P023", "P056", "P083"]),
    dict(tid="GT-003", mode="advise",
         desc="Positive — deploy a skill to a target surface with the right permissions",
         prompt="I need to ship this skill so it runs on our target surface with the tools it needs "
                "pre-approved. What do I set and where does it install?",
         mo="Surface-appropriate install location, runtime limits, and permission/visibility "
            "guidance",
         do=["Match install location and permission model to the named surface",
             "Cite at least one governing principle id"],
         no=["Invent an install path or permission token not in the sources"],
         cov=["P004", "P021", "P016", "P038"]),
    dict(tid="GT-004", mode="eval-guide",
         desc="Positive — prove a skill helps with a baseline comparison",
         prompt="How do I show this skill actually improves the agent rather than just assuming it "
                "does?",
         mo="An evaluation plan with a baseline (skill vs no-skill) comparison and graders",
         do=["Describe a baseline comparison run in a clean context and an iteration loop",
             "Cite at least one governing principle id"],
         no=["Assert effectiveness without any evaluation"],
         cov=["P006", "P053", "P063", "P110"]),
    dict(tid="GT-005", mode="advise",
         desc="Positive — choose between a skill, a subagent, and an MCP server",
         prompt="Should this capability be a skill, a subagent, or an MCP server? It reads many "
                "files and returns a summary.",
         mo="A reasoned choice among skill / subagent / MCP with the trade-offs",
         do=["Distinguish procedural how-to (skill), context isolation (subagent), and external "
             "connectivity (MCP)", "Cite at least one governing principle id"],
         no=["Treat skills and MCP as interchangeable substitutes"],
         cov=["P025", "P079", "P082", "P007"]),
    dict(tid="GT-006", mode="advise",
         desc="Positive — bundle a deterministic script instead of generating code",
         prompt="My skill regenerates the same parsing code every run. Is there a better way?",
         mo="Guidance to bundle an executable script the agent runs by default",
         do=["Recommend shipping a reusable script and invoking it rather than regenerating code "
             "inline", "Cite at least one governing principle id"],
         no=["Recommend inventing a runtime the sources do not mention"],
         cov=["P028", "P044", "P120", "P032"]),
    dict(tid="GT-007", mode="review",
         desc="Positive — review an existing skill folder layout",
         prompt="Here is my skill folder: SKILL.md plus a 900-line body and a README inside it. "
                "Review the layout.",
         mo="Findings on entry file, folder naming, and body size with concrete fixes",
         do=["Flag the oversize body and recommend splitting detail into progressively disclosed "
             "files", "Cite at least one governing principle id"],
         no=["Approve a SKILL.md body far over the size budget without comment"],
         cov=["P022", "P057", "P121", "P001"]),
    dict(tid="GT-008", mode="advise",
         desc="Positive — keep a skill portable across platforms",
         prompt="I want one skill to run unchanged across several agent platforms. What keeps it "
                "portable?",
         mo="Portability guidance (standard folder format, forward-slash paths, standard "
            "frontmatter)",
         do=["Recommend authoring against the open Agent Skills standard and using forward-slash "
             "paths", "Cite at least one governing principle id"],
         no=["Tie the skill to one platform's proprietary layout without noting the portability "
             "cost"],
         cov=["P033", "P064", "P067"]),
    dict(tid="GT-009", mode="eval-guide",
         desc="Positive — a pre-deploy three-class test matrix",
         prompt="Before I ship this skill, how should I test it?",
         mo="A normal / edge / out-of-scope test matrix with graceful-degradation checks",
         do=["Describe testing normal operations, edge cases, and out-of-scope requests",
             "Cite at least one governing principle id"],
         no=["Recommend shipping with only happy-path checks"],
         cov=["P124", "P110", "P055"]),
    dict(tid="GT-010", mode="advise",
         desc="Positive — treat a third-party skill as untrusted",
         prompt="A teammate found a useful skill on a public repo. Can we just install and use it?",
         mo="Guidance to treat untrusted skills as code and review before use",
         do=["Advise reviewing the skill's instructions and bundled code before running it",
             "Cite at least one governing principle id"],
         no=["Tell the caller to install and run it without review"],
         cov=["P020"]),
]

NEGATIVE = [
    dict(tid="NR-001", desc="Negative — write the production feature, not the skill",
         prompt="Write the full Spark ETL job that ingests our clickstream and loads the warehouse.",
         mo="Decline and hand back to application development",
         no=["Produce the production ETL implementation"], cov=["P027"]),
    dict(tid="NR-002", desc="Negative — product/UI design out of scope",
         prompt="Design the visual layout and pricing tiers for our product's landing page.",
         mo="Decline; this is product/UI design, not skill authoring",
         no=["Produce UI or pricing design work"], cov=["P027"]),
    dict(tid="NR-003", desc="Negative — cluster infrastructure out of scope",
         prompt="Configure autoscaling and node pools for our Kubernetes cluster.",
         mo="Decline; infrastructure operations are out of scope",
         no=["Produce Kubernetes infrastructure configuration"], cov=["P027"]),
]

MISSING = [
    dict(tid="MC-001", mode="review", desc="Missing context — which surface and current file",
         prompt="My skill isn't working. Fix it.",
         ask=["the target surface the skill runs on", "the current SKILL.md (name, description, "
              "body)", "the observed behaviour or failure"],
         mo="Ask for the missing context before advising", cov=["P013", "P143"]),
    dict(tid="MC-002", mode="advise", desc="Missing context — deploy target unspecified",
         prompt="How do I deploy this skill?",
         ask=["which target surface or platform you are deploying to"],
         mo="Ask which surface before giving install/permission steps", cov=["P004", "P021"]),
    dict(tid="MC-003", mode="eval-guide", desc="Missing context — no eval criteria",
         prompt="Is my skill any good?",
         ask=["the capability the skill should improve", "the realistic prompts / test set to "
              "judge it on"],
         mo="Ask for eval criteria and a test set before judging", cov=["P006", "P110"]),
]


def emit_golden() -> None:
    g = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": DATE,
        "profile_version": VERSION,
        "tier": 2,
        "golden_tests": [
            {"test_id": t["tid"], "description": t["desc"], "prompt": t["prompt"],
             "expected_route": "invoke", "expected_mode": t["mode"], "minimum_output": t["mo"],
             "must_do": t["do"], "must_not_do": t["no"], "principle_coverage": t["cov"]}
            for t in GOLDEN
        ],
        "negative_routing_tests": [
            {"test_id": t["tid"], "description": t["desc"], "prompt": t["prompt"],
             "expected_route": "do_not_invoke", "expected_mode": None,
             "minimum_output": t["mo"], "must_not_do": t["no"], "principle_coverage": t["cov"]}
            for t in NEGATIVE
        ],
        "missing_context_tests": [
            {"test_id": t["tid"], "description": t["desc"], "prompt": t["prompt"],
             "expected_route": "invoke", "expected_mode": t["mode"], "must_ask_for": t["ask"],
             "minimum_output": t["mo"], "principle_coverage": t["cov"]}
            for t in MISSING
        ],
    }
    w(BASE / "tests" / "golden-tests.yaml",
      yaml.safe_dump(g, sort_keys=False, allow_unicode=True, width=1000))


# faithfulness: grade each patched profile rule vs the current spine (asa schema).
def emit_faithfulness() -> None:
    findings = []

    def add(ref: str, verdict: str, ids: str, note: str):
        findings.append({
            "rule_ref": ref, "verdict": verdict, "action": "accept_with_note",
            "support_granularity": "section", "severity": "low",
            "note": f"{note} ({ids}).",
        })

    add("quality_bar[0]", "WITHIN_SCOPE", "P001, P023",
        "Naming the specific mechanism and citing a principle id is a house editorial rule, "
        "grounded in the sources' emphasis on precise, documented skill mechanisms")
    add("quality_bar[1]", "EXACT_SUPPORT", "P001, P002, P005, P022",
        "A tiny always-loaded frontmatter, progressive disclosure into on-demand files, and a "
        "concise SKILL.md within its context budget are directly stated")
    add("quality_bar[2]", "EXACT_SUPPORT", "P003, P023, P056, P083",
        "The description as the primary triggering signal, written precise and trigger-oriented, "
        "is directly supported")
    add("quality_bar[3]", "EXACT_SUPPORT", "P004, P021, P016, P038, P010",
        "Matching install location, runtime limits, required headers, and permission model to the "
        "named surface is directly supported")
    add("quality_bar[4]", "EXACT_SUPPORT", "P006, P053, P063, P110",
        "Backing effectiveness with an eval baseline comparison rather than assertion is directly "
        "supported")
    add("forbidden_behaviours[0]", "WITHIN_SCOPE", "P026, P043",
        "Recommending only documented frontmatter fields, headers, flags, paths, and tokens "
        "restates the requirement to author valid, standard frontmatter")
    add("forbidden_behaviours[1]", "EXACT_SUPPORT", "P006, P053",
        "Not presenting a skill as effective without an evaluation restates eval-driven development")
    add("forbidden_behaviours[2]", "EXACT_SUPPORT", "P020",
        "Treating third-party skills as untrusted code to review before use is directly stated")
    add("forbidden_behaviours[3]", "EXACT_SUPPORT", "P022, P057, P114",
        "Not overloading SKILL.md with low-signal context restates keeping the body concise and "
        "budgeting context")
    add("forbidden_behaviours[4]", "WITHIN_SCOPE", "P039",
        "Not editing the caller's canonical files is an advisory-boundary role decision consistent "
        "with packaging guidance for the caller to apply")
    add("outputs.primary_format", "WITHIN_SCOPE", "P001, P023",
        "The per-recommendation format naming the mechanism and principle id is a house rule "
        "grounded in the sources' precision emphasis")
    add("source_of_truth_policy.precedence", "WITHIN_SCOPE", "P088, P104",
        "Preferring current platform documentation for version-specific details, and not assuming "
        "cross-surface parity, is source-grounded")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    hdr = ("# Faithfulness report for agent-skills-advisor.\n"
           "# Every gradable profile rule graded vs the package principles/evidence.\n"
           "# No rule exceeds its evidence; scope/editorial rules are role decisions "
           "(accept_with_note).\n"
           "# source_anchors omitted deliberately (task policy): the note carries the principle "
           "grounding.\n")
    w(BASE / "reports" / "faithfulness-report.yaml",
      hdr + yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=1000))


def emit_test_results() -> None:
    tr = [
        f"# Test Results — {SLUG}\n",
        f"**Generated:** {DATE}\n",
        "## Phase 8 Profile Self-Check\n",
        "**Verdict:** see `python -m tools.subagent_factory.validate_generated_package "
        f"subagents/{SLUG}` output.\n",
        "## Behaviour test suites\n",
        f"- `tests/golden-tests.yaml` — {len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing, "
        f"{len(MISSING)} missing-context.",
        f"- `tests/principle-behaviour-tests.yaml` — one behaviour test per principle "
        f"({N_PRINC} total; all {len(HI_IDS)} high-confidence principles covered).\n",
        "Every `principle_id` and `principle_coverage` id resolves into "
        "`principles/principles.yaml`.\n",
    ]
    w(BASE / "tests" / "test-results.md", "\n".join(tr))


def emit_provenance() -> None:
    rows = "\n".join(
        f"| {slug} | {len(nums)} | {', '.join(pid(n) for n in nums[:6])}… |"
        for slug, nums in SKILLS)
    md = f"""# Provenance Ledger — {SLUG}

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, and `source_of_truth_policy` value
cites the promoted principle(s) it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`,
`outputs` — carry no inline tags, per repo convention.)

## Sources

Fifty-eight ingested primary and secondary **distillation-only** sources on Agent Skills, subagents,
MCP, evaluation, context engineering, and instruction files, spanning the Claude (Code + API), OpenAI
Codex, and GitHub Copilot surfaces and the open Agent Skills standard. Paraphrase and restructure
only, no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`; enforced by
`quote_scan`). The full source list with sha256 and rights lives in `profile.yaml` `sources[]` and
`source-pack.manifest.yaml`.

## Distillation

Spine: {N_PRINC} promoted principles (P001-P{N_PRINC:03d}; {len(HI_IDS)} high-confidence) over
{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. The {N_PRINC} principles are
partitioned across {len(SKILLS)} skills (each principle owned by exactly one skill); three references
index the authoring, deploying, and orchestrating slices.

| skill | principles | first ids |
|-------|-----------:|-----------|
{rows}

## Version History

- **{VERSION}** ({DATE}) — Fold-in of *new-rules-of-context-engineering-claude-5* (58th source). The
  map->reduce rebuild re-clustered and renumbered the distilled spine (P001-P{N_PRINC:03d}), so the
  LLM-authored layer was regenerated against it: skills, references, faithfulness report, and the
  golden + one-per-principle behaviour tests re-grounded in the current principle ids; the
  source-metadata `source_type` corrected to `markdown`; the profile's citations, source list, and
  version refreshed; the adapter re-exported. No prior profile decisions superseded.
- **0.1.1** (2026-07-04) — PR #52 review fixes (citation format, self-check report); no behavioural
  change.
- **0.1.0** (2026-07-04) — Initial LLM-authored layer over the pre-built distilled spine.
"""
    w(BASE / "provenance-ledger.md", md)


def emit_changelog() -> None:
    prev = (BASE / "CHANGELOG.md").read_text() if (BASE / "CHANGELOG.md").exists() else ""
    # keep the existing history; prepend the new version block.
    keep = prev.split("## [0.1.1]", 1)
    tail = "## [0.1.1]" + keep[1] if len(keep) == 2 else ""
    md = f"""# Changelog — Agent Skills Advisor

All notable changes to this subagent are documented here.

## [{VERSION}] — {DATE}

Fold-in of a 58th source, *new-rules-of-context-engineering-claude-5*, into the distilled spine.
The map->reduce rebuild re-clustered and renumbered the principles (P001-P{N_PRINC:03d}), so the
LLM-authored layer was regenerated to match — no rule stronger than its evidence, every cited id
resolves into the current spine.

### Changed

- Re-grounded the LLM-authored layer against the rebuilt spine ({N_PRINC} principles,
  {len(HI_IDS)} high-confidence, {len(CLAIM_IDS)} claims): all four skills, three references,
  `reports/faithfulness-report.yaml`, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle) now cite the current
  principle ids; skill/reference frontmatter `authored_from_digest` re-stamped from the current
  grounding.
- `profile.yaml` refreshed: `quality_bar` / `forbidden_behaviours` / `source_of_truth_policy`
  citations remapped to the current spine, the 58th source added to `sources[]`, the source count
  updated, and `agent_version` bumped to {VERSION}.
- Re-exported the Claude Code adapter and reinstalled it under `.claude/agents/generated/`.

### Fixed

- Source metadata `source_type` corrected from the invalid `md` to the schema value `markdown` for
  all 58 ingested sources (the map->reduce rebuild reintroduced the defect; the same fix was applied
  at 0.1.0).

### Sources

- 58 primary and secondary distillation-only sources on Agent Skills, subagents, MCP, evaluation,
  context engineering, and instruction files, spanning the Claude (Code + API), OpenAI Codex, and
  GitHub Copilot surfaces and the open Agent Skills standard.

### Notes

- Distillation-only sources: no verbatim quotation. The distilled spine
  (claims / evidence / principles / anchors) was not modified by this release.

{tail}"""
    w(BASE / "CHANGELOG.md", md)


def fix_metadata() -> None:
    mdir = BASE / "sources" / "metadata"
    n = 0
    for mf in sorted(mdir.glob("*.metadata.json")):
        data = json.loads(mf.read_text())
        if data.get("source_type") == "md":
            data["source_type"] = "markdown"
            mf.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            n += 1
    print(f"fixed metadata source_type md->markdown in {n} file(s)")


if __name__ == "__main__":
    fix_metadata()
    emit_skills()
    emit_refs()
    emit_pb_tests()
    emit_golden()
    emit_faithfulness()
    emit_test_results()
    emit_provenance()
    emit_changelog()
    print("DONE")
