# FND-PARENT-0030 — Strict report-evidence gate accepts missing and hash-inconsistent runtime results

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0030 |
| Title / Titel | Strict report-evidence gate accepts missing and hash-inconsistent runtime results |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P1 |
| Severity / Schweregrad | high |
| Confidence / Konfidenz | reproduced |
| Status | closed (archived) — current-user closure after unchanged-path revalidation |
| Final disposition / Enddisposition | `closed_by_current_user_after_current_master_unchanged_evidence_integrity_validation` |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

The strict verified-report evidence gate formerly accepted critical `missing` input status and did not recompute declared output hashes or byte counts. The isolated Parent remediation rejects unverified and malformed status schemas, derives and verifies the canonical twelve-cell artifact chain, and preserves the source fields it verifies. Exact PR #59 source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` passed all non-skipped required CI, CodeQL, and SonarQube Cloud Quality Gate checks before merge, with zero submitted reviews, review requests, and review threads. The protected-squash Parent `master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` source tree matches the source head. Retained detached-master post-merge validation passed the 57/57 evidence-integrity suite, bilingual 11/11, shell syntax, and `git diff --check`. This finding is `verified`, never `closed` or risk-accepted. A separate detached-producer-receipt finding is tracked as `FND-PARENT-0031`.

## Observed behavior / Beobachtetes Verhalten

On `verified-report-governance.yml:49` → `Makefile:392` → `check-generated-report-layout.py`, critical refresh records `full_runtime_matrix`, `full_matrix_job_completeness`, and `verified_runtime_mismatch_analysis` have `input_status=missing`, but strict output does not name them. The verified-run manifest declares `full-runtime-matrix.generated.json` as SHA-256 `e3510bad867fdcf97ee0892378b608c484c081b568334b85f55784354d103711`, 12419 bytes; the actual file is SHA-256 `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007`, 12418 bytes, with no strict mismatch error. The current PR #59 fixture also showed that `BUILD_ROOT:../outside-runtime.json`, `framework:../outside-runtime.json`, and `../outside-runtime.json` each accepted a matching hash for an external regular file. Governance-only passes; strict fails only for unrelated stale reports.

## Expected behavior / Erwartetes Verhalten

Strict acceptance requires a valid run ID, detached command receipt, complete twelve-cell raw runtime matrix, job-local regular artifact paths, matching connector/profile/run identity, and newly computed hashes and byte counts. Claimed critical-input paths and trusted roots are normalized before containment comparison, while leaf and intermediate symlink rejection remains explicit. All non-verified critical states fail closed; a dashboard or report name cannot create runtime authenticity.

## Impact / Auswirkung

A forged or copied report/manifest can make derived diagnostics look complete without proving the matching raw runtime run, artifact chain, checksum, connector, or profile. A forged critical-input receipt could additionally make an external regular file appear trusted through lexical traversal and a known digest. The FND-PARENT-0024 workflow wiring is correct, but its strict gate must enforce this result-file boundary.

## Affected files and symbols / Betroffene Dateien und Symbole

- `ci/checks/documentation/check-generated-report-layout.py` — `check_manifest`, `check_critical_report_run_consistency`, `validate_critical_input_records`, `trusted_input_roots`, `input_root_for_path`, `is_within`, `has_symlink_component`, `check_verified_runtime_diagnostics`, and `check_verified_runtime_artifact_chain`.
- `ci/evidence/reports/generate-full-matrix-job-completeness.py` — `rewrite_manifest`; `ci/evidence/reports/refresh-connector-reports.py` — `build_governance_record`.
- `ci/runtime/lifecycle/run-full-matrix-parallel.sh` and `ci/runtime/lifecycle/run-verified-report-run.py` — canonical job producer and `generated_output_records`.
- Source commits: `1e0c825de82d1325b5e7b070a4916de2f5af2207` and `dd6e0455c4838949ce86cff81ce89dccd4e524f8`; protected PR #59 source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`; protected-squash Parent `master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`.

## Evidence / Evidence

- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`.
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/FND-PARENT-0030-result-file-authenticity/strict-gate-pre-fix-analysis.json`.
- Type: `strict_gate_result_authenticity_validation`; SHA-256: `9a5def690f41d36ae5fd63a7dd0c95e08803d25f7dd4c1f005a9e84de3bcc0f5`.
- Strict and governance-only checks were observed on 2026-07-18 UTC. Strict reported stale reports but omitted the named missing/hash/byte cases; governance-only passed.
- Post-fix artifact: `.../FND-PARENT-0030-result-file-authenticity/post-fix-validation.json`, SHA-256 `49e9463ca746524cacb82e8355a488a2caec8c32b6b2a22d6d474741582e24ea`; the 25 focused negative/control tests, shell syntax, in-memory compilation, and diff check passed. The strict retained-evidence control now fails closed; governance-only still passes without asserting runtime evidence.
- PR #59 containment artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260719T134234Z-pr59-containment-evidence-61aae959/evidence/pr59-critical-input-containment-validation.md`, run `20260719T134234Z-pr59-containment-evidence-61aae959`, SHA-256 `6f79cc322e568d8943434db95abd98caa5d6ad37dc06f2df7a6b468f8d41f1f3`. The pre-fix fixture failed as expected for all three traversal forms; after normalization the focused 32-test suite, the 11-test bilingual-doc suite, and `git diff --check` passed.
- Final PR #59 exact-head scan artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260719T141048Z-pr59-final-security-diff-98aafaa7/evidence/pr59-final-security-diff-report.md`, run `20260719T141048Z-pr59-final-security-diff-98aafaa7`, SHA-256 `2a37f50ff38fca2613fe2851d54463b41f121fd88d806b80f90cb439676ed369`. The sealed scan covers all ten final `aabde81..fb9becc` diff rows and reports no new reportable security finding.
- Current PR #59 exact-head artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr59-d4-current-head-verification.md`, run `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`, type `pr59_d4_current_head_verification`, SHA-256 `38e88188683330e57704bb3d4559c5604dbea303c1f305fb17e695545267107d`. At `d4f88b886dac6fd5f483940015d6310bc239f814`, `gh pr checks`, exact-head check-run and CodeQL-alert queries observed 33 successful runs, 6 expected skips, no failed/pending/cancelled runs, active required contexts succeeding, CodeQL with 0 open alerts, and a passing SonarQube Cloud Quality Gate. SonarQube Cloud's automated comment reported 9 new issues and 0 security hotspots; it is not a human review. The same artifact records 0 submitted reviews, 0 review requests, and 0 review threads, plus a passing local exact-diff check with no Framework, MRTS, or gitlink path. Focused controls cover paired mutable result/job/raw forgery, raw-only rewrite, receipt symlinks, deterministic intermediate-read and verified-runs-publication swaps, post-validation swaps, foreign-run selection, the complete twelve-cell control, and the owner-read-only `0400` assertion.
- Post-merge verification: run ID `20260720T141403Z-pr55-pr59-master-integration-8a0b8640`; artifact `/var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-5a22cbf-postmerge-validation.json`; type `pr59_protected_squash_merge_postmerge_security_finding_verification`; SHA-256 `7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51`; command: `Protected PR #59 squash merge with --match-head-commit from exact source head b9b22cc36958ba506278f3aa3fbc1d383ea6a151 to Parent master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188; retained detached-master validation runs the 57/57 evidence-integrity suite, including valid full-matrix and forged identity/result/path/symlink/hash/seal/swap controls, plus bilingual 11/11, shell syntax, git diff --check, and clean/no-.pyc checks.` Working directory `/root/git/ModSecurity-conector`; exit code `0`; observed at `2026-07-20T15:09:01Z`; retention status `retained_task_evidence`. Before merge, source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` passed all non-skipped required CI, CodeQL, and SonarQube Cloud Quality Gate checks with zero submitted reviews, review requests, and review threads. The post-merge Parent `master` source tree matches the source head.

## Root-cause analysis / Grundursachenanalyse

The strict consumer validated selected derived-report status claims and file existence. It rejected only `stale`/`blocked`, did not require list-typed aggregate status fields, did not recompute detached artifact hashes, and did not validate the raw full-matrix job chain. The producer manifest rewrite also lost identity and hash fields needed for a consumer verifier. The PR #59 `present`-input guard additionally compared `.absolute()` lexical paths after `resolve_input_reference()` preserved `..`, allowing logical containment to disagree with the physical target. The repaired mutable chain still requires a separate Parent-generated aggregate seal against synchronized receipt rewriting (`FND-PARENT-0031`).

## Proposed remediation / Vorgeschlagene Remediation

The isolated Parent branch now provides a strict verifier that starts at a validated run ID and detached command receipt, derives expected twelve-cell raw job paths rather than trusting report paths, validates identity/status/schema and regular job-local artifacts, recomputes hashes and sizes, rejects leaf and intermediate symlinks, and accepts only allowlisted list-typed critical status records. It normalizes claimed critical-input paths and trusted roots before containment comparison. It preserves raw evidence fields and emits typed refresh arrays. Exclude self-generated manifest records from detached hash checks. Do not change #55, Framework, MRTS, or generated reports by hand. Deliver a detached aggregate producer receipt only through the separate `FND-PARENT-0031` branch.

## Acceptance criteria / Akzeptanzkriterien

- Strict mode rejects missing runtime manifests, foreign run IDs, copied connector/profile records, unsafe paths, checksum/byte mismatches, and incomplete matrix jobs.
- A complete twelve-cell canonical Parent run with matching hashes and identity passes the focused verifier.
- Derived reports cannot create authenticity; all critical non-verified states fail closed in strict mode.
- `BUILD_ROOT:`, `framework:`, and unprefixed lexical parent traversal fail closed even when an external regular file has the declared digest; a matching in-root receipt remains accepted.
- Self-generated manifests are excluded or use an explicit detached receipt; no self-reference is treated as proof.
- FND-PARENT-0024 workflow wiring remains unchanged, with no Framework/MRTS change, suppression, or merge.

## Validation plan / Validierungsplan

1. Add temporary fixture builders before the source fix.
2. Test missing manifest, checksum/byte tamper, incomplete job, foreign run, copied connector/profile, `BUILD_ROOT:`/`framework:`/unprefixed parent traversal, path escape, and a full valid control.
3. Completed: exact PR #59 source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` passed all non-skipped required CI, CodeQL, and SonarQube Cloud Quality Gate checks with zero submitted reviews, review requests, and review threads. Protected squash merge produced Parent `master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`, whose source tree matches the source head; retained detached-master validation passed 57/57 integrity controls, bilingual 11/11, shell syntax, `git diff --check`, and clean/no-`.pyc` checks.
4. Keep `FND-CROSS-0001` as an expected end-to-end strict-gate blocker; never weaken this verifier. The `FND-SONAR-0001` global `master` error is independent of this verification and is neither accepted nor suppressed.

