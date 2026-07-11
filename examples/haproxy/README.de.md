# HAProxy ModSecurity Beispiele

**Sprache:** [English](README.md) | Deutsch

## Inhaltsverzeichnis

- [Status](#status)
- [Zweck](#zweck)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Dateien](#dateien)
- [Produktionspfade](#produktionspfade)
- [Request-Phasen 1/2](#request-phasen-12)
- [Phase 3 Response Headers](#phase-3-response-headers)
- [Phase 4 / RESPONSE_BODY Strict-Abort](#phase-4--response_body-strict-abort)
- [Variablen- und Platzhalterreferenz](#variablen--und-platzhalterreferenz)
- [Runtime-Evidence](#runtime-evidence)
- [Reload und Restart](#reload-und-restart)
- [Grenzen](#grenzen)
- [Externer Einsatz](#externer-einsatz)
- [Nicht-Claims](#nicht-claims)
- [Verwandte Dokumente](#verwandte-dokumente)

## Status

Produktionsnahe HAProxy-SPOE/SPOP-Beispiele für `haproxy-modsecurity-spoa`.
Der gewählte Pfad unterstützt Request-Phasen und Response-Header;
RESPONSE_BODY ist nicht implementiert und wird nicht als Produktionssupport
dargestellt.

## Zweck

Diese Beispiele zeigen den produktiven SPOA-Pfad für HAProxy:
`haproxy-modsecurity-spoa`, HAProxy + SPOE/SPOP + libmodsecurity,
Decision-Logging, Audit-Log-Plumbing, Request-Phasen 1/2 und implementierte
Phase-3-Response-Header. Sie bieten keinen ausgewählten
Response-Body-/Phase-4-Pfad.

## Benötigte Komponenten

HAProxy, `haproxy-modsecurity-spoa`, libmodsecurity v3, SPOE-Konfiguration,
ModSecurity-Regeln, optional CRS sowie beschreibbare HAProxy-/SPOA-/
ModSecurity-Log-Orte.

## Dateien

- `haproxy-request-only.cfg`: HAProxy-Request-Phase-Enforcement über SPOE.
- `haproxy-response-headers.cfg`: HAProxy-Request- plus Response-Header-Checks.
- `haproxy-phase4-strict-abort.cfg`: historisches deaktiviertes Sample; kein
  ausführbares Phase-4-Beispiel.
- `spoe-modsecurity.conf`: SPOE-Message- und Variablen-Mapping.
- `modsecurity-agent.conf`: Konfiguration für `haproxy-modsecurity-spoa`.

## Produktionspfade

Die Beispiele verwenden produktionsnahe Pfade:

- `/usr/local/sbin/haproxy-modsecurity-spoa`
- `/etc/haproxy/haproxy.cfg`
- `/etc/haproxy/spoe-modsecurity.conf`
- `/etc/haproxy/modsecurity-agent.conf`
- `/etc/modsecurity/haproxy-rules.conf`
- `/var/log/haproxy-modsecurity/decision.jsonl`
- `/var/log/haproxy-modsecurity/audit.log`
- `/var/log/haproxy-modsecurity/agent.log`

## Request-Phasen 1/2

`haproxy-request-only.cfg` sendet Request-Metadaten, Header und Request Body
über die Gruppe `request-check` an den SPOA-Service. HAProxy erzwingt
zurückgegebene Transaction-Variablen mit `http-request deny`, Redirect- und
Silent-Drop-Regeln.

## Phase 3 Response Headers

`haproxy-response-headers.cfg` ergänzt die Gruppe `response-check`. Sie sendet
Response-Status und ausgewählte Response Header an den SPOA-Service und
erzwingt zurückgegebene Variablen mit `http-response`-Regeln.

## Phase 4 / RESPONSE_BODY Strict-Abort

`haproxy-phase4-strict-abort.cfg` ist ein historisches deaktiviertes Artefakt.
Die ausgewählte SPOE/SPOP-Konfiguration sendet nur Response-Header; sie besitzt
keinen Response-Body-Pfad, daher ist Phase 4 / RESPONSE_BODY
`not_implemented`. Das ausgemusterte Sample darf weder verwendet noch als
aktueller Laufzeitnachweis berichtet werden.

## Variablen- und Platzhalterreferenz

| Name | Typ | Erforderlich | Beispielwert | Verwendet in | Bedeutung | Änderung erfordert Restart/Reload | Hinweise |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `haproxy-modsecurity-spoa` | Binary-Pfad | Ja | `/usr/local/sbin/haproxy-modsecurity-spoa` | Service Unit oder Process Supervisor | Produktiver SPOA/SPOP-Prozess, der libmodsecurity lädt. | SPOA neu starten | Gebaut durch `make -C connectors/haproxy build-spoa-runtime`. |
| `filter spoe engine modsecurity` | HAProxy-Direktive | Ja | `config /etc/haproxy/spoe-modsecurity.conf` | `haproxy-*.cfg` | Hängt die ModSecurity-SPOE-Engine ein. | HAProxy reloaden | Config-Pfad muss für HAProxy lesbar sein. |
| `http-request send-spoe-group` | HAProxy-Direktive | Ja | `modsecurity request-check` | Request-HAProxy-Konfigurationen | Sendet Request-Daten an den SPOA-Service. | HAProxy reloaden | Für Phasen 1/2 erforderlich. |
| `http-response send-spoe-group` | HAProxy-Direktive | Response-Modi | `modsecurity response-check` | Response-Header-HAProxy-Konfigurationen | Sendet Response-Daten an den SPOA-Service. | HAProxy reloaden | Nur für Phase 3; es wird kein Response-Body gesendet. |
| `be_spoa_modsecurity` | HAProxy-Backend | Ja | `127.0.0.1:12345` | `haproxy-*.cfg` | SPOP-Backend für den SPOA-Prozess. | HAProxy reloaden | Adresse muss zu Agent-`listen` passen. |
| `spoe-agent modsecurity-agent` | SPOE-Section | Ja | `use-backend be_spoa_modsecurity` | `spoe-modsecurity.conf` | Definiert SPOE-Agent und Backend. | HAProxy reloaden | Verwendet HAProxy `mode spop`. |
| `groups` | SPOE-Option | Ja | `request-check response-check` | `spoe-modsecurity.conf` | Deklariert verfügbare SPOE-Gruppen. | HAProxy reloaden | Request-only-Deployments können die Response-Gruppe weiterhin definiert lassen. |
| `register-var-names` | SPOE-Option | Ja | `blocked action status redirect_url rule_id phase error` | `spoe-modsecurity.conf` | Registriert von SPOA zurückgegebene Transaction-Variablen. | HAProxy reloaden | HAProxy-Enforcement-Regeln lesen diese Variablen. |
| `max-frame-size` | SPOE-Option | Ja | `65532` | `spoe-modsecurity.conf` | Begrenzt die SPOE-Frame-Größe. | HAProxy reloaden | Mit Request-/Response-Body-Limits abstimmen. |
| `request_id` | SPOE-Message-Argument | Ja | `unique-id` | `spoe-modsecurity.conf` | Korreliert Requests in Decision- und Audit-Logs. | HAProxy reloaden | `unique-id-header` stellt denselben Wert upstream bereit. |
| `headers_bin` | SPOE-Message-Argument | Request-Checks | `req.hdrs_bin` | `spoe-modsecurity.conf` | Sendet Request Header in binärer Form. | HAProxy reloaden | Wird von Request-Phasen verwendet. |
| `body` | SPOE-Message-Argument | Request-Checks | `req.body` | `spoe-modsecurity.conf` | Sendet begrenzte Request-Body-Bytes. | HAProxy reloaden | Erfordert `option http-buffer-request`. |
| `response_headers_bin` | SPOE-Message-Argument | Response-Checks | `res.hdrs_bin` | `spoe-modsecurity.conf` | Sendet Response Header in binärer Form und erhält wiederholte Werte wie `Set-Cookie`. | HAProxy reloaden | Bevorzugt für Phase-3-Response-Header-Evidence. |
| `response_headers` | SPOE-Message-Argument | Response-Checks | `res.hdrs` | `spoe-modsecurity.conf` | Sendet Response Header für Phase 3. | HAProxy reloaden | Von Response-Header-Evidence unterstützt. |
| `listen` | Agent-Config-Key | Ja | `127.0.0.1:12345` | `modsecurity-agent.conf` | Adresse, auf der `haproxy-modsecurity-spoa` lauscht. | SPOA neu starten | Muss zum HAProxy-SPOP-Backend passen. |
| `rules-file` | Agent-Config-Key | Ja | `/etc/modsecurity/haproxy-rules.conf` | `modsecurity-agent.conf` | ModSecurity-Regeln, die vom SPOA-Prozess geladen werden. | SPOA neu starten | CRS bei Bedarf aus dieser Datei einbinden. |
| `decision-log` | Agent-Config-Key | Ja | `/var/log/haproxy-modsecurity/decision.jsonl` | `modsecurity-agent.conf` | JSONL-Runtime-Decision-Log. | SPOA neu starten | Für Evidence und Debugging aufbewahren. |
| `audit-log` | Agent-Config-Key | Nein | `/var/log/haproxy-modsecurity/audit.log` | `modsecurity-agent.conf` | libmodsecurity-Audit-Log-Ausgabe. | SPOA neu starten | Schreibbare Verzeichnisberechtigungen sicherstellen. |
| `log-file` | Agent-Config-Key | Nein | `/var/log/haproxy-modsecurity/agent.log` | `modsecurity-agent.conf` | Agent-Diagnose-Log. | SPOA neu starten | Mit Systemlogs rotieren. |
| `mode` | Agent-Config-Key | Ja | `block` | `modsecurity-agent.conf` | Aktiviert disruptives Enforcement. | SPOA neu starten | Detection Mode nur verwenden, wenn er im bereitgestellten Binary implementiert ist. |
| `fail-mode` | Agent-Config-Key | Ja | `closed` | `modsecurity-agent.conf` | Verhalten bei Processing-Fehlern. | SPOA neu starten | Entsprechend der Service-Risikotoleranz wählen. |
| `request-body-limit` | Agent-Config-Key | Nein | `65532` | `modsecurity-agent.conf` | Begrenzt verarbeitete Request-Body-Bytes. | SPOA neu starten | Innerhalb der SPOE-Frame-Limits halten. |
| `response-body-limit` | Agent-Config-Key | Deaktiviert | `0` | `modsecurity-agent.conf` | Deaktiviert Response-Body-Verarbeitung. | SPOA neu starten | Es existiert kein ausgewählter Response-Body-Pfad. |
| `response-body-timeout` | Agent-Config-Key | Deaktiviert | `0` | `modsecurity-agent.conf` | Deaktiviert Response-Body-Warten. | SPOA neu starten | Es existiert kein ausgewählter Response-Body-Pfad. |
| `spoe-timeout` | Agent-Config-Key | Nein | `2000` | `modsecurity-agent.conf` | Agent-seitiger SPOE-Timeout in Millisekunden. | SPOA neu starten | Mit HAProxy-Processing-Timeout abstimmen. |
| `worker-count` | Agent-Config-Key | Nein | `1` | `modsecurity-agent.conf` | Anzahl der SPOA-Worker. | SPOA neu starten | Nach Tests für Produktionsverkehr dimensionieren. |
| `max-transactions` | Agent-Config-Key | Nein | `4096` | `modsecurity-agent.conf` | Agent-Transaction-Kapazität. | SPOA neu starten | Mit Speicher und Nebenläufigkeit abstimmen. |

## Runtime-Evidence

Lokale generierte Evidence verwendet:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime/decision.jsonl`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime/audit.log`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`

Der Default-HAProxy-Smoke berichtet `55/55 PASS`. Force-all-HAProxy-Evidence
berichtet `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED /
6 NOT_EXECUTABLE`.

## Reload und Restart

Führen Sie vor dem Reload `haproxy -c -f /etc/haproxy/haproxy.cfg` aus. Reloaden
Sie HAProxy nach Änderungen an HAProxy- oder SPOE-Konfiguration. Starten Sie den
SPOA-Service nach Änderungen an `modsecurity-agent.conf`, Regeldatei, Binary
oder Library-Pfad neu.

## Grenzen

Die Root-Zusammenfassungen sind connector-neutral. Row-Level-HAProxy-Evidence
bleibt in `reports/testing/generated/haproxy-runtime-results.generated.md`. Es
gibt keinen synthetischen Matrix-Writer; generierte Reports verwenden
Runtime-Zusammenfassungen und Snapshot-Daten.

## Externer Einsatz

Dieses Verzeichnis enthält Beispielkonfigurationen für externen Einsatz. Sie
sind nur Startpunkte und keine universellen Produktionsdefaults. Der passende
Compile-Guide erklärt, wie das erforderliche Artefakt
`haproxy-modsecurity-spoa` gebaut oder vorbereitet wird. Kopieren oder
adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen; Pfade wie
`/etc/...`, `/usr/lib/...`, `127.0.0.1`, Ports, Backend-URLs und Log-Pfade sind
Platzhalter, sofern sie nicht zu Ihrem System passen.

Service-Kontext: HAProxy plus SPOA-Prozess. Nach dem Anpassen der Dateien
`haproxy -c` ausführen, HAProxy reloaden und den betreiberverwalteten
SPOA-Prozess neu starten. HAProxy-Logs, `decision.jsonl`, `audit.log` und
SPOA-Diagnose-Logs prüfen.

## Nicht-Claims

- Diese Beispiele sind keine pauschale Production-Readiness-Zertifizierung.
- Sie belegen nicht jedes Paket, jede Version oder jedes Layout.
- Phase 4 / RESPONSE_BODY ist im ausgewählten SPOP-Pfad `not_implemented`; das
  ausgemusterte Sample ist deaktiviert und kein aktueller Laufzeitnachweis.

## Verwandte Dokumente

- [COMPILE_HAPROXY.de.md](../../COMPILE_HAPROXY.de.md)
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
- `reports/testing/haproxy-poc.md`
