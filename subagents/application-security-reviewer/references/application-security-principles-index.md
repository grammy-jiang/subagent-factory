---
name: application-security-principles-index
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
  claims:
  - C00345
  - C00012
  - C00371
  - C00406
  - C00158
  - C00303
  - C00391
  - C00488
  - C00376
  - C00366
  - C00147
  - C00296
  - C00343
  - C00357
  - C00384
  - C00401
  - C00143
  - C00024
  - C00044
  - C00069
  - C00095
  - C00217
  - C00427
  - C00317
  - C00465
  - C00076
  - C00137
  - C00288
  - C00415
  - C00460
  - C00433
  - C00001
  - C00006
  - C00008
  - C00131
  - C00064
  - C00042
  - C00179
  - C00223
  - C00257
  - C00423
  - C00221
  - C00244
  - C00274
  - C00265
  - C00456
  - C00482
  - C00002
  - C00018
  - C00086
  evidence:
  - E00188
  - E00010
  - E00212
  - E00242
  - E00111
  - E00170
  - E00232
  - E00316
  - E00217
  - E00207
  - E00100
  - E00163
  - E00186
  - E00200
  - E00225
  - E00240
  - E00096
  - E00019
  - E00033
  - E00048
  - E00068
  - E00125
  - E00260
  - E00179
  - E00295
  - E00055
  - E00090
  - E00157
  - E00251
  - E00290
  - E00266
  - E00001
  - E00006
  - E00007
  - E00085
  - E00043
  - E00031
  - E00120
  - E00128
  - E00144
  - E00256
  - E00127
  - E00139
  - E00151
  - E00147
  - E00286
  - E00312
  - E00002
  - E00015
  - E00061
  source_anchors:
  - 3d98983ce864-c0008
  - 1a5b18f0f07e-c0000
  - 3d98983ce864-c0010
  - 3d98983ce864-c0012
  - 1a5b18f0f07e-c0004
  - 3d98983ce864-c0006
  - 3d98983ce864-c0011
  - 3d98983ce864-c0017
  - 3d98983ce864-c0009
  - 1a5b18f0f07e-c0001
  - 1a5b18f0f07e-c0002
  - 3d98983ce864-c0000
  - 3d98983ce864-c0014
  - 3d98983ce864-c0007
  - 3d98983ce864-c0016
  - 1a5b18f0f07e-c0003
  - 3d98983ce864-c0005
  - 3d98983ce864-c0013
  - 3d98983ce864-c0001
  - 3d98983ce864-c0003
  - 3d98983ce864-c0004
  - 3d98983ce864-c0015
  authored_from_digest: 7590318b6359fd66a725fe26fb45fd074a7369f651d7cfbbda82125a0eb406b4
---

# Application Security Principles Index

The full set of application-security principles distilled from the two sources, grouped by the skill
that applies them. Each entry is a paraphrase with its confidence; no source text is quoted
verbatim.

## Web Vulnerability Defense

_Defend the core web attack classes at the point untrusted data is used._

