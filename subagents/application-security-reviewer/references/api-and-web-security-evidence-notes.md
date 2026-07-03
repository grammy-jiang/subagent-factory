---
name: api-and-web-security-evidence-notes
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P003
  - P004
  - P007
  - P008
  - P009
  - P010
  - P013
  - P014
  - P015
  - P016
  - P022
  - P023
  - P024
  - P025
  - P029
  - P030
  - P031
  - P041
  - P042
  - P043
  - P044
  - P045
  - P046
  - P047
  claims:
  - C00345
  - C00348
  - C00371
  - C00372
  - C00406
  - C00407
  - C00391
  - C00392
  - C00488
  - C00489
  - C00376
  - C00377
  - C00366
  - C00367
  - C00343
  - C00344
  - C00357
  - C00358
  - C00384
  - C00385
  - C00401
  - C00402
  - C00217
  - C00219
  - C00427
  - C00428
  - C00317
  - C00318
  - C00465
  - C00466
  - C00415
  - C00416
  - C00460
  - C00461
  - C00433
  - C00434
  - C00423
  - C00424
  - C00221
  - C00240
  - C00244
  - C00248
  - C00274
  - C00275
  - C00265
  - C00266
  - C00456
  - C00457
  - C00482
  - C00483
  evidence:
  - E00188
  - E00191
  - E00212
  - E00213
  - E00242
  - E00243
  - E00232
  - E00233
  - E00316
  - E00317
  - E00217
  - E00218
  - E00207
  - E00208
  - E00186
  - E00187
  - E00200
  - E00201
  - E00225
  - E00226
  - E00240
  - E00241
  - E00125
  - E00126
  - E00260
  - E00261
  - E00179
  - E00180
  - E00295
  - E00296
  - E00251
  - E00252
  - E00290
  - E00291
  - E00266
  - E00267
  - E00256
  - E00257
  - E00127
  - E00135
  - E00139
  - E00140
  - E00151
  - E00152
  - E00147
  - E00148
  - E00286
  - E00287
  - E00312
  - E00313
  source_anchors:
  - 3d98983ce864-c0008
  - 3d98983ce864-c0009
  - 3d98983ce864-c0010
  - 3d98983ce864-c0012
  - 3d98983ce864-c0011
  - 3d98983ce864-c0017
  - 3d98983ce864-c0000
  - 3d98983ce864-c0014
  - 3d98983ce864-c0007
  - 3d98983ce864-c0016
  - 3d98983ce864-c0013
  - 3d98983ce864-c0002
  - 3d98983ce864-c0003
  - 3d98983ce864-c0004
  - 3d98983ce864-c0015
  authored_from_digest: 5c6be9a3fd62df969f7674f1a10f54a2bd556808fff6122d59c78ff30f306535
---

# API and Web Security — Evidence Notes

Evidence notes behind the highest-confidence application-security principles. Each note ties a
principle to a sample of its backing claims and evidence records so a reviewer can trace a
recommendation to the distilled source. Sources: Web Application Security (Hoffman, 2020) and
Securing the API Stronghold (Nordic APIs, 2015); both distillation-only.

## P001 — Defend the DOM against XSS by never passing unsanitized user data into it — treat DOM injection as a last resort and pass user data as text, preferring innerText over innerHTML — and by avoiding the…

- `C00345`: The root cause of a stored XSS is a developer literally applying the result of an HTTP request to the DOM (for example via innerHTML), so user-submitted input is interpreted as DOM markup rather than text and any embedded script executes.
- `C00348`: Because stored XSS scripts are held as text server-side, regularly scanning database entries for signs of stored script is a cheap mitigation, but it cannot be a final solution because advanced payloads may be obfuscated (base64, binary)…

Evidence: E00188, E00191.

## P003 — Defend against injection by never letting a client send a query or command to be executed on the server, using prepared statements with bind variables as the first-line SQL defense (with…

- `C00371`: SQL injection lets a malicious user either supply their own parameters to an existing SQL query or escape it and provide their own query, which typically results in a compromised database because of the escalated permissions the SQL…
- `C00372`: All injection attacks share two components — an interpreter and a user-supplied payload that is read into that interpreter due to improper sanitization — so injection can occur against command-line utilities such as a video compressor,…

Evidence: E00212, E00213.

