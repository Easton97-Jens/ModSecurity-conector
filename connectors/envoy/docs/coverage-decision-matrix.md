# Envoy Coverage Decision Matrix

Status: bridge-starter
Runtime status: not-verified

This Envoy matrix is connector-specific status only. Global matrix semantics,
status vocabulary, and promotion gates are defined in
`connectors/_template/docs/coverage-decision-matrix.md` and
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Current Envoy Status

| Gate | Status |
| --- | --- |
| Scaffold | OK |
| Origin/Metadata | bridge-starter metadata present |
| Build | bridge-starter PASS |
| CLI self-test | PASS |
| Harness | Envoy runtime harness missing |
| No-CRS | not-run |
| With-CRS | not-run |
| RESPONSE_BODY | not-verified |
| Promotion | not allowed beyond bridge-starter |

## Gate Checklist

- [x] Connector scaffold exists.
- [x] No local `connectors/envoy/tests` folder is used.
- [x] Framework-owned test paths are referenced.
- [x] Origin/source-map evidence documents that no upstream Envoy source was
      imported.
- [x] Bridge-starter source exists.
- [x] Bridge-starter build exists.
- [x] Bridge CLI self-test exists and passes.
- [ ] Envoy SDK/API dependency exists.
- [ ] libmodsecurity bridge build evidence exists.
- [ ] Production adapter runtime harness evidence exists.
- [ ] No-CRS runtime evidence exists.
- [ ] With-CRS runtime evidence exists.
- [ ] CRS loaded/effective evidence exists.
- [ ] RESPONSE_BODY blocking evidence exists.

## Phase Matrix

| Phase | Envoy status | Evidence |
| --- | --- | --- |
| Phase 0 Scaffold | OK | `connectors/envoy/` scaffold files |
| Phase 1 Origin/Metadata | bridge-starter | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Phase 2 Build | bridge-starter PASS | `make -C connectors/envoy build-starter` |
| Phase 3 Bridge Self-Test | PASS | `make -C connectors/envoy self-test` |
| Phase 4 ModSecurity Bridge | blocked | libmodsecurity headers/libs not found in checked `/src` paths |
| Phase 5 Envoy Harness | missing | `connectors/envoy/harness/README.md` |
| Phase 6 No-CRS Runtime | not-run | no Envoy runtime run |
| Phase 7 With-CRS Runtime | not-run | no Envoy runtime run |
| Phase 8 CRS Evidence | not-verified | no Envoy With-CRS run |
| Phase 9 RESPONSE_BODY | not-verified | no runtime evidence |
| Phase 10 Negative/pass-through | not-verified | local self-test only |
| Phase 11 Audit/log | not-verified | no runtime evidence |
| Phase 12 Promotion | not allowed beyond bridge-starter | runtime gates are open |
