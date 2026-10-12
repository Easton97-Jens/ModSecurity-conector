# Change Record: CR-20261012-pr-411-workflow-tool-regressions

**Sprache:** [English](CR-20261012-pr-411-workflow-tool-regressions.md) | Deutsch

Parent-only-Reparatur der belegten Workflow-Tool-Regressionen in PR #411.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261012-pr-411-workflow-tool-regressions |
| Datum (UTC) | 2026-10-12 |
| Basis-Revision | `159624d7976f881862cfa1d20f27543090a1727d` |

## Motivation und Problemstellung

PR #411 aktualisierte unveränderliche Action-Pins und zizmor. Sein ursprünglicher Head scheiterte in Security workflow lint (Run `38253812611`) und gehostetem NGINX (Run `38253812702`). CodeQL-Fixtures hingen von der aktuellen Lockdatei ab; zizmor ergänzte eine Self-Repository-Prüfung; der isolierte NGINX-Schritt verlor den vorbereiteten Runtime-Snapshot und startete die Vorbereitung erneut.

## Akzeptanzkriterien

Beobachtete Fehler beheben, Prüfsummen-/Berechtigungs-/Isolationskontrollen erhalten, legitimes und negatives Verhalten prüfen, Prüfungen vor künftiger Tool-Veröffentlichung ausführen und einen normalen Folge-Commit in PR #411 pushen, ohne Merge.

## Implementierungsentscheidung und Begründung

Explizite synthetische Release-Basisstände verwenden und Checkout-Fixtures von aktuellen Pin-Änderungen isolieren. Die vollständige nichtrekursive Updater-Unit-Klasse im nativen Vertrag ausführen; echte Integration des kopierten Baums getrennt halten. Prüfsummenvalidiertes vorgeschlagenes actionlint/zizmor samt positiven und negativen Fixtures vor der Veröffentlichung ausführen. GitHub-`$/`-Referenzen verwenden und ausschließlich sichere YAML-`uses`-Skalarpositionen im Speicher für actionlint 1.7.12 normalisieren; zizmor liest Originale. Exakten NGINX-Producer-Snapshot über `env -i` erhalten und Ziel-/Cache-Prüfungen beibehalten.

## Geänderte Dateien

