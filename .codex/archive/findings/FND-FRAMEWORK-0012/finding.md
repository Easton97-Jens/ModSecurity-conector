# FND-FRAMEWORK-0012 — Framework CI lacked enforceable security-scanner and workflow-evidence coverage

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0012` |
| Category | `security_hardening` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P2` / `not_applicable` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary

The original Framework CI-security checks established immutable pins and basic
workflow structure but did not semantically prove that required scanner and
evidence commands were executable on the intended PR path.

## Evidence

- Run ID: `20260718T084030Z-expand-framework-ci-security-be8fb24d`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T084030Z-expand-framework-ci-security-be8fb24d/evidence/final-framework-ci-security-local-validation.md`
- Type: `final_local_ci_security_validation`; SHA-256:
  `979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`
- Validation: exact local Framework HEAD `15e9a034e929fc56bd77c92d783ca2637042e24e`
  passed `make lint`, 64 CI-security tests, semantic contract, locked Ruff,
  actionlint, and zizmor controls.

## Remediation and validation

`ci/checks/security/check-ci-security-evidence-contract.py` now validates
semantic workflow controls, exact checkout mappings, artifact/cache/SARIF
boundaries, and reachable required scanner commands. Regression tests cover
comments, dead control-flow bodies, direct exits, uncalled POSIX/Bash helpers,
and legitimate nested OSV helpers. The source remediation is committed as
`768a06b5b734547f8213cc6918c26ef4a8ef9f67`.

## Acceptance criteria

- Required scanner and evidence commands cannot be satisfied by comments,
  uncalled helpers, or recognized control-flow bodies.
- Legitimate current Framework workflows and their nested OSV helper flow pass.
- Exact final PR-head CI and review evidence confirms the committed control.

## Residual risk and history

The local fix is verified; remote exact-head CI, SonarQube Cloud, review, and
thread evidence remain pending the normal push. `2026-07-18T15:18:00Z`:
created and locally fixed with retained validation evidence.
