# Envoy Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Connector metadata: `minimal_runtime_smoke` / `connector-gap`

| Gate | Current evidence boundary |
|---|---|
| Host integration | Connector-owned HTTP `ext_authz` service profile |
| Common SDK | Real thin mapper callbacks plus Common runtime lifecycle |
| Config | key=value template, concrete path substitution, real config/rule load |
| Request headers | Mapped and bounded in real Envoy host-path smoke |
| Request body | Buffered/bounded path implemented; targeted body case not promoted here |
| Response headers | Unsupported by the selected HTTP authorization protocol |
| Response body | Unsupported; `response_body_verified=false` |
| Decision | Common decision mapped to ext_authz allow/deny; targeted 403 observed |
| Events | Metadata-only Common JSONL event observed; no body payload |
| Build | C17 compile/link verified with warnings as errors |
| Config check | Verified against local libmodsecurity and targeted rules |
| Start | Request-free service start/stop verified locally |
| Minimal runtime | Local Envoy 200/403 host-path smoke observed |
| CRS/full matrix | Not verified |
| Production/security | Not verified |

Runtime evidence remains scoped to the targeted local smoke until root CI,
Framework evidence layout, and repository reports consume the new connector
binary. It does not justify broader metadata promotion.
