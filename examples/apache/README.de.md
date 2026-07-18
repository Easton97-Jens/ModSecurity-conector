# Apache-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: natives httpd-Modul. Die [Minimalreferenz](minimal/httpd.conf)
ist Request-orientiert; die [Safe-Referenz](safe/httpd.conf) wählt die native
HTTP/1.1-P1--P4-Konfigurationsform. P1 sind Request-Header, P2 Request-Body,
P3 Response-Header und P4 Response-Body.

Safe ist die ausgewählte Konfiguration für Apaches EOS-only-All-Response-
Phase-4-Gate. Der Filter hängt Daten-Buckets inkrementell an, hält aber jede
normalisierte Response-Brigade bis zum ersten EOS zurück, bevor er ein
ursprüngliches Byte freigibt. Danach schließt er die Response-Body-Verarbeitung
ab und löst die Intervention genau einmal auf. Das verspricht weder
Regelauswertung pro Chunk noch für Clients sichtbares progressives Response-
Streaming. Ein normaler Deny wird vor der Freigabe der ursprünglichen Ausgabe
aufgelöst; Safe-<code>log_only</code> ist nur ein defensiver Fallback für eine
getrennt als bereits committed nachgewiesene Response. Die
[Strict-Profilgrenze](#strict-profilgrenze) dokumentiert den parserunterstützten
optionalen Fallback-Wert, behauptet aber keinen client-sichtbaren Abbruch.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/httpd.conf](minimal/httpd.conf) | Host-Konfiguration | Request-orientierter Ausgangspunkt. |
| [safe/httpd.conf](safe/httpd.conf) | Host-Konfiguration | Begrenzte native P1--P4-Safe-Referenz. |
| [detection-only/httpd.conf](detection-only/httpd.conf) | Host-Konfiguration | Nativer Connector mit DetectionOnly-Engine-Regeln; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/httpd.conf](disabled/httpd.conf) | Host-Konfiguration | Auf Apache-Ebene deaktivierter Connector; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/request-only.conf](rules/request-only.conf) | Regeln | Rule-Engine-Einstellungen nur für Requests. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Regeln | Begrenzte Response-Body-Einstellungen und lokale P4-Illustration. |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | No-CRS-Quelle und Bedeutung der Regel-IDs. |
| [P1--P4-Safe-Absicht](#p1-p4-safe-absicht) | Dokumentation | Konfigurationsabsicht, kein Testergebnis. |

Alle Pfade in dieser Tabelle sind ab examples/apache repository-relativ. Pfade
in der Konfiguration, einschließlich /usr/lib/apache2/modules/mod_security3.so,
/etc/modsecurity und /var/log, sind Beispiele für Hostinstallationen.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| security3_module | Von LoadModule geladenes Modul | Pflicht; kein Repository-Default; Apache-Paket oder lokaler Build; Server-Scope | mod_security3.so an installiertem Modulpfad. Falsche ABI oder falscher Pfad verhindert den Start. |
| modsecurity_rules_file | Lesbare libmodsecurity-Regeldatei | Pflicht; kein Repository-Default; Host-Konfiguration; Modul-Scope | /etc/modsecurity/modsecurity-phase4.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| modsecurity_phase4_mode | Defensiver Late-P4-Fallback: minimal, safe oder strict | Nur Safe-Datei; Host-Konfiguration; Modul-Scope | safe. Ein normaler gegateter Deny wird vor Release aufgelöst; diese Einstellung wählt nur einen unerwarteten bereits-committed Fallback. |
| modsecurity_phase4_content_types_file | Veraltete Legacy-Datei für Response-MIME-Typen | Optionaler Kompatibilitätsparser; Host-Konfiguration; Modul-Scope | Für neue Apache-Profile nicht konfigurieren: Sie kann das All-Response-Gate nicht einschränken. `SecResponseBodyMimeType` wählt die Engine-Inspektion. |
| modsecurity_phase4_log | Ziel für Decision-JSONL | Optional; Host-Konfiguration; Modul-Scope | /var/log/modsecurity/apache-phase4.jsonl. Request-Metadaten schützen und rotieren. |
| modsecurity_phase4_body_limit und SecResponseBodyLimit | Positive P4-Byte-Limits | Für begrenztes Safe Pflicht; Host- und Regeldatei; keine automatische Angleichung | Connector-Standard sind 1048576 Byte. Das ist ein hartes fail-closed-All-Response-Gate-Limit; eine libModSecurity-`ProcessPartial`-Policy gibt keinen uninspektierten Connector-Tail frei. |
| SecRequestBodyAccess und SecResponseBodyAccess | Request-/Response-Body-Schalter | In passenden Regeln Pflicht; Rule-Engine-Scope | On in Safe-Regeln; Response Access ist bei Request-only Off. |
| SecResponseBodyMimeType und SecResponseBodyLimitAction | Engine-P4-Scope und Policy über dem Limit | In Safe-Regeln Pflicht; Rule-Engine-Scope | Explizite Text-/JSON-Typen wählen die Engine-Inspektion; sie schränken Apaches All-Response-Gate nicht ein. Kein Binary-Verhalten ableiten. |
| SecAuditLog | Audit-Log-Ziel | Optional; Regeldatei; Rule-Engine-Scope | /var/log/modsecurity/apache-audit.log. Zugriff und Aufbewahrung steuern. |

Regel-ID 9002801 gehört nur zu p1-p4-safe.conf. Sie ist weder eine OWASP-CRS-
noch eine No-CRS-Baseline-ID; siehe [No-CRS-Regeln](#no-crs-regeln).

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
| `modsecurity_phase4_mode` | Connector / Common Policy | Wählt nur einen defensiven bereits-committed Fallback; ein gewöhnlicher gegateter P4-Deny wird vor der Freigabe der ursprünglichen Ausgabe aufgelöst. |

`modsecurity on` mit `SecRuleEngine Off` erzeugt den Connector-Pfad, schaltet
aber die Engine-Regelauswertung ab. `modsecurity off` verhindert eine
Connector-Transaction auch dann, wenn eine Regeldatei `SecRuleEngine On` setzt.

## Profile

### DetectionOnly-Profil

`detection-only/httpd.conf` lässt `modsecurity on` aktiv und wählt die
DetectionOnly-Regeldatei. DetectionOnly lädt und bewertet Engine-Regeln und
zeichnet Treffer auf, führt aber keine disruptiven Engine-Aktionen aus.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/httpd.conf` setzt `modsecurity off`; Apache erzeugt keine Connector-
Transaction. Dies unterscheidet sich von `SecRuleEngine Off`, das bei aktivem
Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Safe-Absicht

Die Safe-Referenz konfiguriert die Verarbeitung des nativen httpd-Moduls für
P1 bis P4 und ein All-Response-Gate von 1048576 Byte. Apache speichert alle
normalisierten Output-Brigades bis zum ersten EOS, einschließlich des EOS einer
leeren Response; ein normaler P4-Deny verwirft diese gespeicherte ursprüngliche
Response und sendet den terminalen Fehler, bevor sie freigegeben werden kann.
Die C-API macht die wirksame MIME-Entscheidung von libModSecurity für den
Connector opak; `SecResponseBodyMimeType` wählt daher Engine-Inspektion, ohne
einen Gate-Bypass zu erzeugen. Das veraltete
`modsecurity_phase4_content_types_file` fehlt absichtlich in der Safe-
Konfiguration.

Dieser Abschnitt beschreibt Konfigurationsabsicht, kein Laufergebnis. Die
Input-Aufnahme bleibt über mehrere Brigades hinweg inkrementell, der native
Pfad verspricht aber bewusst kein für Clients sichtbares progressives Response-
Streaming. Fehler beim Anhängen, Speichern oder Abschließen des Bodys verwerfen
die gespeicherte Response und schlagen fail-closed fehl. Nur eine tatsächlich
bereits committed Response kann Safe-Log-only- oder Strict-Abort-Fallback-
Verhalten verwenden. Dafür gibt es hier kein Strict-Beispiel.

## No-CRS-Regeln

Die wiederverwendbare No-CRS-Quelle ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Sie ist repository-relativ und soll vom Betreiber als geprüftes Host-Ruleset,
zum Beispiel /etc/modsecurity/no-crs-baseline.conf, installiert oder kopiert
werden.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

Die eingecheckte Datei p1-p4-safe.conf ist eine illustrative Apache-
Regeldatei. Ihre Regel 9002801 gehört nur zu diesem Beispiel und ist weder
eine OWASP-CRS- noch eine No-CRS-Baseline-ID.

## Validierung

Die gewählten Dateien installieren oder einbinden, alle Hostpfade anpassen und
die vollständige installierte Apache-Konfiguration prüfen:

~~~sh
apachectl -t
~~~

Nach einem beabsichtigten Reload Apache-Error-Log, Decision-Log und Audit-Log
prüfen. Ein Syntaxcheck beweist weder P1--P4-Verhalten noch einen
client-sichtbaren P4-Status, CRS-Abdeckung oder Produktionsreife.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

`modsecurity_phase4_mode strict` wird vom Parser unterstützt, aber dieses
Repository besitzt keinen Apache-Hostnachweis für einen client-sichtbaren
späten Abbruch. Strict ist deshalb optional und enthält hier absichtlich keine
ausführbare Konfiguration. Es gilt nur, wenn der Commit unabhängig nachgewiesen
ist; es wandelt einen normalen P4-Deny vor Release nicht in einen späten Abbruch
um.

Von `safe/httpd.conf` ausgehen, `modsecurity_phase4_mode strict` setzen,
mit `apachectl -t` validieren und host-spezifische Evidenz erfassen, bevor auf
eine Post-Commit-Aktion vertraut wird.

Der fokussierte H1/H2-Evidence-Platzhalter ist
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`. Erst nach
seiner Ausführung werden laufbezogene Artefakte erfasst; diese
Konfigurationsdokumentation behauptet keinen Pass für eines der Protokolle.

## Verwandtes Material

- [Apache-Connector-Quellcode und Validierungsgrenze](../../connectors/apache/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
