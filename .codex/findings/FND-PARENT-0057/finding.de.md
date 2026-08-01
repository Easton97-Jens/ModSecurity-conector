# FND-PARENT-0057 — Draft-Parent-PR #74 expandiert PR-kontrollierte Workflow-Ausgabe an einer Template-zu-Shell-Grenze

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0057 |
| Kategorie | security_candidate |
| Repository / Ownership | parent / parent |
| Priorität / Schweregrad / Konfidenz | P1 / medium / probable |
| Status / Machbarkeit | in_progress / feasible_now |
| Release-Blocker | ja |
| Sicherheitsbewertung | plausible |
| Exakter Scope | Draft-Parent-PR #74, Head 9046c69cc49145e70b18b5fc86a7c3fe67926d5a |

## Zusammenfassung, Scope und Invariante

Der Hosted-Zizmor-Job für den exakten Head endete mit einem
Template-Injection-Signal bei
.github/workflows/verified-report-governance.yml:150:31. Der Legacy-Bash-
Schritt expandierte einen staged-root-Workflow-Output von
verified-evidence-paths, nachdem ausgecheckter PR-Code ihn schreiben konnte.
Dieselbe retained Observation enthält die SonarQube-Cloud-Vulnerability
pythonsecurity:S8707, Key AZ-fw-Tf7_zRPd2N8_S2, bei
ci/evidence/reports/stage-verified-full-matrix-evidence.py:65, wo das damals
benutzerwählbare --github-output Path.open erreichte.

Die aktuelle lokale Korrektur entfernt --github-output und Path.open
vollständig. Ein statischer Workflow-Schritt erzeugt den privaten Stage-Parent
mit umask, mktemp und chmod, sendet nur stage_parent durch den Workflow-Output
in das Step-Environment-Mapping VERIFIED_EVIDENCE_STAGE_ROOT und lässt
Stage-/Final-Commands die quotierte Shell-Variable expandieren. Kein
PR-abgeleiteter Step-Output darf über eine GitHub-Actions-Expression in
Run-Script-Quelltext gelangen, und die Stage-CLI besitzt keinen
benutzerwählbaren Output-File-Sink.

Dies bleibt eine plausible Trust-Boundary-Korrektur, keine Behauptung einer
Exploit-Ausführung, Credential-Offenlegung oder erfolgreichen Umgehung. Sie
ist vom aggregierten Quality-Gate-Record FND-SONAR-0016 und vom
Full-Matrix-Port-Range-Reliability-Record FND-PARENT-0058 getrennt.

## Evidenz und Reproduktion

Die retained Evidence ist
/var/tmp/codex/ModSecurity-conector/runs/20260726T185607Z-pr74-fast-validation-hosted-followup/evidence/hosted-observation.md
(Run 20260726T185607Z-pr74-fast-validation-hosted-followup, SHA-256
5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956,
2.978 Bytes). Das read-only Readback der GitHub-Actions-Failed-Logs und der
SonarQube-Cloud-PR-#74-Quality-Gate/Issues endete mit 0. PR #74 bleibt Draft;
es werden weder Risikoakzeptanz, Close, Merge noch Delivery behauptet.

Zur Reproduktion der ursprünglichen Bedingung die Failed Logs von
GitHub-Actions-Run 30215550687 lesen, den Legacy-Workflow-Output-zu-Stage-
Root-Source-to-Sink-Pfad untersuchen und das frühere --github-output bis
Path.open verfolgen. Zur Validierung der lokalen Korrektur bestätigen, dass
die CLI dieses Argument und diesen Sink nicht mehr bereitstellt; die statische
umask/mktemp/chmod-Stage-Parent-Allokation, den stage_parent-only-Output-
Handoff in VERIFIED_EVIDENCE_STAGE_ROOT sowie die quotierte Shell-Variable in
Stage- und Final-Commands prüfen.

## Remediation, Akzeptanz und Validierung

Die implementierte lokale Remediation entfernt --github-output und Path.open
vollständig. Sie behält die private Stage-Allokation durch umask/mktemp/chmod
workflow-eigen, mappt nur stage_parent durch den Output in
VERIFIED_EVIDENCE_STAGE_ROOT Step-Environment und übergibt Stage-/Final-
Commands nur eine quotierte Shell-Variable. Der strikte vollständige
Report-Governance-Producer bleibt erforderlich; der Acht-Sekunden-Preflight
ist nur ein früher Reject-Pfad.

Die Korrektur ist nur akzeptiert, wenn:

- eine Zizmor-Analyse eines exakten Nachfolger-PR-#74 am Workflow-Pfad kein
  aktives Template-Injection-Finding enthält;
- kein von PR geschriebener Step-Output in ein Run-Script interpoliert wird;
- --github-output in der Stage-CLI fehlt oder abgewiesen wird und Path.open
  kein erreichbarer Output-File-Sink ist;
- statischer Private-Parent, stage_parent-only-Environment-Handoff und
  quotierte Shell-Variable durch fokussierte negative und legitime Controls
  bewiesen sind;
- der strikte Full Producer, repository-native Security-Checks, SonarQube
  Cloud des exakten Nachfolger-Heads, Review und Protected Integration ohne
  Regel-, Quality-Gate-, Exclusion-, Suppression-, Coverage-,
  Framework-/MRTS-/Gitlink- oder Kontrolllockerungsänderung bestehen; und
- FND-SONAR-0016 sein Null-Open-Findings-Kriterium erreicht.

## Abhängigkeiten, Restrisiko und Historie

Abhängigkeiten sind die Exact-Successor-Zero-Open-Finding-Validierung von
FND-SONAR-0016 sowie frische Hosted-Workflow-, Full-Producer-, Review- und
Protected-Integration-Evidence. Die lokale Korrektur ist implementiert, aber
nicht verifiziert: Sie muss beweisen, dass der statische Private-Parent-
Environment-Handoff die beabsichtigten Kontrollen ohne neue Trust Boundary
erhält. FND-PARENT-0058 bleibt ein separater Test-/Runtime-Evidence-
Reliability-Defekt.

Die anfängliche plausible Korrektur wurde am 2026-07-26T18:56:07Z alloziert.
Am 2026-07-26T19:55:51Z wurde die lokale Entfernung von --github-output und
Path.open samt statischem Stage-Parent-Environment-Handoff erfasst. Das Finding
bleibt in_progress; es werden keine fixed-, verified- oder Delivery-
Disposition behauptet.
