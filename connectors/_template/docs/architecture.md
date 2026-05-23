# Architektur – Connector Template

## Ziel

Dieses Dokument beschreibt eine **adapter-owned** Ausgangsarchitektur für neue
Connectoren. Es ist ein Planungsrahmen und **keine** Runtime-Implementierung.

## Adapter-owned Grundprinzip

- Connector-spezifischer Code bleibt unter `connectors/<name>/`.
- Gemeinsame, connector-neutrale Metadaten dürfen genutzt werden, soweit im
  Repository belegt.
- Runtime-Verhalten eines Zielservers darf nicht als generisch angenommen
  werden.

## Was server-spezifisch bleiben muss

Die folgenden Bereiche sind pro Server zu entwerfen und zu beweisen (noch zu
prüfen):

- Hook-Registrierung / Filterkette / Middleware-Einbindung
- Request-/Response-Lifecycle-Integration
- Body-Handling (Buffering, Streaming, Limits)
- Konfigurationsparser und Konfig-Merge-Semantik
- Interventions-Mapping in servereigene Aktionen
- Prozess-/Worker-/Speichermodell des Zielservers

## Was potenziell wiederverwendbar ist (belegt, aber begrenzt)

Aus dem gemeinsamen Bereich können nur connector-neutrale Formen übernommen
werden (belegt), z. B.:

- Status-/Origin-/Intervention-/Capabilities-Datenformen
- Direktiven-/Options-Metadaten, sofern semantisch passend

Wichtig: Daraus folgt **keine** belegte Runtime-Abstraktion für neue Server.

## Nicht zu behaupten

- Keine Aussage, dass Apache-/NGINX-Runtime-Pfade 1:1 übertragbar sind.
- Keine Aussage, dass RESPONSE_BODY/Phase-4-Verhalten automatisch verfügbar ist.
- Keine Aussage über Produktionsreife ohne separate Runtime-Evidenz.
