---
name: namei-pathname-search
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# namei pathname search

## Purpose

Explain how `namei` (7518) converts a pathname into an inode, component by
component, descending the directory tree. The hard parts are the choice of
starting inode (root vs current directory), the per-component directory scan via
the buffer cache, the handling of `.` / `..` and mount-point crossings, and the
distinction between lookup-for-open and lookup-for-create.

## When to use

- A caller asks how a pathname like `/usr/x` is resolved to an inode.
- A caller asks how directory entries are searched or how `..` and mount points
  are handled during a walk.
- A caller asks why `namei` takes a function argument or a mode, or how it
  reports "not found".

## Procedure

1. **Pick the starting inode.** A leading `/` starts at the root inode;
   otherwise the search starts at the process's current-directory inode. Lock /
   hold that inode (`iget`) as the working directory for the first component.
2. **Extract the next component.** Read the next path component (bounded by the
   directory-entry name length) up to the next `/` or end of string. An empty
   path or a trailing component drives the loop termination.
3. **Scan the current directory.** Read the directory's data blocks through the
   buffer cache (`bread`) and compare each entry's name against the component.
   Account for free (zero-inode) slots, which matter for the create case.
4. **Resolve the component.** On a match, obtain the entry's inode (`iget`),
   release the parent directory inode, and make the found inode the new working
   directory. Handle `.` (same inode) and `..` (parent, including the
   mount-point crossing back to the covered inode).
5. **Branch on the operation.** For lookup, a missing final component is a
   failure (return the not-found indication). For create/delete, remember the
   parent directory and the free slot / entry offset so the caller can complete
   the operation.
6. **Terminate and report.** Return the final inode (locked/held) on success, or
   the not-found result, ensuring no parent inode is left held on any exit path.
   Label any reasoning the source does not state outright.

## Inputs

- The pathname or component scenario, the operation kind (lookup vs create), and
  line references if available.

## Output

A component-by-component trace of the walk: start inode, component extraction,
directory scan through the buffer cache, inode acquisition / release, `.`/`..`
and mount handling, and the operation-dependent termination — with inode
hold/release balance checked and speculation labelled.

## References

- `references/v6-procedure-call-cross-reference.md` — `namei`'s use of `iget`,
  `bread`, and directory routines.
- `references/v6-source-file-index.md` — locate the file-system source.

## Provenance

Tier 0. Derived from the profile `always_on` rules on the V6 file system (inode
structure, buffer cache, directory search `namei`, mount table), the
`advise`/`review` modes, and the source markdown (`namei` 7518). No
principle/claim layer; provenance arrays empty by design.
