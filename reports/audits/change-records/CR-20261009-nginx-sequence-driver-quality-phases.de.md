# Change Record: CR-20261009-nginx-sequence-driver-quality-phases

**Sprache:** [English](CR-20261009-nginx-sequence-driver-quality-phases.md) | Deutsch

Begrenztes Sequence-Driver-Refactoring zu gespeicherten Sonar-Findings, ohne Runtime-Behauptung.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-sequence-driver-quality-phases |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Die gespeicherte f639-Analyse meldet S3776 (`run`: 71), sechs S1192-Literalduplikate für Artefakte/Konfiguration und S7498 für den Observation-Konstruktor. Vorbereitung, Fixture-Setup, Ausführung/Cleanup, Observations und Receipts lagen in einer Funktion.

## Akzeptanzkriterien

Begrenzte Phasenhelper extrahieren, ohne CLI, Case-Auswahl, Identitäten, Konfiguration, originale Evidence-Bytes, Fehlerpriorität oder FD-Cleanup-Grenzen zu verändern. Strikte Negativkontrollen erhalten. Keine behauptete Remote-Schließung.

## Implementierungsentscheidung und Begründung

Controls/Assets/Projection, geschlossenes Fault-Setup, Client-Capture, Ausführung, Observations, Receipts und Veröffentlichung trennen. Das bestehende verschachtelte Stop/fsync/close-`finally` bleibt in `execute_sequence`; Ressourcenakquisition und Config-Test liegen weiterhin davor. Wiederholte Leaves/Location-Konfiguration benennen und dieselben Observation-Felder als Dictionary-Literal ausdrücken. Drei geschlossene typisierte Records enthalten zusammengehörige Launch-/Config-Test-Eingaben (`PreparedInvocation`), tatsächliches Ausführungs-/Wire-Ergebnis (`ExecutionOutcome`) und originalen Snapshot-/Config-/Projection-Receipt-Kontext (`ReceiptContext`). Alle Top-Level-Funktionen haben höchstens sieben explizite Parameter. Kein generischer kwargs/Context-Beutel, Invocation-Framework oder neues Reconnect-Verhalten.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`, `tests/test_nginx_begin_driver_evidence.py`, neu `tests/test_nginx_sequence_driver_phases.py` und dieses generierte EN/DE-Paar. Bestehende Sequence-Client/Upstream-Dateien, kompilierte Fixtures, Framework, MRTS und Shared-Source bleiben unverändert.

## Ausgeführte Befehle

RTK-Unit-Befehle und genaue Umgebungen stehen extern in `D-sequence-driver-quality-results.md`. Baseline: 22 Tests, Exit 1, 12 UID-Transition-Subtestfehler (kompiliertes BEGIN-Kind mit Exit 70). Neue Charakterisierung vor Source-Änderung: vier Tests, drei bestandene Verhaltenskontrollen und ein beabsichtigter fehlender Seam. Domain-Grenzen-RED: 14 Tests, Exit 1, drei Parameterzahlfehler und ein fehlender Record. Parserfehler-RED: ein Test, Exit 1, erfasste Wire-Fakten wurden null. Finaler kombinierter Nicht-UID-/CI-Lauf nach Korrektur: 68 Tests, Exit 0, keine Skips. AST-Syntax und `git diff --check` bestanden. Generator erzeugte dieses Paar; Strukturprüfung separat gespeichert. Sonar-Rule-GETs scheiterten vor Analyse an Authentifizierung; keine Dienste oder Credentials geändert.

## Security-Auswirkung

Private frische FD-Flags und exakte Transaktions-/Phasenkontrollen bleiben erhalten. Tests prüfen fehlende Pflicht-Fixtures, abweichende Transaktionen, originale Wire-Bytes, Same-Socket-/Abort-/Backpressure-Parameter, Cleanup- und fsync-Fehler mit garantiertem FD-Close. Domain-Prüfungen erhalten exakte Child-FD-Weitergabe und stellen sicher, dass Config-Test keine pass_fds erhält. Originale Raw-Hashes und dict-Mapping-Override-Semantik bleiben erhalten; Record-Felder sind weder neu zuweisbar noch durch beliebige Keywords erweiterbar. Validatorfehler bleiben vor Host-/Clientfehlern. Keine PASS-Hochstufung oder Guard-Unterdrückung.

## Runtime-Evidence

Nur reine Orchestrierungs-Doubles, begrenzte Loopback-Client-Tests und bestehende kompilierte Common-Budget-Tests. Kein NGINX-/Runtime-Supervisor, Protected-Gate, Produktbuild oder Native-Host-Lauf. Parent-Required-Zahl bleibt 97.

## Bekannte Einschränkungen

Die Sandbox kann den tatsächlichen UID-Wechsel des BEGIN-Fixtures nicht ausführen; der Koordinator muss unveränderte Kontrollen außerhalb wiederholen. Lokales AST-Branch-Inventar ist weder Sonar Cognitive Complexity noch Remote-Schließung. Gesamte Dokumentationsprüfungen scheitern in diesem isolierten Worktree bereits an nicht initialisierten Framework-Linkzielen. Unabhängiges Review fand eine Refactor-Regression: Parsing im Capture-Helper verlor erfasste Wire-Fakten bei Parser-Exception. `capture_sequence_wire` liefert originale Fakten und Response-Bytes jetzt vor Parsing; der Execution-Helper weist sie vor dem unveränderten Parser zu. Fehlerpriorität, Raw-Hashes, leere fehlgeschlagene Requests und fehlende Fakten bei Capture-Fehler sind explizit getestet. Kein generischer Kontext, neuer Execution-Zweig oder zusätzliches Exception-Handling.

## Verbleibende Risiken

Aktuelle Native-Artefakte und Authorities benötigen nach Integration neue Koordinatorprüfung. Bestehende Akquisitions-/Exception-Grenzen vor Ausführung werden absichtlich erhalten, nicht neu entworfen. Kein echter Timing- oder unabhängiger Host-Rollen-Nachweis.

## Nicht ausgeführte Prüfungen mit Begründung

Keine volle CI/Sonar-Analyse, Native-Build/Runtime, Dependency-Installation, externe Dienste, MRTS-Initialisierung, Git-Stage/Commit/Push oder Shared-Source-Änderung: außerhalb des Auftrags. Sonar-Rule-Lookup war wegen fehlender CLI-Authentifizierung/Keychain nicht verfügbar.

## Finaler Diff- und Review-Status

Diff gegen originale Producer-Reihenfolge und kontrollierte RED/GREEN-Evidence geprüft. Ungestagte Lieferung im isolierten Worktree; eigener Change Record getrennt vom vorherigen CI-Fixture-Fix. Koordinator besitzt Integration, UID-Rerun außerhalb der Sandbox und Remote-Quality-Schließung.
