# Topic-Based Subagent Plan

Goal: reorganize subagents around **topics** (so you ask "review my X" by topic, not by book),
using the local book corpus as grounding. Derived from a scan of the project's PDF/ebook repos
on 2026-06-19.

## 1. Corpus inventory (source repos)

| Repo | Books | Note |
|------|------:|------|
| `999-Computer-Books` | 998 PDF | flat `c(N).pdf`; titles in README.md; broad/older CS |
| `Computer-Science-Reference-Books` | 494 PDF | flat `comp(N).pdf`; titles in README.md; textbook-heavy |
| `awesome-book-collection` | 165 PDF + 12 epub | **already topic-foldered**; modern canon (DDIA, Clean Arch) |
| `books` | 52 PDF | **topic-foldered + curated canon** (added 2026-06-20): TCP/IP Illustrated, Site Reliability Engineering, Definitive Guide to SQLite, SQL Performance Explained, High Performance MySQL, Kafka/K8s/Redis/Cassandra. Highest signal-per-file; the cleanest corpus. |
| `subagent-factory` | 490 PDF | already-ingested sources — excluded |

1625 unique titles after dedupe (pre-`books/`). ~1097 map to a CS topic; ~528 are tangential
(GIS, ed-tech, business, electrical eng) and ignored. `books/` adds the canonical/curated layer
that the flat collections lacked (e.g. it supplies the only SQLite + Google-SRE + TCP/IP-Illustrated
copies), and its descriptive folder/filenames make it the easiest corpus for the resolver.

## 2. Topic map (corpus depth = how strongly a topic can be grounded)

| Depth | Topics (book count) |
|-------|---------------------|
| Deep (40+) | OS (79), Math/Theory (68), Python (67), Algorithms/DS (67), Java (61), Data-Science (59), Other-langs (50), Relational-DB (49), Networking (45), Clean-Code/SE (43) |
| Solid (15–39) | K8s/Containers (39), Security (37), Architecture (37), Big-Data/Data-Eng (34), Deep-Learning (28), DevOps/SRE (27), JS-TS (22), ML (22), NoSQL (19), Cloud (18), Compilers (15), Distributed-Sys (15) |
| Thin (<15) | Embedded (13), Game/Graphics (10), Mobile (9), Testing-QA (9), Crypto/Blockchain (7), C/C++ (7), Agile (7), CV (6), Kafka (6), LLM/NLP (3), Go/Rust (1) |

## 3. Proposed topic-based subagent catalog

Action key: **KEEP** (already topic-clean) · **MERGE** (consolidate overlapping existing) ·
**NEW** (rich corpus, no agent yet).

### A. Consolidations (fix the overlap you flagged)

| Proposed | Action | Replaces | Source candidates |
|----------|--------|----------|-------------------|
| `software-design-advisor` | MERGE 3→1 | software-design-reviewer, software-design-simplicity-advisor, software-simplicity-advisor | A Philosophy of Software Design; Code Simplicity; Clean Architecture; Clean Code |
| `kafka-streaming-advisor` | MERGE 2→1 | kafka-benchmarking-advisor, kafka-client-performance-advisor | Kafka in Action; Kafka Best Practices; Kafka Optimization/Benchmarking |
| `relational-db-performance-advisor` | MERGE 3→1 | mysql-at-scale-operations-advisor, mysql-replication-internals-advisor, postgres-query-performance-advisor | High Performance MySQL; Understanding MySQL Internals; Postgres perf; Database Internals |

*Tradeoff on the DB merge:* MySQL-ops vs MySQL-internals vs Postgres are partly distinct
reader-intents. Alternative = keep engine-specific but rename for topic clarity. Decide per taste.

### B. Keep (already 1 topic = 1 agent)

`domain-driven-design-reviewer` · `microservice-patterns-advisor` · `cloud-native-kubernetes-advisor`
· `caching-strategy-advisor` · `api-security-reviewer` + `web-application-security-reviewer` (split by
intent, like a good pair) · `test-driven-development-advisor` · `legacy-code-change-advisor` ·
`pragmatic-programming-advisor` · `java-concurrency-reviewer` · `mockito-unit-testing-advisor` ·
`k6-load-test-scripting-advisor` · `unix-v6-kernel-source-reviewer` + `xv6-kernel-internals-reviewer`
(narrow teaching-kernel readers — genuinely scoped) · non-CS niche: `negotiation-tactics-advisor`,
`startup-ceo-leadership-advisor`, `strengths-based-development-coach`, `employee-payment-scheme-advisor`,
`advertising-effectiveness-advisor`.

### C. New — high priority (deep corpus, no agent)

| Proposed | Corpus | Source candidates |
|----------|-------:|-------------------|
| `python-code-reviewer` | 67 | Python hard-way; data-structures-in-Python; effective-python-style |
| `algorithms-ds-advisor` | 67 | Introduction to Algorithms (CLRS); Algorithms Unlocked; common-sense guide to DS |
| `distributed-systems-advisor` | 15 | Designing Data-Intensive Applications; Database Internals; Building Microservices |
| `data-engineering-advisor` | 34 | designing data-intensive apps; advanced analytics with Spark; agile data science |
| `machine-learning-advisor` | 22+28 | course in ML; neural networks intro; deep-learning overview |
| `networking-advisor` | 45 | Computer Networking top-down (Kurose); Network Warrior; networking fundamentals |
| `devops-sre-advisor` | 27 | Accelerate; CI/CD with GitLab; continuous delivery |
| `java-code-reviewer` | 61 | (broadens java-concurrency-reviewer) Java performance; OO programming in Java |

### D. New — medium priority

| Proposed | Corpus |
|----------|-------:|
| `javascript-typescript-reviewer` | 22 |
| `nosql-data-modeling-advisor` (Mongo/Cassandra/Redis/Elastic) | 19 |
| `cloud-architecture-advisor` (AWS/Azure/GCP) | 18 |
| `operating-systems-advisor` (general; distinct from kernel-source readers) | 79 |
| `software-architecture-advisor` (patterns/system-design) | 37 |
| `application-security-advisor` (general; or fold into the 2 security agents) | 37 |
| `compilers-plt-advisor` | 15 |
| `testing-strategy-advisor` (could absorb mockito + k6) | 9+ |

### E. New — thin corpus (flag: needs external/multi sources)

`llm-genai-advisor` (3 — high relevance, weak local grounding) · `cpp-code-reviewer` (7) ·
`cryptography-advisor` (7) · `embedded-iot-advisor` (13) · `mobile-advisor` (9) ·
`game-graphics-advisor` (10). `go-rust-reviewer` (1) — too thin, skip.

## 4. Net effect

- Current: **27** agents (overlap-heavy in SE-design ×3, DB ×3, Kafka ×2, Testing ×3).
- After consolidations: 27 → **~20** (−7 from merges).
- After P1 new topics (+8): **~28**, but now **topic-indexed** with no same-topic duplicates.
- Full build-out (P1+P2+P3): ~40+ topic agents.

## 5. Recommended sequence

1. Consolidate the 3 overlap clusters (A) via multi-source re-author + supersession.
2. Add the 8 P1 NEW topics (deep corpus → strong Tier-1 packages).
3. Decide P2/P3 by what you actually review.
