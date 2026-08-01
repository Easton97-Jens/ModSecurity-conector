# FND-FRAMEWORK-0038 — Fallback YAML parser misclassified colon-containing plain sequence scalars after reviewed Python migration

PR #39's reviewed Python 3.13 `test-common` runner used the dependency-free
fallback YAML parser because PyYAML was not installed. That parser interpreted
every colon in a list scalar as a mapping separator, turning the valid
`ARGS:foo.` limitation into a dictionary and failing case validation. This is a
P1/non-security exact-head blocker exposed by the required migration.

The narrow repair recognizes an inline mapping only for a colon followed by
whitespace or end-of-value. Regression coverage must prove `ARGS:foo.` remains
a string and preserve the existing `- name: Content-Type` mapping control.
Focused parser and common-structure checks, real fallback-parser materialization,
the complete native lint suite, and the sealed follow-up security-diff scan now
pass. The finding is locally `fixed`; fresh hosted exact-current-head evidence
is still required before a verified delivery disposition.

## Validation and history

- The former failure is retained at GitHub Actions run `29774954997`, job
  `88461999826`; the valid `ARGS:foo.` item had been parsed as a dictionary.
- The refined separator predicate preserved both `ARGS:foo.` as a scalar and
  the legitimate `name: Content-Type` inline mapping in focused tests and the
  real test-common CLI materialization.
- The sealed follow-up scan report is
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T180337Z-framework-python-313-updater-f3349a7e/analysis/codex-security-scans/ModSecurity-test-Framework/4a31df0_remediation_followup_20260720T210011Z/report.md`
  with SHA-256 `be92a7e65c3c81e72140b5441494eb4461df4417ee361c344bd3d0cf56775a5c`.
- 2026-07-20T21:12:33Z — status changed to `fixed` after local parser,
  workflow, and security validation. The remediated commit still needs
  current-head hosted common-structure and the remaining required PR gates;
  no merge, Parent gitlink update, or MRTS action is authorized.
