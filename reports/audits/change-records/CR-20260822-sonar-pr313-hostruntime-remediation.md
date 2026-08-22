# Change Record CR-20260822: PR #313 hostruntime Sonar remediation

**Language:** English | [Deutsch](CR-20260822-sonar-pr313-hostruntime-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260822-sonar-pr313-hostruntime-remediation` |
| Date (UTC) | `2026-08-22` |
| Base revision | `9b26e55059783ea97a304c94bb62dc0c0f2b0554` |
| Scope | Parent repository only: hostruntime manifest projection, focused regression tests, and paired traceability. No Framework, MRTS, Gitlink, Sonar suppression, exclusion, or quality-gate configuration change. |

## Motivation and problem statement

The already merged Parent PR [#313](https://github.com/Easton97-Jens/ModSecurity-conector/pull/313)
has an immutable historical SonarCloud analysis. Its public exact-PR issue query
reported four open New-Code code smells in
`ci/runtime/lifecycle/write-hostruntime-record.py`: three `python:S1192`
duplicate-literal instances and one `python:S3776` cognitive-complexity
instance. All four map directly to the PR #313 source diff.

This successor change remediates the implementation rather than suppressing
the findings. The meaningful zero target is the successor PR's own
exact-head SonarCloud query; no follow-up can rewrite the historical #313
analysis.

## Acceptance criteria

- Remediate all four directly mapped code-smell instances without `NOSONAR`,
  exclusions, suppressions, test deletion, or quality-gate changes.
- Preserve fail-closed artifact-map validation before any projection mutation.
- Preserve runtime-root containment, no-symlink/regular-file checks,
  canonical self-artifact paths, reserved-path rejection, artifact-state
  validation, and checksum verification.
- Add focused regression coverage for the refactored validation branches.
- Obtain a successor PR SonarCloud exact-head issue query with `total: 0` for
  open or confirmed New-Code issues.
- Do not modify Framework, MRTS, a Gitlink, or NGINX-specific configuration.

## Implementation decision and rationale

- Centralized the repeated `manifest.json`, `hostruntime record`, and
  `hostruntime summary` literals as named constants.
- Split the former high-complexity artifact-map validator into small helpers
  for map/name validation, self artifacts, non-produced artifacts, produced
  artifacts, checksums, and reserved paths. The caller ordering is unchanged:
  result artifacts are validated before manifest artifacts.
- Kept `preflight_manifest_projection()` and `project_manifest()` as the two
  callers, so validation remains before output creation and immediately before
  result/manifest projection.
- Added regressions for noncanonical self paths, reserved lifecycle paths in
  both artifact maps, and invalid produced-artifact checksum/state values.

## Security impact

Although the Sonar findings are maintainability code smells, the affected
function guards a security-relevant path and manifest boundary. A focused
review of the successor diff found no weakening of containment, symlink,
checksum, state, or pre-mutation controls. The refactor remains fail closed
for malformed artifact declarations.

## Changed files

- `ci/runtime/lifecycle/write-hostruntime-record.py`
- `tests/test_hostruntime_record.py`
- `reports/audits/change-records/CR-20260822-sonar-pr313-hostruntime-remediation.md`
- `reports/audits/change-records/CR-20260822-sonar-pr313-hostruntime-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| `python -B -m unittest tests/test_hostruntime_record.py` | Passed: 23 tests, including the new path/state/checksum regressions. |
| `python -B -m unittest tests/test_hostruntime_workflow_evidence_contract tests/test_collect_hostruntime_preflight_evidence` | Passed: 9 workflow/evidence-contract and fail-closed collector tests. |
| `python -B -m unittest tests/test_hostruntime_preflight tests/test_ci_security_workflows` | Passed: 55 preflight and CI-security contract tests. |
| `git diff --check` | Passed for the source and test refactor; rerun is required on the final staged delivery diff. |
| Focused source/security review | Passed: no semantic or security regression found in the artifact-validation invariants. |

## Runtime evidence

The focused test suite invokes the projection command against temporary
runtime-root fixtures. Its negative controls observe the command's fail-closed
exit status before a forbidden artifact declaration can be projected.

## Checks not run and rationale

- The full repository suite was not run: the change is confined to the
  hostruntime writer and its dedicated test suite.
- Ruff and a local Sonar scanner are not installed or configured. No tool was
  installed and no gate was bypassed; hosted successor-PR SonarCloud analysis
  is the authoritative measure.
- `make check-bilingual-docs` was blocked by pre-existing missing links into
  the non-materialized Framework Gitlink in the external worktree. The failure
  lists only those unrelated Framework paths, not either new Change Record.
- No host runtime matrix was started because this change does not alter a
  connector configuration or runtime protocol; the relevant behavior is the
  writer's fail-closed artifact validation.

## Known limitations

PR #313's historical issue count remains visible and immutable after its
merge. This successor record and PR can only establish a zero count for the
successor head and, later, for its resulting `master` revision.

## Remaining risks

Local evidence establishes source and focused behavioral coverage, but the
four issue instances are not verified until SonarCloud analyzes the exact
successor PR head. No merge of this successor PR is authorized by this record.

## Final diff and review status

The Parent-only code and test change is ready for final documentation and Git
review, then one successor Draft PR. It does not authorize a merge, any
Framework/MRTS change, a Gitlink update, or a Sonar configuration change.
