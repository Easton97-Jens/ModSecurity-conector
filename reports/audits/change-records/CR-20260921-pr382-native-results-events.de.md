# Change Record: PR #382 native Rückgaben und Ereignisse

**Sprache:** [English](CR-20260921-pr382-native-results-events.md) | Deutsch

## Identität und aktueller Umfang

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260921-pr382-native-results-events` |
| Aktualisiert (UTC) | `2026-09-22` |
| PR-Basis | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
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

## Motivation und Akzeptanzkriterien

Null beim direkten nativen Byte-Append kann konfiguriertes `ProcessPartial`
bedeuten; Phasenauswertung verlangt eins. Host-Callbacks und Datei-APIs behalten
eigene Verträge. Ein technischer Fehler darf weder Regeltreffer noch erfolgreiche
Safe-Beobachtung werden. Logs müssen angeforderte Entscheidungen von beobachteten
Hostaktionen unterscheiden.

Der aktuelle Schritt muss tatsächliche begrenzte NGINX-Terminal- und HAProxy-
Rule-ID-Helfer erkennen, ohne fehlende Aufrufe, invertierte Bedingungen oder
ungeprüfte Ergebnisse zuzulassen. Bestehende Negativtests bleiben aktiv. Der
Nutzer verlangt null neue Sonar-Befunde für die exakte Liefer-SHA; ein grünes
Quality Gate einer älteren Revision erfüllt diese Vorgabe nicht.

## Erhaltene frühere Implementierungen

Gemeinsame native Prädikate und typisierte Fehlerklassifikation erfassen die
genannten Apache-/HAProxy-/Common-Pfade und NGINX-Antwortverarbeitung.
`event_protocol.h` normalisiert bekannte Ereignisse für JSONL und Hash nach
ursprünglicher Eingabevalidierung. Fehlende Beobachtungen ergeben eine leere
tatsächliche Aktion; unbekannte Anwendungsereignisse und tatsächliche Zähler-/
Transportmetadaten bleiben erhalten. Query-Redaktion bleibt aktiv. Der
handgeschriebene Apache-JSON-Fallback wurde entfernt.

HAProxy lagert begrenzte Rule-ID-Dekodierung und abhängigkeitsgeordnete Bereinigung
aus. Die Common-Engine-Brücke ordnet native Engine-Fehler der Klasse ungültiger
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

## 2026-09-22: Ursachen und Reparaturen der Adoption-Prüfungen

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
verlangten die frühere Inline-Schreibweise. Commit `092dfd1c` betrachtet den
ausgelagerten, von Kommentaren bereinigten Dekodierer und seine Interventions-
Aufrufstelle. Ein exakter, bezüglich Leerraum normalisierter Vertrag erhält
Initialisierung, frühe Fehlerrückgabe, vollständige Konvertierung und Integer-
Grenzen. Acht isolierte Regressionstests prüfen diese Anforderungen und weisen
rein auskommentierte oder fehlende Helferaufrufe zurück. Bestehende kompilierte
Dekodierertests bleiben unverändert.

Geänderte Dateien dieses Schritts:

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `ci/checks/connectors/haproxy/check-haproxy-common-adoption.py`
- `tests/test_haproxy_adoption_rule_id.py`
- `.github/workflows/lint.yml` (ergänzt HAProxy-Regressionsschritt)
- zweisprachige Checkliste, Vertrags-/Migrationsanleitung und Change Record.

Für die aktuelle Checker-Reparatur war keine Änderung produktiver C-Quellen nötig.

## Frische Verifikation und genaue Grenzen

Für `092dfd1c8937f9712c03da011e61f1e4eab31840` bestand
[Lint-Job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
folgende Einzelschritte:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_nginx_request_native_results
python -m unittest -v tests.test_nginx_late_error_results
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
python -m unittest -v tests.test_nginx_common_adoption
python -m unittest -v tests.test_haproxy_adoption_rule_id
```

Diese Gruppen umfassen jeweils 29, 9, 9, 33, 100 und 8 Tests. NGINX-/HAProxy-
Adoption-Tests verändern isolierte Quellkopien; kompilierte native Tests prüfen
tatsächliche ausgewählte Funktionen mit kontrolliertem Umfeld. Beides ist kein
HTTP-Test mit sechs Hosts. Die Konfigurationsreferenzschritte bestanden ebenfalls.

