# Glossary

**Language:** English | [Deutsch](glossary.de.md)

This glossary defines repository terms. It does not replace the short local
explanation required where a term first appears in a command, configuration,
or evidence guide.

| Term | Meaning in this repository |
|---|---|
| ABI | Application Binary Interface: the binary-level contract between compiled components. A matching API alone does not guarantee ABI compatibility. |
| ALPN | Application-Layer Protocol Negotiation, the TLS mechanism used to negotiate an application protocol such as HTTP/2. Its presence is not HTTP/2 evidence by itself. |
| API | Application Programming Interface: source-level functions, types, and contracts exposed to callers. |
| APXS | Apache Extension Tool, used by Apache module builds to obtain compiler/linker settings and install modules. |
| Capability | A declared host/profile property in <code>capabilities.json</code>. It can be implemented, unasserted, unsupported, or not implemented; it is not automatically a PASS result. |
| Canonical evidence | A validated, run-scoped artifact set at the configured evidence root. It must retain the run ID, selected profile, and required result/event information. |
| CRS | OWASP Core Rule Set. The repository-owned No-CRS rules are separate from CRS; preparing or selecting CRS input does not prove CRS behavior. |
| Entity Body | HTTP message body after transfer framing has been decoded. For the selected patched lighttpd route, the Entity-Body hook is the relevant response-body representation. |
| EOS | End of stream. A phase can finalize at EOS even when data arrived incrementally before it. |
| Evidence | Artifacts that support one stated observation: results, events, effective configuration, logs, or transport observations. Evidence is scoped to its run and does not extrapolate beyond it. |
| ext_authz | Envoy external authorization integration. It normally decides before the upstream response and therefore has different response visibility from <code>ext_proc</code>. |
| ext_proc | Envoy external processing integration. The selected full-lifecycle Envoy route uses this streamed bridge; its strict post-commit reset remains a separate proof question. |
| First Byte Before EOS | A synchronized observation that the client received a response byte before the upstream response reached EOS. It requires explicit timing/transport artifacts, not just a completed response. |
| Full Lifecycle | The selected host route that binds build, config load, startup, runtime traffic, capability-selected No-CRS cases, and required artifacts to one identity. It is not a production or all-protocol claim. |
| HTX | HAProxy’s internal HTTP transaction representation. The selected HAProxy route uses a native HTX filter and reaches response-body completion at HTX EOS. |
| Integration mode | A recorded host/bridge model such as <code>native-httpd-module</code>, <code>native-nginx-http-module</code>, <code>native-htx-filter</code>, <code>ext_proc</code>, <code>native-traefik-middleware</code>, or <code>patched-native-lighttpd</code>. |
| JSONL | JSON Lines: one JSON object per line. Runtime events and results use this format so records can be streamed and validated independently. |
| Late Intervention | A requested WAF action after the response is already committed. The actual action can be a safe log-only outcome, an abort where the host proves it, or another recorded limitation. |
| No Full Response Buffering | The connector must not retain a connector-owned complete response body merely to evaluate a response-body rule. This property requires its own source/runtime evidence. |
| No-CRS | The repository-owned baseline without a CRS include. Its IDs are in the <code>1100000</code> range and are not OWASP CRS IDs. |
| P1 / P2 / P3 / P4 | ModSecurity processing phases used here: request headers; request body; response headers; response body. A host model can support different subsets. |
| Promotion | The evidence-gated act of allowing a run result to support a stated capability or completion assertion. Source wiring, configuration, or a compatibility smoke cannot promote themselves. |
| QUIC | UDP-based transport used by HTTP/3. A configured binary or protocol label is not QUIC/HTTP/3 validation. |
| Safe | The late-intervention policy that records an action without claiming a client-visible post-commit status rewrite or connection abort. |
| SPOA / SPOE / SPOP | HAProxy Stream Processing Offload Agent, Engine, and Protocol. They describe the HAProxy agent integration vocabulary; they are not interchangeable with the selected native HTX filter mode. |
| Strict | A distinct late-intervention policy/path that may require a host-visible abort after commit. It is only meaningful when the selected host and evidence prove it. |
| TTFB | Time to first byte. In this repository, first-byte claims need the stronger synchronized “First Byte Before EOS” evidence where that case applies. |
| UDS | Unix domain socket, a local inter-process communication endpoint. The selected Traefik native middleware uses a local UDS service; a UDS path must be private and writable by the intended processes. |
| Upstream | The server or fixture that supplies the response to the host proxy/module. It is distinct from the downstream client. |
| Wire Body | Bytes as represented on the wire, potentially including transfer coding or content encoding. It differs from an Entity Body. |

## Related reference points

- [Variables and placeholders](../configuration/variables.md)
- [Build documentation](../build/README.md)
- [Testing documentation](../testing/README.md)
- [Evidence documentation](../evidence/README.md)

The terms above describe the current HTTP/1.1 core documentation boundary. They
do not make production, CRS, HTTP/2, HTTP/3, extended-matrix, or
strict-for-all-connectors claims.
