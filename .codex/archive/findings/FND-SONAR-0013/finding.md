# FND-SONAR-0013 — Common runtime CRS and direct-output integrity candidate

## Classification

- **Category:** `security_candidate` (`python:S5443` and `pythonsecurity:S8707`)
- **Repository / ownership:** `parent` / `parent`
- **Priority / severity / confidence:** `P1` / `high` / `candidate`
- **Status / verification:** `accepted_risk` / `current_source_already_safe_pending_hosted_per_rule_and_live_smoke_evidence`
- **Release blocker / security relevant:** yes / yes
- **Delivery state:** full protected merge `7f72325cbd177e4bd98b3511a58344c04d41b06b` is locally reachable from current Parent `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`; hosted per-rule and live-smoke receipts remain pending.

## Summary

The local PR #97 snapshot identifies a local cross-user configuration-integrity
candidate at Common runtime CRS source selection, generated configuration/audit
output, and direct CLI output paths. `crs_source_candidate_roots()` no longer
consults `RUNNER_TEMP`, `TMPDIR`, `/tmp`, or `/var/tmp`; selected trees are
validated before they can produce ModSecurity `Include` input.

The same diff validates the six direct output destinations `evidence_root`,
`results_dir`, `tmp_root`, `log_root`, `log_dir`, and `config_root` before
`run_smoke()` continues to a write-capable path. The paired Change Record
reports 26 passing focused local tests. Parent-provided current exact-head
evidence for `b3860aac005a98244f5e880efc26a74449b11989` also reports
`compileall`, `--help`, required checks, and all current PR checks passed; the
SonarQube Cloud Quality Gate is `OK` and eight current PR issues are
`CLOSED/FIXED`, including `pythonsecurity:S8707` `AZ-PstOVmYfklgBeDadY`.
The parent-provided PR summary alone was not a protected-merge or
resulting-master verification; the current local revalidation below adds a
full-SHA ancestry proof and retained source/control/sink evidence.

## Current local revalidation — 2026-07-26

`git merge-base --is-ancestor` confirms full protected merge
`7f72325cbd177e4bd98b3511a58344c04d41b06b` is reachable from current Parent
`3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`. Retained task evidence reran all
26 focused CRS/output cases, 6 runtime-path-policy cases, syntax compilation,
CLI help, and whitespace review; the source/control/sink review found the
single production entry point `main() -> run_smoke()` and no unvalidated
production caller of the listed controls.

At the stated cross-user POSIX owner/mode boundary, the candidate is
`already_safe`: only explicit CRS candidates are accepted, source/generation
paths are trusted and no-symlink, and all six CLI output roots are validated
before write-capable operations. This does not claim a live
CRS/libmodsecurity/connector smoke, same-UID race or filesystem-ACL proof, or
hosted per-rule SonarQube evidence. The current user selected a local
archive-only `accepted_risk` disposition for these remaining evidence gaps; no
source change or PR is required and no technical closure is claimed.

## Observed and expected behavior

The reviewed exact PR head is `b3860aac005a98244f5e880efc26a74449b11989`
against local base `38752600e4823fc5a16f3e155047da2d660b9897`; the original
feature commit is `2fb994324c097a846ed6f6d93126cb8def391f0d`. The Parent
confirmed the exact-head local and hosted aggregate result above, but did not
report a protected merge or resulting-master validation.

The diff routes selected CRS source directories through owner, mode,
symlink-component, and ancestor-replacement checks. It creates generated CRS
setup, rule, payload, and audit files with `O_NOFOLLOW` plus exclusive
creation, then revalidates the generated rule before evaluator use. Direct
output paths must be absolute, symlink-free, and contained beneath a safe
`VERIFIED_RUN_ROOT`; rejected inputs must return `SmokeBlocked` / exit `77`
before a runner write.

Only explicit `CRS_SOURCE_DIR` or paths derived from an explicit
`--runtime-lookup-root` may become CRS input. A valid trusted source and a
valid contained verified-runtime output layout must remain accepted.

## Impact and scope

