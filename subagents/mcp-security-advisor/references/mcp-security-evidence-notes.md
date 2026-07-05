---
name: mcp-security-evidence-notes
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P005
  - P007
  - P008
  - P010
  - P012
  - P014
  - P015
  - P016
  - P017
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
  - P036
  - P037
  - P038
  - P039
  - P040
  - P045
  - P046
  - P050
  - P051
  - P052
  - P053
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
  - P099
  - P100
  - P101
  - P102
  - P103
  - P104
  - P105
  - P106
  - P107
  - P108
  - P109
  - P110
  - P111
  - P112
  - P113
  - P114
  - P115
  - P116
  - P117
  - P118
  - P119
  - P120
  - P156
  - P157
  - P158
  - P159
  - P160
  - P161
  - P162
  - P163
  - P164
  - P165
  - P166
  - P167
  - P168
  - P169
  - P170
  - P171
  - P172
  - P173
  - P174
  - P175
  - P176
  - P177
  - P178
  - P179
  - P180
  - P181
  - P182
  - P183
  - P184
  - P185
  - P186
  - P187
  - P188
  - P189
  - P190
  claims:
  - C00002
  - C00003
  - C00006
  - C00007
  - C00008
  - C00010
  - C00017
  - C00018
  - C00019
  - C00020
  - C00023
  - C00024
  - C00028
  - C00029
  - C00040
  - C00043
  - C00046
  - C00047
  - C00054
  - C00056
  - C00058
  - C00059
  - C00061
  - C00062
  - C00066
  - C00067
  - C00076
  - C00077
  - C00078
  - C00085
  - C00094
  - C00095
  - C00102
  - C00103
  - C00110
  - C00111
  - C00113
  - C00114
  - C00118
  - C00119
  evidence:
  - E00001
  - E00002
  - E00005
  - E00006
  - E00007
  - E00009
  - E00010
  - E00011
  - E00012
  - E00013
  - E00016
  - E00017
  - E00021
  - E00022
  - E00033
  - E00034
  - E00035
  - E00036
  - E00042
  - E00044
  - E00046
  - E00047
  - E00049
  - E00050
  - E00054
  - E00055
  - E00064
  - E00065
  - E00066
  - E00072
  - E00076
  - E00077
  - E00084
  - E00085
  - E00091
  - E00092
  - E00094
  - E00095
  - E00097
  - E00098
  source_anchors:
  - 2c66587b05e5-c0000
  - 2c66587b05e5-c0001
  - 2c66587b05e5-c0002
  - 457ef5c30a3b-c0000
  - 457ef5c30a3b-c0002
  - 515304c317e3-c0000
  - 515304c317e3-c0001
  - 515304c317e3-c0002
  - 6954b21807d3-c0000
  - 6ff87e35998d-c0000
  - 8aab528164de-c0000
  - b5eaaf20d167-c0000
  - b5eaaf20d167-c0001
  - c5ec2b54074b-c0000
  - c5ec2b54074b-c0001
  - c82772e8c087-c0000
  - ceb67441a627-c0000
  - ceb67441a627-c0001
  - ceb67441a627-c0003
  - d59e5c41ce9d-c0000
  - d59e5c41ce9d-c0001
  - dcbba5b2c9ad-c0000
  - e6ab8dd9a85c-c0000
  - fa0ccb38ff81-c0000
  - fa0ccb38ff81-c0001
  - fa0ccb38ff81-c0002
  authored_from_digest: 1309bcb6f7e4d89f8fa298d7aef9ae9005eacff07d39e3d112a0dec6b0f5f62f
---

# MCP Security Evidence Notes

Evidence notes for the high-confidence MCP-security principles: each is paired with its backing claims so a reviewer can trace the advisor’s guidance to the distilled source evidence. Sources are distillation-only — paraphrased, never quoted.

## P001 (high confidence)

MCP servers MUST validate every access token per OAuth 2.1 Section 5.2, accept only tokens whose intended audience is the server itself, return HTTP 401 for invalid or expired tokens, and never accept or transit tokens issued for other resources; clients MUST NOT send a server any token not issued by that server's aut…

Backing claims: C00046, C00047, C00048.

## P005 (high confidence)

Pin and reverify MCP server and tool definitions by version, hash, or equivalent integrity check whenever tools are installed, refreshed, or executed.

Backing claims: C00385, C00390, C00410.

