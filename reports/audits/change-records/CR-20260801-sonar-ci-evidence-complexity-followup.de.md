# Änderungsnachweis: Parent-CI-Evidence-SonarQube-Cloud-Complexity-Follow-up

**Sprache:** [English](CR-20260801-sonar-ci-evidence-complexity-followup.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-ci-evidence-complexity-followup` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `caabf33c11d6002f9a1661f215ed195d6e141253` |
| Tracking | `FND-SONAR-0031` — 15 aktuelle `python:S3776`-Receipts und ein 23-Zeilen-Duplikatblock in `ci/evidence`. |
| Grenze | Parent `ci/evidence/**`, `ci/lib/focused_analysis_utils.py`, direkte Parent-Tests und dieses englisch/deutsche Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, Workflows, Scanner-Einstellungen, Quality Gates, Exclusions und Suppressions bleiben unverändert. `master` wird nicht direkt geändert; die einzige autorisierte Änderung ist die unten beschriebene geschützte PR-Integration. |
| Auslieferungs-Tracking | Task-Branch `agent/ci-evidence-sonar-remediation-followup-20260801`; PR [#225](https://github.com/Easton97-Jens/ModSecurity-conector/pull/225) ist offen. Der aktuelle Nutzer hat die Integration genau dieses Parent-PRs in `master` ausdrücklich autorisiert; beim Update dieses Records ist noch kein Merge erfolgt. |

## Motivation und Problemstellung

Die aktuelle Parent-`ci/evidence`-Komponente enthält fünfzehn OPEN-CRITICAL-
`python:S3776`-Cognitive-Complexity-Receipts und 23 duplizierte Zeilen
(0,1 %). Die betroffenen Reportgeneratoren klassifizieren Runtime-Evidence,
rendern Operator-Reports und schreiben unter sicheren Output-Roots. Die
Remediation muss die echten Source-Ursachen verringern und zugleich Schemas,
Reihenfolge, Redaktion, Path-Containment und fail-closed Evidence-Verhalten
bewahren.

## Implementierungsentscheidung und Begründung

Der Patch zerlegt jede ausgewählte Funktion an einer bestehenden
Verantwortungsgrenze: Datensammlung, reine Klassifizierung, Rendering oder
Lifecycle-Ownership. Der doppelte Final-Audit-CLI-Lifecycle wird durch den
bestehenden sicheren Report-Lifecycle mit einem festen Post-Write-Callback
ersetzt. Dadurch bleiben Safe-Root-Registrierung und `write_text_file` in
ihrer bestehenden Reihenfolge, statt einen zweiten Output-Pfad einzuführen.

Die Runtime-Mismatch-Helper bewahren strikte HAProxy-XML-Decision-Prädikate,
einschließlich exakter Boolean-Prüfungen, eines Decision-Records, eines
nicht-disruptiven Passes und leerer Match-Felder. Refresh-Placeholders nutzen
weiterhin den etablierten Safe Writer. Die NGINX-Classifier-Reihenfolge wird
an ihren bestehenden Unit-Vertrag angeglichen. Kein generierter Report, kein
Runtime-Evidence-Artefakt, keine Scanner-Einstellung, Rule, Gate, Exclusion,
Suppression, `NOSONAR`, Workflow, Framework-/MRTS-Source oder Gitlink wird
geändert.

## Akzeptanzkriterien

- Alle fünfzehn aufbewahrten Issue-Keys und der Duplikatblock besitzen eine
  konkrete verhaltensbewahrende Source-Disposition im task-eigenen Diff.
- Fokussierte Tests bewahren Report-Schemas, Reihenfolge, Fallback,
  Safe-Output, Path-Normalisierung und fail-closed Runtime-Evidence-Controls.
- Der exakte aktuelle PR-Head meldet null OPEN/CONFIRMED SonarQube-Cloud-New-
  Issues, null New-Code-Duplikation und ein bestehendes Quality Gate ohne
  Scanner-Control-Änderung.
- Der aktuelle Nutzer hat „bringe das pr 225 in den master“ autorisiert. Die
  Integration darf nur über den repository-konformen geschützten
  Exact-Head-PR-Mechanismus nach frischen Checks, Reviews, Conversations,
  SonarQube Cloud und Resulting-`master`-Verifikation erfolgen; dieser Record
  behauptet keinen Merge.

## Geänderte Dateien

- Elf Parent-`ci/evidence/reports/*.py`-Generatoren, einschließlich Refresh,
  Runtime Mismatch, Final Audit, Phase 4, NGINX, Body Processor,
  Intervention, Response Header, Rule Chain, Remaining Failure und Roadmap.
- `ci/lib/focused_analysis_utils.py` für die eng begrenzte Post-Write-Seam.
- `tests/test_focused_analysis_utils.py`,
  `tests/test_report_conditional_remediation.py` und
  `tests/test_remaining_failure_analysis.py` für direkte Regression- und
  fail-closed Controls.
- Dieses englisch/deutsche Change-Record-Paar und die gepaarten Indizes.

## Ausgeführte Befehle

| Befehl oder Check | Ergebnis |
| --- | --- |
| `python3 -m py_compile` über alle geänderten Python-Quellen und direkten Tests | bestanden. |
| Fokussiertes Python-Aggregat über die geänderten Report-/Evidence-Familien | bestanden: 161 Tests im Task-Worktree, einschließlich direkter Phase-4-Metadata-/Classification-Priorität und Legitimate-Control-Abdeckung. |
| `python3 -m unittest -q tests.test_runtime_env_snapshot_contract` im kanonischen Parent-Checkout | bestanden: 9 Tests. |
| `git diff --check` | vor Traceability-Ergänzungen bestanden; vor Auslieferung erneut auszuführen. |
| Fokussierter Post-Change-Codex-Security-Diff-Review | bestanden: kein reportierbarer diff-induzierter Befund. |
| Breites `make lint` mit task-eigenem externem Build-Root | stoppte bei bereits vorhandenen Apache-C17-Warnungen/-Fehlern außerhalb dieser Änderung; es validiert oder invalidiert den ausgewählten Report-Patch nicht. |
| `git merge --no-edit origin/master` | zweimal als normale Task-Branch-Synchronisierung abgeschlossen: `62f7e13f35edd3f73661f724fd5208dcf1584d18` ist durch `ade8b066e9ffb0e17d9971cb6a9ab9ab4bf2e1c0` enthalten, danach aktuelles `7016a66f3702523098811b45139133c77dee88fb` durch `290843bda5b922dad59a9a9f80688ebf422b960c`; keine der Operationen änderte `master` direkt. |

## Security-Auswirkung

Dies ist Maintainability-Arbeit innerhalb einer sicherheitsrelevanten Evidence-
Grenze. Der Review verifiziert, dass Safe-Root-Registrierung weiterhin jedem
Output-Pfad vorausgeht, der Final-Audit-Callback erst nach dem Schreiben des
sicheren Report-Paars läuft, Refresh-Placeholders weiterhin den Safe Writer
nutzen und HAProxy-XML-Evidence fail-closed bleibt. Es wurden keine neue Shell-
Ausführung, kein direkter unsicherer Write, keine untrusted Path-Erweiterung
und kein Evidence-Classification-Bypass eingeführt.

## Runtime-Evidence

Die fokussierten Tests üben Report-Source-Verträge mit task-eigenen temporären
Fixtures aus. Sie enthalten Safe-Output- und Path-Controls, fail-closed XML-
Decision-Negativfälle, Reihenfolge- und Fallback-Verträge sowie Final-Audit-
Release-Gate-Ergebnisse. Sie behaupten keine vollständige Connector-Matrix
oder Live-Runtime-Report-Regenerierung.

## Bekannte Einschränkungen

Der temporäre Task-Worktree besitzt absichtlich kein initialisiertes Framework-
Submodul. Die separat versuchte vollständige Snapshot-Contract-Suite hat daher
einen reinen Umgebungfall,
`test_with_runner_consumes_the_prepared_snapshot_without_reading_shared_env`,
der dort mit `77` endet, weil
`modules/ModSecurity-test-Framework/ci/lib/common.sh` fehlt. Dieselbe
unveränderte Testsuite besteht im kanonischen Parent-Checkout; dies trennt eine
Worktree-Voraussetzung von einer Source-Patch-Regression.

`make check-generated-report-layout` ist kein bestehender Control: Sowohl
Task-Worktree als auch kanonischer Checkout melden dieselbe veraltete/fehlende
historische Generated-Report-Evidence. Sie wurde nicht repariert, weil kein
generierter Report und kein Evidence-Artefakt im Scope liegen.

## Nicht ausgeführte Prüfungen mit Begründung

Volle Connector-Builds, Runtime-Matrizen und Framework-/MRTS-Checks werden
nicht ausgeführt: Dies ist ein Parent-Report-Source-Refactor ohne Framework- /
MRTS-Änderung. Die jüngste Branch-Synchronisierung und dieses wahrheitsgemäße
Delivery-Record-Update verlangen eine frische Exact-Head-GitHub-Actions- und
SonarQube-Cloud-Runde. Resulting-`master`-Workflows und SonarQube-Cloud-Analyse
sind bis zur separat geschützten Integrationsoperation ausstehend; sie werden
nicht aus PR-Checks abgeleitet.

## Verbleibende Risiken und Verifikationsstatus

Die lokale Source und die fokussierten Tests stützen das beabsichtigte
Verhalten, aber die Branch-Synchronisierung entwertet frühere PR-Check-Evidence
für die Merge-Eignung. Beim Update dieses Records enthält der Task-Branch den
Synchronisierungs-Commit `290843bda5b922dad59a9a9f80688ebf422b960c`; das
Documentation-Update selbst erzeugt einen späteren PR-Head, der erneut ein
vollständiges Exact-Head-GitHub-Actions- und SonarQube-Cloud-Readback verlangt.
Dieser Record behauptet keinen erfolgten Merge, keine Resulting-Master-SHA und
kein Master-Workflow-Ergebnis.

## Finaler Diff- und Review-Status

Nach der ersten normalen Master-Synchronisierung wurden das fokussierte
161-Test-Aggregat und der 9-Test-kanonische Snapshot-Contract erfolgreich
erneut ausgeführt. Die spätere normale Synchronisierung auf
`7016a66f3702523098811b45139133c77dee88fb` und diese Delivery-Record-Korrektur
verlangen vor der geschützten Integration frisch abgeglichene fokussierte Tests,
finales `git diff --check`, Documentation-Pair-Verifikation, staged-file
Secret-Scan, exaktes Remote-Identity-Preflight und Security-Diff-Review. Der
Task bleibt Parent-only; keine Framework-/MRTS-/Gitlink-Änderung ist erlaubt.

## Auslieferungsautorisierung

Der aktuelle Nutzer hat „bringe das pr 225 in den master“ für genau diesen
Parent-PR ausdrücklich autorisiert. Die Autorisierung erlaubt nur die normale
geschützte PR-Integration nach einer neuen Exact-Head-Verifikation; sie
erlaubt keinen direkten `master`-Push, Force-Push, administrativen Bypass,
Framework-/MRTS-Aktion, Gitlink-Change, Branch-Löschung, Release oder
Deployment. Der Merge bleibt unbehauptet, bis GitHub ihn ausweist und die
resultierenden `master`-Checks bestehen.
