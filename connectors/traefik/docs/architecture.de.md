# Traefik-Architektur

**Sprache:** [English](architecture.md) | Deutsch

Status: ForwardAuth-Kompatibilitätsrauch plus eine nicht beworbene Host-Probe für native lokale Plugins
Laufzeitstatus: Das allgemeinere Regelverhalten ist nicht überprüft

Bei der ausgewählten Integrationsarchitektur handelt es sich um einen externen HTTP-Autorisierungsdienst
über `forwardAuth` mit Traefik verbunden. Der Connector besitzt ein C17-Hostprofil,
Thin Request/Response Mapper-Funktionen, ein Service-Einstiegspunkt, Build Glue und
Beispielkonfiguration. Die Engine, Transaktion, Limit, Entscheidung und HTTP
Die Service-Implementierung bleibt unter `common/runtime/` konnektorneutral.

Globale Gerüsttore bleiben drin
`reports/archive/template-verification-nginx-apache/connector-scaffold-decisions.md`.

## Repository-Beweise

- `common/include/msconnector/` stellt konnektorneutrale Metadaten bereit,
  Fähigkeit, Ursprung, Status, Anfrage, Antwort, Transaktion und Intervention
  Datenformen.
- `common/src/` bietet connector-neutrale Hilfsimplementierungen.
- Apache und NGINX behalten serverspezifische Lebenszyklen, Hooks, Filter, Builds usw. bei
  Nutzen Sie die Logik in adaptereigenen Connector-Bäumen.
- `native_middleware/` ist ein Repository-eigenes Go-Modul mit Traefik-Form
  Einstiegspunkte `CreateConfig`, `New` und `ServeHTTP`. Es gibt kein Traefik SDK oder
  CGO-Abhängigkeit; Sein ausgewählter `uds`-Modus erreicht den separat gebauten
  persistenter Common/libmodsecurity-Dienst über eine private UDS-Sitzung pro
  Host-Anfrage.
- In `connectors/traefik` ist keine Traefik-Laufzeitquelle vorhanden.

## Entscheidung über den Integrationspfad

Implementierter Pfad: externe `forwardAuth`-Dienstquelle.

`traefik_forwardauth_service_main.c` registriert den Connector-Namen und die Integration
Modus, Original-URI-Header-Präferenz und Mapper-Rückrufe mit dem neutralen HTTP
Autorisierungsdienst. Der Dienst unterstützt explizite `--check-config` und
`--serve`-Modi. Der Laufzeitstatus bleibt bis zum aktuellen Commit-Beweis ungeprüft
beweist den integrierten Service hinter einem echten Traefik-Anfragepfad.

## Optionsbewertung

| Option | Aktuelle Entscheidung | Grund |
| --- | --- | --- |
| Traefik-Plugin | Host-Probe für den gesamten Lebenszyklus, nicht hochgestuft | Der angeheftete lokale Plugin-Host lädt `native_middleware/`, wählt seine private persistente UDS Common/libmodsecurity-Engine aus und zeichnet die Ergebnisse des Zielhosts ohne Heraufstufung auf |
| Traefik-Middleware | Host-Probe für den gesamten Lebenszyklus, nicht hochgestuft | `native_middleware/` verwendet standardmäßige Go-HTTP-Schnittstellen und eine begrenzte UDS-Engine-Naht; der gezielte Nachweis ist keine Fähigkeitsförderung |
| `forwardAuth` / externer HTTP-Entscheidungsdienst | ausgewählter Kompatibilitätspfad | Connectoreigenes Hostprofil und Service-Binärquelle; es bleibt von der nativen Sonde | getrennt |
| Beiwagen-/Proxy-Brücke | aufgeschoben | Keine Bridge-Laufzeit, Proxy-Konfiguration oder Harness vorhanden |
| Benutzerdefiniertes Modul/Build | aufgeschoben | Es existiert kein Traefik-Quell-/Build-Vertrag |

Ein zukünftiger Laufzeitpfad muss die genaue Traefik-Version/API, Quelle oder SDK dokumentieren
Herkunft, Lizenz, Build-Befehl, Konfiguration, ModSecurity-Integrationspunkt,
Anforderungs-/Antwortzuordnung, Interventionszuordnung, Protokollierungsverhalten und Laufzeit
Ergebnisse.

## Native Middleware-Host-Probe (nicht hochgestuft)

Das Go-Paket ist bewusst von der `forwardAuth`-Kompatibilität getrennt
Architektur. Der Full-Lifecycle-Läufer präsentiert es unter Traefiks Einwegartikeln
`plugins-local`-Arbeitsbereich, erstellt einen persistenten Engine-Dienst im selben
Isoliertes Root, startet den angehefteten Host, überprüft das Laden des Plugins und leitet weiter
Körpertragender Datenverkehr durch die Middleware. Es umschließt einen `net/http`-Anfragetext
in begrenzten Lesevorgängen und umschließt den Antwortschreiber mit `Flush`, `Hijack`, `Push`,
`ReadFrom` und `Unwrap` Konservierung. Es wird keine vollständige Antwort erfasst
Körper.

Vor der Zusage kann die UDS-Engine eine gezielte Ablehnungs-/Umleitungsentscheidung zurückgeben
und erhält erst nach der konkreten ResponseWriter-Aktion ein Host-Ergebnis.
Nach der Reaktionsverpflichtung wird nur eine störende prospektive Entscheidung erfasst
als `log_only`; Das Probe erhebt keinen Anspruch auf einen Reset, einen Client-Abbruch oder einen Upstream
abbrechen. Dieser Pfad ist kein Ersatz für `forwardAuth` und kann nicht geändert werden
kanonische Fähigkeitszustände. Die Host-Sonde wird bewusst nicht beworben.

## Paralleles Phasenziel

Das standardmäßige Runtime-Smoke-Ziel bleibt `integration_mode=forwardAuth`.
`runtime-smoke-traefik-native` ist ein separates Hostziel mit vollem Lebenszyklus
ändert nichts an der Phase-1-Kompatibilitätserklärung.

Verträge für gemeinsam genutzte Daten bleiben in `common/include/msconnector/`:

- `request.h` / `response.h` für HTTP-Mapping;
- `intervention.h` für Blockentscheidungen und zukünftige 403-Antworten;
- `status.h` für neutrale Pass-/BLOCKED-/Fehlerstatuswerte;
- `logging.h` für Protokolldatensätze und Rückrufform;
- `capabilities.h` für Fähigkeitsansprüche;
- `origin.h` für Quellmetadaten;
- `transaction.h` für Transaktions-/Entscheidungsansichten.

Smoke-Nachweise werden von `common/scripts/write_smoke_result.py` über generiert
`common/scripts/run_blocked_runtime_smoke.sh`. Traefik darf kein separates hinzufügen
Ergebnis/Beweis-JSON-Modell. Aktuelle GESPERRTE Beweisaufzeichnungen
`runtime_verified=false`, `production_ready=false`, `full_matrix_ready=false`,
und `crs_complete=false`.

## Protokollgrenze

Der Dienst ordnet die eingehende Autorisierungsanfrage zu und gibt möglicherweise eine Genehmigung oder zurück
störende HTTP-Entscheidung vor dem Upstream-Routing. Standardmäßig ist `forwardAuth` geeignet
Die Upstream-Antwort nicht verfügbar machen. Folglich Antwortheader und Antwort
Die Körperverarbeitung wird für diese Architektur nicht unterstützt. Der Antwort-Mapper ist
Nur registriert, damit sein gemeinsamer Vertrag weiterhin auf Kompilierung/Link geprüft bleibt.
