# Architecture - Connector Template

## Goal

This document is a planning frame for a future adapter-owned connector. It is
not runtime code and does not prove any server integration.

## Required architecture evidence

- [ ] Server lifecycle and hook model documented.
- [ ] Request header path documented.
- [ ] Request body path documented.
- [ ] Response header path documented.
- [ ] Response body path documented, or unsupported behavior documented with
      evidence.
- [ ] Intervention mapping documented.
- [ ] Logging and audit path documented.
- [ ] Startup/reload behavior documented.
- [ ] Thread/process/worker model documented.

## Adapter-owned principle

- Connector-specific code lives under `connectors/<name>/`.
- Shared connector-neutral helpers may be referenced only when their paths and
  contracts are found in the repository.
- Apache/NGINX runtime behavior must not be treated as generic behavior for a
  new server.

## Server-specific areas

Each connector must prove these areas separately:

- hook registration / filter chain / middleware integration
- request/response lifecycle integration
- body handling, including buffering, streaming, and limits
- configuration parser and merge semantics
- ModSecurity intervention mapping into server actions
- process, worker, and memory model

## Reusable evidence

Reusable planning evidence may include:

- shared status, origin, intervention, and capability data shapes
- framework test paths
- documented Make targets
- proven include/library contracts

Reusable planning evidence is not runtime proof.

## Promotion relevance

Architecture documentation can support `scaffolded` or `adapter-owned`. It
cannot support `runtime-smoke-verified`, `crs-verified`, or more than
`partial` without executed runtime evidence.

## What must not be claimed

- Do not claim Apache/NGINX runtime paths transfer to a new connector.
- Do not claim RESPONSE_BODY or phase 4 support automatically exists.
- Do not claim production readiness without runtime evidence.
- Do not invent server APIs, hook names, or lifecycle behavior.
