# Change Record: CR-20261008-nginx-native-dispatch-overrides

**Sprache:** [English](CR-20261008-nginx-native-dispatch-overrides.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-dispatch-overrides |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `9dcd35c7e380c1fc46d12bfd1fa53cfacb999775` |

## Motivation und Problemstellung

Read-only-Registry-Audit fand drei veraltete Parent-Dispatcher-Deskriptoren: Body-Pointer-Ablehnung erfolgt tatsächlich in Phase1; Soft-Budget-Timeout vor Commit erfolgt in Phase1; Clean-Shutdown hat sichtbaren HTTP200 unabhängig von Prozess-Exit0. Exakter Deskriptorvergleich lehnte den aktuellen Framework-Katalog vor nativer Invocation ab.

## Akzeptanzkriterien

Alle42 aktuellen Framework-Deskriptoren einschließlich dieser drei genehmigten Overrides exakt treffen. Fehlende, falsche oder boolesche Phase-/Status-Overrides ablehnen. Generische Case-Erwartungen, alle anderen Dispatch-Kontrollen und strikte fehlende Fault-Fixtures erhalten. Kein Build oder native Runtime.

## Implementierungsentscheidung und Begründung

Nur die CONTRACTS-Override-Tabelle wird korrigiert: body_size_nonzero_with_null_data Phase1/Status400; engine_timeout_before_commit Phase1/Status504/keineRule/native504/engine_timeout; clean_shutdown nativer Status200. Bestehende Operationen, echte CLI, Source-Sealing, Fault-Anforderungen und Selected-Case-Guards bleiben unverändert. Kein Katalog oder Schema wird geändert.

## Geänderte Dateien

Nur `ci/runtime/lifecycle/run-selected-nginx-native-operations.py`, bestehendes `tests/test_nginx_native_operation_dispatch.py` und dieses EN/DE-Paar. Zentraler Collector, Wrapper, Root-Integration, Framework, MRTS und Gitlinks bleiben unberührt.

## Ausgeführte Befehle

Test-first `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT=<current-framework-root> python -m unittest tests.test_nginx_native_operation_dispatch.DispatcherTests.test_current_native_phase_and_clean_shutdown_overrides tests.test_nginx_native_operation_dispatch.DispatcherTests.test_exact_current_framework_registry_selects_all42 -v` endete mit Exit1: drei Deskriptor-Assertions schlugen fehl und die echte Katalogselektion wurde abgelehnt.

Nach begrenzter Korrektur endete `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT=<current-framework-root> python -m unittest tests.test_nginx_native_operation_dispatch tests.test_nginx_selected_native_wiring tests.test_nginx_native_operation_collection -v` mit Exit0: 29 kontrollierte Tests ohne Skips. Der tatsächlich aktuelle Framework-Katalog wurde gelesen, nicht aus Dispatcher-Konstanten rekonstruiert. Die Tests nutzten die Parent-eigene Python-Umgebung. Parent-Archiv- und Whitespace-Prüfungen werden im Handoff genannt.

## Security-Auswirkung

Keine Validierungslockerung oder Produkt-Security-Remediation. Exakter geschlossener Deskriptorvergleich lehnt degradierte oder injizierte Overrides weiterhin ab, einschließlich boolescher Werte statt Phase-Integer. Fault-Library-Autorität und Originalbyte-Retention bleiben strikt.

## Runtime-Evidence

Nur reine Deskriptor-, Orchestrierungs- und Retained-File-Fixtures. Kein NGINX-Build/-Prozess/-Request, Canonical-PASS oder Exact-Head-Runtime-Claim.

## Bekannte Einschränkungen

Der Katalogparitätstest benötigt einen tatsächlich aktuellen Framework-Checkout oder explizites NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT; fehlen beide, erfolgt Skip. Der dokumentierte29-Test-Aufruf übergab den aktuellen Checkout und hatte keine Skips.

## Verbleibende Risiken

Source-Whitelist, Canonical-Faktenvertrag-Integration und serialisierte native Verifikation bleiben Koordinator-eigen. Deskriptorgleichheit beweist nur Planung/Wiring.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, native Runtime, vollständige E2E oder Remote-CI/Sonar: außerhalb dieses begrenzten Besitzes. Keine Toolinstallation, Pins, History-Rewrite oder Root-Worktree-Mutation.

## Finaler Diff- und Review-Status

Vier begrenzte Dateien geprüft. Kein Invocation-Algorithmus, Selektionsscope, generische Framework-Erwartung oder nativer Event wurde geändert. Normaler isolierter Commit geht an den Koordinator.
