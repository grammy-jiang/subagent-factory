# Provenance Ledger — mockito-unit-testing-advisor

schema_version: provenance-ledger-v1
package_slug: mockito-unit-testing-advisor
created_at: 2026-06-11
agent_version: "0.1.0"

---

## Source Registry

| source_id | title | rights_status | sha256 (prefix) |
|-----------|-------|---------------|-----------------|
| mockito-for-spring-l-20260610164325 | Mockito for Spring (Sujoy Acharya, Packt Publishing, 2015) | distillation-only | e5f0853c |

### Rights determination note

The source PDF carries no explicit open-license notice. The file metadata and
conversion report contain no Creative Commons or MIT license declaration.
Under the rights-and-quotation policy, a source without an explicit open license
is classified `distillation-only`: distillation and paraphrase are allowed;
verbatim quotation is prohibited. No passage of three or more consecutive source
sentences appears in any generated artifact.

### Conversion note

The source was ingested via markitdown, which produces unstructured paragraph
text without guaranteed heading hierarchy or page-number anchors. Traceability
relies on paragraph-level anchors (`-t0NNN`) generated during the anchoring step.
All Q1–Q18 answers in `interrogation-records.yaml` cite specific anchor IDs; every
profile field below traces to those anchors through the interrogation QIDs.

---

## Field Distillation Log

