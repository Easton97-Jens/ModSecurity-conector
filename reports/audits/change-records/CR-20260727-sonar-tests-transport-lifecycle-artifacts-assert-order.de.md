# Change Record: Parent-Transport-Lifecycle-Artefakte-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`: AZ-KYVOjfYmbqbBXVNC1 (61), AZ-KYVOjfYmbqbBXVNC2 (62), AZ-KYVOjfYmbqbBXVNC3 (64), AZ-KYVOjfYmbqbBXVNC4 (68), AZ-KYVOjfYmbqbBXVNC5 (69), AZ-KYVOjfYmbqbBXVNC6 (70), AZ-KYVOjfYmbqbBXVNC7 (71), AZ-KYVOjfYmbqbBXVNC8 (72), AZ-KYVOjfYmbqbBXVNC9 (76), AZ-KYVOjfYmbqbBXVNC- (77), AZ-KYVOjfYmbqbBXVNDA (151) und AZ-KYVOjfYmbqbBXVNDB (177). |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und Indizes. Produktionshelper für Transportartefakte, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

Zwölf ausgewählte Assertions übergaben Literale vor beobachteten
Artefaktfeldern oder In-Memory-Counts. Diese Änderung vertauscht nur diese
ersten zwei Argumente zu `Istwert, Erwartungswert`. Die
Framework-Subprocess-Assertion in Zeile 126 bleibt unverändert, ebenso die
Zeile-178-Assertion mit einem `source.read_bytes()`-Erwartungsoperand; sie ist
für eine separate Evaluation-Order-Prüfung zurückgestellt.

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Drei fokussierte Parent-only-Methoden vor der Änderung | bestanden: 3 Tests in 0,004 s. |
| Dieselben Methoden nach der Änderung | bestanden: 3 Tests in 0,004 s. |
| Strukturelles AST-Inventar | bestanden: genau die 12 ausgewählten Zeilen sind Istwert-zuerst; die Zeilen 126 und 178 behielten ihre ursprüngliche Reihenfolge. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0,035 s. |
| `git diff --check` | bestanden, nachdem das vollständige B07-Traceability-Paar und die Indizes hinzugefügt wurden. |

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
Testdiagnostik. Payload-Redaction, Hash-only-Retention und
Forbidden-Payload-Assertions bleiben intakt und bestanden vor und nach der
Änderung. Der lokale Kandidat ist uncommittet; es gab keine gehostete
Sonar-Analyse, keine GitHub-CI, keinen Commit, Push, Pull Request oder
Master-Merge. Die aufgeführten Keys bleiben OPEN, bis ein ausgelieferter Head
analysiert wird.

## Runtime-Evidence

Diese strukturelle Korrektur beansprucht keine zusätzliche Runtime-Evidence;
die bestehende Parent-Testmethoden-Validierung behält ihren dokumentierten
Umfang.

## Bekannte Einschränkungen

Die fokussierte Validierung ist bewusst enger als eine vollständige
Runtime-Matrix und eine gehostete Analyse.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Ergebnisse einer
späteren Runtime-Matrix oder einer gehosteten Analyse bleiben bis zu ihrer
tatsächlichen Beobachtung ausstehend.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden keine zusätzliche Runtime-Matrix
und kein gehosteter Check ausgeführt; die ursprünglichen Validierungsgrenzen
bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
