---
name: navigation-and-information-structure
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P018
  - P027
  - P046
  - P069
  - P070
  - P072
  - P073
  - P079
  - P089
  - P097
  - P098
  - P106
  - P107
  claims:
  - C00304
  - C00305
  - C01372
  - C01373
  - C01517
  - C01518
  - C01527
  - C01528
  - C01223
  - C01224
  - C01531
  - C01532
  - C01258
  - C01259
  - C01476
  - C01477
  - C01522
  - C01523
  - C01260
  - C01261
  - C00318
  - C00319
  - C00323
  - C00324
  - C00504
  - C00512
  - C00537
  - C00547
  authored_from_digest: bf3a22ba56a3276018804fe14c54dc4b7e522ef6fb8edac4d3d96498f6739b62
---

# Navigation and Information Structure

Structure navigation, menus, and information display around the user's goal and mental model.

## When this applies

- Helping users know where they are and where to go (P004).
- Designing how users locate their documents or data (P018).
- Designing an application's menu system (P027).
- Designing keyboard access and cross-vector consistency (P046).

## Procedure

Apply these principles to the situation under review; for each, name the user goal at stake and the trade-off the choice carries.

1. Support navigation and wayfinding with clear, consistent signposts such as titles, breadcrumbs, progress indicators, menus, persistent objects, and labels or terms that match users' mental models. (P004)
2. Separate the storage system from the retrieval system rather than forcing users to conform to a rigid relational schema: keep records in a database-like digital soup that accepts any record and returns a token, build retrieval as an unlimited number of attribute indices each keyed to one concept, fill those indices both by automatic extraction and by easy manual pointers, and never demand that users configure their information in advance, because they rarely can express their needs ahead of time and often change their minds. (P018)
3. Provide multiple parallel command vectors — menus, toolbars, keyboard accelerators, and direct manipulation — so users of different skill sets can command the program the way that suits them, giving immediate vectors to the minimal working set of frequently used functions identified from persona scenarios and pedagogic vectors to beginners, and understanding that information in the world (menus, dialogs) is dependable but slow while information in the head (accelerators) is fast but must be learned, so beginners rely on world vectors and experts increasingly on head vectors; as an exception, deny dangerous commands like Erase All easy parallel vectors and protect them within menus and dialogs like hidden ejector-seat levers. (P027)
4. Build memorization and cross-vector support by showing consistent icons across menus, toolbars, dialogs, and help, and by exposing complete keyboard accelerators and mnemonics beside menu commands. (P046)
5. Follow users' mental models by organizing and indexing information the way the target user thinks, and pursue less is more by constantly reducing interface elements without reducing capability and avoiding complex-but-not-powerful silos, since minimalism depends on a clear understanding of purpose, though reduction is a balancing act because excessive visual simplicity can create cognitive complexity. (P069)
6. Design toolbars to give experienced users fast, visible, immediate access to frequently used functions rather than duplicating the descriptive menu: use images on toolbars and text on menus deliberately, since text is precise but slow (suiting teaching) while a pictograph is ambiguous until learned but then recognized fast (suiting quick access); a butcon's icon need only be recognizable once learned, with its purpose taught through ToolTips (well-timed with about a one-second lag) rather than by labeling it with both text and image, which costs too many pixels; and disable inapplicable toolbar controls by graying them out rather than making them disappear, because users remember toolbar layouts by position. (P070)
7. Improve navigation by reducing the number of places a user must go, keeping windows, views, panes, and controls to the minimum needed, providing signposts as persistent objects, overviews, appropriate control-to-function mapping, interface inflection, and by avoiding hierarchies. (P072)
8. Avoid multi-window navigation schemes for moving between programs: the overlapping-sheets window metaphor does not scale beyond about three applications and causes lost-window confusion, and multiple windows sharing a small screen (overlapping or tiled) is not a good general solution, so prefer full-screen applications with a minimal switching mechanism such as a taskbar; inside a sovereign application, however, multipaned windows that display related information in adjacent panes reduce navigation and window-management excise to almost nil and are practically a requirement. (P073)
9. Design menu structure and item behavior for clarity: use cascading hierarchical menus only in sophisticated sovereign applications for rarely used functions or as a secondary vector (with a wide movement threshold), avoid adaptive menus that hide infrequent items (which studies show slow users down and which they overwhelmingly dislike), avoid bang/immediate menus whose title executes a function (immediate commands belong on toolbars), gray out inapplicable menu items to improve the menu's teaching value, and use a checkmark item that is clearly checked or unchecked rather than a flip-flop item that shows the state not currently chosen. (P079)
10. Use adjacent panes to reduce navigation, placing panes that support drag-and-drop next to each other, avoid splitting one facility across tabbed panes since that increases excise, reserve tabs for a multi-document work area or mutually exclusive supporting panes, group frequently used tools spatially while reserving menus for infrequent commands, and minimize scrolling. (P089)
11. Minimize page-to-page jumps by keeping the structure as flat as possible with broad top-level (global) navigation, elevating frequently used actions for direct access, and structuring the app so the most common 80% of tasks complete on one screen without context switches. (P097)
12. Choose a navigational model to fit the content (hub-and-spoke, fully connected, multilevel/tree, step-by-step, pyramid, pan-and-zoom, or flat), preferring fully-connected short jumps, but switch to a minimal-navigation mode (Back/Next plus an Escape Hatch) when full global navigation would only clutter and distract. (P098)
13. Choose where selected-item details appear by space and use case: Two-Panel Selector (details beside the list, best for overview/browse) for large screens, One-Window Drilldown (details replace the list) for constrained/mobile space, and List Inlay (details expand in place) when users compare items. (P106)
14. Make keyboard shortcuts, tab-order navigation, and direct manipulation available so users can operate without a mouse and act on objects directly (tap, swipe, drag, pinch), and make drag-and-drop work exactly as users expect or the illusion of direct manipulation breaks. (P107)

## Principles applied

- **P004** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P018** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P027** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P046** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P069** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P070** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P072** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P073** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P079** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P089** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P097** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P098** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P106** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P107** (high) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P004, P018, P027, P046, P069, P070, P072, P073, P079, P089, P097, P098, P106, P107, their backing claims and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-report.yaml`.
