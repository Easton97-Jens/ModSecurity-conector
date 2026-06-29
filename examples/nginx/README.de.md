# NGINX ModSecurity Beispiele

**Sprache:** [English](README.md) | Deutsch

## Inhaltsverzeichnis

- [Status](#status)
- [Zweck](#zweck)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Dateien](#dateien)
- [Produktionspfade](#produktionspfade)
- [Request-Only-Modus](#request-only-modus)
- [Phase 4 / RESPONSE_BODY-Modus](#phase-4--response_body-modus)
- [Variablen- und Platzhalterreferenz](#variablen--und-platzhalterreferenz)
- [Logging und Evidence](#logging-und-evidence)
- [Sicherheitshinweise](#sicherheitshinweise)
- [Externer Einsatz](#externer-einsatz)
- [Nicht-Claims](#nicht-claims)
- [Verwandte Dokumente](#verwandte-dokumente)

## Status

NGINX-Dynamic-Module-Beispiele für request-only und begrenzten Strict-Abort.
Produktionsnah, aber kein Nachweis für jeden NGINX-Build, jede Modul-ABI oder
vollständige RESPONSE_BODY-Unterstützung.

## Zweck

Diese Beispiele zeigen produktionsnahe NGINX-Konfiguration für request-only
ModSecurity und begrenzte Strict-Abort-Phase-4- / RESPONSE_BODY-Evidence.

## Benötigte Komponenten

NGINX und `ngx_http_modsecurity_module.so`, gebaut für eine kompatible
NGINX-ABI, libmodsecurity v3, ModSecurity-Regeln, optional CRS sowie
beschreibbare NGINX-/ModSecurity-Log-Orte.

## Dateien

- `nginx-modsecurity-request-only.conf`: NGINX-Modul und request-only
  Direktiven.
- `modsecurity-request-only.conf`: libmodsecurity-Regelkonfiguration für
  Request-Phasen.
- `nginx-modsecurity-phase4-strict-abort.conf`: NGINX-Connector-Direktiven für
  begrenztes Strict-Abort-Phase-4-Verhalten.
- `modsecurity-phase4.conf`: libmodsecurity-Regelkonfiguration für Response
  Bodies.

## Produktionspfade

Die Beispiele verwenden übliche NGINX- und ModSecurity-Pfade:

- `modules/ngx_http_modsecurity_module.so`
- `/etc/nginx/nginx.conf`
- `/etc/modsecurity/modsecurity-request-only.conf`
- `/etc/modsecurity/modsecurity-phase4.conf`
- `/etc/modsecurity/crs/`
- `/var/log/modsecurity/nginx-phase4.jsonl`
- `/var/log/modsecurity/nginx-audit.log`
- `/var/log/nginx/access.log`
- `/var/log/nginx/error.log`

## Request-Only-Modus

Der Request-only-Modus lädt `ngx_http_modsecurity_module`, aktiviert
`modsecurity on` und zeigt mit `modsecurity_rules_file` auf eine Konfiguration
mit `SecResponseBodyAccess Off`.

```bash
nginx -t
nginx -s reload
```

## Phase 4 / RESPONSE_BODY-Modus

Das Strict-Abort-Beispiel aktiviert `SecResponseBodyAccess On` und
`modsecurity_phase4_mode strict`. Der Connector kann späte Interventions
aufzeichnen und einen bereits begonnenen Transfer abbrechen. Das ist
Runtime-Evidence, keine vollständige Buffering-Parität und keine promotete
RESPONSE_BODY-Capability.

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte Strict-Abort-Evidence
wird nur als Runtime-Evidence dokumentiert.

## Variablen- und Platzhalterreferenz

| Name | Typ | Erforderlich | Beispielwert | Verwendet in | Bedeutung | Änderung erfordert Restart/Reload | Hinweise |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `load_module` | NGINX-Direktive | Ja | `modules/ngx_http_modsecurity_module.so` | `nginx-modsecurity-*.conf` | Lädt das NGINX-Connector-Modul. | Restart | Dynamische Module werden beim Master-Start geladen. |
| `modsecurity` | NGINX-Direktive | Ja | `on` | `nginx-modsecurity-*.conf` | Aktiviert ModSecurity im konfigurierten Scope. | Reload | Je nach Bedarf in `http`, `server` oder `location` verwenden. |
| `modsecurity_rules_file` | NGINX-Direktive | Ja | `/etc/modsecurity/modsecurity-request-only.conf` | `nginx-modsecurity-*.conf` | Zeigt NGINX auf die libmodsecurity-Regeldatei. | Reload | Phase-4-Regeldatei nur für begrenzte Response-Evidence verwenden. |
| `modsecurity_phase4_mode` | NGINX-Direktive | Nur Phase 4 | `strict` | `nginx-modsecurity-phase4-strict-abort.conf` | Wählt Strict-Abort-Response-Verhalten. | Reload | Kann eine bereits begonnene Response abbrechen. |
| `modsecurity_phase4_content_types_file` | NGINX-Direktive | Nur Phase 4 | `/etc/modsecurity/phase4-content-types.conf` | `nginx-modsecurity-phase4-strict-abort.conf` | Optionale Allowlist für Response-Body-MIME-Typen. | Reload | In Produktion eng halten. |
| `modsecurity_phase4_log` | NGINX-Direktive | Nur Phase 4 | `/var/log/modsecurity/nginx-phase4.jsonl` | `nginx-modsecurity-phase4-strict-abort.conf` | JSONL-Connector-Decision-Evidence. | Reload | Mit normaler Logrotation rotieren. |
| `gzip` | NGINX-Direktive | Nein | `off` | `nginx-modsecurity-phase4-strict-abort.conf` | Hält Kompression während der Validierung deaktiviert. | Reload | Byte-Reihenfolge prüfen, bevor Kompression aktiviert wird. |
| `proxy_pass` | NGINX-Direktive | Ja | `http://app_backend` | `nginx-modsecurity-*.conf` | Beispielroute zur Upstream-Anwendung. | Reload | Durch Produktions-Upstreams ersetzen. |
| `SecRuleEngine` | ModSecurity-Direktive | Ja | `On` | `modsecurity-*.conf` | Aktiviert Regelausführung. | Reload | Für nicht-disruptiven Rollout `DetectionOnly` verwenden. |
| `SecRequestBodyAccess` | ModSecurity-Direktive | Ja | `On` | `modsecurity-*.conf` | Aktiviert Request-Body-Verarbeitung. | Reload | Request-Body-Support ist von RESPONSE_BODY getrennt. |
| `SecResponseBodyAccess` | ModSecurity-Direktive | Ja | `Off` oder `On` | `modsecurity-*.conf` | Aktiviert oder deaktiviert RESPONSE_BODY-Verarbeitung. | Reload | `On` bleibt begrenzte Strict-Abort-Evidence. |
| `SecResponseBodyMimeType` | ModSecurity-Direktive | Nur Phase 4 | `text/plain text/html application/json` | `modsecurity-phase4.conf` | Begrenzt inspizierte Response-MIME-Typen. | Reload | Explizit halten, um binäre Responses zu vermeiden. |
| `SecResponseBodyLimit` | ModSecurity-Direktive | Nur Phase 4 | `1048576` | `modsecurity-phase4.conf` | Begrenzt libmodsecurity-Response-Body-Buffering. | Reload | Nicht auf unbegrenztes Buffering verlassen. |
| `SecResponseBodyLimitAction` | ModSecurity-Direktive | Nur Phase 4 | `ProcessPartial` | `modsecurity-phase4.conf` | Definiert Verhalten, wenn der Body das Limit überschreitet. | Reload | Mit Produktions-Risikopolicy abstimmen. |
| `IncludeOptional` | ModSecurity-Direktive | Nein | `/etc/modsecurity/crs/rules/*.conf` | `modsecurity-*.conf` | Bindet CRS-Dateien ein, falls vorhanden. | Reload | Fehlende CRS-Dateien blockieren den Start nicht. |
| `SecAuditEngine` | ModSecurity-Direktive | Nein | `RelevantOnly` | `modsecurity-*.conf` | Aktiviert Audit-Logging für relevante Transactions. | Reload | Mit Logrotation verwenden. |
| `SecAuditLog` | ModSecurity-Direktive | Nein | `/var/log/modsecurity/nginx-audit.log` | `modsecurity-*.conf` | Ziel für Audit-Logs. | Reload | Sicherstellen, dass NGINX-Worker schreiben können. |
| `RESPONSE_BODY` | ModSecurity-Collection | Nur Phase 4 | `@contains response-attack` | `modsecurity-phase4.conf` | Beispielziel für Outbound-Regeln. | Reload | Beispielregel durch Produktionsregeln ersetzen. |

## Logging und Evidence

Connector-Phase-4-Decisions sind JSON-Zeilen in `nginx-phase4.jsonl`. Audit
Records werden von libmodsecurity über `SecAuditLog` erzeugt. Access- und
Error-Logs bleiben unter `/var/log/nginx`.

## Sicherheitshinweise

Behalten Sie request-only als Baseline, prüfen Sie die Modul-ABI-Kompatibilität
mit dem bereitgestellten NGINX-Binary, validieren Sie Response-Body-Verhalten
zuerst mit deaktivierter Kompression und bewahren Sie Strict-Abort-Evidence auf,
wenn Outbound-Regeln getestet werden.

## Externer Einsatz

Dieses Verzeichnis enthält Beispielkonfigurationen für externen Einsatz. Sie
sind nur Startpunkte und keine universellen Produktionsdefaults. Der passende
Compile-Guide erklärt, wie das erforderliche Artefakt
`ngx_http_modsecurity_module.so` gebaut oder vorbereitet wird. Kopieren oder
adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen; Pfade wie
`/etc/...`, `/usr/lib/...`, `127.0.0.1`, Ports, Backend-URLs und Log-Pfade sind
Platzhalter, sofern sie nicht zu Ihrem System passen.

Service-Kontext: NGINX. Nach dem Anpassen der Dateien `nginx -t` ausführen und
den NGINX-Service reloaden. NGINX-Error-/Access-Logs und ModSecurity-Audit-Logs
prüfen.

## Nicht-Claims

- Diese Beispiele sind keine pauschale Production-Readiness-Zertifizierung.
- Sie belegen nicht jedes Paket, jede Version oder jedes Layout.
- Phase-4- / RESPONSE_BODY-Beispiele sind nur begrenzte Runtime-Evidence, keine
  promotete vollständige Unterstützung.

## Verwandte Dokumente

- [COMPILE_NGINX.de.md](../../COMPILE_NGINX.de.md)
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`
- `reports/testing/nginx-poc.md`
