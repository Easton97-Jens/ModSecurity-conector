# Envoy Öffentliche Quellen

**Sprache:** [English](public-sources.md) | Deutsch

Status: Referenzen gesammelt
Laufzeitstatus: `minimal_runtime_smoke` für den angestrebten ext_authz-Anforderungspfad

Diese öffentlichen Envoy-Dokumentationslinks wurden als Kandidatenarchitektur gesammelt
Forschung. Sie wählen keinen Integrationsansatz und beweisen nicht, dass a
Der ModSecurity Envoy-Connector ist hier implementiert.

- https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_filters.html
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter.html
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter.html
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/wasm_filter.html
- https://www.envoyproxy.io/docs/envoy/latest/extending/extending
- https://github.com/envoyproxy/go-control-plane/tree/main/envoy/service/ext_proc/v3

Der standardmäßige, vom Repository unterstützte Laufzeitpfad bleibt C HTTP `ext_authz`
Dienst. Das Full-Lifecycle-Profil leitet `ext_proc` separat weiter
`full-lifecycle-envoy-ext-proc` gegen die angeheftete offiziell generierte API und a
echter Envoy-Zuhörer. Sein CGo-Dienst verbindet Common Runtime und libmodsecurity.
und der Hostlauf zeichnet rohe Common P1/P2/P3/P4-Regel-/Aktionsnachweise auf. Es bleibt
nicht hochgestuft und stellt kein Reset, Timeout, HTTP/2, Canonical-Collector,
oder Nachweis der Produktionskompatibilität.
