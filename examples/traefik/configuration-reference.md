# Traefik configuration reference

**Language:** English | [Deutsch](configuration-reference.de.md)

## Scope and source of truth

Selected integration mode: `native-middleware-uds-engine`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.
Compatibility entries are explicitly labelled and are not part of the selected core path.

## Configuration inventory

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`accessLog`](#accesslog) | Host / Connector | Traefik access-log configuration mapping | no | No connector-owned access-log configuration default is declared; the selected template sets an empty configuration mapping. | The YAML object path shown in the selected example. | Enables/configures the Traefik access-log surface in the selected static example. |
| [`entryPoints`](#entrypoints) | Host / Connector | Traefik static entry-point mapping | no | No connector-owned entry-point registry default is declared; the selected template sets the web listener. | The YAML object path shown in the selected example. | Groups named listener definitions used by dynamic routers. |
| [`entryPoints.web`](#entrypoints-web) | Host / Connector | Traefik EntryPoint mapping | no | No connector-owned web entry point default is declared; the selected template sets the :8080 listener. | The YAML object path shown in the selected example. | Defines the named web listener that dynamic routers attach to. |
| [`entryPoints.web.address`](#entrypoints-web-address) | Host / Connector | Traefik listener address string | no | No connector-owned web listener address default is declared; the selected template sets :8080. | The YAML object path shown in the selected example. | Binds the named web entry point used by the example router. |
| [`experimental`](#experimental) | Host / Connector | Traefik static experimental configuration mapping | no | No connector-owned experimental configuration default is declared; the selected template sets the modsecurityNative local-plugin declaration. | The YAML object path shown in the selected example. | Groups static experimental features needed to make the repository-owned local plugin discoverable. |
| [`experimental.localPlugins`](#experimental-localplugins) | Host / Connector | Traefik static local-plugin registry mapping | no | No connector-owned local-plugin registry default is declared; the selected template sets one modsecurityNative declaration. | The YAML object path shown in the selected example. | Registers the local plugin name that dynamic middleware configuration later references. |
| [`experimental.localPlugins.modsecurityNative`](#experimental-localplugins-modsecuritynative) | Host / Connector | Traefik local-plugin declaration mapping | no | No connector-owned modsecurityNative declaration default is declared; the selected template sets the repository module and empty environment settings. | The YAML object path shown in the selected example. | Binds the dynamic plugin name modsecurityNative to its local module configuration. |
| [`experimental.localPlugins.modsecurityNative.moduleName`](#experimental-localplugins-modsecuritynative-modulename) | Host / Connector | Traefik local-plugin Go module path string | no | No connector-owned local-plugin module path default is declared; the selected template sets github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware. | The YAML object path shown in the selected example. | Selects the Go module/package Traefik loads for the modsecurityNative local plugin. |
| [`experimental.localPlugins.modsecurityNative.settings`](#experimental-localplugins-modsecuritynative-settings) | Host / Connector | Traefik local-plugin settings mapping | no | No connector-owned local-plugin settings default is declared; the selected template sets an empty envs list. | The YAML object path shown in the selected example. | Groups host-level settings for the selected local-plugin declaration. |
| [`experimental.localPlugins.modsecurityNative.settings.envs`](#experimental-localplugins-modsecuritynative-settings-envs) | Host / Connector | Traefik local-plugin environment-settings list | no | Selected value is []; no example-provided plugin environment setting is added. | The YAML object path shown in the selected example. | Leaves the local-plugin declaration without example-provided environment inputs. |
| [`http`](#http) | Host / Connector | Traefik dynamic HTTP configuration mapping | no | No connector-owned dynamic HTTP topology default is declared; the selected template sets one app router, one middleware, and one app service. | The YAML object path shown in the selected example. | Groups the request router, middleware attachment, and upstream service used by the example. |
| [`http.middlewares`](#http-middlewares) | Host / Connector | Traefik dynamic middleware registry mapping | no | No connector-owned middleware registry default is declared; the selected template sets the selected native or compatibility middleware. | The YAML object path shown in the selected example. | Groups middleware definitions referenced by routers. |
| [`http.middlewares.modsecurity-native-streaming`](#http-middlewares-modsecurity-native-streaming) | Host / Connector | Traefik named middleware mapping | no | No connector-owned named middleware default is declared; the selected template sets the selected native modsecurity mapping. | The YAML object path shown in the selected example. | Binds the router-visible middleware name to its plugin or forwardAuth configuration. |
| [`http.middlewares.modsecurity-native-streaming.plugin`](#http-middlewares-modsecurity-native-streaming-plugin) | Host / Connector | Traefik plugin middleware mapping | no | No connector-owned plugin middleware mapping default is declared; the selected template sets the modsecurityNative local plugin. | The YAML object path shown in the selected example. | Selects the local-plugin configuration for the named native middleware. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative) | Host / Connector | Traefik local-plugin configuration mapping | no | Plugin CreateConfig supplies bounded defaults; this template explicitly sets all seven selected fields. | The YAML object path shown in the selected example. | Groups limits, transaction ID, and engine connection fields passed to the repository native middleware. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginemode) | Host / Connector | native middleware engine-mode enum | no | passthrough | http.middlewares.<name>.plugin.modsecurityNative | Selects source-only passthrough or the persistent UDS engine; the selected rule-evaluating example uses uds. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginesocketpath) | Host / Connector | absolute Unix-domain socket path | no | none (ignored outside uds; required and validated in uds mode) | http.middlewares.<name>.plugin.modsecurityNative | Names the private UDS path used by native middleware when engineMode is uds. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheaderbytes) | Host / Connector | integer aggregate header-byte bound | no | 65536 | http.middlewares.<name>.plugin.modsecurityNative | Caps aggregate request and response header bytes passed to native middleware engine callbacks. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheadercount) | Host / Connector | integer header-count bound | no | 128 | http.middlewares.<name>.plugin.modsecurityNative | Caps the number of request and response headers passed to native middleware engine callbacks. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxrequestchunkbytes) | Host / Connector | integer request-body chunk-byte bound | no | 32768 | http.middlewares.<name>.plugin.modsecurityNative | Caps each streamed request-body chunk offered to the native middleware engine. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxresponsechunkbytes) | Host / Connector | integer response-body chunk-byte bound | no | 32768 | http.middlewares.<name>.plugin.modsecurityNative | Caps each streamed response-body chunk offered to the native middleware engine. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-transactionidheader) | Host / Connector | HTTP header-name string | no | X-Request-Id | http.middlewares.<name>.plugin.modsecurityNative | Selects the incoming request header used to correlate middleware and engine transaction metadata. |
| [`http.routers`](#http-routers) | Host / Connector | Traefik dynamic router registry mapping | no | No connector-owned router registry default is declared; the selected template sets one app router. | The YAML object path shown in the selected example. | Groups dynamic request-routing definitions. |
| [`http.routers.app`](#http-routers-app) | Host / Connector | Traefik dynamic Router mapping | no | No connector-owned app router default is declared; the selected template sets the explicit catch-all app route. | The YAML object path shown in the selected example. | Binds a request rule and entry point to the listed middleware and app service. |
| [`http.routers.app.entryPoints`](#http-routers-app-entrypoints) | Host / Connector | Traefik router entry-point name list | no | No connector-owned router entry-point binding default is declared; the selected template sets the web entry point. | The YAML object path shown in the selected example. | Restricts the app router to the named static listener. |
| [`http.routers.app.entryPoints[]`](#http-routers-app-entrypoints) | Host / Connector | Traefik entry-point name string | no | No connector-owned router entry-point binding default is declared; the selected template sets the web entry point. | The YAML object path shown in the selected example. | Restricts the app router to the named static listener. |
| [`http.routers.app.middlewares`](#http-routers-app-middlewares) | Host / Connector | ordered Traefik middleware-name list | no | No connector-owned router middleware list default is declared; the selected template sets the selected native UDS middleware. | The YAML object path shown in the selected example. | Attaches middleware to the router in listed order before forwarding to the app service. |
| [`http.routers.app.middlewares[]`](#http-routers-app-middlewares) | Host / Connector | Traefik middleware-name string | no | No connector-owned router middleware list default is declared; the selected template sets the selected native UDS middleware. | The YAML object path shown in the selected example. | Attaches middleware to the router in listed order before forwarding to the app service. |
| [`http.routers.app.rule`](#http-routers-app-rule) | Host / Connector | Traefik router-rule expression string | no | No connector-owned app router rule default is declared; the selected template sets the catch-all PathPrefix(`/`) expression. | The YAML object path shown in the selected example. | Matches incoming requests to the app router. |
| [`http.routers.app.service`](#http-routers-app-service) | Host / Connector | Traefik service-name string | no | No connector-owned router service target default is declared; the selected template sets the app service. | The YAML object path shown in the selected example. | Selects the upstream service after router middleware completes. |
| [`http.services`](#http-services) | Host / Connector | Traefik dynamic service registry mapping | no | No connector-owned service registry default is declared; the selected template sets the app load-balancer service. | The YAML object path shown in the selected example. | Groups upstream service definitions referenced by routers. |
| [`http.services.app`](#http-services-app) | Host / Connector | Traefik named service mapping | no | No connector-owned app service default is declared; the selected template sets one load-balancer with a loopback server. | The YAML object path shown in the selected example. | Binds the router's app service name to its load balancer. |
| [`http.services.app.loadBalancer`](#http-services-app-loadbalancer) | Host / Connector | Traefik LoadBalancer service mapping | no | No connector-owned app load balancer default is declared; the selected template sets one loopback app server. | The YAML object path shown in the selected example. | Groups the upstream server endpoints for the app service. |
| [`http.services.app.loadBalancer.servers`](#http-services-app-loadbalancer-servers) | Host / Connector | repeated Traefik load-balancer server mapping | no | No connector-owned app server list default is declared; the selected template sets one http://127.0.0.1:8081 endpoint. | The YAML object path shown in the selected example. | Defines the endpoint candidates for the app load balancer. |
| [`http.services.app.loadBalancer.servers[].url`](#http-services-app-loadbalancer-servers-url) | Host / Connector | Traefik upstream server URL string | no | No connector-owned app server URL default is declared; the selected template sets http://127.0.0.1:8081. | The YAML object path shown in the selected example. | Targets the application server that receives requests after router middleware. |
| [`log`](#log) | Host / Connector | Traefik log configuration mapping | no | No connector-owned log configuration default is declared; the selected template sets level INFO. | The YAML object path shown in the selected example. | Groups Traefik process-log settings. |
| [`log.level`](#log-level) | Host / Connector | Traefik log-level token | no | No connector-owned log level default is declared; the selected template sets INFO. | The YAML object path shown in the selected example. | Controls Traefik process-log verbosity. |
| [`providers`](#providers) | Host / Connector | Traefik static provider registry mapping | no | No connector-owned provider registry default is declared; the selected template sets the adjacent dynamic File Provider. | The YAML object path shown in the selected example. | Groups configuration providers that supply dynamic routers, middlewares, and services. |
| [`providers.file`](#providers-file) | Host / Connector | Traefik File Provider mapping | no | No connector-owned file provider default is declared; the selected template sets the adjacent traefik-dynamic.yaml file. | The YAML object path shown in the selected example. | Configures the on-disk dynamic configuration provider. |
| [`providers.file.filename`](#providers-file-filename) | Host / Connector | Traefik File Provider path string | no | No connector-owned dynamic file path default is declared; the selected template sets ./traefik-dynamic.yaml. | The YAML object path shown in the selected example. | Selects the companion dynamic file containing routers, middleware, and upstream service definitions. |
| [`providers.file.watch`](#providers-file-watch) | Host / Connector | Traefik File Provider boolean | no | No connector-owned File Provider watch behavior default is declared; the selected template sets false. | The YAML object path shown in the selected example. | Controls whether Traefik watches the dynamic file for reloads after initial load. |
| [`compatibility.forwardauth-dynamic.http`](#compatibility-forwardauth-dynamic-http) | Compatibility | Traefik dynamic HTTP configuration mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Groups the request router, middleware attachment, and upstream service used by the example. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.middlewares`](#compatibility-forwardauth-dynamic-http-middlewares) | Compatibility | Traefik dynamic middleware registry mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Groups middleware definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth) | Compatibility | Traefik named middleware mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Binds the router-visible middleware name to its plugin or forwardAuth configuration. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth) | Compatibility | Traefik ForwardAuth middleware mapping (compatibility only) | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Groups the request-only external authorization service settings. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-address) | Compatibility | Traefik ForwardAuth HTTP URL string (compatibility only) | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "http://127.0.0.1:9000/authorize". | Compatibility YAML path only (forwardauth-dynamic) | Targets the external forwardAuth decision service before the app service is contacted. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-trustforwardheader) | Compatibility | Traefik ForwardAuth boolean (compatibility only) | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures false. | Compatibility YAML path only (forwardauth-dynamic) | Controls whether forwarded request headers are trusted when calling the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers`](#compatibility-forwardauth-dynamic-http-routers) | Compatibility | Traefik dynamic router registry mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Groups dynamic request-routing definitions. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app`](#compatibility-forwardauth-dynamic-http-routers-app) | Compatibility | Traefik dynamic Router mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Binds a request rule and entry point to the listed middleware and app service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app.entryPoints`](#compatibility-forwardauth-dynamic-http-routers-app-entrypoints) | Compatibility | Traefik router entry-point name list | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["web"]. | Compatibility YAML path only (forwardauth-dynamic) | Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]`](#compatibility-forwardauth-dynamic-http-routers-app-entrypoints) | Compatibility | Traefik entry-point name string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "web". | Compatibility YAML path only (forwardauth-dynamic) | Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app.middlewares`](#compatibility-forwardauth-dynamic-http-routers-app-middlewares) | Compatibility | ordered Traefik middleware-name list | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["modsecurity-auth"]. | Compatibility YAML path only (forwardauth-dynamic) | Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app.middlewares[]`](#compatibility-forwardauth-dynamic-http-routers-app-middlewares) | Compatibility | Traefik middleware-name string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "modsecurity-auth". | Compatibility YAML path only (forwardauth-dynamic) | Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app.rule`](#compatibility-forwardauth-dynamic-http-routers-app-rule) | Compatibility | Traefik router-rule expression string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "PathPrefix(`/`)". | Compatibility YAML path only (forwardauth-dynamic) | Matches incoming requests to the app router. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.routers.app.service`](#compatibility-forwardauth-dynamic-http-routers-app-service) | Compatibility | Traefik service-name string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "app". | Compatibility YAML path only (forwardauth-dynamic) | Selects the upstream service after router middleware completes. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.services`](#compatibility-forwardauth-dynamic-http-services) | Compatibility | Traefik dynamic service registry mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Groups upstream service definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.services.app`](#compatibility-forwardauth-dynamic-http-services-app) | Compatibility | Traefik named service mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Binds the router's app service name to its load balancer. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.services.app.loadBalancer`](#compatibility-forwardauth-dynamic-http-services-app-loadbalancer) | Compatibility | Traefik LoadBalancer service mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Groups the upstream server endpoints for the app service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers`](#compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers) | Compatibility | repeated Traefik load-balancer server mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-dynamic) | Defines the endpoint candidates for the app load balancer. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url`](#compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers-url) | Compatibility | Traefik upstream server URL string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "http://127.0.0.1:8081". | Compatibility YAML path only (forwardauth-dynamic) | Targets the application server that receives requests after router middleware. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.accessLog`](#compatibility-forwardauth-static-accesslog) | Compatibility | Traefik access-log configuration mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures {}. | Compatibility YAML path only (forwardauth-static) | Enables/configures the Traefik access-log surface in the selected static example. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.entryPoints`](#compatibility-forwardauth-static-entrypoints) | Compatibility | Traefik static entry-point mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-static) | Groups named listener definitions used by dynamic routers. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.entryPoints.web`](#compatibility-forwardauth-static-entrypoints-web) | Compatibility | Traefik EntryPoint mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-static) | Defines the named web listener that dynamic routers attach to. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.entryPoints.web.address`](#compatibility-forwardauth-static-entrypoints-web-address) | Compatibility | Traefik listener address string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ":8080". | Compatibility YAML path only (forwardauth-static) | Binds the named web entry point used by the example router. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.log`](#compatibility-forwardauth-static-log) | Compatibility | Traefik log configuration mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-static) | Groups Traefik process-log settings. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.log.level`](#compatibility-forwardauth-static-log-level) | Compatibility | Traefik log-level token | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures INFO. | Compatibility YAML path only (forwardauth-static) | Controls Traefik process-log verbosity. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.providers`](#compatibility-forwardauth-static-providers) | Compatibility | Traefik static provider registry mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-static) | Groups configuration providers that supply dynamic routers, middlewares, and services. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.providers.file`](#compatibility-forwardauth-static-providers-file) | Compatibility | Traefik File Provider mapping | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (forwardauth-static) | Configures the on-disk dynamic configuration provider. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.providers.file.filename`](#compatibility-forwardauth-static-providers-file-filename) | Compatibility | Traefik File Provider path string | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "./traefik-dynamic.yaml". | Compatibility YAML path only (forwardauth-static) | Selects the companion dynamic file containing routers, middleware, and upstream service definitions. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.forwardauth-static.providers.file.watch`](#compatibility-forwardauth-static-providers-file-watch) | Compatibility | Traefik File Provider boolean | no | Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures true. | Compatibility YAML path only (forwardauth-static) | Controls whether Traefik watches the dynamic file for reloads after initial load. Compatibility-only host/service setup outside the selected native core path. |
| [`forwardAuth`](#forwardauth) | Compatibility | Traefik compatibility middleware | no | not part of selected native middleware path | Compatibility dynamic middleware | Compatibility-only forwardAuth middleware. |

## Layer separation

Host/connector switches bind or configure host integration. They are not the same setting as `SecRuleEngine`.

- [Common Runtime configuration](../common/common-connector-configuration.md) covers only the `key=value` runtime file and is not presented as an unregistered host directive.
- [ModSecurity Engine directives](../common/modsecurity-directives.md) covers `Sec*` directives in the loaded rule file.
- [Rule examples](../common/rule-examples.md) explains DetectionOnly and engine Off.

## Common Runtime relevance

| Key | Local use | Detailed reference |
| --- | --- | --- |
| `enabled` | Selected runtime profile key | [enabled](../common/common-connector-configuration.md#enabled) |
| `rules_file` | Selected runtime profile key | [rules_file](../common/common-connector-configuration.md#rules-file) |
| `transaction_id_header` | Selected runtime profile key | [transaction_id_header](../common/common-connector-configuration.md#transaction-id-header) |
| `request_body_mode` | Selected runtime profile key | [request_body_mode](../common/common-connector-configuration.md#request-body-mode) |
| `response_body_mode` | Selected runtime profile key | [response_body_mode](../common/common-connector-configuration.md#response-body-mode) |
| `request_body_limit` | Selected runtime profile key | [request_body_limit](../common/common-connector-configuration.md#request-body-limit) |
| `response_body_limit` | Selected runtime profile key | [response_body_limit](../common/common-connector-configuration.md#response-body-limit) |
| `body_limit_action` | Selected runtime profile key | [body_limit_action](../common/common-connector-configuration.md#body-limit-action) |
| `phase4_mode` | Selected runtime profile key | [phase4_mode](../common/common-connector-configuration.md#phase4-mode) |
| `default_block_status` | Selected runtime profile key | [default_block_status](../common/common-connector-configuration.md#default-block-status) |
| `default_error_status` | Selected runtime profile key | [default_error_status](../common/common-connector-configuration.md#default-error-status) |
| `use_error_log` | Selected runtime profile key | [use_error_log](../common/common-connector-configuration.md#use-error-log) |
| `max_header_count` | Selected runtime profile key | [max_header_count](../common/common-connector-configuration.md#max-header-count) |
| `max_header_name_size` | Selected runtime profile key | [max_header_name_size](../common/common-connector-configuration.md#max-header-name-size) |
| `max_header_value_size` | Selected runtime profile key | [max_header_value_size](../common/common-connector-configuration.md#max-header-value-size) |
| `max_total_header_bytes` | Selected runtime profile key | [max_total_header_bytes](../common/common-connector-configuration.md#max-total-header-bytes) |
| `max_event_json_bytes` | Selected runtime profile key | [max_event_json_bytes](../common/common-connector-configuration.md#max-event-json-bytes) |

## Engine directives used by profiles

The local rule profiles use `SecRuleEngine` for On, DetectionOnly, and Off. Where body inspection is selected, `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME scope, limits, and `SecRule` remain ModSecurity Engine directives.

See [Engine reference](../common/modsecurity-directives.md).

## Profiles

| Profile | File | Status |
| --- | --- | --- |
| Minimal | [minimal/traefik-static.yaml](minimal/traefik-static.yaml) | Active starter configuration |
| Safe full lifecycle | [safe/traefik-dynamic.yaml](safe/traefik-dynamic.yaml) | Selected bounded reference |
| Strict | [README.md#strict-profile-boundary](README.md#strict-profile-boundary) | Parser-supported or explicitly optional boundary |
| DetectionOnly | [detection-only/traefik-engine-service.conf](detection-only/traefik-engine-service.conf) | Engine evaluates/logs without disruptive action |
| Disabled | [disabled/traefik-engine-service.conf](disabled/traefik-engine-service.conf) | Connector or engine path disabled |

## Configuration combinations

| Connector | Engine | Request body | Response body | Result |
| --- | --- | --- | --- | --- |
| off | On | any | any | No connector transaction; engine setting is not reached. |
| on | Off | any | any | Connector reaches the engine, but engine rule processing is disabled. |
| on | DetectionOnly | enabled | enabled | Rules can match/log without disruptive enforcement. |
| on | On | Off | On | P2 body is unavailable to the engine; P4 remains host/capability dependent. |
| on | On | On | Off | P4 body is unavailable to the engine. |
| on | On | On | On + safe | Late post-commit P4 results are recorded without a promised later status change. |
| on | On | On | On + strict | Only use a host-specific strict outcome where source/evidence supports it; no synthetic late 403. |
| on | On | over limit + process_partial | over limit + reject | The body policy determines bounded engine input; exact host response handling remains connector-specific. |

## Validation

```sh
traefik check --configFile=<static-config>
```

Repository targets: `make check-config-traefik` and `make check-config-all-connectors`.

## Option details

<a id="accesslog"></a>
## `accessLog`

### Short description

Enables/configures the Traefik access-log surface in the selected static example.

### Syntax

```text
accessLog: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik access-log configuration mapping | empty mapping or documented access-log fields; selected value is {} | no |

### Default

No connector-owned access-log configuration default is declared; the selected template sets an empty configuration mapping.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Host observability only; it does not substitute for transaction P1–P4 processing or engine audit logging.

Enables/configures the Traefik access-log surface in the selected static example.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `{}`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Access logs can contain request metadata; configure safe storage, rotation, and privacy controls for deployment.

<a id="entrypoints"></a>
## `entryPoints`

### Short description

Groups named listener definitions used by dynamic routers.

### Syntax

```text
entryPoints: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik static entry-point mapping | named entry-point mappings; selected key is web | no |

### Default

No connector-owned entry-point registry default is declared; the selected template sets the web listener.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static listener bootstrap; its named entry point selects which requests can reach the router/middleware lifecycle.

Groups named listener definitions used by dynamic routers.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Entry-point addresses define the pre-policy network exposure of Traefik.

<a id="entrypoints-web"></a>
## `entryPoints.web`

### Short description

Defines the named web listener that dynamic routers attach to.

### Syntax

```text
entryPoints.web: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik EntryPoint mapping | address child field; selected entry point is web | no |

### Default

No connector-owned web entry point default is declared; the selected template sets the :8080 listener.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static entry point for the router; the native middleware begins after request routing selects it.

Defines the named web listener that dynamic routers attach to.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Changing this listener changes client reachability before middleware enforcement.

<a id="entrypoints-web-address"></a>
## `entryPoints.web.address`

### Short description

Binds the named web entry point used by the example router.

### Syntax

```text
entryPoints.web.address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik listener address string | Traefik entry-point address such as host:port or :port; selected value is :8080 | no |

### Default

No connector-owned web listener address default is declared; the selected template sets :8080.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Listener bootstrap before router selection and the attached native P1–P4 middleware path.

Binds the named web entry point used by the example router.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `":8080"`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

The selected :8080 form changes listener exposure according to host networking; use a private bind or explicit edge control as appropriate.

<a id="experimental"></a>
## `experimental`

### Short description

Groups static experimental features needed to make the repository-owned local plugin discoverable.

### Syntax

```text
experimental: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik static experimental configuration mapping | localPlugins child mapping shown in the selected native static file | no |

### Default

No connector-owned experimental configuration default is declared; the selected template sets the modsecurityNative local-plugin declaration.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static bootstrap prerequisite for the native P1–P4 middleware path; it does not process traffic itself.

Groups static experimental features needed to make the repository-owned local plugin discoverable.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Local plugin loading executes selected repository code; pin and review the module source before use.

<a id="experimental-localplugins"></a>
## `experimental.localPlugins`

### Short description

Registers the local plugin name that dynamic middleware configuration later references.

### Syntax

```text
experimental.localPlugins: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik static local-plugin registry mapping | named local plugin declarations; selected key is modsecurityNative | no |

### Default

No connector-owned local-plugin registry default is declared; the selected template sets one modsecurityNative declaration.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static bootstrap prerequisite for the native router middleware and its P1–P4 callback surface.

Registers the local plugin name that dynamic middleware configuration later references.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

A registry entry selects executable plugin source; do not add unreviewed local modules.

<a id="experimental-localplugins-modsecuritynative"></a>
## `experimental.localPlugins.modsecurityNative`

### Short description

Binds the dynamic plugin name modsecurityNative to its local module configuration.

### Syntax

```text
experimental.localPlugins.modsecurityNative: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik local-plugin declaration mapping | moduleName and settings child fields | no |

### Default

No connector-owned modsecurityNative declaration default is declared; the selected template sets the repository module and empty environment settings.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static prerequisite for attaching the native middleware; no transaction lifecycle event occurs at declaration time.

Binds the dynamic plugin name modsecurityNative to its local module configuration.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

The declaration controls which local code Traefik loads; protect its configuration and source tree.

<a id="experimental-localplugins-modsecuritynative-modulename"></a>
## `experimental.localPlugins.modsecurityNative.moduleName`

### Short description

Selects the Go module/package Traefik loads for the modsecurityNative local plugin.

### Syntax

```text
experimental.localPlugins.modsecurityNative.moduleName: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik local-plugin Go module path string | module path resolving to the repository native_middleware package | no |

### Default

No connector-owned local-plugin module path default is declared; the selected template sets github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static prerequisite for the native middleware's P1–P4 callback implementation.

Selects the Go module/package Traefik loads for the modsecurityNative local plugin.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

This is code-selection input; use a reviewed, pinned source path and do not substitute an arbitrary module.

<a id="experimental-localplugins-modsecuritynative-settings"></a>
## `experimental.localPlugins.modsecurityNative.settings`

### Short description

Groups host-level settings for the selected local-plugin declaration.

### Syntax

```text
experimental.localPlugins.modsecurityNative.settings: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik local-plugin settings mapping | settings.envs child list; selected mapping contains an empty list | no |

### Default

No connector-owned local-plugin settings default is declared; the selected template sets an empty envs list.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static bootstrap only; the selected native request lifecycle starts when a router invokes the plugin.

Groups host-level settings for the selected local-plugin declaration.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Avoid placing credentials or production-specific secrets in plugin settings.

<a id="experimental-localplugins-modsecuritynative-settings-envs"></a>
## `experimental.localPlugins.modsecurityNative.settings.envs`

### Short description

Leaves the local-plugin declaration without example-provided environment inputs.

### Syntax

```text
experimental.localPlugins.modsecurityNative.settings.envs: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik local-plugin environment-settings list | list of Traefik local-plugin environment setting strings; selected list is empty | no |

### Default

Selected value is []; no example-provided plugin environment setting is added.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static bootstrap only; it does not change P1–P4 visibility by itself.

Leaves the local-plugin declaration without example-provided environment inputs.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `[]`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

An environment setting can carry secrets or change behavior; keep the selected empty list unless an explicit documented input is required.

<a id="http"></a>
## `http`

### Short description

Groups the request router, middleware attachment, and upstream service used by the example.

### Syntax

```text
http: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic HTTP configuration mapping | routers, middlewares, and services child mappings | no |

### Default

No connector-owned dynamic HTTP topology default is declared; the selected template sets one app router, one middleware, and one app service.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Groups the request router, middleware attachment, and upstream service used by the example.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

This topology controls which requests reach the engine and which upstream receives them; protect dynamic configuration writes.

<a id="http-middlewares"></a>
## `http.middlewares`

### Short description

Groups middleware definitions referenced by routers.

### Syntax

```text
http.middlewares: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic middleware registry mapping | named middleware mappings; selected key is modsecurity-native-streaming | no |

### Default

No connector-owned middleware registry default is declared; the selected template sets the selected native or compatibility middleware.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Groups middleware definitions referenced by routers.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Middleware definitions are policy attachment points; unreviewed changes can remove or replace inspection.

<a id="http-middlewares-modsecurity-native-streaming"></a>
## `http.middlewares.modsecurity-native-streaming`

### Short description

Binds the router-visible middleware name to its plugin or forwardAuth configuration.

### Syntax

```text
http.middlewares.modsecurity-native-streaming: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik named middleware mapping | one native modsecurity middleware configuration mapping | no |

### Default

No connector-owned named middleware default is declared; the selected template sets the selected native modsecurity mapping.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Binds the router-visible middleware name to its plugin or forwardAuth configuration.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The router reference must continue to point to this reviewed middleware name to avoid bypass.

<a id="http-middlewares-modsecurity-native-streaming-plugin"></a>
## `http.middlewares.modsecurity-native-streaming.plugin`

### Short description

Selects the local-plugin configuration for the named native middleware.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik plugin middleware mapping | named local-plugin child mapping; selected child is modsecurityNative | no |

### Default

No connector-owned plugin middleware mapping default is declared; the selected template sets the modsecurityNative local plugin.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Selects the local-plugin configuration for the named native middleware.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The plugin reference chooses code that processes requests and responses; preserve the reviewed local plugin name.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative`

### Short description

Groups limits, transaction ID, and engine connection fields passed to the repository native middleware.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik local-plugin configuration mapping | the seven native middleware Config fields documented from CreateConfig/normalizedConfig | no |

### Default

Plugin CreateConfig supplies bounded defaults; this template explicitly sets all seven selected fields.

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig/normalizedConfig`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Groups limits, transaction ID, and engine connection fields passed to the repository native middleware.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The UDS fields and bounds are enforcement-relevant; passthrough is not rule evaluation.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginemode"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode`

### Short description

Selects source-only passthrough or the persistent UDS engine; the selected rule-evaluating example uses uds.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode: <engineMode>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| native middleware engine-mode enum | passthrough \| uds | no |

### Default

passthrough

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

passthrough always allows and supplies no rule evaluation; uds is the engine transport for native P1/P2/P3/P4 callbacks.

Selects source-only passthrough or the persistent UDS engine; the selected rule-evaluating example uses uds.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `uds`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Use uds for the selected rule-evaluating path; passthrough is intentionally not enforcement.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginesocketpath"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath`

### Short description

Names the private UDS path used by native middleware when engineMode is uds.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath: <engineSocketPath>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| absolute Unix-domain socket path | required for uds; absolute with no NUL or '..' segment | no |

### Default

none (ignored outside uds; required and validated in uds mode)

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

Transport endpoint for native P1/P2/P3/P4 engine callbacks when uds mode is selected.

Names the private UDS path used by native middleware when engineMode is uds.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `/run/traefik-msconnector/engine.sock`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The socket directory and socket must be private to trusted processes; path traversal and NUL are rejected.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheaderbytes"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes`

### Short description

Caps aggregate request and response header bytes passed to native middleware engine callbacks.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes: <maxHeaderBytes>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer aggregate header-byte bound | positive; uds maximum 65536 | no |

### Default

65536

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

P1 request-header and P3 response-header callback byte bound.

Caps aggregate request and response header bytes passed to native middleware engine callbacks.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `65536`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The UDS wire contract rejects values above 65536; retain a bounded header budget.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheadercount"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount`

### Short description

Caps the number of request and response headers passed to native middleware engine callbacks.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount: <maxHeaderCount>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer header-count bound | positive; uds maximum 128 | no |

### Default

128

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

P1 request-header and P3 response-header callback bound; it does not buffer body bytes.

Caps the number of request and response headers passed to native middleware engine callbacks.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `128`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

A finite count limits header-flood work before data reaches the UDS engine.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxrequestchunkbytes"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes`

### Short description

Caps each streamed request-body chunk offered to the native middleware engine.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes: <maxRequestChunkBytes>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer request-body chunk-byte bound | positive; uds maximum 32768 | no |

### Default

32768

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

P2 request-body callback bound; it is a per-chunk limit, not a total request-body limit.

Caps each streamed request-body chunk offered to the native middleware engine.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `32768`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The UDS wire contract rejects values above 32768 and prevents one callback from accepting an unbounded chunk.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxresponsechunkbytes"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes`

### Short description

Caps each streamed response-body chunk offered to the native middleware engine.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes: <maxResponseChunkBytes>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer response-body chunk-byte bound | positive; uds maximum 32768 | no |

### Default

32768

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

P4 response-body callback bound; a late disruptive result remains log-only after response commitment.

Caps each streamed response-body chunk offered to the native middleware engine.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `32768`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The UDS wire contract rejects values above 32768; retain the bound for response-stream resource control.

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-transactionidheader"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader`

### Short description

Selects the incoming request header used to correlate middleware and engine transaction metadata.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader: <transactionIDHeader>
```

### Valid contexts

- http.middlewares.<name>.plugin.modsecurityNative

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| HTTP header-name string | non-empty non-whitespace header name | no |

### Default

X-Request-Id

Source: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Inheritance and merge

Traefik dynamic configuration object; no Common Runtime merge.

Merge: Traefik/plugin configuration is normalized once by the plugin.

### Phases and runtime effect

P1 request-header metadata selection; the value is carried through later lifecycle summaries, not used as a policy rule by itself.

Selects the incoming request header used to correlate middleware and engine transaction metadata.

### Validation and errors

normalizedConfig rejects invalid values; Traefik parses the containing dynamic configuration.

### Example

Selected example value: `X-Request-Id`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Do not put credentials or arbitrary sensitive payload into a correlation header; event/log consumers must protect it.

<a id="http-routers"></a>
## `http.routers`

### Short description

Groups dynamic request-routing definitions.

### Syntax

```text
http.routers: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic router registry mapping | named router mappings; selected key is app | no |

### Default

No connector-owned router registry default is declared; the selected template sets one app router.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Groups dynamic request-routing definitions.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Router rules and middleware order are enforcement-relevant; avoid unaudited route additions.

<a id="http-routers-app"></a>
## `http.routers.app`

### Short description

Binds a request rule and entry point to the listed middleware and app service.

### Syntax

```text
http.routers.app: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic Router mapping | rule, entryPoints, middlewares, and service child fields | no |

### Default

No connector-owned app router default is declared; the selected template sets the explicit catch-all app route.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Binds a request rule and entry point to the listed middleware and app service.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The router is the attachment point for the native UDS middleware or compatibility forwardAuth; removing it bypasses that path.

<a id="http-routers-app-entrypoints"></a>
## `http.routers.app.entryPoints`

### Short description

Restricts the app router to the named static listener.

### Syntax

```text
http.routers.app.entryPoints: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik router entry-point name list | defined static entry-point names | no |

### Default

No connector-owned router entry-point binding default is declared; the selected template sets the web entry point.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path.

Restricts the app router to the named static listener.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `["web"]`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Binding a router to a public entry point exposes its middleware/service path to that listener's clients.

<a id="http-routers-app-entrypoints"></a>
## `http.routers.app.entryPoints[]`

### Short description

Restricts the app router to the named static listener.

### Syntax

```text
http.routers.app.entryPoints[]: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik entry-point name string | name declared under static entryPoints; selected value is web | no |

### Default

No connector-owned router entry-point binding default is declared; the selected template sets the web entry point.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path.

Restricts the app router to the named static listener.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `"web"`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Binding a router to a public entry point exposes its middleware/service path to that listener's clients.

<a id="http-routers-app-middlewares"></a>
## `http.routers.app.middlewares`

### Short description

Attaches middleware to the router in listed order before forwarding to the app service.

### Syntax

```text
http.routers.app.middlewares: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ordered Traefik middleware-name list | names declared under http.middlewares | no |

### Default

No connector-owned router middleware list default is declared; the selected template sets the selected native UDS middleware.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Attaches middleware to the router in listed order before forwarding to the app service.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `["modsecurity-native-streaming"]`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service.

<a id="http-routers-app-middlewares"></a>
## `http.routers.app.middlewares[]`

### Short description

Attaches middleware to the router in listed order before forwarding to the app service.

### Syntax

```text
http.routers.app.middlewares[]: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik middleware-name string | selected native UDS middleware name | no |

### Default

No connector-owned router middleware list default is declared; the selected template sets the selected native UDS middleware.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.

Attaches middleware to the router in listed order before forwarding to the app service.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `"modsecurity-native-streaming"`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service.

<a id="http-routers-app-rule"></a>
## `http.routers.app.rule`

### Short description

Matches incoming requests to the app router.

### Syntax

```text
http.routers.app.rule: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik router-rule expression string | Traefik rule DSL; selected value is PathPrefix(`/`) | no |

### Default

No connector-owned app router rule default is declared; the selected template sets the catch-all PathPrefix(`/`) expression.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Selects requests that enter the attached native middleware P1/P2 path or compatibility P1 authorization path.

Matches incoming requests to the app router.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: ``PathPrefix(`/`)``.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The selected catch-all rule routes every path on the entry point; narrow it in a real deployment if required.

<a id="http-routers-app-service"></a>
## `http.routers.app.service`

### Short description

Selects the upstream service after router middleware completes.

### Syntax

```text
http.routers.app.service: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik service-name string | name declared under http.services; selected value is app | no |

### Default

No connector-owned router service target default is declared; the selected template sets the app service.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Forwarding occurs after request-side middleware; the native path can observe the returned response at P3/P4.

Selects the upstream service after router middleware completes.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `"app"`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

The target service URL is an egress destination; review it separately from middleware selection.

<a id="http-services"></a>
## `http.services`

### Short description

Groups upstream service definitions referenced by routers.

### Syntax

```text
http.services: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic service registry mapping | named service mappings; selected key is app | no |

### Default

No connector-owned service registry default is declared; the selected template sets the app load-balancer service.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The native middleware can receive the app response at P3/P4 after this service returns it; compatibility forwardAuth cannot.

Groups upstream service definitions referenced by routers.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Services define request destinations after middleware; review their endpoint URLs and credentials.

<a id="http-services-app"></a>
## `http.services.app`

### Short description

Binds the router's app service name to its load balancer.

### Syntax

```text
http.services.app: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik named service mapping | loadBalancer child mapping | no |

### Default

No connector-owned app service default is declared; the selected template sets one load-balancer with a loopback server.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Upstream service stage after request middleware; native response callbacks can observe returned headers/body at P3/P4.

Binds the router's app service name to its load balancer.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

This mapping is an upstream routing target; do not confuse it with the ModSecurity engine service.

<a id="http-services-app-loadbalancer"></a>
## `http.services.app.loadBalancer`

### Short description

Groups the upstream server endpoints for the app service.

### Syntax

```text
http.services.app.loadBalancer: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik LoadBalancer service mapping | servers child list | no |

### Default

No connector-owned app load balancer default is declared; the selected template sets one loopback app server.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

After request middleware, the selected server response is available to native P3/P4 callbacks; not to compatibility forwardAuth.

Groups the upstream server endpoints for the app service.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Each server URL is a traffic destination; limit it to the intended upstream.

<a id="http-services-app-loadbalancer-servers"></a>
## `http.services.app.loadBalancer.servers`

### Short description

Defines the endpoint candidates for the app load balancer.

### Syntax

```text
http.services.app.loadBalancer.servers: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Traefik load-balancer server mapping | one or more server URL mappings; selected example has one server | no |

### Default

No connector-owned app server list default is declared; the selected template sets one http://127.0.0.1:8081 endpoint.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Native response lifecycle P3/P4 begins only after the selected server responds; compatibility forwardAuth remains request-only.

Defines the endpoint candidates for the app load balancer.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Adding a server adds an upstream destination; review network scope and transport security.

<a id="http-services-app-loadbalancer-servers-url"></a>
## `http.services.app.loadBalancer.servers[].url`

### Short description

Targets the application server that receives requests after router middleware.

### Syntax

```text
http.services.app.loadBalancer.servers[].url: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik upstream server URL string | absolute backend URL; selected value is http://127.0.0.1:8081 | no |

### Default

No connector-owned app server URL default is declared; the selected template sets http://127.0.0.1:8081.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The returned upstream response is the native middleware's P3/P4 source; forwardAuth compatibility has no later response visibility.

Targets the application server that receives requests after router middleware.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `http://127.0.0.1:8081`.

Source-backed example: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Safety and operations

Loopback keeps the example local; remote URLs require explicit TLS, identity, and egress controls.

<a id="log"></a>
## `log`

### Short description

Groups Traefik process-log settings.

### Syntax

```text
log: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik log configuration mapping | level child field | no |

### Default

No connector-owned log configuration default is declared; the selected template sets level INFO.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Host observability only; no direct P1–P4 payload visibility change.

Groups Traefik process-log settings.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Logs can contain request and operational metadata; choose retention and access controls separately.

<a id="log-level"></a>
## `log.level`

### Short description

Controls Traefik process-log verbosity.

### Syntax

```text
log.level: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik log-level token | Traefik-supported level token; selected value is INFO | no |

### Default

No connector-owned log level default is declared; the selected template sets INFO.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Host observability only; it does not change native or compatibility lifecycle callbacks.

Controls Traefik process-log verbosity.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `INFO`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

Debug logging can expose more operational metadata; do not equate host logs with ModSecurity audit output.

<a id="providers"></a>
## `providers`

### Short description

Groups configuration providers that supply dynamic routers, middlewares, and services.

### Syntax

```text
providers: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik static provider registry mapping | file provider child mapping | no |

### Default

No connector-owned provider registry default is declared; the selected template sets the adjacent dynamic File Provider.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Static-to-dynamic handoff; it makes the router/middleware lifecycle available but does not process a transaction itself.

Groups configuration providers that supply dynamic routers, middlewares, and services.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

A provider controls live routing configuration; protect its source file and directory.

<a id="providers-file"></a>
## `providers.file`

### Short description

Configures the on-disk dynamic configuration provider.

### Syntax

```text
providers.file: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik File Provider mapping | filename and watch child fields | no |

### Default

No connector-owned file provider default is declared; the selected template sets the adjacent traefik-dynamic.yaml file.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Loads the router/middleware configuration that exposes the native lifecycle path or compatibility request path.

Configures the on-disk dynamic configuration provider.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

The dynamic file can alter routes and middleware; grant write access only to trusted operators.

<a id="providers-file-filename"></a>
## `providers.file.filename`

### Short description

Selects the companion dynamic file containing routers, middleware, and upstream service definitions.

### Syntax

```text
providers.file.filename: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik File Provider path string | readable dynamic-configuration path; selected relative path is ./traefik-dynamic.yaml | no |

### Default

No connector-owned dynamic file path default is declared; the selected template sets ./traefik-dynamic.yaml.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Supplies the routing configuration that attaches native P1–P4 middleware or compatibility P1 authorization.

Selects the companion dynamic file containing routers, middleware, and upstream service definitions.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `"./traefik-dynamic.yaml"`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

A relative path resolves from the host configuration context; deploy the matching file together and protect it from untrusted writes.

<a id="providers-file-watch"></a>
## `providers.file.watch`

### Short description

Controls whether Traefik watches the dynamic file for reloads after initial load.

### Syntax

```text
providers.file.watch: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik File Provider boolean | true \| false | no |

### Default

No connector-owned File Provider watch behavior default is declared; the selected template sets false.

Source: `selected Traefik example; no connector-owned Traefik host default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Dynamic lifecycle configuration reload control; it does not itself change per-request P1–P4 visibility.

Controls whether Traefik watches the dynamic file for reloads after initial load.

### Validation and errors

traefik check --configFile=<static-config>; load the selected File Provider configuration.

### Example

Selected example value: `false`.

Source-backed example: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Safety and operations

watch=true makes future file writes live configuration changes; selected native file uses false, compatibility example uses true.

<a id="compatibility-forwardauth-dynamic-http"></a>
## `compatibility.forwardauth-dynamic.http`

### Short description

Groups the request router, middleware attachment, and upstream service used by the example. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic HTTP configuration mapping | routers, middlewares, and services child mappings | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups the request router, middleware attachment, and upstream service used by the example. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

This topology controls which requests reach the engine and which upstream receives them; protect dynamic configuration writes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-middlewares"></a>
## `compatibility.forwardauth-dynamic.http.middlewares`

### Short description

Groups middleware definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic middleware registry mapping | named middleware mappings; selected key is modsecurity-auth | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups middleware definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Middleware definitions are policy attachment points; unreviewed changes can remove or replace inspection. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth`

### Short description

Binds the router-visible middleware name to its plugin or forwardAuth configuration. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik named middleware mapping | one forwardAuth compatibility middleware configuration mapping | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Binds the router-visible middleware name to its plugin or forwardAuth configuration. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

The router reference must continue to point to this reviewed middleware name to avoid bypass. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth`

### Short description

Groups the request-only external authorization service settings. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik ForwardAuth middleware mapping (compatibility only) | address and trustForwardHeader child fields | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups the request-only external authorization service settings. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Do not present forwardAuth as the native UDS rule-evaluating path; its service receives request authorization data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-address"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address`

### Short description

Targets the external forwardAuth decision service before the app service is contacted. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik ForwardAuth HTTP URL string (compatibility only) | absolute HTTP/HTTPS authorization-service URL; selected value is http://127.0.0.1:9000/authorize | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "http://127.0.0.1:9000/authorize".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Targets the external forwardAuth decision service before the app service is contacted. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `"http://127.0.0.1:9000/authorize"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Use a trusted, private service and do not embed credentials in the URL; it is distinct from the native UDS engine. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-trustforwardheader"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader`

### Short description

Controls whether forwarded request headers are trusted when calling the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik ForwardAuth boolean (compatibility only) | true \| false | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures false.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Controls whether forwarded request headers are trusted when calling the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `false`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

false avoids trusting client-supplied forwarded identity/route headers by default; deploy explicit proxy trust boundaries if changing it. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers"></a>
## `compatibility.forwardauth-dynamic.http.routers`

### Short description

Groups dynamic request-routing definitions. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic router registry mapping | named router mappings; selected key is app | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups dynamic request-routing definitions. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Router rules and middleware order are enforcement-relevant; avoid unaudited route additions. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app"></a>
## `compatibility.forwardauth-dynamic.http.routers.app`

### Short description

Binds a request rule and entry point to the listed middleware and app service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic Router mapping | rule, entryPoints, middlewares, and service child fields | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Binds a request rule and entry point to the listed middleware and app service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

The router is the attachment point for the native UDS middleware or compatibility forwardAuth; removing it bypasses that path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app-entrypoints"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.entryPoints`

### Short description

Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.entryPoints: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik router entry-point name list | defined static entry-point names | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["web"].

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `["web"]`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Binding a router to a public entry point exposes its middleware/service path to that listener's clients. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app-entrypoints"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]`

### Short description

Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik entry-point name string | name declared under static entryPoints; selected value is web | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "web".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `"web"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Binding a router to a public entry point exposes its middleware/service path to that listener's clients. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app-middlewares"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.middlewares`

### Short description

Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.middlewares: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ordered Traefik middleware-name list | names declared under http.middlewares | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["modsecurity-auth"].

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `["modsecurity-auth"]`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app-middlewares"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]`

### Short description

Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.middlewares[]: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik middleware-name string | selected compatibility forwardAuth middleware name | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "modsecurity-auth".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `"modsecurity-auth"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app-rule"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.rule`

### Short description

Matches incoming requests to the app router. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.rule: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik router-rule expression string | Traefik rule DSL; selected value is PathPrefix(`/`) | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "PathPrefix(`/`)".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Selects requests that enter the attached native middleware P1/P2 path or compatibility P1 authorization path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Matches incoming requests to the app router. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: ``"PathPrefix(`/`)"``.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

The selected catch-all rule routes every path on the entry point; narrow it in a real deployment if required. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-routers-app-service"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.service`

### Short description

Selects the upstream service after router middleware completes. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.service: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik service-name string | name declared under http.services; selected value is app | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "app".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Forwarding occurs after request-side middleware; the native path can observe the returned response at P3/P4. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Selects the upstream service after router middleware completes. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `"app"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

The target service URL is an egress destination; review it separately from middleware selection. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-services"></a>
## `compatibility.forwardauth-dynamic.http.services`

### Short description

Groups upstream service definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik dynamic service registry mapping | named service mappings; selected key is app | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The native middleware can receive the app response at P3/P4 after this service returns it; compatibility forwardAuth cannot. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups upstream service definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Services define request destinations after middleware; review their endpoint URLs and credentials. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-services-app"></a>
## `compatibility.forwardauth-dynamic.http.services.app`

### Short description

Binds the router's app service name to its load balancer. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik named service mapping | loadBalancer child mapping | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Upstream service stage after request middleware; native response callbacks can observe returned headers/body at P3/P4. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Binds the router's app service name to its load balancer. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

This mapping is an upstream routing target; do not confuse it with the ModSecurity engine service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-services-app-loadbalancer"></a>
## `compatibility.forwardauth-dynamic.http.services.app.loadBalancer`

### Short description

Groups the upstream server endpoints for the app service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app.loadBalancer: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik LoadBalancer service mapping | servers child list | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

After request middleware, the selected server response is available to native P3/P4 callbacks; not to compatibility forwardAuth. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups the upstream server endpoints for the app service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Each server URL is a traffic destination; limit it to the intended upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers"></a>
## `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers`

### Short description

Defines the endpoint candidates for the app load balancer. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Traefik load-balancer server mapping | one or more server URL mappings; selected example has one server | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Native response lifecycle P3/P4 begins only after the selected server responds; compatibility forwardAuth remains request-only. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Defines the endpoint candidates for the app load balancer. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Adding a server adds an upstream destination; review network scope and transport security. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers-url"></a>
## `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url`

### Short description

Targets the application server that receives requests after router middleware. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-dynamic)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik upstream server URL string | absolute backend URL; selected value is http://127.0.0.1:8081 | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "http://127.0.0.1:8081".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The returned upstream response is the native middleware's P3/P4 source; forwardAuth compatibility has no later response visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Targets the application server that receives requests after router middleware. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `"http://127.0.0.1:8081"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Loopback keeps the example local; remote URLs require explicit TLS, identity, and egress controls. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-accesslog"></a>
## `compatibility.forwardauth-static.accessLog`

### Short description

Enables/configures the Traefik access-log surface in the selected static example. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.accessLog: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik access-log configuration mapping | empty mapping or documented access-log fields; selected value is {} | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures {}.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Host observability only; it does not substitute for transaction P1–P4 processing or engine audit logging. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Enables/configures the Traefik access-log surface in the selected static example. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `{}`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

Access logs can contain request metadata; configure safe storage, rotation, and privacy controls for deployment. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-entrypoints"></a>
## `compatibility.forwardauth-static.entryPoints`

### Short description

Groups named listener definitions used by dynamic routers. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.entryPoints: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik static entry-point mapping | named entry-point mappings; selected key is web | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Static listener bootstrap; its named entry point selects which requests can reach the router/middleware lifecycle. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups named listener definitions used by dynamic routers. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

Entry-point addresses define the pre-policy network exposure of Traefik. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-entrypoints-web"></a>
## `compatibility.forwardauth-static.entryPoints.web`

### Short description

Defines the named web listener that dynamic routers attach to. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.entryPoints.web: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik EntryPoint mapping | address child field; selected entry point is web | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Static entry point for the router; the native middleware begins after request routing selects it. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Defines the named web listener that dynamic routers attach to. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

Changing this listener changes client reachability before middleware enforcement. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-entrypoints-web-address"></a>
## `compatibility.forwardauth-static.entryPoints.web.address`

### Short description

Binds the named web entry point used by the example router. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.entryPoints.web.address: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik listener address string | Traefik entry-point address such as host:port or :port; selected value is :8080 | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ":8080".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Listener bootstrap before router selection and the attached native P1–P4 middleware path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Binds the named web entry point used by the example router. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `":8080"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

The selected :8080 form changes listener exposure according to host networking; use a private bind or explicit edge control as appropriate. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-log"></a>
## `compatibility.forwardauth-static.log`

### Short description

Groups Traefik process-log settings. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.log: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik log configuration mapping | level child field | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Host observability only; no direct P1–P4 payload visibility change. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups Traefik process-log settings. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

Logs can contain request and operational metadata; choose retention and access controls separately. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-log-level"></a>
## `compatibility.forwardauth-static.log.level`

### Short description

Controls Traefik process-log verbosity. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.log.level: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik log-level token | Traefik-supported level token; selected value is INFO | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures INFO.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Host observability only; it does not change native or compatibility lifecycle callbacks. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Controls Traefik process-log verbosity. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `INFO`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

Debug logging can expose more operational metadata; do not equate host logs with ModSecurity audit output. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-providers"></a>
## `compatibility.forwardauth-static.providers`

### Short description

Groups configuration providers that supply dynamic routers, middlewares, and services. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.providers: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik static provider registry mapping | file provider child mapping | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Static-to-dynamic handoff; it makes the router/middleware lifecycle available but does not process a transaction itself. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Groups configuration providers that supply dynamic routers, middlewares, and services. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

A provider controls live routing configuration; protect its source file and directory. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-providers-file"></a>
## `compatibility.forwardauth-static.providers.file`

### Short description

Configures the on-disk dynamic configuration provider. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.providers.file: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik File Provider mapping | filename and watch child fields | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Loads the router/middleware configuration that exposes the native lifecycle path or compatibility request path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Configures the on-disk dynamic configuration provider. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

The dynamic file can alter routes and middleware; grant write access only to trusted operators. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-providers-file-filename"></a>
## `compatibility.forwardauth-static.providers.file.filename`

### Short description

Selects the companion dynamic file containing routers, middleware, and upstream service definitions. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.providers.file.filename: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik File Provider path string | readable dynamic-configuration path; selected relative path is ./traefik-dynamic.yaml | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "./traefik-dynamic.yaml".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Supplies the routing configuration that attaches native P1–P4 middleware or compatibility P1 authorization. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Selects the companion dynamic file containing routers, middleware, and upstream service definitions. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `"./traefik-dynamic.yaml"`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

A relative path resolves from the host configuration context; deploy the matching file together and protect it from untrusted writes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="compatibility-forwardauth-static-providers-file-watch"></a>
## `compatibility.forwardauth-static.providers.file.watch`

### Short description

Controls whether Traefik watches the dynamic file for reloads after initial load. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.forwardauth-static.providers.file.watch: <value>
```

### Valid contexts

- Compatibility YAML path only (forwardauth-static)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik File Provider boolean | true \| false | no |

### Default

Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures true.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Dynamic lifecycle configuration reload control; it does not itself change per-request P1–P4 visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.

Controls whether Traefik watches the dynamic file for reloads after initial load. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as a Traefik forwardAuth compatibility configuration.

### Example

Selected example value: `true`.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Safety and operations

watch=true makes future file writes live configuration changes; selected native file uses false, compatibility example uses true. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

<a id="forwardauth"></a>
## `forwardAuth`

### Short description

Compatibility-only forwardAuth middleware.

### Syntax

```text
forwardAuth: { address: <url>, trustForwardHeader: <bool> }
```

### Valid contexts

- Compatibility dynamic middleware

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Traefik compatibility middleware | forwardAuth fields in the compatibility example | no |

### Default

not part of selected native middleware path

Source: `compatibility template`.

### Inheritance and merge

not part of native middleware

Merge: not part of native middleware

### Phases and runtime effect

Request-authorization compatibility path; no selected P3/P4 configuration.

Routes to separate authorization service.

### Validation and errors

Separate Traefik compatibility configuration validation.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Safety and operations

Do not present forwardAuth as the native UDS rule-evaluating path.
