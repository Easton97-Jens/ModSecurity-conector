# NGINX-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: natives NGINX-HTTP-Modul.
[minimal/nginx.conf](minimal/nginx.conf) ist Request-only.
[safe/nginx.conf](safe/nginx.conf) ist die begrenzte HTTP/1.1-P1--P4-Safe-
Referenz. [strict/nginx.conf](strict/nginx.conf) dokumentiert eine
parser-unterstützte Konfigurationsform, nicht die Behauptung eines beobachteten
späten Abbruchs oder Statuswechsels.

Der P4-Body-Filter läuft nach dem Response-Header-Pfad. Safe zeichnet späte
Ergebnisse daher auf, ohne sie als sauberen client-sichtbaren 403 darzustellen.
Die Referenz schaltet gzip aus, bis die Byte-Repräsentation des installierten
Moduls validiert wurde. Sie verspricht weder P4-Bewertung pro Chunk noch einen
vollständigen Connector-Response-Buffer.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/nginx.conf](minimal/nginx.conf) | Host-Konfiguration | Request-only-Referenz des nativen Moduls. |
| [safe/nginx.conf](safe/nginx.conf) | Host-Konfiguration | Begrenzte P1--P4-Safe-Referenz. |
| [strict/nginx.conf](strict/nginx.conf) | Host-Konfiguration | Explizit begrenzte Strict-Konfigurationsform. |
| [rules/request-only.conf](rules/request-only.conf) | Regeln | Request-only-Einstellungen. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Regeln | Begrenzte P4-Einstellungen und lokale Illustration. |
| [rules/README.de.md](rules/README.de.md) | Dokumentation | No-CRS-Quelle und Regel-IDs. |
| [expected/p1-p4-safe.de.md](expected/p1-p4-safe.de.md) | Dokumentation | Nur Absicht, keine Test-Evidence. |

Die genannten Pfade sind ab examples/nginx repository-relativ. Modul, Regeln,
Logs, Listener und Upstream-Werte darin sind Hostbeispiele.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| load_module-Pfad | Installiertes dynamisches NGINX-Modul | Pflicht; kein Repository-Default; Betreiber; Main-Scope | modules/ngx_http_modsecurity_module.so. Das Modul muss zur exakten NGINX-ABI passen. |
| modsecurity_rules_file | Lesbare libmodsecurity-Regeldatei | Pflicht; kein Repository-Default; Host-Konfiguration; http-Scope | /etc/modsecurity/modsecurity-phase4.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| modsecurity_phase4_mode | P4-Policy: minimal, safe oder strict | Für Safe- oder Strict-Datei Pflicht; Host-Konfiguration; http-Scope | safe in safe/nginx.conf. Strict ist hier nur Konfiguration. |
| modsecurity_phase4_content_types_file | Explizite Liste der Response-MIME-Typen | Optional; Host-Konfiguration; http-Scope | /etc/modsecurity/phase4-content-types.conf. Fehlende Datei lässt Validierung fehlschlagen. |
| modsecurity_phase4_log | Ziel für Decision-JSONL | Optional; Host-Konfiguration; http-Scope | /var/log/modsecurity/nginx-phase4.jsonl. Request-Metadaten schützen und rotieren. |
| app_backend und 127.0.0.1:8081 | Upstream-Gruppe und lokaler TCP-Endpunkt | Für diese Proxy-Referenzen Pflicht; Host-Konfiguration; http-Scope | Durch gewünschten Upstream ersetzen. Loopback vermeidet unbeabsichtigte Freigabe beim lokalen Test. |
| listen 8080 und server_name example.test | Listener und Virtual-Host-Selektor | In diesen Dateien Pflicht; Host-Konfiguration; Server-Scope | Für installierten Host ersetzen; ein öffentlicher Bind verändert die Exponierung. |
| SecResponseBodyLimit | Positives P4-Byte-Limit | Für begrenzte P4-Regeln Pflicht; Regeldatei; Rule-Engine-Scope | 1048576 Bytes. Aus dieser Referenz kein unbegrenztes Verhalten ableiten. |

Regel-ID 9001801 ist nur illustrativ, weder OWASP-CRS- noch No-CRS-Baseline-ID;
siehe [rules/README.de.md](rules/README.de.md).

## Validierung

Die gewählte Datei in die installierte NGINX-Konfiguration kopieren oder
einbinden, alle Hostwerte anpassen und danach die vollständige installierte
Konfiguration prüfen:

~~~sh
nginx -t
~~~

Nach einem beabsichtigten Reload NGINX-Error-Log und konfigurierte
ModSecurity-Logs prüfen. Die Validierung beweist nur Syntax und lesbare
Abhängigkeiten, nicht P1--P4-Ergebnisse, sichtbaren späten P4-Status,
Strict-Abbruch, Produktionsreife oder CRS-Abdeckung.

## Verwandtes Material

- [NGINX-Connector-Quellcode und Validierungsgrenze](../../connectors/nginx/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
