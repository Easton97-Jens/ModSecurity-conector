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

## Motivation und Problemstellung

Die konkrete Sonar-Regel, der Parent-Testumfang und die Begründung für den
Erhalt des Verhaltens stehen im vorhergehenden Abschnitt
`## Motivation und Entscheidung`. Diese strukturelle Korrektur ändert weder
den dokumentierten Quelltext noch das Testverhalten.

## Akzeptanzkriterien

- Die bereits dokumentierte Remediation und fokussierte Validierung bleiben
  unverändert.
- Dieses englisch/deutsche Change-Record-Paar behält gleichwertige technische
  Fakten.
- Blockierte, nicht ausgeführte oder ausstehende gehostete Evidence wird nicht
  als bestanden dargestellt.

## Implementierungsentscheidung und Begründung

Die bestehende Begründung und Validierung bleiben erhalten. Die kanonischen
Change-Record-Überschriften werden ergänzt, statt den Dokumentationschecker zu
schwächen oder eine recordspezifische Ausnahme zu schaffen.

## Geänderte Dateien

Der ursprüngliche versionierte Umfang steht in `## Identität` und der
vorhergehenden Implementierungsbeschreibung. Dieses Follow-up ändert nur die
Struktur dieses Change-Record-Paars.

## Ausgeführte Befehle

Die exakten Befehle und beobachteten Ergebnisse bleiben in `## Validierung`;
diese strukturelle Korrektur klassifiziert kein Ergebnis neu.

## Security-Auswirkung

Der bestehende nachfolgende Abschnitt bleibt für diese konkrete Grenze
maßgeblich. Diese Normalisierung ändert keine Sicherheitskontrolle.

## Security-Auswirkung und Einschränkungen

`not_applicable` für Produktionscode: Es handelt sich ausschließlich um
Testdiagnostik. Die Overlay-/Validation-Integrity-Assertions und die
Framework-Boundary-Ablehnung bleiben erhalten. Der lokale Kandidat ist
uncommittet; es gab keine gehostete Sonar-Analyse, keine GitHub-CI, keinen
Commit, Push, Pull Request oder Master-Merge. Die aufgeführten Keys bleiben
OPEN, bis ein ausgelieferter Head analysiert wird.

## Runtime-Evidence

Diese strukturelle Korrektur beansprucht keine zusätzliche Runtime-Evidence;
die bestehende Parent-Testmethoden-Validierung behält ihren dokumentierten
Umfang.

## Bekannte Einschränkungen

Der Record behält die explizit blockierte Voraussetzung des
Framework-Validators und die daraus folgende Begrenzung der Validierung bei.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Ergebnisse eines
späteren Framework-Validators oder einer gehosteten Analyse bleiben bis zu
ihrer tatsächlichen Beobachtung ausstehend.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden kein zusätzlicher
Framework-Validator und kein gehosteter Check ausgeführt; die ursprünglichen
blockierten Voraussetzungen bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