## Related findings / Verwandte Findings

- `FND-PARENT-0024` — workflow selection of strict vs. governance-only gate.
- `FND-PARENT-0031` — missing detached Parent producer receipt for synchronized mutable artifact rewrites.
- `FND-CROSS-0001` — stale Cross runtime evidence remains a separate blocker.
- `FND-SONAR-0001` — independent global `master` error; neither accepted nor suppressed by this verification.

## Residual risk / Restrisiko

This finding is `verified` on Parent `master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` after protected PR #59 source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` and post-merge original-reproduction plus legitimate-control validation. It is not `closed` or risk-accepted. The receipt chain is not a signature, ACL, process-identity, UID-isolation, or external-attestation boundary: mode `0400` limits group/other access only, while an actor with arbitrary same-UID write access to the Parent evidence namespace remains outside this local filesystem trust model. `FND-PARENT-0031` is separately verified; `FND-CROSS-0001` remains an independent stale-Cross-evidence condition and does not reopen this verified finding. The `FND-SONAR-0001` global `master` error is independent of this verification and is neither accepted nor suppressed. No risk is accepted.

## Closure / Abschluss

The current user authorized closure and archival. The affected paths are unchanged through Parent master `6ca7e1536ce7e93da68099db9c586b88852ff13e`, and `tests.test_generated_report_evidence_integrity` passed in the 144-test control suite.

