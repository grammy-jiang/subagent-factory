---
name: signal-machinery
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# signal machinery

## Purpose

Explain the V6 signal machinery: how a signal is posted to a process with
`psignal` (3963), how a process detects a pending signal with `issig` (3991),
and how it is acted upon with `psig` (4043) — which either terminates the
process (often producing a core image via `core`, 4094) or arranges delivery to
a user handler. The recurring subtlety is *when* a signal is noticed: posting
only records it; the action happens at a controlled point on the way back to user
mode.

## When to use

- A caller asks how a signal is delivered to a process in V6.
- A caller asks the difference between posting (`psignal`), detecting (`issig`),
  and acting (`psig`).
- A caller asks how a signalled process is woken, terminated, or dumped, or how
  a user-mode handler is invoked.

## Procedure

1. **Posting (`psignal`, 3963).** Describe recording the signal number in the
   target's `proc` entry. If the process is asleep at an interruptible priority,
   it is made runnable (`setrun`) so it can notice the signal; a non-
   interruptible sleep is not disturbed. Posting does not itself run the action.
2. **Detection (`issig`, 3991).** Explain that the kernel checks for a pending,
   non-ignored signal at safe points — typically on return from a system call or
   trap, and inside the `sleep` path. `issig` reports whether action is due.
3. **Action (`psig`, 4043).** For a caught signal, arrange a call to the user's
   handler (set up the user stack so execution resumes in the handler and later
   returns). For an uncaught signal, default to termination.
4. **Termination and core (`core`, 4094).** When the signal's default is to
   dump, `core` writes the process image to a `core` file before exit; describe
   the conditions under which a core image is (or is not) produced.
5. **Tie to scheduling and growth.** Note the interaction with `sleep`/`setrun`
   (a signal can break an interruptible sleep) and, where relevant, `grow`
   (4136) for user-stack adjustment when setting up handler delivery.
6. **State the timing invariant.** Signals are *posted* asynchronously but
   *acted on* synchronously at defined kernel exit / sleep points — never mid-
   instruction. Label any reasoning the source does not state outright.

## Inputs

- The routine or scenario (`psignal`/`issig`/`psig` call site, a termination or
  handler-delivery question), with line references if available.

## Output

A trace from post to action: `psignal` recording and conditional wakeup, the
`issig` detection point, the `psig` branch to handler-delivery vs termination,
and `core` dumping — with the post-vs-act timing invariant stated and
speculation labelled.

## References

- `references/v6-procedure-call-cross-reference.md` — links among `psignal`,
  `issig`, `psig`, `core`, `setrun`, `sleep`, `grow`.
- `references/unix-programmer-manual-cross-reference.md` — `signal` system-call
  semantics for the user-visible behaviour.

## Provenance

Tier 0. Derived from the profile `always_on` rules on the process lifecycle and
trap/interrupt dispatch (kernel vs user trap paths), the `advise`/`review`
modes, and the source markdown (TOC: `psignal` 3963, `issig` 3991, `psig` 4043,
`core` 4094, `grow` 4136). No principle/claim layer; provenance arrays empty by
design.
