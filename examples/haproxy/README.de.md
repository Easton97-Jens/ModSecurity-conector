# HAProxy-Beispiele

**Sprache:** [English](README.md) | Deutsch

Nativer HTX oder SPOE/SPOP mit nativem HTX-Response-Companion stehen zur Wahl.
Beide benötigen den gepatchten HAProxy-Filterparser. Diese Referenzen decken
HTTP/1.1 ab.

## Dateien

| Layout | Nativer HTX | SPOE/SPOP mit Response-Companion |
| --- | --- | --- |
| `off` | [haproxy-htx.cfg](off/haproxy-htx.cfg) | [Bundle](spoe-spop/off/) |
| `safe` | [haproxy-htx.cfg](safe/haproxy-htx.cfg) | [Bundle](spoe-spop/safe/) |
| `strict` | [haproxy-htx.cfg](strict/haproxy-htx.cfg) | [Bundle](spoe-spop/strict/) |
| `all` | [haproxy-htx.cfg](all/haproxy-htx.cfg) | [Bundle](spoe-spop/all/) |

`off` bewahrt die native Interventionsbehandlung. `all` zeigt die vollständige
Konfiguration und wählt den zulässigen Wert `phase4-mode strict`.

## Anzupassende Werte

`rules-file`, Listener, Upstream und Connect-/Client-/Server-Timeouts für die
Installation setzen. Die Referenzen verwenden `127.0.0.1:8080`,
`127.0.0.1:8081` und `/etc/modsecurity/no-crs-baseline.conf`. Body-Zugriff,
Inspektionslimits und Limitaktionen gehören in Engine-Regeln. Syntax,
Defaults und routenspezifische Einstellungen stehen in der generierten
[Konfigurationsreferenz](configuration-reference.de.md).

## Profile

### DetectionOnly-Profil

[detection-only/haproxy-htx.cfg](detection-only/haproxy-htx.cfg) hält den Filter
aktiv und verwendet [DetectionOnly-Regeln](rules/detection-only.conf). Diese
werten Treffer aus und protokollieren sie, unterdrücken dabei disruptive
Engine-Aktionen.

### Deaktiviertes Profil

[disabled/haproxy-htx.cfg](disabled/haproxy-htx.cfg) lässt den nativen Filter weg.
Bei aktivem Filter deaktiviert [rules/engine-off.conf](rules/engine-off.conf)
die Engine-Auswertung über `SecRuleEngine Off`.

## P1--P4-Semantik und Topologie

| Phase | Nativer HTX | SPOE/SPOP-Lösung |
| --- | --- | --- |
| P1 | Request-Header an Engine | SPOE-Request-Nachricht an SPOP-Agent |
| P2 | Request-Body und EOS an Engine | Begrenzt gepuffertes `req.body` an Agent |
| P3 | Response-Header an Engine | HTX-Companion beansprucht opaken MRC1-Handle über private UDS |
| P4 | Response-Chunks und EOS an Engine | HTX-Companion sendet begrenzte Chunks und genau ein EOS |

Safe zeichnet eine späte P4-Entscheidung nach Response-Ausgabebeginn als
log-only auf. Die SPOE-Request-Route behält ihre Host-Buffering- und Frame-Limits.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Der Parser akzeptiert `phase4-mode strict`. Der aktuelle Hostpfad zeichnet
eine Post-Commit-Abbruchanforderung als `not_attempted` auf, wenn der Abbruch
nicht sicher ausführbar ist. Client-sichtbares Verhalten für den gewählten
Host und das Profil validieren.

## SPOE/SPOP-Response-Companion-Lösung

Jedes Bundle enthält `haproxy.cfg`, `spoe.cfg` und `spoa-agent.conf`. Private
Socket- und Logpfade gemeinsam mit der Prozessidentität anpassen.

| Parameter | Referenzwert |
| --- | --- |
| `tune.bufsize` / `max-frame-size` | 65536 / 65532 |
| `response-body-timeout` / `spoe-timeout` | 2000 / 2000 ms |
| `max-transactions` / `worker-count` | 64 / 8 |
| `response-companion-uid/gid` | 1000 / 1000, passend zur Agent-Identität |

`response-companion=native-htx`, private UDS, passende UID/GID, begrenzte Frames,
EOS und Timeouts sind verpflichtende Startbedingungen. Korrelations- oder
Companion-Fehler werden fail-closed mit Cleanup behandelt. Nur opake Handles
überqueren die UDS.

## No-CRS-Regeln

Eine geprüfte Kopie der [No-CRS-Baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
am konfigurierten Regelpfad installieren. IDs `1100001`, `1100101`, `1100201`
und `1100301` entsprechen P1, P2, P3 und P4. Siehe den
[gemeinsamen Regel-Leitfaden](../common/rule-examples.de.md).

## SPOE/SPOP-Kompatibilitätsmaterial

Die historischen Illustrationen für [Request-only](compatibility-spoe/haproxy-request-only.cfg)
und [Response-Header](compatibility-spoe/haproxy-response-headers.cfg) verwenden
[SPOE-Mapping](compatibility-spoe/spoe-modsecurity.conf) und
[SPOA-Prozesseinstellungen](compatibility-spoe/modsecurity-agent.conf).
Response-Body-Controls sind mit `response-body-timeout=0` deaktiviert.
Das [historische Strict-Abbruchbeispiel](compatibility-spoe/legacy-phase4-strict-abort.cfg)
ist deaktiviert. Für P3/P4-Body-Verarbeitung die obigen Response-Companion-Bundles
verwenden.

In Kompatibilitätsdateien SPOP-Backend mit Agent-`listen`, Gruppen- und
Rückgabevariablennamen mit Enforcement-Ausdrücken sowie alle Regel-/Logpfade
abgleichen. Der beispielhafte SPOP-Endpunkt ist `127.0.0.1:12345`. Frame-Limits
erhalten und Metadatenlogs schützen. Detaillierte Felder stehen in der
Konfigurationsreferenz.

## Validierung

Nach Anpassung der gewählten Dateien den installierten gepatchten Hostchecker
verwenden.

~~~sh
haproxy -c -f /etc/haproxy/haproxy.cfg
~~~

Den tatsächlichen installierten Konfigurationspfad wählen. Runtime-Enforcement
benötigt profilspezifische Traffic-Evidenz. Siehe den
[HAProxy-Connector-Leitfaden](../../connectors/haproxy/README.de.md) und
[Beispielindex](../README.de.md).
