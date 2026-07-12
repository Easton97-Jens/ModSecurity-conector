# Traefik Build

**Sprache:** [English](build.md) | Deutsch


Status: minimal_runtime_smoke (nur ForwardAuth-Anfragepfad)
Laufzeitstatus: Verhalten des breiteren Connectors nicht überprüft

Ein Metadaten-Starter zur Kompilierungszeit und ein lokaler Entscheidungsdienst-Selbsttest bleiben bestehen
Kompatibilität. Der eigentliche Connector-Build erzeugt nun ein langlebiges externes
`forwardAuth`-Dienst, der mit der Common Runtime und libmodsecurity verknüpft ist.

## Connector-Build

```sh
MODSECURITY_INCLUDE_DIR=/local/include \
MODSECURITY_LIB_DIR=/local/lib \
make -C connectors/traefik build-connector
```

Der Build verwendet C17 mit `-Wall -Wextra -Werror`, schreibt außerhalb des Checkouts,
und führt nur die Kompilierung/Verknüpfung durch. Sein Standardartefakt ist
`$BUILD_ROOT/traefik-connector/traefik-forwardauth`.

Nachfolgende Phasen sind absichtlich getrennt:

```sh
make -C connectors/traefik check-config
make -C connectors/traefik start-smoke
make -C connectors/traefik runtime-smoke
```

Die Konfigurationsprüfung führt `--check-config` aus. Der Startrauch führt `--serve` aus,
startet echtes Traefik mit einer temporären Konfiguration des ForwardAuth-Dateianbieters und prüft
beide Prozesslebenszyklen und stoppt beide, ohne HTTP-Anfragen zu senden.
Der Laufzeitrauch ist eine dritte, separate Stufe, die echten Datenverkehr durchleitet
Traefik und der integrierte Connector-Service.

## Starterbefehle erstellen

```sh
connectors/traefik/build/build-starter.sh
make -C connectors/traefik build-starter
make -C connectors/traefik build-decision-service
make -C connectors/traefik self-test-decision-service
```

`build-forwardauth-starter` gibt jetzt einen Alias ​​für das eigentliche Kompilierungs-/Linkziel an.
`self-test-forwardauth` bleibt ein explizit lokaler Legacy-Entscheidungsmodelltest
und ist kein Laufzeitbeweis.

## Native Go-Middleware-Quellen-Build und Host-Probe

Das Repository enthält außerdem `connectors/traefik/native_middleware/`, ein Go
Modul geformt für die Middleware-Einstiegspunkte von Traefik. Es bleibt getrennt von
`build-connector`, der den C-Kompatibilitätsdienst `forwardAuth` erstellt.

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

Die ersten Zielläufe konzentrierten sich auf `go test ./...` und `go vet ./...`; der zweite
führt auch `go build ./...` aus. Die einzige beibehaltene Ausgabe ist ein Kompilierungsbericht darunter
`$BUILD_ROOT/traefik-native-middleware/build.txt`, außerhalb der Kasse. Die
Quellstandard verwendet `PassthroughEngine`; Ein erfolgreicher lokaler Build allein reicht nicht aus
ein Regelbewertungs- oder Fähigkeitsüberprüfungsergebnis.

Die separate Pinned-Host-Sonde stellt das Modul unter einen Einwegartikel
`plugins-local`-Arbeitsbereich, materialisiert statische und Dateianbieterkonfiguration,
und leitet eine körpertragende Anfrage über Traefik weiter:

```sh
TRAEFIK_BIN=/absolute/local/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absolute/runtime-root \
MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
MSCONNECTOR_RULES_FILE=/absolute/no-crs-baseline.conf \
make -C connectors/traefik runtime-smoke-traefik-native
```

`config/traefik-native-middleware-static.yaml` und
`config/traefik-native-middleware-dynamic.yaml` bleiben Referenzformen; die
Runner verwendet die veränderbare Checkout-Konfiguration nicht wieder. Die Sonde baut und
startet einen privaten persistenten UDS Common/libmodsecurity-Dienst und prüft dann
Plugin-Laden und gezieltes P1--P4-sicheres Hostverhalten. Es fördert nicht a
Antwortkörper-, Phasen-, Late-Action-, First-Byte- oder No-Puffer-Fähigkeit.

Der Metadaten-Starter kompiliert:

- `common/src/origin.c`
- `common/src/capabilities.c`
- `connectors/traefik/metadata.c`
- `connectors/traefik/src/traefik_build_starter.c`

Der Decision-Service-Starter kompiliert zusätzlich:

- `common/src/intervention.c`
- `common/src/status.c`
- `connectors/traefik/src/traefik_decision_service.c`
- `connectors/traefik/src/traefik_decision_service_main.c`

Pfade einschließen:

- `common/include`
- `connectors/traefik`
- `connectors/traefik/src`

Standardartefaktpfade:

- `$BUILD_ROOT/traefik-build-starter/traefik_build_starter`
- `$BUILD_ROOT/traefik-build-starter/traefik_decision_service_starter`

Standardergebnispfade:

- `$BUILD_ROOT/traefik-build-starter/result.txt`
- `$BUILD_ROOT/traefik-build-starter/decision-service-result.txt`

Letzter lokaler Status: Metadaten-Build-Starter PASS; Entscheidungsservice-Starter-Build
PASS; Entscheidungsservice-Selbsttest PASS.

## Nicht implementiert/nicht überprüft

Von dieser Quelle wird kein Traefik SDK, keine CGO-Integration oder keine Traefik-Binärdatei erstellt
bauen. Das native Go-Modul verfügt über eine separate UDS-Prüfung für den angehefteten Host und bleibt bestehen
nicht gefördert. Die Prüfung in der Reaktionsphase wird von der Auswahl weiterhin nicht unterstützt
`forwardAuth`-Autorisierungsprotokoll; Die native UDS-Probe hat nur gezielt
P3/P4-sicherer Beweis. Keiner der Quellpfade beansprucht Produktion oder volle Laufzeit
Überprüfung.

## Produktions-Build-Blocker

Ein Anspruch auf Produktionsunterstützung bleibt solange gesperrt, bis diese umgesetzt sind bzw
bewiesen:

- CI-Build-/Link-Beweise mit angehefteten libmodsecurity-Eingaben beibehalten
- Beweise für das Laden der Konfiguration und den Start des Dienstes aufbewahrt
- Nachweise für die Genehmigungs-/Blockierungsanforderung von Traefik an den Dienst aufbewahrt
- umfassendere Nachweise für Herunterfahren, Parallelität, Zeitüberschreitung und Fehlerpfad
- Begrenzung des Anforderungstexts und übergroße Anforderungsnachweise
- Ereignis-JSONL-Beweis ohne Anforderungstext-Nutzdaten
- explizite Bereitstellung und Herkunfts-/Lizenzdokumentation