## P004 — Manage a reported vulnerability by reproducing it first in an automated production-like staging environment (to confirm it is real and find the root cause), scoring it with a system such as CVSS…

- `C00406`: Not all vulnerabilities carry equal risk, so each should be triaged and prioritized by financial risk to the company, difficulty of exploitation, type of data compromised, existing contractual agreements, and mitigations already in place,…
- `C00407`: While a fix for a known vulnerability is being developed, additional logging should be put in place to detect whether any attacker is exploiting it in the meantime, because lack of logging for known vulnerabilities has led to the demise…

Evidence: E00242, E00243.

## P007 — Integrate open source dependencies securely by isolating risky code (a decentralized server or constrained environment over embedding it in core code), choosing the integration method by size,…

- `C00391`: Relying on open source software means relying on a codebase that has probably not been audited to the same stringent standards as your own code, and because auditing a large OSS codebase and every incoming pull request is impractical and…
- `C00392`: How a web application integrates an OSS package matters because the integration structure dictates the data moving between them, the method by which it moves, and the level of privilege the OSS code is given, ranging from a centralized…

Evidence: E00232, E00233.

## P008 — Secure the whole dependency tree through automation and pinning, because third-, fourth-, and deeper-party dependencies cannot be manually reviewed and each unique dependency and version must be…

- `C00488`: A dependency tree comprises third-party dependencies, their dependencies (fourth-party), and deeper levels; manual code-level review of such a tree does not scale and is often impossible once fourth-party dependencies have their own…
- `C00489`: Each unique dependency and each unique version of each dependency must be evaluated, because one version may carry critical vulnerabilities that a later version does not, and components rarely standardize on the same version across the…

Evidence: E00316, E00317.

## P009 — Treat command injection as a top-severity risk and defend it with least privilege and meticulous sanitization: because injected commands run against the host OS (often as superuser on Unix) and can…

