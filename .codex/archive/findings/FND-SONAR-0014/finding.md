# FND-SONAR-0014 — PR #97 Common runtime smoke maintainability follow-up

## Classification

- **Category:** `sonarqube_finding` (`maintainability_code_smells`)
- **Rules:** `python:S1192` and `python:S3415`
- **Repository / ownership:** `parent` / `parent`
- **Priority / severity / confidence:** `P3` / `major` / `candidate`
- **Status / verification:** `accepted_risk` / `current_parent_semantics_revalidated_pending_hosted_per_rule_receipt`
- **Release blocker / security relevant:** no / no
- **Delivery state:** full protected merge `7f72325cbd177e4bd98b3511a58344c04d41b06b` is locally reachable from current Parent `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`; the hosted per-rule receipt remains pending.

## Summary

The paired PR #97 Change Record reports two `python:S1192` duplicate-literal
observations and four `python:S3415` assertion argument-order observations on
the initial Draft PR analysis. The local follow-up introduces named runtime/
CRS constants and corrects four assertion orders. The supplied focused suite
reports 26 passing cases.

Parent-provided exact-head evidence for `b3860aac005a98244f5e880efc26a74449b11989`
reports the 26 focused tests, `compileall`, `--help`, required/current PR
checks, and SonarQube Cloud Quality Gate passed; eight current PR issues are
`CLOSED/FIXED` in aggregate. The current user selected a local archive-only
`accepted_risk` disposition for the missing retained hosted per-rule
S1192/S3415 receipt; the current local merge and semantics evidence is
recorded below, without claiming a Quality-Gate pass, fix, or release result.

## Current local revalidation — 2026-07-26

Full protected merge `7f72325cbd177e4bd98b3511a58344c04d41b06b` is an
ancestor of current Parent `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`.
The retained task report reran the 26 focused controls, syntax, CLI help, and
whitespace review. `CRS_SETUP_TEMPLATE_NAME`, `RUNTIME_PATH_DEPENDENCY`, and
`RUNTIME_OUTPUT_PATH_FIELDS` remain named constants; the four corrected
assertion controls retain their rejection and legitimate-control behavior.
FND-SONAR-0013's security boundary was independently revalidated in the same
report. No source change or PR is needed; hosted per-rule S1192/S3415 evidence
remains the only completion gap.

## Observed and expected behavior

The reviewed exact PR head is `b3860aac005a98244f5e880efc26a74449b11989`
against base `38752600e4823fc5a16f3e155047da2d660b9897`; original feature
commit `2fb994324c097a846ed6f6d93126cb8def391f0d`. The Parent confirmed the
current exact-head aggregate result, but no protected merge or
resulting-master validation.

The diff introduces `CRS_SETUP_TEMPLATE_NAME`, `RUNTIME_PATH_DEPENDENCY`, and
`RUNTIME_OUTPUT_PATH_FIELDS` for repeated text and changes four unittest
assertion argument orders. The corrections must preserve the same rejection
and legitimate-control behavior, preserve FND-SONAR-0013's path/provenance
boundary, and never change a Sonar rule, profile, suppression, exclusion, or
Quality Gate. The user-directed local archive disposition does not substitute
for technical evidence or weaken that boundary.

## Impact and affected scope

The impact is maintainability debt and future review/static-analysis noise; it
is not a demonstrated runtime or security defect and does not independently
block release integration. It also does not change the P1 security-candidate
status of `FND-SONAR-0013`.

Affected paths and symbols are:

- `common/scripts/run_local_runtime_smoke.py` —
  `CRS_SETUP_TEMPLATE_NAME`, `RUNTIME_PATH_DEPENDENCY`, and
  `RUNTIME_OUTPUT_PATH_FIELDS`.
- `tests/test_common_runtime_smoke_crs_source_security.py` — four assertion
  argument-order corrections.
- The paired PR #97 Change Record files.

## Reproduction and evidence

Inspect the local PR #97 diff and its paired Change Record, then run:

```text
env PYTHONDONTWRITEBYTECODE=1 python -m unittest -v tests.test_common_runtime_smoke_crs_source_security
```

Verify the changed assertions maintain the same control/rejection behavior.
The Change Record reports 26 passing focused cases, but this record task did
not rerun or retain the raw test log. A later exact-head SonarQube Cloud query
must compare rule, component, and disposition for `python:S1192` and
`python:S3415` without changing a Sonar control.

