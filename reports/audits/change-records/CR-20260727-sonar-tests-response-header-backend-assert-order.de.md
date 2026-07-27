# Change Record: Parent-Response-Header-Backend-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260727-sonar-tests-response-header-backend-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-tests-response-header-backend-assert-order |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`: AZ-KYVUDfYmbqbBXVNGK (109), AZ-KYVUDfYmbqbBXVNGL (110), AZ-KYVUDfYmbqbBXVNGM (111), AZ-KYVUDfYmbqbBXVNGN (112), AZ-KYVUDfYmbqbBXVNGO (157) und AZ-KYVUDfYmbqbBXVNGR (198). |
| Grenze | Parent-Testquelltext sowie dieses englisch/deutsche Change-Record-Paar und seine Indizes. Backend-Verhalten, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

Die sechs ausgewählten `unittest`-Assertions übergeben ein erwartetes Literal vor dem beobachteten Wert. Das Vertauschen ausschließlich dieser beiden Argumente verbessert die Fehldiagnostik-Konvention, ohne Prädikat oder Erwartungswert zu ändern.

## Akzeptanzkriterien

- Korrigiere ausschließlich die sechs unabhängigen Assertions zu Istwert zuerst und Erwartungswert danach.
- Erhalte HTTP-Fixture-Ablauf, Server-Lebenszyklus, Response-Reads, Invalid-Header-Ablehnung und Harness-Quelltext-Assertions.
- Lasse die drei Parent-only Methoden vor und nach der Änderung sowie AST-Inventur und `git diff --check` bestehen.
- Lasse die fünf Framework-abhängigen S3415-Assertions unverändert, bis ihr Gitlink-Setup ausdrücklich autorisiert ist.
- Pflege ein gleichwertiges englisch/deutsches Change-Record-Paar und die Indizes.

## Implementierungsentscheidung und Begründung

Die sechs Aufrufe übergeben nun den bereits beobachteten Response-Status, Header, Body oder Subprocess-Returncode zuerst und das unveränderte erwartete Literal danach. Bei `response.read()` wird der beobachtbare Receiver vor demselben nebenwirkungsfreien Literal ausgewertet; das Assertion-Prädikat bleibt unverändert. Erwartungswert, Meldung, Retry-Grenze, Fixture, Subprocess und Backend-Verhalten wurden nicht geändert.

## Geänderte Dateien

