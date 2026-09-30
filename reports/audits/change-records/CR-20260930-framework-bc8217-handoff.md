# Change Record: Framework candidate bc8217d handoff

**Language:** English | [Deutsch](CR-20260930-framework-bc8217-handoff.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-framework-bc8217-handoff |
| Date (UTC) | 2026-09-30 |
| Base revision | `9bc87cbdb600b09c6edd02667a75b117a1f09eea` |

## Motivation and problem statement

[GitHub Actions job 109955091216](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36735191087/job/109955091216) rejects Framework candidate `bc8217d325809b9aba9a1d8c16964d71a01933ee` with `Framework common.sh differs from approved reviewed structure`. The candidate moves beyond the normalized structure digest approved in the Parent, so the submodule updater cannot publish a coherent handoff.

## Acceptance criteria

Pin the exact reviewed Framework candidate, update only its registered Parent projections and generated bilingual compiler guides, and set the verifier and regression-test digest to the independently calculated normalized candidate digest. Keep the source-field allowlist, candidate validation, workflow permissions and no-auto-merge behavior unchanged. Required CI and runtime checks must pass before merge.

## Implementation decision and rationale

Advance the Parent Framework gitlink from `0290a979ba4bc63a7abed175a53471367b385553` to `bc8217d325809b9aba9a1d8c16964d71a01933ee`. The candidate changes 17 `common.sh` assignment values but no shell control flow; ModSecurity v3 and HAProxy source fields are already registered, while PCRE2, OpenSSL, Node, CodeQL and Ruff remain intentionally subject to exact structural review. Set the approved normalized digest to `eed16dbe606c2770cf830cdb06884c7a5f68544e13c7f5ebb3106d3107e11fdc` in both verifier and test without broadening the mutable-field allowlist. Synchronize the six closed Parent targets, including HAProxy 3.2.23 to 3.2.25 and ModSecurity v3.0.16 to v3.0.17 (`1925753989ccce977cdaae417b55c9726c7cf02c`). Update the guide-generator constants and corresponding English/German outputs together.

## Changed files

- `modules/ModSecurity-test-Framework`
- `ci/tools/verify-framework-candidate-contract.py`
- `tests/test_verify_framework_candidate_contract.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/haproxy/htx-overlay/version-contract.json`
- `scripts/generate_compiler_guides.py`
- `tests/test_compiler_guides.py`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `tests/test_ci_security_workflows.py`
- `docs/build/compilers/libmodsecurity.md`
- `docs/build/compilers/libmodsecurity.de.md`
- `reports/audits/change-records/CR-20260930-framework-bc8217-handoff.md`
- `reports/audits/change-records/CR-20260930-framework-bc8217-handoff.de.md`

## Commands executed

The failed job log, current Parent and Framework revisions, candidate `common.sh`, registered synchronization targets and affected Parent files were inspected through the GitHub connection. The exact-value changes were checked in memory against the closed registries. No local repository command was run; no hosted check is claimed as passed at record creation.

## Security impact

This is an explicit approval of the exact Framework candidate, which also contains security-workflow and updater-policy changes. The Parent candidate verifier still treats `common.sh` as data and keeps its existing validation and path boundaries. No rule, permission, Quality Gate or mutable-field allowlist is relaxed. Review the Framework submodule diff and its release provenance before merge.

## Runtime evidence

No new connector runtime, ABI or WAF-behavior result is established by the pin and documentation update alone. Hosted tests and runtime checks for the PR head are required for those claims.

## Known limitations

The independent review checked the PCRE2, OpenSSL and Ruff asset digests and the CodeQL and ModSecurity tag commits; the HAProxy 3.2.25 archive digest was not independently fetched. The SonarQube MCP server was unavailable in this task environment.

## Remaining risks

The Framework candidate changes upstream dependency pins and security automation in addition to ModSecurity v3.0.17. Build, runtime and compatibility regressions remain possible until the PR's exact-head checks and human review complete.

## Checks not run and rationale

The repository-local secrets scan, official synchronizer and guide generator, focused unit tests, bilingual documentation checks, `git diff --check`, SonarQube analysis and runtime checks could not run in this projectless Windows task: SonarQube MCP did not start, the existing CLI was not authenticated, and no new credential authorization was granted. Do not treat static diff inspection as those checks.

## Final diff and review status

Deliver as a Draft PR against `master`. No merge or direct `master` write is authorized. Review the final diff and current-head hosted checks, then update this record with actual results before any merge.