- `.github/workflows/all-connectors-no-crs.yml`
- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/test-nginx-exact-head.yml`
- `.github/workflows/test-nginx.yml`
- `Makefile`
- `ci/tools/lint_workflows.py`
- `ci/tools/update-workflow-tools.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_lint_workflows.py`
- `tests/test_nginx_exact_head_gate_contract.py`
- `tests/test_nginx_exact_head_runtime_handoff.py`
- `docs/security/ci-security-tooling.md`
- `docs/security/ci-security-tooling.de.md`
- Dieser Change Record und sein englischer Begleiter.

## Ausgeführte Befehle

Alle lokalen Befehle verwendeten RTK. Aus dem externen Parent-Worktree:

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr-411-repair make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`: 274 Tests bestanden, 6 wegen fehlender Namespace-/Ownership-Capabilities übersprungen; Prüfung gepinnter Tool-Einträge bestanden.
- Updater-Unit-Klasse: 45 Tests bestanden; ursprüngliche Suite reproduzierte 3 Failures und 1 Error. Die Prüfung des kopierten Baums deckte außerdem Fixture-Abhängigkeiten und fehlende kopierte NGINX-Eingaben auf; beides wurde korrigiert.
- `tests.ci_security.test_update_workflow_tools.WorkflowToolUpdaterIntegrationTests`: finale Integration des kopierten Baums bestanden (1 Test, 138.941 Sekunden), einschließlich echtem nativem Vertrag unter einem synthetischen künftigen Checkout-Pin.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 RUNNER_TEMP=/var/tmp/codex/ModSecurity-conector/runs/pr-411-repair TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr-411-repair /root/git/ModSecurity-conector/.venv/bin/python ci/tools/update-workflow-tools.py validate --root . --candidate /var/tmp/codex/ModSecurity-conector/runs/pr-411-repair/current-lock-candidate.json --validate-proposed-tree`: echter Vertrag des privaten Baums und Lint-/Fixture-Prüfungen mit heruntergeladenen Tools bestanden, ohne den Checkout zu ändern.
- `tests.test_lint_workflows`: 4 Tests bestanden, einschließlich Erhalt von Block-Skalaren, Pfadzurückweisung und weitergereichten Fehlern.
- `tests.test_nginx_exact_head_gate_contract`, `tests.test_nginx_exact_head_runtime_handoff` und `tests.test_runtime_env_snapshot_contract`: 31 Tests mit sauberem Framework am exakten Gitlink bestanden.
- Gepinntes actionlint über `ci/tools/lint_workflows.py`: alle Workflows und Berechtigungs-Fixtures bestanden. Gepinntes zizmor offline: ursprünglicher Baum reproduzierte Exit `12`; korrigierter Baum bestand. Beide unsicheren Fixtures lieferten `14`; beide sicheren Fixtures lieferten `0`.
- `make check-bilingual-docs` und `make check-doc-links`, RTK-gewrappt mit expliziten Parent-Python-/Framework-Pfaden: nach lokaler Materialisierung des Frameworks am exakten Gitlink bestanden. Anfängliche Linkfehler wegen fehlendem Submodul waren Umgebungsfehler, keine Fehler geänderter Dokumente.
- `rtk proxy git diff --check`: bestanden. Unabhängige Read-only-Prüfung fand zunächst einen Fehler der Regex-/Skript-Normalisierung; Token-Korrektur und Regression bestanden.

## Security-Auswirkung

SHA-Pins, offizielle Upstream-Identitäten, Prüfsummenprüfung, Berechtigungs-Allowlists und Isolation unvertrauenswürdiger PRs bleiben durchgesetzt. Candidate-Lint weist Prüfsummen-, Start-, Timeout-, Finding- und unerwartete negative Fixture-Exits zurück. Keine Suppression oder Severity-Schwelle wurde ergänzt. Skripte/Kommentare bleiben bei actionlint-Normalisierung erhalten; zizmor prüft Originalquellen. Keine Secrets, Abhängigkeiten, globalen Services oder Framework-/MRTS-Quellen wurden geändert.

## Runtime-Evidence

Die ausführbare Übergabe-Regression reproduzierte vor dem Fix eine unerwartete zweite Vorbereitung (Exit `93`) und bestand danach. Sie führt die tatsächliche Workflow-Shell und den Cache-Wrapper aus und ersetzt nur die aufwendige Build-Grenze. Sie prüft vorbereitete Pfade, entfernte Umgebungswerte, fehlgeschlagene Provisionierung und zurückgewiesene Ziel-/Cache-Metadaten. Dies belegt die Übergabe; echte gehostete NGINX-Ausführung gehört zur CI nach dem Push.

## Bekannte Einschränkungen

Der vorhandene lokale Parent-Interpreter ist Python `3.14.4`; CI pinnt `3.14.7`. Lokale Prüfungen belegen Kompatibilität innerhalb derselben Minor-Version, keine Ausführung auf dem exakten CI-Patch. Actionlint benötigt den dokumentierten Syntax-Adapter, bis Upstream `$/` unterstützt.

## Verbleibende Risiken

Künftige Tool-Releases können neue Regeln oder Fehler einführen; das Proposed-Tree-Lint weist solche Kandidaten vor der Veröffentlichung zurück, statt aus gültigen Prüfsummen auf Kompatibilität zu schließen. Echter Host-Runtime- und exakter CI-Toolchain-Erfolg erfordern die Workflows am aktuellen PR-Head.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiges gehostetes NGINX und GitHub-/SonarQube-Prüfungen des aktuellen Heads liefen nicht lokal; GitHub führt sie nach dem autorisierten Push aus. Keine unbeteiligten Connector-Neubauten, breiten Security-Scans, Paketinstallationen oder Merge wurden ausgeführt. Ruff fehlt in der bestehenden Umgebung und wurde nicht installiert.

## Finaler Diff- und Review-Status

Begrenzte Quellen, Tests, EN/DE-Anleitung und dieses Paar geprüft. Ursprünglicher Parent-master und verschachtelte Repositorys erhalten. Delivery-Ziel ist der bestehende PR-#411-Branch `automation/update-modsecurity-conector-workflow-tools`; Push und CI-Readback des aktuellen Heads folgen der lokalen Prüfung. Kein Merge und keine master-Aktualisierung autorisiert.

Folgekorrektur: Reparatur-Commit `f805bab6b1634a087be437ea994f21e87510669c` wurde normal in PR #411 gepusht. Seine actionlint-, zizmor- und NGINX-Strukturprüfungen bestanden. SonarQube-Check `114923255883` meldete vom Bediener vorgegebene CLI-Pfade/Executables des Helpers sowie eine Maintainability-Frage im Exception-Test. Native Aufrufer lieferten bereits geprüfte Pfade und prüfsummenvalidierte Binärdateien; ein entfernter Exploit wurde nicht belegt. Der Helper akzeptiert nun keine beliebigen Pfad-/Tool-Argumente, leitet feste Staging-Pfade ab, prüft Pfad-/Dateiidentität und verwendet festes Host-ShellCheck. Regressionstests prüfen zurückgewiesene CLI-Eingaben, Symlinks, beschreibbare Tools, Candidate-Containment und YAML-Endungen. Der Exception-Test erzeugt seine Release-Fixture vor `assertRaises`. CI des aktuellen Heads wird nach dem Folge-Push neu geprüft; kein Gate und kein Finding-Status wurde abgeschwächt.

Prüfung der Folgekorrektur: 8 Helper-Tests und 2 ausführbare Proposed-Lint-Tests bestanden (10 Tests, 17.120 Sekunden). Derselbe native Befehl `validate --validate-proposed-tree` bestand erneut mit echten vorgeschlagenen Tools und vollständigem Vertrag. Normales actionlint im festen Modus, zizmor auf Originalquellen, zweisprachige Dokumentation/Dokumentlinks und Whitespace-Prüfungen bestanden. Die unabhängige Read-only-Prüfung fand kein verbleibendes validiertes Problem.