## P007 (high confidence)

Deliver Protected Resource Metadata via a WWW-Authenticate resource_metadata parameter on 401 responses or a well-known URI; clients MUST parse WWW-Authenticate headers, react to 401s, prefer the resource_metadata URL when present, and otherwise fall back to the well-known URIs in the specified order.

Backing claims: C00017, C00018, C00021.

## P008 (high confidence)

Bind every MCP authorization decision to the identity of the caller that triggers the invocation, and re-authorize when a new caller interacts; authorization enforced only at the server or resource level, without being scoped to the caller, is insecure.

Backing claims: C00401, C00402, C01176.

## P010 (high confidence)

Treat all tool descriptions, annotations, schemas, and retrieved resource content as untrusted unless obtained from a trusted server, because tool poisoning, full-schema poisoning, resource-content poisoning, typosquatting, and shadow servers can inject malicious behaviour or instructions.

Backing claims: C00145, C00146, C00147.

## P012 (high confidence)

Treat every tool's metadata — its name and natural-language description loaded at MCP registration — as untrusted data, never as instructions the agent may obey; a description must not be able to add steps to a tool's operation or invoke other tools.

Backing claims: C00742, C00744, C00745.

## P014 (high confidence)

Clients MUST implement PKCE (S256 when technically capable) and verify PKCE support before authorizing by checking code_challenge_methods_supported in the authorization-server (or OpenID provider) metadata, refusing to proceed when it is absent; OpenID-Connect-Discovery authorization servers MUST publish this field.

Backing claims: C00061, C00062, C00063.

## P015 (high confidence)

Log tool invocations with their parameters and originating prompt at every layer (host, client, server), centralize cross-cutting logging via MCP gateways or proxies, keep immutable records of actions and authorizations (e.g., IdP token exchange), and use OpenTelemetry for end-to-end linkability.

Backing claims: C00197, C00198, C00203.

## P016 (high confidence)

Validate every tool invocation and model-execution request against well-defined schemas, expected ranges, and the intended execution context (checking malformed inputs, missing fields, and excessive sizes), and block or restrict parameter forwarding when the data source is ambiguous or user-supplied.

Backing claims: C00238, C00259, C00270.

## P017 (high confidence)

Use a cryptographic MCP message envelope to bind JSON-RPC traffic to agent identity, message integrity, timestamp freshness, nonce-based replay resistance, and auditability, while pairing it with application-layer controls for command and context semantics.

Backing claims: C00372, C00373, C00380.

## P019 (high confidence)

Select MCP transport by deployment target: stdio for local servers (low-latency, no network overhead) and HTTP/S with streaming for remote servers (adds standard authentication); do not assume one transport fits both.

Backing claims: C00656, C00657, C00658.

## P020 (high confidence)

MCP proxy servers that use static client IDs MUST obtain user consent for each dynamically registered client before forwarding to third-party authorization servers, to prevent confused-deputy exploitation via stolen authorization codes.

Backing claims: C00076, C00085, C00086.

## P021 (high confidence)

Build on OAuth 2.1 and the referenced RFC subset (RFC 8414, RFC 7591, RFC 9728, Client ID Metadata Documents) rather than inventing bespoke authorization; authorization servers MUST implement OAuth 2.1 with appropriate measures for both confidential and public clients.

Backing claims: C00006, C00010, C00674.

## P022 (high confidence)

Run agents and MCP servers with least privilege, always sandbox any server that touches the host (files, commands, network) or executes LLM-generated code, and do not rely on containers alone as a security boundary—add stronger isolation such as gVisor, Kata Containers, or SELinux sandboxes.

Backing claims: C00179, C00180, C00181.

## P023 (high confidence)

Do not adopt or standardize on the SSE-over-HTTP transport: it is deprecated in the MCP specification (and client migration to the recommended streamable HTTP transport lags), so use streamable HTTP instead.

Backing claims: C00236, C01338, C01339.

## P024 (high confidence)

Treat all contextual and Resource input (documents, pasted text, retrieved content, emails, Slack) as untrusted rather than authoritative, because obfuscated embedded directives can redirect tool calls (indirect prompt injection).

Backing claims: C00428, C00429, C01025.

## P025 (high confidence)

Enforce authentication and authorization at the per-tool level for every tool that can reach a sensitive operation; missing per-tool checks enable unauthorized access to sensitive operations.

Backing claims: C00425, C00426, C01179.

