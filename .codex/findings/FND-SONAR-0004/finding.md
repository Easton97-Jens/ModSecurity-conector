# FND-SONAR-0004 — SonarQube Cloud project analyzes read-only Framework and MRTS trees

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-SONAR-0004` |
| Category | `sonarqube_finding` |
| Repository | `parent` |
| Ownership | `sonarqube_configuration` |
| Priority | `P1` |
| Severity | `not_applicable` |
| Confidence | `confirmed` |
| Status | `blocked` |
| Release blocker | `true` |
| Security relevant | `true` |

## Summary

The current Parent SonarQube Cloud project includes 341 Framework-exclusive and
17 MRTS issue records even though those nested repositories are read-only and
outside this task's ownership boundary.

## Observed and expected behavior

The superseding retained paginated baseline for remote Parent SHA
`aabde81a9a315bf3e494e595ab0399357c596f9c` contains 358 records beneath
`modules/ModSecurity-test-Framework/`: 337 open and 4 closed
Framework-exclusive records, plus 17 open MRTS-subtree records. Public
effective settings confirm `sonar.autoscan.enabled=true`; the Parent has no
versioned scanner configuration. No Parent-owned source fix can remediate
these nested-source records.

A Parent Sonar analysis must report only Parent-owned source paths. Framework
and MRTS paths must have zero analyzed issue records without suppressing,
disabling, or broadly excluding Parent source rules.

## Impact, scope, and preconditions

The current analysis cannot be reconciled entirely through authorized Parent
source changes, and nested security/quality records can distort project-wide
metrics and gate triage. This requires Automatic Analysis of the Parent
checkout and the task's read-only Framework/MRTS boundary; neither nested
repository was read or modified.

Affected paths:

- `modules/ModSecurity-test-Framework/`
- `modules/ModSecurity-test-Framework/tools/MRTS/`

## Evidence and reproduction

Retained evidence:

- Run: `20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260719T131708Z-sonarcloud-parent-remediation-baseline-bbce9d6b/evidence/sonar-baseline-issues.json`
- SHA-256: `1d03d14de35cd0ec0bb5e26854534e1f1ec4694ed3e917ac220e65c0ed5ef25f`
- Producer: RTK-proxied public SonarQube Cloud V1 issue pagination followed by
  component-prefix accounting; working directory
  `/root/git/ModSecurity-conector`; exit code `0`; observed
  `2026-07-19T13:18:35Z`; retention `retained_task_evidence`.
- Run: `20260719T134711Z-sonarcloud-parent-remediation-current-3de21a87`
- Artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T134711Z-sonarcloud-parent-remediation-current-3de21a87/evidence/sonar-baseline-issues.json`
- SHA-256: `b219bff16466e443c11733e335ae8b9bf9b63aac2cf556bd5b0d9fd8d3e8175c`
- Producer: RTK-proxied public SonarQube Cloud V1 exact-current issue
  pagination followed by component-prefix accounting; working directory
  `/root/git/ModSecurity-conector`; exit code `0`; analysis observed
  `2026-07-19T13:20:27Z`; retention `retained_task_evidence`.

Reproduce by counting components in the retained baseline beginning with
`Easton97-Jens_ModSecurity-conector:modules/ModSecurity-test-Framework/` and
its `/tools/MRTS/` subtree, then read the public effective project setting
`sonar.autoscan.enabled`.

## Root cause and proposed remediation

The project scope is contaminated by nested Framework/MRTS paths. Public
effective setting `sonar.autoscan.enabled=true` and the lack of Parent scanner
configuration support Automatic Analysis as the active mechanism, but this
task has no project-administration credential or authority to change that
external setting.

An authorized SonarQube Cloud administrator must configure a narrow ownership
boundary that excludes only these two nested repository trees, or approve a
CI-managed scanner with an explicit Parent-only source scope. The solution
must not use `NOSONAR`, rule disabling, suppressions, or broad Parent-source
exclusions.

## Acceptance criteria and validation

1. A fresh SHA-bound analysis has zero components and issue records below the
   Framework and MRTS paths.
2. Parent source remains analyzed and all Parent rules and gate controls remain
   active.
3. The scope change and exact resulting analysis revision are retained without
   secrets.

Validation must paginate the post-change issues, compare Parent counts and
gate conditions, and prove that no prohibited suppression or broad exclusion
was introduced. A representative Parent component is the legitimate control.

## Dependencies, blockers, related records, and residual risk

Dependency and blocker: SonarQube Cloud project-administration access or an
approved CI-scanner migration decision. Related record:
`FND-SONAR-0001`.

Residual risk: project-wide quality and security counts include nested findings
that this Parent-only task is forbidden to modify. No user risk acceptance
exists.

## History

- `2026-07-19T13:30:00Z`: Created from the paginated current Sonar baseline
  after deduplication against `FND-SONAR-0001`. No nested source or project
  setting was changed.
- `2026-07-19T14:09:34Z`: Superseding current-scope baseline revalidated —
  remote Parent SHA `aabde81a9a315bf3e494e595ab0399357c596f9c` retains the
  exact same accounting: 337 open and 4 closed Framework-exclusive records,
  plus 17 open MRTS-subtree records. No nested source, project setting,
  suppression, rule, or risk-acceptance mutation was performed; the authorized
  external scope correction remains blocked.
