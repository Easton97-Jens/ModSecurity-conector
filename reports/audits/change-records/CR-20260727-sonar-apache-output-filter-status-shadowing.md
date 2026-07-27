# Change Record: Parent Apache output-filter status shadowing for SonarQube Cloud C:S1117

**Language:** English | [Deutsch](CR-20260727-sonar-apache-output-filter-status-shadowing.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-apache-output-filter-status-shadowing |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `c:S1117` Code Smell `AZ98JcyRLJyjbmyNA5LH` at `connectors/apache/src/msc_filters.c:1213`. |
| Boundary | Parent Apache output-filter source and its Parent source-contract test, plus this English/German Change Record pair and indexes. Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

`output_filter(...)` already owns an outer `rc` status variable. The local
result of `apache_finish_unread_request_body(...)` now has the descriptive
name `request_body_rc`, removing the shadowed declaration without changing a
status value, branch, request-body operation, response-header operation, or
Apache filter ABI.

The paired source-contract regression records the relevant control flow: a
non-success unread-body-drain status is returned before the response-header
section, while the existing success path continues to that section.

## Validation

| Check | Result |
| --- | --- |
| Focused Parent source-contract module | passed: `tests.test_apache_request_transaction_cleanup`, 6 tests in 0.013s. |
| Existing Apache Common-adoption structural control | passed: `ci/checks/connectors/apache/check-apache-common-adoption.py`. |
| Native Apache request-transaction cleanup check | blocked_environment: the check exited 77 because no usable `apxs`/`apxs2` Apache headers are available; it did not compile the C source. |
| `git diff --check` | passed after the full B22 traceability pair and indexes were added. |

## Motivation and problem statement

The concrete Sonar rule, Parent scope, and behavior-preservation rationale are
recorded in the preceding `## Motivation and decision` section. This
structural correction does not change the documented source or test behavior.

## Acceptance criteria

- Preserve the exact remediation and focused validation already recorded.
- Retain equivalent technical facts in this English/German Change Record pair.
- Do not convert blocked, unrun, or pending hosted evidence into a pass.

## Implementation decision and rationale

Keep the existing rationale and validation intact, and restore the canonical
Change Record headings instead of weakening the documentation checker or
creating a record-specific exception.

## Changed files

The original versioned scope is recorded in `## Identity` and the preceding
implementation narrative. This follow-up changes only the structure of this
Change Record pair.

## Commands executed

The exact commands and observed outcomes remain in `## Validation`; this
structural correction does not reclassify any result.

## Security impact

The existing section below remains authoritative for this record's specific
boundary. This normalization changes no security control.

## Security impact and limitations

Security classification: `not_applicable` as a security finding. This is a
Code Smell, not a demonstrated attacker-controlled path or broken control.
The security-relevant protocol invariant was nevertheless reviewed: an
unread-body drain failure must return before response headers are passed to
ModSecurity, and the focused source contract preserves that ordering. Native
Apache compilation/runtime validation remains blocked by unavailable Apache
development headers. The local candidate is uncommitted and no hosted Sonar
analysis, GitHub CI, commit, push, pull request, or master merge has occurred.
The Sonar key remains OPEN until a delivered head is analyzed.

## Runtime evidence

No additional runtime evidence is claimed by this structural correction; the
existing validation retains only its recorded source-contract scope.

## Known limitations

The existing security and validation text records the unavailable Apache
development-header prerequisite and its resulting native-validation limit.

## Remaining risks

No new risk is introduced by record normalization. Hosted analysis and any
native Apache evidence remain limited to results actually observed later.

## Checks not run and rationale

No additional connector runtime, native Apache build, or hosted check is run
for this documentation-only correction; the original blocked prerequisites
remain unchanged.

## Final diff and review status

The earlier delivery wording is a snapshot of the original local validation.
This record does not assert a final PR verification, merge, or Sonar issue
closure for a later delivery head.
