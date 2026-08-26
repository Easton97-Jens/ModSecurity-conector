# P1–P4-Connector-Parität: Current-Master-Baseline und Ausführungsplan

**Sprache:** [English](p1-p4-connector-parity-baseline.md) | Deutsch

## Zweck, Scope und Evidenzgrenze

Dieser Bericht ist die code-nahe Baseline für das vom Benutzer verlangte
P1–P4-Paritätsprogramm. Er dokumentiert den beobachteten Zustand des Parent-
`master` bei `6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` am 2026-08-26 und
definiert die Arbeit für den verlangten Zielzustand. Er beansprucht nicht, dass
das Programm abgeschlossen ist.

Der gewählte Scope umfasst die zehn Parent-Connectorpfade Apache, NGINX,
HAProxy HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy ext_proc, Traefik
forwardAuth, Traefik Native UDS, Stock-lighttpd und Patched-lighttpd.
CI-Workflows, Branch-Regeln, Required Checks, Framework-/MRTS-Source,
Gitlinks und gehostete Testkonfiguration liegen außerhalb des Scopes. Der
Bericht stützt sich auf die Inspektion der aktuellen Source,
Capability-Dateien, Harnesses und Dokumentation; er behauptet keinen
Connector-Build und keine reale P1–P4-Hostmatrix.

Das gemeinsame Evidenzmodell verlangt mehr als einen HTTP-Status: Ein Lauf
muss Regel-ID, Connector-Event, angeforderte Entscheidung, beobachtete
Hostaktion und Cleanup-Ergebnis an eine Transaktion binden. Bodies werden nur
als begrenzte Metadaten, Digests, Längen und EOS-Status dargestellt; rohe
Body-Payloads dürfen nicht in Event-JSONL gelangen.

## Kanonischer Phasenvertrag

`common/include/msconnector/phase.h` und
`common/rules/p1_p4_traffic_vectors.json` definieren die
Repository-Bedeutungen der vier Phasen:

| Phase | Kanonischer Zeitpunkt | Aktuelle Vektor-Regel-IDs |
| --- | --- | --- |
| P1 | Request-Header | `1101001` |
| P2 | Tatsächlicher Request-Body, finalisiert bei EOS | `1102001`, `1102002` |
| P3 | Upstream-Response-Header | `1103001` |
| P4 | Response-Body, finalisiert bei EOS | `1104001`, `1104002`, `1104003` |

Der Zielvertrag muss diese Reihenfolge sowie die gemeinsamen
Entscheidungsarten, Limits, Timeout-Semantik, den Fail-Modus, deterministisches
Cleanup und Korrelationsfelder erhalten. Insbesondere darf eine P4-Safe-
Entscheidung als `log_only` dokumentiert werden; P4 Strict braucht ein
deterministisches, client-sichtbares Real-Host-Ergebnis und darf nicht allein
aus einem treiberseitigen Abort oder Reset abgeleitet werden.

## Aktuelle Implementierungs- und Evidenzmatrix

Jede nachstehende Zeile liegt unterhalb des verlangten Status
`fully_runtime_verified`. Eine source-seitige Implementierung oder ein
Harness-Einstiegspunkt ist kein kanonischer Runtime-Nachweis.

