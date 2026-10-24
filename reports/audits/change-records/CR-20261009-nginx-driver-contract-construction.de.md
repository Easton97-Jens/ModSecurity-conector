# Change Record: CR-20261009-nginx-driver-contract-construction

**Sprache:** [English](CR-20261009-nginx-driver-contract-construction.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-driver-contract-construction |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |

## Motivation und Problemstellung

Sonar meldete wiederholte Ablehnungsfelder und Sequenzabläufe zwischen Parent-Produzenten und unabhängigen Framework-Verträgen. Entdopplung der Parent-Konstruktion bei unveränderter Unabhängigkeit. Validator-Erwartungen werden nicht in einen Produzenten importiert.

## Akzeptanzkriterien

Alle neun vollständigen Ablehnungs-Dictionaries, Feldtypen und Schlüsselreihenfolgen sowie alle 22 Sequenz-IDs, Status-Tupel und Aufrufreihenfolgen bleiben erhalten. Unabhängige Framework-Parität und Kontrollen veränderter Werte müssen bestehen. Keine Änderung an Auswahl, Validator, Beobachtung, Receipt, Freshness oder Runtime-Verhalten.

## Implementierungsentscheidung und Begründung

Der lokale reine Konstruktor `rejection_contract` zentralisiert feste Config-only-Ablehnungsfelder und erzeugt pro Aufruf eine eigene Diagnoseliste. Fallspezifische Direktiven, Werte und Diagnosen bleiben explizit. Sequenzabläufe gruppieren ausschließlich benachbarte gleiche Eingaben vor der Überführung in das bestehende geordnete Dictionary. Produzenten-Erwartungen bleiben unabhängig verfasst; Validatoren bleiben unverändert. Keine neue Helper-Quelldatei oder Source-Capture-Grenze.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`
- `tests/test_nginx_driver_contract_tables.py`
- `reports/audits/change-records/CR-20261009-nginx-driver-contract-construction.md`
- `reports/audits/change-records/CR-20261009-nginx-driver-contract-construction.de.md`

## Ausgeführte Befehle

Alle Befehle verwenden `rtk proxy`, den gewählten Parent-Virtualenv-Python, externe `TMPDIR` / `PYTHONPYCACHEPREFIX` und `PYTHONNOUSERSITE=1`. `$PARENT_PYTHON` bezeichnet diesen Interpreter.

- Vor Refactoring: `$PARENT_PYTHON -m unittest -v tests.test_nginx_driver_contract_tables`: Exit 0, sechs Tests. Vollständige Basis-Snapshots, unabhängige Framework-Parität und negative Kontrollen veränderter Werte/Reihenfolgen bestanden auf unveränderten Drivern.
- Native Scaffold-Erstellung: `ci/tools/new-change-record.py create --name nginx-driver-contract-construction --base-revision 240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee --date 2026-10-09`: Exit 0.

Nach Refactoring: `$PARENT_PYTHON -m unittest -v tests.test_nginx_driver_contract_tables tests.test_nginx_configtest_driver tests.test_nginx_selected_configtest_wiring tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases tests.test_nginx_native_operation_dispatch`: Exit 0, 87 Tests in 71.165s, keine Skips. Sowohl `FRAMEWORK_ROOT` als auch `NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT` benennen explizit den vorhandenen gepinnten Framework-Checkout. Der frühere Lauf mit 86 Tests bestand mit einem ausgelassenen Registry-Check; der finale Lauf führte diesen Check und den neuen Konstruktor-Unabhängigkeitstest aus.

`$PARENT_PYTHON -m py_compile` für die drei Python-Dateien, `ci/tools/new-change-record.py check` und `git diff --check`: alle Exit 0. Die Archivprüfung validiert ausschließlich die Struktur. Logs: `driver-contract-characterization-before.log`, `driver-contract-focus-after.log`, `driver-contract-focus-final.log`, `driver-contract-static.log`, mit beobachteten Exitdateien im externen Task-Analyseverzeichnis. Dies sind Eingabevertrags-/Unit-Prüfungen, keine native NGINX-Ausführung.

## Security-Auswirkung

Keine Änderung an Autorisierungs-, Isolations- oder Validierungskontrollen. Der Konstruktor erzeugt ausschließlich Eingaben. Beobachtete Exitcodes, Diagnosen, Identitäten und Fault-Receipts erfordern weiterhin unabhängige Prüfungen. Kein synthetisches PASS und keine synthetische Runtime-Evidence.

## Runtime-Evidence

Keine in diesem isolierten Refactoring. Kontrollierte Unit-Executables sind kein echter NGINX-Runtime-Nachweis. Die Root-Integration verantwortet den anschließenden echten Exact-Head-Lauf.

## Bekannte Einschränkungen

Der isolierte Worktree enthält kein ausgechecktes Framework-Submodul. Paritätstests lesen explizit den vorhandenen exakt gepinnten separaten Framework-Checkout. Dadurch werden weder fehlende Dokumentations-Linkziele ausgecheckt noch Runtime-Verhalten bewiesen.

## Verbleibende Risiken

Frische integrierte Prüfungen und Sonar-Readback bleiben vor Delivery-Aussagen erforderlich. Erwartete Eingaben bleiben unabhängig von Produzenten-Beobachtungen und Framework-Validatoren.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Builds, Runtime-Probes, privilegierte Läufe, Ports, Full-E2E, Scanner-Veröffentlichung, Git-Commit/Push oder Framework-/MRTS-Schreibzugriffe. Vollständige Dokumentationsprüfungen erfordern ausgecheckte Framework-Integration; Archivstruktur und manuelle EN/DE-Parität sind getrennte Prüfungen. Keine Abhängigkeits-/Toolchain-Installation.

## Finaler Diff- und Review-Status

Nur die zwei Produzentendateien, das neue Charakterisierungsmodul und das EN/DE-Record-Paar wurden geändert. Root-Review/Integration bleiben erforderlich. Keine Profilverkleinerung, Ausschlüsse, reine Identifier-Umbenennung zur Umgehung oder abgeschwächtes Quality Gate.
