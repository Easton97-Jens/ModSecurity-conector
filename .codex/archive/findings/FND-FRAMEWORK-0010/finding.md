# FND-FRAMEWORK-0010 — Framework documentation aggregate is blocked by possible MRTS traversal

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0010` |
| Title / Titel | `Framework documentation aggregate is blocked by possible MRTS traversal` |
| Category / Kategorie | `documentation_drift` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Framework PR #52 adds an explicit `tools/MRTS` exclusion to the Markdown-link
inventory and a direct negative boundary regression. The reviewed PR-head tree
equals resulting Framework master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`;
the focused regression, documentation aggregate, and applicable master checks
pass.

## Observed behavior / Beobachtetes Verhalten

Before PR #52 the Markdown-link checker relied on Git's present omission of
submodule contents and had no direct control for an unexpectedly reported
`tools/MRTS` Markdown path.

## Expected behavior / Erwartetes Verhalten

The Framework documentation aggregate must exclude original MRTS even when a
Git inventory reports a nested Markdown path, while continuing to select and
validate owned Framework documentation.

## Impact / Auswirkung

The ownership/traversal boundary is verified on resulting Framework master.
This static documentation control does not assert a connector runtime result or
change any Parent or MRTS delivery boundary.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `ci/checks/documentation/check-doc-links.py`
- `tests/security_regression/test_parser_hardening.py`

### Symbols / Symbole

- `ci/checks/documentation/check-doc-links.py:SKIP_DIR_PARTS`
- `tests/security_regression/test_parser_hardening.py:MarkdownHeadingHardeningTests.test_excludes_mrts_submodule_paths_even_if_git_reports_them`

## Preconditions / Voraussetzungen

- Framework PR #52 is normally merged into Framework master.
- The resulting Framework-master tree equals the reviewed PR-head tree.

## Reproduction / Reproduktion

- `sed -n '87,90p;125,136p' .codex/reports/repository-full-assessment.md`
- Run `tests.security_regression.test_parser_hardening` with an inventory that
  contains `docs/guide.md` and `tools/MRTS/ignored.md`; only the Framework
  document may be selected.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:87-90,125-136`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '87,90p;125,136p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260726-remediate-active-framework-findings`
  - Artifact: `.codex/runs/20260726-remediate-active-framework-findings/evidence/fnd-framework-0010-resulting-master-verification.md`
  - Type: `resulting_framework_master_finding_verification`; SHA-256: `cbf90db531a6e4eab99ae84de6ba1008a07d6644b9805dcae2745fc54ad2aee9`
  - Result: PR #52 was normally merged at `2026-07-26T17:35:13Z` as Framework
    master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; its reviewed head tree
    is identical to resulting master. The focused 11-test regression, the
    documentation aggregate, and all applicable resulting-master checks pass.

## Root-cause analysis / Grundursachenanalyse

The former Markdown-link inventory depended implicitly on current Git submodule
behavior rather than enforcing the independently owned MRTS boundary itself.

## Proposed remediation / Vorgeschlagene Remediation

Implemented in Framework PR #52: explicitly exclude `tools/MRTS` from the
Markdown-link inventory and retain a mocked-inventory negative regression with
an owned Framework-document control.

## Acceptance criteria / Akzeptanzkriterien

- Satisfied: the documentation aggregate completes without traversing original
  MRTS.
- Satisfied: the direct boundary control proves that the MRTS path is excluded
  even when the inventory reports it.

## Validation plan / Validierungsplan

- Passed: scoped Framework documentation aggregate on the reviewed tree that is
  identical to resulting master.
- Passed: negative boundary fixture that would fail on MRTS traversal.

## Regression tests / Regressionstests

- Passed: `tests.security_regression.test_parser_hardening` (11 tests),
  including the unexpected-MRTS-path control.

## Legitimate control tests / Legitime Kontrolltests

- Passed: `ci/checks/documentation/check-doc-links.py` prints `doc links ok`
  and retains owned Framework documentation selection.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-MRTS-0001`

## Residual risk / Restrisiko

The static Framework documentation boundary is closed. This evidence neither
claims an MRTS runtime result nor authorizes a Parent Gitlink update, MRTS
delivery, or a substitution of unrelated upstream-digest evidence.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-26T17:43:12Z`: fixed_verified_closed_after_framework_pr52_normal_merge —
  PR #52 added the explicit `tools/MRTS` exclusion and direct negative
  regression. Its reviewed head tree equals resulting Framework master
  `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; focused negative/legitimate
  controls and applicable master checks passed. The finding advances
  `blocked` → `fixed` → `verified` → `closed` without risk acceptance.
