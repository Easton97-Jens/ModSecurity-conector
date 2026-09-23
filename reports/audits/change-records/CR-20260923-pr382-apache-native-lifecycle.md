# Change Record: Apache native failure and lifecycle boundaries

**Language:** English | [Deutsch](CR-20260923-pr382-apache-native-lifecycle.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260923-pr382-apache-native-lifecycle` |
| Base revision | `ad22918e92849a10483439d72ac9a50154ec00be` |
| Scope | Parent repository, Draft PR #382, I09/I10 implementation |

## Motivation and problem statement

The current request is to bring I09 and I10 to a state where only live-host
proof remains. Source inspection found actual remaining Apache gaps: an
unchecked nonzero intervention result, native buffers abandoned on zero,
unchecked retained copies, late Location mutation, audit re-entry and a missing
native-engine initialization check. These are code defects, not missing host
reports. This slice addresses them; it does not silently close other routes.

## Acceptance criteria

Preserve operation-specific return contracts, first error causes, request-owned
copies, valid rule statuses and body-limit handling. Release native buffers on
every post-call exit, never mutate committed response headers and never collect
an actionable intervention from logging. Reject failed initialization; bind
cleanup to the owning configuration generation. Keep all existing scanner rules,
zero new Sonar findings and exact zero new duplication. Update the checklist
only from verified implementation and test evidence.

## Implementation decision and rationale

A private failure mapper clears stale rule metadata and passes the first
canonical cause to the existing once-event boundary. A checked native collector
separates exact 0/1 results from failures; retained values and redirect storage
must exist before any response header changes. Native and host failures use
separate callers of the same mapper. The rule mapper rejects prior technical
errors. Audit records an attempt before native callbacks and preserves failure.
Initialization publishes only a valid engine; APR initialization bookkeeping
is checked and configuration cleanup no longer targets a later global instance.

## Changed files

Apache module and private state header, source-contract regressions, compiled
native/APR lifecycle tests and the existing Apache CI job. No dependency or
Framework/MRTS changes. Physical event-sink propagation remains the separate I11
implementation boundary.

## Commands executed

No local project commands: the mandatory RTK wrapper is unavailable. The
existing GitHub workflow is extended after its already-installed Apache/APR
prerequisites to execute:

```sh
python3 -m unittest -v tests.test_apache_intervention_cleanup
python3 -m unittest -v tests.test_apache_native_lifecycle
make check-apache-autotools-bootstrap
```

New execution and exact-head Sonar results are pending at preparation. Source
regressions retain ownership/order assertions while following the new helper;
the old assertion requiring the leaking zero early return is corrected.

## Security impact

Technical failures cannot reuse a prior rule identifier or install a redirect.
Native buffers have one release owner. Native failure and host allocation failure
retain different causes. No added log payloads, capability promotion, scanner
exclusions, accepted findings, credential changes or broader CI permissions.

## Runtime evidence

Twenty compiled tests use actual selected product functions, checked-in Apache
state declarations, real APR pools/tables and the real Common state machine.
Native results, allocation failures, diagnostics and the final event emitter
are controlled seams. A compiled zero-cleanup negative control reproduces the
original leak. This is not live httpd, physical log persistence or client I/O.

## Known limitations

I09/I10 overall remain in progress during this slice. Filter/API exits outside
this module, other integration routes and the existing native Go verification
must be reconciled before claiming that only live-host proof remains. Existing
I11 physical output gaps and I12 route evidence are not relabelled complete.

## Remaining risks

Fresh full module compilation, source/adoption checks, test fixture compilation
and exact-head Sonar evidence are mandatory. Audit cannot retract a sent
response. An independent secret-scanning failure remains a release blocker.

## Checks not run and rationale

No local build/test/gofmt or diff commands; unavailable mandatory RTK. No live
host or full transport matrix. Remote results must be read back for the exact
published revision and must not be inferred from prior successful runs.

## Final diff and review status

Draft PR branch only; no merge, master update, force push or deployment.
