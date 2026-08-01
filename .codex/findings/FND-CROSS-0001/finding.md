# FND-CROSS-0001 — Evidence freshness manifest contains stale entries and SHA mismatches

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-CROSS-0001` |
| Title / Titel | `Evidence freshness manifest contains stale entries and SHA mismatches` |
| Category / Kategorie | `evidence_gap` |
| Repository / Repository | `parent_and_framework` |
| Ownership / Ownership | `cross_repository` |
| Priority / Priorität | `P0` |
| Severity / Severity | `low` |
| Confidence / Confidence | `confirmed` |
| Status | `validated` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The assessment recorded 58 stale entries and 9 SHA mismatches in freshness evidence.

Current state (`2026-07-26T18:27:22Z`): Parent PR #74 needs a newly hosted,
descriptor-staged, payload-safe retained machine-readable chain before this P0
finding can advance. The pre-retention producer had no artifact upload. Its
first published successor (`881a6bccf0a324ead467ced47b64514164b00981`) was
not accepted because pathname checks did not bind the later upload action; its
two runs were cancelled before upload and produced no artifact.

## Observed behavior / Beobachtetes Verhalten

The assessment recorded 58 stale entries and 9 SHA mismatches in freshness
evidence. Parent PR #74's original hosted workflow generated the structured
chain but did not retain it after runner teardown. The first retention
successor could also have followed a later replacement path outside its
intended allowlist.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against known Parent and Framework revisions,
copied through a descriptor-safe staged allowlist, bound to the final strict
gate, and retained as a payload-safe machine-readable artifact before this
finding can advance beyond `validated`.

## Impact / Auswirkung

Release and assurance claims remain bounded by the recorded evidence. An
unbound pathname upload could retain content outside the intended structured
allowlist as well as fail to establish the required freshness chain.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `.github/workflows/verified-report-governance.yml`
- `ci/checks/common/check-python-version-contract.py`
- `ci/evidence/reports/stage-verified-full-matrix-evidence.py`
- `ci/lib/verified_full_matrix_receipt.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_generated_report_evidence_integrity.py`
- `tests/test_python_version_contract.py`

### Symbols / Symbole

- None / Keine

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '204,230p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:204-230`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '204,230p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
  - Type: `strict_runtime_evidence_gate_failure`; SHA-256:
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`
  - Command: `rtk gh pr checks 55 --repo Easton97-Jens/ModSecurity-conector`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `1`
  - Observed at: `2026-07-18T11:13:55Z`; retention:
    `retained_task_evidence`
- Run ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-current-master-transfer-revalidation.md`
  - Type: `framework_current_master_validation_prerequisite_blocker`; SHA-256:
    `067db2ef9c429fa405737d193aa7a7fa5751c158b4d0ffdddbc6667918ce3ed6`
  - Command: `rtk proxy test -x /var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/tmp/framework-current-master-worktree/.venv/bin/python`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `1`
  - Observed at: `2026-07-20T22:18:23Z`; retention:
    `retained_task_evidence`
