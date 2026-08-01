# Finding FND-SONAR-0022: Block-status generator permits CLI-selected output to escape its selected root

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `security_validated` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P1` / `medium` / `confirmed` |
| Status / feasibility | `fixed` / `feasible_now` |
| Release blocker / security relevant | yes / yes |
| Sonar inventory | `pythonsecurity:S8707`, `AZ8d8_sBE36x1qGA4xhY` |

## Summary, behavior, and impact

The inventory-bound SonarQube Cloud vulnerability `pythonsecurity:S8707`, key
`AZ8d8_sBE36x1qGA4xhY`, applies to the Parent block-status generator's
CLI-selected output boundary. The historical generator accepted
`--out-dir ../generator-outside/baseline-escape` and created generated files
outside the caller-selected current-working-directory root.

Expected behavior accepts only a relative descendant of the deliberately
selected current working directory. Absolute paths, parent traversal,
intermediate-symlink escape, and a final generated-file symlink must not alter
an external target; ordinary nested in-root output remains valid. Protected-
squash PR #200 from exact head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` is now Parent master
`13890da56ad19a105629243349f39ea8c084f396`. Its generator and checker blobs
equal the reviewed candidate; the original containment and legitimate-output
controls, focused reliability suite, bilingual suite, and all 14 master
workflows passed. Default-branch analysis
`c1f32224-aa05-4202-9b10-65c15165ff35` no longer reports the original key.
The finding remains `fixed` rather than `verified` solely because the
non-ignored default-branch Quality Gate is `ERROR`; it is not risk-accepted.

## Scope, preconditions, and reproduction

- Affected files/symbols: `ci/tools/generate-block-status-config.py`,
  `ci/checks/common/check-block-status-generator.py`, `generate`,
  `resolve_output_dir`, `open_output_dir`, and `write_generated_file`.
- Preconditions: a caller controls `--out-dir`; a writable sibling or an
  externally resolving path entry is available; the historical implementation
  is used.
- Reproduce the baseline from a task-owned current working directory with
  `--out-dir ../generator-outside/baseline-escape`; generated files appear
  outside the selected root. Then run the focused checker: nested in-root
  output passes, while traversal, absolute, intermediate-symlink, and
  final-file-symlink controls cannot alter an external target.

## Evidence

Run ID: `ci-tools-sonar-remediation-20260730`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `.codex/plans/ci-tools-sonar-remediation.md` | `0029f0724d663e1d84408d56af69e71724a79f79dbb24c862aa0f628ffc0852c` | Inventory records analysis `00fc69e7-8a50-4c44-9eae-abaf077610f5`, issue `AZ8d8_sBE36x1qGA4xhY`, and the baseline traversal reproduction. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/report.md` | `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7` | Complete focused security-diff review has zero diff-introduced findings; all focused hostile-path controls pass locally. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/artifacts/05_findings/attack_path_analysis_report.md` | `9cb84a91230740f9ca22f10e64c98cf1900edc6ab9fe581d5dd8dc2c14d30d92` | The final patch rejects absolute/traversal inputs, uses no-follow directory descriptors, and atomically replaces only fixed generated names. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-exact-head-verification.md` | `42ba7a4ff8ff0172997a935f04a7fdf560b7b6ce9c70daab97fa24e69024f3be` | Exact Draft-PR #200 head is OPEN/Draft/CLEAN and MERGEABLE; required checks and SonarQube Cloud readbacks pass with zero PR issues, zero new violations, and `0.0%` new-code duplication. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-66db7e3f-exact-head-verification.md` | `33cc911a5ee393fb44906c3e4dac76634df86d99fe07b3e105be9962148c840a` | Refreshed Draft-PR #200 head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` against master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` is OPEN/Draft/CLEAN and MERGEABLE; required checks and SonarQube Cloud readbacks pass with zero PR issues, zero new violations, and `0.0%` new-code duplication. |

All observations are from the Parent scope; Framework, MRTS, Gitlinks,
scanner rules, Quality Gates, exclusions, `NOSONAR`, and suppressions are
unchanged.

