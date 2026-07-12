# Persistenter lokaler Engine-Service

`traefik-engine-service` ist die persistente lokale Common/libmodsecurity-
Engine für den ausgewählten nativen Traefik-Hostpfad. Sie ist ein
Unix-Domain-Socket-Prozess mit genau einer gemeinsamen Runtime. Das ist nötig,
weil Traefik die lokale Go-Middleware über Yaegi lädt und die C++-
libmodsecurity dort nicht direkt linken kann.

`native_middleware/` wählt die Engine nur mit `engineMode: uds` und einem
privaten absoluten `engineSocketPath`. Der native Hostprobe erzeugt beides
unter seinem connector-spezifischen Runtime-Root. Die eingecheckte
Referenzkonfiguration bleibt absichtlich bei `passthrough`, damit sie keinen
veralteten oder gemeinsam genutzten Socket-Pfad enthält. Ein Source-Build oder
ein lokaler Protokolltest ist kein Traefik-Hostnachweis und promotet keine
Capabilities, CRS-Unterstützung, Safe/Strict oder Produktionsreife.

## Build und lokaler Protokolltest

```sh
MODSECURITY_INCLUDE_DIR=/absolut/include \
MODSECURITY_LIB_DIR=/absolut/lib \
make -C connectors/traefik build-engine-service

MODSECURITY_INCLUDE_DIR=/absolut/include \
MODSECURITY_LIB_DIR=/absolut/lib \
make -C connectors/traefik test-engine-service
```

`test-engine-service` baut den C17-Service, führt Parser-/Negativtests aus,
startet eine echte lokale Common/libmodsecurity-Serviceinstanz und treibt eine
sichere Transaktion sowie die lokale gezielte Request-Header-Deny-Regel über
Unix-Sockets. Er verwirft außerdem einen zu großen Chunk und ein unzulässiges
Outcome. Das ist nur ein Service-/Protokoll-Test: Traefik startet nicht und
keine Hostaktion wird dadurch belegt.

Die Beispielkonfiguration ist `config/traefik-engine-service.conf`. Ihr
relativer `rules_file`-Pfad erwartet das Repository-Root als Arbeitsverzeichnis;
produktive Aufrufe müssen einen vertrauenswürdigen absoluten Regelpfad und ein
privates Runtime-Verzeichnis verwenden. Der Daemon verweigert einen vorhandenen
Socket-Pfad, bindet neue Sockets mit `0600` und löscht keinen beliebigen
bestehenden Pfad.

## Echte native Hostprobe

Der separate Hostprobe baut die Engine in seinem isolierten Runtime-Root,
startet sie einmal und wählt sie im echten gepinnten Traefik-Local-Plugin-Pfad:

```sh
MODSECURITY_INCLUDE_DIR=/absolut/include \
MODSECURITY_LIB_DIR=/absolut/lib \
TRAEFIK_BIN=/absolut/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absolut/leerer-runtime-root \
MSCONNECTOR_RULES_FILE=/absolut/no-crs-baseline.conf \
make -C connectors/traefik runtime-smoke-traefik-native
```

Ist `MSCONNECTOR_RULES_FILE` gesetzt, lädt der Probe genau diese kanonische
No-CRS-Regeldatei und erwartet die IDs `1100001`, `1100101`, `1100201` und
`1100301`. Ohne die Variable ist ausschließlich für einen selbständigen
lokalen Probe die eigene gezielte Regeldatei mit getrennten IDs erlaubt. Der
Probe verlangt P1-Allow `200`, P1-Deny `403`, P2-Deny `403`, P3-Deny vor dem
Commit `403` und P4-Safe/Log-only mit sichtbarem `200`. P4-Strict ist explizit
`NOT EXECUTED`.

## Lebenszyklus und Begrenzungen

`src/traefik_engine_protocol.h` ist die normative Wire-Spezifikation. Jeder
Frame hat 12 Byte: `MSE1`, Version `1`, Opcode, zwei Null-Reservierungsbytes
und eine Big-Endian-Payloadlänge. Die Payload ist auf 65.536 Byte und jeder
rohe Request-/Response-Chunk auf 32.768 Byte begrenzt. Es gelten zusätzlich
Grenzen für URI, IDs, Adressen und höchstens 128 Header. NUL-Bytes in Metadaten,
Restbytes, ungültige Flags, falsche Reihenfolgen und doppelte EOS werden
abgelehnt. Payloads werden weder geloggt noch in `RESULT` zurückgespiegelt.

Eine Socket-Verbindung trägt genau eine Transaktion; der Daemon und seine
Engine bleiben über Verbindungen hinweg bestehen. Die Go-Middleware öffnet
einmal pro `ServeHTTP` eine UDS-Verbindung und verwendet sie für den gesamten
P1--P4-Lebenszyklus. Common-Aufrufe werden durch ein Mutex serialisiert, die
Transaktionszustände bleiben verbindungslokal.

Der Client ruft explizit auf:

1. `BEGIN` für Request-Metadaten/Header,
2. `REQUEST_CHUNK` und genau ein `REQUEST_EOS`,
3. `RESPONSE_HEADERS`, optionale `RESPONSE_CHUNK`, genau ein `RESPONSE_EOS`
   sowie `RESPONSE_COMMIT` für die tatsächlichen Host-Commit-Metadaten,
4. `FINISH` und nach erfolgreichem Abschluss `DESTROY`.

EOF, Protokollfehler oder Socket-Timeout zerstören eine offene Transaktion,
erzeugen aber keinen hostbestätigten Outcome. `RESULT` enthält nur begrenzte
Entscheidungsmetadaten sowie ggf. Transaction-ID, Rule-ID und Redirect-URL,
nie Bodies, Header, URI-Werte oder Regelmeldungen.

## Outcome-Grenze

`OUTCOME` wird erst gesendet, nachdem der Go-`ResponseWriter` die konkrete
Hostaktion geschrieben hat. Ein fehlgeschlagener oder kurzer Body-Write führt
nur zu Commit-Metadaten, aber nie zu einem hostbestätigten Event. Vor einem
Response-Commit akzeptiert der Service nur die passende disruptive Aktion mit
`HOST_ACTION_APPLIED` und passendem sichtbaren Status. Common behält das rohe
Engine-Entscheidungsereignis und schreibt danach ein zweites,
hostbestätigtes Ereignis mit `transport_result=http_status`.

Nach Header-/Body-Commit kann eine disruptive Response-Body-Entscheidung nur
als `LOG_ONLY` ohne Action-Flag und mit dem tatsächlich bereits sichtbaren
Status bestätigt werden. Das zweite Ereignis verwendet dann
`transport_result=log_only`. Der Service kann keine Traefik-Response
zurücksetzen und weder einen späten Abort noch eine Strict-Intervention
behaupten.

Der Hostprobe setzt `event_path` unter seinem eigenen Runtime-Root und die
Common-Integration exakt auf `native-traefik-middleware`. Er übernimmt nur
metadatenhaltiges JSONL und filtert hostbestätigte Events über die kanonischen
`transport_result`-Werte. Weder Request- noch Response-Payloads werden als
Evidenz übernommen. Cancellation-/Disconnect-Fälle und jede
Capability-Promotion bleiben getrennte Arbeit.