- tests/test_response_header_backend.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Fokussierte Befehle verwendeten Parent-`.venv`-Python, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1` und task-eigenes externes `TMPDIR`.

- rtk proxy env ... `<Parent-.venv-Python>` -m unittest -v `<drei ausgewählte ResponseHeaderBackendTest-Methoden>` vor der Änderung
- rtk proxy env ... `<Parent-.venv-Python>` -m unittest -v `<dieselben drei Methoden>` nach der Änderung
- rtk proxy env ... `<Parent-.venv-Python>` -c `<strukturelle AST-Inventur der sechs Assertions>`
- rtk proxy git diff --check

## Tests und tatsächliche Ergebnisse

| Befehl oder Prüfung | Ergebnis |
| --- | --- |
| Drei ausgewählte Parent-only Methoden vor der Änderung | bestanden: 3 Tests in 0.347 s. |
| Dieselben drei Methoden nach der Änderung | bestanden: 3 Tests in 0.347 s. |
| Strukturelle AST-Inventur | bestanden: genau die Zeilen 109-112, 157 und 198 haben die ausgewählten Istwert-zuerst-Ausdrücke und unveränderte typisierte Erwartungswerte. |
| Erste ad-hoc-AST-Präsentationsprüfungen | nur fehlgeschlagen, weil `ast.unparse` Literal-Anführungszeichen normalisiert und die erste Erwartungswert-Map Strings statt typisierter Literale verwendete; kein Produktquelltext- oder Testfehler ist aufgetreten. Die finale strukturelle AST-Inventur bestand. |
| `git diff --check` | bestanden, nachdem das vollständige B03-Traceability-Paar und die Indizes hinzugefügt wurden. |
| Bilinguale Change-Record-Validierung | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0.035 s. |
| `make check-bilingual-docs` | blocked_environment: genau 20 bestehende fehlende Ziele unter dem absichtlich nicht initialisierten Framework-Gitlink; kein B03-Record-Fehler. |
| `make check-doc-links` | blocked_environment: genau 16 bestehende fehlende Ziele unter dem absichtlich nicht initialisierten Framework-Gitlink; kein B03-Record-Fehler. |

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung ist `not_applicable`: Es handelt sich ausschließlich um Testdiagnostik. Der Test behält Loopback-Backend, Fixture-Input, Header-Injection-Ablehnung, Subprocess-Cleanup und statische Harness-Prüfungen. Kein Backend- oder Produktions-Sicherheitscontrol wurde geändert und es wird kein Sicherheitsbefund als behoben behauptet.

## Dokumentationsstatus

Die reine Testquelltextkorrektur ändert keinen generierten oder leserorientierten Guide. Das englisch/deutsche Change-Record-Paar und die Indizes liefern die erforderliche Traceability.

## Runtime-Evidence

Die ausgewählten Tests üben ein bestehendes Loopback-Test-Backend aus. Sie sind fokussierte Test-Evidence, keine Connector-Host- oder Produktions-Runtime-Evidence.

## Bekannte Einschränkungen

Dieser Batch adressiert ausschließlich sechs Parent-S3415-Keys. Fünf weitere S3415-Keys desselben Testmoduls bleiben unverändert, weil ihre Methoden vom absichtlich nicht initialisierten Framework-Gitlink abhängen. Die Keys bleiben im aktuellen Inventar OPEN, bis eine neue Analyse einen ausgelieferten Head auswertet.

## Verbleibende Risiken

Eine versehentliche Änderung von Erwartungswert oder Aufrufreihenfolge könnte Diagnostik schwächen oder die Consumption des Response-Bodys ändern. Der enge Sechs-Aufruf-Diff, die Istwert-vor-Erwartungswert-AST-Inventur und die Parent-only-Tests vor und nach der Änderung mindern dieses Risiko. Aus diesem Batch folgt keine Aussage über übrige S3415-Zeilen.

## Nicht ausgeführte Prüfungen mit Begründung

- Das vollständige Modul `tests.test_response_header_backend` wird nicht ausgeführt, weil es Framework-abhängige Methoden enthält und das saubere Task-Worktree absichtlich keinen initialisierten Framework-Gitlink besitzt. Die drei geänderten Methoden sind unabhängig Parent-only und wurden vor und nach ausgeführt.
- Connector-Builds, Host-Runtime-Smokes, Framework-Prüfungen und MRTS-Prüfungen sind nicht anwendbar, da keine Connector-/Runtime-Implementierung oder Repository-übergreifender Inhalt geändert wurde.
- `tests.test_bilingual_docs` bestand. Die beiden vollständigen Dokumentations-Make-Checks wurden ausgeführt und sind ausschließlich auf den 20 beziehungsweise 16 bestehenden fehlenden Framework-Gitlink-Zielen `blocked_environment`. Gehostete SonarQube-Cloud-Analyse, GitHub-CI, Commit, Push, Pull Request und Merge wurden nicht ausgeführt; keine Master-Integration ist autorisiert.

## Finaler Diff- und Review-Status

Der lokale Task-Worktree-Kandidat enthält uncommittet die Sechs-Aufruf-Assertion-Order-Korrektur mit dem erforderlichen Traceability-Material. Im autoritativen Parent-Checkout wurde kein Quelltext geändert. Es gab keine Framework- oder MRTS-Aktion, kein Gitlink-Update, keine Scanner-Control-Änderung, keine externe Issue-Disposition, keinen Push, keinen Pull Request und keinen Master-Merge. Spätere Validierungs- und Delivery-Evidence wird nur aus beobachteten Ergebnissen dokumentiert.
