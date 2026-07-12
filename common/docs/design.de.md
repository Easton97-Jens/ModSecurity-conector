# Gemeinsames Design

**Sprache:** [English](design.md) | Deutsch


Status: eingerüstet

## Grenze

`common/` ist steckerneutral. Es kann Anfrage, Antwort, Transaktion definieren,
Interventions-, Status-, Ursprungs-, Protokollierungs- und Fähigkeitstypen, die von verwendet werden können
Tests und Steckeradapter, es darf jedoch keine enthalten oder davon abhängen
Server-/Proxy-SDK.

## C-First-Schnittstelle

Die gemeinsam genutzten Header sind C-first, da Apache und NGINX lokal analysiert werden
Connectors rufen libmodsecurity über seine C-API auf. Die C++-Header sind dünn
Aliase über die C-Strukturen, kein separates Eigentumsmodell.

Dadurch wird keine vollständige Connector-API implementiert. Es definiert neutrale Datenformen
dass spätere Connector-Adapter in libmodsecurity v3-Aufrufe übersetzen können.

Das Projekt zeichnet die vollständige Entscheidung zwischen C und C++ auf
`docs/architecture/c-vs-cpp-decision.md`. Kurz gesagt: Produktsteckerkerne bleiben C-first,
C++ bleibt auf Thin Wrapper, Build-/Test-Dienstprogramme und optionale Hilfsprogramme beschränkt
Programme und C++-Objekte dürfen Apache, NGINX oder zukünftige Server-ABI nicht überschreiten
Grenzen.

## Phase 1 Gründung

Die erste kontrollierte Refaktorierungsphase fügt nur kleine steckerneutrale Daten hinzu
Formen:

- `intervention.h` stellt die von einer Eingriffsprüfung zurückgegebenen Daten dar, aber
  entscheidet nicht, wie ein Server die Antwort sendet.
- `status.h` definiert generische Operationsergebnisse, keine HTTP-Statuscodes.
- `origin.h` zeichnet Quell-/Versions-/Lizenzmetadaten auf und impliziert keinen Code
  Eigentums- oder Importstatus.

Vorhandene `request.h`, `response.h`, `transaction.h`, `logging.h` und
`capabilities.h` bleiben steckerneutral. `capabilities.h` ist das Kanonische
Capability-Header; Es wird kein Duplikat `capability.h` eingeführt.

`transaction.h` besitzt auch die kleine `msconnector_decision`-Form, die von Open verwendet wird
Connector-Adapter, um den Neutralstatus, den Eingriff, die Regel-ID und den Grund zurückzugeben
Daten, ohne Connector-lokale Ergebnistypen zu erstellen.

## Runtime-Smoke-Evidence-Helfer

Steckverbinderneutrale Rauchergebnishelfer leben unter `common/scripts/`, nicht unter dem
öffentliche C-Header. Sie zentralisieren das JSON-Schreiben von Ergebnissen/Beweisen für offene Zwecke
Konnektorkabelbäume, während die Laufzeit-ABI auf Anforderung, Antwort,
Intervention, Status, Protokollierung, Fähigkeiten, Ursprung, Transaktion und Entscheidung
Daten.

Diese Helfer schreiben möglicherweise häufige Rauchartefakte wie `result.json`,
`summary.json`, `summary.txt` und `results.jsonl`. Sie dürfen nicht enthalten
Serverspezifische Bedingungen oder hängen von Envoy, Traefik, lighttpd, Apache, HAProxy oder ab
Nginx-SDKs.

Die Erkennung von Laufzeitabhängigkeiten gehört zu den Shell-Helfern des Test-Frameworks
Quelle `modules/ModSecurity-test-Framework/ci/lib/common.sh`. Stecker muss rauchen
Verwenden Sie von common.sh verwaltete Pfade oder explizite Umgebungsvariablen wie z
`ENVOY_BIN`, `TRAEFIK_BIN` und `LIGHTTPD_BIN`. Sie dürfen keine Runtime installieren
Komponenten greifen global oder stillschweigend auf das System `PATH` zurück.

