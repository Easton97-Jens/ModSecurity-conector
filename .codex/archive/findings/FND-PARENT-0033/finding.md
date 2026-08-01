# Finding: Predictable runtime roots and unvalidated run IDs grant filesystem authority outside the verified run root

**Language:** English | [Deutsch](finding.de.md)

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0033` |
| Category | `security_validated` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P0` / `high` / `reproduced` |
| Status | `fixed` |
| Release blocker / security relevant | yes / yes |

## Summary, behavior, and impact

Runtime entry points accepted predictable temporary roots, mutable path
fragments, and unchecked `VERIFIED_RUN_ID` values before downstream writers
opened or cleaned paths. The retained pre-fix proof demonstrated root,
parent/final-symlink, final-file, traversal/absolute-ID, empty/overlong/
Unicode-ID, foreign-file, parallel, and validation/open-race failures. A local
same-user attacker could redirect a report/evidence write or deletion outside
the intended runtime root.

Expected behavior is a current-user-owned, capability-bound 0700 root with
bounded allowlisted IDs before joins, descriptor/no-follow/exclusive I/O, no
foreign-file adoption, and symlink-leaf-only cleanup.

## Affected scope and preconditions

- Files/symbols: `ci/lib/runtime_path_security.py`, runtime lifecycle bridges,
  `prepare_runtime_root`, `validate_verified_run_id`,
  `relative_path_below`, and direct runtime writers including MRTS-native
  Parent staging.
- An attacker can create/replace a writable ancestor component and an affected
  entry point consumes it before the fixed boundary.

## Reproduction and evidence

1. Pre-create a root, parent, or final symlink to a foreign sentinel; invoke a
   legacy runtime writer.
2. Supply `..`, an absolute, empty, overlong, or Unicode-separator run ID; or
   swap a file/directory between validation and open.
3. The retained exact-head evidence has the historical path
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/runtime-temp-path-revalidation.md`
   (not distributed in this reconciliation checkout),
   SHA-256 `db84a74c2048327ec886d03b33f04885af9b368799f45fc9959111f0b4eb1216`.
   Its command exited 0 with 54 focused tests on commit
   `576c08e9fdb27bc0ec9a6507a02c28413004ac25`.

## Root cause and remediation

String-derived paths were trusted as authority across allocation, run-ID
propagation, writing, reading, and cleanup. PR A uses descriptor-relative
`lstat`/no-follow/exclusive primitives, 0700 capability-bound roots, a
bounded ASCII allowlist, ownership records, secure shell/Python bridges, and
safe cleanup throughout the mapped Parent writers.

## Acceptance, validation, and controls

- All permitted artifacts stay below the canonical verified root with
  restrictive modes; all symlink/traversal/foreign/race controls preserve the
  sentinel.
- `tests/test_verified_runtime_path_hardening.py`,
  `test_runtime_artifact_io_hardening.py`,
  `test_mrts_native_full_path_hardening.py`, and
  `test_runtime_env_snapshot_contract.py` cover regression and normal controls.
- Exact-head `sh -n` and ShellCheck for `run-mrts-native-full.sh` passed.

## Dependencies, blockers, related findings, and residual risk

No remediation dependency remains. Framework/MRTS end-to-end integration is
`blocked_missing_evidence`, not a pass or risk acceptance. Related findings
are `FND-PARENT-0034` and `FND-PARENT-0035`; they have distinct report and
Library-rule boundaries. The fix remains delivery-pending until exact PR CI and
review evidence exist; no merge or risk acceptance is authorized.

## History

- `2026-07-18T14:46:42Z`: pre-fix exploit classes validated; exact PR-A head
  controls passed; status set to `fixed` pending verified PR.
