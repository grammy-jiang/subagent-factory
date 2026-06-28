---
name: build-and-release-automation
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P030
  - P067
  claims:
  - C00315
  - C00317
  - C00320
  - C00321
  - C00133
  - C00319
  - C00325
  source_anchors: []
  authored_from_digest: 1c104e9b903746d5e57dfc1d7cabd8c52cab0b35432ca8e8c13a2c598e99ad8a
---

## Purpose

Make the build, test, and release pipeline fully automated and reproducible: starting from
an empty directory and a known environment it must check out the source, build, run a
complete test suite, and produce a shippable deliverable — all in a single command with no
manual steps and on a regular automated cadence so regressions are caught close to their
cause.

## When to use

- Any step of producing a release currently requires a human to remember or execute a
  manual action.
- The build cannot be reproduced reliably from a clean checkout or an empty directory.
- Tests exist but are not run on a regular automated schedule.
- A regression surfaced long after the change that introduced it.
- Different developer machines produce subtly different build outputs or environments.

## Procedure

### 1. Audit and remove every manual step

Walk the current release path from development through shipping. List every point that
requires a human: hand-edited config files, "remember to run X" steps, manual copy or
upload actions, ad hoc environment setup. Each item is a reliability gap. Replace each
with a scripted equivalent — shell script, makefile target, or scheduled job kept under
source control (C00315). A build that still contains manual steps is not automated.

### 2. Define the from-empty build target

The build must start from an empty directory with only a known environment available.
Enumerate every input the build consumes: source files, metadata, dependency manifests,
version identifiers. Nothing may be silently supplied by a developer's local machine.
The build procedure should check out the latest source, build from a top-level build
definition marked with a version, create the distributable image, and run the tests
(C00320). If this sequence cannot complete unattended, identify and remove the blocker.

### 3. Wire builds and scripts into source control

Build scripts, makefiles, shell scripts, and scheduled-job definitions must live under
source control alongside the production code — not on a shared server drive or a single
developer's workstation (C00133). Source control enables automatic, repeatable builds
that pull the latest source and run unattended without manual copy steps. If a team
member will not adopt this, set up a private repository for the automation you own.

### 4. Integrate the full test run into the build

A complete test run is part of the build, not a separate optional phase. The deliverable
is only shippable once its tests have passed as part of the automated build (C00317).
Wire the test-suite entry point into the build target so that "build" and "test" are a
single command. Failing to do this means tests drift out of sync with the code.

### 5. Schedule frequent automated builds

Run the full build — including all available tests — on a regular cadence such as nightly
(C00321). Frequent runs mean a regression is detected close to the change that caused it.
When tests are run only occasionally, the failure may surface months after the offending
commit, making root cause analysis far harder.

### 6. Guard against test rot and skipped runs

Treat "tests have not been run in a while" as a risk signal. A gap in automated runs
means months of changes accumulated with no regression check (C00321). Surface the last
run date in a visible place — a project dashboard or status page — so the gap cannot go
unnoticed. Automate publication of build results from the repository so the information
stays current (C00325).

### 7. Address dependency blind spots in build tools

If the build uses recursive make, verify that cross-directory dependency relationships are
correctly expressed (C00319). Recursive invocations see only the dependencies within a
single sub-invocation and can miss a needed rebuild or perform unnecessary work. Prefer
a flat or unified dependency graph, or at minimum test the from-empty build in a clean
environment to confirm nothing is silently precomputed.

### 8. Distinguish development builds from release builds

Use a separate target or tagged lock for final ship builds, which may carry different
optimization and debug flags than the development build (C00320). Rerun the full test
suite whenever the product is compiled with different flags than earlier versions. Track
the version identity in the build definition so any release can be regenerated exactly.

### 9. Verify reproducibility

After automating, confirm a clean run on a fresh environment produces the same deliverable
as the previous run. This proves the pipeline depends on nothing outside its declared
inputs. Run this verification on a machine that has never built the project before, or
use a container or VM to isolate the environment.

## Inputs

- The current build and release scripts, and any manual runbook or step-by-step
  instructions used today.
- The test suite entry point and its exit-code behavior.
- The source control system and scheduler (e.g., cron, CI service) available to the team.
- The target environments for the deliverable (compilation flags, runtime dependencies).

## Output

- A from-empty, no-manual-step build definition that includes the test run and is kept
  under source control.
- A scheduled automated build cadence (at minimum nightly).
- A list of removed manual steps with their scripted replacements.
- A record of any remaining reproducibility gaps and the plan to close them.

## References

- `skills/test-harness-structuring/SKILL.md` — the test suite the build must execute.
- `references/pragmatic-tips-70-cheatsheet.md` — Tip: Don't Use Manual Procedures.

## Provenance

Derived from P003 (automate everything the team does with scripted, repeatable tools kept
under source control), P030 (always use source code control for everything, enabling
automatic repeatable builds), and P067 (run a full nightly build executing all available
tests to catch regressions close to their cause). Core claims: C00315 (people are not as
repeatable as computers; use shell scripts and scheduled jobs kept under source control),
C00317 (build with scripted tools so checkout/build/test/ship is a single command),
C00320 (build procedure from empty directory through versioned source to distributable
image and tests), C00321 (nightly full-test builds catch regressions close to their
cause; skipping leaves breakage undiscovered for months), C00133 (source control enables
automatic, repeatable builds that run unattended without manual copy steps), C00319
(recursive make sees only intra-invocation dependencies; guard against missed rebuilds),
C00325 (let the computer do repetitious work; build tools with cron, make, and scripting
languages). Source is distillation-only; all wording is paraphrased.
