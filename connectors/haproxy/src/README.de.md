# HAProxy-Quellcode

**Sprache:** [English](README.md) | Deutsch

`haproxy_spoa_agent_starter.h` / `.c` behalten die lokale Starter-Entscheidungs-API;
`haproxy_spoa_main.c` bietet `--describe` an.
`haproxy_spop_diagnostic_runtime.c` implementiert den SPOP-Dienst mit seinen
produktiven und Legacy-Serve-Befehlen. `haproxy_modsecurity_binding.h` / `.c`
besitzen die libmodsecurity-Transaktions-, Body-, Interventions- und
Fehlerbehandlung. `haproxy_modsecurity_mapper.h` / `.c` adaptieren die
Hostmetadaten. Produktive Legacy-Auswertungshelfer bleiben im Binding, weil der
Legacy-SPOP-Server sie aufruft.

Der Produktbuild `make -C connectors/haproxy build-modsecurity-binding` erzeugt
`libhaproxy-modsecurity-binding.a`. Er baut kein Testprogramm mehr und verlinkt
nicht mehr das Common-Testergebnismodell. Compile-/Link-Proben für die
SDK-Kompatibilität bleiben im Produktbuild; eine fehlende optionale Rule-ID-API
verwendet die unterstützte Baseline, ohne die erforderliche API-Prüfung
abzuschwächen.

Eingebettete Starter-, Binding- und SPOP-Regressionsdefinitionen gehören nun zum
gepinnten Framework unter `connector_native_tests/connectors/haproxy/src/`.
Der eigenständige Binding-Treiber liegt unter
`connector_suite/adapters/haproxy/src/haproxy_modsecurity_binding_self_test.c`.
Produktprogramme bieten `--self-test` und `--runtime-self-test` nicht mehr an.

Aus dem Connector-Wurzelverzeichnis wird mit explizitem `ON_DEMAND_TESTS=1` eines
der benannten Spezialtargets über `make -C connectors/haproxy` aufgerufen:
`self-test-spoa`, `self-test-spoa-runtime`, `self-test-modsecurity-binding` oder
`self-test-modsecurity-binding-crs`. Das CRS-Target verlangt zusätzlich ein
`MODSECURITY_RULE_PREAMBLE_FILE`, das eine vorhandene Präambel bezeichnet. Das
Framework verlangt den expliziten Checkout samt Revision und externe Ausgaben,
erhält alle Assertions und aktiviert diese Spezialbestände nicht standardmäßig.

Weitere Harnesses und Fixtures gehören zum Framework unter
`connector_suite/adapters/haproxy/`. Natives HTX und SPOE/SPOP mit einem
Response-Companion bleiben getrennte Laufzeitprofile. Quellcode, Kompilierung
und lokale Selbsttests allein belegen weder Host-Lifecycle noch Response-Body.
