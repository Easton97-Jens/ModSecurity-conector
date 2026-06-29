# Apache ModSecurity Beispiele

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

Apache-Request-only- und begrenzte Phase-4-Beispiele. Produktionsnah, aber kein
Nachweis für jedes Apache-Distribution-Paket, jedes MPM oder vollständige
RESPONSE_BODY-Unterstützung.

## Zweck

Diese Beispiele zeigen produktionsnahe Apache-httpd-Konfiguration für
request-only ModSecurity und begrenzte Phase-4- / RESPONSE_BODY-Evidence.

## Benötigte Komponenten

Apache httpd/APXS und `mod_security3.so`, gebaut für dieselbe Apache-ABI,
libmodsecurity v3, ModSecurity-Regeln, optional CRS sowie beschreibbare Apache-/
ModSecurity-Log-Orte.

## Dateien

- `apache-modsecurity-request-only.conf`: Apache-Modul- und request-only
  Connector-Direktiven.
- `modsecurity-request-only.conf`: libmodsecurity-Regelkonfiguration für
  Request-Phasen.
- `apache-modsecurity-phase4-buffered.conf`: Apache-Connector-Direktiven für
  begrenztes Phase-4-Buffering.
- `modsecurity-phase4.conf`: libmodsecurity-Regelkonfiguration für Response
  Bodies.

## Produktionspfade

Die Beispiele verwenden übliche Debian-artige Pfade:

- `/usr/lib/apache2/modules/mod_security3.so`
- `/etc/modsecurity/modsecurity-request-only.conf`
- `/etc/modsecurity/modsecurity-phase4.conf`
- `/etc/modsecurity/crs/`
- `/var/log/modsecurity/apache-phase4.jsonl`
- `/var/log/modsecurity/apache-audit.log`
- `/var/log/apache2/access.log`
- `/var/log/apache2/error.log`

Passen Sie Pfade für Distributionen an, die `/etc/httpd` und `/var/log/httpd`
verwenden.

## Request-Only-Modus

Der Request-only-Modus aktiviert ModSecurity für Request-Phasen und behält
`SecResponseBodyAccess Off` bei. Er ist der konservative Default, wenn späte
Response-Unterbrechung nicht akzeptabel ist.

```bash
apachectl configtest
apachectl graceful
```

## Phase 4 / RESPONSE_BODY-Modus

Das Phase-4-Beispiel aktiviert `SecResponseBodyAccess On`, MIME-Einschränkungen,
`SecResponseBodyLimit`, `SecResponseBodyLimitAction ProcessPartial` und das
Apache-Connector-`modsecurity_phase4_body_limit`. Wenn Apache die gepufferte
Response vor dem Commit inspizieren kann, kann eine disruptive Phase-4-Regel
einen blockierenden Status zurückgeben. Wenn eine Response bereits committed
ist, ist Strict-Abort-Verhalten Runtime-Evidence, keine saubere
Full-Body-Promotion.

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte Strict-Abort-Evidence
wird nur als Runtime-Evidence dokumentiert.

## Variablen- und Platzhalterreferenz

