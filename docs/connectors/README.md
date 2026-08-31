# Connector documentation

**Language:** English | [Deutsch](README.de.md)

This section navigates six host integrations and ten logical connector
profiles. The host-family rows below are navigation only: the shared contract
assesses each logical profile separately, and a result for one profile is not
evidence for another profile in the same host family. “P1”, “P2”, “P3”, and
“P4” mean the ModSecurity request-header, request-body, response-header, and
response-body phases. A route’s actual case status is run-specific and comes
from its evidence; source presence, a capability manifest, or a build does not
itself make a PASS claim.

The selected HTTP/1.1 core documentation does not claim production readiness,
CRS verification, complete HTTP/2 or HTTP/3 verification, a complete matrix,
or strict behavior for all connectors.

## Host-family navigation

| Host integration | Current host-family core runner | Logical-profile boundary | Connector entry point | P1–P4 scope and boundary |
|---|---|---|---|---|
| Apache | <code>native-httpd-module</code> | <code>apache</code> is direct | [guide](apache.md) / [source](../../connectors/apache/README.md) | Native module route; P1–P4 observations remain run/evidence dependent and response-body processing can finalize at EOS |
| NGINX | <code>native-nginx-http-module</code> | <code>nginx</code> is direct | [guide](nginx.md) / [source](../../connectors/nginx/README.md) | Native HTTP module route; P1–P4 require the selected host run and artifacts |
| HAProxy | <code>native-htx-filter</code> | <code>haproxy-htx</code> is direct; <code>haproxy-spoe-spop</code> is a separate companion profile | [guide](haproxy.md) / [source](../../connectors/haproxy/README.md) | Native HTX body slices are incremental and P4 completes at HTX EOS; raw SPOP alone is not response-phase evidence |
| Envoy | <code>ext_proc</code> | <code>envoy-ext-proc</code> is direct; <code>envoy-ext-authz</code> requires its response observer | [guide](envoy.md) / [source](../../connectors/envoy/README.md) | Streamed external processing; strict post-commit reset remains a separate, evidence-gated question |
| Traefik | <code>native-traefik-middleware</code> | <code>traefik-native-uds</code> is direct; <code>traefik-forwardauth</code> requires its response observer | [guide](traefik.md) / [source](../../connectors/traefik/README.md) | Native middleware with a local UDS service; strict reset remains separate until host evidence proves it |
| lighttpd | <code>patched-native-lighttpd</code> | Canonical Stock profile <code>lighttpd-stock</code> / <code>stock-lighttpd-sidecar</code>; separate direct profile <code>lighttpd-patched</code> / <code>patched-native-lighttpd</code> | [guide](lighttpd.md) / [source](../../connectors/lighttpd/README.md) | The unmodified native <code>stock-lighttpd</code> route is a noncanonical P1/P3 compatibility translation; neither logical profile is a fallback for the other |

The host-family runner value is the internal target identity checked by the
root lifecycle runner. It does not collapse the logical profiles listed below.
The recorded integration mode is the descriptive value written into run-local
effective capability information. Do not interchange the names or set them
manually to reclassify a request-only service, companion, or compatibility
translation.

## Logical profile inventory

| Logical connector solution | Profile ID | Contract route and evidence boundary |
|---|---|---|
| Apache Native | <code>apache</code> | Direct native HTTPD module route |
| NGINX Native | <code>nginx</code> | Direct native NGINX HTTP module route |
| HAProxy HTX Native | <code>haproxy-htx</code> | Direct native HTX filter route |
| HAProxy SPOE/SPOP + HTX Response Companion | <code>haproxy-spoe-spop</code> | SPOP maps P1/P2; the mandatory native-HTX response companion maps P3/P4 |
| Envoy ext_authz + ext_proc Response Observer | <code>envoy-ext-authz</code> | Request authorization service plus mandatory response observer; the direct service alone is request-only |
| Envoy ext_proc Native | <code>envoy-ext-proc</code> | Direct streamed external-processing route |
| Traefik forwardAuth + Response Observer | <code>traefik-forwardauth</code> | Request authorization service plus mandatory private-UDS response observer; the direct service alone is request-only |
| Traefik Native UDS | <code>traefik-native-uds</code> | Direct native middleware and local UDS engine route |
| lighttpd Stock Sidecar | <code>lighttpd-stock</code> | Canonical logical Stock route: a traffic-owning bounded HTTP/1.1 sidecar; component evidence is not native Stock-module host evidence |
| lighttpd Patched Native | <code>lighttpd-patched</code> | Separate patched-native route; it is not a Stock-route fallback |

