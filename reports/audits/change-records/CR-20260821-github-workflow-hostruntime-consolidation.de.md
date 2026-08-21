# Change Record: GitHub-Workflow-Host-Runtime-Konsolidierung

**Sprache:** [English](CR-20260821-github-workflow-hostruntime-consolidation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260821-github-workflow-hostruntime-consolidation |
| Datum (UTC) | 2026-08-21 |
| Basis-Revision | `aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf` |
| Delivery-Status | Ein Parent-only-Task-Branch, ein task-eigener Commit und ein Pull Request nach `master` sind autorisiert. Commit, Push, PR-Erstellung, Hosted-Checks und Merge-Evidence stehen bei Erstellung dieses Records noch aus; ein Merge ist nicht autorisiert. |

## Motivation und Problemstellung

Vier Connector-Workflows duplizierten denselben Host-Runtime-Preflight-Aufruf,
die bereinigte Evidence-Projektion und die Summary-Erzeugung. Dadurch wurden
Security-Controls schwerer konsistent wartbar. Zusätzlich scheiterte `Update
pinned workflow tools` auf `master` reproduzierbar, weil dessen begrenzter
Candidate-Tree statische transitive Eingaben des bestehenden CI-Security-
Contracts ausließ.

## Akzeptanzkriterien

- Alle 29 Repository-Workflow-Dateien, Workflow-Namen, Trigger, Jobs,
  Berechtigungen, Action-SHAs, Connector-Profile, Artefakte und unabhängigen
  Security-Scanner bleiben erhalten.
- Nur die vier äquivalenten Evidence-Collection-Implementierungen werden
  zentralisiert.
- Fail-closed-Evidence-Semantik bleibt erhalten und Shell-/Pfad-Injection wird
  verhindert.
- Die begrenzte Candidate-Tree-Validierung des Updaters wird repariert, ohne
  seine Source-Allowlist zu erweitern oder den Contract zu umgehen.
- Fokussierte Tests, YAML/actionlint/ShellCheck/zizmor-Validierung, ein
  Security-Diff-Review, gekoppelte englisch-deutsche Traceability und nach
  finalem Delivery-Preflight ein nicht gemergter PR werden bereitgestellt.

## Implementierungsentscheidung und Begründung

- `ci/runtime/common/collect_hostruntime_preflight_evidence.py` wurde ergänzt;
  Envoy, HAProxy, NGINX und Traefik rufen es nur mit ihren ursprünglichen
  Connector-/Profil-/Konfigurations-/Fixture-Werten auf. NGINX behält die
  Markdown-Code-Formatierung; alle vier Workflows behalten exakte
  Artefaktpfade und `if: always()`-Uploads.
- Der Collector validiert einfache Komponenten und Repository-relative Pfade,
  ruft den bestehenden Preflight über einen Argumentvektor auf und publiziert
  ausschließlich begrenzte Allowlist-Felder. Fehlerhafter Status, `PASS` mit
  Nonzero-Exit, fehlende Lock-Daten und Binary-Fehler werden `BLOCKED`; der
  Runtime-Status bleibt `NOT_RUN`.
- Die Proposed-Tree-Baseline des Updaters enthält jetzt nur die während der
  Fehlerreproduktion gefundenen exakten statischen Eingaben. Ein Regressionstest
  führt den echten kopierten CI-Security-Contract aus. Pin-Assertions beziehen
  unveränderliche SHAs aus dem reviewed Lock und normalisieren vor dem Digest
  nur diese Pin-/Kommentar-Fragmente; Action-Identität und aller anderer
  Publisher-Inhalt bleiben abgedeckt.

## Security-Auswirkung

Die Änderung berührt GitHub-Actions-Ausführung, CI-Evidence und Updater-
Provenance. Sie bewahrt unveränderliche Action-Pins, Least-Privilege-
Berechtigungen, read-only Checkout-Credentials, Artefakt-Contracts und
restriktive Updater-Allowlists. Der gemeinsame Collector ergänzt weder
Shell-Ausführung noch externe Downloads; seine Ausgabe ist fail-closed und
payload-sicher. Ein späterer fokussierter Review reproduzierte die unten
aufgezeichnete Same-User-Artefakt-Symlink-Grenzverletzung; der Successor behebt
sie vor der Auslieferung.

Der anfängliche Diff-Review meldete diese Grenzverletzung nicht. Ein späterer
fokussierter Review reproduzierte einen Same-User-`RUNNER_TEMP`-Symlink-
Overwrite im Fallback-Pfad des Collectors. Der Successor validiert den privaten
Artefakt-Root und verwendet für jeden Collector-Output die bestehenden
descriptor-basierten atomaren No-Follow-Reader/Writer; zwei Regressionen
weisen vorab angelegte Root- und finale Status-Symlinks ab, ohne deren
Sentinel-Target zu verändern.

## Geänderte Dateien

- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-haproxy.yml`
- `.github/workflows/test-nginx.yml`
- `.github/workflows/test-traefik.yml`
- `ci/runtime/common/collect_hostruntime_preflight_evidence.py`
- `ci/tools/update-workflow-tools.py`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_collect_hostruntime_preflight_evidence.py`
- `tests/test_hostruntime_workflow_evidence_contract.py`
- dieses gekoppelte Change-Record-Paar und die gekoppelten Archivindizes

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Collector- und Workflow-Evidence-Contracts | bestanden: 6 Tests |
| `tests.test_ci_security_workflows` | bestanden: 28 Tests |
| `tests.ci_security.test_update_workflow_tools` | bestanden: 35 Tests einschließlich echter Copied-Tree-Validierung |
| `make check-ci-security-contract` | bestanden: 122 Tests; 5 fähigkeitsabhängige Skips; Validierung gepinnter actionlint/zizmor/gitleaks-Tools bestanden |
| APR-Provenance-/Static-Contracts | Exit 0: 7 statische Passes; 15 Skips, weil der externe Framework-Checkout-HEAD vom Parent-Gitlink abweicht |
| Alle Workflow-YAML parsen | bestanden: 29 Dateien |
| actionlint mit ShellCheck | bestanden |
| Offline-zizmor mit strict collection | bestanden: keine unsupprimierten Findings; 94 bestehende Suppressions berücksichtigt |
| Direkte sichere Collector-Ausführung | bestanden: bereinigte `BLOCKED`/`NOT_RUN`-Evidence bei fehlenden lokalen Runtime-Voraussetzungen erzeugt |
| `git diff --check` vor Traceability | bestanden |
| Vollständiges `make lint` | blockiert/scheitert in der Framework-abhängigen No-CRS-Gruppe, weil der Task-Worktree einen leeren Framework-Gitlink besitzt und dessen Katalog fehlt; 27 vorherige Host-Runtime-Tests bestanden |
| `make check-bilingual-docs` | nur durch vorbestehende fehlende Framework-Gitlink-Targets blockiert; kein neuer Change-Record-Fehler bleibt |
| `make check-doc-links` | nur durch dieselben fehlenden Framework-Gitlink-Targets blockiert, bevor Framework-Dokumentationslinks geprüft werden können |

| Collector-Symlink-Grenze und Runtime-Artefakt-Contracts | bestanden: 44 Tests; Root- und finale Status-Symlink-Targets blieben unverändert |

## Runtime-Evidence

Der reproduzierbare Fehler von `Update pinned workflow tools` wurde in seinem
Candidate-only-Tree erneut ausgelöst; dort fehlten erforderliche Contract-
Eingaben. Nach der Closure-Reparatur besteht derselbe echte Copied-Tree-
Contract, ohne den Source-Checkout zu verändern. Der Host-Runtime-Helper wurde
nur unter sicheren lokalen Bedingungen fehlender Runtime ausgeführt und
behauptet kein Connector-Runtime-Ergebnis.

Der vollständige Security-Diff-Report liegt außerhalb des Source-Trees unter
`/var/tmp/codex/ModSecurity-conector/runs/workflow-consolidation-20260821/security-diff-scan/report.md`.

## Nicht ausgeführte Prüfungen mit Begründung

`make setup-dev` wurde nicht ausgeführt, weil es das separate Framework-
Repository bootstrapped, das der Benutzer nicht als beschreibbar ausgewählt
hat. Vor der Auslieferung wurden weder Live-Maintenance-Workflow-Dispatch,
Token-Mint, Artefakt-Cleanup, Root-Broker, Runtime-Matrix noch GitHub-Actions-
Rerun ausgeführt. Diese Aktionen sind für den lokalen Konsolidierungsnachweis
nicht erforderlich und würden die Task-Grenze erweitern.

## Bekannte Einschränkungen

Der Framework-Gitlink des Task-Worktrees ist nicht initialisiert. Daher kann
das vollständige `make lint` seine Framework-abhängigen No-CRS-Tests nicht
ausführen, obwohl workflow-spezifische, Security-Contract- und statische
Checks bestehen. Hosted-Checks auf dem späteren exakten PR-Head bleiben für
die GitHub-Ausführung erforderlich.

## Verbleibende Risiken

Der gemeinsame Collector verlangt jetzt einen privaten Artefakt-Root ohne
Symlink, statt das von GitHub Runnern gelieferte temporäre Verzeichnis als
ausreichenden Confinement-Nachweis zu behandeln. Künftige Workflow-Änderungen
müssen das Verhalten pro Connector-Wrapper bewahren und Input-Mappings
explizit ergänzen. Die Closure
des Updater-Fixes ist notwendigerweise auf die aktuellen statischen Eingaben
von `check-ci-security-contract` begrenzt; zukünftige Contract-Abhängigkeiten
brauchen dieselbe eingeschränkte Review.

## Finaler Diff- und Review-Status

Der lokale finale Review ist für die Auslieferung bereit: Nur nachgewiesene
duplizierte Collection-Logik wurde zentralisiert; die Workflow-Anzahl bleibt
vor und nach der Änderung 29; kein Workflow wurde entfernt; kein Security-
Scanner oder erforderlicher Wrapper wurde konsolidiert. Source-Diff, finale
Bilingual-/Documentation-Checks, Git-Preflight, Commit, PR, Exact-Head-
Hosted-Checks und der Nicht-Merge-Delivery-Status müssen vor Abschluss
abgelesen werden.
