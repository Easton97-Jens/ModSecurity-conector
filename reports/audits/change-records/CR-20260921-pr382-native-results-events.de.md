# Change Record: PR #382 native Rückgaben und Ereignisse

**Sprache:** [English](CR-20260921-pr382-native-results-events.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260921-pr382-native-results-events` |
| Datum (UTC) | `2026-09-21` |
| Basis-Revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Basis dieser Fortsetzung | `6ff390486e90a10c30c7fb6199870532ecde367a` |
| Getestete Implementierungsrevision | `10b3379561de81a8018467b724b4edb8c8742ef2` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull Request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Lieferumfang: nur Parent-Repository. Der PR ist Draft; kein Merge ausgeführt.

## Motivation und Problemstellung

Direkte libModSecurity-Body-Append-Rückgaben wurden von nativen Bindings
unterschiedlich behandelt. Ein Append-Ergebnis null kann konfiguriertes
`ProcessPartial` bedeuten; die abschließende Phasenauswertung verlangt dagegen
eins. Technische Fehler erreichten außerdem unterschiedliche Ereignisklassen.
Dieser PR führt gemeinsame Prädikate und Ereignisnormalisierung ein; diese
Fortsetzung korrigiert seinen Testaufbau und die fehlende Common-Zuordnung von
Engine-Fehlern. Die vollständige Connector-übergreifende Migration ist nicht fertig.

## Akzeptanzkriterien

Maßgeblich ist die [getrennte Implementierungs-/Verifikationscheckliste](../../../docs/pr-382-checklist.de.md).
Abgeschlossene Teilschritte benötigen tatsächliche Quellcodeänderungen und
passende Testnachweise. Eine vollständige Migration verlangt zusätzlich alle
ausgewählten nativen/Companion-Routen, konsistente Fehler-/Ausgabebehandlung,
vollständige Regressionstests und echte Host-/Transportvalidierung. Diese
übergeordneten Kriterien bleiben offen.

## Implementierungsentscheidung und Begründung

Native Byte-Übernahme, Phasenauswertung, Host-Rückgabewerte und Engine-
Interventionen getrennt halten. Der Byte-Append-Helfer darf nicht auf
`msc_request_body_from_file()` angewendet werden, dessen Rückgaben zusätzliche
Fehlerbedeutungen haben.

Die Common-Weitergabe fehlgeschlagener Callbacks bildet jetzt
`MSCONNECTOR_ERROR_MODSECURITY_FAILURE` auf
`MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` ab und entspricht damit
den geänderten nativen Bindings. Vorhandene Zuordnungen für Hostfehler, Timeout,
nicht verfügbare Engine, Body-Limit, Protokoll und Phasenfolge bleiben erhalten.
Die Änderung verändert keine Hostaktion und behauptet keinen Regeltreffer.

Der C-Testextraktor liefert für die betreffenden Common-Funktionen bereits die
vollständige Deklaration. Das Entfernen doppelter Rückgabetyp-Präfixe repariert
die Kompilierung ohne schwächere Compilerwarnungen oder Prüfungen. Ein separater
kompilierter Test prüft den echten Klassifizierer und den zuständigen Contract
mit einer protokollierenden Testausgabe. Die angepassten NGINX-Quellcodeprüfungen
folgen den gemeinsamen Prädikaten und verlangen weiterhin terminalen Fehler,
Abbruch nach Antwortbeginn und keine erfolgreiche Bytezählung nach Append-
Fehler. Sie sind Quellcodeprüfungen, kein Ersatz für native Tests.

## Security-Auswirkung

Ein Engine-Fehler darf nicht zu Allow/Log-only, einer falschen Regelblockierung
oder angeblich erfolgreicher Untersuchung werden. Fehlerursache und beobachtete
Hostaktion bleiben getrennt. Diese Fortsetzung schaltet keine Validierung,
Compilerwarnung, Redaktion, Schutzkontrolle privater Logdateien, Abhängigkeit,
Branch-Protection oder bestehende CI-Prüfung ab. Diese Berichte enthalten keine
Request-/Response-Inhalte oder Zugangsdaten.

## Geänderte Dateien

Diese Fortsetzung ändert:

- `common/src/modsecurity_engine.c`
- `tests/test_native_result_event_protocol.py`
- `tests/test_native_error_classification.py`
- `tests/test_nginx_upstream_security_contract.py`
- `.github/workflows/lint.yml`
- `docs/pr-382-checklist.md` und `docs/pr-382-checklist.de.md`
- diesen Change Record und seine englische Fassung.

Frühere PR-Commits führten außerdem die gemeinsamen Native-/Event-Header ein
und änderten Apache, HAProxy, NGINX-Antwortbehandlung, Common Runtime, JSONL und
Integritäts-Hashing. Diese früheren Änderungen stehen im PR-Diff und werden
nicht als in dieser Fortsetzung neu abgeschlossen ausgegeben. Generierte
Konfigurationsausgaben und Framework-/MRTS-Dateien bleiben unverändert.

## Ausgeführte Befehle

GitHub CI meldete in [Lauf 35628608293, Job 106429001084](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35628608293/job/106429001084)
erfolgreich abgeschlossene Schritte für beide Befehle auf der getesteten
Implementierungsrevision:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
```

Der erste Befehl kompiliert echten Common-Serializer-/Hash-Code sowie extrahierte
native Callback-/Klassifizierer-Funktionen mit `-std=c17 -Wall -Wextra -Werror`.
Er prüft außerdem die Quellcode-Anbindung. Der zweite Befehl prüft Phase-4-
Migration und NGINX-Quellcodeverträge. Diese Ergebnisse bedeuten nicht, dass der
gesamte Workflow grün ist.

Die zugehörigen Workflows `test-common`, `test-apache`, `test-nginx` und
`quick-framework-check` schlugen auf dieser Revision fehl. Alte Apache-
Adoption- und NGINX-Adoption-/Mutationserwartungen sind weiterhin offen.
Sie werden weder ausgenommen noch verborgen. Spätere Checklisten-/Change-Record-
Commits ändern nur Dokumentation; deren aktuelle Head-CI muss getrennt gelesen
werden.

Ein GitHub-Vergleich von der Basis dieser Fortsetzung bis
`41c2d4e9dd6a5563ca1007ad574c17575003623c` bestätigte vor diesem Change-Record-
Paar sieben erwartete geänderte Dateien und nur sieben zusätzliche
Produktivcodezeilen. Dies ist eine begrenzte Remote-Diff-Prüfung, keine lokale
Ausführung von `git diff --check`.

## Runtime-Evidence

In dieser Fortsetzung wurde keine vollständige native HTTP- oder Transportmatrix
für sechs Familien ausgeführt. Sechs Connector-Identitäten in einer Common-
Testdatei beweisen nicht sechs unabhängige Hostintegrationen. Host-spezifische
Strict-Unterstützung wird nicht aufgewertet.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale repository-eigene Builds/Tests und `git diff --check` wurden nicht
ausgeführt: Der erforderliche lokale Projektwrapper war nicht verfügbar und
es wurde kein lokaler Checkout eingerichtet. Die Validierung nutzt die oben
beschriebenen tatsächlichen GitHub-CI-Schritte. Vollständige CI des endgültigen
Heads, gesonderte Linkprüfung, vollständige native Fehlerinjektion und
Host-Log-/Transportgleichheit bleiben ohne spätere Dokumentation offen.

## Bekannte Einschränkungen

NGINX-Request-/Dateipfade, späte technische Interventionsfehler, Logging vom
Erzeuger bis zur Ausgabe, doppelte terminale Ereignisse und Gleichwertigkeit
direkter/Companion-Profile benötigen weitere Arbeit. Insbesondere darf fehlende
Transportbeobachtung nicht als ausgeführte Blockierung erscheinen. Vorhandene
Strukturprüfungsfehler verhindern weiterhin die Review-Freigabe. Die umfassenden
EN/DE-Vertrags-/Migrationsanleitungen und Beispiele sind noch nicht vollständig.

## Verbleibende Risiken

Ein gültiges Teilübernahme-Ergebnis beweist nicht, dass alle übergebenen Bytes
untersucht wurden. Ein später Abbruch kann bereits gesendete Daten nicht
zurückholen. Ein gemeinsames JSON-Schema kann weder fehlende Hostbeobachtungen
erzeugen noch nicht unterstützte Reset-/Abbruchfähigkeiten bereitstellen.
Die Normalisierung von JSONL-Namen/Aktionen kann nachgelagerte Log-Auswerter
betreffen und verlangt vollständige Migrationshinweise vor einer Freigabe.

## Finaler Diff- und Review-Status

Gesamt: `partial`. Die begrenzten Quellcode-/Testkorrekturen sind committed und
die genannten CI-Schritte bestanden. Checkliste und Change Record unterscheiden
vorhandenen Code, verifizierte Teilschritte, fehlgeschlagene und nicht ausgeführte
Prüfungen. Der PR bleibt Draft; es gab keinen Merge, direkten Master-Push,
Deployment, Abhängigkeitswechsel oder Framework-/MRTS-Schreibzugriff.
Ein Bestehen aller erforderlichen Prüfungen des endgültigen Heads wird nicht
behauptet.
