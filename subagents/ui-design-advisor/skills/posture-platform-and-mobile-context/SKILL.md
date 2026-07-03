---
name: posture-platform-and-mobile-context
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P014
  - P016
  - P022
  - P023
  - P024
  - P026
  - P029
  - P033
  - P034
  - P035
  - P036
  - P039
  - P042
  - P080
  - P085
  - P087
  - P088
  - P103
  - P104
  - P105
  claims:
  - C00154
  - C00156
  - C01307
  - C01308
  - C01281
  - C01282
  - C01115
  - C01116
  - C01173
  - C01174
  - C00918
  - C00919
  - C01190
  - C01191
  - C01204
  - C01205
  - C00964
  - C00965
  - C01297
  - C01298
  - C01479
  - C01480
  - C01182
  - C01183
  - C01167
  - C01168
  - C01162
  - C01163
  - C01589
  - C01590
  authored_from_digest: 286b3631142b46a712d5dcbf09393176b36d24683c15ca3cf1abd9fd108a0719
---

# Posture, Platform, and Mobile Context

Choose platform and posture early and fit the interaction to the context — sovereign, transient, mobile, embedded.

## When this applies

- Designing how a system responds to and communicates with the user (P007).
- Choosing the conceptual basis of an interface (P014).
- Designing a product's behavior toward the user (P016).
- Beginning to design a product's structure (P022).

## Procedure

Apply these principles to the situation under review; for each, name the user goal at stake and the trade-off the choice carries.

