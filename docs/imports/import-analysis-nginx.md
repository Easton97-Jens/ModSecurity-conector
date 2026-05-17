# Import Analysis: ModSecurity NGINX Connector

Status: implemented

Local reference: `/root/conecter/ModSecurity-nginx`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Observed ref: `master`, `v1.0.4-14-g9eb44fd`

## Role

This repository is an NGINX connector for libmodsecurity v3. It is now a
controlled source import under `connectors/nginx/upstream/`. Imported files are
kept NGINX-specific and documented in `connectors/nginx/ORIGIN.md`.

## Build System

Observed files:

- `config`
- `README.md`

Build follows NGINX third-party module conventions with `--add-module` or
`--add-dynamic-module` as documented by the source README.

## Test System

Observed tests:

- `tests/README.md`
- `tests/modsecurity-*.t`
- `tests/nginx-tests-cvt.pl`

The tests are NGINX-specific and depend on the nginx test harness and `prove`.

## libmodsecurity v3 Use

Observed public C API calls include engine/ruleset setup, transaction creation,
request/response phase calls, logging, intervention handling, and cleanup.

## NGINX Hooks

Observed concepts:

- HTTP access phase handler
- HTTP log phase handler
- header filter
- body filter
- location/main config creation and merge
- dynamic/static module ordering considerations

These are `connector-specific` and belong only under `connectors/nginx/`.

## Reuse Classification

| Concept | Source | Scope | Compatibility | Decision |
| --- | --- | --- | --- | --- |
| v3 C API phase sequence | v3 via connector | engine-specific | compatible | Document and adapt |
| NGINX phase/filter registration | connector | connector-specific | compatible only for NGINX | Tracked in `docs/roadmap/todo-inventory.md` |
| nginx-tests cases | connector | connector-specific | partial | Map to `tests/nginx/` |
| Source code files | connector | connector-specific | compatible only for NGINX | Imported under `connectors/nginx/upstream/` |

## Import Decision

The import is intentionally separated from `common/`. NGINX phase handlers,
header/body filters, configuration merge logic, and NGINX module build metadata
stay under `connectors/nginx/`. Future common extraction requires separate proof
via real-world Apache and NGINX smoke tests.
