# Ausrichtung der Envoy-Vorlage

**Sprache:** [English](envoy-template-alignment.md) | Deutsch

Status: Brückenstarter
Laufzeitstatus: nicht überprüft

Envoy verfügt jetzt über Repository-lokale origin/source-map-Metadaten und eine lokale
sidecar/HTTP Brückenstarter. Es gibt immer noch keinen laufzeitverifizierten Envoy-Adapter
Implementierung, keine lokalen Tests und keine Envoy-Laufzeitansprüche.

Global/shared Regeln werden referenziert statt dupliziert:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Integrationspfad

Der ausgewählte minimale Pfad ist `bridge-starter`: Kompilieren Sie einen lokalen sidecar/HTTP
Bridge-Entscheidungsmodell gegen steckerneutralen `common/`-Code. Produktiv
Die native/ext_proc/proxy-wasm-Integration bleibt aufgrund dieses Repositorys zurückgestellt
enthält keine Envoy SDK/API-Header, ext_proc protobuf/gRPC-Bindungen,
Proxy-wasm SDK/toolchain oder ein Envoy-Laufzeit-Harness.

## Was der Starter kann

- Repository-lokale Envoy-Metadaten und Bridge-Quelle kompilieren;
- Modellanforderungsheader und URI/query-Eingabe mit `msconnector_request`;
- Rückgabe von allow/block-Entscheidungen mit `msconnector_status` und
  `msconnector_intervention`;
- Führen Sie einen lokalen CLI-Selbsttest durch, der Zulassungs- und 403-Blockierungsentscheidungen abdeckt.

## Was der Starter nicht behaupten kann

- kein echter Envoy API verwenden;
- keine libmodsecurity API Verwendung;
- nein CRS laden;
- kein No-CRS- oder With-CRS-Laufzeitlauf;
- keine RESPONSE_BODY Verifizierung;
- Keine Framework-eigene YAML-Ausführung für Envoy.

## Phasenmatrix

| Phase | Status |
| --- | --- |
| Phase 0 Scaffold | OK |
| Phase 1 Origin/Metadata | bridge-starter |
| Phase 2 Build | bridge-starter PASS |
| Phase 3 Bridge Self-Test | PASS |
| Phase 4 ModSecurity Bridge | blocked; libmodsecurity headers/libs not found |
| Phase 5 Envoy Harness | blocked entrypoint only |
| Phase 6 No-CRS | not-run |
| Phase 7 With-CRS | not-run |
| Phase 8 CRS Evidence | not-verified |
| Phase 9 RESPONSE_BODY | not-verified |
| Phase 10 Negative/pass-through | local self-test only |
| Phase 11 Audit/log | not-verified |
| Phase 12 Promotion | not allowed beyond bridge-starter |

## Build-Starter-Nachweis

- Befehl: `make -C connectors/envoy build-starter`
- Ergebnis: PASS für die lokale Bridge-Starter-Kompilierung
- Befehl: `make -C connectors/envoy self-test`
- Ergebnis: PASS für den lokalen Bridge-Entscheidungs-Selbsttest
- Ausgabepfad: `/src/ModSecurity-conector-build/envoy-bridge-starter`
- Laufzeitstatus bleibt bestehen `not-verified`

## Framework-Starter-Nachweis

`make connector-starter-checks` zeichnet auch Envoy-Starterergebnisse auf
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` und
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Diese Aufzeichnungen dienen ausschließlich der Nachweissicherung und werden aufbewahrt
`runtime_verified: false`, `runtime_status: not-verified` und
`response_body_verified: false`.

## Runtime-Smoke-Eintrittspunkt

`make smoke-envoy` ruft jetzt den Framework-eigenen Envoy Runtime-Smoke Runner auf,
der an `connectors/envoy/harness/run_envoy_smoke.sh` sendet. Aktuell
Der Status lautet BLOCKED, da dieser Connector-seitige Einstiegspunkt nur Diagnosedaten schreibt
Nachweise und es gibt keinen echten Envoy server/config/runtime-Harness. Laufzeit bleibt bestehen
nicht verifiziert und RESPONSE_BODY bleibt nicht verifiziert.
