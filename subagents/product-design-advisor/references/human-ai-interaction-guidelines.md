---
name: human-ai-interaction-guidelines
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P005
  - P007
  - P009
  - P014
  - P015
  - P017
  - P022
  - P024
  - P026
  - P027
  - P052
  - P056
  - P110
  claims: []
  evidence: []
  source_anchors:
  - 46752b705098-c0000
  - 8e4a3c16f130-c0000
  - 8e4a3c16f130-c0001
  - 8fbc209156c3-c0000
  - 8fbc209156c3-c0001
  - aee5e1086948-c0000
  - eaf474371bb4-c0000
  - eaf474371bb4-c0001
  authored_from_digest: d5ae4f8fd2c25be86e3850e1f9cbfa91f2655f12669435838db936fa4d0e64a1
---

# Human-AI interaction guidelines

The catalogue of human-centered-AI interaction guidelines behind the `human-centered-ai-interaction-design` skill, grouped by the design question each answers. Each row gives the principle id (as cited in the skill), a paraphrased guideline, and its source. Product-management principles are catalogued separately in `product-principles-index.md`.

## Control model: automation and human control are independent

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P001 | Treat human control and computer automation as two independent dimensions; deliberately seek high-automation designs that still preserve meaningful human control, giving users choices over goals, timing, framing, and initiation. Some tasks legitimately sit at high-automation/low-timing-control (rapid safety devices) or high-control/low-automation (skilled creative work). | Shneiderman, HCAI (2020) |
| P007 | Reject the automation-versus-augmentation false choice; integrate AI algorithms with interface design so the system amplifies, augments, and empowers people, keeping AI a supporting element around human goals. | Shneiderman, HCAI: Three Fresh Ideas |

## Tool, not teammate

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P017 | Design computers to support people — reducing workload, raising performance, ensuring safety — not as teammates, partners, or companions that form emotional bonds; keep responsibility with humans. | Shneiderman, HCAI: Three Fresh Ideas |
| P056 | Do not default to human-like agents or robots; first consider tool-like, tele-operated, supervisory, or appliance-like designs that exploit machine strengths, favoring comprehensible, predictable, controllable interfaces. Bio-inspired ideas are starting points only when compared with non-human-like alternatives. | Shneiderman, HCAI: Three Fresh Ideas |

## User control of automation

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P026 | Give users efficient, always-available means to directly invoke and to terminate automated services. | Amershi et al., Guidelines for Human-AI Interaction; Horvitz, Mixed-Initiative UIs |
| P052 | Apply the Prometheus interface rules for human control over automation (see checklist below). | Shneiderman, HCAI (2020) |

**Prometheus interface rules (P052) — checklist:**
1. Consistent interfaces so users can form, express, and revise intent.
2. Continuous visual display of the objects and actions of interest.
3. Rapid, incremental, and reversible actions.
4. Informative feedback that acknowledges each action.
5. Progress indicators for ongoing operations.
6. Completion reports that confirm accomplishment.

## Mixed-initiative behavior

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P022 | Maintain a working memory of recent interactions so users can make natural, efficient references to their shared short-term context (distinct from long-term learning of user behavior). | Amershi et al., Guidelines for Human-AI Interaction; Horvitz, Mixed-Initiative UIs |
| P110 | Derive an action threshold p* by equating the expected utilities of acting and not acting across the four goal-by-action outcome utilities; at run time, act when the inferred goal probability exceeds p* and refrain below it. | Horvitz, Mixed-Initiative UIs |
| P015 | Choose the interaction modality by task demands: use speech when hands or eyes are unavailable, and prefer persistent, information-rich visual displays for dense, spatial, comparative, or ongoing status information. | Shneiderman, HCAI: Three Fresh Ideas |

## Safety interlocks

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P014 | Prevent excessive-control mistakes with well-designed interlocks, guards, and software range-checking that bound unsafe or irreversible actions and mitigate both excessive automation and excessive human discretion (e.g., the patient-controlled-analgesia pattern of user-triggered actions within enforced safe limits). | Shneiderman, HCAI (2020) |

## Evaluation by human outcomes

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P005 | Evaluate AI designs by human outcomes — self-efficacy, creativity, clear accountability, social participation, privacy, security, fairness, reliability, safety, and trustworthiness — shifting focus from machine autonomy toward users, experience, and human performance. | Shneiderman, HCAI: A New Synthesis |

## Governance and oversight

| ID | Guideline (paraphrased) | Source |
|----|-------------------------|--------|
| P009 | Translate AI ethics commitments into concrete governance across engineering reliability, management safety culture, independent oversight, and public regulation. | Shneiderman, HCAI: A New Synthesis |
| P024 | At the industry or public level, use independent oversight — regulation, external audits, insurance accountability, civil-society input, and professional standards — to strengthen trust. | Shneiderman, HCAI (2020) |
| P027 | Engineer safety through open management that builds a safety culture: leadership commitment, channels to report problems, internal review of failures and near misses, and public failure reporting. | Shneiderman, HCAI (2020) |

## Provenance

Every row paraphrases a promoted principle in this package's `principles/principles.yaml`; the principle ids and the section-level source anchors are listed in this file's frontmatter provenance and resolve there, and each principle's backing claims and evidence are recorded in the `human-centered-ai-interaction-design` skill that cites it. Several of these guidelines are medium-confidence or hedged in the sources and are stated here as preferences to weigh, not absolutes. All sources (Shneiderman's three HCAI works, Amershi et al.'s guidelines, and Horvitz's mixed-initiative paper) are distillation-only, so every statement here is paraphrased, not quoted.
