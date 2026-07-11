# unix-v6-kernel-source-reviewer

**Version:** 0.1.0 (draft)
**Display name:** UNIX V6 Kernel Source Reviewer

## Purpose

This subagent explains, annotates, and critiques UNIX Sixth Edition (PDP-11)
kernel source code procedures, data structures, and subsystems. It is intended
for developers and students who want grounded, line-traceable commentary on the
V6 kernel — the permanently-resident nucleus as it existed at UNSW in December
1975.

## When to invoke

- To understand what a specific V6 kernel procedure does (e.g. swtch, namei,
  getblk, sleep, wakeup, trap)
- To understand a kernel data structure field (proc, user, inode, buffer flags)
- To walk through a subsystem (process scheduling, buffer cache, file system,
  interrupt handling, memory segmentation)
- To get an explanation of an obscure or apparently anomalous coding pattern
- To interpret PDP-11 assembly conventions as they appear in m40.s or l40.s

## When NOT to invoke

- For UNIX V7, BSD, System III/V, Linux, or any post-V6 kernel
- For user-space programs, shell scripts, or library routines
- For hardware design questions beyond the software-visible PDP-11/40 interface

## Supported modes

| Mode | Purpose |
|------|---------|
| advise | Explain what a procedure or subsystem does and why |
| review | Critique a code passage for correctness or design quality |
| extract | Enumerate data-structure fields, callers, or parameter semantics |

## Source rights

The primary source for this subagent carries `rights_status: proprietary/restricted`.
No verbatim quotation from the source is permitted in any generated output.
All content is distilled and paraphrased from the source material.

## Package layout

```
subagents/unix-v6-kernel-source-reviewer/
  profile.yaml                  canonical profile
  provenance-ledger.md          field-level distillation log
  CHANGELOG.md                  version history
  README.md                     this file
  tests/
    golden-tests.yaml           routing and quality tests
  sources/
    metadata/                   source metadata JSON files
  skills/                       skill stubs (to be written)
  references/                   reference stubs (to be written)
```

## Validation

```bash
python -m tools.subagent_factory.validate_generated_package subagents/unix-v6-kernel-source-reviewer
```
