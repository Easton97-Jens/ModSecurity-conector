# Traefik-Beispiele

**Sprache:** [English](README.md) | Deutsch

## Integration und Grenze

Das native Profil verwendet das repository-eigene Local Plugin und einen
persistenten privaten Unix-Domain-Socket-Engine-Service. Das forwardAuth-Profil
kombiniert Request-Autorisierung mit einem privaten Response-Observer.

## Vollständige Matrix der logischen Lösungen

| Lösung | Off | Safe | Strict | All | Phaseneingabe |
| --- | --- | --- | --- | --- | --- |
| Native UDS | [Bündel](native-uds/off/) | [Bündel](native-uds/safe/) | [Bündel](native-uds/strict/) | [Bündel](native-uds/all/) | `modsecurityNative` streamt P1--P4 in einer Transaktion. |
| forwardAuth + Observer | [Bündel](forwardauth/off/) | [Bündel](forwardauth/safe/) | [Bündel](forwardauth/strict/) | [Bündel](forwardauth/all/) | forwardAuth liefert P1/P2, `modsecurityResponseObserver` liefert P3/P4. |

Auf die forwardAuth-Middleware muss unmittelbar der private UDS-Observer folgen.
Request-Bodies werden begrenzt gepuffert mit `forwardBody: true` und
`maxBodySize: 4096`. Der Observer beansprucht das undurchsichtige
Transaktionshandle. Fehlende Handles und Observer-Timeouts werden fail-closed
behandelt und bereinigen die Transaktion.

## Dateien

Die eigenständige [statische Off-Datei](off/traefik-static.yaml),
[dynamische Datei](off/traefik-dynamic.yaml) und
[Engine-Datei](off/traefik-engine-service.conf) zeigen Local-Plugin-Registrierung,
File-Provider-Anbindung und UDS-Service-Konfiguration. Die [dynamische Safe-Datei](safe/traefik-dynamic.yaml)
und [Engine-Datei](safe/traefik-engine-service.conf) wählen gestreamte Bodies
und `phase4_mode=safe`.

### DetectionOnly-Profil

[detection-only/traefik-engine-service.conf](detection-only/traefik-engine-service.conf)
wählt [DetectionOnly-Regeln](rules/detection-only.conf) mit der UDS-Middleware.
Treffer werden bei deaktivierten disruptiven Engine-Aktionen bewertet und protokolliert.

### Deaktiviertes Profil

[disabled/traefik-engine-service.conf](disabled/traefik-engine-service.conf)
setzt `enabled=off`. [Engine-Off-Regeln](rules/engine-off.conf) lassen den
Connector bei deaktivierter Engine-Regelauswertung aktiv.

## Anzupassende Werte

- Den passenden Quelltext von `github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware`
  im installierten Traefik-Local-Plugin-Workspace bereitstellen.
- `entryPoints.web.address`, Router-Regeln, Upstream-URL und
  `providers.file.filename` anpassen. Relative File-Provider-Pfade beziehen
  sich auf das Traefik-Arbeitsverzeichnis.
- `engineMode: uds` und einen privaten `engineSocketPath` wie
  `/run/traefik-msconnector/engine.sock` setzen. Das Elternverzeichnis schützen
  und dem vertrauenswürdigen Service zuordnen. Legacy-`passthrough` wird abgewiesen.
- Geprüfte Regeln installieren und `rules_file`, Ereignisziele sowie
  Berechtigungen anpassen. Eine Regelquelle aktivieren und transaktionsspezifische
  IDs verwenden. Event-JSONL enthält ausschließlich Metadaten.

Der native Service verwendet eine monotone Deadline pro vollständigem Frame.
Seine CLI-Option `--max-workers N` begrenzt Worker auf standardmäßig 64 und
höchstens 256. Beim Herunterfahren signalisiert er aktive Sockets und wartet
vor der Finalisierung auf die Worker.

## Konfigurationsreferenz

Die generierte [Konfigurationsreferenz](configuration-reference.de.md) beschreibt
statisches/dynamisches YAML, Plugin-Defaults, Common-Runtime-Felder sowie
Header-/Chunk-/Inaktivitätskontrollen. Body-Inspektionslimits und Aktionen gehören
in Engine-Regeln. Siehe [Konfiguration](../../docs/configuration.de.md).

## P1--P4-Safe-Absicht

Die native HTTP/1.1-Referenz verwendet Streaming-Body-Modi und Safe-Log-only
für P4-Entscheidungen nach dem Response-Commit. `phase4_mode=off` deaktiviert
die zusätzliche Late-Policy und bewahrt native Behandlung. `all` wählt den
bestehenden Wert `strict`. Clientbeobachtbares Verhalten benötigt einen passenden Hostlauf.

## No-CRS-Regeln

Die geprüfte [No-CRS-Baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
installieren und im Engine-Service wählen. Phasen-IDs und Engine-Modi erläutern
die [Beispielübersicht](../README.de.md) und [Regelbeispiele](../common/rule-examples.de.md).

## forwardAuth-Kompatibilität

Die älteren [dynamischen](compatibility-forwardauth/traefik-dynamic.yaml) und
[statischen](compatibility-forwardauth/traefik-static.yaml) Dateien zeigen
Request-Autorisierung. Beide Dateien gemeinsam anpassen, einschließlich
File-Provider-Pfad, Listener, Router, vertrauenswürdiger Authorization-URL und
Application-Upstream. Credentials aus URLs heraushalten. Eine Änderung von
`trustForwardHeader: false` benötigt eine ausdrückliche Vertrauensregel für
Proxy-Header. Für Response-Prüfung die vollständigen `forwardauth/`-Bündel oben wählen.

## Validierung

Die ausgewählten statischen/dynamischen Dateien an die File-Provider-Orte
kopieren, Pfade und Endpunkte anpassen und die installierte statische
Konfiguration prüfen. `/etc/traefik/traefik.yaml` ist ein Installationsbeispiel.

~~~sh
traefik check --configFile=/etc/traefik/traefik.yaml
~~~

Plugin-Laden, privaten Engine-Socket und Service-Zugriff auf die Regeldatei
prüfen. Ein Konfigurationscheck belegt das Laden. Die [Testanleitung](../../docs/testing-and-evidence.de.md)
beschreibt Runtime-Validierung.

## Strict-Profilgrenze <a id="strict-profilgrenze"></a>

Common Runtime weist `phase4_mode=strict` für beide Profile beim Start ab, weil
die erforderliche `strict_post_commit_action` unbewiesen ist. Die Strict- und
`all`-Bündel zeigen diese Zulassungsgrenze. Off und Safe sind zur Laufzeit zulässig.

## Verwandtes Material

- [Traefik-Connector-Anleitung](../../connectors/traefik/README.de.md)
- [Repository-Beispielübersicht](../README.de.md)
