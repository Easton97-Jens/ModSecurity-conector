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

`.github/workflows/ci-security-codeql.yml`, `.github/workflows/ci-security-secrets.yml`, `.github/workflows/ci-security-workflow-lint.yml`, `.github/workflows/lint.yml`, `.github/workflows/protocol-contract.yml`, `.github/workflows/sonar-native-security.yml`, `.github/workflows/sonarqube.yml`, `.github/workflows/update-go-version.yml`, `.github/workflows/update-python-version.yml`, `.github/workflows/update-submodules.yml`, `.github/workflows/update-workflow-tools.yml`, `.github/workflows/validate-go-candidate.yml`, `.github/workflows/verified-report-governance.yml`, `ci/tools/sync-framework-component-versions.py`, `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.md`, `reports/audits/change-records/CR-20261102-updater-bootstrap-contracts.de.md`.

## Ausgeführte Befehle

RTK-gekapselte gezielte Python-Proben mit der bestehenden virtuellen Parent-Umgebung: PASS für acht Verifier-Schritte und acht Negativkontrollen ohne Flag. Die YAML-Projektionsschnittstelle scheitert bei deaktivierten Site-Abhängigkeiten mit `ModuleNotFoundError: No module named 'yaml'` und liest mit verfügbarer bestehender Abhängigkeit 17981 Bytes. Der native Change-Record-Generator lief mit explizitem Connector-/Framework-Kontext. Erste Generator-Aufrufe ohne Paket-/Kontextpfade scheiterten vor der Dateierstellung.

Zusammengesetzte statische Validierung mit der separat bearbeiteten Framework-Quelle erkannte 53 Python-Jobs ohne Verletzung. Eine Negativkontrolle mit Scaffold-Kontext vor dem Setup wurde abgelehnt; die tatsächlich ergänzte Shell-Prüfung akzeptierte passende und verwarf abweichende initialisierte Framework-Identitäten. Der unverändert gepinnte Framework-Checker meldet weiterhin 45 Verletzungen bei Composite-Reihenfolge, geschütztem Mapping und geschlossenen Job-Inventaren; dies ist eine separate Framework-Delivery-/Pin-Voraussetzung. Bei Immutable-Action-Jobs prüft die Provenienzprüfung committed Gitlink und initialisierten Checkout vor ausgechecktem Python gegen den ausgewählten unveränderlichen Action-SHA. Das geschlossene Synchronisiererregister verantwortet jetzt alle sechs frühen Prüfungs-Pins neben Action-/Input-Pins. No-op- und Pinwechsel-Rücksetzungsprüfungen bestehen für alle 22 registrierten Workflow-Projektionen; veraltete, fehlende, zusätzliche und symbolische Prüfungs-Pins werden abgewiesen. Die tatsächliche Shell-Prüfung verwirft selbst einen passend geänderten Gitlink/Checkout, wenn er vom ausgewählten unveränderlichen Action-SHA abweicht. Alle 27 nativen Kontext-Jobs erhalten Workflow-/Job-Rechte und erzwingen Provenienzprüfung vor Verifier und Kontext nach Verifier; alle Prüfungsskripte bestanden `bash -n`. Kein geänderter Gitlink oder gehostetes Ergebnis wird behauptet.

## Security-Auswirkung

Die Vorbereitung führt gepinnten Installer-Code aus und liest den gepinnten Framework-Lock vor dem Kandidaten-Checkout. Kandidatenrechte, Sandbox, Hashprüfungen, Abhängigkeits-Allowlisten und Publisher-Berechtigungen bleiben unverändert. `-P` entfernt den impliziten Importpfad des Skriptverzeichnisses.

## Runtime-Evidence

Kein gehosteter Workflow oder Connector-Runtime-Lauf ausgeführt. Lokale Evidence belegt nur Verifier-Form und YAML-Importvoraussetzung.

## Bekannte Einschränkungen

Framework-weite geschlossene Workflow-Inventare und Bootstrap-Reihenfolge bleiben separate Voraussetzungen. Diese Änderung belegt keinen erfolgreichen vollständigen Python-Updater.

## Verbleibende Risiken

Ein autorisierter gehosteter Wiederholungslauf ist weiterhin für das vollständige Updater-Verhalten erforderlich; spätere unabhängige Vertragsfehler können bestehen bleiben.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Paketinstallation, vollständige Suite, gehostete CI, Publisher-, Sonar- oder Runtime-Ausführung: außerhalb dieser gezielten lokalen Korrektur. Kein Commit, Push, PR, Gitlink- oder MRTS-Eingriff durch diesen Worker.

## Finaler Diff- und Review-Status

Gezielten Diff geprüft; `git diff --check` bestanden. `rtk make check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/parent-updater-contracts-20261102/modules/ModSecurity-test-Framework` bestanden, einschließlich Repository-Pfadreferenzen. Delivery bleibt beim koordinierenden Agenten.
