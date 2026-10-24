# PR #410: Sonar-Reparatur und Abschlussverifikation

**Sprache:** [English](pr-410-sonar-remediation-20261024.md) | Deutsch

## Ergebnis am versionierten Prüfpunkt

Die konkreten Sonar-Ursachen des PR-Ausgangsstands wurden ohne Quality-Gate-
Ausschluss, Regelunterdrückung, Accepted-Issue-Einstufung oder Umschreiben
historischer Ergebnisse bearbeitet. Der Patch erhält den reduzierten
I12-Abschluss und ändert weder Framework- noch MRTS-Gitlink.

Der eine erlaubte lokale Funktionslauf wurde exakt einmal ausgeführt und ist
**fehlgeschlagen**. Er führte 39 unittest-Methoden für 79 vorab deklarierte
expandierte aktive Szenarien aus: 65 expandierte Szenarien bestanden, fünf
scheiterten beim gemeinsamen C++-Hilfsbuild, eines lief an einer Envoy-Fixture-
Root-Grenze in einen Fehler, und acht spätere Companion-Varianten wurden nach
dem Abbruch der Methode nicht erreicht. Es gab keinen Retry; danach wurde kein
ausführbares Verhalten mehr geändert. Dieser Prüfpunkt ist daher
`remediation_required` und nicht `verified_pr`, unabhängig von einem späteren
grünen Scanner-Ergebnis.

Der genaue veröffentlichte Commit und die automatische CI-/Sonar-Rücklesung
werden nach dem einzigen finalen Push im PR festgehalten; dieses statische
Dokument behauptet keinen zukünftigen Commit oder Provider-Status.

## Sonar-Ausgangsinventar

Das vollständige Inventar liegt maschinenlesbar in
[sonar-baseline.json](../reports/testing/pr410-sonar-remediation-20261024/sonar-baseline.json).
Es ist an PR-Head `30d50a181278904a552e295d9a2c1ae1265e8b87`, Analyse
`e18acebb-7e6c-4727-a572-afe02105a43b`, Compute-Task
`AaFrW5KKk-m4lzyjl55H` und Analysezeit `2026-10-24T00:39:09Z` gebunden.

| Kategorie | Ausgangsstand |
| --- | ---: |
| Offene Issues | 231 |
| Vulnerabilities / Code Smells / Bugs | 90 / 141 / 0 |
| Blocker / Critical / Major / Minor | 5 / 121 / 76 / 29 |
| Offene Security Hotspots / akzeptierte Issues | 0 / 0 |
| Neue duplizierte Blöcke / Zeilen | 21 / 851 |
| Dichte neuer duplizierter Zeilen | 0.20824055087089086 |
| PR-Coverage-Messwerte | nicht vorhanden |
| Quality Gate | `ERROR`: neue Security Rating E (5), erforderlich A (1) |

Alle 231 offenen Issues, jede Datei und jeder Block mit Duplikation, alle
gemeldeten Messwerte, der Compute-Task und alle 50 GitHub-Annotationen wurden
gelesen. Die 50 Annotationen waren damit nur eine Darstellungsmenge und keine
Anzahl bestätigter Sicherheitslücken. Sonar meldete ein Reliability-Issue, 90
Security-Issues und 140 Maintainability-Issues. Die drei Konfigurationswarnungen
betrafen Python-Version, fehlende Testklassifizierung und eine nicht näher
bezeichnete Kodierung; das lokale Inventar enthielt nur ASCII-, UTF-8- oder
Binärdateien.

## Ursachen und Reparaturen

