# Architecture Docs

Status: implemented

Architecture docs define what is connector-neutral, what stays server-specific,
and how shared evidence maps to Common C-first data shapes.

## Documents

| Document | Use |
| --- | --- |
| `architecture.md` | High-level repository architecture and libmodsecurity v3 transaction flow |
| `c-vs-cpp-decision.md` | C-first public API decision and C++ boundaries |
| `common-extraction-plan.md` | What may move to `common/`, and when |
| `connector-adapter-interface.md` | Future adapter responsibilities and report metadata |
| `capability-model.md` | Capability vocabulary used by YAML cases and summaries |
| `status-model.md` | Runtime, import, and Common operation status mapping |
| `refactor-phase-1-plan.md` | First conservative Common foundation plan |

## Current Boundary

`common/` contains connector-neutral types and docs only. Apache hooks, NGINX
filters, server-specific config parsing, and libmodsecurity transaction
ownership stay under `connectors/<name>/` until separate proof exists.
