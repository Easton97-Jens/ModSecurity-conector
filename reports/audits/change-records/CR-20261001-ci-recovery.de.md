# Change Record: CR-20261001-ci-recovery

**Sprache:** [English](CR-20261001-ci-recovery.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261001-ci-recovery |
| Datum (UTC) | 2026-10-01 |
| Basis-Revision | `b0f3bdab429717b5b0311c30c5b4d1153c672ac0` |

## Motivation und Problemstellung

Die Fehler aus Parent-Lauf [36906913089](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36906913089) und Framework-Lauf [36703337419](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36703337419) beheben und aktuelle CI auf verwandte Fehler prüfen. Die Parent-Wartung verlangte fälschlich auch für einen geprüften, bereits gemergten Wartungsbranch einen einzigen Bot-Commit. Weitere Lücken betrafen lange Unix-Socket-Pfade, die Ablehnung des bereitgestellten Traefik-Host-Stagings, Broker-Berechtigungen und Tag-Abruf, unvollständige Updater-Inventare/Eingaben des kopierten Baums sowie vorübergehende API-Fehler der Artefaktbereinigung.

Der Benutzer verlangte anschließend eine einzige gepflegte Stelle für
`FRAMEWORK_SHA`, weitere gewöhnliche Revisionspins, Komponentenauswahl und
Toolchains. Dies erweitert den angeforderten Reparaturumfang; es autorisiert
keine Framework-/MRTS-Quelländerungen oder geschützte Broker-Aktivierung.

## Akzeptanzkriterien

Regressionen müssen die ursprünglichen Fehler abdecken, ohne Publisher-Identität, Runtime-Isolation, unveränderliche Pins oder standardmäßig verweigerte Berechtigungen abzuschwächen. Die aktuelle gehostete Framework-Veröffentlichung und ihre PR-Prüfungen müssen erfolgreich sein. Gehostete Parent-Validierung und geschützte Broker-Aktivierung bleiben erforderlich, bevor alle Workflows als funktionsfähig gelten.

Gewöhnliche Revisions- und Toolchain-Consumer müssen einen strikten Parent-
Datensatz verwenden; unabhängige Gitlink-/Commit-Provenienz, Komponenten-
Zuständigkeit und enger Feldumfang der Updater bleiben durchgesetzt.

## Implementierungsentscheidung und Begründung

Offene Wartungsbranches bleiben auf die konfigurierte App beschränkt; geprüfte gemergte Remediation-Historie darf erst nach Prüfung von PR-Identität, Merge-Abstammung und aktuellen Branch-Schutzbedingungen wiederverwendet werden. Private kurze Socket-Verzeichnisse verwenden und revisionsgebundene Artefaktwurzeln erhalten. Nur den exakt bereitgestellten Traefik-Host-Pfad zulassen. Die exakt leere Berechtigungszuordnung des Broker-Callers akzeptieren und den genehmigten CRS-Tag unabhängig abrufen/prüfen. Das explizite Updater-Publisher-Inventar und die schreibgeschützten Baseline-Eingaben vervollständigen; Make prüft gezielt das Inventar und CI die vollständige Suite, um rekursive Kandidatenvalidierung zu vermeiden. Action-Pin-Assertions aus der zentralen Lockdatei ableiten. API-Aufrufe der Artefaktbereinigung dreimal wiederholen.

Die nachträgliche Schnittstellenkorrektur des Socket-Wrappers erhält private `0700`-Wurzeln, Eigentümer-/Vorfahrensprüfungen, Socket-Bytegrenzen, Prüfung des Prozessendes und Aufbewahrung bei unsicherer Bereinigung. Der Low-Level-Befehlsrunner bleibt eine interne Test-API statt CLI-Befehlseingabe. Nach dieser Quelländerung ist gehostete/Quality-Evidence des neuen Heads erforderlich.

Der frische gehostete Apache-CRS-Job `110539160124` in [Lauf 36912740744](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912740744) zeigte weiteren erforderlichen Reparaturbedarf: Die gepinnte HTTPD-`2.4.68`-URL `https://downloads.apache.org/httpd/httpd-2.4.68.tar.bz2` lieferte `404`, während die identische offizielle Archiv-URL `https://archive.apache.org/dist/httpd/httpd-2.4.68.tar.bz2` `200` lieferte. Der literale SHA-256 bleibt `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06`. Die Parent-Bereitstellung implementiert unabhängig die exakte Wiederherstellung nach direkter 404 über das offizielle Archiv mit demselben Dateinamen, die im geprüften Framework-master bereits vorliegt. Sie verlangt ausdrückliche HTTPD-Aktivierung, verbietet Redirect-/Authentifizierungs-/Timeout-/Fremdkomponenten-Fallbacks, prüft den literalen Digest vor der Archivauflistung und erhält die kanonische Cache-Identität mit tatsächlichen Download-Metadaten. Der ausgewählte Framework-Gitlink wird in CRS-Workflow und Vertragsfixture synchronisiert; `common.sh`, `.gitmodules` und die MRTS-Revision bleiben unverändert.

Der kanonische Traefik-No-CRS-Host wurde gebaut und gestartet, aber seine Route
scheiterte, weil Yaegi den `syscall`-Import des Observers deaktivierte. Der
gepinnte Traefik-`3.7.13`-Loader reproduzierte diesen Fehler. Das feste
Observer-Manifest deklariert jetzt `useUnsafe: true`, und ausschließlich seine
Plugin-spezifischen Betreibereinstellungen aktivieren diese Anforderung
explizit; beide Deklarationen sind notwendig. Statische Konfiguration und
beide Smoke-Einstiegspunkte aktivieren `experimental.abortOnPluginFailure`,
um den Start bei Ladefehlern abzubrechen. Die Quelle bleibt der feste
eingecheckte Observer, der ohne Symlinks in einem privaten Arbeitsverzeichnis
bereitgestellt wird. Es gibt keine globale Aktivierung oder Aktivierung für
andere Plugins; die Linux-`SO_PEERCRED`-UID-/GID-Authentifizierung bleibt
intakt und wird nicht zur Umgehung des Importfehlers entfernt.

Gewöhnliche Auswahl wird im exakten Datenrecord mit fünf Feldern
`ci/tooling/project-versions.lock.json` zentralisiert: Schema `1`, Framework-/MRTS-
Revisionen, Python `3.14.7` und Go `1.27.1`. Generierte `.python-version`-/
`.go-version`-Ansichten bleiben mit Setup-Actions kompatibel; die Go-Modul-
Untergrenze `1.26.5` bleibt getrennt. Komponentendefinitionen gehören weiterhin
zur `ci/lib/common.sh` des ausgewählten Frameworks; der unveränderliche Framework-
Pin wählt diese Quelle ohne duplizierte Komponentenautorität aus. Geschützte
Broker-Tupel bleiben unabhängig. Der Reader prüft den exakten Parent-Git-Blob,
aufgezeichnete Gitlinks und materialisierte HEADs unabhängiger Repositorys bei
deaktivierten Replacement-Objekten. Updater erhalten unabhängige zentrale Felder,
validieren bestehende und neue Kandidaten und teilen einen Directory-`flock`.
Identitäts-/Inhaltsprüfungen und Erfassungen der Ersetzung vor Directory-fsync
sichern Rollback ab, ohne crash-atomare Mehrdateiupdates zu behaupten. Die
zweisprachige [Versionspin-Referenz](../../../docs/reference/version-pins.de.md)
erläutert diese Kontrollen und native Ansichtssynchronisierung.

Ein weiterer echter Traefik-Host-Fehler lieferte `503`/`403` statt der erlaubten
Kontrolle: Yaegi wählte den Nicht-Linux-Peer-Credential-Stub, wenn nur moderne
`//go:build`-Constraints vorhanden waren. Passende ältere Zeilen `// +build linux`
und `// +build !linux` ergänzen jetzt beide modernen Constraints. Dies erhält
das fehlgeschlossene Nicht-Linux-Verhalten und die Linux-UID-/GID-Authentifizierung.

Der sequenzielle Smoke-Report scheiterte an einem Producer-/Eingabe-Mismatch:
Sein nativer Apache-/NGINX-Producer kann die von der allgemeinen strikten
Aktualisierung erwarteten Full-Matrix-/MRTS-Eingaben nicht liefern. Dedizierte
Ziele `test-smoke-sequential-no-crs` und `test-smoke-sequential-with-crs`
verwenden jetzt ausschließlich für diesen Workflow `bounded-smoke`.
Allgemeines `test-no-crs`/`test-with-crs` und der vollständige Katalog von
`refresh-all-reports` (`--strict-inputs`) bleiben erhalten. Die aktuelle native
Fallermittlung liefert im diagnostizierten Scope Apache 54 und NGINX 60 Fälle;
die Validierung ermittelt exakte variantenspezifische Mengen statt fest
codierter Zahlen. Frische Coverage- und Runtime-Cache-Reports desselben Runs
sind verpflichtend. Ein privater Beleg ist durch exakte Parent-Blob-/Gitlink-
Prüfungen an Framework/MRTS, festen Modulpfad, Run-Identität und native
Fallauswahl gebunden. Alle Zeilen müssen Variante/Connector entsprechen, live
sein und ohne Ausnahmen bestehen. Fehlende/zusätzliche Fälle, Revisions-/
Variantendrift, veraltete/symlinkbasierte Eingaben und fehlgeschlagene/blockierte
Producer-Return-Codes scheitern. Der Snapshot-Generator muss frische Parent-
eigene, Run-gebundene Ausgabe erzeugen; generierte Reports werden nicht gestagt.
Dies gleicht die Validierung dem echten Producer an, schwächt das vollständige
Gate nicht ab und erhöht keine Full-Matrix-, MRTS- oder Response-Body-Evidence.

Nach dem Report-Profil folgt eine erforderliche With-CRS-Bootstrap-Korrektur:
Der abgelöste `5605febc`-Job `111165203104` scheiterte tatsächlich um `08:43` UTC,
weil `prepare-fresh-crs-source.sh` `ci_require_absolute_path` aufrief, bevor die
Framework-`ci/lib/common.sh` geladen war. Dieser Fehler trat trotz einer
Abbruchanforderung auf; er wird nicht als reiner Abbruch eingestuft. Die Runtime
lieferte `77`, bevor Producer-Eingaben existierten, und das Gate für frische
Eingaben wies das fehlende Apache-Ergebnis korrekt zurück. Das begrenzte Rezept
lädt jetzt den tatsächlichen Framework-Common-Helper vor dem Parent-CRS-Helper.
Die ausgeführte Shell-Regression deckt beide Varianten, ein frisches
`RESULTS_DIR`, leere geerbte Scope-Flags, Fetch-vor-Producer-Reihenfolge und
tatsächliche Relative-Path-Ablehnung vor dem Abruf ab. Der Profil-Lauf mit
18 Tests bestand in 9.315 Sekunden. Vollständige Report-/Fallvalidierung bleibt erhalten.

Die Full-Smoke-Artefakte des veröffentlichten
`4d42e818d4fc8ab85ebc028d6276fd3aa380aedc` belegen Apache 54/54 No-CRS- und
55/55 With-CRS-Fälle, alle live `PASS`, ohne Fehler oder Skips. Gewöhnliches
NGINX blieb durch den unprivilegierten Wrapper und den impliziten Output-Root-
Mismatch blockiert; dies sind keine Full-Smoke-Pässe. Der ausstehende
Coordinator verwendet die bestehende typisierte Functional-A-Fallroute für
die geschlossenen gewöhnlichen NGINX-Kataloge mit 60/61 Fällen. Unprivilegierte
Bereitstellung geht einer festen sauberen `sudo`-/`env -i`-Übergabe voraus,
mit unabhängig geprüften committeten Revisionen, nativem Katalog, Runtime-
Artefakten und vorbereitetem CRS. Fall-Runtimes sind frisch, Worker bleiben
getrennt/nicht Root, und vollständige Live-Records werden vor unprivilegierter
nativer Normalisierung in private begrenzte Runner-Evidence projiziert.
Harness-`case-info` erhält seinen validierten privaten Work-Root ausdrücklich
als `--output-root`. Geschützte Broker-Aktivierung/Attestierung bleibt getrennt.

Am selben veröffentlichten Head beobachtete die generische Traefik-Runtime echte
`200`/`403` und erfolgreiche Fälle, aber das Inventar erbte eine veraltete
Binary-Auswahl. Der neue Resolver lässt nur das exakte aktuelle Connector-Build-
Staging zu, weist unsichere Dateien zurück und bietet keinen geerbten/Cache-
Fallback; das native Profil bleibt getrennt. Ein dediziertes
`check-bounded-smoke-runtime-contract` führt die vier zuständigen Unit-Module
im Full-Workflow aus; die kopierte Updater-Baseline bleibt von Framework-
Materialisierung isoliert. Der Quell-Security-Review ist jetzt abgeschlossen, ohne verbleibende konkrete
Findings; finale lokale Validierung steht unten. CI des neuen Heads und
vollständige Runtime-Evidence bleiben ausstehend.

## Geänderte Dateien

- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/cleanup-artifacts.yml`
- `.github/workflows/reusable-five-connectors-profile.yml`
- `.github/workflows/open-connectors-smoke.yml`
- `.github/workflows/nginx-root-broker.yml`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-traefik.yml`
- `.github/workflows/update-go-version.yml`
- `.github/workflows/update-python-version.yml`
- `.github/workflows/update-submodules.yml`
- `.github/workflows/update-workflow-tools.yml`
- `Makefile`
- `ci/lib/framework_revision_pins.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/evidence/reports/refresh-connector-reports.py`
- `ci/runtime/broker/nginx_root_broker.py`
- `ci/runtime/lifecycle/run-connector-stage.sh`
- `ci/runtime/lifecycle/with-private-sockets.py`
- `ci/tooling/project-versions.lock.json`
- `ci/tools/read-framework-revisions.py`
- `ci/tools/sync-framework-component-versions.py`
- `ci/tools/sync-project-versions.py`
- `ci/tools/update-workflow-tools.py`
- `ci/tools/verify-framework-candidate-contract.py`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/start_envoy_connector.sh`
- `connectors/traefik/config/traefik-response-observer-static.yaml`
- `connectors/traefik/response_observer/.traefik.yml`
- `connectors/traefik/response_observer/peercred_linux.go`
- `connectors/traefik/response_observer/peercred_other.go`
- `connectors/traefik/scripts/runtime_smoke.py`
- `connectors/apache/src/mod_security3.c`
- `connectors/apache/src/msc_filters.c`
- `connectors/nginx/config`
- `connectors/traefik/scripts/start-smoke.sh`
- `docs/reference/variables.de.md`
- `docs/reference/variables.md`
- `docs/reference/version-pins.de.md`
- `docs/reference/version-pins.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- `docs/security/trusted-nginx-root-broker.md`
- `modules/ModSecurity-test-Framework`
- `reports/audits/change-records/CR-20261001-ci-recovery.de.md`
- `reports/audits/change-records/CR-20261001-ci-recovery.md`
- `scripts/version_updater_common.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/framework_sha_fixture.py`
- `tests/test_apache_intervention_cleanup.py`
- `tests/test_c_cpp_diagnostics.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_full_smoke_workflow_contract.py`
- `tests/test_framework_revision_pins.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_private_runtime_sockets.py`
- `tests/test_project_toolchain_pins.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `tests/test_traefik_runtime_smoke_security.py`
- `tests/test_update_framework_versions.py`
- `tests/test_update_go_version.py`
- `tests/test_update_python_version.py`
- `tests/test_update_submodules_local_git.py`
- `tests/test_verify_framework_candidate_contract.py`
- `tests/version_updater_test_support.py`
- `ci/runtime/lifecycle/run-bounded-nginx-cases.py`
- `ci/runtime/lifecycle/resolve-traefik-host-binary.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_all_connectors_no_crs_workflow_contract.py`
- `tests/test_bounded_nginx_cases.py`
- `tests/test_resolve_traefik_host_binary.py`
- `tests/test_nginx_harness_path_authority.py`

## Ausgeführte Befehle

Alle lokalen Befehlseinstiegspunkte verwendeten RTK. `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`: PASS, 175 Tests, fünf bestehende umgebungsbedingte Skips sowie Provenance-Validierung für actionlint/zizmor/gitleaks. Die Updater-Suite bestand 38 Tests einschließlich echter Validierung des vorgeschlagenen Baums; Workflow-Verträge bestanden 31 Tests. Die koordinierte integrierte Regressionsvalidierung bestand 118 Tests. Actionlint bestand für alle 31 Workflows. Quick-check erreichte nach 600 Sekunden beim HAProxy-Check das Zeitlimit; dies ist kein vollständiger Quick-check-Pass.

```sh
rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_private_runtime_sockets tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.ci_security.test_update_workflow_tools
rtk proxy bash -c '/root/go/bin/actionlint .github/workflows/*.yml'
```

Der integrierte Lauf mit 118 Tests dauerte 98.147 Sekunden. Task-Evidence ist unter `/var/tmp/codex/ModSecurity-conector/ci-recovery-inventory.md`, `/var/tmp/codex/ModSecurity-conector/ci-recovery-20261001-plan.md` und `/var/tmp/codex/ModSecurity-conector/ci-recovery-ci-contract.log` aufbewahrt.

Die begrenzte Wiederholung mit `rtk proxy env CI=true ... timeout 600 make quick-check`, denselben externen Build-/Log-Wurzeln und Interpretern bestand (Exit 0, 275 Tests). Das native Lint übersprang die C17-Kompilierung für NGINX und HAProxy ausdrücklich wegen fehlender Header. Der frühere lokale Zeitabbruch entstand bei der automatischen Bereitstellung von Voraussetzungen vor den HAProxy-Compilerproben. Diese Ergebnisse belegen die beiden übersprungenen Compilerprüfungen nicht. Das Wiederholungslog liegt unter `/var/tmp/codex/ModSecurity-conector/ci-recovery-quick-check-ci.log`.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links
rtk git diff --check
```

Record-Struktur, zweisprachige Dokumentation, Repository-Pfadreferenzen, Dokumentationslinks und Diff-Whitespace-Prüfungen bestanden.

Die integrierte Validierungsaufnahme zur geschlossenen CLI bestand 121 Tests in 101.701 Sekunden. Das Framework-eigene Ziel `test-httpd-source-recovery` mit Python 3.14.7 bestand 18 Tests in 57.008 Sekunden auf dem ausgewählten master `6948ec5b916e400c4fcaa1b6ccfa64251f606f8d`; Kandidatenvertragsprüfung und nativer Synchronisierungscheck bestanden. Die Parent-Bereitstellungssuite bestand 95 Tests mit fünf bestehenden Skips; der generische Cache-Vertrag bestand 45 Tests. Der echte Parent-HTTPD-Abruf stellte nach der kanonischen 404 dasselbe offizielle Archiv wieder her und verifizierte SHA-256 `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06` vor der Archivauflistung. Vor dem Commit des ausgewählten Gitlinks bestand ein weiterer nativer Quick-check im CI-Modus nach den HTTPD-/Framework-Änderungen (Exit 0, 280 Tests), mit neun Fixture-Skips, weil der ausgewählte Framework-Checkout neuer als der noch committete Parent-Gitlink war, sowie den beiden Compiler-Skips wegen fehlender Header. Das Log liegt unter `/var/tmp/codex/ModSecurity-conector/ci-recovery-quick-check-final.log`. Diese Prüfungen belegen den Abruf und ihre jeweiligen lokalen Verträge; sie belegen weder einen frischen gehosteten Parent-HTTPD-Runtime-Pass noch einen neuen Sonar-Pass.

Der hashgeprüfte Traefik-3.7.13-Host bestand alle 20 Runtime-Sicherheitstests, einschließlich echtem Laden der Route und Startabbruch bei fehlender Importfreigabe in einer der beiden Deklarationen. Die nativen Go-Unit-Tests und vet des Observers bestanden ebenfalls mit der vorhandenen Go-1.27.1-Toolchain. Diese Prüfungen belegen Loader-Verhalten und Observer-Quellprüfungen; vollständige gehostete Engine-Transaktionen bleiben separate Evidence.

Die koordinierten zentralen Lock-Regressionsaufnahmen bestanden 18 Reader-Tests,
16 Toolchain-Tests, eine kombinierte Suite mit 83 Tests und 55 Framework-
Synchronizer-Tests. Dies sind begrenzte Aufnahmen; finale integrierte und gehostete
Evidence für den neuen Quell-Head bleibt erforderlich. Die hashverifizierte
Traefik-Host-/Engine-Validierung bestand 29 Tests ohne Skips, einschließlich
authentifiziertem `MRC1`-`CLAIM`-Erfolg bei gleicher UID und Ablehnung einer falschen
UID vor Frame-Bytes. Go-Unit-/vet-Prüfungen des Observers bestanden und der Nicht-
Linux-Stub blieb fehlgeschlossen. Eine echte lokale Runtime mit aktuellem C-Service
und gepinntem Traefik beobachtete erlaubte `200` und verweigerte `403`. Diese lokalen
Prüfungen ersetzen keine gehostete Engine-Evidence des finalen Heads.

Die anschließende native Zentralisierungsvalidierung bestand 216 CI-Sicherheits-
Vertragstests mit fünf bestehenden Umgebungs-/Privilegien-Skips, 38 vollständige
Workflow-/Tool-Updater-Tests und 74 Updater-/Sprachvertragstests. Die 19 Reader-
und 16 zentralen Toolchain-Tests sind im Vertragsergebnis mit 216 Tests enthalten.
Actionlint bestand für alle 31 Workflows; Zweisprachigkeits-, Link-, Variablen-
und Connector-Konfigurationsprüfungen bestanden, mit 21 aktuellen generierten
Konfigurationsdateien. Diese Prüfungen belegen keinen gehosteten Runtime-Erfolg.
Die Quellreparaturen für Legacy-Event-Pfad und Full-NGINX-Profile-Registry-Root
sind jetzt wie unten beschrieben implementiert; auch die Apache-`413`-Quellreparatur ist implementiert und besitzt getrennte lokale Evidence unten. Ein Pass aller Workflows wird nicht behauptet.

Der Legacy-Traefik-Smoke-Starter materialisiert jetzt ausschließlich seine
eingecheckte Standardkonfiguration im privaten Run-Verzeichnis mit Run-lokalem
`event_path`; eine explizit übergebene Konfiguration bleibt unverändert.
Staged-NGINX-Konfiguration löst eine fehlende Profile Registry ausschließlich
aus einem übergebenen kanonischen `common/include`-Layout mit SDK-Header auf.
Die Priorität eines expliziten Registry-Roots bleibt erhalten; ungültige oder
unabhängige Roots scheitern. Die Diagnostics-Regression führte vier positive/
negative Config-Prefix-Fälle aus. Die Traefik-Sicherheitsvalidierung bestand
31 Tests mit zwei Skips wegen fehlendem Host in diesem lokalen Lauf; eine
getrennte Startprüfung mit echtem C-Service und gepinntem Host bestand.
Ein nativer Quick-check nach diesen abgeschlossenen Korrekturen bestand
(Exit 0, 280 Tests, keine Unit-Skips), ausschließlich mit den beiden expliziten
NGINX-/HAProxy-C17-Compiler-Skips wegen fehlender Header. Er fand vor der noch
ausstehenden Apache-Reparatur statt und validiert sie nicht. Die Fixture-
Grammatikkorrektur deckt stabile Go-Versionen `1.0.0`/`2.0.1` ab; ihr zusätzlicher
Framework-Lauf mit 32 Tests bestand.

Die Apache-Korrektur löst globale Common-Konfigurationsdefaults lokal in
`connectors/apache/src/mod_security3.c` und `connectors/apache/src/msc_filters.c`
auf und erhält explizit konfigurierte Grenzen, statt nicht gesetzte Grenzen
als null zu behandeln. Alle 12 zuvor fehlschlagenden Fälle bestanden mit echtem
lokalem Apache `2.4.66` und Engine `3.0.14`. Ein kleiner erlaubter Body lieferte
`200`; ein übergroßer Body mit `1048577` Bytes lieferte `413` mit korrekten
Zählern. Die 22 gezielten Tests und C17-Kompilierung mit
`-Wall -Wextra -Werror` bestanden. Die gehostete ausgewählte Runtime mit Apache
`2.4.68`/Engine `3.0.16` benötigt weiterhin Evidence des neuen Heads.

Die vollständige Workflow-/Tool-Suite bestand erneut 38 Tests mit der nativen
Make-Voraussetzung; die Root-Traefik-/Engine-/C++-Validierung mit echtem Host
bestand 38 Tests ohne Skips. Die unten beschriebene begrenzte Report-Quellkorrektur ist implementiert;
ihre finalen gezielten Regressionen bestanden wie unten aufgezeichnet;
gehostete Validierung des neuen Heads steht noch aus. Ein Erfolg aller Workflows wird nicht behauptet.

Die nachfolgende Quellvalidierung bestand 35 Reader-/Toolchain-Tests,
34 Framework-Sync-Tests, 219 CI-Vertragstests mit fünf bestehenden Umgebungs-/
Privilegien-Skips und 38 vollständige Workflow-/Tool-Tests. Die Produktions-CLI
des Synchronizers ist jetzt an ihr eigenes Parent-Repository gebunden;
Fixture-APIs bleiben getrennt. Partial-Callback, ASCII-erhaltende Regex-
Bereinigung, isolierte Exception-Assertions und Status-Refactoring beheben die
beobachteten Findings ohne Unterdrückung. Die finale Suite zum begrenzten Profil bestand 16 Tests nach dem Leeren von
`FORCE_ALL_CASES` und Ergänzen fester CLI-Root-, Pfad- und Timeout-Schutzbedingungen.
Die kombinierte Report-/Reader-/Integritätssuite bestand 116 Tests vor diesen
letzten Schutzbedingungen; dieses frühere kombinierte Ergebnis deckt sie nicht
ab. Finales actionlint bestand für alle 31 Workflows. Sonar- und gehostete
Runtime-Ergebnisse des nächsten exakten Heads bleiben erforderlich.

Das finale native `make check-bounded-smoke-runtime-contract` bestand 61 Tests
in 17.044 Sekunden: 18 Report-/Wiring-, 23 Coordinator-, 14 Harness-Pfad- und
sechs Host-Resolver-Tests. Native CI-Sicherheitsvalidierung bestand 219 Tests
in 105.446 Sekunden mit fünf bestehenden Privilegien-Skips; die vollständige
Workflow-/Tool-Suite bestand 38 Tests in 98.561 Sekunden, und actionlint bestand
für alle 31 Workflows. Der unabhängige Security-Review endete ohne verbleibendes
konkretes Finding. Diese Ergebnisse sind lokale Quellvalidierung, kein
gehosteter Pass des nächsten Heads.

Der Legacy-Lauf [37111252518](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37111252518)
des veröffentlichten Heads scheiterte bei `runtime-smoke-traefik`. Er verwendet
denselben Baseline-Consumer, aber die Host-Versionsursache wurde nicht direkt
belegt, weil das normalisierte Ergebnis in den aufbewahrten Artefakten fehlte.
Die begrenzte Retention-Korrektur exportiert aktuelles `RUNTIME_EVIDENCE_ROOT`
unter verifiziertem `evidence/runtime-evidence` und ergänzt ausschließlich diese
aktuelle Evidence im bestehenden Collector, ohne Cache-, Quell- oder Build-
Bäume. Die eingefrorene Retention-/Topologie-Quelle bestand 71 Tests in 29.688 Sekunden
über `tests.test_runtime_env_snapshot_contract`, `tests.test_collect_no_crs_source`
und `tests.test_resolve_traefik_host_binary`. Der Snapshot-Vertrag verlangt einen
eindeutigen Root-eigenen `0711`-Namespace, einen privaten Runner-eigenen `0700`-
Provisioning-Root und einen getrennten Worker, der diesen privaten Root nicht
traversieren kann. Actionlint bestand nach diesen Änderungen erneut für alle
31 Workflows.

Die zusätzliche No-CRS-Suite zeigte zwei veraltete Test-Assertions, die
Workflow-weite Leserechte statt bereits strengerem `permissions: {}` mit festen
Job-Lesegrants erwarteten. Die korrigierten Assertions erhalten Deny-Default
und prüfen diese expliziten Job-Grants. Der wiederverwendbare Fünf-Connector-
Workflow führt dieses Vertragsmodul jetzt vor der Matrixauflösung aus. Die
tatsächlichen zuständigen Module `tests.test_no_crs_selected_runner_wiring`,
`tests.test_five_connector_no_crs_profile` und
`tests.test_all_connectors_no_crs_workflow_contract` bestanden 28 Tests in
10.125 Sekunden. Lokale Quellvalidierung ist für diese Auslieferungsaufnahme
abgeschlossen; frische gehostete/Sonar-Evidence des exakten Heads bleibt
erforderlich. Die ursprüngliche Legacy-Host-Versionsursache bleibt unbelegt,
weil ihr normalisiertes Artefakt fehlte.

## Security-Auswirkung

Publisher-Identität, Abstammung gemergter PRs, expliziter Schreibumfang, standardmäßig verweigerte Berechtigungen, unveränderliche Action-Pins und Runtime-Isolation bleiben durchgesetzt. Die Traefik-Staging-Zulassung ist exakt und erweitert das Vertrauen nicht allgemein auf Build-Verzeichnisse. Socket-Wurzeln sind privat und validiert. Die Aktivierung eingeschränkter Yaegi-Imports ist auf den festen lokalen Observer begrenzt und erhält die Linux-Peer-Credential-Authentifizierung; ein Ladefehler bricht den Start ab. Diese Änderung enthält keine Framework-/MRTS-Quelländerungen. Nur der Framework-Gitlink des Task-Parents wird von `9181dc77dfb0685d87fa109e6800dc6052d77cc9` auf den geprüften Framework-master `6948ec5b916e400c4fcaa1b6ccfa64251f606f8d` angehoben; die ursprünglichen Arbeitscheckouts bleiben erhalten und MRTS bleibt `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. Framework-PR 133 war bereits vor der Auswahl gemergt; dieser Task führt keinen Framework-Merge aus.

## Runtime-Evidence

Der frische Framework-Publisher-Lauf [36908638390](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36908638390) war auf master `6948ec5` erfolgreich und erstellte Draft-[PR 134](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/134), Head `51c70128693f0e836d8bff8af947232bca0691fc`. Alle 20 Prüfungen endeten ohne Fehler, mit drei advisory Skips; Sonar meldete OK. Dies belegt Framework-Publisher/PR-Prüfungen, keine frische Parent-Connector-Runtime. Bei der ursprünglichen Quellbereitstellung stand gehostete Parent-Validierung noch aus.

Die erste Parent-Bereitstellung erfolgte als [PR 400](https://github.com/Easton97-Jens/ModSecurity-conector/pull/400), Head `35259700fcf0558e430f5fc78cc4f7c3920e92ce`. Reguläre GitHub-Prüfungen waren grün, während Runtime-Prüfungen noch liefen; das genaue Sonar-Ergebnis war `ERROR` mit Sicherheitsbefunden zu `S5443` (Auswahl temporärer Pfade aus der Umgebung) und `S8705` (generischer CLI-Befehl) sowie fünf Maintainability-Findings. Die anschließende Quellkorrektur beschränkt die CLI auf feste Envoy-/Traefik-Lifecycle-Auswahl und einen ausdrücklich übergebenen, validierten Socket-Elternpfad. Dieser Fehler des ursprünglichen Heads ist historisch; das Ergebnis des veröffentlichten korrigierten Heads steht unten. Findings wurden weder unterdrückt noch als False Positive eingestuft, und Gates wurden nicht abgeschwächt.

Manuelle Läufe des ursprünglichen Heads: [36912803996](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912803996) (kanonisches No-CRS), [36912808790](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912808790) (Legacy Open Connectors) und [36912813685](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912813685) (Full Smoke mit deaktivierter Bereinigung). Die erste gehostete Runde ist jetzt abgeschlossen: Kanonisches No-CRS für Envoy, HAProxy und lighttpd bestand; CRS für Envoy, Traefik, HAProxy und lighttpd bestand; NGINX am exakten Head bestand. Der kanonische Apache-Job, Legacy Open Connectors und Full Smoke waren durch die HTTPD-404 blockiert. Kanonisches No-CRS für Traefik scheiterte an der Route-Readiness und zeigte den oben beschriebenen Observer-Ladefehler. Diese Ergebnisse des ursprünglichen Heads sind historisch; ein Pass aller Workflows wird nicht behauptet. Gehostete Ergebnisse sind immer an ihren genauen SHA gebunden; finale Bereitstellung und CI-Rücklesung werden in PR 400 und im Task-Ausführungsplan nachgehalten.

Der korrigierte Commit `e240bb2d4e21da9eb832c94dec7df672167b6636` wurde in PR 400 veröffentlicht. Seine exakte Sonar-Analyse um `2026-10-03T06:35:23+0000` meldete Quality Gate `OK` und null Vulnerabilities, mit vier Maintainability-Findings: drei Regex-Findings zu `S6353` und einem Complexity-Finding zu `prepare_archive` nach `S3776`. Die Nachbesserung vereinfacht diesen bestehenden Helper und verwendet `re.ASCII`, um ausschließlich ASCII-basiertes Matching zu erhalten; HTTPD-Wiederherstellungsregeln und Runtime-Verträge bleiben unverändert. Diese Nachbesserung erhält einen neuen Head; das genannte Sonar-Ergebnis validiert ihn daher nicht.

Der native Quick-check im CI-Modus nach dem Commit auf `e240bb2d4e21da9eb832c94dec7df672167b6636` bestand (Exit 0, 280 Tests) ohne Unit-Test-Skips: Die neun früheren Gitlink-Fixture-Skips entfielen durch den Commit des ausgewählten Gitlinks. Nur die beiden ausdrücklich gemeldeten NGINX-/HAProxy-Compilerprüfungen blieben wegen fehlender Header übersprungen.

Frische Runtime-Läufe des korrigierten Heads [37103593221](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103593221) (kanonisches No-CRS), [37103594952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103594952) (Legacy Open Connectors), [37103596368](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103596368) (Full Smoke mit deaktivierter Bereinigung) und [37103555691](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103555691) (CRS) liefen bei dieser Aufnahme ohne beobachteten Fehler. Laufende Jobs sind keine bestandenen Prüfungen. Bereitstellung, Prüfungen und Sonar-Rücklesung des finalen Heads bleiben in PR 400 und im externen Task-Plan nachgehalten, um eine reine Dokumentations-CI-Schleife zu vermeiden.

Die Maintainability-Korrektur wurde als `f986fe7ef8e46a0a838a8937b2986d6ffd564208`
veröffentlicht. Ihre exakte Sonar-Analyse um `2026-10-03T06:43:34+0000` meldete
Quality Gate `OK`, null Bugs, null Vulnerabilities und null Code Smells, ohne
Unterdrückung oder Gate-Abschwächung. Die vorherigen schweren `e240bb2`-Läufe wurden
abgelöst/abgebrochen; ihre obige Laufzustandsaufnahme ist historisch und erfüllt
keine Abschlusskriterien. Die `f986fe7`-CRS-Runde bestand alle fünf ausgewählten
Connector-Jobs und das Aggregat. Die nachfolgende Zentralisierung und die Yaegi-
Build-Constraint-Korrekturen benötigen einen neuen exakten Head und frische
gehostete/Sonar-Evidence; keiner der früheren grünen Scans validiert sie.

Der nächste ausgelieferte Commit `1ca0d4be9f008f30344a46bb084f324e8fd8f496`
bestand den strikten Reader nach dem Commit gegen seine tatsächlich committeten
Lock-Blob-/Gitlink-Daten; Remote-Task-Branch und PR-400-Head entsprachen exakt
diesem SHA. Alle automatischen Prüfungen dieses exakten Heads sind jetzt abgeschlossen
und erfolgreich, einschließlich der zuvor laufenden CRS- und NGINX-Prüfungen
am exakten Head. Die Sonar-Analyse um
`2026-10-03T07:42:59+0000` meldete `ERROR` mit einem Finding zu `S8707` und sechs
Maintainability-Findings. Die obigen nachfolgenden Quelländerungen beheben diese
Findings, aber ihr Sonar-Ergebnis am neuen Head steht noch aus. Frühere grüne
Scans sind historisch und belegen keine Qualität des nächsten Heads.

Die Korrektur des begrenzten Profils wurde als
`5605febc27dd741a561ede13003a7b47cedce5ae` mit der beobachteten Profilvalidierung
von 16 Tests veröffentlicht. Ihre exakte Sonar-Analyse um
`2026-10-03T08:27:06+0000` meldete Quality Gate `ERROR`, null Bugs, eine
Vulnerability und einen Code Smell. Alle sieben früheren `1ca0d4b`-Findings waren
behoben. Das neue Finding `S8705` betrifft die in Metadaten-Befehlsargumente
interpolierte Variante: Diese besitzt bereits argparse-/Identitäts-Allowlists
und keine Shell-Ausführung; die Beobachtung validiert daher keinen Injection-
Pfad. Die gezielte Korrektur wählt ausschließlich literale interne Befehle,
und die `S9073`-Korrektur teilt eine zusammengesetzte Test-Assertion auf;
kein Finding wird unterdrückt. Die korrigierte Profilsuite bestand 17 Tests in 9.514 Sekunden; der ergänzte
Pipeline-Argument-Assertion-Test bestand anschließend ebenfalls. Der Helper
liefert nur zwei interne Literalbefehle, und eine ungültige Variante stoppt vor
dem Generator. Eine neue Sonar-Analyse des exakten Heads bleibt erforderlich.

Reguläre Prüfungen auf `5605febc` waren bislang erfolgreich; die fünf CRS- und
fünf No-CRS-Connector-Runtimes, Legacy Smoke und sequenzieller Full Smoke standen
noch aus. Diese Teilergebnisse sind kein vollständiger Runtime-Pass und
validieren die nachfolgende Befehlsauswahlkorrektur nicht.

Die Literal-Label-Korrektur wurde als
`a0ad0ef7de7ca4aa197705760c0932d68fbb3949` veröffentlicht. Die exakte Sonar-
Analyse um `2026-10-03T08:33:53+0000` meldete Quality Gate `OK`, null Bugs,
Vulnerabilities und Code Smells; alle Findings waren ohne Unterdrückung behoben.
Reguläre Prüfungen sind alle erfolgreich; CRS für Envoy/Traefik/lighttpd bestand,
während übrige schwere und Exact-Head-Runtime-Prüfungen bei dieser Aufnahme noch
ausstanden. Die frühere `5605febc`-No-CRS-Diagnose war noch aktiv. Die obige
Bootstrap-Quellkorrektur erhält einen neuen Head und benötigt frische CI-/Sonar-
Evidence; der `a0ad0ef7`-Erfolg validiert sie nicht und belegt keinen Pass aller
Runtime-Workflows.

Der Bootstrap-Commit `4d42e818d4fc8ab85ebc028d6276fd3aa380aedc` besitzt eine
exakte Sonar-Analyse um `2026-10-03T08:51:35+0000`: Quality Gate `OK`, null Bugs,
Vulnerabilities/Code Smells und offene Issues. Die obigen Apache- und Traefik-
Beobachtungen gehören zu diesem veröffentlichten Head. Sie diagnostizieren
die verbleibenden gewöhnlichen NGINX-Orchestrierungs- und Host-Inventarfehler;
sie validieren die ausstehenden Quellkorrekturen nicht. Finale Auslieferungs-/
Runtime-/Sonar-Evidence des nächsten Heads wird in PR 400 und dem externen
Ausführungsplan erhalten, statt versionierte Dokumentation wiederholt allein
für CI-Status zu ändern.

Die gewöhnliche Runtime-/Inventarkorrektur wurde als
`11b7e1b0f64235741c2d05c5107f448ea0ebc9d2` veröffentlicht. Ihre exakte Sonar-
Analyse um `2026-10-03T10:02:16+0000` meldete Quality Gate `ERROR`: null Bugs,
ein Security-Finding zu `S8705` und zehn Code Smells. Die nachfolgende
Quellkorrektur ordnet die CLI-Variante vor Launcher- oder Pfadaktionen explizit
festen Literalen zu; unbekannte Werte werden abgelehnt. Konstanten, äquivalente
Exception-Basisklassen und eine potenziell fehlschlagende Operation pro Testkontext beheben die
begleitenden Findings. Unterdrückung oder Gate-Änderung wird nicht verwendet.
Die korrigierte Coordinator-Suite bestand 24 Tests; natives
`make check-bounded-smoke-runtime-contract` bestand 62 Tests in 17.263 Sekunden.
Ein neuer ausgelieferter Head und seine exakte Sonar-/Hosted-Runtime-Evidence
stehen noch aus; diese lokalen Ergebnisse sind kein gehosteter Pass des neuen Heads.

## Bekannte Einschränkungen

Lokale privilegienabhängige Namespace-Integration hatte fünf bestehende Skips. Quick-check im CI-Modus bestand mit den beiden Compiler-Skips wegen fehlender Header; der normale lokale Versuch erreichte das Zeitlimit. Der geschützte Broker-Caller bleibt auf `49c40779a7b6de9f699391bcd524ea069787df42` gepinnt; dieser Patch allein aktiviert die geänderte Broker-Quelle nicht.

## Verbleibende Risiken

Eine geprüfte geschützte Broker-Aktivierung/Neupinnung und echte Evidence für beide ausgewählten Broker-Profile bleiben erforderlich. Gehostete Parent-Ausführung kann weitere Runner-spezifische Fehler aufdecken. Das aktuelle explizite Updater-Inventar verhindert unbemerkte Veröffentlichungslücken; neue Workflows müssen geprüft und in Inventar sowie Staging aufgenommen werden.

## Nicht ausgeführte Prüfungen mit Begründung

Ein vollständiger gehosteter Parent-Pass und beide geschützten Broker-Runtime-Profile stehen aus. Die Integration in Parent master war nicht autorisiert; daher wurden weder Integration noch geschützte Aktivierung/Neupinnung ausgeführt. Für die lokalen C17-Compilerprüfungen von NGINX und HAProxy fehlen Header-Voraussetzungen.

## Finaler Diff- und Review-Status

Die ursprünglichen und korrigierten Änderungen wurden in PR 400 bereitgestellt. Für den zuletzt veröffentlichten Head `11b7e1b0` liegt die obige Sonar-Aufnahme `ERROR` vor. Die gezielte Varianten-/Findings-Korrektur bestand lokale Coordinator- und Runtime-Vertragsvalidierung; Auslieferung und frische gehostete/Sonar-Evidence des exakten Heads bleiben erforderlich. Frühere Apache-/Traefik-Evidence bleibt an ihren aufgezeichneten historischen Head gebunden. Die Gesamtreparatur bleibt bis zu dieser Evidence und geschützter Aktivierung teilweise abgeschlossen. Die ursprünglichen Arbeitscheckouts bleiben erhalten; nur der Framework-Gitlink des Task-Parents wird wie oben dokumentiert geändert. Weder Parent-master-Integration noch Framework-/MRTS-Quelländerungen werden behauptet. Beide Sprachfassungen enthalten dieselben Werte und Einschränkungen.
