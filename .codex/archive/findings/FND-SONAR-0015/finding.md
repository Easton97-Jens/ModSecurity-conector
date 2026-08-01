# FND-SONAR-0015 — Compile-database input reaches a file-read boundary without a private capture-root contract

## Classification

| Field | Value |
| --- | --- |
| Category | security_candidate |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / high / probable |
| Status / verification | closed (archived) / closed_by_current_user_after_current_master_compile_database_boundary_validation |
| Feasibility | feasible_now |
| Release blocker / security relevant | no / yes |
| Profile | Parent CI compilation-database ingestion |
| Delivery state | protected_squash_merged_resulting_master_workflows_verified |

## Summary

Before PR #98, non-verify CLI input could reach load_database(...).read_text after only a basic file check, without an explicit private capture-root provenance or containment contract. Exact head a2f2dd1f8bd2c433ee4cb107a0bf94281fbd7640 was protected-squash-merged as master 3311f3fd0e6dee01efc905e62f55bbdb3490ad20. All 14 applicable master-push workflows passed and the three targeted base Sonar keys are CLOSED/FIXED. The project-wide Quality Gate ERROR belongs to a separate baseline backlog and is not attributed to this remediation.

## Observed and expected behavior

At the pre-remediation base, --input could reach the JSON read sink with no capture-root binding. Sonar key AZ9dWiALxi9ITghe3pzq recorded a high-impact pythonsecurity:S8707 candidate. Current repository call sites are CI-owned Bear wrappers; no remote, cross-principal, or untrusted same-UID caller path is demonstrated.

The non-verify input must be an absolute existing regular file outside the checkout and below an absolute, non-symlinked external capture root owned by the effective user and inaccessible to group/other users. Root and input validation must occur before load_database reads JSON. A valid private capture must still be accepted.

## Impact and security assessment

Without the contract, a caller could make the CI helper parse an arbitrary readable file. The supported scope is a CI-local path-integrity candidate, not a proven remote exploit. The PR-specific security review found no validated high- or critical-impact regression in the remediation.

The boundary is --input and --capture-root through external_capture_root, external_capture_input_path and captured_database_entries to load_database and Path.read_text. The two non-verify wrappers create fresh private mktemp roots and pass fixed local files. A same-EUID replacement race was considered, but no distinct attacker-controlled writer in the private root is evidenced. The pre-existing output-path boundary is not changed by this PR and is outside this finding.

## Affected files and symbols

- ci/checks/analysis/compile_database.py — external_capture_root, external_capture_input_path, captured_database_entries, load_database, parse_arguments and main.
- ci/checks/analysis/compile-db-cpp17.sh and ci/checks/analysis/compile-db-nginx-c17.sh — pass the fresh private capture root.
- tests/test_c_cpp_diagnostics.py — regression and legitimate-control coverage.
- The paired Change Record and indexes.

## Preconditions and reproduction

The pre-remediation path requires a non-verify invocation with --input that reaches JSON parsing. Material security impact beyond the candidate scope would additionally require an untrusted caller or cross-principal write/read relationship.

Inspect the old non-verify flow to see --input reach load_database(...).read_text without capture-root validation. At the exact PR head, test missing root, relative input, checkout input, escape and loop symlinks, unsafe root permissions, root symlink and verify-only misuse; each must fail before parsing or publishing. A valid JSON file under a private 0700 capture root is the legitimate control.

## Evidence and limitations

- Task run 20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b observed seven focused tests in tests/test_c_cpp_diagnostics.py, eleven tests in tests/test_bilingual_docs.py, two wrapper shell syntax checks and git diff --check as passed at a2f2dd1f8bd2c433ee4cb107a0bf94281fbd7640.
- The exact head passed all six required GitHub checks, CodeQL, OSV, SonarCloud Code Analysis, report governance and other non-skipped PR checks. SonarCloud Quality Gate API returned OK.
- The PR issue query returned one issue, AZ-QC5_F7_w-jke5-e7_, and it is CLOSED/FIXED. After the protected merge, direct master-key lookup records AZ9dWiALxi9ITghe3pzq, AZ9dWiALxi9ITghe3pzp and AZ9dWiALxi9ITghe3pzo as CLOSED/FIXED at 2026-07-24T08:22:45Z.
- Tool output was observed in the task but no separate receipt file was retained. The focused suite does not run a full Bear/compiler capture integration.
- No remote exploit, cross-principal caller, or distinct untrusted same-UID writer was demonstrated.

## Root cause and proposed remediation

The old non-verify flow treated the CLI value as a file after only a basic file check. It did not bind it to a private external Bear capture root before the read sink.

PR #98 requires --capture-root with --input, validates root path class, ownership and permissions, resolves and confines the input, and passes only the validated path to load_database. The two CI wrappers retain their private mktemp capture flow. Do not weaken these checks or the legitimate private-capture control.

## Acceptance criteria and validation plan

1. Exact head a2f2dd1f8bd2c433ee4cb107a0bf94281fbd7640 rejects every listed unsafe root/input case before parsing or publishing and accepts the valid private capture.
2. The seven focused diagnostics tests, eleven bilingual documentation tests, two shell syntax checks, diff check, required checks, CodeQL, OSV, SonarCloud and Quality Gate pass without suppressions or control changes.
3. The PR was protected-squash-merged only at the exact checked head; resulting master 3311f3fd0e6dee01efc905e62f55bbdb3490ad20 and all 14 applicable master-push workflows passed.
4. Post-merge master Sonar analysis records the three base keys as CLOSED/FIXED.

The protected merge, master workflow and exact-key reanalysis plan is complete. Reassess only if this CI helper later becomes a supported cross-principal interface.

## Regression and legitimate-control tests

- tests/test_c_cpp_diagnostics.py — seven focused tests passed.
- tests/test_bilingual_docs.py — eleven tests passed for the Change Record pair.
- A valid JSON capture under a current-user-owned 0700 external root is accepted and published.
- Existing valid merge and verify behavior remains covered by the focused diagnostics suite.

## Dependencies, blockers and related findings

There is no Framework or MRTS dependency. Bear/compiler integration prerequisites are optional and were not needed for this focused boundary suite. There is no current delivery blocker; protected merge and master verification remain required evidence.

The separate pre-existing output-path boundary is not changed by this PR and is outside this finding. No canonical related-finding record is asserted from this worktree. There is no duplicate.

## Residual risk and history

The remediation is verified on the protected resulting master. A same-EUID TOCTOU candidate is not reportable on current evidence because no distinct untrusted writer can access the private root; reassess if the tool becomes a cross-principal interface. The separate project-wide Sonar Quality Gate ERROR remains tracked elsewhere.

- 2026-07-24T08:16:22Z: Canonical record created as fixed with exact-head validation pending protected merge and resulting-master evidence.
- 2026-07-24T08:28:09Z: PR #98 was protected-squash-merged as master 3311f3fd0e6dee01efc905e62f55bbdb3490ad20; all 14 applicable master-push workflows passed and the three targeted base keys are CLOSED/FIXED.
- 2026-07-26T14:09:02Z: Current user authorized closure and archival; the affected paths are unchanged through Parent master 6ca7e1536ce7e93da68099db9c586b88852ff13e and `tests.test_c_cpp_diagnostics` passed in the 144-test control suite.
