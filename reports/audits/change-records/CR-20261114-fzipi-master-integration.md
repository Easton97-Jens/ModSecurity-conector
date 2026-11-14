# Change Record: CR-20261114-fzipi-master-integration

**Language:** English | [Deutsch](CR-20261114-fzipi-master-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261114-fzipi-master-integration |
| Date (UTC) | 2026-11-14 |
| Base revision | `43baefa2d3a6ce66876aca1a2cd0d7b50e2a412a` |

## Motivation and problem statement

The Parent still selected Framework `31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`, whose fixtures do not match the completed connector followup. [Framework PR 171](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/171) is now squash-merged; this integration selects its master commit `3ff8b75c9f4d2cb3614a4dcb7afd2e5360e074d8` through the native candidate and publication contracts.

## Acceptance criteria

Select the merged, reviewed Framework tree; synchronize only its lock/workflow projections and Parent gitlink; retain other component/tool/runtime versions and MRTS. Parent master integration is authorized only with green required tests. Candidate verification does not substitute for new-pin Parent CI, final hook admission or merge authorization.

## Implementation decision and rationale

Use the native verifier and synchronizer rather than hand-edit generated references. The extracted Framework common script is input data, never sourced. The selected master tree is identical to reviewed `f3813dad`; its different squash commit identity is recorded explicitly. MRTS remains `ee2174431c4edf97e66afe32558ce8454deb2397`.

## Changed files

Component lock plus 22 workflow projections, the Parent Framework gitlink and this EN/DE record pair. The coordinator owns the 23 generated files and planned gitlink staging; this record author changes only this pair. No product-source behavior, MRTS content or other version selection is changed by this integration.

## Commands executed

Aliases identify the actual selected locations: `P` is the Parent worktree, `F` the Framework task Git-object worktree, `E` the approved external run root, `C=$E/master-integration/framework-common.data`, and `PY` the canonical Framework interpreter. `O=31531f74cfe26c2a40d4bb5f6eaae4c0920127e1`, `S=3ff8b75c9f4d2cb3614a4dcb7afd2e5360e074d8`, `B=43baefa2d3a6ce66876aca1a2cd0d7b50e2a412a`. Every command below used `rtk bypass env RUNNER_TEMP=$E/master-integration FRAMEWORK_ROOT=$F TEST_ROOT=$F CONNECTOR_ROOT=$P CONNECTOR_REVISION=$B PYTHONDONTWRITEBYTECODE=1 $PY -I`:

| Command after prefix | Coordinator-observed result |
| --- | --- |
| `$P/ci/tools/verify-framework-candidate-contract.py --candidate-sha $S --framework-common $C --candidate-framework-root $F --expected-parent-framework-sha $O` | PASS after restoring pinned Git-source access. |
| `$P/ci/tools/sync-framework-component-versions.py --framework-common $C --framework-object-root $F --framework-sha $S --sync` | PASS; component lock and 22 workflow references synchronized. |
| `$P/ci/tools/sync-framework-component-versions.py --framework-common $C --framework-object-root $F --framework-sha $S --check` | PASS; changed list `[]`. |
| `$P/ci/tools/verify-framework-candidate-contract.py --candidate-sha $S --framework-common $C --candidate-framework-root $F --expected-parent-framework-sha $S` | PASS against the synchronized lock. |
| `$P/ci/tools/sync-framework-component-versions.py --framework-common $C --framework-object-root $F --framework-sha $S --verify-primary --base $B` | PASS for working-tree publication bytes. |

The first candidate invocation failed because the old pinned Framework Git source was unavailable through the no-Git export. That export was retained externally; a linked Framework Git worktree was registered at the old pin, then checked out at the selected new pin without recursively initializing MRTS. The subsequent results above do not erase that initial failure.

## Security impact

The Framework pin is a test-supply-chain boundary. Native verification checks Git-backed source identity and approved projections; no source-data script execution or validation bypass is introduced. A new exact operator gitlink admission may still be required by the hook; it has not been installed or approved at this point. No bypass is claimed.

## Runtime evidence

Before Framework merge, reviewed `f3813dad` passed 19 runner methods, all nine actual native NGINX scenarios and seven CI workflows, with zero reported issues/hotspots. The merged Framework master has the same tree. At this record snapshot, five post-master Framework runs comprise three successes and two still pending. These facts do not establish Parent CI for the new pin or another host/profile.

## Known limitations

The new Framework worktree has no initialized MRTS checkout; the actual existing MRTS repository remains unchanged at its recorded pin. No full materialized-pin verification is claimed. The retained external export without Git metadata is not a replacement for the Git source required by the native verifier.

## Remaining risks

Parent master merge has not occurred. Remaining required CI, final staged-byte review and any exact hook admission must succeed before authorized integration. Passing candidate/publication checks alone cannot establish runtime or final delivery success.

## Checks not run and rationale

Parent CI for the new pin requires normal commit/push and has not run. The two pending post-master Framework runs and final staged documentation/index checks are not claimed passed. The coordinator will run and record those checks before committing/integrating; no future result is represented as observed evidence.

## Final diff and review status

This pair fills the native scaffold without altering its identity/date/base. The coordinator retains ownership of generated projection review, gitlink staging, final checks and Parent master lifecycle. This author performs no Git action, source edit or MRTS write; no final commit, all-green Parent state or completed Parent merge is claimed.


Final local pre-commit evidence: full Parent bilingual/path-reference/link checks passed; staged whitespace passed; the native synchronizer `--verify-primary --base 43baefa2d3a6ce66876aca1a2cd0d7b50e2a412a --staged` returned `FRAMEWORK_PRIMARY_VERIFIED`. The selected merged Framework at `modules/ModSecurity-test-Framework` then passed `python -m unittest -v modsecurity_connector_tests.test_runtime_event_sink_failures modsecurity_connector_tests.test_runtime_host_action_validation modsecurity_connector_tests.test_haproxy_binding_refactor`: 26 methods in 6.679 seconds, exit 0. These directly cover the previously failing extraction/mock seams. Hosted Parent checks still require a normal commit and push; no future merge or admission pass is claimed.
