# Change Record: Finale Cognitive-Complexity-Remediation für Parent-CI-Provisioning

**Sprache:** [English](CR-20260801-ci-provisioning-two-cognitive-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-ci-provisioning-two-cognitive-remediation` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `6dc912643133e5c7d3c305979d4052da9cb45153` |
| Tracking | `FND-SONAR-0030`; `AZ9cRyj3HhV2CayPTPzB`; `AZ9cRyj3HhV2CayPTPzC` |
| Grenze | Parent `ci/provisioning` und ein direkter Parent-Cache-Contract-Test; Framework, MRTS, Gitlinks, `.github`, SonarQube-Cloud-Einstellungen, Abhängigkeiten und `master` bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Analyse von `master` enthält zwei verbleibende
`python:S3776`-Maintainability-Zeilen in
`ci/provisioning/components/prepare-runtime-components.py`:
`prepare_apache_httpd()` und `prepare_nginx_runtime()` haben jeweils kognitive
Komplexität 16, obwohl 15 erlaubt ist. Das angefragte Verzeichnis hat null
Security-, null Reliability- und null Duplikatzeilen-Befunde.

## Akzeptanzkriterien

- Die beiden exakten Zeilen erhalten eine verhaltenserhaltende Source-
  Remediation ohne `NOSONAR`, Suppression, Exclusion, Regel-, Quality-Gate-
  oder Threshold-Änderung.
- Keyed Apache- und NGINX-Pläne verwenden weiter validiertes transaktionales
  Staging; unkeyed Pläne bleiben direkt.
- Bestehende Cache-, Provenance-, Containment-, Command-Construction-,
  Publication-, Record- und Failure-Semantik bleibt unverändert.
- Fokussierte Tests und anwendbare lokale Checks bestehen; Exact-Head-GitHub-
  Actions und SonarQube-Cloud-Analyse bleiben für `verified_pr` erforderlich.

## Implementierungsentscheidung und Begründung

`prepare_connector_with_optional_staging()` besitzt nun die bereits gemeinsame
Entscheidung: Ein keyed nichttransaktionaler Plan nimmt den bestehenden
`prepare_connector_transactionally()`-Pfad, während ein unkeyed oder bereits
gestagter Plan seinen Prepare-Callback direkt aufruft. Die öffentlichen Apache-
und NGINX-Einstiegspunkte delegieren an private Per-Plan-Implementierungen,
deren bisheriger Body und Kontrollfluss-Reihenfolge erhalten bleiben. Zwei
direkte Tests beweisen direkte/unkeyed und transaktionale/keyed Delegation;
bestehende Apache- und NGINX-Cache-Contract-Tests üben weiterhin tatsächliches
Staging und Publication aus.

## Security-Auswirkung

Der Source ist sicherheitsrelevant, weil er Cache-Pfade, Downloads, Provenance,
Publication und subprocess-nahe Daten verarbeitet. Die bewahrte Invariante
lautet: Keyed Connector-Pläne bleiben im bestehenden validierten Managed-Root-
Staging-/Publication-Control, während unkeyed Pläne direkt bleiben. Der
fokussierte Source-/Control-Review fand keine plausible diff-induzierte
Security-Regression und keinen reportierbaren Security-Befund. Er ist kein
vollständiger Repository-Security-Scan und kein Runtime-Build-Ergebnis.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- Dieses englische/deutsche Change-Record-Paar.

## Tests und tatsächliche Ergebnisse

| Befehl | Ergebnis |
| --- | --- |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/provisioning/components/prepare-runtime-components.py tests/test_runtime_component_cache_contract.py` | bestanden |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_runtime_component_cache_contract` | bestanden: 34 Tests |
| `git diff --check` | vor der finalen Dokumentationsvalidierung bestanden; finale eingegrenzte Wiederholung bleibt vor Delivery erforderlich |

Der ausgewählte Interpreter ist `/root/git/ModSecurity-conector/.venv/bin/python`
(Python `3.14.4`) mit `PYTHONNOUSERSITE=1`,
`PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1` und
`PYTHONDONTWRITEBYTECODE=1`. Test-Temporary-State liegt in task-eigenem
externem Storage.

## Ausgeführte Befehle

Die Befehle und Ergebnisse in der vorstehenden Tabelle bilden den vollständigen
lokalen Ausführungsnachweis zum Zeitpunkt der Autorenschaft. Auch
`make check-no-crs-source-normalization` und `make check-bilingual-docs`
wurden ausgeführt; ihre exakten blockierten beziehungsweise Remediation-
Zustände stehen unter **Nicht ausgeführte Prüfungen mit Begründung** und im
Task-Plan. Kein Build-, Dependency-Installation-, Commit-, Push-, PR- oder
Merge-Befehl lief bei der Record-Autorenschaft.

## Runtime-Evidence

Die bestehende Suite übt Apache-Keyed-Staging, NGINX-Rebuilds bei einem
marker-eigenen Partial-Root, Sichtbarkeit atomarer Publication, Ablehnung von
Managed-Root-Löschung, Digest-vor-Publication und die neuen direkten/unkeyed
sowie keyed/staged Delegation-Controls aus. Kein Third-Party-Download und kein
nativer Connector-Build lief.

## Nicht ausgeführte Prüfungen mit Begründung

- `make check-no-crs-source-normalization` wurde versucht, aber während der
  Collection blockiert: Der isolierte Parent-Worktree enthält absichtlich nicht
  die Framework-Submodule-Datei
  `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`.
  Framework zu initialisieren oder zu ändern liegt außerhalb dieses Parent-only
  Tasks.
- `make check-bilingual-docs` und `make check-doc-links` erreichten beide den
  neuen Change Record erfolgreich, werden jedoch von denselben absichtlich
  fehlenden Framework-Targets blockiert, auf die bereits vorhandene Repository-
  Dokumente verweisen. Kein task-eigener Dokumentationslink schlug fehl.
- `make check-runtime-path-policy` wurde mit dem ausgewählten Parent-
  Interpreter versucht und ist blockiert, weil sein Shell-Control dasselbe
  fehlende `modules/ModSecurity-test-Framework/ci/lib/common.sh` importiert;
  es übte keinen geänderten Runtime-Path-Control aus.
- Ein echter Runtime-Component-Provision/Build lief nicht, weil er Third-Party-
  Komponenten herunterlädt und kompiliert; das geht über diese strukturelle
  Remediation hinaus.
- Ruff und Pyright liefen nicht, weil die ausgewählte Parent-virtuelle Umgebung
  keines der beiden Tools enthält; kein Paket- oder Dependency-Contract änderte
  sich.
- Exact-Head-GitHub-Actions und SonarQube-Cloud-Analyse liefen noch nicht, weil
  bei der Record-Autorenschaft kein Commit, Push oder Pull Request existiert.

## Bekannte Einschränkungen

Lokale Checks können die Hosted-Disposition der zwei historischen SonarQube-
Cloud-Zeilen nicht beweisen. Die Exact-Head-PR-Analyse muss ihre Schließung,
null neue Issues und null New-Code-Duplikation zeigen, bevor der Draft-PR
`verified_pr` erreichen kann.

## Verbleibende Risiken

Der weitere repositoryweite SonarQube-Cloud-Backlog ist außerhalb des Scopes.
Diese Änderung autorisiert keine `master`-Integration.

## Finaler Diff- und Review-Status

Dieser Pre-Delivery-Record berichtet nur beobachtete lokale Ergebnisse. Er
behauptet keinen Commit, Pull Request, Hosted-Check, Quality Gate, Approval,
Merge oder Release.