## History / Historie

- `2026-07-18T12:50:18Z`: `validated_strict_result_file_authenticity_gap` — direct strict/governance executions and canonical manifest comparison confirmed omitted missing-input and hash/byte mismatch errors. #55 remains unchanged; isolated Parent fixture-first remediation is next.
- `2026-07-18T13:53:55Z`: `fixture_first_remediation_locally_validated` — 25 focused negative/control tests reject forged checksum/PASS content, missing/raw/foreign/incomplete/copy/path/schema cases and retain a valid twelve-cell control. The retained strict check now fails closed; governance-only remains non-runtime evidence. Independent review allocated synchronized mutable receipt rewriting to separate `FND-PARENT-0031`.
- `2026-07-19T10:00:00Z`: `pr59_revalidation_found_unverified_present_input_receipts` — a focused PR #59 diff review confirmed that the strict status allowlist still accepted a nonexistent or substituted critical input when metadata self-declared `present`. The local correction now requires a trusted regular file and matching SHA-256; missing, empty, symlink, and digest-mismatch controls plus a legitimate control passed in the focused suite. `FND-PARENT-0031` remains separate and open; no finding is closed or risk accepted.
- `2026-07-19T13:43:18Z`: `pr59_lexical_parent_traversal_reproduced_and_locally_fixed` — `BUILD_ROOT:`, `framework:`, and unprefixed `../...` receipts each accepted a correctly hashed external regular file because `.absolute()` preserved lexical traversal. The narrow `resolve(strict=False)` containment fix retains symlink rejection; 32 focused tests cover original/alternate traversal, digest mismatch, summary/JSONL fallback, and a legitimate in-root receipt. Delivery and master verification remain pending.
- `2026-07-19T14:19:05Z`: `pr59_final_synchronized_security_diff_scan_completed` — the bounded correction is committed as `fcdf9b2479486ad25c1e4bd4f28556b9339a1287`, normally synchronized with master `aabde81a9a315bf3e494e595ab0399357c596f9c`, and pushed at exact head `fb9becc76f903d68fa36c212cc60940a5e6e20c5`. The sealed final scan covers all ten diff rows and finds no new reportable issue. Remote checks, reviews, SonarCloud, merge, and resulting-master verification remain pending.
- `2026-07-20T09:57:03Z`: `pr59_d4_current_head_fixed_pending_master_sync_and_post_merge_reproduction` — retained artifact SHA-256 `38e88188683330e57704bb3d4559c5604dbea303c1f305fb17e695545267107d` verifies PR #59 exact head `d4f88b886dac6fd5f483940015d6310bc239f814`: 33 successful checks, 6 expected skips, successful active required contexts, CodeQL with 0 open alerts, a passing SonarQube Cloud Quality Gate, 0 submitted reviews/requests/threads, and a passing local exact-diff check. The PR is still Draft and two commits behind Parent `master` `9ef0619b9c00729c16b7056943d7843785223095`; the finding is therefore `fixed`, not verified or closed, pending normal synchronization, fresh exact-head validation, authorized merge, and post-merge original reproduction.
- `2026-07-20T15:09:01Z`: `verified_on_protected_pr59_squash_merge_parent_master` — exact source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` passed all non-skipped PR #59 checks, required protected contexts, CodeQL, SonarQube Cloud Quality Gate, issue query, and zero-review/thread controls. Matching remote refs were protected-squash-merged with `--match-head-commit` as Parent `master` `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`; its source tree matches the source head. Retained detached-master evidence records 57/57 integrity controls, including original forged identity/result/path/symlink/hash/seal/swap reproductions failing closed and a valid full-matrix control passing, plus bilingual 11/11, shell syntax, diff, and clean/no-`.pyc`. The finding transitions `fixed` to `verified`, never `closed`; its own release blocker is `false` and no risk is accepted. The `FND-SONAR-0001` global `master` error is independent and neither accepted nor suppressed.
