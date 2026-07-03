---
name: ui-design-evidence-notes
kind: reference
status: ready
provenance:
  principles:
  - P030
  - P103
  - P104
  - P109
  - P020
  - P019
  - P006
  - P037
  - P100
  - P099
  - P102
  - P059
  - P060
  claims:
  - C00385
  - C00386
  - C00390
  - C00391
  - C00467
  - C00468
  - C00476
  - C00477
  - C00539
  - C00541
  - C00570
  - C00571
  - C00627
  - C00628
  - C00637
  - C00638
  - C00721
  - C00722
  - C00766
  - C00767
  - C00847
  - C00848
  - C01355
  - C01356
  - C01419
  - C01420
  authored_from_digest: 7af0dda6e874363a8a351b4e838c3b510cf85576659325d82c6521b250d59f28
---

# UI Design Evidence Notes

Quantitative thresholds and measured findings behind several principles, for when a recommendation needs a concrete number or an empirical rationale. Each note names its principle; the figure is the source's, and holds only in the context the source studied — state it as guidance, not a universal law, and validate for the caller's users.

## Measured thresholds

- **P030 — Label placement.** Top-aligned form labels are fastest to process (eye-tracking, Penzo: ~50ms to associate label and field, versus ~500ms for left-aligned and ~240ms for right-aligned). Prefer top-aligned for speed; left-aligned can aid scanning of a long optional form — a trade-off.
- **P103 — Touch-target size.** Make mobile touch targets large enough to hit reliably — about 48x48 dp on Android and 44x44 pt on iOS, with spacing between targets.
- **P109 — Response-time feedback.** Show a loading indicator when a response exceeds about one second; below ~0.1s feels instantaneous and needs none; the ~1s mark is where users notice the delay.
- **P104 — Mobile layout.** Linearize mobile content into a single vertical column with labels above controls, degrading gracefully at small widths.
- **P020 — Inline validation timing.** Use inline validation where users may need help, timing feedback after the answer is complete rather than mid-keystroke.
- **P019 — Question count.** Fewer questions mean faster completion — test every question for whether it earns its place; each removed field reduces effort and drop-off.
- **P006 — Form effort.** Respect the user's time: make forms short, minimize and deduce inputs, and make the path to completion obvious.
- **P037 — Action affordance.** Choose the action affordance for the job — always-visible buttons for primary actions, and match the control's look to its behavior.

## Provenance

Grounded in principles P030, P103, P104, P109, P020, P019, P006, P037, P100, P099, P102, P059, P060, their backing claims and evidence records, and paragraph anchors under `sources/anchors/`. Figures are the sources' own; treat them as context-bound guidance and validate with the caller's users. See `provenance-ledger.md`.