If the pre-follow-up direct path selection were reachable, a different local
user able to preseed a shared temporary path or unsafe output target could
influence configuration input or direct output location. The affected boundary
is:

`CRS/output CLI or environment selection → Common runtime smoke → generated configuration/audit artifacts → local evaluator or result writer`

This is a local configuration/file-integrity candidate. It does **not** prove
a remote request-to-parser path, arbitrary CRS code execution, a
current-master exploit, or a successful runtime attack. Same-UID races and
filesystem ACL semantics are outside the stated POSIX owner/mode claim.

Affected Parent paths and symbols are:

- `common/scripts/run_local_runtime_smoke.py` —
  `crs_source_candidate_roots`, `resolve_crs_source_dir`,
  `validate_crs_source_dir`, `prepare_crs_smoke_config`,
  `validate_runtime_output_paths`, `require_verified_runtime_output_path`,
  `secure_crs_output_file`, `write_trusted_crs_output`, and `run_smoke`.
- `tests/test_common_runtime_smoke_crs_source_security.py`.
- The paired variables documentation and Change Record files listed in the
  JSON record.

## Reproduction and evidence

Inspect the local PR #97 diff from base `38752600e4823fc5a16f3e155047da2d660b9897`
to snapshot `b3860aac005a98244f5e880efc26a74449b11989`. Then run:

```text
env PYTHONDONTWRITEBYTECODE=1 python -m unittest -v tests.test_common_runtime_smoke_crs_source_security
```

The paired Change Record reports 26 passing focused cases, including ambient
CRS candidates, unsafe source/generated-output variants, all six direct output
roots, relative and broad verified roots, symlink escapes/loops, a preexisting
CRS suffix symlink, and legitimate controls. This bounded record task did not
rerun or retain the raw test log.

Evidence source: `/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/worktrees/pr55/reports/audits/change-records/CR-20260723-sonar-common-crs-source-integrity.md`, SHA-256
`d07f3fb43265c7acfad64934c0b73c859ac3c30a048fff0b7e6064a0e334a8c9`,
run `20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b`,
observed with `git diff --name-status`, `git diff --check`, and `sha256sum`
at `2026-07-24T07:58:00Z`, exit `0`. The German pair has SHA-256
`e7b9461f09f84cb43b8f736806743d0d83b7ea028507e25b88666f4c22182e24`.
Both are volatile worktree sources, not sealed execution receipts. The
Parent-provided exact-head hosted summary has no supplied raw receipt path or
full per-key response in this bounded record task.

The historical rule references are `AZ70UrU3IhrooTjfZnAX`,
`AZ70UrU3IhrooTjfZnAY`, `AZ70UrU3IhrooTjfZnAZ` (`python:S5443`) and
`AZ-PstOVmYfklgBeDadY` (`pythonsecurity:S8707`). The supplied exact-head
summary explicitly identifies the S8707 key as `CLOSED/FIXED` and reports the
aggregate eight-issue set `CLOSED/FIXED`; it does not contain a retained raw
per-key mapping for every historical S5443 reference.

## Root cause and proposed remediation

Before the reviewed diff, ambient temporary roots could become CRS candidates
and selected/generated paths did not have the documented end-to-end
trusted-source, no-symlink, provenance, and verified-output-root boundary.

Keep the PR #97 controls narrow: accept only explicit source candidates,
validate selected source and generated output components, use no-follow and
exclusive creation, revalidate the rule before evaluator use, and validate all
six direct CLI output roots before the first write-capable action. Preserve
valid explicit-source and verified-root controls. Do not substitute a Sonar
suppression, exclusion, rule/profile or Quality-Gate change, false-positive
disposition, or risk acceptance for technical evidence.

## Acceptance criteria and validation plan

1. The current exact PR #97 head rejects unsafe CRS source/generated-output
   inputs before evaluator rule-file use and has no ambient shared-temporary
   source fallback.
2. The six direct output paths are absolute, canonicalized, no-symlink, and
   contained below a safe `VERIFIED_RUN_ROOT` before any runner filesystem
   operation; rejected input returns exit `77` without a runner write.
