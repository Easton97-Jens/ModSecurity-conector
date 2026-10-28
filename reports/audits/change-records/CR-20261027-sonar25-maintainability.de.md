# Change Record: CR-20261027-sonar25-maintainability

**Sprache:** [English](CR-20261027-sonar25-maintainability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261027-sonar25-maintainability |
| Datum (UTC) | 2026-10-27 |
| Basis-Revision | `0867713cca9401a80831f116efdacce4727d4e13` |

## Motivation und Problemstellung

Der Nutzer verlangte ausdrücklich die Korrektur der 25 verbleibenden Sonar-Befunde in PR #382. Vollständiger authentifizierter CLI-Readback bestätigte elf Komplexitätsbefunde, acht doppelte Literale, zwei Generator-Konstruktoren, zwei ausführliche Regex-Klassen, einen verschachtelten Bedingungsausdruck und einen mehrdeutigen Ausnahmetest. Der Umfang betrifft sechs vorhandene native Analysehilfen und einen vorhandenen Test.

## Akzeptanzkriterien

Diese 25 Befunde durch Quelländerungen beheben, Verhalten und Sicherheitsprüfungen erhalten, keinen neuen Befund in geänderten Quellen einführen und den neuen veröffentlichten Head mit Pflicht-CI sowie bestehenden Sonar-Analysen prüfen. 100 expandierte automatische Fälle / 80 Ausführungen, 1893 On-demand-Fälle / 839 Ausführungen und E2E 26 bleiben erhalten. Keine neue Funktion, Testkatalog, I12-Kampagne, Analyseprojekt, Framework-/MRTS-Arbeit, Merge, Release oder Deployment.

## Implementierungsentscheidung und Begründung

Geordnete SDK-/Archiv-, Capture-, Producer-, Quellmapping- und Graphvalidierungsschritte in kleine Hilfsfunktionen aufteilen; vorhandene öffentliche Signaturen, tatsächliche Befehle, ausdrückliche Fehler, Prüfreihenfolge und Manifestformate erhalten. Doppelte Literale als Konstanten benennen und Dictionary-Comprehensions verwenden. Regex-Kürzel behalten ASCII-Ziffernsemantik. Das Ausnahme-Fixture vor assertRaisesRegex aufbauen, damit nur der beabsichtigte Aufruf den erwarteten Fehler erfüllen kann.

## Geänderte Dateien

`ci/checks/analysis/prepare-sonar-native-ci.py`; `ci/checks/analysis/sonar-native-security/{build-target,capture,go_provenance,source_mapping,validate}.py`; `tests/test_sonar_native_ci.py`; Quellhashes in `config/testing/active-cases.json`; generatorerzeugtes Archiv; dieses EN/DE-Record und das kompakte PR-Statuspaar. Testselektoren, expandierte Fälle, Workflows, Gates und Quellscope bleiben unverändert.

Der erste veröffentlichte Folgefix `39793006` schloss alle 25 ursprünglichen IDs als `CLOSED / FIXED` (Analyse `d17df325-5caa-489c-b669-e4b06e09956b`, Gate OK), führte aber einen `S7500`-Kopier-Comprehension-Befund im Pinparser ein. Die finale Präzisierung filtert und zerlegt direkt in der Comprehension wie die bereits akzeptierte Builder-Form. Ihr notwendiger Push ersetzt die vorherige CI durch die bestehende cancel-in-progress-Regel; frühere Zwischenergebnisse bleiben historisch erhalten. Kein unveränderter Rerun und keine neue Kampagne wurde beauftragt.

## Ausgeführte Befehle

RTK umschloss Regel-/API-Readback, Quell-/Diff-Review und AST-/Syntaxprüfungen. Alle elf Basis-Komplexitätswerte stimmen mit der rein lesenden Schätzung überein; geänderte Funktionen liegen geschätzt bei höchstens 15. Die sieben ursprünglichen Validatorfunktionen sind nach Hilfsfunktions-/Zustandsnormalisierung und begrenzter ASCII-Regex-Normalisierung AST-identisch. Unabhängiges Review fand keine konkrete Regression. Kanonische Inventarzulassung `972866207512972dda9bc4b4d7be387fcbf35f8d5b13753b684dc2f40a177adb` erfolgte vor ausdrücklicher On-demand-Ausführung: 29 vorhandene Ausführungen / 38 expandierte Fälle PASS, keine Skips. Das Archiv wurde mit `ci/tools/update-test-archive.py` regeneriert. Evidence liegt im externen Aufgabenroot `runs/pr382-sonar25-20261027`, einschließlich `targeted-admission.json` und `active-tests-_i43xiv4/summary.json`.

## Security-Auswirkung

Der Refactor erhält Ownership/Rechte, kanonische Vorfahren, Quell-/Header-/Hash-Abschluss, echte Compiler-/Linkerherkunft, Archivgrenzen, private Ausgaben, SDK-Identität, exakte Revision sowie Scanner-/Gate-Kontrollen. Keine Suppression, kein Ausschluss, Accepted-risk-Disposition, Abhängigkeitsänderung oder Abschwächung wurde eingeführt.

## Runtime-Evidence

Gezielte Tests verwenden vorhandene Offline-Fixtures einschließlich der echten Validator-Exportschnittstelle; lokal wurde keine Anwendung, kein Connector-Host und keine historische Matrix-/Oraclekampagne gestartet. Frühere SDK-/Native-Analyseergebnisse gehören zur Basis 0867713. Automatische CI und Serverergebnisse des aktuellen Heads stehen im PR.

## Bekannte Einschränkungen

AST und lokale Tests belegen ihre eigenen Ebenen. Die Komplexitätsschätzung ist kalibrierte statische Orientierung, kein verbindliches Sonar-Ergebnis. Implizite Python-Diagnostik fehlerhafter Pinzeilen bleibt eine ValueError-Abweisung; keine neue Pinsyntax wird zugelassen. Neue Hosted-Analyse muss Befundabschluss und tatsächliche Builds bestätigen.

## Verbleibende Risiken

Hilfsfunktionsextraktion berührt Provenienz- und Traversierungspfade; gezielte Negativ- und statische Reihenfolgeprüfungen bestanden. Finale CI/Sonar am veröffentlichten Head bleiben Lieferkriterium; der tatsächliche terminale Status steht in PR #382. Bereits bestehende, unabhängige Advisory-Befunde liegen außerhalb dieses gezielten Auftrags.

## Nicht ausgeführte Prüfungen mit Begründung

Kein vollständiger Offlinekatalog, keine neuen Tests, zusätzliche native Kampagne, Abhängigkeitsinstallation oder lokale Scannerkampagne. Bestehende automatische Workflows laufen nach dem notwendigen normalen Push; Wiederholungen brauchen konkrete Korrektur oder Infrastrukturursache. Coverage bleibt nach früherer Nutzerentscheidung außerhalb der Abnahme.

## Finaler Diff- und Review-Status

Begrenztes Quellreview und gezielte Tests bestanden. Normaler Commit/Push bleibt auf den vorhandenen Aufgabenbranch begrenzt. Finale Head-Gleichheit, tatsächliche CI-/Sonar-Befundauflösung, Review-Feedback, Ready-Status und gestoppte Monitore stehen in [PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) und dem [kompakten Abschlussrecord](../../../docs/pr-382-merge-readiness.de.md). Kein Master-Merge ist autorisiert.
