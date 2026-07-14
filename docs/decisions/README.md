# Architecture decision records

**Language:** English | [Deutsch](README.de.md)

## Purpose and scope

This directory is the lightweight Architecture Decision Record (ADR) home for
the connector product monorepo. It records durable decisions whose alternatives,
security impact, test/evidence impact, and documentation impact must remain
reviewable. It is not a place for generated reports, runtime artifacts, or a
retroactive rewrite of history.

No versioned ADR process or individual ADR was present when this directory was
created. This README establishes the process; it is not itself an ADR.

## When to create an ADR

Create an ADR before or with a material decision that changes a repository
boundary, a shared product contract, a lifecycle invariant, a security
boundary, or the location/meaning of reusable tests and evidence. Keep a
small implementation detail in its owning change record unless its rationale
will guide later cross-connector work.

Each ADR is versioned in this directory as an English/German pair named
`ADR-<number>-<short-slug>.md` and `ADR-<number>-<short-slug>.de.md`. Keep
technical literals, status, date, links, code blocks, and tables equal in both
files. Record the associated Change Record and update affected concept,
architecture, configuration, security, and connector documentation.

## Required template

Use this template for every new ADR. Replace every angle-bracket placeholder.

~~~text
# ADR-<number>: <title>

## ID
ADR-<number>

## Status
proposed | accepted | superseded | deprecated

## Date
YYYY-MM-DD

## Context
<problem, constraints, and evidence boundary>

## Decision
<decision and scope>

## Alternatives
<alternatives and why they were not selected>

## Consequences
<positive, negative, migration, and ownership consequences>

## Security impact
<trust, data, limits, failure, and residual-risk impact>

## Test and evidence impact
<required contract tests, runtime evidence, and non-claims>

## Affected documentation
<paths that must be updated>
~~~

## Candidate first ADRs

These are recommendations only. Do not treat them as accepted decisions until
their own ADR files are reviewed and accepted.

| Suggested ID | Decision to capture | Why it should be durable |
| --- | --- | --- |
| `ADR-001` | Parent product monorepo and independent Framework repository | Fixes the product/test ownership boundary. |
| `ADR-002` | Host-neutral `common/` contract | Prevents server/proxy SDK coupling in shared code. |
| `ADR-003` | Shared P1--P4 lifecycle semantics | Keeps observable phase meaning consistent across adapters. |
| `ADR-004` | Connector self-sufficiency for build, packaging, and installation | Defines what must exist for a host-specific product. |
| `ADR-005` | Parent product-contract tests versus reusable Framework tests | Makes future test placement and evidence ownership reviewable. |

## Evidence boundary

An ADR may cite code, configuration, tests, reports, or a Change Record, but
it must distinguish `verified`, `documented_not_runtime_verified`,
`compatibility_only`, `unknown`, and `out_of_scope` claims as defined by
[the repository concept](../repository-concept.md). An ADR does not make a
runtime PASS or production-ready claim without its scoped canonical evidence.
