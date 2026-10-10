# Change Record: CR-20261010-nginx-intervention-outcome-projection

**Language:** English | [Deutsch](CR-20261010-nginx-intervention-outcome-projection.de.md)

Focused collector repair; fresh runtime confirmation remains pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-nginx-intervention-outcome-projection |
| Date (UTC) | 2026-10-10 |
| Base revision | `dca17fd5690c2ec2b8806024d1061744db8c3ad8` |

## Motivation and problem statement

The historical Full97 on the base revision had 80 Case-PASS, nine FAIL and eight NOT_EXECUTED. Completion/cleanup defaults overwrote observed intervention fields.

## Acceptance criteria

Keep the matching transaction/rule/phase-bound decision; reject ambiguous identities and retain genuine technical faults.

## Implementation decision and rationale

Intervention decision fields are projected separately from later lifecycle state. Unmatched/conflicting interventions cannot supply decision values. The first evidenced technical error remains authoritative.

## Changed files

`ci/runtime/lifecycle/collect-no-crs-source.py`, `tests/test_no_crs_outcome_projection.py`, this EN/DE record pair.

## Commands executed

`rtk proxy env PYTHONNOUSERSITE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.test_nginx_first_byte_binding tests.test_no_crs_outcome_projection tests.test_collect_no_crs_source_helpers tests.test_collect_no_crs_source tests.test_native_first_byte_shell_environment`: 86 tests passed, exit 0. Initial A RED exit 1 reproduced 403→0 and cross-TX/priority gaps; one invalid allow-action fixture was corrected.

## Security impact

No validator, privacy allowlist, Required scope or product semantics weakened. No response payload is retained in the receipt. MRTS unchanged.

## Runtime evidence

Historical R13 is unchanged. Offline fixtures are not a new runtime run. Fresh real bounded focus and integrated-SHA evidence remain coordinator-owned and are not yet claimed here.

## Known limitations

Unit regressions are not Full97 or protected Exact-Head proof.

## Remaining risks

Fresh Phase-3 deny/redirect and Phase-4 Safe/Strict focus must verify decisions, roles and cleanup.

## Checks not run and rationale

New Full97 is not authorized. Protected/admin operations are out of scope. Full lint, fresh CI/Sonar and publication are not claimed by this worker.

## Final diff and review status

Focused source changes prepared for independent review and separate commit. No commit, push, merge, retarget or Undraft performed by this worker.
