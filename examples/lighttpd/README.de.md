# lighttpd-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: natives lighttpd-Modul namens mod_msconnector. Die
[Minimalreferenz](minimal/lighttpd.conf) ist für die Stock-Host-/Modulform und
lässt beide Body-Modi auf none. Die
[Safe-Referenz](safe/lighttpd-http1-identity.conf) und ihre passende
[Runtime-Datei](safe/msconnector-runtime.conf) benötigen den passenden
gepatchten lighttpd-1.4.84-Host und das passende Modul. Ihr Scope ist auf
geproxyte HTTP/1.1-Identity-Entity-Daten begrenzt.

Die Safe-Referenz konfiguriert die P1--P4-Form mit phase4_mode safe. P1 sind
Request-Header, P2 Request-Body, P3 Response-Header und P4 Response-Body. Sie
behauptet weder clientbeobachtetes P4-Verhalten noch vollständiges
Response-Buffering, HTTP/2, HTTP/3, Kompression, File-/Zero-Copy-Verarbeitung
oder Strict-Abbruch. Das [Strict-Verzeichnis](strict/README.de.md)
dokumentiert die optionale Grenze ohne implementierten Host-Abbruch.

Der bewahrte [Sidecar-Proxy](compatibility-sidecar/README.de.md) ist keine
native Modulkonfiguration und hat keinen nativen Lifecycle-Claim.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/lighttpd.conf](minimal/lighttpd.conf) | Host-Konfiguration | Stock-natives Modul mit deaktivierten Bodies. |
| [minimal/msconnector-runtime.conf](minimal/msconnector-runtime.conf) | Runtime-Konfiguration | Regeln und begrenzte Header-Metadaten für Minimalmodus. |
| [safe/lighttpd-http1-identity.conf](safe/lighttpd-http1-identity.conf) | Host-Konfiguration | Gepatchte native HTTP/1.1-Identity-Entity-Referenz. |
| [safe/msconnector-runtime.conf](safe/msconnector-runtime.conf) | Runtime-Konfiguration | Gestreamte Body-Modi und Safe-P4-Policy. |
| [rules/README.de.md](rules/README.de.md) | Dokumentation | No-CRS-Quelle und Phasen-IDs. |
| [expected/p1-p4-safe.de.md](expected/p1-p4-safe.de.md) | Dokumentation | Konfigurationsabsicht, keine Run-Evidence. |
| [compatibility-sidecar/](compatibility-sidecar/README.de.md) | Kompatibilität | Illustrativer nicht-nativer Proxyaufbau. |

