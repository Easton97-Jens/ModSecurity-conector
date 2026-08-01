# FND-FRAMEWORK-0005 — PCRE2 archive digest can be unset before Framework extraction

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0005` |
| Title / Titel | `PCRE2 archive digest can be unset before Framework extraction` |
| Category / Kategorie | `security_validated` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `validated` |
| Status | `fixed` |
| Final disposition / Finale Disposition | `fixed_pending_framework_pr_verification` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The Framework PCRE2 source-archive path previously accepted an empty digest and could extract unverified bytes. The task branch now requires a reviewed SHA-256 literal before the real extraction sink and retains focused local proof.

## Observed behavior / Beobachtetes Verhalten

Before the fix, `PCRE2_SHA256` and `PCRE2_SHA256_URL` defaulted to empty and optional verification helpers returned successfully before extraction. After the fix, empty, whitespace-only, malformed, and mismatching `PCRE2_SHA256` values exit `77` before the PCRE2 archive reaches `tar`; the matching local fixture reaches the expected extraction path.

## Expected behavior / Erwartetes Verhalten

No PCRE2 archive may reach extraction or any later processing until a non-empty, syntactically valid, exactly matching SHA-256 digest has been verified.

## Impact / Auswirkung

The implemented control closes the previously optional archive-integrity boundary in the Framework PCRE2 provisioning path. Current-head PR verification remains blocked by the independent `FND-FRAMEWORK-0001` common-structure failure.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `modules/ModSecurity-test-Framework/ci/lib/common.sh`
- `modules/ModSecurity-test-Framework/ci/provisioning/prepare-apache-build.sh`
- `modules/ModSecurity-test-Framework/tests/security_regression/test_pcre2_archive_digest.py`
- `modules/ModSecurity-test-Framework/tests/fixtures/pcre2-digest/`

### Symbols / Symbole

- `PCRE2_SHA256`
- `verify_required_pcre2_sha256`
- `build_pcre2_from_source`
- `extract_tar_strip`

## Preconditions / Voraussetzungen

- The Framework Apache PCRE2 source-build path is invoked.
- A caller provides the PCRE2 archive source and may override `PCRE2_SHA256`.
- The retained assessment and task-run evidence remain available.

## Reproduction / Reproduktion

- Pre-fix: inspect the optional digest helpers before the PCRE2 `extract_tar_strip` sink in the Framework base revision.
- Post-fix: run `tests.security_regression.test_pcre2_archive_digest` through the actual `prepare-apache-build.sh` entry point with the isolated local archive fixture.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:221-227,238-244`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '221,227p;238,244p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T092308Z-fnd-framework-0005-pcre2-digest-e064e1d8`
  - Artifact: `.codex/runs/20260718T092308Z-fnd-framework-0005-pcre2-digest-e064e1d8/validation.md`
  - Type: `security_fix_validation_receipt`; SHA-256: `7f8c99d3df6788a145f09de893ee990f2e04d3a0ecec077aa57121d54c3ec0db`
  - Command: focused actual preparation-script regression, Framework lint/documentation checks, source-to-sink review, and current-head PR/CI/Sonar inspection
  - Working directory: `/var/tmp/codex/ModSecurity-test-Framework/worktrees/fw-pcre2-digest`; exit code: `0`
  - Observed at: `2026-07-18T10:01:20Z`; retention: `retained_local_hash_addressed`

## Root-cause analysis / Grundursachenanalyse

The Apache PCRE2 provisioning path treated both digest sources as optional: its verification helpers returned successfully for empty input and extraction followed immediately.

## Proposed remediation / Vorgeschlagene Remediation

Implemented a reviewed PCRE2 SHA-256 default that preserves explicit empty overrides, a PCRE2-specific required 64-hex verifier, exact archive hashing before the sole extraction sink, and isolated negative/control regressions with `tar` instrumentation.

## Acceptance criteria / Akzeptanzkriterien

- An empty, whitespace-only, syntactically invalid, or mismatching PCRE2 digest fails before extraction or further processing.
- Every negative case proves that the PCRE2 archive did not reach `tar`.
- A syntactically valid exactly matching digest permits the isolated fixture archive to reach the expected extraction path.

## Validation plan / Validierungsplan

- Run the actual preparation script with isolated empty, whitespace-only, malformed, and mismatching digest fixtures and capture `tar` instrumentation.
- Run the matching-digest control through the same script boundary.
- Run focused Framework regression, syntax, documentation, lint/static-analysis, ShellCheck, and source-to-sink checks.

## Regression tests / Regressionstests

- `tests/security_regression/test_pcre2_archive_digest.py`: four negative digest cases plus one matching control through `ci/provisioning/prepare-apache-build.sh`.

## Legitimate control tests / Legitime Kontrolltests

- A correct SHA-256 for the deterministic local PCRE2 fixture exits `0`, reaches the PCRE2 `tar` marker once, and completes the fixture `pcre2-config` path.