## P026 (high confidence)

Run local MCP servers inside isolation boundaries and restrict their filesystem and network access to the minimum required for their intended function.

Backing claims: C00392, C00393, C00832.

## P027 (high confidence)

Avoid auto-approving command execution in MCP-enabled environments, especially where commands can affect sensitive data, local systems, development workspaces, or production infrastructure.

Backing claims: C00395, C00396, C00747.

## P028 (high confidence)

Gate critical, high-impact, or irreversible actions behind explicit human confirmation before execution (Plan-then-Execute pre-execution gating, with a two-person rule for the highest-impact actions), accepting the efficiency loss for the reduction in harm.

Backing claims: C00435, C00436, C01072.

## P029 (high confidence)

Institute regular red-team and adversarial-testing exercises using external experts or automated attack frameworks to simulate prompt injections and tool tampering, so weaknesses are found and patched before real adversaries exploit them.

Backing claims: C00456, C00457, C01126.

## P030 (high confidence)

Treat MCP context as a boundary-sensitive asset and enforce strict context isolation and lifecycle controls with per-user, per-agent, per-workflow, and per-tenant namespaces, isolated retrieval stores, sensitivity tagging, TTL and purge, pre-storage redaction, approval and preview for sensitive sharing, access logging…

Backing claims: C00358, C00359, C00360.

## P031 (high confidence)

Do not infer authorization correctness from the presence of authorization logic, specific APIs, or framework constructs; authorization state may be cached in memory, held as a global flag, tied to a session, or embedded in initialization logic and then reused, and checks are scattered rather than at fixed APIs — so re…

Backing claims: C01184, C01186, C01187.

## P032 (high confidence)

Enforce strong MCP authentication and authorization with mutual authentication, short-lived scoped and bound tokens, server-side validation, per-request deny-by-default RBAC or ABAC, lifecycle controls, least privilege, centralized IAM and policy decisions, secure endpoint defaults, and immediate credential incident r…

Backing claims: C00333, C00334, C00335.

## P033 (high confidence)

Bound every MCP agent with unique identity, documented least-privilege scopes, policy-as-code enforcement, just-in-time elevation for risky access, continuous entitlement review, runtime guardrails, tamper-evident action logs, and separation of permission-granting from deployment authority.

Backing claims: C00290, C00291, C00292.

## P034 (high confidence)

Preserve MCP intent-flow integrity by anchoring the original user goal, treating retrieved resources and tool outputs as untrusted data, validating every planned action against the goal, using isolated checker or policy-decision controls, and pausing for human re-authentication on intent drift.

Backing claims: C00322, C00323, C00324.

## P036 (high confidence)

Enforce least-privilege secure delegation for MCP servers using OAuth: authenticate users via existing OIDC identity providers, register servers as IAM clients (using Dynamic Client Registration when needed), never pass through user-provided tokens, perform token exchange for accountability, minimize scopes, and use s…

Backing claims: C00151, C00160, C00161.

## P037 (high confidence)

Treat MCP schemas, tool manifests, descriptors, and signed tool definitions as executable contracts: require author identity and signature or hash verification, immutable governed version control, semantic policy checks, provenance logging, schema pinning, revalidation before use, approval for high-impact behavior, an…

Backing claims: C00301, C00302, C00303.

## P038 (high confidence)

Harden according to the deployment pattern: for all-local use stdio transport (which eliminates DNS-rebinding risk) plus sandboxing; for single-tenant remote require client-server authentication, secure OS-keychain/secret-manager credential storage, and authenticated encrypted channels with enforced server allowlists;…

Backing claims: C00206, C00207, C00208.

## P039 (high confidence)

Handle MCP credentials as ephemeral, scoped, vault-backed secrets: inject them only at runtime, keep them out of model context and stored diagnostics, redact sensitive records, audit credential flows, and rotate immediately on suspected exposure.

Backing claims: C00281, C00282, C00283.

## P040 (high confidence)

Make MCP audit and telemetry complete enough for accountability and incident response: capture structured action and context evidence, protect log integrity, forward telemetry to central monitoring, preserve privacy through redaction and encryption, maintain baselines and traces, govern retention and access, and test…

Backing claims: C00345, C00346, C00347.

## P045 (high confidence)

