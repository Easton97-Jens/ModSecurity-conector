# Finding FND-SONAR-0023: Native ModSecurity oracle result writer exceeds Sonar parameter-count threshold

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / security relevant | no / no |
| Sonar inventory | `c:S107`, `AZ7b3dgOcO69wzd-_jHt` |

## Summary, behavior, and impact

The inventory-bound `c:S107` code smell reported the eight-argument
`write_result` function in `ci/tools/native_modsecurity_oracle.c`. It is a
maintainability finding, not a validated attacker-controlled security path.
The task patch groups coherent result data in private `struct result_context`
and uses that context for result serialization without changing the public
CLI, JSON fields/order, reason strings, or exit-state contract.

Protected-squash PR #200 from exact head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` produced Parent master
`13890da56ad19a105629243349f39ea8c084f396`. The native Oracle and focused
reliability-test blobs equal the reviewed candidate; all 14 master workflows
passed, and default-branch analysis
`c1f32224-aa05-4202-9b10-65c15165ff35` no longer reports
`AZ7b3dgOcO69wzd-_jHt`. The independent non-ignored global Quality Gate
`ERROR` is not an acceptance criterion for this non-security finding, so its
status is `verified`, not `closed`.

## Scope, reproduction, and evidence

- Affected files/symbols: `ci/tools/native_modsecurity_oracle.c`,
  `tests/test_sonar_reliability_contract.py`, `write_result`, and
  `struct result_context`.
- Preconditions: SonarQube Cloud analyzes the inventory revision containing
  the eight-parameter definition; the Oracle is compiled with supported C17
  toolchains.
- Reproduce by reviewing `c:S107` key `AZ7b3dgOcO69wzd-_jHt`, compiling the
  patch with GCC and Clang under `-std=c17 -Wall -Wextra -Werror`, and running
  the focused source contract plus real-libmodsecurity 200/403/setup-error
  controls.

Run ID: `ci-tools-sonar-remediation-20260730`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `.codex/plans/ci-tools-sonar-remediation.md` | `0029f0724d663e1d84408d56af69e71724a79f79dbb24c862aa0f628ffc0852c` | Records `AZ7b3dgOcO69wzd-_jHt` and the compact result-context design. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/report.md` | `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7` | C17 GCC/Clang and real-libmodsecurity 200/403/setup-error controls pass; phase and result semantics are retained. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/runtime/native-final-gcc-allow-result.json` | `ad1ed3ba88d88b8eb03683083a103461d2efb28e46135ace7365d297eaa80843` | Real LibModSecurity 3.0.14 allowed control returns pass with expected/actual status `200`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-exact-head-verification.md` | `42ba7a4ff8ff0172997a935f04a7fdf560b7b6ce9c70daab97fa24e69024f3be` | Exact Draft-PR #200 head is OPEN/Draft/CLEAN and MERGEABLE; required checks and SonarQube Cloud Quality Gate/readbacks pass with zero PR issues, including original `c:S107` key `AZ7b3dgOcO69wzd-_jHt`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-66db7e3f-exact-head-verification.md` | `33cc911a5ee393fb44906c3e4dac76634df86d99fe07b3e105be9962148c840a` | Refreshed Draft-PR #200 head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` against master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` is OPEN/Draft/CLEAN and MERGEABLE; required checks and SonarQube Cloud Quality Gate/readbacks pass with zero PR issues, including original `c:S107` key `AZ7b3dgOcO69wzd-_jHt`. |

## Root cause, remediation, and controls

`write_result` mixed a stable output representation with too many independent
result values. The repair retains private request/result contexts, passes the
result context plus status/reason to the writer, and preserves the existing
serialization semantics. No Sonar rule, Quality Gate, exclusion, `NOSONAR`,
or suppression changes.

Acceptance is demonstrated on exact resulting master: default-branch analysis
no longer reports the original `c:S107` key, public JSON/CLI behavior is
preserved, GCC/Clang warning-as-error builds and real-library controls pass,
and hosted checks completed without bypass. Regression:
`tests/test_sonar_reliability_contract.py`. Legitimate controls: real 200,
403, and setup-error result paths.

## Dependencies, blockers, related findings, and residual risk

Exact Draft-PR and resulting-master hosted analyses are retained. Integration
and resulting-master revalidation are complete; there is no technical blocker
for this verified finding. `FND-SONAR-0016` is aggregate Sonar context;
`FND-SONAR-0024` is the separate complexity cause; `FND-PARENT-0036` is the
distinct native lifetime finding. No risk acceptance was made; the protected
master integration is recorded as evidence.

## History

- `2026-07-30T10:46:48Z`: allocated as the distinct `c:S107` source boundary;
  local compiler, source-contract, and real-libmodsecurity controls pass,
  hosted exact-head Sonar verification was pending at that time.
- `2026-07-30T11:07:21Z`: exact Draft-PR #200 head `2bc97ac058725fdba6a36ad93307487c160b1f05` passed
  required GitHub checks and SonarQube Cloud Quality Gate/readbacks. Original
  `c:S107` key `AZ7b3dgOcO69wzd-_jHt` is absent from the PR issue query; status
  remains `fixed` pending authorized integration and resulting-master
  verification.
- `2026-07-30T11:33:48Z`: after master advanced to `726322b17d6423c7f9e3bba0e6affc051dbf94cd`, refreshed exact Draft-PR #200 head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` passed required GitHub checks and SonarQube Cloud Quality Gate/readbacks. Original `c:S107` key `AZ7b3dgOcO69wzd-_jHt` is absent from the zero-issue PR query; status remains `fixed` pending authorized integration and resulting-master verification.

## Resulting-master disposition

Protected-squash PR #200 exact head `5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` produced Parent master
`13890da56ad19a105629243349f39ea8c084f396` at `2026-07-30T12:11:32Z`. The native Oracle and focused
reliability-test blobs equal the reviewed candidate; its direct semantic,
compiler, and real-LibModSecurity controls therefore apply to this exact source.
All 14 master workflows passed, and default-branch analysis `c1f32224-aa05-4202-9b10-65c15165ff35`
no longer reports `AZ7b3dgOcO69wzd-_jHt`.

The project-wide Quality Gate remains non-ignored `ERROR` for retained
unrelated conditions, but that is not an acceptance criterion for this
non-security maintainability finding. The original key is absent on resulting
master with preserved controls, so the status advances to `verified`, not
`closed`. Receipt SHA-256: `69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
