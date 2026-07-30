# Change Record: Parent Common HTTP authorization-service const correctness

**Language:** English | [Deutsch](CR-20260730-sonar-common-http-auth-maintenance.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-common-http-auth-maintenance` |
| Date (UTC) | 2026-07-30 |
| Base revision | `fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f` |
| Tracking | Current `common/runtime/http_authorization_service.c` SonarQube Cloud issues `AZ9MwjL6-bUaKQ_zSGBP`, `AZ9MwjL6-bUaKQ_zSGBQ`, `AZ9MwjL6-bUaKQ_zSGBT`, `AZ9MwjL6-bUaKQ_zSGBU`, `AZ9MwjL6-bUaKQ_zSGBV`, `AZ9MwjL6-bUaKQ_zSGBW`, `AZ9MwjL6-bUaKQ_zSGBX`, `AZ9MwjL6-bUaKQ_zSGBY`, and `AZ9MwjL6-bUaKQ_zSGBa` (`c:S5350`, `c:S995`, and `c:S1066`). |
| Boundary | Parent Common HTTP authorization service, paired Change Record/index documents, and no Framework/MRTS/Gitlink/workflow/Sonar configuration change. |

## Motivation and problem statement

The current Common baseline has eight locations where the HTTP parser or a
runtime view retains a writable pointer even though it only reads through that
pointer, plus one nested transaction-finish conditional.  The parser must keep
mutating its owned request buffer at the deliberate delimiters; the fix must
not accidentally make those mutation sites immutable or change request,
timeout, transaction, or response semantics.

## Acceptance criteria

- The eight Sonar const-correctness findings use `const` only at read-only
  pointer boundaries while parser-owned delimiter writes remain valid.
- The transaction-finish result remains evaluated only when a transaction
  exists, with the same error status, decision name, and success result.
- The C source compiles and the real timeout-service smoke preserves malformed
  CLI, timeout, request, and response control behavior in explicit C17 mode
  with both available compilers.
- No security control, Sonar rule, Quality Gate, suppression, or runtime
  dependency is changed.

## Implementation decision and rationale

Read-only parser cursors, header-range bounds, header values, and the runtime
view are now declared `const`.  The one mutable parsing cursor is reconstructed
from the owned request buffer and the read-only first-line boundary, so the
existing NUL termination of header delimiters remains explicit and legal.
The transaction-finish branch now uses short-circuit conjunction; C guarantees
that the finish call is not made for a null transaction, preserving the former
nested control flow.

## Changed files

- `common/runtime/http_authorization_service.c`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260730-sonar-common-http-auth-maintenance.md`
- `reports/audits/change-records/CR-20260730-sonar-common-http-auth-maintenance.de.md`

## Commands executed

| Command or control | Actual result |
| --- | --- |
| `BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260730-common-sonar-remediation/build/http-auth-gcc VERIFIED_RUN_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260730-common-sonar-remediation/runtime/http-auth-gcc CC=gcc make check-http-authorization-service-timeout` | passed with `-std=c17 -Wall -Wextra -Werror`; the smoke completed malformed-CLI and timeout controls and three loopback request/response service controls. |
| Same command with `CC=clang` and the separate `http-auth-clang` external roots | passed with the same explicit C17 warning contract and smoke controls. |
| `git diff --check` | passed before this record was added; it will be rerun for the final delivery candidate. |

## Security impact

This is a maintainability-only C type/control-flow correction in an HTTP
authorization boundary.  It does not alter header syntax validation, body-size
limits, peer/local endpoint conversion, transaction construction, response
serialization, or timeout handling.  The short-circuit condition retains the
null-transaction guard, and no validation or error path was weakened.

## Runtime evidence

The existing `check-http-authorization-service-timeout` smoke compiles the
service with its real Common dependencies and exercises invalid CLI forms,
bounded socket service startup, timeout behavior, and valid HTTP request
handling.  It is focused service evidence, not a full connector or
libmodsecurity matrix.

## Checks not run and rationale

- No full connector/CRS/MRTS matrix was run: this patch changes only Common
  parser type qualifiers and a short-circuit expression, not connector
  integration or rule execution.
- A full repository security scan was not run: the source change has no new
  controlled input, sink, policy, or security control; the focused C smoke
  exercises the changed service boundary.
- Hosted GitHub Actions, current-head SonarQube Cloud analysis, and review
  status are not yet available because the task branch has not yet been
  delivered. They are required before the Draft PR is called verified.

## Remaining risks

SonarQube Cloud remains the authority for confirming that all nine selected
baseline Code Smells disappear in the PR comparison.  Any later source or
documentation commit requires a fresh exact-head hosted verification round.

## Final diff and review status

The candidate is limited to the selected Common service, required bilingual
traceability, and no nested-repository or scanner-configuration file. Draft
PR [#196](https://github.com/Easton97-Jens/ModSecurity-conector/pull/196) was
created from the task branch. This record-only follow-up requires a fresh
current-head GitHub Actions, SonarQube Cloud, and review verification round;
no merge or `master` change is claimed.