Treat every server-supplied OAuth discovery URL as untrusted and apply SSRF defenses: require HTTPS in production, block private/reserved and cloud-metadata IP ranges, use a vetted library instead of hand-rolled IP validation, apply the same checks to redirect targets, prefer an egress proxy for server-side deployment…

Backing claims: C00102, C00103, C00104.

## P046 (high confidence)

Secure the MCP software supply chain by requiring signed provenance for components, deployment SBOM and cryptographic inventories, pinned approved sources, dependency and code scanning, and sandboxed third-party plugins with constrained network and filesystem access.

Backing claims: C00309, C00310, C00311.

## P050 (high confidence)

Apply conventional security hygiene to MCP components: enforce least privilege to avoid overexposure, validate inputs against command injection and path traversal, add integrity validation to messages and responses, protect stored credentials and tokens, and securely handle transport descriptors.

Backing claims: C00220, C00229, C00230.

## P051 (high confidence)

Because authorization correctness in MCP servers is an execution-time property, complement static analysis with selective dynamic validation: issue controlled invocations to resource-affecting paths and interpret success without an authorization failure as the resource being accessible under existing state, and an exp…

Backing claims: C01227, C01228, C01229.

## P052 (high confidence)

Do not cache or persist authorization state and reuse it across tool invocations without a per-invocation, caller-scoped re-check; one-time authorization combined with server-level trust lets later calls inherit an authorized state regardless of their origin and expands the attack surface.

Backing claims: C01178, C01180, C01183.

## P053 (high confidence)

Recognize that MCP middleware executes tools in its own execution context, so backend services authenticate only the MCP server's identity and cannot see the originating agent or the intent of individual invocations; therefore the MCP layer, not the backend, must attribute and scope authorization.

Backing claims: C01196, C01197, C01198.

## P064 (high confidence)

Enforce transport-layer controls matched to the transport in use: payload limits and integrity checks on all transports; client-server and downstream authentication, mutual TLS, TLS encryption, plus CORS and CSRF protection on HTTP transports; and secure descriptor handling on stdio to prevent MITM, impersonation, rep…

Backing claims: C00156, C00186, C00187.

## P065 (high confidence)

When using Client ID Metadata Documents, host the metadata at an HTTPS URL that contains a path and whose client_id equals the URL exactly, include at least client_id/client_name/redirect_uris, and have the authorization server validate the client_id-URL match, the presented redirect URIs, and that the document is wel…

Backing claims: C00028, C00029, C00030.

## P066 (high confidence)

Protect against open redirection: pre-register redirect URIs, have the authorization server validate them by exact match, avoid redirecting user agents to untrusted URIs (auto-redirecting only trusted ones), and have clients use and verify the state parameter, discarding mismatched or missing state.

Backing claims: C00066, C00067, C00068.

## P067 (high confidence)

Run a strict OAuth state lifecycle: generate a cryptographically random state per request, persist it server-side only after the user approves consent and set the tracking cookie immediately before the third-party redirect, then at the callback require an exact state match, reject missing/mismatched state, and make st…

Backing claims: C00094, C00095, C00096.

## P068 (high confidence)

Close the stdio proxy escalation path by eliminating its enabling vulnerabilities (OAuth URL validation, CSP, input sanitization) and hardening the proxy itself: sandbox/containerize spawned processes, restrict their filesystem access, log stdio usage, require extra authorization for dangerous commands, and isolate pr…

Backing claims: C00126, C00127, C00128.

## P069 (high confidence)

Prioritize review of developer-facing MCP servers: they dominate the ecosystem, expose dense execution interfaces (over 50% insecure), and often aggregate multiple powerful capabilities, so a single authorization failure can escalate into diverse, high-impact outcomes.

Backing claims: C01193, C01242, C01247.

## P070 (high confidence)

Use agent passports, trust levels, capability lists, mutual authentication, revocation, and self-hostable trust authority operations to bind MCP agent identity, permissions, and server acceptance to verifiable credentials.

Backing claims: C00374, C00375, C00376.

## P071 (high confidence)

Use hardware TEEs with remote attestation to isolate MCP clients and servers from compromised hardware, malicious infrastructure operators, and co-tenancy threats, rejecting shadow or compromised servers whose measurements fail attestation, but always complement TEEs with runtime controls because they do not cover vul…

Backing claims: C00174, C00175, C00176.

## P072 (high confidence)

