# FND-SONAR-0031 — CI-Evidence-Reportgeneratoren bewahren fünfzehn SonarQube-Cloud-Cognitive-Complexity-Befunde und einen Duplikatblock

**Sprache:** [English](finding.md) | Deutsch

## Klassifikation

| Feld | Wert |
| --- | --- |
| Kategorie | `maintainability` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Severity / Confidence | `P2` / `not_applicable` / `confirmed` |
| Status / Feasibility | `verified` / `feasible_now` |
| Release-Blocker / sicherheitsrelevant | nein / ja |
| Security-Bewertung | fokussierter Post-Change-Security-Diff-Review: null reportierbare diff-induzierte Befunde |

## Zusammenfassung und Scope

Das revisionsgebundene SonarQube-Cloud-Master-Inventar hat fünfzehn OPEN-
CRITICAL-`python:S3776`-Receipts in Parent-`ci/evidence`-Reportgeneratoren
und einen 23-Zeilen-Duplikatblock. Es enthält keine Bugs, Vulnerabilities oder
Security-Hotspots in der ausgewählten Komponente. Alle Items gehören dem Parent
und besitzen eine verhaltensbewahrende Source-Level-Dispostion im task-eigenen
Worktree.

Der Scope ist auf Parent-Evidence-Report-Quellen, einen bestehenden Parent-
Lifecycle-Helper, direkte Parent-Tests, zweisprachige Traceability und lokale
Evidence begrenzt. Framework, MRTS, Gitlinks, Workflows, SonarQube-Cloud-
Einstellungen, Quality Gates, Exclusions, Suppressions, `NOSONAR`, direkte
Master-Writes und zusätzliche Merges sind ausgeschlossen.

Der geschützte exakte PR-#225-Head
`74bcb950f8a75835b4fb59175a783e9aedcfd1c3` wurde normal als Resulting-
Parent-Master `6dc912643133e5c7d3c305979d4052da9cb45153` gemergt. Seine
vierzehn exakten SHA-GitHub-Actions-Workflows bestanden. Der aktuelle Master-
Readback markiert alle fünfzehn aufbewahrten `python:S3776`-Keys als
`CLOSED/FIXED` und meldet null Violations, Bugs, Vulnerabilities,
Security-Hotspots, Duplikatzeilen und Duplikatdichte für `ci/evidence`.

## Beobachtetes und erwartetes Verhalten

Auf `caabf33c11d6002f9a1661f215ed195d6e141253` meldet die Analyse
`3b1a67b0-1026-4dbc-a437-192604db29b4` Komplexitäten von 16 bis 33 bei
erlaubten 15. Das einzige ausgewählte Duplikatpaar ist der gleichwertige CLI-
Lifecycle zwischen den Final-Consistency-Audit- und Rule-Chain-Generatoren.

Die Report-Schemas, Reihenfolge, der sichere Output-Root-Lifecycle,
Redaktion, zweistufige Path-Normalisierung und fail-closed Runtime-Evidence-
Controls müssen unverändert bleiben, während fokussierte Helper getrennte
Parsing-, Filter-, Klassifizierungs-, Rendering- und Post-Write-
Verantwortlichkeiten besitzen. Beide Einstiegspunkte müssen den etablierten
sicheren Lifecycle ohne doppeltes Scaffolding verwenden.

## Auswirkung und Security-Bewertung

Der Befund ist Maintainability-Arbeit, aber der ausgewählte Code behandelt
pfadbegrenzte Ausgabe, serialisierte Reports, Runtime-Evidence-Interpretation
und Klassifizierung. Ein unvorsichtiger Refactor könnte Evidence-Integrität
schwächen.

Der fokussierte Post-Change-Security-Review fand keinen reportierbaren
diff-induzierten Security-Befund. Er bestätigte insbesondere Safe-Root-Setup
vor Ausgabe und Post-Write-Callback, unveränderte Safe-Writer-Verwendung für
Refresh-Placeholders, zweistufige Path-Normalisierung und fail-closed HAProxy-
XML-Decision-Evidence. Es gibt keine Behauptung eines repositoryweiten
Security-Scans oder einer Hosted-Analyse.

## Betroffene Dateien und Symbole

Betroffene Source-Dateien sind:

- `ci/evidence/reports/refresh-connector-reports.py`
- `ci/evidence/reports/generate-connector-roadmap.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-final-consistency-audit.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `ci/evidence/reports/generate-phase4-hard-abort-capability.py`
- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/lib/focused_analysis_utils.py`

