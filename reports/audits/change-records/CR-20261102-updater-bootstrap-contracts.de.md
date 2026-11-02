# Change Record: CR-20261102-updater-bootstrap-contracts

**Sprache:** [English](CR-20261102-updater-bootstrap-contracts.md) | Deutsch

Begrenzte Korrektur des Updater-Bootstraps.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261102-updater-bootstrap-contracts |
| Datum (UTC) | 2026-11-02 |
| Basis-Revision | `430d3194fa04ca4aafcdaef6aeb256d21dc18f0c` |

## Motivation und Problemstellung

Lauf `41412832386` erreichte eine YAML-abhängige Kandidatenprüfung vor der PyYAML-Vorbereitung. Lauf `41412784227` zeigte Verifier-Befehle ohne das erforderliche `-P`.

## Akzeptanzkriterien

Die bestehende hashgebundene Abhängigkeit vorbereiten, solange Framework noch dem Parent-Gitlink entspricht; Kandidatenisolation erhalten. Interpreter-Verifier-Befehle der Updater an den gepinnten Framework-Vertrag anpassen und alle betroffenen nativen Bootstrap-Jobs als Shell-Provenienzprüfung, Python-Setup, stdlib-Interpreter-Verifier, Kontextbindung und anschließend weitere Python-Verbraucher anordnen.

## Implementierungsentscheidung und Begründung

Den unveränderten Block zur Abhängigkeitsvorbereitung vor Kandidaten-Checkout und YAML-abhängigen Vertrag verschieben. Die Python-, Go- und Submodul-Verifier mit `-P` aufrufen; Versions- und Interpreterpfad-Argumente erhalten. 27 Kontextbindungen in 13 nativen Workflows neu ordnen, kanonisches Setup/Verifier im Submodul-Resolver ergänzen und vor Ausführung des ausgecheckten Verifiers den initialisierten Framework-HEAD gegen den committed Gitlink authentifizieren. Die Kompatibilitätsausnahme des Go-Resolvers auf Trusted-Base unverändert erhalten.

## Geänderte Dateien

`.github/workflows/ci-findings-regressions.yml`, `.github/workflows/ci-security-codeql.yml`, `.github/workflows/ci-security-secrets.yml`, `.github/workflows/ci-security-workflow-lint.yml`, `.github/workflows/lint.yml`, `.github/workflows/nginx-root-broker.yml`, `.github/workflows/open-connectors-smoke.yml`, `.github/workflows/protocol-contract.yml`, `.github/workflows/quick-framework-check.yml`, `.github/workflows/reusable-five-connectors-profile.yml`, `.github/workflows/run-protected-nginx-exact-head.yml`, `.github/workflows/run-protected-nginx-root-broker.yml`, `.github/workflows/run-trusted-lighttpd-namespace-dispatch.yml`, `.github/workflows/sonar-native-security.yml`, `.github/workflows/sonarqube.yml`, `.github/workflows/test-apache.yml`, `.github/workflows/test-common.yml`, `.github/workflows/test-connectors-with-crs-no-mrts.yml`, `.github/workflows/test-envoy.yml`, `.github/workflows/test-full-smoke-sequential.yml`, `.github/workflows/test-haproxy.yml`, `.github/workflows/test-lighttpd.yml`, `.github/workflows/test-nginx-exact-head.yml`, `.github/workflows/test-nginx.yml`, `.github/workflows/test-traefik.yml`, `.github/workflows/update-go-version.yml`, `.github/workflows/update-python-version.yml`, `.github/workflows/update-submodules.yml`, `.github/workflows/update-workflow-tools.yml`, `.github/workflows/validate-go-candidate.yml`, `.github/workflows/verified-report-governance.yml`, `ci/tooling/project-versions.lock.json`, `ci/tools/sync-framework-component-versions.py`, `docs/security/ci-security-tooling.de.md`, `docs/security/ci-security-tooling.md`, `modules/ModSecurity-test-Framework`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.de.md`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.md`.

## Ausgeführte Befehle

