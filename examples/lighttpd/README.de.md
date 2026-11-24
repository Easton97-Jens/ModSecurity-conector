# lighttpd-Beispiele

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Stock verwendet den Repository-Sidecar für den vollständigen Austausch zwischen
Client und privatem Backend. Patched verwendet `mod_msconnector` mit dem
passenden Framework-synchronisierten gepatchten lighttpd-Host. Beide liefern
P1--P4-Eingaben über ihre jeweilige Integration.

## Profile

### Logische Lösungsbündel

| Lösung | Off | Safe | Strict | All | Hostvoraussetzungen |
| --- | --- | --- | --- | --- | --- |
| Stock | [Bündel](stock/off/) | [Bündel](stock/safe/) | [Bündel](stock/strict/) | [Bündel](stock/all/) | Nativer Sidecar, privates Backend, Runtime-Datei und `stock-sidecar.args`. |
| Patched | [Bündel](patched/off/) | [Bündel](patched/safe/) | [Bündel](patched/strict/) | [Bündel](patched/all/) | Passendes gepatchtes Host-/Modulpaar, Hostkonfiguration und Runtime-Datei. |

Die Stock-Beispiele lauschen an `127.0.0.1:8080` und leiten zum privaten Backend
an `127.0.0.1:8081` weiter. Patched-Beispiele wählen
`msconnector.request-body-gate = "pre-upstream"` und prüfen Identity-HTTP/1.1-
Entities über `mod_proxy`. Ihr Umfang schließt komprimierte, HTTP/2-, HTTP/3-,
File- und Zero-Copy-Responses aus.

### P1-P4-Vertrag

P1/P2 sind Request-Header/-Body und P3/P4 Response-Header/-Body. Common Runtime
wählt die Entscheidung, und der Adapter führt die unterstützte Hostaktion aus.

### DetectionOnly-Profil

Die ältere [DetectionOnly-Runtime-Datei](detection-only/msconnector-runtime.conf)
ist ein natives Kompatibilitätsbeispiel. Ihre [DetectionOnly-Regeln](rules/detection-only.conf)
bewerten und protokollieren Treffer bei deaktivierten disruptiven Engine-Aktionen.
Für die vollständige Topologie die Stock- oder Patched-Bündel oben verwenden.

### Deaktiviertes Profil

[disabled/lighttpd.conf](disabled/lighttpd.conf) setzt
`msconnector.enabled = "disable"` und benötigt keine Runtime-Datei. Die
[Engine-Off-Regeln](rules/engine-off.conf) lassen den Connector bei deaktivierter
Engine-Regelauswertung aktiv.

## Anzupassende Werte

Modul-ABI und Installationspfade, Document Root, Logs, PID-/Upload-Pfade,
Listener, Upstreams, Runtime-Dateien und geprüfte Regelpfade anpassen.
Runtime- und Ereignisverzeichnisse mit passenden Service-Berechtigungen anlegen.
Eine Regelquelle aktivieren und transaktionsspezifische IDs verwenden.
Event-JSONL auf Metadaten begrenzen.

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md) beschreibt
Host-Direktiven, Common-Runtime-Felder und Kompatibilitätskonfiguration.
Vom gewählten Host unterstützte Body-Modi wählen. Body-Inspektionslimits und
Aktionen mit [Konfiguration](../../docs/configuration.de.md) in Engine-Regeln festlegen.

## P1--P4-Safe-Absicht

Safe wählt Streaming-Eingaben mit `phase4_mode=safe` und Log-only-Behandlung
von P4-Entscheidungen nach Beginn der Response-Ausgabe. `off` deaktiviert die
zusätzliche Late-Policy und bewahrt native Interventions-/Fehlerbehandlung.
`all` verwendet die bestehende Policy `strict`. Clientbeobachtbares Verhalten
in einem passenden Hostlauf validieren.

## No-CRS-Regeln

