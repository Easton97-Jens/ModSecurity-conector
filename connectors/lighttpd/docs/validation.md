# lighttpd Validation

Status: bridge-starter
Runtime status: not-verified

The lighttpd metadata/probe and bridge starter can be compile-checked and
self-tested locally, but lighttpd runtime validation has not been run.

| Area | lighttpd status |
| --- | --- |
| Metadata/build-starter compile | PASS via `connectors/lighttpd/build/build_starter.sh` |
| Bridge-starter compile | PASS via `make -C connectors/lighttpd build-bridge-starter` |
| Bridge-starter self-test | PASS via `make -C connectors/lighttpd self-test-bridge` |
| Native lighttpd module build | blocked |
| FastCGI implementation | blocked |
| SCGI implementation | blocked |
| Runtime harness | not implemented |
| No-CRS | not run |
| With-CRS | not run |
| RESPONSE_BODY | not verified |
| Negative/pass-through | not verified |
| Audit/log | not verified |

Executable tests are framework-owned and must use shared paths when a real
lighttpd build and harness exist:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/lighttpd/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Starter PASS does not count as runtime evidence. lighttpd cannot be promoted
beyond bridge-starter/partial without repository-backed runtime evidence and
PASS/FAIL/BLOCKED counts for its own real-world connector path.

## Framework-Owned Starter Evidence

`make connector-starter-checks` runs lighttpd build-starter, bridge-starter, and
bridge self-test checks from
`modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`.
Results are written to
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` and
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

The lighttpd entries are connector-starter build/self-test evidence only:
`runtime_verified` is `false`, `runtime_status` is `not-verified`, and
`response_body_verified` is `false`.
