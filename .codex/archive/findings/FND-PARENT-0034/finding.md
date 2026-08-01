# Finding: Temporary report writers can clobber foreign files through symlinked roots or report leaves

**Language:** English | [Deutsch](finding.de.md)

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0034` |
| Category | `security_validated` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P0` / `high` / `reproduced` |
| Status | `fixed` |
| Release blocker / security relevant | yes / yes |

## Summary, behavior, and impact

Predictable temporary report roots and pathname-based report/index/log/cleanup
writes allowed a pre-created symlink to redirect publication into a foreign
path. Before the fix, a real `TMP_ROOT/modsecurity-doc-cleanup` symlink caused
`generate-connector-roadmap.py` to overwrite a foreign sentinel and return 0.
A local attacker could corrupt same-user files through a temporary-root or
final-leaf symlink.

Expected behavior is a random private temporary root plus descriptor-bound,
canonical write authority; unsafe children, parent/final links, foreign files,
and cleanup substitutions must be rejected or removed only as a leaf.

## Affected scope and preconditions

- Files/symbols: `ci/lib/report_path_safety.py`, report generators,
  `refresh-connector-reports.py`, `generate-connector-roadmap.py`, inventory
  generation, `allocate_private_output_directory`, `prepare_report_directory`,
  `write_report_index`, and `run_command`.
- The attacker can prepare a directory/leaf link under a report output ancestor
  before a generator or publisher uses its legacy pathname path.

## Reproduction and evidence

1. Create `TMP_ROOT/modsecurity-doc-cleanup` as a directory link to a
   directory containing a sentinel and run the roadmap generator.
2. Repeat with parent/final links and a validation-to-publish swap.
3. The retained exact-head evidence has the historical path
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/report-temp-writer-revalidation.md`
   (not distributed in this reconciliation checkout),
   SHA-256 `c4dc1573be22442521af0e6254bff8c205068fad51feb5d68b0d3775a80d1660`.
   The post-fix command exited 0 with 18 focused tests on PR-B head
   `3a3e1274e62182a6cb0853d1352a40a52a9196f5`; the legacy class now returns 1
   and preserves the sentinel.

## Root cause and remediation

Lexical `Path` objects and a predictable temporary directory were treated as
write authority. PR B separates canonical read/write authorities, traverses
directory FDs with `lstat`/no-follow semantics, publishes atomically to
allowlisted leaves, allocates CSPRNG private roots, validates children, and
unlinks only known symlink leaves. Runtime logs retain PR-A capability binding
when `VERIFIED_RUN_ROOT` is present.

## Acceptance, validation, and controls

- Legacy, parent/final/swap links and foreign-file attempts preserve sentinels.
- Absolute/traversal/empty/long/Unicode children fail; parallel allocation and
  normal report/index controls succeed.
- `tests/test_report_temp_path_findings_poc.py` passed 18/18; in-memory
  compilation passed for 21 changed Python files and `git diff --check` passed.

## Dependencies, blockers, related findings, and residual risk

`FND-PARENT-0033` supplies the verified runtime capability used for runtime
logs. Full Framework-backed refresh/layout remains `blocked_missing_evidence`.
`FND-PARENT-0035` is separate Library rule authority. The local fix remains
delivery-pending until exact PR CI/review evidence; no merge or risk acceptance
is authorized.

## History

- `2026-07-18T14:46:42Z`: real pre-fix clobber reproduced; exact PR-B head
  controls passed; status set to `fixed` pending verified PR.