Eine geprüfte Regeldatei installieren und in der Runtime-Konfiguration wählen.
Die [No-CRS-Baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
ist die Quelle des Repository-Testprofils. Phasen-IDs und Engine-Modi erläutern
die [Beispielübersicht](../README.de.md) und [Regelbeispiele](../common/rule-examples.de.md).

## Sidecar-Kompatibilität

Das ältere [Host-only-Proxybeispiel](compatibility-sidecar/lighttpd-sidecar-proxy.conf)
zeigt Routing zu einem betreiberseitigen Sidecar. Listener, Backend, Modul- und
Logpfade anpassen. Für Connector-Lifecycle-Konfiguration ein vollständiges
Stock- oder Patched-Bündel oben wählen.

## Stock-Service-Einrichtung

Der Launcher liest feste `stock-sidecar.args`-Dateien und startet die installierte
native Komponente unter `/usr/libexec/msconnector/lighttpd-stock-sidecar`.
Die Dateien liefern `--config`, `--listen`, `--upstream` und `--timeout-ms`.
Beide Endpunkte müssen literale Loopback-Adressen sein. Nach Installation der
Komponente und Anpassung der Regel-/Ereignispfade als Service-UID aus dem
Repository-Root starten.

~~~sh
python3 connectors/lighttpd/launch_stock_sidecar.py --profile safe
~~~

Akzeptierte Profile sind `all`, `off`, `safe` und `strict`. `--install-root`
verlagert die festen Komponenten-, absoluten Konfigurations- und Spoolpfade für
gestufte Installationen. Externe Builds am festen Komponentenpfad bereitstellen.
Der Launcher prüft Eigentümer, Berechtigungen und nativen Artefakttyp und führt
das Programm über einen festgehaltenen Deskriptor aus.

Spoolverzeichnisse unter `/var/lib/msconnector/lighttpd-stock/{all,off,safe,strict}`
müssen der effektiven UID gehören und Modus 0700 haben. Der Launcher erstellt
fehlende Kinder bei vorhandenen Schreibrechten seiner UID und weist unsichere
bestehende Pfade ab. Ein Administrator kann Vorfahren und ausgewähltes
Profilverzeichnis mit tatsächlicher Service-UID/-GID bereitstellen.
Die Befehle beschreiben die Erstbereitstellung.

~~~sh
install -d -o root -g root -m 0755 /var/lib/msconnector /var/lib/msconnector/lighttpd-stock
install -d -o SERVICE_UID -g SERVICE_GID -m 0700 /var/lib/msconnector/lighttpd-stock/safe
~~~

Konfigurationsvorfahren wie `/etc/lighttpd` dürfen Modus 0755 behalten.
Spool-Zulassung verwendet standardmäßig `--spool-capacity-bytes` 268435456
(256 MiB) für die Summe offener Reservierungen und `--spool-free-reserve-bytes`
67108864 (64 MiB) für verfügbaren freien Speicher. Nach P1-Allow allokiert der
Service die deklarierte Request-Länge mit `posix_fallocate` und prüft freien
Speicher vor der Body-Inspektion erneut. Allokationsfehler liefern 503 mit einem
Connector-Ressourcenfehler. Reservierungen bestehen bis zum Deskriptorschluss,
und eine Verzeichnissperre verhindert parallele Sidecars mit demselben Spool.
Synchrone Allokation kann Deadline-Prüfungen überdauern.

## Validierung

Für Patched das passende Host-/Modulpaar installieren, die Konfiguration
anpassen und die installierte Hostdatei prüfen. Für Stock private
Backend-Konfiguration und die Sidecar-Einrichtung oben prüfen.
Der folgende Pfad ist ein Installationsbeispiel.

~~~sh
lighttpd -tt -f /etc/lighttpd/lighttpd.conf
~~~

Dies prüft Syntax und lesbare Eingaben. Die [Testanleitung](../../docs/testing-and-evidence.de.md)
beschreibt Runtime-Validierung.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Common Runtime lässt `phase4_mode=strict` für Stock zu, dessen Sidecar-Profil
einen getesteten Socket-Shutdown nach dem Commit besitzt. Patched weist den
Wert beim Start ab, weil seine erforderliche Hostaktion unbewiesen ist.
Die Strict- und `all`-Bündel zeigen das jeweilige Zulassungsverhalten.

## Verwandtes Material

- [lighttpd-Connector-Anleitung](../../connectors/lighttpd/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