Die aufbewahrten Issue-Keys und Symbole stehen vollständig im strukturierten
Record: `AZ9cRyiqHhV2CayPTPx_`, `AZ9cRyi6HhV2CayPTPyT`,
`AZ7ep2ThZ5UXdmR_OUeO`, `AZ7ajOtE7vSmgsKNjY2U`,
`AZ7WiKyayVFzp-oVN3ZD`, `AZ7PU4lam6NRVhQ0A9r7`,
`AZ9cRyiqHhV2CayPTPyN`, `AZ9cRyiqHhV2CayPTPyB`,
`AZ7HxAmX_i61V0DF6_GQ`, `AZ7HxAoZ_i61V0DF6_G4`,
`AZ7HxAmF_i61V0DF6_GI`, `AZ7HxAmq_i61V0DF6_GU`,
`AZ7HxAnC_i61V0DF6_Gd`, `AZ7HxAlw_i61V0DF6_GE` und
`AZ7HxAoH_i61V0DF6_G1`.

## Voraussetzungen, Reproduktion und Evidence

Der Scope ist an die Current-Master-Analyse
`3b1a67b0-1026-4dbc-a437-192604db29b4` und Revision
`caabf33c11d6002f9a1661f215ed195d6e141253` gebunden. Reproduziere ihn mit
den aufbewahrten read-only SonarQube-Cloud-Issue-, Component-Metric- und
Duplicate-Block-API-Abfragen im Inventar-Receipt:

- Historischer Pfad des Sonar-Master-CI-Evidence-Inventars
  `.codex/runs/20260801-ci-evidence-sonar-remediation/evidence/sonar-master-ci-evidence-inventory.json`
  (nicht in diesem Reconciliation-Checkout verteilt)
  — SHA-256 `d521f5a19ac7e6f40f0c49e4c65357a9bdd1dbfed65bf21bbfde4809de19865b`;
  Exit `0`; beobachtet `2026-08-01T14:05:20Z`.

Die Resulting-Master-Verifikation hat den historischen Pfad
`.codex/runs/20260801-pr225-master-integration/evidence/master-verification.json`
(nicht in diesem Reconciliation-Checkout verteilt)
aufbewahrt — SHA-256 `d63bacab44956e35958cef9d8bd82e476853a3d77d672ab804285077f4173a4b`;
Exit `0`; beobachtet `2026-08-01T16:32:10Z`. Sie ist an Master
`6dc912643133e5c7d3c305979d4052da9cb45153` gebunden und wird nicht aus der
Baseline wiederverwendet.

## Root Cause und Remediation

Die betroffenen Funktionen sammelten zu viele unabhängige Report-
Verantwortlichkeiten, und zwei CLI-Einstiegspunkte bewahrten gleichwertiges
Lifecycle-Scaffolding. Der Patch extrahiert enge Helper bei Erhalt der
bestehenden Verträge. Das Final Audit erreicht seinen bestehenden sicheren
Lifecycle durch einen expliziten Post-Write-Callback; Refresh-Ausgabe nutzt
weiterhin den Safe Writer; und Runtime-XML-Evidence bewahrt ihre strikten
All-or-Nothing-Decision-Prädikate.

Keine SonarQube-Cloud-Rule, kein Quality Gate, keine Exclusion, Suppression,
kein `NOSONAR`, Workflow, Framework-/MRTS-Source oder Gitlink wird geändert.
Dies ist kein reiner Metrik-Code-Move.

## Akzeptanzkriterien und Validierungsplan

- Jeder aufbewahrte Issue-Key und der Duplikatblock besitzt eine konkrete
  Source-Level-Disposition.
- Fokussierte Source-/Schema-/Reihenfolge-/Path-/Evidence-Controls bestehen,
  einschließlich legitimer Safe-Output- und fail-closed negativer Controls.
- Ein fokussierter Post-Change-Security-Diff-Review meldet keinen
  reportierbaren neuen Befund.
- Der exakte PR-Head hat null OPEN/CONFIRMED SonarQube-Cloud-New-Issues,
  null New-Code-Duplikation und ein bestehendes Quality Gate ohne Änderung von
  Scanner-Controls.
- Die separat autorisierte Integration besitzt einen Resulting-Master-
  SonarQube-Cloud-Readback: Die ursprünglichen fünfzehn Keys sind
  `CLOSED/FIXED`, und `ci/evidence` meldet null Duplikatzeilen, bevor dieser
  Record `verified` wird.

Die lokale Suite enthält `tests.test_focused_analysis_utils`,
`tests.test_report_conditional_remediation`, `tests.test_case_metadata_utils`,
`tests.test_remaining_failure_analysis`,
`tests.test_nginx_mrts_http500_cluster_analysis`,
`tests.test_report_presentation_literals`,
`tests.test_generated_report_evidence_integrity`,
`tests.test_evidence_output_security`, `tests.test_runtime_path_security` und
`tests.test_runtime_env_snapshot_contract`.

## Abhängigkeiten, Blocker und Restrisiko

