# Change Record: Reparatur der read-only Update-Submodules-Runtime-Pfad-Validierung

**Sprache:** [English](CR-20260723-update-submodules-runtime-path-validation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-update-submodules-runtime-path-validation |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | 95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3 |
| Grenze | Parent-`Update submodules`-read-only-Validator, sein Parent-Runtime-Path-Policy-Checker und seine Testabdeckung, dieses englische/deutsche Change-Record-Paar sowie beide Change-Record-Indizes. Framework-Source, MRTS, der Parent-Framework-Gitlink, Workflow-Berechtigungen, Action-Pins, Dependency-Locks, Resolver-Reihenfolge und Publisher-Verhalten bleiben unverändert. |
| Finding-Verknüpfung | FND-PARENT-0050: bestätigter Parent-CI-Fehler durch eine veraltete Self-Test-Erwartung. Sein vollständiges englisches/deutsches/JSON-Canonical-Import-Paket wird in task-eigener Evidence aufbewahrt; der lokale Canonical-`.codex/findings`-Import ist `blocked_permissions`, weil dieser Mount read-only ist. Verwandter historischer Kontext: FND-PARENT-0045, FND-PARENT-0048 und FND-PARENT-0049. |
| Delivery-Status | Draft-Parent-[PR #93](https://github.com/Easton97-Jens/ModSecurity-conector/pull/93) wurde aus `agent/update-submodules-run19-remediation` nach den Commits `b4eb4733706cbc555e6bb5be26492ec2058e0ec2` und `4cb226071ce3f42f5bff803a6e99ab748a2a7aef` erstellt. Dieses Change-Record-Amendment ist ein normaler Folge-Commit; sein exakter finaler Head wird in PR-/Task-Evidence aufbewahrt, statt eine selbstreferenzielle Commit-Schleife zu erzeugen. Es wird noch kein Exact-Head-CI-, Review-, SonarQube-Cloud-, Merge- oder Resulting-Master-Workflow-Ergebnis behauptet. Der aktuelle Prompt autorisiert nur eine normale Parent-PR-only-Reparaturintegration und ihre Resulting-Master-Validierung. |

## Motivation und Problemstellung

GitHub Actions `Update submodules` Run #19 / Run [29991272761](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29991272761) erreichte Parent-`master` `95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3` und löste Framework-Candidate `935cf14c676a24672be5c336e92cd13457cc35c8` auf. Die hash-gelockte PyYAML-Validierungsvoraussetzung installierte erfolgreich, doch der read-only-Validator scheiterte in `make quick-check`, weil der Parent-Shell-Self-Test verlangte, dass `assert_safe_runtime_path` `/src` akzeptiert.

Das Candidate-Framework klassifiziert Source-Checkout-Roots korrekt als Non-System-/read-only-Pfade und nicht als veränderbare Runtime-Ziele. Der Parent-Checker vermischte diese zwei Eigenschaften und lehnte daher einen strengeren, sichereren Framework-Candidate ab, bevor der enge Publisher laufen konnte. Der Publisher wurde nach dem Validierungsfehler korrekt übersprungen.

## Akzeptanzkriterien

- Der Checker beweist weiterhin, dass Source-Roots keine Systempfade sind, verlangt aber nicht mehr, dass sie als schreibbare Runtime-Pfade akzeptiert werden.
- Ein verifizierter Runtime-/Cache-Descendant bleibt der positive `assert_safe_runtime_path`-Control.
- Die Regression schlägt mit dem früheren Verhalten fehl, indem sie eine Framework-Implementierung simuliert, die Source-Roots als Runtime-Write-Pfade zurückweist.
- Read-only-Berechtigungen von Resolver/Validator, Validierungsreihenfolge, Dependency-Locks, Action-Pins, Candidate-Scope und enge Publisher-Isolation bleiben unverändert.
- Exact-Head-PR-Checks, Review-/Conversation-Status, SonarQube Cloud falls konfiguriert, repository-etablierter PR-only-Squash-Merge und ein neuer Resulting-Master-`Update submodules`-Run werden beobachtet, bevor diese Reparatur als vollständig berichtet wird.

## Implementierungsentscheidung und Begründung

`check_shell_policy` führt seine positive Shell-Assertion nun nur für den verifizierten Cache-/Runtime-Control aus. Die getrennten Non-System-Assertions für `/src`, `/src/ModSecurity-conector-build`, den Parent-Checkout und den Parent-Build-Pfad bleiben erhalten. Ein Source-Ort kann Non-System und read-only sein, ohne ein zulässiger veränderbarer Runtime-Root zu sein.

Die Regression verwendet ein Candidate-Shell-Test-Double, das jeden an `assert_safe_runtime_path` übergebenen Source-Root zurückweist, aber den verifizierten Cache-Pfad akzeptiert. Sie sichert ab, dass der Checker das Runtime-Write-Prädikat für Source-Orte nie aufruft. Weder Framework-Implementierung noch Gitlink oder MRTS-Inhalt werden geändert.

## Geänderte Dateien

- `ci/checks/security/check-runtime-path-policy.py`: Beibehaltung der Non-System-Klassifikation von Source-Pfaden, aber Entfernung der veralteten positiven Runtime-Write-Erwartung für Source-Roots.
- `tests/test_runtime_path_policy.py`: Hinzufügen der Source-Root-Rejection-Regression bei Beibehaltung des positiven Verified-Cache-Controls.
- Dieses englische/deutsche Change-Record-Paar und beide Change-Record-Indizes.

Keine Workflow-Datei, Framework-Source, MRTS-Inhalt, Parent-Gitlink, Action-Pin, Workflow-Berechtigung, Secret, Dependency-Lock oder Publisher-Code wird geändert.

## Ausgeführte Befehle

- Hosted-Diagnose: Run `29991272761` scheiterte bei `check-runtime-path-policy` mit `test_path is not under an allowed runtime/cache root: /src`; der Resolver endete erfolgreich, der read-only-Validator erreichte `make quick-check`, und der Publisher wurde übersprungen.
- Bestanden: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp .venv/bin/python -m unittest -v tests.test_runtime_path_policy` — 6 Tests, einschließlich der neuen Source-Root-Rejection-Regression.
- Bestanden: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp RUNNER_TEMP=<task-run>/tmp make check-runtime-path-policy` — `check-runtime-path-policy: PASS`.
- Bestanden: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp RUNNER_TEMP=<task-run>/tmp make check-ci-security-contract` — 16 Tests; der Resolver → read-only Validator → enge Publisher-Contract blieb abgedeckt.
- Blockierte Umgebung: Der ausgewählte External-Root-`make quick-check` lief durch Shell-Syntax und 66 Normalisierungs-/Komponententests, stoppte aber an der vorhandenen lokalen Apache/APXS-Provisionierungsgrenze. Der Framework-Helper fand unmanaged Shared-Cache-Entries und konnte `apxs`/`apxs2` nicht bereitstellen; das Target endete über `check-apache-c17-lint` mit Exit 2. Dies ist kein Fehler des geänderten Python-Checkers oder der Regression, rechtfertigt kein Deaktivieren des Runtime-Component-Controls und wird für die Akzeptanz durch den erforderlichen Hosted-Resulting-Master-Workflow ersetzt.

## Security-Auswirkung

Diese Änderung verengt eine Testannahme; sie erweitert keinen akzeptierten Runtime-Pfad. Source-Roots werden ausdrücklich nicht mehr als veränderbare Runtime-Ziele behandelt. Der positive Cache-/Runtime-Control bleibt erhalten, sodass ein Framework-Candidate nicht durch die Ablehnung aller Pfade bestehen kann. Der Resolver validiert weiter den offiziellen Candidate-SHA, Candidate-Code bleibt im `contents: read`-Validator, und der separat gegatete Publisher bleibt der einzige schreibfähige Pfad. Keine Berechtigung, kein Token, Secret, Action-Pin, Dependency-Acquisition oder Publisher-Gate wird geschwächt.

## Runtime-Evidence

Nicht anwendbar. Dies ist eine statische Parent-Validator-/Self-Test-Reparatur. Sie behauptet keinen Connector-, HTTP-, HTTP/2-, HTTP/3- oder Runtime-Erfolg. Die einzige erforderliche Hosted-Behavior-Evidence ist das Ergebnis des Resulting-Master-`Update submodules`-Workflows.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein lokaler vollständiger Abschluss von `make quick-check` ist in diesem Checkout nicht verfügbar, weil sein Apache/APXS-Dependency-Provisioner bei unmanaged Cache-Entries fail-closed scheitert. Der Fehler wurde als Environment-Evidence aufbewahrt; kein Cache, Framework oder Control wurde zur Umgehung geändert.
- Kein Framework-Change, Framework-PR, Framework-Merge, Framework-Gitlink-Update, MRTS-Change oder MRTS-Test lief; alles liegt außerhalb des Scopes.
- Exact-Head-GitHub-Checks, SonarQube Cloud, Review, PR-only-Squash-Merge und der Resulting-Master-Workflow stehen bei diesem Pre-Delivery-Snapshot aus und müssen ausschließlich aus beobachteter GitHub-Evidence erfasst werden.

## Bekannte Einschränkungen

Das lokale Canonical-Finding-Register kann FND-PARENT-0050 derzeit nicht annehmen, weil sein `.codex`-Mount read-only ist. Das vollständige bilinguale/JSON-Import-Paket wird in task-eigener Evidence aufbewahrt und muss importiert werden, wenn das Register schreibbar ist. Dies ändert weder den versionierten Parent-Fix noch behauptet es, dass Canonical-Finding/Index/Backlog/Roadmap aktualisiert wurde.

## Verbleibende Risiken

Bis der exakte Task-PR-Head reviewed ist und seine erforderlichen Checks bestehen, und bis ein frischer `Update submodules`-Run auf Resulting-`master` erfolgreich ist, bleibt die automatisierte Framework-Candidate-Veröffentlichung korrekt blockiert. Die vorhandene fail-closed-Validierung und die enge Publisher-Isolation verhindern Veröffentlichung bei einem Validierungsfehler. Kein Risiko wird akzeptiert.

## Finaler Diff- und Review-Status

Der Pre-Delivery-Review findet den beabsichtigten Source-Diff auf den Parent-Runtime-Path-Self-Test und seine Regression begrenzt. `git diff --check`, die bilinguale Dokumentationsvalidierung, die Dokumentations-Link-Validierung, die ausgewählte Python-Kompilierung und der fokussierte Security-Diff-Review schlossen erfolgreich ab. Der Security-Review fand keine berichtspflichtige Regression: Source-Roots sind nicht neu write-safe, der verifizierte Cache-Control bleibt erhalten, und die Trennung von read-only Resolver/Validator und engem Publisher ist unverändert. Exact-Head-CI, SonarQube Cloud, Review, Merge und Resulting-Master-Workflow-Dispositions stehen weiter aus und werden vor Abschluss mit beobachteter Evidence abgeglichen.
