# HAProxy Test Framework Contract

**Language:** English | [Deutsch](test-framework-contract.de.md)

Status: current ownership boundary

Executable cases, matrix generation, runtime snapshots, and generated reports
are framework-owned. The HAProxy connector owns source, examples, and the
runtime harness that the framework invokes.

## Connector-Owned

- `connectors/haproxy/src/`
- `connectors/haproxy/Makefile`
- `connectors/haproxy/harness/run_haproxy_smoke.sh`
- `examples/haproxy/`
- connector metadata and origin files

## Framework-Owned

- YAML cases under `modules/ModSecurity-test-Framework/tests/cases/`
- case selection and normalization helpers
- runtime matrix orchestration
- runtime validation snapshot generation
- generated report rendering

## Reporting Contract

- Default HAProxy smoke reports the supported non-former-XFAIL subset:
  `55/55 PASS`.
- Force-all HAProxy evidence remains separate:
  `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED / 6 NOT_EXECUTABLE`.
- Root summaries are connector-neutral.
- Row-level HAProxy details stay in
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- There is no synthetic matrix writer.

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` strict-abort sample is disabled, legacy, and
noncanonical; it is not current runtime evidence.
