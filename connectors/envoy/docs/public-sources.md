# Envoy Public Sources

Status: references collected
Runtime status: `minimal_runtime_smoke` for the targeted ext_authz request path

These public Envoy documentation links were collected as candidate architecture
research. They do not select an integration approach and do not prove that a
ModSecurity Envoy connector is implemented here.

- https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_filters.html
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_authz_filter.html
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter.html
- https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/wasm_filter.html
- https://www.envoyproxy.io/docs/envoy/latest/extending/extending
- https://github.com/envoyproxy/go-control-plane/tree/main/envoy/service/ext_proc/v3

The standard repository-backed runtime path remains the C HTTP `ext_authz`
service. The full-lifecycle profile separately selects the Go `ext_proc`
service against the pinned official generated API and a real Envoy listener.
That host run proves streamed transport/callback delivery only: it has no
Common/libmodsecurity bridge, rule evaluation, reset, timeout, or production
compatibility evidence.
