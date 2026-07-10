---
name: interservice-communication-selection
kind: skill
status: ready
provenance:
  principles:
  - P086
  - P122
  - P103
  - P028
  - P025
  - P016
  - P004
  - P005
  - P006
  - P089
  claims:
  - C00016
  - C00136
  - C00137
  - C00138
  - C00139
  - C00151
  - C00152
  - C00166
  - C00167
  - C00186
  - C00015
  - C00156
  source_anchors: []
  authored_from_digest: b8bac2bcefef86719e40727749a5960354915f6fcee1f39196b7e672d9c66f3d
---

# Inter-Service Communication Selection

## Purpose

Guide a caller choosing how services communicate (synchronous vs. asynchronous),
how a failing dependency is contained, how service instances are located, and how
events are published reliably. This is the specialised walkthrough for the
**Communication** group (internal communication, reliability, discovery, and
reliable messaging).

## When to use

Use when the caller is deciding how services talk to each other, is worried about a
synchronous dependency's availability, needs runtime service discovery, or must
publish an event as part of a state change. Do not use for the *external* API edge
(route to `external-api-design`).

## Procedure

1. **Choose the interaction style before the technology.** The interaction style is
   technology-independent; classify it on two dimensions — one-to-one vs.
   one-to-many, synchronous vs. asynchronous — and note that a blocking
   request/response is tight coupling even when it runs over a message broker
   (C00138, C00139, P086). The two communication-style patterns are Remote procedure
   invocation and Messaging (C00016, P122).

2. **Weigh RPI vs. messaging by forces.** RPI is synchronous request/response over
   REST or gRPC — simple and immediate, but it couples the caller's availability to
   the callee's; messaging is asynchronous over a broker (AMQP, STOMP) — it improves
   availability and decouples sender from receiver, at the cost of
   messaging-infrastructure complexity (C00136, C00151, C00152, P028). Default to
   loosely coupled services communicating by asynchronous messaging, reserving
   synchronous REST mostly for communicating with external applications (C00137,
   P103).

3. **Model the messaging.** A sender writes a message (a document, command, or event
   with a header and body) to a channel and a receiver reads it: point-to-point
   channels for one-to-one interactions such as commands, publish-subscribe channels
   for one-to-many interactions such as events, with asynchronous request/response
   done via a reply-channel header and correlation id (C00166, C00167, P025).

4. **Maximise availability by minimising synchronous calls.** A system operation's
   availability is the product of the availabilities of every service it synchronously
   invokes, so prefer self-contained request handling — replicate needed data via
   events, or finish processing asynchronously after returning a response (C00186,
   P016).

5. **Protect every synchronous call.** Where RPI is used, recommend network timeouts,
   an upper bound on outstanding requests, and a Circuit breaker (via a resilience
   library) so a slow or failed dependency cannot cascade; decide per case how to
   recover — an error, a fallback or cached value, or graceful degradation by omitting
   non-critical data (C00015, C00156, P004).

6. **Locate instances with discovery.** If runtime location is in scope, use a
   service-discovery mechanism and contrast client-side discovery (the client queries
   the registry and load-balances) with server-side discovery (a router does it on the
   client's behalf) (P005).

7. **Publish events reliably.** When a service must update its database and publish a
   message, warn about the non-atomic dual-write problem and recommend the
   Transactional Outbox pattern — insert the message into an OUTBOX table inside the
   same local transaction, then relay it by polling or transaction-log tailing (P006).
   Because brokers usually guarantee only at-least-once delivery, require idempotent
   consumers that record processed message ids (P089). Never recommend a non-atomic
   dual write.

8. **Hand off.** The architecture owner decides and implements; this skill informs.

## Inputs

- **Required:** the interaction in question (who calls whom, sync/async tolerance,
  availability needs), and whether an event must be published as part of a write.

## Output

A recommended communication style with its trade-off, circuit-breaker / timeout
protection for synchronous calls, a discovery approach where relevant, and a
reliable-publishing design (transactional outbox + relay + idempotent consumers)
where an event accompanies a write.

## References

- `references/microservice-pattern-language-map.md` — the Communication and
  Discovery groups.

## Provenance

Tier 2. Grounded in principles P086/P122/P103 (choose interaction style; RPI vs.
messaging; default async), P028/P025 (REST/gRPC; messaging model), P016 (minimise
synchronous calls for availability), P004 (protect synchronous calls), P005
(service discovery), P006 (transactional outbox), and P089 (idempotent consumers),
from `chris-richardson-mic-19016f24` (Microservices Patterns, Chris Richardson,
Manning 2018, `distillation-only`). No verbatim quotation.
