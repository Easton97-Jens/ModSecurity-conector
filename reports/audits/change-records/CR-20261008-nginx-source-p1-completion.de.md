# Change Record: CR-20261008-nginx-source-p1-completion

**Sprache:** [English](CR-20261008-nginx-source-p1-completion.md) | Deutsch

Tatsächlicher Source-P1-Abschluss, keine Host-Auslieferung.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-source-p1-completion |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `9cfae553e7e69b1db8211f1a4ce0afc986b88604` |

## Motivation und Problemstellung

Native P1-Verarbeitung ohne Intervention hatte bislang kein quellenproduziertes Abschlussereignis, sofern kein Regelcallback auftrat. Driver- oder Cleanup-Events können tatsächlichen Request-Header-Abschluss nicht beweisen.

## Akzeptanzkriterien

Nur nach nativem Return1, abgeschlossenem Common-P1 und bestehender Fortsetzung ohne Intervention emittieren. Kein Event bei Denial, ungültigem nativem Return, Clock-/Budgetfehlern, terminalem/bereinigtem Zustand oder doppelter P1-Ausführung. Weder Host200, tatsächlich ausgeliefertes Allow, Request-EOS noch vollständigen Request-Erfolg behaupten.

## Implementierungsentscheidung und Begründung

Einen engen Konstruktor mit tatsächlichem Common-Wartezustand, keiner aktiven Phase, exakt abgeschlossenem P1-Mask, last_completed P1, keinem Fehler und keinem Cleanup ergänzen. Tatsächlichen nativen Return erhalten, bevor Intervention ret überschreibt. Nach allen Interventionszweigen durch den bestehenden begrenzten Request-Event-Writer emittieren; fehlender/fehlschlagender Sink bleibt warning-only.

## Geänderte Dateien

connectors/nginx/src/ngx_http_modsecurity_request_completion.h; connectors/nginx/src/ngx_http_modsecurity_access.c; connectors/nginx/SOURCE_MAP.json; tests/test_nginx_p1_completion_source.py; this EN/DE pair.

## Ausgeführte Befehle

RTK-gekapselte Parent-.venv-Unittests tests.test_nginx_p1_completion_source kompilieren tatsächlichen vollständigen P1-Caller/Result-Boundary sowie echte Common-Transitions, Budgets und JSONL mit C17 -Wall -Wextra -Werror. Originalquelle RED: 3 erwartete Missing-Event-Fehler in 4 Methoden; geänderte Quelle GREEN: 4 Methoden. Logs stream-c-p1-completion-red-final.log und stream-c-p1-completion-green.log erhalten die Ergebnisse. Finale Regression von P1, Connection/URI, Budget, P3/P4, Materialisierung und Kontextbuchhaltung besteht 31 Tests (stream-c-p1-completion-cross-final.log), einschließlich eines echten Common-Fehlers während des kontrollierten nativen Callbacks. Syntax/SOURCE_MAP-Identität, ci/tools/new-change-record.py check, make check-bilingual-docs und make check-doc-links (expliziter aktueller Framework-Checkout) bestehen. Keine fremden Source-Edits.

## Security-Auswirkung

Custom request_headers_complete/MSCONN_PHASE1_COMPLETE wird vom tatsächlichen Common-Protocol-View erhalten. Es hat leere Rule, ok/allow/requestedallow, leeres actual_action, http0/visible0/not_observable, echte Request-Metadaten und begrenzten Grund native_return=1;common_completed=1. Keine Regel, Host-Auslieferung oder Transport-Erfolg wird erzeugt.

## Runtime-Evidence

Nur kontrollierte C17-Source-/Serializer-Tests. Native Verarbeitung, Host-Metadaten-/Header-Plumbing und monotone Uhr sind kontrolliert; Common-Transitions, Budgetbridge, Eventkonstruktor und Serializer sind tatsächliche Quelle. Keine native NGINX-Runtime ausgeführt.

## Bekannte Einschränkungen

Completion beschreibt nur P1. Bestehendes Request-Logging bleibt warning-only; fehlende Source-Events dürfen Evidence-Consumer nicht ableiten. Bestehende Budget-/Fault-/Enforcement-Semantik der Caller bleibt unverändert.

## Verbleibende Risiken

Vor Runtime-Abdeckung oder Canonical-Akzeptanz muss der Koordinator neu bauen und frische native Runs ausführen. Bestehende Raw-Denial-Vokabel ist Common engine_decision/MSCONN_EVENT_ENGINE_DECISION bei transport_result not_observable; RULE_MATCHED wird als rule_match serialisiert. Source-Callbacknamen dürfen nicht mit Raw-JSONL verwechselt werden.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Build/Runtime, E2E, Remote-CI, Sonar, Framework-Edit, Gitlink-Änderung oder Push: außerhalb dieser begrenzten Producer-Aufgabe.

## Finaler Diff- und Review-Status

Fokussierten Source-Diff geprüft. Keine Common-Semantikänderung, kein neues Kontextfeld oder synthetische Evidenz. SOURCE_MAP enthält den neuen produktiven Header. Separater Sechs-Dateien-Commit mit nativ generierten EN/DE-Überschriften.
