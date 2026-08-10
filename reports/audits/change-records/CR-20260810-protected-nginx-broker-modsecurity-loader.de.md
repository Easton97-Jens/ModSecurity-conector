# Change Record

**Sprache:** [English](CR-20260810-protected-nginx-broker-modsecurity-loader.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260810-protected-nginx-broker-modsecurity-loader |
| Datum (UTC) | 2026-08-10 |
| Basis-Revision | e24527eb729584aac3d815cbf32ef6b7026f729c |
| Framework-Gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation und Problemstellung

Der geschützte Resulting-master-Lauf `31344894963` band Caller-, Broker- und
Framework-Revisionen erfolgreich, aber beide Profile stoppten im
unprivilegierten Build-Schritt vor der Candidate-Erstellung. Der Producer
wählte Libtools Alias `libmodsecurity.so` als geschütztes Artefakt; dieser Alias
ist ein Symlink, daher wies ihn die bestehende no-follow-Producer-Kontrolle
korrekt ab.

Das geprüfte ModSecurity-Objekt verwendet den ABI-Namen `libmodsecurity.so.3`.
Das Kopieren nur eines unversionierten Root-Artefakts würde den Fehler daher in
den dynamischen Loader verschieben. Außerdem könnte ein NGINX-Modul mit einem
Runner-Cache-`DT_RPATH` oder `DT_RUNPATH` das zugelassene Library-Verzeichnis
umgehen. Beide Fehler müssen außerhalb der Root-Grenze bleiben.

## Akzeptanzkriterien

Der geschützte Producer behält gewöhnliche Libtool-Aliasse für generische
Link-Time-Consumer bei, veröffentlicht aber ein reguläres enthaltenes
`prefix/lib/libmodsecurity.so.3`-Artefakt für die geschützte Provenance. Seine
Cache-Identität ändert sich, damit ein älteres nur-Alias-Präfix nicht
wiederverwendet werden kann. Jeder erwartete Alias muss ein direktes
Basename-Ziel besitzen, und die descriptor-relative Auflösung muss beide
Aliasse an ein reguläres Terminalobjekt binden, bevor die geschützte Kopie über
den an dieses Terminal gebundenen Deskriptor erzeugt wird.

Der Broker bindet genau diesen regulären Artefaktnamen in Provenance-Record,
Snapshot, Candidate, Root-Layout und Loader-Umgebung. Er weist Symlink,
Pfad außerhalb der Root, Metadaten-/Digest-Abweichung oder eine dynamische
Section mit `DT_RPATH`, `DT_RUNPATH`, Slash enthaltendem `DT_NEEDED`,
`DT_AUDIT`, `DT_DEPAUDIT`, `DT_FILTER` oder `DT_AUXILIARY` vor der
Candidate-Erstellung ab. Die feste Untersuchung besitzt eine reale begrenzte
Deadline. Der geschützte Workflow setzt die feste Auswahl
`NGX_IGNORE_RPATH=YES` vor `make fetch-deps`.

## Technische Entscheidungen

Die Reparatur akzeptiert an keiner geschützten Producer-, Candidate- oder
Root-Grenze einen Symlink. Sie löst die Libtool-Aliasse descriptor-relativ auf,
fordert direkte Basename-Aliasziele und prüft, dass beide erwarteten Aliasse
sich auf dasselbe reguläre Terminalobjekt auflösen. Sie materialisiert die
getrennte reguläre Kopie mit ABI-Namen über den an dieses
Terminal gebundenen Deskriptor; Nested-Symlink-Escape oder Austausch wird
abgewiesen.

Das bestehende Opt-in `NGX_IGNORE_RPATH=YES` hat nur im expliziten
ModSecurity-Library-Branch von `connectors/nginx/config` Vorrang; das normale
Connector-Verhalten bleibt ohne dieses Opt-in unverändert. Der Broker nutzt das
feste absolute `/usr/bin/readelf` mit leerem `PATH`, begrenzter Ausgabe, einer
realen begrenzten Deadline und ohne Shell, um zugelassenes Source-Modul und
Library vor der Candidate-Erstellung zu prüfen.

Ein lokales Follow-up behebt zwei Sonar-Findings aus PR #271: das
Cognitive-Complexity-Problem (`python:S3776`) des Producer-Alias-Resolvers und
das Regex-Problem (`python:S8786`) des Broker-Dynamic-Parsers. Dies ist nur
lokale Remediation-Evidence und kein Ergebnis einer Post-Fix-Hosted-
Sonar-Analyse.

## Implementierungsentscheidung und Begründung

`MODSECURITY_OUTPUT_LAYOUT_VERSION` ist Teil der ModSecurity-Cache-Identität
und verhindert damit, dass ein älterer vollständiger Cache-Eintrag den neuen
geschützten Artefaktvertrag erfüllt. Der generische
`libmodsecurity.so`-Readiness-/Linker-Name bleibt unverändert. Der geschützte
Record wählt stattdessen die materialisierte reguläre
`libmodsecurity.so.3`-Kopie.

Die feste Artefaktnamen-Map des Brokers, Snapshot-Reader, Candidate-Kopie,
Root-Admission, Final-Manifest-Validierung und `LD_LIBRARY_PATH` verwenden
nun denselben ABI-Namen. Er führt keinen ambienten Lookup für das
Untersuchungstool aus und schlägt fail-closed fehl, wenn eines der geprüften
ELFs `DT_RPATH`, `DT_RUNPATH`, Slash enthaltendes `DT_NEEDED`, `DT_AUDIT`,
`DT_DEPAUDIT`, `DT_FILTER` oder `DT_AUXILIARY` enthält oder nicht innerhalb
der begrenzten Deadline untersucht werden kann. Alle Untersuchungen laufen
unprivilegiert und finden vor der Candidate-Erstellung sowie jeder
`sudo`-Aktion statt.

## Geänderte Dateien

- .github/workflows/nginx-root-broker.yml
- ci/provisioning/components/prepare-runtime-components.py
- ci/runtime/broker/nginx_root_broker.py
- connectors/nginx/config
- tests/test_runtime_env_snapshot_contract.py
- tests/test_runtime_component_cache_contract.py
- tests/test_nginx_root_broker.py
- tests/test_nginx_root_broker_crs_profile.py
- tests/test_nginx_root_broker_workflow.py
- docs/security/trusted-nginx-root-broker.md und docs/security/trusted-nginx-root-broker.de.md
- dieser Change Record und CR-20260810-protected-nginx-broker-modsecurity-loader.md

## Tests und tatsächliche Ergebnisse

Die anfängliche fokussierte Producer-, Cache-, Broker-, CRS-Profil-, Workflow-
und CI-Security-Suite bestand nach der anfänglichen Loader-Reparatur lokal 83
Tests. Nach der erweiterten Security-Entdeckung und -Remediation bestand eine
spätere Broker-/CRS-Suite 43 Tests und die fokussierte Remediation bestand 2
Tests. Die fokussierte Producer-Matrix bestand 5 Tests. Diese decken direkte
Basename-Libtool-Aliasse, descriptor-gebundene Veröffentlichung des regulären
ABI-Artefakts und die erweiterte Dynamic-Section-Ablehnung vor der
Candidate-Erstellung mit einer legitimen Kontrolle ab.

Das vollständige owning Cache-Modul bestand 38 Tests und hatte einen bekannten
Isolated-Worktree-Fixture-Fehler. Der Fehler war
`test_nginx_discards_marker_owned_partial_root_before_build` und wurde durch
die fehlende isolierte Fixture-Datei
`connector/common/src/header_validation_internal.h` verursacht. Der Fehler
wurde weder unterdrückt noch als Pass dargestellt.

Nachdem die Sonar-Findings aus PR #271 lokal behoben waren, bestand die
erweiterte fokussierte Suite 88 Tests. Das lokale Follow-up bestand außerdem
die Syntaxkompilierung für Producer- und Broker-Module, die CI-Security-
Contract-Prüfung und die Whitespace-Prüfung des getrackten Diffs. Dies sind
lokale Ergebnisse, keine Hosted-PR-, Sonar-, Runtime- oder
Cleanup-Evidence.

## Ausgeführte Befehle

Die obigen Ergebnisse mit 83, 43, 2 und 5 Tests sind frühere historische lokale
Beobachtungen; ihre exakten Befehlszeilen werden hier nicht rekonstruiert. Die
folgenden späteren Befehle und Ergebnisse wurden tatsächlich beobachtet:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=../tmp python3 -m unittest -v \
  tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_output_layout_version_changes_the_cache_identity \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_materialize_a_regular_runtime_soname \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_unsafe_or_ambiguous_libtool_chains \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_nested_symlink_parent_escape \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_runtime_copy_remains_bound_to_verified_inode \
  tests.test_nginx_root_broker \
  tests.test_nginx_root_broker_crs_profile \
  tests.test_nginx_root_broker_workflow \
  tests.test_ci_security_workflows
```

Ergebnis: PASS, 86 Tests bestanden.

```sh
rtk proxy sh -n connectors/nginx/config
```

Ergebnis: Exit 0.

```sh
rtk proxy shellcheck --shell=sh --severity=error connectors/nginx/config
```

Ergebnis: Exit 0.

```sh
rtk proxy make check-ci-security-contract
```

Ergebnis: Exit 0, 26 Tests bestanden.

```sh
rtk proxy git diff --check
```

Ergebnis: Exit 0 für den aktuellen getrackten Diff.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=../tmp python3 -m unittest -v tests.test_runtime_component_cache_contract
```

Ergebnis: 38 Tests bestanden und 1 Fehler trat in
`test_nginx_discards_marker_owned_partial_root_before_build` auf, weil dem
isolierten Fixture `connector/common/src/header_validation_internal.h` fehlte.
Der Fehler wurde nicht unterdrückt.

Anschließend wurden für das lokale Sonar-Remediation-Follow-up
folgende Befehle ausgeführt:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=../tmp python3 -m unittest -v tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_output_layout_version_changes_the_cache_identity tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_materialize_a_regular_runtime_soname tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_unsafe_or_ambiguous_libtool_chains tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_nested_symlink_parent_escape tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_runtime_copy_remains_bound_to_verified_inode tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_cyclic_and_nonregular_libtool_chains tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow tests.test_ci_security_workflows
```

Ergebnis: PASS, 88 Tests bestanden.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m py_compile ci/provisioning/components/prepare-runtime-components.py ci/runtime/broker/nginx_root_broker.py
```

Ergebnis: bestanden.

```sh
rtk proxy make check-ci-security-contract
```

Ergebnis: bestanden.

```sh
rtk proxy git diff --check
```

Ergebnis: bestanden.

## Security-Auswirkung

Der ursprüngliche Lauf bleibt fail-closed: Beide Profile stoppten vor
Candidate-Erstellung, Root-Admission, jeder `sudo`-Aktion, NGINX-Start,
Evidence und Cleanup-Verifikation. Die Reparatur bewahrt diese Reihenfolge und
verhindert zusätzlich, dass ein ansonsten geprüftes Modul oder eine Shared
Library einen Runner-Cache-dynamischen Suchpfad, eine Slash enthaltende
Abhängigkeit oder einen dynamischen Audit-/Filter-Hook behält.
Descriptor-relative Auflösung direkter Basename-Aliasse und die
descriptor-gebundene geschützte Kopie weisen Nested-Symlink-Escape und
Austausch ab. Es werden kein System-NGINX, kein ambienter `PATH`, kein Symlink,
kein Caller-vorgegebener Artefaktpfad und keine Root-Shell eingeführt. Diese
Kontrollen laufen vor der Candidate-Erstellung und bleiben
unprivilegiert/pre-root.

## Runtime-Evidence

Lauf `31344894963` ist nur Failure-Evidence. Er erreichte die damals aktuellen
geschützten Snapshot- und unveränderlichen Binding-Prüfungen, stoppte aber
bevor der Loader-Vertrag bestehen konnte. Für diesen Kandidaten existiert kein
erfolgreiches Root-, Worker-, No-CRS-, CRS-, Audit-, Evidence-Readback- oder
Cleanup-Ergebnis.

## Bekannte Einschränkungen

Der verfügbare lokale Interpreter ist CPython 3.14.4, während
`.python-version` CPython 3.14.6 verlangt. Lokale Tests sind Source-/Static-
Evidence, keine CI-äquivalente Interpreter- oder Hosted-Root-Evidence. Der
kanonische lokale Finding-Store ist read-only gemountet, daher konnte der
getrennte vorgeschlagene Record FND-PARENT-0117 dort nicht erstellt werden;
kein konkurrierender Record wurde erstellt. FND-PARENT-0113 bleibt blockiert.
Die frühere Sonar-Analyse von PR #271 meldete `python:S3776` und
`python:S8786`; die lokale Remediation hat noch keine Post-Fix-Hosted-
Sonar-Analyse erhalten.

## Verbleibende Risiken

Die Broker-Reparatur benötigt weiterhin einen neuen unveränderlichen Commit,
Exact-Head-Hosted-Checks, CodeQL, SonarQube Cloud, Review und normalen Merge.
Ein separater Caller-Repin muss anschließend diesen neuen Broker-Commit und
seinen Framework-Gitlink binden. Nur ein Resulting-master-geschützter No-CRS-
und `owasp-crs`-Lifecycle mit Evidence-Readback und Cleanup kann PR #240
entsperren.

## Nicht ausgeführte Prüfungen mit Begründung

Kein lokales `make fetch-deps`, keine Root-Aktion, kein NGINX-Start, kein
CRS-Fetch, Audit oder Cleanup-Lauf wurde versucht. Diese Aktionen benötigen
den geschützten Resulting-master-Workflow, echte Hosted-Runner-Isolation und
den separaten Post-Merge-Caller-Repin. Hosted-PR-Checks und SonarQube Cloud
sind ebenfalls noch nicht verfügbar, weil diese Reparatur noch nicht
committet oder veröffentlicht ist.

## Finaler Review-Status

Dies ist ausschließlich lokale Reparatur-Evidence. Es erstellt keinen Pull
Request und behauptet keinen Delivery-, Merge-, Caller-Repin- oder
erfolgreichen Phase-D-Lifecycle.

## Finaler Diff- und Review-Status

Der task-owned Branch beginnt bei `e24527eb729584aac3d815cbf32ef6b7026f729c`.
Der beabsichtigte Diff ist Parent-only und verändert weder Framework-Source,
Framework-Gitlink, MRTS, Caller-Pins, Root-Action-Allowlist, Trigger noch
Permissions. Vor der Veröffentlichung bleiben ein finaler scoped
Security-Diff-Review und alle anwendbaren lokalen Prüfungen erforderlich.
