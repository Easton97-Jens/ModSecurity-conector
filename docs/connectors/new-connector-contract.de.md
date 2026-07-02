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
