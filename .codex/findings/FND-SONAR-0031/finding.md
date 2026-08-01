# FND-SONAR-0031 — CI evidence report generators retain fifteen SonarQube Cloud cognitive-complexity findings and one duplicate block

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / security relevant | no / yes |
| Security assessment | focused post-change security-diff review: zero reportable diff-induced findings |

## Summary and scope

The revision-bound SonarQube Cloud master inventory has fifteen OPEN CRITICAL
`python:S3776` receipts in Parent `ci/evidence` report generators and one
23-line duplicate block. It contains no selected-component bugs,
vulnerabilities, or security hotspots. All items are Parent-owned and have a
behavior-preserving source-level disposition in the task-owned worktree.

The scope is limited to Parent evidence-report sources, one existing Parent
lifecycle helper, direct Parent tests, bilingual traceability, and local
evidence. Framework, MRTS, Gitlinks, workflows, SonarQube Cloud settings,
Quality Gates, exclusions, suppressions, `NOSONAR`, direct master writes, and
additional merges are excluded.

Protected PR #225 exact head
`74bcb950f8a75835b4fb59175a783e9aedcfd1c3` was normally merged as resulting
Parent master `6dc912643133e5c7d3c305979d4052da9cb45153`. Its fourteen
exact-SHA GitHub Actions workflows passed. The current master readback marks
all fifteen retained `python:S3776` keys `CLOSED/FIXED` and reports zero
violations, bugs, vulnerabilities, security hotspots, duplicated lines, and
duplicate density for `ci/evidence`.

## Observed and expected behavior

At `caabf33c11d6002f9a1661f215ed195d6e141253`, analysis
`3b1a67b0-1026-4dbc-a437-192604db29b4` reports complexities from 16 through
33 where 15 is allowed. The only selected duplicate pair is the equivalent
CLI lifecycle between the final-consistency-audit and rule-chain generators.

The report schemas, ordering, safe output-root lifecycle, redaction,
two-stage path normalization, and fail-closed runtime-evidence controls must
remain unchanged while focused helpers own separate parsing, filtering,
classification, rendering, and post-write responsibilities. Both entry points
must use the established safe lifecycle without duplicate scaffolding.

## Impact and security assessment

The finding is maintainability work, but the selected code handles
path-constrained output, serialized reports, runtime-evidence interpretation,
and classification. A careless refactor could weaken evidence integrity.

The focused post-change security review found no reportable diff-induced
security finding. It specifically confirmed safe-root setup before output and
the post-write callback, unchanged safe writer use for refresh placeholders,
two-stage path normalization, and fail-closed HAProxy XML decision evidence.
There is no claim of a repository-wide security scan or of hosted analysis.

## Affected files and symbols

Affected source files are:

- `ci/evidence/reports/refresh-connector-reports.py`
- `ci/evidence/reports/generate-connector-roadmap.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-final-consistency-audit.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `ci/evidence/reports/generate-phase4-hard-abort-capability.py`
- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/lib/focused_analysis_utils.py`

The retained issue keys and symbols are listed exactly in the structured
record: `AZ9cRyiqHhV2CayPTPx_`, `AZ9cRyi6HhV2CayPTPyT`,
`AZ7ep2ThZ5UXdmR_OUeO`, `AZ7ajOtE7vSmgsKNjY2U`,
`AZ7WiKyayVFzp-oVN3ZD`, `AZ7PU4lam6NRVhQ0A9r7`,
`AZ9cRyiqHhV2CayPTPyN`, `AZ9cRyiqHhV2CayPTPyB`,
`AZ7HxAmX_i61V0DF6_GQ`, `AZ7HxAoZ_i61V0DF6_G4`,
`AZ7HxAmF_i61V0DF6_GI`, `AZ7HxAmq_i61V0DF6_GU`,
`AZ7HxAnC_i61V0DF6_Gd`, `AZ7HxAlw_i61V0DF6_GE`, and
`AZ7HxAoH_i61V0DF6_G1`.

## Preconditions, reproduction, and evidence

The scope is bound to current master analysis
`3b1a67b0-1026-4dbc-a437-192604db29b4` and revision
`caabf33c11d6002f9a1661f215ed195d6e141253`. Reproduce it with the retained,
read-only SonarQube Cloud issue, component-metric, and duplicate-block API
queries recorded in the inventory receipt:

- Historical Sonar master CI-evidence inventory path
  `.codex/runs/20260801-ci-evidence-sonar-remediation/evidence/sonar-master-ci-evidence-inventory.json`
  (not distributed in this reconciliation checkout)
  — SHA-256 `d521f5a19ac7e6f40f0c49e4c65357a9bdd1dbfed65bf21bbfde4809de19865b`;
  exit `0`; observed `2026-08-01T14:05:20Z`.

The resulting-master verification has the historical path
`.codex/runs/20260801-pr225-master-integration/evidence/master-verification.json`
(not distributed in this reconciliation checkout)
— SHA-256 `d63bacab44956e35958cef9d8bd82e476853a3d77d672ab804285077f4173a4b`;
exit `0`; observed `2026-08-01T16:32:10Z`. It is bound to master
`6dc912643133e5c7d3c305979d4052da9cb45153`, not reused from the baseline.

## Root cause and remediation

