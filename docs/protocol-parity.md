# HTTP/2 and HTTP/3 protocol parity workstream

**Language:** English | [Deutsch](protocol-parity.de.md)

This is an in-progress independent Parent workstream. It records the current
evidence for HTTP/2 and HTTP/3 lifecycle parity across the six selected
connectors. It is not a completion claim. HTTP/1.1 remains the regression
baseline.

## Update on 2026-10-28: current master and CI remediation

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

The Framework submodule is uninitialized and was not modified. MRTS was
untouched. curl has HTTP/2 but lacks HTTP/3. `curl --http3` exits `2`.
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

## Regression and capability evidence

- 28 selected Python tests passed (Apache/NGINX/C/C++ group).
- The current combined Python command passed 98 tests with 1 expected
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

## Delivery state

Commit `5e7b34d1887984f74d061872d7652a3f71d87856` is pushed as
`feature/http2-http3-protocol-parity` and represented by Draft PR
[#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348).
At initial delivery verification, local, remote, and PR-head SHAs matched. CI checks
were queued or in progress and are not claimed as passed. No merge has
occurred. The Framework submodule and MRTS remain unchanged.
