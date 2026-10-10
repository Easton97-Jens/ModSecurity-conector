# Change Record: CR-20261010-nginx-ab-cognitive-followup

**Language:** English | [Deutsch](CR-20261010-nginx-ab-cognitive-followup.de.md)

Bounded behavior-preserving quality follow-up; no new runtime authorization.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-nginx-ab-cognitive-followup |
| Date (UTC) | 2026-10-10 |
| Base revision | `2686b07aaf64b0541d743b53970008bd86caa91f` |

## Motivation and problem statement

PR #396 analysis at `2686b07aaf64b0541d743b53970008bd86caa91f` reported exactly two `python:S3776` findings: `canonical_semantics` complexity 20/15 and `verify_binding` 16/15. This follow-up changes structure only.

## Acceptance criteria

Preserve intervention/rule/phase/transaction matching, first technical-fault priority, snapshot versus completion counters, exact exception messages and check order. Existing negative controls and added characterizations must pass before and after refactoring; fresh server-side Sonar confirmation remains required.

## Implementation decision and rationale

Extract `restore_intervention_decision` and `bound_append` without changing the original predicates or their order. Keep canonical fault and snapshot restoration in their original order. No suppression, threshold change, new evidence field or validator relaxation.

## Changed files

`ci/runtime/lifecycle/collect-no-crs-source.py`, `ci/lib/first_byte_binding.py`, `tests/test_no_crs_outcome_projection.py`, `tests/test_nginx_first_byte_binding.py`, and this EN/DE Change Record pair.

## Commands executed

Through `rtk proxy`, using shared Python 3.14.7 and `PARENT_TEST_FRAMEWORK_ROOT` pointing to the separate Framework worktree: `python -m unittest -v tests.test_no_crs_outcome_projection tests.test_nginx_first_byte_binding tests.test_collect_no_crs_source_helpers tests.test_collect_no_crs_source tests.test_native_first_byte_shell_environment`: 91 tests before and after, exit 0. An offline differential check against the frozen base verified 4800 canonical input/expectation combinations and 26 valid/invalid binding receipts, including exact returned values or exception type/message, exit 0. Native Change Record scaffold generation succeeded. Full native lint and final documentation checks are recorded in the external follow-up evidence; their results are not inferred from unit tests.

## Security impact

Behavior-preserving refactoring of security-relevant evidence consumers. Cross-transaction rejection, fail-closed ambiguity, file/hash/path/time checks and fault precedence remain unchanged. Framework and MRTS are unchanged.

## Runtime evidence

No runtime execution or new Runtime Evidence in this quality follow-up. Offline fixtures do not establish Full97 or Exact-Head PASS.

## Known limitations

No local scanner was authorized. Reduced complexity is a source-review expectation, not a claimed fresh Sonar result. Shared Python 3.14.7 does not reproduce Framework CI Python 3.14.8. Full `make lint` exited 2 in the isolated uninitialized worktree: the existing runtime-path checker sources the absent nested Framework `ci/lib/common.sh`, ignoring the supplied external `FRAMEWORK_ROOT`. `make check-bilingual-docs` and `make check-doc-links` each exited 2 for existing links into that absent submodule. No initialization, symlink or checker relaxation was performed. Archive-only Change Record check passed; the documented `tests.test_change_record tests.test_prepare_reviewed_framework_handoff` suite passed 39 tests, exit 0. An earlier operator invocation named a nonexistent documentation test module and exited 1; this is retained in the external log, not treated as a source failure. Integrated lint/docs rerun remains required in the populated worktree.

## Remaining risks

Fresh integrated-head CI/Sonar and coordinator review are still required. Historical Full97 failures and protected infrastructure limitations remain separate.

## Checks not run and rationale

No Full97, actual NGINX request, namespace/root operation, remote publication or scanner: explicitly outside this bounded worker task. No claim that green unit tests satisfy required runtime evidence.

## Final diff and review status

Minimal two-file production extraction plus four characterization methods and the generated EN/DE record pair. Worker made no commit/push; integration and final review belong to the coordinator.