| Connectorpfad | Source und lokale Einstiegspunkte | Beobachteter P1–P4-Status | Erforderliche Arbeit vor der Abnahme |
| --- | --- | --- | --- |
| Apache | `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`; `connectors/apache/Makefile.am`; `connectors/apache/harness/run_apache_smoke.sh` | P1–P4-Adapter existieren, die Capabilities stehen aber auf `implemented_not_asserted`. | Kanonische Real-Host-P1–P4-Safe/Strict-Evidenz erzeugen; Client-/Upstream-Abbruchbehandlung implementieren und beweisen, derzeit `not_implemented`. |
| NGINX | `connectors/nginx/src/ngx_http_modsecurity_module.c`, Access-/Header-/Body-Filteradapter; `connectors/nginx/harness/run_nginx_smoke.sh` | P1–P4-Adapter existieren, sind aber `implemented_not_asserted`; P4 unterliegt nach gesendeten Response-Headers Late-Intervention-Grenzen. | Reales P1–P4-Safe/Strict-Verhalten beweisen und Client-/Upstream-Abbruch- sowie Pre-Commit-P4-Deny-Lücken schließen, ohne das Master-/Worker-Modell zu schwächen. |
| HAProxy HTX | `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`; `connectors/haproxy/Makefile`; `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` | P1–P3 werden durch lokale Harness-Fälle ausgeübt; P4 wird nach dem Forwarding beobachtet, Safe wird `log_only`, Strict hat keine Hostaktion. | Ein Pre-Commit-Response-Body-Enforcement-Design erstellen und client-sichtbares Strict-Verhalten, Fehler, Folge-Traffic und Cleanup beweisen. |
| HAProxy SPOE/SPOP | `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/src/haproxy_modsecurity_binding.c`; `connectors/haproxy/Makefile`; `connectors/haproxy/harness/run_haproxy_smoke.sh` | P1/P2 sowie optionale P3-Headers existieren; P4-Response-Body-Behandlung und Safe/Strict sind `not_implemented`. | Einen Response-Body-fähigen Pfad, begrenzte serverseitige I/O, Disconnect-Behandlung und vollständige P4-/Fehler-/Cleanup-Evidenz ergänzen. |
| Envoy ext_authz | `connectors/envoy/src/envoy_ext_authz_service_main.c` über `common/runtime/http_authorization_service.c`; `connectors/envoy/Makefile`; `connectors/envoy/config/envoy-ext-authz.conf` | Request-Autorisierung ist verfügbar; gepuffertes P2 ist konfigurationsabhängig; P3/P4 stehen diesem Pre-Upstream-Protokoll nicht zur Verfügung. | Einen responsefähigen Companion oder kombinierten Pfad bereitstellen und testen. Es muss eine Ende-zu-Ende-Connectorlösung sein, keine dauerhafte `not_applicable`-Ausnahme. |
| Envoy ext_proc | `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`, `internal/processor/common_runtime_engine.go`; `connectors/envoy/Makefile`; `config/envoy-ext-proc-streaming.yaml.in` | P1–P4-Streaming-Wiring existiert; Post-Commit-Safe ist `log_only`; Strict-Abort wird ausdrücklich nicht versucht. | Deterministisches client-sichtbares Strict-Verhalten, serverseitige Idle-Grenzen, alle Fehlerpfade, Folge-Traffic und Cleanup definieren und beweisen. |
| Traefik forwardAuth | `connectors/traefik/src/traefik_forwardauth_service_main.c` über `common/runtime/http_authorization_service.c`; `connectors/traefik/Makefile`; `connectors/traefik/config/traefik-forwardauth.conf` | P1 existiert; das Standardprofil hat `request_body_mode=none`; P3/P4 sind für Pre-Upstream-forwardAuth nicht sichtbar. | Einen responsefähigen Companion oder kombinierten Pfad ergänzen und vollständiges P1–P4-, Safe/Strict-, Fehler- und Cleanup-Verhalten als eine Connectorlösung beweisen. |
| Traefik Native UDS | `connectors/traefik/native_middleware/middleware.go`, `engine_uds.go`; `connectors/traefik/Makefile`; `connectors/traefik/scripts/runtime-native-middleware.sh` | P1–P4-Source-Wiring existiert; Post-Commit-Safe ist `log_only`; Strict-Abort ist `NOT EXECUTED`. | Deterministisches Strict-Ergebnis sowie Engine-down, Invalid-Response, Disconnect, Folgeanfrage und Cleanup mit einem realen Host beweisen. |
| Stock lighttpd | `connectors/lighttpd/module/mod_msconnector.c`; `connectors/lighttpd/Makefile`; `connectors/lighttpd/build/build_module.sh` | P1- und Response-Header-Wiring existieren; die gewählte Stock-ABI hat `request_body_mode=none` und keinen Response-Body-Hook. | Eine ABI-korrekte Full-Body-Strategie wählen; der aktuelle Stock-Pfad kann universelle P2/P4-Abnahme ohne eine unterstützte responsefähige Lösung nicht erfüllen. |
| Patched lighttpd | `connectors/lighttpd/module/mod_msconnector.c`; `connectors/lighttpd/patches/0001-lighttpd-msconnector-stream-hooks.patch`; `connectors/lighttpd/Makefile` | P1–P4-Source-Hooks existieren, mit Post-Commit-Safe-Wiring; Strict ist `NOT EXECUTED`. | Kanonische Real-Host-P1–P4-/Safe/Strict-, First-Byte-, Disconnect-/Abort-, Folgeanfrage- und Cleanup-Evidenz liefern. |

Die connectorübergreifenden Harnesses und Evidenzregeln liegen unter
`connectors/composite_harness/`, während `docs/testing-and-evidence.md` die
Trennung zwischen statischen Behauptungen und laufgebundener Evidenz festlegt.
Der aktuelle Coverage-Bericht enthält keine vollständige Matrix mit
`runtime_verified=true`; seine bestehenden Ergebnisse sind keine Promotion des
Zehn-Pfad-P1–P4-Ziels.

## Gemeinsame Arbeitspakete und Abhängigkeiten

