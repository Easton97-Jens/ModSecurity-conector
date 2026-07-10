# Envoy-Coverage-Entscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Connector-Metadaten: `minimal_runtime_smoke` / `connector-gap`

| Gate | Aktuelle Evidence-Grenze |
|---|---|
| Hostintegration | Connector-eigenes HTTP-`ext_authz`-Serviceprofil |
| Common SDK | Echte dünne Mapper-Callbacks plus Common-Runtime-Lifecycle |
| Config | key=value-Vorlage, konkrete Pfadersetzung, echter Config-/Rule-Load |
| Request-Header | Im echten Envoy-Hostpfad-Smoke begrenzt und gemappt |
| Request-Body | Gepufferter/begrenzter Pfad implementiert; kein promoteter Body-Case |
| Response-Header | Vom gewählten HTTP-Autorisierungsprotokoll nicht unterstützt |
| Response-Body | Nicht unterstützt; `response_body_verified=false` |
| Decision | Common-Decision auf ext_authz Allow/Deny gemappt; gezielter 403 beobachtet |
| Events | Metadata-only Common-JSONL beobachtet; keine Body-Payload |
| Build | C17-Compile/Link mit Warnings-as-Errors verifiziert |
| Config-Check | Mit lokaler libmodsecurity und gezielter Regel verifiziert |
| Start | Request-freier Service-Start/-Stop lokal verifiziert |
| Minimale Runtime | Lokaler Envoy-200/403-Hostpfad-Smoke beobachtet |
| CRS/Full Matrix | Nicht verifiziert |
| Produktion/Sicherheit | Nicht verifiziert |

Runtime-Evidence bleibt auf den gezielten lokalen Smoke begrenzt, bis Root-CI,
Framework-Evidence-Layout und Repository-Reports das neue Connector-Binary
verwenden. Daraus folgt keine breitere Metadata-Promotion.
