# Traefik-Quelle

**Sprache:** [English](README.md) | Deutsch

Status: minimal_runtime_smoke (nur ForwardAuth-Anfragepfad)
Laufzeitstatus: Verhalten des breiteren Connectors nicht überprüft

Dieses Verzeichnis enthält:

- `traefik_build_starter.c`: Metadaten-Smoke-Quelle zur Kompilierungszeit.
- `traefik_decision_service.h`: Starter-Deklarationen für lokale Entscheidungsdienste.
- `traefik_decision_service.c`: Lokale speicherinterne Entscheidungslogik zum Zulassen/Blockieren.
- `traefik_decision_service_main.c`: CLI/Selbsttest-Einstiegspunkt.
- `traefik_modsecurity_mapper.c`: Thin C17-Funktionen, die an den Common delegieren
  generische Request/Response-Mapper-Verträge.
- `traefik_forwardauth_service_main.c`: Connector-Hostprofil und Einstiegspunkt
  für die Laufzeit des gemeinsam genutzten HTTP-Autorisierungsdiensts.

Der ausgewählte Kompatibilitätsadapterpfad ist ein externer `forwardAuth`-Dienst.
Das separate `../native_middleware/` Go-Modul wird nur von ausgewählt
nicht beworbenes lokales Plugin-Host-Probe mit vollem Lebenszyklus. Es verfügt über eine Durchreiche
Motornaht, keine CGO-Brücke oder Regelbewertungsanspruch. Upstream-Antwort
Die Inspektion wird vom ausgewählten Anforderungsphasenprotokoll ausdrücklich nicht unterstützt.
obwohl der Antwort-Mapper für die allgemeine Vertragsprüfung verknüpft ist.

Die Produktionsquelle darf nur mit Repository-gestütztem Ursprung, Lizenz usw. hinzugefügt werden.
Quellzuordnung, Metadaten, Build- und Validierungsnachweise. Schließen Sie nicht auf Traefik
Adapterverhalten von anderen Anschlüssen.