RTK-gekapselte gezielte Python-Proben mit der bestehenden virtuellen Parent-Umgebung: PASS für acht Verifier-Schritte und acht Negativkontrollen ohne Flag. Die YAML-Projektionsschnittstelle scheitert bei deaktivierten Site-Abhängigkeiten mit `ModuleNotFoundError: No module named 'yaml'` und liest mit verfügbarer bestehender Abhängigkeit 17981 Bytes. Der native Change-Record-Generator lief mit explizitem Connector-/Framework-Kontext. Erste Generator-Aufrufe ohne Paket-/Kontextpfade scheiterten vor der Dateierstellung.

Zusammengesetzte statische Validierung mit der separat bearbeiteten Framework-Quelle erkannte 53 Python-Jobs ohne Verletzung. Eine Negativkontrolle mit Scaffold-Kontext vor dem Setup wurde abgelehnt; die tatsächlich ergänzte Shell-Prüfung akzeptierte passende und verwarf abweichende initialisierte Framework-Identitäten. Der anfänglich unveränderte Framework-Pin meldete 45 Verletzungen bei Composite-Reihenfolge, geschütztem Mapping und geschlossenen Job-Inventaren. Nach ausdrücklicher Nutzerautorisierung integrierte der Koordinator die gemeinsame Framework-Revision `a26b028104b28ddd980290b5af7b3fb195c43f9a` einschließlich Python 3.15 und Framework-Vertragskorrekturen; der native Python-Vertrag besteht jetzt für 53 Jobs. Bei Immutable-Action-Jobs prüft die Provenienzprüfung committed Gitlink und initialisierten Checkout vor ausgechecktem Python gegen den ausgewählten unveränderlichen Action-SHA. Das geschlossene Synchronisiererregister verantwortet jetzt alle sechs frühen Prüfungs-Pins neben Action-/Input-Pins. No-op- und Pinwechsel-Rücksetzungsprüfungen bestehen für alle 22 registrierten Workflow-Projektionen; veraltete, fehlende, zusätzliche und symbolische Prüfungs-Pins werden abgewiesen. Die tatsächliche Shell-Prüfung verwirft selbst einen passend geänderten Gitlink/Checkout, wenn er vom ausgewählten unveränderlichen Action-SHA abweicht. Alle 27 nativen Kontext-Jobs erhalten Workflow-/Job-Rechte und erzwingen Provenienzprüfung vor Verifier und Kontext nach Verifier; alle Prüfungsskripte bestanden `bash -n`. Der Parent-Arbeitsbaum enthält jetzt den autorisierten gemeinsamen Framework-Gitlink und 23 generierte Ansichten (Projekt-Lock plus 22 Workflows). Kein gehostetes Ergebnis wird behauptet.

Der Koordinator führte `rtk bypass env PYTHONNOUSERSITE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/framework-python315-20261102/parent /root/git/ModSecurity-conector/.venv/bin/python ci/tools/sync-framework-component-versions.py --sync --framework-common /var/tmp/codex/ModSecurity-conector/runs/framework-python315-20261102/parent/framework-common-a26b028.sh --framework-sha a26b028104b28ddd980290b5af7b3fb195c43f9a` aus; der Austausch von `--sync` gegen `--check` bestand ohne weitere Änderungen. Eingabe ist der exakte Git-Blob `a26b028104b28ddd980290b5af7b3fb195c43f9a:ci/lib/common.sh`. Natives `make check-python-version-contract` mit explizitem `FRAMEWORK_ROOT` des Task-Kind-Checkouts und `/var/tmp/codex/ModSecurity-conector/runs/framework-python315-20261102/venv/bin/python` bestand für 53 Jobs. `verify-framework-candidate-contract.py` mit vollständigem explizitem Kontext und virtueller Parent-Umgebung bestand für dieselbe Revision und NGINX `release-1.31.6`.

## Security-Auswirkung

