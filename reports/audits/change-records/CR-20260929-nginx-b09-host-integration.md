# B09 real NGINX error-page integration

**Language:** English | [Deutsch](CR-20260929-nginx-b09-host-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260929-nginx-b09-host-integration` |
| Date (UTC) | 2026-09-29 |
| Base revision | `f490ba693d2a014ead7b6b477cc7933a0f3e4bc6` |
| Delivery target | Existing Parent Draft PR #391; no merge |

## Motivation and problem statement

The merge review identified missing real error-page-routing evidence for B09.
The existing source-isolated classifier tests cannot show actual NGINX phase
scheduling or whether the protected target's content handler is reached.

## Acceptance criteria

Use the already provisioned exact-head NGINX/module/libmodsecurity artifacts
and the existing distinct non-root worker. An origin returning 418 routes to
an internal protected target. With a harmless P2 deny marker the client must
receive 403, the native log must identify the P2 rule, and the protected backend
must not be called. Without the marker the target must return its control body
and be called exactly once. Exercise both disabled and enabled/allowing origins,
repeat denials, require subsequent allowed requests and graceful process cleanup.

## Implementation decision and rationale

Add a bounded loopback HTTP/1 fixture to the existing hosted Functional-A
entrypoint. The root launcher, artifact provisioning, worker account, private
root layout, earlier controls and evidence writer remain unchanged. The shell
adds one fixed Python invocation after its existing evidence projection.
The new fixture verifies its head and worker UID/GID, binds artifact hashes,
uses private test-owned rules and observes the backend, not only client status.
It does not claim arbitrary recursive-error-page policy or complete profile coverage.

## Changed files

- `connectors/nginx/harness/run_error_page_intervention.py`
- `connectors/nginx/harness/run_exact_head_use_error_log.sh`
- This English/German Change Record pair.

## Commands executed

The complete original shell was reconstructed and matched to Git blob
`b90c8d90364d4a6330ded43cbc8a2fadde9eb644` before the single-line addition.
The Python fixture was parsed as an AST; local project execution was not
performed because required RTK and provisioned native artifacts are absent.
Actual integration and CI results are pending for the new published head.

## Security impact

No connector production code, gate, token permission, root broker, worker
identity policy, dependency pin or gitlink changes. Loopback traffic and files
belong only to the fresh test run. Root master and non-root worker remain
separate; child process identities and cleanup are observed explicitly.

## Runtime evidence

On success the job prints NGINX_B09_RESULT with the Parent SHA, artifact/rule
hashes, individual status/backend observations, worker separation and cleanup.
Private raw logs stay under the Functional-A run root. Existing Functional-A
results do not implicitly certify B09; the new explicit receipt is required.
This is a bounded integration result, not independent protected attestation.

## Known limitations

The test covers HTTP/1, one internal error-page hop and a P2 header predicate.
It does not prove every error-page recursion policy, response-phase intervention,
body transfer mode or deployment. No finding is automatically closed.

## Remaining risks

A failure must be diagnosed at the actual host boundary, not hidden by relaxing
assertions. Combined changes with other NGINX PRs still require fresh checks.
PR #392 now owns only B13/C07 and no longer supplies a competing classifier.

## Checks not run and rationale

Local native builds and runtime tests were not run in the editor because its
mandatory command wrapper and provisioned environment are unavailable. The
new hosted invocation must run and its result be inspected before acceptance.

## Final diff and review status

Only the fixture, one fixed invocation and paired record are added. Existing
checks and their assertions remain intact. Draft status, open findings and
separate repository boundaries are preserved; no merge or force push occurs.
