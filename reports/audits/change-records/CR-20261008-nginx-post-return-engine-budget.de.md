# Change Record: CR-20261008-nginx-post-return-engine-budget

**Sprache:** [English](CR-20261008-nginx-post-return-engine-budget.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-post-return-engine-budget |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `49e2011b21893d1d30fdeedbe177deb48af0e4ce` |

## Motivation und Problemstellung

Zwei erforderliche native Timeout-Records benötigen einen echten Engine-Zeitvertrag. Ein langsamer Upstream ist kein Engine-Timeout. Das freigegebene NGINX-spezifische Budget ist standardmäßig deaktiviert.

## Akzeptanzkriterien

CLOCK_MONOTONIC um die vier tatsächlichen terminalen Process-APIs messen; nur ein gültiger Return1 und eine Laufzeit strikt über dem konfigurierten Budget versiegeln ENGINE_TIMEOUT vor Common-Completion. Ungültige Returns behalten ihre native Fehlerklassifikation.

## Implementierungsentscheidung und Begründung

`modsecurity_engine_call_budget_ms` akzeptiert dezimale Millisekunden; null deaktiviert die Messung, Vererbung in location/server/main verwendet den normalen Unset-Sentinel. Erkennung erst nach Rückkehr, kein harter Abbruch. Der P3-Pfad erzeugt technische Fehler-Events und verhindert doppelte Timeout-Events.

## Geänderte Dateien

NGINX SOURCE_MAP, Common-Header und Access-/Header-/Body-/Module-Aufrufstellen; Budget-Bridge und tatsächliche technische Emitter-Tests; Request-C-Fixture-Anpassungen. Reiner Arithmetikheader und vollständige P3-Source-Caller-Tests wurden separat committed.

## Ausgeführte Befehle

Die RTK-umhüllte Python-unittest-Auswahl für test_nginx_engine_budget_bridge, test_nginx_native_technical_events, test_nginx_p3_technical_source, test_nginx_request_native_results und test_nginx_request_error_events bestand frisch38 Tests (root-budget-callers-final-focus.log, exit0). Der vorherige Source-Teil bestand71 kontrollierte C17-Tests. URI-/Request-Error-/Native-Limit-Fokus bestand frisch32 Tests. Echte Common-Zustände und JSONL-Serialisierung mit C17-Warnungen als Fehler dienen diesen Tests.

## Security-Auswirkung

Keine Regel-ID erfinden; ungültige oder fehlgeschlagene native Returns nicht durch Laufzeit verdecken. Clock-Fehler sind CONNECTOR, nicht Timeout. Phase-Completion und Downstream-Weitergabe bleiben hinter echtem Erfolg versiegelt.

## Runtime-Evidence

Keine neue native Binary-/Modul-Ausführung behaupten. Vorhandene Runtime-Diagnose besitzt alte Artefakt-Provenienz und zertifiziert diese Änderungen nicht.

## Bekannte Einschränkungen

Nur synchrone terminale P1-/P2-/P3-/P4-Process-Aufrufe sind erfasst, nicht Connection-/URI-/Append-/Logging-/Getter-/Cleanup-APIs. Ein hängender Engine-Aufruf wird nicht unterbrochen.

## Verbleibende Risiken

Clock-Verhalten, Directive-Vererbung und native Wire-Effekte vor/nach Commit brauchen frischen Artefakt-/Config-/Runtime-Nachweis. Source-Tests allein schließen Required-Coverage nicht.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer vollständiger Build, echte begrenzte Fault-Invocations, integrierte97 Canonical, Remote-CI/Sonar und geschützter Trusted-Base-Lauf: Source- und Canonical-Integration sind noch in Arbeit.

## Finaler Diff- und Review-Status

Gezielter Source-Budget-/Emitter-Umfang; unabhängige BEGIN-/Finish-/Cleanup-/Orchestrierungsarbeit bewusst nicht gestagt. Required-Auswahl, MRTS und Gitlinks unverändert.
