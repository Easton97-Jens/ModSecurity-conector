# HAProxy-Beispiele für nativen HTX

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: nativer HTX-Filter. Die nativen Referenzen
[minimal](minimal/haproxy-htx.cfg) und [Safe](safe/haproxy-htx.cfg) sind von
dem bewahrten [SPOE/SPOP-Kompatibilitätsmaterial](compatibility-spoe/README.de.md)
getrennt.

Die Safe-Datei wählt phase4-mode safe für den ausgewählten HTTP/1.1-P1--P4-
Kern. Sie ist eine Konfigurationsreferenz für den gepatchten Hostfilter, keine
Behauptung, dass Stock-HAProxy ihn lädt. P1, P2, P3 und P4 sind Request-Header,
Request-Body, Response-Header und Response-Body. An der späten P4-Grenze
bewahrt Safe die Response, statt einen Statuswechsel zu erfinden. Dieses
Verzeichnis behauptet weder vollständiges Response-Buffering noch
Regelbewertung pro Chunk oder einen clientbeobachteten Strict-Abbruch. Das
[Strict-Verzeichnis](strict/README.de.md) hält die optionale Parsergrenze fest,
ohne einen nativen Host-Abbruch zu behaupten.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/haproxy-htx.cfg](minimal/haproxy-htx.cfg) | Host-Konfiguration | Parser-unterstützter minimaler P4-Modus des nativen HTX. |
| [safe/haproxy-htx.cfg](safe/haproxy-htx.cfg) | Host-Konfiguration | Native HTTP/1.1-P1--P4-Safe-Referenz. |
| [rules/README.de.md](rules/README.de.md) | Dokumentation | Quelle und IDs der kanonischen No-CRS-Rules-Datei. |
| [expected/p1-p4-safe.de.md](expected/p1-p4-safe.de.md) | Dokumentation | Konfigurationsabsicht, kein Laufergebnis. |
| [compatibility-spoe/](compatibility-spoe/README.de.md) | Kompatibilität | Früherer SPOE/SPOP-Pfad, absichtlich getrennt. |

Die nativen Referenzen verwenden Hostinstallationswerte: Listener
127.0.0.1:8080, Upstream 127.0.0.1:8081 und Rules-Datei
/etc/modsecurity/no-crs-baseline.conf. Keiner davon ist ein
repository-relativer Pfad.

## Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel, Auswirkung und Sicherheit |
| --- | --- | --- | --- |
| filter modsecurity-htx | Direktive des gepatchten HAProxy-Filters | Pflicht; kein Stock-Host-Default; im Frontend-Scope konfiguriert | Der gepatchte Host muss diesen Parser bereitstellen. Lehnt ein Stock-Binary ihn ab, ist das eine Konfigurationsinkompatibilität, kein Grund für stilles Fallback. |
| rules-file | Lesbare installierte Regeldatei | Pflicht; kein Repository-Default; Filterargument; Frontend-Scope | /etc/modsecurity/no-crs-baseline.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| phase4-mode | P4-Policy: minimal, safe oder strict | Optionales Filterargument; Frontend-Scope; Safe-Datei setzt safe | safe. Zeichnet ein spätes P4-Ergebnis auf, ohne es als Statuswechsel auszugeben. |
| bind-Adresse | Listener-TCP-Adresse | Pflicht; Host-Konfiguration; Frontend-Scope | 127.0.0.1:8080. Für lokale Tests private Adresse wählen; ein öffentlicher Bind verändert die Exponierung. |
| Upstream-Server | Backend-Host und TCP-Port | Pflicht; Host-Konfiguration; Backend-Scope | 127.0.0.1:8081. Durch gewünschten Application-Endpunkt ersetzen. |
| timeout connect/client/server | Positive HAProxy-Dauer | In diesen Referenzen Pflicht; Host-Konfiguration; defaults-Scope | 2s und 5s. Für die Anwendung anpassen; Timeouts sind keine WAF-Entscheidungen. |

No-CRS-Regel-IDs und ihre Phasenbedeutung stehen in
[rules/README.de.md](rules/README.de.md). Die historischen SPOE-Optionen und
ihre getrennten Limits bleiben bei den Kompatibilitätsdateien dokumentiert.

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md) trennt
den nativen HTX-Parser von den SPOE/SPOP-Kompatibilitätsdateien.

| Einstellung | Ebene | Aufgabe |
| --- | --- | --- |
| `filter modsecurity-htx` | Host / Connector | Bindet den ausgewählten nativen HTX-Lifecycle-Filter ein. |
| `SecRuleEngine` | ModSecurity Engine | Wertet Regeln aus, die über `rules-file` geladen werden. |
| `SecRequestBodyAccess` | ModSecurity Engine | Erlaubt P2-Eingaben, wenn natives HTX sie liefert. |
| `SecResponseBodyAccess` | ModSecurity Engine | Erlaubt P4-Eingaben, wenn natives HTX sie liefert. |
| `phase4-mode` | Connector / Common Policy | Fordert die Late-P4-Policy minimal, safe oder strict an. |

Das Entfernen des nativen Filters deaktiviert den Connector-Pfad.
`SecRuleEngine Off` entfernt den Filter nicht, deaktiviert aber die
Engine-Regelverarbeitung. `filter spoe` bleibt ein getrennter
Kompatibilitätsweg und keine native HTX-Einstellung.

## Validierung

Die gewählte Referenz in eine installierte gepatchte HAProxy-Konfiguration
übernehmen, Rules-Datei und Adressen anpassen und danach den Hostchecker
ausführen:

~~~sh
haproxy -c -f /etc/haproxy/haproxy.cfg
~~~

Der Pfad ist ein Distributionsbeispiel; den echten Host-Konfigurationspfad
wählen. Ein erfolgreicher Check beweist, dass dieses HAProxy-Binary die Datei
geparst hat. Er beweist weder P1--P4-Ergebnisse noch P4-Clientverhalten,
Strict-Abbrüche, Produktionsreife oder native HTX-Eigenschaften des
SPOE/SPOP-Kompatibilitätspfads.

## Verwandtes Material

- [HAProxy-Connector-Quellcode und native HTX-Grenze](../../connectors/haproxy/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
