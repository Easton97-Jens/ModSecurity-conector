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
| [detection-only/nginx.conf](detection-only/nginx.conf) | Host-Konfiguration | Nativer Connector mit DetectionOnly-Engine-Regeln; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/nginx.conf](disabled/nginx.conf) | Host-Konfiguration | Auf NGINX-Ebene deaktivierter Connector; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/request-only.conf](rules/request-only.conf) | Regeln | Request-only-Einstellungen. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Regeln | Begrenzte P4-Einstellungen und lokale Illustration. |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | No-CRS-Quelle und Regel-IDs. |
| [P1--P4-Safe-Absicht](#p1-p4-safe-absicht) | Dokumentation | Nur Absicht, keine Test-Evidence. |

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
siehe [No-CRS-Regeln](#no-crs-regeln).

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md)
dokumentiert alle 10 registrierten `ngx_command_t`-Direktiven, ihre
`http → server → location`-Kontexte und die umgebenden Beispiel-Hostfelder.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `modsecurity on|off` | Host / Connector | Aktiviert oder deaktiviert die NGINX-Connector-Verarbeitung im gemergten Kontext. |
| `SecRuleEngine` | ModSecurity Engine | Wertet geladene Regeln aus und wählt Enforcement, DetectionOnly oder Off. |
| `SecRequestBodyAccess` | ModSecurity Engine | Stellt dem Engine-P2-Request-Body-Eingaben bereit. |
| `SecResponseBodyAccess` | ModSecurity Engine | Stellt berechtigte P4-Response-Body-Eingaben bereit. |
| `modsecurity_phase4_mode` | Connector / Common Policy | Wählt die gewünschte Late-P4-Policy; Safe verspricht keine späte 403. |

`modsecurity off` beendet den NGINX-Access-Handler-Connector-Pfad; konfigurierte
Regeln können beim Konfigurationsparsen trotzdem geladen worden sein.
`SecRuleEngine` ist eine Engine-Einstellung und lädt oder aktiviert das
NGINX-Modul nicht selbst.

## Profile

### DetectionOnly-Profil

`detection-only/nginx.conf` lässt `modsecurity on` aktiv und wählt die
DetectionOnly-Regeldatei. DetectionOnly lädt und bewertet Engine-Regeln und
zeichnet Treffer auf, führt aber keine disruptiven Engine-Aktionen aus.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/nginx.conf` setzt `modsecurity off`; NGINX erzeugt keine Connector-
Transaction. Dies unterscheidet sich von `SecRuleEngine Off`, das bei aktivem
Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Safe-Absicht

Die Safe-Konfiguration aktiviert das native Modul, beschränkt die
Response-Prüfung auf die genannten Content-Types und verwendet Safe für eine
späte P4-Entscheidung. Ein später Treffer verspricht keinen vom Client
gesehenen Ersatz-403. Die Referenz lässt gzip deaktiviert, damit die
untersuchte Byte-Repräsentation nicht vorausgesetzt wird.

Die Strict-Konfiguration ist nur eine vorhandene Konfigurationsform. Sie
beweist weder einen clientbeobachteten Abbruch noch einen Statuswechsel oder
vollständiges Response-Buffering.

## No-CRS-Regeln

Die wiederverwendbare No-CRS-Quelle ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Eine geprüfte Kopie am in der NGINX-Konfiguration gewählten Rules-Dateipfad
installieren.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

Die illustrative Datei p1-p4-safe.conf verwendet 9001801 nur als lokales
Beispiel. Es ist weder eine OWASP-CRS- noch eine No-CRS-Baseline-ID.

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

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

[strict/nginx.conf](strict/nginx.conf) ist eine parserunterstützte Strict-
Konfigurationsform. Sie behauptet keinen sichtbaren späten Statuswechsel;
Post-Commit-Strict-Verhalten muss gegen den installierten NGINX-Host validiert
werden.

Pfade und Endpunkte anpassen, `nginx -t` ausführen und einen Abbruch als
host-spezifisches Ergebnis statt als garantierte spätere 403 behandeln.

## Verwandtes Material

- [NGINX-Connector-Quellcode und Validierungsgrenze](../../connectors/nginx/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
