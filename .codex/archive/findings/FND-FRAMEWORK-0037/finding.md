# FND-FRAMEWORK-0037 — Python-maintenance workflow used unsupported job-level runner context and unannotated literal Markdown

Exact-head workflow lint for Framework PR #39 rejected `runner.temp` in the
new candidate job's job-level `env`, because `runner` is not available at that
scope. It also reported SC2016 for intentional Markdown backticks in the
single-quoted Draft-PR body. This is a deterministic P1/non-security delivery
blocker, not a permission or token exposure.

The repair retains only the candidate at job scope, initializes the fixed
runner paths at step runtime through `$GITHUB_ENV`, and narrowly suppresses
SC2016 immediately before the literal `printf`. It must retain all existing
read/write isolation, immutable pins, schedule/manual gates, and Draft-only
publication. Local workflow/contract checks, the complete native lint suite,
and the sealed 11-file security-diff scan now pass. The finding is locally
`fixed`; a fresh exact-current-head hosted workflow-lint run and the remaining
PR gates are still required before a verified delivery disposition.

## Validation and history

- The former failure is retained at GitHub Actions run `29774954611`, job
  `88461998115`; it reported the unsupported job-level context and SC2016.
- The repair passed 36 focused tests, 85 CI-security tests,
  `make check-github-actions-workflows`, `make test-workflow-contract`,
  `make check-documentation`, full native `make lint`, and `git diff --check`.
- The sealed follow-up scan report is
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T180337Z-framework-python-313-updater-f3349a7e/analysis/codex-security-scans/ModSecurity-test-Framework/4a31df0_remediation_followup_20260720T210011Z/report.md`
  with SHA-256 `be92a7e65c3c81e72140b5441494eb4461df4417ee361c344bd3d0cf56775a5c`.
- 2026-07-20T21:12:33Z — status changed to `fixed` after local regression,
  workflow, and security validation. The remediated commit must still pass
  current-head hosted Actions; no merge, Parent gitlink update, or MRTS action
  is authorized.
