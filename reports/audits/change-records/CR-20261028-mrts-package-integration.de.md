# Change Record: CR-20261028-mrts-package-integration

**Sprache:** [English](CR-20261028-mrts-package-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-mrts-package-integration |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `c5993ed9a7b59fc0bd58f105595ec79f596c88d6` |

## Motivation und Problemstellung

Der native Aufrufer verwendete Generierungsausgaben ohne geprüftes Paket, änderte gemeinsame FTW-Ports, leitete PASS-Zahlen aus Summen ab und ignorierte Job-Writerfehler. Diese Parent-Änderung übernimmt die eigenständige Framework-MRTS-Paketschnittstelle; sie führt keinen allgemeinen Testumzug durch.

## Akzeptanzkriterien

Jedes Ziel erhält ein geprüftes privates Paket; Vorbereitungsfehler dürfen keine alten Artefakte wiederverwenden, und Writerfehler werden weitergegeben. Explizite strukturierte Ergebnisse trennen ausgewählte/ausgeführte/bestandene/fehlgeschlagene/übersprungene/fehlende Fälle; fehlende Pflichtergebnisse können kein PASS erzeugen. Framework- und MRTS-Gitlinks bleiben unverändert. Gezielte Parent-Verhaltensprüfungen bestehen; native Hostqualifikation wird nicht behauptet.

## Implementierungsentscheidung und Begründung

**Pin-Statushinweis, 2026-10-30:** Parent-Master `ee1345f1` (#433) wählt
Framework `d3b47aec9410f7adc3bb40df1ea413c00c438e89` mit beiden Paket-/
Ergebnis-APIs. Dies ersetzt die fehlende API-/Pin-Voraussetzung dieses
historischen Records, führt dessen Runtime-Evidence aber nicht erneut aus und
qualifiziert sie nicht höher. MRTS bleibt unverändert. Ursprüngliche
aufgabenspezifische Aussagen bleiben unten erhalten.

Die einzige Framework-Schnittstelle `ci/provisioning/mrts-package.py` für `prepare`, `verify` und `materialize` verwenden. Jedes native Ziel nutzt ein eigenes Paket und eine mittels `--output json --file` erzeugte `go-ftw.json`. Framework besitzt `ci/lib/mrts_results.py` und die erneute Berichtsvalidierung. Berichte verwenden den externen `MRTS_NATIVE_REPORT_ROOT`, standardmäßig unter `MRTS_NATIVE_ROOT`. Der aktuelle Parent-Pin enthält diese APIs noch nicht; der PR ist abhängig und bleibt bis Framework-Integration und separat autorisiertem Parent-Pin-Update Draft. Keine Änderung an MRTS-Quellen oder Pin. Die generischen Apache-Einzelfall-, Fallloop- und Fehlerergebnispfade stoppen jetzt bei Writerfehlern; der ausgewählte CRS-Veröffentlichungsvertrag bleibt unverändert. Das Inventar aktualisiert nur die geänderte Apache-Quellbindung, keine Fallauswahl.

## Geänderte Dateien

- `ci/runtime/lifecycle/run-mrts-native-full.sh`
- `tests/test_mrts_native_package_handoff.py`
- `connectors/apache/harness/run_apache_smoke.sh`
- `config/testing/active-cases.json`
- `reports/testing/test-selection-archive.generated.json`
- `docs/testing/mrts-package-integration.md`
- `docs/testing/mrts-package-integration.de.md`
- `reports/audits/change-records/CR-20261028-mrts-package-integration.md`
- `reports/audits/change-records/CR-20261028-mrts-package-integration.de.md`

## Ausgeführte Befehle

Die Befehle liefen im Parent-Task-Worktree `/var/tmp/codex/ModSecurity-conector/worktrees/mrts-connector-20261028`, ausgenommen die explizite Prüfung der Basisdatei. Diese entspricht exakt der Datei aus der Basisrevision.

| Command | Result |
| --- | --- |
| `rtk bypass /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py create --name mrts-package-integration --base-revision c5993ed9a7b59fc0bd58f105595ec79f596c88d6 --date 2026-10-28` | 0 |
| `rtk bypass env ON_DEMAND_TESTS=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/connector TMPDIR=/var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/connector PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_mrts_native_package_handoff` | 0; 4 tests |
| `rtk bypass sh -n ci/runtime/lifecycle/run-mrts-native-full.sh` | 0 |
| `rtk bypass /root/git/ModSecurity-conector/.venv/bin/python ci/tools/update-test-archive.py` | 0 |
| `rtk bypass /root/git/ModSecurity-conector/.venv/bin/python ci/tools/update-test-archive.py --check` | 0 |
| `rtk bypass shellcheck ci/runtime/lifecycle/run-mrts-native-full.sh` | 1; SC1007, SC2034, SC1091, SC2329 |
| `rtk bypass shellcheck /var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/connector/native-baseline.sh` | 1; SC1007, SC2034, SC1091, SC2329 |
| `rtk bypass git diff --check` | 0 |
| `rtk bypass sh -n connectors/apache/harness/run_apache_smoke.sh` | 0 |
| `rtk bypass /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` | 0 |
| `rtk make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` | 0 |
| `rtk make check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/mrts-framework-20261028` | 0 |
| `rtk bypass env RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/connector TMPDIR=/var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/connector /root/git/ModSecurity-conector/.venv/bin/python ci/lib/active_test_inventory.py --check` | 0 |


## Security-Auswirkung

Der Producer kann aus Gesamtsummen oder erfolgreichem Prozessabschluss allein kein Host-PASS erzeugen. Gemeinsame Artefakte bleiben bei Portänderungen eines Ziels unverändert; Paketprüfung und private Materialisierung verbleiben im Framework. Bestehende Pfad-, Schema- und Headervalidierung werden nicht abgeschwächt. Der Berichtsconsumer akzeptiert externe Ausgabe nur innerhalb des nativen Runtime-Roots.

## Runtime-Evidence

Ein separat koordinierter H1-Nachweis bestand auf den finalen Arbeitsquellhashes: lokale Definition mit ausdrücklichem Status → gepinnter MRTS-Generator → ein importierter aktiver Fall `mrts_100000_framework_h1_100000_1` → privates Paket → geladener aktueller Apache-Adapter → beobachtetes HTTP 403 und strukturiertes `phase1_intervention`/Regel `100000`/`deny` → nichtleeres eindeutiges Ergebnis und validierter Bericht. Exakte Befehle/Umgebung und gehashter Nachweis liegen unter `/var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/h1/`. `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/pycache python3 /var/tmp/codex/ModSecurity-conector/mrts-integration-20261028/h1/validate-runtime.py` bestand mit Exit 0 und wiederholte unabhängig strengen Repository-Summary-Validator, Paketprüfung und Apache-Cleanup. `runtime-evidence.json` bindet getestete Arbeitsquellen-, Modul-, Build-Materialisierungs-, Konfigurations-, Definitions-/Artefaktmanifest-, Ergebnis-, Event- und Summary-Hashes.

Der erste H1-Lauf zeigte ignorierte Apache-Writerfehler; finale Quellen geben diese weiter und die fokussierte Negativregression besteht. Die Framework-Ergebnisprojektion erhält importiertes `runtime_verified:false`, daher promoviert Fall-PASS keine generische Variablenunterstützung (`verified_variables:[]`); der Summary-Validator wurde nicht gelockert. Ursprüngliche Upstream-Fälle mit unzureichender Klassifikation bleiben pending. Dies ist ein Schnittstellennachweis, keine Upstream-Korpus-, Full-Native- oder Hosted-Qualifikation des aktuellen Heads. Quellcodehashes statt der späteren Dokumentations-/Commitidentität binden diesen lokalen Nachweis.

## Bekannte Einschränkungen

Native go-ftw, albedo, nginx und apachectl waren bei der lokalen Voraussetzungsprüfung nicht auf PATH verfügbar. Kein vollständiger nativer MRTS-Korpus wurde gestartet. ShellCheck meldet dieselben bestehenden Befunde in aktueller und Basisdatei; ein ShellCheck-Pass wird nicht behauptet. Framework ist eine ungemergte Repository-Abhängigkeit; der Parent-Gitlink bleibt unverändert.

## Verbleibende Risiken

Die abhängige Framework-API muss vor Integration dieses Parent-Aufrufers verfügbar sein. Framework nur separat autorisiert mergen; anschließend separat autorisiertes Parent-Pin-Update auf den exakten SHA unter Erhaltung von MRTS durchführen. Der Testumzug kann ebenfalls nativen Aufrufer oder generiertes On-Demand-Archiv berühren; diese Schnittstellen abgleichen und Archiv neu generieren. Keine Änderung der aktiven Standardfallauswahl.

## Nicht ausgeführte Prüfungen mit Begründung

Keine historische MRTS-Matrix, H2/H3, Coverage-Kampagne, vollständige Abhängigkeitsprüfung, native vollständige Runtime oder Deployment wurde für diesen Parent-Teil beauftragt. Hosted-CI- und Sonar-Ergebnisse auf veröffentlichtem Head sind noch nicht beobachtet. Das begrenzte H1-Ergebnis ist oben dokumentiert; kein vollständiger nativer Korpus- oder Protokollmatrix-Erfolg wird behauptet.

## Finaler Diff- und Review-Status

Parent-Quelldiff und Fehlerpfadtests wurden lokal geprüft. Dieser Worker hat weder Commit, Push, PR, Merge noch Gitlinkänderung ausgeführt. Zweisprachigkeit, Links und Change-Record-Struktur bestanden nach nichtrekursivem Export der exakt gepinnten Framework-Quellen in den Task-Worktree für relative Links. Der Quellexport enthält kein `.git`-Verzeichnis und ändert keinen Gitlink. Finale repositoryübergreifende Integration, Secret-Scan und Lieferevidence verbleiben beim Koordinator.
