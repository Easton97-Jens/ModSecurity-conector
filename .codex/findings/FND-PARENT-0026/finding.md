# FND-PARENT-0026 — Runtime path policy trusts caller-controlled project roots as confinement anchors

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0026 |
| Title / Titel | Runtime path policy trusts caller-controlled project roots as confinement anchors |
| Category / Kategorie | security_hardening |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P2 |
| Severity / Schweregrad | medium |
| Confidence / Konfidenz | reproduced |
| Status | fixed |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

Runtime path helpers accepted mutable project-root values as trusted
containment anchors. Setting them to `/` made descendants of `/etc` and
`/root` runtime-allowed; the lifecycle resolver also accepted broad
`/root/poc-*` bases.

## Observed behavior / Beobachtetes Verhalten

`ci/lib/runtime_path_utils.py:50-98` derives trusted roots from mutable
environment inputs. A side-effect-free probe classified `/etc/evidence-escape`
and `/root/evidence-escape` as allowed when project roots were `/`. The
lifecycle resolver accepted five `/root/poc-*` bases without writing.

## Expected behavior / Erwartetes Verhalten

Project roots cannot declassify arbitrary system-path descendants. Invocation-
owned runtime bases must be canonical safe children of a validated external
task root, while source roots remain separate read-only inputs.

## Impact / Auswirkung

A local or future caller that controls path inputs can bypass intended
containment and direct lifecycle artifacts toward broad system-user locations.
Current workflows bind roots to runner temporary locations, so untrusted
pull-request expression reachability was not proven.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/common/resolve-runtime-paths.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/checks/evidence/check-runtime-producer-readiness.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_runtime_path_policy.py`
- `tests/test_resolve_runtime_paths.py`
- `tests/test_runtime_producer_readiness_path_policy.py`

### Symbols / Symbole

- `runtime_path_allowed`
- `resolve_runtime_paths`
- `REPO_ROOT`
- `CONNECTOR_ROOT`
- `FRAMEWORK_ROOT`

### Provenance / Herkunft

- Source commits: `46f35ad40822081e5b4c8d5c120dd41e2a74344f`,
  `614c80493b6ebd25a17e1d27979071e5e30584d4`
- Flow: caller-controlled project roots → positive helper containment decision
  → lifecycle resolver → later runtime artifact writes.

## Preconditions / Voraussetzungen

- A caller can provide project or lifecycle root inputs.
- The helper/resolver is used before a runtime artifact write.

## Reproduction / Reproduktion

1. Call the side-effect-free helper with `REPO_ROOT=/`, `CONNECTOR_ROOT=/`, and
   `FRAMEWORK_ROOT=/`; inspect `/etc/evidence-escape` and
   `/root/evidence-escape`.
2. Run the lifecycle resolver with `/root/poc-*` bases and observe successful
   resolution without writes.
3. Use a distinct task-owned external root as the legitimate control.

## Evidence / Evidence

- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-003-path-confinement/validation_report.md`
  - Type: `codex_security_validation_report`; SHA-256:
    `f4468abc4b55ead3129e62093cbe85e3022800f5a99e903b6f0ad1e1c1a457f3`
  - Command: `rtk env PYTHONPATH=/root/git/ModSecurity-conector/ci/lib
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python <side-effect-free path probe>`;
    resolver probes are retained with the report.
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed `2026-07-18T09:22:02Z`; retention:
    `retained_task_evidence`.

