# Change Record: Parent Apache maintainability remediation

**Language:** English | [Deutsch](CR-20260730-sonar-apache-maintainability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-apache-maintainability` |
| Date (UTC) | 2026-07-30 |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | `FND-SONAR-0027`; 13 open SonarQube Cloud `CODE_SMELL` findings in `connectors/apache/src`. |
| Boundary | Parent `connectors/apache/`, focused Apache validation, regression contracts, and this paired Change Record/index only. |

## Motivation and problem statement

The current SonarQube Cloud inventory for `connectors/apache/src` reports 13
maintainability findings: two excessive parameter lists, three Cognitive
Complexity findings, six nested conditional expressions, one oversized runtime
state structure, and one unused variadic helper. There are no open Apache
security, reliability, or duplication findings in that inventory.

## Acceptance criteria

- Each recorded Sonar issue key is removed by a source-level remediation, not
  by a suppression, exclusion, scanner, or Quality Gate change.
- Apache request/response event metadata, header snapshots, phase-4 EOS
  containment, directory-configuration merge precedence, and APR cleanup
  ownership retain their existing contracts.
- Changed Apache C units compile under C17 with `-Wall -Wextra -Werror`; the
  focused native harnesses and Python regression contracts pass.
- A fresh exact-head hosted SonarQube Cloud analysis confirms that the original
  13 keys and task-owned replacement issues are absent before any integration.

## Implementation decision and rationale

The intervention event now has one typed input object instead of two wide
functions and nested conditional selection. Request, response-snapshot,
response-gate, and intervention fields are grouped by lifecycle responsibility
without changing their lifetime or default-zero initialization. The filter
phases and directory merge are split into private, single-purpose helpers.
The unused file-writing variadic function is removed. The native cleanup
harness now links APR-util, which owns `apr_brigade_cleanup`.

## Changed files

- `connectors/apache/src/mod_security3.c`
- `connectors/apache/src/mod_security3.h`
- `connectors/apache/src/msc_config.c`
- `connectors/apache/src/msc_filters.c`
- `connectors/apache/src/msc_utils.c`
- `connectors/apache/src/msc_utils.h`
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
- focused Apache regression-contract tests and this paired Change Record/index

## Commands executed

| Command | Result |
| --- | --- |
| Focused intervention cleanup contract | passed (5 tests). |
| Focused phase-4 and synchronized-upstream contracts | passed (17 tests). |
| `make check-apache-request-transaction-cleanup` | passed; native APR lifecycle harness passed after the runner linked APR-util. |
| `make check-apache-ruleset-cleanup` | passed; native RulesSet APR lifecycle harness passed. |
| Direct changed-unit C17 compilation | passed for `msc_config.c`, `msc_filters.c`, and `msc_utils.c` with `-Wall -Wextra -Werror`. |
| Direct mapper C17 compilation | passed with the grouped state definition. |
| Full `make check-apache-c17` | blocked by pre-existing current-master diagnostics in `mod_security3.c` and `msc_config.h`, tracked separately as `FND-PARENT-0069`; no new task-owned diagnostic appears before that baseline stop. |
| `git diff --check` | passed before record creation; rerun before delivery. |

## Security impact

This refactor retains the request/response trust boundary: response bodies stay
set aside through EOS, phase-4 failures remain fail-closed, and intervention
records preserve their bounded common-event serialization. No authentication,
authorization, input validation, logging policy, Sonar control, Framework,
MRTS, Gitlink, or workflow permission is weakened or changed.

## Runtime evidence

The real APR harnesses exercise request-transaction cleanup and directory
RulesSet ownership. Phase-4 regression contracts retain normal, deny,
log-only, error-document, fragmented-bucket, and terminal-output assertions.

## Known limitations

No live Apache/httpd process, CRS, or full connector matrix was run locally.
The full C17 aggregation remains unable to pass until the independent current-
master diagnostic set in `FND-PARENT-0069` is remediated.

## Checks not run and rationale

No live host matrix or full repository security scan was run because this is a
focused maintainability refactor of an already covered native filter boundary.
Hosted Actions, review, and exact-head SonarQube Cloud evidence remain pending
until the Draft PR is delivered.

## Remaining risks

SonarQube Cloud is the authority for the original keys. Local compilation and
focused tests cannot prove their final removal or rule against new issues; no
integration is claimed until fresh exact-head hosted analysis is green.

## Final diff and review status

The candidate is source-local, C17-checked where the current baseline permits,
and paired with traceability. Delivery and exact-head verification are pending;
no merge or `master` change is claimed.
