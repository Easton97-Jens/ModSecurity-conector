# Apache-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: natives httpd-Modul. Die [Minimalreferenz](minimal/httpd.conf)
ist Request-orientiert; die [Safe-Referenz](safe/httpd.conf) wählt die native
HTTP/1.1-P1--P4-Konfigurationsform. P1 sind Request-Header, P2 Request-Body,
P3 Response-Header und P4 Response-Body.

Safe ist eine Policy nach dem Commit, keine Garantie eines sichtbaren Status.
Der Filter gibt aktuelle Daten weiter und beendet die Response-Body-Verarbeitung
bei EOS. Das verspricht weder Regelbewertung pro Chunk noch einen
Connector-eigenen vollständigen Response-Buffer. Eine späte P4-Entscheidung
muss als Log-only aufgezeichnet werden, solange passende Host-Evidence nichts
Weiteres belegt. Das [Strict-Verzeichnis](strict/README.de.md) dokumentiert den
parserunterstützten optionalen Wert, behauptet aber keinen client-sichtbaren
Abbruch.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/httpd.conf](minimal/httpd.conf) | Host-Konfiguration | Request-orientierter Ausgangspunkt. |
| [safe/httpd.conf](safe/httpd.conf) | Host-Konfiguration | Begrenzte native P1--P4-Safe-Referenz. |
| [rules/request-only.conf](rules/request-only.conf) | Regeln | Rule-Engine-Einstellungen nur für Requests. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Regeln | Begrenzte Response-Body-Einstellungen und lokale P4-Illustration. |
| [rules/README.de.md](rules/README.de.md) | Dokumentation | No-CRS-Quelle und Bedeutung der Regel-IDs. |
| [expected/p1-p4-safe.de.md](expected/p1-p4-safe.de.md) | Dokumentation | Konfigurationsabsicht, kein Testergebnis. |

Alle Pfade in dieser Tabelle sind ab examples/apache repository-relativ. Pfade
in der Konfiguration, einschließlich /usr/lib/apache2/modules/mod_security3.so,
/etc/modsecurity und /var/log, sind Beispiele für Hostinstallationen.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| security3_module | Von LoadModule geladenes Modul | Pflicht; kein Repository-Default; Apache-Paket oder lokaler Build; Server-Scope | mod_security3.so an installiertem Modulpfad. Falsche ABI oder falscher Pfad verhindert den Start. |
| modsecurity_rules_file | Lesbare libmodsecurity-Regeldatei | Pflicht; kein Repository-Default; Host-Konfiguration; Modul-Scope | /etc/modsecurity/modsecurity-phase4.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| modsecurity_phase4_mode | Late-P4-Policy: minimal, safe oder strict | Nur Safe-Datei; Host-Konfiguration; Modul-Scope | safe. Eine späte Entscheidung wird nicht als erfundener Status dargestellt. |
| modsecurity_phase4_content_types_file | Datei expliziter Response-MIME-Typen | Optional; Host-Konfiguration; Modul-Scope | /etc/modsecurity/phase4-content-types.conf. Eng halten; unlesbare Datei lässt Validierung fehlschlagen. |
| modsecurity_phase4_log | Ziel für Decision-JSONL | Optional; Host-Konfiguration; Modul-Scope | /var/log/modsecurity/apache-phase4.jsonl. Request-Metadaten schützen und rotieren. |
| modsecurity_phase4_body_limit und SecResponseBodyLimit | Positive P4-Byte-Limits | Für begrenztes Safe Pflicht; Host- und Regeldatei; keine automatische Angleichung | 1048576 Bytes. Abweichungen ändern den P4-Input; nie unbegrenzt setzen. |
| SecRequestBodyAccess und SecResponseBodyAccess | Request-/Response-Body-Schalter | In passenden Regeln Pflicht; Rule-Engine-Scope | On in Safe-Regeln; Response Access ist bei Request-only Off. |
| SecResponseBodyMimeType und SecResponseBodyLimitAction | P4-Scope und Policy über dem Limit | In Safe-Regeln Pflicht; Rule-Engine-Scope | Explizite Text-/JSON-Typen und ProcessPartial. Kein Binary-Verhalten ableiten. |
| SecAuditLog | Audit-Log-Ziel | Optional; Regeldatei; Rule-Engine-Scope | /var/log/modsecurity/apache-audit.log. Zugriff und Aufbewahrung steuern. |

Regel-ID 9002801 gehört nur zu p1-p4-safe.conf. Sie ist weder eine OWASP-CRS-
noch eine No-CRS-Baseline-ID; siehe [rules/README.de.md](rules/README.de.md).

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md)
dokumentiert alle 11 registrierten Apache-Direktiven, die hier verwendeten
Hostfelder und ihre Parser-/Default-/Merge-Anker.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `modsecurity on|off` | Host / Connector | Aktiviert oder deaktiviert die Apache-Transaction-Erzeugung. |
| `SecRuleEngine` | ModSecurity Engine | Wertet geladene Regeln aus und wählt Enforcement, DetectionOnly oder Off. |
| `SecRequestBodyAccess` | ModSecurity Engine | Stellt dem Engine-P2-Request-Body-Eingaben bereit. |
| `SecResponseBodyAccess` | ModSecurity Engine | Stellt berechtigte P4-Response-Body-Eingaben bereit. |
| `modsecurity_phase4_mode` | Connector / Common Policy | Wählt die gewünschte Late-P4-Policy; Safe verspricht keine späte 403. |

`modsecurity on` mit `SecRuleEngine Off` erzeugt den Connector-Pfad, schaltet
aber die Engine-Regelauswertung ab. `modsecurity off` verhindert eine
Connector-Transaction auch dann, wenn eine Regeldatei `SecRuleEngine On` setzt.

## Validierung

Die gewählten Dateien installieren oder einbinden, alle Hostpfade anpassen und
die vollständige installierte Apache-Konfiguration prüfen:

~~~sh
apachectl -t
~~~

Nach einem beabsichtigten Reload Apache-Error-Log, Decision-Log und Audit-Log
prüfen. Ein Syntaxcheck beweist weder P1--P4-Verhalten noch einen
client-sichtbaren P4-Status, CRS-Abdeckung oder Produktionsreife.

## Verwandtes Material

- [Apache-Connector-Quellcode und Validierungsgrenze](../../connectors/apache/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
