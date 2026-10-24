# Change Record: CR-20261008-nginx-selected-native-host-wiring

**Sprache:** [English](CR-20261008-nginx-selected-native-host-wiring.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-selected-native-host-wiring |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `b7f3bb22a8ee5ebfe78a0f3b4fb3b32238200f91` |

## Motivation und Problemstellung

Vor Änderungen ergab read-only `select_cases('nginx', manifest, catalog, 'no_crs_baseline', 'full_lifecycle', 'http1')` gegen den aktuellen Source-Stand 97 ausgewählte Cases, darunter alle 42 nativen Deskriptoren. Der Host-Wrapper rief nur Framework-Smoke und Parent-Configtests auf; der native Dispatcher wurde nie aufgerufen.

## Akzeptanzkriterien

Den vorhandenen geschlossenen nativen Dispatcher nach Smoke und Configtests aufrufen, Selection-/Run-/Source-Eingaben und fünf obligatorische Fault-Library-Eingaben erhalten, Smoke > Config > Native als Exitpriorität bewahren und fehlende ausgewählte Fixtures strikt behandeln. Dispatcher, Baseline/Collector, Framework-Proof, Artefakte und Runtime-Policy nicht ändern.

## Implementierungsentscheidung und Begründung

`run-nginx-selected-host.sh` ruft jetzt Smoke, Configtests und `run-selected-nginx-native-operations.py` in dieser Reihenfolge auf und erfasst jeden tatsächlichen Exit. `run_framework_host` setzt bereitgestellte Selected-IDs/Fixtures, Run-ID, Projection-Parent, Parent-/Framework-Tupelfelder und fünf Fault-Library-Variablen nach Component-Provisioning erneut. Ein explizites Caller-`NGINX_PREFIX` wird bedingt erneut gesetzt; bei fehlendem Caller-Präfix bleibt das tatsächliche provisionierte Snapshot-Präfix statt eines erfundenen leeren Werts erhalten. BUILD_ROOT, RESULTS_DIR und FRAMEWORK_ROOT bleiben gleich. Der unveränderte Dispatcher ermittelt echte Git-Identitäten und erzeugt frische isolierte Projection-Children.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-selected-host.sh`, `ci/runtime/lifecycle/run-connector-stage.sh`, neu `tests/test_nginx_selected_native_wiring.py` und dieses EN/DE-Paar. Roots `run-no-crs-baseline.sh`, Authority/Finalizer/Schema und Collector-Integration werden nicht geändert. Keine Framework-/MRTS-/Gitlink-Änderungen.

## Ausgeführte Befehle

`rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_selected_native_wiring` endete zunächst mit 1 und sieben fehlgeschlagenen Assertions, danach bestanden sechs Tests. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_selected_native_wiring tests.test_nginx_native_operation_dispatch tests.test_no_crs_selected_runner_wiring.NoCrsSelectedRunnerWiringTest.test_stage_rejects_missing_selected_cases_and_preserves_dispatch_controls` bestand mit 15 Tests, Exit 0 und ohne Skips. `rtk proxy sh -n ci/runtime/lifecycle/run-nginx-selected-host.sh ci/runtime/lifecycle/run-connector-stage.sh` und `rtk git diff --check` endeten mit 0. Parent-Record-Archive-/Paarprüfungen validieren nur Dokumentstruktur.

## Security-Auswirkung

Kein kataloggesteuerter Subprocess wird eingeführt: Der vorhandene geschlossene Dispatcher behält seine 42-Case-Whitelist, exakte Source-Receipts, sichere frische Outputs und obligatorische Ablehnung fehlender Fault-Libraries. `NGX_NATIVE_INPUT_FAULT_LIBRARY`, `NGX_NATIVE_BEGIN_FAULT_LIBRARY`, `NGX_NATIVE_WRITE_FAULT_LIBRARY`, `NGX_NATIVE_FINISH_FAULT_LIBRARY` und `NGX_NATIVE_ENGINE_BUDGET_FAULT_LIBRARY` werden ohne No-Fault-Fallback weitergegeben. Fehlende Dispatcher und native Fehler können nicht still zu Erfolg werden.

## Runtime-Evidence

Tests führen die tatsächlichen Parent-Shell-Skripte mit kontrollierten Smoke-/Config-/Native-/Provisioning-Kollaboratoren aus. Sie belegen nur Aufrufreihenfolge, Eingabeweitergabe und Exitverhalten; kein NGINX-Build, nativer Request, kanonisches PASS oder Exact-Head-Nachweis wird behauptet.

## Bekannte Einschränkungen

Die read-only 42-Case-Selection ist Source-Planung, kein Nachweis nativer Ausführung. Tatsächliche Binary-/Modul-/Fault-Library-Identität und kanonischer Bundle-Proof bleiben Aufgaben von Root/Framework.

## Verbleibende Risiken

Root muss Baseline-Collection-Autorität und finale Bundle-Retention noch verdrahten, echte neu gebaute Fault-Libraries bereitstellen und serialisierte native Verifikation ausführen. Der unveränderte Dispatcher versiegelt echte P/F/M-Revisionen unabhängig, statt Test-Tupelwerte zu übernehmen.

## Nicht ausgeführte Prüfungen mit Begründung

Build, Native-Runtime, vollständiges E2E, kanonische Required-Case-Verifikation und Remote-CI/Sonar wurden nicht ausgeführt: Diese Aufgabe erlaubt nur begrenztes Parent-Wiring und kontrollierte Tests. Bestehende isolierte Submodule-Linkfehler liegen außerhalb dieses Umfangs.

## Finaler Diff- und Review-Status

Die zwei eigenen Shell-Skripte, gezielten Tests und der gepaarte Nachweis wurden geprüft. Bestehende Smoke-/Config-Routen, strikter Selected-Fixture-Guard und Exitpriorität bleiben erhalten. Keine Runtime-Evidence oder PASS wurde erfunden; fremde Arbeit bleibt erhalten.
