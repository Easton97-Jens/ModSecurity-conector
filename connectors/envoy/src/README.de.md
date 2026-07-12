# Envoy-Quelle

**Sprache:** [English](README.md) | Deutsch

Status: ext_authz-Connector-Quelle; `minimal_runtime_smoke` / `connector-gap`
Laufzeitstatus: Nur gezielter Anforderungsheader 200/403-Pfad

Dieses Verzeichnis enthält die Repository-lokale Quelle für den Envoy HTTP `ext_authz`
Service und der ältere Bridge-Selbsttest:

- `envoy_ext_authz_service_main.c`: Hostprofil im Besitz des Connectors und gemeinsam genutzt
  Einstiegspunkt für den HTTP-Autorisierungsdienst.
- `envoy_modsecurity_mapper.h` / `.c`: Thin C17-Anfrage, Antwort und Konfiguration
  Mapper-Funktionen über den Common-Generic-Mapper.
- `envoy_bridge.h`: Bridge-Entscheidungs-API über konnektorneutrale Anforderungsdaten.
- `envoy_bridge.c`: deterministisches Zulassungs-/Blockierungsentscheidungsmodell für lokal
  Selbsttests.
- `envoy_bridge_main.c`: CLI-Einstiegspunkt für `--self-test`.

Der Dienst wählt das externe HTTP-Autorisierungsmodell von Envoy ohne Import aus
Envoy SDK-Typen. Es delegiert Konfiguration, libmodsecurity-Lebenszyklus, begrenzt
HTTP-Analyse, Transaktionsverarbeitung, Entscheidungen und Ereignisausgabe an
`common/runtime/`. Der Response Mapper ist zur Vertragsvollständigkeit verlinkt, aber
`ext_authz` bleibt nur in der Anforderungsphase.

Der ältere Bridge-Starter ruft keine Envoy- oder libmodsecurity-APIs auf und bleibt bestehen
Nur Selbsttest. Weder das Vorhandensein der Quelle noch ihr Selbsttest sind ein Laufzeitbeweis.
