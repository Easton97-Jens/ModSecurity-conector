# lighttpd-Connector

Status: `minimal_runtime_smoke` für den nativen Phase-1-Headerpfad

Der primäre Integrationspfad ist jetzt ein Repository-eigenes natives
lighttpd-Modul. Es bindet die connector-neutrale Runtime aus `common/runtime`
ein, überführt echte lighttpd-Request- und Response-Header in Common-SDK-Modelle
und setzt disruptive Phase-1-Entscheidungen mit `http_status_set_err()` um.

Gegen das gepinnte lighttpd 1.4.84 und libmodsecurity lokal belegt sind:

- C17-Compile und Link von `mod_msconnector.so` mit Warnungen als Fehler;
- echtes Laden des Moduls und erfolgreiche lighttpd-Konfigurationsprüfung;
- echter Vordergrundstart, PID-Prüfung und sauberes Stoppen ohne Request;
- separater Host-Runtime-Smoke: `OPTIONS *` liefert 200, während
  `X-Modsec-Smoke: block` durch Regel `1000001` mit 403 blockiert wird;
- JSONL-Metadaten mit Connector und Regel-ID, ohne Body-Payload.

Dies ist bewusst ein enger, partieller Runtime-Pfad. Request- und
Response-Bodies sind in diesem nativen Modul nicht implementiert und werden
niemals an die Runtime übergeben. Es gibt keine Behauptung zu CRS, Produktionsreife,
Security-Verifikation, Response-Body-Verarbeitung oder Full Matrix.

## Implementierter Pfad

`module/mod_msconnector.c` implementiert Plugin-Initialisierung, Cleanup,
Config-Registrierung, Request-Header-Hook, Response-Start-Hook,
Transaction-Lifecycle, Block-/Fehlerstatus und Cleanup beim Request-Reset.

`src/lighttpd_modsecurity_mapper.c` kapselt sämtliche lighttpd-Typen. Die
gemappten Header bleiben bis zum Request-Reset gültig, da die Common Runtime
Request und Response während der Transaktion nur ausleiht.

## Konfiguration

```lighttpd
server.modules += ( "mod_msconnector" )
msconnector.enabled = "enable"
msconnector.config-file = "/absoluter/pfad/msconnector-runtime.conf"
```

Die referenzierte Common-Runtime-Datei verwendet `key=value`. Sie bildet unter
anderem Regelquellen, Transaction-ID, Body-Modi und Limits, Block-/Fehlerstatus,
Event-Pfad und Header-Limits ab. Für den aktuellen nativen Phase-1-Pfad müssen
beide Body-Modi `none` sein.

`config/lighttpd-native.conf` ist ein Beispiel; seine beiden absoluten
Platzhalterpfade müssen ersetzt werden. Der native Harness erzeugt selbst eine
ausführbare Konfiguration mit verwalteten absoluten Pfaden.

## Build und Nachweise

```sh
make -C connectors/lighttpd build-lighttpd-bridge
make -C connectors/lighttpd self-test-lighttpd-bridge
make -C connectors/lighttpd build-lighttpd-connector
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

Der native Build benötigt absolute Pfade in `LIGHTTPD_SOURCE_DIR`,
`MODSECURITY_INCLUDE_DIR` und `MODSECURITY_LIB_DIR`. Das erzeugte lighttpd
`config.h` wird über `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_BUILD_DIR` oder
`LIGHTTPD_CONFIG_DIR` gefunden. Für die Host-Nachweise ist zusätzlich
`LIGHTTPD_BIN` erforderlich.

`start-smoke-lighttpd` sendet ausdrücklich keine Requests. Nur der separate
`runtime-smoke-lighttpd` führt den 200/403-Requestpfad aus. Der ältere
Bridge-Starter und der Framework-Sidecarpfad bleiben getrennte Alternativen;
deren Self-Tests sind kein Nachweis für den nativen Hostpfad.

## Claim-Grenzen

Belegt ist ausschließlich `minimal_runtime_smoke` beziehungsweise ein
`partial_runtime_path` für Header und Phase-1-Deny. Nicht belegt sind Bodies,
Late Intervention, CRS, Produktionshärtung, Security-Verifikation und die
vollständige Testmatrix.

## Kanonische Grenze für Phase 4

Das aktuelle native Modul besitzt einen Response-Start-Header-Hook, aber keinen
nativen Response-Body-Hook. Es übergibt ModSecurity bewusst keine
Response-Body-Daten. `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` sind deshalb in diesem Modul
`not_implemented`.

Dies ist eine Implementierungsgrenze und keine Aussage, dass lighttpd
Response-Body-Verarbeitung grundsätzlich nie unterstützen kann. Phase-4-Fälle
bleiben `NOT_EXECUTED` (oder werden durch die Capability-Auswahl nicht gewählt),
bis ein nativer Response-Body-Pfad implementiert ist. Ohne Architekturbeleg
dürfen sie nicht `UNSUPPORTED` heißen. Folglich gibt es noch keinen
Phase-4-Nachweis für getrennte ursprüngliche, angeforderte und sichtbare
Statuswerte, späte Aktionen oder Verbindungsabbruch.

Der vorhandene Phase-1-Header-Deny ist ein getrenntes Nachweisergebnis.
Ereignisse und Berichte bleiben metadatenbasiert und enthalten niemals
Response-Body-Payloads.