- Delivery evidence:
  - Draft PR: `58` (`agent/harden-evidence-path-confinement`); exact head:
    `4f028f911807def8b771faaa3b16c58a513e0385`.
  - Retained delivery artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
    (`draft_pr_delivery_status`, SHA-256
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`).
  - `rtk gh pr checks 58 --repo Easton97-Jens/ModSecurity-conector` exited
    `0` at `2026-07-18T11:13:55Z`: `33` checks passed; CodeQL check run
    `88072083077` and SonarCloud check run `88072115412` passed.
- Focused security-review evidence:
  `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/security_diff_review.md`
  reviewed the same exact head and recorded no new actionable diff-specific
  finding.

## Root-cause analysis / Grundursachenanalyse

The policy uses caller-controlled project roots as positive authorization
anchors instead of constraining writable runtime paths to one invocation-owned
external root.

## Proposed remediation / Vorgeschlagene Remediation

Reject broad/system bases and environment-derived project roots for writable
runtime paths. Resolve each writable lifecycle base against a validated
invocation root; retain explicit read-only source-root handling separately.

## Remediation update / Remediation-Update

- PR `58` (`agent/harden-evidence-path-confinement`) at exact head
  `4f028f911807def8b771faaa3b16c58a513e0385` follows commits
  `1ee0ba3718ef35c210ed959988460d03db21d46c` and
  `4f028f911807def8b771faaa3b16c58a513e0385` and confines writable runtime
  paths to the validated invocation root.
- Focused runtime-path tests passed `13`; shell syntax and diff checks passed.
  The full runtime-path policy shell half is blocked only because
  `modules/ModSecurity-test-Framework/ci/lib/common.sh` is absent from the
  isolated Parent worktree; no Framework content was changed or bypassed.
- The focused security diff review found no new actionable diff-specific
  finding. This finding is `fixed`, not `verified` or `closed`: no merge and
  no master rerun occurred.

## Acceptance criteria / Akzeptanzkriterien

- `/`, `/etc`, `/root`, and their descendants cannot become writable runtime
  roots through project-root values.
- Symlink, traversal, and mixed-root escapes fail closed after canonicalization.
- A distinct safe run layout below the task-owned external root remains
  accepted.
- Current workflow-owned runner temporary layouts remain supported.

## Validation plan / Validierungsplan

- Add broad-root and path-escape fixtures before the source fix, including a
  lexical traversal/symlink alternative.
- Run helper and lifecycle-resolver negative/control tests without writing to
  system paths.
- Run focused runtime-path and lifecycle suites plus a security diff scan.

## Regression tests / Regressionstests

- Focused `runtime_path_utils` tests for broad project-root rejection.
- Focused `resolve-runtime-paths` tests for canonical task-root containment.

## Legitimate control tests / Legitime Kontrolltests

- A safe connector run layout below a task-owned external root resolves
  successfully.
- Read-only project-source paths remain usable where explicitly required.

## Dependencies / Abhängigkeiten

- None.

## Blockers / Blocker

- None for the isolated Parent hardening change.

## Related findings / Verwandte Findings

- None.

## Residual risk / Restrisiko

PR `58` exact head `4f028f911807def8b771faaa3b16c58a513e0385` passed `33`
checks, CodeQL, SonarCloud, focused negative controls, and security review.
The full local shell-policy half remains blocked by absent
`modules/ModSecurity-test-Framework/ci/lib/common.sh` in the isolated Parent
worktree; no Framework content was changed. No merge or master rerun occurred.
The finding remains `fixed`, not `verified` or `closed`, and no risk has been
accepted.

## History / Historie

- `2026-07-18T09:22:02Z`: `validated_side_effect_free_path_escape` —
  controlled root values bypassed helper containment for system-path descendants;
  current PR-expression reachability was not established.
- `2026-07-18T11:13:55Z`: `fixed_on_verified_pr_head` — PR `58` exact head
  `4f028f911807def8b771faaa3b16c58a513e0385` passed `33` GitHub checks,
  CodeQL, SonarCloud, focused negative/control tests, and security review. The
  finding remains `fixed` rather than `verified` or `closed` until merge and
  master rerun.
- `2026-07-18T11:51:43Z`: `corrected_affected_file_provenance` —
  corrected the non-existent
  `ci/runtime/lifecycle/resolve-runtime-paths.py` path to
  `ci/runtime/common/resolve-runtime-paths.py` and recorded the actual
  Parent checks and focused test files from PR `58`.
