# Change Record: Parent HAProxy binding body-phase deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-binding-body-phase-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-binding-body-phase-deduplication |
| Date (UTC) | 2026-07-29 |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | Two current SonarQube Cloud CPD pairs in the HAProxy binding: phase-2 and phase-4 chunk append/finalization paths (68 reported duplicate lines). |
| Boundary | Parent HAProxy binding source and paired Change Record indexes. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The binding duplicated lifecycle guards and bookkeeping in request-body phase 2
and response-body phase 4. Reduction must retain distinct phase numbers,
transaction-state fields, libmodsecurity entry points, diagnostics, and
intervention capture timing without creating a connector-owned body buffer.

## Acceptance criteria

- Shared append and finish helpers retain the former null, header-before-body,
  post-EOS, pointer/length, library-failure, accounting, and decision paths.
- Explicit request and response wrappers retain their public APIs and use only
  their existing `msc_append_*_body` and `msc_process_*_body` functions.
- The native binding self-test passes under GCC and Clang in C17 mode with
  `-Wall -Wextra -Werror`.
- Exact-head hosted checks and SonarQube Cloud must prove zero New Issues, zero
  New-Code Duplicate Lines, zero New-Code duplication density, and a lower
  total duplicate count before any merge consideration.

## Implementation decision and rationale

A typed per-call phase descriptor supplies transaction fields, messages, phase
number, and matching libmodsecurity entry points to two small helpers. The
public functions remain explicit wrappers, including the `transaction == 0`
diagnostic needed before a descriptor can be constructed. This removes the two
duplicated pairs without changing phase ownership or the external API.

## Changed files

- `connectors/haproxy/src/haproxy_modsecurity_binding.c` — typed common body
  append/finalization helpers and four explicit phase wrappers.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| GCC C17 native binding build | passed with `-std=c17 -Wall -Wextra -Werror` against the temporary existing libmodsecurity prefix. |
| GCC C17 `self-test-modsecurity-binding` | passed; request-body disruptive-rule self-test reported status 403. |
| Clang C17 native binding build | passed with `-std=c17 -Wall -Wextra -Werror` against the same temporary prefix. |
| Clang C17 `self-test-modsecurity-binding` | passed with the same self-test-only scope. |
| `python3 ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | passed; lifecycle, borrowed-slice, EOS-callsite, host-action, and no-unsupported-claim controls passed. |
| `python3 ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | passed. |
| `git diff --check` | passed. |

## Security impact

This code processes HTTP-derived body chunks at a host-protocol boundary. The
refactor preserves the source-to-sink invariant: a nonzero length still
requires a non-null borrowed pointer; each phase reaches only its matching
libmodsecurity function; post-EOS input remains rejected; and only the phase
finisher captures that phase's intervention. The native request-body rule
self-test passed through the real libmodsecurity C API. No validation,
isolation, logging, late-intervention, or Quality Gate control is relaxed.

## Runtime evidence

The compiled self-tests use the temporary existing libmodsecurity prefix and
confirm the phase-1 and request-body rule path. They do not execute a live
HAProxy runtime, CRS rules, or response-body enforcement. The static HTX
contract directly verifies phase-4 dispatch and finalization source invariants,
but it is not a host-runtime claim.

## Known limitations

- A live HAProxy 3.2.21 plus libmodsecurity runtime and CRS fixture were not
  available in this task worktree.
- The full Codex Security diff-scan capability is unavailable in this runtime:
  its mandatory delegated-worker preflight is incomplete. This record does not
  claim a complete scanner report.
- Hosted checks and a fresh exact-head SonarQube Cloud analysis remain pending.

## Remaining risks

- Future descriptor users must remain limited to compatible body append/finish
  functions and the matching transaction fields; a new phase or ownership
  contract needs a lifecycle review.

## Checks not run and rationale

No live HAProxy/libmodsecurity runtime, response-body enforcement test, CRS
self-test, full connector matrix, or complete Codex Security diff scan ran.
The external source/fixtures are absent in this temporary task environment,
and the scanner's mandatory delegated-worker capability is unavailable. Native
C17 binding self-tests and the static HTX contract are the strongest available
controls.

## Final diff and review status

The candidate is confined to the Parent HAProxy binding and bilingual
traceability. It removes two confirmed 17-line CPD pairs reported as 68
duplicate lines. Local compile, self-test, static contracts, and whitespace
review are complete. A Draft PR and exact-head hosted verification remain
required before any delivery or merge claim.