1. **Zuerst Source-Ownership abgleichen.** Die offenen Draft-PRs #344, #345
   und #346 überlappen mit dem hier benötigten gemeinsamen Vertrag,
   Connector-Implementierungen und Failure-Cleanup. Dieser Branch basiert
   absichtlich auf aktuellem `master` und kopiert, mergt, rebaset oder
   beansprucht diese nicht gemergte Arbeit nicht. Vor konkurrierenden
   Source-Edits ist eine benutzerautorisierte Integrations- oder
   Ablösungsentscheidung nötig.
2. **Den gemeinsamen Vertrag verbindlich machen.** Transaction State,
   Decision-to-Event-Mapping, Phasenreihenfolge, begrenzte Request-/Response-
   Metadaten, Timeouts, Fail-open-/Fail-closed-Policy und Cleanup-Receipt-
   Schema angleichen. Das bestehende Problem `FND-PARENT-0234`—ein Event kann
   eine Hostaktion vor deren Bestätigung behaupten—bleibt release-blockierend,
   bis eine Source- und Runtime-Reparatur verifiziert ist.
3. **Architektonische Phasenlücken schließen.** Responsefähige kombinierte
   Pfade für Envoy ext_authz und Traefik forwardAuth implementieren; einen
   vollständigen Response-Body-Pfad für SPOE/SPOP und eine ABI-korrekte Lösung
   für Stock lighttpd entwickeln. Diese Pfade dürfen beim universellen Ziel
   nicht `not_applicable` bleiben.
4. **Safe und Strict standardisieren.** Safe als explizite Post-Commit-
   Beobachtung erhalten, wenn Intervention nicht mehr möglich ist. Für Strict
   den frühesten erzwingbaren Punkt bestimmen und das daraus resultierende
   Host-/Client-Transportverhalten beweisen, statt einen connectorlokalen
   Reset als Nachweis zu akzeptieren.
5. **Fehler und Ressourcenlebenszyklus normalisieren.** Für jeden Pfad Engine
   down, Timeout, fehlerhafte Antwort, Client-Disconnect/Cancel, eine gültige
   Folgeanfrage und Cleanup von Prozessen, Ports, UDS-Pfaden, Streams und
   task-eigenen Artefakten beweisen.
6. **Nur laufgebundene Evidenz promoten.** Jeder Pfad muss separat bauen,
   Konfiguration validieren, einen realen Host starten/auf Readiness prüfen,
   Allow, P1, P2 mit tatsächlichem Body, P3, P4 Safe, P4 Strict, alle
   erforderlichen Fehlerfälle und Cleanup ausführen. Erst dann darf sein
   Status `fully_runtime_verified` werden.

## Security-Review-Baseline

Dieser statische Baseline-Bericht erstellt kein neues validiertes Finding. Das
bestehende `FND-PARENT-0234` wird nicht dupliziert. Die fokussierte
Source-Review identifizierte außerdem drei plausible HAProxy-SPOP-Kandidaten,
die vor einem Finding oder einer Remediation-Behauptung Runtime-Validierung
brauchen: blockierende Peer-I/O trotz geparster Timeout-Option, einen
Peer-Disconnect-`SIGPIPE`/`EPIPE`-Pfad und Header-Count-Validierung, die einen
Mapping-Fehler loggen könnte, ohne die Transaktion abzulehnen. Die gewählten
Defaults binden SPOP an Loopback; das begrenzt, ersetzt aber nicht die Prüfung
dieser Pfade. Kein Security-Control, Logging-Limit oder Cleanup-Check wird
durch diesen Dokumentationsmeilenstein geschwächt.

## Abnahme und nächstes Ausführungsgate

Das Gesamtprogramm ist erst abgenommen, wenn jeder genannte Connectorpfad ein
Real-Host-Evidenzbundle für Build, Konfiguration, Readiness, Allow, P1, P2,
P3, P4 Safe, P4 Strict, Engine down, Timeout, ungültige Antwort, Disconnect
oder Cancel, Folge-Traffic und Cleanup besitzt—mit Korrelationsfeldern, die
die tatsächliche Hostaktion belegen. In der finalen Matrix darf keine Zelle
`not_run`, `not_applicable`, `partially_runtime_verified` oder `failed_build`
enthalten.

Dieser Meilenstein schließt die Baseline-Analyse und den priorisierten Plan aus
Prompt 1 ab; er startet kein großflächiges Source-Refactoring. Der nächste
Source-Meilenstein ist ausschließlich durch die Ownership-Entscheidung zu den
überlappenden, nicht gemergten PRs blockiert, nicht durch eine Behauptung, die
fehlenden Capabilities seien nicht unterstützbar. Ein isolierter task-eigener
lokaler Storage-Preflight für künftige Builds und Runtime-Evidenz bestand; in
dieser reinen Dokumentationsänderung wurden weder Build noch Hostprozess noch
lokale Connector-Runtime-Matrix gestartet.