## Integration modes

| Mode | Host and role | Request/response visibility | Core route or compatibility term | Known boundary |
|---|---|---|---|---|
| <code>native-httpd-module</code> | Apache module loaded by httpd | Host request/response hooks and filters | Selected Apache core route | Response-body decisions may finalize at EOS; evidence must show the actual outcome |
| <code>native-nginx-http-module</code> | NGINX HTTP module | NGINX request/response processing | Selected NGINX core route | Host configuration, worker permissions, and runtime artifacts remain profile-specific |
| <code>native-htx-filter</code> | HAProxy native HTX filter | HTX request/response representation | Selected HAProxy core route | HTX/EOS semantics are not a claim of complete transport or protocol coverage |
| <code>ext_proc</code> | Envoy external processing bridge | Streamed host/processor exchange | Selected Envoy core route | A processor/gRPC event is not automatically proof of a client-visible strict reset |
| <code>native-traefik-middleware</code> | Traefik native middleware with local UDS service | Middleware request/response path through its local engine | Recorded selected Traefik mode | UDS locality and source wiring do not themselves prove strict transport behavior |
| <code>patched-native-lighttpd</code> | Patched lighttpd native core plus module | HTTP/1 entity-body ranges before transfer framing; selected `mod_proxy` P2 gate buffers until EOS/allow with `body_limit_action=reject` | Recorded selected lighttpd mode | The gate is not a claim for HTTP/2/HTTP/3, other stream handlers, P4, or unrestricted upstream streaming |
| <code>ext_authz</code> | Envoy external authorization service | Normally pre-upstream authorization view | Request component of the separate <code>envoy-ext-authz</code> logical profile | It does not observe the later upstream response without its mandatory observer |
| <code>forwardAuth</code> | Traefik forward-auth integration | Authorization request/response decision | Request component of the separate <code>traefik-forwardauth</code> logical profile | Do not relabel the direct service as native-middleware evidence or omit its mandatory observer |
| <code>spoe-spop-agent</code> | HAProxy agent/protocol vocabulary | Agent-mediated request/response path | Request component of the separate <code>haproxy-spoe-spop</code> logical profile | Do not interchange raw SPOP with the mandatory native-HTX response companion |

<code>EOS</code> means end of stream, <code>HTX</code> is HAProxy’s internal
HTTP transaction representation, and <code>UDS</code> is a Unix domain socket.
See the [glossary](../reference/glossary.md) for the complete definitions.

## Target map

| Task | Target | Important input | Output / limitation |
|---|---|---|---|
| Build one connector | <code>make build-<connector></code> | Safe <code>BUILD_ROOT</code>; host prerequisites | Build output only; no runtime assertion |
| Check one configuration | <code>make check-config-<connector></code> | Prepared selected host/config | Config-load diagnostic; no traffic |
| Run a minimal smoke | <code>make runtime-smoke-<connector></code> where provided | Prepared host and safe runtime paths | Focused runtime output; not full-lifecycle evidence |
| Run the selected No-CRS baseline | <code>make no-crs-baseline-<connector></code> | <code>NO_CRS_RULES_FILE</code>, safe paths | Candidate evidence selected by capabilities |
| Run one full lifecycle | <code>make full-lifecycle-<connector></code> | Target-managed profile identity; <code>NO_CRS_RUN_ID</code> recommended | Candidate full-lifecycle artifacts |
| Validate a connector run | <code>make evidence-check-<connector></code> | <code>NO_CRS_RUN_ID</code> or latest run ID, <code>EVIDENCE_ROOT</code> | Read-only evidence validation |

