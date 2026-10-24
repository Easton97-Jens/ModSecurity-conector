# Engine-owned response inspection limits

**Language:** English | [Deutsch](CR-20261004-engine-owned-response-limits.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261004-engine-owned-response-limits` |
| Date (UTC) | 2026-10-04 |
| Base revision | `9d18eebf6f01e0f370ffa9555e50101612cba11e` |

## Motivation and problem statement

Connector-owned cumulative Phase-4 response budgets duplicated libModSecurity policy and could reject responses that the engine would not inspect, including MIME-excluded responses or configurations using `SecResponseBodyLimitAction ProcessPartial`. The repository-wide target is one ownership rule for Apache, NGINX, HAProxy, Envoy, Traefik and lighttpd: libModSecurity owns WAF response-inspection selection and byte limits; connectors retain only genuine host/transport/resource safety limits.

## Acceptance criteria

- Every valid Phase-4 mode resolves the legacy connector cumulative response-inspection ceiling to an accounting-only maximum instead of a configured WAF byte budget.
- NGINX no longer applies its separate safe/strict cumulative response limit.
- Envoy Common Runtime mode readback disables its cumulative response precheck for off, safe and strict while preserving per-chunk and overflow checks.
- Apache, HAProxy, Common Runtime, Traefik and lighttpd inherit the same ownership rule through shared runtime/helper paths.
- Independent allocation, bounded-storage, chunk/frame, timeout, file-read and arithmetic-overflow protections remain active.
- The target is recorded in `.codex/context/phase4-target-semantics.md` and bilingual reader documentation.

## Implementation decision and rationale

The existing `msconnector_phase4_effective_body_limit` API remains as a compatibility shim. Valid modes return `SIZE_MAX` only as an arithmetic/accounting ceiling; unset or unknown modes still return zero and fail closed. NGINX now uses that shared helper instead of applying its own safe/strict budget branch. Common Runtime forces reject semantics only for impossible response-counter overflow so `ProcessPartial` cannot convert arithmetic overflow into a successful append.

Legacy `modsecurity_phase4_body_limit` parsing is retained to avoid an immediate configuration-breaking change. It remains classified as a native host directive and is marked deprecated in source-backed configuration metadata; its runtime effect is compatibility-only rather than a WAF inspection policy. Removing the public option can be a separate breaking migration.

## Changed files

- `.codex/context/phase4-target-semantics.md`
- `ci/checks/documentation/connector_config_reference.py`
- `common/include/msconnector/phase4_budget.h`
- `common/runtime/msconnector_runtime.c`
- `common/src/directive_spec.c`
- `connectors/apache/README.de.md`
- `connectors/apache/README.md`
- `connectors/apache/src/msc_filters.c`
- `connectors/envoy/README.de.md`
- `connectors/envoy/README.md`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_budget.go`
- `connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go`
- `connectors/haproxy/README.de.md`
- `connectors/haproxy/README.md`
- `connectors/lighttpd/README.de.md`
- `connectors/lighttpd/README.md`
- `connectors/nginx/README.de.md`
- `connectors/nginx/README.md`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/traefik/README.de.md`
- `connectors/traefik/README.md`
- `docs/phase4-mode-budget.de.md`
- `docs/phase4-mode-budget.md`
- `examples/apache/README.de.md`
- `examples/apache/README.md`
- `examples/apache/configuration-reference.de.md`
- `examples/apache/configuration-reference.md`
- `examples/common/common-connector-configuration.de.md`
- `examples/common/common-connector-configuration.md`
- `examples/nginx/README.de.md`
- `examples/nginx/README.md`
- `examples/nginx/configuration-reference.de.md`
- `examples/nginx/configuration-reference.md`
- `reports/connector-configuration-inventory.json`
- `tests/test_nginx_phase4_mode_budget.py`
- `tests/test_phase4_all_connector_budget.py`
- `tests/test_phase4_envoy_budget.py`
- `tests/run_nginx_body_buffer_fixture.py`
- `tests/test_nginx_body_buffer_fixture.py`
- `reports/audits/change-records/CR-20261004-engine-owned-response-limits.md`
- `reports/audits/change-records/CR-20261004-engine-owned-response-limits.de.md`

## Commands executed

No repository-native build/test/documentation command was executed. Repository policy requires RTK for project shell commands; an environment probe found no installed `rtk`, so the task did not silently fall back to unwrapped commands. GitHub connector reads/writes and source-level exact-match checks were used to prepare the branch.

## Security impact

This removes a connector-level rejection path that could terminate otherwise legitimate large or MIME-excluded responses. It does not disable libModSecurity response inspection or its `SecResponseBodyLimit` policy. Independent host and transport resource controls remain required. Paths that buffer responses may still enforce explicit bounded-storage capacity.

## Runtime evidence

GitHub Actions on previous PR head `b17e5374fdb46854066644a83f2e1b366dbc433a` built and exercised the native NGINX exact-head path. Its functional-A runtime reported `passed`; the job later failed because the body-buffer fixture still expected the removed connector budget to reject `memory-over-limit`. That stale expectation was corrected for memory/file/mixed over-limit cases on the current branch. This previous-head result is remediation evidence, not current-head verification.

## Known limitations

Legacy budget configuration remains parseable and can look active to older automation even though it no longer controls WAF response inspection. The branch has source-level, documentation and native-fixture regression changes but no local executed project test result because the mandatory RTK wrapper is unavailable.

## Remaining risks

Native host regressions are required to prove that large responses remain streaming/bounded and that no host-specific buffer path relied exclusively on the removed cumulative inspection budget. Live late-intervention behavior is not changed or proven by this source-level migration.

## Checks not run and rationale

Local `tests.test_nginx_phase4_mode_budget`, `tests.test_phase4_all_connector_budget`, `tests.test_phase4_envoy_budget`, configuration-reference generation checks, bilingual/link checks, native connector builds, host runtime regressions, sanitizers, SonarQube and `git diff --check` were not run because the repository-mandated RTK wrapper is unavailable in this execution environment. Previous-head GitHub CI exposed two task-owned failures: missing German generator mappings and stale NGINX over-limit fixture expectations. Both are corrected; current-head CI and review must verify the remediation.

## Final diff and review status

The change is prepared on a task branch from the recorded base revision and is intended for a Draft pull request. No merge to `master` is authorized or claimed. Current-head CI, review and Quality Gate results are pending.
