# FND-PARENT-0071 — Apache smoke runtime omits a ServerRoot-resolved MIME artifact

## Identity

- Category: runtime_defect
- Repository / ownership: parent / parent
- Priority / severity / confidence: P1 / not_applicable / validated
- Status / feasibility: fixed / feasible_now
- Release blocker / candidate-integration blocker / security relevance: true / false / true
- Scope: resulting Parent master 154ee724eba4653fa6378fc3c8729ae433e65697, tree-identical to final PR #183 head 4e4dfb36e1b05f7eda38450fd3710e3a04905118

## Summary

**Current resulting-master disposition — 2026-07-29T11:27:25Z.** PR #183
merged as master `154ee724eba4653fa6378fc3c8729ae433e65697`; tree
`c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0` equals final head
`4e4dfb36e1b05f7eda38450fd3710e3a04905118`, and all 14 master-SHA workflows
succeeded. Detached-master focused Apache/MIME unit checks and
`make check-apache-common-adoption` passed. These facts supersede the historic
candidate-only wording below but do not replace a fresh resulting-master live
start/readiness/403/`SIGUSR1` run; the finding remains `fixed`, not `verified`
or `closed`.

The Apache smoke harness generated only `conf/mime.types` even though the
rendered configuration sets `ServerRoot` to the generated runtime root and the
available Apache `mod_mime` resolves its default `mime.types` at
`$ServerRoot/mime.types`. The pre-fix configuration parse says `Syntax OK`, but
the Apache process fails before any request with `AH01597` for the missing
root-level MIME file.

A mutable local repair creates the generated MIME artifact in both locations.
Retained controls then show a live HTTP/1.1 `phase2_args_block` denial at 403
and a `SIGUSR1` graceful restart with restored readiness. The record is
**fixed locally only**: it remains a P1 Apache smoke/runtime release blocker
until an independent committed PR exact head and resulting-master reproduction
exist. It is neither verified nor closed.

## Evidence and boundary

| Artifact | SHA-256 or result | Evidence |
| --- | --- | --- |
| Pre-fix config test | bbafef10c22b9323fa5589564990f57fbf57f9a632381d5e765dc5a3b25b4a1b | `apache2 -t` reports `Syntax OK`; parsing does not prove process liveness. |
| Pre-fix Apache error log | 0c7791f4b9935d6eda358d1c47dfcee2cc0baf547331b776ea3ea6ae5ded6fff | `AH01597` names the missing `ServerRoot/mime.types` before any request. |
| Mutable harness repair | 9046a8caff239fa0bfe430224eb2819e2f01fa1e49fb50a16c21bf37fee7ece2 | Defines and writes `MIME_TYPES_ROOT_FILE` as well as the existing `conf/` file. |
| Mutable static contract | 167413ac60fee5dd215d2c9524d0bded1d344ee1425bc3284193ede9502e8399 | Focused test must be rerun from a committed PR head. |
| Root and `conf/` MIME artifacts | fafe925e793113aff60a22955ace0e8ddc4c3b068117f71b97d1897a58983317 | Both generated files exist with equal content. |
| Post-fix phase-2 control | cbfb2a07f77347b3554933173065063b237eca437e11882fe45db407afc11f1c | Live Apache reports expected/actual HTTP 403 and `status=pass`. |
| Post-fix restart log | ac01ca9bf7ea2615e4c02842b1b1dfd06ef0404962957ca68737406673f6566d | Records `SIGUSR1 received` and graceful restart. |

The task worktree's Git HEAD remains
`9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; the two-location repair is an
uncommitted working-tree delta. The retained runtime artifact hashes are
read-only observations in the registered task root, not a sealed exact-PR-head
evidence set.

## Root cause and remediation direction

`run_apache_smoke.sh` populated only the conf-relative MIME file, while
`apache_smoke.conf` makes the generated runtime root the `ServerRoot`. The
runtime default lookup needs the root-level file before Apache starts; a
syntax-only configuration test does not exercise that open operation.

Promote the demonstrated dual-location artifact change and focused static
contract in a separate Parent PR. On its exact head, prove both generated
paths, configuration parsing, live Apache readiness, the HTTP/1.1 403 control,
and graceful restart/readiness. Then reproduce the original startup condition
and controls on resulting master before any verified or closed status.

## Acceptance and distinctness

Acceptance requires both generated MIME locations in a fresh runtime, actual
Apache process startup/readiness, phase-2 HTTP/1.1 403, SIGUSR1 graceful
restart/readiness, and a negative static contract for a one-location harness.
The independently committed repair must pass exact-head and resulting-master
validation.

This record is distinct from FND-PARENT-0070: 0070 owns APXS DSO source
materialization in `connectors/apache/build/apxs-wrapper.in`; this record owns
runtime configuration artifact placement in `connectors/apache/harness/`.
It does not prove the separate FND-PARENT-0064 RulesSet APR lifecycle condition
has been repaired.

## History

- 2026-07-29T11:27:25Z: the resulting-master delivery facts above were
  reconciled; fresh master live start/readiness/403/`SIGUSR1` validation remains required.

- 2026-07-29T10:33:55Z: retained pre-fix `AH01597` evidence and local repair
  controls created the canonical Parent runtime-defect record. The repair is
  fixed locally only, pending committed exact-head and resulting-master
  validation.
