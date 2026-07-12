> Status: Historisch
> Ersetzt durch: [../current/six-connector-core-completion.de.md](../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Archivierter Snapshot der Connectoren vor dem kanonischen Modell

**Sprache:** [English](connector_status_remaining.md) | Deutsch

> **Historisches Archiv — durch das kanonische No-CRS-Modell abgelöst.**
>
> Die nachfolgende Analyse bleibt ausschließlich als Snapshot vor der
> Host-Integration erhalten. Sie ist kein aktueller Status, keine
> Capability-Deklaration, kein Runtime-Nachweis und kein Umsetzungsplan.
> Insbesondere die Aussagen, Envoy, Traefik und lighttpd seien nur Starter ohne
> Runtime, sind überholt.
>
> Für den aktuellen Branch-Stand gelten der generierte
> [No-CRS-Gesamtsnapshot](../current/all-connectors-no-crs-baseline.de.md) und die
> [kanonische Capability-Matrix](../testing/generated/canonical/connector-capabilities.generated.de.md).
> Sie trennen Implementierungsgrenzen von verifizierter Evidence und sind die
> alleinige Quelle für den kanonischen No-CRS-Status.
>
> Die aktuellen Host-Pfade sind Envoy HTTP `ext_authz`, Traefik HTTP
> `forwardAuth` und das native lighttpd-Plugin. Ihre Existenz ist kein
> kanonischer PASS: Bis ein kanonisches `result.json` vorliegt, bleibt der
> generierte No-CRS-Snapshot `NOT EXECUTED`; ein Starter oder lokaler Self-Test
> darf ihn nicht heraufstufen.

## Zusammenfassung

Apache, HAProxy und Nginx werden hier nur als Referenzrahmen genannt. Sie
gelten nach Vorgabe als fertig und wurden nicht erneut bewertet.

Gefunden wurden drei Nicht-Referenz-Connectoren mit eigenen
Connector-Verzeichnis:

- `connectors/envoy/`
- `connectors/lighttpd/`
- `connectors/traefik/`

Zusätzlich existieren zwei geplante bzw. bewusst nicht unabhängige
Kandidaten in Roadmap-/Onboarding-Unterlagen:

- LiteSpeed / OpenLiteSpeed: nur geplant, ohne `connectors/litespeed/`.
- OpenResty: ausdrücklich als Nginx-Variante bzw. durch den
  vorhandener Nginx-Connector abgedeckt, nicht als eigener Connector.

`connectors/_template/` ist nur eine Scaffold-Vorlage und kein Connector. Unter
`examples/` gibt es aktuell nur Apache-, HAProxy- und Nginx-Spiele; für
Envoy, Lighttpd, Traefik, LiteSpeed und OpenResty existieren keine
Beispielkonfigurationen.

Wichtig zur Prüfart: Es wurden keine Builds, Tests oder Smokes ausgeführt. Stirb
Bewertung basiert auf gelesenen Dateien, Make-/CI-Targets, Dokumentation,
TODOs, Roadmap-Hinweise und vorhandene Report-Artefakten.

Gesamtbild: Keiner der weiteren Connectoren ist fertig oder
laufzeitverifiziert. Envoy, Lighttpd und Traefik besitzen Dokumentation,
Metadaten, Source-Maps, lokaler C-Starter und blockierte Runtime-Smoke-
Einstiegspunkte. Diese Starter verfügen über Compile-/Self-Test-Fähigkeit für lokale
Probe-Modelle, aber kein echtes Server-/Proxy-Traffic-Handling, keine
libmodsecurity-Transaktionen, keine CRS-Ausführung, keine Audit-Logs und kein
`RESPONSE_BODY`-Blockierung.

Sicherheits- und Evidence-Hinweise sind im Projekt sehr konservativ: Neue
Connectoren dürfen keine Runtime-, CRS-, Full-Matrix- oder Production-Claims enthalten
machen, bevor `result.json`, Logs, Decision-/Audit-Evidence und sicher
Runtime-Pfade vorhanden sind. Die aktuellen Harness-Skripte erzwingen
Artefaktpfade unter `BUILD_ROOT`/`BUILD_ROOT/results`/`BUILD_ROOT/logs` und
Schreiben Sie nicht in den Connector-Checkout.

## Gefundene Connectoren außer Apache, HAProxy und Nginx

| Connector | Status | Build vorhanden | Tests vorhanden | Doku vorhanden | Nächster Schritt |
|---|---|---|---|---|---|
| Envoy | Stub, buildbarer Bridge-Starter, runtime nicht verifiziert | Ja: `connectors/envoy/Makefile`, `connectors/envoy/build/build_metadata.sh`; kein produktiver Envoy-/ModSecurity-Build | Nur lokaler CLI-Self-Test und blockierter `make smoke-envoy`; CI prüft Struktur | Ja | `ext_proc` vs. `ext_authz` entscheiden und targeted Envoy-Runtime-Smoke mit 403-Evidence bauen |
| Lighttpd | Stub, buildbarer Bridge-Starter, runtime nicht verifiziert | Ja: `connectors/lighttpd/Makefile`, `build/build_starter.sh`, `build/bridge_starter.sh`; kein lighttpd-Modul/FastCGI/SCGI-Build | Nur Starter-Self-Tests und blockierter `make smoke-lighttpd`; CI prüft Struktur | Ja | Architekturentscheidung native Module vs. FastCGI/SCGI/Sidecar, danach Request-Blocking-Proof |
| Traefik | Stub, Decision-Service-Starter, runtime nicht verifiziert | Ja: `connectors/traefik/Makefile`, `build/build-starter.sh`; kein Traefik-Plugin/Middleware/forwardAuth-Runtime-Build | Nur lokaler Decision-Service-Self-Test und blockierter `make smoke-traefik`; CI prüft Struktur | Ja | `forwardAuth`-/Decision-Service-Proof mit echter Traefik-Anfrage und 403-Evidence |
| LiteSpeed / OpenLiteSpeed | nur geplant | Nein | Nein | Ja, roadmap-only | Erst Install-/Lizenz-/Start-Proof für OpenLiteSpeed plus ein CRS/Request-Blocking-Smoke |
| OpenResty | kein eigener Connector; durch Nginx abgedeckt | Nein | Nein | Ja, roadmap-only | Nicht separat anlegen; höchstens später Nginx-Kompatibilitäts-Smoke |

## Detailanalyse pro Connector

### Envoyr
- Status:
  - Stub / `partial_skeleton`.
  - In den Connector-Dateien als `bridge-starter` und `Laufzeitstatus:
    nicht verifiziert` beschrieben.
  - Kein fertiger Connector, keine Runtime-Verifikation.
- Relevante Dateien:
  - `connectors/envoy/README.md`
  - `connectors/envoy/TODO.md`
  - `connectors/envoy/ORIGIN.md`
  - `connectors/envoy/SOURCE_MAP.json`
  - `connectors/envoy/metadata.c`
  - `connectors/envoy/metadata.h`
  - `connectors/envoy/Makefile`
  - `connectors/envoy/build/build_metadata.sh`
  - `connectors/envoy/src/README.md`
  - `connectors/envoy/src/envoy_bridge.c`
  - `connectors/envoy/src/envoy_bridge.h`
  - `connectors/envoy/src/envoy_bridge_main.c`
  - `connectors/envoy/harness/README.md`
  - `connectors/envoy/harness/run_envoy_smoke.sh`
  - `connectors/envoy/docs/architecture.md`
  - `connectors/envoy/docs/build.md`
  - `connectors/envoy/docs/validation.md`
  - `connectors/envoy/docs/coverage-decision-matrix.md`
  - `connectors/envoy/docs/public-sources.md`
  - `modules/ModSecurity-test-Framework/ci/runtime/run-envoy-smoke.sh`
  - `modules/ModSecurity-test-Framework/tests/cases/connector-specific/envoy/README.md`
  - `.github/workflows/test-envoy.yml`
  - `reports/archive/template-verification-nginx-apache/envoy-template-alignment.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.md`
- Vorhanden:
  - Repo-lokaler C-Bridge-Starter über `envoy_bridge.*`.
  - Nutzung connector-neutraler Strukturen wie `msconnector_request`,
    `msconnector_intervention` und `msconnector_status`.
  - Lokale Build-/Self-Test-Targets:
    `make -C connectors/envoy build-starter` und
    `make -C connectors/envoy self-test`.
  - `connectors/envoy/Makefile` enthält außerdem
    `build-modsecurity-bridge`, das aktuell mit Exit 77blockiert, weil
    libmodsecurity-Header/-Libraries nicht vorhanden sind.
  - `make smoke-envoy` im Root-`Makefile`, delegiert über
    `modules/ModSecurity-test-Framework/ci/runtime/run-envoy-smoke.sh` auf
    `connectors/envoy/harness/run_envoy_smoke.sh`.
  - Das Harness-Skript schreibt bewusst BLOCKED-Evidence und endet mit 77,
    weil kein echter Envoy-Server, keine Envoy-Konfiguration und kein
    Runtime-Harness implementiert sind.
  - Struktur-CI in `.github/workflows/test-envoy.yml`.
  - Public-Source-Hinweise zu Envoy HTTP Filter, `ext_authz`, Wasm und
    Erweiterungsdokumente in `connectors/envoy/docs/public-sources.md`.
  - Roadmap empfiehlt Envoy als nächsten Proof-Kandidaten.
- Fehlend:
  - Kein nativer Envoy HTTP Filter.
  - Kein `ext_proc`-gRPC-Service.
  - Kein `ext_authz`-Service.
  - Kein proxy-wasm/Wasm-Modul.
  - Keine Envoy-Konfiguration wie `connectors/envoy/config/envoy.yaml`.
  - Keine Envoy-Binary-/Container-Pin, keine Start-/Stop-Logik, keine Ports,
    keine Upstream-App.
  - Keine libmodsecurity-Lifecycle-Implementierung, keine Ruleset-Ladung,
    keine CRS-Ausführung.
  - Keine Runtime-Logs, keine `result.json`, keine Case-Run-Artefakte.
  - Keine No-CRS-/With-CRS-Runtime-Evidence.
  - Keine Audit-/Decision-Evidence aus echtem Envoy-Traffic.
  - Keine RESPONSE_BODY-, Request-Body- oder negative/pass-through-Evidence.
  - Keine Beispiele unter `examples/envoy/`.
  - Keine ausführbaren Envoy-YAML-Cases; nur README unter
    `modules/ModSecurity-test-Framework/tests/cases/connector-specific/envoy/`.
- Risiken:
  - `ext_proc` passt semantisch besser für Request-/Body-/Response-Experimente,
    bringt aber gRPC/protobuf- und Body-Processing-Komplexität.
  - `ext_authz` ist einfacher für einen ersten 403-Block-Proof, deckt aber
    Request-Body und Response-Body sind nur eingeschränkt möglich.
  - Filter-Ordering, Header-Mutation, HTTP/2, gRPC, Streaming und
Intervention-Mapping sind unbewiesen.
  - Ein Reverse-Proxy-Setup für Apache/Nginx wäre nur Infrastruktur-Smoke; der
    ModSecurity-Entscheidung würde dann dem Downstream-Connector gehören.
  - Aktueller Starter ruft weder Envoy-APIs noch libmodsecurity auf. Daraus
    Es darf keine ModSecurity-Kompatibilität abgeleitet werden.
  - Hardening-Offenspunkte: Timeout-/Fail-open-/Fail-closed-Defaults,
    Body-Limits, Decision-Service-Isolation und Secret-/Log-Handling sind noch
    nicht definiert.
- Nächster Schritt:
  - Envoy als nächsten Connector bearbeiten, aber nur als gezielten Proof.
  - Zuerst in `connectors/envoy/docs/architecture.md` die erste
    Integrationsfläche festlegen: bevorzugt `ext_proc`, alternativ `ext_authz`
    für den kleineren 403-Proof.
  - Danach minimal erstellen/anpassen:
    `connectors/envoy/config/envoy.yaml`,
    `connectors/envoy/harness/run_envoy_smoke.sh`,
    optional `connectors/envoy/scripts/run-smoke.sh`,
    ein kleiner Decision-Service oder Ausbau unter `connectors/envoy/src/`,
    sowie ein Framework-Case wie
    `modules/ModSecurity-test-Framework/tests/cases/connector-specific/envoy/envoy_request_blocking_smoke.yaml`.
  - Nachweise müssen unter einer geprüften Runtime-Root wie
    `$VERIFIED_RUN_ROOT/envoy-smoke/` liegen und `full_matrix_ready=false`
deklarieren.

### Lighttpd
- Status:
  - Stub / `partial_skeleton`.
  - In den Connector-Dateien als `bridge-starter` und `Laufzeitstatus:
    nicht verifiziert` beschrieben.
  - Kein fertiger Connector, keine Runtime-Verifikation.
- Relevante Dateien:
  - `connectors/lighttpd/README.md`
  - `connectors/lighttpd/TODO.md`
  - `connectors/lighttpd/ORIGIN.md`
  - `connectors/lighttpd/SOURCE_MAP.json`
  - `connectors/lighttpd/metadata.c`
  - `connectors/lighttpd/metadata.h`
  - `connectors/lighttpd/Makefile`
  - `connectors/lighttpd/build/build_starter.sh`
  - `connectors/lighttpd/build/bridge_starter.sh`
  - `connectors/lighttpd/src/README.md`
  - `connectors/lighttpd/src/lighttpd_build_starter.c`
  - `connectors/lighttpd/src/lighttpd_bridge.c`
  - `connectors/lighttpd/src/lighttpd_bridge.h`
  - `connectors/lighttpd/src/lighttpd_bridge_main.c`
  - `connectors/lighttpd/harness/README.md`
  - `connectors/lighttpd/harness/run_lighttpd_smoke.sh`
  - `connectors/lighttpd/docs/architecture.md`
  - `connectors/lighttpd/docs/build.md`
  - `connectors/lighttpd/docs/validation.md`
  - `connectors/lighttpd/docs/coverage-decision-matrix.md`
  - `connectors/lighttpd/docs/public-sources.md`
  - `modules/ModSecurity-test-Framework/ci/runtime/run-lighttpd-smoke.sh`
  - `modules/ModSecurity-test-Framework/tests/cases/connector-specific/lighttpd/README.md`
  - `.github/workflows/test-lighttpd.yml`
  - `reports/archive/template-verification-nginx-apache/lighttpd-template-alignment.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.md`
- Vorhanden:
  - Repo-eigener Metadata-/Probe-Build-Starter.
  - Repo-eigener Decision-Service-Bridge-Starter mit CLI-Self-Test.
  - Lokale Ziele:
    `make -C connectors/lighttpd build-starter`,
    `make -C connectors/lighttpd self-test`,
    `make -C connectors/lighttpd build-bridge-starter`,
    `make -C connectors/lighttpd self-test-bridge`.
  - Build-Skripte schreiben laut Doku nach
    `$BUILD_ROOT/lighttpd-build-starter/` und
`$BUILD_ROOT/lighttpd-bridge-starter/`.
  - `make smoke-lighttpd` im Root-`Makefile`, delegiert über
    `modules/ModSecurity-test-Framework/ci/runtime/run-lighttpd-smoke.sh`.
  - Das Harness-Skript schreibt BLOCKED-Evidence und endet mit 77, weil kein
    jedoch lighttpd-Server, keine Konfiguration und kein Runtime-Harness
    implementiert sind.
  - Struktur-CI in `.github/workflows/test-lighttpd.yml`.
  - Public-Source-Hinweise zu lighttpd Plugin-Hooks und `mod_magnet`.
- Fehlend:
  - Kein nativer lighttpd-Modulcode.
  - Kein FastCGI-/SCGI-Protokolladapter.
  - Keine Lighttpd-Header, kein SDK, keine ausgewählte Source-Version.
  - Keine lighttpd-Include-/Library-Pfade.
  - Keine lighttpd-Konfiguration, keine Start-/Stop-Logik, kein Runtime-Harness.
  - Keine libmodsecurity-API-Integration, kein Regelladen, kein CRS.
  - Keine No-CRS-/With-CRS-Runtime-Evidence.
  - Keine Audit-/Access-/Decision-Logs aus echtem lighttpd-Traffic.
  - Keine RESPONSE_BODY-, Request-Body- oder negative/pass-through-Evidence.
  - Keine Beispiele unter `examples/lighttpd/`.
  - Keine ausführbaren Lighttpd-YAML-Cases; nur README unter
    `modules/ModSecurity-test-Framework/tests/cases/connector-specific/lighttpd/`.
- Risiken:
  - Integrationspfad ist offen: native Plugin-Integration, FastCGI/SCGI,
    Externer Service oder Sidecar/Proxy.
  - Request-Body-Verfügbarkeit, Response-Filter-Hooks und Plugin-Lifecycle
    sind unbewiesen.
  - Stabile Verpackung für ein lighttpd-Modul ist offen.
  - Ein Sidecar/Proxy könnte praktischer sein, müsste aber echtes sein
    Request-Mapping, Intervention-Mapping und Fail-open-/Fail-closed-Verhalten
    sauber belegen.
  - Aktueller Bridge-Self-Test ist nur lokales Probe-Modell und keines
    Laufzeit-Block-Nachweis.
- Nächster Schritt:
  - Zuerst eine Machbarkeitsentscheidung in
    `connectors/lighttpd/docs/architecture.md`: natives Modul vs.
    FastCGI/SCGI vs. Sidecar/Proxy.
  - Danach ein gezielter Request-Blocking-Proof mit minimaler
    lighttpd-Konfiguration, echte HTTP-Anfrage, `result.json`,
    Server-/Decision-Logs und Cleanup-Logik.
  - Erste betroffene Dateien:
    `connectors/lighttpd/docs/architecture.md`,
    `connectors/lighttpd/docs/build.md`,
    `connectors/lighttpd/harness/run_lighttpd_smoke.sh`,
    optional `connectors/lighttpd/config/` oder
`connectors/lighttpd/scripts/`, plus ein Framework-Case unter
    `modules/ModSecurity-test-Framework/tests/cases/connector-specific/lighttpd/`.

### Traefik
- Status:
  - Stub / `partial_skeleton`.
  - In den Connector-Dateien als `decision-service-starter` und
    `Runtime status: not-verified` beschrieben.
  - Kein fertiger Connector, keine Runtime-Verifikation.
- Relevante Dateien:
  - `connectors/traefik/README.md`
  - `connectors/traefik/TODO.md`
  - `connectors/traefik/ORIGIN.md`
  - `connectors/traefik/SOURCE_MAP.json`
  - `connectors/traefik/metadata.c`
  - `connectors/traefik/metadata.h`
  - `connectors/traefik/Makefile`
  - `connectors/traefik/build/build-starter.sh`
  - `connectors/traefik/src/README.md`
  - `connectors/traefik/src/traefik_build_starter.c`
  - `connectors/traefik/src/traefik_decision_service.c`
  - `connectors/traefik/src/traefik_decision_service.h`
  - `connectors/traefik/src/traefik_decision_service_main.c`
  - `connectors/traefik/harness/README.md`
  - `connectors/traefik/harness/run_traefik_smoke.sh`
  - `connectors/traefik/docs/architecture.md`
  - `connectors/traefik/docs/build.md`
  - `connectors/traefik/docs/validation.md`
  - `connectors/traefik/docs/coverage-decision-matrix.md`
  - `connectors/traefik/docs/public-sources.md`
  - `modules/ModSecurity-test-Framework/ci/runtime/run-traefik-smoke.sh`
  - `modules/ModSecurity-test-Framework/tests/cases/connector-specific/traefik/README.md`
  - `.github/workflows/test-traefik.yml`
  - `reports/archive/template-verification-nginx-apache/traefik-template-alignment.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.md`
- Vorhanden:
  - Repo-eigener Metadata-Build-Starter.
  - Repo-eigener lokaler Decision-Service-Starter in C für In-Memory-
    Allow/Block-Entscheidungen.
  - Lokale Ziele:
    `make -C connectors/traefik build-starter`,
    `make -C connectors/traefik build-decision-service`,
    `make -C connectors/traefik self-test-decision-service`.
  - Kompatibilitäts-Aliase `build-forwardauth-starter` und
    `self-test-forwardauth`, die aktuell denselben lokalen Decision-Service-
Starter und noch kein echtes `forwardAuth` beweisen.
  - `make smoke-traefik` im Root-`Makefile`, delegiert über
    `modules/ModSecurity-test-Framework/ci/runtime/run-traefik-smoke.sh`.
  - Das Harness-Skript schreibt BLOCKED-Evidence und endet mit 77, weil kein
    echter Traefik-Server, keine Konfiguration und kein Runtime-Harness
    implementiert sind.
  - Struktur-CI in `.github/workflows/test-traefik.yml`.
  - Dokumentierte Optionen: Plugin, Middleware, `forwardAuth`/externer Dienst,
    Sidecar/Proxy, Benutzerdefinierter Build.
- Fehlend:
  - Kein Traefik-Go-Plugin.
  - Keine Middleware, kein Go-Modul, keine Traefik-API-Integration.
  - Kein echter `forwardAuth`-HTTP-Service.
  - Keine Traefik-Konfiguration, kein Traefik-Binary-/Container-Harness.
  - Keine libmodsecurity-Lifecycle-Integration, kein Regelladen, kein CRS.
  - Keine Runtime-Logs, keine `result.json`, keine Case-Run-Artefakte aus
    echter Traefik-Traffic.
  - Keine No-CRS-/With-CRS-Runtime-Evidence.
  - Keine RESPONSE_BODY-, Request-Body-, Audit-/Log- oder
    negative/pass-through-Evidence.
  - Keine Beispiele unter `examples/traefik/`.
  - Keine ausführbaren Traefik-YAML-Cases; nur README unter
`modules/ModSecurity-test-Framework/tests/cases/connector-specific/traefik/`.
- Risiken:
  - Traefik Plugin-Sandbox, Yaegi/Wasm und Go-Modul-Abhängigkeiten können sterben
    libmodsecurity-Distribution erschweren.
  - Request-Body-Buffering und Response-Mutation sind unbewiesen.
  - Ein Go-Plugin zu früh zu bauen könnte die einfachere Frage verdecken, ob
    ein `forwardAuth`-/Decision-Service überhaupt den ersten 403-Proof sauber
    leisten kann.
  - Aktueller Starter hat keine HTTP-Server-Komponente; `forwardAuth` ist nur
    als Alias benannt, nicht implementiert.
  - Hardening-Offenspunkte: Auth-Service-Timeouts, Fail-open-/Fail-closed-
    Entscheidung, Request-Body-Limits, Header-Sanitizing und Log-/Secret-
    Behandlung.
- Nächster Schritt:
  - Nicht sofort Plugin/Middleware bauen. Erst einen `forwardAuth`-/Decision-
    Service-Proof erstellen, der Traefik startet, eine bekannte Anfrage an den
    Decision-Service schickt und HTTP 403 mit `result.json` und Logs beweist.
  - Erste betroffene Dateien:
    `connectors/traefik/docs/architecture.md`,
    `connectors/traefik/docs/build.md`,
    `connectors/traefik/harness/run_traefik_smoke.sh`,
    optional `connectors/traefik/config/` oder
`connectors/traefik/scripts/`, plus ein Framework-Case unter
    `modules/ModSecurity-test-Framework/tests/cases/connector-specific/traefik/`.

### LiteSpeed / OpenLiteSpeed
- Status:
  - Nur geplant.
  - Kein eigenes Connector-Verzeichnis.
  - Roadmap-Kandidat, nicht runtime-verifiziert.
- Relevante Dateien:
  - `docs/architecture/new-connector-onboarding.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.json`
  - `ci/evidence/reports/generate-connector-roadmap.py`
- Vorhanden:
  - Roadmap-Eintrag für LiteSpeed/OpenLiteSpeed.
  - Empfehlung, zuerst OpenLiteSpeed als CI-freundlichere Variante zu prüfen.
  - Geplanter erster Nachweis: Install-/Start-Proof plus ein CRS-/Request-
    Blocking-Smoke, fällt Automatisierung und Lizenz es erlauben.
- Fehlend:
  - Kein `connectors/litespeed/`.
  - Keine README, TODO, ORIGIN, SOURCE_MAP, Metadaten, Build-Skripte, Harness,
    Konfiguration oder Beispiele.
  - Keine Make-Targets.
  - Keine CI-Workflows.
  - Keine Framework-Fälle.
  - Keine Runtime-Evidence, kein `result.json`, keine Logs.
- Risiken:
  - Lizenz- und Download-Automatisierung.
  - Unterschiede zwischen OpenLiteSpeed ​​und LiteSpeed ​​Enterprise Edition.
  - Paketverfügbarkeit und CI-Reproduzierbarkeit.
  - ModSecurity-/CRS-Kompatibilität darf nicht angenommen werden.
- Nächster Schritt:
  - Noch kein Connector-Scaffold, vor Installierbarkeit, Lizenzpfad und
    minimaler Start reproduzierbar belegt sind.
  - Zuerst eine Feasibility-Notiz oder ein Roadmap-Update mit Install-Log,
    Start-Log, Minimal-Konfiguration, Request-Transcript und Zielstruktur für
    `result.json`.

### OpenResty
- Status:
  - Kein eigener Connector.
  - Als Nginx-basierte Variante durch den bestehenden Nginx-Connector
    Abgedeckt.
  - Roadmap-Status sinngemäß `covered_by_existing_connector`.
- Relevante Dateien:
  - `docs/architecture/new-connector-onboarding.md`
  - `docs/architecture/connector-contract.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.md`
  - `reports/testing/generated/manifest/connector-roadmap.generated.json`
  - `ci/evidence/reports/generate-connector-roadmap.py`
- Vorhanden:
  - Architekturentscheidung: OpenResty soll aktuell nicht als separater
    Connector geführt werden.
  - Zukünftiger Kompatibilitäts-Smoke darf höchstens als Nginx-Runtime-Variante
    entstehen.
- Fehlend:
  - Kein `connectors/openresty/`.
  - Keine separate Doku, kein Build, kein Test, keine CI, keine Berichte, keine
    Voll-Matrix-Zeilen.
- Risiken:
  - Ein separater Connector würde Ownership, Reports und Full-Matrix-Zeilen enthalten
    duplizieren und könnte falsche Kompatibilitäts-Claims erzeugen.
  - OpenResty-spezifische Lua-/Nginx-Modulinteraktionen wären bei Bedarf als
    Nginx-Variante separat zu beweisen.
- Nächster Schritt:
  - Keine eigene Connector-Arbeit starten.
  - Falls relevant, eine Nginx-geführte OpenResty-Kompatibilitätsentscheidung
    oder später einen Nginx-Variant-Smoke definieren.

## Offene Fragen

- Envoy: Soll der erste Nachweis `ext_proc` oder `ext_authz` verwenden?
  `ext_proc` ist semantisch breiter, `ext_authz` ist für den ersten 403-Proof
  einfacher.
- Envoy: Soll der erste Decision-Service bereits echte libmodsecurity-
  Transaktionen ausführen oder nur einen ModSecurity-ähnlichen Deny-Pfad
  beweisen?
- Lighttpd: Native Plugin-Integration, FastCGI/SCGI oder Sidecar/Proxy?
- Traefik: Reicht ein `forwardAuth`-Proof als erster Runtime-Nachweis, bevor ein
  Go-Plugin oder Middleware-Prototyp wird gestartet?
- LiteSpeed: Ist OpenLiteSpeed rechtlich und technisch reproduzierbar in CI
  installierbar?
- OpenResty: Gibt es konkrete OpenResty-spezifische Risiken, die nicht schon
  durch den Nginx-Connector erfasst werden?
- Framework: Soll für Envoy, Lighttpd und Traefik echt sein
  Connector-spezifische YAML-Fälle unter
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
  entstehen?
- Reporting: Ab welchem gezielten Proof sollen neue Laufzeitberichte generiert werden
  Erlaubt werden, ohne Full-Matrix- oder Merge-Readiness-Claims zu erzeugen?
- Härtung: Welche Fail-open-/Fail-closed-, Timeout-, Body-Limit-, Audit-,
  Decision-Log- und Secret-Handling-Defaults sollen externe Decision-Services sein
bekommen?
- Roadmap-Hygiene: `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
  enthält noch ältere Hinweise wie `Status: unknown` für Envoy, Lighttpd und
  Traefik; Die aktuellen Connector-Dateien sind spezifischer und sollten bei
  die nächste Roadmap-Aktualisierung maßgeblich sein.

## Priorisierte Roadmap

1. Envoy als nächsten Connector bearbeiten.
   - Warum: Es gibt bereits `connectors/envoy/`, Metadaten, Source-Map,
     Bridge-Starter, Make-Targets, Harness-Entrypoint und eine klare
     Roadmap-Empfehlung. Envoy hat mit `ext_proc` und `ext_authz` realistische
     HTTP-Control-Points für einen eng begrenzten Request-Blocking-Proof.
   - Ziel: Ein gezielter Runtime-Smoke, kein Full-Matrix-Start.
   - Zuerst anpassen/erstellen:
     `connectors/envoy/docs/architecture.md`,
     `connectors/envoy/TODO.md`,
     `connectors/envoy/README.md`,
     `connectors/envoy/config/envoy.yaml`,
     `connectors/envoy/harness/run_envoy_smoke.sh`,
     optional `connectors/envoy/scripts/run-smoke.sh`,
     Entscheidungs-Service-Code gemäß `connectors/envoy/src/`,
     und ein Fall unter
     `modules/ModSecurity-test-Framework/tests/cases/connector-specific/envoy/`.
   - Erfolgskriterium: Envoy startete lokal, eine wohlwollende Anfrage erreichte den
     Upstream, ein bekannter Deny-Request liefert HTTP 403 über Envoy, und
     `result.json`, Envoy-Logs, Decision-Service-Logs sowie Case-Run-Artefakte
     liegen unter einer sicheren Runtime-Root.

2. Traefik als zweiter praktischer Proof vorbereiten.
   - Warum: Dieser Decision-Service-Starter passt gut zu einem
     `forwardAuth`-Proof und könnte Architekturwissen für externe
     Decision-Services liefern.
   - Zuerst anpassen/erstellen:
     `connectors/traefik/docs/architecture.md`,
     `connectors/traefik/harness/run_traefik_smoke.sh`,
     `connectors/traefik/config/`,
     `connectors/traefik/scripts/`,
     und ein Framework-Case unter
     `modules/ModSecurity-test-Framework/tests/cases/connector-specific/traefik/`.

3. Lighttpd erst nach Architekturentscheidung weiterziehen.
   - Warum: Ohne Entscheidung natives Modul vs. FastCGI/SCGI vs. Sidecar/Proxy
     ist Build- und Harness-Arbeit zu ungerichtet.
   - Zuerst anpassen:
     `connectors/lighttpd/docs/architecture.md`,
     `connectors/lighttpd/docs/build.md`,
     `connectors/lighttpd/harness/run_lighttpd_smoke.sh`.

4. LiteSpeed ​​/ OpenLiteSpeed ​​nur als Feasibility-Spike.
   - Warum: Es gibt kein Connector-Verzeichnis und hohe Lizenz-/Installations-
     und CI-Risiko.
   - Zuerst erstellen:
     Feasibility-Notiz oder Roadmap-Ergänzung mit Install-/Start-Proof,
     Minimal-Konfiguration und geplanter Evidence-Struktur. Erst danach
     `connectors/litespeed/` anlegen.

5. OpenResty nicht als eigener Connector starten.
   - Warum: Die Architektur ordnet OpenResty dem Nginx-Connector zu.
   - Zuerst nur bei Bedarf dokumentieren:
     Nginx-geführte Kompatibilitätsentscheidung oder später ein
     OpenResty-Smoke als Nginx-Runtime-Variante, ohne eigene Reports und ohne
     eigene Full-Matrix-Zeilen.
