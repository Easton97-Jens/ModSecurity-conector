# Change Record: Parent HAProxy binding body-phase deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-binding-body-phase-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-binding-body-phase-deduplication |
| Date (UTC) | 2026-07-29 |
| Base revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` (original selected PR head: `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`). |
| Tracking | Two current SonarQube Cloud CPD pairs in the HAProxy binding: phase-2 and phase-4 chunk append/finalization paths (68 reported duplicate lines). |
| Boundary | Parent HAProxy binding source, its local binding self-test/fixture/Make target, reader documentation, and paired Change Record indexes. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

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
- The binding self-test exercises both public body-wrapper lifecycle paths:
  null transaction, nonzero-length/null-pointer rejection, response append
  before headers, valid append/finalization, post-EOS append, and duplicate
  finalization.
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
- `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c`,
  `connectors/haproxy/Makefile`, and
  `connectors/haproxy/harness/fixtures/modsecurity-binding-lifecycle.conf` —
  real-libmodsecurity request/response wrapper-lifecycle regression coverage.
- `connectors/haproxy/README.md` and `connectors/haproxy/README.de.md` —
  accurately bounded self-test coverage and runtime limitations.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| Earlier selected-PR-head controls | historical only; they are not evidence for the synchronized candidate. |
| GCC C17 binding build and self-test | passed at implementation candidate `4d17b3f5e0fea7ea9cbc555381c59336a0bf529f` with `-std=c17 -Wall -Wextra -Werror` and the registered temporary libmodsecurity prefix; P2/P4 lifecycle output is `self-test-only`. |
| Clang C17 binding build and self-test | passed with the same flags, prefix, and lifecycle output. |
| Parent `check-haproxy-c17` | passed; the focused HAProxy C17 compile completed. |
| Static HTX overlay contract | passed all checks, including borrowed-chunk forwarding and exactly one guarded P2/P4 EOS callsite. |
| HAProxy Common-adoption contract | passed all checks. |
| Bilingual documentation unit suite | passed: 21 tests. |
| Candidate diff hygiene | passed: `git diff --check origin/master...4d17b3f`. |
| `test-htx-overlay` helper harness | `blocked_environment`: its static first stage passed, then the intentionally unmaterialized Framework file `modules/ModSecurity-test-Framework/tests/runners/synchronized_upstream.py` was absent. No Framework content was materialized or changed to obtain a pass. |

## Security impact

This code processes HTTP-derived body chunks at a host-protocol boundary. The
refactor preserves the source-to-sink invariant: a nonzero length still
requires a non-null borrowed pointer; each phase reaches only its matching
libmodsecurity function; post-EOS input remains rejected; and only the phase
finisher captures that phase's intervention. The native request-body rule
self-test and the added public-wrapper lifecycle regression were rerun with
both compilers on implementation candidate `4d17b3f...`. No validation, isolation, logging,
late-intervention, or Quality Gate control is relaxed.

## Runtime evidence

The enhanced self-test used the temporary existing libmodsecurity prefix and
confirmed the phase-1/request-body rule path plus P2 and P4 wrapper lifecycle
guards. It does not execute a live HAProxy runtime, CRS rules, or a positive
response-body enforcement rule. The static HTX
contract verifies phase-4 dispatch and finalization source invariants, but it
is not a host-runtime claim.

## Known limitations

- A live HAProxy 3.2.21 plus libmodsecurity runtime and CRS fixture were not
  run in this narrow task. The helper harness cannot proceed in this temporary
  Parent worktree because its pinned Framework runner is intentionally not
  materialized.
- A fresh exact-candidate Codex Security diff scan, hosted checks, and
  SonarQube Cloud analysis remain pending.

## Remaining risks

- Future descriptor users must remain limited to compatible body append/finish
  functions and the matching transaction fields; a new phase or ownership
  contract needs a lifecycle review.

## Checks not run and rationale

No live HAProxy runtime, response-body enforcement test, CRS self-test, or
full connector matrix is planned for this narrow binding-lifecycle regression.
The attempted full helper harness is classified `blocked_environment`, not
passed; its static first stage is separately recorded as passed. A complete
Security Diff Scan and hosted checks remain required before delivery.

## Final diff and review status

The synchronized candidate is confined to the Parent HAProxy binding, its
narrowly coupled self-test/fixture/Make target, and bilingual traceability.
It removes two confirmed 17-line CPD pairs reported as 68 duplicate lines.
Fresh local compile, self-test, static-contract, and whitespace evidence is
recorded above. A complete Security Diff Scan and exact-head hosted
verification remain required before any delivery or merge claim.