The placeholder <code>&lt;connector&gt;</code> allows
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code>, and <code>lighttpd</code>. Example:

~~~sh
NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-nginx
~~~

<code>NO_CRS_RUN_ID</code> is a safe identifier for one evidence set. It is
required by explicit evidence gates, has no fixed root default, and must not
contain secrets, personal data, slashes, or traversal segments. The example
does not assert the outcome of the command; inspect the generated artifacts
and validation result. See [configuration variables](../reference/variables.md#no-crs-and-evidence-variables).

## Configuration variables and placeholders

The central [variable reference](../reference/variables.md) documents
format, default, setter, scope, effect, and safety for root variables and
direct harness controls. The concise connector-specific groups are:

| Connector | Typical direct variables | What to verify before use |
|---|---|---|
| Apache | <code>APACHE_HTTPD</code>, <code>APXS</code>/<code>APXS_BIN</code>, <code>APACHE_MODULE</code>, <code>HTTPD_PREFIX</code>, <code>PORT</code> | Trusted host/module paths and a loopback port |
| NGINX | <code>NGINX_BINARY</code>, <code>NGINX_MODULE</code>, <code>NGINX_PREFIX</code>, <code>NGINX_HARNESS_PARENT</code>, <code>NGINX_WORKER_USER</code> | Module/binary compatibility and worker access to runtime paths |
| HAProxy | <code>HAPROXY_BIN</code>, <code>SPOA_RUNTIME_BIN</code>, <code>HAPROXY_HTX_CANONICAL_RULES_FILE</code>, port offsets | Trusted host/agent binaries and non-conflicting loopback ports |
| Envoy | <code>ENVOY_BIN</code>, <code>EXT_PROC_BIN</code>, <code>ENVOY_CONFIG</code>, <code>EXT_PROC_PORT</code> | Generated config outside checkout and valid local ports |
| Traefik | <code>TRAEFIK_BIN</code>, <code>TRAEFIK_NATIVE_RUNTIME_ROOT</code>, <code>TRAEFIK_ENGINE_SOCKET_PARENT</code>, <code>TRAEFIK_CONNECTOR_CONFIG</code>, <code>TRAEFIK_CONNECTOR_LISTEN</code> | Trusted binary, private runtime/socket parent, loopback listen addresses |
| lighttpd | <code>LIGHTTPD_BIN</code>, <code>LIGHTTPD_PATCHED_ROOT</code>, <code>LIGHTTPD_CONNECTOR_MODULE</code>, <code>LIGHTTPD_SMOKE_PORT</code> | Matching patched host/module, absolute external paths, valid loopback port |

Names in this table are not a promise that every direct override is suitable
for CI or canonical evidence. The root targets set compatible invocation-local
values and should be preferred.

## Status and evidence boundary

Use <code>PASS</code>, <code>FAIL</code>, <code>BLOCKED</code>,
<code>NOT EXECUTED</code>, <code>NOT APPLICABLE</code>, and
<code>UNSUPPORTED</code> exactly as defined in
[Testing and evidence](../testing-and-evidence.md). A capability may be
<code>implemented_not_asserted</code> without any particular canonical run
having passed. Conversely, an evidence run is evaluated against its selected
profile, rules, case requirements, and artifacts; it does not certify
unselected protocols or compatibility paths.

Read [Testing and evidence](../testing-and-evidence.md) before using a connector result in a
report or claim.

## New and future connector contract

A new connector first declares origin, capabilities, configuration mapping,
request/response mapping, decision/event mapping, and artifact layout. It keeps
host API types, hooks, filters, protocol framing, build glue, and object
lifetime in its connector tree. It may use Common request/response/config
contracts and the generic mapper only when the host data fits those contracts;
body payloads are never logged through that path.

| Requirement | Before a runtime claim |
| --- | --- |
| Configuration | Register host syntax while keeping host-specific parser types local |
| Mapping | Validate mapped request/response output against Common contracts |
| Provenance | Maintain origin metadata, capability manifest, and selected mode |
| Testing | Provide a real host harness and payload-safe run artifacts |
| Status | Keep starter paths not verified until matching runtime evidence exists |

Future host work follows the same distinction between host integration and
logical profile used by the six current integrations and ten current profiles.
A source scaffold, generic mapper, compatible API, or build smoke does not
establish a real-world connector path.

## New connector evidence contract

A new connector keeps host hooks, parser registrations, body/response
handling, protocol framing, build glue, object lifetime, and host-specific
diagnostics in its connector tree. Its repository guide is the canonical
reader-facing explanation; code-adjacent files record provenance and local
execution details. Do not create a connector-local test tree: reusable
executable cases, schemas, and runners stay Framework-owned.

| Required artifact | Minimum recorded content | Boundary |
| --- | --- | --- |
| <code>README.*</code> | Selected route, local build/harness entry points, and explicit limitations | Source or configuration presence is not runtime evidence |
| <code>TODO.md</code> | Open integration, coverage, and promotion work | A checked box is not a result record |
| <code>ORIGIN.md</code> and source map | Upstream choice, license, imported files, local changes, and pins | Never invent source, license, version, or API facts |
| <code>metadata.*</code> and build glue | Connector identity, owned build inputs, paths, and prerequisite behavior | A compile/link check is not host traffic |
| Harness and local configuration | Exact selected host/profile inputs and payload-safe output location | A start/config check is not a lifecycle result |
| Framework case/catalog references | Case scope, ruleset variant, runner, and result/evidence identifiers | Do not copy Framework tests into <code>connectors/&lt;name&gt;/tests</code> |

## Evidence and promotion conditions

Record the command, exit behavior, connector scope, selected profile, ruleset,
run ID, effective non-secret configuration, result/event artifacts, and
PASS/FAIL/BLOCKED/NOT EXECUTED outcomes before making a scoped claim. No-CRS
and With-CRS variants remain separate: one never substitutes for the other.
The minimum review matrix covers P1, P2, P3, P4, response-body behavior,
negative/pass-through behavior, audit/log observations, configuration/startup
behavior, and remaining blocking or failing rows.

| Scope label | Minimum recorded basis | Insufficient basis |
| --- | --- | --- |
| <code>template</code> or <code>scaffolded</code> | Structure and documentation requirements only | Any inferred host behavior |
| <code>adapter-owned</code> | Owned source/build metadata plus provenance | A guessed upstream or copied compatibility description |
| <code>runtime-smoke-verified</code> | Current selected host smoke with command and result artifacts | Static source, a generated report, or a process-only start |
| <code>crs-verified</code> | Current selected With-CRS run, effective CRS input, and result artifacts | A No-CRS outcome |
| <code>partial</code> | Truthfully bounded structure or selected evidence | A claim of complete phase, protocol, or matrix coverage |
| More than <code>partial</code> | Reviewed matrix and evidence for every claimed capability; gaps stay explicit | Pass-through/log-only output as response-body blocking proof |

Framework cases live under
<code>modules/ModSecurity-test-Framework/tests/cases/</code>, optional
connector-specific cases under
<code>modules/ModSecurity-test-Framework/tests/cases/connector-specific/&lt;connector&gt;/</code>,
and Framework runners under
<code>modules/ModSecurity-test-Framework/tests/runners/</code>. Cite only
targets that exist in the parent Makefile and read the
[testing/evidence guide](../testing-and-evidence.md) before interpreting a
result.