Die Suchreihenfolge ist zuerst die explizite binäre Umgebungsvariable und dann die lokale
common.sh-verwaltete Roots wie `$CONNECTOR_COMPONENT_CACHE`,
`$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
`$VERIFIED_RUN_ROOT` und `$SOURCE_ROOT`. Fehlt eine Abhängigkeit, raucht es
muss BLOCKIERTE Beweise schreiben und 77 verlassen. Envoy, Traefik und lighttpd dürfen eingestellt werden
`runtime_verified=true` erst nach `common/scripts/run_local_runtime_smoke.py`
beweist echtes lokales HTTP 200/403-Verhalten durch die aufgelöste Binärdatei und die
ausgewählten Integrationsmodus.

`common.sh` besitzt auch die Standardeinstellungen für Open-Connector-Komponenten: `ENVOY_*`,
`TRAEFIK_*` und `LIGHTTPD_*` Komponenten-Roots, Laufzeit-Roots, Konfigurations-Roots, Protokoll
Wurzeln, Ergebniswurzeln, binäre Standardeinstellungen, Smoke-Ports, Upstream-/Authz-Ports und
Standardeinstellungen für den Integrationsmodus. Es definiert nur diese Werte; es schafft nicht
Verzeichnisse, Validierung von Laufzeiten, Herunterladen von Artefakten oder Installieren von Abhängigkeiten.

Das Staging lokaler Komponenten wird durch explizite Vorbereitungsskripts gehandhabt:
`prepare-envoy-runtime.sh`, `prepare-traefik-runtime.sh` und
`prepare-lighttpd-runtime.sh`. Ohne `ALLOW_RUNTIME_DOWNLOADS=1`, diese
Skripte melden eine vorhandene lokale Binärdatei, wenn vorhanden, und beenden andernfalls 77
ohne herunterzuladen. Mit expliziter Einwilligung laden sie nur die angehefteten Inhalte herunter
Komponentenartefakt, überprüfen Sie den `common.sh` SHA256 vor dem Staging und schreiben Sie nur
unter `$CONNECTOR_COMPONENT_CACHE`. Envoy stellt eine direkte Binärdatei bereit; Traefik
extrahiert nur die erwartete Binärdatei `traefik` aus ihrem Tarball; Lighttpd-Stufen
verifizierte Quelle und unterstützt einen expliziten lokalen `ALLOW_RUNTIME_BUILDS=1`-Build
unter `$CONNECTOR_COMPONENT_CACHE/lighttpd`. Lighttpd Phase 1 verwendet
`integration_mode=sidecar_proxy`: Der Rauch startet einen lokalen Lighttpd stromaufwärts und
einen lokalen Sidecar-Entscheidungs-Proxy, bevor Laufzeitnachweise festgelegt werden.

Envoy, Traefik und lighttpd unterstützen auch ein optionales Targeting
libmodsecurity-unterstützter Smoke durch Setzen von `DECISION_BACKEND=libmodsecurity` oder
Verwenden Sie die Connector-spezifischen Make-Verknüpfungen. Hier liegt eine zweite Evidenzebene vor
Oben auf dem einfachen Entscheidungs-Service-Rauch. Der Shared Runner wird geladen
`common/rules/modsecurity_targeted_smoke.conf` erstellt einen lokalen Testauswerter
gegen lokale, von common.sh verwaltete libmodsecurity-Header und -Bibliotheken und sendet
`X-Modsec-Smoke: block` über den Proxy-Authentifizierungspfad. Nur dieser gezielte Modus darf
Legen Sie `modsecurity_backend_verified=true` fest, und zwar nur, wenn das Entscheidungsprotokoll angezeigt wird
libmodsecurity hat die Regel `1000001` geladen und einen 403-Eingriff zurückgegeben. Fehlt
Lokale libmodsecurity-Header/Bibliotheken erzeugen Exit 77/BLOCKED-Beweise mit
`decision_backend=libmodsecurity` und `modsecurity_backend_verified=false`.
Der Resolver wird in `connector-smoke-common.sh` geteilt; es akzeptiert nur explizite
lokale Überschreibungen oder von common.sh verwaltete externe Laufzeit-/Komponentenstämme und
lehnt System-/PATH-Fallbacks für libmodsecurity ab. Der genaue Aufrufstamm lautet
werden als Ausführungsmetadaten aufgezeichnet und nicht als entwicklerlokaler Pfad dokumentiert.

Derselbe Läufer mit offenem Anschluss unterstützt auch minimale und sekundäre CRS-Rauchungen
mit `DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs` oder dem
Connector-spezifische CRS Make-Ziele.
Die CRS-Quelle der Wahrheit bleibt in `common.sh`: `CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR` und `CRS_RUNTIME_DIR`. Der Läufer kann eine bereits abwickeln
gestaffelter CRS-Checkout nur von durch common.sh verwalteten, verifizierten externen Roots; es
lädt CRS nicht herunter, installiert CRS nicht global und durchsucht keine Systempfade. Die
Die generierte Rauchkonfiguration wird unten beschrieben
die Connector-Laufzeit/Ergebnis-Root als `crs-smoke/` für den Minimalfall und
`crs-secondary-smoke/` für den sekundären Fall.

Der minimale CRS-Rauch verwendet die vorhandene `crs_sqli_anomaly_block`-Nutzlast wieder.
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`. Ein PASS erfordert eine
zulässige Anfrage mit HTTP 200, eine CRS-gestützte blockierte Anfrage mit HTTP 403 und
eine beobachtete CRS-Regel-ID/-Nachricht aus libmodsecurity-Interventionsnachweisen. Nur
Dieser Beweis kann `crs_minimal_smoke_verified=true` festlegen. Es darf nicht untergehen
`crs_complete=true`, `production_ready=true`, `full_matrix_ready=true` oder
`response_body_verified=true`. CRS führt write `crs-result.json` und aus
`crs-decision.log`; gezielte libmodsecurity-Läufe behalten `targeted-result.json` bei
und `modsecurity-decision.log`.

