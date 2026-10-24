# Change Record: CR-20261009-nginx-sonar-c-quality-20261009

**Sprache:** [English](CR-20261009-nginx-sonar-c-quality-20261009.md) | Deutsch

Begrenzter isolierter Patch; keine native Runtime- oder Scanner-Closure-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-sonar-c-quality-20261009 |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Frische C-Befunde erfordern enge Strukturänderungen bei Erhalt tatsächlicher nativer Beobachtungen, Intervention-Ownership und Post-Return-Budget-Priorität.

## Akzeptanzkriterien

Bestehende Caller- und Common-Serializer-Kontrollen erhalten; ungültige Socket-Metadaten ablehnen; alle P4-Completion-Prädikate und terminalen Event-/Status-Semantiken erhalten.

## Implementierungsentscheidung und Begründung

retained/seen/supplied/append_calls in eine konstante Input-Struktur bündeln (sieben Parameter); nur bounded Rule-ID-Parsing extrahieren; verschachtelte Bedingungen mit identischem Kurzschlussverhalten auflösen; Deklarationen teilen und Loop-Scope reduzieren. Beide Socket-Output-Strukturen initialisieren, ohne Rollen-/Socket-Prüfungen zu lockern.

## Geänderte Dateien

`connectors/nginx/src/ngx_http_modsecurity_module.c`, `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`, `connectors/nginx/src/ngx_http_modsecurity_phase4_observation.h`; `tests/fixtures/nginx_engine_budget_fault.c`, `tests/fixtures/nginx_phase4_observation.c`, `tests/fixtures/nginx_response_body_limit.c`, `tests/fixtures/nginx_write_fault.c`; `tests/test_nginx_cleanup_observation.c`, `tests/test_nginx_native_intervention_chain.py`, `tests/test_nginx_write_fault_socket_scope.py` und dieses EN/DE-Paar.

## Ausgeführte Befehle

Root-Integration:Der bestehende Inline-Rule-ID-Quellguard scheiterte nach der Helper-Extraktion zunächst (65 Tests, ein Fehler, Exit1). Der Guard prüft jetzt den tatsächlichen begrenzten Helper und die Aufrufreihenfolge, mit Negativkontrollen für fehlende/späte/unbegrenzte/zusätzlich bedingte Extraktion. Der integrierte RTK-Fokus über neun Module bestand anschließend66 Tests/5,494s/Exit0 ohne SKIPs. Zusätzlich geändert ist `tests/test_nginx_upstream_security_contract.py`. Dies bleiben Quell-/kompilierte Unit-Prüfungen, keine frische NGINX-Runtime-Evidenz.

Abschließende Zusatzprüfungen:alle sieben betroffenen C-Fixtures/Cleanup-Dateien C17-Syntax Exit0; drei geänderte Python-Dateien py_compile Exit0; `tests.test_change_record` und `tests.test_prepare_reviewed_framework_handoff`:39 Tests, Exit0; Record-Archiv-Check Exit0; Pfad-/Linkdiagnostik für die vier neuen Records:0 Fehler. `make check-bilingual-docs` und `make check-doc-links` scheiterten an bestehenden Submodule-Links, da das Framework-Verzeichnis im isolierten Worktree nicht befüllt ist. Der explizite externe FRAMEWORK_ROOT ersetzt diese relativen Links nicht. Keine fehlende Dependency wurde verändert oder eine Prüfung gelockert.

Alle Befehle nutzten RTK. Bestehende Charakterisierung mit sechs Suites:27 Tests, Exit0. Sieben Focus-Suites nach Änderungen:34 Tests, Exit0. Direkte C17-Cleanup-Kompilation und Executable:Exit0. Suite-Namen: `tests.test_nginx_phase4_observation`, `tests.test_nginx_phase4_native_body_source`, `tests.test_nginx_native_intervention_chain`, `tests.test_nginx_engine_budget_bridge`, `tests.test_nginx_response_body_limit`, `tests.test_nginx_common_input_fault_scope`, `tests.test_nginx_write_fault_socket_scope`. Framework-Umgebung an `7db219af6b6e911b73de8b437f82e63efdb06bde` gebunden; temporäre Dateien extern. Dokumentationsprüfung folgt separat.

## Security-Auswirkung

Keine Native-Result-, Rollen-, Pfad-, Payload-, Status- oder Evidence-Grenze wird gelockert. Socket-Kontrollen prüfen Syscall-Fehler, kurze Outputs, falsche Familien/Adressen/Port, falsche UID/PPID/Master und unvollständig befüllte Outputs. Der Konstruktor verlangt weiterhin tatsächliches Native1 und Common-completed P4.

## Runtime-Evidence

Keine. Kontrollierte C17-Host-/Syscall-Tests und tatsächliche Common-Serialisierung sind keine gehostete native Lifecycle-Evidence.

## Bekannte Einschränkungen

Das S836-Signal belegt keine reale Kernel-Vertragsverletzung. Nullinitialisierung ist defensiv. Keine Scanner-Closure wird behauptet. Die Inherited-FD-Security-Migration besitzt einen separaten Record.

## Verbleibende Risiken

Frische integrierte Source-Prüfungen und Sonar-Readback bleiben erforderlich; Extraction-Test-Fixtures müssen den tatsächlichen Helper erhalten.

## Nicht ausgeführte Prüfungen mit Begründung

Native Build/Runtime und Veröffentlichung waren ausgeschlossen und bleiben Root-owned. Kein Scanner wurde aus dem geänderten Checkout gestartet.

## Finaler Diff- und Review-Status

Focus-Tests und Whitespace-Prüfung bestanden. Änderungen verbleiben unstaged in einem isolierten Worktree; keine Git-Schreiboperation erfolgte.
