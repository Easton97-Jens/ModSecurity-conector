# Architektur – Connector-Vorlage

**Sprache:** [English](architecture.md) | Deutsch

## Ziel

Dieses Dokument ist ein Planungsrahmen für einen zukünftigen adaptereigenen Connector. Es ist
kein Laufzeitcode und beweist keine Serverintegration.

## Erforderlicher Architekturnachweis

- [ ] Serverlebenszyklus und Hook-Modell dokumentiert.
- [ ] Anforderungsheaderpfad dokumentiert.
- [ ] Anforderungstextpfad dokumentiert.
- [ ] Antwort-Header-Pfad dokumentiert.
- [ ] Antworttextpfad dokumentiert oder nicht unterstütztes Verhalten dokumentiert mit
      Beweise.
- [ ] Interventionskartierung dokumentiert.
- [ ] Protokollierungs- und Prüfpfad dokumentiert.
- [ ] Start-/Neuladeverhalten dokumentiert.
- [ ] Thread-/Prozess-/Worker-Modell dokumentiert.

## Adaptereigenes Prinzip

- Connector-spezifischer Code befindet sich unter `connectors/<name>/`.
- Auf gemeinsam genutzte Connector-neutrale Helfer kann nur verwiesen werden, wenn ihre Pfade und
  Verträge finden Sie im Repository.
- Das Laufzeitverhalten von Apache/NGINX darf nicht als generisches Verhalten für a behandelt werden
  neuer Server.

## Serverspezifische Bereiche

Jeder Connector muss diese Bereiche separat nachweisen:

- Hook-Registrierung / Filterkette / Middleware-Integration
- Integration des Anforderungs-/Antwortlebenszyklus
- Körperhandhabung, einschließlich Pufferung, Streaming und Grenzwerte
- Konfigurationsparser und Zusammenführungssemantik
- Zuordnung von ModSecurity-Eingriffen zu Serveraktionen
- Prozess-, Worker- und Speichermodell

## Wiederverwendbare Beweise

Zu den wiederverwendbaren Planungsnachweisen können gehören:

- Gemeinsame Status-, Ursprungs-, Interventions- und Fähigkeitsdatenformen
- Framework-Testpfade
- Dokumentierte Ziele setzen
- bewährte Include-/Bibliotheksverträge

Wiederverwendbare Planungsnachweise sind kein Laufzeitnachweis.

## Werberelevanz

Die Architekturdokumentation kann `scaffolded` oder `adapter-owned` unterstützen. Es
kann `runtime-smoke-verified`, `crs-verified` oder mehr nicht unterstützen
`partial` ohne ausgeführten Laufzeitnachweis.

## Was nicht beansprucht werden darf

- Beanspruchen Sie nicht die Übertragung von Apache/NGINX-Laufzeitpfaden auf einen neuen Connector.
- Behaupten Sie nicht, dass RESPONSE_BODY vorhanden ist, da sonst automatisch Phase-4-Unterstützung vorhanden ist.
- Beanspruchen Sie keine Produktionsbereitschaft ohne Laufzeitnachweise.
- Erfinden Sie keine Server-APIs, Hook-Namen oder Lebenszyklusverhalten.
