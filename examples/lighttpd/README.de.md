# lighttpd-Beispiele für das native Modul

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Es gibt zwei logische Lösungen. [Stock](stock/) ist der traffic-owning
Repository-Sidecar und führt den vollständigen Client-zu-privatem-Backend-
Austausch für P1--P4 aus. [Patched](patched/) ist das native
`mod_msconnector`-Modul mit dem Framework-synchronisierten gepatchten
lighttpd-Host und seinen HTTP/1.1-Identity-Entity-Hooks.

Die Safe-Referenz konfiguriert die P1--P4-Form mit phase4_mode safe. P1 sind
Request-Header, P2 Request-Body, P3 Response-Header und P4 Response-Body. Sie
behauptet weder clientbeobachtetes P4-Verhalten noch vollständiges
Response-Buffering, HTTP/2, HTTP/3, Kompression, File-/Zero-Copy-Verarbeitung
oder Strict-Abbruch. Die [Strict-Profilgrenze](#strict-profilgrenze)
dokumentiert die optionale Grenze ohne implementierten Host-Abbruch.

Der Stock-Sidecar erhält `--config`, `--listen`, `--upstream` und
`--timeout-ms` als Kommandozeilenargumente. `stock-sidecar.args` sind lesbare
ARGV-Aufzeichnungen und kein zweiter Konfigurationsparser. Beide Endpunkte
sind literale Loopback-Adressen; der Sidecar besitzt Cleanup und benötigt
keine prozessübergreifende Transaktionsregistry.

## Dateien

| Pfad | Typ | Zweck |
| --- | --- | --- |
| [stock/](stock/) | Stock-Lösung | `minimal`, `safe`, `strict` und `all`; Sidecar-ARGV, privates Backend und vollständige Runtime-Dateien. |
| [patched/](patched/) | Patched-Lösung | `minimal`, `safe`, `strict` und `all`; nativer Host und vollständige Runtime-Dateien. |
| [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Runtime-Konfiguration | Stock-Body-Modi mit DetectionOnly-Regeln; siehe [DetectionOnly-Profil](#detectiononly-profil). |
| [disabled/lighttpd.conf](disabled/lighttpd.conf) | Host-Konfiguration | Natives Plugin deaktiviert; siehe [Deaktiviertes Profil](#deaktiviertes-profil). |
| [rules/detection-only.conf](rules/detection-only.conf) | Regeln | DetectionOnly-Engine-Einstellungen. |
| [rules/engine-off.conf](rules/engine-off.conf) | Regeln | Engine-Off-Einstellungen, getrennt vom Deaktivieren des Connectors. |
| [No-CRS-Regeln](#no-crs-regeln) | Dokumentation | No-CRS-Quelle und Phasen-IDs. |
| [P1--P4-Safe-Absicht](#p1-p4-safe-absicht) | Dokumentation | Konfigurationsabsicht, keine Run-Evidence. |
| [P1--P4-Vertrag](#p1-p4-vertrag) | Architektur | Gleiche Phasenbedeutung für beide logischen Lösungen. |

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
| request_body_mode und response_body_mode | none, buffered oder streaming gemäß Hostfähigkeit | Pflicht; Runtime-Konfiguration; Engine-Scope | streaming für den Stock-Sidecar und den passenden Patched-Host; nie auf einem ungepatchten nativen Stock-Modul aktivieren. |
| request_body_limit, response_body_limit, body_limit_action | Positive Byte-Limits und reject- oder process_partial-Policy | Bei aktivierten Bodies Pflicht; Runtime-Konfiguration; Engine-Scope | 1048576 und reject. Grenzen bedeuten kein vollständiges Connector-Buffering. |
| phase4_mode | P4-Policy: minimal, safe oder strict | In diesen Runtime-Dateien Pflicht; Runtime-Konfiguration; Engine-Scope | safe für gepatchtes Safe; all wählt strict. Beweist weder Statuswechsel noch Abbruch. |
| server.stream-response-body und proxy.server | Gepatchte Delivery-Einstellung und lokale Upstream-Route | In Patched-Bündeln Pflicht; Host-Konfiguration; Server-Scope | 1 und 127.0.0.1:8081. Nur Identity-HTTP/1.1; kein gzip/br- oder HTTP/2-Verhalten ableiten. |
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

## Profile

### Logische Lösungsbündel

Jedes Bündel enthält die Topologie-Artefakte, die Common-Runtime-`key=value`-
Datei und für Stock die Sidecar-ARGV-Aufzeichnung. Jede Runtime-Datei nutzt
dieselben begrenzten Header-/Body-/Event-Limits und zeigt quellenvalide
inaktive Regelquellen- und Transaktions-ID-Alternativen als Kommentare. Nie
mehr als eine Regelquelle aktivieren und die statische Transaktions-ID nicht
produktiv verwenden.

| Lösung | Varianten | P1/P2/P3/P4-Besitzer |
| --- | --- | --- |
| Stock | `stock/{minimal,safe,strict,all}/` | `stock-lighttpd-sidecar`; begrenzt gestreamte Request- und Response-Bodies. |
| Patched | `patched/{minimal,safe,strict,all}/` | `mod_msconnector`-Hooks; Pre-upstream-Request-Gate und Identity-HTTP/1.1-Response-Scope. |

Stock-Backends binden nur an `127.0.0.1:8081`; der Sidecar lauscht an
`127.0.0.1:8080` und leitet nur an dieses private Backend weiter. Patched-
Konfigurationen setzen ausdrücklich `msconnector.request-body-gate = "pre-upstream"`.

### P1-P4-Vertrag

P1 bedeutet Request-Header, P2 Request-Body, P3 Response-Header und P4
Response-Body. Allow, Block, Redirect, Rate-Limit/Hostaktion, Safe/log-only,
Strict/Enforce, Timeout, nicht erreichbare Engine, ungültige Engineantwort,
Connector-/Protokollfehler, Client-Cancel, Upstream-Disconnect und Cleanup
sind gemeinsame Common-Runtime-Entscheidungskategorien. Der Hostadapter
übersetzt nur die resultierende Aktion. Strict nach Response-Commit verspricht
keinen Abbruch.

### DetectionOnly-Profil

`detection-only/msconnector-runtime.conf` ist ein altes natives
Kompatibilitätsprofil. Die kanonischen Stock- und Patched-Lösungen sind die
sechs obigen Variantenbündel, die jeweils P1--P4 abdecken.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Dieses Profil ist Konfigurationsanleitung und
keine Runtime-Evidenz.

### Deaktiviertes Profil

`disabled/lighttpd.conf` setzt `msconnector.enabled = "disable"`; keine
Runtime-Datei ist nötig. Dies unterscheidet sich von `SecRuleEngine Off`, das
bei aktivem Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

Nach dem Anpassen der Hostpfade den untenstehenden Connector-
Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1--P4-Verhalten ableiten.

## P1--P4-Safe-Absicht

Die Patched-Safe-Referenz ist auf den passenden gepatchten nativen
Framework-synchronisierten lighttpd-Host und Identity-HTTP/1.1-Entity-Daten
über mod_proxy begrenzt. Sie wählt
gestreamte Body-Modi und phase4_mode safe. Sie aktiviert weder komprimierte
Entities noch behauptet sie HTTP/2-, HTTP/3-, File- oder Zero-Copy-
Response-Prüfung.

Eine späte P4-Entscheidung ist eine Safe-Log-only-Grenze, kein behaupteter
sichtbarer 403 oder Strict-Abbruch. Alle acht kanonischen Bündel enthalten
eine Strict-Konfiguration.

## No-CRS-Regeln

Das native Modul liest die geprüfte installierte Regeldatei, die von
msconnector.config-file benannt wird. Die Repositoryquelle für das
No-CRS-Profil ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

## Sidecar-Kompatibilität

Die bewahrte Datei ist eine alte host-only Proxyillustration. Sie ist kein
logisches Profil und ersetzt weder das traffic-owning [Stock-Bündel](stock/)
noch das native [Patched-Bündel](patched/).

### Anzupassende Werte

| Name | Zweck und Format | Pflicht/Default, Setzer, Geltungsbereich | Beispiel und Grenze |
| --- | --- | --- |
| server.modules | Installierte lighttpd-Proxy- und Logging-Module | Pflicht; Host-Konfiguration; Server-Scope | mod_accesslog und mod_proxy. Dies ist nicht mod_msconnector. |
| server.document-root und Logpfade | Host-Dateisystempfade | Pflicht; Host-Konfiguration; Server-Scope | /var/empty und relative Lognamen. Durch beschreibbare Betreiberpfade ersetzen. |
| server.port | Dezimaler TCP-Listener-Port | Pflicht; Host-Konfiguration; Server-Scope | 8080. Für lokale Übungen privaten Listener binden. |
| proxy.server-Host und -Port | Upstream-Endpunkt | Pflicht; Host-Konfiguration; Proxy-Scope | 127.0.0.1:8081. Durch gewünschtes Backend ersetzen. |
| $HTTP-Hostausdruck | lighttpd-Selektor für Request-Host-Header | In diesem Beispiel Pflicht; Host-Konfiguration; Conditional-Scope | Passt auf jeden Host. Ist eine Host-Sprachvariable, keine Shellvariable und kein Secret. |

Ein separater betreiberseitiger Sidecar liegt außerhalb der Lifecycle-Claims
der nativen Beispiele.

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

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Alle acht kanonischen Bündel enthalten sichtbare Strict-Konfigurationen. Common
Runtime lässt `phase4_mode=strict` nur für das traffic-owning Stock-Sidecar zu,
dessen Profil einen getesteten Socket-Shutdown nach Commit besitzt. Das
gepatchte native Profil wird beim Start abgewiesen, weil diese Hostaktion noch
nicht nachgewiesen ist. Keiner der Fälle behauptet ein ungetestetes
Client-Ergebnis für den gepatchten Host.

Das passende Host-/Modulpaar und die Common-Runtime-Konfiguration validieren,
bevor ein strikter Wert getestet wird; das gepatchte Profil nicht als
ausführbaren Client-Abbruch beschreiben.

## Verwandtes Material

- [lighttpd-Connector-Quellcode und gepatchte Hostgrenze](../../connectors/lighttpd/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
