# Phase-4 budget scope, native errors and NULL guards

**Language:** English | [Deutsch](CR-20260920-phase4-all-connector-budget.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260920-phase4-all-connector-budget` |
| Date (UTC) | 2026-09-20 |
| Base revision | `785a620de7b1c6b566a73eed642457eeb8419bb4` |

## Motivation and problem statement

Apply the user's requested budget rule across all connector families:
the extra cumulative Phase-4 inspection budget applies only to `safe` and
`strict`; `off` keeps configured engine inspection and native error handling.
Restore NGINX's negative intervention result handling from before upstream
PR #377, add missing NULL guards, and remove stale README statements.

## Acceptance criteria

Both the body planner and secondary contract/prechecks follow the same mode.
`off` can ingest more than the configured extra inspection budget, with
checked accounting. Enabled budgets accept their exact boundary and preserve
existing over-limit behavior. NGINX negative native results in `off` call
`ngx_http_filter_finalize_request` with `NGX_HTTP_INTERNAL_SERVER_ERROR`.
Missing configuration must not be dereferenced. Independent engine, memory,
message/frame and transport safeguards remain active.

## Implementation decision and rationale

A header-only Common helper supplies the effective cumulative budget. `off`
uses `SIZE_MAX` only as an arithmetic ceiling, never an allocation size.
Apache, HAProxy native/HTX and Common Runtime use it at their relevant budget
checks. NGINX uses the Common planner in every mode and a matching metadata ceiling.
Common Runtime covers direct and response-companion ingestion; Envoy's Go
precheck reads an optional capability from the loaded Common engine, not its
independent late-action setting. lighttpd's streaming Content-Length precheck
follows the mode while its buffered capacity guard stays in place.
`process_partial` cannot hide an off-mode accounting overflow.

NGINX uses the legacy negative-result finalizer only in `off`; other
integrations retain their own existing APR/Common/host return conventions.
NULL guards cover NGINX, Apache, Common logging and Traefik. Existing Envoy
bridge guards remain unchanged.

## Security impact

This intentionally removes only the additional cumulative P4 cap in `off`.
Engine inspection/settings, native failures, counter overflow, file metadata
and read validation, fixed scratch buffers, request budgets, bounded
allocations, gRPC chunk sizes and companion transport limits remain.
No unsupported response route or strict-abort capability is promoted.

## Changed files

- `common/include/msconnector/phase4_budget.h`
- `common/runtime/msconnector_runtime.c`
- `connectors/apache/README.de.md`
- `connectors/apache/README.md`
- `connectors/apache/src/msc_filters.c`
- `connectors/envoy/README.de.md`
- `connectors/envoy/README.md`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_budget.go`
- `connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/haproxy/README.de.md`
- `connectors/haproxy/README.md`
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/lighttpd/README.de.md`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/nginx/README.de.md`
- `connectors/nginx/README.md`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/traefik/README.de.md`
- `connectors/traefik/README.md`
- `connectors/traefik/src/traefik_engine_service.c`
- `docs/phase4-mode-budget.de.md`
- `docs/phase4-mode-budget.md`
- `reports/audits/change-records/CR-20260920-phase4-all-connector-budget.de.md`
- `reports/audits/change-records/CR-20260920-phase4-all-connector-budget.md`
- `tests/test_nginx_phase4_mode_budget.py`
- `tests/test_phase4_all_connector_budget.py`
- `tests/test_phase4_envoy_budget.py`

## Commands executed

During initial preparation, executed through the Python unittest API in an isolated source workspace:
`tests.test_nginx_phase4_mode_budget` and
`tests.test_phase4_all_connector_budget`: 30 tests passed with GCC and the
same 30 passed with Clang. The Common fixture uses `-std=c17 -Wall -Wextra -Werror`; the original NGINX
fixture selected C11 and is aligned to C17 in the follow-up. Fixtures use actual
helper/planner/branch source and small host doubles.
`tests.test_phase4_envoy_budget`: two checks passed, including stdlib-only
`go test -count=1 -v .` on actual extracted Go functions and the added Go
table tests. This does not build the full Envoy/CGo package.

Seven mutation controls each produced an expected assertion failure:
shared off budget, NGINX legacy negative finalizer, NGINX secondary metadata
budget, Apache secondary metadata budget, HAProxy HTX precheck, Common Runtime
secondary metadata budget, and Envoy cumulative precheck. Final restored
suites passed again. These are seven controls, not seven production failures.

New patch lines have no trailing whitespace. Diff contexts and reconstructed
file hashes are verified by a standalone Python validator in the delivery
package; this is not a claim that native `git apply --check` ran.

### PR #381 CI remediation (2026-09-21)

The unchanged NGINX Common-adoption checker reproduced the failure on
`59fd49017a81f5c0ac846109c17ea7ce627db877` (exit 1): the off branch used a manual
byte increment outside the Common planner. After the source fix the same
checker passed (exit 0). All modes now use one Common planning call; off
selects `SIZE_MAX`. On overflow, Common saturates bytes seen without advancing
bytes inspected, accepts no bytes, and returns failure.

The metadata budget is resolved by a small NULL-safe helper rather than the
nested conditional expression reported as Sonar `c:S3358`. No rule suppression,
checker relaxation, workflow change or dependency change is used.

Fresh isolated Python API validation on the revised source:
- `tests.test_nginx_phase4_mode_budget`, `tests.test_phase4_all_connector_budget`
  and `tests.test_phase4_envoy_budget`: 34 tests passed with GCC and the same
  34 passed with Clang; the C fixtures now both select C17.
- `tests.test_phase4_migration_contract`, `tests.test_nginx_native_security_contract`
  and `tests.test_nginx_upstream_security_contract`: 33 tests passed.
- The unchanged documentation checker's record-heading, identity, structural
  parity, code-fence and local-link checks passed for this record pair.

These checks used Python 3.13 in the isolated snapshot, not the canonical
Python 3.14.7/RTK environment. Complete CI and native-host results for the
follow-up commit must be evaluated separately.

## Runtime evidence

None from live NGINX, httpd, HAProxy, Envoy, Traefik or lighttpd servers.
No HTTP/1, HTTP/2, HTTP/3, production, sanitizer or real-engine integration
success is asserted.

## Checks not run and rationale

No local repository-native RTK-wrapped make checks, full host builds, full
Go/CGo package tests, complete regression suites or canonical whole-repository
bilingual/link check were run: RTK, the configured interpreter and the native
host environment were unavailable. No package/toolchain installation or
dependency mutation was performed. Remote CI for the initial PR head was
inspected: lint reported invalid record headings/identity, and quick checks
failed the shared NGINX accounting contract. Sonar's gate passed with one
new maintainability issue. Fresh follow-up CI/Sonar results are pending at
the time of this remediation record.

## Known limitations

The source archive was from `da9b0bf7e06df77cc93ba45371454042740c5dd3`.
All nine changed pre-existing production source files were independently
byte-verified against GitHub blobs at the selected base. The eight README
migration deltas from PR #380 were preserved in the patch baseline; the
original archive was not presented as a complete current checkout.
The preparation session initially produced a local change package. This
branch publishes those source files for Draft review; current-head CI and
full host validation remain separate. This is not a merged change.

## Remaining risks

Host-specific integration and error-page behavior need native regression
tests. A buffered compatibility route may still reject an oversized response
because of its independent storage limit in `off`. Unsupported strict-abort
profiles remain unsupported. The patch does not change Framework/MRTS or
disable CI/security gates.

## Final diff and review status

The initial source files are published in Draft PR #381. This follow-up
changes only the NGINX body/header filters, their budget regression test and
this record pair. Source diff and isolated checks were reviewed; the existing
quality gates remain unchanged. The PR records the current head and CI state;
no merge or production approval is asserted here.
