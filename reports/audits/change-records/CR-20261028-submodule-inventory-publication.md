# Change Record: CR-20261028-submodule-inventory-publication

**Language:** English | [Deutsch](CR-20261028-submodule-inventory-publication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-submodule-inventory-publication |
| Date (UTC) | 2026-10-28 |
| Base revision | `cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3` |

## Motivation and problem statement

PR #429 changed the Framework gitlink and central lock but omitted the inventory companions. Its Python 3.15.1 admission failed with reviewed source digest mismatch for ci/tooling/project-versions.lock.json before selected checks could run. The publisher itself had succeeded in run 40671467579. The user requested repair of both the open PR and the producer.

## Acceptance criteria

Repair PR #429 without changing case/selector/profile/source membership. Synchronize exactly two companions atomically with fixed primary targets. Independently reconstruct full primary and companion bytes from trusted master before staging and from stage-zero blobs afterwards. Reject forged metadata, stale source bindings and unsafe companion modes; preserve rollback and existing branch identity/history gates.

## Implementation decision and rationale

The synchronizer reuses the existing complete inventory admission and fixed companion derivation. Its existing transaction includes companion replacements and post-write readmission. Independent --verify-companions --base reconstruction proves complete registered primary bytes first, then exact derived companion bytes; --staged checks regular 100644 stage-zero blobs. Existing archive source_sha256 slots may follow only proven fixed primary test-source changes; inventory_sha256 follows the generated inventory. Definitions and selection metadata remain unchanged. The workflow adds only the two fixed paths and a strict 100644/M raw-diff branch.

## Changed files

ci/tools/sync-framework-component-versions.py; tests/test_update_framework_versions.py; .github/workflows/update-submodules.yml; tests/test_ci_security_workflows.py; config/testing/active-cases.json; reports/testing/test-selection-archive.generated.json; docs/build/README.md and docs/build/README.de.md; this Change Record pair. The separate PR #429 repair commit cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3 contains only the two generated companions.

## Commands executed

All project shell commands used the task-owned RTK v1.0.1 bypass with isolated task data/config/temp roots. Under Python 3.15.1, ci/tools/run-active-tests.py --check passed for repaired PR #429: 100 default cases and 1893 on demand. ci/tools/update-test-archive.py --check and git diff --check passed. Two focused workflow tests passed, including actual shell allowlist/raw-diff execution with legitimate companions and rejected executable/symlink/add/delete/unregistered variants. The new regression rejected the legitimate update with the original workflow. The main agent freshly ran 41 tests (39 synchronizer tests plus the two workflow tests), all passed in 48.691s on the integrated tree. Full inventory admission, native archive --check, bilingual documentation, variable references (103), repository/documentation links, Change Record structure and whitespace passed. The backend regression also fails for the intended missing-companion reason against the old synchronizer.

## Security impact

The publisher consumes statically parsed candidate data and trusted master code. New companion authority is restricted to two existing regular files, exact trusted-base reconstruction and unchanged selection/metadata. Atomic rollback and concurrent-edit preservation remain active. Validator isolation, permissions, credentials, candidate execution, ref gates, auto-merge prohibition and open-branch one-updater-commit rule remain unchanged.

## Runtime evidence

The original stale-binding rejection was reproduced at PR head 7bfe28818bff8319a77693254d49b6053231d8e4 and no longer reproduces after repair cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3. This is inventory/publication evidence, not a connector runtime or I12 qualification. New hosted CI results must remain bound to their actual head.

## Known limitations

The repaired open PR #429 has an additional reviewed commit. Its branch is intentionally ineligible for automatic open-branch reuse until reviewed integration under the existing one-updater-commit rule. This repair does not authorize a merge. Full hosted updater publication with the permanent fix requires integration of trusted publisher code.

## Remaining risks

A fresh hosted run may reveal a later independent failure; none is silently accepted. Exact byte reconstruction and stage-zero checks intentionally reject concurrent drift rather than overwriting it. Framework and MRTS remain separate read-only repositories for this task.

## Checks not run and rationale

No new all-connector matrix, I12 campaign or broad security scan was started. Hosted runtime, Sonar and merge readiness are not inferred from local fixture or inventory success. Required head-bound CI remains a separate delivery criterion.

## Final diff and review status

The immediate PR repair was derived from trusted base b8f76fd718bf26dd3a4345dd6700534690d8a49d; local and published tree 65236d801b1bc73bb74de9cd57591e1034f9d9b0 matched. Independent final source/workflow review found no material blocker. A fresh full Parent checkout at 7eb41bb805c6c3d07244af2068d6db9930740bdc exercised the real Framework transition 99a7985c1be92a2297b1b59208f64df6768f2cbf to 3a4f2281568139d94fda6b51dc2e07bb8fc06c67 through the public CLI: --sync changed only the central lock and two companions, --check and native archive --check passed, and --verify-companions --base succeeded before and after explicit staging with --staged. The permanent publisher fix is included directly in repaired PR #429 so both inventory changes are reviewed, tested and integrated together. No merge is authorized by this change.
