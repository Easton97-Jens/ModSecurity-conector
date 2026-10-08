# Change Record: CR-20261008-nginx-native-cleanup-and-technical-faults

**Sprache:** [English](CR-20261008-nginx-native-cleanup-and-technical-faults.md) | Deutsch

Nur Source-Nachweis; die integrierte native Runtime bleibt ungeprüft.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-cleanup-and-technical-faults |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `f0aa2fe099837d44d760012d28bd247729c73120` |

## Motivation und Problemstellung

Required-Fehlerfälle benötigen echte technische und Cleanup-Beobachtungen. Bisher fehlten diese Beobachtungen bei nativen Logging- und Transaktionserzeugungsfehlern.

## Akzeptanzkriterien

Die tatsächlich erhaltene Common-Fehlerklasse ausgeben; Cleanup erst nach Rückkehr von Common-Cleanup und nativem Cleanup beobachten. Keine nachträgliche HTTP-Antwort aus Logging, kein doppeltes natives Cleanup und kein Zugriff auf die freigegebene native Transaktion.

## Implementierungsentscheidung und Begründung

Common-Cleanup-Beobachtungskonstruktor und vorhandenen JSONL-Writer verwenden. Den Abschluss des nativen Cleanup erfassen, den nativen Zeiger löschen, dann den tatsächlichen Common-Übergang serialisieren. Protokollfehler vor Aufnahme erhalten keine erfundene Transaktion; native Allokationsfehler erhalten ihren Connector-Fehler vor echtem Cleanup.

## Geänderte Dateien

`connectors/nginx/SOURCE_MAP.json`, `src/ngx_http_modsecurity_module.c`, `src/ngx_http_modsecurity_log.c` unter diesem Connector; `tests/test_nginx_native_cleanup_bridge.py`, `tests/test_nginx_native_logging.py`; dieses EN/DE-Paar. Der bereits committete Cleanup-Header wird in den Materialisierungsvertrag aufgenommen.

## Ausgeführte Befehle

RTK-gekapselter Python-Unittest-Fokus: native Cleanup-Bridge (5), natives Logging (8), technische Fehlerereignisse (4), Engine-Aufrufbudget (5), Response-Header-Aufrufer (5): 27 Tests, Exit 0. Evidence: externes `root-cleanup-fault-callers-final-focus.log`. Change-Record- und Git-Whitespace-Prüfungen sind vor dem Commit erforderlich.

## Security-Auswirkung

Writer und Common-Validierung bleiben strikt. Ein fehlgeschlagener Cleanup-Beobachtungsschreibvorgang kann Cleanup nicht rückgängig machen und wird ausdrücklich protokolliert; fehlende Evidence muss Canonical-Zertifizierung weiterhin verhindern. Keine Payload, Secrets, erfundene Rule-ID oder Trusted-Root-Behauptung.

## Runtime-Evidence

Keiner für das neue integrierte Modul. Tests kompilieren aktuellen Source mit kontrollierten Host-/Native-Fixtures; das sind keine echten NGINX-Requests und keine Canonical-Coverage.

## Bekannte Einschränkungen

Der Cleanup-Hook ist void. Seine Beobachtung kann einen früheren Writerfehler nicht reparieren oder die bereits sichtbare Antwort ändern. Vollständige Materialisierung, frischer Modulbuild und nativer Lifecycle bleiben erforderlich.

## Verbleibende Risiken

Pool-Cleanup-Registrierungs- und Allokationsfehler hängen weiterhin vom echten Host-Lifecycle ab. Strikte Reader und Runtime-Fixtures müssen die exakt ausgegebenen Identitäten und erhaltenen Ursachen prüfen.

## Nicht ausgeführte Prüfungen mit Begründung

Kein frischer integrierter nativer E2E, vollständiger Lint oder geschützter Exact-Head-Workflow: Canonical-Anbindung und frischer Build sind noch unvollständig; Trusted-Base-/Host-Freigabe ist separat.

## Finaler Diff- und Review-Status

Cleanup-/Logging-Änderungen und den ausdrücklichen Materializer-Eintrag geprüft. Unabhängige offene Config- und Raw-H1-Arbeit ausgeschlossen. Dieser reine Source-Nachweis schließt keinen Required-Record.
