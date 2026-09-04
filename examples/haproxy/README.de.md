# HAProxy-Beispiele für nativen HTX

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Integrationsmodus: nativer HTX-Filter. Die nativen Referenzen
[minimal](minimal/haproxy-htx.cfg), [Safe](safe/haproxy-htx.cfg) und
[Strict](strict/haproxy-htx.cfg) sowie [all](all/haproxy-htx.cfg) bilden die
native HTX-Lösung. Die [SPOE/SPOP-Lösung](#spoespop-response-companion-lösung)
hat passende minimal-, safe-, strict- und all-Bundles und verbindet den
Request-seitigen SPOE/SPOP-Agent mit dem nativen HTX-Response-Companion. Die
all-Layouts verwenden den bestehenden Strict-Policy-Wert; sie führen keinen
P4-Policy-Wert `all` ein.

Die Safe-Datei wählt phase4-mode safe für den ausgewählten HTTP/1.1-P1--P4-
Kern. Sie ist eine Konfigurationsreferenz für den gepatchten Hostfilter, keine
Behauptung, dass Stock-HAProxy ihn lädt. P1, P2, P3 und P4 sind Request-Header,
Request-Body, Response-Header und Response-Body. An der späten P4-Grenze
bewahrt Safe die Response, statt einen Statuswechsel zu erfinden. Dieses
Verzeichnis behauptet weder vollständiges Response-Buffering noch
Regelbewertung pro Chunk oder einen clientbeobachteten Strict-Abbruch. Das
[Strict-Profilgrenze](#strict-profilgrenze) hält die optionale Parsergrenze fest,
ohne einen nativen Host-Abbruch zu behaupten.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [minimal/haproxy-htx.cfg](minimal/haproxy-htx.cfg) | Host-Konfiguration | Parser-unterstützter minimaler P4-Modus des nativen HTX. |
| [safe/haproxy-htx.cfg](safe/haproxy-htx.cfg) | Host-Konfiguration | Native HTTP/1.1-P1--P4-Safe-Referenz. |
| [strict/haproxy-htx.cfg](strict/haproxy-htx.cfg) | Host-Konfiguration | Parser-unterstützte Strict-Policy-Grenze des nativen HTX. |
| [all/haproxy-htx.cfg](all/haproxy-htx.cfg) | Host-Konfiguration | Umfassendes natives HTX-Layout mit allen sichtbaren quellenbasierten Filtereinstellungen. |
| [spoe-spop/minimal/](spoe-spop/minimal/) | Logisches Bundle | SPOE/SPOP P1/P2 plus nativer HTX-Companion P3/P4, minimal. |
| [spoe-spop/safe/](spoe-spop/safe/) | Logisches Bundle | SPOE/SPOP P1/P2 plus nativer HTX-Companion P3/P4, Safe. |
| [spoe-spop/strict/](spoe-spop/strict/) | Logisches Bundle | SPOE/SPOP P1/P2 plus nativer HTX-Companion P3/P4, Strict-Grenze. |
| [spoe-spop/all/](spoe-spop/all/) | Logisches Bundle | Vollständiges SPOE/SPOP-P1/P2- und privates natives-HTX-P3/P4-Companion-Layout. |
| [detection-only/haproxy-htx.cfg](detection-only/haproxy-htx.cfg) | Host-Konfiguration | Nativer Connector mit DetectionOnly-Regeln; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/haproxy-htx.cfg](disabled/haproxy-htx.cfg) | Host-Konfiguration | Nativer Filter fehlt; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | Quelle und IDs der kanonischen No-CRS-Rules-Datei. |
| [P1--P4-Semantik und Topologie](#p1-p4-semantik-und-topologie) | Dokumentation | Gemeinsame Phasenbedeutung und logische Zusammensetzung. |
| [SPOE/SPOP-Response-Companion-Lösung](#spoespop-response-companion-lösung) | Logische Lösung | Aktuelle responsefähige SPOE/SPOP-Bundles. |
| [SPOE/SPOP-Kompatibilitätsmaterial](#spoespop-kompatibilitätsmaterial) | Kompatibilität | Historische Request/Header-Beispiele, kein P3/P4-Nachweis. |

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
[No-CRS-Regeln](#no-crs-regeln). Die historischen SPOE-Optionen und ihre
getrennte Limits stehen im [SPOE/SPOP-Kompatibilitätsmaterial](#spoespop-kompatibilitätsmaterial).

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

## Profile

### DetectionOnly-Profil

`detection-only/haproxy-htx.cfg` lässt den nativen HTX-Filter aktiv und wählt
die DetectionOnly-Regeldatei. DetectionOnly lädt und bewertet Engine-Regeln und
zeichnet Treffer auf, führt aber keine disruptiven Engine-Aktionen aus.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/haproxy-htx.cfg` lässt `filter modsecurity-htx` weg; SPOE wird nicht
ersetzt. Dies unterscheidet sich von `SecRuleEngine Off`, das bei aktivem
Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Semantik und Topologie

Die native HTX-Safe-Referenz wählt phase4-mode safe. Sie ist für den
gepatchten nativen Filterpfad gedacht, nicht für den SPOE/SPOP-
Kompatibilitätsservice. Eine P4-Entscheidung nach dem Beginn einer Response
wird als Safe-Log-only aufgezeichnet; die Konfiguration verspricht keinen
Statuswechsel und keinen Strict-Abbruch.

Die Minimal-Referenz zeigt den parser-unterstützten minimal-Modus; die
Strict-Referenz wählt `phase4-mode strict`. Strict ist eine Policy-Anforderung
an der Hostgrenze. Der aktuelle Quellcode zeichnet sie als `not_attempted` auf,
wenn ein Abbruch nach dem Commit nicht sicher möglich ist. Kein Bundle
verspricht einen client-sichtbaren späten Abbruch.

| Phase | Nativer HTX | Logische SPOE/SPOP-Lösung |
| --- | --- | --- |
| P1 | HTX-Request-Header -> Engine | HAProxy-SPOE-Request-Nachricht -> SPOP-Agent |
| P2 | Begrenzter HTX-Request-Body + EOS -> Engine | Begrenztes gepuffertes `req.body`-SPOE-Argument + SPOP-Agent |
| P3 | HTX-Response-Header -> Engine | Nativer HTX-Response-Companion beansprucht den opaken MRC1-Handle über private UDS |
| P4 | Begrenzte HTX-Response-Chunks + EOS -> Engine | Nativer HTX-Response-Companion leitet begrenzte Chunks und genau ein EOS weiter |

## SPOE/SPOP-Response-Companion-Lösung

Jedes Bundle enthält `haproxy.cfg`, `spoe.cfg` und `spoa-agent.conf`. Die drei
Varianten unterscheiden sich nur in der gewählten P4-Policy sowie privaten
Socket-/Logpfaden. Alle anwendbaren Begrenzungsparameter sind sichtbar:

| Parameter | Eingecheckter Wert | Grenze |
| --- | ---: | --- |
| `tune.bufsize` / `max-frame-size` | 65536 / 65532 | HAProxy- und SPOE-Request-Grenzen |
| `request-body-limit` / `response-body-limit` | 65532 / 65532 | Request- und MRC1-Response-Grenzen |
| `response-body-timeout` / `spoe-timeout` | 2000 / 2000 ms | Companion- und Agent-Timeout |
| `max-transactions` / `worker-count` | 64 / 8 | Begrenzter State, deterministische Ownership und Peer-Isolation |
| `response-companion-uid/gid` | 1000 / 1000 | Muss zur Agent-Identität passen |

`response-companion=native-htx`, private UDS, passende UID/GID, ein Wert
ungleich null für `response-body-limit`, EOS und Timeout sind verpflichtende
Startbedingungen. Fehlende Korrelation oder Companion-Fehler werden
fail-closed behandelt und bereinigt; kein nativer Transaktionszeiger geht über
die UDS. Der private UDS-Pfad ist ein Beispiel und muss gemeinsam mit der
Service-Identität geändert werden.

## No-CRS-Regeln

Die nativen HTX-Referenzen verwenden eine installierte Kopie der
repository-eigenen [No-CRS-Baseline-Regeln](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Der rules-file-Wert im HAProxy-Filter ist ein Host-Installationspfad, kein
relativer Pfad zum HAProxy-Prozess.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

## SPOE/SPOP-Kompatibilitätsmaterial

Die folgenden bewahrten Dateien sind historische Kompatibilitätsreferenzen.
Sie sind nicht die P1--P4-Lösung; für einen responsefähigen logischen
Connector die [Response-Companion-Bundles](#spoespop-response-companion-lösung)
verwenden.

| Datei | Geltungsbereich |
| --- | --- |
| [haproxy-request-only.cfg](compatibility-spoe/haproxy-request-only.cfg) | Request-SPOE-Gruppe für P1/P2-artige Request-Entscheidungen. |
| [haproxy-response-headers.cfg](compatibility-spoe/haproxy-response-headers.cfg) | Ergänzt Response-Header-SPOE; keine Response-Body-Verarbeitung. |
| [spoe-modsecurity.conf](compatibility-spoe/spoe-modsecurity.conf) | Mapping für SPOE-Agent, Gruppen, Nachrichten und Rückgabevariablen. |
| [modsecurity-agent.conf](compatibility-spoe/modsecurity-agent.conf) | Einstellungen des SPOA-Prozesses. |
| [legacy-phase4-strict-abort.cfg](compatibility-spoe/legacy-phase4-strict-abort.cfg) | Deaktiviertes historisches Beispiel; nie als P4-Evidence verwenden. |

### Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- |
| filter spoe engine modsecurity config | HAProxy-SPOE-Filter und lesbare Agent-Datei | Pflicht; Host-Konfiguration; Frontend-Scope | /etc/haproxy/spoe-modsecurity.conf. Wählt Kompatibilitäts-SPOE, nicht natives HTX. |
| send-spoe-group | Request- oder Response-Header-SPOE-Nachrichtengruppe | Für passende Datei Pflicht; Host-Konfiguration; Request-/Response-Scope | request-check oder response-check. response-check sendet keinen Response-Body. |
| be_spoa_modsecurity | SPOP-Backendname und Endpunkt | Pflicht; Host-Konfiguration; Backend-Scope | 127.0.0.1:12345. Muss zum listen-Wert des Agenten passen. |
| groups und register-var-names | SPOE-Gruppennamen und Rückgabe-Transaction-Variablen | Pflicht; spoe-modsecurity.conf; Agent-Scope | request-check response-check und blocked/action/status-Felder. Namen müssen zu HAProxy-Enforcement-Ausdrücken passen. |
| max-frame-size | Positives SPOE-Frame-Byte-Limit | Pflicht; spoe-modsecurity.conf; Agent-Scope | 65532. Begrenzt einen Frame, schafft keine P4-Body-Unterstützung. |
| rules-file | Lesbare Agent-Regeldatei | Pflicht; modsecurity-agent.conf; SPOA-Scope | /etc/modsecurity/haproxy-rules.conf. Ein geprüftes Ruleset kann Traffic blockieren. |
| decision-log, audit-log, log-file | Beschreibbare Prozesslogpfade | decision-log Pflicht, andere optional; SPOA-Scope | /var/log/haproxy-modsecurity. Metadaten schützen und keine Secrets loggen. |
| response-body-limit und response-body-timeout | Kompatibilitäts-Response-Body-Controls | Explizit deaktiviert; SPOA-Scope | 0 und 0. Nicht als P4-Unterstützung darstellen. |

SPOP-Adresse 127.0.0.1:12345, HAProxy-Listener 127.0.0.1:8080, Upstream
127.0.0.1:8081 und /etc- oder /var/log-Pfade sind Hostbeispiele, keine
repository-relativen Pfade.

Dieser Pfad darf nicht verwendet werden, um natives HTX-Verhalten,
P4-Response-Body-Verarbeitung, Safe-Late-Verhalten, Strict-Abbruch, First Byte
vor EOS oder No-Full-Response-Buffer zu behaupten.

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

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Der native HTX-Parser akzeptiert `phase4-mode strict`; die eingecheckten
nativen und SPOE/SPOP-Bundles wählen ihn. Der aktuelle Hostpfad zeichnet den
gewünschten Abbruch als `not_attempted` auf, wenn Response-Bytes bereits
committed sind. Das ist keine Abbruchgarantie.

Das optionale Argument am nativen Filter setzen, mit `haproxy -c -f <config>`
validieren und es ohne neue Host-Evidenz nicht als client-sichtbaren Abbruch
darstellen.

## Verwandtes Material

- [HAProxy-Connector-Quellcode und native HTX-Grenze](../../connectors/haproxy/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
