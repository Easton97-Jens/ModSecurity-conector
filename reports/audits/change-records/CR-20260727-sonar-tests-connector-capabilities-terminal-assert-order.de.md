# Change Record: Parent-Connector-Capabilities-Abschluss-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`: AZ-KYVU7fYmbqbBXVNHA (376), AZ-KYVU7fYmbqbBXVNHB (387), AZ-KYVU7fYmbqbBXVNHC (425), AZ-KYVU7fYmbqbBXVNHD (432), AZ-KYVU7fYmbqbBXVNHE (433), AZ-KYVU7fYmbqbBXVNHF (434) und AZ-KYVU7fYmbqbBXVNHI (469). |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und Indizes. Produktionsverhalten der Connector-Capabilities, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

Sieben ausgewählte Assertions übergaben Literal-/Listen-/Dictionary-/Name-
Erwartungswerte vor beobachteten Merge-, Result-, Payload- oder Return-Code-
Werten. Diese Änderung vertauscht nur diese ersten zwei Argumente zu `Istwert,
Erwartungswert`. Die benachbarten Validator-Zeilen 450 und 454 bleiben
unverändert: Die erste hat einen echten Framework-Gitlink-Umgebungsblocker,
die zweite besitzt einen `command.index()`-Operand und benötigt eine separate
Evaluation-Order-Prüfung.

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Vier fokussierte Parent-only-Methoden vor der Änderung | bestanden: 4 Tests in 0,281 s. |
| Dieselben Methoden nach der Änderung | bestanden: 4 Tests in 0,282 s. |
| Fünf-Methoden-Preflight einschließlich Zeile 450 | blocked_environment: Genau der nicht initialisierte Framework-Kanonische-Validator fehlt; Zeile 450 wurde ohne Quelltextänderung ausgeschlossen. |
| Strukturelles AST-Inventar | bestanden: Genau sieben ausgewählte Zeilen sind Istwert-zuerst; die Zeilen 450 und 454 bleiben Original-Order-Ausschlüsse. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0,035 s. |
| `git diff --check` | bestanden, nachdem das vollständige B09-Traceability-Paar und die Indizes hinzugefügt wurden. |

## Security-Auswirkung und Einschränkungen

`not_applicable` für Produktionscode: Es handelt sich ausschließlich um
Testdiagnostik. Die Overlay-/Validation-Integrity-Assertions und die
Framework-Boundary-Ablehnung bleiben erhalten. Der lokale Kandidat ist
uncommittet; es gab keine gehostete Sonar-Analyse, keine GitHub-CI, keinen
Commit, Push, Pull Request oder Master-Merge. Die aufgeführten Keys bleiben
OPEN, bis ein ausgelieferter Head analysiert wird.
