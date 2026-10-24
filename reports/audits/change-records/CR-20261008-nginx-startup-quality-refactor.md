# Change Record: CR-20261008-nginx-startup-quality-refactor

**Language:** English | [Deutsch](CR-20261008-nginx-startup-quality-refactor.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-startup-quality-refactor |
| Date (UTC) | 2026-10-08 |
| Base revision | `54877d2824c402a3912c71755bac7fcc884da5f4` |

## Motivation and problem statement

Seven current Parent Sonar findings concern duplicated literals and cognitive complexity in strict startup and receipt code. The eighth configtest-driver finding is coordinator-owned.

## Acceptance criteria

Preserve exact operations, failures, native transaction/rule binding, owned PIDFD cleanup, capture bounds and serialized artifact bytes.

## Implementation decision and rationale

Extract narrow helpers for startup captures, owned-role observation, graceful master shutdown, bound-child retirement, actual native probe and receipt fields. Reuse constants without changing public driver entry points.

## Changed files

ci/runtime/lifecycle/run-nginx-valid-rules.py; ci/runtime/lifecycle/collect-no-crs-source.py; tests/test_nginx_valid_rules_driver.py; this EN/DE record.

## Commands executed

RTK-wrapped Parent Python: two missing-helper RED controls, then 23 valid-rules tests GREEN and 10 config collection controls GREEN. Collector suite60: two missing nested Framework catalog errors and three SKIPs in isolated worktree, not product PASS. Git diff check run before commit. Sonar rule API400 prevented fresh rule details; reported S3776/S1192 snapshot used.

## Security impact

No ownership, containment, transaction, integer-rule, timeout, cleanup, native-event or artifact guard is weakened. Forced cleanup remains unverified.

## Runtime evidence

No new runtime claim: unit mocks exercise failures and exact preserved arguments. MIME diagnostic run is separate and does not verify this startup refactor.

## Known limitations

Remote Sonar closure and actual integrated startup validation require coordinator checks. Nested Framework is intentionally uninitialized in this isolated Parent worktree.

## Remaining risks

Potential integration conflicts with coordinator receipt additions require semantic review; this patch adds no new receipt fields.

## Checks not run and rationale

Full Parent lint and integrated/remote checks not run here. Broad collector suite cannot find the isolated nested catalog; use the integrated worktree without bypassing checks.

## Final diff and review status

Explicit task-owned files only; independent local commit, no push, merge, amend or gitlink update. Required final acceptance remains outstanding.
