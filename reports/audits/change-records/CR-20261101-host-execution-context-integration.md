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

The `.codex` context and routing changes are independent of #348 and other PRs. The #348 dependency applies only to product/test compatibility of the selected Framework pin and final pair qualification; it is not a prerequisite for the context instructions themselves.

## Acceptance criteria

Draft delivery requires a scoped diff, consistent Framework gitlink and registered projections, current pin/provenance and documentation checks, secret scanning, and explicit dependency disclosure. Release readiness additionally requires the Apache contract, the committed Parent/Framework pair, artifact readmission, fresh NGINX host execution and launcher/cleanup evidence, and current exact-head CI/Sonar results. This task authorizes no merge.

## Implementation decision and rationale

The selected Framework pin is `b85280278310f4034af78149ac13671438965c7b`, the directly integrated successor of the requested `5ef57603a4933f18c988f1f9f32b93f478182440`, from [Framework PR #150](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/150). This deviation is required for a concrete reason: at `5ef57603a4933f18c988f1f9f32b93f478182440`, the specialist archive had not been regenerated after Framework PR #147. It contained 7946 rather than 7957 definitions and omitted the new preflight tests and blocked-sequence case. This caused Connector CI failures in Common, Quick, NGINX, and Scaffold; it was a task-related omission, separate from #348 incompatibility.

The archive at `b85280278310f4034af78149ac13671438965c7b` matches the owning generator byte for byte and contains 7957 definitions. The ten checked host-implementation, harness, test, and guide paths are byte-identical to the requested commit. The source inventory changes only one compiler-test binding digest; selectors and cases are unchanged. All five master workflows at the selected commit passed. Sonar confirmed that exact commit with analysis `b8bd5d2c-57a5-4bca-8086-36237aa1bcba` at `2026-11-01T20:24:20Z`, Quality Gate OK. This does not establish success at the new Connector head.

Framework PR #150 was integrated separately; this task changes or merges no Framework code. Generated Parent projections are updated only through `ci/tools/sync-framework-component-versions.py`. The separate Framework code-scanning PR, product changes from #348, and MRTS remain outside this diff.

## Changed files

- `.codex/context/index.md` routes native host context decisions to `.codex/context/security-runtime-preflight.md`; the latter links the maintained Framework guide.
- `.codex/inheritance-manifest.toml` refreshes only the two task-owned catalog hashes.
- `modules/ModSecurity-test-Framework` selects the integrated Framework commit; `project-versions.lock.json` and 22 registered `.github/workflows/` files carry the generated ordinary SHA projections. The 23 projection targets change only the registered old revision to the selected Framework revision: 54 workflow references and one lock reference. Protected and historical identities remain unchanged.
- This record and `CR-20261101-host-execution-context-integration.de.md` document the Parent delivery boundary.

The versioned durable guide is `modules/ModSecurity-test-Framework/docs/host-execution-context.md` and its `.de.md` companion. No connector product source or MRTS file changes belong to this diff.

## Commands executed

Fresh pin-candidate checks with Framework `b85280278310f4034af78149ac13671438965c7b` and starting Parent head `e03bc528c90c52974a5dc615da19070e33a72a86` passed without skips: 13 preflight tests (5.610 s), seven integration tests (0.732 s), and nine fixture-based pin/provenance contract tests (14.413 s). The native projection check returned `changed=[]`; the candidate contract verified the actual and expected Framework revision. `make check-active-inventory` and the separate archive check passed with exactly 7957 definitions. This verifies the working-tree candidate before its follow-up commit, not its still-unknown final head.

The fresh Apache contract failed with exit 2 at `apache_response_protocol`; explicit Common C17 compilation with `ON_DEMAND_TESTS=1` also failed with exit 2 at missing protocol/late-intervention APIs, including `msconnector_late_intervention_context`, `protocol_kind_parse`, and `STREAM_RESET`. Expectations were not changed. The Traefik contract additionally needs `Summary.ResponseIncomplete` from the separate product work.

All local commands use RTK and the prescribed Framework interpreter. Task-scoped secret scanning passed before source access with the existing Framework configuration, without new exceptions or configuration changes. The final changed-file scan of the b852 candidate and repeated documentation checks are performed after record edits finish; their actual results and subsequent PR-head checks belong to external evidence and the PR description. Private reports and raw logs are not committed.

The following transcription factors the identical observed RTK/environment prefix into `checked`. Path aliases name the selected Parent worktree, its Framework root, the prescribed interpreter, and the approved external task root. `CONNECTOR_REVISION` is the starting head before the pin follow-up commit. `framework-common-b852.sh` was extracted from the selected Framework commit.

```sh
checked() {
  rtk bypass env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=$TASK_ROOT/private TMPDIR=$TASK_ROOT/tests PYTHONPATH=$FRAMEWORK_ROOT:$FRAMEWORK_ROOT/connector_suite TEST_ROOT=$FRAMEWORK_ROOT FRAMEWORK_ROOT=$FRAMEWORK_ROOT FRAMEWORK_REVISION=b85280278310f4034af78149ac13671438965c7b CONNECTOR_ROOT=$PARENT_ROOT CONNECTOR_REVISION=e03bc528c90c52974a5dc615da19070e33a72a86 CONNECTOR_TEST_PROFILE=h1 CONNECTOR_TEST_OUTPUT_ROOT=$TASK_ROOT/tests EXECUTION_CONTEXT_TEST_ROOT=$TASK_ROOT/tests "$@"
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
checked $FRAMEWORK_PYTHON -P ci/tools/sync-framework-component-versions.py --check --framework-common $TASK_ROOT/private/framework-common-b852.sh --framework-sha b85280278310f4034af78149ac13671438965c7b
checked $FRAMEWORK_PYTHON -P ci/tools/verify-framework-candidate-contract.py --repo-root $PARENT_ROOT --candidate-sha b85280278310f4034af78149ac13671438965c7b --framework-common $TASK_ROOT/private/framework-common-b852.sh --candidate-framework-root $FRAMEWORK_ROOT --expected-parent-framework-sha b85280278310f4034af78149ac13671438965c7b
checked make -C $PARENT_ROOT check-active-inventory PYTHON=$FRAMEWORK_PYTHON BUILD_ROOT=$TASK_ROOT/private/b852-inventory TMP_ROOT=$TASK_ROOT/tests LOG_ROOT=$TASK_ROOT/private/b852-inventory-logs
checked $FRAMEWORK_PYTHON -P $FRAMEWORK_ROOT/connector_suite/modsecurity_connector_ci/tools/update-test-archive.py --check
```

## Security impact

The routing requires a fresh preflight inside the actual host launcher/namespace before identity-dependent work. It preserves UID/GID transitions, private UDS/path checks, root-master and non-root-worker requirements, protected broker admission, and cleanup checks. Preflight PASS proves prerequisites only. No authorization, guard, test expectation, CI condition, or Quality Gate is weakened.

## Runtime evidence

The fresh preflight suite at the selected b852 candidate included a separate daemon-launcher probe. This checks the launcher execution context, not the final committed product pair. No fresh final-pair NGINX host proof is claimed. Required evidence is master UID/GID 0, worker 65534, readiness, HTTP `200→403→200`, rule/transaction correlation, and verified process/listener cleanup. A separate non-root-launcher probe must also be fresh. Envoy has no host-execution proof in this change.

## Known limitations

The additional migration-map check fails for this pair: 12 Envoy Makefile caller positions and nine corresponding case links differ from the Framework map generated against external #348 input `b43faa78`. The Parent Makefile is unchanged from base `2abad408`; inventory, archive, source bindings and counts agree. This independent input-position mismatch remains failed and is not repaired by importing product changes or rewriting Framework projections in Parent.

The current base also lacks Traefik contract field `Summary.ResponseIncomplete`, as well as the Common protocol/late-intervention-context APIs and Apache `apache_response_protocol` required by the selected Framework. PR #348 is a separate, unmerged Draft and is an integration dependency. After its separate integration, merge current `master` into this branch and repeat qualification on the final committed pair. Draft publication does not establish compatibility.

## Remaining risks

Previously reused NGINX artifacts need matching product-source, build, and artifact evidence against the final product revision; old runtime evidence cannot substitute. Five independent baseline inheritance drifts remain unchanged: `PARENT-CHANGE-WORKFLOW`, `PARENT-CONNECTOR-MATRIX`, `PARENT-DEFINITION-OF-DONE`, `PARENT-PHASE4-TARGET-SEMANTICS`, and `PARENT-TESTING-AND-EVIDENCE`. The two refreshed catalog entries are not Framework child inheritance pins. A separate pre-existing Framework child `PARENT-COMMAND-EXECUTION` inheritance mismatch is also preserved; it is distinct from the five stale Parent catalog entries.

## Checks not run and rationale

The complete local revision reader is blocked by the uninitialized MRTS checkout. This task neither initializes nor changes MRTS. Agreement of static committed pins does not replace that complete materialized revision chain.

The successful Apache contract, complete committed-pair qualification, NGINX artifact readmission, fresh NGINX sequence, separate launcher probe, verified cleanup, and final PR-head CI/Sonar qualification remain outstanding. Missing product APIs block release readiness. No Envoy host run was performed. The eventual merge must retain zero new Sonar issues including accepted issues and zero new hotspots; this Draft does not claim that final result.

## Final diff and review status

[Connector PR #436](https://github.com/Easton97-Jens/ModSecurity-conector/pull/436) is already published as a separate Draft. The justified pin correction is delivered as an ordinary follow-up commit. While #348 is absent, the Draft remains unqualified for release. The isolated worktree preserves the original checkout's local changes; only context, pin/projection, and paired record changes are selected. No successful current PR-head CI/Sonar results or merge outcome are claimed. This task authorizes no merge.
