# HTTP/2 and HTTP/3 protocol parity workstream

**Language:** English | [Deutsch](protocol-parity.de.md)

This is an in-progress independent Parent workstream. It records the current
evidence for HTTP/2 and HTTP/3 lifecycle parity across the six selected
connectors. It is not a completion claim. HTTP/1.1 remains the regression
baseline.

## Update on 2026-11-01: migrated tests and Framework integration

Test ownership has moved to the Framework. Parent PR #348 incorporates Parent
master `a6001a09`, initially pinned to Framework `d503ddbe`. Fifteen obsolete
Parent paths are removed rather than restored; the 13 mapped checker/test
deltas preserve 24 definitions (19 Go, five Python) in the Framework and remain
recoverable from Parent history `db431efa`.

[Framework PR #148](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/148)
integrates these ports and the terminal-outcome/NGINX QUIC fixes from #143/#144.
Its regular squash merge completed at `2026-11-01T19:09:19Z`; the remotely
verified Framework master at that checkpoint was
`91f5370c7eddcebdc7e49d2099c58054ec2d5d5d`.
The final PR head passed 15 hosted checks with three intended skips. Direct
Sonar readback for that exact head recorded an OK gate with all five conditions
and zero open PR issues. Separately, all seven workflows on master `91f5370c`
succeeded; its direct Sonar analysis at `2026-11-01T19:26:02Z` passed all five
conditions (ratings 1 <= 1, duplication 0 <= 3%, hotspots 100 >= 100%).
PRs #143/#144 were closed unmerged with reference to #148; their branches at
`b7d643f` / `9e49913` are retained.

Final native Parent validation exposed additional migration-integrity defects.
The Product generator `scripts/generate_compiler_guides.py` now maps the NGINX
preparer's public `source_path` instead of referencing its deleted Parent path
and fixes the actual migrated Apache/HAProxy harness links. All 18 generated
guide outputs remain byte-identical to their tracked versions. The selected
Parent projection/revision/candidate suite passed 55 tests. Apache initially
passed 21 tests and failed one stale full-AST golden expectation.

Separate [Framework Draft #150](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/150),
first published head `e1b4f8b24ab95749d685db3e6581e26da302dd57` on base
`91f5370c`, repairs
two existing test modules: compiler expectations/actual forwarded Make targets
and the independently audited full-AST golden. Six migration-context transforms
reconstruct the checker byte-for-byte since #142, preserving every predicate,
message, order and control. The combined 44 methods passed in 27.660 seconds;
eight actual-target controls and 26 isolated parser controls also passed.
Native Apache with #150, NGINX and Common C17 targets passed. Native generation,
binding and admission counts remain unchanged (526 fixed Framework bindings /
235 Product paths); 350 documentation pairs and four canonical checks passed.
No new methods, selectors, versions or weakened gates are introduced by #150.

Framework #147 subsequently advanced master to
`5ef57603a4933f18c988f1f9f32b93f478182440` with host-execution-context
preflights. #150 normally merges that master at its new published head
`af6997be5c5cee38e3feb9274c3269d52784bbe1`, replacing the first candidate.
Native regeneration resolves the inventory conflict while retaining two new
preflight bindings and five default consumers; compared with `5ef57603`, only
the intended compiler-test hash differs in the inventory. Current admission is
528 fixed Framework bindings / 235 Product paths, with 100/80 standard,
2586/1140 optional and 1993 baseline IDs unchanged. Inventory SHA-256 is
`147ebacc795c634bd9d4b21cfbcd408e635dd55de8b757be2671d3b056ac1cb8`.
Fresh 44-method validation passed in 26.138 seconds; native generation/checks,
public admission, 354 bilingual checks, 2159 path checks with zero obsolete
paths, record/link checks and four canonical checks passed. Independent review
confirmed both test fixes unchanged and no EN/DE or inventory blocker. The
earlier #150 compiler-guide entrypoint also passed 22 tests in 0.848 seconds,
with all 18 guides byte-identical. These results do not launch a host campaign.

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

Native generation preserves 100 standard cases / 80 executions and 1993
baseline IDs; the optional catalog is 2586 cases / 1140 executions. The earlier
Framework stage had 526 bindings, superseded by 528 after #147. Those focused
Framework-stage checks passed 12 Python methods,
43 protocol methods, four QUIC helper methods, 348 documentation pairs and
canonical checks. The post-#146 Traefik parity selection passed 16 tests / 18
terminals with the race detector. The earlier full Traefik run (173 pass
terminals, one real-service skip) predates #146 and does not qualify its new
leaves. Before the later `2abad408` master integration, all 31 informational
leaves were compiled but NOT_RUN because selected Parent `b43faa78` lacked
the separate Product fix and #435 was then closed unmerged. That historical
limitation is superseded by the bounded merge-interaction unit evidence above,
not by a full host/TLS/H2/H3 runtime qualification.

The dated snapshots below retain their original evidence and inventory counts;
they do not describe current test ownership, inventory or submodule state.
The protocol matrix remains an unqualified historical snapshot. This migration
and integrity increment does not establish a new TLS/H2/H3 qualification
campaign or new host runtime results. MRTS remains outside the change scope.

## Historical update on 2026-10-30: subsequent master pin refresh

Verified Parent head `096170f7ab0ba19537546ce861f818fbab6e1772`
passed 59 hosted checks, with five intended skips. Master then advanced to
`ee1345f17c5390fd2341751e88fc510c7e7b580c` through submodule update #433.
This follow-up integrates that revision normally and regenerates the sole
archive conflict. The Framework pin and project lock now agree on
`d3b47aec9410f7adc3bb40df1ea413c00c438e89`, which contains the previously
missing package/result APIs. MRTS remains pinned unchanged. API availability
does not establish new host or protocol runtime qualification.

No new tests or selectors are authored. Active case selection remains 100;
the inventory only inherits requirement-string formatting and the updated
lock digest. Existing upstream Framework tests are inherited with its pin,
not newly authored here. Connector product code and issue #401 integration
remain unchanged. Separate Framework Draft
[PR #143](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/143)
tightens protocol-artifact terminal-outcome integrity; its commit `78b103f8`
is not included in the Parent pin. Current-head CI/Sonar is verified separately
after publication. The complete H1/H2/H3 workstream remains unfinished.

## Historical update on 2026-10-30: integration integrity

The saved candidate `1dca1c8eabd17d71a3327ccf3f828c3c5cb8fa01`
completed all 59 executed hosted checks successfully, including Sonar; five
checks were skipped. This increment integrates current master
`ec18f9e92286379a2410e917f76e6a5502675804` through a normal merge.
Its only conflict is the generated specialist archive, regenerated from both
branches' sources. The current master's selection and Apache harness digest
are retained alongside the PR's nine source-digest updates. All source digests
match; no active selection or selector is changed. The archive contains 6228
on-demand definitions, distinct from the unchanged 100 active cases.

No new tests are authored in this increment. Master's existing private-package
handoff tests are inherited unchanged. Connector product source and issue #401
mapping are preserved, as are master's package/result integrity checks. The
documented dependency on a later Framework package API remains a limitation;
this merge does not change Framework/MRTS source or either Gitlink. New-head
CI/Sonar verification remains pending at preparation time. The earlier checks
do not prove the new merge or complete H1/H2/H3 runtime qualification.

## Historical update on 2026-10-28: current master and CI remediation

This increment incorporates `master` revision
`c5993ed9a7b59fc0bd58f105595ec79f596c88d6` through a normal merge,
preserving the published PR history. Apache's negotiated P3 protocol now uses
master's native-phase success check. NGINX retains the typed mapper errors and
counts its synthetic HTTP/3 Host against the same received-header limit.
Traefik combines incomplete-response/EOS handling with master's checked close,
terminal-error and `http.ErrAbortHandler` behavior.

The five failed structure/lint jobs on `ab3d4d27` shared a stale Apache checker
expectation. The checker now requires both negotiated protocol and the native
success guard; negative mutations cover bypasses. The NGINX checker and its
mutations likewise enforce the combined raw/synthetic header limit. Sonar issue
`AaF3fXFNfuQxuJn35iQJ` (`c:S859`) is addressed with a local mutable Host-name
array instead of a const-dropping cast.

Fresh local validation passed: both adoption checkers, 21 selected Python
scenarios and 44 selected Traefik cases with the race detector. One stale
source assertion failed initially and passed after alignment with the merged
limit guard. The 100-case active inventory is unchanged apart from source
digests; its admission check and regenerated archive consistency check passed.
The Python checks used the existing local Python 3.14.4; hosted CI uses the
repository's interpreter contract. Independent source review found no new
validated security issue. Current-head hosted CI and Sonar validation remain
pending at this revision. The earlier test deferral is superseded for CI repair;
full H1/H2/H3 runtime qualification remains incomplete.

On the first published candidate `2a6089c3`, the required C++17 Sonar job and
all five previously failing structure/lint jobs pass; the const-cast issue is
absent. Two new `python:S1192` checker literals are now shared constants, and
the same eight Apache positive/negative scenarios pass again. The advisory
C++20 analysis reports a lighttpd null dereference even though its own source
view contains the explicit null return; independent review establishes no
reachable null edge. Its redundant error guards are combined into one
NULL-first short-circuit guard without changing behavior. Both existing native
null/normal-completion cases pass. This adds two scenarios (67 total with the
earlier selection) and one source-digest refresh; the 100-case selection stays
unchanged. After Framework setup, bilingual/path/link checks also pass. Hosted
validation of this follow-up remains pending; no Sonar server state, rule or
gate is changed.

## Historical update on 2026-10-24: master synchronization and NGINX issue #401

PR #348 incorporates `master` revision
`42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3` through a normal merge. Envoy
keeps the current required Host/authority validation together with this
workstream's stricter pseudo-header and modern-protocol checks. Traefik keeps
the current bounded request-body drain and connection cleanup together with
the incomplete-response/EOS controls. Both branches' test definitions and
Change Record entries are retained after conflict resolution.

For [ModSecurity-nginx issue #401](https://github.com/owasp-modsecurity/ModSecurity-nginx/issues/401),
the NGINX adapter supplies one inspection-only `Host` from a received HTTP/3
`:authority` when no case-insensitive Host entry exists. The mapper, request
hostname, native P1 header feed, and header count/byte accounting use the same
authority selection. An explicit Host, including an empty one, suppresses this
fallback. The adapter does not change NGINX's header list or derive a Host from
configuration. It preserves the original authority's port and bracketed IPv6
form, matching the raw-authority behavior of NGINX's HTTP/2 Host shim. Native
H3 version metadata is explicitly `3.0`.

This update is source-reviewed but `implemented_not_runtime_verified`.
Functional tests, builds, protocol traffic, and CI-green acceptance are deferred
at the user's request. All results and environment probes below are historical
2026-08 evidence, not fresh validation of the merged revision. The full
workstream and H1/H2/H3 runtime matrix remain incomplete.

## Evidence boundary

The neutral Common model represents `unknown`, H1, H2, and H3 protocol states,
stream identity, commit and EOS state, and stream-reset selection. H2 stream ID
0 and a freely set `STREAM_RESET` are conservatively not emitted as a stream
reset. This model does not prove that every adapter uses it.

In the original 2026-08 environment snapshot, the Framework submodule was
uninitialized and was not modified. MRTS was untouched. That curl had HTTP/2
but lacked HTTP/3; `curl --http3` exited `2`.
Therefore H3 runtime status is `runtime_skipped_missing_client`; H3 runtime is
not verified.

## Connector status matrix

Statuses are independent. `not_run` means that no evidence was supplied for
that dimension; `blocked` identifies an observed prerequisite limitation.
`source-level fixed` and `implemented_not_runtime_verified` describe source
evidence only and are not runtime passes.

| Connector | H1 baseline | H2 code | H2 runtime | H3 code/capability | H3 runtime | P1 | P2 | P3 | P4 | Late intervention | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | contract_verified (source only) | configured_not_exercised | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | contract_verified (source only; protocol from `ap_get_protocol(r->connection)` plus canonical HTTP/1 `r->proto_num`; unknown fails closed) | not_run | not_run | source-level fixed / runtime not verified |
| NGINX | contract_verified (historical source only) | implemented_not_asserted | not_run | implemented_not_runtime_verified (authority-to-Host mapping) | runtime_not_verified (deferred) | implemented_not_runtime_verified | not_run | not_run | not_run | not_run | source-level fixed / runtime not verified |
| HAProxy | not_run | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |
| Envoy | not_run | configured_not_exercised | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | source-level configured / runtime not verified |
| Traefik | contract_verified (source only) | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | contract_verified (source only) | source-level fixed / runtime not verified |
| lighttpd | not_run | unsupported_by_host_model | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |

The Apache P3 change now derives protocol from
`ap_get_protocol(r->connection)` plus canonical HTTP/1 `r->proto_num`, and
fails closed for unknown protocol. NGINX stops synthesizing
`Transfer-Encoding` for H2 streams and has a guarded H3 path. Traefik marks an
initial non-EOF `ReadFrom` source error
(with or without bytes) incomplete, and prevents a post-commit response-body
engine error from causing synthetic EOS. The original direct post-commit
engine-error reproduction and the new initial-ReadFrom source-error
reproduction failed before repair; the focused post-patch Go selection passed.
No H2/H3 traffic claim is made and actual Traefik H2/H3 runtime was not
executed. Its `responseIncomplete` state suppresses false EOS and normal
FINISH for host, engine, commit, and source errors. `finish()` marks a
post-commit failed EOS callback as `responseIncomplete`; failed or unconfirmed
pre-commit deny/error responses are marked incomplete as well. An initial
`(0,nil)` ReaderFrom does not delegate before pre-commit controls. No false-EOS
or normal-FINISH behavior is claimed. A pre-commit EOS engine error marks the
completion incomplete even when a visible fallback exists. Missing Applied or
Late log-only acknowledgements also mark completion incomplete, so normal
FINISH is not claimed. On Late log-only acknowledgement errors, the delegated
ReaderFrom-EOF path also emits no synthetic EOS.

Envoy now has separately materialized `http1` and `h2` downstream profiles:
`http1` selects only ALPN `http/1.1` and the HTTP/1 HCM codec, while `h2`
selects ALPN `h2`, the HTTP/2 HCM codec, and `http2_protocol_options`. The
materializer rejects another value instead of falling back. Its existing Python
runtime helper remains HTTP/1.1-only. Focused Go contract tests for the
`ext_proc` request-header adapter path preserve an Envoy-provided `HTTP/2`
metadata value and reject duplicate, uppercase, or unsupported request
pseudo-headers, CR/LF/NUL header values, connection-specific headers for modern
protocols, and invalid `TE` values when the supplied protocol is HTTP/2 or
HTTP/3.
These are source/configuration and adapter-boundary checks only: no Envoy
binary/config-load or client-negotiated H2 traffic was run.

The matrix preserves the separate `connectors/*/capabilities.json` claims:
Apache H2 is `configured_not_exercised` and its H3 host path is
`not_implemented`; NGINX H2 and H3 are `implemented_not_asserted`; HAProxy
and Traefik are `not_implemented` for the selected native modern-protocol
profiles; Envoy downstream H2 and TLS/ALPN are `configured_not_exercised`;
lighttpd H2 is `unsupported_by_host_model` and H3 is `not_implemented`.

No security finding is fully verified. The accurate classification for the
changes above is source-level fixed / runtime not verified.

## Neutral lifecycle contract

The Common contract keeps protocol and lifecycle decisions separate from
connector-specific host types. It covers:

- `unknown`, H1, H2, and H3 protocol selection;
- stream identity and transaction correlation;
- commit state and terminal EOS handling;
- stream-reset selection for a multiplexed protocol; and
- safe versus strict late-intervention choices.

Adapters must still demonstrate that they map and enforce this model. The
matrix therefore does not promote Common-model coverage into connector runtime
coverage.

## Historical regression and capability evidence

- 28 selected Python tests passed (Apache/NGINX/C/C++ group).
- The combined Python command at that revision passed 98 tests with 1 expected
  Framework-identity skip.
- Previous baselines were 20 passed/3 skipped and 39 passed/2 skipped.
- Capability group 93 had one expected environment failure because the
  Framework validator was missing while the Framework submodule was
  uninitialized.
- Common C17 passed.
- Common C17 helper passed.
- Common SDK/adapter/security checks passed.
- Apache C17 passed.
- Apache static test passed.
- Traefik package test passed.
- Four focused Go regressions intentionally failed before the fix and passed
  after it.
- Three test-first Go regressions intentionally failed before the fix and
  passed after it.
- A new test-first ReaderFrom regression intentionally failed before the guard
  and passed after it.
- H2 runtime traffic was not supplied for the matrix.
- H3 runtime is `runtime_skipped_missing_client` and not verified.

An accidental initial shared build output was observed during the workstream.
This is a local storage limitation only; it is not protocol or runtime
evidence and does not support a broader claim.

## Historical initial delivery state

Commit `5e7b34d1887984f74d061872d7652a3f71d87856` is pushed as
`feature/http2-http3-protocol-parity` and represented by Draft PR
[#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348).
At initial delivery verification, local, remote, and PR-head SHAs matched. CI checks
were queued or in progress and are not claimed as passed. No merge has
occurred at that initial delivery. The Framework submodule and MRTS were
unchanged at that point. See the 2026-11-01 update for the current integration
scope and pending delivery evidence.