Der sekundäre CRS-Rauch verwendet denselben CRS-Resolver und Läufer, ausgewählt mit
`CRS_SMOKE_CASE=secondary` oder `smoke-envoy-crs-secondary`,
`smoke-traefik-crs-secondary`, `smoke-lighttpd-crs-secondary` und
`smoke-open-connectors-crs-secondary` Ziele erstellen. Es sendet
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E` und muss das beobachtete CRS extrahieren
Regel-ID/Nachricht von libmodsecurity Audit/Interventionsnachweis. Ein gelungener
Sekundärlauf kann `crs_secondary_smoke_verified=true` setzen und schreiben
`crs-secondary-result.json`, `crs-secondary-decision.log` und
`crs-secondary-audit.log`. Wenn CRS, libmodsecurity und die Laufzeit vorhanden sind
aber die Sekundärsonde nicht blockiert ist, ist das Ergebnis FAIL. Fehlendes CRS,
fehlende libmodsecurity oder fehlende Laufzeitabhängigkeiten bleiben Exit 77/BLOCKED
Beweise.

Offizielle Quellmetadaten für diese Open-Connector-Laufzeitkomponenten werden nachverfolgt
in `modules/ModSecurity-test-Framework/ci/provisioning/runtime-components.manifest.json`.
Die festen Versionen, offiziellen Quell-URLs, Download-URLs und SHA256-Werte sind
definiert in `common.sh`; Das Manifest spiegelt sie wider, sodass sie maschinenlesbar sind
Inventar. Downloads sind standardmäßig deaktiviert und nur über erlaubt
explizit `ALLOW_RUNTIME_DOWNLOADS=1` Bereiten Sie Ziele mit SHA256-Überprüfung vor
in `$CONNECTOR_COMPONENT_CACHE`.

Der manuelle GitHub Actions-Workflow
`.github/workflows/open-connectors-smoke.yml` führt zuerst das vorhandene aus
`prepare-runtime-components`-Ziel zur Bereitstellung gemeinsam genutzter lokaler libmodsecurity und CRS
Eingaben unter common.sh-verwalteten Roots und bereitet dann Envoy, Traefik und Lighttpd vor
Laufzeitkomponenten vor der Ausführung der einfachen Laufzeit, gezielte libmodsecurity,
minimales CRS und sekundäres CRS raucht mit `TMPDIR=/tmp`. Es kopiert
`/tmp/ModSecurity-conector-verified/` in `ci-artifacts/open-connectors/` und
lädt dieses Verzeichnis als `open-connectors-smoke-evidence` hoch, einschließlich danach
Fehler vorbereiten oder rauchen. Der temporäre, schmale `push`-Trigger im Workflow
Die Datei dient lediglich als Diagnosehilfe. Das Workflow-Artefakt dient nur als Beweis; das tut es
Fördern Sie nicht die Produktionsbereitschaft, die Vollmatrixbereitschaft, die CRS-Vollständigkeit oder
Unterstützung des Antwortkörpers.

## libmodsecurity v3-Ausrichtung

Die Phasennamen spiegeln die öffentliche v3-Transaktionssequenz wider:

- Verbindungsmetadaten
- URI
- Header anfordern
- Anforderungstext
- Antwortheader
- Antwortkörper
- Protokollierung

Die eigentlichen Aufrufe von libmodsecurity gehören zu Connector-Adaptern oder einem Future
Engine-zugewandte Ebene mit expliziten Eigentumsregeln. Sie sind nicht darin versteckt
`common/`, bis ihre Lebensdauer, Fehler und Bereinigungsverträge dokumentiert sind.

## Offene Arbeit

Verfolgt in `docs/roadmap/todo-inventory.md`:

- gemeinsame Eigentumsregeln für Header- und Body-Puffer;
- zukünftige Verwendung neutraler Statuswerte durch die Adapter-API;
- Kompilierungstests, die beweisen, dass gemeinsame Header unabhängig von jedem Connector bleiben.
