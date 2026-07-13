# Traefik-Beispiele für die native Middleware

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: repository-eigenes Traefik-Local-Plugin plus persistenter
lokaler Unix-Domain-Socket-Engine-Service. Die
[statische Minimalreferenz](minimal/traefik-static.yaml) registriert Local
Plugin und File Provider. Die benachbarten minimalen dynamischen und
Engine-Service-Dateien wählen dieselbe UDS-Form mit `phase4_mode=minimal`; die
[dynamische Safe-Referenz](safe/traefik-dynamic.yaml)
wählt engineMode uds. Die passende
[Engine-Service-Konfiguration](safe/traefik-engine-service.conf) wählt
gestreamte Bodies und phase4_mode safe.

Dies ist die native HTTP/1.1-P1--P4-Safe-Referenz. P1, P2, P3 und P4 sind
Request-Header, Request-Body, Response-Header und Response-Body. Safe behauptet
weder einen späten Statuswechsel noch einen Strict-Verbindungsabbruch. Die
Konfiguration verspricht keinen vollständigen Response-Buffer und keine
Regelbewertung pro Chunk. Die Strict-Profilgrenze dokumentiert die optionale
Grenze, statt einen ausführbaren Host-Abbruch zu behaupten.

[forwardAuth-Kompatibilitätsdateien](#forwardauth-kompatibilität) sind nur
Request-Authorization und dürfen nicht als P3/P4-Kernpfad gelten.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/traefik-static.yaml](minimal/traefik-static.yaml) | Statische Host-Konfiguration | Local-Plugin-Registrierung, Web-EntryPoint und File Provider. |
| [minimal/traefik-dynamic.yaml](minimal/traefik-dynamic.yaml) | Dynamische Host-Konfiguration | Minimale UDS-Middleware-/Router-/Service-Form. |
| [minimal/traefik-engine-service.conf](minimal/traefik-engine-service.conf) | Engine-Konfiguration | Gestreamte Body-Modi mit minimaler Late-P4-Policy. |
| [safe/traefik-dynamic.yaml](safe/traefik-dynamic.yaml) | Dynamische Host-Konfiguration | Router, Middleware, UDS-Engine-Auswahl und lokaler Upstream. |
| [safe/traefik-engine-service.conf](safe/traefik-engine-service.conf) | Engine-Konfiguration | Regeln, Limits, gestreamte Body-Modi und Safe-Policy. |
| [detection-only/traefik-engine-service.conf](detection-only/traefik-engine-service.conf) | Engine-Konfiguration | DetectionOnly-Regeln mit ausgewählter UDS-Middleware; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/traefik-engine-service.conf](disabled/traefik-engine-service.conf) | Engine-Konfiguration | Runtime deaktiviert, ohne forwardAuth zu einem nativen Pfad zu machen; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | No-CRS-Quelle und Phasen-IDs. |
| [P1--P4-Safe-Absicht](#p1-p4-safe-absicht) | Dokumentation | Konfigurationsabsicht, keine Evidence. |
| [forwardAuth-Kompatibilität](#forwardauth-kompatibilität) | Kompatibilität | Frühere Request-only-Route. |

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

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md)
dokumentiert statische/dynamische YAML-Felder, native Plugin-Defaults, die
Common-Runtime-Datei und den getrennt markierten forwardAuth-Kompatibilitätsweg.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `engineMode: uds` | Host / Connector | Wählt den persistenten nativen UDS-Engine-Service. |
| `SecRuleEngine` | ModSecurity Engine | Wählt Enforcement, DetectionOnly oder Off in der Engine-Regeldatei. |
| `request_body_mode` | Common Runtime | Wählt die native Engine-P2-Body-Verarbeitung. |
| `response_body_mode` | Common Runtime | Wählt die native Engine-P4-Body-Verarbeitung. |
| `phase4_mode` | Common Runtime | Zeichnet die gewünschte Late-P4-Policy auf; Go-Middleware bleibt nach Commit log-only. |

`engineMode: passthrough` ist eine Source-only-Allow-Engine und kein
Rule-Enforcement. `SecRuleEngine Off` lässt die UDS-Route bestehen, deaktiviert
aber Engine-Regeln. forwardAuth ist ein getrennter Request-only-Kompatibilitätsweg.

## Profile

### DetectionOnly-Profil

`detection-only/traefik-engine-service.conf` wird mit der UDS-dynamischen
Middleware verwendet und wählt DetectionOnly-Regeln. DetectionOnly lädt und
bewertet Engine-Regeln und zeichnet Treffer auf, führt aber keine disruptiven
Engine-Aktionen aus.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/traefik-engine-service.conf` setzt `enabled=off`; forwardAuth wird
dadurch nicht zu einem nativen Pfad. Dies unterscheidet sich von
`SecRuleEngine Off`, das bei aktivem Hostconnector die Regelauswertung
innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Safe-Absicht

Die native Local-Plugin-Referenz verwendet engineMode uds und einen privaten
lokalen Engine-Socket. Ihre Service-Konfiguration wählt gestreamte Body-Modi
und phase4_mode safe. Ein P4-Ergebnis nach dem Commit soll Safe-Log-only
bleiben; es ist kein behaupteter Response-Wechsel oder Strict-
Verbindungsabbruch.

Die forwardAuth-Dateien sind Request-only-Kompatibilitätsmaterial. Sie dürfen
nicht zur Beschreibung von P3/P4-Abdeckung benutzt werden. Das
[Strict-Profilgrenze](#strict-profilgrenze) dokumentiert die optionale Grenze;
es ist kein Host-Abbruch-Anspruch.

## No-CRS-Regeln

Der persistente lokale UDS-Engine-Service benötigt eine installierte geprüfte
Regeldatei. Die Repositoryquelle für das No-CRS-Profil ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

## forwardAuth-Kompatibilität

Die bewahrten Dateien halten die frühere Request-Authorization-Konfiguration
fest. Sie sind vom nativen Local-Plugin-/UDS-Kern unter [safe/](safe/) getrennt.

### Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- |
| entryPoints.web.address | Listener-Adressstring | Pflicht; statische Datei; Traefik-Static-Scope | :8080. Ein öffentlicher Listener verändert die Exponierung. |
| providers.file.filename | Dynamischer Dateipfad relativ zum Traefik-Arbeitsverzeichnis | Pflicht; statische Datei; File-Provider-Scope | ./traefik-dynamic.yaml. Für diese Route beide Kompatibilitätsdateien zusammen kopieren. |
| Router-Regel und entryPoints | Request-Matcher und benannter Entry Point | Pflicht; dynamische Datei; Router-Scope | PathPrefix für alle Pfade und web. Für echtes Deployment begrenzen. |
| forwardAuth-Adresse | Authorization-Service-HTTP-URL | Pflicht; dynamische Datei; Middleware-Scope | http://127.0.0.1:9000/authorize. Keine Tokens oder Credentials einbetten. |
| trustForwardHeader | Boolesche Forwarded-Header-Policy | Pflicht; dynamische Datei; Middleware-Scope | false. Änderung verändert die Vertrauensgrenze und benötigt eine explizite Proxy-Header-Policy. |
| App-Service-URL | Upstream-HTTP-URL | Pflicht; dynamische Datei; Service-Scope | http://127.0.0.1:8081. Für Deployment ersetzen. |

Die [forwardAuth-Konfiguration](compatibility-forwardauth/traefik-dynamic.yaml)
läuft vor der Upstream-Response-Verarbeitung. Sie darf nicht als P3/P4-
Prüfung, natives Middleware-Verhalten, Safe-Late-Verhalten,
Strict-Verhalten, First-Byte-Evidence oder No-Full-Response-Buffer-Evidence
beschrieben werden.

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

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Common Runtime akzeptiert `phase4_mode=strict`, aber die native Go-Middleware
stuft disruptive P4-Entscheidungen nach Commit zu log-only herab. Strict ist
optional und es wird kein Abbruchprofil behauptet.

Das Safe-UDS-Setup beibehalten, statische/dynamische Konfiguration und den
Engine-Service validieren und neue Host-Evidenz verlangen, bevor ein strikter
Transportanspruch erhoben wird.

## Verwandtes Material

- [Traefik-Connector-Quellcode und native Service-Grenze](../../connectors/traefik/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
