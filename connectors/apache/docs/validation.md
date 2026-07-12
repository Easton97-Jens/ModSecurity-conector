# Apache Validation

**Language:** English | [Deutsch](validation.de.md)

Status: evidence-scoped

Apache runtime claims require a concrete smoke or matrix command and generated
evidence. A successful build alone is not a runtime pass.

## Commands

```bash
git submodule update --init --recursive
make smoke-apache
make generate-test-matrix
make check-test-matrix
FORCE_ALL_CASES=1 make runtime-matrix-all
```

## Historical Evidence

These snapshots are not current canonical Phase-4 facet evidence.

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default Apache smoke (historical) | 54 | 54 | 0 | 0 | 0 |
| Apache force-all (historical) | 133 | 100 | 27 | 0 | 6 |

Executable YAML cases are owned by the framework module:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Generated evidence is recorded in:

- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`
- `reports/testing/test-coverage-overview.md`

## Not Claimed

- No broad Apache regression-suite pass is claimed without a matching runtime
  command and generated result.
- Force-all FAIL rows are not hidden by the default smoke summary.
- Full RESPONSE_BODY support is not promoted.

Phase 4 / RESPONSE_BODY remains non-promoted. Strict-mode source wiring is not
evidence of a real host-side late abort.

## Native P3 and separate P4 host evidence

Use the native full-lifecycle host path for response-header and response-body
evidence:

```bash
NO_CRS_RUN_ID=apache-native-$(date -u +%Y%m%dT%H%M%SZ) make full-lifecycle-apache
```

P3 deny and redirect are executed through the deterministic response-header
upstream before Apache commits the response. The safe and strict P4 cases are
separate real-host cases: safe must retain the visible response and record
`log_only`, while strict must record `connection_aborted`. Their event records
identify the executed path with `integration_mode: native-httpd-module`.

Inspect the per-case `result.json`, `case-assert.log`, `error.log`, and
metadata-only `phase4.log` under the generated host runtime directory. A build,
source inspection, or a single HTTP status is not a substitute for those
case-specific results.

## Canonical Phase-4 validation

The native output-filter implementation is declared
`implemented_not_asserted` for every response-body and late-intervention
facet.  This document therefore specifies evidence requirements, not a
current PASS claim.

| Case | Required evidence | Must not be inferred from |
| --- | --- | --- |
| `phase4_rule_observed` | Real Apache Phase-4 rule `1100301` observation | a visible 403 alone |
| `phase4_deny_before_commit` | requested deny, headers not committed, and matching visible client status | a post-commit match |
| `phase4_deny_after_commit_log_only` | requested `deny`, actual `log_only`, unchanged visible status, late flag | a rule ID or a 403 expectation |
| `phase4_deny_after_commit_abort` | actual `abort_connection` and `connection_aborted=true` | a generic connection failure |
| status/action metadata | original host status, requested WAF status, visible status, requested and actual actions | a single `http_status` value |

If a current canonical run cannot supply these observations, it is
`NOT_EXECUTED`; no outcome is promoted from source inspection or a historical
matrix.  Events remain metadata-only and must not contain response-body data.
