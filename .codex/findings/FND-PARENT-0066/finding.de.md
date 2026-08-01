# FND-PARENT-0066 — Ungültige Full-Matrix-Control-Evidence kann den Status pass behalten und eine reine Evidence-Reklassifizierung erlauben

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0066 |
| Kategorie | evidence_gap |
| Repository / Ownership | Parent / Parent |
| Priorität / Schweregrad / Confidence | P2 / low / validated |
| Status / Feasibility | fixed / feasible_now |
| Release-Blocker / sicherheitsrelevant | false / true |
| Connector / Profil | Apache-, HAProxy-, NGINX-Full-Matrix-Evidence / verified runtime mismatch analysis |

## Zusammenfassung

Auf Parent-Revision 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 bewahrt
full_matrix_case_control_evidence() im Fallback ein vom Producer erklärtes
pass, obwohl sein erforderliches pass/403/403/live-Prädikat fehlschlägt. Beide
Collection-Semantics-Classifier verwenden nur den ausgegebenen Status als
All-Pass-Gate. Die aufbewahrte fokussierte Pre-Fix-Unit belegt die Non-Live-
Variante; die benachbarte Wrong-Actual-Status-Variante nimmt denselben Fallback.

Dies ist ein begrenzter CI-Evidence-Integrity-Fehler. Er belegt weder einen
Request-Path-Enforcement-Bypass noch einen externen Hosted-CI-Angreiferpfad,
Source-Ausführung, File-Zugriff oder Secret-Offenlegung.

## Grenze, Verhalten und Auswirkung

Full-Matrix-Summary-JSON überschreitet die Grenze von Connector-CI-Producern
zu einem Evidence-Generator. Ein Control ist nur legitim, wenn sein Producer-
Status pass ist, sein Expected-Status 403 ist, sein Actual- oder Observed-
Status 403 ist und es live lief. Der Helper gibt derzeit bei jedem
fehlgeschlagenen Prädikat den Producer-Status unverändert aus. Die beiden
Downstream-Classification-Funktionen erlauben danach eine reine Evidence- /
Documentation-Only-Reklassifizierung, wenn alle ausgegebenen Status pass sind.

Damit kann veraltete oder fehlerhafte Producer-Evidence ein Non-Live- oder
False-Allow-Control ausreichend erscheinen lassen und die Kritikalität eines
generierten Mismatch-Reports oder sein Merge-Readiness-Signal senken. Die
Evidence belegt nur diese Report-Control-Grenze und beansprucht keine direkte
Produktionsauswirkung.

## Reproduktion und Evidence

Der fokussierte Test
tests.test_report_conditional_remediation.ReportConditionalRemediationTest.test_full_matrix_control_evidence_keeps_fixed_case_and_fallback_contracts
liefert einen HAProxy-Record mit status=pass, expected_status=403,
actual_status=403 und live_executed=false. Er verlangt vom Helper status=fail;
die Baseline gibt stattdessen status=pass aus und endet mit Exit 1.

| Evidence | Ergebnis |
| --- | --- |
| /var/tmp/codex/ModSecurity-conector/runs/ci-b-verified-runtime-mismatch-qgBSMu/pre-fix-control-evidence-negative-test.txt | Aufbewahrter Pre-Fix-Regression-Failure, SHA-256 ef0876d194abe7258f5302263b0efa0a35f40a869cf84d2d00ad5d463427efe9 |
| Command | rtk proxy bash -lc 'PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_report_conditional_remediation.ReportConditionalRemediationTest.test_full_matrix_control_evidence_keeps_fixed_case_and_fallback_contracts' |
| Ergebnis | Exit 1 vor der Reparatur; erwartet fail, beobachtet pass für das Non-Live-Control |

Der gleiche Test enthält den benachbarten Fall status=pass, expected 403,
actual 200, live true. Auch dieser muss nach der Source-Reparatur nicht
erfolgreich sein.

## Remediation und Validierung

Wrapper und vierteiliges Erfolgsprädikat bleiben erhalten. Nur ein Fallback-
Producer-pass wird zu fail normalisiert, wenn das Prädikat nicht erfüllt ist.
Nicht-pass-Status und Evidence-Felder des Producers bleiben erhalten. Direkte
Coverage für die Non-Live- und Wrong-Actual-Pfade wird ergänzt; legitime
Live-403-Apache- und -NGINX-Controls sowie die Äquivalenz von Wrapper und
parametrisiertem Helper bleiben erhalten.

Akzeptanzkriterien:

- Ein pass/403/403/Non-Live-Record ist nicht erfolgreich.
- Ein pass/403/200/Live-Record ist nicht erfolgreich.
- Gültige pass/403/403/Live-Controls bleiben pass.
- Keines der Downstream-Status-only-All-Pass-Gates kann vom fehlgeschlagenen
  Prädikat ein falsches pass erhalten.
- Fokussierte Tests, Syntax-/Diff-Checks, finaler Bypass-Review und
  Exact-Head-Hosted-PR-Checks werden ohne Abschwächung eines Evidence- oder
  Scanner-Controls aufgezeichnet.

## Restrisiko und Historie

Der Record ist fixed, nicht verified oder closed. Die Reparatur wandelt ein
ungültiges Fallback-`pass` zu `fail`; die aufbewahrte Post-Fix-Regression
besteht, das vollständige direkte Testmodul besteht 11 Tests, ausgewählte
Python-Kompilierung und Diff-Hygiene bestehen, und ein vollständiger lokaler
Security-Diff-Scan über zwei Pfade meldet null reportierbare Findings. Draft-
PR #178 steht lokal, remote und auf GitHub exakt auf
`178f0f9b965f75982230ef855fe386474e9a4652`; alle 33 Hosted-Checks bestehen.
SonarQube Cloud meldet Quality Gate `OK`, null offene PR-Issues,
`new_violations=0`, `new_duplicated_lines=0` und
`new_duplicated_lines_density=0.0`. Eine Original-Reproduktion auf dem
resultierenden Master bleibt vor verified oder closed erforderlich. Er ist
kein Release-Blocker; Risikoakzeptanz, Merge, Master-Ergebnis oder Hosted-
Exploit werden nicht beansprucht.

- 2026-07-29T09:02:14Z — fokussierter Pre-Fix-Non-Live-Bypass reproduziert
  und aufbewahrt.
- 2026-07-29T09:02:14Z — enge Parent-CI-Remediation gestartet.
- 2026-07-29T09:26:36Z — lokale Source-Reparatur nach aufbewahrter Post-Fix-
  Control-Regression, 11-Test-Modul, Syntax-/Diff-Checks und vollständigem
  lokalem Security-Diff-Review auf fixed gesetzt; Exact-Head-Hosted-
  Verifikation bleibt ausstehend.
- 2026-07-29T09:48:47Z — Exact-Head-Verifikation von Draft-PR #178
  abgeschlossen: Lokaler, Remote- und GitHub-Head sind
  `178f0f9b965f75982230ef855fe386474e9a4652`; alle 33 Hosted-Checks bestehen,
  und SonarQube Cloud meldet Quality Gate OK, null offene PR-Issues sowie null
  neue Violations/Duplicate Lines. Das Finding bleibt fixed bis zu einem
  separat autorisierten Master-Ergebnis und der Original-Reproduktion.
