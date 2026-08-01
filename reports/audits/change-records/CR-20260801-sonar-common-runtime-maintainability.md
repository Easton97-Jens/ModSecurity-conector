# Change Record: Parent Common Runtime SonarQube Cloud maintainability remediation

**Language:** English | [Deutsch](CR-20260801-sonar-common-runtime-maintainability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260801-sonar-common-runtime-maintainability |
| Date (UTC) | 2026-08-01 |
| Base revision | `b370740dcb16739be7e0b323152f69da31c1a8c1` |
| Tracking | Complete current `common/runtime/` SonarQube Cloud maintainability remediation. Hosted verification is required for the exact published PR head. |
| Boundary | Parent `common/runtime/`, the direct Common SDK contract check, and this bilingual Change Record/index pair. Framework, MRTS, Gitlinks, other Parent areas, workflows, SonarQube Cloud configuration, suppressions, exclusions, Quality Gates, and direct `master` writes are out of scope. |

## Motivation and problem statement

The current-master SonarQube Cloud inventory for `common/runtime/` contains
18 open/confirmed maintainability rows and no security, bug, hotspot, or
duplication row. The request is to remediate this complete current scope in
one Parent pull request without changing scanner policy or hiding findings.

| Rule | Count | Remediation disposition |
| --- | ---: | --- |
| `c:S1820` | 1 | Grouped cohesive private transaction state. |
| `c:S107` | 1 | Replaced the wide body-limit helper argument list with typed progress and policy context. |
| `c:S995` | 2 | Marked read-only runtime/parser pointers as `const`. |
| `c:S5350` | 10 | Preserved immutable views for read-only runtime and parser operations. |
| `c:S3776` | 3 | Separated configuration validation, event construction, and transaction-start phases into named private helpers. |
| `c:S1912` | 1 | Replaced non-reentrant calendar conversion with platform-safe reentrant conversion. |
| Total | 18 | 16 rows in `msconnector_runtime.c` and 2 rows in `http_authorization_service.c`. |

## Acceptance criteria

- Cover every currently inventoried `common/runtime/` SonarQube Cloud row
  with a source-level remediation or an explicit evidence-based disposition.
- Preserve bounded HTTP parsing, configuration validation, body-limit policy,
  transaction phase ordering, event integrity, error propagation, and public
  runtime APIs.
- Compile changed C as C17 with `-Wall -Wextra -Werror` using GCC and Clang.
- Keep new violations and new-code duplication at zero, verified only by a
  fresh SonarQube Cloud analysis of the exact PR head.
- Deliver only a task-owned Draft PR; this record does not authorize a merge
  to `master`.

## Implementation decision and rationale

The private transaction object now groups related bounded event metadata and
the already public `msconnector_runtime_body_progress` values. Public progress
accessors retain their original output fields; the runtime still retains no
host request, response, or body pointer. `apply_body_limit_plan` therefore
receives one typed progress object and the existing policy context rather than
ten independent pointers and values.

Configuration parsing is partitioned by value family while preserving all
accepted keys, destinations, defaults, validation functions, side effects,
and error text. Event assembly is split into body, response-state, host-action,
and JSONL-write helpers without changing hash order, escaping, size checks, or
the update of the previous event hash. Transaction startup is likewise split
only at its existing validation, allocation, native-phase, and request-body
boundaries; abort behavior remains centralized in the existing cleanup path.

The authorization service only changes local parser traversal pointers to
`const`. The timestamp helper uses `gmtime_r` on the POSIX build path and
`gmtime_s` on Windows, replacing the prior non-reentrant fallback. No public
API, SonarQube Cloud policy, suppression, exclusion, or `NOSONAR` marker is
introduced.

The direct Common SDK contract now recognizes the equivalent grouped private
body-progress representation. It continues to require bounded progress,
limit outcomes, explicit end-of-stream state, and the prohibition on retaining
host-owned request or response pointers.

## Security impact

The touched paths process untrusted HTTP request/response data and
operator-controlled configuration. The refactor preserves the existing
security invariants: string and header validation precede engine calls;
resource limits and body-limit action remain active; only bounded metadata is
copied into events; JSONL serialization is size-checked before write; and the
flow guard retains phase and immutable-finalization enforcement. No
authentication, authorization, parser validation, limit, path policy,
logging, test, scanner, or Quality Gate control was weakened.

The finalized local security-diff review covers both runtime translation units
and the direct SDK contract. It records zero new reportable security findings;
the readable report is retained in the task-owned external run directory. This
is source-level evidence and does not claim a complete native host runtime.

## Changed files

- `common/runtime/msconnector_runtime.c`
- `common/runtime/http_authorization_service.c`
- `ci/checks/common/check-common-sdk-contract.py`
- This English/German Change Record pair and both Change Record indexes.

## Commands executed

| Control | Result |
| --- | --- |
| `make check-common-helpers-c17` | passed |
| `make check-common-sdk-contract` | passed |
| `python3 tests/test_sonar_reliability_contract.py` | passed: 12 tests |
| `make check-common-security-contract` | passed |
| `make check-common-memory-safety` | passed |
| `make check-common-flow-integrity` | passed |
| `make check-http-authorization-service-timeout MSCONNECTOR_C_STD=c17` | passed |
| GCC C17 syntax check for both changed runtime translation units | passed |
| Clang C17 syntax check for both changed runtime translation units | passed |
| `make check-bilingual-docs` | blocked only by existing links into the deliberately uninitialized Framework submodule; no new Change Record or index diagnostic |
| `git diff --check` | passed |
| Codex Security diff review | passed: complete local-diff coverage, zero reportable findings |

## Runtime evidence

The authorization-service timeout smoke exercises bounded HTTP input, loopback
service startup, timeout behavior, and response handling. Common helper,
contract, security, memory-safety, and flow controls exercise the relevant
bounded-data and lifecycle invariants. These checks do not claim a full native
connector-plus-libmodsecurity host matrix result.

## Checks not run and rationale

A full native host matrix is not run locally because this change is confined
to the connector-neutral runtime and does not select one host adapter. No
stub, altered Gitlink, Framework source, or relaxed prerequisite was used to
manufacture that evidence. The local SonarQube Cloud scanner is not installed;
the authoritative New-Code issue and duplication result must be observed on
the exact published PR head.

The repository has no `check-documentation` Make target. The available
`check-bilingual-docs` control was run; its only diagnostics are existing
Framework-submodule link targets outside this Parent-only change.

## Known limitations

Local source and focused runtime evidence cannot prove the hosted Quality Gate
for a future PR commit. Any SonarQube Cloud new issue, new duplication, or
failed required check must be corrected on the task branch before review or
integration.

## Remaining risks

The exact pushed head may receive a different hosted result from the
current-master inventory. This record makes no claim about a PR, review,
hosted CI, SonarQube Cloud result, or merge that has not yet been observed.

## Final diff and review status

The diff is restricted to Parent Common Runtime source, its direct contract
assertion, and the bilingual traceability record. Any hosted evidence is valid
only when it is bound to the currently published exact PR head; it is retained
separately from this record. No direct `master` write or merge is authorized by
this request.