- Run ID: `20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T201536Z-pr55-runtime-snapshot-revalidation-20f91607/evidence/framework-current-master-python-environment-preflight.md`
  - Type: `framework_ci_python_and_dependency_contract_blocker`; SHA-256:
    `7491f9abd99c80e0c2c16b2ba2d3ef4ec5a21e4e93ea7ea272bb0d6b4e6f5082`
  - Command: `rtk proxy /usr/bin/python3.14 --version`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-21T04:22:56Z`; retention:
    `retained_task_evidence`

- Run ID: 20260721T055738Z-framework-pr39-delivery-followup-416b152c
  - Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-cpython313-validation.md
  - Type: framework_pr39_cpython31314_local_qualification; SHA-256:
    2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30
  - Command: Framework PR #39 CPython 3.13.14 qualification receipt: hash-locked PyYAML-6.0.3 installation and pip check; 30 direct affected tests; make test-ci-security-contract (89 tests); make check-python-version; make check-github-actions-workflows; make test-workflow-security-contract (7 tests); make check-documentation; python -m compileall -q ci tests; worktree-scoped response-body guard; make lint.
  - Working directory: framework-python-updater; exit code: 0
  - Observed at: 2026-07-21T06:13:56Z; retention: retained

This receipt supersedes only the PR #39 local CPython environment premise. It
does not rerun or reconcile the original 58 stale entries and 9 SHA mismatches.

- Run ID: `20260726T171724Z-pr74-hosted-evidence-retention`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T171724Z-pr74-hosted-evidence-retention/evidence/pr74-hosted-evidence-retention-preflight.md`
  - Type: `hosted_runtime_evidence_retention_gap_preflight`; SHA-256:
    `3e5c1580b2e7765782cc83dae6122318aac97a26b7ac7b8c32d8d55f007bbcf3`
  - Command: artifact-inventory readback for hosted PR/push runs
    `30210885288` and `30210883722`, plus exact-head readback for
    `30210885288`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-26T17:17:24Z`; retention:
    `retained_task_evidence`
  - Both active exact-head runs reported an artifact count of `0`.
- Run ID: `20260726T171724Z-pr74-hosted-evidence-retention`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T171724Z-pr74-hosted-evidence-retention/evidence/pr74-artifact-retention-security-correction.md`
  - Type: `payload_safe_artifact_retention_security_correction`; SHA-256:
    `1c980e2b3de51b08144ae33fd534f882264780bc5fd4b22ce15689bb640bae5a`
  - Command: focused descriptor-staging, workflow-security, and Python-contract
    validation of the local successor to published PR #74 head
    `881a6bccf0a324ead467ced47b64514164b00981`
  - Working directory:
    `/var/tmp/codex/worktrees/parent/migrate-pr55-pr74-master-V27zuA/pr74`;
    exit code: `0`
  - Observed at: `2026-07-26T18:27:22Z`; retention:
    `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a
product-code root cause. The Parent strict report gate correctly rejects the
unresolved stale or mismatched runtime evidence instead of converting
governance validation into runtime proof.

The hosted producer also needed an explicit payload-safe export: its generated
manifests and receipts are valid only inside the ephemeral runner unless the
workflow retains an allowlisted structured artifact after the strict gate. The
first export attempted pathname checks, but those checks did not bind
`actions/upload-artifact` to the checked source objects.

## Proposed remediation / Vorgeschlagene Remediation

Regenerate and reconcile revision-bound evidence, retain a descriptor-staged
machine-readable manifest chain, and keep the strict report gate failing
closed on an unresolved SHA mismatch or a changed staged source.

The successor workflow must retain only the three manifest JSON files, current
run command/aggregate receipts, raw matrix index, and twelve job JSON records;
it must exclude build trees, logs, `run.log`, result JSONL, request/response
payloads, headers, and cookies.

## Acceptance criteria / Akzeptanzkriterien

- Every retained assessment claim is tied to the current Parent and Framework revisions.
- The freshness manifest reports no unexplained stale entry or SHA mismatch.
- The exact hosted upload contains only the fixed eighteen-file staged
  allowlist and its final byte/digest binding to the strict-gate source set.

## Validation plan / Validierungsplan

- Regenerate the freshness manifest at the target revisions.
- Verify each report/reference SHA and retain the raw machine-readable result.
- Download the exact-head success-only artifact and verify one matching run ID,
  Parent/Framework revisions, declared hashes, and all twelve structured
  full-matrix job records, plus the staged allowlist's exact path set.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.
- `tests.test_ci_security_workflows` requires a post-gate, SHA/run-bound,
  payload-safe staged artifact allowlist and rejects log/result-payload paths.
- `tests.test_generated_report_evidence_integrity` rejects intermediate/final
  source symlinks, source mutation/replacement, unsafe staging parents, reused
  staging roots, and post-stage source changes while retaining the legitimate
  18-file control.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.
- A successful exact-head strict producer must upload the staged allowlisted
  structured records without broadening workflow permissions or retaining
  runtime payloads.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- Fresh Parent and Framework evidence and a regenerated freshness manifest have
  not been produced; the original 58 stale entries and 9 SHA mismatches remain
  unresolved.
- The retained `2026-07-21T04:22:56Z` current-master candidate preflight
  remains evidence for that separate candidate, but the
  `2026-07-21T06:13:56Z` Framework PR #39 CPython 3.13.14 receipt does not
  revalidate that candidate or mint the fresh Parent runtime evidence required
  by this finding.
- Exact Parent PR #74 head `77bd39e64194cf5e6d221d874d9c6924549711eb` had
  pre-retention hosted producers with no artifact inventory. Published successor
  `881a6bccf0a324ead467ced47b64514164b00981` was unsafe and both of its runs
  were cancelled before upload. The uncommitted descriptor-staging successor
  must be committed, pass the strict producer, and retain its bound structured
  evidence before freshness can be reconciled.

## Related findings / Verwandte Findings

- `FND-CROSS-0002`
- `FND-CROSS-0005`
- `FND-PARENT-0037`

## Residual risk / Restrisiko

The condition remains open. PR 55 exact head
`42b31f1c84c0c915a5cb65119714613fbf3e0c40` correctly fails its strict
runtime-evidence gate because this freshness condition remains unresolved. No
risk has been accepted by the current user.

The current-master candidate transfer is retained and static checks passed,
but no fresh Parent runtime evidence or regenerated freshness manifest has
been minted. The later Framework PR #39 receipt proves its own
Framework-specific CPython 3.13.14 local qualification only; it does not
revalidate the separate current-master candidate and does not resolve the
original 58 stale entries or 9 SHA mismatches. No risk is accepted.

The pre-retention Parent PR #74 producers do not close this finding because
neither retains a raw artifact chain. Published successor
`881a6bccf0a324ead467ced47b64514164b00981` was cancelled before upload
because pathname checks did not safely bind it. The descriptor-staged snapshot
protects the normal runner boundary but cannot prevent an arbitrary surviving
same-UID process from modifying a runner path after the final comparison; a
separate identity or a descriptor/stream-consuming uploader would be stronger.
The successor must be published, pass, and have its artifact reconciled before
`validated` or `release_blocker: true` can change. No risk is accepted.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T11:13:55Z`:
  `strict_report_gate_correctly_rejected_stale_runtime_evidence` — Parent PR 55
  head `42b31f1c84c0c915a5cb65119714613fbf3e0c40` failed the strict
  runtime-evidence gate as designed, preserving this finding as `validated`
  rather than minting governance-only runtime evidence.