## Root-cause triage / Grundursachen-Triage

- Base Framework SHA: `cdc91a398d6c156eaff927d742b23018a3817fb6`; task head: `320627da979f5a3da607460d6e3b6bb0b9cb8c61`.
- Verdict: `confirmed` before remediation; static confidence: `medium`. The validated task control is at `ci/provisioning/prepare-apache-build.sh:300-327,361-364`.
- Root-cause group: `RC-FW-003-pcre2-archive-digest-fail-closed`; singleton. It is related to `FND-FRAMEWORK-0006` only as an archive-integrity family, not a shared patch or regression group.
- Source → broken control / sink before remediation: `PCRE2_SOURCE_URL` archive bytes with empty `PCRE2_SHA256` and `PCRE2_SHA256_URL` defaults → optional verification helpers accepted empty values → `tar` extraction. The fixed path calls `verify_required_pcre2_sha256` immediately before the sole PCRE2 `extract_tar_strip` sink.
- Attacker prerequisites before remediation: a PCRE2 source build ran with an empty digest and the external archive was substituted before consumption. No upstream substituted archive was fetched or executed.
- Countercontrol after remediation: the no-colon `PCRE2_SHA256` expansion preserves an explicitly empty override for rejection; the verifier requires exactly 64 hexadecimal characters, normalizes case, hashes the archive, compares exact equality, and `PCRE2_SHA256_URL` has no extraction-verification fallback.
- Required regression / legitimate control: empty, whitespace-only, 64-character non-hex, and wrong 64-hex digests fail before `tar`; the matching fixture digest reaches one PCRE2 `tar` marker.
- Parent impact: none; a later Framework delivery can reach Parent only through a separately authorized gitlink update. MRTS impact: none; no MRTS path is involved.
- Delivery boundary: Framework-only branch `codex/fix-framework-pcre2-digest` and Draft PR [#22](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/22); Parent gitlink unchanged; MRTS untouched. SonarQube Cloud Quality Gate passed with zero security hotspots.
- Current-head blocker: PR #22 `test-common` / `common-structure` fails with `expected 141 YAML cases, found 179`. The same condition failed at the base SHA and is independently tracked as `FND-FRAMEWORK-0001`; it is outside this Finding-only scope.
- Proof boundary: no real download or full Apache build was run because the isolated fixture exercised the actual script enforcement boundary, as authorized by the task.

## Remediation validation / Remediation-Validierung

- The local full-script regression passed three unittest methods covering four negative inputs and one matching control.
- Empty, whitespace-only, malformed 64-character non-hex, and wrong 64-hex digests each exited `77` and wrote no PCRE2 archive entry to the fake `tar` log.
- The matching deterministic local bzip2 fixture exited `0`, wrote exactly one PCRE2 `tar` marker, and completed the fixture `pcre2-config` path.
- Fixture JSON syntax, `sh -n`, `bash -n`, `make check-documentation`, `make lint`, `git diff --check`, and static source-to-sink review passed. ShellCheck 0.11.0 retained the same 17 base diagnostics, none in the modified PCRE2 control.
- SonarQube Cloud for PR #22 passed its Quality Gate; the PR reports two new issues, zero security hotspots, and zero new-code coverage/duplication.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- `FND-FRAMEWORK-0001`: current-head PR #22 cannot reach `verified_pr` while `test-common` / `common-structure` fails with `expected 141 YAML cases, found 179`; the same failure exists at the base SHA and is outside this Finding-only scope.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0006`

## Residual risk / Restrisiko

The task branch enforces the PCRE2 archive-digest boundary and has local source-to-sink proof. The independently tracked `FND-FRAMEWORK-0001` common-structure failure prevents current-head `verified_pr`; no risk has been accepted and no merge occurred.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T08:09:21Z`: root_cause_triaged — Current static evidence confirmed optional PCRE2 digest enforcement; it remains separate from the NGINX consumer/control path.
- `2026-07-18T10:01:20Z`: local_fail_closed_remediation_validated — The task branch requires the PCRE2 verifier immediately before extraction; the four negative cases never reach `tar` and the matching control succeeds. Draft PR #22 remains unmerged; its `verified_pr` state is blocked only by the pre-existing `FND-FRAMEWORK-0001` common-structure failure while the SonarQube Cloud Quality Gate passed.

## 2026-07-19 direct stale-PR reintroduction hazard

Direct comparisons from current Framework `master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` show that stale unmerged heads
#24, #27, and #29 restore empty PCRE2 digest defaults, optional-success
verification, and extraction/build after the skipped check. The source-to-sink
condition is a merge blocker only: `master` remains `fixed` and the finding is
not reopened.

Retained evidence: run `20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
observed `2026-07-19T12:01:55Z` by RTK-prefixed direct-diff and static PCRE2
source-to-sink review.
