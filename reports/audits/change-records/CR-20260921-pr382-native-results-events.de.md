# Change Record: PR #382 native Rückgaben und Ereignisse

**Sprache:** [English](CR-20260921-pr382-native-results-events.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260921-pr382-native-results-events` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Nativer Implementierungsprüfstand | `52445b18bf5944208f218871ce0f87f8f077d47d` |
| Letzter Code-/Test-Prüfstand | `092dfd1c8937f9712c03da011e61f1e4eab31840` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull Request | [Draft #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Nur Parent-Repository. Kein Merge, Master-Push, Deployment, Abhängigkeitsupdate,
Framework-/MRTS-Schreibzugriff, Scanner-Unterdrückung oder Akzeptieren von Issues.
Aktueller Umfang ist die Reparatur der Adoption-Prüfungen und korrekte
Dokumentation, keine neue Hostfähigkeit. Die
[Checkliste](../../../docs/pr-382-checklist.de.md) trennt implementierte,
verifizierte und offene Punkte. Die Gesamtmigration bleibt `partial`.

## Motivation und Problemstellung

Null beim direkten nativen Byte-Append kann konfiguriertes `ProcessPartial`
bedeuten; Phasenauswertung verlangt eins. Host-Callbacks und Datei-APIs behalten
eigene Verträge. Ein technischer Fehler darf weder Regeltreffer noch erfolgreiche
Safe-Beobachtung werden. Logs müssen angeforderte Entscheidungen von beobachteten
Hostaktionen unterscheiden.

Die nächsten blockierenden Adoption-Prüfungen erwarteten noch Schreibweisen vor
dem Refactoring. Im vorherigen Dokumentationsupdate fehlten außerdem erforderliche
Change-Record-Überschriften und Identitätsfelder. Diese Korrektur repariert die
Dokumente, nicht deren Prüfer.

## Akzeptanzkriterien

Tatsächliche begrenzte NGINX-Terminal- und HAProxy-Rule-ID-Helfer erkennen, ohne
fehlende Aufrufe, invertierte Bedingungen oder ungeprüfte Ergebnisse zuzulassen.
Bestehende Negativtests erhalten. EN/DE-Checklisten mit tatsächlichen
Teilimplementierungen und revisionsgebundenen Tests abgleichen. Vorgeschriebene
Change-Record-Struktur, gleiche Identitätswerte und Sprachparität erhalten.

Der Nutzer verlangt null neue Sonar-Befunde für die exakte Liefer-SHA. Eine alte
Analyse oder ein grünes Quality Gate allein reicht nicht. Sicherheits-Scan-Funde
und fehlende Laufzeitnachweise bleiben unabhängig von erfolgreichem Sonar offen.

## Implementierungsentscheidung und Begründung

Gemeinsame native Prädikate und typisierte Fehlerklassifikation erfassen die
genannten Apache-/HAProxy-/Common-Pfade und NGINX-Antwortverarbeitung.
`event_protocol.h` normalisiert bekannte Ereignisse für JSONL und Hash nach
ursprünglicher Eingabevalidierung. Fehlende Beobachtungen ergeben eine leere
tatsächliche Aktion; unbekannte Anwendungsereignisse und tatsächliche Zähler-/
Transportmetadaten bleiben erhalten. Query-Redaktion bleibt aktiv. Der
handgeschriebene Apache-JSON-Fallback wurde entfernt.

HAProxy lagert begrenzte Rule-ID-Dekodierung und abhängigkeitsgeordnete Bereinigung
aus. Die Common-Engine-Brücke ordnet native Engine-Fehler ungültigen
Engine-Antworten zu, ohne Timeout-, Protokoll-, Connector- und Body-Limit-Ursachen
zusammenzufassen.

NGINX-Request-Änderungen bis `fcbaca03` akzeptieren gültige teilweise Byte-Übernahme,
prüfen Dateileser-Rückgaben weiterhin strikt und erzwingen kumulative Datei-/
Body-Grenzen. Request-Phasen werden erst nach nativem Erfolg abgeschlossen;
Wiedereintritt nach Request-Fehlern bleibt terminal. Änderungen in `52445b18`
verhindern, dass negative späte Interventionen und verpflichtende Phase-4-Logfehler
zur erfolgreichen Safe-Log-only-Behandlung gelangen. Ein begrenzter privater
Helfer erlaubt nur synchron erzeugte Core-Fehlerantworten; spätere Wiederholungen
bleiben gesperrt. Dies sind implementierte Teilbereiche, kein Nachweis aller
Request-Ereigniserzeuger oder Hosttransporte.

Der NGINX-Checker erwartete `return ret`, die geprüfte Chain gibt inzwischen aber
`ngx_http_modsecurity_phase4_fail_control(r, mcf, ctx, cause)` zurück. Commit
`7bd3b235` verlangt genau diese terminale Weiterleitung. In der isolierten
Testkopie fehlte der private Header; zwei Mutationsstellen passten noch zum alten
Code. Der parallele Commit `f7aa2f2c` blieb erhalten: Er kopiert den echten Header,
repariert die Stellen, verlangt Exitstatus 1 samt exakter FAIL-Diagnose, erhält
alle 96 vorhandenen Tests und ergänzt vier Regressionen. Kein Force-Push oder
Überschreiben wurde verwendet.

Der anschließende Lint-Fehler bei `f7aa2f2c` wurde auf zwei veraltete HAProxy-
Rule-ID-Schreibweisenprüfungen zurückgeführt. Der echte Dekodierer initialisiert
seinen Puffer mit `{0}` und kehrt bei Extraktion `<= 0` zurück; die Prüfungen
verlangten frühere Inline-Zuweisungen. Commit `092dfd1c` betrachtet den
ausgelagerten, von Kommentaren bereinigten Dekodierer und seine Interventions-
Aufrufstelle. Der bezüglich Leerraum normalisierte Vertrag erhält
Initialisierung, frühe Fehlerrückgabe, vollständige Konvertierung und Integer-
Grenzen. Acht isolierte Tests weisen unsichere Änderungen, rein auskommentierte
Bedingungen und fehlende Helferaufrufe zurück. Kompilierte Dekodierertests bleiben erhalten.

## Geänderte Dateien

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `tests/test_haproxy_adoption_rule_id.py`
- `.github/workflows/lint.yml` (ergänzt HAProxy-Regressionsschritt)
- Zweisprachige Checkliste, Vertrags-/Migrationsanleitung und Change Record.

Der aktuelle Checker-Schritt ändert keine produktiven C-Quellen. Die
Dokumentationskorrektur stellt vorgeschriebene Überschriften und Identitätsfelder
wieder her, erhält Nachweisgrenzen und erfasst den offenen Sicherheits-Scan-Fund.

## Ausgeführte Befehle

Für `092dfd1c8937f9712c03da011e61f1e4eab31840` bestand
[Lint-Job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
folgende einzelne CI-Schritte:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_nginx_request_native_results
python -m unittest -v tests.test_nginx_late_error_results
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
python -m unittest -v tests.test_nginx_common_adoption
python -m unittest -v tests.test_haproxy_adoption_rule_id
```

Diese Gruppen umfassen jeweils 29, 9, 9, 33, 100 und 8 Tests. Die
Konfigurationsreferenzschritte bestanden ebenfalls. Am selben Prüfstand schlossen
`test-common`, `test-apache`, `quick-framework-check` und `test-nginx` erfolgreich
ab. NGINX-Syntax- und Trockenlaufnachweise stehen in
[Job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305).
Dies sind CI-Ausführungen, keine lokal ausgeführten Befehle.

### Historische Nachweise

| Revision | Nachweis | Bedeutung |
| --- | --- | --- |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [Lint-Job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690) | Fokussierte Native-/Event-Tests bestanden; damalige NGINX-Mutationen schlugen fehl |
| `1709e1def4706f0124d56fc687b3faf1fd8e2946` | [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579) | 16 Apache-Mutationen und eingegrenzte Prüfungen bestanden; danach scheiterte der NGINX-Checker |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [HAProxy-Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189) | Acht kompilierte Helfertests und native API-Compile-/Link-Kompatibilität bestanden |
| `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` | [Lint-Job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958) | 100 NGINX-Adoption-Tests und exakte Sonar-Null-Prüfung bestanden; später scheiterte Lint an veralteten HAProxy-Prüfungen |

Ältere Berichte bleiben in der Git-Historie. Ergebnisse gelten nicht für spätere
Revisionen. Die Dokumentationsprüfung von `91f07e12` schlug fehl, weil dieser
Bericht vorgeschriebene Vorlagenabschnitte/Identitätsfelder nicht mehr enthielt.
Diese Korrektur stellt sie wieder her; ein erfolgreicher eigener Prüflauf wird
erst nach CI-Bestätigung behauptet.

## Security-Auswirkung

Bestehende Validierung, Redaktion, Fehlerweitergabe, unabhängige Grenzen und
Zurückweisung nicht unterstützter Profile bleiben aktiv. Keine Sicherheitsprüfung
oder Compilerwarnung wurde deaktiviert. Der Schritt erfindet keine Strict-/
Resetfähigkeit. Ein später Abbruch kann gesendete Bytes nicht zurückholen.

### Sonar und unabhängiger Sicherheits-Scan

`ci/checks/common/check-sonar-zero.py` prüft Anbieter und exakte SHA und verlangt
erfolgreich abgeschlossene Analyse mit explizit null Issues/Hotspots/Annotationen.
Fehlende oder mehrdeutige Ergebnisse schlagen fehl. Kein Issue wurde akzeptiert
und keine Regel abgeschaltet.

[Sonar-Check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571)
für `91f07e124fe09056dc46dc59d65693f406b4b1a1` meldet 0 neue Issues, 0 akzeptierte
Issues, 0 Security Hotspots und 0 Annotationen. Die gemeldete Duplikation im neuen
Code beträgt 0.2%, die Coverage 0.0%; null Befunde behauptet nicht, dass auch diese
Kennzahlen null sind oder die Regressionstests gemessene Coverage liefern. Der
nächste Commit benötigt weiterhin seine eigene Analyse.

Der unabhängige [Secret-Scan-Job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952)
für `91f07e12` meldet einen Fund. Sein verfügbares Protokoll nennt keine Regel,
Datei oder Commitstelle. Der Fund bleibt ungeklärt und wird nicht als Fehlalarm
abgetan; hier werden keine Geheimniswerte wiedergegeben und weder Ausnahmen
noch Änderungen der Git-Historie eingeführt.

## Runtime-Evidence

NGINX-/HAProxy-Adoption-Tests verändern isolierte Quellkopien. Kompilierte native
Tests prüfen ausgewählte echte Funktionen mit kontrolliertem Host-/Engine-/
Log-Umfeld. Dies sind keine sechs Live-Hosts. Workflow-Namen und Preflight-
Artefakte belegen weder natives HTTP-/Transportverhalten noch gleiche Logs echter Routen.

## Bekannte Einschränkungen

Die Gesamtimplementierung bleibt unvollständig. Typisierte Request-Fehlerereignisse,
übrige native/API-Routen und Erzeuger-/Ausgabeverhalten benötigen weitere Arbeit.
Die Dokumentationsprüfung dieser Korrektur und End-Head-CI-/Sonar-Ergebnisse
brauchen frische Bestätigung. Der unabhängige Secret-Scan-Fund bleibt offen.

## Verbleibende Risiken

Doppelte terminale Einträge, Öffnungs-/Schreib-/Kurzschreib-/Serialisierungsfehler
und angeforderte gegenüber beobachteten Aktionen jeder direkten, Companion-,
Middleware- und Sidecar-Route prüfen. Transportbezogene Fehlerinjektion, Client-
Bytes und benachbarte Streams, Laufzeitlogs, Connector-Anleitungen sowie
historische Auswerter-/Hash-Versionskompatibilität bleiben zu verifizieren.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Projektbefehle, native Builds und lokales `git diff --check` wurden wegen
des fehlenden vorgeschriebenen RTK-Ausführungswrappers nicht ausgeführt.
Verifikation nutzt tatsächliche GitHub-CI und entfernte Commitvergleiche.
Vollständige Live-HTTP-/Transportverifikation für sechs Familien, alle erforderlichen
End-Head-Prüfungen und Freigabereview bleiben offen. Stelle und Bewertung des
Sicherheitsfunds wurden noch nicht festgestellt.

## Finaler Diff- und Review-Status

NGINX-Adoption-Reparatur und anschließende HAProxy-Checker-Korrektur besitzen die
oben genannten bestandenen Tests. Request-/Datei- und Spätfehler-Teilbereiche haben
eigene Checklistenpunkte. EN/DE-Berichte verwenden die vorgeschriebene Vorlage,
ohne ihren Prüfer abzuschwächen. Parallele Commits bleiben erhalten. Diese
Lieferung bleibt Draft und insgesamt `partial`; kein Merge oder Deployment erfolgte.