## Root cause, remediation, and acceptance

The historical code joined a caller-controlled directory with generated
filenames through ordinary path operations, without a containment contract or
descriptor-anchored no-follow traversal. The task patch rejects absolute and
parent-traversal values, requires an in-root relative descendant, opens each
directory component with no-follow semantics, and uses an exclusive temporary
file plus descriptor-relative atomic replacement for fixed generated names.

Acceptance and validation include the focused generator and Sonar reliability
contracts, the byte-compatible `501,403` output control, the sealed security
review, and default-branch analysis on exact master
`13890da56ad19a105629243349f39ea8c084f396`, which no longer reports
`AZ8d8_sBE36x1qGA4xhY` without a scanner-control change. Promotion to
`verified` or `closed` additionally requires the non-ignored default-branch
Quality Gate to be `OK`; that condition remains unmet.

## Dependencies, controls, related findings, and residual risk

Exact Draft-PR and resulting-master SonarQube Cloud evidence is retained; the
authorized integration and resulting-master revalidation have occurred.
Regression controls are
`ci/checks/common/check-block-status-generator.py` and
`tests/test_sonar_reliability_contract.py`; the legitimate control is nested
in-root output with byte-compatible generated output. The remaining condition
is the non-ignored default-branch Quality Gate `ERROR`, which blocks security
promotion but is not waived.

`FND-SONAR-0001` and `FND-SONAR-0016` are related Sonar context, not
duplicates; `FND-PARENT-0036` is a distinct native-lifetime boundary. The
selected current-working-directory root remains a trusted, exclusive
caller/environment assumption. No risk acceptance was made; the protected
master integration is retained as evidence.

## History

- `2026-07-30T10:46:48Z`: allocated after inventory and baseline traversal
  reproduction established the independently remediable CLI-to-filesystem
  boundary; local patch and security review pass, exact PR-head verification
  was pending at that time.
- `2026-07-30T11:07:21Z`: exact Draft-PR #200 head `2bc97ac058725fdba6a36ad93307487c160b1f05` passed required
  GitHub checks and SonarQube Cloud Quality Gate/readbacks: zero PR issues,
  zero new violations, and `0.0%` new-code duplication. The finding is
  `fixed` on the candidate but remains release-blocking on current master
  until authorized integration and resulting-master revalidation.
- `2026-07-30T11:33:48Z`: after master advanced to `726322b17d6423c7f9e3bba0e6affc051dbf94cd`, normal merge commit `66db7e3f2de324c960d8db36b4b6760d958cd7e1` retained both Change-Record index entries. The refreshed Draft PR is CLEAN/MERGEABLE; required checks and SonarQube Cloud Quality Gate/readbacks pass with zero PR issues, zero new violations, and `0.0%` new-code duplication. Status remains `fixed` pending authorized integration and resulting-master revalidation.

## Resulting-master disposition

PR #200 was protected-squash-merged from exact head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` at `2026-07-30T12:11:32Z` as
Parent master `13890da56ad19a105629243349f39ea8c084f396`. The master generator
and checker blobs equal the reviewed candidate; `make check-block-status-generator`,
the 12-test reliability suite, the 22-test bilingual suite, `git diff --check`,
and all 14 master workflows passed. Exact default-branch Sonar analysis
`c1f32224-aa05-4202-9b10-65c15165ff35` no longer reports
`AZ8d8_sBE36x1qGA4xhY`, and no vulnerability/bug is open in the two changed
`ci/tools` source paths.

The project-wide default-branch Quality Gate is nevertheless non-ignored
`ERROR` because of retained unrelated security-rating/hotspot conditions. The
security verification rule requires Quality Gate `OK` before promotion beyond
`fixed`; this P1 release-blocking finding is therefore not risk-accepted and
remains `fixed`, not `verified` or `closed`. The retained receipt is
`pr200-master-integration-13890da5.md`, SHA-256
`69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
