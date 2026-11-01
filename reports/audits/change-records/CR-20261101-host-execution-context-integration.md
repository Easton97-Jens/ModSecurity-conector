# Change Record: CR-20261101-host-execution-context-integration

**Language:** English | [Deutsch](CR-20261101-host-execution-context-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261101-host-execution-context-integration |
| Date (UTC) | 2026-11-01 |
| Base revision | `2abad408cae7e5a103d12a9a9e432129bfe0468f` |

## Motivation and problem statement

Deliver the prepared Parent host-execution-context routing and the integrated Framework preflight through a separate Connector Draft PR. Missing protocol APIs in the current Parent source prevent release qualification. Preserve that dependency rather than importing product changes from [PR #348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348).

## Acceptance criteria

Draft delivery requires a scoped diff, consistent Framework gitlink and registered projections, current pin/provenance and documentation checks, secret scanning, and explicit dependency disclosure. Release readiness additionally requires the Apache contract, the committed Parent/Framework pair, artifact readmission, fresh NGINX host execution and launcher/cleanup evidence, and current exact-head CI/Sonar results. This task authorizes no merge.

## Implementation decision and rationale

Select the integrated Framework commit `5ef57603a4933f18c988f1f9f32b93f478182440`, delivered by [Framework PR #147](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/147), rather than a moving branch. Its tested PR head was `20f8d5bc36614d21dae1635a08c9206fc09da96b`; all five merge-commit master workflows passed. That PR head had Quality Gate OK, zero new issues including accepted issues, and zero new security hotspots. These historical Framework results do not qualify the new Connector head. Update generated projections only through `ci/tools/sync-framework-component-versions.py`. Keep the separate Framework code-scanning PR, #348, and MRTS outside this change.

## Changed files

- `.codex/context/index.md` routes native host context decisions to `.codex/context/security-runtime-preflight.md`; the latter links the maintained Framework guide.
- `.codex/inheritance-manifest.toml` refreshes only the two task-owned catalog hashes.
- `modules/ModSecurity-test-Framework` selects the integrated Framework commit; `project-versions.lock.json` and 22 registered `.github/workflows/` files carry the generated ordinary SHA projections. The 23 projection targets change only the registered old revision to the selected Framework revision: 54 workflow references and one lock reference. Protected and historical identities remain unchanged.
- This record and `CR-20261101-host-execution-context-integration.de.md` document the Parent delivery boundary.

The versioned durable guide is `modules/ModSecurity-test-Framework/docs/host-execution-context.md` and its `.de.md` companion. No connector product source or MRTS file changes belong to this diff.

## Commands executed

Fresh checks on working-tree base `2abad408cae7e5a103d12a9a9e432129bfe0468f` with Framework `5ef57603a4933f18c988f1f9f32b93f478182440` passed: 13 preflight tests (4.609 s), seven integration tests (0.681 s), and nine pin/provenance contract tests (13.577 s), without skips. The native projection check returned `changed=[]`; the candidate contract verified the actual and expected Framework revision. The Apache contract failed with exit 2 because its inherited Phase 3 assertion requires the missing negotiated-protocol helper. The explicit `ON_DEMAND_TESTS=1` Common C17 API compilation also failed with exit 2: unknown `msconnector_late_intervention_context`, missing `protocol_kind_parse`/`name`/`is_multiplexed`/`context_init`/`resolve_for_context`, and undeclared HTTP enums and `STREAM_RESET`. These are compatibility blockers, not corrected expectations. These working-tree checks are not final committed-head qualification.

All local commands use RTK and the prescribed Framework interpreter; source access follows the repository secret-scanning protocol. Private reports, exact command receipts, and raw logs remain outside Git. Source-scoped secret scanning passed before access using the existing Framework configuration, without adding or modifying scanner exceptions or configuration. Gitleaks 8.30.1 also passed on all 28 changed regular files before staging. The scanned-byte manifest is retained externally and must match staged blobs. Native bilingual, path/link and Change Record structure checks passed. Actual PR-head CI/Sonar results remain separate from this local evidence.

The following transcription factors the identical observed RTK/environment prefix into `checked`; path aliases name the selected Parent worktree, its Framework root, the prescribed interpreter, and the approved external task root. It preserves the executed selectors and flags. `CONNECTOR_REVISION` identifies the working-tree base, not a future delivery head. The admitted `framework-common-merged.sh` was extracted from the selected Framework commit. The Common default target exited 0 for its selected default scenarios; it did not execute the full missing-API compiler check.

```sh
checked() {
  rtk bypass env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=$TASK_ROOT/private TMPDIR=$TASK_ROOT/tests PYTHONPATH=$FRAMEWORK_ROOT:$FRAMEWORK_ROOT/connector_suite TEST_ROOT=$FRAMEWORK_ROOT FRAMEWORK_ROOT=$FRAMEWORK_ROOT FRAMEWORK_REVISION=5ef57603a4933f18c988f1f9f32b93f478182440 CONNECTOR_ROOT=$PARENT_ROOT CONNECTOR_REVISION=2abad408cae7e5a103d12a9a9e432129bfe0468f CONNECTOR_TEST_PROFILE=h1 CONNECTOR_TEST_OUTPUT_ROOT=$TASK_ROOT/tests EXECUTION_CONTEXT_TEST_ROOT=$TASK_ROOT/tests "$@"
}
checked $FRAMEWORK_PYTHON -P -m unittest -v \
    modsecurity_connector_tests.test_execution_context_preflight \
    modsecurity_connector_tests.test_hostruntime_preflight.HostruntimePreflightTests.test_missing_binary_is_blocked \
    modsecurity_connector_tests.test_hostruntime_preflight.HostruntimePreflightTests.test_incomplete_identity_evidence_cannot_pass \
    modsecurity_connector_tests.test_hostruntime_preflight.HostruntimePreflightTests.test_valid_lock_drives_version_and_safe_artifact_metadata
checked $FRAMEWORK_PYTHON -P -m unittest -v \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_harness_validates_authority_before_root_mutation_sinks \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_worker_path_authority_precedes_the_non_root_handoff \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_worker_preflight_uses_the_rendered_nginx_group \
    modsecurity_connector_tests.test_nginx_harness_path_authority.NginxHarnessPathAuthorityTests.test_worker_helpers_use_only_fixed_runuser_capabilities \
    modsecurity_connector_tests.test_nginx_sequence_driver_phases.SequenceDriverPhasesTests.test_success_receipts_are_raw_bound_without_canonical_promotion \
    modsecurity_connector_tests.test_nginx_sequence_driver_phases.SequenceDriverPhasesTests.test_config_rejection_never_starts_client_and_still_attempts_cleanup \
    modsecurity_connector_tests.test_nginx_sequence_driver_phases.SequenceDriverPhasesTests.test_blocked_context_precedes_projection_configtest_and_child
checked $FRAMEWORK_PYTHON -P -m unittest -v \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_exact_repository_chain_is_accepted \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_uncommitted_lock_rewrite_is_rejected_even_when_semantically_identical \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_lock_cannot_override_parent_framework_gitlink \
    modsecurity_connector_tests.test_framework_revision_pins.RevisionProvenanceTests.test_framework_and_mrts_materialized_head_mismatches_are_rejected \
    modsecurity_connector_tests.test_update_framework_versions.SyncFrameworkVersionsTests.test_framework_sha_projection_updates_only_revision_lock \
    modsecurity_connector_tests.test_update_framework_versions.SyncFrameworkVersionsTests.test_framework_sha_projection_rejects_malformed_lock_without_writes \
    modsecurity_connector_tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_current_parent_contract_matches_the_candidate_without_writing \
    modsecurity_connector_tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_candidate_mrts_gitlink_must_match_locked_selection \
    modsecurity_connector_tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_each_unprotected_handoff_layer_rejects_a_representative_drift
checked $FRAMEWORK_PYTHON -P ci/tools/sync-framework-component-versions.py --check --framework-common $TASK_ROOT/private/framework-common-merged.sh --framework-sha 5ef57603a4933f18c988f1f9f32b93f478182440
checked $FRAMEWORK_PYTHON -P ci/tools/verify-framework-candidate-contract.py --repo-root $PARENT_ROOT --candidate-sha 5ef57603a4933f18c988f1f9f32b93f478182440 --framework-common $TASK_ROOT/private/framework-common-merged.sh --candidate-framework-root $FRAMEWORK_ROOT --expected-parent-framework-sha 5ef57603a4933f18c988f1f9f32b93f478182440
checked make -C $PARENT_ROOT check-apache-common-adoption PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/build TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/logs
checked make -C $PARENT_ROOT check-common-helpers-c17 PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/common-build TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/common-logs
checked make -C $PARENT_ROOT check-common-helpers-c17 ON_DEMAND_TESTS=1 PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/common-api-build TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/common-api-logs
```

## Security impact

The routing requires a fresh preflight inside the actual host launcher/namespace before identity-dependent work. It preserves UID/GID transitions, private UDS/path checks, root-master and non-root-worker requirements, protected broker admission, and cleanup checks. Preflight PASS proves prerequisites only. No authorization, guard, test expectation, CI condition, or Quality Gate is weakened.

## Runtime evidence

The fresh preflight suite included a separate daemon-launcher probe. This checks the launcher execution context, not the final committed product pair. No fresh final-pair NGINX host proof is claimed. Required evidence is master UID/GID 0, worker 65534, readiness, HTTP `200→403→200`, rule/transaction correlation, and verified process/listener cleanup. A separate non-root-launcher probe must also be fresh. Envoy has no host-execution proof in this change.

## Known limitations

The current base lacks the Common protocol/late-intervention-context APIs and Apache `apache_response_protocol` required by the selected Framework. PR #348 is a separate, unmerged Draft and is an integration dependency. After its separate integration, merge current `master` into this branch and repeat qualification on the final committed pair. Draft publication does not establish compatibility.

## Remaining risks

Previously reused NGINX artifacts need matching product-source, build, and artifact evidence against the final product revision; old runtime evidence cannot substitute. Five independent baseline inheritance drifts remain unchanged: `PARENT-CHANGE-WORKFLOW`, `PARENT-CONNECTOR-MATRIX`, `PARENT-DEFINITION-OF-DONE`, `PARENT-PHASE4-TARGET-SEMANTICS`, and `PARENT-TESTING-AND-EVIDENCE`. The two refreshed catalog entries are not Framework child inheritance pins. A separate pre-existing Framework child `PARENT-COMMAND-EXECUTION` inheritance mismatch is also preserved; it is distinct from the five stale Parent catalog entries.

## Checks not run and rationale

The successful Apache contract, complete committed-pair qualification, NGINX artifact readmission, fresh NGINX sequence, separate launcher probe, verified cleanup, and final PR-head CI/Sonar qualification remain outstanding. Missing product APIs block release readiness. No Envoy host run was performed. The eventual merge must retain zero new Sonar issues including accepted issues and zero new hotspots; this Draft does not claim that final result.

## Final diff and review status

The isolated worktree preserves the original checkout's local changes. Only the task-owned context, pin/projection, and paired record changes are selected. The PR is intended to remain Draft while #348 is absent; no Connector delivery SHA, successful current-head CI/Sonar result, or merge outcome is asserted here.
