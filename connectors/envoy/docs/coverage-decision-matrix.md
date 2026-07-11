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

## Canonical Phase-4 decision

The selected Envoy HTTP `ext_authz` model runs before the upstream response.
The response-body and late-intervention facets are therefore architecture
boundaries, not pending runtime work.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered`, `phase4`, and `phase4_rule_evaluation` | `unsupported_by_host_model` | `UNSUPPORTED`: ext_authz receives no upstream response body |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | no response-phase commitment point is exposed |
| `late_intervention`, `late_intervention_log_only`, and `late_intervention_abort` | `unsupported_by_host_model` | no later upstream response reaches the authorization service |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | no original/visible upstream-response status or late action exists in this host path |

Request-side 200/403 evidence is deliberately excluded from these rows.
`UNSUPPORTED` never counts as `PASS`, and events contain metadata only.