- `C00376`: SQL injection is first an injection attack and second a code injection attack, because the injected script runs under an interpreter or CLI rather than against the host operating system, which would instead be command injection.
- `C00377`: Non-SQL code injection is often application specific because it requires a CLI or interpreter controllable through an API endpoint, so a library that invokes a CLI behind the scenes (for example an image-compression library calling…

Evidence: E00217, E00218.

## P010 — Defend against XXE by disabling external entities in every XML parser and verifying parser behavior rather than assuming safe defaults.

- `C00366`: An XXE attack relies on an improperly configured XML parser, and almost all XXE vulnerabilities are found at an endpoint that accepts an XML or XML-like payload, including SVG, HTML/DOM, PDF (XFDF), and RTF, which many XML parsers also…
- `C00367`: The XML specification's external entity directive is interpreted on the machine evaluating the XML, so a crafted payload sent to a server's XML parser can read files in the server's file system, such as /etc/passwd or /etc/shadow,…

Evidence: E00207, E00208.

## P013 — Understand that XSS exists because applications execute scripts in users' browsers, that any dynamically created script modifiable by a user is a risk, and that its three OWASP categories (stored,…

- `C00343`: Cross-Site Scripting exploits the fact that web applications execute scripts in users' browsers, so any dynamically created and executed script puts the application at risk if it can be contaminated or modified, particularly by an end user.
- `C00344`: The three main categories of XSS designated by OWASP are stored (the code is stored in a database before execution), reflected (the code is not stored but reflected by a server), and DOM-based (the code is both stored and executed in the…

Evidence: E00186, E00187.

## P014 — Recognize that CSRF abuses the browser's trust model (the browser attaches authentication data to a request regardless of where the link came from) to make an authenticated user issue requests…

- `C00357`: CSRF attacks exploit the trust relationship between a website and the browser: API calls that rely on this relationship but yield too much trust to the browser can be abused with crafted links or forms to make an authenticated user issue…
- `C00358`: The two main identifiers of a CSRF attack are privilege escalation and stealth: the user account that initiates the forged request typically does not know it occurred.

Evidence: E00200, E00201.

## P015 — Understand and defend against denial of service across its classes — regex (catastrophic backtracking from greedy expressions), logical (targeting resource-intensive operations), and distributed…

- `C00384`: Denial-of-service attacks consume server or client resources to deny legitimate users, ranging from distributed attacks using many coordinated devices down to code-level DoS that affects a single user, and they usually cause no permanent…
- `C00385`: DoS vulnerabilities are most effectively tested in a local development environment so real users do not experience service interruption, and most bug bounty programs outright ban DoS submissions for this reason.

Evidence: E00225, E00226.

## P016 — Begin security in the architecture phase, before any code is written, by collecting and risk-evaluating all business requirements, building communication between security and engineering, and…

- `C00401`: Defensive security work begins before any code is written, in the architecture phase, with deep attention to the data flowing through the application, because most of security engineering is efficiently securing data in transit and…
- `C00402`: It is much easier and cheaper to catch and resolve deep architectural security flaws before writing and deploying software, because after an application has been adopted the depth of feasible re-architecture is limited and can be…

Evidence: E00240, E00241.

## P022 — Design and review architecture for the worst case by assuming malicious users and accounting for the application's distributed nature; designing only for legitimate, well-intentioned users is a…

- `C00217`: Good security starts with good design that explicitly accounts for the distributed nature of a modern application.
- `C00219`: Attacks on modern applications are often slow and methodical: the attacker patiently probes the entire surface area for any entry point, then designs an exploit specific to that point and optimized against the application's business model.

Evidence: E00125, E00126.

## P023 — Avoid the core secure-coding anti-patterns: do not ship temporary mitigations without a planned permanent fix, do not rely on blacklists (prefer whitelists, easing their maintenance with vetting),…

- `C00427`: Temporary or incomplete security mitigations should generally be avoided in favor of a permanent solution even if it takes longer, and a temporary solution should only be implemented when there is a preplanned timeline for designing and…
- `C00428`: Blacklists are a security anti-pattern because they only protect an application given perfect knowledge of all current and future malicious inputs, which is unattainable, so they can usually be bypassed with little effort (such as buying…

Evidence: E00260, E00261.

## P024 — Reduce version fingerprinting and keep dependencies patched, because insecurely configured default headers (X-Powered-By, Server, X-AspNet-Version) and default error or 404 pages reveal the software…

- `C00317`: Detecting a client-side framework or library and pinning its version number often surfaces applicable ReDoS, Prototype Pollution, and XSS vulnerabilities, especially in older versions that have not been updated, so the version should…
- `C00318`: Detecting software running on the client is much easier than detecting software on the server because client code is downloaded and referenced via the DOM, whereas server dependencies must be inferred from distinct marks in HTTP traffic…

Evidence: E00179, E00180.

## P025 — Defend against CSRF application-wide: verify the origin and referer headers against trusted origins as a first line (but not the only one, since an XSS on a trusted origin bypasses it), make…

- `C00465`: A first line of CSRF defense is verifying the origin and referer headers against a list of trusted origins, because these headers cannot be set programmatically with JavaScript in major browsers and so have a low chance of being spoofed;…
- `C00466`: Header verification alone fails when an attacker obtains an XSS on a whitelisted origin (so the forged request appears to come legitimately from your own servers), which is especially worrisome when the site hosts user-generated content,…

Evidence: E00295, E00296.

## P029 — Protect credentials and sensitive data: enforce password strength by entropy (reject common-list passwords and any derived from the user's name, birthdate, or address rather than counting special…

- `C00415`: Password strength is governed by entropy — the lack of observable patterns and avoidance of common words — rather than by length or special characters, so applications should reject passwords found in a top common-password list and…
- `C00416`: Credentials should never be stored in plain text but hashed before storage, because a hash is not reversible (so even staff cannot recover user passwords), is efficient to compute, and has near-zero collision probability so two passwords…

Evidence: E00251, E00252.

## P030 — Use Content Security Policy as a first-line XSS control delivered via header or meta tag, whitelisting script sources (avoiding wildcard hosts and unsafe-inline/unsafe-eval, and rewriting eval-like…

- `C00460`: Content Security Policy is a browser-enforced configuration that controls what external scripts can load, from where, and which DOM APIs may execute them; whitelisting script sources with script-src ('self' plus trusted origins) causes…
- `C00461`: Wildcard host whitelists in a CSP carry inherent risk, because whitelisting a pattern like *.example.com can become harmful if a future subdomain is repurposed to allow user-uploaded scripts.

Evidence: E00290, E00291.

## P031 — Layer automated vulnerability discovery against production code, since even well-architected and reviewed applications still ship flaws: combine static analysis (source-level, configured for the…

- `C00433`: Applications with the best architecture experience the fewest and lowest-risk vulnerabilities, and those with sufficient code-review processes fewer than those without, but even securely architected and reviewed applications still need…
- `C00434`: Automating vulnerability discovery is essential because automation is cheap, effective, and long-lasting at finding routine flaws that slip past architects and reviewers, but it is not good at finding logical vulnerabilities specific to…

Evidence: E00266, E00267.

## P041 — Run a security review by traversing the code from the client to its API calls, then to the dependencies those APIs rely on (databases, logs, helper libraries), then to unintentionally exposed or…

- `C00423`: Organizations that perform only functional code reviews should add a code security review as an additional step, ideally at merge-request time when the full feature is integrated, because an additional reviewer from outside the immediate…
- `C00424`: A code security review checks for common archetypes such as XSS, CSRF, and injection, but more importantly for logic-level vulnerabilities that require deep context into the feature's purpose and cannot be found by automated tools or…

Evidence: E00256, E00257.

## P042 — Secure client-side code as rigorously as server code, because modern exploits increasingly target the user through the browser, DOM, and CSS, and scale through email, social media, and camouflaged…

- `C00221`: Frontend developers who write no server-side code must still understand the security risks their code exposes and how to mitigate them, because many attacks originate from malicious code running in the browser, the DOM, or CSS.
- `C00240`: Modern web exploits increasingly target the user through the browser rather than the network or server, a shift driven by Web 2.0 applications that store user-submitted data and share it between users.

Evidence: E00127, E00135.

## P043 — Recognize that the modern attack surface is the application logic itself and that it constantly moves, so stay current with new technologies whose controls are immature and treat web security as a…

- `C00244`: Because browser security has advanced (Same Origin Policy, CSP, TLS), the most successful modern attackers target the application logic written by developers rather than the browser itself, since exploiting code bugs is easier than…
- `C00248`: Modern web applications are far larger and more complex than their predecessors — often hundreds of open source dependencies, integrations with other sites, multiple databases, and multiple servers — and the modern hacker spends most time…

Evidence: E00139, E00140.

## P044 — Choose authentication schemes that resist interception and replay: avoid HTTP basic auth because base64 is encoding not encryption and its credentials leak easily, prefer hashed schemes with replay…

- `C00274`: HTTP basic authentication attaches a base64-encoded username:password in the Authorization header on every request, and because base64 is encoding rather than encryption the credentials are easily leaked via compromised WiFi over HTTP or…
- `C00275`: Digest authentication employs cryptographic hashes instead of base64 encoding and has more defenses against interception and replay attacks than HTTP basic authentication.

Evidence: E00151, E00152.

## P045 — Avoid JavaScript footguns that create security risk: never declare implicit global variables (which land on the window object), prefer let and const over var for block scoping, and guard against…

- `C00265`: A JavaScript variable declared without var, let, or const is hoisted into global scope and added as a pointer on the window object, which is bad practice that can cause namespacing conflicts and significant security vulnerabilities or…
- `C00266`: Always strive to use let and const rather than var in JavaScript, because their block scoping reduces scope-related bugs and improves readability.

Evidence: E00147, E00148.

## P046 — Output-encode untrusted data for its context and treat CSS as an attack vector: HTML entity encoding of the big-five characters lets user data display safely only inside a div-like node and does not…

- `C00456`: Performing HTML entity encoding on all HTML tags in user-supplied data lets the characters be displayed in the browser while preventing them from being interpreted as JavaScript.
- `C00457`: HTML entity encoding of the big-five characters (&, <, >, double quote, single quote) lets user-supplied characters display in the browser without being interpreted as JavaScript, but it only protects content injected into a div-like DOM…

Evidence: E00286, E00287.

## P047 — Defend against single-source DoS by building comprehensive logging of every request's response time and of asynchronous background jobs, keeping evil greedy-backtracking regular expressions out of…

- `C00482`: A first measure against DoS attacks is building comprehensive server logging that records all requests alongside their response time, and manually logging the performance of asynchronous background job functions (such as a backup that…
- `C00483`: Regex DoS is best defended by a code review process plus a static analysis tool or linter that scans regular expressions for evil greedy-backtracking patterns (such as a repeated group followed by +) and keeps them out of the codebase,…

Evidence: E00312, E00313.