Evidence source: `/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/worktrees/pr55/reports/audits/change-records/CR-20260723-sonar-common-crs-source-integrity.md`, SHA-256
`d07f3fb43265c7acfad64934c0b73c859ac3c30a048fff0b7e6064a0e334a8c9`,
run `20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b`,
observed at `2026-07-24T07:58:00Z` with `git diff --name-status`, `git diff
--check`, and `sha256sum`, exit `0`. Its German pair SHA-256 is
`e7b9461f09f84cb43b8f736806743d0d83b7ea028507e25b88666f4c22182e24`.
Both are volatile worktree sources, not sealed execution receipts. The
Parent-provided aggregate hosted summary has no supplied raw per-rule receipt
path in this bounded record task.

## Root cause and proposed remediation

The initial Draft PR analysis reportedly identified repeated literal text and
assertion argument order that did not meet configured Sonar maintainability
rules. The bounded evidence does not establish a broader runtime defect or
behavioral change beyond those patterns.

Retain the named shared constants and semantically equivalent assertion order.
The current aggregate exact-head result reports eight PR issues
`CLOSED/FIXED`; retain a per-rule receipt to verify the two S1192 and four
S3415 observations specifically, then repeat it after any head change.
Do not weaken FND-SONAR-0013's path/provenance controls to reduce a
maintainability finding.

## Acceptance criteria and validation plan

1. The current exact PR #97 head preserves Common runtime smoke rejection and
   legitimate-control behavior after literal deduplication and assertion-order
   correction.
2. Focused tests, syntax/help checks, bilingual Change Record review, and
   `git diff --check` pass for that exact head.
3. The confirmed exact head retains Quality Gate `OK` and aggregate current PR
   issues `CLOSED/FIXED` without a control change; a retained per-rule receipt
   verifies the two S1192 and four S3415 observations specifically.
4. FND-SONAR-0013's path/provenance boundary remains intact and independently
   validated.

Retain a raw per-rule exact-head receipt, repeat it after any head change, run
the focused semantics/syntax/help/bilingual/whitespace checks, and review the
diff for accidental security-control weakening. After protected merge, verify
the resulting master SHA and applicable master checks before marking this
finding verified.

## Dependencies, blockers, and residual risk

Dependencies are Parent Python for the focused suite and read access to current
SonarQube Cloud results. The full merge/current-Parent relationship and local
semantics are now evidenced; the blocker is a retained raw per-rule
S1192/S3415 hosted receipt.

Residual risk is maintainability/review uncertainty until those remaining
receipts exist. The current user accepts that uncertainty only for the local
archive; no merge, resulting-master, runtime-exploit, security-remediation,
fix, or release claim is made. Related finding: `FND-SONAR-0013`.

## History

- `2026-07-24T07:58:00Z`: Allocated from the paired local PR #97 Change
  Record as a nonblocking `in_progress` / `unverified` S1192/S3415 follow-up.
  No current hosted result or merge outcome is asserted.
- `2026-07-24T08:04:28Z`: Parent confirmed exact head `b3860aac005a98244f5e880efc26a74449b11989`; 26 focused tests, `compileall`, `--help`, required/current PR checks passed, Quality Gate was `OK`, and eight current PR issues were `CLOSED/FIXED`. PR #97 remains unmerged.
- `2026-07-26T17:18:12Z`: Local Git confirms full merge
  `7f72325cbd177e4bd98b3511a58344c04d41b06b` is an ancestor of current Parent
  `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`. The retained task report records
  focused control semantics, syntax/help, whitespace, and preservation of the
  named literals and assertion order. Hosted per-rule S1192/S3415 evidence
  remains open.

## Delivery update

The Parent previously confirmed a protected merge and 14 green master-push
workflows. This task now records the full merge SHA and its reachability from
the current Parent head, plus local semantic validation. The nonblocking
follow-up is `accepted_risk` only for this local archive because a retained
hosted per-rule S1192/S3415 receipt is unavailable. No independent runtime or
security impact, Quality-Gate pass, fix, verified closure, or release approval
is asserted.

## User-directed local archive disposition — 2026-07-26

After reviewing the current SonarQube Cloud/GitHub reconciliation, the current
user selected this exact triplet for a lossless local archive move. The retained
decision receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260726T182851Z-user-selected-parent-sonar-archive/decision.md`
with SHA-256 `d5dc1ed08dfca22b841c02eee45e0459665f026924ff531f158d1e5dd0145cdf`.

The user accepts only the missing retained current per-rule S1192/S3415
SonarQube receipt for this local archive. The record is not fixed, verified, or
closed. Before any production, publication, release, or technical-closure
decision, restore the complete triplet to `.codex/findings/` and rerun its
existing acceptance criteria.
