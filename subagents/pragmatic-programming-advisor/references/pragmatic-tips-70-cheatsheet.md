---
name: pragmatic-tips-70-cheatsheet
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P005
  - P006
  - P007
  - P008
  - P009
  - P010
  - P011
  - P012
  - P013
  - P014
  - P015
  - P016
  - P017
  - P018
  - P019
  - P020
  - P021
  - P022
  - P023
  - P024
  - P025
  - P026
  - P027
  - P028
  - P029
  - P030
  - P031
  - P032
  - P033
  - P034
  - P035
  - P036
  - P037
  - P038
  - P039
  - P040
  - P041
  - P042
  - P043
  - P044
  - P045
  - P046
  - P047
  - P048
  - P049
  - P050
  - P051
  - P052
  - P053
  - P054
  - P055
  - P056
  - P057
  - P058
  - P059
  - P060
  - P061
  - P062
  - P063
  - P064
  - P065
  - P066
  - P067
  - P068
  - P069
  - P070
  - P071
  - P072
  - P073
  - P074
  - P075
  - P076
  - P077
  - P078
  claims:
  - C00013
  - C00040
  - C00054
  - C00116
  - C00130
  - C00160
  - C00175
  - C00202
  - C00209
  - C00241
  - C00326
  - C00353
  source_anchors: []
  authored_from_digest: 72d98c2b23c00b4d8798a3a5f3d922717ea2cc553854f5a745baa8c8bbab867b
---

# Pragmatic Tips Cheatsheet

A themed quick-reference mapping the pragmatic tips this package distilled to their
current principle ids. **Every description is a paraphrase**, not verbatim source text
(the source is distillation-only). Tip numbers are the source's own. Use this as an
index — follow the principle id to the full statement and derived claims for detail.

---

## Craft and attitude

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Care about the craft | Only develop software if you intend to do it well. | P060 |
| Think about your work | Appraise every decision as you make it; do not run on auto-pilot. | P060 |
| Choose contextually | No single best language or tool exists; pick what fits the circumstances. | P052 |
| Invest in knowledge | Treat skills as an expiring asset; invest small amounts every day, diversify, and rebalance. | P011 |
| Read critically | Analyze what you read and hear; resist hype and single-answer zealotry. | P069 |

---

## Responsibility and attitude under pressure

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Take responsibility | Accept accountability; when you err, offer options not excuses. | P021 |
| Fix broken windows | Repair bad designs, wrong decisions, and poor code as soon as found, or board them up. | P039 |
| Be a catalyst for change | When approval is blocked, build something reasonable and demonstrable first. | P061 |
| Keep the big picture | Most project disasters accumulate gradually; watch beyond your own task. | P061 |
| Good enough is a requirement | Specify quality level as part of requirements; ship early for feedback rather than chasing perfection. | P042 |

---

## DRY — no duplication of knowledge

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| DRY rule | Every piece of knowledge must have one authoritative representation; duplication guarantees eventual inconsistency. | P040 |
| Imposed duplication | When environment forces multiple representations, generate them from one source with an active build-time generator. | P002 |
| Inadvertent duplication | Normalize data; replace derivable fields with calculated values. | P002 |
| Impatient duplication | Resist copy-paste under deadline pressure; the shortcut costs more later. | P071 |
| Interdeveloper duplication | Prevent with clear design, frequent communication, and a shared utility location. | P053 |
| Deliberate DRY exception | You may cache a computed value (breaking DRY) for performance, but hide the violation behind the owning module's interface. | P070 |
| Comment why not how | Keep low-level knowledge in the code; use comments only for high-level explanation. | P012 |

---

## Orthogonality and decoupling

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Eliminate effects between unrelated things | Design self-contained, single-purpose components; changes in one must not affect another. | P001 |
| Orthogonality test | If one requirement changes dramatically, ideally only one module should need to change. | P001 |
| Layering | Make each layer depend only on abstractions of the layer below. | P001 |
| Isolate third-party tools | Wrap external toolkits behind abstract interfaces so you can swap them later. | P001 |
| Avoid global data | Every reference to a global couples your code to every other consumer; pass context explicitly. | P063 |
| Deduplicate near-identical functions | Treat them as a structural smell and refactor via patterns such as Strategy. | P063 |
| Unit-test as orthogonality probe | If linking the unit test drags in most of the system, the module is poorly decoupled. | P062 |
| Write shy code | Modules must hide unnecessary detail and not depend on other modules' implementations. | P015 |
| Law of Demeter | Call methods only on objects you own, were passed, or created; ask the owning object for what you need. | P015 |
| Demeter cost/benefit | Weigh wrapper-method overhead; tightly couple modules only for a well-understood, acceptable performance trade-off. | P072 |
| Delegate over inherit | Prefer has-a over is-a to reduce inheritance coupling; forward-declare instead of including full headers. | P051 |
| Cyclic dependencies | Avoid cyclic dependencies among files, directories, and libraries; they are extremely hard to undo. | P073 |
| Organize teams orthogonally | Group by functionality with well-defined responsibilities; gauge coupling by how many people must discuss each change. | P022 |

