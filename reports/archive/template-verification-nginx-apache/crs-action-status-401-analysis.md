> Status: Historical
> Superseded by: [../../current/six-connector-core-completion.md](../../current/six-connector-core-completion.md)
> Date: retained as a historical report during repository organization on 2026-07-12
> Evidence boundary: historical planning, assessment, or snapshot; not current canonical evidence.

# CRS Action Status 401 Analysis

**Language:** English | [Deutsch](crs-action-status-401-analysis.de.md)

Status: resolved by scoped expectation update; exact CRS/action-merging root
cause remains not fully proven.

Updated: 2026-05-30 20:55:03 UTC

## Scope

This report documents the former With-CRS mismatch for
`action_status_401_phase1_block` and the repository-backed change that resolved
the runtime expectation without changing Apache or NGINX adapter code.

No Apache/NGINX adapter logic, connector harness logic, connector build logic,
or new YAML testcases were added. The required change was made inside the
framework submodule because the framework had no variant-specific expected
status handling for a case that is valid in both No-CRS and With-CRS contexts.

## Files Changed In The Framework Submodule

- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`
- `modules/ModSecurity-test-Framework/tests/README.md`
- `modules/ModSecurity-test-Framework/tests/runners/README.md`

Framework path used by the parent repository:
`modules/ModSecurity-test-Framework`.

Submodule status after the current checks: parent points to framework commit
`4bec4d960fea89525db9e439ea567df15943a2e7`; the framework working tree is
clean.

## Expectation Model

The base testcase expectation remains No-CRS:

```yaml
expect:
  status: 401
  intervention: block
  rule_id: 2320
```

The With-CRS expectation is now scoped through a variant override:

```yaml
expect:
  variants:
    with-crs:
      status: 403
```

This means the 403 expectation applies only when
`MODSECURITY_TEST_VARIANT=with-crs`. The base No-CRS expectation remains 401.

## Evidence Before The Change

Earlier With-CRS run:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Former result:

| Connector | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| Apache | `action_status_401_phase1_block` | 401 | 403 | FAIL |
| NGINX | `action_status_401_phase1_block` | 401 | 403 | FAIL |

No-CRS was already correct before the change:

| Connector | Expected | Actual | Status |
| --- | ---: | ---: | --- |
| Apache | 401 | 401 | PASS |
| NGINX | 401 | 401 | PASS |

The same With-CRS run proved CRS was active through
`crs_sqli_anomaly_block`, expected 403 and actual 403 for both connectors.

## Evidence After The Change

Commands:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common
```

Results:

| Command | Connector | PASS | FAIL | BLOCKED | Evidence |
| --- | --- | ---: | ---: | ---: | --- |
| `make test-no-crs` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt` |
| `make test-no-crs` | NGINX | 60 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt` |
| `make test-with-crs` | Apache | 55 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt` |
| `make test-with-crs` | NGINX | 61 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt` |
| `make smoke-common` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.txt` |
| `make smoke-common` | NGINX | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.txt` |

`action_status_401_phase1_block` after the change:

| Variant | Connector | Expected | Actual | Status | Evidence |
| --- | --- | ---: | ---: | --- | --- |
| No-CRS | Apache | 401 | 401 | PASS | `/src/ModSecurity-conector-build/results/no-crs/apache-results.jsonl` |
| No-CRS | NGINX | 401 | 401 | PASS | `/src/ModSecurity-conector-build/results/no-crs/nginx-results.jsonl` |
| With-CRS | Apache | 403 | 403 | PASS | `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl` |
| With-CRS | NGINX | 403 | 403 | PASS | `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl` |

CRS effectiveness evidence:

| Connector | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| Apache | `crs_sqli_anomaly_block` | 403 | 403 | PASS |
| NGINX | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

Evidence paths:

- `/src/coreruleset`
- `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`
- `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl`

Framework checks:

| Command | Result | Note |
| --- | --- | --- |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |

## What The Fix Proves

- The framework can now keep No-CRS and With-CRS expected statuses separate.
- The base No-CRS expectation for `action_status_401_phase1_block` remains
  401 and is passing for Apache and NGINX.
- The With-CRS expectation for the same case is 403 and is passing for Apache
  and NGINX.
- CRS is active in the With-CRS target, as shown by `crs_sqli_anomaly_block`
  PASS for both connectors.
- The former 401/403 mismatch is resolved for the current `/src` runs.

## What Is Still Not Proven

- The exact CRS/default-action or ModSecurity action-merging mechanism that
  produced 403 in the With-CRS context is still not fully proven.
- This is not evidence of Apache-only or NGINX-only adapter behavior; both
  connectors now follow the same variant expectations.
- RESPONSE_BODY blocking is not verified by this case.
- Full runtime verification beyond `partial` is not proven because promotion
  also requires the full minimum matrix and RESPONSE_BODY blocking evidence.

## Decision

The expectation change is accepted and scoped to With-CRS only. The connector
evaluations may record No-CRS and With-CRS runtime targets as PASS for the
current `/src` runs, but Apache and NGINX remain `partial` until the full
minimum matrix, including RESPONSE_BODY blocking or a documented supported gap,
is complete.
