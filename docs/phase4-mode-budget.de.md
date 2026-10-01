# Phase-4-Modus und kumulierte Inspection-Budgets

**Sprache:** [English](phase4-mode-budget.md) | Deutsch

## Geltungsbereich

Dieser Vertrag umfasst Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd in
diesem Repository. Er betrifft das zusätzliche kumulierte Inspection-Budget
des Connectors, nicht die Response-Body-Policy von libModSecurity oder andere
Ressourcenlimits.

| Modus | Zusätzliches kumuliertes Phase-4-Budget | Inspection und Fehler |
| --- | --- | --- |
| `off` (Standard) | Nicht durchgesetzt | Konfigurierte Engine-Inspection und native Interventions-/Fehlerbehandlung bleiben aktiv. |
| `safe` | Durchgesetzt | Bestehende frühe Durchsetzung und spätes `log_only` bei Regelinterventionen bleiben erhalten, soweit unterstützt. |
| `strict` | Durchgesetzt | Bestehende frühe Durchsetzung und unterstützte späte Abbrüche bleiben erhalten. |

`UNSET` und ungültige Modi sind keine Synonyme für `off`. Konfigurationsprüfung
und die Anforderung eines positiven konfigurierten Limits gelten in jedem
Modus weiter. `SecResponseBodyAccess`, `SecResponseBodyMimeType`,
`SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit` und die Limit-Aktion
der Engine werden nicht verändert.

## Implementierungsgrenzen

Apache und NGINX verwenden `modsecurity_phase4_body_limit`. Das native
HAProxy-Binding und Integrationen über die Common Runtime verwenden ihr
konfiguriertes Response-Inspection-Budget. Kumulativer Planer und sekundärer
Transaktionszähler müssen übereinstimmen. HAProxy HTX setzt auch sein
Stream-Budget konsistent. Die Content-Length-Vorprüfung im lighttpd-
Streaming-Sidecar folgt demselben Modus. Der Go-Prozessor von Envoy fragt den
geladenen Common-Engine-Modus über eine explizite Budget-Capability ab, nicht
über die separat konfigurierte Late-Action-Policy. Nachrichten-/Chunk-Limit
und Überlaufprüfungen des vorzeichenbehafteten Zählers bleiben aktiv.

Die Common-Runtime-Änderungen umfassen direkte und Response-Companion-Append-
Pfade von Envoy, Traefik und lighttpd. Reine Request-Kompatibilitätsrouten
benötigen weiterhin ihren unterstützten Observer/Companion. Die Protokoll- und
Companion-Transportlimits von HAProxy SPOE/SPOP bleiben unabhängig und werden
nicht deaktiviert. Kein bislang ununterstütztes Profil erhält durch diese
Änderung einen funktionierenden Phase-4-Pfad.

Das interne effektive Limit ist in `off` nur als Darstellung eines fehlenden
konfigurierten kumulierten Limits `SIZE_MAX`. Es ist niemals eine
Allokationsgröße. Bytezählerüberlauf, ungültige Zeiger, fehlerhafte Datei-Reads,
Lifecycle-Verstöße und Engine-Fehler bleiben Fehler. `process_partial` darf
einen Zählerüberlauf in `off` nicht zu einem erfolgreichen unbegrenzten Append
machen.

## Unabhängige Ressourcenlimits

Header-/Event-Limits, maximale Chunks und Nachrichten, Korrelationskapazitäten,
Timeouts und begrenzter Response-Speicher bleiben aktiv. Der bestehende
öffentliche Response-Limit-Getter der Common Runtime beschreibt weiterhin die
begrenzte Host-/Transport-Allokationskapazität. Er darf nicht `SIZE_MAX`
zurückgeben. Ein puffernder Kompatibilitäts-Sidecar kann deshalb auch in `off`
eine zu große Response ablehnen; dies ist seine unabhängige Speicherkapazität,
nicht das deaktivierte zusätzliche kumulierte Phase-4-Budget.

## Native Fehler und NULL-Prüfungen

In NGINX verwendet ein negativer nativer Interventions-Rückgabewert bei `off`
wie vor PR #377 den Pfad
`ngx_http_filter_finalize_request(..., NGX_HTTP_INTERNAL_SERVER_ERROR)`.
Positive Statuswerte werden unverändert zurückgegeben; bei null läuft die
Verarbeitung normal weiter. Die Safe-/Strict-Interventionspolicy bleibt
unverändert.

Andere Integrationen behalten ihre eigenen Rückgabekonventionen: APR-Status,
null/nichtnull für Common-Runtime-Erfolg und hostspezifische Transportfehler.
Die Integer-Konvention von NGINX darf nicht in diese APIs kopiert werden.

P4-Planer, Handler und Logger von NGINX prüfen fehlende Konfiguration. Die
P4-Bucket- und Interventionspfade von Apache prüfen fehlenden Zustand,
Konfiguration und Request-Objekte. Der gemeinsame Event-Writer prüft Runtime,
Event und Datei vor dem Dereferenzieren. Traefik prüft den Service einer
Session vor dem Lesen ihrer Response-Body-Policy. Bestehende Prüfungen der
Envoy-Bridge bleiben erhalten.

## Grenzen der Validierung

Fokussierte kompilierte Helper-/Branch-Tests und Source-Wiring-Prüfungen sind
keine HTTP-Integrationstests mit laufendem NGINX, httpd, HAProxy, Envoy, Traefik
oder lighttpd. Vor einem Merge sind native Host-Regressionen, Allokations-/
Transportprüfungen und CI für den aktuellen Commit nötig. Der [Change Record](../reports/audits/change-records/CR-20260920-phase4-all-connector-budget.de.md) enthält die tatsächlich ausgeführten
Prüfungen und Ergebnisse.