3. Legitimate trusted sources and contained verified-runtime output layouts
   remain accepted through the same production boundary.
4. The focused suite, syntax/help checks, exact diff review, and
   source-to-sink/alternate-bypass review pass for the exact head.
5. The confirmed exact head retains Quality Gate `OK` and the current PR issue
   set `CLOSED/FIXED` without changing Sonar controls; any later head requires
   fresh evidence.
6. A real CRS/libmodsecurity smoke runs only with documented prerequisites;
   otherwise it remains explicitly `not_run` or `blocked`.

The validation sequence is: retain a raw exact-head test/hosted receipt when
available; repeat it after any head change; review direct callers and
overrides; run the real smoke only when its prerequisites are available; then,
after protected merge, verify resulting-master SHA, the original legitimate
controls, and applicable master checks before marking this finding verified.

## Dependencies, blockers, and residual risk

Dependencies are a current exact PR #97 head, a Parent Python environment,
read access to GitHub and SonarQube Cloud for exact-head verification, and
optional local libmodsecurity/CRS/host components for a real smoke.

The remaining blockers are the lack of a retained raw per-key receipt for each
historical S5443 reference and the absence of a real evaluator/host-connector
smoke in this bounded task. Full protected-merge SHA reachability and the
current focused source/control/sink rerun are now retained locally.
The current user accepts these gaps only for the local archive; no production,
publication, release, or technical-closure decision is authorized. Related
finding: `FND-SONAR-0014`.

## History

- `2026-07-24T07:58:00Z`: Allocated from the local PR #97 diff and paired
  Change Record as an `in_progress` / `unverified` candidate. The 26-case
  local-test statement is retained with its limitation; hosted and merge
  results are intentionally not claimed.
- `2026-07-24T08:04:28Z`: Parent confirmed exact head `b3860aac005a98244f5e880efc26a74449b11989`; 26 focused tests, `compileall`, `--help`, required/current PR checks passed, Quality Gate was `OK`, and eight current PR issues were `CLOSED/FIXED`, including S8707 key `AZ-PstOVmYfklgBeDadY`. PR #97 remains unmerged.
- `2026-07-26T17:18:12Z`: Local Git confirms full merge
  `7f72325cbd177e4bd98b3511a58344c04d41b06b` is an ancestor of current Parent
  `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`. The retained task report records
  26 focused CRS/output tests, 6 runtime-path-policy tests, syntax/help,
  whitespace, and static source/control/sink review. The current-source
  security assessment is `already_safe` at the documented cross-user POSIX
  owner/mode boundary; hosted per-rule SonarQube and live-smoke evidence remain
  open.

## Delivery update

The Parent previously confirmed a protected merge and 14 green master-push
workflows. This task now independently records full merge SHA
`7f72325cbd177e4bd98b3511a58344c04d41b06b` and its reachability from the
current Parent head, plus a retained current local rerun. The finding is
`accepted_risk` only for this local archive because no retained hosted
per-rule SonarQube receipt or live CRS/libmodsecurity/connector smoke exists.
No remote exploit, fix, verified closure, production safety, or release
approval is claimed.

## User-directed local archive disposition — 2026-07-26

After reviewing the current SonarQube Cloud/GitHub reconciliation, the current
user selected this exact triplet for a lossless local archive move. The retained
decision receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260726T182851Z-user-selected-parent-sonar-archive/decision.md`
with SHA-256 `d5dc1ed08dfca22b841c02eee45e0459665f026924ff531f158d1e5dd0145cdf`.

The user accepts only the documented residual uncertainty for this archive:
missing hosted per-rule SonarQube evidence, an unrun real
CRS/libmodsecurity/connector smoke, broader filesystem/identity assumptions,
and current static-analyzer signals. The record is not fixed, verified, or
closed. Before any production, publication, release, or technical-closure
decision, restore the complete triplet to `.codex/findings/` and rerun its
existing acceptance criteria.
