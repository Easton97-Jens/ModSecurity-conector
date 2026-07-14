---
name: valyu-research
description: Plan and document bounded external research without enabling the blocked Valyu service integration.
---

# Plan bounded external research

This repository-authored skill records how to decide whether external research
is necessary. It does not enable or invoke Valyu, create credentials, or make
paid requests.

## Trigger conditions

- The user asks for research whose answer is not available in the repository
  and requires current authoritative external sources.
- A task needs a source-backed comparison, standards check, or provenance
  investigation.
- A future Valyu integration is being evaluated under the extension audit.

## Do not use when

- Repository evidence, supplied material, or a stable answer is sufficient.
- Repository evidence or an already-available official source answers the
  question; do not perform external research merely to duplicate it.
- The request asks to activate the hosted Valyu MCP without a safe secret and
  tool-boundary design approved by this repository.
- The research would transmit sensitive code, credentials, request payloads,
  or private review material to an external service.
- The question concerns an OpenAI product and official OpenAI sources are the
  required authority.

## Local procedure

1. State the research question, source authority, data classification, explicit
   maximum cost, and whether a repository-only or already-available official
   answer exists.
2. Prefer primary, no-cost sources, cite every external assertion, and retain
   only citation-level evidence.
3. Check `docs/security/external-agent-services.md` and the extension lock
   manifest before considering an external agent service.
4. Keep secrets in the approved runtime environment only; never place them in
   repository configuration, prompts, documentation, or test fixtures.
5. Never transmit internal source, logs, private reviews, credentials, or
   request payloads to an external service. Locally validate every result
   against the cited primary source.
6. Report whether the service remains blocked, documented only, or safely
   enabled. Do not substitute a similarly named tool for a documented one.

## Safety boundary

As of this adapter's revision, the hosted Valyu integration remains blocked
because its documented connection format places the secret in a URL and its
tool naming does not match the requested allowlist. This skill creates no
exception to that boundary.

## Provenance

Repository-authored. Concept discovery is recorded in [UPSTREAM.md](UPSTREAM.md);
no third-party skill text, script, dependency, or credential handling was
imported.