| Name | Typ | Erforderlich | Beispielwert | Verwendet in | Bedeutung | Änderung erfordert Restart/Reload | Hinweise |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `security3_module` | Apache-Modulname | Ja | `mod_security3.so` | `apache-modsecurity-*.conf` | Lädt den Apache-Connector. | Restart oder Graceful Reload | Pfad ist distributionsspezifisch. |
| `modsecurity` | Apache-Direktive | Ja | `on` | `apache-modsecurity-*.conf` | Aktiviert ModSecurity im konfigurierten Scope. | Graceful Reload | In globaler Konfiguration oder vhost-Scope verwenden. |
| `modsecurity_rules_file` | Apache-Direktive | Ja | `/etc/modsecurity/modsecurity-request-only.conf` | `apache-modsecurity-*.conf` | Zeigt Apache auf die libmodsecurity-Regeldatei. | Graceful Reload | Phase-4-Regeldatei nur für begrenzte Response-Evidence verwenden. |
| `modsecurity_use_error_log` | Apache-Direktive | Nein | `on` | `apache-modsecurity-*.conf` | Sendet Connector-Diagnostik an das Apache-Error-Log. | Graceful Reload | Während Rollout nützlich. |
| `modsecurity_phase4_mode` | Apache-Direktive | Nur Phase 4 | `safe` | `apache-modsecurity-phase4-buffered.conf` | Wählt Connector-Phase-4-Verhalten. | Graceful Reload | Safe Mode bevorzugt sauberes Blocken vor Response-Commit. |
| `modsecurity_phase4_content_types_file` | Apache-Direktive | Nur Phase 4 | `/etc/modsecurity/phase4-content-types.conf` | `apache-modsecurity-phase4-buffered.conf` | Optionale Allowlist für Response-Body-MIME-Typen. | Graceful Reload | In Produktion eng halten. |
| `modsecurity_phase4_log` | Apache-Direktive | Nur Phase 4 | `/var/log/modsecurity/apache-phase4.jsonl` | `apache-modsecurity-phase4-buffered.conf` | JSONL-Connector-Decision-Evidence. | Graceful Reload | Mit normaler Logrotation rotieren. |
| `modsecurity_phase4_body_limit` | Apache-Direktive | Nur Phase 4 | `1048576` | `apache-modsecurity-phase4-buffered.conf` | Begrenzt Connector-Response-Buffering. | Graceful Reload | Mit `SecResponseBodyLimit` abstimmen. |
| `SecRuleEngine` | ModSecurity-Direktive | Ja | `On` | `modsecurity-*.conf` | Aktiviert Regelausführung. | Graceful Reload | Für nicht-disruptiven Rollout `DetectionOnly` verwenden. |
| `SecRequestBodyAccess` | ModSecurity-Direktive | Ja | `On` | `modsecurity-*.conf` | Aktiviert Request-Body-Verarbeitung. | Graceful Reload | Request-Body-Support wird getrennt von RESPONSE_BODY promoted. |
| `SecResponseBodyAccess` | ModSecurity-Direktive | Ja | `Off` oder `On` | `modsecurity-*.conf` | Aktiviert oder deaktiviert RESPONSE_BODY-Verarbeitung. | Graceful Reload | `On` ist in diesen Beispielen nur begrenzte Evidence. |
| `SecResponseBodyMimeType` | ModSecurity-Direktive | Nur Phase 4 | `text/plain text/html application/json` | `modsecurity-phase4.conf` | Begrenzt inspizierte Response-MIME-Typen. | Graceful Reload | Explizit halten, um binäre Responses zu vermeiden. |
| `SecResponseBodyLimit` | ModSecurity-Direktive | Nur Phase 4 | `1048576` | `modsecurity-phase4.conf` | Begrenzt libmodsecurity-Response-Body-Buffering. | Graceful Reload | Mit Connector-Limit abstimmen. |
| `SecResponseBodyLimitAction` | ModSecurity-Direktive | Nur Phase 4 | `ProcessPartial` | `modsecurity-phase4.conf` | Definiert Verhalten, wenn der Body das Limit überschreitet. | Graceful Reload | Unbegrenztes Buffering vermeiden. |
| `IncludeOptional` | ModSecurity-Direktive | Nein | `/etc/modsecurity/crs/rules/*.conf` | `modsecurity-*.conf` | Bindet CRS-Dateien ein, falls vorhanden. | Graceful Reload | Fehlende CRS-Dateien blockieren den Start nicht. |
| `SecAuditEngine` | ModSecurity-Direktive | Nein | `RelevantOnly` | `modsecurity-*.conf` | Aktiviert Audit-Logging für relevante Transactions. | Graceful Reload | Mit Logrotation verwenden. |
| `SecAuditLog` | ModSecurity-Direktive | Nein | `/var/log/modsecurity/apache-audit.log` | `modsecurity-*.conf` | Ziel für Audit-Logs. | Graceful Reload | Sicherstellen, dass Verzeichnisberechtigungen Apache-Schreibzugriff erlauben. |
| `RESPONSE_BODY` | ModSecurity-Collection | Nur Phase 4 | `@contains response-attack` | `modsecurity-phase4.conf` | Beispielziel für Outbound-Regeln. | Graceful Reload | Beispielregel durch Produktionsregeln ersetzen. |

## Logging und Evidence

Connector-Decisions werden nach `apache-phase4.jsonl` geschrieben, wenn
Phase-4-Connector-Logging aktiviert ist. Audit Records werden von
libmodsecurity über `SecAuditLog` geschrieben. Apache-Access- und Error-Logs
bleiben im Apache-Log-Verzeichnis.

## Sicherheitshinweise

Beginnen Sie mit dem Request-only-Modus, aktivieren Sie Audit-Logging, validieren
Sie CRS-Includes und deaktivieren Sie Kompression, bis das Deployment belegt hat,
ob der Connector komprimierte oder unkomprimierte Response-Bytes sieht.

## Externer Einsatz

Dieses Verzeichnis enthält Beispielkonfigurationen für externen Einsatz. Sie
sind nur Startpunkte und keine universellen Produktionsdefaults. Der passende
Compile-Guide erklärt, wie das erforderliche Artefakt `mod_security3.so` gebaut
oder vorbereitet wird. Kopieren oder adaptieren Sie nur die Dateien, die zu
Ihrem Deployment passen; Pfade wie `/etc/...`, `/usr/lib/...`, `127.0.0.1`,
Ports, Backend-URLs und Log-Pfade sind Platzhalter, sofern sie nicht zu Ihrem
System passen.

Service-Kontext: Apache/httpd. Nach dem Anpassen der Dateien `apachectl
configtest` ausführen und den Apache-Service reloaden. Apache-Error-/Access-
Logs und ModSecurity-Audit-Logs prüfen.

## Nicht-Claims

- Diese Beispiele sind keine pauschale Production-Readiness-Zertifizierung.
- Sie belegen nicht jedes Paket, jede Version oder jedes Layout.
- Phase-4- / RESPONSE_BODY-Beispiele sind nur begrenzte Runtime-Evidence, keine
  promotete vollständige Unterstützung.

## Verwandte Dokumente

- [COMPILE_APACHE.de.md](../../COMPILE_APACHE.de.md)
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
- `reports/testing/apache-poc.md`
