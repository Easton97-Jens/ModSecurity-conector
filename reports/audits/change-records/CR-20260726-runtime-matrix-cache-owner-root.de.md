# Change Record: Parent-Runtime-Matrix-Cache-Owner-Root-Handoff

**Sprache:** [English](CR-20260726-runtime-matrix-cache-owner-root.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260726-runtime-matrix-cache-owner-root |
| Datum (UTC) | 2026-07-26 |
| Basis-Revision | 6ca7e1536ce7e93da68099db9c586b88852ff13e |
| Grenze | Parent-Runtime-Matrix- und vorbereitete Runtime-Environment-Snapshot-Handoffs, Parent-Regressionstests und dieses englisch/deutsche Change-Record-Paar mit Index. Der mitgeführte Framework-Gitlink ist bereits auf Parent-`master` gemergt; hier werden weder Framework- noch MRTS-Quellen geändert. |
| Finding-Verknüpfung | FND-CROSS-0008; FND-PARENT-0056; FND-CROSS-0001 bleibt offen, bis frische legitime Runtime-Evidence das strikte Terminal-Gate besteht. |

## Motivation und Problemstellung

Die vollständige Parent-Runtime-Matrix behält ihren Job-spezifischen
`BUILD_ROOT` für Logs, temporäre Dateien, Ergebnisse und isolierte Connector-
Ausführung. Cache-gestützte Apache- und NGINX-Connector-Builds gehören jedoch
nicht zu diesem Job-Root. Der Runner leitet jetzt einen engen Owner Root aus
dem verifizierten Component-Cache ab:

```text
CONNECTOR_COMPONENT_CACHE/builds/connectors
```

Er validiert diesen Root und jeden Apache-/NGINX-Build-Pfad vor dem Connector-
Aufruf. Ein Cache-Build-Pfad außerhalb des abgeleiteten Roots wird abgewiesen,
bevor `make` läuft. Für einen akzeptierten Pfad übergibt der Runner denselben
expliziten Root als `APACHE_BUILD_OWNER_ROOT` beziehungsweise
`NGINX_BUILD_OWNER_ROOT`; er weitet `BUILD_ROOT` nicht auf und deaktiviert den
Framework-Löschguard nicht.

Das direkte Target `runtime-matrix-all-runtime` erreicht den Framework-Runner
über einen vorbereiteten Invocation-lokalen Runtime-Environment-Snapshot.
Dieser Snapshot veröffentlicht nun für beide Connectoren denselben engen Owner
Root, sodass der direkte Runner bei einem legitimen Cache-Refresh nicht auf
seinen nicht zugehörigen Job-`BUILD_ROOT` zurückfallen kann.

Parent-PR #125 führt bereits Framework-Commit
`a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`, der die Framework-NGINX-Owner-
Root-Fähigkeit enthält. Diese Änderung verwendet diese Fähigkeit an der Parent-
eigenen Matrix-Grenze; sie verändert den Gitlink nicht über das normale
Branch-Update von `master` hinaus.

## Akzeptanzkriterien

- Cache-gestützte Apache- und NGINX-Refreshes erhalten denselben expliziten
  Owner Root aus `CONNECTOR_COMPONENT_CACHE/builds/connectors`.
- Ein Connector-Build-Pfad außerhalb dieses engen Roots schlägt fehl, bevor
  `make` aufgerufen wird.
- Der isolierte Job-`BUILD_ROOT` bleibt vom Cache-Owner-Root getrennt.
- Der Invocation-lokale Runtime-Environment-Snapshot veröffentlicht dieselben
  engen Apache- und NGINX-Owner-Roots für die direkte Runtime-Matrix-Ausführung.
- Bei einem Hosted-Producer-Fehler wird das begrenzte NGINX-`configure`-Log
  nur aus seinem festen erwarteten Pfad nach der bestehenden Prüfung auf
  reguläre Nicht-Symlink-Datei ausgegeben.
- Weder Löschguard, striktes Evidence-Gate, SonarQube-Cloud-Policy noch
  Branch-Schutz werden gelockert.
- Der aktualisierte exakte PR-#74-Head benötigt weiterhin vollständige Hosted-
  Producer-, Terminal-Gate-, SonarQube-Cloud-, Review- und Protected-
  Integration-Evidence.

## Implementierungsentscheidung und Begründung

Der betroffene Sink ist der Framework-Refresh-Löschguard. Die erzwungene
Invariante lautet: Ein Refresh-Target muss ein absoluter, sicher generierter
Pfad unter dem expliziten Connector-Cache-Build-Owner-Root sein. Die Parent-
Kontrolle verwendet den Framework-Helper für kanonischen Pfad-Containment vor
dem Dispatch; der Framework-Guard lehnt am Löschpunkt weiterhin unsichere,
relative, symlinked, Sibling- oder Systempfade ab.

Legitime vorbereitete Cache-Builds bleiben refreshbar. Ein Nicht-Cache-Build-
Root wird jetzt abgewiesen, statt einen Connector-Provisioning-Pfad mit nicht
zugehöriger Ownership zu erreichen. Der Parent-Snapshot übergibt die
Connector-spezifische Authority an den direkten Framework-Runtime-Runner,
statt eines mutierbaren Shared Exports oder eines impliziten `BUILD_ROOT`-
Defaults. Es werden weder Cleanup, `REFRESH`-Deaktivierung, Suppression,
Quality-Gate-Änderung noch ein Branch-Protection-Bypass verwendet.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`: leitet den engen
  Connector-Cache-Owner-Root ab, validiert ihn und übergibt ihn an Apache und
  NGINX.
- `ci/provisioning/components/prepare-runtime-components.py`: übergibt
  denselben engen Owner Root beim Bauen der Cache-Einträge und im vorbereiteten
  Invocation-lokalen Runtime-Environment-Snapshot.
- `tests/test_full_matrix_cache_owner_root.py`: kontrollierte Same-Boundary-
  Positiv- und Outside-Owner-Ablehnungstests sowie direkte Runtime-Matrix-
  Snapshot-Propagation-Coverage.
- `tests/test_runtime_component_cache_contract.py`: prüft, dass beide
  Connector-Build-Provisioner den engen Owner Root erhalten.
- `.github/workflows/verified-report-governance.yml`: behält den bestehenden
  begrenzten Failure-Summary-Helper bei und verwendet ihn für den festen
  NGINX-`configure`-Logpfad, damit ein späterer Source-Build-Fehler seine
  verwertbare Diagnose enthält.
- `tests/test_ci_security_workflows.py`: prüft, dass das NGINX-Log auf
  demselben Diagnosepfad für reguläre Nicht-Symlink-Dateien mit Command-
  Masking bleibt.
- `modules/ModSecurity-test-Framework`: der normale Merge von aktuellem
  Parent-Master führt seinen bereits integrierten Gitlink mit.
- `reports/audits/change-records/README.md`, `README.de.md` sowie dieser
  gepaarte Change Record.

## Ausgeführte Befehle

- `sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` — bestanden.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_full_matrix_cache_owner_root`
  — bestanden (drei Tests). Die Kontrollen führen den echten Matrix-Shell-
  Runner und den direkten Framework-Runtime-Matrix-Runner über den
  kontrollierten Invocation-lokalen Snapshot aus. Sie prüfen explizite Apache-
  und NGINX-Owner-Roots bei `REFRESH=1`; die Negativkontrolle prüft die
  Ablehnung vor `make`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_runtime_component_cache_contract`
  — bestanden (27 Tests), einschließlich Owner-Root-Assertions der
  Cache-Provisioner.
- `git diff --check` — bestanden.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_ci_security_workflows`
  — bestanden (20 Tests), einschließlich der begrenzten NGINX-
  Failure-Diagnosekontrolle.
- `make check-ci-security-contract` — bestanden (20 Workflow-Security-Tests
  und Validierung der gepinnten Tools actionlint, zizmor und gitleaks).

## Security-Auswirkung

Dies ist eine Pfad-Containment-Korrektur am Parent-zu-Framework-Handoff. Sie
hält einen Cache-Build in seinem deklarierten Owner Root und bewahrt den
Framework-Löschguard als finalen fail-closed Sink. Keine Vertrauensgrenze wird
aufgeweitet.

Die Folgefehler-Diagnose verwendet weder Discovery noch Glob noch einen
abgeleiteten Logpfad. Sie gibt höchstens 300 Zeilen aus dem festen
`$BUILD_ROOT/logs/nginx/nginx-configure.log` nur aus, wenn dieser Pfad eine
reguläre Nicht-Symlink-Datei innerhalb der bestehenden
`::stop-commands::`-Grenze ist. Sie legt keine Credentials offen, aktiviert
keinen privilegierten Workflow und verändert den NGINX-Buildbefehl nicht.

## Runtime-Evidence

Die kontrollierten Regressionen führen den echten Parent-Full-Matrix-Shell-
Runner und den direkten Framework-Runtime-Matrix-Runner über dieselbe
Invocation-lokale Snapshot-Grenze wie der Hosted-Producer aus. Sie sind keine
nativen Connector-Builds, Host-Deployments oder vollständige Runtime-Evidence-
Producer; dies bleibt für den aktualisierten exakten PR-#74-Head erforderlich.

## Bekannte Einschränkungen

Die lokalen Kontrollen ersetzen `make` nur an der finalen Connector-Smoke-
Grenze und behaupten daher keinen Apache- oder NGINX-Build. Die zugehörigen
Framework-Owner-Root-Löschkontrollen wurden separat gemergt und validiert. Der
vorherige Hosted-Producer des exakten Heads legte den fehlenden direkten
Snapshot-Handoff offen; das strikte Parent-Evidence-Gate muss nun erneut auf
dem Nachfolge-#74-Head laufen.

Der Vorgänger-Head erreichte den NGINX-Source-Build-`configure`-Befehl statt
des früheren Owner-Root-Guards, aber seine Failure-Summary ließ das feste Log
dieses Befehls aus. Die neue begrenzte Diagnose ist nötig, um den verbleibenden
Source-Build-Fehler zu klassifizieren; sie behauptet nicht, dass der NGINX-
Runtime-Producer besteht.

## Verbleibende Risiken

FND-CROSS-0008 und FND-CROSS-0001 bleiben offen, bis der Hosted-Exact-Head-
Producer legitime Cache-gestützte Evidence durch das strikte Gate nachweist.
Kein Risiko wird akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

Kein lokaler vollständiger Connector-Build oder echte Host-/Runtime-Matrix wird
behauptet. Sie benötigt die autoritative Hosted-Producer-Umgebung und bleibt
für den aktualisierten exakten Parent-PR-#74-Head erforderlich, ebenso das
strikte Terminal-Evidence-Gate, SonarQube-Cloud-Issue-/Duplikations-Readback,
Reviews und geschützte Merge-Voraussetzungen.

Kein Framework- oder MRTS-Source-Test und keine solche Änderung gehört zu
dieser Parent-Änderung. Framework-Owner-Root-Kontrollen wurden unabhängig vor
diesem Handoff gemergt.

## Finaler Diff- und Review-Status

Der lokale Diff ist auf die Parent-Matrix-/Snapshot-Handoffs, fokussierte
Regressionstests, das normale Master-Gitlink-Update und diesen zweisprachigen
Record/Index begrenzt. Er bestand fokussierte Security-/Pfad- und Cache-
Provisioner-Tests; die breiteren lokalen Checks und frische Exact-Head-Hosted-
Validierung müssen vor einem geschützten Merge erneut auf dem Nachfolge-Commit
laufen.

## Fortsetzung: Common-Source-Handoff des bereiten NGINX-Snapshots

Das begrenzte Exact-Head-NGINX-`configure`-Log von Parent #74 identifiziert
den verbleibenden Fehler: `MSCONNECTOR_COMMON_SRC` ist während der
Managed-Cache-Vorbereitung vorhanden, fehlt aber im späteren Invocation-
lokalen Snapshot der direkten Runtime-Matrix. Der Parent leitet den Wert jetzt
ausschließlich aus dem aufgelösten, geprüften
`CONNECTOR_ROOT/common/src` ab und veröffentlicht ihn für einen bereiten
NGINX-Eintrag. Er leitet keinen vom Job bereitgestellten Wert weiter, fügt
keinen Fallback hinzu, weitet keinen Cache-Owner-Root auf und verändert nicht
das fehlgeschlossene Framework-Verhalten für fehlende Quellen.

`tests/test_runtime_env_snapshot_contract.py` prüft, dass ein bereiter
NGINX-Eintrag genau diesen Common-Source-Root veröffentlicht und ein
blockierter Eintrag keine NGINX-Runtime-Werte veröffentlicht. Das direkte
Matrix-Fixture beweist außerdem, dass der Framework-Runner den Wert über
dieselbe sourcebare lokale Snapshot-Grenze wie die Owner-Roots erhält. Der
fokussierte Befehl
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_runtime_env_snapshot_contract tests.test_full_matrix_cache_owner_root tests.test_runtime_component_cache_contract`
bestand alle 38 Tests. Dies ist kein nativer NGINX-Erfolg: Der neue exakte
Parent-PR-#74-Head benötigt weiterhin Hosted-Producer, striktes Terminal-Gate,
SonarQube-Cloud-Readback, Review-/Protection-Evidence und geschützte
Integration.

## Fortsetzung: exakte CI-Interpreter-Identität und All-Core-Sichtbarkeit

Der gehostete Parent-PR-#74-Head
`ef0b6ab27162e9735e9ff9d8beb3516446eed1ff` erzeugte das vorgesehene
hash-gesperrte Venv `verified-report-python` und installierte Framework
`PyYAML==6.0.3`, exportierte danach jedoch den bloßen Selektor
`PYTHON=python3`. Parent-Makefile, Verified-Run-Dispatcher und Framework-
Runtime-Runner reichen diesen Selektor korrekt weiter; er kann dennoch
außerhalb des Venv aufgelöst werden, wenn ein späterer Runtime-Helper `PATH`
ändert. Der exakte Hosted-Run `30222002129` / Job `89845969175` schlug deshalb
in `update-runtime-snapshot.py` mit `ModuleNotFoundError: No module named
'yaml'` fehl. Der fehlgeschlagene strikte Producer bleibt abgelehnt; dies ist
zusätzliche Ursachen-Evidenz für `FND-CROSS-0001`, keine erfolgreiche
Runtime-Evidenz.

Der Workflow behält jetzt den praktischen `PATH`-Export, übergibt aber nach
einem direkten `import yaml`-Check den exakt erzeugten Interpreter als
`PYTHON=$venv/bin/python`. Das erhält die verifizierte setup-python-Auswahl,
den Hash-Lock, `--only-binary`, `--require-hashes`, die No-Write-Berechtigung
und den fail-closed Import-Vertrag; Framework-Source, dessen Lock, MRTS und
ein Gitlink bleiben unverändert.

Der Full-Matrix-Runner leitet seine Standardobergrenze bereits aus `nproc`,
dann `getconf _NPROCESSORS_ONLN`, dann `1` ab; ein fester Workflow-Wert würde
dieses hostbewusste Verhalten deaktivieren. Sein neuer schreibgeschützter
Modus `--print-effective-parallelism` meldet die tatsächlich gewählte
Obergrenze und ob sie auto-erkannt oder explizit ist, bevor irgendein Python-
Prozess, Runtime-Pfad, Build, Port oder Matrix-Aktion startet. Der Workflow
ruft diesen Modus sichtbar vor dem strikten Producer auf, und die normale
Scheduling-Meldung behält dieselbe Source-Markierung.

Geänderte Fortsetzungsdateien:

- `.github/workflows/verified-report-governance.yml`
- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`
- `tests/test_ci_security_workflows.py`
- `tests/test_full_matrix_parallel_scheduler.py`
- `docs/reference/variables.md` und `docs/reference/variables.de.md`
- dieses gepaarte Change Record

Tatsächlich ausgeführte fokussierte Validierung nach dieser Fortsetzung:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_ci_security_workflows tests.test_full_matrix_parallel_scheduler` — bestanden, 32 Tests. Sie beweist, dass der Workflow seinen hash-gesperrten Abhängigkeitsvertrag behält, den exakten Venv-Interpreter statt des bloßen Selektors exportiert, die sichtbare Diagnose aufruft, keine bestehende Workflow-Sicherheitskontrolle zurückweist und auto-erkannte/explizite Obergrenzen-Diagnosen sowie das normale Scheduler-Verhalten ausführt.

Die finalen exakten Hosted-Head-Checks `report-governance`, Terminal-
Evidence-Gate, SonarQube-Cloud-Readback, Review-/Thread- und geschützten
Merge-Checks sind für diesen Nachfolgecommit noch nicht gelaufen. Das lokale
Ergebnis ist deshalb `remediation_required`, keine Behauptung, dass
`FND-CROSS-0001` behoben ist oder der PR gemergt werden kann.

Die lokale Kontrolle `check-python-interpreter-contract.py` ist
`blocked_environment`: Dieses Task-Venv ist CPython 3.14.4, während
`.python-version` 3.14.6 verlangt, und seine Shell kann den von
`actions/setup-python` gesetzten PATH nicht nachbilden. Sie wird nicht durch
einen anderen Interpreter ersetzt; der Hosted-Workflow des Nachfolgecommits
bleibt die maßgebliche Compatibility-Kontrolle.
