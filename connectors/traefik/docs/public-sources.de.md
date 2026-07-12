# Öffentliche Traefik-Quellen

**Sprache:** [English](public-sources.md) | Deutsch

Status: Nur Referenz
Laufzeitstatus: nicht überprüft

Die folgenden Links wurden zuvor als öffentliches Traefik-Referenzmaterial aufgezeichnet
für die Kandidatenintegrationsforschung. Sie sind keine importierte Quelle, Build
Beweise oder Laufzeitbeweise und beweisen nicht, dass es sich um einen ModSecurity-Connector handelt
hier umgesetzt.

- https://doc.traefik.io/traefik/extend/extend-traefik/
- https://doc.traefik.io/traefik/master/reference/install-configuration/experimental/plugins/
- https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/forwardauth/
- https://plugins.traefik.io/create

Der Standardkompatibilitätspfad bleibt der repoeigene lokale Entscheidungsdienst
Starter plus Metadaten-Build-Starter. Das separat gehaltene Repo
Das `native_middleware/`-Paket folgt dem dokumentierten Go-Middleware-Einstiegspunkt
Form und enthält einen lokalen `.traefik.yml`. Die Host-Probe-Stufen für den gesamten Lebenszyklus
Es wählt in einem angehefteten lokalen Traefik-Plugin-Arbeitsbereich ein privates persistentes UDS aus
Common/libmodsecurity-Engine und zeichnet nur gezielte Metadaten auf, P1--P4-sicher
Ergebnisse des Gastgebers. Dieser Beweis fördert keine Regelfähigkeit.
