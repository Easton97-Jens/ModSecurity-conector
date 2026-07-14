# Gemeinsames Design

**Sprache:** [English](design.md) | Deutsch

Status: aktuelle Grenzreferenz

## Verbindlichkeit und Geltungsbereich

Diese Notiz fasst die aktuelle Ownership-Grenze von `common/` zusammen. Die
verbindliche Produktquelle ist das
[Repository-Konzept](../../docs/repository-concept.de.md), und die aktuelle
Architekturquelle ist die [Architektur](../../docs/architecture.de.md).
Connector-Guides definieren ihre hostspezifischen Build-, Konfigurations-,
Lifecycle-, Kompatibilitäts- und Evidence-Details. Diese Notiz begründet keinen
Runtime-, Production-Readiness- oder Capability-Promotion-Claim.

## Host-neutraler Common-Vertrag

`common/` bleibt host-neutral. Es stellt C-first-Contracts und
Implementierungen für neutrale Lifecycle-Unterstützung, Konfiguration, Limits,
Decisions, Events, Logging/Redaction und Engine-nahe Helfer bereit. Es darf
keine Host-SDK-Typen, Host-Hooks, Host-Filter, Hostobjekt-Lebensdauern,
Host-Konfigurationsregistrierung oder client-sichtbare Hostaktionen einbinden
oder von ihnen abhängen.

Hostspezifisches Mapping, Callback-Registrierung, hosteigene Allokation,
Commit-Semantik, Interventionsmaterialisierung, Build-Glue und Installation
bleiben in `connectors/<name>/`. Ein Common-Type oder -Helfer ist kein
Nachweis, dass jeder Host eine Lifecycle-Phase oder eine Intervention
implementiert.

## Ownership-, Daten- und Interventionsgrenze

Der Hostadapter besitzt Requests, Responses, Buffer und Hostobjekte. Common
akzeptiert nur validierte begrenzte Ansichten oder Kopien für den jeweiligen
Aufruf und darf über Callbacks hinweg keinen connector-eigenen vollständigen
Response-Body behalten. Es besitzt nur seine dokumentierte neutrale Runtime,
Rules, kopierte Konfiguration und Transaction-Metadaten; Connectoren behalten
Host-Cleanup und Exactly-once-Lifecycle-Verantwortung.

Common kann eine angeforderte Decision und payload-sichere Metadaten
repräsentieren. Der Hostadapter bestimmt, ob und wie diese Decision zu einer
tatsächlichen client-sichtbaren Aktion wird, insbesondere nach Response-Commit.

## Ausgewählte Produktrouten

Die folgenden ausgewählten Produktrouten bezeichnen nur Ownership. Ein
Routenname, Source-Contract, Build oder Dokumentationscheck ist keine
Runtime-Evidence.

| Connector | Ausgewählte Produktroute | Kompatibilitätsmaterial |
| --- | --- | --- |
| Apache | `native-httpd-module` | Keine ausgewählte Kompatibilitätsroute |
| NGINX | `native-nginx-http-module` | Keine ausgewählte Kompatibilitätsroute |
| HAProxy | `native-htx-filter` | `spoe-spop-agent` ist `compatibility_only` |
| Envoy | `ext_proc` | `ext_authz` ist `compatibility_only` |
| Traefik | `native-traefik-middleware` | `forwardAuth` ist `compatibility_only` |
| lighttpd | `patched-native-lighttpd` | `sidecar_proxy` ist `compatibility_only` |

## Test- und Evidence-Grenze

Das Parent-Repository besitzt Produkt-Contracts, Connector-Seams, Build-Wiring
und hostspezifische Artefaktproduktion.
`modules/ModSecurity-test-Framework/` besitzt wiederverwendbare Cases, Runner,
Normalizer, Schemas und Report-Generierung. Ein zweiter wiederverwendbarer
Case-Katalog oder Normalizer gehört nicht nach `common/`.

[Tests und Nachweise](../../docs/testing-and-evidence.de.md) definiert, was
jede Testebene belegen kann. Source-, Dokumentations- und Contract-Checks
schützen nur ihre angegebene Grenze; sie ersetzen weder ausgewählten
Hostverkehr noch kanonische run-scoped Evidence.

## Historisches Material

Frühere Entwurfs- und Open-Connector-Smoke-Materialien bleiben über
die Git-Historie verfügbar. Sie sind kein aktueller Routen-, Build-, Runtime-
oder Evidence-Guide. Einen Legacy-Pfad nur beibehalten, wenn seine
Connector-Dokumentation ihn `compatibility_only` nennt und von der ausgewählten
Route trennt.

## Verwandte Referenzen

- [Repository-Konzept](../../docs/repository-concept.de.md)
- [Architektur](../../docs/architecture.de.md)
- [Tests und Nachweise](../../docs/testing-and-evidence.de.md)
- [Common-Quellbaum-Guide](../README.de.md)