| Ursache und betroffene Befunde | Reparatur und erhaltene Grenze |
| --- | --- |
| 125 Befunde und 19 von 21 Duplikatblock-Vorkommen stammten aus Dateien mit Quellcode-Endung unter `ci/runtime/lifecycle/i12/objects/text/**`. Sie sind unveränderliche, hashgebundene historische Datensätze und keine gepflegten Programme. | 61 Klartextobjekte und ein historischer Observer-Repository-Snapshot wurden in die vorhandene verlustfreie JSON-Darstellung `text_lines` überführt. Alle 346.634 rekonstruierten Bytes und SHA-256-Identitäten bleiben exakt. `capture_sources.py` lehnt Quellcode-Endungen im Klartextformat nun ab. Historische Ergebnisse, Deltas, Profile und Revisionen wurden nicht geändert. |
| Envoy importierte oder exponierte historische Helfer noch transitiv; der archivierte Host-Log-Parser trug außerdem das einzige Reliability-Issue `python:S8786`. | Gepflegte Module `host_log_observations.py` und `grpc_stream_observations.py` werden normal geprüft. Historische Helfer bleiben authentifizierte Provenienz-Daten und können weder aktuelle Parser-Identitäten ersetzen noch über das Helferverzeichnis importiert werden. Das Parsing ist begrenzt und linear. |
| Live-Python-Security-Flows akzeptierten Evidence-Pfade oder Publikationsziele ohne gemeinsame Lese-/Schreibgrenze. | `ci/lib/i12_path_safety.py` bündelt kanonische Roots, Traversal-/Symlink-/Privatpfad-/Modus-/Checkout-Ablehnung, begrenzte deskriptorgebundene Lesezugriffe sowie Create-/Replace-Semantik. Apache, HAProxy, Traefik, lighttpd, Envoy und Report-Produzenten verwenden diese Grenze. Die vorhandene `CODEX_PROJECT_STATE`-Kompatibilität bleibt explizit. |
| Evidence-Generatoren enthielten wiederholte unbegrenzte Parsing-/Publikationslogik und hohe kognitive Komplexität. | Current-Report-, Lifecycle-Ledger- und Oracle-Reconciliation-Generatoren nutzen den gemeinsamen begrenzten I/O-Vertrag und kleinere lineare Parser, ohne historische Ergebnisse oder Qualifikationsgrenzen zu vermischen. |
| NGINX-Acceptance/-Qualification und Native-Observer-Code vermischten unabhängige Prüfungen in großen Funktionen; der Native-Observer-Test duplizierte dieselbe Compile-Fixture. | NGINX-Prüfungen wurden ohne Abschwächung von Identität, Provenienz, physischen Produzenten oder negativen Events zerlegt. Native-C-Finalisierung verwendet benannte Helfer/Zustände; die Tests teilen eine Compile-Fixture und behalten getrennte Runtime-/Companion-Szenarien. |
| Der automatischen Analyse fehlten explizite Python- und Testquellenangaben. | `.sonarcloud.properties` setzt Python 3.14 und klassifiziert `tests/**/*.py`, `**/test_*.py` sowie `**/*_test.py` als Tests. Die Datei enthält keinen Source-, Issue-, Coverage-, Duplikations- oder Regelausschluss. |

Der Patch adressiert alle Ursachengruppen des Ausgangsinventars. Ob Issues und
Duplikate tatsächlich geschlossen sind, entscheidet erst die automatische
Analyse des veröffentlichten Heads, nicht der Diff allein.

## Wirkung auf Duplikation und Coverage

Vierzehn historische Objektpfade verursachten 19 Duplikatblock-Vorkommen. Ihre
Datenumstellung entfernt die falsche Beziehung zwischen gepflegtem Code, ohne
ein rekonstruiertes historisches Byte zu ändern. Die übrigen zwei Vorkommen
waren ein echtes Duplikat in `tests/test_native_lifecycle_observer.py`; eine
gemeinsame Fixture-Kompilierung bedient nun Runtime- und Companion-Prüfungen,
während getrennte Parameter, Ownership-Fehler, EOS-Varianten und Assertions
erhalten bleiben.

Kein Test wurde gelöscht, um Grün zu erzielen. Sonar lieferte keinen
PR-Coverage-Messwert; daher wird kein Coverage-Prozentsatz behauptet. Die
explizite Testklassifizierung ermöglicht der Folgeanalyse die korrekte Ebene.

## Eingefrorenes Testbudget und Einmallauf

Der unveränderliche Plan ist
[test-plan.json](../reports/testing/pr410-sonar-remediation-20261024/test-plan.json),
das Ergebnis steht in
[run-result.json](../reports/testing/pr410-sonar-remediation-20261024/run-result.json).
Ein importfreier Preflight löste jeden Selektor aus dem Quelltext auf und würde
oberhalb der gemeinsamen Grenze vor der Ausführung fehlschlagen.

