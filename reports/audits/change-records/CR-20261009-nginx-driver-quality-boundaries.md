# Change Record: CR-20261009-nginx-driver-quality-boundaries

**Language:** English | [Deutsch](CR-20261009-nginx-driver-quality-boundaries.de.md)

Behavior-preserving driver quality corrections; runtime and remote closure remain separate gates.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-driver-quality-boundaries |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

The revision-bound Parent analysis reports repeated literals, nested route
selection and excessive client complexity. Refactoring must retain exact
operation routing, source receipts and bounded HTTP observations.

## Acceptance criteria

Keep the closed42 native routes, Required selection, immutable omission tuple
API, first-response-only strict abort, original declared-length snapshot,
body bounds, no hidden reconnect and upstream marker barrier unchanged.

## Implementation decision and rationale

Use explicit closed route tables, immutable shared fault-key values and named
artifact constants. Extract input validation, request construction, bounded
response reading and marker release in their original order. Preserve actual
socket acquisition and finally cleanup in the client. Keep variable-length
omission/event tuples as collections rather than inventing padding fields.

## Changed files

`ci/runtime/common/response_fixture_omission.py`; lifecycle modules
`nginx_sequence_client.py`, `nginx_sequence_upstream.py`,
`run-selected-nginx-native-operations.py`, `run-nginx-event-boundary-cases.py`,
`run-nginx-raw-h1.py`, `run-nginx-mime-cases.py`, `run-nginx-phase4-cases.py`;
`tests/test_response_fixture_omission.py`, `tests/test_nginx_sequence_client.py`,
`tests/test_nginx_dispatch_routes.py`, `tests/test_nginx_sequence_upstream_barrier.py`;
this English/German record pair. The lifecycle modules are below
`ci/runtime/lifecycle/`.

## Commands executed

All commands used RTK and the existing Parent Python environment with external
temporary storage and an explicit Framework catalog. Original baseline37
tests passed. Focused simple-driver21, closed-dispatch10, client/transport13
and independent route/barrier7 checks passed, each exit0. These subsets overlap
and are not an additive suite total. Record and integrated full gates follow
coordinator integration; no remote finding closure is claimed here.

## Security impact

No validation, source authority, isolation, body limit or Required contract is
weakened. Direct controls reject missing/relative fault libraries and duplicate
catalog identities. Socket/callback failures propagate and close the original
connection; error observations cannot become successful abort evidence.

## Runtime evidence

Unit loopback fixtures and controlled response/barrier collaborators are not
NGINX runtime evidence. No native request or Canonical PASS is asserted for
this candidate.

## Known limitations

An intermediate new test incorrectly assumed a short content-length read was
already closed. Its failing logs are retained; the corrected test preserves
rejection of an unclosed message. This is not a demonstrated product defect.
Fresh Sonar analysis and combined native evidence remain outstanding.

## Remaining risks

The actual host must still prove framing, Root/nobody identities, native fault
delivery, all selected Required evidence and cleanup at the integrated tuple.

## Checks not run and rationale

Ruff is absent from the existing environment and was not installed. Full
integrated lint, current-revision CI/Sonar, complete native runtime and protected
Exact-Head verification are not certified by these focused tests.

## Final diff and review status

Independent read-only review found no concrete behavior regression, identified
missing snapshot/callback/barrier/route controls, and those controls were added
and executed. Coordinator integration and final diff review remain required.
