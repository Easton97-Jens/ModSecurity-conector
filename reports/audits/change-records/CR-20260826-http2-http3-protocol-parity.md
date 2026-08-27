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

The Framework submodule is uninitialized and was not modified. MRTS was
untouched.

## Commands executed

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
