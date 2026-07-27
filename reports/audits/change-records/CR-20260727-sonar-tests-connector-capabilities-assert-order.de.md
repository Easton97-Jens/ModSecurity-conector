# Change Record: Parent-Connector-Capabilities-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-connector-capabilities-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-connector-capabilities-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`: AZ-KYVU7fYmbqbBXVNGk (142), AZ-KYVU7fYmbqbBXVNGl (144), AZ-KYVU7fYmbqbBXVNGm (145), AZ-KYVU7fYmbqbBXVNGn (146), AZ-KYVU7fYmbqbBXVNGo (148), AZ-KYVU7fYmbqbBXVNGp (149), AZ-KYVU7fYmbqbBXVNGq (150), AZ-KYVU7fYmbqbBXVNGr (151), AZ-KYVU7fYmbqbBXVNGs (176), AZ-KYVU7fYmbqbBXVNGt (177) und AZ-KYVU7fYmbqbBXVNGu (178). |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und Indizes. Produktionsverhalten der Connector-Capabilities, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Entscheidung

Elf ausgewählte `unittest`-Assertions übergaben ein erwartetes Literal vor
einem beobachteten Dictionary-Subscript. Diese Änderung vertauscht ausschließlich
diese ersten zwei Argumente zu `Istwert, Erwartungswert`; derselbe Key-Lookup,
dieselbe Assertion, dieselben erwarteten Literale, dieselben temporären
Git-Fixtures und dieselbe Capability-/Provenance-Semantik bleiben erhalten. Die
benachbarten Assertions mit variablen Erwartungswerten in den Zeilen 143 und
147 sind keine Inventarzeilen und bleiben unverändert.

## Akzeptanzkriterien

- Korrigiere nur die elf aufgeführten S3415-Assertions.
- Erhalte beide temporären Git-Repository-Fixtures und ihre Gitlink-/Provenance-Assertions.
- Lasse die zwei betroffenen Parent-only-Testmethoden vor und nach der Änderung bestehen.
- Lasse eine strukturelle AST-Prüfung für genau die elf Istwert-zuerst-Assertions, die bilinguale Dokumentationsprüfung und `git diff --check` bestehen.
- Lasse Framework-/MRTS-Quelltext und Gitlinks unverändert.

## Geänderte Dateien

- tests/test_connector_capabilities.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Validierung

| Prüfung | Ergebnis |
| --- | --- |
| Erste fokussierte Methode vor der Änderung | bestanden: 1 Test in 0,246 s. |
| Zweite fokussierte Methode vor ihrer Drei-Zeilen-Änderung | bestanden: 1 Test in 0,169 s. |
| Beide fokussierten Methoden nach der vollständigen Elf-Zeilen-Änderung | bestanden: 2 Tests in 0,376 s. |
| Strukturelles AST-Inventar | bestanden: genau die Zeilen 142, 144-146, 148-151 und 176-178 haben einen Subscript-Istwert vor einem Literal-Erwartungswert. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0,034 s. |
| `git diff --check` | bestanden, nachdem das vollständige B04-Traceability-Paar und die Indizes hinzugefügt wurden. |

## Security-Auswirkung

`not_applicable`: Es handelt sich ausschließlich um Testdiagnostik. Die Tests
behalten ihre temporären Repositories, Git-Metadaten-Prüfungen und das
Parent-only-Quellverhalten. Kein Produktions- oder Sicherheitscontrol änderte
sich und kein Sicherheitsbefund wird als behoben behauptet.

## Einschränkungen und Delivery-Status

Das vollständige Modul `tests.test_connector_capabilities` ist keine B04-
Evidenz, weil eine unabhängige Methode den absichtlich nicht initialisierten
Framework-Gitlink benötigt. Die zwei geänderten Methoden erzeugen eigene
temporäre Framework-ähnliche Repositories und bestanden unabhängig. Der lokale
Kandidat ist uncommittet; es gab keine gehostete Sonar-Analyse, keine GitHub-CI,
keinen Commit, Push, Pull Request oder Master-Merge. Die aufgeführten Keys
bleiben OPEN, bis ein ausgelieferter Head analysiert wird.

## Motivation und Problemstellung

Die vorangehende Entscheidung beschreibt die ursprüngliche Reparatur der
Assertion-Reihenfolge. Dieses Follow-up erhält diese Evidenz und normalisiert
den Record zugleich auf den erforderlichen Change-Record-Vertrag des Projekts.

## Implementierungsentscheidung und Begründung

Identität, Umfang, Validierungsevidence und Security-Klassifikation bleiben
erhalten. Es kommen ausschließlich die erforderliche Abschnittsstruktur und
explizite Statusgrenzen hinzu; aus dieser Record-Korrektur entstehen keine
Änderungen an Test- oder Connector-Quelltext.

## Ausgeführte Befehle

Die exakten Befehle und beobachteten Ergebnisse bleiben in `## Validierung`;
diese strukturelle Korrektur klassifiziert kein historisches Ergebnis neu.

## Runtime-Evidence

Es wird keine zusätzliche Runtime-Evidence beansprucht. Die fokussierte
Parent-only-Testmethoden-Evidenz behält ihren dokumentierten Umfang.

## Bekannte Einschränkungen

Die bestehenden Einschränkungen und der Delivery-Status bleiben maßgeblich:
Das vollständige Framework-abhängige Aggregatmodul und die gehostete Analyse
liegen außerhalb der ursprünglichen fokussierten Evidenz.

## Verbleibende Risiken

Die Record-Normalisierung führt kein neues Risiko ein. Ergebnisse eines
Framework-Aggregats oder einer gehosteten Analyse bleiben bis zu ihrer
tatsächlichen Beobachtung ausstehend.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Dokumentationskorrektur werden kein zusätzliches
Framework-abhängiges Aggregat und kein gehosteter Check ausgeführt; die
ursprünglichen Validierungsgrenzen bleiben unverändert.

## Finaler Diff- und Review-Status

Die frühere Delivery-Formulierung ist eine Momentaufnahme der ursprünglichen
lokalen Validierung. Dieser Record behauptet keine finale PR-Verifikation,
keinen Merge und keinen Sonar-Issue-Abschluss für einen späteren Delivery-Head.
