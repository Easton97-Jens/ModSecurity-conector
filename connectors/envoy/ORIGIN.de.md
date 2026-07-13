# Ursprung des Envoy-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: repository-local ext_authz connector source plus a non-promoted Go/CGo
ext_proc Common/libmodsecurity path selected by the full-lifecycle profile
Runtime status: `minimal_runtime_smoke` for the HTTP ext_authz request path

In dieses Repository wurde keine Upstream-Quellbasis eines Envoy-Connectors
importiert.

## Quellen-Evidenz

| Feld | Wert |
| --- | --- |
| Komponente | ModSecurity-Envoy-ext_authz-Connector plus vom Full-Lifecycle ausgewählter ext_proc-Transportpfad |
| Upstream-Envoy-Quelle | not selected |
| Upstream-Connector-Quelle | not selected |
| Source-Branch | not selected |
| Source-Commit | not selected |
| Source-Beschreibung/Version | not selected |
| Lizenz für importierten Upstream-Code | not selected |
| Importierte Upstream-Dateien | none |
| Lokale Quellenart | repository-lokaler ext_authz-Service, Bridge-Self-Test und ext_proc-CGo/Common-Stream-Adapter |

Der C-Quellcode in `connectors/envoy/metadata.*` und `connectors/envoy/src/`
sowie der Go-Quellcode in `connectors/envoy/ext_proc/` sind repository-lokaler
Code. Sie wurden nicht aus Envoy, proxy-wasm, gRPC, protobuf oder einem
ModSecurity-Connector-Upstream kopiert. Der ext_proc-Build löst offizielle
generierte Envoy-Go-API-Abhängigkeiten über die gepinnten Modul-/Checksum-Dateien
auf; generierter Upstream-protobuf-Code wird nicht in dieses Repository
eingecheckt.

## Nicht erhobene Claims

- Es ist keine native Envoy-HTTP-Filterimplementierung importiert oder
  implementiert.
- Es ist kein Envoy-External-Processing-Service importiert. Ein
  repository-lokaler Go/CGo-ext_proc-Service verknüpft Common Runtime und
  libmodsecurity und besitzt einen begrenzten realen Envoy-HTTP/1.1-
  Regel-/Aktions-Smoke; diese Evidenz ist nicht hochgestuft und keine
  kanonische Sammel- oder Produktionsverifikation.
- Es ist kein proxy-wasm-Modul importiert oder implementiert.
- Der Connector delegiert den libmodsecurity-Lifecycle an die
  connector-neutrale `common/runtime`-API, statt host-spezifischen Runtime-Code
  einzubetten.
- Keine Response-Phase, CRS-, Security-, Full-Matrix- oder
  Produktionskompatibilität ist durch den minimalen Request-Path-Smoke
  verifiziert.

## Lokaler Bridge-Starter

Der lokale Bridge-Starter modelliert einen HTTP-Request mit
connector-neutralen `msconnector_request`-Daten, wertet ein deterministisches
Self-Test-Block-/Allow-Signal aus und gibt eine `msconnector_intervention`
zurück. Dies ist ein lokaler CLI-Self-Test für den künftigen
Sidecar-/HTTP-Bridge-Pfad, keine Envoy-Runtime-Evidenz und keine
ModSecurity-Regelauswertung.

## Lokaler ext_authz-Service

`envoy_ext_authz_service_main.c` definiert ein repository-lokales
Envoy-Host-Profil für den connector-neutralen HTTP-Autorisierungsservice. Es
werden weder Envoy-SDK-Quellcode noch -Typen importiert: Envoy kommuniziert mit
dem Service über sein externes HTTP-`ext_authz`-Protokoll. Compile-, Start- und
reale Envoy-Request-Evidenz bleiben separate Promotion-Gates.

## Lokaler ext_proc-Common-Runtime-Pfad

`ext_proc/` verwendet die offizielle generierte Envoy-Go-
External-Processing-API über das gepinnte Modul
`github.com/envoyproxy/go-control-plane/envoy`. Es hält protobuf-Typen lokal
zum Connector und besitzt pro Stream begrenzten Zustand, inkrementelle
Body-Callbacks, EOS-/Cancellation-Cleanup und eine `STREAMED`-Envoy-Vorlage.
Die normale CGo-Executable öffnet für jeden Stream eine echte
Common-/libmodsecurity-Transaktion. `runtime-smoke-envoy-ext-proc` validiert
separat generiertes YAML mit echtem Envoy und zeichnet run-lokales rohes
Common-Decision-JSONL sowie payload-freie Completion-Metadaten auf. Es besitzt
begrenzte HTTP/1.1-P1/P2/P3/P4-Regel-/Aktions-Evidenz, stuft jedoch keine
Fähigkeit hoch.