1. Design software to behave like a considerate, supportive human colleague, because people unconsciously treat interactive products as sentient and inconsiderate products irritate regardless of features, and it is not substantially harder to build, following the ideal division of labor in which the computer does the work and the person does the thinking. (P007)
2. Use interface metaphors sparingly: prefer idiomatic designs over implementation-centric or metaphoric paradigms, and never bend or limit the interface to preserve a metaphor unless a truly powerful one fits naturally. (P014)
3. Make a product considerate by embodying the traits of a caring person: take an interest and remember what the user tells it, defer and submit to the user, be forthcoming, use common sense, be conscientious about the larger goal, keep quiet about its own problems, be perceptive by remembering preferences, be self-confident rather than asking Are you sure while staying ready to undo, fail gracefully, know when to bend the rules with suspense states, and take responsibility for the work it hands to other devices. (P016)
4. Treat visual interface design as a critical, unique communication discipline conducted alongside interaction and industrial design, not as afterthought skinning: place aesthetics within a functional framework driven by user-experience and business goals, and match the visual structure to the logical structure of the users' mental models and the program's behavior so the display communicates behavior clearly. (P022)
5. Make transient-posture applications simple, clear, and obvious, limited to a single window and view with instructions built into the surface and taking no more space than needed, and give them a memory so they relaunch to their previous size, position, and configuration; treat dialog boxes and the interactive parts of daemonic applications as transient, showing a daemon icon only for continuous useful status and providing a control panel plus inline access. (P023)
6. Treat design principles and interface standards as contextual guidelines: understand the actual target users, goals, and working conditions, follow a standard's spirit, and depart only when a clearly better idiom serves those users. (P024)
7. Design embedded systems by their guiding principles: do not think of the product as a computer or bring desktop idioms to it, design the hardware and software interface together from a goal-directed and ergonomic perspective, let environmental context drive the design, use modes judiciously, limit the scope to a specific set of tasks done well, balance navigation against display density, and limit and simplify input. (P026)
8. Design kiosks for infrequent, often one-time public users without keyboards: optimize for first-time use with a transient posture, distinguish transactional kiosks that let users reach a specific goal fast from explorational kiosks that must engage through an interesting experience, show process orientation and escape hatches, plan placement and wayfinding with industrial design, and keep touch targets large with sparing text input and no drag or scroll, keeping hardware-button mappings consistent. (P029)
9. Design the represented model around the user's mental model rather than the implementation model, keeping it simpler than the actual implementation because it is the model designers most control. (P033)
10. Apply memory concretely: use the previous setting as the default and remember options until manually changed without re-offering turned-off features, remember file locations per file type and window position, remember repeated action patterns, remember essentially everything since storage is cheap, remember deduced information for silent reasonableness checks, persist the undo stack across sessions, and auto-fill past entries to reduce errors. (P034)
11. Treat each window, pane, or dialog box as a separate room and do not add one unless it serves a purpose existing windows cannot: put functions in the window where they are used, so a task integral to the application's purpose belongs in the main window rather than a dialog (one of the most frequently violated UI principles), reserve a separate room such as a dialog for functions performed outside the user's normal sequence (purging a database, importing clip art), and avoid windows pollution from putting a single function in each dialog, since a goal involves a series of functions whose connections many windows cannot show. (P035)
12. Deliver application-quality interaction design when complex behavior runs in a browser: know the Web spectrum of informational, transactional, and application, set an informational site's sovereign-versus-transient balance by visit frequency, optimize for common display sizes, avoid forcing unnecessary navigation since perceived load time tracks goal achievement more than actual time, do not assume Web apps are easier to build or more usable for free, and design sovereign Web applications like desktop applications. (P036)
13. Optimize sovereign applications, which monopolize the user's attention for long continuous full-screen periods, for perpetual intermediates: be generous with screen real estate and default to maximized, use a conservative minimal visual style, provide rich modeless feedback and rich input, map control placement to frequency of use, and maximize document views by default. (P039)
14. Make platform and posture among the first design decisions: choose the platform to balance persona needs against business and technical constraints, and set the product's posture, its behavioral stance reflecting how much attention the user devotes, from the usage context rather than the designer's taste, since look-and-feel is a behavioral choice; define an overall posture plus per-feature postures and make hardware platform decisions in concert with and after interaction design. (P042)
15. Reduce reliance on documentation through good design and templates, and treat online help as a reference for perpetual intermediates with strong indexing, shortcuts, overviews, and ToolTips rather than as a beginner crutch. (P080)
16. For handhelds, integrate functionality to minimize navigation guided by context scenarios, validate the form with weighted physical models, design most data devices as satellites of a desktop, avoid floating and pop-up windows in favor of a full-screen sovereign style, and treat phones as transient with an arguably nonvisual best interface. (P085)
17. Serve experts and perpetual intermediates to their distinct needs: give experts fast shortcuts to their working set and new powerful features, and give intermediates their frequently used working set front and center with ToolTips and the reassurance that advanced features exist, remembering that experts disproportionately influence prospective buyers. (P087)
18. For television, automotive, appliance, and audible interfaces, match the context: make TV interfaces readable across the room with simple five-way navigation and organize multi-device control around user activities rather than device functions; for cars minimize hands-off-wheel time with consistent layout, direct labeled mappings, single-press mode switching, and non-distracting audible feedback; make appliances transient and simple with familiar hardware controls; and for audible interfaces organize by mental model with common options first, signposting available functions and always offering a way back, to the top, and to a human. (P088)
19. Make mobile touch targets large enough to hit (about 48x48 dp Android or 44x44 pt iOS with spacing, and make surrounding whitespace tappable), and minimize typing with autocompletion, prefills, and numeric entry. (P103)
20. Linearize mobile content into a single vertical column (labels above controls, degrade well at minimum width) and optimize the common sequences: minimize typing, screen loads, scrolling, and taps. (P104)
21. Design for the distracted, mobile context: support quick, reentrant, self-explanatory tasks; behave well in varied light, noise, motion, and social situations; and leverage device location and hardware. (P105)

## Principles applied

- **P007** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P014** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P016** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P022** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P023** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P024** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P026** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P029** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P033** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P034** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P035** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P036** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P039** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P042** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P080** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P085** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P087** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P088** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P103** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P104** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P105** (high) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P007, P014, P016, P022, P023, P024, P026, P029, P033, P034, P035, P036, P039, P042, P080, P085, P087, P088, P103, P104, P105, their backing claims and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-report.yaml`.