Identify the security-relevant tool entry as the moment a protocol-level tools/call invocation commits to concrete execution — not an exported function or callback — because MCP dispatch is dynamic and implementation-specific (name-to-handler maps, generic dispatchers, layered callbacks, runtime-built handlers, decora…

Backing claims: C01188, C01218, C01219.

## P073 (high confidence)

Prevent cross-tenant leakage through shared efficiency optimizations: sharing key-value caches or vector indexes across tenants creates covert side channels even without an explicit bug (the PROMPTPEEK attack reconstructs another user's prompt token by token from cache hits), so relax separation for efficiency only wi…

Backing claims: C01102, C01103, C01104.

## P074 (high confidence)

Trace the control flow from each tool entry point to every operation that interacts with system, file, network, or physical resources — including sensitive operations reached transitively through helpers or libraries — and along each path determine whether authorization is absent, cached as server-level state, or expl…

Backing claims: C01215, C01217, C01224.

## P075 (high confidence)

Judge an MCP server's security posture from repository signals - project size, lines of code, and commit history - and continuously monitor maintenance: about 21.9% of servers are inactive over a year (an unpatched long tail) and oversized dependency-heavy servers widen the attack surface, while most servers are light…

Backing claims: C01284, C01326, C01327.

## P099 (high confidence)

Treat MCP authorization as optional, but when it is used apply this specification to HTTP-based transports (SHOULD conform), keep STDIO transports on environment-supplied credentials (SHOULD NOT use this flow), and require established security best practices on any other transport.

Backing claims: C00002, C00003, C00004.

## P100 (high confidence)

Enforce authentication and role-based access control (including CRUD-level permissions) on MCP components and bind each session to an identity, since MCP leaves identity and RBAC optional and many implementations omit them.

Backing claims: C00243, C00244, C00245.

## P101 (high confidence)

Do not require an MCP authorization server to own user interface, login, or account storage; it may delegate user authentication and account management to another service.

Backing claims: C00478, C00479, C00480.

## P102 (high confidence)

Clients MUST implement RFC 8707 Resource Indicators and include a resource parameter identifying the target MCP server by its canonical URI in both authorization and token requests, sending it regardless of whether the authorization server supports it, so tokens are bound to their intended resource.

Backing claims: C00040, C00043, C00055.

## P103 (high confidence)

Preserve MCP client bootstrap from a single server URL by using protected-resource metadata to point clients from the MCP resource server to the appropriate authorization server metadata.

Backing claims: C00467, C00468, C00469.

## P104 (high confidence)

Allowlist authorization-URL schemes: permit only http/https (https in production), reject javascript:, data:, file:, vbscript: and other dangerous schemes, and prefer allowlist over blocklist validation to prevent XSS via malicious authorization URLs.

Backing claims: C00118, C00120, C00121.

## P105 (high confidence)

Before securing an MCP system, classify its deployment pattern (all-local, single-tenant hybrid, or multi-tenant cloud) and explicitly map the resulting trust boundaries, because security posture is set by where server code originates, where it executes, and what resources it can reach.

Backing claims: C00140, C00141, C00142.

## P106 (high confidence)

Govern the full MCP server lifecycle: mandatory code-signing and binary authorization before install, private vetted repositories with software-composition analysis, allow-lists with documented reviews, SBOM tracking, hash-pinned dependencies and reproducible builds, a centralized server inventory, automated shadow-de…

Backing claims: C00199, C00200, C00201.

## P107 (high confidence)

Prevent shadow MCP deployments by requiring central registration before deployment, CI/CD gates, owner and compliance metadata, continuous discovery, secure baseline templates, central IAM, service identities, segmentation, anomaly monitoring, developer education, policy signoff, threat-hunting playbooks, and incident…

Backing claims: C00354, C00355, C00356.

## P108 (high confidence)

Account for MCP's inherent architectural weaknesses when threat modeling: centralized credential stores are high-value targets, the spec lacks native fine-grained authorization, LLMs transform but do not sanitize malicious input, and there is no control-plane/data-plane separation so any adversary-controllable input c…

Backing claims: C00215, C00216, C00217.

## P109 (high confidence)

Require identity-bound server authentication and integrity or signature verification, because without them tool shadowing, model-switching, unauthorized context injection, and unverified message modification grant attackers silent control.

Backing claims: C01026, C01027, C01030.

## P110 (high confidence)

Use one unified threat model in which security breaches and safety failures converge: an indirect prompt injection can cause an honestly-mistaken destructive action, and a tool-parameter hallucination can cause a breach, so never triage epistemic errors and unauthorized actions as separate domains.

Backing claims: C01013, C01014, C01016.

## P111 (high confidence)

Treat tools as the primary security boundary: give each tool a single, explicitly bounded purpose, prefer narrow purpose-built tools over powerful general ones (e.g., a prepared statement over arbitrary SQL), and never delegate security-critical validation or constraint enforcement to the LLM.

Backing claims: C00190, C00191, C00192.

## P112 (high confidence)

Make security-relevant elicitations clear about their implications and do not rely solely on the human user; where the risk of dangerous tool execution is unacceptable, enforce host/client configurations that unprivileged users cannot change to keep confirmation prompts enabled, and use server-side elicitation for exp…

Backing claims: C00153, C00194, C00195.

## P113 (high confidence)

Review MCP deployments as agent-mediated security boundaries where model-selected tool calls can reach sensitive systems, not merely as conventional API integrations.

Backing claims: C00382, C00383, C00386.

## P114 (high confidence)

Flag any MCP tool that passes tool parameters into a system-command invocation without authentication, caller verification, or input sanitization: it becomes an unauthenticated remote-command-execution endpoint running at the server process's privilege, and such flaws are observed in real high-star projects. These att…

Backing claims: C01194, C01195, C01257.

## P115 (high confidence)

Defend Tool Poisoning at the pre-execution reasoning stage: screen tool descriptions before they enter the agent's planning context rather than relying on content-based output filtering or model safety alignment, which do not catch TPA (refusal stays under 3%).

Backing claims: C01142, C01169, C01170.

## P116 (high confidence)

Enumerate and test all three attack paradigms when assessing an agent: explicit-trigger function hijacking (P1), implicit-trigger function hijacking (P2), and implicit-trigger parameter tampering (P3); covering only one leaves the others unmeasured.

Backing claims: C01148, C01149, C01150.

## P117 (high confidence)

Interpret MCP ecosystem growth cautiously: measured scale is smaller than raw counts suggest, MCP.so has plateaued, and new growth is driven largely by duplication (via MCP Market) rather than novel projects.

Backing claims: C01280, C01318, C01319.

## P118 (high confidence)

Resolve cross-market MCP entities with multi-feature matching (GitHub URL as strong id, TF-IDF cosine text similarity, author and license, temporal activity) plus content hashing; auto-merge above a threshold and escalate borderline cases to human review - never rely on a single identifier.

Backing claims: C01300, C01302, C01304.

## P119 (high confidence)

Crawl reproducibly and resiliently: rate-limited, robots-aware requests, time-versioned snapshots, rotating IPs, keyword variants, and semi-automated CAPTCHA handling with cookie or session reuse - these lifted coverage about 18% and sustained roughly 36-hour sessions at about 96.7% success.

Backing claims: C01300, C01301, C01314.

## P120 (high confidence)

Treat the MCP ecosystem as transitional - widely adopted in appearance but structurally fragile (over 50% low-value, supply-chain monocultures, uneven maintenance, slow client protocol migration) - and weight advice toward sustainability, server security, and client interoperability.

Backing claims: C01288, C01336, C01351.

## P156 (high confidence)

Gate one-click local MCP server configuration behind explicit, fully transparent consent: show the exact untruncated command, flag it as code execution on the user's machine, require approval with a cancel option, and highlight dangerous patterns and sensitive-path access.

Backing claims: C00113, C00114, C00115.

## P157 (high confidence)

Model the MCP server as an OAuth 2.1 resource server and the MCP client as an OAuth 2.1 client acting for a resource owner, and treat the authorization server as a separable component (co-hosted or standalone) located via metadata.

Backing claims: C00007, C00008, C00009.

## P158 (high confidence)

Follow OAuth 2.1 Section 7 security best practices end to end: implement secure token storage, issue short-lived access tokens, and rotate refresh tokens for public clients.

Backing claims: C00054, C00056, C00057.

## P159 (high confidence)

Advertise required scopes in the WWW-Authenticate scope parameter; clients MUST treat the challenge scopes as authoritative for the current request, MUST NOT assume any subset/superset relationship to scopes_supported, and MUST apply the scope-selection fallback when no scope is provided.

Backing claims: C00019, C00020, C00022.

## P160 (high confidence)

When discovering authorization-server metadata, clients MUST probe multiple well-known endpoints in the defined priority order, which differs depending on whether the issuer URL includes a path component.

Backing claims: C00023, C00024, C00025.

## P161 (high confidence)

Enforce communication security: serve all authorization-server endpoints over HTTPS, restrict every redirect URI to localhost or HTTPS, and follow OAuth 2.1 Section 1.5.

Backing claims: C00058, C00059, C00060.

## P162 (high confidence)

Never accept mis-audienced tokens or pass a client-supplied token through to downstream services: audience-validation failure lets attackers reuse tokens across services and token passthrough creates confused-deputy exposure.

Backing claims: C00077, C00078, C00082.

## P163 (high confidence)

When sessions are used for state, make session IDs secure random values (e.g., UUIDs from a CSPRNG), bind them to user-specific identity such as <user_id>:<session_id>, and rotate or expire them to limit hijacking impact.

Backing claims: C00110, C00111, C00112.

## P164 (high confidence)

Open authorization URLs without a shell: never invoke cmd.exe/sh/PowerShell to open URLs, use platform non-shell openers, and web clients should apply a restrictive CSP (script-src/default-src 'self') to block injected JavaScript and command injection.

Backing claims: C00119, C00123, C00124.

## P165 (high confidence)

Continuously detect and eliminate shadow, zombie, and malicious MCP servers through automated discovery, a centralized inventory, and decommissioning, because absent provenance and inventory controls attackers deploy unauthorized servers and distribute malicious or rug-pull packages that introduce unvetted capabilitie…

Backing claims: C00225, C00226, C00233.

## P166 (high confidence)

Establish explicit trust boundaries/zones between MCP components, gate dynamic tool discovery behind origin verification or authorization, align tools and models to data-classification zones, prefer local MCP servers for private data, and control egress via a filtering proxy or DLP.

Backing claims: C00267, C00268, C00269.

## P167 (high confidence)

Separate sensitive MCP servers from general-purpose servers so payment, authentication, and personal-data capabilities are not exposed to broad shared contexts.

Backing claims: C00394, C00413, C00414.

## P168 (high confidence)

Treat each connected MCP server as a separate untrusted security domain and monitor or mediate cross-server data flows.

Backing claims: C00383, C00413, C00414.

## P169 (high confidence)

Treat every MCP integration as a privilege-execution boundary, not a passive text interface: MCP turns the LLM into an active system component with shell-level privileges acting on untrusted context, and the attack surface grows with each connected file, database, or API.

Backing claims: C01011, C01012, C01036.

## P170 (high confidence)

Verify MCP server provenance before deployment: require developers to publish code signatures and SBOMs, verify contents and signatures against an approved-source and signing-key policy, protect all data in transit with TLS, and prefer end-to-end signatures proving authenticity of returned resources.

Backing claims: C00183, C00184, C00185.

## P171 (high confidence)

Strictly validate and sanitize every input with allowlists at each trust boundary (path canonicalization, parameterized queries, context-aware output encoding for SQL/shell/HTML), treat AI-generated content as untrusted requiring the same validation, and deploy prompt-injection detection with strict schemas across all…

Backing claims: C00170, C00171, C00173.

## P172 (high confidence)

Secure MCP deployments with defense-in-depth—zero-trust architecture, hardware isolation via TEEs, rigorous supply-chain vetting, and continuous monitoring—because documented incidents show that failures of authentication, session management, and supply-chain control are active, not theoretical, threats.

Backing claims: C00157, C00204, C00205.

## P173 (high confidence)

Do not rely on MCP protocol guarantees for security; enforce it through implementation rigor and standard external controls (reverse proxies, middleware firewalls, application sandboxing/containment), because the protocol cannot enforce security principles itself.

Backing claims: C00239, C00249, C00265.

## P174 (high confidence)

Enforce resource-consumption controls—token, context-size, and API-call quotas plus cost management—to prevent resource-exhaustion denial of service and denial-of-wallet, since the protocol specifies none by default.

Backing claims: C00154, C00223, C00224.

## P175 (high confidence)

Apply traditional controls (authentication, authorization, input validation) AND explicitly address agentic-specific risks—dynamic tool invocation, implicit trust between agents, and shared/overlapping context—across the entire lifecycle rather than at endpoints alone.

Backing claims: C00240, C00241, C00242.

## P176 (high confidence)

Execute agent-produced commands, queries, file operations, and API calls only through validated tool boundaries that use allowlists, metacharacter rejection, path normalization, structured APIs, parameterization, sandboxing, least privilege, secret isolation, approval for sensitive actions, and immutable call logging.

Backing claims: C00316, C00317, C00318.

## P177 (high confidence)

Enforce token and session lifecycle management—expiration, rotation, revocation, reuse/replay control, and idempotency—rather than relying on MCP's optional authorization and unmanaged OAuth 2.1 bearer tokens.

Backing claims: C00251, C00252, C00253.

## P178 (high confidence)

Design MCP servers so the initialize phase is the sole entry point for session creation: bind the OAuth token, caller identity (for example client_id), and connection context into an isolated per-connection session, verify the caller identity at initialization and reject a mismatch, and authorize each subsequent tools…

Backing claims: C01272, C01273, C01274.

## P179 (high confidence)

Handle MCP server installation as a supply-chain control point requiring trusted sources, code and tool-definition review, package-integrity checks, dependency scanning, and package-name verification.

Backing claims: C00415, C00418, C00419.

## P180 (high confidence)

Monitor MCP command execution for injection symptoms by correlating forbidden syntax, failed validation, privilege-escalation primitives, suspicious process arguments, abnormal syscall patterns, unexpected outbound traffic, sensitive path access, and unusual host resource consumption.

Backing claims: C00319, C00320, C00321.

## P181 (high confidence)

Treat sensitive-API usage as a first-class audit surface for MCP servers, scanning for five threat classes - network request (exfiltration or SSRF), code execution (eval, exec, Function), system command (os.system, subprocess, child_process), file operation, and HTML injection - recognizing such calls are widespread t…

Backing claims: C01285, C01333, C01334.

## P182 (high confidence)

Grant agents only task-required tools, and constrain each tool by explicit resources and operations instead of broad wildcard permissions.

Backing claims: C00423, C00424, C00427.

## P183 (high confidence)

Model MCP as a client-server protocol over stateful JSON-RPC 2.0 in which the host instantiates one client per server (n servers means n clients) and each client keeps a persistent session across RPC calls.

Backing claims: C01289, C01290, C01293.

## P184 (high confidence)

Validate and pin tool metadata and surface complete tool definitions to the approver before execution, because context/tool poisoning hides malicious instructions in tool metadata, schema, or docstrings that agents follow blindly.

Backing claims: C01022, C01023, C01024.

## P185 (high confidence)

Concentrate interception and approval at the Host as the policy enforcement point and security boundary (the LLM never touches a data source directly), and do not let Human-in-the-Loop approval be the only line of defense.

Backing claims: C01017, C01018, C01019.

## P186 (high confidence)

Measure a decentralized MCP ecosystem with per-registry adapters plus schema inference and canonicalization into a unified schema, because registries differ in data model and access method (HTML pages, JSON APIs, static catalogs).

Backing claims: C01299, C01301, C01307.

## P187 (high confidence)

Assume the malicious action will be performed by a legitimate, already-registered tool while the poisoned tool is never executed; do not gate solely on 'new or unknown tool', because that stealth pattern is chosen specifically to look unsuspicious and to bypass new-tool permission models.

Backing claims: C01141, C01146, C01147.

## P188 (high confidence)

Prioritize defenses against parameter tampering: it is empirically the most effective paradigm (average ASR 46.7% vs 36.7% explicit and 26.7% implicit function hijacking), likely because the primary call still matches user intent and only a single parameter is altered — so validate tool-call parameters against user in…

Backing claims: C01151, C01166, C01167.

## P189 (high confidence)

When measuring TPA, define Attack Success narrowly — the agent calls a separate legitimate tool to complete the malicious action — compute ASR over valid outputs only, and record the four-way outcome taxonomy (Success / Ignored / Direct-Execution / Refused) so direct-execution and refusal are not hidden inside a singl…

Backing claims: C01155, C01156, C01157.

## P190 (high confidence)

Treat dependency monoculture as systemic risk: Java servers concentrate on Spring (a single flaw like SpringShell can cascade), and over 93% of servers are JavaScript or Python, so a popular npm or PyPI vulnerability can cascade widely - audit and diversify shared dependencies.

Backing claims: C01282, C01324, C01330.

## Grounding

Every principle and claim id above resolves in this package’s distilled spine. Source anchors are chunk-level paragraph anchors from `sources/anchors/`.
