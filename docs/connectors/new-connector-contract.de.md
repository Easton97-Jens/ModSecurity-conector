**Sprache:** [English](new-connector-contract.md) | Deutsch

# Vertrag für neue Connectoren

Ein zukünftiger Connector soll vollständige Metadaten, Capabilities,
Konfigurationsmapping, Request/Response-Mapping, Decision-Mapping,
Event-/Log-Mapping und Artefaktlayout deklarieren, bevor Unterstützung behauptet
wird.

Dieses Dokument ist nur ein Vertragsleitfaden. Es migriert keinen bestehenden
Connector und behauptet kein Laufzeitverhalten, keine Capability-Unterstützung
und keine Produktionsreife.

## Erwartungen an das Common-Paket

Zukünftige Connector-Adoption soll Host-Requests/-Responses über die Common
Request-/Response-Helfer abbilden, Manifeste und Origin-Governance offenlegen,
die Build-Contract-Target-Begriffe verwenden, wenn sie übernommen werden, und
Runtime-Reports wahrheitsgemäß halten. Kein bestehender Connector wird durch
diese reine Dokumentationsaktualisierung übernommen.

## Directive-, Mapper- und CRS-Setup-Contracts

Neue Connectoren sollten die globalen Common-Contracts nutzen, bevor sie Runtime-Claims formulieren:

- Host-Direktiven aus dem connector-neutralen `directive_adapter`-Modell registrieren; konkrete Server-Typen wie `ngx_command_t` und Apache `command_rec` bleiben im Connector.
- Request-Mapper von Host-Requests wie `ngx_http_request_t`, Apache `request_rec` oder entsprechenden APIs nach `msconnector_request` implementieren und das Ergebnis gegen `request_mapper_contract` validieren.
- Response-Mapper nach `msconnector_response` implementieren und gegen `response_mapper_contract` validieren; dieser Contract loggt keine Body-Payloads.
- CRS-/Ruleset-Setup mit der `crs`-Konfiguration nur als Setup-Konvention beschreiben. Eine gültige CRS-Konfiguration ist kein CRS-PASS-Claim.

Dieser Leitfaden verlangt und behauptet keine Adoption durch bestehende NGINX-, Apache-, HAProxy-, Envoy-, lighttpd- oder Traefik-Runtimes. Host-spezifische Request-Chains, APR-Pools, Bucket Brigades, Server-Hooks, Filter und Body-Puffer bleiben Connector-Eigentum.

## Hinweis zum bestehenden Apache-Connector

Der Apache-Connector ist ein Beispiel für beginnende Adapter-Adoption: Common
besitzt semantische Konfiguration, Direktiven, Mapper-Contracts und Events,
während Apache-eigener Code Apache-API-Zugriffe sowie Filter-/Hook-Mechanik
behält. Dieser Hinweis ist keine Aussage zu Produktionsreife, CRS, Full-Matrix
oder Runtime-Verifikation.