Es gibt keinen Source-Level-Blocker und keine verbleibende Abhängigkeit. Der
exakte PR-#225-Head `74bcb950f8a75835b4fb59175a783e9aedcfd1c3` bestand seine
frischen geschützten Checks und das SonarQube-Cloud-PR-Quality-Gate, bevor
GitHub ihn normal als Master `6dc912643133e5c7d3c305979d4052da9cb45153`
mergte. Alle vierzehn exakten Master-GitHub-Actions-Workflows bestanden. Die
direkte Resulting-Master-Reproduktion schließt alle fünfzehn ursprünglichen
`python:S3776`-Keys und dokumentiert null `ci/evidence`-Duplikatzeilen. Das
globale Master-Quality-Gate ist dennoch wegen derselben bereits bestehenden
`new_security_rating`-E-Bedingung wie auf dem direkten Vorgänger
`7016a66f3702523098811b45139133c77dee88fb` `ERROR`; sie wird getrennt unter
`FND-SONAR-0001` verfolgt und diesem Finding nicht zugeschrieben.

Der temporäre Task-Worktree hat kein initialisiertes Framework-Submodul, daher
beendet ein Environment-Snapshot-Test dort erwartbar mit `77`; derselbe
unveränderte Test besteht im kanonischen Parent-Checkout. Ein breiter
`make lint`-Versuch stoppt bei bereits vorhandenen Apache-C17-Fehlern außerhalb
dieses Task-Scopes. Keine Einschränkung wird als erfolgreiche vollständige
Suite oder Finding-Auflösung behauptet.

Verwandtes Aggregat: `FND-SONAR-0016`. Es gibt kein Duplicate-Finding und
kein akzeptiertes Risiko. Der Source-Patch ist
`014eaff40557ba33346ea0cb33ce8d27be8546d0`, gefolgt von normaler Task-Branch-
Synchronisierung und ihrem Traceability-Update bei
`d86fd1f91177ae8dceb2906a00d802e4735cd9b4`; keiner der Commits ist ein
Hosted- oder Resulting-Master-Beweis.

## Historie

- `2026-08-01T14:05:20Z`: Das revisionsgebundene Current-Master-Sonar-
  Inventar identifizierte alle fünfzehn Receipts und den einzelnen
  Duplikatblock.
- `2026-08-01T15:34:38Z`: Als dedizierter Record angelegt, weil das verwandte
  Aggregat `FND-SONAR-0016` weder die exakten aktuellen Keys noch den exakten
  Duplikatblock enthält. Lokale Remediation und fokussierte Control-Evidence
  sind in Bearbeitung; es werden kein Commit, Push, PR, Hosted-Verifikation,
  Merge oder Master-Change behauptet.
- `2026-08-01T15:51:57Z`: Die Parent-Source-/Test-Remediation wurde committed,
  normal mit aktuellem `origin/master` synchronisiert und durch 161
  fokussierte Task-Worktree-Tests plus 9 kanonische Snapshot-Contract-Tests
  erneut ausgeführt. Der Lifecycle-Status ist `fixed`, nicht `verified`: Es
  werden kein Push, Draft-PR, Exact-Head-Hosted-Analyse, Merge oder
  Resulting-Master-Reproduktion behauptet.
- `2026-08-01T15:55:56Z`: Draft-PR #225 Exact Head
  `d86fd1f91177ae8dceb2906a00d802e4735cd9b4` stimmt lokal, remote und auf
  GitHub überein. Alle 39 GitHub-Checks sind terminal (33 bestanden, 6
  scope-übersprungen), und SonarQube Cloud meldet Quality Gate `OK`, null
  offene PR-Issues, null neue duplizierte Zeilen und 0,0 % New-Code-
  Duplikation. Es werden kein Merge und kein Resulting-Master-Ergebnis
  behauptet; der Record bleibt `fixed`.
- `2026-08-01T16:32:10Z`: GitHub mergte den geschützten exakten PR-#225-Head
  `74bcb950f8a75835b4fb59175a783e9aedcfd1c3` normal als Resulting-Parent-
  Master `6dc912643133e5c7d3c305979d4052da9cb45153`. Alle vierzehn exakten
  Master-GitHub-Actions-Workflows bestanden. Die gebundene SonarQube-Cloud-
  Master-Analyse markiert alle fünfzehn aufbewahrten `python:S3776`-Keys
  `CLOSED/FIXED`; die ausgewählte `ci/evidence`-Komponente meldet null
  Violations und null Duplikatzeilen. Das globale Quality Gate bleibt allein
  wegen der bereits bestehenden `new_security_rating`-E-Baseline unter
  `FND-SONAR-0001` ERROR; sie entspricht dem direkten Vorgänger und ist keine
  PR-#225-Regression. Dieser Record ist daher `verified`, nicht automatisch
  `closed`.
