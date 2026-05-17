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
| `common-runtime-boundaries.md` | What the new Common C helpers do and do not own |
| `adapter-owned-layer.md` | Adapter-owned source boundaries beside retained upstream imports or, for NGINX, after upstream removal |
| `shadow-build-source-plan.md` | Generated `$BUILD_ROOT` connector source strategy |
| `apache-adapter-owned-migration-plan.md` | Planned Apache materialized Autotools/APXS migration criteria |
| `connector-adapter-interface.md` | Future adapter responsibilities and report metadata |
| `capability-model.md` | Capability vocabulary used by YAML cases and summaries |
| `status-model.md` | Runtime, import, and Common operation status mapping |
| `refactor-phase-1-plan.md` | First conservative Common foundation plan |
| `refactor-phase-3-review.md` | First implementation-level Common extraction review |
| `refactor-phase-6-review.md` | First adapter-owned source skeleton review |
| `refactor-phase-9-review.md` | NGINX adapter-owned source migration and PR #377 status |
| `replace-and-reduce-plan.md` | Controlled upstream replacement candidates and phase-4 decision |

## Current Boundary

`common/` contains connector-neutral types, tiny metadata helpers, and docs
only. `connectors/apache/src/` contains adapter-owned metadata helpers only.
`connectors/nginx/src/` now owns the NGINX module source used by monorepo
default builds through `$BUILD_ROOT/nginx-build/connector-src`. Apache hooks,
NGINX filters, server-specific config parsing, and libmodsecurity transaction
ownership are still connector-specific and are not Common-owned.
