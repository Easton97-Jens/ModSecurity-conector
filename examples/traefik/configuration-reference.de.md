# Traefik-Konfigurationsreferenz

**Sprache:** [English](configuration-reference.md) | Deutsch

## Geltungsbereich und maßgebliche Quellen

Ausgewählter Integrationsmodus: `native-middleware-uds-engine`. Diese Datei wird aus registrierten Parsern, Konfigurationsstrukturen, geprüften Service-Verträgen und aktiven Beispielen erzeugt.
Kompatibilitätseinträge sind ausdrücklich als solche markiert und gehören nicht zum ausgewählten Kernpfad.

## Konfigurationsinventar

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`accessLog`](#accesslog) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `accessLog` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `accessLog` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden. |
| [`entryPoints`](#entrypoints) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`entryPoints.web`](#entrypoints-web) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `entryPoints.web` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `entryPoints.web` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`entryPoints.web.address`](#entrypoints-web-address) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `entryPoints.web.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `entryPoints.web.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`experimental`](#experimental) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `experimental` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `experimental` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads. |
| [`experimental.localPlugins`](#experimental-localplugins) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `experimental.localPlugins` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `experimental.localPlugins` konfiguriert die lokale Plugin-Konfiguration. Sie verbindet den Host mit der ausgewählten lokalen Plugin-Implementierung und ihren Einstellungen. |
| [`experimental.localPlugins.modsecurityNative`](#experimental-localplugins-modsecuritynative) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `experimental.localPlugins.modsecurityNative` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `experimental.localPlugins.modsecurityNative` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`experimental.localPlugins.modsecurityNative.moduleName`](#experimental-localplugins-modsecuritynative-modulename) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `experimental.localPlugins.modsecurityNative.moduleName` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `experimental.localPlugins.modsecurityNative.moduleName` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`experimental.localPlugins.modsecurityNative.settings`](#experimental-localplugins-modsecuritynative-settings) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `experimental.localPlugins.modsecurityNative.settings` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `experimental.localPlugins.modsecurityNative.settings` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`experimental.localPlugins.modsecurityNative.settings.envs`](#experimental-localplugins-modsecuritynative-settings-envs) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `experimental.localPlugins.modsecurityNative.settings.envs` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `experimental.localPlugins.modsecurityNative.settings.envs` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http`](#http) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads. |
| [`http.middlewares`](#http-middlewares) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `http.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.middlewares` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming`](#http-middlewares-modsecurity-native-streaming) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.middlewares.modsecurity-native-streaming` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.middlewares.modsecurity-native-streaming` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin`](#http-middlewares-modsecurity-native-streaming-plugin) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.middlewares.modsecurity-native-streaming.plugin` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginemode) | Host / Connector | YAML-Steuerfeld | nein | passthrough | http.middlewares.<name>.plugin.modsecurityNative | Wählt source-only-passthrough oder die persistente UDS-Engine; das ausgewählte regelauswertende Beispiel verwendet uds. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginesocketpath) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | http.middlewares.<name>.plugin.modsecurityNative | Benennt den privaten UDS-Pfad, den die native Middleware bei engineMode=uds verwendet. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheaderbytes) | Host / Connector | YAML-Limitfeld | nein | 65536 | http.middlewares.<name>.plugin.modsecurityNative | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheadercount) | Host / Connector | YAML-Limitfeld | nein | 128 | http.middlewares.<name>.plugin.modsecurityNative | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxrequestchunkbytes) | Host / Connector | YAML-Limitfeld | nein | 32768 | http.middlewares.<name>.plugin.modsecurityNative | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxresponsechunkbytes) | Host / Connector | YAML-Limitfeld | nein | 32768 | http.middlewares.<name>.plugin.modsecurityNative | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader`](#http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-transactionidheader) | Host / Connector | YAML-Steuerfeld | nein | X-Request-Id | http.middlewares.<name>.plugin.modsecurityNative | Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`http.routers`](#http-routers) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.routers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`http.routers.app`](#http-routers-app) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.routers.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`http.routers.app.entryPoints`](#http-routers-app-entrypoints) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.routers.app.entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`http.routers.app.entryPoints[]`](#http-routers-app-entrypoints) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `http.routers.app.entryPoints[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app.entryPoints[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`http.routers.app.middlewares`](#http-routers-app-middlewares) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `http.routers.app.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app.middlewares` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`http.routers.app.middlewares[]`](#http-routers-app-middlewares) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `http.routers.app.middlewares[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app.middlewares[]` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`http.routers.app.rule`](#http-routers-app-rule) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.routers.app.rule` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app.rule` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`http.routers.app.service`](#http-routers-app-service) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.routers.app.service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.routers.app.service` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`http.services`](#http-services) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `http.services` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.services` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`http.services.app`](#http-services-app) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.services.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.services.app` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`http.services.app.loadBalancer`](#http-services-app-loadbalancer) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `http.services.app.loadBalancer` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.services.app.loadBalancer` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`http.services.app.loadBalancer.servers`](#http-services-app-loadbalancer-servers) | Host / Connector | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `http.services.app.loadBalancer.servers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.services.app.loadBalancer.servers` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`http.services.app.loadBalancer.servers[].url`](#http-services-app-loadbalancer-servers-url) | Host / Connector | YAML-Adressfeld | nein | Der Connector definiert für `http.services.app.loadBalancer.servers[].url` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `http.services.app.loadBalancer.servers[].url` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`log`](#log) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `log` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `log` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden. |
| [`log.level`](#log-level) | Host / Connector | YAML-Steuerfeld | nein | Der Connector definiert für `log.level` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `log.level` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden. |
| [`providers`](#providers) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `providers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `providers` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`providers.file`](#providers-file) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `providers.file` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `providers.file` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`providers.file.filename`](#providers-file-filename) | Host / Connector | YAML-Kennungsfeld | nein | Der Connector definiert für `providers.file.filename` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `providers.file.filename` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`providers.file.watch`](#providers-file-watch) | Host / Connector | YAML-Konfigurationsfeld | nein | Der Connector definiert für `providers.file.watch` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | Der im ausgewählten Beispiel gezeigte YAML-Objektpfad. | Das YAML-Feld `providers.file.watch` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`compatibility.forwardauth-dynamic.http`](#compatibility-forwardauth-dynamic-http) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http` konfiguriert die Kompatibilitätsintegration. Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads. |
| [`compatibility.forwardauth-dynamic.http.middlewares`](#compatibility-forwardauth-dynamic-http-middlewares) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader`](#compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-trustforwardheader) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg. |
| [`compatibility.forwardauth-dynamic.http.routers`](#compatibility-forwardauth-dynamic-http-routers) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`compatibility.forwardauth-dynamic.http.routers.app`](#compatibility-forwardauth-dynamic-http-routers-app) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`compatibility.forwardauth-dynamic.http.routers.app.entryPoints`](#compatibility-forwardauth-dynamic-http-routers-app-entrypoints) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]`](#compatibility-forwardauth-dynamic-http-routers-app-entrypoints) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.forwardauth-dynamic.http.routers.app.middlewares`](#compatibility-forwardauth-dynamic-http-routers-app-middlewares) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.middlewares` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.middlewares` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`compatibility.forwardauth-dynamic.http.routers.app.middlewares[]`](#compatibility-forwardauth-dynamic-http-routers-app-middlewares) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`compatibility.forwardauth-dynamic.http.routers.app.rule`](#compatibility-forwardauth-dynamic-http-routers-app-rule) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.rule` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.rule` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.rule` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`compatibility.forwardauth-dynamic.http.routers.app.service`](#compatibility-forwardauth-dynamic-http-routers-app-service) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.service` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.service` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu. |
| [`compatibility.forwardauth-dynamic.http.services`](#compatibility-forwardauth-dynamic-http-services) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.services` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.services` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.services` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.forwardauth-dynamic.http.services.app`](#compatibility-forwardauth-dynamic-http-services-app) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.forwardauth-dynamic.http.services.app.loadBalancer`](#compatibility-forwardauth-dynamic-http-services-app-loadbalancer) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers`](#compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers) | Kompatibilität | YAML-Liste oder -Zuordnung | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url`](#compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers-url) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice. |
| [`compatibility.forwardauth-static.accessLog`](#compatibility-forwardauth-static-accesslog) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.accessLog` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.accessLog` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.accessLog` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden. |
| [`compatibility.forwardauth-static.entryPoints`](#compatibility-forwardauth-static-entrypoints) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.entryPoints` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.forwardauth-static.entryPoints.web`](#compatibility-forwardauth-static-entrypoints-web) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.entryPoints.web` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.entryPoints.web` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.entryPoints.web` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.forwardauth-static.entryPoints.web.address`](#compatibility-forwardauth-static-entrypoints-web-address) | Kompatibilität | YAML-Adressfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.entryPoints.web.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.entryPoints.web.address` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.entryPoints.web.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht. |
| [`compatibility.forwardauth-static.log`](#compatibility-forwardauth-static-log) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.log` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.log` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.log` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden. |
| [`compatibility.forwardauth-static.log.level`](#compatibility-forwardauth-static-log-level) | Kompatibilität | YAML-Steuerfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.log.level` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.log.level` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.log.level` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden. |
| [`compatibility.forwardauth-static.providers`](#compatibility-forwardauth-static-providers) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.providers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.providers` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.providers` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`compatibility.forwardauth-static.providers.file`](#compatibility-forwardauth-static-providers-file) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.providers.file` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.providers.file` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.providers.file` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`compatibility.forwardauth-static.providers.file.filename`](#compatibility-forwardauth-static-providers-file-filename) | Kompatibilität | YAML-Kennungsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.providers.file.filename` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.providers.file.filename` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.providers.file.filename` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`compatibility.forwardauth-static.providers.file.watch`](#compatibility-forwardauth-static-providers-file-watch) | Kompatibilität | YAML-Konfigurationsfeld | nein | Der Connector definiert für `compatibility.forwardauth-static.providers.file.watch` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest. | YAML-Pfad `compatibility.forwardauth-static.providers.file.watch` im ausgewählten Traefik-Template. | Das YAML-Feld `compatibility.forwardauth-static.providers.file.watch` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird. |
| [`forwardAuth`](#forwardauth) | Kompatibilität | Traefik-Kompatibilitäts-Middleware | nein | nicht Teil des ausgewählten nativen Middleware-Pfads | dynamische Kompatibilitäts-Middleware | forwardAuth-Middleware nur für die Kompatibilität. |

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
| Minimal | [minimal/traefik-static.yaml](minimal/traefik-static.yaml) | Aktive Startkonfiguration |
| Sicherer vollständiger Lebenszyklus | [safe/traefik-dynamic.yaml](safe/traefik-dynamic.yaml) | Ausgewählte begrenzte Referenz |
| Strikt | [README.de.md#strict-profilgrenze](README.de.md#strict-profilgrenze) | Parserunterstützte oder ausdrücklich optionale Grenze |
| DetectionOnly | [detection-only/traefik-engine-service.conf](detection-only/traefik-engine-service.conf) | Engine wertet aus/protokolliert ohne disruptive Aktion |
| Deaktiviert | [disabled/traefik-engine-service.conf](disabled/traefik-engine-service.conf) | Connector- oder Engine-Pfad deaktiviert |

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
traefik check --configFile=<static-config>
```

Repository-Ziele: `make check-config-traefik` und `make check-config-all-connectors`.

## Optionsdetails

<a id="accesslog"></a>
## `accessLog`

### Kurzbeschreibung

Das YAML-Feld `accessLog` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Syntax

```text
accessLog: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `accessLog` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `accessLog` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `accessLog` die Protokollierung konfiguriert.

Das YAML-Feld `accessLog` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `{}`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik access-log configuration mapping
allowed_values: empty mapping or documented access-log fields; selected value is {}
default: No connector-owned access-log configuration default is declared; the selected template sets an empty configuration mapping.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Host observability only; it does not substitute for transaction P1–P4 processing or engine audit logging.
security_relevance: Access logs can contain request metadata; configure safe storage, rotation, and privacy controls for deployment.
runtime_effect: Enables/configures the Traefik access-log surface in the selected static example.
description: Enables/configures the Traefik access-log surface in the selected static example.
```

<a id="entrypoints"></a>
## `entryPoints`

### Kurzbeschreibung

Das YAML-Feld `entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
entryPoints: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `entryPoints` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `entryPoints` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik static entry-point mapping
allowed_values: named entry-point mappings; selected key is web
default: No connector-owned entry-point registry default is declared; the selected template sets the web listener.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static listener bootstrap; its named entry point selects which requests can reach the router/middleware lifecycle.
security_relevance: Entry-point addresses define the pre-policy network exposure of Traefik.
runtime_effect: Groups named listener definitions used by dynamic routers.
description: Groups named listener definitions used by dynamic routers.
```

<a id="entrypoints-web"></a>
## `entryPoints.web`

### Kurzbeschreibung

Das YAML-Feld `entryPoints.web` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
entryPoints.web: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `entryPoints.web` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `entryPoints.web` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `entryPoints.web` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `entryPoints.web` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik EntryPoint mapping
allowed_values: address child field; selected entry point is web
default: No connector-owned web entry point default is declared; the selected template sets the :8080 listener.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static entry point for the router; the native middleware begins after request routing selects it.
security_relevance: Changing this listener changes client reachability before middleware enforcement.
runtime_effect: Defines the named web listener that dynamic routers attach to.
description: Defines the named web listener that dynamic routers attach to.
```

<a id="entrypoints-web-address"></a>
## `entryPoints.web.address`

### Kurzbeschreibung

Das YAML-Feld `entryPoints.web.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
entryPoints.web.address: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `entryPoints.web.address` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `entryPoints.web.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `entryPoints.web.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `entryPoints.web.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `":8080"`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik listener address string
allowed_values: Traefik entry-point address such as host:port or :port; selected value is :8080
default: No connector-owned web listener address default is declared; the selected template sets :8080.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Listener bootstrap before router selection and the attached native P1–P4 middleware path.
security_relevance: The selected :8080 form changes listener exposure according to host networking; use a private bind or explicit edge control as appropriate.
runtime_effect: Binds the named web entry point used by the example router.
description: Binds the named web entry point used by the example router.
```

<a id="experimental"></a>
## `experimental`

### Kurzbeschreibung

Das YAML-Feld `experimental` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.

### Syntax

```text
experimental: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `experimental` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `experimental` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `experimental` die Host-/Connector-YAML-Konfiguration konfiguriert.

Das YAML-Feld `experimental` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Die Auswirkung auf Netzwerk, Routing und Policy vor dem Einsatz mit dem dokumentierten Template und Quellanker prüfen.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik static experimental configuration mapping
allowed_values: localPlugins child mapping shown in the selected native static file
default: No connector-owned experimental configuration default is declared; the selected template sets the modsecurityNative local-plugin declaration.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static bootstrap prerequisite for the native P1–P4 middleware path; it does not process traffic itself.
security_relevance: Local plugin loading executes selected repository code; pin and review the module source before use.
runtime_effect: Groups static experimental features needed to make the repository-owned local plugin discoverable.
description: Groups static experimental features needed to make the repository-owned local plugin discoverable.
```

<a id="experimental-localplugins"></a>
## `experimental.localPlugins`

### Kurzbeschreibung

Das YAML-Feld `experimental.localPlugins` konfiguriert die lokale Plugin-Konfiguration. Sie verbindet den Host mit der ausgewählten lokalen Plugin-Implementierung und ihren Einstellungen.

### Syntax

```text
experimental.localPlugins: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `experimental.localPlugins` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `experimental.localPlugins` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `experimental.localPlugins` die lokale Plugin-Konfiguration konfiguriert.

Das YAML-Feld `experimental.localPlugins` konfiguriert die lokale Plugin-Konfiguration. Sie verbindet den Host mit der ausgewählten lokalen Plugin-Implementierung und ihren Einstellungen.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Nur überprüfte lokale Plugin-Pfade, Module und Einstellungen verwenden; Änderungen können den Prüfpfad ersetzen.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik static local-plugin registry mapping
allowed_values: named local plugin declarations; selected key is modsecurityNative
default: No connector-owned local-plugin registry default is declared; the selected template sets one modsecurityNative declaration.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static bootstrap prerequisite for the native router middleware and its P1–P4 callback surface.
security_relevance: A registry entry selects executable plugin source; do not add unreviewed local modules.
runtime_effect: Registers the local plugin name that dynamic middleware configuration later references.
description: Registers the local plugin name that dynamic middleware configuration later references.
```

<a id="experimental-localplugins-modsecuritynative"></a>
## `experimental.localPlugins.modsecurityNative`

### Kurzbeschreibung

Das YAML-Feld `experimental.localPlugins.modsecurityNative` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
experimental.localPlugins.modsecurityNative: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `experimental.localPlugins.modsecurityNative` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `experimental.localPlugins.modsecurityNative` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `experimental.localPlugins.modsecurityNative` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `experimental.localPlugins.modsecurityNative` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik local-plugin declaration mapping
allowed_values: moduleName and settings child fields
default: No connector-owned modsecurityNative declaration default is declared; the selected template sets the repository module and empty environment settings.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static prerequisite for attaching the native middleware; no transaction lifecycle event occurs at declaration time.
security_relevance: The declaration controls which local code Traefik loads; protect its configuration and source tree.
runtime_effect: Binds the dynamic plugin name modsecurityNative to its local module configuration.
description: Binds the dynamic plugin name modsecurityNative to its local module configuration.
```

<a id="experimental-localplugins-modsecuritynative-modulename"></a>
## `experimental.localPlugins.modsecurityNative.moduleName`

### Kurzbeschreibung

Das YAML-Feld `experimental.localPlugins.modsecurityNative.moduleName` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
experimental.localPlugins.modsecurityNative.moduleName: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `experimental.localPlugins.modsecurityNative.moduleName` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `experimental.localPlugins.modsecurityNative.moduleName` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `experimental.localPlugins.modsecurityNative.moduleName` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `experimental.localPlugins.modsecurityNative.moduleName` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik local-plugin Go module path string
allowed_values: module path resolving to the repository native_middleware package
default: No connector-owned local-plugin module path default is declared; the selected template sets github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static prerequisite for the native middleware's P1–P4 callback implementation.
security_relevance: This is code-selection input; use a reviewed, pinned source path and do not substitute an arbitrary module.
runtime_effect: Selects the Go module/package Traefik loads for the modsecurityNative local plugin.
description: Selects the Go module/package Traefik loads for the modsecurityNative local plugin.
```

<a id="experimental-localplugins-modsecuritynative-settings"></a>
## `experimental.localPlugins.modsecurityNative.settings`

### Kurzbeschreibung

Das YAML-Feld `experimental.localPlugins.modsecurityNative.settings` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
experimental.localPlugins.modsecurityNative.settings: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `experimental.localPlugins.modsecurityNative.settings` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `experimental.localPlugins.modsecurityNative.settings` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `experimental.localPlugins.modsecurityNative.settings` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `experimental.localPlugins.modsecurityNative.settings` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik local-plugin settings mapping
allowed_values: settings.envs child list; selected mapping contains an empty list
default: No connector-owned local-plugin settings default is declared; the selected template sets an empty envs list.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static bootstrap only; the selected native request lifecycle starts when a router invokes the plugin.
security_relevance: Avoid placing credentials or production-specific secrets in plugin settings.
runtime_effect: Groups host-level settings for the selected local-plugin declaration.
description: Groups host-level settings for the selected local-plugin declaration.
```

<a id="experimental-localplugins-modsecuritynative-settings-envs"></a>
## `experimental.localPlugins.modsecurityNative.settings.envs`

### Kurzbeschreibung

Das YAML-Feld `experimental.localPlugins.modsecurityNative.settings.envs` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
experimental.localPlugins.modsecurityNative.settings.envs: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `experimental.localPlugins.modsecurityNative.settings.envs` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `experimental.localPlugins.modsecurityNative.settings.envs` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `experimental.localPlugins.modsecurityNative.settings.envs` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `experimental.localPlugins.modsecurityNative.settings.envs` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `[]`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik local-plugin environment-settings list
allowed_values: list of Traefik local-plugin environment setting strings; selected list is empty
default: Selected value is []; no example-provided plugin environment setting is added.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static bootstrap only; it does not change P1–P4 visibility by itself.
security_relevance: An environment setting can carry secrets or change behavior; keep the selected empty list unless an explicit documented input is required.
runtime_effect: Leaves the local-plugin declaration without example-provided environment inputs.
description: Leaves the local-plugin declaration without example-provided environment inputs.
```

<a id="http"></a>
## `http`

### Kurzbeschreibung

Das YAML-Feld `http` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.

### Syntax

```text
http: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http` die Host-/Connector-YAML-Konfiguration konfiguriert.

Das YAML-Feld `http` konfiguriert die Host-/Connector-YAML-Konfiguration. Sie konfiguriert einen quellenbasierten Teil des ausgewählten Host- und Connectorpfads.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Die Auswirkung auf Netzwerk, Routing und Policy vor dem Einsatz mit dem dokumentierten Template und Quellanker prüfen.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic HTTP configuration mapping
allowed_values: routers, middlewares, and services child mappings
default: No connector-owned dynamic HTTP topology default is declared; the selected template sets one app router, one middleware, and one app service.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: This topology controls which requests reach the engine and which upstream receives them; protect dynamic configuration writes.
runtime_effect: Groups the request router, middleware attachment, and upstream service used by the example.
description: Groups the request router, middleware attachment, and upstream service used by the example.
```

<a id="http-middlewares"></a>
## `http.middlewares`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `http.middlewares` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic middleware registry mapping
allowed_values: named middleware mappings; selected key is modsecurity-native-streaming
default: No connector-owned middleware registry default is declared; the selected template sets the selected native or compatibility middleware.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: Middleware definitions are policy attachment points; unreviewed changes can remove or replace inspection.
runtime_effect: Groups middleware definitions referenced by routers.
description: Groups middleware definitions referenced by routers.
```

<a id="http-middlewares-modsecurity-native-streaming"></a>
## `http.middlewares.modsecurity-native-streaming`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.middlewares.modsecurity-native-streaming` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.middlewares.modsecurity-native-streaming` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik named middleware mapping
allowed_values: one native modsecurity middleware configuration mapping
default: No connector-owned named middleware default is declared; the selected template sets the selected native modsecurity mapping.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: The router reference must continue to point to this reviewed middleware name to avoid bypass.
runtime_effect: Binds the router-visible middleware name to its plugin or forwardAuth configuration.
description: Binds the router-visible middleware name to its plugin or forwardAuth configuration.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin"></a>
## `http.middlewares.modsecurity-native-streaming.plugin`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.middlewares.modsecurity-native-streaming.plugin` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.middlewares.modsecurity-native-streaming.plugin` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik plugin middleware mapping
allowed_values: named local-plugin child mapping; selected child is modsecurityNative
default: No connector-owned plugin middleware mapping default is declared; the selected template sets the modsecurityNative local plugin.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: The plugin reference chooses code that processes requests and responses; preserve the reviewed local plugin name.
runtime_effect: Selects the local-plugin configuration for the named native middleware.
description: Selects the local-plugin configuration for the named native middleware.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik local-plugin configuration mapping
allowed_values: the seven native middleware Config fields documented from CreateConfig/normalizedConfig
default: Plugin CreateConfig supplies bounded defaults; this template explicitly sets all seven selected fields.
default_source: connectors/traefik/native_middleware/middleware.go:CreateConfig/normalizedConfig
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: The UDS fields and bounds are enforcement-relevant; passthrough is not rule evaluation.
runtime_effect: Groups limits, transaction ID, and engine connection fields passed to the repository native middleware.
description: Groups limits, transaction ID, and engine connection fields passed to the repository native middleware.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginemode"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode`

### Kurzbeschreibung

Wählt source-only-passthrough oder die persistente UDS-Engine; das ausgewählte regelauswertende Beispiel verwendet uds.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode: <engineMode>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | passthrough \| uds | nein |

### Standardwert

passthrough

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineMode` die Middleware-Anbindung konfiguriert.

Wählt source-only-passthrough oder die persistente UDS-Engine; das ausgewählte regelauswertende Beispiel verwendet uds.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `uds`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: native middleware engine-mode enum
phase_relevance: passthrough always allows and supplies no rule evaluation; uds is the engine transport for native P1/P2/P3/P4 callbacks.
security_relevance: Use uds for the selected rule-evaluating path; passthrough is intentionally not enforcement.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-enginesocketpath"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath`

### Kurzbeschreibung

Benennt den privaten UDS-Pfad, den die native Middleware bei engineMode=uds verwendet.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath: <engineSocketPath>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | für uds erforderlich; absolut und ohne NUL- oder '..'-Segment | nein |

### Standardwert

Der Connector definiert für `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.engineSocketPath` die Middleware-Anbindung konfiguriert.

Benennt den privaten UDS-Pfad, den die native Middleware bei engineMode=uds verwendet.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `/run/traefik-msconnector/engine.sock`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: absolute Unix-domain socket path
default: none (ignored outside uds; required and validated in uds mode)
phase_relevance: Transport endpoint for native P1/P2/P3/P4 engine callbacks when uds mode is selected.
security_relevance: The socket directory and socket must be private to trusted processes; path traversal and NUL are rejected.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheaderbytes"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes: <maxHeaderBytes>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Limitfeld | positiv; UDS-Maximum 65536 | nein |

### Standardwert

65536

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `65536`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: integer aggregate header-byte bound
phase_relevance: P1 request-header and P3 response-header callback byte bound.
security_relevance: The UDS wire contract rejects values above 65536; retain a bounded header budget.
runtime_effect: Caps aggregate request and response header bytes passed to native middleware engine callbacks.
description: Caps aggregate request and response header bytes passed to native middleware engine callbacks.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxheadercount"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount: <maxHeaderCount>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Limitfeld | positiv; UDS-Maximum 128 | nein |

### Standardwert

128

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxHeaderCount` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `128`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: integer header-count bound
phase_relevance: P1 request-header and P3 response-header callback bound; it does not buffer body bytes.
security_relevance: A finite count limits header-flood work before data reaches the UDS engine.
runtime_effect: Caps the number of request and response headers passed to native middleware engine callbacks.
description: Caps the number of request and response headers passed to native middleware engine callbacks.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxrequestchunkbytes"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes: <maxRequestChunkBytes>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Limitfeld | positiv; UDS-Maximum 32768 | nein |

### Standardwert

32768

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxRequestChunkBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `32768`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: integer request-body chunk-byte bound
phase_relevance: P2 request-body callback bound; it is a per-chunk limit, not a total request-body limit.
security_relevance: The UDS wire contract rejects values above 32768 and prevents one callback from accepting an unbounded chunk.
runtime_effect: Caps each streamed request-body chunk offered to the native middleware engine.
description: Caps each streamed request-body chunk offered to the native middleware engine.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-maxresponsechunkbytes"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes: <maxResponseChunkBytes>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Limitfeld | positiv; UDS-Maximum 32768 | nein |

### Standardwert

32768

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.maxResponseChunkBytes` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `32768`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: integer response-body chunk-byte bound
phase_relevance: P4 response-body callback bound; a late disruptive result remains log-only after response commitment.
security_relevance: The UDS wire contract rejects values above 32768; retain the bound for response-stream resource control.
runtime_effect: Caps each streamed response-body chunk offered to the native middleware engine.
description: Caps each streamed response-body chunk offered to the native middleware engine.
```

<a id="http-middlewares-modsecurity-native-streaming-plugin-modsecuritynative-transactionidheader"></a>
## `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader`

### Kurzbeschreibung

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader: <transactionIDHeader>
```

### Gültige Kontexte

- http.middlewares.<name>.plugin.modsecurityNative

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | nichtleerer Headername ohne Leerraum | nein |

### Standardwert

X-Request-Id

Quelle: `connectors/traefik/native_middleware/middleware.go:CreateConfig`.

### Vererbung und Zusammenführung

Dynamisches Traefik-Konfigurationsobjekt; kein Common-Runtime-Merge.

Zusammenführung: Die Traefik-/Plugin-Konfiguration wird einmalig durch das Plugin normalisiert.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `http.middlewares.modsecurity-native-streaming.plugin.modsecurityNative.transactionIDHeader` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

normalizedConfig weist ungültige Werte ab; Traefik parst die enthaltende dynamische Konfiguration.

### Beispiel

Ausgewählter Beispielwert: `X-Request-Id`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: HTTP header-name string
phase_relevance: P1 request-header metadata selection; the value is carried through later lifecycle summaries, not used as a policy rule by itself.
security_relevance: Do not put credentials or arbitrary sensitive payload into a correlation header; event/log consumers must protect it.
runtime_effect: Selects the incoming request header used to correlate middleware and engine transaction metadata.
description: Selects the incoming request header used to correlate middleware and engine transaction metadata.
```

<a id="http-routers"></a>
## `http.routers`

### Kurzbeschreibung

Das YAML-Feld `http.routers` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
http.routers: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.routers` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `http.routers` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic router registry mapping
allowed_values: named router mappings; selected key is app
default: No connector-owned router registry default is declared; the selected template sets one app router.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: Router rules and middleware order are enforcement-relevant; avoid unaudited route additions.
runtime_effect: Groups dynamic request-routing definitions.
description: Groups dynamic request-routing definitions.
```

<a id="http-routers-app"></a>
## `http.routers.app`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
http.routers.app: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.routers.app` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `http.routers.app` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic Router mapping
allowed_values: rule, entryPoints, middlewares, and service child fields
default: No connector-owned app router default is declared; the selected template sets the explicit catch-all app route.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: The router is the attachment point for the native UDS middleware or compatibility forwardAuth; removing it bypasses that path.
runtime_effect: Binds a request rule and entry point to the listed middleware and app service.
description: Binds a request rule and entry point to the listed middleware and app service.
```

<a id="http-routers-app-entrypoints"></a>
## `http.routers.app.entryPoints`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
http.routers.app.entryPoints: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.routers.app.entryPoints` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app.entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app.entryPoints` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `http.routers.app.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `["web"]`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik router entry-point name list
allowed_values: defined static entry-point names
default: No connector-owned router entry-point binding default is declared; the selected template sets the web entry point.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path.
security_relevance: Binding a router to a public entry point exposes its middleware/service path to that listener's clients.
runtime_effect: Restricts the app router to the named static listener.
description: Restricts the app router to the named static listener.
```

<a id="http-routers-app-entrypoints"></a>
## `http.routers.app.entryPoints[]`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app.entryPoints[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
http.routers.app.entryPoints[]: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `http.routers.app.entryPoints[]` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app.entryPoints[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app.entryPoints[]` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `http.routers.app.entryPoints[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `"web"`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik entry-point name string
allowed_values: name declared under static entryPoints; selected value is web
default: No connector-owned router entry-point binding default is declared; the selected template sets the web entry point.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path.
security_relevance: Binding a router to a public entry point exposes its middleware/service path to that listener's clients.
runtime_effect: Restricts the app router to the named static listener.
description: Restricts the app router to the named static listener.
```

<a id="http-routers-app-middlewares"></a>
## `http.routers.app.middlewares`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app.middlewares` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
http.routers.app.middlewares: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `http.routers.app.middlewares` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app.middlewares` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `http.routers.app.middlewares` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `["modsecurity-native-streaming"]`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: ordered Traefik middleware-name list
allowed_values: names declared under http.middlewares
default: No connector-owned router middleware list default is declared; the selected template sets the selected native UDS middleware.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service.
runtime_effect: Attaches middleware to the router in listed order before forwarding to the app service.
description: Attaches middleware to the router in listed order before forwarding to the app service.
```

<a id="http-routers-app-middlewares"></a>
## `http.routers.app.middlewares[]`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app.middlewares[]` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
http.routers.app.middlewares[]: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `http.routers.app.middlewares[]` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app.middlewares[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app.middlewares[]` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `http.routers.app.middlewares[]` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `"modsecurity-native-streaming"`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik middleware-name string
allowed_values: selected native UDS middleware name
default: No connector-owned router middleware list default is declared; the selected template sets the selected native UDS middleware.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware is attached to the router; its source-defined streaming callbacks cover P1/P2/P3/P4 when the UDS engine path is running. Configuration alone is not runtime evidence.
security_relevance: Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service.
runtime_effect: Attaches middleware to the router in listed order before forwarding to the app service.
description: Attaches middleware to the router in listed order before forwarding to the app service.
```

<a id="http-routers-app-rule"></a>
## `http.routers.app.rule`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app.rule` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
http.routers.app.rule: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.routers.app.rule` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app.rule` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app.rule` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `http.routers.app.rule` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: ``PathPrefix(`/`)``.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik router-rule expression string
allowed_values: Traefik rule DSL; selected value is PathPrefix(`/`)
default: No connector-owned app router rule default is declared; the selected template sets the catch-all PathPrefix(`/`) expression.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Selects requests that enter the attached native middleware P1/P2 path or compatibility P1 authorization path.
security_relevance: The selected catch-all rule routes every path on the entry point; narrow it in a real deployment if required.
runtime_effect: Matches incoming requests to the app router.
description: Matches incoming requests to the app router.
```

<a id="http-routers-app-service"></a>
## `http.routers.app.service`

### Kurzbeschreibung

Das YAML-Feld `http.routers.app.service` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
http.routers.app.service: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.routers.app.service` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.routers.app.service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.routers.app.service` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `http.routers.app.service` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `"app"`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik service-name string
allowed_values: name declared under http.services; selected value is app
default: No connector-owned router service target default is declared; the selected template sets the app service.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Forwarding occurs after request-side middleware; the native path can observe the returned response at P3/P4.
security_relevance: The target service URL is an egress destination; review it separately from middleware selection.
runtime_effect: Selects the upstream service after router middleware completes.
description: Selects the upstream service after router middleware completes.
```

<a id="http-services"></a>
## `http.services`

### Kurzbeschreibung

Das YAML-Feld `http.services` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
http.services: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `http.services` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.services` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.services` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `http.services` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic service registry mapping
allowed_values: named service mappings; selected key is app
default: No connector-owned service registry default is declared; the selected template sets the app load-balancer service.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The native middleware can receive the app response at P3/P4 after this service returns it; compatibility forwardAuth cannot.
security_relevance: Services define request destinations after middleware; review their endpoint URLs and credentials.
runtime_effect: Groups upstream service definitions referenced by routers.
description: Groups upstream service definitions referenced by routers.
```

<a id="http-services-app"></a>
## `http.services.app`

### Kurzbeschreibung

Das YAML-Feld `http.services.app` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
http.services.app: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.services.app` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.services.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.services.app` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `http.services.app` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik named service mapping
allowed_values: loadBalancer child mapping
default: No connector-owned app service default is declared; the selected template sets one load-balancer with a loopback server.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Upstream service stage after request middleware; native response callbacks can observe returned headers/body at P3/P4.
security_relevance: This mapping is an upstream routing target; do not confuse it with the ModSecurity engine service.
runtime_effect: Binds the router's app service name to its load balancer.
description: Binds the router's app service name to its load balancer.
```

<a id="http-services-app-loadbalancer"></a>
## `http.services.app.loadBalancer`

### Kurzbeschreibung

Das YAML-Feld `http.services.app.loadBalancer` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
http.services.app.loadBalancer: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `http.services.app.loadBalancer` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.services.app.loadBalancer` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.services.app.loadBalancer` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `http.services.app.loadBalancer` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik LoadBalancer service mapping
allowed_values: servers child list
default: No connector-owned app load balancer default is declared; the selected template sets one loopback app server.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: After request middleware, the selected server response is available to native P3/P4 callbacks; not to compatibility forwardAuth.
security_relevance: Each server URL is a traffic destination; limit it to the intended upstream.
runtime_effect: Groups the upstream server endpoints for the app service.
description: Groups the upstream server endpoints for the app service.
```

<a id="http-services-app-loadbalancer-servers"></a>
## `http.services.app.loadBalancer.servers`

### Kurzbeschreibung

Das YAML-Feld `http.services.app.loadBalancer.servers` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
http.services.app.loadBalancer.servers: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `http.services.app.loadBalancer.servers` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.services.app.loadBalancer.servers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.services.app.loadBalancer.servers` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `http.services.app.loadBalancer.servers` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Traefik load-balancer server mapping
allowed_values: one or more server URL mappings; selected example has one server
default: No connector-owned app server list default is declared; the selected template sets one http://127.0.0.1:8081 endpoint.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Native response lifecycle P3/P4 begins only after the selected server responds; compatibility forwardAuth remains request-only.
security_relevance: Adding a server adds an upstream destination; review network scope and transport security.
runtime_effect: Defines the endpoint candidates for the app load balancer.
description: Defines the endpoint candidates for the app load balancer.
```

<a id="http-services-app-loadbalancer-servers-url"></a>
## `http.services.app.loadBalancer.servers[].url`

### Kurzbeschreibung

Das YAML-Feld `http.services.app.loadBalancer.servers[].url` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
http.services.app.loadBalancer.servers[].url: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `http.services.app.loadBalancer.servers[].url` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `http.services.app.loadBalancer.servers[].url` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `http.services.app.loadBalancer.servers[].url` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `http.services.app.loadBalancer.servers[].url` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `http://127.0.0.1:8081`.

Quellenbasiertes Beispiel: [examples/traefik/safe/traefik-dynamic.yaml](../../examples/traefik/safe/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik upstream server URL string
allowed_values: absolute backend URL; selected value is http://127.0.0.1:8081
default: No connector-owned app server URL default is declared; the selected template sets http://127.0.0.1:8081.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: The returned upstream response is the native middleware's P3/P4 source; forwardAuth compatibility has no later response visibility.
security_relevance: Loopback keeps the example local; remote URLs require explicit TLS, identity, and egress controls.
runtime_effect: Targets the application server that receives requests after router middleware.
description: Targets the application server that receives requests after router middleware.
```

<a id="log"></a>
## `log`

### Kurzbeschreibung

Das YAML-Feld `log` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Syntax

```text
log: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `log` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `log` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `log` die Protokollierung konfiguriert.

Das YAML-Feld `log` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik log configuration mapping
allowed_values: level child field
default: No connector-owned log configuration default is declared; the selected template sets level INFO.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Host observability only; no direct P1–P4 payload visibility change.
security_relevance: Logs can contain request and operational metadata; choose retention and access controls separately.
runtime_effect: Groups Traefik process-log settings.
description: Groups Traefik process-log settings.
```

<a id="log-level"></a>
## `log.level`

### Kurzbeschreibung

Das YAML-Feld `log.level` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Syntax

```text
log.level: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | Die zulässige Ausprägung von `log.level` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `log.level` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `log.level` die Protokollierung konfiguriert.

Das YAML-Feld `log.level` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `INFO`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik log-level token
allowed_values: Traefik-supported level token; selected value is INFO
default: No connector-owned log level default is declared; the selected template sets INFO.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Host observability only; it does not change native or compatibility lifecycle callbacks.
security_relevance: Debug logging can expose more operational metadata; do not equate host logs with ModSecurity audit output.
runtime_effect: Controls Traefik process-log verbosity.
description: Controls Traefik process-log verbosity.
```

<a id="providers"></a>
## `providers`

### Kurzbeschreibung

Das YAML-Feld `providers` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
providers: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `providers` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `providers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `providers` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `providers` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik static provider registry mapping
allowed_values: file provider child mapping
default: No connector-owned provider registry default is declared; the selected template sets the adjacent dynamic File Provider.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Static-to-dynamic handoff; it makes the router/middleware lifecycle available but does not process a transaction itself.
security_relevance: A provider controls live routing configuration; protect its source file and directory.
runtime_effect: Groups configuration providers that supply dynamic routers, middlewares, and services.
description: Groups configuration providers that supply dynamic routers, middlewares, and services.
```

<a id="providers-file"></a>
## `providers.file`

### Kurzbeschreibung

Das YAML-Feld `providers.file` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
providers.file: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `providers.file` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `providers.file` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `providers.file` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `providers.file` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik File Provider mapping
allowed_values: filename and watch child fields
default: No connector-owned file provider default is declared; the selected template sets the adjacent traefik-dynamic.yaml file.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Loads the router/middleware configuration that exposes the native lifecycle path or compatibility request path.
security_relevance: The dynamic file can alter routes and middleware; grant write access only to trusted operators.
runtime_effect: Configures the on-disk dynamic configuration provider.
description: Configures the on-disk dynamic configuration provider.
```

<a id="providers-file-filename"></a>
## `providers.file.filename`

### Kurzbeschreibung

Das YAML-Feld `providers.file.filename` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
providers.file.filename: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `providers.file.filename` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `providers.file.filename` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `providers.file.filename` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `providers.file.filename` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `"./traefik-dynamic.yaml"`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik File Provider path string
allowed_values: readable dynamic-configuration path; selected relative path is ./traefik-dynamic.yaml
default: No connector-owned dynamic file path default is declared; the selected template sets ./traefik-dynamic.yaml.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Supplies the routing configuration that attaches native P1–P4 middleware or compatibility P1 authorization.
security_relevance: A relative path resolves from the host configuration context; deploy the matching file together and protect it from untrusted writes.
runtime_effect: Selects the companion dynamic file containing routers, middleware, and upstream service definitions.
description: Selects the companion dynamic file containing routers, middleware, and upstream service definitions.
```

<a id="providers-file-watch"></a>
## `providers.file.watch`

### Kurzbeschreibung

Das YAML-Feld `providers.file.watch` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
providers.file.watch: <value>
```

### Gültige Kontexte

- Der im ausgewählten Beispiel gezeigte YAML-Objektpfad.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | true \| false | nein |

### Standardwert

Der Connector definiert für `providers.file.watch` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Durch Host-YAML/API bestimmt; keine Common-Runtime-Merge-Einstellung.

Zusammenführung: Durch Host-YAML/API bestimmt; eingecheckte statische und dynamische Konfigurationen sind getrennte Ebenen.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `providers.file.watch` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `providers.file.watch` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

traefik check --configFile=<static-config>; die ausgewählte File-Provider-Konfiguration laden.

### Beispiel

Ausgewählter Beispielwert: `false`.

Quellenbasiertes Beispiel: [examples/traefik/minimal/traefik-static.yaml](../../examples/traefik/minimal/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik File Provider boolean
default: No connector-owned File Provider watch behavior default is declared; the selected template sets false.
default_source: selected Traefik example; no connector-owned Traefik host default
phase_relevance: Dynamic lifecycle configuration reload control; it does not itself change per-request P1–P4 visibility.
security_relevance: watch=true makes future file writes live configuration changes; selected native file uses false, compatibility example uses true.
runtime_effect: Controls whether Traefik watches the dynamic file for reloads after initial load.
description: Controls whether Traefik watches the dynamic file for reloads after initial load.
```

<a id="compatibility-forwardauth-dynamic-http"></a>
## `compatibility.forwardauth-dynamic.http`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http` konfiguriert die Kompatibilitätsintegration. Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads.

### Syntax

```text
compatibility.forwardauth-dynamic.http: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http` die Kompatibilitätsintegration konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http` konfiguriert die Kompatibilitätsintegration. Sie konfiguriert einen getrennten Kompatibilitätspfad außerhalb des ausgewählten nativen Kernpfads.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Diese Einstellung nicht als Nachweis einer nativen Full-Lifecycle-Integration verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic HTTP configuration mapping
allowed_values: routers, middlewares, and services child mappings
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: This topology controls which requests reach the engine and which upstream receives them; protect dynamic configuration writes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the request router, middleware attachment, and upstream service used by the example. Compatibility-only host/service setup outside the selected native core path.
description: Groups the request router, middleware attachment, and upstream service used by the example. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-middlewares"></a>
## `compatibility.forwardauth-dynamic.http.middlewares`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.middlewares` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.middlewares` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic middleware registry mapping
allowed_values: named middleware mappings; selected key is modsecurity-auth
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Middleware definitions are policy attachment points; unreviewed changes can remove or replace inspection. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups middleware definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.
description: Groups middleware definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik named middleware mapping
allowed_values: one forwardAuth compatibility middleware configuration mapping
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: The router reference must continue to point to this reviewed middleware name to avoid bypass. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Binds the router-visible middleware name to its plugin or forwardAuth configuration. Compatibility-only host/service setup outside the selected native core path.
description: Binds the router-visible middleware name to its plugin or forwardAuth configuration. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik ForwardAuth middleware mapping (compatibility only)
allowed_values: address and trustForwardHeader child fields
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Do not present forwardAuth as the native UDS rule-evaluating path; its service receives request authorization data. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the request-only external authorization service settings. Compatibility-only host/service setup outside the selected native core path.
description: Groups the request-only external authorization service settings. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-address"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"http://127.0.0.1:9000/authorize"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik ForwardAuth HTTP URL string (compatibility only)
allowed_values: absolute HTTP/HTTPS authorization-service URL; selected value is http://127.0.0.1:9000/authorize
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "http://127.0.0.1:9000/authorize".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Use a trusted, private service and do not embed credentials in the URL; it is distinct from the native UDS engine. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Targets the external forwardAuth decision service before the app service is contacted. Compatibility-only host/service setup outside the selected native core path.
description: Targets the external forwardAuth decision service before the app service is contacted. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-middlewares-modsecurity-auth-forwardauth-trustforwardheader"></a>
## `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Syntax

```text
compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | true \| false | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` die Middleware-Anbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.middlewares.modsecurity-auth.forwardAuth.trustForwardHeader` konfiguriert die Middleware-Anbindung. Sie bindet die ausgewählte Middleware an den Request- und Response-Verarbeitungsweg.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `false`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Middleware-Referenzen und ihre Reihenfolge müssen erhalten bleiben, damit die geprüfte Sicherheitsverarbeitung nicht umgangen wird.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik ForwardAuth boolean (compatibility only)
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures false.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: false avoids trusting client-supplied forwarded identity/route headers by default; deploy explicit proxy trust boundaries if changing it. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Controls whether forwarded request headers are trusted when calling the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
description: Controls whether forwarded request headers are trusted when calling the compatibility authorization service. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers"></a>
## `compatibility.forwardauth-dynamic.http.routers`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic router registry mapping
allowed_values: named router mappings; selected key is app
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Router rules and middleware order are enforcement-relevant; avoid unaudited route additions. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups dynamic request-routing definitions. Compatibility-only host/service setup outside the selected native core path.
description: Groups dynamic request-routing definitions. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app"></a>
## `compatibility.forwardauth-dynamic.http.routers.app`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic Router mapping
allowed_values: rule, entryPoints, middlewares, and service child fields
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: The router is the attachment point for the native UDS middleware or compatibility forwardAuth; removing it bypasses that path. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Binds a request rule and entry point to the listed middleware and app service. Compatibility-only host/service setup outside the selected native core path.
description: Binds a request rule and entry point to the listed middleware and app service. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app-entrypoints"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.entryPoints`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.entryPoints: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `["web"]`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik router entry-point name list
allowed_values: defined static entry-point names
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["web"].
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Binding a router to a public entry point exposes its middleware/service path to that listener's clients. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.
description: Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app-entrypoints"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.entryPoints[]` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"web"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik entry-point name string
allowed_values: name declared under static entryPoints; selected value is web
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "web".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Selects which listener traffic can reach the attached native P1–P4 middleware or compatibility request path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Binding a router to a public entry point exposes its middleware/service path to that listener's clients. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.
description: Restricts the app router to the named static listener. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app-middlewares"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.middlewares`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.middlewares` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.middlewares: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.middlewares` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app.middlewares` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.middlewares` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app.middlewares` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.middlewares` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `["modsecurity-auth"]`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: ordered Traefik middleware-name list
allowed_values: names declared under http.middlewares
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ["modsecurity-auth"].
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.
description: Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app-middlewares"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.middlewares[]: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.middlewares[]` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"modsecurity-auth"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik middleware-name string
allowed_values: selected compatibility forwardAuth middleware name
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "modsecurity-auth".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Compatibility forwardAuth runs before upstream handling for request authorization; it has no selected P3/P4 response-header/body visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Removing/reordering this reference can bypass inspection or authorization; retain the reviewed middleware before the service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.
description: Attaches middleware to the router in listed order before forwarding to the app service. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app-rule"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.rule`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.rule` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.rule: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.rule` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app.rule` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.rule` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app.rule` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.rule` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: ``"PathPrefix(`/`)"``.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik router-rule expression string
allowed_values: Traefik rule DSL; selected value is PathPrefix(`/`)
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "PathPrefix(`/`)".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Selects requests that enter the attached native middleware P1/P2 path or compatibility P1 authorization path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: The selected catch-all rule routes every path on the entry point; narrow it in a real deployment if required. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Matches incoming requests to the app router. Compatibility-only host/service setup outside the selected native core path.
description: Matches incoming requests to the app router. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-routers-app-service"></a>
## `compatibility.forwardauth-dynamic.http.routers.app.service`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.service` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Syntax

```text
compatibility.forwardauth-dynamic.http.routers.app.service: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.routers.app.service` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.routers.app.service` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.routers.app.service` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.routers.app.service` die Request-Routing-Entscheidung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.routers.app.service` konfiguriert die Request-Routing-Entscheidung. Sie ordnet eingehende Requests einer Route, Middleware oder einem Upstream zu.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"app"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Eine Änderung der Reihenfolge oder Zielzuordnung kann die Inspektion umgehen; nur geprüfte Routen und Zielservices verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik service-name string
allowed_values: name declared under http.services; selected value is app
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "app".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Forwarding occurs after request-side middleware; the native path can observe the returned response at P3/P4. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: The target service URL is an egress destination; review it separately from middleware selection. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects the upstream service after router middleware completes. Compatibility-only host/service setup outside the selected native core path.
description: Selects the upstream service after router middleware completes. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-services"></a>
## `compatibility.forwardauth-dynamic.http.services`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.services` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.services` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.services` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.services` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik dynamic service registry mapping
allowed_values: named service mappings; selected key is app
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: The native middleware can receive the app response at P3/P4 after this service returns it; compatibility forwardAuth cannot. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Services define request destinations after middleware; review their endpoint URLs and credentials. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups upstream service definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.
description: Groups upstream service definitions referenced by routers. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-services-app"></a>
## `compatibility.forwardauth-dynamic.http.services.app`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.services.app` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.services.app` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik named service mapping
allowed_values: loadBalancer child mapping
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Upstream service stage after request middleware; native response callbacks can observe returned headers/body at P3/P4. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: This mapping is an upstream routing target; do not confuse it with the ModSecurity engine service. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Binds the router's app service name to its load balancer. Compatibility-only host/service setup outside the selected native core path.
description: Binds the router's app service name to its load balancer. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-services-app-loadbalancer"></a>
## `compatibility.forwardauth-dynamic.http.services.app.loadBalancer`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app.loadBalancer: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik LoadBalancer service mapping
allowed_values: servers child list
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: After request middleware, the selected server response is available to native P3/P4 callbacks; not to compatibility forwardAuth. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Each server URL is a traffic destination; limit it to the intended upstream. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups the upstream server endpoints for the app service. Compatibility-only host/service setup outside the selected native core path.
description: Groups the upstream server endpoints for the app service. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers"></a>
## `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Liste oder -Zuordnung | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: repeated Traefik load-balancer server mapping
allowed_values: one or more server URL mappings; selected example has one server
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: Native response lifecycle P3/P4 begins only after the selected server responds; compatibility forwardAuth remains request-only. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Adding a server adds an upstream destination; review network scope and transport security. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Defines the endpoint candidates for the app load balancer. Compatibility-only host/service setup outside the selected native core path.
description: Defines the endpoint candidates for the app load balancer. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-dynamic-http-services-app-loadbalancer-servers-url"></a>
## `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Syntax

```text
compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` die Upstream- oder Service-Verbindung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-dynamic.http.services.app.loadBalancer.servers[].url` konfiguriert die Upstream- oder Service-Verbindung. Sie wählt die Zielinstanz, den Transport oder das Zeitlimit für einen Upstream- beziehungsweise Prozessorservice.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"http://127.0.0.1:8081"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

Upstream-Adressen, Zeitlimits und Service-Ziele sind sicherheitsrelevant und müssen auf vertrauenswürdige lokale oder freigegebene Ziele begrenzt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik upstream server URL string
allowed_values: absolute backend URL; selected value is http://127.0.0.1:8081
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "http://127.0.0.1:8081".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-dynamic)
phase_relevance: The returned upstream response is the native middleware's P3/P4 source; forwardAuth compatibility has no later response visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Loopback keeps the example local; remote URLs require explicit TLS, identity, and egress controls. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Targets the application server that receives requests after router middleware. Compatibility-only host/service setup outside the selected native core path.
description: Targets the application server that receives requests after router middleware. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-accesslog"></a>
## `compatibility.forwardauth-static.accessLog`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.accessLog` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Syntax

```text
compatibility.forwardauth-static.accessLog: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.accessLog` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.accessLog` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.accessLog` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.accessLog` die Protokollierung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.accessLog` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `{}`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik access-log configuration mapping
allowed_values: empty mapping or documented access-log fields; selected value is {}
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures {}.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Host observability only; it does not substitute for transaction P1–P4 processing or engine audit logging. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Access logs can contain request metadata; configure safe storage, rotation, and privacy controls for deployment. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Enables/configures the Traefik access-log surface in the selected static example. Compatibility-only host/service setup outside the selected native core path.
description: Enables/configures the Traefik access-log surface in the selected static example. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-entrypoints"></a>
## `compatibility.forwardauth-static.entryPoints`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.forwardauth-static.entryPoints: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.entryPoints` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.entryPoints` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.entryPoints` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.entryPoints` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.entryPoints` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik static entry-point mapping
allowed_values: named entry-point mappings; selected key is web
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Static listener bootstrap; its named entry point selects which requests can reach the router/middleware lifecycle. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Entry-point addresses define the pre-policy network exposure of Traefik. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups named listener definitions used by dynamic routers. Compatibility-only host/service setup outside the selected native core path.
description: Groups named listener definitions used by dynamic routers. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-entrypoints-web"></a>
## `compatibility.forwardauth-static.entryPoints.web`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.entryPoints.web` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.forwardauth-static.entryPoints.web: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.entryPoints.web` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.entryPoints.web` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.entryPoints.web` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.entryPoints.web` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.entryPoints.web` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik EntryPoint mapping
allowed_values: address child field; selected entry point is web
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Static entry point for the router; the native middleware begins after request routing selects it. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Changing this listener changes client reachability before middleware enforcement. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Defines the named web listener that dynamic routers attach to. Compatibility-only host/service setup outside the selected native core path.
description: Defines the named web listener that dynamic routers attach to. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-entrypoints-web-address"></a>
## `compatibility.forwardauth-static.entryPoints.web.address`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.entryPoints.web.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Syntax

```text
compatibility.forwardauth-static.entryPoints.web.address: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.entryPoints.web.address` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Adressfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.entryPoints.web.address` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.entryPoints.web.address` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.entryPoints.web.address` die Listener-Bindung und Netzwerk-Erreichbarkeit konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.entryPoints.web.address` konfiguriert die Listener-Bindung und Netzwerk-Erreichbarkeit. Sie legt fest, an welcher Adresse oder welchem Port der Host Verbindungen annimmt oder einen lokalen Dienst erreicht.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `":8080"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Adresse und Port bestimmen die Erreichbarkeit vor der Regelverarbeitung; nur geprüfte private Bindungen verwenden.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik listener address string
allowed_values: Traefik entry-point address such as host:port or :port; selected value is :8080
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures ":8080".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Listener bootstrap before router selection and the attached native P1–P4 middleware path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: The selected :8080 form changes listener exposure according to host networking; use a private bind or explicit edge control as appropriate. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Binds the named web entry point used by the example router. Compatibility-only host/service setup outside the selected native core path.
description: Binds the named web entry point used by the example router. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-log"></a>
## `compatibility.forwardauth-static.log`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.log` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Syntax

```text
compatibility.forwardauth-static.log: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.log` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.log` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.log` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.log` die Protokollierung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.log` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik log configuration mapping
allowed_values: level child field
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Host observability only; no direct P1–P4 payload visibility change. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Logs can contain request and operational metadata; choose retention and access controls separately. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups Traefik process-log settings. Compatibility-only host/service setup outside the selected native core path.
description: Groups Traefik process-log settings. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-log-level"></a>
## `compatibility.forwardauth-static.log.level`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.log.level` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Syntax

```text
compatibility.forwardauth-static.log.level: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.log.level` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Steuerfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.log.level` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.log.level` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.log.level` die Protokollierung konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.log.level` konfiguriert die Protokollierung. Sie steuert, welche Host- oder Verwaltungsereignisse protokolliert werden.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `INFO`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Logs können sensible Betriebs- und Sicherheitsdaten enthalten; Zugriff, Rotation und Zielpfad absichern.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik log-level token
allowed_values: Traefik-supported level token; selected value is INFO
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures INFO.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Host observability only; it does not change native or compatibility lifecycle callbacks. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: Debug logging can expose more operational metadata; do not equate host logs with ModSecurity audit output. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Controls Traefik process-log verbosity. Compatibility-only host/service setup outside the selected native core path.
description: Controls Traefik process-log verbosity. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-providers"></a>
## `compatibility.forwardauth-static.providers`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.providers` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
compatibility.forwardauth-static.providers: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.providers` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.providers` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.providers` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.providers` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.providers` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik static provider registry mapping
allowed_values: file provider child mapping
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Static-to-dynamic handoff; it makes the router/middleware lifecycle available but does not process a transaction itself. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: A provider controls live routing configuration; protect its source file and directory. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Groups configuration providers that supply dynamic routers, middlewares, and services. Compatibility-only host/service setup outside the selected native core path.
description: Groups configuration providers that supply dynamic routers, middlewares, and services. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-providers-file"></a>
## `compatibility.forwardauth-static.providers.file`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.providers.file` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
compatibility.forwardauth-static.providers.file: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.providers.file` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.providers.file` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.providers.file` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.providers.file` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.providers.file` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik File Provider mapping
allowed_values: filename and watch child fields
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures the compatibility mapping shown in this file.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Loads the router/middleware configuration that exposes the native lifecycle path or compatibility request path. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: The dynamic file can alter routes and middleware; grant write access only to trusted operators. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Configures the on-disk dynamic configuration provider. Compatibility-only host/service setup outside the selected native core path.
description: Configures the on-disk dynamic configuration provider. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-providers-file-filename"></a>
## `compatibility.forwardauth-static.providers.file.filename`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.providers.file.filename` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
compatibility.forwardauth-static.providers.file.filename: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.providers.file.filename` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Kennungsfeld | Die zulässige Ausprägung von `compatibility.forwardauth-static.providers.file.filename` ergibt sich aus dem ausgewählten Traefik-Template und der Hostvalidierung. | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.providers.file.filename` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.providers.file.filename` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.providers.file.filename` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `"./traefik-dynamic.yaml"`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik File Provider path string
allowed_values: readable dynamic-configuration path; selected relative path is ./traefik-dynamic.yaml
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures "./traefik-dynamic.yaml".
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Supplies the routing configuration that attaches native P1–P4 middleware or compatibility P1 authorization. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: A relative path resolves from the host configuration context; deploy the matching file together and protect it from untrusted writes. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Selects the companion dynamic file containing routers, middleware, and upstream service definitions. Compatibility-only host/service setup outside the selected native core path.
description: Selects the companion dynamic file containing routers, middleware, and upstream service definitions. Compatibility-only host/service setup outside the selected native core path.
```

<a id="compatibility-forwardauth-static-providers-file-watch"></a>
## `compatibility.forwardauth-static.providers.file.watch`

### Kurzbeschreibung

Das YAML-Feld `compatibility.forwardauth-static.providers.file.watch` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Syntax

```text
compatibility.forwardauth-static.providers.file.watch: <value>
```

### Gültige Kontexte

- YAML-Pfad `compatibility.forwardauth-static.providers.file.watch` im ausgewählten Traefik-Template.

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| YAML-Konfigurationsfeld | true \| false | nein |

### Standardwert

Der Connector definiert für `compatibility.forwardauth-static.providers.file.watch` keinen unabhängigen Standardwert; das ausgewählte Template legt den gezeigten Wert ausdrücklich fest.

Quelle: `Ausgewähltes Traefik-Template und der im Quellanker referenzierte Validierungscode.`.

### Vererbung und Zusammenführung

Verhalten der Kompatibilitäts-Host-API; keine native Connector-Vererbung.

Zusammenführung: Verhalten der Kompatibilitäts-Host-API; kein Merge der ausgewählten nativen Konfiguration.

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Die P1–P4-Relevanz folgt daraus, wie `compatibility.forwardauth-static.providers.file.watch` das Laden der dynamischen Konfiguration konfiguriert.

Das YAML-Feld `compatibility.forwardauth-static.providers.file.watch` konfiguriert das Laden der dynamischen Konfiguration. Sie legt fest, aus welcher Datei oder welchem Provider dynamische Hostkonfiguration geladen wird.

### Validierung und Fehler

Als Traefik-forwardAuth-Kompatibilitätskonfiguration validieren.

### Beispiel

Ausgewählter Beispielwert: `true`.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-static.yaml](../../examples/traefik/compatibility-forwardauth/traefik-static.yaml).

### Sicherheit und Betrieb

Konfigurationsdateien und Verzeichnisse müssen vor unbefugtem Schreiben geschützt sein.

### Technische Quellmetadaten (unverändert)

Die folgenden Quellwerte bewahren die technische, englische Originalmetadatenangabe für diesen YAML-Pfad; Namen, konkrete Werte, Defaults und Protokollbegriffe bleiben dadurch vollständig nachvollziehbar.

```text
value_type: Traefik File Provider boolean
default: Absent from the selected native UDS middleware configuration. The repository declares no connector-owned compatibility default for this field; this compatibility template configures true.
default_source: compatibility template; selected/native classification
contexts: Compatibility YAML path only (forwardauth-static)
phase_relevance: Dynamic lifecycle configuration reload control; it does not itself change per-request P1–P4 visibility. Compatibility classification: do not infer selected native P3 response-header or P4 response-body coverage.
security_relevance: watch=true makes future file writes live configuration changes; selected native file uses false, compatibility example uses true. Compatibility-only: do not promote this setting as selected native full-lifecycle configuration.
runtime_effect: Controls whether Traefik watches the dynamic file for reloads after initial load. Compatibility-only host/service setup outside the selected native core path.
description: Controls whether Traefik watches the dynamic file for reloads after initial load. Compatibility-only host/service setup outside the selected native core path.
```

<a id="forwardauth"></a>
## `forwardAuth`

### Kurzbeschreibung

forwardAuth-Middleware nur für die Kompatibilität.

### Syntax

```text
forwardAuth: { address: <url>, trustForwardHeader: <bool> }
```

### Gültige Kontexte

- dynamische Kompatibilitäts-Middleware

### Werte

| Typ | Zulässige Werte | Erforderlich |
| --- | --- | --- |
| Traefik-Kompatibilitäts-Middleware | forwardAuth-Felder im Kompatibilitätsbeispiel | nein |

### Standardwert

nicht Teil des ausgewählten nativen Middleware-Pfads

Quelle: `Kompatibilitäts-Template`.

### Vererbung und Zusammenführung

nicht Teil der nativen Middleware

Zusammenführung: nicht Teil der nativen Middleware

### Phasen und Laufzeitwirkung

P1–P4-Relevanz: Kompatibilitätspfad für Request-Autorisierung; keine ausgewählte P3/P4-Konfiguration.

Leitet an den separaten Autorisierungsservice weiter.

### Validierung und Fehler

Separate Validierung der Traefik-Kompatibilitätskonfiguration.

### Beispiel

Ausgewählter Wert: Syntax oben und quellenbasierte Datei unten verwenden.

Quellenbasiertes Beispiel: [examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml](../../examples/traefik/compatibility-forwardauth/traefik-dynamic.yaml).

### Sicherheit und Betrieb

forwardAuth nicht als nativen UDS-Pfad zur Regelauswertung darstellen.