Die Vorbereitung führt gepinnten Installer-Code aus und liest den gepinnten Framework-Lock vor dem Kandidaten-Checkout. Kandidatenrechte, Sandbox, Hashprüfungen, Abhängigkeits-Allowlisten und Publisher-Berechtigungen bleiben unverändert. `-P` entfernt den impliziten Importpfad des Skriptverzeichnisses.

## Runtime-Evidence

Kein gehosteter Workflow oder Connector-Runtime-Lauf ausgeführt. Lokale Evidence belegt den gemeinsamen Python-Workflow-Vertrag, den exakten Framework-Kandidatenvertrag und die YAML-Importvoraussetzung; sie belegt kein gehostetes Updater- oder Connector-Runtime-Verhalten.

## Bekannte Einschränkungen

Die gemeinsam geprüfte Revision `a26b028104b28ddd980290b5af7b3fb195c43f9a` ist der geprüfte Integrations-Pin dieses Records. Eine nachfolgende Framework-Änderung erfordert erneute Synchronisierung und native Prüfungen. Diese Änderung belegt keinen erfolgreichen vollständigen gehosteten Python-Updater.

## Verbleibende Risiken

Ein autorisierter gehosteter Wiederholungslauf ist weiterhin für das vollständige Updater-Verhalten erforderlich; spätere unabhängige Vertragsfehler können bestehen bleiben.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Paketinstallation, vollständige Suite, gehostete CI, Publisher-, Sonar- oder Runtime-Ausführung: außerhalb dieser gezielten lokalen Korrektur. Der Koordinator committete native Parent-Korrekturen als `df858e0b04d851b392accc95f70118489c2d02f2`; die gemeinsame Framework-Revision `a26b028104b28ddd980290b5af7b3fb195c43f9a` liegt auf Framework-PR #158. Parent-Pin-Delivery und gehosteter Erfolg werden noch nicht behauptet. Keine MRTS-Quelländerung oder Änderung des Kind-Gitlinks `tools/MRTS`; er und der Parent-MRTS-Lock bleiben bei `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Finaler Diff- und Review-Status

Gezielten Diff geprüft; `git diff --check` bestanden. `rtk make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/parent-updater-contracts-20261102/modules/ModSecurity-test-Framework` bestanden, einschließlich Repository-Pfadreferenzen. Delivery bleibt beim koordinierenden Agenten.

Koordinator-Nachweis: Der gemeinsame Framework-Stand ist auf `a26b028104b28ddd980290b5af7b3fb195c43f9a` aktualisiert; erneute native Synchronisation und No-op-Prüfung bestanden. 78 fokussierte Parent-Projektions-/Python-/Installationsprüfungen bestanden zuvor auf echtem Python 3.15.2 beim gemeinsamen Zwischenstand; dessen Product-Bootstrap bleibt unverändert. Die Paketquellen-Korrektur betrifft Framework-Sonar-CI. Neue gehostete Parent-Prüfungen bleiben erforderlich.

Der erste gehostete Parent-Folgelauf auf `73984fd57c9b2c4030a72e41aa489c66196a5b6e` bestand Source-Gate und Python-3.15.1-Interpreterprüfung, scheiterte danach jedoch korrekt an veralteten Framework-Quelldigests im aktiven Inventar. Der neue gemeinsame Framework-Pin erneuert über den vorhandenen Generator genau zehn Digestwerte; sämtliche anderen Inventarfelder und alle 100 automatischen Standardfälle bleiben unverändert. Die native Inventarzulassung besteht lokal. Neue gehostete Prüfungen des aktualisierten Parent-Commits bleiben erforderlich. MRTS wurde lokal nicht initialisiert; die vollständige Materialisierungsprüfung muss die CI erbringen.

Die Folgeprüfung auf Parent `5aafe1be10f4893dc73c24d33f37988f0f697f30` erreichte das nachgelagerte deklarative Spezialistenarchiv. Dessen veraltete Generatoransicht wurde im Framework nativ erneuert; das vollständige `make check-active-inventory` bestand danach mit Inventar und Archiv unter Python 3.15.2. Der aktualisierte Gitlink und alle verwalteten Action-Referenzen beziehen gemeinsam diesen Archiv-Folgecommit. Automatischer Testumfang und Prüfregeln bleiben erhalten.

