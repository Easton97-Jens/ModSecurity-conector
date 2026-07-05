**Sprache:** [English](common-sdk.md) | Deutsch

# Common SDK

Envoy, Traefik und lighttpd besitzen lokale Common-SDK-Mapper-Gerüste für `msconnector_config`, `msconnector_request` und `msconnector_response`. Dies ist nur ein Structure-/Compile-Contract. Host-API-Glue, Runtime-Lifecycle, Build-Glue, Protokoll-/Frame-Handling, Event-Artefakt-Callsites und libmodsecurity-Transaktionsbesitz bleiben Connector-spezifische Arbeit. Diese Connectoren bleiben `not_verified` / `connector-gap`, bis echte Runtime-Evidence vorhanden ist.

## Generischer Mapper-Helfer

Das Common-SDK enthält `msconnector_generic_map_request()` und `msconnector_generic_map_response()` für Starter-Connectoren, die ihre lokalen Daten bereits als connector-neutrale Request- und Response-Felder ausdrücken können. Envoy, Traefik und lighttpd nutzen diesen Helfer über dünne lokale Header-Aliase.

Der Helfer übernimmt keine Header- oder Body-Bytes, protokolliert keine Body-Payloads und ändert den Status `not_verified` / `connector-gap` dieser Connectoren nicht. Die verbleibenden Starter-Connectoren vermeiden connector-lokale Mapper-Quellkopien, indem ihre Einstiegspunkte auf den connector-neutralen generischen Mapper zeigen; Validierung und Body-Metadaten-Zuweisung liegen dadurch an einer Common-Stelle.

Aufrufer des generischen Mappers müssen `hostname` als NUL-terminierte Zeichenkette übergeben, wenn das Feld gesetzt ist. Header-Value-Slices werden niemals als C-String-Hostnamen exponiert. Body-Größen größer als null erfordern einen nicht-NULL Body-Zeiger und bleiben metadatenbezogen, sofern der Aufrufer sichere Body-Bytes besitzt.
