# Change Record: Parent-No-CRS-Selected-Runner-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-no-crs-selected-runner-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-no-crs-selected-runner-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`: AZ-KYVRQfYmbqbBXVNDt (30), AZ-KYVRQfYmbqbBXVNDu (46), AZ-KYVRQfYmbqbBXVNDv (133), AZ-KYVRQfYmbqbBXVNDw (139), AZ-KYVRQfYmbqbBXVNDx (168), AZ-KYVRQfYmbqbBXVNDy (193), AZ-KYVRQfYmbqbBXVNDz (194), AZ-KYVRQfYmbqbBXVND0 (218), AZ-KYVRQfYmbqbBXVND1 (219), AZ-KYVRQfYmbqbBXVND2 (282), AZ-KYVRQfYmbqbBXVND3 (316), AZ-KYVRQfYmbqbBXVND4 (340) und AZ-KYVRQfYmbqbBXVND5 (360). |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und Indizes. No-CRS-Runner-Verhalten, Makefiles, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

Dreizehn ausgewählte Assertions übergaben ein erwartetes Literal oder einen
konstruierten Erwartungsstring vor dem beobachteten Command-/Result-Wert. Nur
die ersten zwei Argumente folgen jetzt `Istwert, Erwartungswert`; jeder bereits
vorhandene dritte Diagnoseparameter bleibt unverändert. Die feindlichen
Make-Value- und Shell-Injection-Testinputs, ihr erwarteter BLOCKED-Output und
die Sentinel-Assertions werden nicht geändert.

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Drei fokussierte Parent-only-Methoden vor der Änderung | bestanden: 3 Tests in 0,235 s. |
| Dieselben Methoden nach der Änderung | bestanden: 3 Tests in 0,223 s. |
| Strukturelles AST-Inventar | bestanden: genau 13 ausgewählte Zeilen haben einen beobachteten Wert zuerst und ein Literal/einen konstruierten Erwartungswert danach. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0,033 s. |
| `git diff --check` | bestanden, nachdem das vollständige B06-Traceability-Paar und die Indizes hinzugefügt wurden. |

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
Testdiagnostik. Die fokussierten Methoden behalten ihre feindlichen
Make-Value-Prüfungen und Shell-Injection-Sentinel-Assertions, die vor und nach
der Änderung bestanden. Der lokale Kandidat ist uncommittet; es gab keine
gehostete Sonar-Analyse, keine GitHub-CI, keinen Commit, Push, Pull Request
oder Master-Merge. Die aufgeführten Keys bleiben OPEN, bis ein ausgelieferter
Head analysiert wird.

## Runtime-Evidence

Diese strukturelle Korrektur beansprucht keine zusätzliche Runtime-Evidence;
die bestehende Parent-Testmethoden-Validierung behält ihren dokumentierten
Umfang.

## Bekannte Einschränkungen

Die fokussierte Validierung ist bewusst enger als eine vollständige
Framework-abhängige Aggregat-Suite und eine gehostete Analyse.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Ergebnisse einer
späteren Aggregat-Suite oder einer gehosteten Analyse bleiben bis zu ihrer
tatsächlichen Beobachtung ausstehend.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden kein zusätzliches
Framework-Aggregat und kein gehosteter Check ausgeführt; die ursprünglichen
Validierungsgrenzen bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