| Eintrag | Anzahl/Status |
| --- | ---: |
| Historische eingefrorene Reserve, nicht erneut ausgeführt | 21 |
| Ausgewählte aktive Szenarien | 79 |
| Gemeinsames Projektbudget | 100 / 100 |
| Exakte Selektoren / unittest-Methoden | 30 / 39 |
| Lokale Befehle / Retries | 1 / 0 |
| Expandiert PASS / FAIL / ERROR / nicht erreicht | 65 / 5 / 1 / 8 |
| unittest-Zusammenfassung | `FAILED (failures=5, errors=1)` in 11,431 s |

Die 21 historischen Fälle verbrauchen dasselbe projektweite Budget, wurden aber
nicht ausgeführt. Die 79 ausgewählten Szenarien waren Unit-, Vertrags-,
synthetische Evidence- und lokal kompilierte C-/APR-/SDK-Kontrollen; sie
starteten weder Host, Netzwerk, Protokollmatrix noch historische I12-Kampagne.

Fehler und Fehlschläge:

- Die Envoy-Kontrolle für historische Helfer schrieb eine temporäre Fixture
  unterhalb des Lauf-Roots. Die gepflegte Transportreferenz nutzte jedoch die
  beim Modulimport fixierten `evidence_io.DEFAULT_ROOTS` statt des vom Test
  gepatchten Storage-Roots. Die Admission stoppte vor der Assertion gegen
  transitive Imports.
- Fünf expandierte Native-Szenarien erreichten dieselbe C++-SDK-Hilfs-
  Voraussetzung. Deren Argument `-isystem /usr/include` ließ GCC-15-libstdc++
  `#include_next <stdlib.h>` vor den Runtime-Assertions fehlschlagen.
- Der erste Compile-Fehler der Companion-Methode verhinderte deren acht
  nachfolgende sequenzielle Varianten.

Das vollständige schreibgeschützte Log liegt außerhalb des Checkouts unter
`/var/tmp/codex/ModSecurity-conector/pr410-sonar-final-20261024.0T0N9T/functional-run.log`
(SHA-256 `4015acc961e1af01a1d88884a2960ae349230f44a001c4d93841521ea6fcdaa3`,
21.256 Bytes). Für diese Aufgabe ist kein zweiter lokaler Lauf erlaubt.

## Weitere Verifikation

- Der statische Archiv-/Integrationsprüfer bestand für 62 Umstellungen, 346.634
  rekonstruierte Bytes, alle Archiv-/Delta-Hashes, die erlaubten
  Manifestübergänge, aktuelle Pins, 64 JSON-Dateien, 61 geänderte Python-AST-/
  Symboltabellendateien und den unveränderten Framework-Gitlink.
- `git diff --check` bestand.
- Strikte Prüfungen mit `-std=c17 -Wall -Wextra -Werror -fsyntax-only`
  bestanden für Native-Lifecycle-Observer und Apache-Header-Semantics-Probe.
- Ein fokussierter defensiver Patch-Review fand kein verbleibendes konkretes
  Security-Problem. Er war statisch und ersetzt weder Runtime noch Scanner.

## Grenzen und Lieferstatus

Eingefrorene I12-Auswahl, Archivdisposition, historische PASS-/FAIL-Bindungen
und die Grenze `I12_COMPLETE=false` bleiben unverändert. Weder Framework-/MRTS-
Repository noch Gitlink, historischer Oracle, Hostlauf oder Matrix wurden
geändert oder ausgeführt.

Die automatischen Standard-Testpfade des Repositories sind weiterhin nicht
vollständig an ein autoritatives Inventar mit technischer Vorabgrenze gebunden.
Nur diese Aufgabenauswahl besaß einen verifizierten 79+21-Guard. Die globale
automatische Cap-Durchsetzung bleibt `not_verified` und benötigt eine getrennt
autorisierte Migration.

Weil der einzige lokale Lauf fehlschlug und ein Teil des ausgewählten Verhaltens
nicht erreicht wurde, fehlen aktuelle Runtime-Akzeptanz und lokale
Abschlussverifikation. PR #410 muss Draft/`remediation_required` bleiben; grüne
automatische CI oder Sonar können dieses lokale Ergebnis nicht rückwirkend in
einen Pass umwandeln.
