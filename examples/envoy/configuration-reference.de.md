# Envoy-Konfigurationsreferenz

**Sprache:** [English](configuration-reference.md) | Deutsch

## Geltungsbereich und maßgebliche Quellen

Ausgewählter Integrationsmodus: `ext-proc`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.
Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.

## Konfigurationsinventar

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`--check-config`](#check-config) | Umgebung / Laufzeit | Kommandozeilenoption | nein | optional | msconnector_envoy_ext_proc-Kommandozeile | Kommandozeilenoption des ext_proc-Service. |
| [`--config`](#config) | Umgebung / Laufzeit | Kommandozeilenoption | ja | erforderlich | msconnector_envoy_ext_proc-Kommandozeile | Kommandozeilenoption des ext_proc-Service. |
| [`--event-log`](#event-log) | Umgebung / Laufzeit | Kommandozeilenoption | nein | optional | msconnector_envoy_ext_proc-Kommandozeile | Kommandozeilenoption des ext_proc-Service. |
| [`--listen`](#listen) | Umgebung / Laufzeit | Kommandozeilenoption | nein | optional | msconnector_envoy_ext_proc-Kommandozeile | Kommandozeilenoption des ext_proc-Service. |
| [`--runtime-config`](#runtime-config) | Umgebung / Laufzeit | Kommandozeilenoption | nein | optional | msconnector_envoy_ext_proc-Kommandozeile | Kommandozeilenoption des ext_proc-Service. |
| [`@ADMIN_PORT@`](#admin-port) | Beispielplatzhalter | Template-Platzhalter | ja | kein Wert; muss materialisiert werden | Envoy-YAML-Template vor der Materialisierung | Template-Platzhalter, kein Envoy-Konfigurationsfeld. |
| [`@ENVOY_RELEASE@`](#envoy-release) | Beispielplatzhalter | Template-Platzhalter | ja | kein Wert; muss materialisiert werden | Envoy-YAML-Template vor der Materialisierung | Template-Platzhalter, kein Envoy-Konfigurationsfeld. |
| [`@EXT_PROC_PORT@`](#ext-proc-port) | Beispielplatzhalter | Template-Platzhalter | ja | kein Wert; muss materialisiert werden | Envoy-YAML-Template vor der Materialisierung | Template-Platzhalter, kein Envoy-Konfigurationsfeld. |
| [`@LISTEN_PORT@`](#listen-port) | Beispielplatzhalter | Template-Platzhalter | ja | kein Wert; muss materialisiert werden | Envoy-YAML-Template vor der Materialisierung | Template-Platzhalter, kein Envoy-Konfigurationsfeld. |
| [`@UPSTREAM_PORT@`](#upstream-port) | Beispielplatzhalter | Template-Platzhalter | ja | kein Wert; muss materialisiert werden | Envoy-YAML-Template vor der Materialisierung | Template-Platzhalter, kein Envoy-Konfigurationsfeld. |
| [`admin`](#admin) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `admin` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `admin` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads. |
| [`admin.access_log_path`](#admin-access-log-path) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `admin.access_log_path` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `admin.access_log_path` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads. |
| [`admin.address`](#admin-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `admin.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `admin.address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads. |
| [`admin.address.socket_address`](#admin-address-socket-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `admin.address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `admin.address.socket_address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads. |
| [`admin.address.socket_address.address`](#admin-address-socket-address-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `admin.address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `admin.address.socket_address.address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads. |
| [`admin.address.socket_address.port_value`](#admin-address-socket-address-port-value) | Host / Connector | YAML-Portfeld | nein | Der Connector definiert für `admin.address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `admin.address.socket_address.port_value` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads. |
| [`cleanup_timeout_ms`](#cleanup-timeout-ms) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`engine_timeout_ms`](#engine-timeout-ms) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`late_action_policy`](#late-action-policy) | Connector-Service | LateActionPolicy | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Wählt die Protokollierung später Entscheidungen; minimal und safe erfassen späte disruptive Entscheidungen als log_only, während strict strict_abort_not_attempted statt eines erfundenen Status/Resets erfasst. |
| [`listen_address`](#listen-address) | Connector-Service | Zeichenkette | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_body_chunk_bytes`](#max-body-chunk-bytes) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_grpc_message_bytes`](#max-grpc-message-bytes) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_header_count`](#max-header-count) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_header_name_bytes`](#max-header-name-bytes) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_header_value_bytes`](#max-header-value-bytes) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_request_body_bytes`](#max-request-body-bytes) | Connector-Service | 64-Bit-Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_response_body_bytes`](#max-response-body-bytes) | Connector-Service | 64-Bit-Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`max_total_header_bytes`](#max-total-header-bytes) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`shutdown_timeout_ms`](#shutdown-timeout-ms) | Connector-Service | Ganzzahl | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`static_resources`](#static-resources) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads. |
| [`static_resources.clusters`](#static-resources-clusters) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.clusters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].connect_timeout`](#static-resources-clusters-connect-timeout) | Host / Connector | YAML-Zeitlimitfeld | nein | Der Connector definiert für `static_resources.clusters[].connect_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].connect_timeout` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].http2_protocol_options`](#static-resources-clusters-http2-protocol-options) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.clusters[].http2_protocol_options` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].http2_protocol_options` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].load_assignment`](#static-resources-clusters-load-assignment) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].load_assignment.cluster_name`](#static-resources-clusters-load-assignment-cluster-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.cluster_name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.cluster_name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].load_assignment.endpoints`](#static-resources-clusters-load-assignment-endpoints) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`](#static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-port-value) | Host / Connector | YAML-Portfeld | nein | Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.clusters[].name`](#static-resources-clusters-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.clusters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.clusters[].type`](#static-resources-clusters-type) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.clusters[].type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.clusters[].type` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`static_resources.listeners`](#static-resources-listeners) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.listeners` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].address`](#static-resources-listeners-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `static_resources.listeners[].address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].address.socket_address`](#static-resources-listeners-address-socket-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `static_resources.listeners[].address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].address.socket_address.address`](#static-resources-listeners-address-socket-address-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `static_resources.listeners[].address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].address.socket_address.port_value`](#static-resources-listeners-address-socket-address-port-value) | Host / Connector | YAML-Portfeld | nein | Der Connector definiert für `static_resources.listeners[].address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains`](#static-resources-listeners-filter-chains) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters`](#static-resources-listeners-filter-chains-filters) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].name`](#static-resources-listeners-filter-chains-filters-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config`](#static-resources-listeners-filter-chains-filters-typed-config) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.@type`](#static-resources-listeners-filter-chains-filters-typed-config-type) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-type) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-allow-mode-override) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-failure-mode-allow) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service-envoy-grpc) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service-envoy-grpc-cluster-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-grpc-service-timeout) | Host / Connector | YAML-Zeitlimitfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-max-message-timeout) | Host / Connector | YAML-Zeitlimitfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-message-timeout) | Host / Connector | YAML-Zeitlimitfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-request-body-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-request-header-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-request-trailer-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-response-body-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-response-header-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-processing-mode-response-trailer-mode) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-request-attributes) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-request-attributes) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response`](#static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-send-body-without-waiting-for-header-response) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`](#static-resources-listeners-filter-chains-filters-typed-config-route-config) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-prefix) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-route) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster`](#static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-route-cluster) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`](#static-resources-listeners-filter-chains-filters-typed-config-stat-prefix) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`static_resources.listeners[].name`](#static-resources-listeners-name) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `static_resources.listeners[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `static_resources.listeners[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`transaction_id_header`](#transaction-id-header) | Connector-Service | Zeichenkette | ja | kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld | ext_proc-Service-JSON-Objekt | Setzt eine begrenzte ext_proc-Service-Steuerung. |
| [`compatibility.ext_authz.static_resources`](#compatibility-ext-authz-static-resources) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources` konfiguriert die Kompatibilitätsintegration. Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads. |
| [`compatibility.ext_authz.static_resources.clusters`](#compatibility-ext-authz-static-resources-clusters) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].connect_timeout`](#compatibility-ext-authz-static-resources-clusters-connect-timeout) | Kompatibilität | YAML-Zeitlimitfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].connect_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].connect_timeout` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].connect_timeout` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment`](#compatibility-ext-authz-static-resources-clusters-load-assignment) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name`](#compatibility-ext-authz-static-resources-clusters-load-assignment-cluster-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`](#compatibility-ext-authz-static-resources-clusters-load-assignment-endpoints-lb-endpoints-endpoint-address-socket-address-port-value) | Kompatibilität | YAML-Portfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.clusters[].name`](#compatibility-ext-authz-static-resources-clusters-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.clusters[].type`](#compatibility-ext-authz-static-resources-clusters-type) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].type` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].type` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.ext_authz.static_resources.listeners`](#compatibility-ext-authz-static-resources-listeners) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].address`](#compatibility-ext-authz-static-resources-listeners-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].address.socket_address`](#compatibility-ext-authz-static-resources-listeners-address-socket-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address.socket_address` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].address.socket_address.address`](#compatibility-ext-authz-static-resources-listeners-address-socket-address-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value`](#compatibility-ext-authz-static-resources-listeners-address-socket-address-port-value) | Kompatibilität | YAML-Portfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains`](#compatibility-ext-authz-static-resources-listeners-filter-chains) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-type) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-type) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request-allowed-headers) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request-allowed-headers-patterns) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-authorization-request-allowed-headers-patterns-exact) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri-cluster) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri-timeout) | Kompatibilität | YAML-Zeitlimitfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-http-filters-typed-config-http-service-server-uri-uri) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-domains) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-match-prefix) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-route) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-route-config-virtual-hosts-routes-route-cluster) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`](#compatibility-ext-authz-static-resources-listeners-filter-chains-filters-typed-config-stat-prefix) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.ext_authz.static_resources.listeners[].name`](#compatibility-ext-authz-static-resources-listeners-name) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].name` im ausgewählten Envoy-Template. | Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`envoy.filters.http.ext_authz`](#envoy-filters-http-ext-authz) | Kompatibilität | Envoy-Kompatibilitätsfilter | nein | nicht Teil des ausgewählten ext_proc-Pfads | Kompatibilitäts-Envoy-HTTP-Filterkette | ext_authz-Filter nur für die Kompatibilität. |

## Trennung der Ebenen

Host-/Connector-Schalter binden oder konfigurieren die Hostintegration. Sie sind nicht identisch mit `SecRuleEngine`.

- [Common-Runtime-Konfiguration](../common/common-connector-configuration.de.md) beschreibt nur die `key=value`-Runtime-Datei und wird nicht als nicht registrierte Hostdirektive ausgegeben.
- [ModSecurity-Engine-Direktiven](../common/modsecurity-directives.de.md) beschreibt die `Sec*`-Direktiven der geladenen Regeldatei.
- [Regelbeispiele](../common/rule-examples.de.md) erklären DetectionOnly und das Abschalten der Engine.

## Common-Runtime-Relevanz

| Schlüssel | Lokale Verwendung | Detailreferenz |
| --- | --- | --- |
| `enabled` | Schlüssel des ausgewählten Runtime-Profils | [enabled](../common/common-connector-configuration.de.md#enabled) |
| `rules_file` | Schlüssel des ausgewählten Runtime-Profils | [rules_file](../common/common-connector-configuration.de.md#rules-file) |
| `transaction_id_header` | Schlüssel des ausgewählten Runtime-Profils | [transaction_id_header](../common/common-connector-configuration.de.md#transaction-id-header) |
| `request_body_mode` | Schlüssel des ausgewählten Runtime-Profils | [request_body_mode](../common/common-connector-configuration.de.md#request-body-mode) |
| `response_body_mode` | Schlüssel des ausgewählten Runtime-Profils | [response_body_mode](../common/common-connector-configuration.de.md#response-body-mode) |
| `request_body_limit` | Schlüssel des ausgewählten Runtime-Profils | [request_body_limit](../common/common-connector-configuration.de.md#request-body-limit) |
| `response_body_limit` | Schlüssel des ausgewählten Runtime-Profils | [response_body_limit](../common/common-connector-configuration.de.md#response-body-limit) |
| `body_limit_action` | Schlüssel des ausgewählten Runtime-Profils | [body_limit_action](../common/common-connector-configuration.de.md#body-limit-action) |
| `phase4_mode` | Schlüssel des ausgewählten Runtime-Profils | [phase4_mode](../common/common-connector-configuration.de.md#phase4-mode) |
| `default_block_status` | Schlüssel des ausgewählten Runtime-Profils | [default_block_status](../common/common-connector-configuration.de.md#default-block-status) |
| `default_error_status` | Schlüssel des ausgewählten Runtime-Profils | [default_error_status](../common/common-connector-configuration.de.md#default-error-status) |
| `use_error_log` | Schlüssel des ausgewählten Runtime-Profils | [use_error_log](../common/common-connector-configuration.de.md#use-error-log) |
| `max_header_count` | Schlüssel des ausgewählten Runtime-Profils | [max_header_count](../common/common-connector-configuration.de.md#max-header-count) |
| `max_header_name_size` | Schlüssel des ausgewählten Runtime-Profils | [max_header_name_size](../common/common-connector-configuration.de.md#max-header-name-size) |
| `max_header_value_size` | Schlüssel des ausgewählten Runtime-Profils | [max_header_value_size](../common/common-connector-configuration.de.md#max-header-value-size) |
| `max_total_header_bytes` | Schlüssel des ausgewählten Runtime-Profils | [max_total_header_bytes](../common/common-connector-configuration.de.md#max-total-header-bytes) |
| `max_event_json_bytes` | Schlüssel des ausgewählten Runtime-Profils | [max_event_json_bytes](../common/common-connector-configuration.de.md#max-event-json-bytes) |

## Von Profilen verwendete Engine-Direktiven

Die lokalen Regelprofile verwenden `SecRuleEngine` für On, DetectionOnly und Off. Wo Body-Inspektion gewählt wird, bleiben `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME-Scope, Limits und `SecRule` ModSecurity-Engine-Direktiven.

Siehe [Engine-Referenz](../common/modsecurity-directives.de.md).

## Profile

| Profil | Datei | Status |
| --- | --- | --- |
| Minimal | [minimal/envoy-ext-proc-streaming.yaml.in](minimal/envoy-ext-proc-streaming.yaml.in) | Aktive Startkonfiguration |
| Sicherer vollständiger Lebenszyklus | [safe/envoy-ext-proc-streaming.yaml.in](safe/envoy-ext-proc-streaming.yaml.in) | Ausgewählte begrenzte Referenz |
| Strikt | [strict/README.de.md](strict/README.de.md) | Parserunterstützte oder ausdrücklich optionale Grenze |
| DetectionOnly | [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Engine wertet aus/protokolliert ohne disruptive Aktion |
| Deaktiviert | [disabled/msconnector-runtime.conf](disabled/msconnector-runtime.conf) | Connector- oder Engine-Pfad deaktiviert |

## Konfigurationskombinationen

| Connector | Engine | Request-Body | Response-Body | Ergebnis |
| --- | --- | --- | --- | --- |
| off | On | beliebig | beliebig | Keine Connector-Transaktion; die Engine-Einstellung wird nicht erreicht. |
| on | Off | beliebig | beliebig | Der Connector erreicht die Engine, aber deren Regelauswertung ist deaktiviert. |
| on | DetectionOnly | aktiviert | aktiviert | Regeln können ohne disruptive Durchsetzung treffen/protokollieren. |
| on | On | Off | On | Der P2-Body steht der Engine nicht zur Verfügung; P4 bleibt host-/fähigkeitsabhängig. |
| on | On | On | Off | Der P4-Body steht der Engine nicht zur Verfügung. |
| on | On | On | On + safe | Späte P4-Ergebnisse nach dem Commit werden ohne zugesagte spätere Statusänderung aufgezeichnet. |
| on | On | On | On + strict | Ein hostspezifisches strict-Ergebnis nur verwenden, wenn Quelle/Nachweis es stützen; keine künstliche spätere 403. |
| on | On | über Limit + process_partial | über Limit + reject | Die Body-Policy bestimmt die begrenzte Engine-Eingabe; die genaue Host-Response-Behandlung bleibt connectorspezifisch. |

## Validierung

```sh
envoy --mode validate -c <generated-config>
```

Repository-Ziele: `make check-config-envoy` und `make check-config-all-connectors`.

## Optionsdetails

## `--check-config`

### Kurzbeschreibung

Kommandozeilenoption des ext_proc-Service.

### Syntax

```text
--check-config
```

### Gültige Kontexte

- msconnector_envoy_ext_proc-Kommandozeile

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kommandozeilenoption | siehe CLI-Verwendung; gegebenenfalls Pfad/host:port | nein |

### Standardwert

optional

Quelle: `Flag-Registrierung in main.go`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: --listen überschreibt listen_address nach dem JSON-Dekodieren; andere Optionen sind direkte Prozesseingaben.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Runtime-Serviceeinrichtung; --runtime-config wählt den tatsächlichen Engine-Pfad.

Steuert Start- und Prüfverhalten des ext_proc-Service.

### Validierung und Fehler

main validiert JSON und, sofern ausgewählt, die Common Runtime vor dem Bereitstellen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Sicherheit und Betrieb

Absolute kontrollierte Pfade für Runtime-/Ereignisdateien und einen privaten Service-Listener verwenden.

## `--config`

### Kurzbeschreibung

Kommandozeilenoption des ext_proc-Service.

### Syntax

```text
--config PATH
```

### Gültige Kontexte

- msconnector_envoy_ext_proc-Kommandozeile

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kommandozeilenoption | siehe CLI-Verwendung; gegebenenfalls Pfad/host:port | ja |

### Standardwert

erforderlich

Quelle: `Flag-Registrierung in main.go`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: --listen überschreibt listen_address nach dem JSON-Dekodieren; andere Optionen sind direkte Prozesseingaben.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Runtime-Serviceeinrichtung; --runtime-config wählt den tatsächlichen Engine-Pfad.

Steuert Start- und Prüfverhalten des ext_proc-Service.

### Validierung und Fehler

main validiert JSON und, sofern ausgewählt, die Common Runtime vor dem Bereitstellen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Sicherheit und Betrieb

Absolute kontrollierte Pfade für Runtime-/Ereignisdateien und einen privaten Service-Listener verwenden.

## `--event-log`

### Kurzbeschreibung

Kommandozeilenoption des ext_proc-Service.

### Syntax

```text
--event-log PATH
```

### Gültige Kontexte

- msconnector_envoy_ext_proc-Kommandozeile

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kommandozeilenoption | siehe CLI-Verwendung; gegebenenfalls Pfad/host:port | nein |

### Standardwert

optional

Quelle: `Flag-Registrierung in main.go`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: --listen überschreibt listen_address nach dem JSON-Dekodieren; andere Optionen sind direkte Prozesseingaben.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Runtime-Serviceeinrichtung; --runtime-config wählt den tatsächlichen Engine-Pfad.

Steuert Start- und Prüfverhalten des ext_proc-Service.

### Validierung und Fehler

main validiert JSON und, sofern ausgewählt, die Common Runtime vor dem Bereitstellen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Sicherheit und Betrieb

Absolute kontrollierte Pfade für Runtime-/Ereignisdateien und einen privaten Service-Listener verwenden.

## `--listen`

### Kurzbeschreibung

Kommandozeilenoption des ext_proc-Service.

### Syntax

```text
--listen PATH
```

### Gültige Kontexte

- msconnector_envoy_ext_proc-Kommandozeile

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kommandozeilenoption | siehe CLI-Verwendung; gegebenenfalls Pfad/host:port | nein |

### Standardwert

optional

Quelle: `Flag-Registrierung in main.go`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: --listen überschreibt listen_address nach dem JSON-Dekodieren; andere Optionen sind direkte Prozesseingaben.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Runtime-Serviceeinrichtung; --runtime-config wählt den tatsächlichen Engine-Pfad.

Steuert Start- und Prüfverhalten des ext_proc-Service.

### Validierung und Fehler

main validiert JSON und, sofern ausgewählt, die Common Runtime vor dem Bereitstellen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Sicherheit und Betrieb

Absolute kontrollierte Pfade für Runtime-/Ereignisdateien und einen privaten Service-Listener verwenden.

## `--runtime-config`

### Kurzbeschreibung

Kommandozeilenoption des ext_proc-Service.

### Syntax

```text
--runtime-config PATH
```

### Gültige Kontexte

- msconnector_envoy_ext_proc-Kommandozeile

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Kommandozeilenoption | siehe CLI-Verwendung; gegebenenfalls Pfad/host:port | nein |

### Standardwert

optional

Quelle: `Flag-Registrierung in main.go`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: --listen überschreibt listen_address nach dem JSON-Dekodieren; andere Optionen sind direkte Prozesseingaben.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Runtime-Serviceeinrichtung; --runtime-config wählt den tatsächlichen Engine-Pfad.

Steuert Start- und Prüfverhalten des ext_proc-Service.

### Validierung und Fehler

main validiert JSON und, sofern ausgewählt, die Common Runtime vor dem Bereitstellen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`.

### Sicherheit und Betrieb

Absolute kontrollierte Pfade für Runtime-/Ereignisdateien und einen privaten Service-Listener verwenden.

## `@ADMIN_PORT@`

### Kurzbeschreibung

Template-Platzhalter, kein Envoy-Konfigurationsfeld.

### Syntax

```text
@ADMIN_PORT@
```

### Gültige Kontexte

- Envoy-YAML-Template vor der Materialisierung

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Template-Platzhalter | vom Materializer bereitgestellter und validierter Wert | ja |

### Standardwert

kein Wert; muss materialisiert werden

Quelle: `Template enthält einen erforderlichen Platzhalter`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: wird einmalig durch den Repository-Materializer ersetzt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Host-Bootstrap.

Liefert der erzeugten Envoy-Konfiguration einen Release-Marker oder lokalen Endpunktwert.

### Validierung und Fehler

Der Materializer weist unaufgelöste Platzhalter und ungültige Ports ab; die Ausgabe muss außerhalb des Checkouts liegen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Private, konfliktfreie Ports verwenden; erzeugte Runtime-Ausgabe nie im Checkout ablegen.

## `@ENVOY_RELEASE@`

### Kurzbeschreibung

Template-Platzhalter, kein Envoy-Konfigurationsfeld.

### Syntax

```text
@ENVOY_RELEASE@
```

### Gültige Kontexte

- Envoy-YAML-Template vor der Materialisierung

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Template-Platzhalter | vom Materializer bereitgestellter und validierter Wert | ja |

### Standardwert

kein Wert; muss materialisiert werden

Quelle: `Template enthält einen erforderlichen Platzhalter`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: wird einmalig durch den Repository-Materializer ersetzt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Host-Bootstrap.

Liefert der erzeugten Envoy-Konfiguration einen Release-Marker oder lokalen Endpunktwert.

### Validierung und Fehler

Der Materializer weist unaufgelöste Platzhalter und ungültige Ports ab; die Ausgabe muss außerhalb des Checkouts liegen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Private, konfliktfreie Ports verwenden; erzeugte Runtime-Ausgabe nie im Checkout ablegen.

## `@EXT_PROC_PORT@`

### Kurzbeschreibung

Template-Platzhalter, kein Envoy-Konfigurationsfeld.

### Syntax

```text
@EXT_PROC_PORT@
```

### Gültige Kontexte

- Envoy-YAML-Template vor der Materialisierung

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Template-Platzhalter | vom Materializer bereitgestellter und validierter Wert | ja |

### Standardwert

kein Wert; muss materialisiert werden

Quelle: `Template enthält einen erforderlichen Platzhalter`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: wird einmalig durch den Repository-Materializer ersetzt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Host-Bootstrap.

Liefert der erzeugten Envoy-Konfiguration einen Release-Marker oder lokalen Endpunktwert.

### Validierung und Fehler

Der Materializer weist unaufgelöste Platzhalter und ungültige Ports ab; die Ausgabe muss außerhalb des Checkouts liegen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Private, konfliktfreie Ports verwenden; erzeugte Runtime-Ausgabe nie im Checkout ablegen.

## `@LISTEN_PORT@`

### Kurzbeschreibung

Template-Platzhalter, kein Envoy-Konfigurationsfeld.

### Syntax

```text
@LISTEN_PORT@
```

### Gültige Kontexte

- Envoy-YAML-Template vor der Materialisierung

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Template-Platzhalter | vom Materializer bereitgestellter und validierter Wert | ja |

### Standardwert

kein Wert; muss materialisiert werden

Quelle: `Template enthält einen erforderlichen Platzhalter`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: wird einmalig durch den Repository-Materializer ersetzt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Host-Bootstrap.

Liefert der erzeugten Envoy-Konfiguration einen Release-Marker oder lokalen Endpunktwert.

### Validierung und Fehler

Der Materializer weist unaufgelöste Platzhalter und ungültige Ports ab; die Ausgabe muss außerhalb des Checkouts liegen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Private, konfliktfreie Ports verwenden; erzeugte Runtime-Ausgabe nie im Checkout ablegen.

## `@UPSTREAM_PORT@`

### Kurzbeschreibung

Template-Platzhalter, kein Envoy-Konfigurationsfeld.

### Syntax

```text
@UPSTREAM_PORT@
```

### Gültige Kontexte

- Envoy-YAML-Template vor der Materialisierung

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Template-Platzhalter | vom Materializer bereitgestellter und validierter Wert | ja |

### Standardwert

kein Wert; muss materialisiert werden

Quelle: `Template enthält einen erforderlichen Platzhalter`.

### Vererbung und Zusammenführung

nicht anwendbar

Zusammenführung: wird einmalig durch den Repository-Materializer ersetzt.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Nur Host-Bootstrap.

Liefert der erzeugten Envoy-Konfiguration einen Release-Marker oder lokalen Endpunktwert.

### Validierung und Fehler

Der Materializer weist unaufgelöste Platzhalter und ungültige Ports ab; die Ausgabe muss außerhalb des Checkouts liegen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Private, konfliktfreie Ports verwenden; erzeugte Runtime-Ausgabe nie im Checkout ablegen.

## `admin`

### Kurzbeschreibung

Das YAML-Feld `admin` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Syntax

```text
admin: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `admin` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `admin` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `admin` die administrative Envoy-Schnittstelle konfiguriert.

Das YAML-Feld `admin` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Admin mapping
allowed_values: access_log_path and address child fields
default: No connector-owned admin configuration default is declared; the selected template sets a loopback listener with /dev/null access log.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Management plane only; it does not create or alter P1–P4 callbacks.
security_relevance: Admin exposure is a separate privileged surface and must remain private in the example.
runtime_effect: Groups Envoy management-interface configuration.
description: Groups Envoy management-interface configuration.
```

## `admin.access_log_path`

### Kurzbeschreibung

Das YAML-Feld `admin.access_log_path` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Syntax

```text
admin.access_log_path: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `admin.access_log_path` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `admin.access_log_path` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `admin.access_log_path` die administrative Envoy-Schnittstelle konfiguriert.

Das YAML-Feld `admin.access_log_path` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `/dev/null`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: filesystem path string
allowed_values: writable path accepted by Envoy; selected value is /dev/null
default: No connector-owned admin access-log path default is declared; the selected template sets /dev/null.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Management-plane only; it does not alter P1–P4 ext_proc visibility.
security_relevance: Administrative logs can contain operational metadata; /dev/null suppresses them in this example rather than providing an audit design.
runtime_effect: Selects where Envoy writes administrative HTTP access records.
description: Selects where Envoy writes administrative HTTP access records.
```

## `admin.address`

### Kurzbeschreibung

Das YAML-Feld `admin.address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Syntax

```text
admin.address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `admin.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `admin.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `admin.address` die administrative Envoy-Schnittstelle konfiguriert.

Das YAML-Feld `admin.address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy admin core.Address mapping
allowed_values: one supported address form; selected form is a loopback socket_address
default: No connector-owned admin address default is declared; the selected template sets 127.0.0.1 and @ADMIN_PORT@.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Management-plane only; independent of P1–P4 transaction processing.
security_relevance: Admin endpoints are sensitive; keep the selected listener loopback/private.
runtime_effect: Groups the Envoy administration listener address.
description: Groups the Envoy administration listener address.
```

## `admin.address.socket_address`

### Kurzbeschreibung

Das YAML-Feld `admin.address.socket_address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Syntax

```text
admin.address.socket_address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `admin.address.socket_address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `admin.address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `admin.address.socket_address` die administrative Envoy-Schnittstelle konfiguriert.

Das YAML-Feld `admin.address.socket_address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy admin SocketAddress mapping
allowed_values: address and port_value child fields
default: No connector-owned admin socket-address default is declared; the selected template sets 127.0.0.1 plus @ADMIN_PORT@.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Management-plane only; independent of P1–P4 transaction processing.
security_relevance: Do not bind the administration socket publicly without a separate access-control design.
runtime_effect: Pairs the Envoy administration host and TCP port.
description: Pairs the Envoy administration host and TCP port.
```

## `admin.address.socket_address.address`

### Kurzbeschreibung

Das YAML-Feld `admin.address.socket_address.address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Syntax

```text
admin.address.socket_address.address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `admin.address.socket_address.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `admin.address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `admin.address.socket_address.address` die administrative Envoy-Schnittstelle konfiguriert.

Das YAML-Feld `admin.address.socket_address.address` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `127.0.0.1`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy admin host/IP string
allowed_values: valid host or IP literal; selected value is 127.0.0.1
default: No connector-owned admin host default is declared; the selected template sets 127.0.0.1.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Management-plane only; independent of P1–P4 transaction processing.
security_relevance: Loopback prevents the example admin interface from being reachable remotely.
runtime_effect: Binds the Envoy administration listener to the selected interface.
description: Binds the Envoy administration listener to the selected interface.
```

## `admin.address.socket_address.port_value`

### Kurzbeschreibung

Das YAML-Feld `admin.address.socket_address.port_value` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Syntax

```text
admin.address.socket_address.port_value: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Portfeld | Die zulässige Ausprägung von `admin.address.socket_address.port_value` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `admin.address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `admin.address.socket_address.port_value` die administrative Envoy-Schnittstelle konfiguriert.

Das YAML-Feld `admin.address.socket_address.port_value` konfiguriert die administrative Envoy-Schnittstelle. Sie konfiguriert die administrative Listener- oder Protokollierungsseite außerhalb des Datenpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `@ADMIN_PORT@`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Administrative Endpunkte und Logs müssen privat bleiben und dürfen nicht ohne ausdrückliches Deployment-Konzept freigegeben werden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy admin uint32 TCP port
allowed_values: materializer-validated decimal port 1..65535
default: No connector-owned admin port default is declared; the selected template sets the @ADMIN_PORT@ materializer input.
default_source: selected template and prepare_envoy_ext_proc_config.sh materializer
phase_relevance: Management-plane only; independent of P1–P4 transaction processing.
security_relevance: Use a private, non-conflicting port; exposing admin APIs is unrelated to ModSecurity enforcement.
runtime_effect: Selects the local TCP port for Envoy administration endpoints.
description: Selects the local TCP port for Envoy administration endpoints.
```

## `cleanup_timeout_ms`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"cleanup_timeout_ms": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `1000`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `engine_timeout_ms`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"engine_timeout_ms": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `150`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `late_action_policy`

### Kurzbeschreibung

Wählt die Protokollierung später Entscheidungen; minimal und safe erfassen späte disruptive Entscheidungen als log_only, während strict strict_abort_not_attempted statt eines erfundenen Status/Resets erfasst.

### Syntax

```text
"late_action_policy": <LateActionPolicy>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| LateActionPolicy | minimal \| safe \| strict | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Wählt die Protokollierung später Entscheidungen; minimal und safe erfassen späte disruptive Entscheidungen als log_only, während strict strict_abort_not_attempted statt eines erfundenen Status/Resets erfasst.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `"safe"`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `listen_address`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"listen_address": <string>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | nichtleeres host:port | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `"127.0.0.1:18083"`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_body_chunk_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_body_chunk_bytes": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `1048576`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_grpc_message_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_grpc_message_bytes": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `1114112`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_header_count`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_header_count": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `128`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_header_name_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_header_name_bytes": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `256`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_header_value_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_header_value_bytes": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `8192`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_request_body_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_request_body_bytes": <int64>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| 64-Bit-Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `10485760`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_response_body_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_response_body_bytes": <int64>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| 64-Bit-Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `10485760`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `max_total_header_bytes`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"max_total_header_bytes": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `32768`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `shutdown_timeout_ms`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"shutdown_timeout_ms": <int>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Ganzzahl | positiver Wert | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `5000`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `static_resources`

### Kurzbeschreibung

Das YAML-Feld `static_resources` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.

### Syntax

```text
static_resources: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources` die Host-/Connector-YAML-Konfiguration konfiguriert.

Das YAML-Feld `static_resources` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Die Auswirkung auf Netzwerk, Routing und Policy vor dem Einsatz mit dem dokumentierten Template und Quellanker prüfen.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Bootstrap static_resources mapping
allowed_values: listener and cluster child mappings shown in the template
default: No connector-owned static-resource set default is declared; the selected template sets the explicit listener and static clusters.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap establishes the selected ext_proc P1–P4 path but does not itself process a transaction.
security_relevance: All listener and cluster children affect traffic exposure or destination; review as one topology.
runtime_effect: Declares the complete static data-plane topology used by the checked-in example.
description: Declares the complete static data-plane topology used by the checked-in example.
```

## `static_resources.clusters`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.clusters` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Cluster mapping
allowed_values: one or more Cluster objects; selected template declares upstream_service and msconnector_ext_proc
default: No connector-owned cluster list default is declared; the selected template sets the explicit upstream and local processor clusters.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: upstream_service provides the request/response path; msconnector_ext_proc transports selected P1–P4 callbacks.
security_relevance: Clusters define where application traffic and inspection data can leave the listener.
runtime_effect: Declares the static service destinations used by routing and ext_proc gRPC.
description: Declares the static service destinations used by routing and ext_proc gRPC.
```

## `static_resources.clusters[].connect_timeout`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].connect_timeout` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].connect_timeout: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Zeitlimitfeld | Die zulässige Ausprägung von `static_resources.clusters[].connect_timeout` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].connect_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].connect_timeout` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].connect_timeout` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `0.5s`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy protobuf Duration for cluster connection attempts
allowed_values: non-negative duration; selected native value is 0.5s (compatibility example uses 0.25s)
default: No connector-owned cluster connect timeout default is declared; the selected template sets the explicit template duration.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: A long timeout retains connections; a short timeout can trigger processor failures or upstream unavailability.
runtime_effect: Bounds TCP connection establishment to the upstream or local processor endpoint.
description: Bounds TCP connection establishment to the upstream or local processor endpoint.
```

## `static_resources.clusters[].http2_protocol_options`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].http2_protocol_options` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].http2_protocol_options: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.clusters[].http2_protocol_options` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].http2_protocol_options` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].http2_protocol_options` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].http2_protocol_options` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `{}`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Http2ProtocolOptions mapping
allowed_values: empty or configured HTTP/2 options; selected value is {} on the ext_proc cluster
default: Absent unless configured; the selected ext_proc cluster explicitly sets an empty HTTP/2 options mapping.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Transport prerequisite for the ext_proc bidirectional stream carrying P1–P4 callbacks.
security_relevance: Do not remove HTTP/2 support from the selected gRPC processor cluster.
runtime_effect: Enables the HTTP/2 protocol options needed by the Envoy gRPC ext_proc cluster.
description: Enables the HTTP/2 protocol options needed by the Envoy gRPC ext_proc cluster.
```

## `static_resources.clusters[].load_assignment`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].load_assignment: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ClusterLoadAssignment mapping
allowed_values: cluster_name plus endpoint/lb_endpoints children
default: No connector-owned static load assignment default is declared; the selected template sets the explicit loopback endpoint set.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: Endpoint assignments are egress/control-plane inputs; review every address and port.
runtime_effect: Groups the endpoints assigned to a static cluster.
description: Groups the endpoints assigned to a static cluster.
```

## `static_resources.clusters[].load_assignment.cluster_name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.cluster_name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].load_assignment.cluster_name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.cluster_name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.cluster_name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.cluster_name` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.cluster_name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `upstream_service, msconnector_ext_proc`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ClusterLoadAssignment.cluster_name string
allowed_values: must match the enclosing Cluster.name; selected values match upstream_service or msconnector_ext_proc
default: No connector-owned load-assignment cluster name default is declared; the selected template sets the enclosing static cluster name.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: A mismatch invalidates or misroutes the endpoint configuration.
runtime_effect: Associates the endpoint assignment with its enclosing cluster.
description: Associates the endpoint assignment with its enclosing cluster.
```

## `static_resources.clusters[].load_assignment.endpoints`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy LocalityLbEndpoints mapping
allowed_values: one or more locality endpoint groups; the example has one group
default: No connector-owned endpoint-group list default is declared; the selected template sets one loopback locality group.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: Each endpoint is a traffic destination; preserve the intended private scope.
runtime_effect: Groups load-balanced endpoints for the static cluster.
description: Groups load-balanced endpoints for the static cluster.
```

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy LbEndpoint mapping
allowed_values: one or more endpoint mappings; the example has one endpoint per cluster
default: No connector-owned load-balancer endpoint list default is declared; the selected template sets one explicit loopback endpoint.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: An added endpoint receives copied requests or ext_proc messages; require explicit trust review.
runtime_effect: Defines endpoint candidates selected by Envoy's cluster load balancer.
description: Defines endpoint candidates selected by Envoy's cluster load balancer.
```

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Endpoint mapping
allowed_values: endpoint address child mapping
default: No connector-owned endpoint object default is declared; the selected template sets the explicit loopback socket address.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: The endpoint is a concrete traffic target and must be constrained to the intended service.
runtime_effect: Contains the network address of one cluster endpoint.
description: Contains the network address of one cluster endpoint.
```

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.Address mapping
allowed_values: one supported Envoy address form; selected form is socket_address
default: No connector-owned cluster endpoint address default is declared; the selected template sets a loopback socket_address mapping.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: Changing it changes egress or inspection-service reachability.
runtime_effect: Contains the TCP address for one upstream or ext_proc service endpoint.
description: Contains the TCP address for one upstream or ext_proc service endpoint.
```

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.SocketAddress mapping
allowed_values: address and port_value child fields
default: No connector-owned cluster endpoint socket-address default is declared; the selected template sets 127.0.0.1 plus its materialized port.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: The selected loopback values keep both upstream and processor endpoint examples local.
runtime_effect: Pairs the static cluster endpoint host and TCP port.
description: Pairs the static cluster endpoint host and TCP port.
```

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `127.0.0.1`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress host/IP string
allowed_values: valid endpoint host or IP literal; selected value is 127.0.0.1
default: No connector-owned cluster endpoint host default is declared; the selected template sets 127.0.0.1.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: Loopback avoids external egress in the example; a remote host needs transport and trust controls.
runtime_effect: Targets the static upstream or ext_proc endpoint host.
description: Targets the static upstream or ext_proc endpoint host.
```

## `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Portfeld | Die zulässige Ausprägung von `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `@UPSTREAM_PORT@, @EXT_PROC_PORT@`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress uint32 TCP port
allowed_values: materializer-validated decimal port 1..65535
default: No connector-owned cluster endpoint port default is declared; the selected template sets the @UPSTREAM_PORT@ or @EXT_PROC_PORT@ materializer input.
default_source: selected template and prepare_envoy_ext_proc_config.sh materializer
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: Port changes can send traffic to a different local service; retain explicit private service ownership.
runtime_effect: Targets the TCP port of the selected upstream or ext_proc endpoint.
description: Targets the TCP port of the selected upstream or ext_proc endpoint.
```

## `static_resources.clusters[].name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.clusters[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].name` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `upstream_service, msconnector_ext_proc`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Cluster.name string
allowed_values: unique non-empty cluster name; selected values are upstream_service and msconnector_ext_proc
default: No connector-owned cluster-name default is declared; the selected template sets the two named static clusters.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: upstream_service supplies the normal request/response flow; msconnector_ext_proc carries P1–P4 processor traffic.
security_relevance: Cluster names resolve traffic destinations; do not redirect an inspection target to an unreviewed service.
runtime_effect: Names a static endpoint group referenced by the route or ext_proc gRPC service.
description: Names a static endpoint group referenced by the route or ext_proc gRPC service.
```

## `static_resources.clusters[].type`

### Kurzbeschreibung

Das YAML-Feld `static_resources.clusters[].type` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
static_resources.clusters[].type: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.clusters[].type` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.clusters[].type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.clusters[].type` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `static_resources.clusters[].type` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `STATIC`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Cluster DiscoveryType enum
allowed_values: Envoy discovery type; selected native value STATIC, compatibility values STRICT_DNS
default: No connector-owned cluster discovery type default is declared; the selected template sets STATIC for the selected native local endpoints.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected cluster list contains upstream_service, which receives the post-request-filter flow and returns the response seen at P3/P4, and msconnector_ext_proc, which transports selected P1/P2/P3/P4 callbacks.
security_relevance: STATIC keeps the selected endpoints explicit; DNS discovery changes endpoint resolution and should be reviewed for egress/identity impact.
runtime_effect: Determines how Envoy resolves the endpoint set for the named cluster.
description: Determines how Envoy resolves the endpoint set for the named cluster.
```

## `static_resources.listeners`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.listeners` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Listener mapping
allowed_values: one or more Listener objects; selected template declares one loopback HTTP listener
default: No connector-owned listener list default is declared; the selected template sets one msconnector_ext_proc_listener.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap container for the filter chain that exposes selected P1–P4 ext_proc callbacks.
security_relevance: A listener changes the network attack surface before request policy is reached.
runtime_effect: Declares the downstream listener objects present in the static bootstrap.
description: Declares the downstream listener objects present in the static bootstrap.
```

## `static_resources.listeners[].address`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `static_resources.listeners[].address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.Address mapping
allowed_values: one supported Envoy address form; the example selects socket_address
default: No connector-owned listener-address default is declared; the selected template sets a loopback socket_address mapping.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: Changing the child socket address changes network exposure before any ModSecurity processing.
runtime_effect: Contains the downstream listener bind address used before the HTTP filter chain runs.
description: Contains the downstream listener bind address used before the HTTP filter chain runs.
```

## `static_resources.listeners[].address.socket_address`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].address.socket_address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `static_resources.listeners[].address.socket_address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].address.socket_address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.SocketAddress mapping
allowed_values: address plus port_value (or another Envoy-supported socket-address form)
default: No connector-owned listener socket-address default is declared; the selected template sets 127.0.0.1 and @LISTEN_PORT@.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: The selected loopback pair keeps the example private; a wildcard bind requires an explicit exposure decision.
runtime_effect: Pairs the listener host and TCP port that accept downstream traffic.
description: Pairs the listener host and TCP port that accept downstream traffic.
```

## `static_resources.listeners[].address.socket_address.address`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].address.socket_address.address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `static_resources.listeners[].address.socket_address.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].address.socket_address.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `127.0.0.1`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress host/IP string
allowed_values: a valid listener host or IP literal; selected value is 127.0.0.1
default: No connector-owned listener host default is declared; the selected template sets 127.0.0.1.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: The selected value is loopback-only.
runtime_effect: Binds the downstream HTTP listener to the selected network interface.
description: Binds the downstream HTTP listener to the selected network interface.
```

## `static_resources.listeners[].address.socket_address.port_value`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].address.socket_address.port_value: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Portfeld | Die zulässige Ausprägung von `static_resources.listeners[].address.socket_address.port_value` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].address.socket_address.port_value` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `@LISTEN_PORT@`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress uint32 TCP port
allowed_values: materializer-validated decimal port 1..65535
default: No connector-owned listener port default is declared; the selected template sets the @LISTEN_PORT@ materializer input.
default_source: selected template and prepare_envoy_ext_proc_config.sh materializer
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: Use a private, non-conflicting port; port selection affects reachability before P1.
runtime_effect: Selects the TCP port on which downstream requests enter the ext_proc filter chain.
description: Selects the TCP port on which downstream requests enter the ext_proc filter chain.
```

## `static_resources.listeners[].filter_chains`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Listener.FilterChain mapping
allowed_values: one or more filter-chain mappings; the example has one HTTP chain
default: No connector-owned filter-chain set default is declared; the selected template sets one chain containing the HTTP connection manager.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: Filter ordering determines whether ext_proc sees traffic before routing; do not insert an unreviewed bypass.
runtime_effect: Defines the network-filter sequence applied to accepted downstream connections.
description: Defines the network-filter sequence applied to accepted downstream connections.
```

## `static_resources.listeners[].filter_chains[].filters`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy NetworkFilter mapping
allowed_values: network filters with a name and typed_config; selected item is HTTP connection manager
default: No connector-owned network-filter list default is declared; the selected template sets the HCM filter.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: Removing or replacing HCM removes the selected HTTP/ext_proc lifecycle path.
runtime_effect: Installs the HTTP connection manager that owns routing and the nested ext_proc HTTP filter chain.
description: Installs the HTTP connection manager that owns routing and the nested ext_proc HTTP filter chain.
```

## `static_resources.listeners[].filter_chains[].filters[].name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `envoy.filters.network.http_connection_manager`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy NetworkFilter factory name
allowed_values: registered network-filter name; selected value is envoy.filters.network.http_connection_manager
default: No connector-owned network-filter factory default is declared; the selected template sets the HTTP connection manager factory name.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: A different network filter can remove HTTP routing and all ext_proc visibility.
runtime_effect: Selects Envoy's HTTP connection manager implementation for the listener.
description: Selects Envoy's HTTP connection manager implementation for the listener.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: google.protobuf.Any mapping for HttpConnectionManager
allowed_values: an Any payload whose @type is the Envoy v3 HttpConnectionManager URL
default: No connector-owned HCM typed configuration default is declared; the selected template sets the explicit HttpConnectionManager payload.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: The payload controls which filters receive downstream traffic; validate the concrete type URL with Envoy.
runtime_effect: Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters.
description: Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.@type`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.@type: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: protobuf Any type URL string
allowed_values: type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
default: No connector-owned HCM Any type default is declared; the selected template sets the explicit v3 HttpConnectionManager URL.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: A mismatched type URL prevents a valid HTTP/ext_proc listener configuration.
runtime_effect: Lets Envoy decode the surrounding typed_config as an HTTP connection manager.
description: Lets Envoy decode the surrounding typed_config as an HTTP connection manager.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: ordered repeated Envoy HTTP filter mapping
allowed_values: HTTP filters with factory name and typed_config; selected order is ext_proc then router
default: No connector-owned HTTP-filter chain default is declared; the selected template sets ext_proc then router ordered pair.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The selected order enables P1/P2/P3/P4 ext_proc callbacks before traffic is handed to the router.
security_relevance: Moving router ahead of ext_proc bypasses the selected inspection/authorization path.
runtime_effect: Orders HTTP processing: ext_proc runs before the router forwards upstream.
description: Orders HTTP processing: ext_proc runs before the router forwards upstream.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `envoy.filters.http.ext_proc, envoy.filters.http.router`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HTTP filter factory-name string
allowed_values: registered HTTP filter name; selected values are envoy.filters.http.ext_proc and envoy.filters.http.router
default: No connector-owned HTTP-filter factories default is declared; the selected template sets the ext_proc/router ordered pair.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: ext_proc exposes P1–P4; router terminates the filter chain and forwards to the upstream.
security_relevance: Filter order is an enforcement boundary: ext_proc must remain before router for the selected path.
runtime_effect: Selects the ext_proc policy filter and terminal router implementations in the HCM chain.
description: Selects the ext_proc policy filter and terminal router implementations in the HCM chain.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated google.protobuf.Any HTTP-filter configuration mapping
allowed_values: Any payloads whose @type values select ExternalProcessor and Router
default: No connector-owned HTTP typed configurations default is declared; the selected template sets the explicit ExternalProcessor and Router payloads.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The ExternalProcessor payload sets concrete P1–P4 visibility; the Router payload forwards the post-filter request.
security_relevance: A mismatched Any payload/name pair can invalidate or bypass the intended inspection chain.
runtime_effect: Holds the per-filter configuration corresponding to each HTTP filter item.
description: Holds the per-filter configuration corresponding to each HTTP filter item.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `type.googleapis.com/envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: protobuf Any type URL string
allowed_values: ExternalProcessor and Router v3 type URLs in the same order as the HTTP filters
default: No connector-owned HTTP Any type URLs default is declared; the selected template sets the explicit ExternalProcessor and Router v3 URLs.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: ExternalProcessor chooses P1–P4 callbacks; Router supplies the terminal forwarding stage.
security_relevance: The type URL must match the neighboring filter factory; otherwise Envoy cannot apply the selected lifecycle policy.
runtime_effect: Lets Envoy decode each HTTP filter's typed configuration.
description: Lets Envoy decode each HTTP filter's typed configuration.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | true \| false | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.allow_mode_override` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `false`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc boolean
default: Envoy proto default false; the selected template explicitly sets false.
default_source: Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: Guards the configured P1–P4 processing_mode contract; false keeps the static selected lifecycle surface.
security_relevance: false prevents the remote processor from widening/narrowing configured P1–P4 visibility at runtime.
runtime_effect: Allows or ignores a processor-supplied mode_override that would change processing_mode after request headers.
description: Allows or ignores a processor-supplied mode_override that would change processing_mode after request headers.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | true \| false | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.failure_mode_allow` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `false`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc boolean
default: Envoy proto default false; the selected template explicitly sets false.
default_source: Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: Failure behavior for the ext_proc stream serving all selected P1–P4 callbacks.
security_relevance: false avoids silently allowing traffic when the local processor cannot be reached; availability and denial behavior still need runtime evidence.
runtime_effect: Chooses whether processor stream errors/timeouts fail open (true) or produce Envoy's error handling (false).
description: Chooses whether processor stream errors/timeouts fail open (true) or produce Envoy's error handling (false).
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy GrpcService mapping
allowed_values: one gRPC service selector; selected form is envoy_grpc
default: No connector-owned ext_proc gRPC service default is declared; the selected template sets the msconnector_ext_proc envoy_grpc target.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Transport for all selected ext_proc callbacks: P1, P2, P3, P4, and trailer/EOS notifications.
security_relevance: The processor endpoint must be trusted and private; it receives selected request/response metadata and body chunks.
runtime_effect: Names the bidirectional gRPC side stream used by the ExternalProcessor filter.
description: Names the bidirectional gRPC side stream used by the ExternalProcessor filter.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: EnvoyGrpc cluster-reference mapping
allowed_values: cluster_name child naming a declared HTTP/2 cluster
default: No connector-owned Envoy gRPC target default is declared; the selected template sets the msconnector_ext_proc cluster reference.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Carries the full selected P1–P4 external-processing stream.
security_relevance: The cluster reference must resolve to the reviewed ext_proc service, not an arbitrary remote endpoint.
runtime_effect: Uses Envoy-managed gRPC transport rather than an inline URI for the external processor.
description: Uses Envoy-managed gRPC transport rather than an inline URI for the external processor.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.envoy_grpc.cluster_name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `msconnector_ext_proc`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy cluster-name string
allowed_values: name of a declared HTTP/2-capable cluster; selected value is msconnector_ext_proc
default: No connector-owned ext_proc service cluster default is declared; the selected template sets msconnector_ext_proc.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Transport target for P1 request headers, P2 request chunks, P3 response headers, P4 response chunks, and EOS trailers.
security_relevance: Changing it can send inspected headers/bodies to another processor; retain a private trusted target.
runtime_effect: Binds ExternalProcessor gRPC traffic to the local ext_proc cluster.
description: Binds ExternalProcessor gRPC traffic to the local ext_proc cluster.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Zeitlimitfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.grpc_service.timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `0.2s`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy protobuf Duration
allowed_values: non-negative duration; selected value is 0.2s
default: No connector-owned gRPC service timeout default is declared; the selected template sets 0.2s.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Applies to the ext_proc transport that serves selected P1–P4 callbacks.
security_relevance: A value that is too small creates avoidable processor failures; too large retains request resources longer.
runtime_effect: Bounds service establishment/operation as configured on the ext_proc gRPC service reference.
description: Bounds service establishment/operation as configured on the ext_proc gRPC service reference.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Zeitlimitfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.max_message_timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `0.25s`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy protobuf Duration maximum override timeout
allowed_values: non-negative duration; selected value is 0.25s
default: Envoy default is 0, which disables the processor override_message_timeout API; the selected template permits overrides up to 0.25s.
default_source: Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: Applies to timeout control for selected P1–P4 ext_proc exchanges; it does not change their visibility modes.
security_relevance: A finite cap limits remote processor influence over stream retention; setting a positive cap deliberately enables this API.
runtime_effect: Caps a processor-requested extension of the per-message timeout.
description: Caps a processor-requested extension of the per-message timeout.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Zeitlimitfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.message_timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `0.2s`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy protobuf Duration per ext_proc message
allowed_values: non-negative duration; selected value is 0.2s
default: Envoy ext_proc default 200 milliseconds when omitted; the selected template explicitly sets 0.2s.
default_source: Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: Applies to per-message P1/P2/P3/P4 ext_proc exchanges except observability/full-duplex/gRPC cases documented by Envoy.
security_relevance: Too large a timeout retains stream resources; too small a timeout creates processor failures governed by failure_mode_allow.
runtime_effect: Limits how long Envoy waits for each required external-processor response.
description: Limits how long Envoy waits for each required external-processor response.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc ProcessingMode mapping
allowed_values: header, body, and trailer send-mode child enums
default: Envoy defaults send request/response headers, skip trailers, and send no bodies; this template overrides every selected lifecycle field.
default_source: Envoy ext_proc v3 ProcessingMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: Controls P1 request headers, P2 request body, P3 response headers, P4 response body, and trailer/EOS delivery.
security_relevance: Omitting body modes loses body visibility; preserve explicit streaming modes for the selected full-lifecycle bridge.
runtime_effect: Groups the ext_proc visibility controls for request/response headers, bodies, and trailers.
description: Groups the ext_proc visibility controls for request/response headers, bodies, and trailers.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | NONE \| STREAMED \| BUFFERED \| BUFFERED_PARTIAL \| FULL_DUPLEX_STREAMED \| GRPC | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_body_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `STREAMED`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc BodySendMode enum
default: Envoy proto default NONE; the selected template explicitly sets STREAMED.
default_source: Envoy ext_proc v3 ProcessingMode.BodySendMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: request/P2: selected STREAMED makes the body available incrementally to the ext_proc bridge.
security_relevance: Body delivery exposes payload data and consumes stream resources; the selected Common bridge requires STREAMED with bounded service controls.
runtime_effect: Selects request/P2 body delivery to ext_proc; STREAMED sends incremental body chunks.
description: Selects request/P2 body delivery to ext_proc; STREAMED sends incremental body chunks.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | DEFAULT \| SEND \| SKIP | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_header_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `SEND`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc HeaderSendMode enum
default: Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND.
default_source: Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: request/P1: selected SEND exposes the header callback to the bridge.
security_relevance: Headers can include security-sensitive metadata; use the private local ext_proc service and its configured bounds.
runtime_effect: Selects whether request/P1 headers are sent to the external processor.
description: Selects whether request/P1 headers are sent to the external processor.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | DEFAULT \| SEND \| SKIP | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.request_trailer_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `SEND`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc HeaderSendMode enum for trailers
default: Envoy effective default SKIP for trailers; the selected template explicitly sets SEND.
default_source: Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: request EOS/trailer visibility after the corresponding body stream; it complements P2/P4 streaming.
security_relevance: Trailer metadata is part of the transaction; do not treat it as a body-size bypass.
runtime_effect: Sends request trailers/EOS metadata to the external processor when trailers are present.
description: Sends request trailers/EOS metadata to the external processor when trailers are present.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | NONE \| STREAMED \| BUFFERED \| BUFFERED_PARTIAL \| FULL_DUPLEX_STREAMED \| GRPC | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_body_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `STREAMED`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc BodySendMode enum
default: Envoy proto default NONE; the selected template explicitly sets STREAMED.
default_source: Envoy ext_proc v3 ProcessingMode.BodySendMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: response/P4: selected STREAMED makes the body available incrementally to the ext_proc bridge.
security_relevance: Body delivery exposes payload data and consumes stream resources; the selected Common bridge requires STREAMED with bounded service controls.
runtime_effect: Selects response/P4 body delivery to ext_proc; STREAMED sends incremental body chunks.
description: Selects response/P4 body delivery to ext_proc; STREAMED sends incremental body chunks.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | DEFAULT \| SEND \| SKIP | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_header_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `SEND`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc HeaderSendMode enum
default: Envoy effective default SEND for request and response headers; the selected template explicitly sets SEND.
default_source: Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: response/P3: selected SEND exposes the header callback to the bridge.
security_relevance: Headers can include security-sensitive metadata; use the private local ext_proc service and its configured bounds.
runtime_effect: Selects whether response/P3 headers are sent to the external processor.
description: Selects whether response/P3 headers are sent to the external processor.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | DEFAULT \| SEND \| SKIP | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode` die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.processing_mode.response_trailer_mode` konfiguriert die Sichtbarkeit und zeitliche Verarbeitung von P1–P4 im ext_proc-Pfad. Sie bestimmt, welche Request-/Response-Daten der externe Prozessor im ausgewählten Lebenszyklus erhält.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `SEND`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Body- und Header-Sichtbarkeit nur mit begrenzten Eingaben und geschützten Protokolldaten aktivieren.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc HeaderSendMode enum for trailers
default: Envoy effective default SKIP for trailers; the selected template explicitly sets SEND.
default_source: Envoy ext_proc v3 ProcessingMode.HeaderSendMode API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: response EOS/trailer visibility after the corresponding body stream; it complements P2/P4 streaming.
security_relevance: Trailer metadata is part of the transaction; do not treat it as a body-size bypass.
runtime_effect: Sends response trailers/EOS metadata to the external processor when trailers are present.
description: Sends response trailers/EOS metadata to the external processor when trailers are present.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy request-attribute name list
allowed_values: supported Envoy request attribute names; selected list requests protocol, source/destination address, and source/destination port
default: Absent list requests no additional attributes; this template explicitly requests five attributes used by processor.requestMetadataFromEnvoy.
default_source: Envoy ext_proc v3 ExternalProcessor API and connectors/envoy/ext_proc/internal/processor/processor.go:requestMetadataFromEnvoy
phase_relevance: P1 request metadata only; it seeds the transaction before P2 body callbacks and before later response callbacks.
security_relevance: Peer addresses and ports are operationally sensitive; the processor bounds and validates received metadata rather than deriving it from the gRPC peer.
runtime_effect: Requests concrete peer/protocol metadata for the ext_proc ProcessingRequest attributes map.
description: Requests concrete peer/protocol metadata for the ext_proc ProcessingRequest attributes map.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.request_attributes[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `request.protocol, source.address, source.port, destination.address, destination.port`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy request-attribute path string
allowed_values: request.protocol | source.address | source.port | destination.address | destination.port
default: No additional attribute is requested when omitted; this template explicitly requests all five metadata paths consumed by requestMetadataFromEnvoy.
default_source: selected template and connectors/envoy/ext_proc/internal/processor/processor.go:requestMetadataFromEnvoy
phase_relevance: P1 request metadata visibility; the selected bridge uses it to construct transaction metadata before P2/P3/P4 callbacks.
security_relevance: Do not add unbounded or sensitive attributes without reviewing processor handling and event logging.
runtime_effect: Makes protocol and client/server endpoint metadata available to the ext_proc processor's request-metadata mapper.
description: Makes protocol and client/server endpoint metadata available to the ext_proc processor's request-metadata mapper.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | true \| false | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.send_body_without_waiting_for_header_response` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `false`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_proc boolean
default: Envoy proto default false; the selected template explicitly sets false.
default_source: Envoy ext_proc v3 ExternalProcessor API pinned by connectors/envoy/ext_proc/go.mod
phase_relevance: Controls P1-to-P2/P3-to-P4 sequencing for STREAMED bodies; it does not itself enable body visibility.
security_relevance: Keeping false preserves the selected decision ordering and avoids uncontrolled early body delivery to the processor.
runtime_effect: When true with STREAMED bodies, Envoy sends body chunks before the processor's header response; false retains header-response ordering.
description: When true with STREAMED bodies, Envoy sends body chunks before the processor's header response; false retains header-response ordering.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteConfiguration mapping
allowed_values: inline route configuration with a name and virtual_hosts
default: No connector-owned inline route configuration default is declared; the selected template sets msconnector_ext_proc_route.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.
security_relevance: Routes control upstream reachability; constrain domains and prefixes in a real deployment.
runtime_effect: Defines the route lookup that selects the upstream after request-side filters run.
description: Defines the route lookup that selects the upstream after request-side filters run.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `msconnector_ext_proc_route`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteConfiguration.name string
allowed_values: non-empty local route-config name; selected value is msconnector_ext_proc_route
default: No connector-owned route-config name default is declared; the selected template sets msconnector_ext_proc_route.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routing metadata only; request filtering still occurs in the preceding HTTP filter order.
security_relevance: The name is not an authorization boundary; do not encode secrets in it.
runtime_effect: Names the inline route configuration for Envoy diagnostics and references.
description: Names the inline route configuration for Envoy diagnostics and references.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy VirtualHost mapping
allowed_values: one or more virtual-host mappings; the example has local_service
default: No connector-owned virtual-host list default is declared; the selected template sets one local_service entry.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.
security_relevance: Over-broad virtual hosts can route unexpected Host values to the upstream.
runtime_effect: Groups host/domain matches and routes for the HCM.
description: Groups host/domain matches and routes for the HCM.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `["*"]`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy VirtualHost domain matcher
allowed_values: a list of Envoy domain patterns
default: No connector-owned virtual-host domain matcher default is declared; the selected template sets the catch-all `*` pattern.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Host matching precedes upstream routing after request-header P1 processing.
security_relevance: The selected `*` catches all hosts; replace it with intended domains before exposure.
runtime_effect: Selects which Host/:authority values enter this virtual host's route list.
description: Selects which Host/:authority values enter this virtual host's route list.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `"*"`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy VirtualHost domain-pattern string
allowed_values: exact host, suffix/wildcard domain pattern, or *; selected item is *
default: No connector-owned virtual-host domain matcher default is declared; the selected template sets the catch-all `*` pattern.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Host matching precedes upstream routing after request-header P1 processing.
security_relevance: The selected `*` catches all hosts; replace it with intended domains before exposure.
runtime_effect: Selects which Host/:authority values enter this virtual host's route list.
description: Selects which Host/:authority values enter this virtual host's route list.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `local_service`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy VirtualHost.name string
allowed_values: non-empty virtual-host name; selected value is local_service
default: No connector-owned virtual-host name default is declared; the selected template sets local_service.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routing metadata only; it does not independently change ext_proc visibility.
security_relevance: Use opaque operational names rather than confidential data.
runtime_effect: Labels the virtual-host route group.
description: Labels the virtual-host route group.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Route mapping
allowed_values: one or more match/action route mappings; the example has one prefix route
default: No connector-owned route list default is declared; the selected template sets one `/` prefix route to upstream_service.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: The matched route is selected after P1; its upstream yields the response seen at P3/P4.
security_relevance: Route order and match breadth determine where request traffic can be sent.
runtime_effect: Contains ordered route matching and upstream actions for the virtual host.
description: Contains ordered route matching and upstream actions for the virtual host.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteMatch mapping
allowed_values: the child fields shown in this template
default: No connector-owned RouteMatch mapping default is declared; the selected template sets the explicit `/` prefix and upstream_service action.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.
security_relevance: An over-broad match or unsafe route action can expose an unintended upstream.
runtime_effect: Groups the prefix matcher for the selected route.
description: Groups the prefix matcher for the selected route.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `"/"`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteMatch prefix string
allowed_values: path-prefix matcher; selected value is /
default: No connector-owned route prefix default is declared; the selected template sets the catch-all `/` prefix.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.
security_relevance: The catch-all `/` reaches every path in the virtual host; narrow it when policy requires.
runtime_effect: Matches request paths for the selected route.
description: Matches request paths for the selected route.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteAction mapping
allowed_values: the child fields shown in this template
default: No connector-owned RouteAction mapping default is declared; the selected template sets the explicit `/` prefix and upstream_service action.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.
security_relevance: An over-broad match or unsafe route action can expose an unintended upstream.
runtime_effect: Groups the cluster action selected after the route match.
description: Groups the cluster action selected after the route match.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.route.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `upstream_service`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteAction cluster-name string
allowed_values: name of a declared static_resources.clusters entry; selected value is upstream_service
default: No connector-owned route cluster target default is declared; the selected template sets upstream_service.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Routes are consulted after P1 request-header filtering; they direct the upstream response that later reaches P3/P4.
security_relevance: The target must be a reviewed local/upstream endpoint; an untrusted target creates an egress path.
runtime_effect: Routes matching downstream requests to the named upstream cluster.
description: Routes matching downstream requests to the named upstream cluster.
```

## `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `msconnector_ext_proc_ingress`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: HttpConnectionManager statistics-prefix string
allowed_values: non-empty metrics namespace token; selected value is msconnector_ext_proc_ingress
default: No connector-owned HCM statistic prefix default is declared; the selected template sets msconnector_ext_proc_ingress.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Observability only; it does not change P1–P4 payload visibility.
security_relevance: Metric names should not embed secrets, user identifiers, or unbounded request data.
runtime_effect: Prefixes HCM metrics for the selected ingress listener.
description: Prefixes HCM metrics for the selected ingress listener.
```

## `static_resources.listeners[].name`

### Kurzbeschreibung

Das YAML-Feld `static_resources.listeners[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
static_resources.listeners[].name: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `static_resources.listeners[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `static_resources.listeners[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `static_resources.listeners[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `static_resources.listeners[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Außerhalb des Checkouts materialisieren und anschließend envoy --mode validate -c <generated-config> ausführen.

### Beispiel

Ausgewählter Beispielwert: `msconnector_ext_proc_listener`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-streaming.yaml.in](../../examples/envoy/safe/envoy-ext-proc-streaming.yaml.in).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Listener.name string
allowed_values: unique non-empty listener name in this bootstrap
default: No connector-owned listener-name default is declared; the selected template sets `msconnector_ext_proc_listener`.
default_source: selected Envoy v3 template; connector owns no bootstrap default
phase_relevance: Bootstrap only; this listener carries the selected ext_proc HTTP filter chain, whose processing_mode exposes P1 request headers, P2 request body chunks, P3 response headers, and P4 response body chunks.
security_relevance: A name is control-plane metadata, but it should not disclose tenant or secret identifiers.
runtime_effect: Names the downstream HTTP listener for Envoy configuration and observability.
description: Names the downstream HTTP listener for Envoy configuration and observability.
```

## `transaction_id_header`

### Kurzbeschreibung

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Syntax

```text
"transaction_id_header": <string>
```

### Gültige Kontexte

- ext_proc-Service-JSON-Objekt

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Zeichenkette | nichtleerer HTTP-Headername | ja |

### Standardwert

kein Wert; JSON-Decoder/Config.Validate verlangt jedes ausgewählte Feld

Quelle: `processor.Config besitzt keine impliziten Feldstandardwerte`.

### Vererbung und Zusammenführung

Keine Vererbung; ein JSON-Objekt wird dekodiert, unbekannte Felder werden abgewiesen.

Zusammenführung: Kein Merge; ein zweiter JSON-Wert wird nach dem einen Konfigurationsobjekt abgewiesen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Limits und späte Policy beeinflussen das Prozessorverhalten in P1–P4.

Setzt eine begrenzte ext_proc-Service-Steuerung.

### Validierung und Fehler

Config.Validate weist leere, nichtpositive, ungültige Enum- und host:port-Werte sowie widersprüchliche gRPC-/Body-Limits ab.

### Beispiel

Ausgewählter Beispielwert: `"x-request-id"`.

Quellenbasiertes Beispiel: [examples/envoy/safe/envoy-ext-proc-service.json](../../examples/envoy/safe/envoy-ext-proc-service.json).

### Sicherheit und Betrieb

Alle Header-, Body-, gRPC- und Timeout-Werte begrenzen; die Listen-Adresse des Service privat halten.

## `compatibility.ext_authz.static_resources`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources` konfiguriert die Kompatibilitätsintegration. Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads.

### Syntax

```text
compatibility.ext_authz.static_resources: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources` die Kompatibilitätsintegration konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources` konfiguriert die Kompatibilitätsintegration. Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Diese Einstellung nicht als Nachweis einer nativen Full-Lifecycle-Integration verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Bootstrap static_resources mapping
allowed_values: listener and cluster child mappings shown in the template
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Bootstrap establishes the selected ext_proc P1–P4 path but does not itself process a transaction. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: All listener and cluster children affect traffic exposure or destination; review as one topology. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Declares the complete static data-plane topology used by the checked-in example. Compatibility-only host/service setup outside the selected native core path.
description: Declares the complete static data-plane topology used by the checked-in example. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Cluster mapping
allowed_values: one or more Cluster objects; selected template declares upstream_service and msconnector_ext_proc
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: upstream_service provides the request/response path; msconnector_ext_proc transports selected P1–P4 callbacks. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Clusters define where application traffic and inspection data can leave the listener. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Declares the static service destinations used by routing and ext_proc gRPC. Compatibility-only host/service setup outside the selected native core path.
description: Declares the static service destinations used by routing and ext_proc gRPC. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].connect_timeout`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].connect_timeout` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].connect_timeout: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].connect_timeout` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Zeitlimitfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].connect_timeout` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].connect_timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].connect_timeout` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].connect_timeout` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `0.25s`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy protobuf Duration for cluster connection attempts
allowed_values: non-negative duration; selected native value is 0.5s (compatibility example uses 0.25s)
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.25s.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A long timeout retains connections; a short timeout can trigger processor failures or upstream unavailability. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Bounds TCP connection establishment to the upstream or local processor endpoint. Compatibility-only host/service setup outside the selected native core path.
description: Bounds TCP connection establishment to the upstream or local processor endpoint. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ClusterLoadAssignment mapping
allowed_values: cluster_name plus endpoint/lb_endpoints children
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Endpoint assignments are egress/control-plane inputs; review every address and port. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the endpoints assigned to a static cluster. Compatibility-only host/service setup outside the selected native core path.
description: Groups the endpoints assigned to a static cluster. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.cluster_name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `modsecurity_authz, app_backend`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ClusterLoadAssignment.cluster_name string
allowed_values: must match the enclosing Cluster.name; selected values match upstream_service or msconnector_ext_proc
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz, app_backend.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A mismatch invalidates or misroutes the endpoint configuration. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Associates the endpoint assignment with its enclosing cluster. Compatibility-only host/service setup outside the selected native core path.
description: Associates the endpoint assignment with its enclosing cluster. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy LocalityLbEndpoints mapping
allowed_values: one or more locality endpoint groups; the example has one group
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Each endpoint is a traffic destination; preserve the intended private scope. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups load-balanced endpoints for the static cluster. Compatibility-only host/service setup outside the selected native core path.
description: Groups load-balanced endpoints for the static cluster. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy LbEndpoint mapping
allowed_values: one or more endpoint mappings; the example has one endpoint per cluster
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: An added endpoint receives copied requests or ext_proc messages; require explicit trust review. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Defines endpoint candidates selected by Envoy's cluster load balancer. Compatibility-only host/service setup outside the selected native core path.
description: Defines endpoint candidates selected by Envoy's cluster load balancer. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Endpoint mapping
allowed_values: endpoint address child mapping
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The endpoint is a concrete traffic target and must be constrained to the intended service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Contains the network address of one cluster endpoint. Compatibility-only host/service setup outside the selected native core path.
description: Contains the network address of one cluster endpoint. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.Address mapping
allowed_values: one supported Envoy address form; selected form is socket_address
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Changing it changes egress or inspection-service reachability. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Contains the TCP address for one upstream or ext_proc service endpoint. Compatibility-only host/service setup outside the selected native core path.
description: Contains the TCP address for one upstream or ext_proc service endpoint. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `{ address: 127.0.0.1, port_value: 9000 }, { address: 127.0.0.1, port_value: 8081 }`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.SocketAddress mapping
allowed_values: address and port_value child fields
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { address: 127.0.0.1, port_value: 9000 }, { address: 127.0.0.1, port_value: 8081 }.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The selected loopback values keep both upstream and processor endpoint examples local. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Pairs the static cluster endpoint host and TCP port. Compatibility-only host/service setup outside the selected native core path.
description: Pairs the static cluster endpoint host and TCP port. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `127.0.0.1`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress host/IP string
allowed_values: valid endpoint host or IP literal; selected value is 127.0.0.1
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 127.0.0.1.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Loopback avoids external egress in the example; a remote host needs transport and trust controls. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Targets the static upstream or ext_proc endpoint host. Compatibility-only host/service setup outside the selected native core path.
description: Targets the static upstream or ext_proc endpoint host. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Portfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].load_assignment.endpoints[].lb_endpoints[].endpoint.address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `9000, 8081`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress uint32 TCP port
allowed_values: materializer-validated decimal port 1..65535
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 9000, 8081.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Port changes can send traffic to a different local service; retain explicit private service ownership. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Targets the TCP port of the selected upstream or ext_proc endpoint. Compatibility-only host/service setup outside the selected native core path.
description: Targets the TCP port of the selected upstream or ext_proc endpoint. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].name` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].name` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `modsecurity_authz, app_backend`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Cluster.name string
allowed_values: unique non-empty cluster name; selected values are upstream_service and msconnector_ext_proc
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz, app_backend.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: upstream_service supplies the normal request/response flow; msconnector_ext_proc carries P1–P4 processor traffic. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Cluster names resolve traffic destinations; do not redirect an inspection target to an unreviewed service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Names a static endpoint group referenced by the route or ext_proc gRPC service. Compatibility-only host/service setup outside the selected native core path.
description: Names a static endpoint group referenced by the route or ext_proc gRPC service. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.clusters[].type`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].type` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.ext_authz.static_resources.clusters[].type: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.clusters[].type` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.clusters[].type` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.clusters[].type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.clusters[].type` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.clusters[].type` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `STRICT_DNS`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Cluster DiscoveryType enum
allowed_values: Envoy discovery type; selected native value STATIC, compatibility values STRICT_DNS
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures STRICT_DNS.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The compatibility cluster list contains modsecurity_authz for request authorization and app_backend for the allowed upstream flow; it does not establish selected native P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: STATIC keeps the selected endpoints explicit; DNS discovery changes endpoint resolution and should be reviewed for egress/identity impact. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Determines how Envoy resolves the endpoint set for the named cluster. Compatibility-only host/service setup outside the selected native core path.
description: Determines how Envoy resolves the endpoint set for the named cluster. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Listener mapping
allowed_values: one or more Listener objects; selected template declares one loopback HTTP listener
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Bootstrap container for the filter chain that exposes selected P1–P4 ext_proc callbacks. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A listener changes the network attack surface before request policy is reached. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Declares the downstream listener objects present in the static bootstrap. Compatibility-only host/service setup outside the selected native core path.
description: Declares the downstream listener objects present in the static bootstrap. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.Address mapping
allowed_values: one supported Envoy address form; the example selects socket_address
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Changing the child socket address changes network exposure before any ModSecurity processing. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Contains the downstream listener bind address used before the HTTP filter chain runs. Compatibility-only host/service setup outside the selected native core path.
description: Contains the downstream listener bind address used before the HTTP filter chain runs. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].address.socket_address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address.socket_address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address.socket_address` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].address.socket_address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address.socket_address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].address.socket_address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `{ address: 0.0.0.0, port_value: 8080 }`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy core.SocketAddress mapping
allowed_values: address plus port_value (or another Envoy-supported socket-address form)
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { address: 0.0.0.0, port_value: 8080 }.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The selected loopback pair keeps the example private; a wildcard bind requires an explicit exposure decision. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Pairs the listener host and TCP port that accept downstream traffic. Compatibility-only host/service setup outside the selected native core path.
description: Pairs the listener host and TCP port that accept downstream traffic. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address.socket_address.address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `0.0.0.0`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress host/IP string
allowed_values: a valid listener host or IP literal; selected value is 127.0.0.1
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.0.0.0.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A wildcard or public value exposes the listener before ext_proc policy can run. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Binds the downstream HTTP listener to the selected network interface. Compatibility-only host/service setup outside the selected native core path.
description: Binds the downstream HTTP listener to the selected network interface. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Portfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].address.socket_address.port_value` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `8080`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy SocketAddress uint32 TCP port
allowed_values: materializer-validated decimal port 1..65535
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 8080.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Use a private, non-conflicting port; port selection affects reachability before P1. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects the TCP port on which downstream requests enter the ext_proc filter chain. Compatibility-only host/service setup outside the selected native core path.
description: Selects the TCP port on which downstream requests enter the ext_proc filter chain. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Listener.FilterChain mapping
allowed_values: one or more filter-chain mappings; the example has one HTTP chain
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Filter ordering determines whether ext_authz compatibility sees traffic before routing; do not insert an unreviewed bypass. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Defines the network-filter sequence applied to accepted downstream connections. Compatibility-only host/service setup outside the selected native core path.
description: Defines the network-filter sequence applied to accepted downstream connections. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy NetworkFilter mapping
allowed_values: network filters with a name and typed_config; selected item is HTTP connection manager
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Removing or replacing HCM removes the selected HTTP/ext_authz compatibility lifecycle path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Installs the HTTP connection manager that owns routing and the nested ext_authz compatibility HTTP filter chain. Compatibility-only host/service setup outside the selected native core path.
description: Installs the HTTP connection manager that owns routing and the nested ext_authz compatibility HTTP filter chain. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `envoy.filters.network.http_connection_manager`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy NetworkFilter factory name
allowed_values: registered network-filter name; selected value is envoy.filters.network.http_connection_manager
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures envoy.filters.network.http_connection_manager.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A different network filter can remove HTTP routing and all ext_authz compatibility visibility. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects Envoy's HTTP connection manager implementation for the listener. Compatibility-only host/service setup outside the selected native core path.
description: Selects Envoy's HTTP connection manager implementation for the listener. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: google.protobuf.Any mapping for HttpConnectionManager
allowed_values: an Any payload whose @type is the Envoy v3 HttpConnectionManager URL
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The payload controls which filters receive downstream traffic; validate the concrete type URL with Envoy. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters. Compatibility-only host/service setup outside the selected native core path.
description: Carries the HCM stat prefix, inline route configuration, and ordered HTTP filters. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: protobuf Any type URL string
allowed_values: type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A mismatched type URL prevents a valid HTTP/ext_proc listener configuration. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Lets Envoy decode the surrounding typed_config as an HTTP connection manager. Compatibility-only host/service setup outside the selected native core path.
description: Lets Envoy decode the surrounding typed_config as an HTTP connection manager. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: ordered repeated Envoy HTTP filter mapping
allowed_values: HTTP filters with factory name and typed_config; selected order is ext_authz then router
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The selected order enables compatibility P1 request authorization before the router; it does not create P2/P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Moving router ahead of ext_authz bypasses the selected inspection/authorization path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Orders HTTP processing: ext_authz runs before the router forwards upstream. Compatibility-only host/service setup outside the selected native core path.
description: Orders HTTP processing: ext_authz runs before the router forwards upstream. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `envoy.filters.http.ext_authz, envoy.filters.http.router`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HTTP filter factory-name string
allowed_values: registered HTTP filter name; selected values are envoy.filters.http.ext_authz and envoy.filters.http.router
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures envoy.filters.http.ext_authz, envoy.filters.http.router.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: ext_authz is compatibility request authorization; router forwards after it and no selected P2/P3/P4 path exists. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Filter order is an enforcement boundary: ext_authz must remain before router for the selected path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects the ext_authz policy filter and terminal router implementations in the HCM chain. Compatibility-only host/service setup outside the selected native core path.
description: Selects the ext_authz policy filter and terminal router implementations in the HCM chain. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated google.protobuf.Any HTTP-filter configuration mapping
allowed_values: Any payloads whose @type values select ExtAuthz and Router
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The ExtAuthz payload controls compatibility P1 request authorization; the Router payload forwards the allowed request. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A mismatched Any payload/name pair can invalidate or bypass the intended inspection chain. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Holds the per-filter configuration corresponding to each HTTP filter item. Compatibility-only host/service setup outside the selected native core path.
description: Holds the per-filter configuration corresponding to each HTTP filter item. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.@type` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: protobuf Any type URL string
allowed_values: ExtAuthz and Router v3 type URLs in the same order as the HTTP filters
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz, type.googleapis.com/envoy.extensions.filters.http.router.v3.Router.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: ExtAuthz performs compatibility P1 request authorization; Router is terminal forwarding and does not expose selected P2/P3/P4 callbacks. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The type URL must match the neighboring filter factory; otherwise Envoy cannot apply the selected lifecycle policy. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Lets Envoy decode each HTTP filter's typed configuration. Compatibility-only host/service setup outside the selected native core path.
description: Lets Envoy decode each HTTP filter's typed configuration. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_authz HTTP service mapping (compatibility only)
allowed_values: one HTTP service; mutually exclusive with grpc_service
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility request authorization only; do not infer selected native P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: HTTP service is compatibility-only and cannot provide the selected body/trailer full-lifecycle path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Configures the compatibility ext_authz-style HTTP service instead of the selected gRPC ext_proc service. Compatibility-only host/service setup outside the selected native core path.
description: Configures the compatibility ext_authz-style HTTP service instead of the selected gRPC ext_proc service. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy ext_authz AuthorizationRequest mapping (compatibility only)
allowed_values: allowed_headers child mapping shown in the compatibility template
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility P1 request-header authorization only; no selected body or response visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Only forward the headers the compatibility service needs; extra headers may disclose credentials or user data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the header-forwarding policy for the compatibility authorization request. Compatibility-only host/service setup outside the selected native core path.
description: Groups the header-forwarding policy for the compatibility authorization request. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HeaderMatcher list mapping (compatibility only)
allowed_values: one or more header matcher patterns; selected policy has exact authorization and content-type
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility P1 request-header authorization only; no native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Header forwarding can expose credentials; keep the matcher list minimal and audit changes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
description: Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HeaderMatcher list mapping (compatibility only)
allowed_values: one or more header matcher patterns; selected policy has exact authorization and content-type
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility P1 request-header authorization only; no native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Header forwarding can expose credentials; keep the matcher list minimal and audit changes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
description: Groups the allow-list of request headers forwarded to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.authorization_request.allowed_headers.patterns[].exact` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `authorization, content-type`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HeaderMatcher exact header-name string (compatibility only)
allowed_values: lower-case/HTTP header name exact matcher; selected values are authorization and content-type
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures authorization, content-type.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility P1 request-header authorization only; no selected P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The authorization value is sensitive; ensure the compatibility service and its logs are trusted. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Forwards only matching request headers to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
description: Forwards only matching request headers to the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HttpService.server_uri mapping (compatibility only)
allowed_values: URI, cluster, and timeout child fields
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility request authorization only; no selected full response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Keep the authorization service private and do not embed credentials in a URI. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the compatibility service URI, logical cluster, and deadline. Compatibility-only host/service setup outside the selected native core path.
description: Groups the compatibility service URI, logical cluster, and deadline. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `modsecurity_authz`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy cluster-name string (compatibility only)
allowed_values: name of a declared compatibility cluster; selected value is modsecurity_authz
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures modsecurity_authz.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility request authorization only; no selected P3/P4 coverage. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The name must resolve to a reviewed service cluster; do not treat it as the native ext_proc target. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Associates the HTTP authorization URI with its configured Envoy cluster. Compatibility-only host/service setup outside the selected native core path.
description: Associates the HTTP authorization URI with its configured Envoy cluster. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Zeitlimitfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.timeout` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `0.2s`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy protobuf Duration (compatibility HTTP authorization timeout)
allowed_values: non-negative duration; selected value is 0.2s
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures 0.2s.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility request authorization only; no P3/P4 response inspection. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Deadline choice changes failure pressure; it is not an ext_proc full-lifecycle timeout guarantee. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Bounds one compatibility authorization HTTP request. Compatibility-only host/service setup outside the selected native core path.
description: Bounds one compatibility authorization HTTP request. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.http_filters[].typed_config.http_service.server_uri.uri` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `http://127.0.0.1:9000`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy HTTP service URI string (compatibility only)
allowed_values: absolute HTTP/HTTPS URI; selected value is http://127.0.0.1:9000
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures http://127.0.0.1:9000.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility request authorization only; no native response-body P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Loopback limits the example exposure; a remote URI needs TLS, identity, and egress review. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Identifies the HTTP authorization endpoint for compatibility ext_authz requests. Compatibility-only host/service setup outside the selected native core path.
description: Identifies the HTTP authorization endpoint for compatibility ext_authz requests. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteConfiguration mapping
allowed_values: inline route configuration with a name and virtual_hosts
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Routes control upstream reachability; constrain domains and prefixes in a real deployment. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Defines the route lookup that selects the upstream after request-side filters run. Compatibility-only host/service setup outside the selected native core path.
description: Defines the route lookup that selects the upstream after request-side filters run. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `local_route`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteConfiguration.name string
allowed_values: non-empty local route-config name; selected value is msconnector_ext_proc_route
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures local_route.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Routing metadata only; request filtering still occurs in the preceding HTTP filter order. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The name is not an authorization boundary; do not encode secrets in it. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Names the inline route configuration for Envoy diagnostics and references. Compatibility-only host/service setup outside the selected native core path.
description: Names the inline route configuration for Envoy diagnostics and references. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy VirtualHost mapping
allowed_values: one or more virtual-host mappings; the example has local_service
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Over-broad virtual hosts can route unexpected Host values to the upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups host/domain matches and routes for the HCM. Compatibility-only host/service setup outside the selected native core path.
description: Groups host/domain matches and routes for the HCM. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `["*"]`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy VirtualHost domain matcher
allowed_values: a list of Envoy domain patterns
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["*"].
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Host matching precedes upstream routing after request-header P1 processing. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The selected `*` catches all hosts; replace it with intended domains before exposure. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.
description: Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].domains[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"*"`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy VirtualHost domain-pattern string
allowed_values: exact host, suffix/wildcard domain pattern, or *; selected item is *
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "*".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Host matching precedes upstream routing after request-header P1 processing. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The selected `*` catches all hosts; replace it with intended domains before exposure. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.
description: Selects which Host/:authority values enter this virtual host's route list. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `backend`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy VirtualHost.name string
allowed_values: non-empty virtual-host name; selected value is local_service
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures backend.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Routing metadata only; it does not independently change ext_proc visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Use opaque operational names rather than confidential data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Labels the virtual-host route group. Compatibility-only host/service setup outside the selected native core path.
description: Labels the virtual-host route group. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Envoy Route mapping
allowed_values: one or more match/action route mappings; the example has one prefix route
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: The matched route is selected after P1; its upstream yields the response seen at P3/P4. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Route order and match breadth determine where request traffic can be sent. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Contains ordered route matching and upstream actions for the virtual host. Compatibility-only host/service setup outside the selected native core path.
description: Contains ordered route matching and upstream actions for the virtual host. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `{ prefix: "/" }`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteMatch mapping
allowed_values: the child fields shown in this template
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { prefix: "/" }.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: An over-broad match or unsafe route action can expose an unintended upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the prefix matcher for the selected route. Compatibility-only host/service setup outside the selected native core path.
description: Groups the prefix matcher for the selected route. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].match.prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"/"`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteMatch prefix string
allowed_values: path-prefix matcher; selected value is /
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "/".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The catch-all `/` reaches every path in the virtual host; narrow it when policy requires. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Matches request paths for the selected route. Compatibility-only host/service setup outside the selected native core path.
description: Matches request paths for the selected route. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `{ cluster: app_backend }`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteAction mapping
allowed_values: the child fields shown in this template
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures { cluster: app_backend }.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: An over-broad match or unsafe route action can expose an unintended upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the cluster action selected after the route match. Compatibility-only host/service setup outside the selected native core path.
description: Groups the cluster action selected after the route match. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.route_config.virtual_hosts[].routes[].route.cluster` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `app_backend`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy RouteAction cluster-name string
allowed_values: name of a declared static_resources.clusters entry; selected value is upstream_service
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures app_backend.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility route selection follows ext_authz P1 request authorization and forwards an allowed request; the compatibility filter has no selected P2/P3/P4 response lifecycle. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: The target must be a reviewed local/upstream endpoint; an untrusted target creates an egress path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Routes matching downstream requests to the named upstream cluster. Compatibility-only host/service setup outside the selected native core path.
description: Routes matching downstream requests to the named upstream cluster. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].filter_chains[].filters[].typed_config.stat_prefix` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `ingress_http`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: HttpConnectionManager statistics-prefix string
allowed_values: non-empty metrics namespace token; selected value is msconnector_ext_proc_ingress
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ingress_http.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Observability only; it does not change P1–P4 payload visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: Metric names should not embed secrets, user identifiers, or unbounded request data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Prefixes HCM metrics for the selected ingress listener. Compatibility-only host/service setup outside the selected native core path.
description: Prefixes HCM metrics for the selected ingress listener. Compatibility-only host/service setup outside the selected native core path.
```

## `compatibility.ext_authz.static_resources.listeners[].name`

### Kurzbeschreibung

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.ext_authz.static_resources.listeners[].name: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.ext_authz.static_resources.listeners[].name` im ausgewählten Envoy-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.ext_authz.static_resources.listeners[].name` ergibt sich aus dem ausgewählten Envoy-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.ext_authz.static_resources.listeners[].name` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Envoy-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.ext_authz.static_resources.listeners[].name` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.ext_authz.static_resources.listeners[].name` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Envoy-ext_authz-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `listener_0`.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Envoy Listener.name string
allowed_values: unique non-empty listener name in this bootstrap
default: Absent from the selected native ext_proc configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures listener_0.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (ext_authz)
phase_relevance: Compatibility bootstrap only; this listener carries ext_authz request authorization before the router and does not establish selected native P2/P3/P4 visibility. Compatibility ext_authz path: request authorization/P1 only; no selected ext_proc P2 body, P3 response-header, or P4 response-body coverage.
security_relevance: A name is control-plane metadata, but it should not disclose tenant or secret identifiers. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Names the downstream HTTP listener for Envoy configuration and observability. Compatibility-only host/service setup outside the selected native core path.
description: Names the downstream HTTP listener for Envoy configuration and observability. Compatibility-only host/service setup outside the selected native core path.
```

## `envoy.filters.http.ext_authz`

### Kurzbeschreibung

ext_authz-Filter nur für die Kompatibilität.

### Syntax

```text
name: envoy.filters.http.ext_authz
```

### Gültige Kontexte

- Kompatibilitäts-Envoy-HTTP-Filterkette

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Envoy-Kompatibilitätsfilter | ext_authz-v3-Konfiguration | nein |

### Standardwert

nicht Teil des ausgewählten ext_proc-Pfads

Quelle: `Kompatibilitäts-Template`.

### Vererbung und Zusammenführung

nicht Teil der ext_proc-Konfiguration

Zusammenführung: nicht Teil der ausgewählten Full-Lifecycle-Konfiguration

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Kompatibilitätspfad für Request-Autorisierung; keine Abdeckung von ausgewähltem P3/P4.

Leitet an den separaten Autorisierungs-Kompatibilitätsservice weiter.

### Validierung und Fehler

Separate Validierung der ext_authz-Konfiguration.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml](../../examples/envoy/compatibility-ext-authz/envoy-ext-authz.yaml).

### Sicherheit und Betrieb

Nicht als native ext_proc-Full-Lifecycle-Konfiguration darstellen.
