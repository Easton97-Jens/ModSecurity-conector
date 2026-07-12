# Envoy configuration reference

**Language:** English | [Deutsch](configuration-reference.de.md)

## Scope and source of truth

Selected integration mode: `ext-proc`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.
Compatibility entries are explicitly labelled and are not part of the selected core path.

## Configuration inventory

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`--check-config`](#check-config) | Environment / runtime | CLI flag | no | optional | msconnector_envoy_ext_proc command line | ext_proc service CLI flag. |
| [`--config`](#config) | Environment / runtime | CLI flag | yes | required | msconnector_envoy_ext_proc command line | ext_proc service CLI flag. |
| [`--event-log`](#event-log) | Environment / runtime | CLI flag | no | optional | msconnector_envoy_ext_proc command line | ext_proc service CLI flag. |
| [`--listen`](#listen) | Environment / runtime | CLI flag | no | optional | msconnector_envoy_ext_proc command line | ext_proc service CLI flag. |
| [`--runtime-config`](#runtime-config) | Environment / runtime | CLI flag | no | optional | msconnector_envoy_ext_proc command line | ext_proc service CLI flag. |
| [`@ADMIN_PORT@`](#admin-port) | Example placeholder | template placeholder | yes | none; must be materialized | Envoy YAML template before materialization | Template placeholder, not an Envoy configuration field. |
| [`@ENVOY_RELEASE@`](#envoy-release) | Example placeholder | template placeholder | yes | none; must be materialized | Envoy YAML template before materialization | Template placeholder, not an Envoy configuration field. |
| [`@EXT_PROC_PORT@`](#ext-proc-port) | Example placeholder | template placeholder | yes | none; must be materialized | Envoy YAML template before materialization | Template placeholder, not an Envoy configuration field. |
| [`@LISTEN_PORT@`](#listen-port) | Example placeholder | template placeholder | yes | none; must be materialized | Envoy YAML template before materialization | Template placeholder, not an Envoy configuration field. |
| [`@UPSTREAM_PORT@`](#upstream-port) | Example placeholder | template placeholder | yes | none; must be materialized | Envoy YAML template before materialization | Template placeholder, not an Envoy configuration field. |
| [`admin`](#admin) | Host / Connector | Envoy Admin mapping | no | No connector-owned admin configuration default is declared; the selected template sets a loopback listener with /dev/null access log. | The YAML object path shown in the selected example. | Groups Envoy management-interface configuration. |
| [`admin.access_log_path`](#admin-access-log-path) | Host / Connector | filesystem path string | no | No connector-owned admin access-log path default is declared; the selected template sets /dev/null. | The YAML object path shown in the selected example. | Selects where Envoy writes administrative HTTP access records. |
| [`admin.address`](#admin-address) | Host / Connector | Envoy admin core.Address mapping | no | No connector-owned admin address default is declared; the selected template sets 127.0.0.1 and @ADMIN_PORT@. | The YAML object path shown in the selected example. | Groups the Envoy administration listener address. |
| [`admin.address.socket_address`](#admin-address-socket-address) | Host / Connector | Envoy admin SocketAddress mapping | no | No connector-owned admin socket-address default is declared; the selected template sets 127.0.0.1 plus @ADMIN_PORT@. | The YAML object path shown in the selected example. | Pairs the Envoy administration host and TCP port. |
| [`admin.address.socket_address.address`](#admin-address-socket-address-address) | Host / Connector | Envoy admin host/IP string | no | No connector-owned admin host default is declared; the selected template sets 127.0.0.1. | The YAML object path shown in the selected example. | Binds the Envoy administration listener to the selected interface. |
| [`admin.address.socket_address.port_value`](#admin-address-socket-address-port-value) | Host / Connector | Envoy admin uint32 TCP port | no | No connector-owned admin port default is declared; the selected template sets the @ADMIN_PORT@ materializer input. | The YAML object path shown in the selected example. | Selects the local TCP port for Envoy administration endpoints. |
| [`cleanup_timeout_ms`](#cleanup-timeout-ms) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`engine_timeout_ms`](#engine-timeout-ms) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`late_action_policy`](#late-action-policy) | Connector service | LateActionPolicy | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Selects late decision reporting; minimal and safe record late disruptive decisions as log_only, while strict records strict_abort_not_attempted rather than a fabricated status/reset. |
| [`listen_address`](#listen-address) | Connector service | string | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_body_chunk_bytes`](#max-body-chunk-bytes) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_grpc_message_bytes`](#max-grpc-message-bytes) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_header_count`](#max-header-count) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_header_name_bytes`](#max-header-name-bytes) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_header_value_bytes`](#max-header-value-bytes) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_request_body_bytes`](#max-request-body-bytes) | Connector service | int64 | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_response_body_bytes`](#max-response-body-bytes) | Connector service | int64 | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`max_total_header_bytes`](#max-total-header-bytes) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`shutdown_timeout_ms`](#shutdown-timeout-ms) | Connector service | int | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`static_resources`](#static-resources) | Host / Connector | Envoy Bootstrap static_resources mapping | no | No connector-owned static-resource set default is declared; the selected template sets the explicit listener and static clusters. | The YAML object path shown in the selected example. | Declares the complete static data-plane topology used by the checked-in example. |
| [`static_resources.clusters`](#static-resources-clusters) | Host / Connector | repeated Envoy Cluster mapping | no | No connector-owned cluster list default is declared; the selected template sets the explicit upstream and local processor clusters. | The YAML object path shown in the selected example. | Declares the static service destinations used by routing and ext_proc gRPC. |
| [`static_resources.clusters[].connect_timeout`](#static-resources-clusters-connect-timeout) | Host / Connector | Envoy protobuf Duration for cluster connection attempts | no | No connector-owned cluster connect timeout default is declared; the selected template sets the explicit template duration. | The YAML object path shown in the selected example. | Bounds TCP connection establishment to the upstream or local processor endpoint. |
| [`static_resources.clusters[].http2_protocol_options`](#static-resources-clusters-http2-protocol-options) | Host / Connector | Envoy Http2ProtocolOptions mapping | no | Absent unless configured; the selected ext_proc cluster explicitly sets an empty HTTP/2 options mapping. | The YAML object path shown in the selected example. | Enables the HTTP/2 protocol options needed by the Envoy gRPC ext_proc cluster. |
| [`static_resources.clusters[].load_assignment`](#static-resources-clusters-load-assignment) | Host / Connector | Envoy ClusterLoadAssignment mapping | no | No connector-owned static load assignment default is declared; the selected template sets the explicit loopback endpoint set. | The YAML object path shown in the selected example. | Groups the endpoints assigned to a static cluster. |
| [`static_resources.clusters[].load_assignment.cluster_name`](#static-resources-clusters-load-assignment-cluster-name) | Host / Connector | Envoy ClusterLoadAssignment.cluster_name string | no | No connector-owned load-assignment cluster name default is declared; the selected template sets the enclosing static cluster name. | The YAML object path shown in the selected example. | Associates the endpoint assignment with its enclosing cluster. |
| [`static_resources.clusters[].load_assignment.endpoints`](#static-resources-clusters-load-assignment-endpoints) | Host / Connector | repeated Envoy LocalityLbEndpoints mapping | no | No connector-owned endpoint-group list default is declared; the selected template sets one loopback locality group. | The YAML object path shown in the selected example. | Groups load-balanced endpoints for the static cluster. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints) | Host / Connector | repeated Envoy LbEndpoint mapping | no | No connector-owned load-balancer endpoint list default is declared; the selected template sets one explicit loopback endpoint. | The YAML object path shown in the selected example. | Defines endpoint candidates selected by Envoy's cluster load balancer. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint) | Host / Connector | Envoy Endpoint mapping | no | No connector-owned endpoint object default is declared; the selected template sets the explicit loopback socket address. | The YAML object path shown in the selected example. | Contains the network address of one cluster endpoint. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address) | Host / Connector | Envoy core.Address mapping | no | No connector-owned cluster endpoint address default is declared; the selected template sets a loopback socket_address mapping. | The YAML object path shown in the selected example. | Contains the TCP address for one upstream or ext_proc service endpoint. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address) | Host / Connector | Envoy core.SocketAddress mapping | no | No connector-owned cluster endpoint socket-address default is declared; the selected template sets 127.0.0.1 plus its materialized port. | The YAML object path shown in the selected example. | Pairs the static cluster endpoint host and TCP port. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-address) | Host / Connector | Envoy SocketAddress host/IP string | no | No connector-owned cluster endpoint host default is declared; the selected template sets 127.0.0.1. | The YAML object path shown in the selected example. | Targets the static upstream or ext_proc endpoint host. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-port-value) | Host / Connector | Envoy SocketAddress uint32 TCP port | no | No connector-owned cluster endpoint port default is declared; the selected template sets the @UPSTREAM_PORT@ or @EXT_PROC_PORT@ materializer input. | The YAML object path shown in the selected example. | Targets the TCP port of the selected upstream or ext_proc endpoint. |
| [`static_resources.clusters[].name`](#static-resources-clusters-name) | Host / Connector | Envoy Cluster.name string | no | No connector-owned cluster-name default is declared; the selected template sets the two named static clusters. | The YAML object path shown in the selected example. | Names a static endpoint group referenced by the route or ext_proc gRPC service. |
| [`static_resources.clusters[].type`](#static-resources-clusters-type) | Host / Connector | Envoy Cluster DiscoveryType enum | no | No connector-owned cluster discovery type default is declared; the selected template sets STATIC for the selected native local endpoints. | The YAML object path shown in the selected example. | Determines how Envoy resolves the endpoint set for the named cluster. |
| [`static_resources.listeners`](#static-resources-listeners) | Host / Connector | repeated Envoy Listener mapping | no | No connector-owned listener list default is declared; the selected template sets one msconnector_ext_proc_listener. | The YAML object path shown in the selected example. | Declares the downstream listener objects present in the static bootstrap. |
| [`static_resources.listeners[].address`](#static-resources-listeners-address) | Host / Connector | Envoy core.Address mapping | no | No connector-owned listener-address default is declared; the selected template sets a loopback socket_address mapping. | The YAML object path shown in the selected example. | Contains the downstream listener bind address used before the HTTP filter chain runs. |
| [`static_resources.listeners[].address.socket_address`](#static-resources-listeners-address-socket-address) | Host / Connector | Envoy core.SocketAddress mapping | no | No connector-owned listener socket-address default is declared; the selected template sets 127.0.0.1 and @LISTEN_PORT@. | The YAML object path shown in the selected example. | Pairs the listener host and TCP port that accept downstream traffic. |
| [`static_resources.listeners[].address.socket_address.address`](#static-resources-listeners-address-socket-address-address) | Host / Connector | Envoy SocketAddress host/IP string | no | No connector-owned listener host default is declared; the selected template sets 127.0.0.1. | The YAML object path shown in the selected example. | Binds the downstream HTTP listener to the selected network interface. |
| [`static_resources.listeners[].address.socket_address.port_value`](#static-resources-listeners-address-socket-address-port-value) | Host / Connector | Envoy SocketAddress uint32 TCP port | no | No connector-owned listener port default is declared; the selected template sets the @LISTEN_PORT@ materializer input. | The YAML object path shown in the selected example. | Selects the TCP port on which downstream requests enter the ext_proc filter chain. |
| [`static_resources.listeners[].filter_chains`](#static-resources-listeners-filter-chains) | Host / Connector | repeated Envoy Listener.FilterChain mapping | no | No connector-owned filter-chain set default is declared; the selected template sets one chain containing the HTTP connection manager. | The YAML object path shown in the selected example. | Defines the network-filter sequence applied to accepted downstream connections. |
| [`static_resources.listeners[].filter_chains[].filters`](#static-resources-listeners-filter-chains-filters) | Host / Connector | repeated Envoy NetworkFilter mapping | no | No connector-owned network-filter list default is declared; the selected template sets the HCM filter. | The YAML object path shown in the selected example. | Installs the HTTP connection manager that owns routing and the nested ext_proc HTTP filter chain. |
| [`static_resources.listeners[].filter_chains[].filters[].name`](#static-resources-listeners-filter-chains-filters-name) | Host / Connector | Envoy NetworkFilter factory name | no | No connector-owned network-filter factory default is declared; the selected template sets the HTTP connection manager factory name. | The YAML object path shown in the selected example. | Selects Envoy's HTTP connection manager implementation for the listener. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config`](#static-resources-listeners-filter-chains-filters-typed-config) | Host / Connector | google.protobuf.Any mapping for HttpConnectionManager | no | No connector-owned HCM typed configuration default is declared; the selected template sets the explicit HttpConnectionManager payload. | The YAML object path shown in the selected example. | Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.@type`](#static-resources-listeners-filter-chains-filters-typed-config-type) | Host / Connector | protobuf Any type URL string | no | No connector-owned HCM Any type default is declared; the selected template sets the explicit v3 HttpConnectionManager URL. | The YAML object path shown in the selected example. | Lets Envoy decode the surrounding typed_config as an HTTP connection manager. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters) | Host / Connector | ordered repeated Envoy HTTP filter mapping | no | No connector-owned HTTP-filter chain default is declared; the selected template sets ext_proc then router ordered pair. | The YAML object path shown in the selected example. | Orders HTTP processing: ext_proc runs before the router forwards upstream. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-name) | Host / Connector | Envoy HTTP filter factory-name string | no | No connector-owned HTTP-filter factories default is declared; the selected template sets the ext_proc/router ordered pair. | The YAML object path shown in the selected example. | Selects the ext_proc policy filter and terminal router implementations in the HCM chain. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config) | Host / Connector | repeated google.protobuf.Any HTTP-filter configuration mapping | no | No connector-owned HTTP typed configurations default is declared; the selected template sets the explicit ExternalProcessor and Router payloads. | The YAML object path shown in the selected example. | Holds the per-filter configuration corresponding to each HTTP filter item. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-type) | Host / Connector | protobuf Any type URL string | no | No connector-owned HTTP Any type URLs default is declared; the selected template sets the explicit ExternalProcessor and Router v3 URLs. | The YAML object path shown in the selected example. | Lets Envoy decode each HTTP filter's typed configuration. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-allow-mode-override) | Host / Connector | Envoy ext_proc boolean | no | Envoy proto default false; the selected template explicitly sets false. | The YAML object path shown in the selected example. | Allows or ignores a processor-supplied mode_override that would change processing_mode after request headers. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-failure-mode-allow) | Host / Connector | Envoy ext_proc boolean | no | Envoy proto default false; the selected template explicitly sets false. | The YAML object path shown in the selected example. | Chooses whether processor stream errors/timeouts fail open (true) or produce Envoy's error handling (false). |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service) | Host / Connector | Envoy GrpcService mapping | no | No connector-owned ext_proc gRPC service default is declared; the selected template sets the msconnector_ext_proc envoy_grpc target. | The YAML object path shown in the selected example. | Names the bidirectional gRPC side stream used by the ExternalProcessor filter. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service-envoy-grpc) | Host / Connector | EnvoyGrpc cluster-reference mapping | no | No connector-owned Envoy gRPC target default is declared; the selected template sets the msconnector_ext_proc cluster reference. | The YAML object path shown in the selected example. | Uses Envoy-managed gRPC transport rather than an inline URI for the external processor. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service-envoy-grpc-cluster-name) | Host / Connector | Envoy cluster-name string | no | No connector-owned ext_proc service cluster default is declared; the selected template sets msconnector_ext_proc. | The YAML object path shown in the selected example. | Binds ExternalProcessor gRPC traffic to the local ext_proc cluster. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service-timeout) | Host / Connector | Envoy protobuf Duration | no | No connector-owned gRPC service timeout default is declared; the selected template sets 0.2s. | The YAML object path shown in the selected example. | Bounds service establishment/operation as configured on the ext_proc gRPC service reference. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-max-message-timeout) | Host / Connector | Envoy protobuf Duration maximum override timeout | no | Envoy default is 0, which disables the processor override_message_timeout API; the selected template permits overrides up to 0.25s. | The YAML object path shown in the selected example. | Caps a processor-requested extension of the per-message timeout. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-message-timeout) | Host / Connector | Envoy protobuf Duration per ext_proc message | no | Envoy ext_proc default 200 milliseconds when omitted; the selected template explicitly sets 0.2s. | The YAML object path shown in the selected example. | Limits how long Envoy waits for each required external-processor response. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode) | Host / Connector | Envoy ext_proc ProcessingMode mapping | no | Envoy defaults send request/response headers, skip trailers, and send no bodies; this template overrides every selected lifecycle field. | The YAML object path shown in the selected example. | Groups the ext_proc visibility controls for request/response headers, bodies, and trailers. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-request-body-mode) | Host / Connector | Envoy ext_proc BodySendMode enum | no | Envoy proto default NONE; the selected template explicitly sets STREAMED. | The YAML object path shown in the selected example. | Selects request/P2 body delivery to ext_proc; STREAMED sends incremental body chunks. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-request-header-mode) | Host / Connector | Envoy ext_proc HeaderSendMode enum | no | Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND. | The YAML object path shown in the selected example. | Selects whether request/P1 headers are sent to the external processor. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-request-trailer-mode) | Host / Connector | Envoy ext_proc HeaderSendMode enum for trailers | no | Envoy effective default SKIP for trailers; the selected template explicitly sets SEND. | The YAML object path shown in the selected example. | Sends request trailers/EOS metadata to the external processor when trailers are present. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-response-body-mode) | Host / Connector | Envoy ext_proc BodySendMode enum | no | Envoy proto default NONE; the selected template explicitly sets STREAMED. | The YAML object path shown in the selected example. | Selects response/P4 body delivery to ext_proc; STREAMED sends incremental body chunks. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-response-header-mode) | Host / Connector | Envoy ext_proc HeaderSendMode enum | no | Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND. | The YAML object path shown in the selected example. | Selects whether response/P3 headers are sent to the external processor. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-response-trailer-mode) | Host / Connector | Envoy ext_proc HeaderSendMode enum for trailers | no | Envoy effective default SKIP for trailers; the selected template explicitly sets SEND. | The YAML object path shown in the selected example. | Sends response trailers/EOS metadata to the external processor when trailers are present. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-request-attributes) | Host / Connector | repeated Envoy request-attribute name list | no | Absent list requests no additional attributes; this template explicitly requests five attributes used by processor.requestMetadataFromEnvoy. | The YAML object path shown in the selected example. | Requests concrete peer/protocol metadata for the ext_proc ProcessingRequest attributes map. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-request-attributes) | Host / Connector | Envoy request-attribute path string | no | No additional attribute is requested when omitted; this template explicitly requests all five metadata paths consumed by requestMetadataFromEnvoy. | The YAML object path shown in the selected example. | Makes protocol and client/server endpoint metadata available to the ext_proc processor's request-metadata mapper. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-send-body-without-waiting-for-header-response) | Host / Connector | Envoy ext_proc boolean | no | Envoy proto default false; the selected template explicitly sets false. | The YAML object path shown in the selected example. | When true with STREAMED bodies, Envoy sends body chunks before the processor's header response; false retains header-response ordering. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`](#static-resources-listeners-filter-chains-filters-typed-config-route-config) | Host / Connector | Envoy RouteConfiguration mapping | no | No connector-owned inline route configuration default is declared; the selected template sets msconnector_ext_proc_route. | The YAML object path shown in the selected example. | Defines the route lookup that selects the upstream after request-side filters run. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-name) | Host / Connector | Envoy RouteConfiguration.name string | no | No connector-owned route-config name default is declared; the selected template sets msconnector_ext_proc_route. | The YAML object path shown in the selected example. | Names the inline route configuration for Envoy diagnostics and references. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts) | Host / Connector | repeated Envoy VirtualHost mapping | no | No connector-owned virtual-host list default is declared; the selected template sets one local_service entry. | The YAML object path shown in the selected example. | Groups host/domain matches and routes for the HCM. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Host / Connector | repeated Envoy VirtualHost domain matcher | no | No connector-owned virtual-host domain matcher default is declared; the selected template sets the catch-all `*` pattern. | The YAML object path shown in the selected example. | Selects which Host/:authority values enter this virtual host's route list. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Host / Connector | Envoy VirtualHost domain-pattern string | no | No connector-owned virtual-host domain matcher default is declared; the selected template sets the catch-all `*` pattern. | The YAML object path shown in the selected example. | Selects which Host/:authority values enter this virtual host's route list. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-name) | Host / Connector | Envoy VirtualHost.name string | no | No connector-owned virtual-host name default is declared; the selected template sets local_service. | The YAML object path shown in the selected example. | Labels the virtual-host route group. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes) | Host / Connector | repeated Envoy Route mapping | no | No connector-owned route list default is declared; the selected template sets one `/` prefix route to upstream_service. | The YAML object path shown in the selected example. | Contains ordered route matching and upstream actions for the virtual host. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match) | Host / Connector | Envoy RouteMatch mapping | no | No connector-owned RouteMatch mapping default is declared; the selected template sets the explicit `/` prefix and upstream_service action. | The YAML object path shown in the selected example. | Groups the prefix matcher for the selected route. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-prefix) | Host / Connector | Envoy RouteMatch prefix string | no | No connector-owned route prefix default is declared; the selected template sets the catch-all `/` prefix. | The YAML object path shown in the selected example. | Matches request paths for the selected route. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-route) | Host / Connector | Envoy RouteAction mapping | no | No connector-owned RouteAction mapping default is declared; the selected template sets the explicit `/` prefix and upstream_service action. | The YAML object path shown in the selected example. | Groups the cluster action selected after the route match. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-route-cluster) | Host / Connector | Envoy RouteAction cluster-name string | no | No connector-owned route cluster target default is declared; the selected template sets upstream_service. | The YAML object path shown in the selected example. | Routes matching downstream requests to the named upstream cluster. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`](#static-resources-listeners-filter-chains-filters-typed-config-stat-prefix) | Host / Connector | HttpConnectionManager statistics-prefix string | no | No connector-owned HCM statistic prefix default is declared; the selected template sets msconnector_ext_proc_ingress. | The YAML object path shown in the selected example. | Prefixes HCM metrics for the selected ingress listener. |
| [`static_resources.listeners[].name`](#static-resources-listeners-name) | Host / Connector | Envoy Listener.name string | no | No connector-owned listener-name default is declared; the selected template sets `msconnector_ext_proc_listener`. | The YAML object path shown in the selected example. | Names the downstream HTTP listener for Envoy configuration and observability. |
| [`transaction_id_header`](#transaction-id-header) | Connector service | string | yes | none; JSON decoder/Config.Validate requires every selected field | ext_proc service JSON object | Sets one bounded ext_proc service control. |
| [`compatibility.ext_authz.static_resources`](#compatibility-ext-authz-static-resources) | Compatibility | Envoy Bootstrap static_resources mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Declares the complete static data-plane topology used by the checked-in example. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters`](#compatibility-ext-authz-static-resources-clusters) | Compatibility | repeated Envoy Cluster mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Declares the static service destinations used by routing and ext_proc gRPC. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].connect_timeout`](#compatibility-ext-authz-static-resources-clusters-connect-timeout) | Compatibility | Envoy protobuf Duration for cluster connection attempts | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.25s. | Compatibility YAML path only (ext_authz) | Bounds TCP connection establishment to the upstream or local processor endpoint. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment`](#compatibility-ext-authz-static-resources-clusters-load-assignment) | Compatibility | Envoy ClusterLoadAssignment mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups the endpoints assigned to a static cluster. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name`](#compatibility-ext-authz-static-resources-clusters-load-assignment-cluster-name) | Compatibility | Envoy ClusterLoadAssignment.cluster_name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz, app_backend. | Compatibility YAML path only (ext_authz) | Associates the endpoint assignment with its enclosing cluster. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints) | Compatibility | repeated Envoy LocalityLbEndpoints mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups load-balanced endpoints for the static cluster. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints) | Compatibility | repeated Envoy LbEndpoint mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Defines endpoint candidates selected by Envoy's cluster load balancer. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint) | Compatibility | Envoy Endpoint mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Contains the network address of one cluster endpoint. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address) | Compatibility | Envoy core.Address mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Contains the TCP address for one upstream or ext_proc service endpoint. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address) | Compatibility | Envoy core.SocketAddress mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { address: 127.0.0.1, port_value: 9000 }, { address: 127.0.0.1, port_value: 8081 }. | Compatibility YAML path only (ext_authz) | Pairs the static cluster endpoint host and TCP port. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-address) | Compatibility | Envoy SocketAddress host/IP string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 127.0.0.1. | Compatibility YAML path only (ext_authz) | Targets the static upstream or ext_proc endpoint host. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-port-value) | Compatibility | Envoy SocketAddress uint32 TCP port | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 9000, 8081. | Compatibility YAML path only (ext_authz) | Targets the TCP port of the selected upstream or ext_proc endpoint. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].name`](#compatibility-ext-authz-static-resources-clusters-name) | Compatibility | Envoy Cluster.name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz, app_backend. | Compatibility YAML path only (ext_authz) | Names a static endpoint group referenced by the route or ext_proc gRPC service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.clusters[].type`](#compatibility-ext-authz-static-resources-clusters-type) | Compatibility | Envoy Cluster DiscoveryType enum | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures STRICT_DNS. | Compatibility YAML path only (ext_authz) | Determines how Envoy resolves the endpoint set for the named cluster. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners`](#compatibility-ext-authz-static-resources-listeners) | Compatibility | repeated Envoy Listener mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Declares the downstream listener objects present in the static bootstrap. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].address`](#compatibility-ext-authz-static-resources-listeners-address) | Compatibility | Envoy core.Address mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Contains the downstream listener bind address used before the HTTP filter chain runs. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].address.socket_address`](#compatibility-ext-authz-static-resources-listeners-address-socket-address) | Compatibility | Envoy core.SocketAddress mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { address: 0.0.0.0, port_value: 8080 }. | Compatibility YAML path only (ext_authz) | Pairs the listener host and TCP port that accept downstream traffic. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].address.socket_address.address`](#compatibility-ext-authz-static-resources-listeners-address-socket-address-address) | Compatibility | Envoy SocketAddress host/IP string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.0.0.0. | Compatibility YAML path only (ext_authz) | Binds the downstream HTTP listener to the selected network interface. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value`](#compatibility-ext-authz-static-resources-listeners-address-socket-address-port-value) | Compatibility | Envoy SocketAddress uint32 TCP port | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 8080. | Compatibility YAML path only (ext_authz) | Selects the TCP port on which downstream requests enter the ext_proc filter chain. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains`](#compatibility-ext-authz-static-resources-listeners-filter-chains) | Compatibility | repeated Envoy Listener.FilterChain mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Defines the network-filter sequence applied to accepted downstream connections. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters) | Compatibility | repeated Envoy NetworkFilter mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Installs the HTTP connection manager that owns routing and the nested ext_authz compatibility HTTP filter chain. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-name) | Compatibility | Envoy NetworkFilter factory name | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures envoy.filters.network.http_connection_manager. | Compatibility YAML path only (ext_authz) | Selects Envoy's HTTP connection manager implementation for the listener. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config) | Compatibility | google.protobuf.Any mapping for HttpConnectionManager | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-type) | Compatibility | protobuf Any type URL string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager. | Compatibility YAML path only (ext_authz) | Lets Envoy decode the surrounding typed_config as an HTTP connection manager. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters) | Compatibility | ordered repeated Envoy HTTP filter mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Orders HTTP processing: ext_authz runs before the router forwards upstream. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-name) | Compatibility | Envoy HTTP filter factory-name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures envoy.filters.http.ext_authz, envoy.filters.http.router. | Compatibility YAML path only (ext_authz) | Selects the ext_authz policy filter and terminal router implementations in the HCM chain. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config) | Compatibility | repeated google.protobuf.Any HTTP-filter configuration mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Holds the per-filter configuration corresponding to each HTTP filter item. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-type) | Compatibility | protobuf Any type URL string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router. | Compatibility YAML path only (ext_authz) | Lets Envoy decode each HTTP filter's typed configuration. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service) | Compatibility | Envoy ext_authz HTTP service mapping (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Configures the compatibility ext_authz-style HTTP service instead of the selected gRPC ext_proc service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request) | Compatibility | Envoy ext_authz AuthorizationRequest mapping (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups the header-forwarding policy for the compatibility authorization request. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request-allowed-headers) | Compatibility | Envoy HeaderMatcher list mapping (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request-allowed-headers-patterns) | Compatibility | Envoy HeaderMatcher list mapping (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request-allowed-headers-patterns-exact) | Compatibility | Envoy HeaderMatcher exact header-name string (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures authorization, content-type. | Compatibility YAML path only (ext_authz) | Forwards only matching request headers to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri) | Compatibility | Envoy HttpService.server_uri mapping (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups the compatibility service URI, logical cluster, and deadline. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri-cluster) | Compatibility | Envoy cluster-name string (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz. | Compatibility YAML path only (ext_authz) | Associates the HTTP authorization URI with its configured Envoy cluster. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri-timeout) | Compatibility | Envoy protobuf Duration (compatibility HTTP authorization timeout) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.2s. | Compatibility YAML path only (ext_authz) | Bounds one compatibility authorization HTTP request. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri-uri) | Compatibility | Envoy HTTP service URI string (compatibility only) | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures http://127.0.0.1:9000. | Compatibility YAML path only (ext_authz) | Identifies the HTTP authorization endpoint for compatibility ext_authz requests. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config) | Compatibility | Envoy RouteConfiguration mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Defines the route lookup that selects the upstream after request-side filters run. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-name) | Compatibility | Envoy RouteConfiguration.name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures local_route. | Compatibility YAML path only (ext_authz) | Names the inline route configuration for Envoy diagnostics and references. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts) | Compatibility | repeated Envoy VirtualHost mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Groups host/domain matches and routes for the HCM. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Compatibility | repeated Envoy VirtualHost domain matcher | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["*"]. | Compatibility YAML path only (ext_authz) | Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Compatibility | Envoy VirtualHost domain-pattern string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "*". | Compatibility YAML path only (ext_authz) | Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-name) | Compatibility | Envoy VirtualHost.name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures backend. | Compatibility YAML path only (ext_authz) | Labels the virtual-host route group. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes) | Compatibility | repeated Envoy Route mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file. | Compatibility YAML path only (ext_authz) | Contains ordered route matching and upstream actions for the virtual host. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match) | Compatibility | Envoy RouteMatch mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { prefix: "/" }. | Compatibility YAML path only (ext_authz) | Groups the prefix matcher for the selected route. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-prefix) | Compatibility | Envoy RouteMatch prefix string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "/". | Compatibility YAML path only (ext_authz) | Matches request paths for the selected route. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-route) | Compatibility | Envoy RouteAction mapping | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { cluster: app_backend }. | Compatibility YAML path only (ext_authz) | Groups the cluster action selected after the route match. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-route-cluster) | Compatibility | Envoy RouteAction cluster-name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures app_backend. | Compatibility YAML path only (ext_authz) | Routes matching downstream requests to the named upstream cluster. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-stat-prefix) | Compatibility | HttpConnectionManager statistics-prefix string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ingress_http. | Compatibility YAML path only (ext_authz) | Prefixes HCM metrics for the selected ingress listener. Compatibility-only host/service setup outside the selected native core path. |
| [`compatibility.ext_authz.static_resources.listeners[].name`](#compatibility-ext-authz-static-resources-listeners-name) | Compatibility | Envoy Listener.name string | no | Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures listener_0. | Compatibility YAML path only (ext_authz) | Names the downstream HTTP listener for Envoy configuration and observability. Compatibility-only host/service setup outside the selected native core path. |
| [`envoy.filters.http.ext_authz`](#envoy-filters-http-ext-authz) | Compatibility | Envoy compatibility filter | no | not part of selected ext_proc path | Compatibility Envoy HTTP filter chain | Compatibility-only ext_authz filter. |

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
| Minimal | [minimal/envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in) | Active starter configuration |
| Safe full lifecycle | [safe/envoy-ext-proc-streaming.yaml.in](safe/envoy-ext-proc-streaming.yaml.in) | Selected bounded reference |
| Strict | [strict/README.md](strict/README.md) | Parser-supported or explicitly optional boundary |
| DetectionOnly | [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Engine evaluates/logs without disruptive action |
| Disabled | [disabled/msconnector-runtime.conf](disabled/msconnector-runtime.conf) | Connector or engine path disabled |

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
envoy --mode validate -c <generated-config>
```

Repository targets: `make check-config-envoy` and `make check-config-all-connectors`.

## Option details

## `--check-config`

### Short description

ext_proc service CLI flag.

### Syntax

```text
--check-config
```

### Valid contexts

- msconnector_envoy_ext_proc command line

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| CLI flag | see CLI usage; path/host:port where applicable | no |

### Default

optional

Source: `main.go flag registration`.

### Inheritance and merge

not applicable

Merge: --listen overrides listen_address after JSON decoding; other flags are direct process inputs.

### Phases and runtime effect

Runtime service setup; --runtime-config selects the actual engine path.

Controls ext_proc service startup/check behavior.

### Validation and errors

main validates JSON and, where selected, Common Runtime before serving.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Safety and operations

Use absolute controlled paths for runtime/event files and a private service listener.

## `--config`

### Short description

ext_proc service CLI flag.

### Syntax

```text
--config PATH
```

### Valid contexts

- msconnector_envoy_ext_proc command line

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| CLI flag | see CLI usage; path/host:port where applicable | yes |

### Default

required

Source: `main.go flag registration`.

### Inheritance and merge

not applicable

Merge: --listen overrides listen_address after JSON decoding; other flags are direct process inputs.

### Phases and runtime effect

Runtime service setup; --runtime-config selects the actual engine path.

Controls ext_proc service startup/check behavior.

### Validation and errors

main validates JSON and, where selected, Common Runtime before serving.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Safety and operations

Use absolute controlled paths for runtime/event files and a private service listener.

## `--event-log`

### Short description

ext_proc service CLI flag.

### Syntax

```text
--event-log PATH
```

### Valid contexts

- msconnector_envoy_ext_proc command line

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| CLI flag | see CLI usage; path/host:port where applicable | no |

### Default

optional

Source: `main.go flag registration`.

### Inheritance and merge

not applicable

Merge: --listen overrides listen_address after JSON decoding; other flags are direct process inputs.

### Phases and runtime effect

Runtime service setup; --runtime-config selects the actual engine path.

Controls ext_proc service startup/check behavior.

### Validation and errors

main validates JSON and, where selected, Common Runtime before serving.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Safety and operations

Use absolute controlled paths for runtime/event files and a private service listener.

## `--listen`

### Short description

ext_proc service CLI flag.

### Syntax

```text
--listen PATH
```

### Valid contexts

- msconnector_envoy_ext_proc command line

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| CLI flag | see CLI usage; path/host:port where applicable | no |

### Default

optional

Source: `main.go flag registration`.

### Inheritance and merge

not applicable

Merge: --listen overrides listen_address after JSON decoding; other flags are direct process inputs.

### Phases and runtime effect

Runtime service setup; --runtime-config selects the actual engine path.

Controls ext_proc service startup/check behavior.

### Validation and errors

main validates JSON and, where selected, Common Runtime before serving.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Safety and operations

Use absolute controlled paths for runtime/event files and a private service listener.

## `--runtime-config`

### Short description

ext_proc service CLI flag.

### Syntax

```text
--runtime-config PATH
```

### Valid contexts

- msconnector_envoy_ext_proc command line

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| CLI flag | see CLI usage; path/host:port where applicable | no |

### Default

optional

Source: `main.go flag registration`.

### Inheritance and merge

not applicable

Merge: --listen overrides listen_address after JSON decoding; other flags are direct process inputs.

### Phases and runtime effect

Runtime service setup; --runtime-config selects the actual engine path.

Controls ext_proc service startup/check behavior.

### Validation and errors

main validates JSON and, where selected, Common Runtime before serving.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Safety and operations

Use absolute controlled paths for runtime/event files and a private service listener.

## `@ADMIN_PORT@`

### Short description

Template placeholder, not an Envoy configuration field.

### Syntax

```text
@ADMIN_PORT@
```

### Valid contexts

- Envoy YAML template before materialization

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| template placeholder | materializer-provided, validated value | yes |

### Default

none; must be materialized

Source: `template contains a required placeholder`.

### Inheritance and merge

not applicable

Merge: substituted once by the repository materializer.

### Phases and runtime effect

Host bootstrap only.

Supplies a release marker or local endpoint value to the generated Envoy configuration.

### Validation and errors

The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use private, non-conflicting ports; never place generated runtime output in the checkout.

## `@ENVOY_RELEASE@`

### Short description

Template placeholder, not an Envoy configuration field.

### Syntax

```text
@ENVOY_RELEASE@
```

### Valid contexts

- Envoy YAML template before materialization

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| template placeholder | materializer-provided, validated value | yes |

### Default

none; must be materialized

Source: `template contains a required placeholder`.

### Inheritance and merge

not applicable

Merge: substituted once by the repository materializer.

### Phases and runtime effect

Host bootstrap only.

Supplies a release marker or local endpoint value to the generated Envoy configuration.

### Validation and errors

The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use private, non-conflicting ports; never place generated runtime output in the checkout.

## `@EXT_PROC_PORT@`

### Short description

Template placeholder, not an Envoy configuration field.

### Syntax

```text
@EXT_PROC_PORT@
```

### Valid contexts

- Envoy YAML template before materialization

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| template placeholder | materializer-provided, validated value | yes |

### Default

none; must be materialized

Source: `template contains a required placeholder`.

### Inheritance and merge

not applicable

Merge: substituted once by the repository materializer.

### Phases and runtime effect

Host bootstrap only.

Supplies a release marker or local endpoint value to the generated Envoy configuration.

### Validation and errors

The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use private, non-conflicting ports; never place generated runtime output in the checkout.

## `@LISTEN_PORT@`

### Short description

Template placeholder, not an Envoy configuration field.

### Syntax

```text
@LISTEN_PORT@
```

### Valid contexts

- Envoy YAML template before materialization

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| template placeholder | materializer-provided, validated value | yes |

### Default

none; must be materialized

Source: `template contains a required placeholder`.

### Inheritance and merge

not applicable

Merge: substituted once by the repository materializer.

### Phases and runtime effect

Host bootstrap only.

Supplies a release marker or local endpoint value to the generated Envoy configuration.

### Validation and errors

The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use private, non-conflicting ports; never place generated runtime output in the checkout.

## `@UPSTREAM_PORT@`

### Short description

Template placeholder, not an Envoy configuration field.

### Syntax

```text
@UPSTREAM_PORT@
```

### Valid contexts

- Envoy YAML template before materialization

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| template placeholder | materializer-provided, validated value | yes |

### Default

none; must be materialized

Source: `template contains a required placeholder`.

### Inheritance and merge

not applicable

Merge: substituted once by the repository materializer.

### Phases and runtime effect

Host bootstrap only.

Supplies a release marker or local endpoint value to the generated Envoy configuration.

### Validation and errors

The materializer rejects unresolved placeholders and invalid ports; output must be outside the checkout.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use private, non-conflicting ports; never place generated runtime output in the checkout.

## `admin`

### Short description

Groups Envoy management-interface configuration.

### Syntax

```text
admin: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Admin mapping | access_log_path and address child fields | no |

### Default

No connector-owned admin configuration default is declared; the selected template sets a loopback listener with /dev/null access log.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Management plane only; it does not create or alter P1–P4 callbacks.

Groups Envoy management-interface configuration.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Admin exposure is a separate privileged surface and must remain private in the example.

## `admin.access_log_path`

### Short description

Selects where Envoy writes administrative HTTP access records.

### Syntax

```text
admin.access_log_path: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| filesystem path string | writable path accepted by Envoy; selected value is /dev/null | no |

### Default

No connector-owned admin access-log path default is declared; the selected template sets /dev/null.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Management-plane only; it does not alter P1–P4 ext_proc visibility.

Selects where Envoy writes administrative HTTP access records.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `/dev/null`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Administrative logs can contain operational metadata; /dev/null suppresses them in this example rather than providing an audit design.

## `admin.address`

### Short description

Groups the Envoy administration listener address.

### Syntax

```text
admin.address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy admin core.Address mapping | one supported address form; selected form is a loopback socket_address | no |

### Default

No connector-owned admin address default is declared; the selected template sets 127.0.0.1 and @ADMIN_PORT@.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Management-plane only; independent of P1–P4 transaction processing.

Groups the Envoy administration listener address.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Admin endpoints are sensitive; keep the selected listener loopback/private.

## `admin.address.socket_address`

### Short description

Pairs the Envoy administration host and TCP port.

### Syntax

```text
admin.address.socket_address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy admin SocketAddress mapping | address and port_value child fields | no |

### Default

No connector-owned admin socket-address default is declared; the selected template sets 127.0.0.1 plus @ADMIN_PORT@.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Management-plane only; independent of P1–P4 transaction processing.

Pairs the Envoy administration host and TCP port.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Do not bind the administration socket publicly without a separate access-control design.

## `admin.address.socket_address.address`

### Short description

Binds the Envoy administration listener to the selected interface.

### Syntax

```text
admin.address.socket_address.address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy admin host/IP string | valid host or IP literal; selected value is 127.0.0.1 | no |

### Default

No connector-owned admin host default is declared; the selected template sets 127.0.0.1.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Management-plane only; independent of P1–P4 transaction processing.

Binds the Envoy administration listener to the selected interface.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `127.0.0.1`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Loopback prevents the example admin interface from being reachable remotely.

## `admin.address.socket_address.port_value`

### Short description

Selects the local TCP port for Envoy administration endpoints.

### Syntax

```text
admin.address.socket_address.port_value: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy admin uint32 TCP port | materializer-validated decimal port 1..65535 | no |

### Default

No connector-owned admin port default is declared; the selected template sets the @ADMIN_PORT@ materializer input.

Source: `selected template and prepare_envoy_ext_proc_config.sh materializer`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Management-plane only; independent of P1–P4 transaction processing.

Selects the local TCP port for Envoy administration endpoints.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `@ADMIN_PORT@`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use a private, non-conflicting port; exposing admin APIs is unrelated to ModSecurity enforcement.

## `cleanup_timeout_ms`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"cleanup_timeout_ms": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `1000`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `engine_timeout_ms`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"engine_timeout_ms": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `150`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `late_action_policy`

### Short description

Selects late decision reporting; minimal and safe record late disruptive decisions as log_only, while strict records strict_abort_not_attempted rather than a fabricated status/reset.

### Syntax

```text
"late_action_policy": <LateActionPolicy>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| LateActionPolicy | minimal \| safe \| strict | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Selects late decision reporting; minimal and safe record late disruptive decisions as log_only, while strict records strict_abort_not_attempted rather than a fabricated status/reset.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `"safe"`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `listen_address`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"listen_address": <string>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | non-empty host:port | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `"127.0.0.1:18083"`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_body_chunk_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_body_chunk_bytes": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `1048576`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_grpc_message_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_grpc_message_bytes": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `1114112`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_header_count`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_header_count": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `128`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_header_name_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_header_name_bytes": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `256`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_header_value_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_header_value_bytes": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `8192`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_request_body_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_request_body_bytes": <int64>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int64 | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `10485760`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_response_body_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_response_body_bytes": <int64>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int64 | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `10485760`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `max_total_header_bytes`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"max_total_header_bytes": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `32768`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `shutdown_timeout_ms`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"shutdown_timeout_ms": <int>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| int | positive value | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `5000`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `static_resources`

### Short description

Declares the complete static data-plane topology used by the checked-in example.

### Syntax

```text
static_resources: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Bootstrap static_resources mapping | listener and cluster child mappings shown in the template | no |

### Default

No connector-owned static-resource set default is declared; the selected template sets the explicit listener and static clusters.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap establishes the selected ext_proc P1–P4 path but does not itself process a transaction.

Declares the complete static data-plane topology used by the checked-in example.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

All listener and cluster children affect traffic exposure or destination; review as one topology.

## `static_resources.clusters`

### Short description

Declares the static service destinations used by routing and ext_proc gRPC.

### Syntax

```text
static_resources.clusters: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Cluster mapping | one or more Cluster objects; selected template declares upstream_service and msconnector_ext_proc | no |

### Default

No connector-owned cluster list default is declared; the selected template sets the explicit upstream and local processor clusters.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

upstream_service provides the request/response path; msconnector_ext_proc transports selected P1–P4 callbacks.

Declares the static service destinations used by routing and ext_proc gRPC.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Clusters define where application traffic and inspection data can leave the listener.

## `static_resources.clusters[].connect_timeout`

### Short description

Bounds TCP connection establishment to the upstream or local processor endpoint.

### Syntax

```text
static_resources.clusters[].connect_timeout: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy protobuf Duration for cluster connection attempts | non-negative duration; selected native value is 0.5s (compatibility example uses 0.25s) | no |

### Default

No connector-owned cluster connect timeout default is declared; the selected template sets the explicit template duration.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Bounds TCP connection establishment to the upstream or local processor endpoint.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `0.5s`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A long timeout retains connections; a short timeout can trigger processor failures or upstream unavailability.

## `static_resources.clusters[].http2_protocol_options`

### Short description

Enables the HTTP/2 protocol options needed by the Envoy gRPC ext_proc cluster.

### Syntax

```text
static_resources.clusters[].http2_protocol_options: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Http2ProtocolOptions mapping | empty or configured HTTP/2 options; selected value is {} on the ext_proc cluster | no |

### Default

Absent unless configured; the selected ext_proc cluster explicitly sets an empty HTTP/2 options mapping.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Transport prerequisite for the ext_proc bidirectional stream carrying P1–P4 callbacks.

Enables the HTTP/2 protocol options needed by the Envoy gRPC ext_proc cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `{}`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Do not remove HTTP/2 support from the selected gRPC processor cluster.

## `static_resources.clusters[].load_assignment`

### Short description

Groups the endpoints assigned to a static cluster.

### Syntax

```text
static_resources.clusters[].load_assignment: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ClusterLoadAssignment mapping | cluster_name plus endpoint/lb_endpoints children | no |

### Default

No connector-owned static load assignment default is declared; the selected template sets the explicit loopback endpoint set.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Groups the endpoints assigned to a static cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Endpoint assignments are egress/control-plane inputs; review every address and port.

## `static_resources.clusters[].load_assignment.cluster_name`

### Short description

Associates the endpoint assignment with its enclosing cluster.

### Syntax

```text
static_resources.clusters[].load_assignment.cluster_name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ClusterLoadAssignment.cluster_name string | must match the enclosing Cluster.name; selected values match upstream_service or msconnector_ext_proc | no |

### Default

No connector-owned load-assignment cluster name default is declared; the selected template sets the enclosing static cluster name.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Associates the endpoint assignment with its enclosing cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `upstream_service, msconnector_ext_proc`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A mismatch invalidates or misroutes the endpoint configuration.

## `static_resources.clusters[].load_assignment.endpoints`

### Short description

Groups load-balanced endpoints for the static cluster.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy LocalityLbEndpoints mapping | one or more locality endpoint groups; the example has one group | no |

### Default

No connector-owned endpoint-group list default is declared; the selected template sets one loopback locality group.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Groups load-balanced endpoints for the static cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Each endpoint is a traffic destination; preserve the intended private scope.

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`

### Short description

Defines endpoint candidates selected by Envoy's cluster load balancer.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy LbEndpoint mapping | one or more endpoint mappings; the example has one endpoint per cluster | no |

### Default

No connector-owned load-balancer endpoint list default is declared; the selected template sets one explicit loopback endpoint.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Defines endpoint candidates selected by Envoy's cluster load balancer.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

An added endpoint receives copied requests or ext_proc messages; require explicit trust review.

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`

### Short description

Contains the network address of one cluster endpoint.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Endpoint mapping | endpoint address child mapping | no |

### Default

No connector-owned endpoint object default is declared; the selected template sets the explicit loopback socket address.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Contains the network address of one cluster endpoint.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The endpoint is a concrete traffic target and must be constrained to the intended service.

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`

### Short description

Contains the TCP address for one upstream or ext_proc service endpoint.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.Address mapping | one supported Envoy address form; selected form is socket_address | no |

### Default

No connector-owned cluster endpoint address default is declared; the selected template sets a loopback socket_address mapping.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Contains the TCP address for one upstream or ext_proc service endpoint.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Changing it changes egress or inspection-service reachability.

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`

### Short description

Pairs the static cluster endpoint host and TCP port.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.SocketAddress mapping | address and port_value child fields | no |

### Default

No connector-owned cluster endpoint socket-address default is declared; the selected template sets 127.0.0.1 plus its materialized port.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Pairs the static cluster endpoint host and TCP port.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The selected loopback values keep both upstream and processor endpoint examples local.

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`

### Short description

Targets the static upstream or ext_proc endpoint host.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress host/IP string | valid endpoint host or IP literal; selected value is 127.0.0.1 | no |

### Default

No connector-owned cluster endpoint host default is declared; the selected template sets 127.0.0.1.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Targets the static upstream or ext_proc endpoint host.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `127.0.0.1`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Loopback avoids external egress in the example; a remote host needs transport and trust controls.

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`

### Short description

Targets the TCP port of the selected upstream or ext_proc endpoint.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress uint32 TCP port | materializer-validated decimal port 1..65535 | no |

### Default

No connector-owned cluster endpoint port default is declared; the selected template sets the @UPSTREAM_PORT@ or @EXT_PROC_PORT@ materializer input.

Source: `selected template and prepare_envoy_ext_proc_config.sh materializer`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Targets the TCP port of the selected upstream or ext_proc endpoint.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `@UPSTREAM_PORT@, @EXT_PROC_PORT@`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Port changes can send traffic to a different local service; retain explicit private service ownership.

## `static_resources.clusters[].name`

### Short description

Names a static endpoint group referenced by the route or ext_proc gRPC service.

### Syntax

```text
static_resources.clusters[].name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Cluster.name string | unique non-empty cluster name; selected values are upstream_service and msconnector_ext_proc | no |

### Default

No connector-owned cluster-name default is declared; the selected template sets the two named static clusters.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

upstream_service supplies the normal request/response flow; msconnector_ext_proc carries P1–P4 processor traffic.

Names a static endpoint group referenced by the route or ext_proc gRPC service.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `upstream_service, msconnector_ext_proc`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Cluster names resolve traffic destinations; do not redirect an inspection target to an unreviewed service.

## `static_resources.clusters[].type`

### Short description

Determines how Envoy resolves the endpoint set for the named cluster.

### Syntax

```text
static_resources.clusters[].type: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Cluster DiscoveryType enum | Envoy discovery type; selected native value STATIC, compatibility values STRICT_DNS | no |

### Default

No connector-owned cluster discovery type default is declared; the selected template sets STATIC for the selected native local endpoints.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.

Determines how Envoy resolves the endpoint set for the named cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `STATIC`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

STATIC keeps the selected endpoints explicit; DNS discovery changes endpoint resolution and should be reviewed for egress/identity impact.

## `static_resources.listeners`

### Short description

Declares the downstream listener objects present in the static bootstrap.

### Syntax

```text
static_resources.listeners: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Listener mapping | one or more Listener objects; selected template declares one loopback HTTP listener | no |

### Default

No connector-owned listener list default is declared; the selected template sets one msconnector_ext_proc_listener.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap container for the filter chain that exposes selected P1–P4 ext_proc callbacks.

Declares the downstream listener objects present in the static bootstrap.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A listener changes the network attack surface before request policy is reached.

## `static_resources.listeners[].address`

### Short description

Contains the downstream listener bind address used before the HTTP filter chain runs.

### Syntax

```text
static_resources.listeners[].address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.Address mapping | one supported Envoy address form; the example selects socket_address | no |

### Default

No connector-owned listener-address default is declared; the selected template sets a loopback socket_address mapping.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Contains the downstream listener bind address used before the HTTP filter chain runs.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Changing the child socket address changes network exposure before any ModSecurity processing.

## `static_resources.listeners[].address.socket_address`

### Short description

Pairs the listener host and TCP port that accept downstream traffic.

### Syntax

```text
static_resources.listeners[].address.socket_address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.SocketAddress mapping | address plus port_value (or another Envoy-supported socket-address form) | no |

### Default

No connector-owned listener socket-address default is declared; the selected template sets 127.0.0.1 and @LISTEN_PORT@.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Pairs the listener host and TCP port that accept downstream traffic.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The selected loopback pair keeps the example private; a wildcard bind requires an explicit exposure decision.

## `static_resources.listeners[].address.socket_address.address`

### Short description

Binds the downstream HTTP listener to the selected network interface.

### Syntax

```text
static_resources.listeners[].address.socket_address.address: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress host/IP string | a valid listener host or IP literal; selected value is 127.0.0.1 | no |

### Default

No connector-owned listener host default is declared; the selected template sets 127.0.0.1.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Binds the downstream HTTP listener to the selected network interface.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `127.0.0.1`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The selected value is loopback-only.

## `static_resources.listeners[].address.socket_address.port_value`

### Short description

Selects the TCP port on which downstream requests enter the ext_proc filter chain.

### Syntax

```text
static_resources.listeners[].address.socket_address.port_value: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress uint32 TCP port | materializer-validated decimal port 1..65535 | no |

### Default

No connector-owned listener port default is declared; the selected template sets the @LISTEN_PORT@ materializer input.

Source: `selected template and prepare_envoy_ext_proc_config.sh materializer`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Selects the TCP port on which downstream requests enter the ext_proc filter chain.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `@LISTEN_PORT@`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use a private, non-conflicting port; port selection affects reachability before P1.

## `static_resources.listeners[].filter_chains`

### Short description

Defines the network-filter sequence applied to accepted downstream connections.

### Syntax

```text
static_resources.listeners[].filter_chains: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Listener.FilterChain mapping | one or more filter-chain mappings; the example has one HTTP chain | no |

### Default

No connector-owned filter-chain set default is declared; the selected template sets one chain containing the HTTP connection manager.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Defines the network-filter sequence applied to accepted downstream connections.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Filter ordering determines whether ext_proc sees traffic before routing; do not insert an unreviewed bypass.

## `static_resources.listeners[].filter_chains[].filters`

### Short description

Installs the HTTP connection manager that owns routing and the nested ext_proc HTTP filter chain.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy NetworkFilter mapping | network filters with a name and typed_config; selected item is HTTP connection manager | no |

### Default

No connector-owned network-filter list default is declared; the selected template sets the HCM filter.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Installs the HTTP connection manager that owns routing and the nested ext_proc HTTP filter chain.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Removing or replacing HCM removes the selected HTTP/ext_proc lifecycle path.

## `static_resources.listeners[].filter_chains[].filters[].name`

### Short description

Selects Envoy's HTTP connection manager implementation for the listener.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy NetworkFilter factory name | registered network-filter name; selected value is envoy.filters.network.http_connection_manager | no |

### Default

No connector-owned network-filter factory default is declared; the selected template sets the HTTP connection manager factory name.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Selects Envoy's HTTP connection manager implementation for the listener.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `envoy.filters.network.http_connection_manager`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A different network filter can remove HTTP routing and all ext_proc visibility.

## `static_resources.listeners[].filter_chains[].filters[].typed_config`

### Short description

Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| google.protobuf.Any mapping for HttpConnectionManager | an Any payload whose @type is the Envoy v3 HttpConnectionManager URL | no |

### Default

No connector-owned HCM typed configuration default is declared; the selected template sets the explicit HttpConnectionManager payload.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The payload controls which filters receive downstream traffic; validate the concrete type URL with Envoy.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.@type`

### Short description

Lets Envoy decode the surrounding typed_config as an HTTP connection manager.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.@type: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| protobuf Any type URL string | type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager | no |

### Default

No connector-owned HCM Any type default is declared; the selected template sets the explicit v3 HttpConnectionManager URL.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Lets Envoy decode the surrounding typed_config as an HTTP connection manager.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A mismatched type URL prevents a valid HTTP/ext_proc listener configuration.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`

### Short description

Orders HTTP processing: ext_proc runs before the router forwards upstream.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ordered repeated Envoy HTTP filter mapping | HTTP filters with factory name and typed_config; selected order is ext_proc then router | no |

### Default

No connector-owned HTTP-filter chain default is declared; the selected template sets ext_proc then router ordered pair.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The selected order enables P1/P2/P3/P4 ext_proc callbacks before traffic is handed to the router.

Orders HTTP processing: ext_proc runs before the router forwards upstream.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Moving router ahead of ext_proc bypasses the selected inspection/authorization path.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`

### Short description

Selects the ext_proc policy filter and terminal router implementations in the HCM chain.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HTTP filter factory-name string | registered HTTP filter name; selected values are envoy.filters.http.ext_proc and envoy.filters.http.router | no |

### Default

No connector-owned HTTP-filter factories default is declared; the selected template sets the ext_proc/router ordered pair.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

ext_proc exposes P1–P4; router terminates the filter chain and forwards to the upstream.

Selects the ext_proc policy filter and terminal router implementations in the HCM chain.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `envoy.filters.http.ext_proc, envoy.filters.http.router`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Filter order is an enforcement boundary: ext_proc must remain before router for the selected path.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`

### Short description

Holds the per-filter configuration corresponding to each HTTP filter item.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated google.protobuf.Any HTTP-filter configuration mapping | Any payloads whose @type values select ExternalProcessor and Router | no |

### Default

No connector-owned HTTP typed configurations default is declared; the selected template sets the explicit ExternalProcessor and Router payloads.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The ExternalProcessor payload sets concrete P1–P4 visibility; the Router payload forwards the post-filter request.

Holds the per-filter configuration corresponding to each HTTP filter item.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A mismatched Any payload/name pair can invalidate or bypass the intended inspection chain.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`

### Short description

Lets Envoy decode each HTTP filter's typed configuration.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| protobuf Any type URL string | ExternalProcessor and Router v3 type URLs in the same order as the HTTP filters | no |

### Default

No connector-owned HTTP Any type URLs default is declared; the selected template sets the explicit ExternalProcessor and Router v3 URLs.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

ExternalProcessor chooses P1–P4 callbacks; Router supplies the terminal forwarding stage.

Lets Envoy decode each HTTP filter's typed configuration.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `type.googleapis.com/envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The type URL must match the neighboring filter factory; otherwise Envoy cannot apply the selected lifecycle policy.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override`

### Short description

Allows or ignores a processor-supplied mode_override that would change processing_mode after request headers.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc boolean | true \| false | no |

### Default

Envoy proto default false; the selected template explicitly sets false.

Source: `Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Guards the configured P1–P4 processing_mode contract; false keeps the static selected lifecycle surface.

Allows or ignores a processor-supplied mode_override that would change processing_mode after request headers.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `false`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

false prevents the remote processor from widening/narrowing configured P1–P4 visibility at runtime.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow`

### Short description

Chooses whether processor stream errors/timeouts fail open (true) or produce Envoy's error handling (false).

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc boolean | true \| false | no |

### Default

Envoy proto default false; the selected template explicitly sets false.

Source: `Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Failure behavior for the ext_proc stream serving all selected P1–P4 callbacks.

Chooses whether processor stream errors/timeouts fail open (true) or produce Envoy's error handling (false).

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `false`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

false avoids silently allowing traffic when the local processor cannot be reached; availability and denial behavior still need runtime evidence.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service`

### Short description

Names the bidirectional gRPC side stream used by the ExternalProcessor filter.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy GrpcService mapping | one gRPC service selector; selected form is envoy_grpc | no |

### Default

No connector-owned ext_proc gRPC service default is declared; the selected template sets the msconnector_ext_proc envoy_grpc target.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Transport for all selected ext_proc callbacks: P1, P2, P3, P4, and trailer/EOS notifications.

Names the bidirectional gRPC side stream used by the ExternalProcessor filter.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The processor endpoint must be trusted and private; it receives selected request/response metadata and body chunks.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc`

### Short description

Uses Envoy-managed gRPC transport rather than an inline URI for the external processor.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| EnvoyGrpc cluster-reference mapping | cluster_name child naming a declared HTTP/2 cluster | no |

### Default

No connector-owned Envoy gRPC target default is declared; the selected template sets the msconnector_ext_proc cluster reference.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Carries the full selected P1–P4 external-processing stream.

Uses Envoy-managed gRPC transport rather than an inline URI for the external processor.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The cluster reference must resolve to the reviewed ext_proc service, not an arbitrary remote endpoint.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name`

### Short description

Binds ExternalProcessor gRPC traffic to the local ext_proc cluster.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy cluster-name string | name of a declared HTTP/2-capable cluster; selected value is msconnector_ext_proc | no |

### Default

No connector-owned ext_proc service cluster default is declared; the selected template sets msconnector_ext_proc.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Transport target for P1 request headers, P2 request chunks, P3 response headers, P4 response chunks, and EOS trailers.

Binds ExternalProcessor gRPC traffic to the local ext_proc cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `msconnector_ext_proc`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Changing it can send inspected headers/bodies to another processor; retain a private trusted target.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout`

### Short description

Bounds service establishment/operation as configured on the ext_proc gRPC service reference.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy protobuf Duration | non-negative duration; selected value is 0.2s | no |

### Default

No connector-owned gRPC service timeout default is declared; the selected template sets 0.2s.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Applies to the ext_proc transport that serves selected P1–P4 callbacks.

Bounds service establishment/operation as configured on the ext_proc gRPC service reference.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `0.2s`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A value that is too small creates avoidable processor failures; too large retains request resources longer.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout`

### Short description

Caps a processor-requested extension of the per-message timeout.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy protobuf Duration maximum override timeout | non-negative duration; selected value is 0.25s | no |

### Default

Envoy default is 0, which disables the processor override_message_timeout API; the selected template permits overrides up to 0.25s.

Source: `Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Applies to timeout control for selected P1–P4 ext_proc exchanges; it does not change their visibility modes.

Caps a processor-requested extension of the per-message timeout.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `0.25s`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A finite cap limits remote processor influence over stream retention; setting a positive cap deliberately enables this API.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout`

### Short description

Limits how long Envoy waits for each required external-processor response.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy protobuf Duration per ext_proc message | non-negative duration; selected value is 0.2s | no |

### Default

Envoy ext_proc default 200 milliseconds when omitted; the selected template explicitly sets 0.2s.

Source: `Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Applies to per-message P1/P2/P3/P4 ext_proc exchanges except observability/full-duplex/gRPC cases documented by Envoy.

Limits how long Envoy waits for each required external-processor response.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `0.2s`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Too large a timeout retains stream resources; too small a timeout creates processor failures governed by failure_mode_allow.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode`

### Short description

Groups the ext_proc visibility controls for request/response headers, bodies, and trailers.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc ProcessingMode mapping | header, body, and trailer send-mode child enums | no |

### Default

Envoy defaults send request/response headers, skip trailers, and send no bodies; this template overrides every selected lifecycle field.

Source: `Envoy ext_proc v3 ProcessingMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Controls P1 request headers, P2 request body, P3 response headers, P4 response body, and trailer/EOS delivery.

Groups the ext_proc visibility controls for request/response headers, bodies, and trailers.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Omitting body modes loses body visibility; preserve explicit streaming modes for the selected full-lifecycle bridge.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode`

### Short description

Selects request/P2 body delivery to ext_proc; STREAMED sends incremental body chunks.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc BodySendMode enum | NONE \| STREAMED \| BUFFERED \| BUFFERED_PARTIAL \| FULL_DUPLEX_STREAMED \| GRPC | no |

### Default

Envoy proto default NONE; the selected template explicitly sets STREAMED.

Source: `Envoy ext_proc v3 ProcessingMode.BodySendMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

request/P2: selected STREAMED makes the body available incrementally to the ext_proc bridge.

Selects request/P2 body delivery to ext_proc; STREAMED sends incremental body chunks.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `STREAMED`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Body delivery exposes payload data and consumes stream resources; the selected Common bridge requires STREAMED with bounded service controls.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode`

### Short description

Selects whether request/P1 headers are sent to the external processor.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc HeaderSendMode enum | DEFAULT \| SEND \| SKIP | no |

### Default

Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND.

Source: `Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

request/P1: selected SEND exposes the header callback to the bridge.

Selects whether request/P1 headers are sent to the external processor.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `SEND`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Headers can include security-sensitive metadata; use the private local ext_proc service and its configured bounds.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode`

### Short description

Sends request trailers/EOS metadata to the external processor when trailers are present.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc HeaderSendMode enum for trailers | DEFAULT \| SEND \| SKIP | no |

### Default

Envoy effective default SKIP for trailers; the selected template explicitly sets SEND.

Source: `Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

request EOS/trailer visibility after the corresponding body stream; it complements P2/P4 streaming.

Sends request trailers/EOS metadata to the external processor when trailers are present.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `SEND`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Trailer metadata is part of the transaction; do not treat it as a body-size bypass.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode`

### Short description

Selects response/P4 body delivery to ext_proc; STREAMED sends incremental body chunks.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc BodySendMode enum | NONE \| STREAMED \| BUFFERED \| BUFFERED_PARTIAL \| FULL_DUPLEX_STREAMED \| GRPC | no |

### Default

Envoy proto default NONE; the selected template explicitly sets STREAMED.

Source: `Envoy ext_proc v3 ProcessingMode.BodySendMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

response/P4: selected STREAMED makes the body available incrementally to the ext_proc bridge.

Selects response/P4 body delivery to ext_proc; STREAMED sends incremental body chunks.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `STREAMED`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Body delivery exposes payload data and consumes stream resources; the selected Common bridge requires STREAMED with bounded service controls.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode`

### Short description

Selects whether response/P3 headers are sent to the external processor.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc HeaderSendMode enum | DEFAULT \| SEND \| SKIP | no |

### Default

Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND.

Source: `Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

response/P3: selected SEND exposes the header callback to the bridge.

Selects whether response/P3 headers are sent to the external processor.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `SEND`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Headers can include security-sensitive metadata; use the private local ext_proc service and its configured bounds.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode`

### Short description

Sends response trailers/EOS metadata to the external processor when trailers are present.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc HeaderSendMode enum for trailers | DEFAULT \| SEND \| SKIP | no |

### Default

Envoy effective default SKIP for trailers; the selected template explicitly sets SEND.

Source: `Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

response EOS/trailer visibility after the corresponding body stream; it complements P2/P4 streaming.

Sends response trailers/EOS metadata to the external processor when trailers are present.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `SEND`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Trailer metadata is part of the transaction; do not treat it as a body-size bypass.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes`

### Short description

Requests concrete peer/protocol metadata for the ext_proc ProcessingRequest attributes map.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy request-attribute name list | supported Envoy request attribute names; selected list requests protocol, source/destination address, and source/destination port | no |

### Default

Absent list requests no additional attributes; this template explicitly requests five attributes used by processor.requestMetadataFromEnvoy.

Source: `Envoy ext_proc v3 ExternalProcessor API and connectors/envoy/ext_proc/internal/processor/processor.go:requestMetadataFromEnvoy`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

P1 request metadata only; it seeds the transaction before P2 body callbacks and before later response callbacks.

Requests concrete peer/protocol metadata for the ext_proc ProcessingRequest attributes map.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Peer addresses and ports are operationally sensitive; the processor bounds and validates received metadata rather than deriving it from the gRPC peer.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]`

### Short description

Makes protocol and client/server endpoint metadata available to the ext_proc processor's request-metadata mapper.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy request-attribute path string | request.protocol \| source.address \| source.port \| destination.address \| destination.port | no |

### Default

No additional attribute is requested when omitted; this template explicitly requests all five metadata paths consumed by requestMetadataFromEnvoy.

Source: `selected template and connectors/envoy/ext_proc/internal/processor/processor.go:requestMetadataFromEnvoy`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

P1 request metadata visibility; the selected bridge uses it to construct transaction metadata before P2/P3/P4 callbacks.

Makes protocol and client/server endpoint metadata available to the ext_proc processor's request-metadata mapper.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `request.protocol, source.address, source.port, destination.address, destination.port`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Do not add unbounded or sensitive attributes without reviewing processor handling and event logging.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response`

### Short description

When true with STREAMED bodies, Envoy sends body chunks before the processor's header response; false retains header-response ordering.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_proc boolean | true \| false | no |

### Default

Envoy proto default false; the selected template explicitly sets false.

Source: `Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Controls P1-to-P2/P3-to-P4 sequencing for STREAMED bodies; it does not itself enable body visibility.

When true with STREAMED bodies, Envoy sends body chunks before the processor's header response; false retains header-response ordering.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `false`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Keeping false preserves the selected decision ordering and avoids uncontrolled early body delivery to the processor.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`

### Short description

Defines the route lookup that selects the upstream after request-side filters run.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteConfiguration mapping | inline route configuration with a name and virtual_hosts | no |

### Default

No connector-owned inline route configuration default is declared; the selected template sets msconnector_ext_proc_route.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.

Defines the route lookup that selects the upstream after request-side filters run.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Routes control upstream reachability; constrain domains and prefixes in a real deployment.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`

### Short description

Names the inline route configuration for Envoy diagnostics and references.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteConfiguration.name string | non-empty local route-config name; selected value is msconnector_ext_proc_route | no |

### Default

No connector-owned route-config name default is declared; the selected template sets msconnector_ext_proc_route.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routing metadata only; request filtering still occurs in the preceding HTTP filter order.

Names the inline route configuration for Envoy diagnostics and references.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `msconnector_ext_proc_route`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The name is not an authorization boundary; do not encode secrets in it.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`

### Short description

Groups host/domain matches and routes for the HCM.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy VirtualHost mapping | one or more virtual-host mappings; the example has local_service | no |

### Default

No connector-owned virtual-host list default is declared; the selected template sets one local_service entry.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.

Groups host/domain matches and routes for the HCM.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Over-broad virtual hosts can route unexpected Host values to the upstream.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`

### Short description

Selects which Host/:authority values enter this virtual host's route list.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy VirtualHost domain matcher | a list of Envoy domain patterns | no |

### Default

No connector-owned virtual-host domain matcher default is declared; the selected template sets the catch-all `*` pattern.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Host matching precedes upstream routing after request-header P1 processing.

Selects which Host/:authority values enter this virtual host's route list.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `["*"]`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The selected `*` catches all hosts; replace it with intended domains before exposure.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`

### Short description

Selects which Host/:authority values enter this virtual host's route list.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy VirtualHost domain-pattern string | exact host, suffix/wildcard domain pattern, or *; selected item is * | no |

### Default

No connector-owned virtual-host domain matcher default is declared; the selected template sets the catch-all `*` pattern.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Host matching precedes upstream routing after request-header P1 processing.

Selects which Host/:authority values enter this virtual host's route list.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `"*"`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The selected `*` catches all hosts; replace it with intended domains before exposure.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`

### Short description

Labels the virtual-host route group.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy VirtualHost.name string | non-empty virtual-host name; selected value is local_service | no |

### Default

No connector-owned virtual-host name default is declared; the selected template sets local_service.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routing metadata only; it does not independently change ext_proc visibility.

Labels the virtual-host route group.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `local_service`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Use opaque operational names rather than confidential data.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`

### Short description

Contains ordered route matching and upstream actions for the virtual host.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Route mapping | one or more match/action route mappings; the example has one prefix route | no |

### Default

No connector-owned route list default is declared; the selected template sets one `/` prefix route to upstream_service.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

The matched route is selected after P1; its upstream yields the response seen at P3/P4.

Contains ordered route matching and upstream actions for the virtual host.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Route order and match breadth determine where request traffic can be sent.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`

### Short description

Groups the prefix matcher for the selected route.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteMatch mapping | the child fields shown in this template | no |

### Default

No connector-owned RouteMatch mapping default is declared; the selected template sets the explicit `/` prefix and upstream_service action.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.

Groups the prefix matcher for the selected route.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

An over-broad match or unsafe route action can expose an unintended upstream.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`

### Short description

Matches request paths for the selected route.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteMatch prefix string | path-prefix matcher; selected value is / | no |

### Default

No connector-owned route prefix default is declared; the selected template sets the catch-all `/` prefix.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.

Matches request paths for the selected route.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `"/"`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The catch-all `/` reaches every path in the virtual host; narrow it when policy requires.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route`

### Short description

Groups the cluster action selected after the route match.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteAction mapping | the child fields shown in this template | no |

### Default

No connector-owned RouteAction mapping default is declared; the selected template sets the explicit `/` prefix and upstream_service action.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.

Groups the cluster action selected after the route match.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

An over-broad match or unsafe route action can expose an unintended upstream.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster`

### Short description

Routes matching downstream requests to the named upstream cluster.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteAction cluster-name string | name of a declared static_resources.clusters entry; selected value is upstream_service | no |

### Default

No connector-owned route cluster target default is declared; the selected template sets upstream_service.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.

Routes matching downstream requests to the named upstream cluster.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `upstream_service`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

The target must be a reviewed local/upstream endpoint; an untrusted target creates an egress path.

## `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`

### Short description

Prefixes HCM metrics for the selected ingress listener.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| HttpConnectionManager statistics-prefix string | non-empty metrics namespace token; selected value is msconnector_ext_proc_ingress | no |

### Default

No connector-owned HCM statistic prefix default is declared; the selected template sets msconnector_ext_proc_ingress.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Observability only; it does not change P1–P4 payload visibility.

Prefixes HCM metrics for the selected ingress listener.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `msconnector_ext_proc_ingress`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

Metric names should not embed secrets, user identifiers, or unbounded request data.

## `static_resources.listeners[].name`

### Short description

Names the downstream HTTP listener for Envoy configuration and observability.

### Syntax

```text
static_resources.listeners[].name: <value>
```

### Valid contexts

- The YAML object path shown in the selected example.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Listener.name string | unique non-empty listener name in this bootstrap | no |

### Default

No connector-owned listener-name default is declared; the selected template sets `msconnector_ext_proc_listener`.

Source: `selected Envoy v3 template; connector owns no bootstrap default`.

### Inheritance and merge

Host YAML/API defined; not a Common Runtime merge setting.

Merge: Host YAML/API defined; checked-in static and dynamic configurations are separate layers.

### Phases and runtime effect

Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.

Names the downstream HTTP listener for Envoy configuration and observability.

### Validation and errors

Materialize outside the checkout, then run envoy --mode validate -c <generated-config>.

### Example

Selected example value: `msconnector_ext_proc_listener`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Safety and operations

A name is control-plane metadata, but it should not disclose tenant or secret identifiers.

## `transaction_id_header`

### Short description

Sets one bounded ext_proc service control.

### Syntax

```text
"transaction_id_header": <string>
```

### Valid contexts

- ext_proc service JSON object

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | non-empty HTTP header name | yes |

### Default

none; JSON decoder/Config.Validate requires every selected field

Source: `processor.Config has no implicit field defaults`.

### Inheritance and merge

No inheritance; one JSON object is decoded with unknown fields rejected.

Merge: No merge; a second JSON value is rejected after the one configuration object.

### Phases and runtime effect

Limits and late policy affect P1–P4 processor behavior.

Sets one bounded ext_proc service control.

### Validation and errors

Config.Validate rejects empty, non-positive, invalid enum, invalid host:port, and inconsistent gRPC/body limits.

### Example

Selected example value: `"x-request-id"`.

Source-backed example: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Safety and operations

Bound all header, body, gRPC, and timeout values; keep service listen address private.

## `compatibility.ext_authz.static_resources`

### Short description

Declares the complete static data-plane topology used by the checked-in example. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Bootstrap static_resources mapping | listener and cluster child mappings shown in the template | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Bootstrap establishes the selected ext_proc P1–P4 path but does not itself process a transaction. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Declares the complete static data-plane topology used by the checked-in example. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

All listener and cluster children affect traffic exposure or destination; review as one topology. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters`

### Short description

Declares the static service destinations used by routing and ext_proc gRPC. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Cluster mapping | one or more Cluster objects; selected template declares upstream_service and msconnector_ext_proc | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

upstream_service provides the request/response path; msconnector_ext_proc transports selected P1–P4 callbacks. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Declares the static service destinations used by routing and ext_proc gRPC. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Clusters define where application traffic and inspection data can leave the listener. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].connect_timeout`

### Short description

Bounds TCP connection establishment to the upstream or local processor endpoint. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].connect_timeout: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy protobuf Duration for cluster connection attempts | non-negative duration; selected native value is 0.5s (compatibility example uses 0.25s) | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.25s.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Bounds TCP connection establishment to the upstream or local processor endpoint. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `0.25s`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A long timeout retains connections; a short timeout can trigger processor failures or upstream unavailability. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment`

### Short description

Groups the endpoints assigned to a static cluster. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ClusterLoadAssignment mapping | cluster_name plus endpoint/lb_endpoints children | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the endpoints assigned to a static cluster. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Endpoint assignments are egress/control-plane inputs; review every address and port. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name`

### Short description

Associates the endpoint assignment with its enclosing cluster. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ClusterLoadAssignment.cluster_name string | must match the enclosing Cluster.name; selected values match upstream_service or msconnector_ext_proc | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz, app_backend.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Associates the endpoint assignment with its enclosing cluster. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `modsecurity_authz, app_backend`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A mismatch invalidates or misroutes the endpoint configuration. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints`

### Short description

Groups load-balanced endpoints for the static cluster. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy LocalityLbEndpoints mapping | one or more locality endpoint groups; the example has one group | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups load-balanced endpoints for the static cluster. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Each endpoint is a traffic destination; preserve the intended private scope. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`

### Short description

Defines endpoint candidates selected by Envoy's cluster load balancer. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy LbEndpoint mapping | one or more endpoint mappings; the example has one endpoint per cluster | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Defines endpoint candidates selected by Envoy's cluster load balancer. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

An added endpoint receives copied requests or ext_proc messages; require explicit trust review. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`

### Short description

Contains the network address of one cluster endpoint. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Endpoint mapping | endpoint address child mapping | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Contains the network address of one cluster endpoint. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The endpoint is a concrete traffic target and must be constrained to the intended service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`

### Short description

Contains the TCP address for one upstream or ext_proc service endpoint. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.Address mapping | one supported Envoy address form; selected form is socket_address | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Contains the TCP address for one upstream or ext_proc service endpoint. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Changing it changes egress or inspection-service reachability. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`

### Short description

Pairs the static cluster endpoint host and TCP port. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.SocketAddress mapping | address and port_value child fields | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { address: 127.0.0.1, port_value: 9000 }, { address: 127.0.0.1, port_value: 8081 }.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Pairs the static cluster endpoint host and TCP port. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `{ address: 127.0.0.1, port_value: 9000 }, { address: 127.0.0.1, port_value: 8081 }`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The selected loopback values keep both upstream and processor endpoint examples local. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`

### Short description

Targets the static upstream or ext_proc endpoint host. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress host/IP string | valid endpoint host or IP literal; selected value is 127.0.0.1 | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 127.0.0.1.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Targets the static upstream or ext_proc endpoint host. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `127.0.0.1`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Loopback avoids external egress in the example; a remote host needs transport and trust controls. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`

### Short description

Targets the TCP port of the selected upstream or ext_proc endpoint. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress uint32 TCP port | materializer-validated decimal port 1..65535 | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 9000, 8081.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Targets the TCP port of the selected upstream or ext_proc endpoint. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `9000, 8081`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Port changes can send traffic to a different local service; retain explicit private service ownership. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].name`

### Short description

Names a static endpoint group referenced by the route or ext_proc gRPC service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Cluster.name string | unique non-empty cluster name; selected values are upstream_service and msconnector_ext_proc | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz, app_backend.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

upstream_service supplies the normal request/response flow; msconnector_ext_proc carries P1–P4 processor traffic. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Names a static endpoint group referenced by the route or ext_proc gRPC service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `modsecurity_authz, app_backend`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Cluster names resolve traffic destinations; do not redirect an inspection target to an unreviewed service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.clusters[].type`

### Short description

Determines how Envoy resolves the endpoint set for the named cluster. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].type: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Cluster DiscoveryType enum | Envoy discovery type; selected native value STATIC, compatibility values STRICT_DNS | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures STRICT_DNS.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Determines how Envoy resolves the endpoint set for the named cluster. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `STRICT_DNS`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

STATIC keeps the selected endpoints explicit; DNS discovery changes endpoint resolution and should be reviewed for egress/identity impact. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners`

### Short description

Declares the downstream listener objects present in the static bootstrap. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Listener mapping | one or more Listener objects; selected template declares one loopback HTTP listener | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Bootstrap container for the filter chain that exposes selected P1–P4 ext_proc callbacks. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Declares the downstream listener objects present in the static bootstrap. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A listener changes the network attack surface before request policy is reached. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].address`

### Short description

Contains the downstream listener bind address used before the HTTP filter chain runs. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.Address mapping | one supported Envoy address form; the example selects socket_address | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Contains the downstream listener bind address used before the HTTP filter chain runs. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Changing the child socket address changes network exposure before any ModSecurity processing. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].address.socket_address`

### Short description

Pairs the listener host and TCP port that accept downstream traffic. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address.socket_address: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy core.SocketAddress mapping | address plus port_value (or another Envoy-supported socket-address form) | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { address: 0.0.0.0, port_value: 8080 }.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Pairs the listener host and TCP port that accept downstream traffic. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `{ address: 0.0.0.0, port_value: 8080 }`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The selected loopback pair keeps the example private; a wildcard bind requires an explicit exposure decision. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address`

### Short description

Binds the downstream HTTP listener to the selected network interface. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address.socket_address.address: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress host/IP string | a valid listener host or IP literal; selected value is 127.0.0.1 | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.0.0.0.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Binds the downstream HTTP listener to the selected network interface. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `0.0.0.0`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A wildcard or public value exposes the listener before ext_proc policy can run. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value`

### Short description

Selects the TCP port on which downstream requests enter the ext_proc filter chain. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy SocketAddress uint32 TCP port | materializer-validated decimal port 1..65535 | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 8080.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Selects the TCP port on which downstream requests enter the ext_proc filter chain. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `8080`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Use a private, non-conflicting port; port selection affects reachability before P1. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains`

### Short description

Defines the network-filter sequence applied to accepted downstream connections. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Listener.FilterChain mapping | one or more filter-chain mappings; the example has one HTTP chain | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Defines the network-filter sequence applied to accepted downstream connections. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Filter ordering determines whether ext_authz compatibility sees traffic before routing; do not insert an unreviewed bypass. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters`

### Short description

Installs the HTTP connection manager that owns routing and the nested ext_authz compatibility HTTP filter chain. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy NetworkFilter mapping | network filters with a name and typed_config; selected item is HTTP connection manager | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Installs the HTTP connection manager that owns routing and the nested ext_authz compatibility HTTP filter chain. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Removing or replacing HCM removes the selected HTTP/ext_authz compatibility lifecycle path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name`

### Short description

Selects Envoy's HTTP connection manager implementation for the listener. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy NetworkFilter factory name | registered network-filter name; selected value is envoy.filters.network.http_connection_manager | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures envoy.filters.network.http_connection_manager.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Selects Envoy's HTTP connection manager implementation for the listener. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `envoy.filters.network.http_connection_manager`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A different network filter can remove HTTP routing and all ext_authz compatibility visibility. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config`

### Short description

Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| google.protobuf.Any mapping for HttpConnectionManager | an Any payload whose @type is the Envoy v3 HttpConnectionManager URL | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The payload controls which filters receive downstream traffic; validate the concrete type URL with Envoy. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type`

### Short description

Lets Envoy decode the surrounding typed_config as an HTTP connection manager. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| protobuf Any type URL string | type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Lets Envoy decode the surrounding typed_config as an HTTP connection manager. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A mismatched type URL prevents a valid HTTP/ext_proc listener configuration. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`

### Short description

Orders HTTP processing: ext_authz runs before the router forwards upstream. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ordered repeated Envoy HTTP filter mapping | HTTP filters with factory name and typed_config; selected order is ext_authz then router | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The selected order enables compatibility P1 request authorization before the router; it does not create P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Orders HTTP processing: ext_authz runs before the router forwards upstream. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Moving router ahead of ext_authz bypasses the selected inspection/authorization path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`

### Short description

Selects the ext_authz policy filter and terminal router implementations in the HCM chain. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HTTP filter factory-name string | registered HTTP filter name; selected values are envoy.filters.http.ext_authz and envoy.filters.http.router | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures envoy.filters.http.ext_authz, envoy.filters.http.router.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

ext_authz is compatibility request authorization; router forwards after it and no selected P2/P3/P4 path exists. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Selects the ext_authz policy filter and terminal router implementations in the HCM chain. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `envoy.filters.http.ext_authz, envoy.filters.http.router`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Filter order is an enforcement boundary: ext_authz must remain before router for the selected path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`

### Short description

Holds the per-filter configuration corresponding to each HTTP filter item. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated google.protobuf.Any HTTP-filter configuration mapping | Any payloads whose @type values select ExtAuthz and Router | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The ExtAuthz payload controls compatibility P1 request authorization; the Router payload forwards the allowed request. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Holds the per-filter configuration corresponding to each HTTP filter item. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A mismatched Any payload/name pair can invalidate or bypass the intended inspection chain. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`

### Short description

Lets Envoy decode each HTTP filter's typed configuration. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| protobuf Any type URL string | ExtAuthz and Router v3 type URLs in the same order as the HTTP filters | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

ExtAuthz performs compatibility P1 request authorization; Router is terminal forwarding and does not expose selected P2/P3/P4 callbacks. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Lets Envoy decode each HTTP filter's typed configuration. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The type URL must match the neighboring filter factory; otherwise Envoy cannot apply the selected lifecycle policy. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service`

### Short description

Configures the compatibility ext_authz-style HTTP service instead of the selected gRPC ext_proc service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_authz HTTP service mapping (compatibility only) | one HTTP service; mutually exclusive with grpc_service | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility request authorization only; do not infer selected native P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Configures the compatibility ext_authz-style HTTP service instead of the selected gRPC ext_proc service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

HTTP service is compatibility-only and cannot provide the selected body/trailer full-lifecycle path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request`

### Short description

Groups the header-forwarding policy for the compatibility authorization request. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy ext_authz AuthorizationRequest mapping (compatibility only) | allowed_headers child mapping shown in the compatibility template | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility P1 request-header authorization only; no selected body or response visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the header-forwarding policy for the compatibility authorization request. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Only forward the headers the compatibility service needs; extra headers may disclose credentials or user data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers`

### Short description

Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HeaderMatcher list mapping (compatibility only) | one or more header matcher patterns; selected policy has exact authorization and content-type | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility P1 request-header authorization only; no native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Header forwarding can expose credentials; keep the matcher list minimal and audit changes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns`

### Short description

Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HeaderMatcher list mapping (compatibility only) | one or more header matcher patterns; selected policy has exact authorization and content-type | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility P1 request-header authorization only; no native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Header forwarding can expose credentials; keep the matcher list minimal and audit changes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact`

### Short description

Forwards only matching request headers to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HeaderMatcher exact header-name string (compatibility only) | lower-case/HTTP header name exact matcher; selected values are authorization and content-type | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures authorization, content-type.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility P1 request-header authorization only; no selected P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Forwards only matching request headers to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `authorization, content-type`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The authorization value is sensitive; ensure the compatibility service and its logs are trusted. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri`

### Short description

Groups the compatibility service URI, logical cluster, and deadline. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HttpService.server_uri mapping (compatibility only) | URI, cluster, and timeout child fields | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility request authorization only; no selected full response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the compatibility service URI, logical cluster, and deadline. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Keep the authorization service private and do not embed credentials in a URI. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster`

### Short description

Associates the HTTP authorization URI with its configured Envoy cluster. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy cluster-name string (compatibility only) | name of a declared compatibility cluster; selected value is modsecurity_authz | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility request authorization only; no selected P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Associates the HTTP authorization URI with its configured Envoy cluster. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `modsecurity_authz`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The name must resolve to a reviewed service cluster; do not treat it as the native ext_proc target. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout`

### Short description

Bounds one compatibility authorization HTTP request. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy protobuf Duration (compatibility HTTP authorization timeout) | non-negative duration; selected value is 0.2s | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.2s.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility request authorization only; no P3/P4 response inspection. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Bounds one compatibility authorization HTTP request. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `0.2s`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Deadline choice changes failure pressure; it is not an ext_proc full-lifecycle timeout guarantee. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri`

### Short description

Identifies the HTTP authorization endpoint for compatibility ext_authz requests. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy HTTP service URI string (compatibility only) | absolute HTTP/HTTPS URI; selected value is http://127.0.0.1:9000 | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures http://127.0.0.1:9000.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility request authorization only; no native response-body P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Identifies the HTTP authorization endpoint for compatibility ext_authz requests. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `http://127.0.0.1:9000`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Loopback limits the example exposure; a remote URI needs TLS, identity, and egress review. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`

### Short description

Defines the route lookup that selects the upstream after request-side filters run. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteConfiguration mapping | inline route configuration with a name and virtual_hosts | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Defines the route lookup that selects the upstream after request-side filters run. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Routes control upstream reachability; constrain domains and prefixes in a real deployment. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`

### Short description

Names the inline route configuration for Envoy diagnostics and references. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteConfiguration.name string | non-empty local route-config name; selected value is msconnector_ext_proc_route | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures local_route.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Routing metadata only; request filtering still occurs in the preceding HTTP filter order. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Names the inline route configuration for Envoy diagnostics and references. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `local_route`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The name is not an authorization boundary; do not encode secrets in it. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`

### Short description

Groups host/domain matches and routes for the HCM. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy VirtualHost mapping | one or more virtual-host mappings; the example has local_service | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups host/domain matches and routes for the HCM. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Over-broad virtual hosts can route unexpected Host values to the upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`

### Short description

Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy VirtualHost domain matcher | a list of Envoy domain patterns | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["*"].

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Host matching precedes upstream routing after request-header P1 processing. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `["*"]`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The selected `*` catches all hosts; replace it with intended domains before exposure. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`

### Short description

Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy VirtualHost domain-pattern string | exact host, suffix/wildcard domain pattern, or *; selected item is * | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "*".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Host matching precedes upstream routing after request-header P1 processing. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `"*"`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The selected `*` catches all hosts; replace it with intended domains before exposure. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`

### Short description

Labels the virtual-host route group. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy VirtualHost.name string | non-empty virtual-host name; selected value is local_service | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures backend.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Routing metadata only; it does not independently change ext_proc visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Labels the virtual-host route group. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `backend`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Use opaque operational names rather than confidential data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`

### Short description

Contains ordered route matching and upstream actions for the virtual host. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| repeated Envoy Route mapping | one or more match/action route mappings; the example has one prefix route | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

The matched route is selected after P1; its upstream yields the response seen at P3/P4. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Contains ordered route matching and upstream actions for the virtual host. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Route order and match breadth determine where request traffic can be sent. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`

### Short description

Groups the prefix matcher for the selected route. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteMatch mapping | the child fields shown in this template | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { prefix: "/" }.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the prefix matcher for the selected route. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `{ prefix: "/" }`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

An over-broad match or unsafe route action can expose an unintended upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`

### Short description

Matches request paths for the selected route. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteMatch prefix string | path-prefix matcher; selected value is / | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "/".

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Matches request paths for the selected route. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `"/"`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The catch-all `/` reaches every path in the virtual host; narrow it when policy requires. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route`

### Short description

Groups the cluster action selected after the route match. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteAction mapping | the child fields shown in this template | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { cluster: app_backend }.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Groups the cluster action selected after the route match. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `{ cluster: app_backend }`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

An over-broad match or unsafe route action can expose an unintended upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster`

### Short description

Routes matching downstream requests to the named upstream cluster. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy RouteAction cluster-name string | name of a declared static_resources.clusters entry; selected value is upstream_service | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures app_backend.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Routes matching downstream requests to the named upstream cluster. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `app_backend`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

The target must be a reviewed local/upstream endpoint; an untrusted target creates an egress path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`

### Short description

Prefixes HCM metrics for the selected ingress listener. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| HttpConnectionManager statistics-prefix string | non-empty metrics namespace token; selected value is msconnector_ext_proc_ingress | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ingress_http.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Observability only; it does not change P1–P4 payload visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Prefixes HCM metrics for the selected ingress listener. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `ingress_http`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Metric names should not embed secrets, user identifiers, or unbounded request data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `compatibility.ext_authz.static_resources.listeners[].name`

### Short description

Names the downstream HTTP listener for Envoy configuration and observability. Compatibility-only host/service setup outside the selected native core path.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].name: <value>
```

### Valid contexts

- Compatibility YAML path only (ext_authz)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy Listener.name string | unique non-empty listener name in this bootstrap | no |

### Default

Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures listener_0.

Source: `compatibility template; selected/native classification`.

### Inheritance and merge

Compatibility-host API behavior; not native connector inheritance.

Merge: Compatibility-host API behavior; not selected native configuration merge.

### Phases and runtime effect

Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.

Names the downstream HTTP listener for Envoy configuration and observability. Compatibility-only host/service setup outside the selected native core path.

### Validation and errors

Validate as an Envoy ext_authz compatibility configuration.

### Example

Selected example value: `listener_0`.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

A name is control-plane metadata, but it should not disclose tenant or secret identifiers. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.

## `envoy.filters.http.ext_authz`

### Short description

Compatibility-only ext_authz filter.

### Syntax

```text
name: envoy.filters.http.ext_authz
```

### Valid contexts

- Compatibility Envoy HTTP filter chain

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Envoy compatibility filter | ext_authz v3 configuration | no |

### Default

not part of selected ext_proc path

Source: `compatibility template`.

### Inheritance and merge

not part of ext_proc configuration

Merge: not part of selected full-lifecycle configuration

### Phases and runtime effect

Request authorization compatibility path; no selected P3/P4 coverage.

Routes to separate authorization compatibility service.

### Validation and errors

Separate ext_authz configuration validation.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Safety and operations

Do not represent it as the native ext_proc full-lifecycle configuration.
