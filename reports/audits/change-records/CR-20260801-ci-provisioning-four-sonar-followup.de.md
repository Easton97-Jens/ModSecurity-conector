# Change Record: Parent-CI-Provisioning-SonarQube-Cloud-Folgekorrektur mit vier Befunden

**Sprache:** [English](CR-20260801-ci-provisioning-four-sonar-followup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-ci-provisioning-four-sonar-followup` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `e1a656798efb89e77e0526ffc7698cbd02b104b1` |
| Tracking | `FND-SONAR-0030`; `AZ9cRyj3HhV2CayPTPzC`, `AZ9cRyj3HhV2CayPTPzB`, `AZ9cRyj3HhV2CayPTPys` und `AZ9cRyj3HhV2CayPTPy2` |
| Grenze | Nur Parent `ci/provisioning` und ein direkter Parent-Cache-Contract-Test; Framework, MRTS, Gitlinks, `.github`, SonarQube-Cloud-Einstellungen, Abhängigkeiten und `master` bleiben unverändert. |

## Motivation und Problemstellung

Das aktuelle Inventar hat drei `python:S3776`-Zeilen in `BuildLock.__enter__()`, `prepare_apache_httpd()` und `prepare_nginx_runtime()` sowie eine `python:S1066`-Zeile in `remove_incomplete_connector_cache_entry()`. Alle vier sind Maintainability-Befunde in `ci/provisioning/components/prepare-runtime-components.py`; die Komponente hat keinen offenen Security-Befund und meldet `0.0%` Duplikation.

## Akzeptanzkriterien

- Jede der vier Zeilen hat eine verhaltenserhaltende Source-Korrektur ohne `NOSONAR`, Suppression, Exclusion, Regel-, Quality-Gate- oder Threshold-Änderung.
- Lock-Timeout, Owner-Marker und Release-Verhalten bleiben unverändert.
- Ungemanagte unvollständige Cache-Einträge bleiben fail-closed; marker-eigene Einträge bleiben nur unter dem Managed-Root löschbar.
- Apache-/NGINX-Keyed-Pläne behalten transaktionales Staging, und NGINX baut nur, wenn beide Artefaktansichten nicht bereit sind.
- Fokussierte Controls bestehen; Exact-Head-GitHub-Actions und SonarQube-Cloud-Analyse bleiben für `verified_pr` erforderlich.

## Implementierungsentscheidung und Begründung

`BuildLock.__enter__()` delegiert File-Locking und Directory-Fallback-Warten an private Methoden und behält den bestehenden `fcntl`-dann-`ImportError`-Fallback-Contract. Die Stale-Cache-Bedingung ist ein äquivalenter einzelner fail-closed Guard. Apache und NGINX teilen ein privates Prädikat für transaktionale Pläne, und NGINX verwendet einen privaten Helper für die bestehende Build-Bedingung „beide Artefakte nicht bereit“.

## Security-Auswirkung

Der Source verarbeitet Cache-Pfade, Managed-Root-Löschung, heruntergeladene Build-Inputs und subprocess-nahe Daten. Die Invariante bleibt unverändert: Nur durch Managed-Root- und Ownership-Controls autorisierte Einträge können gelöscht werden, und bestehende Provenance-, Digest-, Containment-, Staging- und fail-closed-Controls bleiben erhalten. Der direkte Regressionstest erhält einen ungemanagten Partial-Entry bei verweigerter Migration und entfernt einen legitimen eigenen Eintrag. Es wird kein Security-Befund behauptet.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- Dieses englische/deutsche Change-Record-Paar.

## Tests und tatsächliche Ergebnisse

| Befehl | Ergebnis |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -P -m py_compile ci/provisioning/components/prepare-runtime-components.py` | bestanden |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_prepare_runtime_components tests.test_runtime_component_cache_contract tests.test_runtime_component_cache_identity tests.test_runtime_env_snapshot_contract tests.test_runtime_artifact_utils tests.test_runtime_path_policy` | bestanden: 94 fokussierte Tests |
| `PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=modules/ModSecurity-test-Framework make check-runtime-path-policy` | bestanden |
| `PYTHON=/root/git/ModSecurity-conector/.venv/bin/python make check-bilingual-docs` | bestanden |
| `PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=modules/ModSecurity-test-Framework make check-doc-links` | bestanden |
| `git diff --check` | bestanden |

Der erste breite Lauf endete bei sechs Framework-Fixture-Fällen, weil der neue Worktree kein initialisiertes Submodul hatte. Der isolierte Worktree initialisierte dann nur seine Parent-gepinnte Test-Fixture `6400ee882afa0527e5c0763fa6efb850ffa403f2`; der Wiederholungslauf bestand und änderte weder Framework-Source noch Gitlink.

## Ausgeführte Befehle

Die Befehle und beobachteten Ergebnisse in der vorstehenden Tabelle sind der vollständige lokale Ausführungsnachweis zum Zeitpunkt der Autorenschaft. Der ausgewählte Interpreter ist `/root/git/ModSecurity-conector/.venv/bin/python` (Python `3.14.4`) mit `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1` und `PYTHONDONTWRITEBYTECODE=1`; Build- und Bytecode-Output verwenden den task-eigenen externen Root.

## Runtime-Evidence

Die fokussierte Suite übt Lock-, Cache-Marker-, Staging-, Apache-, NGINX-, HAProxy-, Snapshot-, Artefakt- und Path-Policy-Contracts aus. Sie führt keinen Third-Party-Download oder nativen Connector-Build aus. Framework- und MRTS-Source bleiben außerhalb des Scopes.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein echter Runtime-Component-Provision/Build wurde nicht ausgeführt, weil er Third-Party-Komponenten herunterlädt und kompiliert; das ist breiter als diese strukturelle Korrektur.
- Ruff und Pyright wurden nicht ausgeführt, weil die ausgewählte Parent-virtuelle Umgebung kein `ruff`- oder `pyright`-Modul besitzt. Es wurde kein Paket und kein Dependency-Contract geändert.
- Exact-Head-GitHub-Actions und SonarQube-Cloud-Analyse sind noch nicht ausgeführt, weil bei der Record-Autorenschaft kein Commit, Push oder Pull Request existiert.

## Bekannte Einschränkungen

Lokale Tests können die Hosted-Disposition historischer SonarQube-Cloud-Zeilen nicht beweisen. Finaler scoped Diff-Review, Dokumentations-Checks, Commit, Draft-PR, exakter SHA-Vergleich und current-head Hosted-Checks bleiben erforderlich.

## Verbleibende Risiken

Der weitere repositoryweite SonarQube-Cloud-Backlog ist außerhalb des Scopes. Kein Ergebnis hier autorisiert eine `master`-Integration.

## Finaler Diff- und Review-Status

Dieser Pre-Delivery-Record berichtet nur beobachtete lokale Ergebnisse. Er behauptet keinen Commit, Pull Request, Hosted-Check, Quality Gate, Approval, Merge oder Release.