- `2026-07-20T22:18:23Z`:
  `current_framework_master_prerequisite_blocked_before_parent_runtime_rerun`
  — private current-master candidate
  `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b` received the reviewed
  prerequisite patch without path overlap and passed diff/shell checks; the
  retained report SHA-256 is
  `067db2ef9c429fa405737d193aa7a7fa5751c158b4d0ffdddbc6667918ce3ed6`.
  Its required Framework `.venv/bin/python` is absent, so no system/Parent
  Python substitution, Framework PR, fresh Parent runtime evidence, or
  protected merge was performed.
- `2026-07-21T04:22:56Z`:
  `authorized_framework_environment_preflight_remains_blocked_on_ci_contract`
  — the user authorized a Framework-owned repository environment and dependency
  installation. Framework `master` and the candidate remained
  `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`, MRTS remained unchanged, and
  storage preflight allowed the estimated additional GiB. Retained preflight
  SHA-256 `7491f9abd99c80e0c2c16b2ba2d3ef4ec5a21e4e93ea7ea272bb0d6b4e6f5082`
  showed that all Framework CI workflows and `requirements-ci.lock` require
  CPython `3.13.14`, which is unavailable locally; only CPython `3.14.4` was
  found. `requirements-dev.txt` remains `PyYAML>=6,<7` and its bootstrap
  upgrades Pip. No `.venv`, package download, Framework PR, fresh Parent
  runtime evidence, or protected merge was performed.
- 2026-07-21T06:13:56Z:
  framework_pr39_environment_blocker_superseded_without_freshness_resolution
  — the retained receipt
  20260721T055738Z-framework-pr39-delivery-followup-416b152c, SHA-256
  2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30,
  establishes Framework PR #39 local CPython 3.13.14 qualification with
  hash-locked PyYAML-6.0.3, pip check, 30 direct affected tests, 89 make
  test-ci-security-contract tests, workflow and documentation checks, python
  -m compileall -q ci tests, the response-body guard, and make lint. It
  supersedes only the PR #39 local CPython environment blocker; it does not
  rerun or reconcile the original 58 stale entries and 9 SHA mismatches, so
  status remains `validated`.
- `2026-07-26T17:17:24Z`:
  `hosted_evidence_retention_gap_confirmed_and_remediation_prepared` — exact
  Parent PR #74 head `77bd39e64194cf5e6d221d874d9c6924549711eb` had active
  pull-request and push producers with artifact count `0`. The Parent-only
  remediation adds a success-only, SHA/run-bound, payload-safe allowlist after
  the unchanged strict gate. The successor exact head must publish and have
  that artifact reconciled before this P0 release blocker can advance.
- `2026-07-26T18:27:22Z`:
  `unbound_artifact_upload_corrected_with_descriptor_staging_and_fast_preflight`
  — independent review of published PR #74 head
  `881a6bccf0a324ead467ced47b64514164b00981` found a low/P3 pathname TOCTOU
  exposure; its two runs were cancelled before upload and produced no evidence.
  The local Parent-only successor stages all eighteen allowlisted records
  through descriptor-relative no-follow traversal, exclusive private staging,
  and a final strict-gate source binding. It also adds a 15-minute read-only
  contract preflight and cancels only superseded PR/ref runs while preserving
  the full producer. Local validation passed; exact-head hosted artifact,
  Sonar, and protection evidence remain required.
