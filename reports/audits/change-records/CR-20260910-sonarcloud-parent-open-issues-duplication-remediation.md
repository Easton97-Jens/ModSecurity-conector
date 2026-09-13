# Change Record CR-20260910-sonarcloud-parent-open-issues-duplication-remediation: Parent SonarCloud quality remediation

**Language:** English | [Deutsch](CR-20260910-sonarcloud-parent-open-issues-duplication-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260910-sonarcloud-parent-open-issues-duplication-remediation |
| Date (UTC) | 2026-09-10 |
| Base revision | 26a560e64cbaf906c0d35bba199f65436830d1dd |
| Scope | Parent ModSecurity Connector only; no Framework, MRTS, Gitlink, scanner, rule, Quality Gate, suppression, or exclusion change. Delivery integration is controlled separately. |
| Delivery status | `f3748bf7a91b82dc892bb89fc08b17435cc70230` is the historical refreshed-source snapshot, not the current PR head. Its documentation successor `38cb79d0b738b7ddb39603dea0c6e7337a08583c` completed its exact hosted/Sonar readback before this correction. The current user authorized only PR #361's protected squash integration into `master` and accepted only the separately tracked FND-PARENT-1088 historical-evidence risk. This factual correction creates one normal successor head, which requires complete new exact-head verification before merge. |
| Policy resolution | The Parent traceability policy requires this paired Change Record for a non-trivial versioned product change. It uses the established archive location; no parallel format or index is introduced. |

## Motivation and problem statement

The user requested remediation of the 113 SonarCloud open issues and 0.3%
duplication metric using a PR, restricted to the ModSecurity Connector. Current
authenticated baseline evidence contains 113 OPEN CODE_SMELL records: 112
Parent-owned records and one Framework-owned record. The Parent code requires
real behavior-preserving maintenance refactors rather than scanner workarounds.

## Acceptance criteria

1. Deliver only Parent-owned Connector source, test, and traceability changes.
2. Preserve runtime, parser, process, filesystem, protocol, serialization,
   timeout, ownership, cleanup, and fail-closed controls.
3. Do not use NOSONAR, accepted issues, exclusions, scanner/rule/Quality-Gate
   changes, deleted tests, or weakened assertions.
4. Verify the immutable exact PR head with SonarCloud issue, duplication, and
   Quality Gate readback plus applicable GitHub checks.
5. Report the separately owned Framework issue and cross-owner duplicate blocks
   explicitly rather than claiming an unobserved project-wide zero.

## Implementation decision and rationale

- Refactor the identified Parent code-smell groups in place: cognitive
  complexity, parameter counts, nested control flow, duplicate literals,
  exception contexts, and real duplicate control/test blocks.
- Extract narrowly scoped helpers only when they preserve existing public
  behavior and security controls; retain connector-specific tests rather than
  using generic weakening or deletion.
- Keep Framework, MRTS, Gitlinks, SonarCloud project settings, rules, and
  Quality Gate unchanged. The one Framework issue is tracked by FND-SONAR-0004.
- Treat the 820 known Parent/Framework sibling duplicate lines as
  FND-CROSS-0010. A Parent-only PR can reduce its own actual duplicate blocks
  but cannot remove cross-owner content without a separate authorization and
  delivery lifecycle.
- A local Sonar Vortex analysis was unavailable for the organization, so the
  authoritative closure evidence is the eventual exact PR-head SonarCloud
  analysis, not a substituted local scanner result.

## Security impact

The change touches security-sensitive event serialization, HTTP/SPOA
protocol handling, subprocess supervision, PID/descriptor identity, filesystem
evidence publication, native CGo cleanup, and loopback control paths. The
implementation retains JSON escaping, provenance bounds, URI-query redaction,
frame bounds, deadlines, loopback binding, PID reuse and peer checks,
O_NOFOLLOW descriptor walks, cleanup ownership, and fail-closed behavior.

The historical 28-file security-diff receipt is unavailable and tracked by
FND-PARENT-1088; it is not represented as newly readable evidence. The
historical refreshed-source scan for `f3748bf7` covers its generated 17-path
Parent source inventory, reports zero reportable findings, and is retained at:

/var/tmp/codex/ModSecurity-conector/runs/sonar-pr361-refresh-20260913/security-diff/report.md

Its SHA-256 is 59a2e82783a7e141ac5078162a47775faedde7dae48677b1f10e71d19804babe.
The observed successor `38cb79d0` has a retained full 37-path Parent review
receipt at
`/var/tmp/codex/ModSecurity-conector/runs/sonar-pr361-refresh-20260913/evidence/pr361-full-diff-review-38cb-20260913.md`
(SHA-256 `7c68d66d9c26d2261aeb85e8574e2a3795e609382d0ad1052d0b44e33257fb9f`).
It records a no-reportable-finding disposition for the additional CI/control,
test, and documentation paths; FND-PARENT-1089 tracks the required final
canonical full-diff coverage and this factual correction. No deployment runtime
was exercised.

## Changed files

- ci/checks/connectors/apache/check-apache-common-adoption.py
- ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py
- ci/checks/documentation/connector_config_reference.py
- ci/runtime/lifecycle/with-crs-no-mrts-profile.py
- common/src/event.c
- common/src/json_escape.c
- connectors/apache/harness/apache_process_guard.py
- connectors/apache/harness/run_apache_smoke.sh
- connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go
- connectors/envoy/ext_proc/internal/processor/processor.go
- connectors/envoy/ext_proc/internal/processor/processor_test.go
- connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh
- connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c
- connectors/lighttpd/harness/lighttpd_backend_close_linux_guard.py
- connectors/lighttpd/harness/lighttpd_backend_close_probe.py
- connectors/lighttpd/harness/lighttpd_stock_lifecycle_probe.py
- connectors/lighttpd/harness/run_lighttpd_backend_close.sh
- connectors/lighttpd/harness/run_lighttpd_stock_lifecycle.sh
- connectors/lighttpd/tests/test_backend_close_harness_contract.py
- connectors/nginx/harness/run_nginx_smoke.sh
- connectors/traefik/native_middleware/engine_uds_test.go
- connectors/traefik/native_middleware/middleware_test.go
- tests/http_authorization_service_detached_worker_smoke.c
- tests/http_authorization_service_peer_close_smoke.c
- tests/test_apache_with_crs_profile_evidence_contract.py
- tests/test_apache_smoke_case_output_root.py
- tests/test_event_runtime_security_contract.py
- tests/test_haproxy_spop_peer_isolation_contract.py
- tests/test_haproxy_spop_selftest_cleanup_contract.py
- tests/test_haproxy_spop_sigpipe_peer_isolation_contract.py
- tests/test_protected_nginx_broker_caller.py
- tests/test_sonar_reliability_contract.py
- tests/_haproxy_spop_contract_helpers.py
- reports/audits/change-records/CR-20260910-sonarcloud-parent-open-issues-duplication-remediation.md
- reports/audits/change-records/CR-20260910-sonarcloud-parent-open-issues-duplication-remediation.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

All recorded commands were RTK-proxied. The current reconciliation used the
terminal generated source inventory, exact `git diff --no-ext-diff` full-path
comparison, full-file static security review, GitHub exact-head check readback,
and `/usr/local/bin/sonar-with-env` PR #361 readbacks. Their actual outcomes are
listed below; this correction's successor receives its own fresh hosted
verification and does not inherit these results.

## Tests and actual results

| Check | Actual result |
| --- | --- |
| make check-haproxy-c17 | Passed |
| make check-haproxy-common-adoption | Passed |
| make check-common-helpers-c17 with task-owned BUILD_ROOT | Passed |
| make check-connector-config-reference | Passed |
| make check-http-authorization-service-timeout with task-owned BUILD_ROOT | Passed |
| Offline Envoy go test ./... with GOPROXY=off | Passed |
| Offline Traefik go test ./... with GOPROXY=off | Passed |
| Apache process-guard suite | Passed: 58 tests |
| Lighttpd backend-close contract | Passed: 57 tests |
| Lighttpd stock-lifecycle contract | Passed: 11 tests |
| with-CRS/no-MRTS profile suite | Passed: 23 tests |
| HAProxy cleanup plus NGINX broker contracts | Passed: 15 tests |
| Event runtime security contract | Passed: 7 tests |
| Shell syntax checks for five changed shells | Passed |
| gofmt -d for changed Go paths | Passed; no output |
| git diff --check against base | Passed |
| Formal security-diff scan | Passed; complete coverage of its generated 17-path source inventory, zero reportable findings |
| Second-cycle final security-diff scan | Passed; complete coverage of its generated 17-path source inventory, zero reportable findings |
| Third-cycle final test-deduplication security-diff scan | Passed; complete coverage of its generated 17-path source inventory, zero reportable findings |
| Final HAProxy helper/peer/SIGPIPE/self-test/Sonar-reliability contract run | Passed: 48 tests |
| Final helper and two consumer Python compilation | Passed |
| Isolated Apache parent-SIGKILL candidate/baseline recheck | Passed: 1.395s candidate, 1.327s baseline |
| Exact `f3748bf7a91b82dc892bb89fc08b17435cc70230` GitHub check-run readback | Passed: 43 terminal runs; 37 successful, 6 intentional skips, 0 failures or pending runs |
| Exact `f3748bf7a91b82dc892bb89fc08b17435cc70230` SonarQube Cloud readback | Passed: Quality Gate `OK`, 0 OPEN/CONFIRMED issues, 0 new duplicated lines/blocks, and 0.0% new-code duplication |
| Observed `38cb79d0b738b7ddb39603dea0c6e7337a08583c` GitHub check-run readback | Passed: 43 terminal runs; 37 successful, 6 intentional skips, 0 failures or pending runs, including required contexts and SonarCloud Code Analysis |
| Observed `38cb79d0b738b7ddb39603dea0c6e7337a08583c` SonarQube Cloud readback | Passed: Quality Gate `OK`, 0 OPEN/CONFIRMED issues, 0 new duplicated lines/blocks, and 0.0% new-code duplication |
| Observed `38cb79d0b738b7ddb39603dea0c6e7337a08583c` full 37-path Parent review | Passed: every changed path accounted for; 0 reportable security findings; the factual successor still needs its own canonical exact-head artifact and hosted verification |

The intermittent earlier Apache parent-SIGKILL timeout is tracked as
FND-PARENT-1084. It was observed against candidate and baseline, then did not
reproduce in current isolated rechecks; no timeout or assertion was weakened.

## Runtime evidence

No production connector deployment was run. Focused test fixtures exercise
local process, protocol, and lifecycle controls only and are not presented as
deployment or protected-host evidence. The completed static security-diff scan
and focused regression/control suites are the available local evidence.

## Checks not run and rationale

- The observed pre-correction head `38cb79d0b738b7ddb39603dea0c6e7337a08583c`
  has completed successful hosted checks, but this correction creates a new
  successor with no hosted result yet. Its exact GitHub checks,
  review/conversation state, SonarQube Cloud Quality Gate, OPEN/CONFIRMED issue
  inventory, duplication measures, current-base mergeability, and canonical
  full-diff artifact must be re-read after normal push; no predecessor result
  is reused as evidence for that different head.
- Resulting-master workflows and default-branch SonarQube Cloud analysis do
  not exist until an exact-head-protected authorized squash merge occurs.
- Local Sonar Vortex analysis: unavailable for the organization.
- One Apache with-CRS profile-publication test: blocked because the isolated
  Parent worktree lacks the separately owned Framework case CLI. Framework
  content and the Gitlink were not hydrated or changed.
- Full ShellCheck: blocked by pre-existing warnings in unchanged Apache/NGINX
  lines; no warning was suppressed.
- make check-bilingual-docs and make check-doc-links: run after the paired
  record and archive-index updates. Both are blocked only by existing links to
  targets under the unmaterialized Framework Gitlink; neither reports a
  Change-Record heading or paired-language error.

## Known limitations

The default baseline has one Framework-owned OPEN issue:
AaA34UWlbqrRc02noCI3, python:S1192, at
modules/ModSecurity-test-Framework/ci/checks/catalog/five_connectors_with_crs_no_mrts.py:112.
It cannot be fixed in this Parent-only task.

The baseline aggregate is 2,146 duplicated lines, 92 blocks, 696,956 NCLOC,
and 0.3% density. 820 known Parent/Framework sibling lines remain outside the
authorized scope. A PR can prove only exact-head new-code/task-owned results;
a default-branch project metric requires a later authorized merge and
resulting-master analysis.

## Remaining risks

The user accepted only FND-PARENT-1088's precise historical-evidence risk:
ten prior PR #361 payloads cannot be restored or rehashed. That decision allows
only the necessary factual delivery-evidence refresh and protected squash merge
of this PR; it neither verifies nor closes the finding, waives controls, or
extends to cleanup, another PR, release, repository, later unrelated head,
direct `master` push, force operation, rebase, bypass, or merge-method change.
Framework ownership and cross-repository duplication remain explicit scope
limits for a literal project-wide zero result.

FND-PARENT-1089 is not risk-accepted. It records the prior 17-path/37-path
coverage and stale-head-fact gap and blocks integration until this normal
successor has its complete canonical review and fresh exact-head evidence.

## Delivery reconciliation before final documentation follow-up — 2026-09-10

- Branch: `agent/sonarcloud-open-issues-duplication-20260910`.
- Initial source-and-record commit:
  `ed78748e15cafda884ae819482f91e7d3f7c7d9e`
  (`fix: remediate Parent SonarCloud quality issues`).
- Follow-up source commits:
  `920f478f5c894bc9b51a12686aef10b43b829afc`
  (`fix: resolve remaining SonarCloud issues`),
  `982b7d908f82f99680341cfab152ed8cc9062903`
  (`fix: clear final SonarCloud residuals`), and
  `963468c0c1ca43e4c8708e57e6c2ad87465a6faf`
  (`test: deduplicate HAProxy SPOP contract assertions`).
- Local, remote, and PR source heads matched
  `963468c0c1ca43e4c8708e57e6c2ad87465a6faf` at the final source readback.
- Pull request: [#361](https://github.com/Easton97-Jens/ModSecurity-conector/pull/361)
  against `master`; it was OPEN and not a draft.
- The source head is mergeable with `mergeStateStatus` `BLOCKED` while hosted
  checks run; no review decision or merge is recorded.
- SonarCloud's exact source-head analysis is `OK` with zero Parent
  OPEN/CONFIRMED issues, zero new duplicate lines/blocks, and aggregate
  duplicate reduction of 227 lines / 11 blocks. The displayed aggregate
  density remains 0.3% because it is rounded.
- This historical reconciliation was delivered as a normal documentation-only
  follow-up without amend, force-push, or merge. Its later exact successor
  heads are recorded below only after they exist.

## Delivery refresh pre-successor snapshot and current authorization — 2026-09-13

- Historical refreshed-source snapshot:
  `f3748bf7a91b82dc892bb89fc08b17435cc70230`. Observed pre-correction Parent
  PR #361 head, remote task branch, and refresh worktree head:
  `38cb79d0b738b7ddb39603dea0c6e7337a08583c`; base:
  `9c467ca1ad1c086e9d379ae3cdb7da6d130daf5f`.
- The observed pre-correction readback reported the PR OPEN, non-draft, with no
  reviews, review threads, or inline review comments. Its 43 exact-head runs
  are terminal: 37 successful, six intentional skips, and zero failures or
  pending runs, including the six strict ruleset contexts and `SonarCloud Code
  Analysis`.
- SonarQube Cloud reported Quality Gate `OK`, zero OPEN/CONFIRMED issues, zero
  new duplicated lines/blocks, and 0.0% new-code duplication for that observed
  head. Its aggregate is 1,939 duplicate lines / 83 blocks / 0.3% rounded, 227
  lines / 11 blocks below the current default-branch aggregate; this is not a
  project-dashboard-zero claim.
- At `2026-09-13T08:23:26Z`, the current user explicitly authorized Parent PR
  #361's protected squash integration into `master` and accepted only the
  documented FND-PARENT-1088 residual risk. The acceptance remains limited to
  this PR's necessary factual evidence refresh and protected squash merge.
- The full 37-path static review of `38cb79d0` found no reportable security
  finding. It also exposed FND-PARENT-1089: the prior canonical source
  inventory alone did not represent every changed path, and the record needed
  current-head wording. This paired record is the necessary normal correction.
  Its successor must complete a new exact-head review, GitHub-check, SonarQube
  Cloud, mergeability, and base-freshness cycle before it can be squash-merged;
  no resulting-master status is claimed here.

## Final diff and review status

Local source, test, formatter, diff, and security reviews are complete for the
observed `38cb79d0` candidate, including its full 37-path review receipt. That
pre-successor head has satisfied the task-owned SonarQube Cloud issue and
new-duplication criteria. This paired factual delivery-record correction is a
normal follow-up commit; its resulting successor head, canonical full-diff
artifact, hosted checks, SonarQube Cloud result, review round, and protected
squash merge remain pending their own exact-head evidence. The user has
authorized that single protected integration but not a direct push, bypass, or
unrelated delivery action.
