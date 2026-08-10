# Change Record

**Sprache:** [English](CR-20260810-trusted-nginx-broker-artifact-limit-crs-umask.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260810-trusted-nginx-broker-artifact-limit-crs-umask |
| Datum (UTC) | 2026-08-10 |
| Basis-Revision | 2d1efe0c10b62131bb1a6897aa46a8ba9e85d1db |
| Framework-Gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation und Problemstellung

Der geschützte Resulting-master-Lauf `31368594208` stoppte in beiden Profilen vor jeder Root-Aktion. Der No-CRS-Job `93392350727` wies die geprüfte kanonische `libmodsecurity.so.3` unter dem generischen 8-MiB-Evidence-Datei-Limit ab, obwohl das aufbewahrte geschützte Producer-Artefakt 60.085.848 Byte maß. Der With-CRS-Job `93392350719` stoppte vor Root, weil ein äußeres `umask 077` frische CRS-Sources erzeugen kann, die nicht den exakten geschützten Source-Modi des Brokers entsprechen.

Die Fehler waren fail-closed, verhinderten aber die legitime Candidate-Erstellung. Die Reparatur behält endliche descriptor-gebundene Admission bei; sie erweitert keine generischen Evidence-Limits und lockert keine CRS-Source-Mode-Prüfung.

## Akzeptanzkriterien

Nur die kanonische `libmodsecurity.so.3` erhält ein festes code-eigenes endliches Limit: `MAX_TRUSTED_MODSECURITY_LIBRARY_BYTES = 64 * 1024 * 1024`. Das aufbewahrte Artefakt lässt 7.023.016 Byte Reserve. Die generischen Evidence-Limits von 8 MiB pro Datei und 20 MiB gesamt bleiben für Evidence, NGINX-Binary und -Modul in Kraft. Provenance und der bereits geöffnete no-follow-Deskriptor erzwingen beide das Library-Limit vor Hashing oder Kopieren.

Das äußere Workflow-Umask bleibt `077`. Nur die exakte `fetch-crs.sh`-Ausführung läuft in einer Subshell mit `umask 022`; der Workflow prüft das äußere Umask vor und nach dem Fetch und bewahrt einen Fehlerstatus. Er ändert weder das globale Umask noch verwendet er rekursive Berechtigungsänderungen. Der geschützte CRS-Vertrag fordert weiterhin die Source-Root und das `rules`-Verzeichnis sowie `plugins`, falls es vorhanden ist, mit `0755` sowie ausgewählte Source-Dateien mit `0644`.

Der Shell-Vertrag akzeptiert beide kanonischen Darstellungen `077`/`0077`
und `022`/`0022`, sodass die Prüfung nicht versehentlich von einer
Shell-Schreibweise abhängt.

## Technische Entscheidungen

Die Library-Grenze ist ein fester Broker-Code-Policywert, der bei der
Provenance-Validierung und erneut am geöffneten Deskriptor gilt. Die
Mode-Ausnahme beschränkt sich auf den exakten festen CRS-Fetch-Befehl in
seiner Subshell. Die Reparatur ändert weder Schema, Caller-Input,
öffentliche Schnittstelle, generisches Evidence-Limit, Framework-Gitlink
noch generierte Artefakte.

## Implementierungsentscheidung und Begründung

Der Provenance-Validator erhält pro geschütztem Artefakt ein explizites Maximum. Die Candidate-Kopie prüft es erneut gegen Metadaten des geöffneten Deskriptors und schließt das Intervall vor Digest oder Kopie. Das nur für die Library geltende Maximum wird ausschließlich für die kanonische `libmodsecurity.so.3` übergeben; NGINX-Binary und -Modul behalten das generische Maximum. Die Broker-CRS-Validierung prüft nun ausdrücklich den Source-Root-Mode zusätzlich zu den Modi des erforderlichen Rules- und optionalen Plugins-Verzeichnisses.

## Geänderte Dateien

- .github/workflows/nginx-root-broker.yml
- ci/runtime/broker/nginx_root_broker.py
- tests/test_nginx_root_broker.py
- tests/test_nginx_root_broker_crs_profile.py
- tests/test_nginx_root_broker_workflow.py
- docs/security/trusted-nginx-root-broker.md und docs/security/trusted-nginx-root-broker.de.md
- dieser Change Record und CR-20260810-trusted-nginx-broker-artifact-limit-crs-umask.md

## Tests und tatsächliche Ergebnisse

Vor der Reparatur schlugen vier fokussierte Regressionstests erwartungsgemäß fehl: Eine gültige Library größer als 8 MiB wurde von der Provenance abgewiesen, das Library-spezifische Kopierlimit fehlte, CRS-Verzeichnisse mit `0700` wurden akzeptiert und dem Workflow fehlte der begrenzte Umask-Vertrag.

Nach der Reparatur bestanden acht direkte Broker-, CRS-Profil- und Workflow-Tests. Sie decken die getrennte Library-Grenze und die Durchsetzung am geöffneten Deskriptor, Austauschresistenz vor Candidate-Erstellung, beibehaltene Evidence-Limits, legitime und unsichere CRS-Modi sowie den begrenzten Workflow-Umask-Vertrag ab, einschließlich einer hermetischen fehlgeschlagenen Fetch-Ausführung, die äußeres `077` bewahrt und den Fehler weitergibt.

Ein normaler Sonar-Folgecommit für PR #273 führte danach vier PR-spezifische,
nichtfunktionale Qualitätskorrekturen ohne Suppression aus: Die Auswahl
optionaler CRS-Plugins wurde in einen privaten Helper ausgelagert, ohne deren
Validierungs- oder Admission-Reihenfolge zu ändern, und drei Test-Assertions
konstruieren deterministische Eingaben nun außerhalb ihrer Exception-Capture-
Scopes. Die fokussierte Broker-, CRS-Profil- und Workflow-Suite bestand für
diesen exakten Folgecommit-Working-Tree-Diff 64 Tests.

Die finale Broker-, Caller-, Workflow-, CI-Sicherheits- und Python-Contract-Suite
bestand 123 Tests. Die Cache-Contract- und Cache-Identity-Suite bestand 46
Tests. Das vollständige Snapshot-Modul bestand neun Tests und meldete einen
Umgebungsfehler in `RuntimeEnvironmentSnapshotContractTest.test_with_runner_consumes_the_prepared_snapshot_without_reading_shared_env`: Dieses externe Parent-Worktree enthält `modules/ModSecurity-test-Framework/ci/lib/common.sh` nicht. Der Fehler wurde nicht unterdrückt; Framework wurde in dieser Parent-only-Phase weder initialisiert noch geändert.

## Ausgeführte Befehle

Die folgenden Befehle wurden tatsächlich im Phase-A-Worktree ausgeführt. `../tmp` ist das registrierte task-eigene externe temporäre Verzeichnis; private Build- oder Cache-Pfade werden hier nicht erfasst.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow
```

Ergebnis: PASS, 63 Tests.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow
```

Ergebnis: PASS, 64 Tests für den normalen Sonar-Folgecommit.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_ready_nginx_snapshot_values_bind_the_parent_common_source_root tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_unready_nginx_does_not_publish_runtime_snapshot_values tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_snapshot_is_unique_local_atomic_and_keeps_shared_compatibility_export tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_snapshot_writer_rejects_a_path_outside_the_invocation_report_root tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_native_comparison_uses_the_wrapper_snapshot_not_shared_env tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_native_comparison_does_not_fallback_to_shared_env_for_an_invalid_snapshot tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_central_runners_use_the_exact_local_snapshot_not_shared_runtime_env
```

Ergebnis: PASS, 8 Tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract
```

Ergebnis: PASS, 123 Tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest tests.test_runtime_component_cache_contract tests.test_runtime_component_cache_identity
```

Ergebnis: PASS, 46 Tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_runtime_env_snapshot_contract
```

Ergebnis: Neun Tests bestanden; der eine nicht unterdrückte Fehler ist das
oben beschriebene fehlende Framework-`ci/lib/common.sh`-Fixture.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_python_version_contract
```

Ergebnis: PASS, 24 Tests.

```sh
rtk proxy make PYTHON=python3 check-ci-security-contract
```

Ergebnis: PASS, 26 CI-Sicherheits-Workflow-Tests und Prüfsummen-Record-Validierung für actionlint, zizmor und gitleaks.

```sh
rtk proxy make PYTHON=python3 check-bilingual-docs
rtk proxy make PYTHON=python3 check-doc-links
```

Ergebnis: Beide endeten nur deshalb nonzero, weil diesem Parent-only externen
Worktree absichtlich die lokalen Dokumentationsziele des Framework-Gitlinks
fehlen. Es wurde keine neue Diagnose für geänderte Dokumente oder Change
Records gemeldet; Framework wurde nicht initialisiert oder geändert, um die
globalen Checks grün zu machen.

Prüfsummenverifiziertes actionlint plus ShellCheck bestand für alle Workflow- und Berechtigungs-Fixture-YAMLs. Offline-zizmor bestand für die Workflows und das sichere Fixture; es wies das absichtlich unsichere `pull_request_target`-Fixture korrekt ab. Die bloße Python-Version-Contract-CLI wurde ebenfalls ausgeführt und meldete 21 geerbte Workflow-Inventar-Verletzungen außerhalb dieses Diffs; sie meldete keine Phase-A-spezifische Verletzung.

```sh
rtk proxy git diff --check
```

Ergebnis: Exit 0 für den finalen getrackten Phase-A-Diff.

Dieselbe Whitespace-Prüfung bestand für den Zwei-Dateien-Sonar-Folgecommit vor
seinem normalen Commit.

## Sonar-Folgecommit und statischer Security-Receipt

Der vorherige PR-273-Head `b5681438a1e1a616190ea6f5d79bc8d3ae7ecec1` hatte
ein bestehendes Quality Gate, aber vier neue PR-spezifische Sonar-Findings:
ein `python:S3776` und drei `python:S5778`. Der obige normale Folgecommit
behebt diese Findings ohne `NOSONAR`, Issue-Akzeptanz, Änderung eines
Quality-Profils oder -Gates oder einen Analyse-Ausschluss.

Der versiegelte externe statische Receipt `b5681438_20260810T122838Z` deckt
die vollständige Zwei-Dateien-Worklist des Folgecommits
(`ci/runtime/broker/nginx_root_broker.py` und
`tests/test_nginx_root_broker.py`) gegen diesen Basis-Head ab. Sein lokaler
Snapshot-Digest lautet
`cea33809b578a3223bc45a82fd92f595fab17110cb965891f0a97cc55692c627`; er
verzeichnet null reportable Findings und ein kanonisches HTTPS-
Repositoryziel. Der Receipt ist nur Static-Evidence vor dem Commit: Er ersetzt
weder die SonarQube-Cloud-Analyse des exakten neuen Heads noch Hosted-Checks,
Review-Evidence oder den späteren geschützten Lifecycle.

## Hosted-Delivery-Evidence für unveränderlichen Code-Head

[Draft-PR #273](https://github.com/Easton97-Jens/ModSecurity-conector/pull/273)
wurde nach dem lokalen Phase-A-Repair-Commit
`3042b984484637192742a2d22d9e029f8ad97b61` vom task-eigenen Branch erstellt.
Der Head vor dem Folgecommit
`b5681438a1e1a616190ea6f5d79bc8d3ae7ecec1` ist nur historisch und darf nicht
als Hosted-Evidence für den oben dokumentierten normalen Sonar-Folgecommit
verwendet werden. Dieser Record beansprucht keinen Exact-New-Head-Hosted-
Check, keine SonarQube-Cloud-Analyse, kein Review, keinen Merge und keinen
erfolgreichen geschützten Lifecycle; dies alles bleibt vor dem späteren
Caller-Repin erforderlich.

## Security-Auswirkung

Die Reparatur behält eine fail-closed-Pre-root-Grenze bei: Admission ist begrenzt und erfolgt vor Kopie, Candidate-Erstellung oder Root-Aktion. Kein Caller, Manifest, keine Umgebungsvariable und kein Evidence-Input kann ein größeres Limit wählen. Das begrenzte Fetch-Umask bewahrt privaten umgebenden Workflow-Zustand und ermöglicht nur broker-geforderte frische CRS-Source-Modi.

## Runtime-Evidence

Lauf `31368594208` ist ausschließlich Failure-Evidence vor der Reparatur. Beide Jobs stoppten vor Candidate-Erstellung, Root-Admission, `sudo`, NGINX-Start, Audit, Evidence-Readback und Cleanup-Verifikation. Für diese Änderung liegt kein erfolgreicher geschützter No-CRS- oder `owasp-crs`-Lifecycle vor.

## Bekannte Einschränkungen

Der verfügbare lokale Interpreter ist CPython 3.14.4, während `.python-version` CPython 3.14.6 fordert. Lokale Tests sind Source-/Static-Evidence, kein CI-äquivalenter oder geschützter Root-Runtime-Nachweis. Die vollständige Snapshot-Suite hat den oben dokumentierten, nicht unterdrückten Framework-Source-Fehler im externen Worktree.

## Verbleibende Risiken

Dieser Branch benötigt weiterhin finale lokale Validierung, Security-Review, unveränderliche-Head-Hosted-Checks und einen explizit SHA-gebundenen Merge, bevor ein separater Caller-Repin erfolgen darf. Die Findings bleiben in Arbeit, bis ein Resulting-master-Lifecycle beide Profile mit erforderlicher Evidence und Cleanup-Verifikation besteht.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurden weder lokales `make fetch-deps`, CRS-Netzwerk-Fetch, Candidate-Admission, Root-Aktion, NGINX-Start, Audit, Evidence-Projektion noch Cleanup ausgeführt. Diese benötigen den geschützten Resulting-master-Workflow und sind kein Ersatz für den späteren Phase-C-Lifecycle.

## Finaler Diff- und Review-Status

Status: in Arbeit. Dieser Record ist keine Delivery-Freigabe oder Integration-Evidence.
