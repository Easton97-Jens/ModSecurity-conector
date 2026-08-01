# FND-PARENT-0025 — Allowed blocked status is derived from untrusted child output

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0025 |
| Title / Titel | Allowed blocked status is derived from untrusted child output |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P1 |
| Severity / Schweregrad | high |
| Confidence / Konfidenz | reproduced |
| Status | closed (archived) |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

The status wrapper parsed an allowlisted blocked-reason marker from combined
child stdout and stderr. A child that exited `77` could print that marker and
turn a failed check into a successful workflow result.

## Observed behavior / Beobachtetes Verhalten

`ci/tools/run-check-status.py:186-210` accepted `CHECK_STATUS_REASON` from
child output, and `workflow_exit_code` turned an allowlisted reason into exit
code `0`. Controlled stdout and stderr fixtures both produced
`allowed_by_contract=true` and workflow exit code `0`. The affected Make call
is `Makefile:1132-1134`.

## Expected behavior / Erwartetes Verhalten

Only a parent-verified prerequisite condition may produce an allowed blocked
disposition. Child output and exit codes remain diagnostics; they cannot
authorize successful workflow completion.

## Impact / Auswirkung

A compromised, faulty, or deliberately permissive child command could mask a
required check failure as an allowed environment block.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `ci/tools/run-check-status.py`
- `Makefile`

### Symbols / Symbole

- `extract_block_reason`
- `workflow_exit_code`
- `test-optional-prerequisite-status`

### Provenance / Herkunft

- Source commit: `57d8753bc9db93d42eeb8be806798c7b394a8076`
- Flow: controlled child stdout/stderr → `extract_block_reason` → allowlist →
  `workflow_exit_code` → successful Make/CI disposition.

## Preconditions / Voraussetzungen

- The wrapper allows `apache_development_prerequisite`.
- The executed child can emit stdout or stderr and exit `77`.

## Reproduction / Reproduktion

1. Run the retained stderr spoof fixture through `run-check-status.py` with the
   allowlisted reason.
2. Run the retained stdout spoof fixture through the same wrapper.
3. Observe structured blocked status with `allowed_by_contract=true` and
   wrapper exit code `0` in both cases.

## Evidence / Evidence

- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-002-status-channel/validation_report.md`
  - Type: `codex_security_validation_report`; SHA-256:
    `024f6956d07e3b787f1f4f1441bc107c4c9c15432a9337946a132262a7173218`
  - Command:
    `rtk env BUILD_ROOT=<task-run> PYTHONDONTWRITEBYTECODE=1 .venv/bin/python ci/tools/run-check-status.py --check status_spoof --allow-blocked-reason apache_development_prerequisite -- <controlled-fixture>`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed `2026-07-18T09:22:02Z`; retention:
    `retained_task_evidence`.

- Delivery evidence:
  - Draft PR: `56` (`agent/harden-evidence-status-channel`); exact head:
    `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92`.
  - Retained delivery artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
    (`draft_pr_delivery_status`, SHA-256
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`).
  - `rtk gh pr checks 56 --repo Easton97-Jens/ModSecurity-conector` exited
    `0` at `2026-07-18T11:13:55Z`: `33` checks passed; CodeQL check run
    `88070191900` and SonarCloud check run `88070221640` passed.
- Focused security-review evidence:
  `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/security_diff_review.md`
  reviewed the same exact head and recorded no new actionable diff-specific
  finding.