Alle genannten Pfade sind ab examples/lighttpd repository-relativ. Pfade in
den Konfigurationen sind Beispiele für Hostinstallation oder Hostruntime.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| server.modules | Geordnete Namen installierter lighttpd-Module | Pflicht; Host-Konfiguration; Server-Scope | mod_msconnector für Minimal und mod_proxy plus mod_msconnector für Safe. Passende Modul-ABI verwenden. |
| server.document-root, errorlog, pid-file, upload-dirs | Absolute Hostpfade | In diesen Referenzen Pflicht; Host-Konfiguration; Server-Scope | /srv/lighttpd/htdocs, /srv/lighttpd/log/error.log, /srv/lighttpd/run/lighttpd.pid, /srv/lighttpd/runtime/uploads. Mit passenden Service-Rechten anlegen. |
| server.bind und server.port | Listener-Host und dezimaler Port | Pflicht; Host-Konfiguration; Server-Scope | 127.0.0.1 und 8080. Öffentlicher Bind verändert die Exponierung. |
| msconnector.config-file | Absoluter Pfad zur Runtime-Key=value-Datei | Pflicht; Host-Konfiguration; Modul-Scope | /etc/lighttpd/msconnector-runtime.conf. Die Datei muss für den Hostprozess lesbar sein. |
| rules_file | Installierte geprüfte Regeldatei | Pflicht; Runtime-Konfiguration; Engine-Scope | /etc/modsecurity/no-crs-baseline.conf. Regeln können Traffic blockieren. |
| transaction_id_header | HTTP-Korrelationsheadername | Pflicht; Runtime-Konfiguration; Transaction-Scope | x-modsec-transaction-id. Nur Metadaten, keine Secrets verwenden. |
| request_body_mode und response_body_mode | none, buffered oder streaming gemäß Hostfähigkeit | Pflicht; Runtime-Konfiguration; Engine-Scope | none für Stock-Minimal; streaming für passendes gepatchtes Safe. Streaming nie auf Stock-Host aktivieren. |
| request_body_limit, response_body_limit, body_limit_action | Positive Byte-Limits und reject- oder process_partial-Policy | Bei aktivierten Bodies Pflicht; Runtime-Konfiguration; Engine-Scope | 1048576 und reject. Grenzen bedeuten kein vollständiges Connector-Buffering. |
| phase4_mode | P4-Policy: minimal, safe oder strict | In diesen Runtime-Dateien Pflicht; Runtime-Konfiguration; Engine-Scope | safe für gepatchtes Safe. Beweist weder Statuswechsel noch Abbruch. |
| server.stream-response-body und proxy.server | Gepatchte Delivery-Einstellung und lokale Upstream-Route | Nur in Safe-Hostdatei Pflicht; Host-Konfiguration; Server-Scope | 1 und 127.0.0.1:8081. Nur Identity-HTTP/1.1; kein gzip/br- oder HTTP/2-Verhalten ableiten. |
| event_path | Beschreibbares JSONL-Metadatenziel | In diesen Referenzen Pflicht; Runtime-Konfiguration; Engine-Scope | /var/log/lighttpd/msconnector-events.jsonl. Schützen und rotieren; keine Bodies oder Secrets schreiben. |

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md)
dokumentiert die zwei registrierten `msconnector.*`-Schlüssel, alle aktuellen
Common-Runtime-Schlüssel und die getrennt markierte Sidecar-Kompatibilitätskonfiguration.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `msconnector.enabled` | Host / Connector | Aktiviert oder deaktiviert den nativen Plugin-Start. |
| `SecRuleEngine` | ModSecurity Engine | Wählt Enforcement, DetectionOnly oder Off in der Runtime-Regeldatei. |
| `request_body_mode` | Common Runtime | Wählt Stock-none oder gepatchte Streaming-P2-Eingabe. |
| `response_body_mode` | Common Runtime | Wählt Stock-none oder gepatchte Streaming-P4-Eingabe. |
| `phase4_mode` | Common Runtime | Wählt die Late-P4-Policy; der Source implementiert keinen strikten Host-Abbruch. |

`msconnector.enabled = "disable"` verhindert den Common-Runtime-Start. Bei
aktivem Plugin lässt `SecRuleEngine Off` Host-Callbacks bestehen, deaktiviert
aber die Engine-Regelauswertung. Der Sidecar-Proxy hat keinen nativen
Lifecycle-Anspruch.

## Validierung

Passendes lighttpd-Modul und Konfigurationsdateien installieren, alle Pfade
anpassen und danach die installierte Host-Konfiguration prüfen. Der folgende
Pfad ist ein Installationsbeispiel:

~~~sh
lighttpd -tt -f /etc/lighttpd/lighttpd.conf
~~~

Für die Safe-Referenz zusätzlich exaktes gepatchtes Host-/Modulpaar und privaten
lokalen Upstream prüfen, bevor sie gestartet wird. Ein Konfigurationscheck
beweist nur Syntax und lesbare Inputs, nicht P1--P4-Ergebnisse, Safe-Host-
Actions, Strict-Verhalten, Produktionsreife oder CRS-Abdeckung.

## Verwandtes Material

- [lighttpd-Connector-Quellcode und gepatchte Hostgrenze](../../connectors/lighttpd/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
