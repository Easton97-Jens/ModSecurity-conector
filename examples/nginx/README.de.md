# NGINX-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

Das native HTTP-Modul muss zur ABI der installierten NGINX-Version passen.
Diese Beispiele konfigurieren HTTP/1.1-Request- und Response-Inspektion über P1–P4.

## Dateien

| Konfiguration | Zweck |
| --- | --- |
| [off/nginx.conf](off/nginx.conf) | Native Interventionsbehandlung mit abgeschalteter zusätzlicher Late-Policy |
| [safe/nginx.conf](safe/nginx.conf) | Safe-Einstiegsreferenz für P1–P4 |
| [strict/nginx.conf](strict/nginx.conf) | Strict-Konfigurationsform mit erforderlicher Hostvalidierung |
| [all/nginx.conf](all/nginx.conf) | Vollständiges Direktivenlayout mit `modsecurity_phase4_mode strict` |
| [detection-only/nginx.conf](detection-only/nginx.conf) | Aktiver Connector mit DetectionOnly-Regeln |
| [disabled/nginx.conf](disabled/nginx.conf) | Durch `modsecurity off` deaktivierter Connector |

`all` bezeichnet das Layout. Zulässige Phase-4-Werte sind `off`, `safe` und `strict`.

## Anzupassende Werte

Modulpfad, `modsecurity_rules_file`, Listener, `server_name`, Upstream und
Logziele für die Zielinstallation setzen. Vor Freigabe des Dienstes die
konkrete Bind-Adresse prüfen. gzip deaktiviert lassen, bis die untersuchte
Byte-Repräsentation validiert wurde. Body-Zugriff, MIME-Auswahl,
Inspektionslimits und Limitaktionen gehören in Engine-Regeln. Das veraltete
`modsecurity_phase4_body_limit` entfernen.

Der optionale Sink `modsecurity_phase4_log` benötigt ein sicheres
Elternverzeichnis, eine reguläre Datei, geeignete Eigentümer und den privaten
Deskriptor-Modus `0600`. Für Rotation einen validierten Konfigurations-Reload
verwenden. Generisches NGINX-`USR1`-Erneutöffnen wird nicht unterstützt.
`modsecurity_use_error_log` steuert die Weiterleitung von Engine-Meldungen
an das NGINX-Fehlerlog.

`modsecurity_transaction_id` nur mit einem eindeutigen, servergenerierten Wert
aktivieren. Der kommentierte `$request_id`-Ausdruck setzt diese Hostvariable
voraus. Remote-Regel-Zugangsdaten und Endpunkte benötigen Betreiberkonfiguration.
Syntax, Kontexte und Defaults stehen in der generierten
[Konfigurationsreferenz](configuration-reference.de.md).

## Profile

### DetectionOnly-Profil

[rules/detection-only.conf](rules/detection-only.conf) wertet Regeln aus und
zeichnet Treffer auf, unterdrückt dabei disruptive Engine-Aktionen.

### Deaktiviertes Profil

`modsecurity off` beendet den Access-Handler-Connector-Pfad. Regeln können beim
Konfigurationsparsen weiterhin geladen werden. Bei aktivem Connector
deaktiviert [rules/engine-off.conf](rules/engine-off.conf) die
Engine-Auswertung über `SecRuleEngine Off`.

## P1--P4-Safe-Absicht

[rules/request-only.conf](rules/request-only.conf) aktiviert Request-Inspektion.
[rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) ergänzt Response-Inspektion und
die lokale Beispielregel `9001801`. Der P4-Body-Filter läuft nach dem
Response-Header-Pfad. Safe zeichnet späte Ergebnisse nach Ausgabebeginn auf.
Ein client-sichtbarer Ersatz-403 benötigt eine frühere Entscheidung.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Die Strict-Datei wird vom Parser unterstützt. Post-Commit-Abbruchverhalten am
installierten NGINX-Host validieren, bevor darauf vertraut wird. Diese Dateien
beschreiben Konfigurationsabsicht. Gehostete Event-Sink-Prüfungen und geschützte
NGINX-Attestierung behalten ihre getrennten Ausführungsanforderungen.

## No-CRS-Regeln

Eine geprüfte Kopie der [No-CRS-Baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
am konfigurierten Regelpfad installieren. Ihre IDs `1100001`, `1100101`,
`1100201` und `1100301` entsprechen P1, P2, P3 und P4. Die lokale Regel
`9001801` dient der Illustration. Siehe den
[gemeinsamen Regel-Leitfaden](../common/rule-examples.de.md).

## Validierung

Nach Anpassung von Pfaden und Endpunkten die gesamte installierte
Konfiguration prüfen.

~~~sh
nginx -t
~~~

Nach einem beabsichtigten Reload NGINX- und ModSecurity-Logs prüfen.
Runtime-Enforcement benötigt profilspezifische Traffic-Evidenz. Siehe
[NGINX-Connector-Leitfaden](../../connectors/nginx/README.de.md) und
[Beispielindex](../README.de.md).
