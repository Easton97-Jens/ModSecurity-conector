# Traefik-Beispiele für die native Middleware

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: repository-eigenes Traefik-Local-Plugin plus persistenter
lokaler Unix-Domain-Socket-Engine-Service. Die
[statische Minimalreferenz](minimal/traefik-static.yaml) registriert Local
Plugin und File Provider; die [dynamische Safe-Referenz](safe/traefik-dynamic.yaml)
wählt engineMode uds. Die passende
[Engine-Service-Konfiguration](safe/traefik-engine-service.conf) wählt
gestreamte Bodies und phase4_mode safe.

Dies ist die native HTTP/1.1-P1--P4-Safe-Referenz. P1, P2, P3 und P4 sind
Request-Header, Request-Body, Response-Header und Response-Body. Safe behauptet
weder einen späten Statuswechsel noch einen Strict-Verbindungsabbruch. Die
Konfiguration verspricht keinen vollständigen Response-Buffer und keine
Regelbewertung pro Chunk. Es gibt keine Strict-Datei.

[forwardAuth-Kompatibilitätsdateien](compatibility-forwardauth/README.de.md)
sind nur Request-Authorization und dürfen nicht als P3/P4-Kernpfad gelten.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/traefik-static.yaml](minimal/traefik-static.yaml) | Statische Host-Konfiguration | Local-Plugin-Registrierung, Web-EntryPoint und File Provider. |
| [safe/traefik-dynamic.yaml](safe/traefik-dynamic.yaml) | Dynamische Host-Konfiguration | Router, Middleware, UDS-Engine-Auswahl und lokaler Upstream. |
| [safe/traefik-engine-service.conf](safe/traefik-engine-service.conf) | Engine-Konfiguration | Regeln, Limits, gestreamte Body-Modi und Safe-Policy. |
| [rules/README.de.md](rules/README.de.md) | Dokumentation | No-CRS-Quelle und Phasen-IDs. |
| [expected/p1-p4-safe.de.md](expected/p1-p4-safe.de.md) | Dokumentation | Konfigurationsabsicht, keine Evidence. |
| [compatibility-forwardauth/](compatibility-forwardauth/README.de.md) | Kompatibilität | Frühere Request-only-Route. |

Alle obigen Pfade sind ab examples/traefik repository-relativ. Pfade in den
Dateien sind entweder Hostinstallationspfade oder lokale Testwerte und müssen
angepasst werden.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| moduleName | Go-Modulkennung des Local Plugins | Pflicht; expliziter statischer Wert; Traefik-Local-Plugin-Scope | github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware. Passenden Source im installierten Traefik-Local-Plugin-Workspace bereitstellen. |
| entryPoints.web.address | Listener-Adressstring | Pflicht; expliziter statischer Wert; Traefik-Static-Scope | :8080. Öffentlicher Bind verändert die Exponierung. |
| providers.file.filename | Dynamischer Konfigurationsdateipfad relativ zum Traefik-Arbeitsverzeichnis | Pflicht; expliziter statischer Wert; File-Provider-Scope | ./traefik-dynamic.yaml. Safe-Dynamic-Datei an diesen aufgelösten Ort kopieren. |
| Router-Regel und Service-URL | Request-Matcher und Upstream-URL | Pflicht; dynamische Konfiguration; Router/Service-Scope | PathPrefix für alle Pfade und http://127.0.0.1:8081. Routen begrenzen und Endpunkt für Deployment ersetzen. |
| maxHeaderCount, maxHeaderBytes, maxRequestChunkBytes, maxResponseChunkBytes | Positive Plugin-Limits | Pflicht; dynamische Konfiguration; Middleware-Scope | 128, 65536, 32768, 32768. Kleinere Werte lehnen mehr Input ab; Grenzen nicht entfernen. |
| transactionIDHeader | HTTP-Korrelationsheadername | Pflicht; dynamische Konfiguration; Middleware-Scope | X-Request-Id. Metadaten, kein Geheimnis. |
| engineMode | Native Engine-Modus: passthrough oder uds | Für Safe-Referenz Pflicht; dynamische Konfiguration; Middleware-Scope | uds. Benötigt einen gültigen privaten engineSocketPath. |
| engineSocketPath | Absoluter privater Unix-Socket-Pfad | Bei engineMode uds Pflicht; dynamische Konfiguration; Middleware-Scope | /run/traefik-msconnector/engine.sock. Parent-Verzeichnis muss zugriffsgeschützt sein und dem vertrauenswürdigen Service gehören. |
| rules_file | Installierter geprüfter Rules-Dateipfad | Pflicht; Engine-Konfiguration; Engine-Scope | /etc/modsecurity/no-crs-baseline.conf. Regeln können Traffic blockieren. |
| request_body_mode und response_body_mode | Engine-Body-Modi | Für Safe-Referenz Pflicht; Engine-Konfiguration; Engine-Scope | streaming. Beweist weder vollständiges Buffering noch späte Client-Action. |
| phase4_mode | Name der Late-P4-Policy | Für Safe-Referenz Pflicht; Engine-Konfiguration; Engine-Scope | safe. Erlaubt weder erfundenen Status noch Strict-Abbruch. |

## Validierung

Statische und dynamische Dateien an die vom File Provider gewählten Hostorte
kopieren, alle Pfade und Endpunkte anpassen und die installierte statische
Konfiguration validieren. /etc/traefik/traefik.yaml ist ein
Installationsbeispiel:

~~~sh
traefik check --configFile=/etc/traefik/traefik.yaml
~~~

Zusätzlich prüfen, dass der Engine-Socket privat ist, der Engine-Service die
Rules-Datei lesen kann und Traefik das Local Plugin lädt. Ein
Konfigurationscheck beweist weder P1--P4-Verhalten noch Safe-Host-Actions,
Strict-Verhalten, Produktionsreife oder CRS-Abdeckung.

## Verwandtes Material

- [Traefik-Connector-Quellcode und native Service-Grenze](../../connectors/traefik/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