Der finale gemeinsame Framework-Pin verhindert auch die Wiederholung beim nächsten normalen Python-/Komponentenupdate: Inventar und Spezialistenarchiv werden nativ in der richtigen Reihenfolge erneuert; geschlossene Publisher-Pfade, Prüfung basisabgeleiteter Git-Blobs vor dem Checkout und transaktionaler Common-Rollback bleiben erhalten. 105 fokussierte Framework-Tests und eine echte synthetische Offline-Pinprojektion bestanden. Der Parent erhält keine zusätzliche Schreib- oder Merge-Autorität.

Der frühere Framework-Helper zur Kandidatenprüfung verwendet feste, eingecheckte Referenzen. Beim vorherigen Integrationsstand bestanden 107 fokussierte Tests auf echtem Python 3.15 sowie native Inventar-/Archiv-, kanonische, Dokumentations- und Security-Lint-Prüfungen.

Frische Parent-Prüfung bei `a26b028104b28ddd980290b5af7b3fb195c43f9a`: Natives Synchronisierer-`--check` lieferte `changed: []`; nativer Python-Vertrag bestand für 53 Jobs auf echtem Python 3.15; exakter Kandidatenvertrag bestand mit NGINX `release-1.31.6`. Actionlint `v1.7.12` mit `/usr/bin/shellcheck` akzeptierte alle 22 geänderten Workflows mit nativem Self-Reference-Normalisierer im Speicher. Zweisprachige Dokumentation, Repository-Referenzen und Links bestanden mit explizitem Task-Kind-`FRAMEWORK_ROOT` und Python 3.15. Der Framework-Checkout ist sauber und `tools/MRTS` bleibt unverändert.

Der aktuelle gemeinsame Stand erhält Upstream-PR #155 für Maintenance-Imports/Fehlerdiagnostik und PR #159 für Tooling-Korrekturen und aktualisiert den Framework-eigenen Ruff-Lock auf `0.17.3`. Die Canonical-Maintenance-Pfadpolicy enthält die registrierte Projektion `.github/workflows/ci-findings-regressions.yml`. Der Koordinator meldet 124 fokussierte Python-3.15-Tests, das CRS-Modul mit 10 Fällen, 43 Shared-Tooling-Tests und 33 Fetcher-Tests als bestanden; das Replay des unveränderten archivierten 43-Update-Plans validiert die Pfadkorrektur ohne Veröffentlichung von Komponentenupdates. Native Inventar-/Archivaufnahme bestand mit 8,034 On-demand-Definitionen ohne Änderung der automatischen Auswahl. Parent-Python bleibt `3.15.1`, NGINX `release-1.31.6` und MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; die unabhängig aktualisierte Upstream-MRTS-Revision wird nicht ausgewählt. Der vorherige Parent-Head `28680dd8a054afe6d2cde5c6ba972cd33cf2d47e` schloss 59 Prüfungen erfolgreich ab, fünf wurden erwartungsgemäß übersprungen; dieser Nachweis qualifiziert weder diesen neuen Pin noch einen nachfolgenden Parent-Head. Dieser Vorbereitungsschritt führt keinen Commit/Push aus.

Die finale OSV-Folgekorrektur ergänzt ausschließlich das exakt geprüfte Event-Basis-Kompatibilitätstupel `ff7cae78e085e179950c4b871bbf1d5327c69069` mit Python `3.14.10` und erhält die drei früheren exakten Tupel. Der Koordinator meldet 28 gezielte OSV-/Katalog-/Generatortests als bestanden in 7.096 s sowie Security-, kanonische, Dokumentations- und vollständige native Inventar-/Archivprüfungen. Python-3.15-/Ruff-0.17.3-Bootstrap-Quellen, Parent-Baseline, MRTS und 8,034 On-demand-Definitionen bleiben durch diese Folgekorrektur unverändert.
