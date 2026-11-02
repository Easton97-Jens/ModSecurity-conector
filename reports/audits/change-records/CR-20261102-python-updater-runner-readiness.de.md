# Change Record: CR-20261102-python-updater-runner-readiness

**Sprache:** [English](CR-20261102-python-updater-runner-readiness.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261102-python-updater-runner-readiness |
| Datum (UTC) | 2026-11-02 |
| Basis-Revision | `2cfe7819655f905fb41c63b1f03c3e3d812d59bc` |

## Motivation und Problemstellung

Eine Python-Version kann veröffentlicht sein, bevor ihr exaktes GitHub-Runner-Archiv existiert. Bisher gab der Resolver dabei Candidate-Outputs aus; der Fehler trat erst beim Candidate-Setup auf.

## Akzeptanzkriterien

Fehlende exakte Runner-Archive für `ubuntu-26.04`/`x64` vor jeglichen Resolver-Job-Outputs ablehnen; bei einem exakten offiziellen stabilen Archiv die vier bisherigen Outputs erhalten.

## Implementierungsentscheidung und Begründung

`runpy.run_path` mit dem festen gepinnten Framework-Pfad `ci/tools/python_runner_builds.py` verwenden und nach der Metadatenprüfung `require_build(fetch_manifest(), latest)` aufrufen. Vertrauenswürdiger Event-Checkout, Framework-Kontextbindung, CLI-/JSON-Schnittstelle und nachgelagerte Validierung bleiben erhalten. Es wird kein Candidate-Code importiert. Die Build-Dokumentation korrigiert außerdem ihre veraltete Behauptung, dass dieser Checkout Submodules auslässt.

## Geänderte Dateien

- `.github/workflows/update-python-version.yml`
- `docs/build/README.md`, `docs/build/README.de.md`
- `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`
- `reports/audits/change-records/CR-20261102-python-updater-runner-readiness.md`, `reports/audits/change-records/CR-20261102-python-updater-runner-readiness.de.md`

## Ausgeführte Befehle

- `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/runs/component-updater-fix-20261102/parent/verify_resolver.py .`
- `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/component-updater-fix-20261102/parent /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_manifest_rejects_wrong_platform_arch_or_release_identity tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_manifest_fetch_rejects_redirect_and_oversized_payload tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_manifest_transport_failure_is_a_blocked_metadata_input tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_previous_ubuntu_build_cannot_satisfy_new_target`
- `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/parent-python-updater-20261102/modules/ModSecurity-test-Framework check-bilingual-docs check-doc-links`
- `rtk bypass git diff --check`

Die Offline-Regression mit extrahiertem Resolver schlug vor dem Fix fehl, weil der Fall mit fehlendem Archiv alle vier Outputs ausgab; danach bestanden sowohl fehlendes Archiv/keine Outputs als auch die Kontrolle mit exaktem Archiv. Die vier vorhandenen gepinnten Helper-Tests bestanden (acht expandierte Negativfälle). Dokumentations- und Whitespace-Ergebnisse stehen im finalen Review unten. Die Helper-Tests liefen im gepinnten Framework-Verzeichnis; andere Befehle im Parent-Worktree. Für die Change-Record-Erzeugung war expliziter Kontext nötig; erste Versuche mit unvollständigem Kontext scheiterten ohne Dateierstellung, danach erstellte der dokumentierte Generator beide Vorlagen erfolgreich.

## Security-Auswirkung

Fehlgeschlossenes Verhalten bei fehlenden oder ungültigen offiziellen Runner-Metadaten ohne Credentials oder Redirects. Nur der vertrauenswürdige gepinnte Helper wird ausgeführt; keine Änderung an Abhängigkeiten, Berechtigungen, Gitlink oder Candidate-Code-Ausführung.

## Runtime-Evidence

Kein gehosteter Actions- oder Connector-Runtime-Lauf. Evidence besteht aus offline extrahiertem Workflow-Verhalten und fokussierten Helper-Tests an Framework `f11d4617ff98ad615c72c1b6672fc386394db41e`.

## Bekannte Einschränkungen

Die Prüfung belegt Manifest-Identität und Verfügbarkeit, keinen Download und keine Installation des Candidate-Archivs. Lokal lief Python 3.14; es wird keine Python-3.15-Kompatibilität behauptet.

## Verbleibende Risiken

Das öffentliche Manifest und die Archiv-Verfügbarkeit können sich zwischen Auflösung und Setup ändern. Bestehendes Candidate-Setup und unabhängige Validierung bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Standardsuite, kein CI-Dispatch, Archiv-Download, Candidate-Installation, SonarQube-Scan oder Runtime-Matrix: Die Änderung ist eine enge Workflow-Prüfung; Lieferung und gehostete Checks werden separat koordiniert.

## Finaler Diff- und Review-Status

Lokale Implementierung im isolierten Branch `codex/python-updater-readiness-20261102` vorbereitet. Dieser Record behauptet keinen Commit, Push, PR, Merge oder gehostete Bereitschaft. Finaler Review: `make check-bilingual-docs check-doc-links` mit gepinntem Kontext bestand einschließlich Repository-Pfadrefernzen; `git diff --check` bestand. Beide Sprachpaare und der enge Workflow-Diff wurden manuell geprüft.