---

## Reversibility and configuration

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| No final decisions | Design to keep options open; abstract third-party products behind interfaces so you can switch. | P023 |
| Configure, do not integrate | Drive volatile business rules from metadata in plain text; put abstractions in code, details outside. | P016 |
| Deployment as configuration | If switching the deployment model would take more than a few days, you have not designed for reversibility. | P023 |
| Reload configuration at runtime | Prefer hot-reload for long-lived processes; weigh the added complexity. | P074 |

---

## Plain text and tools

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Keep knowledge in plain text | Human-readable formats are self-describing, tool-friendly, and outlive the applications that created them. | P020 |
| Binary is not more secure | Encrypt or checksum sensitive values rather than relying on an opaque binary format. | P020 |
| Master the shell | The command shell is your workbench; tools amplify talent. | P007 |
| Know one editor deeply | Use it everywhere; do not confine yourself to a single IDE. | P007 |
| Source code control always | Use it for everything — even solo or throwaway work — because it is a project-wide time machine. | P030 |
| Learn a text-manipulation language | Writing code that writes code multiplies productivity at a one-time cost. | P065 |

---

## Tracer bullets and prototypes

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Tracer bullets | Build a thin, production-quality, end-to-end skeleton first; flesh it out incrementally and adjust aim from early misses. | P025 |
| Tracer is not throwaway | Tracer code has error checking, structure, and documentation; it becomes the system's skeleton. | P025 |
| Prototype to learn | Build cheap, disposable explorations of risky areas; the value is the lessons, not the code. | P004 |
| Prototypes need not be code | Post-it notes, whiteboard sketches, and non-functional mock-ups count. | P004 |
| Set disposability expectations | Make clear the prototype is not deployable before coding it; if there is risk of confusion, use tracer bullets instead. | P004 |

---

## Domain languages and estimation

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Program close to the problem domain | Write code using domain vocabulary, backed by a project glossary. | P005 |
| Mini-languages | A domain mini-language can start as a non-executable specification and later become executable code. | P005 |
| Different users, different languages | Provide a mini-environment for each class of user (end users, operations, test managers, developers). | P005 |
| Estimate to avoid surprises | Match accuracy and units to context; decompose into a model, focus on high-impact parameters. | P006 |
| Learn from estimates | Record all estimates; compare against production outcomes and adjust your model. | P006 |
| Iterate schedule with code | Answer on-the-spot requests with a commitment to get back after working through the steps. | P064 |

---

## Contracts, assertions, and defensive coding

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Design with contracts | State each routine's preconditions, postconditions, and class invariants; promise as little as possible. | P008 |
| Liskov Substitution | Put the contract once in the base class so subtypes preserve method meaning. | P044 |
| No perfect software | Accept that you cannot write perfect software; validate all inputs and distrust even your own code. | P059 |
| Crash early | When something impossible happens, terminate promptly — a dead program does far less damage than a crippled one. | P031 |
| Assertions | Guard impossible conditions; keep assertions on in production; never use them in place of real error handling. | P045 |
| Loop invariants | Use loop and semantic invariants to pin boundary conditions and verify correctness. | P055 |
| Exceptions only for exceptional events | Verify: would the code still run with all handlers removed? If not, you are misusing exceptions. | P035 |
| Resource ownership | The routine that allocates a resource frees it; free on every exit path; free in reverse order. | P009 |
| Defensive coding idioms | Never use gets(); null pointers after freeing; check the runtime environment dynamically. | P029 |
| Do not use code you do not understand | Wizard-generated code becomes interwoven with your own; you must be able to maintain and debug it. | P076 |

---

## Debugging

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Blame-free problem solving | Do not panic; fix the root cause, not the symptom; start from cleanly compiling, warning-free code. | P032 |
| Reproduce with a single command | Gather accurate data; observe, do not rely solely on what a reporter says. | P033 |
| Assume it is your code | A single recent change is the most likely cause; prove it in context rather than assuming. | P034 |
| Surprise means wrong assumption | After a surprising bug, add tests that fail without the fix and strengthen your mental model. | P034 |
| Upgrade third-party software carefully | Retest the whole system after upgrading the OS, compiler, or database. | P075 |

