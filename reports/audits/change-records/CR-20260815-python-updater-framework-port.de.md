# Change Record: eingeschränkter Framework-artiger Python-Patch-Updater

**Sprache:** [English](CR-20260815-python-updater-framework-port.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260815-python-updater-framework-port |
| Datum (UTC) | 2026-08-15 |
| Basis-Revision | `55e45726a39bebd3f33aea87807419a882cd3ea8` |
| Framework-Referenz | `Easton97-Jens/ModSecurity-test-Framework@3cb33609626ff689c54b6dc0f31fb7e9401fe75e`, `.github/workflows/check-python-version.yml` |
| Delivery-Status | Der Benutzer hat ausschließlich Feature-Branch-Commit, Push und Draft-PR autorisiert. Weder `master`-Push noch Merge, Ready-for-Review-Übergang oder Auto-Merge sind autorisiert oder werden von diesem Record behauptet. |

## Motivation und Problemstellung

Der Connector-Resolver duplizierte Versionsparsing im Workflow-YAML mit einem
doppelt maskierten Raw-Regular-Expression. Er wies gewöhnliche gültige Releases
wie `3.14.6` und `3.14.7` zurück, bevor Candidate-Outputs geschrieben werden
konnten. Der bisherige Publisher besaß außerdem nicht die vollständigen
Framework-Kontrollen für vertrauenswürdige Events, GitHub-App-Token-Isolation,
Neuaufbau vom aktuellen master, qualifizierten Branch-Lease, vollständige
Draft-PR-Identität und explizite Ergebniszustände.

## Akzeptanzkriterien

- Einen geplanten Updater in `.github/workflows/update-python-version.yml`
  mit ausschließlich `workflow_dispatch` und Cron `17 6 * * 1` beibehalten.
- Vier getrennte Jobs mit read-only Resolver/Validator, einem App-Token-
  Publisher und einem immer laufenden Ergebnis-Job ohne Berechtigungen.
- Die bestehende strikte Updater-Schnittstelle statt einer zweiten YAML-/Shell-
  Versionsgrammatik verwenden; `3.14.6`/`3.14.7` akzeptieren und `3.14.06`,
  `3.14.-1`, `3.15.0` sowie nicht-ASCII-Eingaben zurückweisen.
- Nur `.python-version` über den exakten Wartungs-Branch und einen passenden
  Same-Repository-Draft-PR veröffentlichen, nie direkt nach `master` und nie
  durch Merge oder Auto-Merge.
- Gekoppelte englische/deutsche Dokumentation und Nachvollziehbarkeit erhalten.

## Implementierungsentscheidung und Begründung

Der Port adaptiert die aktuelle Framework-Architektur, ohne Framework oder MRTS
zu ändern. `resolve-python-patch` verwendet den exakten vertrauenswürdigen
Event-SHA und den bestehenden `--check --json`-Output.
`validate-python-patch` installiert den Candidate-Interpreter unabhängig,
validiert die Expected-Version, installiert die vorhandenen hash-gesperrten
Testabhängigkeiten und führt die fokussierten Contracts aus.

`publish-python-update` lässt sein normales `GITHUB_TOKEN` bei `contents: read`.
Nur dieser Job liest `WORKFLOW_UPDATER_APP_CLIENT_ID` und
`WORKFLOW_UPDATER_APP_PRIVATE_KEY` und erstellt dann das vorhandene gepinnte
GitHub-App-Token mit genau `contents: write` und `pull-requests: write`. Er
weist unerwartete Branch-/PR-Kombinationen zurück; prüft Same-Repository-
Head/Base, Titel, Marker, Draft-Status und `auto_merge == null`; baut von
aktuellem `origin/master` neu auf; staged nur `.python-version`; und nutzt die
exakte Form `--force-with-lease=refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_TIP`
nur für einen bereits verifizierten Wartungs-Branch. Der Ergebnis-Job scheitert
fehlgeschlossen bei inkonsistenten übersprungenen, fehlgeschlagenen oder
erfolgreichen Zuständen und schreibt zweisprachigen Summary-Text.

## Security-Auswirkung

Die geänderte Grenze umfasst GitHub-Actions-Event-Trust, App-Credentials,
Repository-Schreibzugriffe, Shell-/Git-Befehle und Pull-Request-Status. Die
Invariante lautet: Nur ein geplanter/manueller kanonischer Nicht-Fork-
`master`-Event kann den App-Token-Publisher erreichen; er kann nur den festen
Wartungs-Branch und einen verifizierten Draft-PR mit ausschließlich
`.python-version` beeinflussen. Er kann keine Workflow-Dateien schreiben,
mergen, Auto-Merge aktivieren oder direkt nach `master` pushen.

Die fokussierte unabhängige Prüfung fand keine validierte Secret-Exposition,
Path-Traversal oder unautorisierte kanonische Schreiboperation. Der erste
GitHub-hosted ZiZmor-Lauf auf dem Draft-PR-Head meldete direkte
Template-Expansion des Publisher-Outputs `changed` in einer Shell-Prüfung. Die
finale Revision übergibt diesen Output über eine Umgebungsvariable, akzeptiert
nur den literalen Wert `true` und besitzt einen Regressionsvertrag; fokussiertes
lokales ZiZmor meldete danach keine Befunde. Die Prüfung bestätigte außerdem
den maskierten Resolverdefekt als bestehendes Availability-Finding
`FND-PARENT-0046` und identifizierte die nun adressierten Admission-, Lease-,
Current-Base- und PR-Status-Kontrollen.

## Geänderte Dateien

- `.github/workflows/update-python-version.yml`
- `ci/checks/common/check-python-version-contract.py`
- `tests/test_update_python_version.py`
- `tests/test_python_version_contract.py`
- `tests/test_ci_security_workflows.py`
- `docs/security/ci-security-tooling.md` und `.de.md`
- `docs/build/README.md` und `.de.md`
- dieses gekoppelte Change-Record-Paar und die gekoppelten Archivindizes.

## Ausgeführte Befehle und Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Updater-/Interpreter-/Versions-/Workflow-Suite | bestanden; 85 Tests |
| `make check-ci-security-contract` | bestanden; 103 Tests, 4 umgebungsbedingt übersprungen; gepinnte Tool-Eingaben validiert |
| Offline-ZiZmor gegen `update-python-version.yml` | nach der Umgebungsvariablen-Remediation bestanden; keine Befunde (sechs Repository-Suppressions) |
| `python -m compileall -q ci scripts tests` mit task-eigenem Pycache-Root | bestanden |
| YAML-Parse des geänderten Updater-Workflows | bestanden |
| `git diff --check` nach finalen Dokumentations-/Indexänderungen | bestanden |
| `ci/checks/common/check-python-version-contract.py --json` | durch vorbestehenden, nicht zusammenhängenden Parent-Inventardrift in aktuellem `master` blockiert; die geänderten Python-Jobs wurden ohne neue lokale Verletzung erkannt |
| `tests.ci_security.test_ci_security_contract` und `tests.security_regression.test_workflow_security_contract` | 16 bestanden, 2 fehlschlugen, weil das bestehende `all-connectors-no-crs.yml` in beiden Parent-Workflow-Allowlisten fehlt; der Updater änderte weder diesen Workflow noch die Allowlisten |
| `make check-bilingual-docs` und `make check-doc-links` | in der frischen Task-Worktree blockiert, weil deren Framework-Submodule-Checkout absichtlich fehlt; alle Fehler betreffen bestehende Framework-Linkziele |

## Runtime-Evidence

Der Draft-PR liefert ein GitHub-hosted Workflow-Lint-Signal; sein erster
ZiZmor-Lauf identifizierte die oben beschriebene direkte Shell-Template-
Expansion. Kein GitHub-hosted Maintenance-Candidate-Lauf, kein App-Token-
Minting, kein Maintenance-Branch-Update, kein Merge und keine Produktions-
Runtime werden hier behauptet.

## Bekannte Einschränkungen

Die lokale Evidence kann weder die Repository-GitHub-App-Konfiguration noch
GitHub-hosted-API-Verhalten über das beobachtete Lint-Ergebnis hinaus oder ein
Live-Candidate-Update nachweisen. Der Task-Worktree lässt außerdem das
Framework-Submodule absichtlich nicht initialisiert, sodass Repository-weite
Framework-Linkziele für Dokumentationsprüfungen nicht verfügbar sind.

## Verbleibende Risiken

GitHub-Hosted-Verhalten benötigt weiterhin einen beobachteten vertrauenswürdigen
geplanten/manuellen Lauf. Die State Machine ist bewusst fehlgeschlossen:
fehlende App-Konfiguration, Candidate-Mismatch, veralteter Branch-Tip,
unerwarteter PR-Status, geänderter Pfad oder PR-Status nach Veröffentlichung
lassen Publisher/Ergebnis scheitern, statt eine Kontrolle zu lockern. Die
nicht zusammenhängenden Basislinien-Inventar-/Allowlist- und nicht initialisierten
Submodule-Dokumentationscheck-Einschränkungen liegen außerhalb dieser
Updater-Änderung.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurde kein GitHub-Hosted-Maintenance-Workflow dispatcht und kein GitHub-
App-Token gemintet: Der Benutzer autorisierte Feature-Branch-Delivery und
einen Draft-PR, nicht aber einen Live-Updater-Run oder eine Merge-bezogene
Aktion. Repository-weite Dokumentationsprüfungen wurden ausgeführt, aber ihre
Framework-eigenen Linkziele sind im absichtlich nicht initialisierten
read-only-Submodule nicht verfügbar. Auch die breiteren Python-Inventar- und
Workflow-Allowlist-Prüfungen wurden ausgeführt; ihre Fehler sind separat
erfasster Current-Base-Drift und keine übersprungenen Updater-Prüfungen.

## Finaler Diff- und Review-Status

Die Implementierung ist auf den angeforderten Updater, seine direkten
Contracts, gekoppelte Dokumentation und Nachvollziehbarkeit begrenzt. Der
Draft-PR bleibt Draft-only; manuelle Prüfung und manueller Merge sind
erforderlich. Finaler Scoped-Diff, exakter Feature-Branch-Head, Remote-Ziel und
Hosted-Checks werden separat beobachtet und festgehalten. Dieser Record
autorisiert weder Merge noch Auto-Merge.
