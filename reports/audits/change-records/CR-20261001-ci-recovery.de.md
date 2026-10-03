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

## Akzeptanzkriterien

Regressionen müssen die ursprünglichen Fehler abdecken, ohne Publisher-Identität, Runtime-Isolation, unveränderliche Pins oder standardmäßig verweigerte Berechtigungen abzuschwächen. Die aktuelle gehostete Framework-Veröffentlichung und ihre PR-Prüfungen müssen erfolgreich sein. Gehostete Parent-Validierung und geschützte Broker-Aktivierung bleiben erforderlich, bevor alle Workflows als funktionsfähig gelten.

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

## Geänderte Dateien

- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/cleanup-artifacts.yml`
- `.github/workflows/nginx-root-broker.yml`
- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-traefik.yml`
- `.github/workflows/update-submodules.yml`
- `.github/workflows/update-workflow-tools.yml`
- `Makefile`
- `ci/runtime/broker/nginx_root_broker.py`
- `ci/runtime/lifecycle/run-connector-stage.sh`
- `ci/tools/update-workflow-tools.py`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/start_envoy_connector.sh`
- `connectors/traefik/config/traefik-response-observer-static.yaml`
- `connectors/traefik/response_observer/.traefik.yml`
- `connectors/traefik/scripts/start-smoke.sh`
- `connectors/traefik/scripts/runtime_smoke.py`
- `docs/reference/variables.de.md`
- `docs/reference/variables.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- `docs/security/trusted-nginx-root-broker.md`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `tests/test_traefik_runtime_smoke_security.py`
- `tests/test_update_submodules_local_git.py`
- `ci/runtime/lifecycle/with-private-sockets.py`
- `reports/audits/change-records/CR-20261001-ci-recovery.de.md`
- `reports/audits/change-records/CR-20261001-ci-recovery.md`
- `tests/test_private_runtime_sockets.py`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `modules/ModSecurity-test-Framework`
- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`

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

## Security-Auswirkung

Publisher-Identität, Abstammung gemergter PRs, expliziter Schreibumfang, standardmäßig verweigerte Berechtigungen, unveränderliche Action-Pins und Runtime-Isolation bleiben durchgesetzt. Die Traefik-Staging-Zulassung ist exakt und erweitert das Vertrauen nicht allgemein auf Build-Verzeichnisse. Socket-Wurzeln sind privat und validiert. Die Aktivierung eingeschränkter Yaegi-Imports ist auf den festen lokalen Observer begrenzt und erhält die Linux-Peer-Credential-Authentifizierung; ein Ladefehler bricht den Start ab. Diese Änderung enthält keine Framework-/MRTS-Quelländerungen. Nur der Framework-Gitlink des Task-Parents wird von `9181dc77dfb0685d87fa109e6800dc6052d77cc9` auf den geprüften Framework-master `6948ec5b916e400c4fcaa1b6ccfa64251f606f8d` angehoben; die ursprünglichen Arbeitscheckouts bleiben erhalten und MRTS bleibt `8a6bb546c4c81d8ffc7be801dceac60c6925685f`. Framework-PR 133 war bereits vor der Auswahl gemergt; dieser Task führt keinen Framework-Merge aus.

## Runtime-Evidence

Der frische Framework-Publisher-Lauf [36908638390](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36908638390) war auf master `6948ec5` erfolgreich und erstellte Draft-[PR 134](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/134), Head `51c70128693f0e836d8bff8af947232bca0691fc`. Alle 20 Prüfungen endeten ohne Fehler, mit drei advisory Skips; Sonar meldete OK. Dies belegt Framework-Publisher/PR-Prüfungen, keine frische Parent-Connector-Runtime. Bei der ursprünglichen Quellbereitstellung stand gehostete Parent-Validierung noch aus.

Die erste Parent-Bereitstellung erfolgte als [PR 400](https://github.com/Easton97-Jens/ModSecurity-conector/pull/400), Head `35259700fcf0558e430f5fc78cc4f7c3920e92ce`. Reguläre GitHub-Prüfungen waren grün, während Runtime-Prüfungen noch liefen; das genaue Sonar-Ergebnis war `ERROR` mit Sicherheitsbefunden zu `S5443` (Auswahl temporärer Pfade aus der Umgebung) und `S8705` (generischer CLI-Befehl) sowie fünf Maintainability-Findings. Die anschließende Quellkorrektur beschränkt die CLI auf feste Envoy-/Traefik-Lifecycle-Auswahl und einen ausdrücklich übergebenen, validierten Socket-Elternpfad. Dieser Fehler des ursprünglichen Heads ist historisch; das Ergebnis des veröffentlichten korrigierten Heads steht unten. Findings wurden weder unterdrückt noch als False Positive eingestuft, und Gates wurden nicht abgeschwächt.

Manuelle Läufe des ursprünglichen Heads: [36912803996](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912803996) (kanonisches No-CRS), [36912808790](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912808790) (Legacy Open Connectors) und [36912813685](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36912813685) (Full Smoke mit deaktivierter Bereinigung). Die erste gehostete Runde ist jetzt abgeschlossen: Kanonisches No-CRS für Envoy, HAProxy und lighttpd bestand; CRS für Envoy, Traefik, HAProxy und lighttpd bestand; NGINX am exakten Head bestand. Der kanonische Apache-Job, Legacy Open Connectors und Full Smoke waren durch die HTTPD-404 blockiert. Kanonisches No-CRS für Traefik scheiterte an der Route-Readiness und zeigte den oben beschriebenen Observer-Ladefehler. Diese Ergebnisse des ursprünglichen Heads sind historisch; ein Pass aller Workflows wird nicht behauptet. Gehostete Ergebnisse sind immer an ihren genauen SHA gebunden; finale Bereitstellung und CI-Rücklesung werden in PR 400 und im Task-Ausführungsplan nachgehalten.

Der korrigierte Commit `e240bb2d4e21da9eb832c94dec7df672167b6636` wurde in PR 400 veröffentlicht. Seine exakte Sonar-Analyse um `2026-10-03T06:35:23+0000` meldete Quality Gate `OK` und null Vulnerabilities, mit vier Maintainability-Findings: drei Regex-Findings zu `S6353` und einem Complexity-Finding zu `prepare_archive` nach `S3776`. Die Nachbesserung vereinfacht diesen bestehenden Helper und verwendet `re.ASCII`, um ausschließlich ASCII-basiertes Matching zu erhalten; HTTPD-Wiederherstellungsregeln und Runtime-Verträge bleiben unverändert. Diese Nachbesserung erhält einen neuen Head; das genannte Sonar-Ergebnis validiert ihn daher nicht.

Der native Quick-check im CI-Modus nach dem Commit auf `e240bb2d4e21da9eb832c94dec7df672167b6636` bestand (Exit 0, 280 Tests) ohne Unit-Test-Skips: Die neun früheren Gitlink-Fixture-Skips entfielen durch den Commit des ausgewählten Gitlinks. Nur die beiden ausdrücklich gemeldeten NGINX-/HAProxy-Compilerprüfungen blieben wegen fehlender Header übersprungen.

Frische Runtime-Läufe des korrigierten Heads [37103593221](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103593221) (kanonisches No-CRS), [37103594952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103594952) (Legacy Open Connectors), [37103596368](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103596368) (Full Smoke mit deaktivierter Bereinigung) und [37103555691](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/37103555691) (CRS) liefen bei dieser Aufnahme ohne beobachteten Fehler. Laufende Jobs sind keine bestandenen Prüfungen. Bereitstellung, Prüfungen und Sonar-Rücklesung des finalen Heads bleiben in PR 400 und im externen Task-Plan nachgehalten, um eine reine Dokumentations-CI-Schleife zu vermeiden.

## Bekannte Einschränkungen

Lokale privilegienabhängige Namespace-Integration hatte fünf bestehende Skips. Quick-check im CI-Modus bestand mit den beiden Compiler-Skips wegen fehlender Header; der normale lokale Versuch erreichte das Zeitlimit. Der geschützte Broker-Caller bleibt auf `49c40779a7b6de9f699391bcd524ea069787df42` gepinnt; dieser Patch allein aktiviert die geänderte Broker-Quelle nicht.

## Verbleibende Risiken

Eine geprüfte geschützte Broker-Aktivierung/Neupinnung und echte Evidence für beide ausgewählten Broker-Profile bleiben erforderlich. Gehostete Parent-Ausführung kann weitere Runner-spezifische Fehler aufdecken. Das aktuelle explizite Updater-Inventar verhindert unbemerkte Veröffentlichungslücken; neue Workflows müssen geprüft und in Inventar sowie Staging aufgenommen werden.

## Nicht ausgeführte Prüfungen mit Begründung

Ein vollständiger gehosteter Parent-Pass und beide geschützten Broker-Runtime-Profile stehen aus. Die Integration in Parent master war nicht autorisiert; daher wurden weder Integration noch geschützte Aktivierung/Neupinnung ausgeführt. Für die lokalen C17-Compilerprüfungen von NGINX und HAProxy fehlen Header-Voraussetzungen.

## Finaler Diff- und Review-Status

Die ursprünglichen und korrigierten Änderungen wurden in PR 400 bereitgestellt. Für den veröffentlichten korrigierten Head liegt die oben dokumentierte erfolgreiche Sonar- und lokale Quick-check-Aufnahme vor; die Maintainability-Nachbesserung und die vollständige gehostete Runtime-Validierung benötigen weiterhin Evidence des finalen Heads. Die Gesamtreparatur bleibt bis zu dieser Evidence und geschützter Aktivierung teilweise abgeschlossen. Die ursprünglichen Arbeitscheckouts bleiben erhalten; nur der Framework-Gitlink des Task-Parents wird wie oben dokumentiert geändert. Weder Parent-master-Integration noch Framework-/MRTS-Quelländerungen werden behauptet. Beide Sprachfassungen enthalten dieselben Werte und Einschränkungen.