---

## Algorithm efficiency

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Estimate algorithm order | Identify big-O from the code's structure; address bad orders with divide-and-conquer. | P026 |
| Avoid premature optimization | Profile first; the asymptotically fastest algorithm is not always best for a given input size. | P054 |

---

## Concurrency and temporal coupling

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Treat time as a design element | Analyze workflow to find parallelism; decouple temporal and ordering dependencies. | P046 |
| Design for concurrency always | Protect shared and global state; keep objects valid whenever they may be called. | P036 |
| Services with well-defined interfaces | Design independent, concurrent services communicating through asynchronous work queues. | P056 |
| Blackboard coordination | Use a blackboard and rules engine for anonymous, asynchronous, heterogeneous participants. | P027 |
| MVC and events | Separate views from models; use publish/subscribe so senders need no knowledge of receivers. | P018 |

---

## Refactoring

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Refactor early and often | Treat software as a garden: refactor when you find duplication, nonorthogonality, drift, or a performance need. | P024 |
| Small, tested steps | Never add functionality during a refactoring pass; take short steps and break the build on incompatible interface changes. | P024 |
| Replace type-code switches | Use subclasses or delegation (has-a) rather than switches on type codes. | P051 |

---

## Testing

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Test early, test often, test automatically | Write test code at the same time as or before production code; coding is not done until all tests pass. | P041 |
| Design to test | Design each module's contract and its tests together; write tests before the code. | P028 |
| Test harness | Make tests easy to find and ship them with the code; build a composable, xUnit-style harness. | P013 |
| Cover the major testing types | Unit, integration (contracts), validation, resource-exhaustion, performance, and usability testing with real users. | P014 |
| Test state coverage | Test state combinations, not just lines; use real and synthetic data; decouple logic from the GUI. | P019 |
| Find bugs once | When a bug is found, add an automated test so a human never has to find that same bug again. | P068 |
| Saboteurs | Verify that tests actually catch bugs by introducing deliberate faults. | P019 |

---

## Build and source control

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Automate everything | Automate builds, tests, web publishing, and administrivia; let the computer do the repetitious work. | P003 |
| Nightly build with full test run | Run all available tests nightly so regressions are caught close to their cause. | P067 |
| Automate build from empty to deliverable | A single command should produce a shippable artifact with no manual steps. | P003 |

---

## Requirements and design

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Dig for requirements | Discover the underlying reason a user does something; work alongside users to think like one. | P057 |
| Keep requirements abstract | Capture semantic invariants; translate surface behaviors into underlying needs; restated fixed values should become configurability. | P047 |
| Avoid the specification trap | Some things are better done than described; treat requirements, design, and implementation as one feedback-driven process. | P048 |
| Use abstractions | Abstractions live longer than details; capture use cases without slavishly following any notation. | P037 |
| Solve constraints explicitly | Enumerate and disprove every avenue; ask whether the thing must be done at all. | P058 |
| Start when ready | Heed nagging doubts; prototype the doubtful area before committing to the full design. | P066 |
| Do not be a slave to formal methods | Fit techniques to your team's practices; expensive tools do not produce better designs. | P043 |
| Manage requirements creep | Actively track new features and show sponsors each one's impact on the schedule. | P077 |

---

## Communication and documentation

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Communicate effectively | Plan what you want to say; know your audience; choose the moment and style; make it two-way. | P017 |
| Documentation as code | Build documentation in rather than bolt it on; use a single presentation-independent source. | P012 |
| Meaningful names | Choose names that are non-misleading; keep tool-maintained information out of comments. | P012 |

---

## Team dynamics

| Theme / Tip | Paraphrased guidance | Principle |
|---|---|---|
| Quality is a team issue | No broken windows; every member contributes; communicate to the outside as one voice. | P050 |
| Sign your work | Take pride and responsibility in what you build. | P078 |
| Meet user expectations | Communicate expectations throughout development; then gently exceed them with low-cost delight. | P049 |

---

## Provenance

Indexes all 78 principles P001–P078. Key claim anchors: C00013 (broken windows), C00040 (DRY),
C00054 (orthogonality), C00116 (plain text), C00130 (source control), C00160 (no perfect
software), C00175 (crash early), C00202 (Law of Demeter), C00209 (configure not integrate),
C00241 (program deliberately), C00326 (test early), C00353 (find bugs once). All tip
descriptions are paraphrased; the source is distillation-only and no verbatim text appears here.
