# HTTP/2 and HTTP/3 protocol parity workstream

**Language:** English | [Deutsch](protocol-parity.de.md)

This is an in-progress independent Parent workstream. It records the current
evidence for HTTP/2 and HTTP/3 lifecycle parity across the six selected
connectors. It is not a completion claim. HTTP/1.1 remains the regression
baseline.

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
| NGINX | contract_verified (source only) | implemented_not_asserted | not_run | implemented_not_asserted | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | source-level fixed / runtime not verified |
| HAProxy | not_run | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |
| Envoy | not_run | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |
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

The matrix preserves the separate `connectors/*/capabilities.json` claims:
Apache H2 is `configured_not_exercised` and its H3 host path is
`not_implemented`; NGINX H2 and H3 are `implemented_not_asserted`; HAProxy,
Envoy, and Traefik are `not_implemented` for the selected native modern-
protocol profiles; lighttpd H2 is `unsupported_by_host_model` and H3 is
`not_implemented`.

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

This workstream is not yet committed, pushed, or represented by a created
pull request. No merge has occurred. The Framework submodule and MRTS remain
unchanged.
