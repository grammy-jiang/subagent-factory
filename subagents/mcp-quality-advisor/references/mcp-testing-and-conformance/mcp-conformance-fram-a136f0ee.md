<!--
source_url: https://github.com/modelcontextprotocol/conformance
title: MCP Conformance Test Framework (README + SDK_INTEGRATION + scenario inventory)
fetched: 2026-07-05
source_type: github
rights_status: open
dimension: testing
note: combines README.md + SDK_INTEGRATION.md + AGENTS.md + runner DESIGN + prose inventory of 49 scenarios / 236 declared checks extracted from src/scenarios/ + tier-audit references
-->

# MCP Conformance Test Framework

Combined prose documentation from the MCP conformance repository (github.com/modelcontextprotocol/conformance) — sources #4 (Test Framework README) and #5 (SDK Integration + the test-scenario/spec files enumerating what conformance checks exist). TypeScript implementation code is omitted; the scenario inventory below is a prose extraction of each scenario's purpose and declared conformance checks.


---

## From `README.md` — Conformance test framework overview

# MCP Conformance Test Framework

A framework for testing MCP (Model Context Protocol) client and server implementations against the specification.

**For SDK maintainers:** See [SDK Integration Guide](./SDK_INTEGRATION.md) for a streamlined guide on integrating conformance tests into your SDK repository.

## Quick Start

### Testing Clients

```bash
# Using the everything-client (recommended)
npx @modelcontextprotocol/conformance client --command "tsx examples/clients/typescript/everything-client.ts" --scenario initialize

# Run an entire suite of tests
npx @modelcontextprotocol/conformance client --command "tsx examples/clients/typescript/everything-client.ts" --suite auth
```

### Testing Servers

```bash
# Run all server scenarios (default)
npx @modelcontextprotocol/conformance server --url http://localhost:3000/mcp

# Run a single scenario
npx @modelcontextprotocol/conformance server --url http://localhost:3000/mcp --scenario server-initialize
```

### List Available Scenarios

```bash
npx @modelcontextprotocol/conformance list
```

## Overview

The conformance test framework validates MCP implementations by:

**For Clients:**

1. Starting a test server for the specified scenario
2. Running the client implementation with the test server URL
3. Capturing MCP protocol interactions
4. Running conformance checks against the specification
5. Generating detailed test results

**For Servers:**

1. Connecting to the running server as an MCP client
2. Sending test requests and capturing responses
3. Running conformance checks against server behavior
4. Generating detailed test results

## Usage

### Client Testing

```bash
npx @modelcontextprotocol/conformance client --command "<client-command>" --scenario <scenario-name> [options]
```

**Options:**

