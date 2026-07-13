# Connector-Beispiele

**Sprache:** [English](README.md) | Deutsch

Dieses Verzeichnis enthält kleine, repository-relative
Konfigurationsreferenzen für die sechs ausgewählten Connectorpfade. Sie sind
Lehrmaterial für Konfigurationen, keine Deployment-Manifeste und für sich
allein keine Evidence.

## Struktur und Geltungsbereich

| Verzeichnis | Integrationsmodus | Kernreferenz | Kompatibilitätsreferenz |
| --- | --- | --- | --- |
| [apache/](apache/README.de.md) | natives httpd-Modul | Native HTTP/1.1-P1--P4-Safe-Konfiguration | keine |
| [nginx/](nginx/README.de.md) | natives NGINX-HTTP-Modul | Native HTTP/1.1-P1--P4-Safe-Konfiguration | keine |
| [haproxy/](haproxy/README.de.md) | nativer HTX-Filter | Native HTTP/1.1-P1--P4-Safe-Konfiguration | [SPOE/SPOP](haproxy/README.de.md#spoespop-kompatibilität) |
| [envoy/](envoy/README.de.md) | Envoy ext_proc | Gestreamte HTTP/1.1-P1--P4-Safe-Konfiguration | [ext_authz](envoy/README.de.md#ext_authz-kompatibilität) |
| [traefik/](traefik/README.de.md) | native Traefik-Middleware | Local-Plugin-/UDS-HTTP/1.1-P1--P4-Safe-Konfiguration | [forwardAuth](traefik/README.de.md#forwardauth-kompatibilität) |
| [lighttpd/](lighttpd/README.de.md) | gepatchtes natives lighttpd-Modul | HTTP/1.1-Identity-Entity-P1--P4-Safe-Referenz | [Sidecar-Proxy](lighttpd/README.de.md#sidecar-kompatibilität) |

Alle Pfade in der Tabelle sind repository-relativ: Sie werden vom Root dieses
Repositorys aus aufgelöst. Ein Hostpfad wie
/etc/modsecurity/no-crs-baseline.conf ist ein Installationsbeispiel, kein
Repositorypfad und kein Wert, der auf jedem Host unverändert übernommen werden
kann.

## P1--P4-Safe-Kern

P1 bedeutet Request-Header, P2 Request-Body, P3 Response-Header und P4
Response-Body. Die Safe-Beispiele wählen die dokumentierte Safe-Policy nach
dem Commit: Kommt eine P4-Entscheidung zu spät für eine saubere
Response-Änderung, wird sie als nicht-disruptives Ergebnis aufgezeichnet und
nicht als erfundener HTTP-Status dargestellt.

Die aktuellen Kernreferenzen sind auf HTTP/1.1 ausgerichtet. Sie bedeuten kein
vollständiges Connector-Response-Buffering. Eigenschaften wie First Byte vor
EOS und No Full Buffer gehören, soweit sie ausgeübt werden, zum jeweiligen
Host-Runner und seiner Evidence, nicht zu einem Versprechen einer statischen
Konfigurationsdatei.

Strict ist absichtlich eng begrenzt. Ein Strict-Verzeichnis gibt es nur, wenn
eine tatsächliche eingecheckte Konfigurationsform vorhanden ist. Es behauptet
nie, dass ein Statuswechsel nach dem Commit, ein Reset oder ein
Verbindungsabbruch beobachtet wurde. Lesen Sie vor dem Aktivieren die
connector-spezifische Einschränkung.

## Konfigurationsreferenzen

| Referenz | Geltungsbereich |
| --- | --- |
| [Common Runtime](common/common-connector-configuration.de.md) | Vollständige quellenbasierte `key=value`-Parseroberfläche. |
| [ModSecurity Engine](common/modsecurity-directives.de.md) | Engine-Direktiven, die tatsächlich in eingecheckten Beispielen verwendet werden. |
| [Regelbeispiele](common/rule-examples.de.md) | Verhalten der Engine bei On, DetectionOnly und Off. |
| [Apache](apache/configuration-reference.de.md) | Apache-`command_rec`-Direktiven und Beispiel-Hostfelder. |
| [NGINX](nginx/configuration-reference.de.md) | NGINX-`ngx_command_t`-Direktiven und Beispiel-Hostfelder. |
| [HAProxy](haproxy/configuration-reference.de.md) | Native HTX-Optionen getrennt von SPOE/SPOP-Kompatibilität. |
| [Envoy](envoy/configuration-reference.de.md) | ext_proc-YAML-/Service-/CLI-Vertrag getrennt von ext_authz. |
| [Traefik](traefik/configuration-reference.de.md) | Native Middleware-/UDS-Konfiguration getrennt von forwardAuth. |
| [lighttpd](lighttpd/configuration-reference.de.md) | Native Plugin-Schlüssel und Common Runtime getrennt vom Sidecar-Proxy. |

## Regeln und erwartete Ergebnisse

Jedes Connector-Parent-README enthält seine No-CRS-Regelquelle und seine
P1--P4-Safe-Absicht. Die rules-Verzeichnisse behalten die eingecheckten
Profildateien, ohne eine veränderliche Framework-Datei in diese Beispiele zu
kopieren. Die Safe-Absicht bleibt Konfigurationsanleitung und kein
Testergebnis.

Die No-CRS-Regel-IDs 1100001, 1100101, 1100201 und 1100301 stehen jeweils für
P1, P2, P3 und P4. Es sind IDs des Repository-Testprofils, keine
OWASP-Core-Rule-Set-IDs.

## Anzupassende Werte

| Wertform | Bedeutung | Beispiel | Sicherheitshinweis |
| --- | --- | --- | --- |
| Host-Konfigurationspfad | Datei des installierten Hosts | /etc/nginx/nginx.conf | Distributionsabhängig; vorhandene Hostdateien nicht blind überschreiben. |
| Rules-Dateipfad | Lesbare ModSecurity-Regeldatei | /etc/modsecurity/no-crs-baseline.conf | Ein geprüftes Ruleset verwenden. Regeln können Traffic blockieren. |
| Listener- oder Upstream-Adresse | Host und TCP-Port für eine lokale Testroute | 127.0.0.1:8080 | Für lokale Tests Loopback binden, sofern keine Netzfreigabe beabsichtigt ist. |
| Log- oder Eventpfad | Beschreibbares Host-/Runtime-Ziel | /var/log/modsecurity/connector.jsonl | Logs können Request-Metadaten enthalten; schützen und rotieren. |
| Privater UDS-Pfad | Absoluter Unix-Domain-Socket-Pfad | /run/traefik-msconnector/engine.sock | In einem Verzeichnis ablegen, das Unberechtigte nicht lesen oder schreiben können. |

Kein Beispiel enthält Credentials, API-Keys, Cookies, Authorization-Header,
TLS-Private-Keys oder andere Geheimnisse. Solche Werte über den sicheren
Konfigurationsmechanismus des Hosts bereitstellen; nicht committen und nicht in
Evidence schreiben.

## Validierung

Vor dem Laden einer Referenz die dokumentierten Hostpfade, den Rules-Dateipfad,
Adressen und Logziele für die Zielmaschine ersetzen. Danach den nativen
Konfigurationscheck des Hosts verwenden und dessen Error-Log prüfen. Das
Connector-README nennt die genaue Referenz und die zu validierende Grenze. Ein
erfolgreicher Syntaxcheck beweist nur, dass der Host die Konfiguration
akzeptiert; er beweist weder P1--P4-Verhalten noch Produktionsreife,
CRS-Abdeckung oder Strict-Late-Intervention.
