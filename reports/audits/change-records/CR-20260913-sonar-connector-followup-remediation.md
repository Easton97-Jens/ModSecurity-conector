# Change Record CR-20260913-sonar-connector-followup-remediation: Parent Connector Sonar follow-up remediation

**Language:** English | [Deutsch](CR-20260913-sonar-connector-followup-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260913-sonar-connector-followup-remediation |
| Date (UTC) | 2026-09-13 |
| Base revision | `7b61b262332be8c89275542c1fa22d6ecb1f57e2` |
| Scope | Parent ModSecurity Connector source, directly affected tests, and this paired traceability record only. No Framework, MRTS, Gitlink, scanner, rule, Quality Gate, suppression, exclusion, dependency, or workflow change. |
| Delivery status | Local candidate on `agent/sonar-connector-followup-20260913`; at this record's creation no commit, push, pull request, merge, or default-branch action has occurred. Exact-head delivery facts require a new PR verification cycle. |
| Policy resolution | The Parent traceability policy requires this English/German Change Record pair for the non-trivial versioned remediation. The archive README is updated as the established index. |

## Motivation and problem statement

Fresh wrapper-authenticated SonarQube Cloud evidence for resulting master
`7b61b262` reported 17 OPEN records: 16 Parent-owned records in ten files and
one separately owned Framework record. The user authorized a Parent-only
follow-up PR to remediate the connector findings. The changes must remove the
Parent findings through behavior-preserving maintenance work rather than
analysis workarounds.

## Acceptance criteria

1. Account for and remediate all 16 current Parent Sonar findings without
   suppressing, accepting, excluding, or weakening analysis and controls.
2. Preserve parser bounds, process/file ownership, event serialization,
   protocol frame limits, timeout, cleanup, restart, and fail-closed behavior.
3. Keep Framework, MRTS, the Gitlink, project settings, rules, Quality Gate,
   dependencies, and workflows unchanged.
4. Verify focused local controls, the final scoped security diff, and the
   exact PR head with SonarQube Cloud and required GitHub checks.
5. Report the remaining Framework issue and aggregate duplication limits
   honestly rather than asserting an unobserved project-wide zero.

## Implementation decision and rationale

- Apply bounded helper extractions to the C and Python cognitive-complexity
  paths while retaining their existing validation, ownership, cleanup, and
  failure behavior.
- Replace only the redundant Apache literal/exception constructs and ambiguous
  Go parameter names; no public interfaces, limits, or behavior are changed.
- Consolidate the HAProxy production-notify task allocation path, which removes
  one current Parent duplicate block without a broad metric-only refactor.
- Keep direct contract tests and add narrow parser-boundary coverage instead
  of deleting or weakening assertions.
- Do not modify the one Framework-owned issue, scanner configuration, Sonar
  settings, Quality Gate, exclusions, or suppressions.

## Security impact

The remediation touches security-relevant event serialization, bounded TCP
table parsing, HTTP request handling, subprocess supervision, SPOP deadlines,
socket/descriptor cleanup, and native ownership transitions. The source review
preserves JSON escaping and redaction, byte/line/frame bounds, malformed-input
rejection, loopback/deadline behavior, `MSG_NOSIGNAL` handling, owner-queue
destruction order, and fail-closed exits. A fresh terminal security-diff scan
is required for this exact candidate; historical PR #361 evidence is neither
used nor accepted as evidence for this follow-up.

## Changed files

- common/src/event.c
- connectors/apache/harness/apache_process_guard.py
- connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go
- connectors/envoy/ext_proc/internal/compositetraefik/uds.go
- connectors/envoy/ext_proc/internal/responseobserver/client.go
- connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c
- connectors/lighttpd/harness/lighttpd_backend_close_linux_guard.py
- connectors/lighttpd/tests/test_backend_close_harness_contract.py
- connectors/traefik/composite_middleware/middleware.go
- tests/http_authorization_service_detached_worker_smoke.c
- tests/test_haproxy_spop_peer_isolation_contract.py
- tests/test_haproxy_spop_selftest_cleanup_contract.py
- tests/test_sonar_reliability_contract.py
- reports/audits/change-records/CR-20260913-sonar-connector-followup-remediation.md
- reports/audits/change-records/CR-20260913-sonar-connector-followup-remediation.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Tests and actual local results

| Check | Actual result |
| --- | --- |
| Envoy response-observer and composite-Traefik Go packages | Passed |
| Traefik composite-middleware Go module | Passed |
| Apache process-guard suite | Passed: 58 tests |
| Combined focused Python contract selection | Passed on the final local source candidate: 191 tests |
| Common C17 helpers | Passed |
| Common security, memory-safety, flow-integrity, and authorization-timeout controls | Passed |
| HAProxy Common adoption | Passed |
| Modified HAProxy source, strict C17 `-Wall -Wextra -Werror -fsyntax-only` | Passed |
| Event/detached-worker focused contracts with ASan/UBSan and event-JSON smokes | Passed |
| Common SDK serialization contract | Passed after the final event-serialization contract reconciliation |
| Lighttpd focused contract suite | Passed: 58 tests |
| HAProxy focused contracts | Passed: 52 tests |
| Task-scoped `make check-haproxy-c17` | Blocked: its helper exits 77 because the isolated Parent worktree intentionally has no Framework `ci/lib/common.sh`; Make reports exit 2 |
| Full HAProxy runtime self-test | Not run: it requires separately provisioned HAProxy/libmodsecurity runtime artifacts and is not substituted by the local static/contract results |

## Commands executed

All recorded commands used the repository's RTK proxy. The completed local
commands include focused Envoy and Traefik `go test` runs, Apache and combined
Python `unittest` selections, the Common and HAProxy Make checks, direct C17
syntax compilation, `gofmt -d`, and `git diff --check`. SonarQube Cloud access
uses only `/usr/local/bin/sonar-with-env`; the fresh exact-head query is still
pending normal PR delivery. A sealed terminal security-diff artifact is the
required pre-delivery evidence for this final local source/documentation
candidate.

## Runtime evidence

No production connector deployment or protected-host runtime was run. The
successful tests are focused local fixtures and native smoke controls; they are
not represented as production-runtime evidence.

## Checks not run and rationale

- The formal terminal security-diff and final complete scoped-diff review run
  after this final versioned-documentation update, before staging.
- Exact PR-head GitHub checks, Sonar Quality Gate, issue/duplication readback,
  review state, and current-base mergeability cannot exist before the normal
  push and PR creation.
- Full HAProxy runtime self-test is not run because the isolated Parent
  worktree lacks separately provisioned HAProxy/libmodsecurity artifacts.
  It is not substituted by the passed local static/contract checks.
- Task-scoped `make check-haproxy-c17` is blocked by the deliberately
  unmaterialized Framework Gitlink; the helper exits 77 before compilation.

## Known limitations

- The remaining project finding is Framework-owned:
  `AaA34UWlbqrRc02noCI3` (`python:S1192`) at
  `modules/ModSecurity-test-Framework/ci/checks/catalog/five_connectors_with_crs_no_mrts.py:112`.
  It remains outside this Parent-only PR.
- The default-branch aggregate of 1,939 duplicate lines / 83 blocks / 0.3%
  includes Framework content. Only an exact PR-head scan can prove this task's
  new-code and task-owned duplicate result; a resulting-master aggregate
  requires a separately authorized merge and later analysis.

## Remaining risks

FND-PARENT-1088's acceptance is limited to unavailable historical PR #361
payloads. It does not waive, replace, or supply any evidence for this PR.
GitHub checks, current-base mergeability, review state, the exact PR-head Sonar
Quality Gate, OPEN/CONFIRMED inventory, and duplication readback remain pending
until normal delivery creates the PR.

## Final diff and review status

At this record update, all 16 Parent findings have a scoped source/test
remediation and the final local 191-test selection plus the Common SDK
serialization contract pass. The candidate remains uncommitted until the
terminal security-diff, complete diff, and delivery preflights finish. The
final state is not yet claimed as verified. No merge is authorized or asserted.
