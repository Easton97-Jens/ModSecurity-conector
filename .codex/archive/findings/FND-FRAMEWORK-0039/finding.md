# FND-FRAMEWORK-0039 — Python maintenance candidate output accepted a caller-selected filesystem path

## Identity

| Field | Value |
| --- | --- |
| Category | security_validated |
| Repository / ownership | framework / framework |
| Priority / severity | P1 / high |
| Confidence / status | validated / fixed |
| Release blocker | yes |

## Evidence and impact

Exact-head SonarCloud analysis of Framework Draft PR #39 reports open issue
`AZ-BJmyc1Sm1F-_jUkdR` (`pythonsecurity:S8707`) at
`ci/tools/update-python-version.py:390`. The Quality Gate is failed solely
because Security on New Code is C. The old CLI accepted a path argument for
`--write-candidate-file` and passed it to `os.open`, after a containment check.
That still leaves a caller-selected path construction boundary at a filesystem
sink.

The required invariant is stronger: candidate validation may create only the
fixed direct child `$RUNNER_TEMP/framework-python-3.13-candidate`. It must
remain absent/non-symlink before exclusive creation, while the legitimate
candidate setup action retains the same fixed input path. No unsafe write is
performed as a proof; hosted static analysis is the concrete trigger.

## Remediation and validation

The narrow repair removes the value-bearing CLI path option, derives the fixed
candidate filename from validated `RUNNER_TEMP`, retains exclusive creation,
and adds a regression that an extra destination is rejected. It must preserve
the current schedule/manual gates, independent resolution, version contract,
and no-update/no-write behavior. Focused tests, workflow lint, full Framework
lint, a source-aware security review, and the sealed 11-file follow-up
security-diff scan now pass. The finding is locally `fixed`; a fresh
exact-current-head SonarCloud analysis must still close the original S8707
issue and pass the PR Quality Gate before the delivery can be verified.

## History

- 2026-07-20T20:10:08Z — hosted PR #39 analysis validated the S8707 finding;
  it is a release blocker until remediation and exact-head reanalysis pass.
- 2026-07-20T21:12:33Z — the CLI was changed to a no-value flag, and the
  updater now derives only `$RUNNER_TEMP/framework-python-3.13-candidate`.
  The extra-destination regression, legitimate candidate materialization,
  focused and native checks, and sealed follow-up scan passed. Hosted exact-head
  SonarCloud reanalysis remains pending; no merge, Parent gitlink update, or
  MRTS action is authorized.
