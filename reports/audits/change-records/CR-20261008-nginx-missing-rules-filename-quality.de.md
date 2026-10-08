# Change Record: CR-20261008-nginx-missing-rules-filename-quality

**Sprache:** [English](CR-20261008-nginx-missing-rules-filename-quality.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-missing-rules-filename-quality |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `8004340da887d143bc5e850822ac122eb5ce8b59` |

## Motivation und Problemstellung

Historisches Parent-Issue AaEa7bLqEJ_FL6Iil9V7, python:S1192, traf weiterhin drei identische missing-rules.conf-Literale im aktuellen Configtest-Producer. Andere Qualitätsrefaktoren änderten diese Datei nicht. Dieser separate Schritt behebt die verbliebene Source-Duplizierung; Remote-Auflösung benötigt einen Scan der neuen Revision.

## Akzeptanzkriterien

Nur diese drei Producer-Literale durch eine Konstante ersetzen; exakten Konfigurationswert, Diagnosefragmente und fehlendes Fixture-Blatt/Zustand erhalten. Bestehende Config-/Collection-/Wiring-Grenzen unverändert lassen. Keine Validator-, Security-, Selection- oder Runtime-Verhaltensänderung.

## Implementierungsentscheidung und Begründung

MISSING_RULES_FILE_NAME für Vertragswert, Diagnosefragment und CONFIGTEST_PATH_FIXTURES-Tupel einführen. Ein vorhandenes Driver-Testmodul erhält einen begrenzten Charakterisierungstest mit unabhängigen exakten String-Erwartungen. Keine Helper-Extraktion, Unterdrückung oder breitere Refaktorierung.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-configtest.py; tests/test_nginx_configtest_driver.py; dieses EN/DE-Paar. Separates externes source-quality-reconciliation.md wurde vor Implementierung gespeichert; Qualitäts-CSV bleibt unverändert.

## Ausgeführte Befehle

Alle Befehle RTK-wrapped mit Parent-eigenem Python und externem TMPDIR. Neuer Test-first-Test test_missing_rules_constant_preserves_all_closed_contract_values lief mit1 Test und exit1, weil MISSING_RULES_FILE_NAME fehlte. `rtk proxy env TMPDIR=<external-task-runs> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PARENT_TEST_FRAMEWORK_ROOT=<explicit-framework-root> python -m unittest tests.test_nginx_configtest_driver tests.test_nginx_configtest_collection tests.test_nginx_selected_configtest_wiring -q` bestand51 Tests, exit0, ohne Skips. `rtk proxy python ci/tools/new-change-record.py check` endete mit exit0 (nur Struktur). Whitespace-Prüfung endete mit exit0. AST-Charakterisierung verlangt zusätzlich genau ein Producer-Literal.

## Security-Auswirkung

Nur semantikgleiche Benennung des Dateinamens. Exakte Diagnosen, Fixture-Abwesenheit/Pfad-Autorität, Artefakt-Containment, Exit-Behandlung und Akzeptanzprüfungen bleiben unverändert.

## Runtime-Evidence

Nur kontrollierte Subprocess-/Unit-Tests; keine echte NGINX-Invocation, kanonischer PASS oder All-Required-Abschlussbehauptung.

## Bekannte Einschränkungen

Gespeicherte Sonar-Readbacks markieren das historische Issue weiterhin OPEN. Source-Korrektur ist kein Remote-RESOLVED-Nachweis.

## Verbleibende Risiken

Koordinator muss den separaten normalen Commit integrieren und den passenden frischen Scan ausführen. Keine Framework-/MRTS-/Gitlink-Änderung gehört zu diesem Schritt.

## Nicht ausgeführte Prüfungen mit Begründung

Native Build/Runtime, vollständiges E2E, Push und Remote-Sonar-Analyse liegen außerhalb begrenzter Autorität. Keine Tool- oder Dependency-Installation.

## Finaler Diff- und Review-Status

Vier eigene Dateien in frischem isoliertem Parent-Worktree auf exakt genannter Revision; unveränderte Literalwerte geprüft. Finale fokussierte Ergebnisse und normaler Commit werden separat übergeben.