- `--command` - The command to run your MCP client (can include flags)
- `--scenario` - The test scenario to run (e.g., "initialize")
- `--suite` - Run a suite of tests in parallel: `all`, `core`, `extensions`, `backcompat`, `auth`, `metadata`, `draft` (scenarios targeting the in-progress draft spec), or `sep-835`
- `--spec-version <version>` - Filter scenarios by spec version (e.g., `2025-11-25`, `2026-07-28`; `draft` is accepted as an alias for the current draft identifier). The draft version selects the latest dated release plus any draft-only scenarios. When omitted, the version is inferred from the scenario's spec applicability (draft-only scenarios run at the draft version, everything else at the latest dated release); an explicitly requested version outside a scenario's applicability window skips the scenario (exit 0) unless `--force` is passed
- `--force` - Run a scenario even if it is not applicable at the requested `--spec-version`
- `--expected-failures <path>` - Path to YAML baseline file of known failures (see [Expected Failures](#expected-failures))
- `--timeout` - Timeout in milliseconds (default: 30000)
- `--verbose` - Show verbose output

The framework appends `<server-url>` as an argument to your command and sets the `MCP_CONFORMANCE_SCENARIO` environment variable to the scenario name. For scenarios that require additional context (e.g., client credentials), the `MCP_CONFORMANCE_CONTEXT` environment variable contains a JSON object with scenario-specific data. When `--spec-version` is passed, its resolved value is forwarded to the client process as `MCP_CONFORMANCE_PROTOCOL_VERSION`; example clients can use this value directly as their `protocolVersion`. SDKs that hard-code their protocol version can ignore it. Clients under test must derive the lifecycle from the protocol version they are asked to run: dated versions through `2025-11-25` use the stateful lifecycle (initialize handshake), while the 2026 draft (`2026-07-28`) uses the stateless lifecycle (per-request `_meta`).

### Server Testing

```bash
npx @modelcontextprotocol/conformance server --url <url> [--scenario <scenario>]
```

**Options:**

- `--url` - URL of the server to test
- `--scenario <scenario>` - Test scenario to run (e.g., "server-initialize"). Runs all available scenarios by default
- `--suite <suite>` - Suite to run: "active" (default; excludes pending and draft-spec scenarios), "all", "draft" (scenarios targeting the in-progress draft spec), or "pending"
- `--expected-failures <path>` - Path to YAML baseline file of known failures (see [Expected Failures](#expected-failures))
- `--verbose` - Show verbose output

## Test Results

**Client Testing** - Results are saved to `results/<scenario>-<timestamp>/`:

- `checks.json` - Array of conformance check results with pass/fail status
- `stdout.txt` - Client stdout output
- `stderr.txt` - Client stderr output

**Server Testing** - Results are saved to `results/server-<scenario>-<timestamp>/`:

- `checks.json` - Array of conformance check results with pass/fail status

## Expected Failures

SDKs that don't yet pass all conformance tests can specify a baseline of known failures. This allows running conformance tests in CI without failing, while still catching regressions.

Create a YAML file listing expected failures by mode:

```yaml
# conformance-baseline.yml
server:
  - tools-call-with-progress
  - resources-subscribe
client:
  - sse-retry
```

Then pass it to the CLI:

```bash
npx @modelcontextprotocol/conformance server --url http://localhost:3000/mcp --expected-failures ./conformance-baseline.yml
```

**Exit code behavior:**

| Scenario Result | In Baseline? | Outcome                                   |
| --------------- | ------------ | ----------------------------------------- |
| Fails           | Yes          | Exit 0 — expected failure                 |
| Fails           | No           | Exit 1 — unexpected regression            |
| Passes          | Yes          | Exit 1 — stale baseline, remove the entry |
| Passes          | No           | Exit 0 — normal pass                      |

This ensures:

- CI passes when only known failures occur
- CI fails on new regressions (unexpected failures)
- CI fails when a fix lands but the baseline isn't updated (stale entries)

## GitHub Action

This repo provides a composite GitHub Action so SDK repos don't need to write their own conformance scripts.

### Server Testing

```yaml
steps:
  - uses: actions/checkout@v4

  # Start your server (SDK-specific)
  - run: |
      my-server --port 3001 &
      timeout 15 bash -c 'until curl -s http://localhost:3001/mcp; do sleep 0.5; done'

  - uses: modelcontextprotocol/conformance@v0.1.11
    with:
      mode: server
      url: http://localhost:3001/mcp
      expected-failures: ./conformance-baseline.yml # optional
```

### Client Testing

```yaml
steps:
  - uses: actions/checkout@v4

  - uses: modelcontextprotocol/conformance@v0.1.11
    with:
      mode: client
      command: 'python tests/conformance/client.py'
      expected-failures: ./conformance-baseline.yml # optional
```

### Action Inputs

| Input               | Required    | Description                                     |
| ------------------- | ----------- | ----------------------------------------------- |
| `mode`              | Yes         | `server` or `client`                            |
| `url`               | Server mode | URL of the server to test                       |
| `command`           | Client mode | Command to run the client under test            |
| `expected-failures` | No          | Path to YAML baseline file                      |
| `suite`             | No          | Test suite to run                               |
| `scenario`          | No          | Run a single scenario by name                   |
| `timeout`           | No          | Timeout in ms for client tests (default: 30000) |
| `verbose`           | No          | Show verbose output (default: false)            |
| `node-version`      | No          | Node.js version (default: 20)                   |

## Example Clients

- `examples/clients/typescript/everything-client.ts` - Single client that handles all scenarios based on scenario name (recommended)
- `examples/clients/typescript/test1.ts` - Simple MCP client (for reference)
- `examples/clients/typescript/auth-test.ts` - Well-behaved OAuth client (for reference)

## Available Scenarios

### Client Scenarios

- **initialize** - Tests MCP client initialization handshake
  - Validates protocol version
  - Validates clientInfo (name and version)
  - Validates server response handling
- **tools-call** - Tests tool invocation
- **auth/basic-dcr** - Tests OAuth Dynamic Client Registration flow
- **auth/basic-metadata-var1** - Tests OAuth with authorization metadata

### Server Scenarios

Run `npx @modelcontextprotocol/conformance list --server` to see all available server scenarios, including:

- **server-initialize** - Tests server initialization and capabilities
- **tools-list** - Tests tool listing endpoint
- **tools-call-\*** - Various tool invocation scenarios
- **resources-\*** - Resource management scenarios
- **prompts-\*** - Prompt management scenarios

## Running Against an SDK at a Specific Ref

The `sdk` subcommand clones an SDK repository at a given ref, builds it, and runs the **local** conformance build against it. This is the inner-loop tool for scenario authors and the basis for cross-SDK CI. Examples below use `npm start --` so they run from source — no `npm run build` between edits.

`--mode client` or `--mode server` is required — each invocation tests exactly one side, so client and server are run (and pass/fail) independently.

```bash
# Run the client conformance suite against typescript-sdk @main (v2)
npm start -- sdk typescript-sdk --mode client

# Run the server conformance suite (separate invocation)
npm start -- sdk typescript-sdk --mode server

# A specific main-line SHA or branch (v2 monorepo)
npm start -- sdk typescript-sdk@abc123f --mode client
npm start -- sdk typescript-sdk@some-branch --mode server

# The published v1.x line — separate entry (npm build), defaults to the v1.x branch
npm start -- sdk typescript-sdk-v1 --mode client
npm start -- sdk typescript-sdk-v1@v1.29.0 --mode server

# Use an existing local checkout (no clone, no fetch)
npm start -- sdk --path ../typescript-sdk --skip-build --mode client

# Narrow to one scenario / suite
npm start -- sdk --path ../typescript-sdk --mode server --scenario server-initialize
npm start -- sdk typescript-sdk --mode client --suite auth

# Target a specific spec version (passed through to the underlying run).
# When omitted, the SDK's `specVersion` from KNOWN_SDKS is used, if set —
# e.g. typescript-sdk-v1 defaults to 2025-11-25.
npm start -- sdk typescript-sdk --mode client --spec-version draft
```

Build/run commands for each official SDK are looked up by name from [`src/sdk-runner/known-sdks.ts`](src/sdk-runner/known-sdks.ts) — no config file is required in the SDK repo. Resolution order is **CLI flag > built-in entry**, so any field can be overridden on the command line for refs that diverge from the built-in.

An SDK can have more than one entry when its layout differs across major versions — e.g. `typescript-sdk` (v2, the `main` monorepo) and `typescript-sdk-v1` (the published npm v1.x line). An entry may set `defaultRef` (the branch used when you don't pass `@<ref>`) and `repo` (the real clone target when the entry name is an alias). Overriding for a one-off ref:

```bash
npm start -- sdk owner/go-sdk@some-branch \
  --mode client \
  --build-cmd 'go build -tags mcp_go_client_oauth -o ./.conformance-client ./conformance/everything-client' \
  --client-cmd './.conformance-client'
```

To add a new SDK to the matrix, add an entry to `KNOWN_SDKS`.

Clones are cached under `.sdk-under-test/` and reused (fetched) on subsequent runs.

## SDK Tier Assessment

The `tier-check` subcommand evaluates an MCP SDK repository against [SEP-1730](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1730) (the SDK Tiering System):

```bash
# Without conformance tests (fastest)
gh auth login
npm run --silent tier-check -- --repo modelcontextprotocol/typescript-sdk --skip-conformance

# With conformance tests (start the everything server first)
npm run --silent tier-check -- \
  --repo modelcontextprotocol/typescript-sdk \
  --conformance-server-url http://localhost:3000/mcp
```

For a full AI-assisted assessment with remediation guide, use Claude Code:

```
/mcp-sdk-tier-audit <local-sdk-path> <conformance-server-url>
```

See [`.claude/skills/mcp-sdk-tier-audit/README.md`](.claude/skills/mcp-sdk-tier-audit/README.md) for full documentation.

## Architecture

See `src/runner/DESIGN.md` for detailed architecture documentation.

### Key Components

- **Runner** (`src/runner/`) - Orchestrates test execution and result generation
  - `client.ts` - Client testing implementation
  - `server.ts` - Server testing implementation
  - `utils.ts` - Shared utilities
  - `index.ts` - Public API exports
- **CLI** (`src/index.ts`) - Command-line interface using Commander.js
- **Scenarios** (`src/scenarios/`) - Test scenarios with expected behaviors
- **Checks** (`src/checks/`) - Conformance validation functions
- **Types** (`src/types.ts`) - Shared type definitions

## Adding New Scenarios

1. Create a new directory in `src/scenarios/<scenario-name>/`
2. Implement the `Scenario` interface with `start()`, `stop()`, and `getChecks()`
3. Register the scenario in `src/scenarios/index.ts`

See `src/scenarios/initialize/` for a reference implementation.


---

## From `SDK_INTEGRATION.md` — Integrating an SDK with the conformance suite

# Using MCP Conformance Tests in SDK Repositories

This guide explains how to integrate the MCP conformance test suite into your language SDK repository. The conformance framework tests your MCP implementation against the protocol specification to ensure compatibility.

## Quick Start

Install and run conformance tests:

```bash
# Client testing (framework starts a test server, runs your client against it)
npx @modelcontextprotocol/conformance client --command "your-client-command" --scenario initialize

# Server testing (your server must already be running)
npx @modelcontextprotocol/conformance server --url http://localhost:3000/mcp --scenario server-initialize
```

## Two Testing Modes

### Client Testing

The framework **starts a test server** and spawns your client against it. Your client receives the server URL as its final command-line argument.

```bash
# Run a single scenario
npx @modelcontextprotocol/conformance client \
  --command "python tests/conformance/client.py" \
  --scenario initialize

# Run a suite of tests
npx @modelcontextprotocol/conformance client \
  --command "python tests/conformance/client.py" \
  --suite auth
```

**Available client suites:** `all`, `core`, `extensions`, `auth`, `metadata`, `sep-835`

Your client should:

1. Accept the server URL as its last argument
2. Read `MCP_CONFORMANCE_SCENARIO` env var to determine which scenario is being tested
3. Read `MCP_CONFORMANCE_CONTEXT` env var for scenario-specific data (e.g., OAuth credentials)

### Server Testing

Your server must be **running before** invoking the conformance tool. The framework connects to it as an MCP client.

```bash
# Start your server first
your-server --port 3001 &

# Then run conformance tests
npx @modelcontextprotocol/conformance server \
  --url http://localhost:3001/mcp \
  --suite active
```

**Available server suites:** `active` (default), `all`, `pending`

**Note:** Server testing requires you to manage server lifecycle (start, health-check, cleanup) yourself.

---

## Expected Failures (Baseline) File

The expected-failures feature lets your CI pass while you work on fixing known issues. It catches regressions by failing when:

- A previously passing test starts failing (regression)
- A previously failing test starts passing (stale baseline - remove the entry)

### File Format

Create a YAML file (e.g., `conformance-baseline.yml`):

```yaml
server:
  - tools-call-with-progress
  - resources-subscribe
client:
  - auth/client-credentials-jwt
```

### Usage

```bash
npx @modelcontextprotocol/conformance server \
  --url http://localhost:3000/mcp \
  --expected-failures ./conformance-baseline.yml
```

### Exit Code Behavior

| Scenario Result | In Baseline? | Exit Code | Meaning                       |
| --------------- | ------------ | --------- | ----------------------------- |
| Fails           | Yes          | 0         | Expected failure              |
| Fails           | No           | 1         | Unexpected regression         |
| Passes          | Yes          | 1         | Stale baseline - remove entry |
| Passes          | No           | 0         | Normal pass                   |

---

## GitHub Action

The conformance repo provides a reusable GitHub Action that handles Node.js setup and conformance execution.

### Client Testing Example

```yaml
name: Conformance Tests
on: [push, pull_request]

jobs:
  conformance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up your SDK
        run: |
          # Your SDK setup (pip install, npm install, etc.)
          pip install -e .

      - uses: modelcontextprotocol/conformance@v0.1.10
        with:
          mode: client
          command: 'python tests/conformance/client.py'
          suite: auth
          expected-failures: ./conformance-baseline.yml
```

### Server Testing Example

```yaml
name: Conformance Tests
on: [push, pull_request]

jobs:
  conformance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up and start server
        run: |
          pip install -e .
          python -m myserver --port 3001 &
          # Wait for server to be ready
          timeout 15 bash -c 'until curl -s http://localhost:3001/mcp; do sleep 0.5; done'

      - uses: modelcontextprotocol/conformance@v0.1.10
        with:
          mode: server
          url: http://localhost:3001/mcp
          suite: active
          expected-failures: ./conformance-baseline.yml
```

### Action Inputs

| Input               | Required    | Description                                     |
| ------------------- | ----------- | ----------------------------------------------- |
| `mode`              | Yes         | `server` or `client`                            |
| `url`               | Server mode | URL of the server to test                       |
| `command`           | Client mode | Command to run the client                       |
| `expected-failures` | No          | Path to YAML baseline file                      |
| `suite`             | No          | Test suite to run                               |
| `scenario`          | No          | Run a single scenario by name                   |
| `timeout`           | No          | Timeout in ms for client tests (default: 30000) |
| `verbose`           | No          | Show verbose output (default: false)            |
| `node-version`      | No          | Node.js version (default: 20)                   |

---

## Writing Conformance Clients/Servers

### Example Client Pattern

See [`src/conformance/everything-client.ts`](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/src/conformance/everything-client.ts) in the TypeScript SDK for a reference implementation. The recommended pattern is a single client that routes behavior based on the scenario:

```python
import os
import sys
import json

def main():
    server_url = sys.argv[-1]  # URL passed as last argument
    scenario = os.environ.get("MCP_CONFORMANCE_SCENARIO", "")
    context = json.loads(os.environ.get("MCP_CONFORMANCE_CONTEXT", "{}"))

    if scenario.startswith("auth/"):
        run_auth_scenario(server_url, scenario, context)
    else:
        run_default_scenario(server_url)

if __name__ == "__main__":
    main()
```

### Example Server Pattern

See [`src/conformance/everything-server.ts`](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/src/conformance/everything-server.ts) in the TypeScript SDK for a reference implementation that handles all server scenarios.

---

## Additional Resources

- [Conformance README](./README.md)
- [Design documentation](./src/runner/DESIGN.md)
- [TypeScript SDK conformance examples](https://github.com/modelcontextprotocol/typescript-sdk/tree/main/src/conformance)


---

## From `AGENTS.md` — Repository guide: scenario structure & how tests run

# AGENTS.md

Guidance for AI agents (and humans) contributing to the MCP conformance test framework.

## What this repo is

A test harness that exercises MCP SDK implementations against the protocol spec. The coverage number that matters here is **spec coverage** — how much of the protocol the scenarios test.

Uses **npm** (not pnpm/yarn). Don't commit `pnpm-lock.yaml` or `yarn.lock`.

## Where to start

**Open an issue first** — whether you've hit a bug in the harness or want to propose a new scenario. For scenarios, sketch which part of the spec you want to cover and roughly how; for bugs, include the command you ran and the output. Either way, a short discussion up front beats review churn on a PR that overlaps existing work or heads in a direction we're not going.

**Don't point an agent at the repo and ask it to "find bugs."** Generic bug-hunting on a test harness produces low-signal PRs (typo fixes, unused-variable cleanups, speculative refactors). If you want to contribute via an agent, give it a concrete target:

- Pick a specific MUST or SHOULD from the [MCP spec](https://modelcontextprotocol.io/specification/) that has no scenario yet, and ask the agent to draft one.
- Pick an [open issue](https://github.com/modelcontextprotocol/conformance/issues) and work on that.

The valuable contribution here is **spec coverage**, not harness polish.

## Scenario design: fewer scenarios, more checks

**The strongest rule in this repo:** prefer one scenario with many checks over many scenarios with one check each.

Why:

- Each scenario often spins up its own HTTP server. These suites run in CI on every push for every SDK, so per-scenario overhead multiplies fast.
- Less code to maintain and update when the spec shifts.
- Progress on making an SDK better shows up as "pass 7/10 checks" rather than "pass 1 test, fail another" — finer-grained signal from the same run.

### Granularity heuristic

Ask: **"Would it make sense for someone to implement a server/client that does just this scenario?"**

If two scenarios would always be implemented together, merge them. Examples:

- `tools/list` + a simple `tools/call` → one scenario
- All content-type variants (image, audio, mixed, resource) → one scenario
- Full OAuth flow with token refresh → one scenario, not separate "basic" + "refresh" scenarios. A client that passes "basic" but not "refresh" just shows up as passing N−2 checks.

Keep scenarios separate when they're genuinely independent features or when they're mutually exclusive (e.g., an SDK should support writing a server that _doesn't_ implement certain stateful features).

### When a PR adds scenarios

- Start with **one end-to-end scenario** covering the happy path with many checks along the way.
- Don't add "step 1 only" and "step 1+2" as separate scenarios — the second subsumes the first.
- Register the scenario in the appropriate suite list in `src/scenarios/index.ts` (`core`, `extensions`, `backcompat`, etc.).

## Check conventions

- **Same `id` for SUCCESS and FAIL.** A check should use one slug and flip `status` + `errorMessage`, not branch into `foo-success` vs `foo-failure` slugs.
- **Optimize for Ctrl+F on the slug.** Repetitive check blocks are fine — easier to find the failing one than to unwind a clever helper.
- Reuse `ConformanceCheck` and other types from `src/types.ts` rather than defining parallel shapes.
- **Don't reimplement the runner.** New subcommands that need to "select scenarios → run them → print summary → compute exit code" must go through the existing `client` / `server` commands (subprocess via `process.execPath` like `tier-check` and `sdk` do) or call shared helpers — never a parallel suite-map / summary loop.
- Include `specReferences` pointing to the relevant spec section.
- **Severity follows the spec keyword:** MUST / MUST NOT → `FAILURE`; SHOULD / SHOULD NOT → `WARNING`. (CI treats WARNING as a failure, so Tier-1 SDKs still need to satisfy SHOULDs — see #245.)
- **A missing prerequisite is a failure, not a skip** (#248). When a check cannot be exercised — the server under test lacks a diagnostic fixture tool, rejects the probe, or advertises a feature it does not serve — report it failed via `notTestable()` / `untestableCheck()` from `src/scenarios/untestable.ts`, with the missing prerequisite named in `errorMessage` and `details.untestable: true`. SKIPPED reads as green in every consumer (pass counts, exit codes, expected-failures), so it is reserved for checks that are legitimately not applicable: an optional capability the server never declared, spec-version inapplicability handled by the runner, or a documented harness gap the suite itself tracks (e.g. `tasks-status-notifications` pending its subscriptions/listen rewrite). The untestable severity follows the underlying requirement's keyword (MUST → `FAILURE`, SHOULD → `WARNING`); the expected-failures baseline is the escape hatch for SDKs that haven't built the fixture yet.

## Descriptions and wording

Be precise about what's **required** vs **optional**. A scenario description that tests optional behavior should make that clear — e.g. "Tests that a client _that wants a refresh token_ handles offline_access scope…" not "Tests that a client handles offline_access scope…". Don't accidentally promote a MAY/SHOULD to a MUST in the prose.

When in doubt about spec details (OAuth parameters, audiences, grant types), check the actual spec in `modelcontextprotocol` rather than guessing.

## Reviewing PRs

### SEP scenarios

Verify requirement levels against the SEP's **spec diff** — the change to `docs/specification/draft/` in the SEP's PR — not the SEP markdown summary or the conformance PR's description. The keyword that governs check severity is the one in the spec text; a bullet under a "Servers SHOULD…" sentence is SHOULD-level even if the SEP's title says "standardize."

```sh
gh api "repos/modelcontextprotocol/modelcontextprotocol/contents/docs/specification/draft/<path>?ref=<sep-branch>" --jq '.content' | base64 -d
```

### Adding a new SEP

Scaffold the requirement-traceability YAML with:

```sh
npx @modelcontextprotocol/conformance new-sep <NNNN>
```

The command looks up PR #`<NNNN>` in `modelcontextprotocol/modelcontextprotocol` (SEP numbers are PR numbers), derives `spec_url` from the `docs/specification/draft/*.mdx` file it changes, and writes `src/seps/sep-<NNNN>.yaml` with TODO `requirements[]` rows. Use `--spec-path` or `--spec-url` to skip the lookup. The `new-sep` Claude Code skill drives the same flow end-to-end, parses the spec diff, and fills in the requirement rows.

### Traceability manifest

`src/seps/traceability.json` is a generated map of, per SEP, which declared `check:` IDs are actually emitted when the conformance suite runs against the reference SDK. It is consumed by plan.modelcontextprotocol.io to track SEP-2484 progress.

The emitted check IDs come from a real suite run (not a source scan), so dynamic (template-literal) IDs resolve to their concrete values. Generate the manifest from a results directory:

```sh
# 1. Run the suite against the reference SDK, collecting checks.json files:
node dist/index.js client --command '<sdk conformance client>' --suite all -o results
node dist/index.js server --url '<sdk conformance server url>' --suite all -o results
# 2. Build the manifest from those results:
npm run traceability -- --results results
npm run traceability -- --results results --strict   # exit 1 on any untested (advisory)
```

Manifest shape: `{ schemaVersion, docs, source, seps }`, where `seps` is keyed by SEP number. Each requirement is `tested` (its check ID was emitted) or `untested` (declared but never emitted — a real gap, or a check that only fires against a deliberately-broken impl, i.e. it needs a negative test). `"tested" means a scenario emitted the check ID, NOT that any SDK passes it` — per-SDK results live in `tier-check`. Matching is exact, so a scenario's emitted check IDs must match the requirement slugs in the yaml (one check ID per MUST/SHOULD, emitted once per case). `source` records what was run against (e.g. `typescript-sdk@<sha>`); the `docs` field points back here.

Contract for consumers (plan.mcp.io): a SEP appears only if it has a traceability yaml or emits `sep-NNNN-*` check IDs. **A SEP absent from the manifest has no conformance artifacts — treat it as not-started** (diff against your own SEP list to find them). `untracked` lists emitted IDs with no yaml row (usually scenario gates).

The manifest is refreshed by `.github/workflows/traceability.yml` (manual/scheduled), which runs the suite against typescript-sdk and opens a PR with the diff — it is **not** a PR gate. Untested checks are advisory for now; the intended future policy is that an untested check must be backed by a negative test.

## Examples: prove it passes and fails

A new scenario should come with:

1. **A passing example** — usually by extending `examples/clients/typescript/everything-client.ts` or the everything-server, not a new file.
2. **A negative test** — a deliberately-broken implementation in `examples/{clients,servers}/typescript/` plus a vitest case asserting the check emits `FAILURE`/`WARNING` against it. See `src/scenarios/client/auth/index.test.ts` and `src/scenarios/server/negative.test.ts` for the pattern. A passing run against the everything-server proves the check doesn't false-positive, but not that it catches anything.

Delete unused example scenarios. If a scenario key in the everything-client has no corresponding test, remove it.

## Don't add new ways to run tests

Use the existing CLI runner (`npx @modelcontextprotocol/conformance client|server ...`). If you need a feature the runner doesn't have, add it to the runner rather than building a parallel entry point.

## Before opening a PR

- `npm run build` passes
- `npm test` passes
- For non-trivial scenario changes, run against at least one real SDK (typescript-sdk or python-sdk) to see actual output. For changes to shared infrastructure (runner, tier-check), test against go-sdk or csharp-sdk too.
- Scenario is registered in the right suite in `src/scenarios/index.ts`
- If you changed a `sep-*.yaml` or scenario check IDs, `src/seps/traceability.json` will drift; the traceability workflow refreshes it via PR (or regenerate locally with `--results` from a suite run)


---

## From `src/runner/DESIGN.md` — Conformance runner design

# Conformance Test Runner Design

## Overview

The conformance test runner is a framework for testing both MCP client and server implementations against the MCP specification. It provides two testing modes:

1. **Client Testing** - Executes client implementations in controlled scenarios and validates their behavior
2. **Server Testing** - Tests server implementations by acting as an MCP client and validating responses

## Architecture

### File Structure

```
src/runner/
├── index.ts      # Exports all public functions
├── client.ts     # Client testing implementation
├── server.ts     # Server testing implementation
└── utils.ts      # Shared utilities (formatting, file I/O, ANSI colors)
```

### Components

**Client Testing:**

1. **Runner** - Orchestrates test execution
2. **Test Server** - MCP server (and optionally auth server for auth scenarios)
3. **Client Process** - The MCP client implementation under test
4. **Scenario** - A specific test case with expected behaviors
5. **Checks** - Validation functions that produce ConformanceCheck results

**Server Testing:**

1. **Runner** - Orchestrates test execution
2. **Test Client** - MCP SDK client that connects to the server under test
3. **Server Process** - The MCP server implementation under test (external)
4. **Scenario** - A specific test case with expected server behaviors
5. **Checks** - Validation functions that produce ConformanceCheck results

### Execution Flow

**Client Testing:**

```
1. Runner starts test server(s) on available port(s)
2. Runner spawns client process with server URL as final argument
3. Server captures MCP interactions
4. Runner captures client stdout/stderr
5. Scenario-specific checks are executed
6. Results are written to results/<scenario>-<timestamp>/
```

**Server Testing:**

```
1. User starts their server implementation
2. Runner connects to server URL as an MCP client
3. Runner sends requests and captures responses
4. Scenario-specific checks validate server behavior
5. Results are written to results/server-<scenario>-<timestamp>/
```

## CLI Interface

The conformance suite provides a unified CLI with two main commands:

### Client Testing

```bash
# Run a single client scenario
npm run start -- client --command "tsx examples/clients/typescript/test1.ts" --scenario initialize

# With verbose output
npm run start -- client --command "tsx examples/clients/typescript/test1.ts" --scenario initialize --verbose

# With custom timeout
npm run start -- client --command "tsx examples/clients/typescript/test1.ts" --scenario initialize --timeout 60000
```

**Arguments:**

- `--command` - The command to run the client (can include existing flags)
- `--scenario` - The scenario to test (e.g., "initialize", "tools-call")
- `--timeout` - Timeout in milliseconds (default: 30000)
- `--verbose` - Show verbose output (JSON format)

The runner will append the server URL as the final argument to the command.

### Server Testing

```bash
# Run a single server scenario
npm run start -- server --url http://localhost:3000/mcp --scenario server-initialize

# Run all server scenarios (default when no --scenario specified)
npm run start -- server --url http://localhost:3000/mcp
```

**Arguments:**

- `--url` - URL of the server to test
- `--scenario <scenario>` - Scenario to test (optional, defaults to all scenarios if not specified)

### List Available Scenarios

```bash
# List all scenarios
npm run start -- list

# List only client scenarios
npm run start -- list --client

# List only server scenarios
npm run start -- list --server
```

## Validation

All CLI arguments are validated using Zod schemas (`src/schemas.ts`) before being passed to runner functions:

**Client Validation:**

- Command is non-empty
- Scenario exists in available scenarios
- Timeout is a positive integer

**Server Validation:**

- URL is a valid HTTP/HTTPS URL
- All specified scenarios exist (if provided)
- Defaults to all scenarios when no `--scenario` is specified

## Scenarios

A scenario represents a specific test case that validates one or more aspects of MCP behavior. Each scenario:

- Configures the test environment with expected behavior
- May run multiple conformance checks
- Validates both request/response patterns and protocol compliance

### Client Scenario Examples

- `initialize` - Tests client initialization handshake
- `tools-call` - Tests tool invocation
- `auth/basic-dcr` - Tests OAuth Dynamic Client Registration flow
- `auth/basic-metadata-var1` - Tests OAuth with authorization metadata variation 1

### Server Scenario Examples

- `server-initialize` - Tests server initialization and capabilities
- `tools-list` - Tests tool listing endpoint
- `tools-call-simple-text` - Tests tool invocation with text response
- `resources-list` - Tests resource listing
- `prompts-list` - Tests prompt listing
- `logging-set-level` - Tests logging level configuration

## Output Structure

Results are written to: `results/<scenario>-<timestamp>/` or `results/server-<scenario>-<timestamp>/`

**Client Testing Files:**

- `checks.json` - Array of ConformanceCheck objects with validation results
- `stdout.txt` - Complete stdout from the client process
- `stderr.txt` - Complete stderr from the client process

**Server Testing Files:**

- `checks.json` - Array of ConformanceCheck objects with validation results

### checks.json Format

```json
[
  {
    "id": "mcp-client-initialization",
    "name": "MCPClientInitialization",
    "description": "Validates that MCP client properly initializes with server",
    "status": "SUCCESS",
    "timestamp": "2024-10-29T14:30:00.000Z",
    "specReferences": [
      {
        "id": "MCP-Lifecycle",
        "url": "https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle"
      }
    ],
    "details": { ... }
  }
]
```

## Programmatic Usage

The runner can also be used programmatically:

```typescript
import { runConformanceTest, printClientResults, runServerConformanceTest, printServerResults } from './runner/index.js';

// Test a client
const clientResult = await runConformanceTest('tsx my-client.ts', 'initialize', 30000);
const { failed } = printClientResults(clientResult.checks);

// Test a server
const serverResult = await runServerConformanceTest('http://localhost:3000/mcp', 'server-initialize');
const { failed } = printServerResults(serverResult.checks);
```

## Shared Utilities

The `utils.ts` module provides shared functionality:

- **File Operations:** `ensureResultsDir()`, `createResultDir()`
- **Formatting:** `formatPrettyChecks()` for colored console output
- **Styling:** ANSI color constants and helpers

## Future Enhancements

- **Test Suites** - Group multiple scenarios for convenience
- **Configurable Timeouts** - Per-scenario timeout configuration
- **Parallel Execution** - Run multiple scenarios concurrently
- **Custom Servers** - Allow custom MCP server implementations for advanced scenarios
- **Report Formats** - HTML, Markdown, or other human-readable formats
- **Watch Mode** - Automatically re-run tests on file changes
- **Coverage Tracking** - Track which parts of the spec are tested


---

## From `src/spec-types/README.md` — Spec types

# spec-types

Vendored copies of `schema/{version}/schema.ts` from the
[modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)
spec repository.

These are the canonical TypeScript types for each protocol version. The
conformance suite imports types from here rather than from
`@modelcontextprotocol/sdk` so that it can test draft spec versions before any
SDK has implemented them.

**Do not edit these files by hand.** To refresh:

```sh
npm run sync-schema -- <sha-or-ref>
```

The `SOURCE` file records the spec commit the current copies came from.

## Import rule

A scenario imports the schema matching its `source.introducedIn`:

```ts
import type { ListToolsResult } from '../../spec-types/2025-06-18';
```

`Connection` implementations import the version whose lifecycle they implement
(stateful → `2025-11-25`, stateless → `draft`).


---

## From `examples/servers/typescript/README.md` — Example conformance target servers

# MCP Conformance Test Server

A reference implementation of an MCP server that implements all features required for conformance testing.

## Features

This server implements:

### Tools

- `test_simple_text` - Returns simple text content
- `test_image_content` - Returns image content (base64 PNG)
- `test_audio_content` - Returns audio content (base64 WAV)
- `test_embedded_resource` - Returns embedded resource
- `test_multiple_content_types` - Returns mixed content types
- `test_tool_with_logging` - Emits log messages during execution
- `test_tool_with_progress` - Reports progress notifications
- `test_error_handling` - Returns error response
- `test_sampling` - Requests LLM completion from client
- `test_elicitation` - Requests user input from client
- `test_dynamic_tool` - Dynamically added/removed tool

### Resources

- `test://static-text` - Static text resource
- `test://static-binary` - Static binary resource (image)
- `test://template/{id}/data` - Resource template with parameter
- `test://watched-resource` - Subscribable resource with updates

### Prompts

- `test_simple_prompt` - Simple prompt without arguments
- `test_prompt_with_arguments(arg1, arg2)` - Parameterized prompt
- `test_prompt_with_embedded_resource(resourceUri)` - Prompt with embedded resource
- `test_prompt_with_image` - Prompt with image content

### Other Capabilities

- Logging at all levels (debug, info, notice, warning, error, critical, alert, emergency)
- Completion support for prompt and resource arguments
- List changed notifications for tools, resources, and prompts
- Resource subscription and update notifications

## Installation

```bash
npm install
```

## Running the Server

```bash
npm start
```

The server will start on `http://localhost:3000` (or the port specified in `PORT` environment variable).

## Endpoints

### MCP Endpoint

- `POST /mcp` - Main MCP protocol endpoint

### Health Check

- `GET /health` - Server health check

## Automatic Behaviors

The server automatically demonstrates dynamic capabilities:

- **Dynamic Tool** - `test_dynamic_tool` is automatically added 2 seconds after server starts
- **Dynamic Resource** - `test://dynamic-resource` is automatically added 2 seconds after server starts
- **Dynamic Prompt** - `test_dynamic_prompt` is automatically added 2 seconds after server starts
- **Resource Updates** - `test://watched-resource` automatically updates every 3 seconds with new content

These behaviors allow testing of MCP notifications without requiring manual triggers.

## Example Usage

### Starting the Server

```bash
npm start
```

### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector http://localhost:3000/mcp
```

### Testing with curl

#### Initialize

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-06-18",
      "capabilities": {},
      "clientInfo": {
        "name": "test-client",
        "version": "1.0.0"
      }
    }
  }'
```

#### List Tools

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
  }'
```

#### Call Tool

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "test_simple_text",
      "arguments": {}
    }
  }'
```

## Conformance Testing

This server implements the MCP Server Conformance Requirements specified in `../../../SERVER_REQUIREMENTS.md`. All tools, resources, and prompts use standardized naming conventions for consistent testing across SDK implementations.

To run conformance tests against this server:

```bash
npx @modelcontextprotocol/conformance server --url http://localhost:3000/mcp
```

## Implementation Notes

- All tool, resource, and prompt names follow the standardized naming conventions (`test_*` for tools/prompts, `test://` for resources)
- Names are descriptive of the feature being tested (e.g., `test_image_content`, `test_tool_with_progress`)
- The server uses the TypeScript MCP SDK (`@modelcontextprotocol/sdk`) high-level API
- Uses `registerTool()`, `registerResource()`, and `registerPrompt()` methods
- Transport is Streamable HTTP (Express) for web-based testing compatibility
- Promise rejections from notifications are caught and handled gracefully

## For SDK Implementers

If you're implementing MCP in another language/SDK:

1. **Read the Requirements**: See `../../../SERVER_REQUIREMENTS.md` for complete specifications
2. **Use This as Reference**: This TypeScript implementation demonstrates all required features
3. **Follow Naming Conventions**: Use exact tool/resource/prompt names specified in requirements
4. **Implement Automatic Behaviors**: Dynamic registration after 2s, resource updates every 3s
5. **Handle Notifications Carefully**: Catch/ignore errors when no client is connected

**Goal**: All SDK example servers provide the same interface, enabling a single test suite to verify conformance across all implementations.

## Negative Test Cases

### no-dns-rebinding-protection.ts

A minimal MCP server that intentionally omits DNS rebinding protection. This is a **negative test case** that demonstrates what a vulnerable server looks like and is expected to **FAIL** the `dns-rebinding-protection` conformance scenario.

```bash
# Run the vulnerable server
npx tsx no-dns-rebinding-protection.ts

# This should FAIL the dns-rebinding-protection checks
npx @modelcontextprotocol/conformance server \
  --url http://localhost:3003/mcp \
  --scenario dns-rebinding-protection
```

**DO NOT** use this pattern in production servers. Always use `createMcpExpressApp()` or the `localhostHostValidation()` middleware for localhost servers.


---

## Conformance scenario & check inventory (extracted from src/scenarios/)

## Conformance scenario inventory (extracted from `src/scenarios/`)

The following enumerates the conformance scenarios/checks defined in this repository. Each entry gives the scenario file, its purpose (from the file's documentation header), and the individual conformance-check assertions it declares. Extracted from scenario definitions; implementation code omitted.

### Client conformance scenarios (server-under-control drives a client-under-test)

#### `client/auth/authorization-server-migration.ts`

SEP-2352 — Authorization-server binding and migration.

The MCP server's PRM initially lists AS₁. The client registers, authorizes,
and calls tools/list. The harness then invalidates the token and flips PRM
to AS₂. On the next 401 the client re-discovers PRM, sees a new issuer, and
MUST re-register with AS₂ rather than reuse AS₁'s client credentials.

Declared conformance checks:
- authorization server has changed

#### `client/auth/basic-cimd.ts`

Fixed client metadata URL that clients should use for CIMD tests.
This URL doesn't need to resolve - the server will accept it as-is
and use hardcoded metadata.

Declared conformance checks:
- Client did not make an authorization request to test CIMD support

#### `client/auth/client-credentials.ts`

Generate an EC P-256 keypair for JWT signing.
Returns both public key (for server verification) and private key PEM (for client signing).

Declared conformance checks:
- Client successfully authenticated with signed JWT assertion
- Client did not make a client_credentials token request
- Missing or invalid Authorization header for Basic auth
- Invalid client credentials
- Client successfully authenticated with client_secret_basic

#### `client/auth/discovery-metadata.ts`

OAuth Metadata Discovery Scenarios

These scenarios test different combinations of PRM and OAuth metadata locations.
The configurations are defined in SCENARIO_CONFIGS below and scenarios are
generated from them.

Declared conformance checks:
- Client requested authorization server at the root path when the AS URL has a path-based location
- Client requested PRM metadata at root location on a server with path-based PRM
- PRM metadata not available at root location

#### `client/auth/enterprise-managed-authorization.ts`

Generate an EC P-256 keypair for IDP ID token signing.

Declared conformance checks:
- IdP only supports token-exchange
- Successfully exchanged IDP ID token for ID-JAG at IdP with all required parameters
- Invalid ID token
- Missing or invalid Authorization header for client_secret_basic authentication
- Malformed Basic auth header (no colon separator)
- Missing assertion in JWT bearer grant
- Successfully verified client auth, ID-JAG claims, and exchanged for access token
- Client did not perform token exchange
- Client did not perform JWT bearer grant exchange

#### `client/auth/issuer-parameter.ts`

Scenario: ISS Parameter Supported (positive)

Server advertises authorization_response_iss_parameter_supported: true and
includes the correct iss value in the authorization redirect. A conformant
client should validate iss and proceed normally.

#### `client/auth/march-spec-backcompat.ts`

Declared conformance checks:
- Client made authorization request to fallback endpoint
- Client requested access token from fallback endpoint
- Client registered with authorization server at fallback endpoint

#### `client/auth/offline-access.ts`

Scenario: Offline Access Scope (SEP-2207)

Tests client behavior when the Authorization Server metadata lists
`offline_access` in `scopes_supported`:

1. Client SHOULD include `refresh_token` in `grant_types` client metadata
   (checked via DCR body or CIMD document, whichever the client uses)
2. Client MAY include `offline_access` in authorization request scope

Setup:
- AS metadata: scopes_supported includes 'offline_access'
- PRM: scopes_supported does NOT include 'offline_access' (per SEP-2207 server guidance)
- Both CIMD and DCR paths available

Declared conformance checks:
- Client used CIMD but metadata URL could not be fetched to verify grant_types
- Client did not use DCR or fetchable CIMD — grant_types could not be inspected
- Client did not complete authorization flow — offline_access scope check could not be performed

#### `client/auth/pre-registration.ts`

Scenario: Pre-registration (static client credentials)

Tests OAuth flow where the server does NOT support Dynamic Client Registration.
Clients must use pre-registered credentials passed via context.

This tests the pre-registration approach described in the MCP spec:
https://modelcontextprotocol.io/specification/draft/basic/authorization#preregistration

Declared conformance checks:
- Client did not use Basic authentication with pre-registered credentials
- Client correctly used pre-registered credentials when server does not support DCR
- Client did not make a token request

#### `client/auth/resource-mismatch.ts`

Scenario: Resource Mismatch Detection

Tests that clients correctly detect and reject when the Protected Resource
Metadata returns a `resource` field that doesn't match the server URL
the client is trying to access.

Per RFC 8707 and MCP spec, clients MUST validate that the resource from
PRM matches the expected server before proceeding with authorization.

Setup:
- Server returns PRM with resource: "https://evil.example.com/mcp" (different origin)
- Client is trying to access the actual server at localhost:<port>/mcp

Expected behavior:
- Client should NOT proceed with authorization
- Client should abort due to resource mismatch
- Test passes if client does NOT complete the auth flow (no authorization request)

#### `client/auth/scope-handling.ts`

Scenario 1: Client uses scope from WWW-Authenticate header

Tests that clients SHOULD follow the scope parameter from the initial
WWW-Authenticate header in the 401 response, per the scope selection strategy.

Declared conformance checks:
- Client did not complete authorization flow - scope check could not be performed
- Missing Authorization header
- Token has insufficient scope
- Client did not make an initial authorization request
- Client did not make a second authorization request for scope escalation
- Client did not make a second authorization request - scope union check could not be performed
- Test is over - client exceeded maximum retry attempts
- Scope upgrade will never succeed
- Client did not make any authorization requests

#### `client/auth/token-endpoint-auth.ts`

Declared conformance checks:
- Client did not make a token request

#### `client/auth/wif-jwt-bearer.ts`

Declared conformance checks:
- Client retried JWT-bearer token request after a failure instead of giving up
- Missing assertion parameter in JWT-bearer token request
- Workload JWT assertion verified — signature, audience, and expiry are valid (iss not validated; keypair is run-scoped)
- Client did not make a JWT-bearer token request

#### `client/elicitation-defaults.ts`

SEP-1034: Elicitation defaults test
Validates that clients properly apply default values for omitted fields
in elicitation responses before sending them to the server

Declared conformance checks:
- Tests that client applies defaults for omitted elicitation fields
- User name
- User age
- User score
- User status
- Verification status
- Client accepts elicitation request
- Client applies string default value for elicitation
- Client applies integer default value for elicitation
- Client applies number default value for elicitation
- Client applies enum default value for elicitation
- Client applies boolean default value for elicitation
- Client handles elicitation with defaults

#### `client/http-custom-headers.ts`

HTTP Custom Headers conformance test scenario for MCP clients (SEP-2243)

Tests that clients correctly handle the `x-mcp-header` extension property:
1. Mirror annotated tool parameter values into `Mcp-Param-{Name}` headers
2. Apply correct value encoding (plain ASCII, Base64 for non-ASCII)
3. Reject tool definitions with invalid `x-mcp-header` annotations

This is a Scenario (acts as a test server that inspects incoming requests
from the client under test).

Declared conformance checks:
- A tool with x-mcp-header annotations to test custom header mirroring and encoding
- Plain ASCII string value
- Integer numeric value
- Boolean value
- Boolean true value
- Empty string value
- Value for header named "Method" — tests that x-mcp-header "Method" produces Mcp-Param-Method (not Mcp-Method)
- Floating point value — no x-mcp-header annotation, should not be mirrored
- Non-ASCII string value — requires Base64 encoding
- String with leading/trailing whitespace — requires Base64 encoding
- String with leading space only — requires Base64 encoding
- String with trailing space only — requires Base64 encoding
- String with internal spaces only — plain ASCII, no Base64
- String with control characters — requires Base64 encoding
- String with carriage return and line feed — requires Base64 encoding
- String with leading tab — requires Base64 encoding
- No x-mcp-header annotation - should not be mirrored
- A tool for testing null/omitted x-mcp-header parameter handling
- Boolean value — will be null to test omission
- No x-mcp-header annotation
- Client supports custom headers: calls the x-mcp-header annotated tool and mirrors at least one parameter
- Client MUST NOT add Mcp-Param headers for parameters without x-mcp-header (number-typed float_val is served unannotated per SEP-2243)
- Client MUST NOT add Mcp-Param headers for parameters without x-mcp-header
- Client MUST omit Mcp-Param header when parameter value is null or not provided
- Client requests tools/list
- Client MUST keep valid tools while excluding invalid ones
- A valid tool with correct x-mcp-header
- x-mcp-header MUST NOT be empty (MUST be rejected by client)
- x-mcp-header MUST only be on primitive types (MUST be rejected)
- Duplicate x-mcp-header "Region" on two properties (MUST be rejected)
- Duplicate case-insensitive x-mcp-header "MyField"/"myfield" (MUST be rejected)
- x-mcp-header MUST NOT contain space (MUST be rejected)
- x-mcp-header MUST NOT contain colon (MUST be rejected)
- x-mcp-header MUST contain only ASCII chars (MUST be rejected)
- x-mcp-header MUST NOT contain control chars (MUST be rejected)

#### `client/http-standard-headers.ts`

HTTP Standard Headers conformance test scenario for MCP clients (SEP-2243)

Tests that clients include the required standard MCP request headers on
Streamable HTTP POST requests:
- `Mcp-Method`: mirrors the `method` field from the JSON-RPC request body
- `Mcp-Name`: mirrors `params.name` or `params.uri` for tools/call,
  resources/read, and prompts/get requests

This is a Scenario (acts as a test server that inspects incoming requests
from the client under test).

Declared conformance checks:
- A simple tool used to test that HTTP headers are sent correctly
- Tool with hyphen in name to test special chars in Mcp-Name header
- Resource URI with percent-encoded spaces
- Resource URI with query string
- A simple prompt for header testing

#### `client/initialize.ts`

_(scenario definition; no extractable description header)_

#### `client/json-schema-ref-deref.ts`

Scenario: JSON Schema network $ref dereferencing (SEP-2106)

SEP-2106 permits the full JSON Schema 2020-12 vocabulary in tool schemas,
including `$ref`. A `$ref` that resolves to a network URI is an SSRF /
fetch-DoS vector: a malicious tool definition could point at internal
infrastructure and have the *client* fetch it during schema processing.

Per SEP-2106, implementations MUST NOT automatically dereference `$ref`
values that resolve to a network URI (anything that is not a same-document
JSON Pointer such as `#/$defs/Foo` or an internal `$anchor`).

This scenario advertises a tool whose inputSchema contains both a
same-document `$ref` and a `$ref` to a canary URL hosted by the scenario
itself. If the client fetches the canary URL at any point before the
scenario stops, the check fails.

Declared conformance checks:
- Look up a user profile by id
- Client never requested tools/list, so $ref handling could not be evaluated

#### `client/mrtr-client.ts`

SEP-2322: MRTR Client Conformance Tests

Tests that clients correctly handle the MRTR (Multi-Round Tool Resolution) flow:
- Echo requestState back unchanged when retrying
- Don't include requestState when server didn't send one
- Use a different JSON-RPC id on retry

The server exposes two tools. The client calls each tool, gets InputRequiredResult,
fulfills the elicitation, and retries. The server verifies correct client behavior.

Declared conformance checks:
- Test tool: triggers MRTR flow with requestState. Client must echo state back unchanged.
- Test tool: triggers MRTR flow WITHOUT requestState. Client must NOT include requestState in retry.
- Test tool: simple tool called between MRTR rounds. Must NOT carry inputResponses or requestState from another tool.
- Test tool: returns a result without resultType. Client must treat it as complete (default).
- Confirm?
- Client MUST echo back the exact value of requestState when retrying
- The JSON-RPC id MUST be different between the initial request and the retry
- If InputRequiredResult does not contain requestState, client MUST NOT include one in the retry
- inputRequests and requestState MUST NOT be used for any other request the client may be sending
- Client MUST assume resultType "complete" when not specified

#### `client/request-metadata.ts`

Severity ranking used to latch per-id check results: a single
non-conformant request is a violation even if later requests are
conformant, so a later better status must never overwrite a worse one.

Declared conformance checks:
- Client sends MCP-Protocol-Version header on every POST
- Client populates _meta on every request with all three required fields
- MCP-Protocol-Version header matches _meta.protocolVersion
- Client retries with a supported version when first choice is rejected

#### `client/sse-retry.ts`

SSE Retry conformance test scenarios for MCP clients (SEP-1699)

Tests that clients properly respect the SSE retry field by:
- Waiting the specified milliseconds before reconnecting
- Sending Last-Event-ID header on reconnection
- Treating graceful stream closure as reconnectable

Declared conformance checks:
- A tool that triggers SSE stream closure to test client reconnection behavior
- Closed tools/call SSE stream to trigger client reconnection
- Client reconnects via GET after SSE stream is closed gracefully
- Client MUST respect the retry field, waiting the given number of milliseconds before attempting to reconnect
- Client MUST respect the retry field timing
- Client SHOULD send Last-Event-ID header on reconnection for resumability

#### `client/tools_call.ts`

Declared conformance checks:
- Add two numbers together
- First number
- Second number
- Validates that the add_numbers tool works correctly

### Server conformance scenarios (harness drives a server-under-test)

#### `server/caching.ts`

Caching (SEP-2549) test scenario for MCP servers

Tests that servers include ttlMs and cacheScope on cacheable results:
tools/list, prompts/list, resources/list, resources/templates/list, resources/read

Declared conformance checks:
- Caching hints scenario failed to connect
- resources/read response includes ttlMs and cacheScope caching hints
- All ttlMs values are non-negative integers
- All cacheScope values are "public" or "private"

#### `server/dns-rebinding.ts`

DNS Rebinding Protection test scenarios for MCP servers

Tests that localhost MCP servers properly validate Host or Origin headers
to prevent DNS rebinding attacks. See GHSA-w48q-cv73-mx4w for details.

Declared conformance checks:
- Server rejects requests with non-localhost Host/Origin headers
- Server accepts requests with valid localhost Host/Origin headers

#### `server/elicitation-defaults.ts`

SEP-1034: Elicitation default values test scenarios for MCP servers

Declared conformance checks:
- Server requests elicitation with default values
- String schema includes default value
- Integer schema includes default value
- Number schema includes default value
- Enum schema includes valid default value
- Boolean schema includes default value

#### `server/elicitation-enums.ts`

SEP-1330: Elicitation enum schema improvements test scenarios for MCP servers

Declared conformance checks:
- Server requests elicitation with enum schemas
- Untitled single-select enum schema uses enum array
- Titled single-select enum schema uses oneOf with const/title
- Legacy titled enum schema uses enumNames (deprecated)
- Untitled multi-select enum schema uses array with items.enum
- Titled multi-select enum schema uses array with items.anyOf

#### `server/http-standard-headers.ts`

HTTP Standard Headers server validation test scenarios (SEP-2243)

Tests that servers properly validate the standard MCP request headers:
- Reject requests where Mcp-Method header doesn't match the body
- Reject requests where Mcp-Name header doesn't match the body
- Accept case variations of header names (case-insensitive)
- Reject case variations of header values (case-sensitive)
- Handle whitespace trimming per HTTP spec
- Validate Base64-encoded custom header values
- Return 400 Bad Request with error code -32020 (HeaderMismatch)

This is a ClientScenario (connects to a server under test and validates
its behavior).

Declared conformance checks:
- Server rejects tools/call where Mcp-Name does not match body params.name
- Server MUST accept leading/trailing whitespace in Mcp-Name value (RFC 9110 §5.5: field parsing MUST exclude OWS before evaluating)
- Server MUST reject tools/call with missing Mcp-Name header when body has params.name
- Setup for header validation tests
- Setup for custom header server validation tests
- Server MUST reject request where custom header is omitted but value is present in body

#### `server/input-required-result.ts`

SEP-2322: InputRequiredResult - Ephemeral Workflow Tests

Tests the ephemeral (stateless) workflow where servers respond with
InputRequiredResult containing inputRequests and/or requestState, and
clients retry with inputResponses and echoed requestState.

Declared conformance checks:
- Server returns InputRequiredResult with elicitation inputRequest
- Server returns complete result after retry with inputResponses
- Server returns InputRequiredResult with sampling inputRequest
- Server returns complete result after retry with sampling response
- Server returns InputRequiredResult with roots/list inputRequest
- Server returns complete result after retry with roots response
- Server returns InputRequiredResult with both inputRequests and requestState
- Server validates echoed requestState and returns complete result
- Server returns InputRequiredResult with multiple inputRequests of different types
- Server returns complete result after all inputResponses are provided
- Round 1: Server returns InputRequiredResult with requestState
- Round 2: Server returns another InputRequiredResult with updated requestState
- Round 3: Server returns complete result
- Server re-requests missing inputResponses via new InputRequiredResult
- prompts/get returns InputRequiredResult with inputRequests
- prompts/get returns complete GetPromptResult after retry with inputResponses
- Server includes resultType field in InputRequiredResult response
- Server does not return InputRequiredResult on unsupported methods
- Server rejects tampered requestState with error
- Server only includes inputRequests for declared client capabilities
- Server ignores extra unrecognized keys in inputResponses
- Server validates InputResponses structure
- Server returns JSON-RPC error for protocol-level input errors

#### `server/json-schema-2020-12.ts`

JSON Schema 2020-12 conformance test scenario (SEP-1613, SEP-2106)

Validates that MCP servers correctly preserve JSON Schema 2020-12 keywords
in tool definitions, ensuring implementations don't strip $schema, $defs,
or additionalProperties fields (SEP-1613).

SEP-2106 broadened inputSchema to permit the full JSON Schema 2020-12
vocabulary alongside the required root `type: "object"`. This scenario also
verifies that composition (allOf/anyOf), conditional (if/then/else), and
reference ($anchor) keywords survive tools/list rather than being stripped.

Declared conformance checks:
- inputSchema.$defs field preserved with expected structure
- inputSchema.additionalProperties field preserved
- inputSchema composition keywords (allOf/anyOf) preserved (SEP-2106)
- inputSchema conditional keywords (if/then/else) preserved (SEP-2106)
- inputSchema reference keyword ($anchor) preserved in $defs (SEP-2106)
- JSON Schema 2020-12 conformance test

#### `server/lifecycle.ts`

Lifecycle test scenarios for MCP servers

Declared conformance checks:
- Server responds to initialize request with valid structure
- Server-provided session ID uses only visible ASCII characters

#### `server/prompts.ts`

Prompts test scenarios for MCP servers

Declared conformance checks:
- Server lists available prompts with valid structure
- Get simple prompt successfully
- Get parameterized prompt with argument substitution
- Get prompt with embedded resource
- Get prompt with image content

#### `server/resources.ts`

Resources test scenarios for MCP servers

Declared conformance checks:
- Server lists available resources with valid structure
- Read text resource successfully
- Read binary resource successfully
- Read resource from template with parameter substitution
- Subscribe to resource successfully
- Server returns -32602 (Invalid Params) for non-existent resource
- Server does not return an empty contents array for a non-existent resource
- Server returns -32602 (Invalid Params) for non-existent resource (SHOULD)
- Server includes the requested URI in the error data field (SHOULD)
- Unsubscribe from resource successfully

#### `server/sse-multiple-streams.ts`

SSE Multiple Streams conformance test scenarios for MCP servers (SEP-1699)

Tests that servers properly support multiple concurrent SSE streams:
- Accepting multiple POST requests that return SSE streams simultaneously
- Each POST request gets its own stream with unique stream ID

Note: The standalone GET stream (without Last-Event-ID) is limited to one per session.
Multiple concurrent streams are achieved via POST requests, each getting their own stream.

Declared conformance checks:
- Server provides session ID for multiple streams test
- Server allows multiple concurrent POST requests (each may return SSE or JSON)
- Multiple POST SSE streams should be functional
- Server returned JSON responses (SSE streams optional)
- Test server multiple SSE streams behavior

#### `server/sse-polling.ts`

SSE Polling conformance test scenarios for MCP servers (SEP-1699)

Tests that servers properly implement SSE polling behavior including:
- Sending priming events with event ID and empty data on POST SSE streams
- Sending retry field in priming events when configured
- Closing SSE stream mid-operation and resuming after client reconnects
- Replaying events when client reconnects with Last-Event-ID

Declared conformance checks:
- Server provides session ID for SSE polling tests
- Server implements test_reconnection tool for SSE polling tests
- Server accepts POST request with SSE stream response
- Server returns text/event-stream for POST request
- Server provides SSE response body
- Server SHOULD send priming event with id and empty data on POST SSE streams
- Server SHOULD send retry field to control client reconnection timing
- Server closes SSE stream mid-call and resumes after client reconnects with Last-Event-ID
- Server supports GET reconnection with Last-Event-ID
- Server closes SSE stream mid-call and resumes after reconnection
- Test server SSE polling behavior

#### `server/stateless.ts`

Stateless MCP test scenarios for MCP servers (SEP-2575)

Declared conformance checks:
- All error responses carry the request JSON-RPC id
- Rejects request with missing _meta with -32602 Invalid params
- Rejects request with _meta missing io.modelcontextprotocol/protocolVersion
- Rejects request with _meta missing io.modelcontextprotocol/clientInfo
- Rejects request with _meta missing io.modelcontextprotocol/clientCapabilities

#### `server/tasks/capability.ts`

SEP-2663 Tasks Extension — capability negotiation conformance.

Tests that the server advertises the io.modelcontextprotocol/tasks
extension correctly, gates the v2 task surface on negotiation, and
supports SEP-2575 per-request capability overrides.

Required server fixtures:
  - greet         — sync-only, returns "Hello, {name}!"
  - slow_compute  — task-supporting, sleeps N seconds

Declared conformance checks:
- Initialize handshakes (with + without extension) succeed

#### `server/tasks/composition.ts`

SEP-2663 + SEP-2322 — MRTR → Tasks composition.

Tests the composition path made normative by SEP-2663 commit 451f5e1:
a tool gathers input via the SEP-2322 MRTR loop on `tools/call`, then
the handler escalates to async on the final round and the server
returns a `CreateTaskResult`. The inlined result of the eventual task
MUST reflect the answer gathered during the MRTR phase, so an
implementation that wires MRTR and tasks as independent surfaces
fails this end-to-end check.

The SEP-2322 ephemeral-MRTR contract (round 1 InputRequiredResult →
round 2 ToolResult) is covered exhaustively by the `input-required-*`
scenarios; only the composition with `CreateTaskResult` on the final
round is SEP-2663-specific, which is why this is the only check in
the tasks suite that drives the MRTR loop end-to-end.

#### `server/tasks/dispatch.ts`

SEP-2663 Tasks Extension — dispatch + envelope conformance.

Bundles a number of small, related checks under one scenario:
  - Removed v1 methods (tasks/result, tasks/list) reject as -32601.
  - Server-directed task creation works without a client `task` hint
    param; legacy v1 `task` param on tools/call is tolerated and
    ignored on sync tools.
  - Immediate-result shortcut: a fast operation MAY skip task creation
    and return a sync ToolResult.
  - SEP-2322 resultType:"complete" discriminator on every non-task
    response (sync tools/call, tasks/get, tasks/update, tasks/cancel).
  - Strong consistency: tasks/get immediately after CreateTaskResult
    MUST resolve.
  - tasks/get with an unknown taskId MUST return -32602.

Required server fixtures:
  - greet           — sync-only
  - slow_compute    — task-supporting (seconds:0 = instant)
  - confirm_delete  — task-supporting, parks for elicitation
  - failing_job     — task-supporting, returns tool error

Declared conformance checks:
- Initialize handshake declaring io.modelcontextprotocol/tasks extension succeeds

#### `server/tasks/headers.ts`

SEP-2243 Mcp-Method / Mcp-Name request-header validation, tasks
surface.

SEP-2243 defines Mcp-Method and Mcp-Name as REQUEST headers (client →
server) used by HTTP infrastructure (proxies, gateways, observability)
to route or shape JSON-RPC traffic without parsing the body. The
server MUST reject requests where the routing headers disagree with
(or are missing for a name-carrying body) the JSON-RPC envelope, with
HTTP 400 + JSON-RPC `-32020 HeaderMismatch`.

This scenario exercises the validation on the tasks surface
specifically — the upstream `http-header-validation` scenario covers
the general case; here we verify mcpkit's tasks/* methods route
through the same validator (matched headers → success; mismatched
header → -32020).

Required server fixtures:
  - greet         — sync-only, returns "Hello, {name}!"
  - slow_compute  — task-supporting, sleeps N seconds

Declared conformance checks:
- Initialize handshake declaring io.modelcontextprotocol/tasks extension succeeds

#### `server/tasks/lifecycle.ts`

SEP-2663 Tasks Extension — server lifecycle conformance.

Tests a server that implements the io.modelcontextprotocol/tasks
extension end-to-end: sync vs async dispatch, DetailedTask shape on
tasks/get, tool errors vs protocol errors, and cancellation
semantics.

Required server fixtures (tools/list output must include all):
  - greet              — sync-only, returns "Hello, {name}!"
  - slow_compute       — task-supporting, sleeps N seconds
  - failing_job        — task-supporting, returns a tool error
  - protocol_error_job — task-supporting, panics into a protocol error

Declared conformance checks:
- Initialize handshake declaring io.modelcontextprotocol/tasks extension succeeds

#### `server/tasks/mrtr-input.ts`

SEP-2322 / SEP-2663 — MRTR input flow on the tasks surface.

Tests the input_required → tasks/update → resume loop, including
partial inputResponses fulfillment when a tool fans out multiple
simultaneous input requests.

Required server fixtures:
  - confirm_delete  — task-supporting, calls TaskElicit once
  - multi_input     — task-supporting, fans out two TaskElicits in
                      parallel so two keys are pending at once

Declared conformance checks:
- Initialize handshake declaring io.modelcontextprotocol/tasks extension succeeds

#### `server/tasks/notifications.ts`

SEP-2663 Tasks Extension — status notifications conformance.

**SKIPPED — pending subscriptions/listen rewrite.** SEP-2663 delivers
`notifications/tasks` over the `subscriptions/listen` stream defined
by SEP-2575, not over the POST SSE response of `tools/call`. This
scenario's harness reads SSE frames off the `tools/call` POST
response, so its observation point misses notifications on servers
that follow the spec — they emit on a stream this harness never
opens.

The scenario is preserved here as a reference point; rewriting the
harness against subscriptions/listen is tracked as a follow-up.

Required server fixtures (for the future re-enabled scenario):
  - slow_compute  — task-supporting, sleeps N seconds.

#### `server/tasks/request-state.ts`

SEP-2663 Tasks Extension — `requestState` absence on the tasks-v2 wire.

SEP-2663 does not define a `requestState` field on the tasks-v2 wire.
This scenario asserts the absence on the two task-bearing message
shapes that a server can populate at task creation and during polling:

  - `CreateTaskResult` MUST NOT carry `requestState`.
  - `DetailedTask` (tasks/get response) MUST NOT carry `requestState`,
    regardless of status.

Why a negative test exists for a field the spec never defines:
SEP-2322 (MRTR) places `requestState` on `InputRequiredResult` — the
same JSON shape slot a fresh implementer might also reach for on the
tasks-v2 `DetailedTask` while reading the two SEPs together. The
absence-assert here catches that cross-SEP confusion. SEP-2322's
`InputRequiredResult.requestState` is unrelated to the tasks-v2 wire
and is exercised by mrtr-input.ts.

Required server fixtures:
  - slow_compute  — task-supporting, sleeps N seconds

Declared conformance checks:
- Initialize handshake declaring io.modelcontextprotocol/tasks extension succeeds
- slow_compute did not return a CreateTaskResult; cannot exercise absence-asserts

#### `server/tasks/required-task-error.ts`

SEP-2663 Tasks Extension — required-task error conformance.

SEP-2575 (Stateless MCP) §"Missing Required Capabilities" defines
the `MissingRequiredClientCapability` JSON-RPC error code (-32021) for
the case where a server cannot service a request without a client
capability the client did not declare. SEP-2663 §"Required
Capabilities" applies that rule to the tasks extension: if a tool's
declared task support is "required" and the client did not declare
`io.modelcontextprotocol/tasks` during `initialize`, the server MUST
reject with that error. The error data
SHOULD carry a `requiredCapabilities` object whose shape mirrors the
`InitializeRequest` capabilities, so the client can self-describe
what to add without needing out-of-band documentation.

This scenario verifies the failure path:
  1. Initialize a session WITHOUT declaring the tasks extension.
  2. Call a tool whose task support is `required`.
  3. Expect a JSON-RPC error with `code: -32021` and
     `data.requiredCapabilities.extensions["io.modelcontextprotocol/tasks"]`
     present.

Required server fixtures:
  - failing_job — a tool registered with task support declared as
                  `required`. The tool's payload behaviour is
                  irrelevant; only the registration-time declaration
                  matters because the error is returned by the
                  middleware before the handler runs.

Declared conformance checks:
- Initialize handshake without the tasks extension capability succeeds

#### `server/tasks/wire-fields.ts`

SEP-2663 Tasks Extension — wire-format / TTL conformance.

Tests the renamed wire fields (ttlMs, pollIntervalMs),
the no-early-TTL-expiry rule, and confirms the v1 `related-task` _meta
key is absent on tasks/get's inlined result (taskId is at root level
already, so the metadata is redundant).

Required server fixtures:
  - slow_compute — task-supporting, sleeps N seconds

Declared conformance checks:
- Initialize handshake declaring io.modelcontextprotocol/tasks extension succeeds

#### `server/tools.ts`

Tools test scenarios for MCP servers

Declared conformance checks:
- Tool names are 1-64 characters and match ^[A-Za-z0-9_./-]+$
- Server lists available tools with valid structure
- Tool returns simple text content
- Tool returns image content
- Tool returns multiple content types
- Tool sends log messages during execution
- Tool returns error correctly
- Tool reports progress notifications
- Tool requests LLM sampling from client
- Tool requests user input from client
- Tool returns audio content
- Tool returns embedded resource content

### Authorization-server conformance scenarios

#### `authorization-server/authorization-code-grant.ts`

Authorization code grant test scenarios for MCP authorization servers

Declared conformance checks:
- Valid authorization code grant

#### `authorization-server/authorization-server-metadata.ts`

Authorization server metadata endpoint test scenarios for MCP authorization servers

Declared conformance checks:
- Valid authorization server metadata response
- Authorization server metadata includes client_id_metadata_document_supported=true (Client ID Metadata Document support)

### Cross-cutting scenarios

#### `untestable.ts`

"Untestable" check policy (issue #248).

A check whose prerequisite is missing — the server under test lacks a
diagnostic fixture tool, rejects the probe that would exercise the
requirement, or advertises a feature it does not actually serve — MUST NOT
report SKIPPED: SKIPPED is excluded from pass/fail counts, exit codes, and
the expected-failures baseline, so the run reads as green and the gap is
invisible to anyone burning down a conformance list. Instead the check
fails, with an errorMessage that names the missing prerequisite, so the
result is red until the prerequisite exists and the scenario can sit in an
expected-failures baseline meanwhile (the documented escape hatch).

SKIPPED remains correct only for checks that are legitimately not
applicable: an optional capability the server never claimed (e.g. a SHOULD
check gated on `prompts.listChanged` the server did not declare), or
spec-version inapplicability handled by the runner.


<!-- inventory: 49 scenario files, 236 extracted check descriptions -->


---

## From `.claude/skills/mcp-sdk-tier-audit/references/feature-list.md` — MCP feature list (audit reference)

# MCP SDK Canonical Feature List

Single source of truth for all MCP features evaluated in the tier audit. **48 non-experimental features** plus 5 experimental (informational only).

When updating this list, also update the total count referenced in `docs-coverage-prompt.md`.

## Non-Experimental Features (48 total)

### Core Features (36)

| #   | Feature                             | Protocol Method                        |
| --- | ----------------------------------- | -------------------------------------- |
| 1   | Tools - listing                     | `tools/list`                           |
| 2   | Tools - calling                     | `tools/call`                           |
| 3   | Tools - text results                |                                        |
| 4   | Tools - image results               |                                        |
| 5   | Tools - audio results               |                                        |
| 6   | Tools - embedded resources          |                                        |
| 7   | Tools - error handling              |                                        |
| 8   | Tools - change notifications        | `notifications/tools/list_changed`     |
| 9   | Resources - listing                 | `resources/list`                       |
| 10  | Resources - reading text            | `resources/read`                       |
| 11  | Resources - reading binary          | `resources/read`                       |
| 12  | Resources - templates               | `resources/templates/list`             |
| 13  | Resources - template reading        |                                        |
| 14  | Resources - subscribing             | `resources/subscribe`                  |
| 15  | Resources - unsubscribing           | `resources/unsubscribe`                |
| 16  | Resources - change notifications    | `notifications/resources/list_changed` |
| 17  | Prompts - listing                   | `prompts/list`                         |
| 18  | Prompts - getting simple            | `prompts/get`                          |
| 19  | Prompts - getting with arguments    | `prompts/get`                          |
| 20  | Prompts - embedded resources        |                                        |
| 21  | Prompts - image content             |                                        |
| 22  | Prompts - change notifications      | `notifications/prompts/list_changed`   |
| 23  | Sampling - creating messages        | `sampling/createMessage`               |
| 24  | Elicitation - form mode             | `elicitation/create`                   |
| 25  | Elicitation - URL mode              | `elicitation/create` (mode: "url")     |
| 26  | Elicitation - schema validation     |                                        |
| 27  | Elicitation - default values        |                                        |
| 28  | Elicitation - enum values           |                                        |
| 29  | Elicitation - complete notification | `notifications/elicitation/complete`   |
| 30  | Roots - listing                     | `roots/list`                           |
| 31  | Roots - change notifications        | `notifications/roots/list_changed`     |
| 32  | Logging - sending log messages      | `notifications/message`                |
| 33  | Logging - setting level             | `logging/setLevel`                     |
| 34  | Completions - resource argument     | `completion/complete`                  |
| 35  | Completions - prompt argument       | `completion/complete`                  |
| 36  | Ping                                | `ping`                                 |

### Transport Features (6)

| #   | Feature                            |
| --- | ---------------------------------- |
| 37  | Streamable HTTP transport (client) |
| 38  | Streamable HTTP transport (server) |
| 39  | SSE transport - legacy (client)    |
| 40  | SSE transport - legacy (server)    |
| 41  | stdio transport (client)           |
| 42  | stdio transport (server)           |

### Protocol Features (6)

| #   | Feature                      |
| --- | ---------------------------- |
| 43  | Progress notifications       |
| 44  | Cancellation                 |
| 45  | Pagination                   |
| 46  | Capability negotiation       |
| 47  | Protocol version negotiation |
| 48  | JSON Schema 2020-12 support  |

## Experimental Features (5, informational only)

| #   | Feature                      | Protocol Method              |
| --- | ---------------------------- | ---------------------------- |
| —   | Tasks - get                  | `tasks/get`                  |
| —   | Tasks - result               | `tasks/result`               |
| —   | Tasks - cancel               | `tasks/cancel`               |
| —   | Tasks - list                 | `tasks/list`                 |
| —   | Tasks - status notifications | `notifications/tasks/status` |


---

## From `.claude/skills/mcp-sdk-tier-audit/references/tier-requirements.md` — SDK conformance tier requirements

# SEP-1730: SDK Tier Requirements Reference

This is the authoritative reference table for MCP SDK tiering requirements, extracted from SEP-1730.

Source: `modelcontextprotocol/docs/community/sdk-tiers.mdx` in the spec repository

## Full Requirements Table

| Requirement                 | Tier 1: Fully Supported                                                                  | Tier 2: Commitment to Full Support                               | Tier 3: Experimental   |
| --------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------- |
| **Conformance Tests**       | 100% pass rate                                                                           | >= 80% pass rate                                                 | No minimum             |
| **New Protocol Features**   | Before new spec version release, timeline agreed per release based on feature complexity | Within 6 months                                                  | No timeline commitment |
| **Issue Triage**            | Within 2 business days                                                                   | Within a month                                                   | No requirement         |
| **Critical Bug Resolution** | Within 7 days                                                                            | Within two weeks                                                 | No requirement         |
| **Stable Release**          | Required with clear versioning                                                           | At least one stable release                                      | Not required           |
| **Documentation**           | Comprehensive with examples for all features                                             | Basic documentation covering core features                       | No minimum             |
| **Dependency Policy**       | Published update policy                                                                  | Published update policy                                          | Not required           |
| **Roadmap**                 | Published roadmap                                                                        | Published plan toward Tier 1 or explanation for remaining Tier 2 | Not required           |

## Exact Thresholds for Automated Checking

| Metric                 | Tier 1 Threshold                                       | Tier 2 Threshold                | How to Measure                                                                           |
| ---------------------- | ------------------------------------------------------ | ------------------------------- | ---------------------------------------------------------------------------------------- |
| Conformance pass rate  | == 100%                                                | >= 80%                          | `passed / (passed + failed) * 100` from conformance suite                                |
| Issue triage time      | <= 2 business days                                     | <= 1 month (30 calendar days)   | Time from issue creation to first label application                                      |
| P0 resolution time     | <= 7 calendar days                                     | <= 14 calendar days             | Time from P0 label application to issue close                                            |
| Stable release version | >= 1.0.0, no pre-release suffix                        | >= 1.0.0 (at least one)         | Check `gh release list` for version matching `^[0-9]+\.[0-9]+\.[0-9]+$` where major >= 1 |
| Documentation coverage | All non-experimental features documented with examples | Core features documented        | Subagent evaluation                                                                      |
| Dependency policy      | Published and findable in repo                         | Published and findable in repo  | Subagent evaluation                                                                      |
| Roadmap                | Published with concrete steps tracking spec components | Published plan toward Tier 1    | Subagent evaluation                                                                      |
| Versioning policy      | Documented breaking change policy                      | N/A (just needs stable release) | Subagent evaluation                                                                      |

## Conformance Score Calculation

Every scenario in the conformance suite has a `specVersions` field indicating which spec version it targets. The valid values are defined as the `SpecVersion` type (as a list) in `src/types.ts` — run `node dist/index.js list` to see the current mapping of scenarios to spec versions.

Date-versioned scenarios (e.g. `2025-06-18`, `2025-11-25`) count toward tier scoring. `draft` and `extension` scenarios are listed separately as informational.

The `--spec-version` CLI flag filters scenarios cumulatively for date versions (e.g. `--spec-version 2025-06-18` includes `2025-03-26` + `2025-06-18`). For `draft`/`extension`, it returns exact matches only.

The tier-check output includes a per-version pass rate breakdown alongside the aggregate.

## Tier Relegation Rules

- **Tier 1 to Tier 2**: Any conformance test fails continuously for 4 weeks
- **Tier 2 to Tier 3**: More than 20% of conformance tests fail continuously for 4 weeks

## Issue Triage Label Taxonomy

SDK repositories must use these consistent labels to enable automated reporting.

### Type Labels (pick one)

| Label         | Description                   |
| ------------- | ----------------------------- |
| `bug`         | Something isn't working       |
| `enhancement` | Request for new feature       |
| `question`    | Further information requested |

Note: Repositories using GitHub's native issue types satisfy this requirement without needing type labels.

### Status Labels (pick one)

| Label                | Description                                             |
| -------------------- | ------------------------------------------------------- |
| `needs confirmation` | Unclear if still relevant                               |
| `needs repro`        | Insufficient information to reproduce                   |
| `ready for work`     | Has enough information to start                         |
| `good first issue`   | Good for newcomers                                      |
| `help wanted`        | Contributions welcome from those familiar with codebase |

### Priority Labels (only if actionable)

| Label | Description                                                     |
| ----- | --------------------------------------------------------------- |
| `P0`  | Critical: core functionality failures or high-severity security |
| `P1`  | Significant bug affecting many users                            |
| `P2`  | Moderate issues, valuable feature requests                      |
| `P3`  | Nice to haves, rare edge cases                                  |

**Total: 12 labels** (3 type + 5 status + 4 priority)

## Key Definitions

### Issue Triage

Labeling and determining whether an issue is valid. This is NOT the same as resolving the issue. An issue is considered triaged when it receives its first label.

### Critical Bug (P0)

- **Security vulnerabilities** with CVSS score >= 7.0 (High or Critical severity)
- **Core functionality failures** that prevent basic MCP operations: connection establishment, message exchange, or use of core primitives (tools, resources, prompts)

### Stable Release

A published version explicitly marked as production-ready. Specifically: version `1.0.0` or higher without pre-release identifiers like `-alpha`, `-beta`, or `-rc`.

### Clear Versioning

Following idiomatic versioning patterns with documented breaking change policies, so users can understand compatibility expectations when upgrading.

### Roadmap

Outlines concrete steps and work items that track implementation of required MCP specification components (non-experimental features and optional capabilities), giving users visibility into upcoming feature support.


---

## From `.claude/skills/mcp-sdk-tier-audit/SKILL.md` — SDK tier-audit methodology

---
name: mcp-sdk-tier-audit
description: >-
  Comprehensive tier assessment for an MCP SDK repository against SEP-1730.
  Produces tier classification (1/2/3) with evidence table, gap list, and
  remediation guide. Works for any official MCP SDK (TypeScript, Python, Go,
  C#, Java, Kotlin, PHP, Swift, Rust, Ruby).
argument-hint: '<local-path> <conformance-server-url> [client-cmd] [--branch <branch>]'
---

# MCP SDK Tier Audit

You are performing a comprehensive tier assessment for an MCP SDK repository against SEP-1730 (the SDK Tiering System). Your goal is to produce a definitive tier classification (Tier 1, 2, or 3) backed by evidence.

## Step 0: Pre-flight Checks

Before doing anything else, verify GitHub CLI authentication:

```bash
gh auth status 2>&1
```

If this fails (exit code non-zero or shows "not logged in"), stop immediately and tell the user:

> GitHub authentication is required for this skill. Please run `gh auth login` first, then re-run the skill.

Do NOT proceed to any other step if this check fails.

After parsing arguments (Step 1), also verify the conformance server is reachable:

```bash
curl -sf <conformance-server-url> -o /dev/null -w '%{http_code}' 2>&1 || true
```

If the server is not reachable, stop and tell the user:

> Conformance server at `<url>` is not reachable. Make sure the everything server is running before invoking this skill.

## Step 1: Parse Arguments

Extract from the user's input:

- **local-path**: absolute path to the SDK checkout (e.g. `~/src/mcp/typescript-sdk`)
- **conformance-server-url**: URL where the SDK's everything server is already running (e.g. `http://localhost:3000/mcp`)
- **client-cmd** (optional): command to run the SDK's conformance client (e.g. `npx tsx test/conformance/src/everythingClient.ts`). If not provided, client conformance tests are skipped and noted as a gap in the report.
- **branch** (optional): Git branch to check on GitHub (e.g. `--branch fweinberger/v1x-governance-docs`). If not provided, derive from the local checkout's current branch: `cd <local-path> && git rev-parse --abbrev-ref HEAD`. This is passed to the tier-check CLI so that policy signal file checks use the correct branch instead of the repo's default branch.

The first two arguments are required. If either is missing, ask the user to provide it.

Derive the GitHub `owner/repo` from the local checkout:

```bash
cd <local-path> && git remote get-url origin | sed 's#.*github.com[:/]##; s#\.git$##'
```

## Step 2: Run the Deterministic Scorecard

The `tier-check` CLI handles all deterministic checks — server conformance, client conformance, labels, triage, P0 resolution, releases, policy signals, and spec tracking. You are already in the conformance repo, so run it directly.

```bash
npm run --silent tier-check -- \
  --repo <owner/repo> \
  --branch <branch> \
  --conformance-server-url <conformance-server-url> \
  --client-cmd '<client-cmd>' \
  --output json
```

If no client-cmd was detected, omit the `--client-cmd` flag (client conformance will be skipped). The `--branch` flag should always be included (derived from the local checkout if not explicitly provided).

The CLI output includes server conformance pass rate, client conformance pass rate (with per-spec-version breakdown), issue triage compliance, P0 resolution times, label taxonomy, stable release status, policy signal files, and spec tracking gap. Parse the JSON output to feed into Step 4.

The conformance results now include a `specVersions` field on each detail entry, enabling per-version pass rate analysis. The `list` command also shows spec version tags: `node dist/index.js list` shows `[2025-06-18]`, `[2025-11-25]`, `[draft]`, or `[extension]` next to each scenario.

### Conformance Baseline Check

After running the CLI, check for an expected-failures baseline file in the SDK repo:

```bash
find <local-path> -name "baseline.yml" -o -name "expected-failures.yml" 2>/dev/null | head -5
```

If found, read the file. It lists known/expected conformance failures. This context is essential for interpreting raw pass rates — a 20% client pass rate due entirely to unimplemented OAuth scenarios is very different from 20% due to broken core functionality.

## Step 3: Launch Parallel Evaluations

Launch 2 evaluations in parallel. Each reads the SDK from the local checkout path.

**IMPORTANT**: Launch both evaluations at the same time (in the same response) so they run in parallel.

### Evaluation 1: Documentation Coverage

Use the prompt from `references/docs-coverage-prompt.md`. Pass the local path.

This evaluation checks:

- Whether all non-experimental features are documented with examples (Tier 1 requirement)
- Whether core features are documented (Tier 2 requirement)
- Produces an evidence table with file:line references

### Evaluation 2: Policy Evaluation

Use the prompt from `references/policy-evaluation-prompt.md`. Pass the local path, the derived `owner/repo`, and the `policy_signals` section from the CLI JSON output.

The CLI has already checked which policy files exist (ROADMAP.md, DEPENDENCY_POLICY.md, dependabot.yml, VERSIONING.md, etc.). The AI evaluation reads only the files the CLI found to judge whether the content is substantive — it does NOT search for files in other locations.

This evaluation checks:

- Dependency update policy (required for Tier 1 and Tier 2)
- Published roadmap (required for Tier 1; plan-toward-Tier-1 for Tier 2)
- Clear versioning with documented breaking change policy (required for Tier 1)
- Produces evidence tables for each policy area

## Step 4: Compute Final Tier

Combine the deterministic scorecard (from the CLI) with the evaluation results (docs, policies). Apply the tier logic:

### Tier 1 requires ALL of:

- Server conformance test pass rate == 100% (date-versioned scenarios only; `draft` and `extension` are informational and not scored)
- Client conformance test pass rate == 100% (date-versioned scenarios only; `draft` and `extension` are informational and not scored)
- Issue triage compliance >= 90% within 2 business days
- All P0 bugs resolved within 7 days
- Stable release >= 1.0.0 with no pre-release suffix
- Clear versioning with documented breaking change policy (evaluation)
- All non-experimental features documented with examples (evaluation)
- Published dependency update policy (evaluation)
- Published roadmap with concrete steps tracking spec components (evaluation)

### Tier 2 requires ALL of:

- Server conformance test pass rate >= 80% (date-versioned scenarios only)
- Client conformance test pass rate >= 80% (date-versioned scenarios only)
- Issue triage compliance >= 80% within 1 month
- P0 bugs resolved within 2 weeks
- At least one stable release >= 1.0.0
- Basic docs covering core features (evaluation)
- Published dependency update policy (evaluation)
- Published plan toward Tier 1 or explanation for remaining Tier 2 (evaluation)

### Otherwise: Tier 3

If any Tier 2 requirement is not met, the SDK is Tier 3.

**Important edge cases:**

- If GitHub issue labels are not set up per SEP-1730, triage metrics cannot be computed. Note this as a gap. However, repos may use GitHub's native issue types instead of type labels — the CLI checks for both.
- If client conformance was skipped (no client command found), note this as a gap but do not block tier advancement based on it alone.

**Conformance Breakdown:**

The **full suite** pass rates (server total, client total) are used for tier threshold checks. To interpret them, present a single conformance matrix combining server and client results. Each detail entry in the tier-check JSON has a `specVersions` field; client category is derived from the scenario name (`auth/` prefix = Auth, everything else = Core). Server scenarios are all Core.

Example:

|              | 2025-03-26 | 2025-06-18 | 2025-11-25 | All\*        |
| ------------ | ---------- | ---------- | ---------- | ------------ |
| Server       | —          | 26/26      | 4/4        | 30/30 (100%) |
| Client: Core | —          | 2/2        | 2/2        | 4/4 (100%)   |
| Client: Auth | 2/2        | 3/3        | 6/11       | 8/16 (50%)   |

Informational (not scored for tier):

|              | draft | extension |
| ------------ | ----- | --------- |
| Client: Auth | 0/1   | 0/2       |

The tier-scoring table only includes date-versioned scenarios. `draft` and `extension` scenarios are shown separately as informational — they do not affect tier advancement.

This immediately shows where failures concentrate. Failures clustered in Client: Auth / `2025-11-25` means "new auth features not yet implemented" — a scope gap, not a quality problem. Failures in Server or Client: Core are more concerning.

If the SDK has a `baseline.yml` or expected-failures file, cross-reference with the matrix to identify whether baselined failures cluster in a specific cell (e.g. all in `2025-11-25` / Client: Auth = scope gap).

**P0 Label Audit Guidance:**

When evaluating P0 metrics, flag potentially mislabeled P0 issues:

- If P0 count is high (>2) but other Tier 2 metrics (conformance, triage compliance, docs) are strong, this may indicate P0 labels are being used for enhancements, lower-priority work, or feature requests rather than actual critical bugs.
- In such cases, recommend a P0 label audit as a remediation action. Review open P0 issues to verify they represent genuine blocking defects vs. misclassified work.
- Document this finding in the remediation output with specific issue numbers and suggested re-triage actions.
- Do not treat high P0 count as an automatic hard blocker if the audit reveals mislabeling; instead, note it as a process improvement opportunity.

## Step 5: Generate Output

Write detailed reports to files using subagents, then show a concise summary to the user.

### Output files (write via subagents)

**IMPORTANT**: Write both report files using parallel subagents (Task tool) so the file-writing work does not pollute the main conversation thread. Launch both subagents at the same time.

Write two files to `results/` in the conformance repo:

- `results/<YYYY-MM-DD>-<sdk-name>-assessment.md`
- `results/<YYYY-MM-DD>-<sdk-name>-remediation.md`

For example: `results/2026-02-11-typescript-sdk-assessment.md`

#### Assessment subagent

Pass all the gathered data (CLI scorecard JSON, docs evaluation results, policy evaluation results) to a subagent and instruct it to write the assessment file using the template from `references/report-template.md`. This file contains the full requirements table, conformance test details (both server and client), triage metrics, documentation coverage table, and policy evaluation evidence.

#### Remediation subagent

Pass all the gathered data to a subagent and instruct it to write the remediation file using the template from `references/report-template.md`. This file always includes both:

- **Path to Tier 2** (if current tier is 3) -- what's needed to reach Tier 2
- **Path to Tier 1** (always) -- what's needed to reach Tier 1

### Console output (shown to the user)

After the subagents finish, output a short executive summary directly to the user:

```
## <sdk-name> — Tier <X>

Conformance:

|              | 2025-03-26 | 2025-06-18 | 2025-11-25 | All* | T2 | T1 |
|--------------|------------|------------|------------|------|----|----|
| Server       | —          | pass/total | pass/total | pass/total (rate%) | ✓/✗ | ✓/✗ |
| Client: Core | —          | pass/total | pass/total | pass/total (rate%) | — | — |
| Client: Auth | pass/total | pass/total | pass/total | pass/total (rate%) | — | — |
| **Client Total** | | | | **pass/total (rate%)** | **✓/✗** | **✓/✗** |

\* unique scenarios — a scenario may apply to multiple spec versions

Informational (not scored for tier):

|              | draft | extension |
|--------------|-------|-----------|
| Client: Auth | pass/total | pass/total |

If a baseline file was found, add a note below the conformance table:
> **Baseline**: {N} failures in `baseline.yml` ({list by cell, e.g. "6 in Client: Auth/2025-11-25, 2 in Client: Auth/extension"}).

Repository Health:

| Check | Value | T2 | T1 |
|-------|-------|----|----|
| Issue Triage | <rate>% (<triaged>/<total>) | ✓/✗ | ✓/✗ |
| Labels | <present>/<required> | ✓/✗ | ✓/✗ |
| P0 Resolution | <count> open | ✓/✗ | ✓/✗ |
| Spec Tracking | <days>d gap | ✓/✗ | ✓/✗ |
| Documentation | <pass>/<total> features | ✓/✗ | ✓/✗ |
| Dependency Policy | <summary> | ✓/✗ | ✓/✗ |
| Roadmap | <summary> | ✓/✗ | ✓/✗ |
| Versioning Policy | <summary> | N/A | ✓/✗ |
| Stable Release | <version> | ✓/✗ | ✓/✗ |

---

**High-Priority Fixes:**
1. <fix description>

**For Tier 2:**
1. <gap description>
2. <gap description>

**For Tier 1:**
1. <gap description>
2. <gap description>

Reports:
- results/<date>-<sdk-name>-assessment.md
- results/<date>-<sdk-name>-remediation.md
```

Use ✓ for pass and ✗ for fail.

**High-Priority Fixes**: List any issues that need urgent attention (e.g., P0 label audit if P0 count is >2 but other metrics are strong, suggesting mislabeled issues). If none, omit this section.

**For Tier 2 / For Tier 1**: List each gap as a separate numbered item. Use "All requirements met" if there are no gaps for that tier. Each item should be a concise action (e.g., "Re-triage mislabeled P0s", "Document 16 undocumented core features").

## Reference Files

The following reference files are available in the `references/` directory alongside this skill:

- `references/feature-list.md` -- Canonical list of 48 non-experimental + 5 experimental features (single source of truth)
- `references/tier-requirements.md` -- Full SEP-1730 requirements table with exact thresholds
- `references/report-template.md` -- Output format template for the audit report
- `references/docs-coverage-prompt.md` -- Evaluation prompt for documentation coverage
- `references/policy-evaluation-prompt.md` -- Evaluation prompt for policy review

Read these reference files when you need the detailed content for evaluation prompts or report formatting.

## Usage Examples

```
# TypeScript SDK — server + client conformance
/mcp-sdk-tier-audit ~/src/mcp/typescript-sdk http://localhost:3000/mcp "npx tsx ~/src/mcp/typescript-sdk/test/conformance/src/everythingClient.ts"

# Python SDK — server + client conformance
/mcp-sdk-tier-audit ~/src/mcp/python-sdk http://localhost:3001/mcp "uv run python ~/src/mcp/python-sdk/.github/actions/conformance/client.py"

# Go SDK — server + client conformance
/mcp-sdk-tier-audit ~/src/mcp/go-sdk http://localhost:3002 "/tmp/go-conformance-client"

# C# SDK — server + client conformance
# Two C#-specific requirements in the client-cmd:
#   --framework net9.0    : required because the project targets net8.0/net9.0/net10.0
#   -- $MCP_CONFORMANCE_SCENARIO : the runner sets this env var and uses shell:true, so the
#                           shell expands it; dotnet passes [scenario, url] to the program
/mcp-sdk-tier-audit ~/src/mcp/csharp-sdk http://localhost:3003 "dotnet run --project ~/src/mcp/csharp-sdk/tests/ModelContextProtocol.ConformanceClient --framework net9.0 -- $MCP_CONFORMANCE_SCENARIO"

# Any SDK — server conformance only (no client)
/mcp-sdk-tier-audit ~/src/mcp/some-sdk http://localhost:3004
```


---

## From `.claude/skills/new-sep/SKILL.md` — Anatomy of adding a new conformance scenario (SEP)

---
name: new-sep
description: >-
  Scaffold a sep-NNNN.yaml requirement-traceability file for the MCP
  conformance repo from a SEP PR's spec diff. Runs the new-sep CLI, then
  parses the modelcontextprotocol/modelcontextprotocol spec diff to populate
  `requirements[]` with the RFC 2119 sentences and proposed check IDs.
argument-hint: '<sep-number>'
---

# new-sep: SEP traceability YAML scaffolding

You are bootstrapping a `sep-NNNN.yaml` file for a new SEP in the MCP conformance repo. The output is the requirement-traceability file specified by SEP-2484: a YAML that maps each normative sentence from the SEP's spec diff to a `check:` ID (testable) or an `excluded:` reason (not testable). The CLI gets the skeleton; you fill in the rows by reading the spec diff.

## Step 0: Pre-flight checks

Before doing anything else, verify GitHub CLI authentication:

```bash
gh auth status 2>&1
```

If this fails, stop immediately and tell the user:

> GitHub authentication is required for this skill. Please run `gh auth login` first, then re-run.

Verify you're running inside the conformance repo:

```bash
test -f package.json && jq -r '.name' package.json
```

The name should be `@modelcontextprotocol/conformance`. If not, stop and ask the user to `cd` into the conformance repo first.

## Step 1: Parse arguments

Extract from the user's input:

- **sep-number** (required): the SEP number, e.g. `2164`. This is also the PR number in `modelcontextprotocol/modelcontextprotocol` by convention.

## Step 2: Generate the skeleton

Run the CLI:

```bash
npm run --silent build
node dist/index.js new-sep <NNNN>
```

(For development against a non-built source tree: `npx tsx src/index.ts new-sep ...`.)

The CLI writes `src/seps/sep-<NNNN>.yaml` with `sep`, `spec_url`, and two TODO `requirements[]` rows. Capture the output path from the CLI's `Wrote …` line and remember it as `$YAML`.

If the CLI errors with "does not change any docs/specification/draft/\*.mdx", the SEP's spec changes landed in a separate PR — ask the user for the spec file path and rerun with `--spec-path docs/specification/draft/<path>`. Do not guess.

## Step 3: Fetch the spec diff

`AGENTS.md` (lines 64–72) is explicit that severity must come from the spec text itself, not the SEP markdown or the conformance PR description:

```bash
gh api "repos/modelcontextprotocol/modelcontextprotocol/pulls/<NNNN>/files" \
  --jq '.[] | select(.filename | test("^docs/specification/draft/.*\\.mdx$")) | {filename, patch}'
```

For each file, pull the added (`+`-prefixed) lines from `patch`. If `patch` is truncated for a large file, fall back to fetching the whole file at the PR's head ref:

```bash
gh api "repos/modelcontextprotocol/modelcontextprotocol/contents/<path>?ref=<sep-branch>" \
  --jq '.content' | base64 -d
```

## Step 4: Extract RFC 2119 requirements

Walk the added lines and identify sentences containing the keywords: **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **MAY**, **OPTIONAL**.

**Quote the whole sentence**, not just the matched line. The matched word may sit inside a bullet point whose lead-in sentence supplies the keyword by inheritance — e.g.:

> Servers SHOULD return standard JSON-RPC errors for common failure cases:
>
> - Resource not found: -32602 (Invalid Params)

The bullet inherits `SHOULD`. The yaml row should quote the _combined_ obligation: `'Servers SHOULD return standard JSON-RPC errors for common failure cases: Resource not found: -32602 (Invalid Params)'` — see `src/seps/sep-2164.yaml` for the canonical example.

**Regex alone is insufficient** (this is called out in Issue #243). Read for context: pronouns, "the server", and "such cases" all refer back to the lead-in.

## Step 5: Map severity → check vs. excluded

From `AGENTS.md:50-56`:

| Keyword                                        | Severity | YAML field                 |
| ---------------------------------------------- | -------- | -------------------------- |
| MUST / MUST NOT / SHALL / SHALL NOT / REQUIRED | FAILURE  | `check: sep-<NNNN>-<slug>` |
| SHOULD / SHOULD NOT                            | WARNING  | `check: sep-<NNNN>-<slug>` |
| MAY / OPTIONAL                                 | —        | _no row — skip entirely_   |

MAY / OPTIONAL sentences are noted in Step 4 only so you consciously skip them — they never produce a yaml row.

A row is `excluded:` when a MUST/SHOULD requirement can't be protocol-observed by the harness. Do **not** write any `excluded:` row on your own authority — every exclusion goes through Step 6.

While classifying, sort each MUST/SHOULD row into one of three buckets:

- **`check:`** — observably testable on the wire.
- **clearly-excluded** — you're confident it can't be observed (e.g. "clients SHOULD also accept -32002" when the harness only drives servers).
- **borderline** — you'd default to `check:` but observability is questionable. Markers:
  - _Internal state_ — verbs like _record_, _store_, _associate_, _track_, _cache_. The harness sees wire traffic, not memory; usually only observable via a downstream row already in your list.
  - _UI / human-facing_ — _display_, _show_, _render_, _prompt the user_.
  - _Precondition phrasing_ — "Before doing X, the implementation MUST Y" where X is itself another row.

Slug convention: lowercase-kebab, derived from the verb phrase. Examples from `sep-2164.yaml`: `no-empty-contents`, `error-code`. Same `id` is used for SUCCESS and FAILURE (`AGENTS.md:52`).

## Step 6: Confirm exclusions with the user

Nothing becomes `excluded:` without sign-off. Two rounds:

**Round 1 — clearly-excluded, single batch question.** One `AskUserQuestion` listing all clearly-excluded rows in the question body (slug + one-line reason each). Options:

- `Exclude all as listed (Recommended)`
- `Flip all to check:`
- `Let me adjust per-row` — if chosen, append these rows to round 2.

Skip this round if the bucket is empty.

**Round 2 — borderline, one question per row.** One `AskUserQuestion` call with a question per borderline row (loop in batches of 4 if needed). For each:

- header: the proposed slug
- question: quote the requirement sentence + your one-line observability concern
- options (list `check:` first — it's the default for borderline):
  - `check:` — keep as a testable check
  - `excluded: <reason>` — drop to excluded with your stated reason
  - `merge into <other-slug>` — offer when the row is a precondition for another row already in the list

Apply the answers before writing. For any `excluded:` outcome, write the reason verbatim into the yaml and add an `issue:` URL if the user supplies one. A `merge` outcome means: drop this row, and append its `text:` to the surviving row's `text:` separated by `/` so the traceability isn't lost.

## Step 7: Rewrite the YAML

Replace the two TODO rows the CLI generated with one row per extracted requirement. Preserve the CLI's quoting style (single quotes, two-space indent — see `src/seps/sep-2164.yaml`).

**Key order within each row** — for `check:` rows the **`check:` key comes first**, then `text:`, then any optional `url:`. Scanning the left margin should reveal every check ID without reading the quoted sentences. For `excluded:` rows the order is **`text:` first**, then `excluded:`, then optional `issue:` — there's no ID to scan for, so lead with the requirement.

**Row order in the file** — all `check:` rows first (in spec-diff order), then **all `excluded:` rows grouped at the bottom**, separated from the checks by **one blank line**. Do not interleave.

```yaml
requirements:
  - check: sep-NNNN-first-slug
    text: '...'
  - check: sep-NNNN-second-slug
    text: '...'

  - text: '...'
    excluded: 'reason'
    issue: https://github.com/modelcontextprotocol/conformance/issues/<NNNN>
```

If a requirement is ambiguous or you're not confident, leave it as a `TODO:` row rather than guessing — humans review this yaml before scenarios get written.

Also fix the `spec_url`: the CLI emits the page URL with no anchor. If the requirements you extracted live under a specific spec subsection (e.g. `#error-handling`), append it.

If a requirement comes from a **different spec page** than `spec_url` (the SEP touched multiple `.mdx` files — the CLI prints these as "PR also changes N other spec file(s)"), give that row a full `url:` override:

```yaml
- check: sep-NNNN-slug
  text: '...'
  url: https://modelcontextprotocol.io/specification/draft/other/page#anchor
```

A row's effective spec reference is `row.url ?? file.spec_url`.

Write the result back to `$YAML`.

## Step 8: Suggest a host scenario

`AGENTS.md` prefers **fewer scenarios with more checks** over one-scenario-per-check. Before telling the user to write a new scenario, look for an existing one the new checks could be folded into.

Determine the suite directory from the requirement subjects ("MCP clients MUST…" → `client/`, "Servers MUST…" → `server/`, "authorization servers MUST…" → `authorization-server/`; a SEP may map to more than one). Then search that directory for scenarios touching the same spec area:

```bash
rg -l -i '<domain-term>|<domain-term-2>' src/scenarios/<suite>/ --type ts
```

Pick 2–3 domain terms from the SEP's subject matter (for a discovery SEP: `metadata`, `well-known`; for an auth-response SEP: `redirect`, `callback`, `pkce`). For each hit, pull the scenario's `name`/`description` to confirm relevance:

```bash
rg -A1 'name:|description:' <hit.ts>
```

If you find a plausible host, recommend it by path. If nothing fits, say so explicitly — a new scenario file is then the right call.

## Step 9: Hand-off

Report to the user, in this order:

1. Path to the generated yaml.
2. Row counts: "`N check:` rows, `M excluded:` rows" — and note which exclusions the user signed off in Step 6.
3. Any requirements you left as `TODO:` and why.
4. **Host-scenario recommendation** from Step 8 — either "consider adding these checks to `src/scenarios/<suite>/<file>.ts` (it already exercises _X_)" or "no existing scenario covers this area; a new file is appropriate".
5. Remaining next steps the user owns:
   - add the checks to the host scenario (or create one) under `src/scenarios/{client,server,authorization-server}/`,
   - register any new scenario in `src/scenarios/index.ts` (`AGENTS.md:48`),
   - add a passing example to the everything-client/server and a negative test, per `AGENTS.md:74-81`.

Do **not** generate or edit scenario `.ts` files or touch `src/scenarios/index.ts`. The skill's scope ends at the yaml plus the recommendation.


---

## From `.claude/skills/review-scenario/SKILL.md` — How conformance scenarios are reviewed

---
name: review-scenario
description: Use when reviewing a conformance PR that adds or changes scenario .ts files for a SEP — before approving, before requesting changes, or as a self-check before opening one.
---

# review-scenario

## What to check

**Spec diff is ground truth.** Pull the SEP's actual spec changes and read the RFC-2119 sentences yourself — don't trust the PR description or SEP summary for keyword levels:

```bash
gh api "repos/modelcontextprotocol/modelcontextprotocol/pulls/<SEP>/files" \
  --jq '.[] | select(.filename | test("^docs/specification/draft/.*\\.mdx$")) | {filename, patch}'
```

If the SEP includes a conformance-test-case table, that table is authoritative for the cases it lists. A table/prose mismatch is a spec gap to flag, not something to silently resolve either way.

**Traceability YAML.** `src/seps/sep-<SEP>.yaml` should exist (run `/new-sep <SEP>` first if not). Diff its rows against the spec sentences you extracted; flag rows that paraphrase rather than quote, claim a keyword level the spec doesn't, or assert something the spec never says. Check IDs follow `sep-<NNNN>-<kebab-slug>`.

**Per-scenario-file:**

- **Spec backing** — would a fully spec-compliant implementation FAIL this check? If yes — or if two compliant SDKs in different languages would get different results — the spec hasn't pinned the behavior; note it as a gap rather than enforce it.
- **Dead checks** — emits FAILURE with no reachable SUCCESS counterpart, or sits behind an always-false guard.
- **Logic** — does a missing/malformed input silently pass? Does the assertion distinguish "rejected for the right reason" from "rejected at all"?

**Coverage.** Count YAML `check:` rows vs how many the PR's scenarios actually exercise; list the gaps.

**Proof it runs.** The PR should reference at least one real implementation the scenario ran green against — the in-repo everything-client/server, or an external SDK via `npx https://pkg.pr.new/@modelcontextprotocol/conformance@<PR>`. No run referenced → ask for one before approving.

**Negative test.** Pins the specific failing slugs, not just `failures.length > 0` (AGENTS.md §Examples: prove it passes and fails).

## Output

This is a first pass for a human reviewer — give them what they need to verify each finding without re-deriving it.

**Open with a summary:** N scenarios added/changed, M distinct check IDs emitted, X/Y YAML `check:` rows covered, and which implementation it was run against.

**Then one bullet per finding.** Each bullet makes its own case — the reviewer should be able to confirm or refute it from the bullet alone:

> **`<check-id>`** — [`file.ts:Lnn`](https://github.com/modelcontextprotocol/conformance/blob/<HEAD-SHA>/path/file.ts#Lnn) — claim. Spec: _"quoted normative sentence"_ ([page#anchor](https://modelcontextprotocol.io/specification/draft/...#anchor)). Consequence: what a compliant impl would do and how this check would mis-report it.

e.g.

> **`client-consistent-version`** — [`stateless.ts:86`](…/blob/abc123/src/scenarios/client/stateless.ts#L86) — no spec backing. Spec: _"Servers MUST NOT rely on prior requests over the same connection to establish context (e.g., capabilities, protocol version)"_ ([lifecycle#stateless](…)). A compliant client may change `protocolVersion` per request; this check FAILs it. The `flippingVersionClient` negative test enforces a non-requirement.

Get `<HEAD-SHA>` once via `gh pr view <PR> --json headRefOid -q .headRefOid` and use it for all permalinks so they don't drift on rebase.

Order: spec-backing → logic/dead → coverage (gap list) → conventions. Put spec gaps in a separate trailing list — those go upstream, not to the PR author.

**Self-review:** fix in place and re-run.

**If asked to push fixes** (stacked diff on top of the PR head): one commit per finding, commit message is the finding. Leave design-level items (scenario count, refactors) as prose.
