---
name: legacy-code-glossary
kind: reference
status: ready
provenance:
  principles:
  - P047
  - P082
  - P081
  - P093
  - P011
  - P075
  - P105
  - P043
  - P004
  - P123
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00067
  - C00072
  - C00073
  - C00053
  - C00054
  - C00055
  source_anchors:
  - 1d83dc6f489c-c0001
  - 1d83dc6f489c-c0003
  authored_from_digest: 9267835a992f125a61671c0e282e85c96f55e45e7f063818da8082953fe31117
---

# Legacy-code glossary

Canonical terms used by this advisor, defined as paraphrases of the source vocabulary.

| Term | Definition |
|------|------------|
| **Legacy code** | Code without tests. Getting tests in place is the prerequisite for changing behaviour quickly and safely, so untested code is risky regardless of how well written (P047). |
| **Edit and Pray** | Changing code carefully and then hoping it still works — the unsafe discipline (P048-adjacent; contrast Cover and Modify). |
| **Cover and Modify** | Covering code with tests as a safety net, then changing it; test feedback catches mistakes — the safe discipline (P048). |
| **Legacy Code Change Algorithm** | Five steps: (1) identify change points, (2) find test points, (3) break dependencies, (4) write tests, (5) make changes and refactor (P130). |
| **Dependency** | The central obstacle to testing legacy code: difficulty creating an object or running a method in a harness is a dependency problem (P105). |
| **Sensing** | A reason to break a dependency: you cannot access values the code computes (P081). |
| **Separation** | A reason to break a dependency: you cannot get the code into a test harness to run at all (P081). |
| **Fake object** | A stand-in that impersonates a collaborator so a test can sense effects through it; the dominant technique for sensing (P081). |
| **Mock object** | A fake that asserts internally; prefer a plain hand-written fake and reach for a mock only when you must write many fakes and the language makes hand-writing them costly (P123). |
| **Seam** | A place where you can alter behaviour without editing in that place, letting dependencies be excluded under test (P082). |
| **Enabling point** | The place, separate from the seam, where you decide which behaviour the seam uses — so source stays identical in production and test (P082). |
| **Seam types** | Preprocessing, link, and object seams, each corresponding to a build step that turns text into running code; object seams are preferred in OO code (P082, P138). |
| **Characterization test** | A test that documents the code's actual current behaviour rather than its intended behaviour (P093). |
| **Assert-fail-observe-expect** | The loop for writing a characterization test: assert a known-wrong value, let the failure reveal actual behaviour, then expect it (P093). |
| **No moral authority** | A characterization test documents what code does, not what it should do; apparent bugs in deployed code are kept, and fixed only after analysing ripple effects — not silently changed (P093, P140). |
| **Refactoring** | Improving the internal structure of software without changing its external behaviour, through a series of small, test-backed steps (P075). |
| **Behaviour preservation** | The primary constraint on any change: far more behaviour must be preserved than is altered (P011). |
| **Effect sketch** | A bubble per affected variable or return value with arrows to what it can change, used to decide where to place tests (P004). |
| **Pinch point** | A narrowing in an effect sketch where tests on one or two methods detect changes across many; also a natural encapsulation boundary (P043). |
| **Unit test (what disqualifies one)** | A test that talks to a database, crosses a network, touches the file system, or needs special environment setup is not a unit test; keep such tests out of the fast suite (P002). |

## Provenance

Paraphrased glossary derived from principles P047, P082, P081, P093, P011, P075, P105, P043,
P004, and P123 (with P130/P138/P140/P002 named inline). Source is distillation-only;
definitions are paraphrased, not quoted.
