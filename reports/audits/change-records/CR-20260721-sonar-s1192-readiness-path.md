# Change Record: Parent readiness-path constant for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260721-sonar-s1192-readiness-path.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-sonar-s1192-readiness-path |
| Date (UTC) | 2026-07-21 |
| Base revision | 2ade0d40983b7af21a65b8cd2884866b85626393 |
| Tracking | One Parent-only python:S1192 Code Smell: AZ9cRybOHhV2CayPTPwc. |
| Boundary | The remaining-connectors claim-policy checker and this Parent traceability pair/index only; Framework, MRTS, gitlinks, connector runtime, scanner configuration, and Quality Gates remain unchanged. |

## Motivation and problem statement

The English readiness-report relative path occurred three times in the
claim-policy checker: once in the report list and twice in the independent
English report read. SonarQube Cloud rule python:S1192 reports that repeated
literal. The checker is a repository policy control, so the replacement must
preserve the exact report selected, existence check, decoding behavior,
diagnostics, regular-expression checks, and connector-status evaluation.

## Acceptance criteria

- Define one module-level constant for reports/current/readiness.md and route
  each previously reported use through it.
- Keep the English and German report-list order and every existing policy
  decision and diagnostic intact.
- Run the native claim-policy target plus syntax/static and traceability checks
  before delivery.
- Obtain fresh exact Draft-PR SonarQube Cloud evidence before claiming the key
  is resolved.

## Implementation decision and rationale

READINESS_REPORT_EN is an immutable module-level relative path. REPORTS uses
the constant for its English member; the separate English read constructs one
Path from the same constant and reuses that Path for its existing is_file and
read_text sequence. The German report entry, the diagnostic string, all regex
patterns, and all control flow remain unchanged.

This is deliberately one source/key rather than a mechanical project-wide
python:S1192 sweep. Other duplicate literals can encode commands, protocol
tokens, report content, or generator semantics and need their own review.

## Security impact

The affected path is a hardcoded repository-relative value, not a value from an
untrusted source. This extraction neither changes file-access authorization nor
normalization, path containment, runtime protocol behavior, authentication,
authorization, logging, scanner configuration, Quality Gates, suppressions,
NOSONAR markers, or false-positive dispositions. A focused assessment found no
security-boundary change requiring a separate security-finding remediation.

## Changed files

- ci/checks/connectors/all/check-remaining-connectors-claim-policy.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| rtk proxy env TMPDIR=<task-owned path> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make check-remaining-connectors-claim-policy | passed: remaining connectors claim policy: ok. |
| rtk proxy env PYTHONPYCACHEPREFIX=<task-owned path> python3 -m py_compile ci/checks/connectors/all/check-remaining-connectors-claim-policy.py | passed. |
| Focused source-structure assertion | passed: the report list and separate English read derive from READINESS_REPORT_EN; no direct ROOT / reports/current/readiness.md construction remains. |
| Focused Change Record contract | passed: all required English/German sections and matching identity values are present. |
| rtk proxy env TMPDIR=<task-owned path> PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs | passed: 11 tests. |
| rtk proxy git diff --check | passed. |
| rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-remaining-connectors-claim-policy | passed on the current-master reconciliation tree: remaining connectors claim policy: ok. |
| rtk proxy git diff --cached --check origin/master | passed after the current-master documentation-conflict resolution. |

The original PR #79 head e0c7e70ed12c5903f5cb751c5903f451a67c2e1a had
observed passing applicable GitHub checks and SonarQube Cloud analysis, but it
became stale and conflicting. Those results do not establish the current-master
reconciliation, which requires a fresh exact-head delivery cycle.

## Runtime evidence

No connector runtime path changes. The focused native target executes the
existing policy checker against current Parent report and metadata files.

## Checks not run and rationale

- A full connector build/runtime matrix is not applicable to this
  semantics-preserving policy-checker constant extraction; no connector source
  or runtime harness changed.
- The full repository bilingual checker is not used as evidence here because it
  includes Framework-linked material outside this Parent-only task. The
  bilingual pair and index receive focused validation instead.

## Known limitations

This change addresses one current Sonar observation only. The native target
proves current policy-checker behavior, not an entire connector runtime matrix.

## Remaining risks

The broader Parent-only SonarQube Cloud backlog remains tracked separately. The
reconciled exact upstream head still requires fresh hosted SonarQube Cloud,
GitHub Actions, review, and delivery evidence before any merge claim.

## Final diff and review status

The source change was delivered as the original PR #79 head
e0c7e70ed12c5903f5cb751c5903f451a67c2e1a. This record corrects its earlier
pre-delivery wording. Current-master reconciliation and any resulting master
integration are separate delivery events: their final branch, commit, PR head,
checks, SonarQube Cloud disposition, review, and merge result must be observed
at their exact delivered heads and are not inferred here.
