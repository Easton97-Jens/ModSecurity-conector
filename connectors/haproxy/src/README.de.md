# HAProxy-Quelle

**Sprache:** [English](README.md) | Deutsch

Status: live-yaml-spoa-runtime (teilweise)
Laufzeitstatus: Live-Anfrage-seitige YAML-Ausführung über HAProxy, SPOA/SPOP,
und libmodsecurity.

Dieses Verzeichnis enthält lokale HAProxy-Starter-/Laufzeitquellen. Der SPOP
Laufzeit- und libmodsecurity-Bindung führen jetzt gemeinsam genutztes Framework YAML aus
Anfrageseitige Fälle laufen über HAProxy, dies ist jedoch noch nicht vollständig
Produktions-HAProxy-Adapter.

Aktuelle Starterdateien:

- `haproxy_spoa_agent_starter.c`
- `haproxy_spoa_agent_starter.h`
- `haproxy_spoa_main.c`
- `haproxy_spop_diagnostic_runtime.c`
- `haproxy_modsecurity_binding.c`
- `haproxy_modsecurity_binding.h`
- `haproxy_modsecurity_binding_self_test.c`

Der Starter kann lokal kompiliert und selbst getestet werden. Es wertet synthetisch aus
In-Process-Anfragen mit Repository-eigenen Anfrage-/Interventions-/Statusformen.
Die SPOP-Laufzeit analysiert Live-NOTIFY-Argumente von HAProxy, einschließlich `method`,
`uri`, `req.hdrs_bin` mit einem sicheren `req.hdrs`-Fallback und `req.body`. Die
Bindung lädt die materialisierte Regeldatei, verarbeitet URI, Header, optional
Anforderungshauptteilbytes und libmodsecurity-Eingriffe, dann sendet die Laufzeit
die verifizierte Set-Var ACK für 403 störende Entscheidungen.

Live-Beweise umfassen derzeit anforderungsseitige Variablen `REQUEST_URI`,
`REQUEST_HEADERS`, `REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`,
`REQUEST_COOKIES`, `REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES` und `XML`,
plus CRS SQLi-Anomalieblockierung in der With-CRS-Variante. Unterstützung für den Anfragetext ist
begrenzt durch den aktuellen anforderungsgepufferten Single-Frame-SPOE-Pfad von HAProxy
(`tune.bufsize 65536`, `max-frame-size 65532`, ein `req.body`-Argument).

Reaktionsphasen, Audit-Log-Zusicherungen, Weiterleitungen, Nicht-403-Störungsstatus,
und `RESPONSE_BODY` bleiben für die HAProxy-Laufzeitförderung nicht implementiert.

Eine produktive Quelle darf nur mit Herkunfts-/Lizenz-/Metadatennachweisen hinzugefügt werden.
einschließlich des zukünftigen HAProxy-Quellursprungs, der Lizenz, importierter Dateien und lokal
Änderungen und Build-/Laufzeitnachweise.