The affected functions collected too many independent report responsibilities,
and two CLI entry points retained equivalent lifecycle scaffolding. The patch
extracts narrow helpers while preserving the existing contracts. The final
audit reaches its existing safe lifecycle through an explicit post-write
callback; refresh output continues to use the safe writer; and runtime XML
evidence retains its strict all-or-nothing decision predicates.

No SonarQube Cloud rule, Quality Gate, exclusion, suppression, `NOSONAR`,
workflow, Framework/MRTS source, or Gitlink is changed. This is not a
metric-only code move.

## Acceptance criteria and validation plan

- Each retained issue key and the duplicate block has a concrete source-level
  disposition.
- Focused source/schema/ordering/path/evidence controls pass, including
  legitimate safe-output and fail-closed negative controls.
- A focused post-change security-diff review reports no reportable new finding.
- The exact PR head has zero OPEN/CONFIRMED SonarQube Cloud new issues,
  zero New-Code duplication, and a passing Quality Gate without scanner-control
  changes.
- The separately authorized integration has a resulting-master SonarQube Cloud
  readback: the original fifteen keys are `CLOSED/FIXED` and `ci/evidence`
  reports zero duplicated lines before this record becomes `verified`.

The local suite includes `tests.test_focused_analysis_utils`,
`tests.test_report_conditional_remediation`, `tests.test_case_metadata_utils`,
`tests.test_remaining_failure_analysis`,
`tests.test_nginx_mrts_http500_cluster_analysis`,
`tests.test_report_presentation_literals`,
`tests.test_generated_report_evidence_integrity`,
`tests.test_evidence_output_security`, `tests.test_runtime_path_security`, and
`tests.test_runtime_env_snapshot_contract`.

## Dependencies, blockers, and residual risk

There is no source-level blocker or remaining dependency. Exact PR #225 head
`74bcb950f8a75835b4fb59175a783e9aedcfd1c3` passed its fresh protected checks
and SonarQube Cloud PR Quality Gate before GitHub normally merged it as master
`6dc912643133e5c7d3c305979d4052da9cb45153`. All fourteen exact-master GitHub
Actions workflows passed. The direct resulting-master reproduction closes all
fifteen original `python:S3776` keys and records zero `ci/evidence` duplicate
lines. The global master Quality Gate is nevertheless `ERROR` on the same
pre-existing `new_security_rating` E condition as immediate predecessor
`7016a66f3702523098811b45139133c77dee88fb`; it is separately tracked by
`FND-SONAR-0001` and is not attributed to this finding.

The temporary task worktree lacks an initialized Framework submodule, so one
environment-snapshot test is expected to exit `77` there; the same untouched
test passes in the canonical Parent checkout. A broad `make lint` attempt
stops at pre-existing Apache C17 errors outside this task's scope. Neither
limitation is claimed as a successful full suite or a finding resolution.

Related aggregate: `FND-SONAR-0016`. No duplicate finding or accepted risk is
recorded. The source patch is `014eaff40557ba33346ea0cb33ce8d27be8546d0`,
followed by normal task-branch synchronization and its traceability update at
`d86fd1f91177ae8dceb2906a00d802e4735cd9b4`; neither commit is a hosted or
resulting-master proof.

## History

- `2026-08-01T14:05:20Z`: the revision-bound current-master Sonar inventory
  identified all fifteen receipts and the single duplicate block.
- `2026-08-01T15:34:38Z`: allocated as a dedicated record because the related
  aggregate `FND-SONAR-0016` contains neither the exact current keys nor the
  exact duplicate block. Local remediation and focused control evidence are in
  progress; no commit, push, PR, hosted verification, merge, or master change
  is claimed.
- `2026-08-01T15:51:57Z`: the Parent source/test remediation was committed,
  synchronized normally with current `origin/master`, and rerun through 161
  focused task-worktree tests plus 9 canonical snapshot-contract tests. The
  lifecycle state is `fixed`, not `verified`: no push, Draft PR, exact-head
  hosted analysis, merge, or resulting-master reproduction is claimed.
- `2026-08-01T15:55:56Z`: Draft PR #225 exact head
  `d86fd1f91177ae8dceb2906a00d802e4735cd9b4` is equal locally, remotely, and
  on GitHub. All 39 GitHub checks are terminal (33 passed, 6 scope-skipped),
  and SonarQube Cloud reports Quality Gate `OK`, zero open PR issues, zero new
  duplicated lines, and 0.0% New-Code duplication. No merge or resulting-
  master result is claimed; the record remains `fixed`.
- `2026-08-01T16:32:10Z`: GitHub normally merged protected PR #225 exact head
  `74bcb950f8a75835b4fb59175a783e9aedcfd1c3` as resulting Parent master
  `6dc912643133e5c7d3c305979d4052da9cb45153`. All fourteen exact-master
  GitHub Actions workflows passed. The bound SonarQube Cloud master analysis
  marks all fifteen retained `python:S3776` keys `CLOSED/FIXED`; the selected
  `ci/evidence` component reports zero violations and zero duplicated lines.
  The global Quality Gate remains ERROR solely on the pre-existing
  `new_security_rating` E baseline recorded by `FND-SONAR-0001`; it matches
  the immediate predecessor and is not a PR #225 regression. This record is
  therefore `verified`, not automatically closed.
