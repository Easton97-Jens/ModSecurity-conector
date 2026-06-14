# lighttpd Coverage Decision Matrix

Status: bridge-starter
Runtime status: not-verified

This file records only the lighttpd-specific state. The global matrix, status
vocabulary, promotion gates, No-CRS/With-CRS separation, runtime evidence
requirements, and RESPONSE_BODY minimum evidence remain defined in
`connectors/_template/docs/coverage-decision-matrix.md` and
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Current lighttpd Status

| Gate | Status |
| --- | --- |
| Scaffold | OK |
| Origin/Metadata | bridge-starter documented |
| Metadata/probe build | PASS |
| Bridge-starter build | PASS |
| Bridge-starter self-test | PASS |
| Native lighttpd module | not implemented |
| FastCGI/SCGI implementation | not implemented |
| Adapter implementation | not implemented |
| Harness | contract only |
| No-CRS | not-run |
| With-CRS | not-run |
| RESPONSE_BODY | not-verified |
| Promotion | not allowed beyond bridge-starter/partial |

## Gate Checklist

- [x] Scaffold documentation exists.
- [x] No local `connectors/lighttpd/tests` folder is used.
- [x] Origin/license status for current repo-owned bridge starter exists.
- [x] Source map for current repo-owned bridge starter exists.
- [x] Metadata exists for bridge-starter status.
- [x] Metadata/probe build-starter evidence path exists.
- [x] Bridge-starter source exists.
- [x] Bridge-starter self-test exists.
- [ ] lighttpd API/SDK/source selected.
- [ ] FastCGI/SCGI protocol adapter exists.
- [ ] lighttpd adapter implementation exists.
- [ ] lighttpd runtime harness evidence exists.
- [ ] No-CRS runtime evidence exists.
- [ ] With-CRS runtime evidence exists.
- [ ] RESPONSE_BODY blocking evidence exists.
- [ ] Negative/pass-through evidence exists.
- [ ] Audit/log evidence exists.

## Phase Matrix

| Phase / Gate | lighttpd status | Evidence |
| --- | --- | --- |
| Phase 0 Scaffold | OK | `connectors/lighttpd/` scaffold files |
| Phase 1 Origin/Metadata | bridge-starter documented | `ORIGIN.md`, `SOURCE_MAP.json`, `metadata.c`, `metadata.h` |
| Phase 2 Build | bridge-starter | `connectors/lighttpd/Makefile`, `build/build_starter.sh`, `build/bridge_starter.sh` |
| Phase 3 Harness | contract only | `connectors/lighttpd/harness/README.md` |
| Phase 4 No-CRS | not-run | no lighttpd runtime evidence |
| Phase 5 With-CRS | not-run | no lighttpd runtime evidence |
| Phase 6 Coverage Matrix | bridge-starter documented | this file references the global matrix |
| Phase 7 RESPONSE_BODY | not-verified | no lighttpd runtime evidence |
| Phase 8 Negative/pass-through | not-verified | no lighttpd runtime evidence |
| Phase 9 Audit/log | not-verified | no lighttpd runtime evidence |
| Phase 10 Promotion | not allowed beyond bridge-starter/partial | blocked by missing adapter and runtime evidence |