- Post-merge master verification:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T103749Z-parent-pr-53-60-integration-a7b98a59/evidence/pr56-master-verification-a73c335.md`
  (`post_merge_master_reproduction_and_workflow_verification`, SHA-256
  `2260f2573467879d7c105dddfb9c64395308b021e1eccec6e53f358fef7c2562`).

## Root-cause analysis / Grundursachenanalyse

The status channel treated free-form child diagnostics as authoritative control
data and joined those data with the allowlist decision.

## Proposed remediation / Vorgeschlagene Remediation

Move the allowed missing-prerequisite decision into an explicit parent-side
structured disposition and remove child-text authorization. Preserve arbitrary
child output only as escaped diagnostics; reject unclassified exit-`77`
results.

## Remediation update / Remediation-Update

- PR `56` final head `cd0211bbefd4baef4ddee300ccf872e4d1ad9a53` moves
  authorization of the allowed blocked disposition to parent-side structured
  preflight and was squash-merged as master
  `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f`.
- `origin/master` is exactly that commit and its tree equals the final PR head.
  `tests/test_optional_prerequisite_status.py` passed `20` focused original
  spoof, bypass, and legitimate-control tests; `allowed_by_contract=false`
  and a nonzero child exit `77` remain enforced for child-controlled output.
- The focused security diff review found no new actionable diff-specific
  finding. All 14 observed exact-master workflows, including CodeQL, Security
  workflow lint, OpenSSF Scorecard, and verified-report-governance, succeeded.
  This finding is `verified`, not `closed`.

## Acceptance criteria / Akzeptanzkriterien

- Neither stdout nor stderr marker text can change a child failure into an
  allowed blocked workflow result.
- A real parent-detected missing Apache development prerequisite remains an
  explicit, schema-valid blocked result.
- All other child failures, including exit `77`, remain nonzero.
- The persisted status record uses the parent disposition rather than untrusted
  child text as its reason field.

## Validation plan / Validierungsplan

- Add stdout and stderr spoof fixtures before the fix and show both fail after
  it.
- Exercise a parent-detected missing-prerequisite control and ordinary child
  failure control.
- Run the focused optional-prerequisite status suite and a security diff scan.

## Regression tests / Regressionstests

- `tests/test_optional_prerequisite_status.py`
- Focused stdout/stderr spoof fixtures for `run-check-status.py`.

## Legitimate control tests / Legitime Kontrolltests

- A genuine missing Apache development prerequisite produces a parent-
  authenticated allowed blocked status.
- A valid child command succeeds without relying on a status marker.

## Dependencies / Abhängigkeiten

- None.

## Blockers / Blocker

- None for the isolated Parent status-channel remediation.

## Related findings / Verwandte Findings

- `FND-PARENT-0024`

## Residual risk / Restrisiko

PR `56` final head `cd0211bbefd4baef4ddee300ccf872e4d1ad9a53` is merged as
master `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f`; the master tree equals the
final head, the original 20-test status-channel suite passes, and all observed
exact-master workflows pass. APXS selector configuration remains trusted
job/operator input; current production PR workflows do not route untrusted PR
input to it. Reassess if that trust boundary changes. No risk has been
accepted. The finding is `verified`, not `closed`.

## History / Historie

- `2026-07-18T09:22:02Z`: `validated_stdout_and_stderr_spoofing` —
  independent controlled stdout and stderr marker fixtures both received an
  allowed blocked workflow disposition.
- `2026-07-18T11:13:55Z`: `fixed_on_verified_pr_head` — PR `56` exact head
  `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92` passed local controls, `33`
  GitHub checks, CodeQL, SonarCloud, and focused security review. The finding
  remains `fixed` rather than `verified` or `closed` until merge and master
  rerun.
- `2026-07-19T11:42:54Z`: `current_master_reproduction_verified` — PR `56`
  merged as `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f`; its master tree equals
  final head `cd0211bbefd4baef4ddee300ccf872e4d1ad9a53`. The 20-test original
  spoof/bypass/legitimate-control suite and 13-test workflow-permission
  contract passed; all 14 observed exact-master workflows passed. The finding
  was `verified` and is now `closed` by the current user after current-master validation and archival authorization.

- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_validation` — `tests.test_optional_prerequisite_status` passed on Parent master `6ca7e1536ce7e93da68099db9c586b88852ff13e` as part of the 144-test control suite.
