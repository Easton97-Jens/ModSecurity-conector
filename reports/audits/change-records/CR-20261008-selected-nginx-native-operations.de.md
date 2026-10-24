# Change Record: CR-20261008-selected-nginx-native-operations

**Sprache:** [English](CR-20261008-selected-nginx-native-operations.md) | Deutsch

Geschlossener Parent-Dispatcher und Sourceadapter; keine Runtime-Promotion.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-selected-nginx-native-operations |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `4a28d86fa0d052397e74f0843ca6931e3dd17cae` |

## Motivation und Problemstellung

Die neuen 42 ausgewählten nativen NGINX-Aufrufe auf echte geschlossene Host-Treiber routen, ohne bestehenden 52-Fall-Collector oder drei Konfigurationsoperationen zu ändern.

## Akzeptanzkriterien

Exakt fünf Gruppen/42 strikte Katalogdeskriptoren, gemeinsame Auswahlvariable, frische externe Outputs/Projektionen, echte Source-SHAs/Gitlink, erforderliche Fault-Fixtures, tatsächliche Exits, originale Receipt-Seals und NOT_EXECUTED-Ausgabe. Kein nativer Prozess/Build/E2E für diesen Slice.

## Implementierungsentscheidung und Begründung

Der Dispatcher akzeptiert nur exakte native_invocations.nginx-Deskriptoren einschließlich zwei Aliasen und neun geschlossenen Overrides; Katalogbefehle sind nie ausführbar. Er verwendet NO_CRS_SELECTED_CASE_IDS, BUILD_ROOT, RESULTS_DIR, NGINX_PREFIX, FRAMEWORK_ROOT und NO_CRS_RUN_ID. Output liegt unter BUILD_ROOT/host-runtime/native-operations-<run>/<case>, mit frischen Projektionseltern je Fall und unabhängigen E-Kindprojektionswurzeln. Der Sourceadapter erhält Original-Source-Receipts und liefert status/canonical_status NOT_EXECUTED. native_operation_receipt enthält schema_version1/case/run/operation/native mode/absolutes bundle_root/optionales source_record_id, invocations main|at|over mit relativem receipt_path und SHA256, verpflichtendes namespaced source_sha256 aus Framework required_source_paths(case_id) sowie E-Eltern-Receipt-Pfad/Hash. Echte Parent-/Framework-/MRTS-SHAs und der Parent-Framework-Gitlink werden getrennt erfasst.

## Geänderte Dateien

Neu: ci/runtime/lifecycle/run-selected-nginx-native-operations.py, nginx-native-operation-source.py, tests/test_nginx_native_operation_dispatch.py und dieser gepaarte Record. Kein bestehender Collector, Wrapper, Treiber, Framework-, MRTS- oder Root-Integrationsfile bearbeitet.

## Ausgeführte Befehle

RTK-gewraptes natives Scaffold create; fokussiert `rtk proxy "${PARENT_PYTHON}" -m unittest discover -s tests -p test_nginx_native_operation_dispatch.py`: initial Exit1 wegen fehlender neuer Implementierung, final Exit0/acht Tests (keine nativen Prozesse). Ein zweiter fehlgeschlagener Orchestrierungscheck zeigte geschützte .git-Platzhalterverzeichnisse; die repositorynative Erkennung tatsächlicher Checkouts korrigierte dies. Exakter Vergleich mit C-Katalogdeskriptoren: 42, Exit0. AST-Parse dreier Dateien: Exit0. `rtk proxy "${PARENT_PYTHON}" -m ruff --version`: Exit1, nicht verfügbar. Prüfung erforderlicher Env-Präsenz: alle fünf false, keine Werte ausgegeben. Finale Record-/Paar-/Diffprüfungen im Handoff erfasst.

## Security-Auswirkung

Geschlossenes Befehls-/Fallrouting; strikte Ablehnung doppelter Auswahl/Katalogfälle; externer frischer Zustand; alle Receipt-Pfadkomponenten NOFOLLOW, begrenzte owner-only reguläre Single-Link-Blätter; sicherer Append erhält bestehende Zeilen, lehnt ausgewählte Duplikate ab und nutzt exklusiven nichtblockierenden Lock. Source-Hashes nutzen die geschlossene Namensraumliste des Readers, nie beliebige receiptgewählte Pfade. Erforderliche native Fault-Bibliotheken scheitern geschlossen.

## Runtime-Evidence

Kein nativer Laufzeittest/Build ausgeführt. Gemockte Subprozess-Receipts beweisen nur Dispatcher-Orchestrierung und erhalten Treiber-Exit7/0 als NOT_EXECUTED, keinen Engine-/Host-PASS. Root besitzt integrierten Runtime-Slot und kanonische Promotion.

## Bekannte Einschränkungen

Abhängig von integrierten tatsächlichen Treibern und Framework-API nginx_native_operation_bundle.py required_source_paths; nicht in diesen isolierten Parent-Slice kopiert oder cherry-picked. Eventkindnamen at/over zeigen auf originale Verzeichnisse und Runsuffixe at255/over256; metadata main auf long-query. Originales Eltern-Envelop bleibt versiegelt. Fehlende Receipts scheitern geschlossen statt Evidenz zu erfinden.

## Verbleibende Risiken

Root muss Collector/Wrapper verdrahten und tatsächliche NGX_NATIVE_INPUT_FAULT_LIBRARY, NGX_NATIVE_BEGIN_FAULT_LIBRARY, NGX_NATIVE_WRITE_FAULT_LIBRARY, NGX_NATIVE_FINISH_FAULT_LIBRARY und NGX_NATIVE_ENGINE_BUDGET_FAULT_LIBRARY für ihre exakten Fälle exportieren. Kein Fallback auf Ausführung ohne Fault. Vollständige integrierte Reader-/Treiber-/Runtime-Verifikation bleibt ausstehend.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Laufzeittest, Build, vollständiges E2E, keine Framework-/MRTS-Tests, Veröffentlichung oder Push gemäß Umfang. Parent-Ruff nicht verfügbar; kein Paket installiert. Integrierte Bilingual-Linkprüfung erfordert Roots materialisierte Framework-Grenze; isolierter Worktree hat 22 bekannte bestehende fehlende Ziele.

## Finaler Diff- und Review-Status

Begrenzter lokaler Review betrifft nur fünf neue Dateien; finale Prüfergebnisse und lokaler Commit-SHA werden Root übergeben. Keine bestehende52/config3-Mutation und keine Shared-File-Änderung; keine externe Auslieferung behauptet.