Am selben Prüfstand schlossen `test-common`, `test-apache`,
`quick-framework-check` und `test-nginx` erfolgreich ab. Der NGINX-Syntax-/
Trockenlaufschritt steht in [Job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305).
Dies ersetzt ältere Fehlerbeschreibungen dieser Prüfungen; Workflow-Namen und
Preflight-Artefakte belegen weiterhin keine vollständige native Laufzeitmatrix.

Beim Vorbereiten der Dokumentation standen die neueste entfernte Sonar-
Bestätigung und das Lint-Gesamtergebnis noch aus. Vollständig grüne End-Head-
Prüfungen werden nicht behauptet. Jeder spätere Commit einschließlich dieses
Dokumentationsupdates benötigt eine eigene frische Analyse.

## Erhaltene historische Nachweise

| Revision | Nachweis | Bedeutung |
| --- | --- | --- |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [Lint-Job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690) | Fokussierte Native-/Event-Tests bestanden; damalige NGINX-Mutationen schlugen fehl |
| `1709e1def4706f0124d56fc687b3faf1fd8e2946` | [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579) | 16 Apache-Mutationstests und eingegrenzte Prüfungen bestanden; danach scheiterte der NGINX-Checker |
| `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` | [HAProxy-Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189) | Acht kompilierte Helfertests und native API-Compile-/Link-Kompatibilität bestanden |
| `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` | [Lint-Job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958) | Alle 100 NGINX-Adoption-Tests und exakte Sonar-Null-Prüfung bestanden; später scheiterte Lint an veralteten HAProxy-Prüfungen |

Frühere Detailberichte bleiben in der Git-Historie erhalten. Diese Erfolge und
Fehler sind revisionsgebunden und keine Aussagen über den neuesten Head.

## Sonar und Sicherheitsauswirkung

`ci/checks/common/check-sonar-zero.py` verwendet jobbezogene GitHub-Leserechte,
prüft Anbieter und exakte SHA und verlangt erfolgreich abgeschlossene Analyse
sowie explizit null Issues/Hotspots/Annotationen. Fehlende oder mehrdeutige
Ergebnisse schlagen fehl. Zugangsdaten und uneingeschränkte Umgebungswerte werden
nicht geloggt. Für ein Ergebnis wurde kein Issue akzeptiert und keine Regel
abgeschaltet. Die frühere [Analyse von `039b7f12`](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547)
meldete vier Null-Befundzähler; auch die exakte Prüfung für `f7aa2f2c` bestand.
Das belegt weder das Ergebnis einer späteren Lieferung noch gemessene Coverage.

Dieser Schritt stärkt Testkopien- und Aufrufergebnisprüfung. Er entfernt keine
bestehenden Sicherheitsprüfungen, ändert keine Engine-Policy oder Ressourcengrenzen
und verleiht keine nicht unterstützten Strict-/Resetfähigkeiten. Ein später
Abbruch kann bereits gesendete Bytes nicht zurückholen.

## Offene Arbeit und nicht ausgeführte Prüfungen

Typisierte Request-Ereignisbehandlung und übrige native/API-Routen abschließen;
Erzeuger-/Ausgabeverhalten, doppelte Ereignisse und Log-I/O-Fehler jeder direkten,
Companion-, Middleware- und Sidecar-Integration vergleichen. Transportbezogene
Fehlerinjektion, Überleben benachbarter Streams, Laufzeit-Logvergleiche, umfassende
Connector-Anleitungen und historische Auswerter-/Hash-Versionskompatibilität
bleiben zu prüfen.

Lokale Befehle, native Builds und lokales `git diff --check` wurden wegen des
fehlenden vorgeschriebenen RTK-Ausführungswrappers nicht ausgeführt. Verifikation
erfolgte durch tatsächliche GitHub-CI. Vollständige Live-HTTP-/Transportprüfung
für sechs Familien, alle erforderlichen End-Head-Prüfungen und Freigabereview
bleiben offen. Änderungen wurden mittels GitHub-Commitvergleich geprüft;
parallele Branch-Commits blieben erhalten.

## Lieferstatus

NGINX-Adoption-Reparatur und anschließende HAProxy-Checker-Korrektur besitzen die
oben genannten bestandenen Tests. Request-/Datei- und Spätfehler-Teilimplementierungen
haben jetzt ausdrücklich eigene Checklistenpunkte. Die Lieferung bleibt Draft
und insgesamt `partial`; diese Testergebnisse erteilen keine Merge- oder
Deployment-Freigabe.
