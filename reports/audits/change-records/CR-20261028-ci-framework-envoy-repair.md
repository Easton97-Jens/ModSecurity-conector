# Change Record: CR-20261028-ci-framework-envoy-repair

**Language:** English | [Deutsch](CR-20261028-ci-framework-envoy-repair.de.md)

Scoped Parent CI repair and reviewed Envoy dependency update. Local verification is complete; current-head hosted CI and Sonar verification remain pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-ci-framework-envoy-repair |
| Date (UTC) | 2026-10-28 |
| Base revision | `f5523da040bd6325b369269ada074be6ba069c4f` |

## Motivation and problem statement

The requested review covers updater run `40576069804`, dependency PRs [#423](https://github.com/Easton97-Jens/ModSecurity-conector/pull/423), [#424](https://github.com/Easton97-Jens/ModSecurity-conector/pull/424), [#425](https://github.com/Easton97-Jens/ModSecurity-conector/pull/425), and SonarQube findings.

The updater rejects the current Parent workflow because its validator still requires a removed `--nginx-archive` argument. The workflow now provisions runtime components and forwards the pinned NGINX tuple through `env -i` to the hosted inventory runner. Separately, the dependency PRs change an inventory-reviewed `go.mod` without updating its reviewed source digest, causing `ACTIVE_INVENTORY_REJECTED` before affected tests run. PR #423 already includes the dependency versions proposed separately in #424 and #425.

## Acceptance criteria

| Criterion | Evidence and status |
| --- | --- |
| Accept the current pinned NGINX handoff and reject missing, duplicate, replaced or commented forwarding | Focused positive regression and 28 forwarding variants passed locally; hosted updater rerun pending. |
| Carry the reviewed combined dependency update from #423 | `go.mod` and `go.sum` are byte-identical to PR #423 head `b55dafccd981654e43639d2038429eb2db637031`; Go build/tests require CI. |
| Rebind only reviewed changed inventory sources and preserve selection | Three explicit SHA256 bindings updated; native archive regenerated. Selection remains 100 cases / 80 executions; on-demand archive remains 1893 cases / 839 executions. Final inventory checks recorded below. |
| Assess Sonar evidence without weakening analysis | Existing failures identified; individual issue IDs and a new analysis are unavailable. No finding reduction or passing gate is claimed. |

## Implementation decision and rationale

Replace the obsolete archive-argument assertion with unique, exact shell forwarding checks for all six `NGINX_FIELDS` and the Parent-owned `NGINX_REQUIRE_PINNED_PROVENANCE` flag. Assignment matching is anchored to assignment-only line prefixes; a comment or unrelated command cannot satisfy the forwarding check. Existing candidate-data, Parent YAML/Python pin, provenance, revision-lock and read-only checks remain in place. The protected NGINX root-broker chain is unchanged.

Extend an existing drift regression instead of adding automatic test selectors. Integrate the two reviewed dependency files from #423: Envoy `v1.40.0`, gRPC `v1.84.0`, protobuf `v1.36.12`, and genproto RPC `v0.0.0-20260720211330-0afa2a65878a`. This includes the version content of #424/#425 without merging or closing those PRs. Update only the reviewed source bindings for the verifier, its test module and `go.mod`; regenerate the specialist archive through its native generator.

## Changed files

| Files | Change |
| --- | --- |
| `ci/tools/verify-framework-candidate-contract.py` | Validate the workflow's current runtime forwarding boundary. |
| `tests/test_verify_framework_candidate_contract.py` | Extend the existing drift test with 28 negative forwarding variants. |
| `connectors/envoy/ext_proc/go.mod`, `connectors/envoy/ext_proc/go.sum` | Reviewed combined update from PR #423. |
| `config/testing/active-cases.json` | Three reviewed source SHA256 bindings only; selection unchanged. |
| `reports/testing/test-selection-archive.generated.json` | Native regeneration after reviewed source rebinding. |
| `reports/audits/change-records/CR-20261028-ci-framework-envoy-repair.md`, `reports/audits/change-records/CR-20261028-ci-framework-envoy-repair.de.md` | Equivalent English/German change records. |

## Commands executed

Project shell commands use task-local RTK `v1.0.1` at `/workspace/scratch/5e0fa1c15f63/task-tools/rtk`, verified against the pinned upstream checksum. The commands below describe their relevant native payloads; task-owned environment and temporary paths are outside the checkout. No credentials were recorded.

| Command or procedure | Actual result |
| --- | --- |
| RTK-wrapped Python 3.11 reproduction loading `git show HEAD:ci/tools/verify-framework-candidate-contract.py` in memory | Exit 0: original verifier raises exactly `NGINX exact-head archive argument must contain exactly one supported assignment` against the current Parent fixture. |
| `python3 -m unittest tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_current_parent_contract_matches_the_candidate_without_writing tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_each_unprotected_handoff_layer_rejects_a_representative_drift` | Python 3.11: 2 tests passed, exit 0; coordinator independently passed the same focused tests on Python 3.12.14. |
| `rtk bypass python3 ci/tools/update-test-archive.py`, then `--check`; `rtk bypass python3 ci/tools/run-active-tests.py --check`; explicit comparison against base | All exit 0. Exactly three reviewed SHA256 slots differ; both complete execution arrays are unchanged (100/80 standard, 1893/839 on demand). |
| `rtk bypass env ON_DEMAND_TESTS=1 python3 -m unittest -v tests.test_verify_framework_candidate_contract` | Exit 0: 29 tests, initially 28 passed and 1 skipped. After initializing the locked Framework submodule, the skipped checked-out-common test separately passed (1/1, exit 0). |
| `rtk bypass git diff --check` | Exit 0 for the combined diff. |
| `rtk bypass make check-bilingual-docs`; `rtk bypass make check-doc-links` | Both exit 0. The initial link check failed solely because Framework was uninitialized; it passed after checking out the exact existing gitlink without changing it. |

The actual updater candidate `3a4f2281568139d94fda6b51dc2e07bb8fc06c67` was fetched read-only. Its `ci/lib/common.sh` has SHA256 `d42967158f7fe01a983ae0e27dca00ea02194362ec84275b16b87db10a703dee`. The original validator reproduced the exact hosted error against these bytes. The corrected CLI passed with `--candidate-sha 3a4f2281568139d94fda6b51dc2e07bb8fc06c67 --framework-common /workspace/scratch/5e0fa1c15f63/task-state/candidate-common.sh --expected-parent-framework-sha 99a7985c1be92a2297b1b59208f64df6768f2cbf --candidate-framework-root modules/ModSecurity-test-Framework`. This proves data admission with the unchanged Parent lock, not the complete hosted updater.

## Security impact

The changed verifier is a data-only CI admission boundary. It preserves fixed source pins and fail-closed behavior while checking the workflow's actual runtime handoff. Missing, duplicate, changed and commented forwarding are rejected without Parent writes. No candidate shell is executed. No Framework/MRTS source, protected broker, CI permissions, rule, Quality Gate, exclusion or suppression is changed.

The dependency update changes a security-relevant network/protocol library boundary. Static parity with the reviewed Dependabot update does not prove runtime compatibility or vulnerability remediation; pinned-toolchain CI remains required.

## Runtime evidence

No hosted runtime, connector matrix or I12 campaign was run. Local contract tests establish only validator behavior. Existing passing checks from other revisions do not qualify this change's future PR head.

## Known limitations

The cloud checkout lacks the original `/root/.agents/skills/goal-driven-execution/SKILL.md`, local `.codex/config.toml` and configured external work roots. Reversible setup used task-owned workspace paths outside the repository and a checksum-verified RTK executable. The original local environment was not reconstructed.

Repository-pinned Python 3.15 and Go 1.26.9 are unavailable. Local Python 3.11/3.12.14 tests are partial compatibility evidence only. Sonar CLI, the required `/usr/local/bin/sonar-with-env`, a compatible Sonar tool connection and container runtime are unavailable here. Selected Sonar plugin skills were inspected, but no direct issue list or new scan was obtained. The user-provided SonarCloud code page also returned CloudFront HTTP 403, including after one reload.

## Remaining risks

The observed master Sonar main and twelve native gates fail; individual issue IDs and complete current metrics were not available. Dependabot Sonar jobs fail with HTTP 403 before analysis. This change does not establish a reduction in findings or repair authentication. New PR CI may reveal separate existing failures or compatibility issues.

A successful local contract test does not prove that the updater's remaining isolation, candidate validation and PR publication steps succeed. Those need a fresh hosted run after integration.

## Checks not run and rationale

Pinned Python 3.15 validation, Go 1.26.9 compilation/tests, hosted updater execution, full connector runtime work and fresh Sonar analysis were not run because their required local toolchains/services are unavailable or their hosted integration has not happened. Documentation and combined-diff checks passed as recorded above. Historical I12 evidence work remains outside this scoped repair.

## Final diff and review status

The integrated diff was reviewed; focused/full affected contract checks, inventory admission, generated archive, documentation and whitespace checks passed. The local state is ready for a task-owned draft PR. The PR description must record subsequent delivery and current-head CI facts. No merge, old-PR closure, master change, passing Sonar gate or `verified_pr` status is claimed.
