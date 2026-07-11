**Sprache:** [English](common-sdk.md) | Deutsch

# Common SDK

## Inkrementeller Body-Lifecycle

Runtime und Engine-Fassade stellen für Host-Adapter mit Streaming-Hooks einen
expliziten Lifecycle mit geliehenen Buffern bereit:

```text
transaction_begin
Request-Header verarbeiten
Request-Body-Chunk* anhängen → Request-Body bei EOS finalisieren
Response-Header verarbeiten
Response-Body-Chunk* anhängen → Response-Body bei EOS finalisieren
transaction_finish → transaction_destroy
```

`msconnector_runtime_transaction_append_request_body_chunk()` und
`msconnector_runtime_transaction_append_response_body_chunk()` leihen den
Pointer mit Länge ausschließlich für die Dauer des Aufrufs. Weder Common noch
ein Event speichert einen Body-Pointer oder eine Payload. Erst
`finish_*_body()` bildet die einmalige Phasengrenze, an der das Backend
libmodsecuritys `process_*_body` aufrufen kann. Ohne weitergehenden
Backend-Nachweis ist dies als inkrementelles Ingest mit End-of-Stream-
Auswertung zu dokumentieren, nicht als Per-Chunk-Regelauswertung.

Der gepufferte Kompatibilitätshelfer `transaction_process_response()` bleibt
für Request-only-Adapter erhalten. Full-Lifecycle-Adapter verwenden die
expliziten Header-/Chunk-/EOS-Aufrufe und melden ihren Commit-Zustand mit
`msconnector_runtime_transaction_set_response_commit_state()`. Common löst
nur die neutrale Late-Intervention-Policy; erst ein echter Host-Adapter darf
log_only oder connection-abort als verifiziert ausweisen.

Der Fortschritt enthält ausschließlich `bytes_seen`, `bytes_inspected`,
`truncated`, `finished` und das kanonische, metadatenbasierte Limit-Ergebnis.
`bytes_seen` wird für jeden beobachteten Chunk aktualisiert, auch für einen
zurückgewiesenen Chunk über dem Limit; `bytes_inspected` steigt erst, nachdem
Common begrenzte Bytes an die Engine übergeben hat.
`body_limit_action=reject` übergibt aus dem beanstandeten Chunk keine Bytes;
`body_limit_action=process_partial` übergibt nur den verbleibenden Anteil und
markiert den Body als gekürzt. Das Eventmodell kann zusätzlich das optionale,
payloadfreie `body_limit_outcome` (`at_limit`, `over_limit`,
`process_partial` oder `reject`) sowie `content_type`, `body_bytes_seen` und
`body_bytes_inspected` ausgeben. Daraus folgt weder ein Streaming-Hook eines
bestimmten Connectors noch ein No-Full-Buffer- oder First-Byte-Runtime-Nachweis.

Der neutrale Konfigurationsvertrag führt `request_body_limit`,
`response_body_limit`, `body_limit_action` und
`late_intervention_timeout`. Das Timeout ist ein Adapter-Budget in
Millisekunden; `0` deaktiviert es. Common parst, validiert, merged und stellt
das Budget bereit, startet aber keinen Host-Timer und bricht keine I/O ab. Erst
ein Connector mit echtem Host-Deadline-/Cancel-Pfad darf die Einstellung als
durchgesetzt oder Timeout-Verhalten als verifiziert ausweisen.
Das flache Runtime-Konfigurationsformat akzeptiert `phase4_event_log` als
neutrale Bezeichnung für den vorhandenen Schlüssel `event_path`.

Envoy, Traefik und lighttpd besitzen lokale Common-SDK-Mapper-Gerüste für `msconnector_config`, `msconnector_request` und `msconnector_response`. Dies ist nur ein Structure-/Compile-Contract. Host-API-Glue, Runtime-Lifecycle, Build-Glue, Protokoll-/Frame-Handling, Event-Artefakt-Callsites und libmodsecurity-Transaktionsbesitz bleiben Connector-spezifische Arbeit. Diese Connectoren bleiben `not_verified` / `connector-gap`, bis echte Runtime-Evidence vorhanden ist.

## Generischer Mapper-Helfer

Das Common-SDK enthält `msconnector_generic_map_request()` und `msconnector_generic_map_response()` für Starter-Connectoren, die ihre lokalen Daten bereits als connector-neutrale Request- und Response-Felder ausdrücken können. Envoy, Traefik und lighttpd nutzen diesen Helfer über dünne lokale Header-Aliase.

Der Helfer übernimmt keine Header- oder Body-Bytes, protokolliert keine Body-Payloads und ändert den Status `not_verified` / `connector-gap` dieser Connectoren nicht. Die verbleibenden Starter-Connectoren vermeiden connector-lokale Mapper-Quellkopien, indem ihre Einstiegspunkte auf den connector-neutralen generischen Mapper zeigen; Validierung und Body-Metadaten-Zuweisung liegen dadurch an einer Common-Stelle.

Aufrufer des generischen Mappers müssen `hostname` als NUL-terminierte Zeichenkette übergeben, wenn das Feld gesetzt ist. Header-Value-Slices werden niemals als C-String-Hostnamen exponiert. Body-Größen größer als null erfordern einen nicht-NULL Body-Zeiger und bleiben metadatenbezogen, sofern der Aufrufer sichere Body-Bytes besitzt.
