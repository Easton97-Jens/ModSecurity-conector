# Change Record CR-20260909-fail-closed-connector-remediation

**Language:** English | [Deutsch](CR-20260909-fail-closed-connector-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260909-fail-closed-connector-remediation |
| Date (UTC) | 2026-09-09 |
| Base revision | 26a560e64cbaf906c0d35bba199f65436830d1dd |
| Branch | security/audit-2026-09-09-fixes |
| Issue or pull request | Draft PR [#360](https://github.com/Easton97-Jens/ModSecurity-conector/pull/360) is open and unmerged. |
| Delivery status | Draft PR #360 was opened from `security/audit-2026-09-09-fixes` at first delivery commit `df582b6aeaf2900e63228ff0b82507266db5b5f8`; local, remote, and PR head matched at creation. This record update is a follow-up commit and cannot self-reference its own final Git object; task delivery evidence records the exact final local/remote/PR-head SHA after push. Hosted checks and review remain pending. Merge, release, deployment, a default-branch write, and a Parent Gitlink change are not authorized. |

## Motivation and problem statement

Enabled connector processing must not treat an internal transaction-setup or
native response-header-processing error as a harmless disabled/non-applicable
path. This Parent-only remediation makes those error paths terminal while
preserving the explicitly disabled behavior and the existing streaming
boundary. It excludes the private audit, raw reproductions, credentials, and
runtime payloads.

## Acceptance criteria

- Enabled Apache request-context setup failures enter the existing fail-closed
  response path rather than returning a successful decline.
- A non-success native NGINX response-header result becomes terminal, restores
  the PCRE allocation state once, and does not call the next header filter.
- Focused negative and legitimate-control contracts pass, while unavailable
  host-runtime proof remains reported as blocked rather than passed.
- English/German connector documentation and this English/German Change Record
  describe the same scope, evidence, and limitations.
- Delivery is limited to an ordinary Parent Draft PR; no Framework/MRTS source,
  Gitlink, CI-permission, merge, release, or deployment change is made.

## Implementation decision and rationale

Apache now distinguishes disabled processing from an enabled setup error. It
publishes a request context only after ownership and cleanup setup are valid;
an enabled construction, expression, or identifier error follows the existing
terminal failure handling.

NGINX records a terminal response-header-processing failure before the upstream
header filter. The failure path restores the PCRE allocation state exactly once,
uses bounded generic logging, returns `NGX_ERROR`, and rejects reinvocation.
The test fixtures cover success, zero, and other non-success native results,
filter ordering, and cleanup.

The existing progressive P4 model was reviewed but not changed. It still makes
no full-response holdback, zero-byte, replacement-response, HTTP/2 reset, or
HTTP/3 reset claim without host evidence.

## Security impact

The affected security boundary is enabled request/response inspection during
connector transaction lifecycle processing. Before this change, an error in an
enabled path could be conflated with a non-applicable outcome, risking traffic
continuing without the intended inspection outcome. The correction makes the
failure observable and terminal at the connector boundary. Focused static and
fixture evidence rechecks the original error class, an alternate non-success
class, and disabled/allow controls. No sensitive test payload or production
data is included in this record.

## Changed files

- Apache implementation and bootstrap contract:
  `connectors/apache/src/mod_security3.c` and
  `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`.
- Apache documentation and regression coverage:
  `connectors/apache/README.md`, `connectors/apache/README.de.md`, and
  `tests/test_apache_request_transaction_cleanup.py`.
- NGINX implementation:
  `connectors/nginx/src/ngx_http_modsecurity_common.h` and
  `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`.
- NGINX contracts and native fault fixtures:
  `tests/test_nginx_upstream_security_contract.py`,
  `tests/test_nginx_p3_header_fixture.py`,
  `tests/run_nginx_p3_header_fixture.py`,
  `tests/nginx_p3_header_observer_fixture/`, and
  `tests/nginx_p3_header_injector_fixture/`.
- Traceability: this paired Change Record and the paired archive indexes.

No Framework or MRTS source, Parent Gitlink, workflow permission, or generated
historical report is changed by this Parent record.

## Commands executed

| Command or check | Result |
| --- | --- |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_apache_request_transaction_cleanup tests.test_apache_fail_closed tests.test_apache_connection_phase_contract` | Exit `0`; 22 focused Apache contracts passed. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_nginx_p3_header_fixture tests.test_nginx_upstream_security_contract tests.test_native_api_fail_closed_contract tests.test_nginx_header_iteration_contract` | Exit `0`; 26 focused NGINX contracts passed. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_p1_p4_vector_catalog tests.test_connector_capabilities tests.test_full_lifecycle_profiles tests.test_full_lifecycle_evidence tests.test_apache_phase4_response_regression_wiring tests.test_apache_phase4_rate_limit tests.test_nginx_phase4_runner_wiring tests.test_nginx_bounded_soak_contract` | Exit `0`; 73 bounded P4 contract tests passed with 3 expected runtime skips. |
| `rtk proxy env FRAMEWORK_ROOT=<task-framework-root> APACHE_C_STANDARDS_OUT=<task-owned-build-root> BUILD_ROOT=<task-owned-build-root> make check-apache-c17` | Exit `0`; Apache C17 standards compile passed. |
| `rtk proxy env FRAMEWORK_ROOT=<task-framework-root> BUILD_ROOT=<task-owned-build-root> NGINX_SOURCE_DIR=<task-owned-configured-source> make check-nginx-c17` | Exit `0`; NGINX C17 standards compile passed against the task-owned configured source. |
| `rtk proxy git diff --check` | Exit `0`; no whitespace error was reported. |
| `rtk proxy make check-bilingual-docs` | Exit `1`; the paired Change Record structure passed after correction, while the task worktree lacks its Framework submodule link targets. This does not establish a documentation pass. |

## Runtime evidence

No Apache or NGINX host-runtime result is claimed. The focused tests exercise
the connector contracts and controlled native-fault fixture boundary only. No
production service was contacted.

## Checks not run and rationale

- The non-root Apache loopback runner configured and built but could not start
  because task-filesystem ownership changes returned `EINVAL`, POSIX ACL setup
  was unavailable, and `/tmp` was read-only. No root fallback was used.
- The NGINX native loopback fixture intentionally rejects root execution and
  could not complete unprivileged ownership/ACL preparation for the same
  filesystem reason. No native loopback result is claimed.
- Fresh exact-head hosted checks, review, and SonarQube disposition do not yet
  exist at pre-delivery record creation.

## Known limitations

The unavailable host-runtime prerequisites leave the original host-level
reproduction and legitimate-control proof `blocked_environment`. Static and
fixture evidence does not establish a client-visible HTTP/1.1, HTTP/2, or
HTTP/3 effect. The P4 review remains a bounded no-change decision.

## Remaining risks

The code-level failure paths and focused regressions are available for review,
but the findings remain locally fixed with host verification pending. They are
not promoted to `verified`, and this record neither accepts the residual risk
nor requests a merge.

## Final diff and review status

An independent scoped security-diff review found no concrete bypass in the
Apache/NGINX changes and no weakened test control. Draft PR #360 is open; this
follow-up requires a fresh exact-head readback after its normal push. Hosted
results, review, and any merge remain outside the current evidence.
