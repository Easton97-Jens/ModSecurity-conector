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

## Security-Auswirkung und Einschränkungen

`not_applicable` für Produktionscode: Es handelt sich ausschließlich um
Testdiagnostik. Die fokussierten Methoden behalten ihre feindlichen
Make-Value-Prüfungen und Shell-Injection-Sentinel-Assertions, die vor und nach
der Änderung bestanden. Der lokale Kandidat ist uncommittet; es gab keine
gehostete Sonar-Analyse, keine GitHub-CI, keinen Commit, Push, Pull Request
oder Master-Merge. Die aufgeführten Keys bleiben OPEN, bis ein ausgelieferter
Head analysiert wird.
