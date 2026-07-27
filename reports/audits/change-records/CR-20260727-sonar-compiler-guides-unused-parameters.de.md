# Change Record: Parent-Compiler-Guide-Bereinigung ungenutzter Parameter für SonarQube Cloud S1172

**Sprache:** [English](CR-20260727-sonar-compiler-guides-unused-parameters.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-compiler-guides-unused-parameters |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1172`-Code-Smells AZ9cRzBeHhV2CayPTP57 (Zeile 604), AZ9cRzBeHhV2CayPTP58 (Zeile 779), AZ9cRzBeHhV2CayPTP5- (Zeile 3559), AZ9cRzBeHhV2CayPTP5_ (Zeile 3573) und AZ9cRzBeHhV2CayPTP6A (Zeile 3610). |
| Grenze | Parent-Python-Generator sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Generierte Guides, Connector-/Runtime-Verhalten, Framework, MRTS, Gitlinks, Sonar-Scanner-Konfiguration, Quality Gates, Suppressions und externer Sonar-Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählten SonarQube-Cloud-Zeilen melden fünf Funktionsparameter im Parent-Compiler-Guide-Generator, die von ihren Funktionskörpern nicht gelesen werden. Allein das Entfernen dieser Parameter und ihrer direkten Call-Site-Argumente klärt den tatsächlichen Abhängigkeitsvertrag, ohne gerenderten Guide-Inhalt zu ändern.

## Akzeptanzkriterien

- Nur die fünf gemeldeten ungenutzten Parameter und passende direkte Call-Site-Argumente entfernen.
- Generierten englisch/deutschen Guide-Inhalt, Generator-Daten, Command-Strings und Runtime-Verhalten bewahren.
- Das vollständige fokussierte Modul `tests.test_compiler_guides` vor und nach der Änderung bestehen lassen sowie `git diff --check` bestehen.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar und die Record-Indizes pflegen.
- Keinen Sonar-Issue vor einer exakten Kandidaten-Head-Analyse als geschlossen behaupten.

## Implementierungsentscheidung und Begründung

`route_comparison` und `selected_preparation` erhalten ihren ungenutzten Parameter `item` nicht mehr. Die NGINX- und Apache-Validierungshelfer sowie der Apache-Runtime-Helper erhalten ihren ungenutzten Parameter `german` nicht mehr. Direkte Call Sites übergeben jetzt nur die vom Callee konsumierten Werte; kein Branch und kein zurückgegebener Dokumentations-String änderte sich.

## Geänderte Dateien

- scripts/generate_compiler_guides.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Fokussierte Kommandos nutzen Parent-.venv-Python, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1` und task-owned externes `TMPDIR`:

- rtk proxy env ... `<Parent .venv python>` -m unittest -v tests.test_compiler_guides (vor der Änderung)
- rtk proxy env ... `<Parent .venv python>` -m unittest -v tests.test_compiler_guides (nach der Änderung)
- rtk proxy env ... `<Parent .venv python>` -m unittest -v tests.test_bilingual_docs
- rtk proxy make check-bilingual-docs
- rtk proxy make check-doc-links
- rtk proxy sh -c 'git diff --check && git diff -- scripts/generate_compiler_guides.py && git status --short'

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussiertes Compiler-Guide-Modul vor der Änderung | bestanden: `tests.test_compiler_guides`, 20 Tests in 0.649s. |
| Fokussiertes Compiler-Guide-Modul nach der Änderung | bestanden: `tests.test_compiler_guides`, 20 Tests in 0.638s. |
| `git diff --check` | bestanden: kein Whitespace-Fehler. |
| Direkter Source-Diff-Review | bestanden: nur fünf ungenutzte Parameter und direkte Call-Site-Argumente wurden geändert. |
| Bilinguales Checker-Unit-Modul | bestanden: `tests.test_bilingual_docs`, 13 Tests in 0.034s. |
| Direkter Change-Record-Paar-Vertrag | bestanden: `check_change_record_pair` gab keinen Fehler zurück. |
| `make check-bilingual-docs` | blocked_environment: 20 vorhandene fehlende Framework-Gitlink-Linkziele; kein Fehler nennt dieses Change-Record-Paar oder seinen Index. |
| `make check-doc-links` | blocked_environment: 16 vorhandene fehlende Framework-Gitlink-Linkziele; kein Fehler nennt dieses Change-Record-Paar oder seinen Index. |

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet `not_applicable`: Diese Änderung entfernt nur ungenutzte Python-Funktionsparameter in einem Dokumentationsgenerator. Sie ändert keinen Pfad-Guard, Netzwerk-Client/Server, Subprozess, Connector, Credential, generierten Guide-Inhalt oder Runtime-Control. Es wird kein Sicherheitsbefund als behoben behauptet.

## Dokumentationsstatus

Der fokussierte Generationstest zeigt, dass ausgegebene englische/deutsche Guide-Dateien unverändert sind. Direkter Paar-Vertrag und bilinguale Checker-Unit-Suite bestehen; die vollständigen Repository-Dokumentationsprüfungen sind ausschließlich durch die bestehenden Linkziele des uninitialisierten Framework-Gitlinks blockiert. Dieses versionierte englisch/deutsche Change-Record-Paar und beide Record-Indizes liefern die Traceability für die reine Source-Bereinigung.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll- oder Produktions-Runtime-Verhalten geändert oder behauptet. Der fokussierte Unit-Test prüft Generator-Ausgabe und Dokumentationsverträge; er ist keine Runtime-Evidence.

## Bekannte Einschränkungen

Dieser Batch bearbeitet nur fünf ausgewählte Parent-`python:S1172`-Zeilen aus der aktuellen SonarQube-Cloud-Inventur mit 1.125 Einträgen. Die Keys bleiben in dieser Inventur OPEN, bis eine neue Analyse einen gelieferten Kandidaten-Head auswertet.

## Verbleibende Risiken

Eine versehentlich übersehene Call Site könnte Guide-Generation fehlschlagen lassen oder einen Guide verändern. Der enge reine Signature-Diff und die vollständige fokussierte Generator-Suite vor und nach der Änderung reduzieren dieses Risiko. Aus dieser Bereinigung folgt keine Aussage über nicht verwandte Sonar-Zeilen oder Sicherheitsbefunde.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Repository-Dokumentationsprüfungen sind nicht bestanden, weil der Task-Worktree bewusst keinen initialisierten Framework-Gitlink enthält. `make check-bilingual-docs` meldet 20 und `make check-doc-links` 16 vorhandene fehlende Framework-Pfade; die fokussierte bilinguale Unit-Suite und der direkte Paar-Vertrag bestehen beide.
- Connector-Builds, Host-Konfigurationsprüfungen, Runtime-Smokes, Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar, weil keine Connector-/Runtime-Implementierung oder Cross-Repository-Inhalte geändert wurden.
- Es wurde keine gehostete SonarQube-Cloud-Analyse, GitHub-CI, Commit, Push, Pull Request oder Merge ausgeführt; die aktuelle Aufgabe hat keine Master-Integrationsautorisierung.

## Finaler Diff- und Review-Status

Der lokale Kandidat im Task-Worktree ist uncommitted und enthält die Signature-Bereinigung sowie erforderliches Traceability-Material. Im autoritativen Parent-Checkout wird keine Source geändert. Es gab keine Framework- oder MRTS-Aktion, kein Gitlink-Update, keine Scanner-Control-Änderung, keine externe Issue-Disposition, keinen Push, Pull Request oder Master-Merge. Spätere lokale Dokumentationsvalidierung und Delivery-Evidence werden ausschließlich aus beobachteten Ergebnissen aufgenommen.