| Field | Source IDs | QIDs / Anchor IDs | Derivation note |
|-------|-----------|-------------------|-----------------|
| `slug` | — | — | Established at package creation; kebab-case role-based. |
| `display_name` | mockito-for-spring-l-20260610164325 | Q1 / t0009, t0062 | Synthesised from Q1 explicit role label. |
| `role` | mockito-for-spring-l-20260610164325 | Q1, Q2 / t0009, t0062, t0085-t0097, t0130-t0149 | One-sentence condensation of Q1 + Q2. |
| `tier` | principles/principles.yaml | principles-v1, PRP-001 through PRP-007 | 7 principles all marked profile_rule: true → Tier 1. |
| `when_to_use[0]` | mockito-for-spring-l-20260610164325 | Q3 / t0085, t0087 | Slow-suite / external-resource trigger from Q3. |
| `when_to_use[1]` | mockito-for-spring-l-20260610164325 | Q3 / t0085 | Hours-long test suite trigger from Q3. |
| `when_to_use[2]` | mockito-for-spring-l-20260610164325 | Q3 / t0093, t0087-t0093 | Void-method verify + ArgumentCaptor trigger from Q3. |
| `when_to_use[3]` | mockito-for-spring-l-20260610164325 | Q3 / t0137-t0138 | MVC controller test trigger from Q3. |
| `when_to_use[4]` | mockito-for-spring-l-20260610164325 | Q3 / t0089 | MockitoJUnitRunner vs initMocks guidance trigger from Q3. |
| `when_not_to_use[0]` | mockito-for-spring-l-20260610164325 | Q4 / t0127-t0129 | Integration-test exclusion from Q4. |
| `when_not_to_use[1]` | mockito-for-spring-l-20260610164325 | Q4 / t0089-t0090 | Mockito-limitations exclusion from Q4. |
| `when_not_to_use[2]` | mockito-for-spring-l-20260610164325 | Q4 / t0097 | Advanced-features exclusion (BDDMockito, inline) from Q4. |
| `inputs.required[0]` | mockito-for-spring-l-20260610164325 | Q5 / t0086-t0088, t0130-t0149 | Class-under-test artifact from Q5. |
| `inputs.required[1]` | mockito-for-spring-l-20260610164325 | Q5 / t0130-t0149 | Spring-layer discriminator from Q5. |
| `outputs.primary_format` | mockito-for-spring-l-20260610164325 | Q6 / t0089-t0093, t0137-t0147 | JUnit 4 test class deliverable from Q6. |
| `modes[advise]` | mockito-for-spring-l-20260610164325 | Q9 / t0089-t0097, t0085 | Evidence: book explains which API to pick, when to use each verify mode. |
| `modes[produce]` | mockito-for-spring-l-20260610164325 | Q9 / t0089-t0093, t0137-t0147 | Evidence: entire Ch2/Ch4 draft test classes step-by-step. |
| `modes[review]` | mockito-for-spring-l-20260610164325 | Q9 / t0063-t0064, t0087-t0088, t0090 | Evidence: source critiques anti-patterns and explains what makes a test wrong. |
| `modes[patch-suggest]` | mockito-for-spring-l-20260610164325 | Q9 / t0090, t0089, t0137 | Evidence: source instructs minimal bounded changes (add setter, switch to doThrow). |
| `quality_bar[0]` | principles/principles.yaml | PRP-001, CL004, CL006, CL007 | No real external resource. Grounded in PRP-001. |
| `quality_bar[1]` | principles/principles.yaml | PRP-002, CL008, CL009, CL029 | @Mock activation pattern. Grounded in PRP-002. |
| `quality_bar[2]` | principles/principles.yaml | PRP-003, PRP-004, CL012-CL014, CL020 | Correct stub syntax. Grounded in PRP-003/004. |
| `quality_bar[3]` | principles/principles.yaml | PRP-005, CL010, CL011 | No final/static mocking. Grounded in PRP-005. |
| `quality_bar[4]` | principles/principles.yaml | PRP-006, CL021-CL025 | Layer isolation. Grounded in PRP-006. |
| `minimum_useful_output` | mockito-for-spring-l-20260610164325 | Q11 / t0091-t0093 | Minimal StockBroker single-test from Q11. |
| `forbidden_behaviours[0]` | principles/principles.yaml | PRP-005, CL010, CL011 | Final/static mock refusal. |
| `forbidden_behaviours[1]` | mockito-for-spring-l-20260610164325 + principles | Q4, PRP-001 / t0085, t0127-t0129 | Integration-test conflation refusal. |
| `forbidden_behaviours[2]` | mockito-for-spring-l-20260610164325 | Q10 / t0087-t0088 | No stubbing the class under test. |
| `forbidden_behaviours[3]` | mockito-for-spring-l-20260610164325 | Q4 evidence-gap / t0097 | No fabricated guidance for uncovered advanced features. |
| `forbidden_behaviours[4]` | mockito-for-spring-l-20260610164325 | Q18 / t0085, t0097 | Flag version-specific API volatility. |
| `handoff_rules[0]` | mockito-for-spring-l-20260610164325 | Q8 / t0063 | Developer owns test code; inferred from audience description. |
| `handoff_rules[1]` | mockito-for-spring-l-20260610164325 | Q8 / t0128-t0129 | Integration-test boundary handed to QA/integration role. |
| `canonical_owner` | mockito-for-spring-l-20260610164325 | Q8, Q17 / t0061, t0085, t0097 | Developer + official Mockito/Spring docs. |
| `precedence` | mockito-for-spring-l-20260610164325 | Q17, Q18 / t0097 | Official versioned javadoc over 2015 book examples. |
| `knowledge_partition.always_on` | mockito-for-spring-l-20260610164325 + principles | Q12, PRP-001–007 / t0088-t0097, t0063-t0064 | 10 always-on items from Q12 cross-referenced with principles. |
| `knowledge_partition.skills` | principles/principles.yaml | operational_mapping.skill in PRP-001–007 | Six skills named as operational_mapping targets in all 7 principles. |
| `sources[0]` | source-pack.manifest.yaml | — | sha256 and title from manifest. |

---

## Conflict Log

No multi-source conflicts. Single source (mockito-for-spring-l-20260610164325).

---

## Evidence Gaps Carried Forward

1. **BDD-style Mockito (BDDMockito)** — mentioned only by reference to companion books
   (t0097); no worked example. The `produce` mode is grounded in plain Mockito examples
   only. BDDMockito excluded from `always_on` and `skills`.

2. **@InjectMocks annotation** — not demonstrated in source; only constructor/setter
   injection shown. @Spy mentioned only in passing at t0090. These patterns are deferred
   to companion books and excluded from skill targets.

3. **Integration-test misclassification refusal** — the source distinguishes unit from
   integration tests clearly (t0085, t0129) but does not state an explicit refusal
   policy. The `when_not_to_use` and `forbidden_behaviours` entries are inferred from
   that conceptual distinction; confidence is medium.

4. **Named handoff recipient** — the source does not name a specific downstream role.
   The handoff rule is inferred from the book's audience description and the chapter
   structure separating unit and integration tests.

---

## Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1.0 | 2026-06-11 | profile-deriver | Initial derivation from interrogation-records.yaml v1, principles-v1, claims.jsonl (CL001–CL042), evidence-records.yaml. |
| 0.3.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |
