# Change Record CR-20260913-sonar-connector-followup-remediation: Parent Connector Sonar follow-up remediation

**Language:** English | [Deutsch](CR-20260913-sonar-connector-followup-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260913-sonar-connector-followup-remediation |
| Date (UTC) | 2026-09-13 |
| Base revision | `7b61b262332be8c89275542c1fa22d6ecb1f57e2` |
| Scope | Parent ModSecurity Connector source, directly affected tests, and this paired traceability record only. No Framework, MRTS, Gitlink, scanner, rule, Quality Gate, suppression, exclusion, dependency, or workflow change. |
| Delivery status | Open, non-draft PR [#368](https://github.com/Easton97-Jens/ModSecurity-conector/pull/368) on `agent/sonar-connector-followup-20260913`, base `master`, at verified remediation source head `40a55c9b481e595087d2bbbe272f824d10857195`. Its exact-head hosted cycle reported 37 successful and six intentionally skipped GitHub checks, no failed/cancelled/pending checks, a mergeable PR with no reviews or inline review comments, Sonar Quality Gate `OK`, zero PR-scoped `OPEN`/`CONFIRMED` records, and zero new duplicated lines/blocks (`0.0%`). The shared PR aggregate was 1,875 duplicated lines / 81 blocks / 0.2%. This is pre-merge evidence only: master integration is user-authorized but not yet performed. |
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
- Replace the helper's newly reported long parameter list with the already
  initialized production-result context, and make two read-only pointers
  `const`; this resolves the three first-readback C findings without changing
  task ownership, join ordering, or response handling.
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
destruction order, and fail-closed exits. The post-readback terminal
security-diff completed with complete coverage and zero reportable findings for
this exact candidate; historical PR #361 evidence is neither used nor accepted
as evidence for this follow-up.

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
| Combined focused Python contract selection | Passed before the three post-readback C corrections: 191 tests |
| Common C17 helpers | Passed |
| Common security, memory-safety, flow-integrity, and authorization-timeout controls | Passed |
| HAProxy Common adoption | Passed |
| Modified HAProxy source, strict C17 `-Wall -Wextra -Werror -fsyntax-only` | Passed |
| Event/detached-worker focused contracts with ASan/UBSan and event-JSON smokes | Passed |
| Common SDK serialization contract | Passed after the final event-serialization contract reconciliation |
| First PR #368 SonarQube Cloud readback (historical) | Quality Gate `OK` and zero new duplicated lines/blocks, but three OPEN helper-introduced C findings (`c:S107` and two `c:S995`); corrected in the subsequent remediation-source head |
| Final remediation-source-head `40a55c9b481e595087d2bbbe272f824d10857195` hosted readback | Passed: Quality Gate `OK`; PR-scoped `OPEN`/`CONFIRMED` inventory zero; new duplicated lines/blocks and density zero; shared aggregate 1,875 duplicated lines / 81 blocks / 0.2%; 37 GitHub checks succeeded and six were intentionally skipped, with none failed, cancelled, or pending |
| Post-readback selected focused contract selection | Passed: 161 tests |
| Post-readback HAProxy source, strict C17 `-Wall -Wextra -Werror -fsyntax-only` | Passed |
| Post-readback HAProxy/Sonar focused contracts | Passed: 38 tests |
| Post-readback detached-worker timeout/lifecycle smoke | Passed |
| Lighttpd focused contract suite | Passed: 58 tests |
| HAProxy focused contracts | Passed: 52 tests |
| Task-scoped `make check-haproxy-c17` | Blocked: its helper exits 77 because the isolated Parent worktree intentionally has no Framework `ci/lib/common.sh`; Make reports exit 2 |
| Full HAProxy runtime self-test | Not run: it requires separately provisioned HAProxy/libmodsecurity runtime artifacts and is not substituted by the local static/contract results |

## Commands executed

All recorded commands used the repository's RTK proxy. The completed local
commands include focused Envoy and Traefik `go test` runs, Apache and combined
Python `unittest` selections, the Common and HAProxy Make checks, direct C17
syntax compilation, `gofmt -d`, and `git diff --check`. SonarQube Cloud access
uses only `/usr/local/bin/sonar-with-env`. The first exact PR #368 readback
returned Quality Gate `OK`, zero new duplicated lines/blocks, and three OPEN
task-owned C findings; the focused C17, contract, and detached-worker smoke
checks passed after their local correction, including the selected 161-test
contract selection. The final exact remediation-source-head readback for
`40a55c9b481e595087d2bbbe272f824d10857195`, recorded at
`2026-09-13T12:47:29Z`, then returned Quality Gate `OK`, zero PR-scoped
`OPEN`/`CONFIRMED` records, zero new duplicated lines/blocks, and a clean
GitHub check rollup of 37 successes and six intentional skips. The
post-readback terminal security-diff completed with complete coverage and zero
reportable findings. Those are pre-merge results and do not assert any
resulting-master analysis.

## Runtime evidence

No production connector deployment or protected-host runtime was run. The
successful tests are focused local fixtures and native smoke controls; they are
not represented as production-runtime evidence.

## Checks not run and rationale

- The post-readback formal terminal security-diff completed with complete
  coverage and zero reportable findings. A final staged scoped-diff review and
  a fresh delivery preflight remain required immediately before protected
  integration.
- The exact remediation-source-head `40a55c9b481e595087d2bbbe272f824d10857195`
  GitHub checks, Sonar Quality Gate, issue/duplication readback, review state,
  and current-base mergeability completed successfully. They do not certify a
  later documentation-only head or any resulting-master analysis.
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
- The historical default-branch aggregate of 1,939 duplicate lines / 83 blocks
  / 0.3% includes Framework content. The final remediation-source-head shared
  aggregate was 1,875 duplicated lines / 81 blocks / 0.2%. The exact PR-head
  scan proves this task's zero new-code duplication result, not a project-wide
  zero; a resulting-master aggregate requires protected integration and later
  analysis.

## Remaining risks

FND-PARENT-1088's acceptance is limited to unavailable historical PR #361
payloads. It does not waive, replace, or supply any evidence for this PR. The
first PR #368 readback identified three helper-introduced C findings; their
correction is covered by the final exact remediation-source-head readback for
`40a55c9b481e595087d2bbbe272f824d10857195`. The PR remains open and master
integration is user-authorized but not yet performed. Fresh current-head,
review, mergeability, Sonar, and resulting-master evidence remains required
immediately before and after that protected integration.

## Final diff and review status

At this record update, all 16 Parent findings have a scoped source/test
remediation. The first hosted scan also identified three helper findings; the
long-parameter and read-only-pointer corrections passed their direct C17,
selected 161-test contract, 38-test focused subset, and detached-worker smoke
checks. The terminal security-diff has complete coverage with zero reportable
findings, and the final remediation-source-head hosted cycle reported a clean
PR-scoped Sonar inventory and GitHub check rollup. The PR remains open and
unmerged. This record does not assert a master merge: protected integration is
user-authorized but must be preceded by a fresh exact-head delivery preflight,
and any resulting-master state must be observed separately.
