# FND-FRAMEWORK-0010 — Framework-Dokumentationsaggregat ist durch mögliche MRTS-Traversal blockiert

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0010` |
| Title / Titel | `Framework-Dokumentationsaggregat ist durch mögliche MRTS-Traversal blockiert` |
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

Framework-PR #52 ergänzt einen expliziten `tools/MRTS`-Ausschluss im
Markdown-Link-Inventar und eine direkte negative Boundary-Regression. Der Tree
des geprüften PR-Heads entspricht Framework-Master
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; die fokussierte Regression, das
Dokumentationsaggregat und die anwendbaren Master-Checks bestehen.

## Observed behavior / Beobachtetes Verhalten

Vor PR #52 verließ sich der Markdown-Link-Checker auf die gegenwärtige
Auslassung von Submodul-Inhalten durch Git und besaß keine direkte Kontrolle
für einen unerwartet gemeldeten `tools/MRTS`-Markdown-Pfad.

## Expected behavior / Erwartetes Verhalten

Das Framework-Dokumentationsaggregat muss originales MRTS auch bei einem
verschachtelten Markdown-Pfad im Git-Inventar ausschließen und zugleich eigene
Framework-Dokumentation weiter auswählen und validieren.

## Impact / Auswirkung

Die Eigentums-/Traversierungsgrenze ist auf dem resultierenden Framework-Master
verifiziert. Diese statische Dokumentationskontrolle behauptet kein
Connector-Runtime-Ergebnis und ändert keine Parent- oder MRTS-Delivery-Grenze.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `ci/checks/documentation/check-doc-links.py`
- `tests/security_regression/test_parser_hardening.py`

### Symbols / Symbole

- `ci/checks/documentation/check-doc-links.py:SKIP_DIR_PARTS`
- `tests/security_regression/test_parser_hardening.py:MarkdownHeadingHardeningTests.test_excludes_mrts_submodule_paths_even_if_git_reports_them`

## Preconditions / Voraussetzungen

- Framework-PR #52 ist normal in Framework-Master gemergt.
- Der Tree des resultierenden Framework-Masters entspricht dem geprüften
  PR-Head-Tree.

## Reproduction / Reproduktion

- `sed -n '87,90p;125,136p' .codex/reports/repository-full-assessment.md`
- Führe `tests.security_regression.test_parser_hardening` mit einem Inventar
  aus, das `docs/guide.md` und `tools/MRTS/ignored.md` enthält; nur das
  Framework-Dokument darf ausgewählt werden.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:87-90,125-136`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '87,90p;125,136p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run-ID: `20260726-remediate-active-framework-findings`
  - Artefakt: `.codex/runs/20260726-remediate-active-framework-findings/evidence/fnd-framework-0010-resulting-master-verification.md`
  - Typ: `resulting_framework_master_finding_verification`; SHA-256: `cbf90db531a6e4eab99ae84de6ba1008a07d6644b9805dcae2745fc54ad2aee9`
  - Ergebnis: PR #52 wurde normal um `2026-07-26T17:35:13Z` als
    Framework-Master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` gemergt;
    sein geprüfter Head-Tree ist identisch zu resultierendem Master. Die
    fokussierte 11-Test-Regression, das Dokumentationsaggregat und alle
    anwendbaren Resulting-Master-Checks bestehen.

## Root-cause analysis / Grundursachenanalyse

Das frühere Markdown-Link-Inventar hing implizit vom aktuellen
Git-Submodulverhalten ab, statt die Grenze des unabhängig besessenen MRTS
selbst zu erzwingen.

## Proposed remediation / Vorgeschlagene Remediation

In Framework-PR #52 umgesetzt: `tools/MRTS` wird explizit vom
Markdown-Link-Inventar ausgeschlossen und eine negative Mock-Inventar-Regression
mit einem eigenen Framework-Dokument-Control bleibt erhalten.

## Acceptance criteria / Akzeptanzkriterien

- Erfüllt: Das Dokumentationsaggregat endet ohne Traversal von originalem MRTS.
- Erfüllt: Das direkte Boundary-Control beweist den MRTS-Ausschluss auch bei
  einer entsprechenden Inventar-Meldung.

## Validation plan / Validierungsplan

- Bestanden: Das eingegrenzte Framework-Dokumentationsaggregat auf dem
  geprüften, mit resultierendem Master identischen Tree.
- Bestanden: Das negative Boundary-Fixture, das bei MRTS-Traversal scheitern
  würde.

## Regression tests / Regressionstests

- Bestanden: `tests.security_regression.test_parser_hardening` (11 Tests),
  einschließlich des Unexpected-MRTS-Path-Controls.

## Legitimate control tests / Legitime Kontrolltests

- Bestanden: `ci/checks/documentation/check-doc-links.py` gibt `doc links ok`
  aus und behält die Auswahl eigener Framework-Dokumentation bei.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-MRTS-0001`

## Residual risk / Restrisiko

Die statische Framework-Dokumentationsgrenze ist geschlossen. Diese Evidence
behauptet weder ein MRTS-Runtime-Ergebnis noch autorisiert sie ein
Parent-Gitlink-Update, eine MRTS-Delivery oder einen Ersatz für nicht verwandte
Upstream-Digest-Evidence.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-26T17:43:12Z`: fixed_verified_closed_after_framework_pr52_normal_merge —
  PR #52 ergänzte den expliziten `tools/MRTS`-Ausschluss und die direkte
  negative Regression. Sein geprüfter Head-Tree entspricht Framework-Master
  `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; fokussierte negative/legitime
  Controls und die anwendbaren Master-Checks bestanden. Das Finding geht ohne
  Risikoakzeptanz von `blocked` über `fixed` und `verified` nach `closed`.
