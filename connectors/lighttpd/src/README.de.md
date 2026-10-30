# lighttpd-Quellcode

**Sprache:** [English](README.md) | Deutsch

Plugin-Lebenszyklus und Common-Runtime-Aufrufe liegen in
`../module/mod_msconnector.c`. `lighttpd_modsecurity_mapper.h` / `.c` übertragen
Request-/Response-Metadaten des Hosts in Common-SDK-Typen. Der Mapper-Stub ohne
Host-API erlaubt Compile-Prüfungen ohne bereitgestellte lighttpd-Header;
`../build/build_module.sh` wählt mit `MSCONNECTOR_LIGHTTPD_HOST_API`, gepinnten
Host-Headern und generierter `config.h` die echte Hostimplementierung aus.

`lighttpd_build_starter.c` bleibt eine Metadatenprobe. `lighttpd_bridge.h` / `.c`
und `lighttpd_bridge_main.c` behalten den historischen Decision-Service-Starter.
Das Bridge-Programm bietet `--status`; sein Befehl `--self-test` und die
enthaltenen Assertions wurden aus dem Produkt entfernt.

Dieselben Assertions liegen nun im gepinnten Framework unter
`connector_native_tests/connectors/lighttpd/src/lighttpd_bridge.inc`.
Aus dem Connector-Wurzelverzeichnis erfolgt der Aufruf mit
`make -C connectors/lighttpd self-test-lighttpd-bridge ON_DEMAND_TESTS=1`.
Connector-spezifische Fixtures, native Smoke-Harnesses und Python-Tests gehören
zum Framework unter `connector_suite/adapters/lighttpd/`.

Der Framework-Runner verlangt einen expliziten Connector-Checkout samt Revision
und ein externes Ausgabeverzeichnis. Diese Spezialtests erweitern die
Standardauswahl nicht. Kompilierung und lokale Starterprüfungen beweisen kein
Hostverhalten; Stock-Sidecar und gepatchtes natives Plugin bleiben getrennte
Laufzeitprofile.
