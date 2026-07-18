# Change Record: GitHub-Workflow-Berechtigungen härten

**Sprache:** [English](CR-20260718-harden-workflow-permissions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-harden-workflow-permissions` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Grenze | Nur Parent-Workflow-Konfiguration, statische Contracts, Fixtures und Nachvollziehbarkeit; Framework, MRTS, Connector-Source, Secrets und Gitlinks unverändert. |

## Motivation und Problemstellung

GitHub Code Scanning meldete fünf offene Scorecard-`TokenPermissionsID`-
Alerts für Schreibrechte auf Workflow-Ebene. Der zeitgesteuerte
Submodule-Updater aktualisierte außerdem ein rekursives Remote-Submodule,
führte `make quick-check` aus und nutzte später in demselben Job `GH_TOKEN`
zum Publishing. Das ist eine plausible Vertrauensgrenzen-Sorge, obwohl keine
direkte Token-Exfiltration nachgewiesen wurde.

Die externe Einstellung `default_workflow_permissions: write` wird weiter
durch `FND-GITHUB-0001` verfolgt. Das Ändern dieser Einstellung liegt außerhalb
dieses Parent-Pull-Requests; deshalb deklariert jeder aktuelle Workflow jetzt
einen expliziten restriktiven Default.

## Akzeptanzkriterien

- Jeder Parent-Workflow hat Top-Level `permissions: contents: read`.
- Zusätzliche Berechtigungen sind auf Jobs begrenzt und beschränken sich auf
  dokumentiertes Cleanup, vertrauenswürdiges Publishing oder SARIF-Uploads.
- Rekursive Ausführung ist von Write-Token-Publishing getrennt; jeder Checkout
  deaktiviert persistierte Credentials.
- CodeQL, OSV und Scorecard behalten enge `security-events: write`-Uploads.
- Statische Contracts und sichere/unsichere Fixtures decken Berechtigungs-,
  PR-Trigger-, Credential-, Submodule-, Cleanup- und SARIF-Grenzen ab.

## Implementierungsentscheidung und Begründung

- `cleanup-artifacts.yml` gibt `actions: write` nur einem checkout-freien Job.
- `test-full-smoke-sequential.yml` führt Artefakt-Cleanup in einem unabhängigen
  checkout-freien `actions: write`-Matrix-Job aus. Der schwere rekursive-
  Submodule-Job hat nur `contents: read` und läuft nach dem Cleanup.
- `update-actions-versions.yml` verwendet standardmäßig `contents: read` und
  begrenzt seine bestehenden `contents`-, `pull-requests`- und `actions`-
  Schreibrechte auf seinen vertrauenswürdigen zeitgesteuerten/manuellen
  Maintenance-Job. Seine Secret-Nutzung bleibt unverändert.
- `update-submodules.yml` löst und validiert den offiziellen Remote-SHA in
  `contents: read`-Jobs auf. Ein separater Publisher validiert den SHA erneut,
  checkt kein Submodule aus, staged nur den Gitlink mit `git update-index` und
  hat `contents: write` plus `pull-requests: write` nur beim Publishing.
- Ein Standardbibliotheks-Contract-Test und gepaarte Fixtures erzwingen die
  Grenze. `actionlint` parst die Fixtures mit ShellCheck-Integration; zizmor
  muss die sichere Fixture akzeptieren und die unsichere Fixture ablehnen.

## Security-Auswirkung

Der update-submodules-Publisher teilt keinen Job und keinen Workspace mehr mit
Remote-Submodule-Ausführung. Er akzeptiert einen Job-Output erst nach
Formatvalidierung und einem exakten `git ls-remote`-Vergleich mit dem
offiziellen Branch. Ein fehlgeschlagenes schreibgeschütztes `make quick-check`
verhindert nun das PR-Publishing. Es werden keine `pull_request_target`,
benannten Secrets, persistenten Credentials, Release-/Deployment-
Berechtigungen, `id-token`, `attestations`, `checks`, `issues` oder `packages`
Schreibrechte ergänzt.

## Geänderte Dateien

- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/cleanup-artifacts.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `.github/workflows/update-actions-versions.yml`
- `.github/workflows/update-submodules.yml`
- `ci/fixtures/workflow-permission-contract/safe.yml`
- `ci/fixtures/workflow-permission-contract/unsafe.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260718-harden-workflow-permissions.md`
- `reports/audits/change-records/CR-20260718-harden-workflow-permissions.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis im aktuellen lokalen Change-Set |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_ci_security_workflows` | bestanden: 13 fokussierte Tests. |
| `make check-ci-security-contract` | bestanden: 13 Tests und drei Checksum-Lock-Validierungen. |
| Checksum-verifiziertes `actionlint -shellcheck=/usr/bin/shellcheck` über Workflows und Fixtures | bestanden. |
| Checksum-verifiziertes `zizmor --offline .github/workflows` | bestanden: keine Findings; 70 konfigurierte Suppressions gemeldet. |
| Bestehende und neue sichere/unsichere zizmor-Fixtures | bestanden: sichere Fixtures akzeptiert; unsichere Fixtures mit Exit-Code `14` abgelehnt. |
| Checksum-verifiziertes `gitleaks git --staged --redact=100 --no-banner` | bestanden: keine Leaks in den 12 gestageten Task-Dateien. |
| `make check-bilingual-docs` | blockiert: Dem Worktree fehlen bestehende Framework-Dokumentationslink-Ziele; der Checker meldet diese vorbestehenden fehlenden Ziele vor Abschluss. |
| `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile tests/test_ci_security_workflows.py` | blockiert: `py_compile` versucht `tests/__pycache__` anzulegen, das in diesem Worktree read-only ist. Die Bytecode-deaktivierte Unit-Suite bestand. |
| `git diff --check` | bestanden im aktuellen lokalen Change-Set. |

## Runtime-Evidence

Nicht anwendbar. Diese Änderung verändert nur GitHub-Actions-Konfiguration und
statische Contracts; sie etabliert keine Connector-, Protokoll-, CRS-,
Framework-, MRTS- oder Host-Runtime-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

OSV, Scorecard, CodeQL/SARIF-Upload, GitHub Secret Scanning und Fork-Runtime-
Verhalten benötigen den exakten Head-SHA des fokussierten Pull Requests.
`make check-doc-links` läuft nicht, weil es Framework-Validierung außerhalb
des Parent-only-Scopes aufruft. Kein Connector-Build, keine Runtime-,
Protokoll-, Sanitizer-, CRS-, Framework- oder MRTS-Prüfung ist für diese
Workflow-only-Änderung anwendbar.

## Bekannte Einschränkungen

Der externe Actions-Default bleibt `write`; explizite Workflow-Defaults decken
die aktuellen Workflows ab, können aber keinen künftigen Workflow schützen,
der ihn auslässt. Das Ändern der Einstellung benötigt separate
Administrator-Autorisierung. Der vertrauenswürdige Maintenance-Job
`update-actions-versions.yml` benötigt weiterhin sein bestehendes
`SUBMODULE_UPDATE_TOKEN` für Module-Publishing; diese Änderung verändert oder
exponiert es nicht.

## Verbleibende Risiken

Statische Contracts können weder GitHubs Runtime-Fork-Token-Policy noch das
Verhalten eines künftigen Remote-Submodule-Commits beweisen. Der Publisher
validiert den ausgewählten Commit erneut und führt ihn nicht aus; verbleibendes
Runner-/Action-Risiko benötigt exakte PR-Checks und fortlaufende Reviews. Es
gibt keine Risikoakzeptanz.

## Finaler Diff- und Review-Status

Die lokale Implementierung, der finale gestagete Diff-Review und redigiertes
gestagetes Gitleaks sind vollständig. Der Bilingual-Checker ist durch
vorbestehende fehlende Framework-Ziele in diesem Worktree blockiert. Erstellung
des fokussierten PRs und exakte-Head-GitHub-Validierung stehen aus und
aktualisieren diesen Record, falls sie die finale Disposition ändern.
