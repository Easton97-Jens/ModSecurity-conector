# NGINX Validation

**Language:** English | [Deutsch](validation.de.md)

Status: evidence-scoped

NGINX runtime claims require a concrete smoke or matrix command and generated
evidence. A successful build alone is not a runtime pass.

## Commands

```bash
git submodule update --init --recursive
make smoke-nginx
make generate-test-matrix
make check-test-matrix
FORCE_ALL_CASES=1 make runtime-matrix-all
```

## Historical Evidence

These snapshots are not current canonical Phase-4 facet evidence.

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default NGINX smoke (historical) | 60 | 60 | 0 | 0 | 0 |
| NGINX force-all (historical) | 140 | 95 | 39 | 0 | 6 |

Executable YAML cases are owned by the framework module:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Generated evidence is recorded in:

- `reports/testing/generated/nginx-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`
- `reports/testing/test-coverage-overview.md`

## Not Claimed

- No broad NGINX regression-suite pass is claimed without a matching runtime
  command and generated result.
- Force-all FAIL rows are not hidden by the default smoke summary.
- Full RESPONSE_BODY support is not promoted.

Phase 4 / RESPONSE_BODY remains non-promoted. Strict-mode source wiring is not
evidence of a real host-side late abort.

## Native P3/P4 host evidence and HTTP/2 applicability

Use the full-lifecycle NGINX target to exercise the real dynamic module with
the deterministic response-header upstream:

```bash
NO_CRS_RUN_ID=nginx-native-$(date -u +%Y%m%dT%H%M%SZ) make full-lifecycle-nginx
```

The P3 deny and redirect rows are response-header cases. The native harness
records them before headers are committed, alongside separate P4 safe and
strict records. A valid P4 record names
`integration_mode: native-nginx-http-module`; it must still show the actual
post-commit action instead of treating a rule match as a visible 403.

For every native harness case, inspect `nginx-version.log` and
`nginx-http2-applicability.json` in that case's host log directory. The latter
is `NOT_APPLICABLE` when the real `nginx -V` output lacks
`--with-http_v2_module`. If it is present, the status remains `NOT_EXECUTED`
until an explicit connector-owned HTTP/2 case and a matching HTTP/2 listener
are available. This prevents a build flag from being promoted as transport
runtime evidence.

## Canonical Phase-4 validation

The bounded NGINX response-body filter is source-declared
`implemented_not_asserted` for its executable response-body and
late-intervention facets. `phase4_pre_commit_deny` is `not_implemented`: this
native body-filter path runs after the response-header path. The following
evidence is required before any remaining individual facet can be promoted.

| Case | Required evidence | Must not be inferred from |
| --- | --- | --- |
| `phase4_rule_observed` | Real NGINX Phase-4 rule `1100301` observation | a visible 403 alone |
| `phase4_deny_before_commit` | not executable in the current NGINX body-filter timing model | body-filter wiring or a visible 403 |
| `phase4_deny_after_commit_log_only` | requested `deny`, actual `log_only`, unchanged visible status, late flag | a rule ID or an expected status |
| `phase4_deny_after_commit_abort` | actual `abort_connection`, retained already-visible status, and `connection_aborted=true` | a log-only record or generic disconnect |
| status/action metadata | original host status, requested WAF status, visible status, requested and actual actions | one overloaded status field |

An unexecuted current case remains `NOT_EXECUTED`; it is never converted into a
403 `PASS`.  Events and reports contain only response metadata, never a body
payload.