- **P001** (high) — Defend the DOM against XSS by never passing unsanitized user data into it — treat DOM injection as a last resort and pass user data as text, preferring innerText over innerHTML — and by avoiding the javascript: URL scheme and text-to-DOM or text-to-script…
- **P003** (high) — Defend against injection by never letting a client send a query or command to be executed on the server, using prepared statements with bind variables as the first-line SQL defense (with database-specific escapers only as a fallback for unparameterizable…
- **P009** (high) — Treat command injection as a top-severity risk and defend it with least privilege and meticulous sanitization: because injected commands run against the host OS (often as superuser on Unix) and can read or write critical files, exfiltrate data, tamper with…
- **P010** (high) — Defend against XXE by disabling external entities in every XML parser and verifying parser behavior rather than assuming safe defaults.
- **P013** (high) — Understand that XSS exists because applications execute scripts in users' browsers, that any dynamically created script modifiable by a user is a risk, and that its three OWASP categories (stored, reflected, DOM-based) can run without user interaction to…
- **P014** (high) — Recognize that CSRF abuses the browser's trust model (the browser attaches authentication data to a request regardless of where the link came from) to make an authenticated user issue requests unknowingly, combining privilege escalation with stealth, and…
- **P015** (high) — Understand and defend against denial of service across its classes — regex (catastrophic backtracking from greedy expressions), logical (targeting resource-intensive operations), and distributed (network-level traffic floods) — by identifying which server…
- **P025** (high) — Defend against CSRF application-wide: verify the origin and referer headers against trusted origins as a first line (but not the only one, since an XSS on a trusted origin bypasses it), make anti-CSRF tokens the primary defense (cryptographic, per-session,…
- **P030** (high) — Use Content Security Policy as a first-line XSS control delivered via header or meta tag, whitelisting script sources (avoiding wildcard hosts and unsafe-inline/unsafe-eval, and rewriting eval-like functions to pass a function rather than a string), while…
- **P042** (high) — Secure client-side code as rigorously as server code, because modern exploits increasingly target the user through the browser, DOM, and CSS, and scale through email, social media, and camouflaged legitimate-looking interfaces such as phishing.
- **P045** (high) — Avoid JavaScript footguns that create security risk: never declare implicit global variables (which land on the window object), prefer let and const over var for block scoping, and guard against Prototype Pollution given that JavaScript objects are mutable…
- **P046** (high) — Output-encode untrusted data for its context and treat CSS as an attack vector: HTML entity encoding of the big-five characters lets user data display safely only inside a div-like node and does not protect script, CSS, or URL contexts; and because CSS can…
- **P047** (high) — Defend against single-source DoS by building comprehensive logging of every request's response time and of asynchronous background jobs, keeping evil greedy-backtracking regular expressions out of the codebase through code review and a regex-scanning linter,…

## Dependency And Supply Chain Security

_Treat the whole transitive dependency tree as untrusted, and scan and pin it._

- **P007** (high) — Integrate open source dependencies securely by isolating risky code (a decentralized server or constrained environment over embedding it in core code), choosing the integration method by size, dependency chain, and upstream activity, avoiding one-click…
- **P008** (high) — Secure the whole dependency tree through automation and pinning, because third-, fourth-, and deeper-party dependencies cannot be manually reviewed and each unique dependency and version must be checked: model the tree and scan it automatically against a…
- **P024** (high) — Reduce version fingerprinting and keep dependencies patched, because insecurely configured default headers (X-Powered-By, Server, X-AspNet-Version) and default error or 404 pages reveal the software and version, letting an attacker cross-reference a known…
- **P038** (medium) — Review dependency updates before installation, compare them to known prior code, and reject update-then-review habits that transfer security responsibility to dependency maintainers.

## Secure Development Lifecycle

_Fold security into the lifecycle from the architecture phase, for the worst case._

- **P016** (high) — Begin security in the architecture phase, before any code is written, by collecting and risk-evaluating all business requirements, building communication between security and engineering, and focusing on data flow — securing data in transit (require all…
- **P022** (high) — Design and review architecture for the worst case by assuming malicious users and accounting for the application's distributed nature; designing only for legitimate, well-intentioned users is a fatal flaw, and proper planning raises the cost of attack.
- **P023** (high) — Avoid the core secure-coding anti-patterns: do not ship temporary mitigations without a planned permanent fix, do not rely on blacklists (prefer whitelists, easing their maintenance with vetting), do not launch unevaluated boilerplate or default framework…
- **P036** (medium) — Make the API provider responsible for the base security design early, including transport protection, authentication and authorization policy, session handling, delegation, and federation verification.
- **P048** (medium) — Build security into API designs from the outset, assuming even initially private APIs may later face public exposure.

## Security Review And Vulnerability Management

_Run a manual review by traversal and manage a reported vulnerability end to end._

- **P004** (high) — Manage a reported vulnerability by reproducing it first in an automated production-like staging environment (to confirm it is real and find the root cause), scoring it with a system such as CVSS (base, temporal, and environmental, customized for IoT or…
- **P031** (high) — Layer automated vulnerability discovery against production code, since even well-architected and reviewed applications still ship flaws: combine static analysis (source-level, configured for the OWASP top 10, strong on common patterns but weak on dynamic…
- **P040** (medium) — Begin any security assessment by mapping the application's structure, combining technical analysis with functional analysis of its purpose, users, and revenue model to identify mission-critical data, and record findings in notes that preserve relationships…
- **P041** (high) — Run a security review by traversing the code from the client to its API calls, then to the dependencies those APIs rely on (databases, logs, helper libraries), then to unintentionally exposed or future APIs, and finally the rest by descending risk —…
- **P043** (high) — Recognize that the modern attack surface is the application logic itself and that it constantly moves, so stay current with new technologies whose controls are immature and treat web security as a cyclical, never-finished process.

## Reconnaissance And Attack Surface Mapping

_Map the attack surface from the attacker's perspective — only where authorised._

- **P006** (medium) — Discover API endpoints and payloads methodically — probe HTTP verbs against known resources, try OPTIONS, reverse-engineer the authentication scheme and token, start from common endpoints (sign in/up, password reset), and shrink an unknown value's search…
- **P012** (medium) — Use several reconnaissance techniques together because no single one is comprehensive, preferring cheap low-noise methods first (a zone-transfer attempt, then a dictionary of common subdomains) and treating noisy brute force as a last resort fired…
- **P028** (medium) — Assume sensitive data and infrastructure leak into public records over time — cached repositories, keys, internal URLs, PII — and proactively hunt for them using search-engine operators, web archives, social-media data APIs, and browser developer tools…
- **P039** (medium) — Use the attacker's perspective — running the same reconnaissance against your own application — to find weak mechanisms and prioritize defenses, recognizing that routine defenses are easily bypassed and that some threats (such as malware hidden in valid…

## Api Identity And Access Management

_Review API security as an identity-and-access-management system._

- **P002** (medium) — Add OpenID Connect and identity-provider federation when an OAuth-based API solution needs standardized user identity, authentication context, or cross-domain trust.
- **P005** (medium) — Prefer modern public-key-backed transport security for network APIs, validate key ownership, avoid plain symmetric-key use over networks, and use TLS over SSL whenever possible.
- **P011** (medium) — Prefer delegated tokens over API-side access tables for microservice-heavy user-to-user delegation, while accounting for application token-management complexity.
- **P018** (medium) — Keep authentication, authorization, federation, and delegation conceptually separate and apply each only to the responsibility it actually serves.
- **P021** (medium) — Choose token transport and profile by security need: use reference tokens when data should remain server-side, avoid bearer tokens when proof of presenter identity is required, prefer Holder-of-Key over custom proof schemes, and avoid obsolete MAC token…
- **P027** (medium) — Expose reference tokens externally, translate them at an edge authentication server or API firewall, and pass JWTs internally when microservices need distributed identity.
- **P029** (high) — Protect credentials and sensitive data: enforce password strength by entropy (reject common-list passwords and any derived from the user's name, birthdate, or address rather than counting special characters), never store passwords in plain text but hash them…
- **P032** (medium) — Review API security as an identity and access-management system that includes the API, surrounding organization, servers, mobile clients, IoT devices, and microservice interactions.
- **P034** (medium) — Use OAuth for delegated access only, and model OAuth integrations around the client, authorization server, resource owner, and resource server responsibilities.
- **P035** (medium) — For microservices, avoid repeating monolithic per-service authentication; use OAuth delegation and OpenID Connect identity where clients need user context or backend sessions.
- **P044** (high) — Choose authentication schemes that resist interception and replay: avoid HTTP basic auth because base64 is encoding not encryption and its credentials leak easily, prefer hashed schemes with replay defenses, couple authentication with two-factor…
- **P050** (medium) — Deploy OAuth and OpenID Connect inside a broader security and identity-management program that also protects servers, mobile clients, networks, firewalls, and cloud infrastructure.

## Api Design And Lifecycle Governance

_Govern the API across its lifecycle and layer its controls._

- **P017** (medium) — For user-to-user sharing of connected-device access, do not rely on ordinary OAuth alone; use an added identity layer such as OpenID Connect to represent the resource owner, delegate, and scopes.
- **P019** (medium) — Favor private or partner API models for sensitive personal data or secure systems, and reserve public exposure for open data that does not connect to confidential systems.
- **P020** (medium) — Reject just-enough API code: validate inputs, prevent unsafe file upload behavior, avoid overbroad storage paths, handle errors safely, and suppress raw implementation diagnostics from external callers.
- **P026** (medium) — Reassess security assumptions when adopting microservices, API-management changes, or cloud infrastructure, including decentralization, physical control loss, backups, file security, and possible co-residency risks.
- **P033** (medium) — Prefer peer-reviewed, proven security standards and products over bespoke mechanisms, combining protocols such as OAuth, OpenID Connect, SCIM, JWT, strong second factors, and policy systems as the use case requires.
- **P037** (medium) — Choose API licensing and availability at the start of the lifecycle, matching exposure to the API purpose, data sensitivity, business model, upkeep capacity, and monetization goals.
- **P049** (medium) — Do not present API keys, OAuth adoption, or any single control as complete API security; require layered controls across enterprise, mobile, network, and API surfaces.

