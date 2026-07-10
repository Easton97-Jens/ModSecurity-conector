# Traefik Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: minimal_runtime_smoke (forwardAuth request path only)
Runtime status: broader connector behavior not verified

This file records Traefik-specific status only. Global matrix rules and
promotion gates are defined in
`connectors/_template/docs/coverage-decision-matrix.md` and
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Current Traefik Status

| Gate | Status | Evidence |
| --- | --- | --- |
| Scaffold | OK | `connectors/traefik/README.md`, `connectors/traefik/TODO.md` |
| Origin/Metadata | starter-present | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Build | link-verified-local | C17 Common-runtime-backed service compile/link target |
| Self-test | pass-local | `make -C connectors/traefik self-test-decision-service` |
| Harness | targeted-pass-local | real Traefik -> forwardAuth -> service 200/403 path |
| No-CRS | not-run | No Traefik runtime command was run |
| With-CRS | not-run | No Traefik runtime command was run |
| RESPONSE_BODY | not-verified | No blocking runtime evidence exists |
| Promotion | not allowed | Runtime gates are open |

## Gate Checklist

- [x] Scaffold files documented
- [x] No local `connectors/traefik/tests` folder
- [x] Repo-owned starter origin documented
- [x] Repo-owned starter metadata documented
- [x] Metadata build-starter evidence documented
- [x] Decision-service starter build documented
- [x] Decision-service starter local self-test documented
- [ ] Production Traefik origin/license evidence documented
- [ ] Production Traefik build evidence documented
- [x] Connector-owned harness implemented and documented
- [ ] No-CRS runtime evidence documented
- [ ] With-CRS runtime evidence documented
- [ ] RESPONSE_BODY blocking evidence documented
- [x] Local targeted negative/pass-through evidence produced
- [ ] Audit/log evidence documented

## Phase Matrix

| Phase / Gate | Traefik status | Decision |
| --- | --- | --- |
| Phase 0 / Scaffold | OK | scaffold-aligned |
| Phase 1 / Origin and metadata | starter-present | production origin remains open |
| Phase 2 / Build | link-verified-local | real service artifact links to Common runtime/libmodsecurity |
| Phase 3 / Harness | targeted-pass-local | real Traefik 200/403 path; retained CI evidence still open |
| Phase 4 / No-CRS | not-run | no runtime claim |
| Phase 5 / With-CRS | not-run | no CRS claim |
| Phase 6 / Coverage matrix | starter-documented | keep runtime statuses separate |
| RESPONSE_BODY blocking | not-verified | no blocking claim |
| Negative/pass-through | pass-local | targeted local evidence only |
| Audit/log evidence | not-verified | no audit/log claim |
| Promotion | not allowed | remains not_verified / connector-gap pending retained CI evidence |
