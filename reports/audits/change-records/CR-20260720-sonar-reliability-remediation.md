# Change Record: SonarQube Cloud reliability bug remediation

**Language:** English | [Deutsch](CR-20260720-sonar-reliability-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260720-sonar-reliability-remediation` |
| Date (UTC) | `2026-07-20` |
| Base revision | `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` |
| Tracking | Current Parent-master SonarQube Cloud Bug records: `python:S5779`, `python:S1751`, three `c:S2637` locations, `c:S5489`, `c:S836`, and `c:S3519`. |
| Boundary | Parent provisioning, Envoy smoke helper, Traefik engine service, Common authorization service, native oracle, and HAProxy SPOP diagnostics only; Framework and MRTS remain unchanged. |

## Motivation and problem statement

The current Parent SonarQube Cloud analysis at the base revision reports nine
open Bug records. Two Python records use a fragile assertion/error path and a
single-iteration loop. The native records include optional pointer copies whose
null-safety is only implied by a size helper, a wrapper-obscured lock pair, an
uninitialized socket-address analysis path, a nullable JSON-string fallback,
and diagnostics that pass the standard-error stream without an explicit guard.

## Acceptance criteria

- Preserve successful cache publication, valid non-chunked Envoy body reads,
  Traefik result serialization, authorization listener behavior, native JSON
  escaping, and HAProxy startup diagnostics.
- Make null, lock, and socket state explicit without a Sonar suppression,
  rule disablement, exclusion, hotspot disposition, or Quality-Gate change.
- Add focused regression/contract coverage and compile all touched C
  translation units with C17 warnings treated as errors.
- Obtain a fresh exact PR-head SonarQube Cloud analysis before claiming the
  original nine Bug keys are resolved.

## Implementation decision and rationale

The cache publisher replaces three `assert` statements with a private
`require_staging_path` guard that remains effective under optimized Python
execution. The Envoy helper performs the one required first-body-byte receive
directly. Traefik copies optional fields only after both a non-null pointer and
positive bounded size are established; its direct mutex pairs make the
lock/unlock relation visible at each call site. Common
initializes accepted and local socket-address objects. The native oracle emits
an empty JSON string for a null optional value before obtaining a byte cursor,
and HAProxy diagnostics explicitly verify the standard-error stream.

These are narrow, behavior-preserving changes at the existing enforcement or
diagnostic boundaries; no public API, connector protocol, Framework source,
MRTS source, scanner configuration, or quality gate is changed.

## Security impact

The affected paths process native connector results, socket peer information,
and runtime/evidence diagnostics. The changes make absent optional values and
uninitialized state fail or serialize safely while retaining legitimate
non-null, bounded inputs. They do not accept malformed input, lower a resource
limit, weaken validation, or hide a scanner result.

## Changed files

- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/traefik/src/traefik_engine_service.c`
- `common/runtime/http_authorization_service.c`
- `ci/tools/native_modsecurity_oracle.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/test_prepare_runtime_components.py`
- `tests/test_envoy_transport_hardening_contract.py`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_sonar_reliability_contract` | passed: 5 focused source-contract tests. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_envoy_transport_hardening_contract` | passed: 8 Envoy transport controls. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_traefik_native_local_plugin` | passed: 16 Traefik native-plugin/UDS controls. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_prepare_runtime_components.PrepareRuntimeComponentsTest.test_require_staging_path_rejects_absence_and_preserves_path` | passed. |
| `rtk proxy cc -std=c17 -Wall -Wextra -Werror -fsyntax-only ...` for each touched C translation unit | passed for Traefik engine service, Common authorization service, native oracle, and HAProxy SPOP diagnostic runtime. |
| `rtk git diff --check` | passed after the documentation pair. |

## Checks not run and rationale

- A broader `tests.test_prepare_runtime_components` run exercised 38 tests;
  35 passed and three HAProxy cache tests failed before the changed code because
  this isolated Parent worktree has no initialized
  `modules/ModSecurity-test-Framework/ci/provisioning/prepare-haproxy-runtime.sh`.
  The three failures are recorded as an external Framework-worktree prerequisite
  gap, not a passing result.
- Full native connector builds and runtime harnesses require a linkable local
  libmodsecurity installation and/or host source; only C17 syntax validation
  was available in this worktree.
- Fresh GitHub Actions, CodeQL, SonarQube Cloud, review, and PR evidence remain
  delivery checks and have not yet been observed for these local changes.

## Known limitations and remaining risks

The C17 checks and focused contracts prove source-level safety and compatibility
at the touched boundaries, but they are not a fresh SonarQube Cloud result.
The current master also contains independent unreviewed security hotspots and
vulnerability backlog tracked separately; this record does not claim to resolve
them. The final delivery state remains local and uncommitted until the scoped
diff, documentation checks, commit, PR, and exact-head checks are completed.

## Final diff and review status

At creation time the implementation has focused regression/control evidence
and C17 syntax checks. The Change Record pair is intentionally explicit about
the missing Framework prerequisite and pending remote checks. This record does
not authorize a merge.
