# Zukünftige Anschlüsse

**Sprache:** [English](future-connectors.md) | Deutsch

In diesem Stabilisierungsschritt wird kein neuer Connector implementiert. Jede Zukunft
Der Connector muss zunächst einen realen Harness bereitstellen, der Apache und entspricht
NGINX.

## HAProxy

- Upstream: https://github.com/haproxy/haproxy
- Erwartetes Modell: SPOE oder nativer Erweiterungspfad müssen Metadaten manuell anfordern und
Körperdaten in der richtigen Phase an libmodsecurity übergeben.
- Schwierige Bereiche: Pufferung, Antwortinspektion, Überwachungsprotokollbesitz und
Zuordnung von ModSecurity-Eingriffen zu HAProxy-Aktionen.
– Wahrscheinlich portable erste Fälle: `REQUEST_HEADERS`, `ARGS`, einfacher Requeststext.
– Wahrscheinlich Connector-spezifische Fälle: Streaming, Backend-Antwortverarbeitung, SPOE
Fehlerpfade.

## Envoyr

- Upstream: https://github.com/envoyproxy/envoy
- Erwartetes Modell: HTTP-Filter oder externer Verarbeitungsablauf.
- Schwierige Bereiche: asynchrone Körperpufferung, Filterreihenfolge, Header-Mutation und
Zuordnung von Interventionen zu Envoy-Antworten.
– Wahrscheinlich portable erste Fälle: Header, Abfrageargumente, roher JSON-Body.
– Wahrscheinlich connectorspezifische Fälle: HTTP/2, gRPC, Streaming, Filterkette
Konfiguration.

## Lighttpd

- Upstream: https://github.com/lighttpd/lighttpd1.4
– Erwartetes Modell: native Plugin-Hook-Integration oder dokumentierte Skriptfähigkeit
Modulpfad.
- Schwierige Bereiche: Verfügbarkeit des Requestskörpers, Antwortfilter-Hooks und Stabilität
Modul-Build-Verpackung.
– Wahrscheinlich portable erste Fälle: Header und Abfrageargumente.
– Wahrscheinlich Connector-spezifische Fälle: Plugin-Lebenszyklus und Serverkonfigurationsanalyse.

## Traefik

- Upstream: https://github.com/traefik/traefik
- Erwartetes Modell: Der plugin/middleware-Pfad muss vor jedem Connector nachgewiesen werden
Ansprüche.
- Schwierige Bereiche: Plugin-Sandbox-Einschränkungen, Requestskörperpufferung, Antwort
Mutation und das Verteilen von libmodsecurity.
- Wahrscheinlich portierbare erste Fälle: Header und Abfrageargumente, sofern die Middleware dies kann
Rufen Sie libmodsecurity sicher auf.
– Wahrscheinlich Connector-spezifische Fälle: dynamisches Neuladen der Konfiguration und anbieterspezifisch
Middleware-Verkabelung.

## Gemeinsame Request

Jeder Connector muss eine JSON-Zusammenfassung mit „connector_path“ erzeugen:
„real-world“`, `validation_mode: „real-world-connector-path“`, stabil
`pass/fail/blocked`-Semantik und keine generierten Artefakte außerhalb von `BUILD_ROOT`.
