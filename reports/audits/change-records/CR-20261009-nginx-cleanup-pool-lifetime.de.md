# Change Record: CR-20261009-nginx-cleanup-pool-lifetime

**Sprache:** [English](CR-20261009-nginx-cleanup-pool-lifetime.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-cleanup-pool-lifetime |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |

## Motivation und Problemstellung

NGINX setzt `r->pool` vor Request-Pool-Cleanup-Callbacks auf NULL. Cleanup allokierte bisher Method-/URI-Strings durch `ngx_http_modsecurity_event_request_metadata` mit diesem gelöschten Zeiger. Der auslösende echte Lauf meldete Worker `SIGSEGV 11` und null Cleanup-Events. Eine deterministische C-Fixture weist die ungültige Allokation unabhängig nach.

## Akzeptanzkriterien

Echte Request-Identität und genau eine wahrheitsgetreue Cleanup-Beobachtung ohne Allokation aus gelöschtem Pool erhalten. Common-/Native-Reihenfolge, Fehler, strikte Serialisierung, URI-Grenzen und Query-Redaktion erhalten. Snapshot-Fehler vor Transaktionszulassung ablehnen.

## Implementierungsentscheidung und Begründung

Exakte längenbegrenzte Methode und ursprüngliche URI bei Context-Erstellung mit aktivem Pool kopieren; zwei C-String-Zeiger im Context speichern. Pool-Speicher bleibt während aller Cleanup-Callbacks aktiv. Cleanup verwendet gespeicherte Identität ohne `r->pool`. Leere Eingaben bleiben leer; NULL-Daten, Überlauf und Allokationsfehler verhindern Context-Erstellung. Identität gehört der zugelassenen Transaktion, auch wenn spätere interne Redirects aktuelle Methodendaten ändern. Bestehende Common-Projektion und Validatoren bleiben unverändert. Keine neue Source-Datei oder SOURCE_MAP-Eintragung.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_nginx_native_cleanup_bridge.py`
- `reports/audits/change-records/CR-20261009-nginx-cleanup-pool-lifetime.md`
- `reports/audits/change-records/CR-20261009-nginx-cleanup-pool-lifetime.de.md`

## Ausgeführte Befehle

Befehle verwendeten `rtk proxy` im isolierten Parent-Worktree; `$PARENT_PYTHON` bezeichnet dessen bestehenden Virtualenv-Interpreter. Logs und temporäre Dateien liegen extern im Task-Analyseverzeichnis `cleanup-pool-lifetime`.

- RED: `$PARENT_PYTHON -m unittest -v tests.test_nginx_native_cleanup_bridge.NativeCleanupBridgeTests.test_destroyed_pool_cleanup_retains_exact_request_metadata_without_allocation`; Exit 1, ein erwarteter Fehler: unveränderte Source versuchte NULL-Pool-Allokation; sichere Fixture lieferte 19. `red.log`.
- GREEN: `$PARENT_PYTHON -m unittest -v tests.test_nginx_native_cleanup_bridge tests.test_nginx_native_technical_events tests.test_nginx_bounded_event_uri tests.test_nginx_native_intervention_chain tests.test_nginx_request_error_events`; Exit 0, 48 Tests in 5.098s, keine SKIPs. `affected.log`. Echte Snapshot-/Cleanup-/Phase-Writer-Funktionen und Common-Zustand/Serialisierung laufen; nur Host-Allokation/Dateischreiben und Native-Cleanup-Schnittstellen sind kontrolliert. Tests prüfen nicht-NUL-terminierte Ausschnitte, Identität nach Änderung ursprünglicher Bytes, leere Eingaben, Allokations-/NULL-/Überlaufablehnung, Wiedereintritt bei gelöschtem Pool, Query-Redaktion, lange URI-Projektion, fehlenden Native-Zeiger und terminale Fehler.
- `NGINX_C_STD_PROFILE=c17 bash ci/checks/connectors/nginx/check-nginx-c-standards.sh`; Exit 0, `PASS: nginx_c_standards c17 compile completed`, sämtliche gelisteten Sources mit `-Wall -Wextra -Werror`. Bestehende generierte NGINX-1.31.6-Header und ModSecurity-Header beweisen ausschließlich Kompilierung.
- `$PARENT_PYTHON ci/checks/connectors/nginx/check-nginx-common-adoption.py`; Exit 0. `adoption.log`.
- `rtk proxy git diff --check`; Exit 0.
- Natives `ci/tools/new-change-record.py create` erzeugte dieses Paar ab der exakten Basis; Exit 0.

## Security-Auswirkung

Beseitigt eine durch Requests erreichbare Cleanup-Allokation aus ungültigem Pool. Metadaten bleiben Request-basiert; keine erfundenen Events oder abgeschwächten Prüfungen. Snapshot-Fehler verhindern Zulassung; gespeicherter Speicher gehört dem bestehenden Request-Pool.

## Runtime-Evidence

Der gemeldete Absturz begründet den Fix. Dieser Worker führte keinen gehosteten NGINX-Lifecycle aus und behauptet keinen Runtime-PASS. Frischer integrierter Build und Root-Master/nobody-Worker-Ausführung bleiben erforderlich.

## Bekannte Einschränkungen

Die Fixture modelliert Pool-Allokation/Löschung statt den vollständigen NGINX-Destruktor auszuführen. Header-Kompilierung beweist Source-Kompatibilität, keine frischen Binaries oder gehostetes Cleanup.

## Verbleibende Risiken

Unabhängige Integration und tatsächliche Cleanup-Prüfung bleiben erforderlich. Zwei zusätzliche Strings verbleiben bis zur Destruktion im Request-Pool. Framework, MRTS, Required97-Auswahl und Canonical-Validatoren bleiben unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Kein kompletter Build, gehostete Runtime, Cache-Änderung, vollständige Repository-Suite, CI, Sonar, Git-Delivery oder geschützte Host-Aktion durch diesen Worker; dies gehört dem Integrationskoordinator. Vollständige Dokumentationslinks benötigen hier fehlende befüllte Framework-Pfade. Archivstruktur und zweisprachiger Inhalt werden separat geprüft.

## Finaler Diff- und Review-Status

Die fünf gelisteten Dateien werden mit RED/GREEN- und C17-Nachweisen zur unabhängigen Integrationsprüfung übergeben. Kein Worker-Commit oder Push. Vollständiger E2E und Delivery bleiben unbestätigt.
