# Change Record: CR-20260930-pr399-component-pin-test-fixtures

**Sprache:** [English](CR-20260930-pr399-component-pin-test-fixtures.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-pr399-component-pin-test-fixtures |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `58345e70eee3753ae67964f6878c8193df8d353e` |

## Motivation und Problemstellung

PR #399 aktualisierte HAProxy auf 3.2.25 und ModSecurity auf v3.0.17. Die Synchronizer-Tests kopierten diese aktuellen Pins, verwendeten jedoch einen historischen Offline-Kandidaten mit 3.2.23/v3.0.16. Der actionlint-Job in Run 36768743096 scheiterte an drei Assertions; alle drei wurden vor dieser Änderung lokal reproduziert.

## Akzeptanzkriterien

Die drei ursprünglichen Regressionen und das Synchronizer-Modul mit 24 Tests bestehen lassen; exakte Dateilisten, Byte-Vergleiche, historische Grammar-Fixture und Produktions-Pins erhalten. Aktuelle gehostete CI-Evidence für den aktualisierten PR-Head ermitteln.

## Implementierungsentscheidung und Begründung

Ausschließlich die temporären Repository-Kopien mit expliziten unabhängigen Komponenten-Pin-Fixtures initialisieren. Die zehn bestehenden generischen Zieldateien abdecken, alle Zuweisungs-/JSON-Slots vor Schreibzugriffen prüfen und den Source-Checkout ablehnen. Produktions-Registry, Parser und Synchronizer nicht zum Erstellen ihrer eigenen Testeingaben verwenden.

## Geänderte Dateien

- `tests/framework_component_fixture.py`
- `tests/test_update_framework_versions.py`
- `reports/audits/change-records/CR-20260930-pr399-component-pin-test-fixtures.md`
- `reports/audits/change-records/CR-20260930-pr399-component-pin-test-fixtures.de.md`

## Ausgeführte Befehle

```sh
python3 -m unittest -v tests.test_update_framework_versions
python3 -m unittest -v tests.test_ci_security_workflows tests.test_validate_submodule_candidate_state tests.test_update_submodules_local_git tests.test_update_framework_versions tests.test_verify_framework_candidate_contract
make check-ci-security-contract
python3 ci/tools/fetch_security_tool.py --tool actionlint --validate-only
python3 ci/tools/fetch_security_tool.py --tool zizmor --validate-only
python3 ci/tools/fetch_security_tool.py --tool gitleaks --validate-only
python3 ci/tools/new-change-record.py check
python3 ci/checks/documentation/check-bilingual-docs.py
git diff --check
```

Lokales Python 3.12.14 und PyYAML 6.0.3: Das Modul mit 24 Tests bestand; die Vertragssuite aus fünf Modulen bestand (109 Tests, einer übersprungen); alle drei Tool-Lock-Prüfungen bestanden. Der vollständige Befehl mit 170 Tests lieferte zwei fehlgeschlagene Tests und 18 Fehler in den unveränderten Sandbox-/Namespace-Suites, weil dieser Ausführungsumgebung `/proc`-Funktionen fehlen (fünf übersprungen). Eine gezielte Fixture-Prüfung bestätigte Source-Checkout-Ablehnung, Byte-Idempotenz und Validierung vor Schreibzugriffen. Die Testbefehle verwendeten `PYTHONNOUSERSITE=1`, `PYTHONDONTWRITEBYTECODE=1` sowie externe Task-Verzeichnisse für `RUNNER_TEMP`/`TMPDIR`. Die aufgeführten Prüfungen der bilingualen Dokumentation, Change-Record-Struktur und des gestagten Diffs bestanden vor der Auslieferung.

## Security-Auswirkung

Nur Testvorbereitung; Produktionsvalidierung, Workflow-Berechtigungen, Dependency-Pins und Sicherheitsassertions bleiben unverändert. Unabhängige literale Fixtures erhalten die Prüfung des produktiven Synchronisierungsverhaltens.

## Runtime-Evidence

Keine Connector-Runtime-Aussage. Diese Änderung betrifft ausschließlich die Vorbereitung von Offline-Vertragstests.

## Bekannte Einschränkungen

Das lokale Python unterscheidet sich vom CI-Pin 3.14.7 des Repositorys. Fehlendes `/proc` verhindert vollständige lokale Sandbox-/Namespace-Evidence; die gehostete CI muss diese Evidence liefern.

## Verbleibende Risiken

Künftige Änderungen am registrierten Zielschema müssen die expliziten Test-Fixture-Zuordnungen aktualisieren. Die Release-Werte der Fixture bleiben bewusst historisch.

## Nicht ausgeführte Prüfungen mit Begründung

Connector-Builds, Runtime-Matrizen und lokale actionlint-/zizmor-Scans wurden nicht wiederholt: Produktions-/Workflow-Dateien bleiben unverändert. Die gehostete CI führt die konfigurierten Checks erneut aus. Kernel-Sandbox-Prüfungen konnten in dieser lokalen Umgebung nicht bestehen.

## Finaler Diff- und Review-Status

Die abgegrenzten Teständerungen wurden unabhängig und nur lesend ohne blockierende Befunde geprüft. Dieser Record beschreibt lokale Evidence vor der Auslieferung; er behauptet kein gehostetes Ergebnis, keinen Merge und keine master-Änderung.
