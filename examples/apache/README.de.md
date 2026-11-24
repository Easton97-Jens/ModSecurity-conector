# Apache-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

Das native httpd-Modul muss zur ABI der installierten Apache-Version passen.
Diese HTTP/1.1-Referenzen decken Request-Header/-Body (P1/P2) und
Response-Header/-Body (P3/P4) ab.

## Dateien

| Konfiguration | Zweck |
| --- | --- |
| [off/httpd.conf](off/httpd.conf) | Native Interventionsbehandlung mit abgeschalteter zusätzlicher Late-Policy |
| [safe/httpd.conf](safe/httpd.conf) | Safe-Einstiegsreferenz für P1–P4 |
| [strict/httpd.conf](strict/httpd.conf) | Strict-Policy für späte Aktionen |
| [all/httpd.conf](all/httpd.conf) | Vollständiges Parameterlayout mit `modsecurity_phase4_mode strict` |
| [detection-only/httpd.conf](detection-only/httpd.conf) | Aktiver Connector mit DetectionOnly-Regeln |
| [disabled/httpd.conf](disabled/httpd.conf) | Durch `modsecurity off` deaktivierter Connector |

`all` bezeichnet das Layout. Zulässige Phase-4-Werte sind `off`, `safe` und `strict`.

## Anzupassende Werte

Installierten Modulpfad, `modsecurity_rules_file`, Listener/Upstream und
Logziele anpassen. Pfade unter `/etc/modsecurity` und `/var/log` sind
Installationsbeispiele. Body-Zugriff, MIME-Auswahl, Inspektionslimits und
Limitaktionen in Engine-Regeln konfigurieren. Das veraltete
`modsecurity_phase4_body_limit` entfernen.

Request-Metadaten in `modsecurity_phase4_log` schützen und rotieren. Ein
root-eigenes Elternverzeichnis muss gegen Schreibzugriffe durch Gruppe/Andere
geschützt sein. Die reguläre Logdatei vorab mit Apache-Worker-Eigentümerschaft
anlegen und diese bei Rotation erhalten. Der Öffner setzt Modus `0600`.

Die Korrelationsüberschreibungen in `all/httpd.conf` sind auskommentiert.
`modsecurity_transaction_id_expr` oder `modsecurity_transaction_id` nur mit
einem validierten, eindeutigen und vom Host erzeugten Wert aktivieren. Syntax,
Defaults und Merge-Verhalten stehen in der generierten
[Konfigurationsreferenz](configuration-reference.de.md).

## Profile

### DetectionOnly-Profil

DetectionOnly wertet Regeln aus und zeichnet Treffer auf, unterdrückt dabei
disruptive Engine-Aktionen. Dazu dient
[rules/detection-only.conf](rules/detection-only.conf).

### Deaktiviertes Profil

`modsecurity off` verhindert Connector-Transaktionen. Bei aktivem Connector
deaktiviert [rules/engine-off.conf](rules/engine-off.conf) die
Engine-Regelauswertung über `SecRuleEngine Off`.

## P1--P4-Safe-Absicht

[rules/request-only.conf](rules/request-only.conf) aktiviert Request-Inspektion.
[rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) ergänzt Response-Inspektion und
die lokale Beispielregel `9002801`. Apache hängt jeden Daten-Bucket an die
Engine an, leitet ihn weiter und löst die finale Body-Entscheidung bei EOS auf.
Nach dem Response-Commit zeichnet Safe ein disruptives Ergebnis als
`log_only` auf und setzt fort.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Strict wählt nach dem Commit den nativen Connection-Abort-Pfad. Das
client-sichtbare Ergebnis am installierten Host validieren, bevor darauf
vertraut wird. Der fokussierte Regressionseinstieg ist
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`.

## No-CRS-Regeln

Eine geprüfte Kopie der [No-CRS-Baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
am konfigurierten Regelpfad installieren. Ihre IDs `1100001`, `1100101`,
`1100201` und `1100301` entsprechen P1, P2, P3 und P4. Die lokale Regel
`9002801` dient der Illustration. Regel-IDs und Engine-Beispiele erklärt der
[gemeinsame Regel-Leitfaden](../common/rule-examples.de.md).

## Validierung

Nach Installation der gewählten Dateien und Anpassung der Pfade die gesamte
Apache-Konfiguration prüfen.

~~~sh
apachectl -t
~~~

Nach einem beabsichtigten Reload Error-, Decision- und Audit-Logs prüfen.
Runtime-Enforcement benötigt profilspezifische Traffic-Evidenz. Siehe
[Apache-Connector-Leitfaden](../../connectors/apache/README.de.md) und
[Beispielindex](../README.de.md).
