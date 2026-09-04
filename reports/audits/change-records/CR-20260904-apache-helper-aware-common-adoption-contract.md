# Change Record: Apache helper-aware Common-adoption contract repair

**Language:** English | [Deutsch](CR-20260904-apache-helper-aware-common-adoption-contract.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260904-apache-helper-aware-common-adoption-contract |
| Date (UTC) | 2026-09-04 |
| Base revision | 2b3d7f7f0bec006b236b5998d011069c9125033f |
| Delivery status | Authorized corrective delivery on a focused branch based on the stated revision. Each commit, normal push, and Draft PR action requires a fresh remote preflight. No merge is authorized by this record. |

## Motivation and problem statement

After PR #345 was squash-merged, five resulting-master workflows stopped at
the same Apache/Common-adoption static check. The product source had moved the
P2 bucket path out of `input_filter()` into
`apache_input_filter_process_bucket()` and changed the append contract to the
bounded `plan.append_size` form. The old checker continued to require the
former monolithic token layout, so it rejected the current bounded helper
architecture.

The repair is checker and test work only. It does not claim to repair the
separate native Apache reverse-proxy P2 runtime issue in `FND-PARENT-0986`.
That finding remains in progress and release-blocking pending its own native
controls and delivered-head evidence.

## Acceptance criteria

- The checker follows the real P2 helper call graph: dispatcher, non-EOS
  processor, EOS handler, finalizer, and terminal error bridge.
- Every non-EOS bucket contract requires direct-body read, limit plan, Common
  record, bounded append using `plan.append_size`, accounting, and only then
  the remove/forward sink.
- EOS rejects a duplicate, finalizes once, routes an intervention through the
  input terminal bridge, and only then releases EOS and removes the filter.
- Comment-only and foreign-function tokens cannot satisfy helper-specific
  assertions.
- A constant-false dead-code decoy cannot satisfy the P2 source-to-sink
  contract while the active path forwards a bucket.
- No Apache product source, workflow, ruleset, branch protection, required
  check, Quality Gate, exclusion, suppression, Framework, MRTS, Gitlink, or
  PR #346 change is included.

## Implementation decision and rationale

`apache_common_adoption_base.py` now extracts one masked, balanced C function
definition and offers a direct-body projection that masks nested compound
blocks. The Apache review checker uses those scoped views rather than a broad
slice of `msc_filters.c`.

The non-EOS guard requires the live pipeline in direct function-body code,
requires one direct canonical success tail, and rejects narrow ambiguous
control constructs in critical P2 helpers (preprocessor branches, labels,
`goto`, and obvious constant-false controls). The EOS helper likewise requires
one direct canonical success tail. The dispatcher must keep the actual EOS
branch immediately followed by the non-EOS processor delegation. Existing
exact-success, terminal-bridge, bounded-append, and P3 fail-closed checks are
retained.

This is deliberately a strict source contract, not a claim of full C AST or
arbitrary runtime reachability proof. A future legitimate helper-shape change
must update the checker and its negative controls deliberately rather than
silently broadening a token search.

## Source-to-contract trace

| Security invariant | Current product function | Delegating call site | Stale checker assumption | New checker proof | Regression control |
| --- | --- | --- | --- | --- | --- |
| Non-EOS body bytes are boundedly processed before forwarding. | `apache_input_filter_process_bucket` | `input_filter` after the EOS branch | The full body pipeline is lexically inside `input_filter`. | Scoped direct-body order: read → plan → Common record → `plan.append_size` append → accounting → one remove/forward tail. | Early forwarding, unbounded append, and constant-false pipeline decoys are rejected. |
| P2 is finalized once only at canonical EOS and an intervention precedes release. | `apache_input_filter_handle_eos` and `msc_finalize_request_body` | The `APR_BUCKET_IS_EOS` branch in `input_filter` | Finalization and EOS error tokens occur in the former monolithic section. | One scoped finalizer call, duplicate-EOS bridge, direct EOS release tail, and no obvious dead-code control. | Removed finalization and constant-false EOS-finalization decoys are rejected. |
| Input errors fail closed through Apache Core rather than an output-side error bucket. | `apache_input_filter_terminal_error` | Context/configuration, non-EOS, and EOS helper error returns | Terminal calls are counted only in the old `input_filter` slice. | Named helper scopes require all three callers and the terminal helper's status neutralization, `ap_die`, and `AP_FILTER_ERROR` return. | Missing EOS delegation/bridge plus comment-only and foreign-function token decoys are rejected. |

## Security impact

The source-to-sink boundary is request-body data entering
`apache_input_filter_process_bucket()` and leaving through
`APR_BUCKET_REMOVE` plus `APR_BRIGADE_INSERT_TAIL`. The repair preserves the
requirement that the bounded Common path succeeds before that forwarding sink.

An adversarial review reproduced a checker-only bypass before this repair:
required planning, record, append, accounting, and error tokens inside
`if (0)` caused the old lexical guard to pass while the active path read and
forwarded a bucket without those controls. The current product source did not
contain that path. The new direct-body and terminal-tail checks reject the
reproduction, and the regression suite contains both non-EOS and EOS
constant-false mutations.

No event serialization, body payload, header, remote-rule, endpoint,
filesystem, archive, or runtime enforcement behavior is changed because no
product runtime source is changed.

## Changed files

- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `tests/test_apache_common_adoption.py`
- `Makefile`
- `reports/audits/change-records/CR-20260904-apache-helper-aware-common-adoption-contract.md`
- `reports/audits/change-records/CR-20260904-apache-helper-aware-common-adoption-contract.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Check | Actual result |
| --- | --- |
| Pre-patch direct Apache checker and `make check-apache-common-adoption` | Reproduced the two stated stale Apache assertions against base `2b3d7f7f0bec006b236b5998d011069c9125033f`. |
| Python compilation of changed checker/test files | Passed. |
| Direct Apache checker | Passed, including the helper-aware P2, EOS, terminal-bridge, bounded append, and P3 guards. |
| `tests.test_apache_common_adoption` | Passed: 10 tests, including the positive architecture and nine negative mutations. |
| `make check-apache-common-adoption` | Passed. |
| `python3 -m unittest discover -s tests -p 'test_apache*.py' -v` | Passed: 69 tests. |
| Apache C17 lint | Passed outside the sandbox because the project check uses a fixed temporary probe root. |
| `make check-no-crs-source-normalization` | Passed: 145 tests after initializing the already-pinned Framework checkout in the isolated worktree. |
| `make generate-test-matrix` and `make check-test-matrix` | Completed; generated report drift was task-external and the nine generated files were restored to `HEAD`. |
| Apache/NGINX harness shell syntax and `make -n` smoke/runtime targets | Passed. |
| `make lint` and `make quick-check` | Reached and passed all preceding Apache checks, then stopped at two unchanged NGINX common-adoption assertions tracked by existing `FND-PARENT-1010`. Candidate-to-base diff for NGINX source and checker is empty; no NGINX change is made here. |
| Final `git diff --check` and documentation checks | Passed after the paired records were added. |

## Runtime evidence

This is a source-contract repair. No native Apache server, proxy, request, or
response flow was started for this change. No request or response body was
retained. The current product P2 path was traced read → plan → record → bounded
append → accounting → forwarding, but that static evidence is not substituted
for native P2 runtime validation.

## Checks not run and rationale

No native Apache P2 runtime replay, complete P1–P4 acceptance, full native
17×10 host matrix, sanitizer matrix, or resulting-master workflow rerun is
claimed. They are not necessary to prove a checker-only repair and remain
separate evidence obligations. Exact pushed-head GitHub Actions, SonarQube
Cloud, and review evidence are also pending until the authorized Draft PR
exists.

## Known limitations

The checker rejects the reproduced dead-code bypass and makes the required P2
shape explicit, but it is not a full C parser or proof of arbitrary macro and
runtime reachability. A future source refactor can legitimately require a
deliberate checker/test update.

## Remaining risks

The task does not resolve `FND-PARENT-0986`'s native HTTP-500/HTTP-403
translation question. It also does not repair the separate master-level NGINX
checker failure tracked in `FND-PARENT-1010`; that blocker prevents the local
aggregate `make lint` and `make quick-check` from reaching later controls.

## Final diff and review status

The delivery diff contains no Apache runtime source, workflow, governance, or
generated-report change. This pre-delivery static record does not claim a
commit, push, Draft PR, exact-head hosted check, SonarQube Cloud result,
Ready-for-Review status, or merge; those delivery facts require independent
exact-head evidence.

An independent final read-only security diff review reran the two
constant-false decoys, the ten-test mutation suite, the direct Apache checker,
and `git diff --check`. It found no additional validated security finding and
confirmed that the product runtime source is unchanged. Its residual note is
the same declared checker boundary: arbitrary nonconstant C control flow and
macro semantics are not proven by this static contract.
