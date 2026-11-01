# Change Record: HTTP/2 and HTTP/3 protocol parity workstream

**Language:** English | [Deutsch](CR-20260826-http2-http3-protocol-parity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260826-http2-http3-protocol-parity` |
| Date (UTC) | 2026-08-26 |
| Base revision | `6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` |
| Delivery status | Committed as `5e7b34d1887984f74d061872d7652a3f71d87856`, pushed to `feature/http2-http3-protocol-parity`, and represented by Draft PR [#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348); local, remote, and PR head matched at initial delivery verification. No merge. |

## Motivation and problem statement

### Test-ownership integration checkpoint — 2026-11-01

The user authorized adopting Parent master
`a6001a09210bc9516256d28af5da45d73f0fe2f2` after the completed test migration.
Fifteen modify/delete conflicts concern thirteen now Framework-owned checker/
test sources and two generated selection/archive files. Their old Parent paths
are removed, not resurrected. The thirteen branch-only deltas are preserved at
their mapped Framework paths and in the retained original `db431efa` history;
the generated schema-5 inventory/archive must be regenerated, not copied back.
The migrated default inventory remains capped at 100 cases.

The completed ports preserve 24 definitions (19 Go, five Python). Native
generation preserves 100 standard cases / 80 executions and 1993 baseline IDs;
the optional catalog contains 2586 cases / 1140 executions. The initial 526
Framework bindings became 528 after #147, as recorded below. No old Parent
test path is restored.

[Framework PR #148](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/148)
includes the ports and verified #143/#144 integrity fixes. Its authorized
regular squash merge completed at `2026-11-01T19:09:19Z`; the remotely verified
Framework master at that checkpoint was
`91f5370c7eddcebdc7e49d2099c58054ec2d5d5d`. The final PR
head passed 15 hosted checks with three intended skips; exact-head direct
Sonar readback reported gate OK, all five conditions and zero open PR issues.
All seven master workflows on `91f5370c` subsequently succeeded. Direct master
Sonar analysis at `2026-11-01T19:26:02Z` passed all five conditions: ratings
1 <= 1, duplication 0 <= 3%, hotspots 100 >= 100%. PRs #143/#144 are closed
unmerged with reference to #148; branches `b7d643f` / `9e49913` are retained.
These are separate PR-head/master observations, not future-head acceptance.
Parent #348 stays an unmerged Draft; Framework merge authority does not
authorize a Parent master merge. No MRTS change or broad TLS/H2/H3
qualification campaign is included. Prior dated evidence remains historical.

Required final native checks uncovered migration-integrity defects. Parent
`scripts/generate_compiler_guides.py` now maps the NGINX preparer's public
`source_path` and corrects the actual migrated Apache/HAProxy harness links.
All 18 generated guide outputs remain byte-identical to tracked files. The
Parent projection/revision/candidate selection passed 55 tests; native Apache
initially passed 21 tests and failed one stale full-AST golden expectation.

[Framework Draft #150](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/150)
was first published at `e1b4f8b24ab95749d685db3e6581e26da302dd57`, based on `91f5370c`.
Its 11 files repair only two existing test modules plus generated bindings,
paired documentation and Change Record: compiler expectations/actual forwarded
Make targets and the independently audited full-AST golden. Six migration-
context transforms reconstruct the checker byte-identically since #142; all
predicates, messages, order and controls remain. Combined 44 methods passed
in 27.660 seconds; eight actual-target controls and 26 independent isolated
parser controls passed. Native Apache with #150, NGINX and Common C17 passed.
Native generators/bindings/admission preserve 100/80 standard, 2586/1140
optional, 526 fixed Framework bindings, 235 Product paths and 1993 baseline IDs.
The new paired integration record and documentation passed 350-pair and four
canonical checks; independent code/catalog and EN/DE review found no blocker.
No new methods/selectors/versions, weakened gates or MRTS writes are included.

Framework #147 independently advanced master to
`5ef57603a4933f18c988f1f9f32b93f478182440` with host-execution-context
preflights. A normal merge into #150 produced current published head
`af6997be5c5cee38e3feb9274c3269d52784bbe1`, based on that master. The sole
inventory conflict was resolved by native regeneration, retaining both new
preflight bindings and five default consumers plus the compiler hash. Independent
comparison against `5ef57603` finds exactly the intended compiler-test hash
difference; master dependency indices and both test fixes are retained.
Current inventory SHA-256 is
`147ebacc795c634bd9d4b21cfbcd408e635dd55de8b757be2671d3b056ac1cb8`:
528 fixed Framework bindings / 235 Product paths; 100/80 standard, 2586/1140
optional and 1993 baseline IDs unchanged. Fresh 44-method validation passed in
26.138 seconds. Native generation/checks, public admission, 354 bilingual
checks, 2159 path checks with zero obsolete paths, record/link and four canonical
checks passed; independent inventory/EN-DE review found no blocker. The earlier
#150 native Parent `check-compiler-guides ON_DEMAND_TESTS=1` entrypoint passed
22 tests in 0.848 seconds, retaining all 18 guide outputs byte-identically.
No additional host campaign, tests, selectors, versions, gate changes or MRTS
writes accompany this master synchronization. The first candidate's earlier
results remain historical and do not establish current-head hosted acceptance.

Framework #150 was actually squash-merged with an exact-SHA guard at
`2026-11-01T20:11:25Z`, producing official master
`b85280278310f4034af78149ac13671438965c7b`. Its complete tree equals `af6997be`.
That PR head passed 12 checks / three intended skips; direct Sonar analysis at
`2026-11-01T20:03:53Z` passed all five conditions (ratings 1 <= 1, duplication
0 <= 3%, hotspots 100 >= 100%) and the complete OPEN/CONFIRMED query returned
zero issues. Three CodeQL Analyze/Post-Analyze configurations passed in bounded
without-upload mode. New `b8528027` master CI is pending, not inherited from
the PR. GitHub's configured auto-delete removed #150's remote branch; its local
branch/worktree remain, and #143/#144 branches remain unchanged as requested.

Independent Parent #435 merged at `2026-11-01T19:49:13Z` into master
`2abad408cae7e5a103d12a9a9e432129bfe0468f`, inheriting Framework pin `e628`,
not `91f5370c`. A clean normal merge produced local Parent
`5b5a4a89aa9cb55b0b95b485611aadb78f276185`; only the incoming 12 middleware
lines are composed with the parity changes. Independent source/security review
found no P3/EOS/protocol regression. Twenty-three pin projections match master;
MRTS/version values are unchanged. The earlier generated intermediate views
were backed up externally before the merge; task source/docs were preserved.

Bounded merge-interaction unit validation passed 16 parity plus six informational
selectors: 22 top-level tests, 53 passing test/subtest terminals plus a package
pass, 48 leaves including all 31 informational leaves, zero failures/skips and
no race report. This used the merged worktree before the local merge commit,
not a whole-committed-head qualification. Its middleware SHA-256 remains
`b8df119f43332c00e7308478cae3f84a5f2d015a96e8d4e9c18d74261e73884b`
after commit. This is real httptest unit evidence, not native-host, private
Common-service, TLS/H2/H3 or MRTS execution.

Final local pin alignment is implemented, not yet committed/pushed: nested
Framework and staged gitlink are exact `b8528027`; native lock plus 22 workflow
views are synchronized. Native pre-candidate `e628` → `b8528027`, 23-file sync,
no-drift check and post-candidate `b8528027` checks passed, both using NGINX
`release-1.31.6`. The immutable Common helper blob matches exact Framework
`b8528027:ci/lib/common.sh`. Combined final-pin Python validation passed all
99 existing methods in 60.799 seconds (7 projection, 19 revision, 29 candidate,
22 compiler, 22 Apache), using Parent `5b5a4a89` plus task edits and Framework
`b8528027`. Intentional negative SHA diagnostics in unittest output are not a
native candidate failure. Native NGINX adoption and Common C17 helper checks
passed with `-std=c17 -Wall -Wextra -Werror`. Public inventory admission passed
with SHA-256 `147ebacc795c634bd9d4b21cfbcd408e635dd55de8b757be2671d3b056ac1cb8`,
100 default / 2686 total / 2586 optional cases and a truthfully dirty Parent
worktree; admission is not test execution. Staged/unstaged whitespace checks
passed. Final guide-byte diff confirmed all 18 outputs unchanged; native
Parent bilingual, repository-path and documentation-link checks passed.
Commit/push and new-head CI/Sonar remain pending at this preparation snapshot.

Framework `b8528027` master CodeQL/Common/Scorecard workflows have succeeded;
lint/Sonar are in progress. Exactly five master workflows were triggered.
The security-Python and five-connector contract workflows are not applicable:
none of the 11 changed paths matches their checked-in push filters. They are
not counted as passing, skipped or missing. MRTS remains
uninitialized/read-only, so strict local actual-materialization verification
is unavailable. Immutable-chain/native pin checks are distinct from fresh
hosted actual-checkout evidence. Parent #348 remains an unmerged Draft at
published `db431efa`; local `5b5a4a89` plus final pin edits is unpublished.
No Parent master merge is authorized.

An initial check against the old d503 checkers rejected the merged product:
NGINX reported three obsolete exact-pattern contracts and Apache rejected the
negotiated Phase3 protocol call (both Make exit2). These are compatibility
failures requiring the preserved Framework checker changes, not failing
product-runtime evidence. Integrated Framework-stage checkers now pass, as do
12 selected Python methods, 43 protocol methods, four QUIC helper methods,
Common C17, 348 documentation pairs and canonical checks. These are bounded
static/unit/compile results, not real negotiated host-protocol evidence.

The post-#146 Traefik race selection passed 16 parity tests / 18 terminals.
The earlier full Traefik result (173 pass terminals, one real-service skip)
predates #146. Before `2abad408` integration, its 31 new informational leaves
were compiled but NOT_RUN, because selected external Parent `b43faa78` lacked
their separate Product fix and #435 was then closed unmerged. This historical
limitation is superseded by the bounded merge-interaction unit proof above,
not a full host qualification. The earlier
Envoy race run covered eight packages / 392 pass terminals without failures
or skips. Local Go 1.27.3 matches the selected toolchain; both module minimum
directives remain 1.26.9. This is not live host/protocol qualification.
Dependency-setup and overlong AF_UNIX failures remain recorded, not converted
to passes. Parent source is external validation input; production context
guards are unchanged and mutation fixtures use real post-mutation Git binding.

This independent Parent workstream records evidence for HTTP/2 and HTTP/3
lifecycle parity across Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd,
while retaining HTTP/1.1 as the regression baseline. It is in progress and is
not a completion claim.

## Acceptance criteria

- Keep protocol, stream identity, commit, EOS, and late-intervention status
  separate for each selected connector.
- Model `unknown`, H1, H2, and H3 in the neutral Common contract without
  promoting that model into adapter proof.
- Record H3 independently and never claim H3 runtime without real traffic.
- Preserve source-level fixed / runtime not verified wording where runtime
  evidence is absent.
- Maintain equivalent English and German documentation and traceability.

## Implementation decision and rationale

Common has a neutral protocol/late-intervention model for `unknown`, H1, H2,
and H3, including stream identity, commit/EOS, and stream-reset selection. This
does not prove all adapters use it.

Apache P3 now derives protocol from `ap_get_protocol(r->connection)` plus
canonical HTTP/1 `r->proto_num`, and unknown protocol fails closed. Common
conservatively does not emit a stream reset for H2 stream ID 0 or a freely set
`STREAM_RESET`. NGINX stops synthesizing `Transfer-Encoding` for H2 streams and
has a guarded H3 path. Traefik marks `responseIncomplete` for host, engine,
commit, and source errors, including a post-commit failed EOS callback in
`finish()` and failed or unconfirmed pre-commit deny/error responses,
suppressing false EOS and normal FINISH. Initial `(0,nil)` ReaderFrom does not
delegate before pre-commit controls; no false-EOS or normal-FINISH behavior is
claimed. The complete independent status matrix is maintained in
`docs/protocol-parity.md` and its German companion.

A pre-commit EOS engine error marks completion incomplete even when a visible
fallback exists. Missing Applied or Late log-only acknowledgements likewise
mark completion incomplete; normal FINISH is not claimed. On Late log-only
acknowledgement errors, the delegated ReaderFrom-EOF path also emits no
synthetic EOS.

## Security impact

The boundary is untrusted protocol, stream, response-body, EOS, and late
intervention state. The documented changes preserve fail-closed behavior where
specified and distinguish source evidence from runtime evidence. No security
finding is fully verified; the accurate wording is source-level fixed / runtime
not verified.

## Changed files

This is the historical original-path list. Test/checker paths removed during
the 2026-11-01 migration are retained here as history, not current Parent-owned
files; their mapped implementation is delivered by Framework PR #148.

- `connectors/lighttpd/README.md`
- `connectors/lighttpd/README.de.md`
- `docs/protocol-parity.md`
- `docs/protocol-parity.de.md`
- `ci/checks/common/check-common-helpers.sh`
- `common/include/msconnector/late_intervention.h`
- `common/src/late_intervention.c`
- `connectors/apache/src/msc_filters.c`
- `tests/test_apache_phase4_response_regression_wiring.py`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `tests/test_nginx_upstream_security_contract.py`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/middleware_test.go`
- `connectors/envoy/Makefile`
- `connectors/envoy/README.md`
- `connectors/envoy/README.de.md`
- `connectors/envoy/capabilities.json`
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in`
- `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `tests/test_envoy_transport_hardening_contract.py`
- `reports/audits/change-records/CR-20260826-http2-http3-protocol-parity.md`
- `reports/audits/change-records/CR-20260826-http2-http3-protocol-parity.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

At the original 2026-08 checkpoint the Framework submodule was uninitialized
and was not modified. MRTS was untouched. The current integration state is
recorded in the 2026-11-01 checkpoint above.

## Commands executed

The commands and PASS results in the 2026-08 sections below are historical.
They have not been rerun or promoted to the merged 2026-10-24 revision. The
2026-10-24 update used source review, Go formatting, JSON/Python syntax,
conflict-marker, Git-index, and diff-integrity inspection only. Functional
tests, builds, runtime traffic, and CI-green acceptance are deferred by the
user request at that historical checkpoint; the 2026-11-01 scope supersedes
that test deferral without authorizing a broad qualification campaign.

The Change Record structural contract passed. The bilingual documentation
checker reports 22 existing missing links into the uninitialized Framework
checkout, with no new task-owned link error. The full documentation-link target
requires that dependency and was not run. The task diff against current master
has no whitespace errors; checking the inherited master delta against the old
PR base also reports two pre-existing blank lines at EOF in master-owned local
inheritance templates, which were preserved unchanged.

- `curl --http3` — exits `2`.
- `rtk proxy env TMPDIR=<registered-run>/tmp GOCACHE=<registered-run>/build/gocache GOMODCACHE=<registered-run>/build/gomodcache GOPATH=<registered-run>/build/gopath GOTOOLCHAIN=local GOFLAGS=-mod=readonly GOPROXY=off go test -run 'Test(EngineErrorAfterCommittedResponseDoesNotInventResponseEOS|IncompleteHostWriteDoesNotInventResponseEOS|LateResponseDecisionDoesNotReplaceCommittedResponse|ReadFromEngineEOSErrorAfterHostCommitDoesNotWriteFailure|ReadFromInitialSourceErrorDoesNotInventResponseEOS)$' .` — passed (focused post-patch Go selection).

The following supplied test results are recorded without inventing command
lines:

- 28 selected Python tests passed (Apache/NGINX/C/C++ group).
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v tests.test_apache_phase4_response_regression_wiring tests.test_nginx_upstream_security_contract tests.test_nginx_protocol_harness_contract tests.test_transport_lifecycle_artifacts tests.test_runtime_observation_contract` — passed (98 tests, 1 expected Framework-identity skip).
- Previous baselines: 20 passed/3 skipped and 39 passed/2 skipped.
- Capability group 93 had one expected environment failure owing to the
  missing uninitialized Framework validator.
- Common C17 passed.
- Common SDK/adapter/security checks passed.
- Apache C17 passed.
- Apache focused static test passed.
- NGINX static test passed.
- Traefik focused Go test passed; the first pre-fix reproduction failed.
- The original direct post-commit engine-error reproduction and the new initial
  `ReadFrom` source-error reproduction failed before repair.
- NGINX native C17 compile was blocked due missing NGINX headers.
- Explicit task-worktree `make protocol-client` — stopped with exit `2` because
  the uninitialized Framework gitlink has no `protocol-client` target.
- Apache static test — passed.
- Apache C17 — passed.
- Common C17 helper — passed.
- Traefik package test — passed.
- Four focused Go regressions intentionally failed before the fix and passed
  after it.
- Three test-first Go regressions intentionally failed before the fix and
  passed after it.
- A new test-first ReaderFrom regression intentionally failed before the guard
  and passed after it.

## Follow-up SonarQube Cloud remediation — 2026-08-27

Exact prior Draft PR #348 head
`9e4cea8dfa9eff6dd4a48051f1500306f02e0f4d` has failed SonarQube Cloud check
run `98318846059`: issue `AaA_yqaofjcmWz1J_WHw`, rule `go:S3776`, marks
`TestReadFromInitialSourceErrorDoesNotInventResponseEOS` at
`connectors/traefik/native_middleware/middleware_test.go:442` with cognitive
complexity `23` where `15` is allowed. The exact current finding is tracked as
FND-SONAR-0068; it is a task-owned maintainability delivery blocker, not a
security finding.

Only the existing table-subtest body was extracted into the test-local
`t.Helper()` function `assertInitialSourceErrorDoesNotInventResponseEOS`.
`before_body`, `after_body`, source-error propagation, response-body checks,
the closed-transaction response-EOS guard, and the response-body-call EOS
guard remain unchanged. No production source, protocol assertion, scanner
configuration, Quality Gate, rule, suppression, `NOSONAR`, exclusion, or
false-positive status changed.

- `rtk proxy env GOCACHE=<task-owned-cache> GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off go test -mod=readonly . -run '^TestReadFromInitialSourceErrorDoesNotInventResponseEOS$' -count=1` — passed.
- `rtk proxy env GOCACHE=<task-owned-cache> GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off go test -mod=readonly . -count=1` — passed.
- `rtk proxy env GOCACHE=<task-owned-cache> GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off go vet -mod=readonly .` — passed.
- `rtk proxy gofmt -d middleware_test.go` — passed with no diff.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` and `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links` — blocked (exit `2`) only by missing Framework-submodule link targets in the uninitialized Parent gitlink; neither reported a changed Change Record defect.
- Targeted `ci/checks/documentation/check-bilingual-docs.py` Change Record pair/structure validation — passed.
- `rtk proxy git diff --check` — passed.

The Go commands ran from `connectors/traefik/native_middleware` with a
registered external cache and disabled module/network acquisition; documentation
and diff checks ran from the Parent task worktree. Exact-successor SonarQube
Cloud evidence remains pending until the focused follow-up commit is pushed; no
successor Quality Gate is claimed here.

## Successor SonarQube Cloud duplication remediation — 2026-08-27

The first normal successor, `1b8da7ff02489efc1b2bb2b37be46daa20d26cb4`, is
pushed and is the matching local, remote, and Draft PR #348 head. Its exact
SonarQube Cloud check run `98507227257` has no GitHub annotations and the
unresolved PR issue search returns zero results, so the original `go:S3776`
target no longer reproduces. The Quality Gate nevertheless fails independently
on `new_duplicated_lines_density`: `7.789678675754625%` / 80 new duplicated
lines across seven blocks, where `<= 3%` is required.

This distinct, task-owned test duplication is tracked as FND-SONAR-0069. Its
evidence identifies only `connectors/traefik/native_middleware/middleware_test.go`:
the inline pre-commit commit/evaluation/acknowledgement-error fixtures and the
direct-write/ReaderFrom late-acknowledgement fixtures share repeated setup and
incomplete-response checks. The new local test-only refactor introduces
`newDeniedResponseRecording`, `newLateAcknowledgementErrorTransaction`,
`serveResponseScenario`, and `assertResponseIncomplete`; every named scenario,
its unique error source, direct-write/ReaderFrom path, no-invented-response-EOS
guard, and `log_only` assertion remains. No production source, scanner
configuration, Quality Gate, rule, suppression, `NOSONAR`, exclusion,
false-positive status, Framework Gitlink, MRTS source, or merge changed.

- The five directly affected named Go tests passed before and after the helper
  extraction with the registered external cache and disabled module/network
  acquisition.
- Package `go test -mod=readonly .`, `go vet -mod=readonly .`, `gofmt -d`, and
  `git diff --check` passed after the extraction.

The normal same-branch commit `35c6b339da9144578b800a3877fded414f24fe31` was
pushed without rewriting history; its local, remote, and PR heads match. Exact
SonarQube Cloud check `98514348339` passed with zero annotations, zero
unresolved issues, zero new duplicated lines/blocks, and `0.0%` new-code
duplication. FND-SONAR-0068 and FND-SONAR-0069 are `fixed` on this Draft PR
head, pending post-merge current-master verification and original
reproduction. This does not claim a merge or complete H2/H3/runtime evidence.

## Envoy downstream H1/H2 profile and metadata hardening — 2026-08-27

The ext_proc materializer now selects only `http1` (default) or `h2` through
`EXT_PROC_DOWNSTREAM_PROTOCOL`; an unknown profile exits with status `2`.
The `http1` rendering advertises only ALPN `http/1.1` with the HTTP/1 HCM codec.
The `h2` rendering advertises only ALPN `h2` with the HTTP/2 HCM codec and
`http2_protocol_options`. `EXT_PROC_DOWNSTREAM_PROTOCOL` exposes the same
selection through the connector Make target. This is a static/profile contract,
not a client or host assertion.

The direct `ext_proc` request-header adapter boundary now preserves the
supplied `HTTP/2` metadata value while rejecting duplicate, uppercase, and
unsupported request pseudo-headers; invalid header names; CR/LF/NUL header
values; connection-specific headers for modern protocols; and invalid `TE`
values when the supplied downstream protocol is HTTP/2 or HTTP/3. The
test-first focused Go selection failed before the guard and passed after it.
The focused materializer contract and `sh -n` passed.

The known non-loopback plaintext ext_proc admission risk remains tracked as
FND-PARENT-0135; this increment does not add mTLS, listener admission control,
or raw lifecycle-artifact protocol-correlation enforcement. No new finding is
closed or promoted. Envoy config-load, a managed H2 client, negotiated ALPN,
multiplexing, reset behavior, and H3 remain unexercised.

## Envoy helper-extraction Sonar remediation — 2026-08-27

At the current pre-remediation Draft PR #348 head
`1ecf2353e14832424cd492efa9919cb3c4418727`, SonarQube Cloud reports the
task-owned `go:S3776` issue `AaBDdUxoMD5aIOx72SVh`: the Envoy request-metadata
function has cognitive complexity `33` where `15` is allowed. FND-SONAR-0070
tracks it as a maintainability delivery blocker, not as a newly asserted
security severity.

The narrow follow-up extracts request-metadata state, pseudo-header,
ordinary-header, finalization, and attribute helpers while preserving the
existing validation path and error behavior. Focused metadata tests, the full
Envoy ext_proc Go suite, `go vet`, format/diff checks, the transport contract,
documentation checks, shell/JSON checks, and configuration-reference checks
passed. A fresh sealed source-level security-diff scan covers the one changed
production file with complete coverage and zero reportable new findings.

Normal successor `07a9d19cc3f1ee832c170d5cfc55cdd607349a66` matches the
local, remote, and open Draft PR #348 head. Its `SonarCloud Code Analysis`
check `98552049461` passed, the PR Quality Gate is `OK`, and the unresolved
issue query returns zero results, including no `AaBDdUxoMD5aIOx72SVh` target.
FND-SONAR-0070 is fixed on that Draft PR head pending post-merge current-master
verification and original reproduction. This source review does not claim
Envoy configuration loading, negotiated ALPN, H2 multiplexing, or H3 runtime
evidence, and it does not close FND-PARENT-0135.

## Runtime evidence

curl has HTTP/2 but lacks HTTP/3. `curl --http3` exits `2`. H3 runtime is
`runtime_skipped_missing_client` and not verified. No H2/H3 traffic claim is
made. Actual Traefik H2/H3 runtime was not executed.

## Checks not run and rationale

No other commands or results were supplied for this documentation record.
Unknown source, build, contract, runtime, P1, P2, P3, P4, and late-intervention
dimensions remain `not_run` or `blocked` as shown in the matrix. The accidental
initial shared build output is recorded only as a local storage limitation; it
does not establish protocol or runtime evidence.

## Known limitations

The Framework submodule is uninitialized. H3 lacks a client in this environment.
Connector runtime evidence is not established for the matrix, including H2/H3
traffic. Native NGINX C17 compilation remains blocked by missing NGINX headers.

## Remaining risks

The neutral Common model may not yet be used by every adapter. Source-level
fixes have not been promoted to runtime verification. No security finding is
fully verified.

## Final diff and review status

**NGINX const-integrity follow-up on 2026-10-30:** native NGINX PR analysis
at `1c0116b09a97f28d13a64565da555ca6163e6b48` still reports
`AaGEBVJegbtoLIpIcyJK` / `c:S995` despite its passing gate. The authority
selector now accepts `const ngx_http_request_t *`; the shared iterator and
its three callers use read-only list-part cursors. Only qualifiers change in
`ngx_http_modsecurity_common.h`, `ngx_http_modsecurity_access.c` and
`ngx_http_modsecurity_header_filter.c` under `connectors/nginx/src/`.
The existing `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
requires the corresponding `const` declarations. Host precedence, raw authority
including port, traversal, ownership and exported ABI remain unchanged. No
tests, fixtures or selectors are authored; active/archive counts remain
100/6228 with no digest or generated-output changes.

`rtk make check-nginx-common-adoption check-active-inventory` passes. Existing
`check-nginx-c17` passes with the available V3-disabled NGINX 1.31.6 headers.
An isolated source copy configures successfully with HTTP/2, HTTP/3, TLS and
system OpenSSL 3.5.5; its native `rtk bypass make -j 8 modules` passes with
C17, `-Wall -Wextra -Werror`, compiling the guarded H3 path and linking the
dynamic module. The generic C17 target against that V3 configuration first
fails because its include helper omits `src/event/quic`; it is not claimed as
passed or weakened. Configure/build logs are retained in external run
`pr348-nginx-const-20261030.LwnYnQ`. This is compile/link evidence only,
not host execution, actual H3 traffic or pinned TLS runtime-profile
qualification. Independent source review found no blocker. Fresh successor
CI and native Sonar issue closure remain required; prior-head checks do not
verify the successor. Framework/MRTS pins, rules and gates remain unchanged.

**Further integrity correction on 2026-10-30:** a bounded HAProxy/lighttpd
source trace found no promoted header-derived protocol or wire-stream identity,
but the lighttpd README pair falsely described the committed-Strict callback as
returning `PLUGIN_BODY_HOOK_ABORT`. The current module instead logs
`NOT EXECUTED` and returns `PLUGIN_BODY_HOOK_CONTINUE`; Common profile admission
rejects Strict because `lighttpd-patched` has no Strict post-commit action,
and module activation propagates that rejection. The paired README correction
states those facts and separates recognized config values from profile
admission. No product, capability, test, fixture, selector or pin changes.
This repairs a source/documentation contradiction, not missing Strict/H2/H3
behavior or runtime proof. RTK-wrapped `make check-bilingual-docs` with Parent
Python and `make check-doc-links` with Framework Python passed (exit 0), as did
`ci/tools/new-change-record.py check` and `git diff --check`. Independent
source-versus-text review found no blocker. No new runtime or native execution
was performed for this documentation-only correction; successor hosted checks
must be observed afresh after publication.

**Subsequent update on 2026-10-30:** Parent master advanced again to
`ee1345f17c5390fd2341751e88fc510c7e7b580c` (#433). It is integrated into
the task branch without rewriting published head `096170f7` (59 successful
checks, five skips). The sole generated archive conflict is regenerated;
active selection remains 100 and connector product source is unchanged.
Master's Framework pin `d3b47aec9410f7adc3bb40df1ea413c00c438e89` matches
its lock and contains the package/result API, superseding the missing-API
limitation below. MRTS pin is unchanged. Paired current guides and a dated
note in the historical package record preserve this distinction. Independent
Framework Draft #143 at `78b103f8` repairs protocol terminal-fact admission;
it is not part of the Parent pin. Existing focused integrity/docs checks and
fresh hosted validation are required for the new Parent head. No tests,
selectors, host qualification, MRTS changes or PR-to-master merge are authored
by this increment; existing Framework tests arrive with the upstream pin.

**Update on 2026-10-30:** the user resumes with integration integrity as the
scope and no new tests while the test system is being rebuilt. Saved head
`1dca1c8eabd17d71a3327ccf3f828c3c5cb8fa01` completed 59 hosted checks
successfully, including Sonar, with five skipped. Current master
`ec18f9e92286379a2410e917f76e6a5502675804` is integrated through a normal
merge. The sole conflict, the specialist archive, is resolved through its
generator. Master's unchanged selection and updated Apache harness digest are
combined with all nine PR source bindings; all digests match. The regenerated
archive has 6228 on-demand definitions; the active selection remains 100.
Master's four existing package-handoff definitions are inherited unchanged;
no test or selector is authored in this increment. Product-source protocol
changes and master package/result integrity guards are preserved. Neither
Framework nor MRTS Gitlink changes; the documented later-Framework-API
dependency remains unqualified. Validation uses existing consistency checks
and fresh hosted CI/Sonar; new-head server results are pending at preparation
time. Full protocol runtime qualification remains incomplete.

**Update on 2026-10-28:** the current CI-repair request supersedes the earlier
test deferral. The branch incorporates master
`c5993ed9a7b59fc0bd58f105595ec79f596c88d6` while preserving the published
`ab3d4d27` head. Seven merge conflicts are reconciled in Apache, NGINX,
Traefik and both archive indexes. Apache combines negotiated P3 protocol with
the native success wrapper; NGINX includes the synthetic authority Host in the
typed client-header limit; Traefik retains checked close, terminal errors,
abort behavior and suppression of false EOS/FINISH.

All five failed structure/lint jobs shared the stale Apache checker literal.
The repaired Apache and NGINX guards pass directly and retain negative bypass
mutations. Sonar issue `AaF3fXFNfuQxuJn35iQJ` / `c:S859` is addressed by
removing the const-dropping Host-name cast. The focused selection passes:
21 Python scenarios and 44 Traefik cases with the race detector. A stale NGINX
source assertion failed first and passed after its expectation was corrected.
Python used the existing local 3.14.4 interpreter; current-head hosted checks
remain required. Eight active-inventory source digests are refreshed without
changing its 100 selected cases, and the specialist archive is regenerated
through its source generator. Inventory admission, archive consistency and
diff checks pass. Independent bounded source review found no new validated
security issue. Hosted CI and Sonar results for the successor are pending;
this is not full H1/H2/H3 runtime qualification or permission to merge to master.

The first successor `2a6089c3` passes required Sonar C++17 and all five repaired
structure/lint jobs. Its cast issue is absent; two new `python:S1192` issues
(`AaGD5oa6tqzpX64G6ssQ`, `AaGD5oa6tqzpX64G6ssR`) are addressed with shared
regex constants, and the eight affected Apache scenarios pass again. The
C++20 advisory's `AaGD49pqgIkAXNgRzIvR` / `c:S2259` issue flow contradicts
its current source view: an explicit null return already precedes the alleged
dereference. Independent review establishes no reachable null edge. A minimal
clarification combines the redundant lighttpd error guards into one NULL-first
short-circuit check, preserving behavior. Its two existing native null/normal
cases pass, giving 67 distinct selected scenarios overall. The ninth source
binding is refreshed without selection changes. Bilingual, repository-path
and documentation-link checks pass after dependency setup. Fresh successor
hosted validation is still required; no server issue state or gate is weakened.

**2026-10-24 update:** PR #348 is refreshed from old head
`81ccd883678c83dda8b4fee61a9acc8a4c4c633c` with current `origin/master`
`42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3` through a normal merge. All nine
conflicts are reconciled: Envoy processor/test, Traefik middleware/UDS/tests,
the Apache regression-definition file, and both archive indexes. Current master
request-body draining, error/cleanup paths, required Envoy Host, documentation,
and Framework gitlink are retained together with the protocol changes.

[Upstream issue #401](https://github.com/owasp-modsecurity/ModSecurity-nginx/issues/401)
is integrated as an adapter-owned change in
`connectors/nginx/src/ngx_http_modsecurity_common.h`,
`connectors/nginx/src/ngx_http_modsecurity_access.c`, and
`connectors/nginx/src/ngx_http_modsecurity_mapper.c`. A shared H3-only selector
exposes raw received authority, preserving port/bracketed IPv6, only when no
explicit Host exists. It supplies the common mapper, hostname, native P1
headers, and bounded count/byte accounting without mutating NGINX's header
list or inventing a configured Host. H3 version metadata is explicitly `3.0`.
Independent source review found no new validated security issue. Tests/builds
and runtime remain `not_run` at the user's request; this is not a verified-PR
or runtime-acceptance claim. Paired protocol, connector, origin-map, and
machine-readable source-map documentation records the same scope. Delivery
uses the existing Draft PR and an ordinary push; no PR-to-master merge is
authorized.

The following paragraphs retain the historical delivery checkpoints.

This is an independent Draft-PR workstream. The paired documentation and
Change Record report only observed results. Commit
`5e7b34d1887984f74d061872d7652a3f71d87856` is pushed as
`feature/http2-http3-protocol-parity` and represented by Draft PR
[#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348).
At initial delivery verification, the local, remote, and PR-head SHAs matched. CI
checks were queued or in progress and are not claimed as passed. No merge has
occurred.

The first local follow-up is pushed as
`1b8da7ff02489efc1b2bb2b37be46daa20d26cb4`; its exact successor resolved the
original `go:S3776` issue but failed the independent FND-SONAR-0069 duplication
gate. The second normal follow-up
`35c6b339da9144578b800a3877fded414f24fe31` is also pushed and its exact
SonarQube Cloud check `98514348339` passed cleanly. Framework Draft PR #112 is
separate; its green checks do not alter the Parent Framework gitlink, Parent
delivery state, or MRTS scope.
