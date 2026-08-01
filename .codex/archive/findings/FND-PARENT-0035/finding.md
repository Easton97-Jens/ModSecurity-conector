# Finding: Raw native rules grant LibModSecurity filesystem and process output authority outside the case root

**Language:** English | [Deutsch](finding.de.md)

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0035` |
| Category | `security_validated` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P0` / `high` / `reproduced` |
| Status | `fixed` |
| Release blocker / security relevant | yes / yes |

## Summary, behavior, and impact

Raw native rules could override `SecDebugLog`/`SecAuditLog` and request
resource/process/CWD-sensitive Library behavior. A controlled case created
external sibling Library output even after Parent case-root preparation. A
case author could write outside the verified native root, invoke side effects,
or consume mutable CWD-relative state.

Expected behavior permits only Parent-owned result/server-log descriptors and
a verified 0700 descriptor-owned CWD; rules never grant Library pathname,
resource, process, or unowned-state authority.

## Affected scope and preconditions

- Files/symbols: `run-native-case-comparison.py`,
  `native_modsecurity_oracle.c`, native rule materialization,
  `run_oracle_with_owned_outputs`, `fchdir`, and `open_output_fd`.
- A raw native rule reaches the comparison runner and LibModSecurity parses it
  before the fixed authority gate.

## Reproduction and evidence

1. Supply `SecDebugLog` or `SecAuditLog` targeting a sibling external path.
2. Run a native case; repeat with a final link to a foreign sentinel.
3. The retained exact-head evidence has the historical path
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/native-rule-output-revalidation.md`
   (not distributed in this reconciliation checkout),
   SHA-256 `54aeaa1474c35daa8793da3d5254f01fb9e751be338daf11e0e14b3620db3b0e`.
   21 tests passed on `0e55bb5e8444b99a9b4eaf50cd22679fe5d6f273`; the real
   LibModSecurity 3.0.16 control reached status 200 while unsafe variants were
   rejected before the C Oracle and preserved sentinels.

## Root cause and remediation

Safe case-root allocation was followed by treating untrusted rules as
authority for Library file/resource/process APIs. PR C fail-closes unsafe
directives/operators/actions, removes the Library audit/debug pathname
preamble, retains Parent-owned output FDs, and validates a private state FD
before `fchdir`.

## Acceptance, validation, and controls

- Original and final-link audit/debug variants fail before the C Oracle.
- Resource/process/output escapes fail; an `initcol`/`setvar` status-200
  control succeeds with descriptor-owned CWD/FDS.
- `tests/test_runtime_env_snapshot_contract.py` passed 21/21; Clang C17 and
  GCC C17 `-fanalyzer` static checks passed.

## Dependencies, blockers, related findings, and residual risk

This uses PR-A descriptor primitives (`FND-PARENT-0033`), but is not the same
root cause. `FND-PARENT-0036` is a separate C lifetime defect. Full
Framework/MRTS native-matrix integration is `blocked_missing_evidence`; the
local fix is delivery-pending until exact PR CI/review evidence. No risk
acceptance or merge is authorized.

## History

- `2026-07-18T14:46:42Z`: real Library escape evidence and exact PR-C head
  controls passed; status set to `fixed` pending verified PR.
