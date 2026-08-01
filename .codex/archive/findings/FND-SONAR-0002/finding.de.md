# FND-SONAR-0002 — Framework-SonarQube-Quality-Gate-Fehler ist auf aktuellem Master verifiziert behoben

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-SONAR-0002` |
| Title / Titel | `Framework-SonarQube-Quality-Gate-Fehler ist auf aktuellem Master verifiziert behoben` |
| Category / Kategorie | `sonarqube_finding` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `sonarqube_configuration` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `verified` — aktueller Framework-master `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6` hat eine revisionsgebundene SonarCloud-Analyse mit Quality Gate `OK` und null aktuellen offenen Leak-Period-Issues; die historischen fehlgeschlagenen Master-Beobachtungen bleiben unten erhalten |
| Feasibility | `already_fixed` — die aktuelle externe Gate-Bedingung wurde als bestanden beobachtet; der Record bleibt `verified`, nicht `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

### Aktuelle Audit-Neubewertung — 2026-07-26T12:12:27Z

Der exakte aktuelle Framework-master `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`
hat die SonarCloud-Analyse `2b78d1c9-9a3c-4497-a076-74c468eff0d8`. Ihr Quality
Gate ist `OK`: alle fünf Bedingungen bestehen, neue Duplikation ist `0.0`, und
die aktuelle Leak-Period-Open-Issue-Abfrage liefert null. Dies prüft den
ursprünglichen Master-Gate-Fehler und seine legitimen Controls erneut, ohne eine
kausale Aussage zu intervenierenden Framework- oder MRTS-Änderungen zu treffen.
Dieses Audit führt keine Parent-, Framework- oder MRTS-Source-, Git- oder
Gitlink-Aktion aus.

Direkte GitHub- und SonarQube-Cloud-Evidence bestätigt, dass Framework-master
`9954b99a31fab0006cdf903ab477c8158c50fea8`,
`36cac3029c735dddf9f717b3ce077b9285567a6a`,
`9a729226d2e040d07d7e7a4acebf201faf06ab37`, das PR-#34-Merge-Ergebnis
`3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`, das PR-#30-Merge-Ergebnis
`efdbcbd98afeed0f39f8912ce1140aaa5742f507` und das PR-#35-Merge-Ergebnis
`4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` fehlgeschlagene SonarQube-Cloud-
Quality-Gates haben. Bei dieser historischen PR-#35-Neubewertung scheiterte
Master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` ausschließlich an New
Security Rating E (Actual Value `5`, Threshold `1`); Reliability und
Maintainability sind A (Actual Value `1`), Duplikation ist `0.0` und
Hotspot-Review `100.0`. Alle sechs exakten Master-GitHub-Actions-Workflows
bestanden. Das Live-Sonar-Inventar enthält 14 offene Vulnerability-Signale:
fünf in Framework-eigenen Pfaden und neun unter read-only `tools/MRTS/`. Das
Inventar bestätigt weder ein einzelnes Scanner-Signal als Vulnerability noch
schreibt es den vorbestehenden Multi-File-Backlog PR #35 ursächlich zu. Der
historische Akzeptanz-Scope erstreckt sich nicht auf PRs #30, #33, #34, #35
oder #36.

### Aktuelle Neubewertung nach PR #37

PR-#37-Source `1e9fa0d22639517193d450b05eb7b07193e41257` wurde normal als
aktueller Framework-master `f73f8842f45318e2df8aff1d31855eeb7c20a22f`
gemergt. Alle anwendbaren Master-Actions- und CodeQL-Checks bestanden, aber
SonarCloud scheiterte ausschließlich an New Security Rating C (Actual `3`,
Threshold `1`). Reliability und Maintainability sind A, Duplikation ist `0.0`,
Hotspot-Review ist `100.0`. Das aktuelle Inventar enthält neun offene Signale,
alle unter unverändertem read-only `tools/MRTS/` und vor PR #37 erstellt. Die
statische claim-spezifische Triage findet CLI-/YAML-gesteuerte Datei-/Process-
Sinks, aber keinen etablierten untrusted Framework-Aufruf; deshalb bleiben alle
neun `needs_review`, keine bestätigten Vulnerabilities oder False Positives.
PR #37 änderte den MRTS-Gitlink nicht; seine nur-PR-#36-Risikoakzeptanz ist
historisch. Eine getrennte aktuelle eng begrenzte Akzeptanz gilt nun nur für
die geschützte PR-#42-Integration und ändert den globalen Finding-Lifecycle
nicht.

### Aktuelle Neubewertung nach PR #43

Der exakte Head `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` von PR #43 wurde
normal als Framework-master `f98a8739cb13b583f23d646784b144e596b61441`
gemergt. Die exakte Analyse `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` ist
terminal `ERROR` ausschließlich auf New Security Rating C (Actual `3`,
Threshold `1`) mit neun offenen read-only-MRTS-Vulnerability-Signalen.
Reliability und Maintainability sind A, Duplikation ist `0.0`, Hotspot-Review
ist `100.0`, und die vier anwendbaren Master-Workflows bestanden. Dieselbe
Analyse hat null offene `python:S3415`-Issues. PR #43 wird keine Kausalität
zugeschrieben. Die historische PR-#42-Akzeptanz bleibt unverändert. Am
2026-07-24 akzeptierte der Nutzer dieses dokumentierte master-only-Restrisiko
getrennt nur für die normale exact-head-geschützte Delivery von PR #44; das
globale Finding bleibt blocked.

### Aktuelle Neubewertung nach PR #45

Der exakte Head dd7e221d903a7e2e0a59af203ba312dfca55d69c von PR #45 wurde
normal mit Exact-Head-Schutz als Framework-master
`7e9a560f3acda65510c93f649b6ed4977e4cd6cb` gemergt. Der Merge-Tree
entspricht dem geprüften PR-Head-Tree. CodeQL Actions/C++/Python,
current-revision advisory, common-structure und scaffold-lint bestanden; der
PR-only-Head-Job wurde beim Master-Trigger erwartungsgemäß übersprungen.
SonarCloud Check Run `89757305894` scheiterte ausschließlich an New Security
Rating C (Actual `3`, Threshold `1`). Das aktuelle Leak-Period-Inventar hat
19 offene/bestätigte Records: neun VULNERABILITY-Records unter read-only
`tools/MRTS/` und zehn CODE_SMELL-Records. Die Security-Keys sind dieselben
neun bereits von diesem Finding erfassten Keys. PR #45 ändert keinen
`tools/MRTS/`-Pfad, daher schreibt die Evidence die Bedingung nicht kausal
dieser Delivery zu. Keine aktuelle Nutzer-Risikoakzeptanz deckt PR #45; das
globale Finding bleibt blocked und Release-Blocker.

### Aktuelle Neubewertung am PR-#47-Integrations-Gate

Der exakte Framework-PR-#47-Head `cb0b810e0770a0a4d10fa5bb08031e70ac9ad9a7`
besteht sein getrenntes SonarQube-Cloud-Quality-Gate mit null Bugs,
Vulnerabilities, Code Smells und offenen PR-Issues; alle aktuellen PR-Checks,
einschließlich beider Lint-Trigger, bestehen. Vor einem normalen Merge wurde
der aktuelle Framework-master `c27c644e088904b71b8380d16ee34f1b36f2c001`
erneut geprüft und liefert weiterhin Quality Gate `ERROR` ausschließlich wegen
New Security Rating C (Actual `3`, Threshold `1`); Reliability,
Maintainability, Duplikation und Hotspot-Review bestehen. PR #47 hat keinen
`tools/MRTS`-Gitlink-Diff, daher belegt dies keine PR-Kausalität. Historische
eng begrenzte Akzeptanzen gelten nur für die von ihnen benannten PRs und
autorisieren PR #47 nicht. Der normale Merge wartet deshalb auf eine neue,
ausdrückliche Nutzerentscheidung; weder der Draft-Status noch ein Merge wurde
verändert.

### Aktuelle eng begrenzte Nutzerakzeptanz für PR #47

Nachdem dieses exakte Restrisiko vorgelegt worden war, wies der aktuelle Nutzer
an: „bringe pr 47 in den master“. Dies akzeptiert nur die dokumentierte
master-only-New-Security-Rating-C-Bedingung für einen normalen,
exact-head-geschützten Framework-PR-#47-Merge. Frische PR-Head-Checks,
Sonar-Evidence, Review-/Regel-Prüfung und die normale Merge-Methode bleiben
verpflichtend. Dies autorisiert keine Parent- oder MRTS-Aktion, keinen direkten
Push oder Bypass, keine Suppression, keine Scanner- oder Quality-Gate-Änderung,
keine Finding-Closure und keinen Waiver für spätere PRs/Releases.

### Verifikation nach dem akzeptierten PR-#47-Merge

PR #47 wurde am `2026-07-26T11:26:19Z` normal als
`bcb5b69f135c8b38b834e00e47b0369ae3bdb670` gemergt. Seine Eltern sind die
geprüfte Basis `c27c644…` und der exakte PR-Head `cb0b810…`; der Merge-Tree
entspricht dem geprüften Head-Tree. Alle an diesen Commit gebundenen
Resulting-Master-Workflows bestanden, einschließlich CodeQL, Lint,
CI-Sicherheitschecks, Common Structure, OpenSSF und der read-only
Framework-Validierung des neuen Updaters. SonarCloud band seine Analyse an
diesen exakten Commit und scheiterte ausschließlich an der akzeptierten New-
Security-Rating-C-Bedingung. Dies verbraucht nur die PR-#47-Delivery-Akzeptanz
und schließt das globale Finding nicht.

Nach dieser Verifikation erzeugte der Updater Draft-PR #49. GitHubs
Ereignisprotokoll schreibt dessen spätere Ready-for-Review- und Merge-Events
dem Konto `Easton97-Jens` zu, nicht GitHub Actions oder dieser Sitzung, und
schreibt master damit getrennt auf `ab7374…` fort. Dieser spätere PR liegt
außerhalb des Auftrags und wird hier weder PR #47 zugeschrieben noch validiert.

## Observed behavior / Beobachtetes Verhalten

Die frühere Analyse `2ab6b2fe-32b1-486c-9b1d-bf5a66ee21e3` dokumentierte 361 sichtbare New-Code-Issues, Security E und Reliability D auf der vorherigen Master-Revision. Nach PR #25 scheiterte exakter Master `9954b99a31fab0006cdf903ab477c8158c50fea8` erneut an SonarCloud, während Lint, test-common/common-structure und CodeQL bestanden. Nach dem autorisierten PR-#26-Squash-Merge scheiterte exakter Master `36cac3029c735dddf9f717b3ce077b9285567a6a` erneut mit Security E und Reliability D, während CodeQL, common structure und scaffold lint bestanden. Nach dem normalen Merge von PR #34 scheiterte exakter Master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` erneut, während seine Actions-/CodeQL-Workflows bestanden und sein exakter PR-Head-Quality-Gate bestand. Nachdem PR #30 am `2026-07-20T07:30:40Z` normal gemergt worden war, scheiterte exakter Master `efdbcbd98afeed0f39f8912ce1140aaa5742f507` am SonarQube-Cloud-Check-Run `88295589868` um `2026-07-20T07:31:35Z` ausschließlich an New Security Rating E (Actual `5`); sein New Reliability Rating ist A (Actual `1`). Alle sechs resultierenden GitHub-Actions-Workflows auf Master bestanden.

Nachdem PR #35 am `2026-07-20T11:57:54Z` normal gemergt worden war, gab der
exakte Master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` am
`2026-07-20T12:03:31Z` erneut Quality Gate `ERROR` zurück, ausschließlich weil
`new_security_rating` `5` gegen Threshold `1` betrug. Reliability und
Maintainability waren A, Duplikation war `0.0`, Hotspot-Review war `100.0`,
und alle sechs exakten Master-GitHub-Actions-Workflows bestanden. Das
öffentliche Issue-Inventar meldete 14 offene Sonar-Vulnerability-Signale: fünf
Framework-eigene und neun unter read-only MRTS. Da der vorherige Master bereits
Security E hatte, schreibt diese Evidence den Backlog weder kausal PR #35 zu
noch macht sie Scanner-Signale zu bestätigten Vulnerabilities. Es gab keine
Parent- oder MRTS-Änderung.

Nachdem PR #45 am `2026-07-26T04:53:10Z` normal gemergt worden war, hat der
exakte Framework-master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` einen
Merge-Tree, der seinem geprüften Head
`dd7e221d903a7e2e0a59af203ba312dfca55d69c` entspricht. Anwendbare
resultierende Master-GitHub-Checks bestanden, während SonarCloud ausschließlich
an New Security Rating C (Actual `3`, Threshold `1`) scheiterte. Das öffentliche
Leak-Period-Inventar enthält 19 offene/bestätigte Records: neun VULNERABILITY-
Records unter read-only MRTS und zehn CODE_SMELL-Records. Die neun Security-
Keys entsprechen den bestehenden FND-SONAR-0002-Inputs. Weil PR #45 keinen
`tools/MRTS/`-Pfad ändert, schreibt diese Beobachtung die Bedingung nicht
kausal dem PR zu. Für PR #45 wurde keine spezifische Nutzer-Risikoakzeptanz
angefordert, abgeleitet oder verwendet.

## Expected behavior / Erwartetes Verhalten

Der exakte aktuelle Framework-Head besteht das Quality Gate und die aktuelle
Leak-Period-Abfrage ist leer. Dies erfüllt das Verifikationskriterium für den
historischen Master-Gate-Fehler. Der Record bleibt `verified` statt `closed`,
damit spätere Gate-Regressionen unabhängig neu bewertet werden; historische
begrenzte Akzeptanzen waiven keine künftigen Bedingungen.

## Impact / Auswirkung

Der historische Default-Branch-Gate-Fehler ist kein aktueller P1-Release-
Blocker mehr: Exakter Master `a7ebf5a…` besteht nun mit null aktuellen offenen
Leak-Period-Issues. Dieses Audit schwächt weder Scanner noch Quality Gate,
unterdrückt kein Issue, ändert keine Parent-/Framework-/MRTS-Source oder
Delivery und autorisiert keinen künftigen Release-Waiver.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `tests/runners/synchronized_upstream.py:355`
- `ci/reporting/generate-connector-work-queue.py:486`
- `ci/checks/catalog/no_crs_baseline.py:1746` (`python:S5443`-Signal)
- `ci/reporting/update-runtime-snapshot.py:72` (`pythonsecurity:S8707`- und `pythonsecurity:S2083`-Signale)
- `tests/runners/runner_core.py:636` (`pythonsecurity:S2083`-Signal)
- `tests/runners/case_cli.py:424` (`pythonsecurity:S2083`-Signal)
- `tools/MRTS/mrts/generate-rules.py:428,444`
- `tools/MRTS/mrts/mrts.py:13,14,30,53,73,83`

### Symbols / Symbole

- `Sonar check 87720680094`
- `Security Rating E`
- `Reliability Rating D`
- `Reliability Rating A on efdbcbd98afeed0f39f8912ce1140aaa5742f507`
- `Sonar check 88295589868`
- `Security Rating E on 4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5`
- `14 offene Sonar-Vulnerability-Signale (5 Framework-eigene; 9 MRTS)`
- `Security Rating C auf f73f8842f45318e2df8aff1d31855eeb7c20a22f`
- `Sonar check 89757305894`
- `Security Rating C auf 7e9a560f3acda65510c93f649b6ed4977e4cd6cb`
- `19 aktuelle Leak-Period-Issues (9 VULNERABILITY; 10 CODE_SMELL)`
- Neun aktuelle read-only-MRTS-Issue-Keys `AZ84XDED2YUGB8FZMhlm`,
  `AZ84XDED2YUGB8FZMhln`, `AZ84XDDw2YUGB8FZMhle`, `AZ84XDDw2YUGB8FZMhlb`,
  `AZ84XDDw2YUGB8FZMhlY`, `AZ84XDDw2YUGB8FZMhlc`, `AZ84XDDw2YUGB8FZMhlZ`,
  `AZ84XDDw2YUGB8FZMhld` und `AZ84XDDw2YUGB8FZMhla`
- `analysis 2ab6b2fe-32b1-486c-9b1d-bf5a66ee21e3`
- `python:S5779`
- `python:S3923`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.
- Öffentliche SonarQube-Cloud-API und GitHub-Check-Decoration bleiben für den exakten aktuellen Framework-SHA lesbar.

## Reproduction / Reproduktion

- `sed -n '187,196p;212,215p' .codex/reports/repository-full-assessment.md`
- Aktuelle Exact-Master-Actions, Sonar-Project-Status und Issue-Inventar für
  Framework-master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` abfragen.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:187-196,212-215`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '187,196p;212,215p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run-ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/sonar-quality-gate-current.md`
  - Typ: `current_sonarqube_cloud_gate_inventory`; SHA-256: `659ef53f520c6d62a17d9b5860babdf183cd849baa057c7239d02b636c3bf418`
  - Befehl: `rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-test-Framework&branch=master'`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am: `2026-07-18T09:20:00Z`; Retention: `retained_task_evidence`
- Run-ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/pr-23-current.md`
  - Typ: `pr_new_code_sonar_gate_disposition`; SHA-256: `c28444cfdd989b9884e367f17e0540ccda9858a3bc10b24b26dd8293b500855d`
  - Befehl: schreibgeschützter PR-Check-Rollup und Thread-Inspektion über RTK
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-common-structure`; Exit-Code: `0`
  - Beobachtet am: `2026-07-18T09:58:40Z`; Retention: `retained_task_evidence`
- Run-ID: `20260720T042405Z-framework-pr-34-master-integration-31a1528d`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T042405Z-framework-pr-34-master-integration-31a1528d/evidence/master-postmerge-verification.md`
  - Typ: `exact_framework_master_sonar_failure_after_pr34_merge`; SHA-256:
    `7471054c232a5e2ad26c3327894535ff9d2245e3ec0f37ec60e077a57caea19a`
  - Exakter Master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` scheiterte am
    SonarQube-Cloud-Check mit Reliability D (Actual 4) und Security E
    (Actual 5), während sein exakter PR-#34-Head das getrennte Quality Gate
    bestand.
- Run-ID: `framework-pr-30-master-sonar-20260720T073135Z`
  - Artefakt: GitHub-Check-Runs-API für
    `efdbcbd98afeed0f39f8912ce1140aaa5742f507` und öffentlicher SonarQube-
    Cloud-`project_status`-Endpunkt für Branch `master`; es wurde keine lokale
    Kopie aufbewahrt.
  - Typ: `external_sonarqube_cloud_current_master_gate_reassessment`;
    SHA-256: `not_retained_external_api_readback`
  - Befehl: `rtk proxy gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/efdbcbd98afeed0f39f8912ce1140aaa5742f507/check-runs --paginate`; `rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-test-Framework&branch=master'`
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am: `2026-07-20T07:31:35Z`; Retention:
    `not_retained_external_api_readback`
  - Exakter Master `efdbcbd98afeed0f39f8912ce1140aaa5742f507` scheiterte am
    Check-Run `88295589868` ausschließlich an New Security Rating E (Actual
    `5`); Reliability ist A (Actual `1`), und alle sechs resultierenden
    GitHub-Actions-Workflows auf Master bestanden. Der vorherige PR-#34-Master
    scheiterte bereits mit Security E; daher wird PR #30 keine Kausalität
    zugeschrieben.
- Run-ID: `20260720T113905Z-framework-pr35-36-integration-de98515c`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T113905Z-framework-pr35-36-integration-de98515c/analysis/master-sonar-after-pr35.json`
  - Typ: `exact_framework_master_sonar_reassessment_after_pr35_merge`;
    SHA-256: `7b62f2b918059d816fcfccafcbff16fdd6e1f92d33191862c406d22d414df988`
  - Befehl: GitHub-Exact-Master-Ref-/Workflow-Readback sowie öffentliche
    SonarQube-Cloud-Project-Status- und Issue-Inventar-Endpunkte über RTK.
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am: `2026-07-20T12:03:31Z`; Retention:
    `retained_task_evidence`
  - Exakter Master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` hat Quality Gate
    `ERROR` ausschließlich auf Security E (Actual `5`), während sechs Actions-
    Workflows, Reliability, Maintainability, Duplikation und Hotspot-Review
    bestehen. Das Inventar hat 14 nicht triagierte Vulnerability-Signale (fünf
    Framework-eigene, neun MRTS); es belegt weder einzelne Vulnerability noch
    PR-#35-Kausalität.
- Run-ID: `20260721T060210Z-framework-pr-37-master-integration-6be553a4`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260721T060210Z-framework-pr-37-master-integration-6be553a4/analysis/postmerge-master-sonar-triage.md`
  - Typ: `exact_framework_master_sonar_reassessment_and_read_only_mrts_claim_triage_after_pr37_merge`; SHA-256:
    `a9a312f1ba760030ceb45644ced6b0d533fe01b9a4d2f8e19c1e832dc54b5830`.
  - Exakter Master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` scheiterte
    ausschließlich an Security C (Actual `3`, Threshold `1`), während
    anwendbare Actions-/CodeQL-Checks bestanden. Alle neun aktuellen
    Gate-treibenden Signale sind unveränderte read-only-MRTS-Inputs, stammen
    vor PR #37 und sind nach statischer Source-/Control-/Sink-Triage
    `needs_review`; es gibt keine PR-#37-Kausalität oder Risikoakzeptanz.
- Run-ID: `20260726T050327Z-framework-pr45-master-integration`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T050327Z-framework-pr45-master-integration/evidence/postmerge-master-verification.md`
  - Typ: `framework_pr45_resulting_master_verification_and_sonar_reassessment`;
    SHA-256: `21a8bb0c5cf83ac6ca0156d3285e5829ca1d871754dc9019516844ef9c94695d`
  - Befehl: RTK-GitHub-PR-/Ref-/Tree-/Compare-/Check-Run-Reads sowie
    öffentliche SonarQube-Cloud-Quality-Gate- und Leak-Period-Issue-Inventar-
    Queries nach dem normalen exact-head-geschützten PR-#45-Merge.
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am: `2026-07-26T05:03:27Z`; Retention:
    `sealed_local_evidence`
  - Exakter Master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` hat denselben
    Tree wie geprüfter Head `dd7e221d903a7e2e0a59af203ba312dfca55d69c`.
    Anwendbare Master-Checks bestehen; SonarCloud scheitert ausschließlich an
    Security C (Actual `3`, Threshold `1`). Das aktuelle Inventar hat 19
    offene/bestätigte Records: dieselben neun MRTS-VULNERABILITY-Signale und
    zehn CODE_SMELL-Records. Keine PR-#45-spezifische Risikoakzeptanz wurde
    verwendet.
- Run-ID: `20260726T051835Z-framework-pr45-boundary-snapshot`
  - Artefakt:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T051835Z-framework-pr45-boundary-snapshot/evidence/final-boundary-snapshot.md`
  - Typ: `framework_pr45_final_parent_framework_mrts_boundary_snapshot`;
    SHA-256: `07da9852d035d0be72a3260258d0d05b350d7a1b1e49c5acd7e6f229f39b13d9`
  - Befehl: RTK-schreibgeschützte Parent-/Framework-/MRTS-Status-, Gitlink-,
    Commit-, Diff-Stat-, Pfad- und Mtime-Reads nach dem PR-#45-Merge.
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet am: `2026-07-26T05:18:35Z`; Retention:
    `sealed_local_evidence`
  - Parent-Gitlink sowie eingebettete Framework-/MRTS-Commits wurden vom Task
    nicht geändert. Der Snapshot bewahrt drei nicht zugeordnete dirty MRTS-
    Working-Tree-Pfade; kein Task-Befehl schrieb, restaurierte, stagte,
    commitete, pushte oder schrieb sie jemandem zu.

## Root-cause analysis / Grundursachenanalyse

Das Quality Gate ist ein vorbestehender externer SonarQube-Cloud-Multi-File-
Backlog. Das aktuelle Leak-Period-Inventar hat neun Gate-treibende
VULNERABILITY-Claims unter read-only MRTS und zehn zusätzliche CODE_SMELL-
Records. Die Security-Claims haben CLI-/YAML-abgeleitete Datei-/Process-Sinks,
aber die aktuelle Framework-Evidence belegt keinen untrusted Aufrufer. PR #45
ändert keinen `tools/MRTS/`-Pfad, daher ist kein kausaler Link zu dieser
Delivery belegt.

## Proposed remediation / Vorgeschlagene Remediation

Jedes Gate-treibende Security-/Reliability-Issue mit claim-spezifischer Source-/Control-/Sink-Evidence triagieren, nur separat autorisierte bestätigte Items remediieren und das aktuelle Framework-Gate ohne Suppression, Exclusion oder Quality-Gate-Abschwächung erneut ausführen.

## Acceptance criteria / Akzeptanzkriterien

- The Framework current gate passes or every remaining item has a current authorized disposition.
- Directly sourced issue detail is retained without original MRTS traversal.
- Der common-structure-Patch des aktuellen Tasks bleibt ursächlich von Sonar-Remediation getrennt.

## Validation plan / Validierungsplan

- Den exakten aktuellen SHA verifizieren und das aktuelle Gate-Ergebnis aufbewahren.
- Sichtbare aktuelle Security-/Reliability-Inputs triagieren, bevor Scanner-Signale als bestätigte Vulnerabilities behandelt werden.
- Das Quality Gate auf einem separat autorisierten Remediation-Head erneut ausführen.

## Regression tests / Regressionstests

- Erst nach Auswahl eines validierten einzelnen Sonar-Findings für Remediation eine claim-spezifische Regression ergänzen.

## Legitimate control tests / Legitime Kontrolltests

- Bestehende passierende Maintainability-, Duplikations- und Hotspot-Review-Gate-Bedingungen bei Remediation eines ausgewählten Issues erhalten.

## Dependencies / Abhängigkeiten

- `FND-FRAMEWORK-0001`-common-structure-Reparatur ist getrennt und kann diesen Quality-Gate-Backlog nicht remediieren.

## Blockers / Blocker

- Für diesen historischen Quality-Gate-Fehler ist kein aktueller Blocker
  beobachtet. Künftige nicht-OK-Analysen oder nichtleere Leak-Period-Ergebnisse
  erfordern eine frische Neubewertung; diese Verifikation schließt keine
  unabhängigen MRTS- oder GitHub-Findings.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0001`
- `FND-CROSS-0005`

## Residual risk / Restrisiko

Der beobachtete Passing-Zustand gilt aktuell nur für exakten Master `a7ebf5a…`
und seine gebundene Analyse `2b78d1c9-9a3c-4497-a076-74c468eff0d8`; eine spätere
externe Änderung kann einen Gate-Fehler wieder einführen. Das Audit klassifiziert
historische Scanner-Signale nicht als False Positives und schreibt ihr
Verschwinden keiner bestimmten Änderung zu. Unabhängige offene Findings behalten
ihren eigenen Status und ihre Akzeptanzkriterien.

## History / Historie

- `2026-07-26T12:12:27Z`: current_master_quality_gate_verified — Exakter
  Framework-master `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6` hat gebundene
  SonarCloud-Analyse `2b78d1c9-9a3c-4497-a076-74c468eff0d8` mit Quality Gate
  `OK`, fünf bestandenen Bedingungen, `0.0` neuer Duplikation und null aktuellen
  offenen Leak-Period-Issues. Dies führt das ursprüngliche Master-Gate-Ergebnis
  und legitime Controls erneut aus; deshalb ist das Finding `verified` /
  `already_fixed` und kein Release-Blocker mehr. Das Audit nimmt keine kausale
  Zuschreibung vor und führt keine Parent-, Framework- oder MRTS-Source-, Git-
  oder Gitlink-Aktion aus.

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T09:27:57Z`: current_task_direct_sonar_inventory — Direkte Current-SHA-Gate-/Issue-Evidence wurde aufbewahrt. Das Gate ist unabhängig von common-structure bestätigt; seine Multi-File-Remediation wird nicht in diesen Patch gemischt.
- `2026-07-18T09:58:40Z`: pr_new_code_gate_distinguished — Der exakte Head des Draft-PR #23 bestand SonarCloud mit null neuen Issues/Hotspots. Dies behebt nicht den Default-Branch-E/D-Backlog, belegt aber, dass er den verified-Status des PR nicht blockiert.
- `2026-07-19T09:52:00Z`: current_master_gate_reconfirmed_after_pr25_merge —
  Framework-master `9954b99a31fab0006cdf903ab477c8158c50fea8` hat erneut einen
  fehlgeschlagenen SonarCloud-Code-Analysis-Check, während Lint,
  test-common/common-structure und CodeQL erfolgreich sind. Der SHA-256 der
  zurückgehaltenen Post-Merge-Receipt ist
  `fdda0551354ccc8cb28794a1f7ca8e35f6aa333a9d6272743e15e7e12aacca34`.
  Die Receipt belegt nicht, dass der NGINX-Provenance-Merge den bestehenden
  Multi-File-Backlog verursachte; das Finding bleibt unabhängig `blocked`.
- `2026-07-20T07:31:35Z`: master_sonar_reassessed_after_pr30_merge_scope_not_extended — Exakter Framework-master `efdbcbd98afeed0f39f8912ce1140aaa5742f507` scheiterte am Check-Run `88295589868` ausschließlich an New Security Rating E (Actual `5`); Reliability ist A (Actual `1`). Der exakte PR-#30-Head und alle sechs resultierenden GitHub-Actions-Workflows auf Master bestanden. Der vorherige Master scheiterte bereits mit Security E; die Evidence schreibt PR #30 deshalb keine Kausalität zu und erweitert die historische Akzeptanz nicht.
- `2026-07-20T12:03:31Z`: master_sonar_reassessed_after_pr35_merge_scope_not_extended — Exakter Framework-master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` gab Quality Gate `ERROR` ausschließlich auf New Security Rating E (Actual `5`) zurück; Reliability und Maintainability waren A, Duplikation war `0.0`, Hotspot-Review war `100.0`, und sechs exakte Master-Actions-Workflows bestanden. Das öffentliche Inventar hat 14 nicht triagierte Vulnerability-Signale (fünf Framework-eigene und neun MRTS). Der vorherige Master hatte bereits Security E, daher wird PR #35 keine Kausalität zugeschrieben und die historische Akzeptanz nicht erweitert.
- `2026-07-20T12:50:36Z`: current_user_bounded_risk_acceptance_for_pr36_master_integration — Nachdem das exakte master-only-Sonar-Ergebnis vorgelegt worden war, wies der Nutzer direkt die Integration von PR #36 an. Die aufbewahrte Akzeptanz deckt ausdrücklich nur die geschützte Framework-PR-#36-Integration nach normalem Refresh und frischen Exact-Head-Controls ab; sie waived weder PR-Head-Sonar noch andere Gates, Parent, MRTS, direkten Push/Bypass oder den allgemeinen FND-SONAR-0002-Release-Blocker.
- `2026-07-21T07:28:49Z`: master_sonar_reassessed_after_pr37_merge_and_mrts_inputs_triaged — exakter PR-#37-Source `1e9fa0d…` mergte normal als Master `f73f884…`; Exact-Head-Sonar und resultierende Master-Actions/CodeQL bestanden, aber Master-Sonar scheiterte ausschließlich an Security C. Die neun vorbestehenden unveränderten MRTS-Inputs sind `needs_review`; es gibt keine PR-#37-Kausalität, MRTS-Aktion, Suppression oder aktuelle Risikoakzeptanz.
- `2026-07-23T07:01:16Z`: current_user_bounded_risk_acceptance_for_pr42_master_integration — der aktuelle Nutzer wies ausdrücklich an, `FND-SONAR-0002` bei der Integration von PR #42 außen vor zu lassen. Frische Master-Evidence meldet weiterhin nur Security C (`3` gegen Threshold `1`) und dieselben neun `needs_review`-read-only-MRTS-Signale. Die Akzeptanz gilt nur für geschützte PR-#42-Delivery und waived kein PR-Head-Gate, keine Cloudflare-Disposition, keine Merge-Methoden-Wahl, keine Parent-/MRTS-Aktion, keinen direkten Push/Bypass, keine Control-Änderung, keine künftige Bedingung und keine Finding-Closure.
- `2026-07-23T11:25:34Z`: master_sonar_reassessed_after_pr43_merge_scope_not_extended — Exakter PR-#43-Source `4c55bb2…` mergte normal als Framework-master `f98a873…`. Die exakte Master-Analyse `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` scheiterte ausschließlich an Security C (Actual `3`, Threshold `1`), während die vier anwendbaren Master-Actions-Workflows bestanden. Das Inventar hat neun read-only-MRTS-Vulnerability-Signale und null `python:S3415`-Issues. PR #43 wird keine Kausalität zugeschrieben; die nur-PR-#42-Akzeptanz wird nicht erweitert.
- `2026-07-24T03:56:04Z`: current_user_bounded_risk_acceptance_for_pr44_master_integration — nachdem das exakte aktuelle master-only-Sonar-Ergebnis und der vollständig geprüfte Zustand von Framework-PR #44 vorgelegt wurden, antwortete der Nutzer direkt auf die präzise Akzeptanzfrage mit „ja“. Der frische PR-#44-Head `3b67efb…` bleibt grün ohne Reviews oder Threads; aktueller Master `f98a873…` scheitert weiter ausschließlich an Security C (`3` gegen Threshold `1`), und die öffentliche API meldet neun offene Vulnerability-Signale. Die Akzeptanz erlaubt nur die normale exact-head-geschützte Delivery von PR #44; sie waived keine Controls, Parent-/MRTS-Grenzen, späteren Bedingungen oder Finding-Closure.
- `2026-07-24T04:16:09Z`: protected_pr44_integration_completed_master_sonar_reassessed_under_bounded_acceptance — exakter PR-#44-Head `3b67efb…` mergte normal mit Exact-Head-Schutz als Framework-master `4c975329…`; sein Tree entspricht dem geprüften Head. Resulting-Master-CodeQL-, Advisory-, common-structure- und Lint-Controls bestanden, während SonarCloud ausschließlich an derselben Security-C-(`3` gegen `1`)-Bedingung scheiterte und das Inventar neun `needs_review`-read-only-MRTS-Signale behält. Die eng begrenzte Akzeptanz wurde nur für dieses Ergebnis verwendet; es erfolgten keine Finding-Closure, False-Positive-Claim, Parent- oder MRTS-Aktion.
- `2026-07-26T05:03:27Z`: master_sonar_reassessed_after_pr45_merge_scope_not_extended — exakter PR-#45-Head `dd7e221…` mergte normal mit Exact-Head-Schutz als Framework-master `7e9a560…`; sein Tree entspricht dem geprüften Head. CodeQL, Advisory, common-structure und scaffold-lint bestanden, während SonarCloud Check Run `89757305894` ausschließlich an Security C (`3` gegen `1`) scheiterte. Das aktuelle Leak-Period-Inventar hat 19 offene/bestätigte Records, darunter dieselben neun read-only-MRTS-VULNERABILITY-Signale und zehn CODE_SMELL-Records. PR #45 ändert keinen `tools/MRTS/`-Pfad, daher wird keine Kausalität zugeschrieben. Keine PR-#45-spezifische Risikoakzeptanz wurde angefordert, abgeleitet oder verwendet; es erfolgte keine task-autorisierte Parent-/MRTS-Gitlink- oder Commit-Aktion und das globale Finding bleibt blocked.
- `2026-07-26T05:18:35Z`: final_boundary_snapshot_preserves_unattributed_mrts_worktree_state — ein schreibgeschützter finaler Snapshot bestätigt, dass Parent-recorded Framework-Gitlink, eingebetteter Framework-Commit und MRTS-Commit von diesem Task nicht geändert wurden. Er bewahrt drei nicht zugeordnete dirty MRTS-Working-Tree-Pfade ohne Restore, Staging, Commit, Push, Merge oder Zuschreibung. Dies ändert weder das PR-#45-Merge-Ergebnis noch den FND-SONAR-0002-Lifecycle.

## Risikoakzeptanz nur für die aktuelle PR-Reconciliation

Am `2026-07-19T12:34:25Z` hat der aktuelle Nutzer Codex ausdrücklich
angewiesen, die fehlgeschlagene **Framework-master**-`SonarCloud Code Analysis`
bei der Korrektur von PR #24, #26, #27 und #29 zur Erhaltung der
NGINX-Provenance-Kontrolle zu ignorieren. Das unveränderliche
Akzeptanzartefakt ist
`/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/analysis/sonar-master-risk-acceptance.md`
mit SHA-256
`109222be8968799f2fef2fa59c7172e2cf57cee3077446bc5472261664133679`.

Die getrennte aktuelle Benutzeranweisung zur Integration autorisierte danach
die genannten Framework-PRs für bedingte Exact-Head-PR-Delivery; sie schwächte
diese Akzeptanz nicht ab. Der resultierende Master
`36cac3029c735dddf9f717b3ce077b9285567a6a` wurde im aufbewahrten Receipt
`fnd-sonar-0002-36cac-master-reassessment.md`, SHA-256
`e548fde741694abca18528f4836f68f1dfcd52e76d2dd45f2b8500ec68829ddf`, erneut
bewertet.

Damit ist ausschließlich das Restrisiko akzeptiert, dass der bekannte
Default-Branch-Security-/Reliability-Backlog auf den resultierenden Mastern
dieser einen sequenziellen Reconciliation echte, noch ungelöste Defekte
enthalten könnte. Nicht akzeptiert, unterdrückt oder umgangen werden ein
SonarCloud-Ergebnis für einen neuen exakten PR-Head, jede andere CI-, Review-,
Security-, Dokumentations-, Konflikt- oder Exact-Head-Anforderung, ein direkter
Master-Push, Parent-Gitlink-Delivery oder eine MRTS-Änderung. Die Disposition
ist neu zu bewerten, wenn sich die Bedeutung des Master-Gates oder der
angeforderte Umfang ändert. Eine separat autorisierte Sonar-Triage/-Remediation
bleibt erforderlich.

## Re-Evaluierung nach PR #26

- `2026-07-19T14:46:13Z`: Exakter Framework-master
  `36cac3029c735dddf9f717b3ce077b9285567a6a` scheiterte am SonarCloud-
  Check-Run `88203518811` mit Security E und Reliability D, während CodeQL,
  common-structure und scaffold-lint bestanden.
- Der aktuelle Framework-only-sequenzielle Scope behält nur dieses master-only
  Restrisiko. Frische PR-Head-Sonar-Gates und jedes andere Control bleiben
  verpflichtend.

## Re-Evaluierung nach PR #33

- `2026-07-19T22:18:45Z`: Exakter Framework-master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` hat einen abgeschlossenen
  fehlgeschlagenen SonarCloud-Code-Analysis-Check. Das öffentliche Quality Gate
  meldet New Reliability D (Actual `4`) und New Security E (Actual `5`),
  während neue Duplikation `0.4` und Hotspot-Review `100.0` betragen.
- Der exakte PR-#33-Head bestand sein getrenntes SonarQube-Cloud-Quality-Gate,
  und die resultierenden Master-Actions-/CodeQL-Controls bestanden. Der
  Master-Backlog wird nicht der Python-3.13-Reparatur zugeschrieben.
- Die aufbewahrte Akzeptanz ist ausdrücklich auf PR #24, #26, #27 und #29
  begrenzt. Sie wird nicht automatisch auf PR #33 erweitert; kein Source-,
  Scanner-, Quality-Gate-, Parent- oder MRTS-Control wurde abgeschwächt.

## Re-Evaluierung nach PR #34

- `2026-07-20T04:52:04Z`: Exakter Framework-master
  `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` scheiterte erneut an SonarQube
  Cloud. Das öffentliche Gate meldet New Reliability D (Actual `4`) und New
  Security E (Actual `5`), während neue Duplikation `0.4` und Hotspot-Review
  `100.0` betragen.
- Der exakte PR-#34-Head bestand sein getrenntes Quality Gate, und die
  resultierenden Master-Actions-/CodeQL-Controls bestanden. Der Master-Backlog
  wird nicht der Phase-4-Workload-Identity-Remediation zugeschrieben.
- Die gespeicherte Benutzerakzeptanz benennt nur PR #24, #26, #27 und #29.
  Sie wird nicht automatisch auf PR #34 erweitert; deshalb ist dieses Finding
  für die aktuelle Master-Integration ohne neue Benutzerentscheidung oder
  separat autorisierte SonarQube-Cloud-Remediation `blocked`.

## Re-Evaluierung nach PR #30

- `2026-07-20T07:31:35Z`: Nachdem PR #30 am `2026-07-20T07:30:40Z` normal
  gemergt worden war, scheiterte exakter Framework-master
  `efdbcbd98afeed0f39f8912ce1140aaa5742f507` am SonarQube-Cloud-Check-Run
  `88295589868` ausschließlich an New Security Rating E (Actual `5`). New
  Reliability Rating ist A (Actual `1`); Duplikations- und Hotspot-Review-
  Bedingungen bestehen.
- Der exakte PR-#30-Head bestand sein getrenntes Quality Gate, und alle sechs
  resultierenden GitHub-Actions-Workflows auf Master bestanden. Der unmittelbar
  vorherige PR-#34-Master hatte bereits Security E, daher belegt diese
  Beobachtung keine Kausalität zu PR #30. Es gab keine Parent- oder MRTS-
  Änderung.
- Die gespeicherte Benutzerakzeptanz bleibt auf PR #24, #26, #27 und #29
  begrenzt. Sie wird nicht automatisch auf PR #30 erweitert; deshalb bleibt
  dieses Finding für die aktuelle PR-#30-Master-Integrationsverifikation ohne
  neue Benutzerentscheidung oder separat autorisierte SonarQube-Cloud-
  Remediation `blocked`.

## Re-Evaluierung nach PR #35

- `2026-07-20T12:03:31Z`: Nachdem PR #35 am `2026-07-20T11:57:54Z` normal
  gemergt worden war, gab exakter Framework-master
  `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` SonarQube-Cloud-Quality-Gate
  `ERROR` ausschließlich auf New Security Rating E (Actual `5`, Threshold `1`)
  zurück. Reliability und Maintainability waren A, Duplikation war `0.0`, und
  Hotspot-Review war `100.0`.
- Alle sechs exakten Master-GitHub-Actions-Workflows bestanden. Das öffentliche
  Inventar hat 14 nicht triagierte Vulnerability-Signale: fünf in Framework-
  eigenen Pfaden und neun unter read-only MRTS. Dies bestätigt weder eine
  einzelne Vulnerability noch, dass PR #35 den bestehenden Master-Backlog
  verursachte.
- Die gespeicherte Benutzerakzeptanz bleibt auf PR #24, #26, #27 und #29
  begrenzt. Sie wird nicht automatisch auf PR #35 oder den aktuellen PR #36
  erweitert. PR #36 muss ungemergt bleiben, bis der Nutzer eine neue exakte
  Risikoentscheidung trifft oder eine abgegrenzte Remediation separat autorisiert.

## Aktuelle eng begrenzte Nutzerakzeptanz für PR #36

- `2026-07-20T12:50:36Z`: Nachdem das aktuelle exakte master-only-Sonar-
  Ergebnis vorgelegt worden war, wies der Nutzer direkt die Integration von
  Framework PR #36 an. Das aufbewahrte Akzeptanzartefakt ist
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T113905Z-framework-pr35-36-integration-de98515c/analysis/pr36-master-sonar-risk-acceptance.md`,
  SHA-256 `5e280a0b832b7ecef6109f297602c137fe3fdb3b2687252163a0b774769fb162`.
- Sie autorisiert bedingt nur den aktuellen Framework PR #36 nach einem
  normalen nicht umschreibenden Refresh von Master
  `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` sowie frischer Exact-Head-CI-,
  Sonar-, Review-, Konflikt-, Dokumentations- und Security-Evidence. Sein Merge
  muss durch Exact-Head-Verifikation geschützt bleiben.
- Sie akzeptiert nur das dokumentierte master-only-Security-E-Gate und das
  nicht triagierte 14-Signal-Inventar. Sie schließt dieses Finding nicht,
  klassifiziert Scanner-Signale nicht als False Positives, waived kein frisches
  PR-Head-Gate oder anderes Control, autorisiert keine Parent- oder MRTS-Arbeit
  und erstreckt sich nicht auf andere PRs, künftige Master-Zustände oder Releases.

## Re-Evaluierung nach PR #36

- `2026-07-20T13:06:39Z`: Der exakte Head der Framework-PR #36
  `1608352912a755f0f8639eddfa2350436446067e` wurde normal und mit
  Exact-Head-Schutz als Master `784977615acfc55567e37b863309abc4a38ac877`
  gemergt. PR-Head-Actions, CodeQL, SonarQube-Cloud-Quality-Gate,
  Dokumentations-, Review-, Konflikt- und Security-Evidence bestanden vor dem
  Merge. Parent und MRTS blieben unverändert.
- Der resultierende Master bestand CodeQL Actions/Python/C++, Lint,
  test-common und OpenSSF. Seine SonarCloud Code Analysis scheiterte
  ausschließlich an New Security Rating E (Actual `5`, Threshold `1`);
  Reliability und Maintainability waren A, Duplikation `0.0` und Hotspot-Review
  `100.0`. Der Nicht-PR-Job `pull-request-head` wurde erwartungsgemäß
  übersprungen.
- Der unmittelbar vorherige Master
  `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` hatte bereits dieselbe
  Security-E-Bedingung. Das aufbewahrte Artefakt
  `analysis/master-sonar-after-pr36.json`, SHA-256
  `5ba2c4ea093419fcf6b1b066c85dd37b7d2a08b29ee23525119e641d2e0093ef`,
  schreibt PR #36 daher keine Kausalität zu. Es dokumentiert die Verwendung der
  eng begrenzten aktuellen Nutzerakzeptanz nur für diese geschützte Delivery;
  das globale P1-Finding bleibt `blocked` und erfordert getrennte Issue-Triage
  oder ein bestandenes Master-Quality-Gate.

## Re-Evaluierung nach PR #38

- `2026-07-20T18:05:00Z`: Der exakte Head von PR #38 bestand sein getrenntes
  SonarQube-Cloud-Quality-Gate mit null neuen Issues und null Security
  Hotspots. Der resultierende Framework-master
  `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b` scheiterte dennoch im Check-Run
  `88432322185` ausschließlich an Security Rating on New Code E; die
  resultierenden Master-Actions und CodeQL bestanden.
- Der unmittelbare Vorgänger `784977615acfc55567e37b863309abc4a38ac877` hatte
  bereits denselben master-only-Fehler. Der Action-Pin-Reparatur wird keine
  Kausalität zugeschrieben. Die frühere eng begrenzte Risikoakzeptanz gilt nur
  für PR #36 und wird nicht auf PR #38 oder spätere Integrationen erweitert.

## Re-Evaluierung nach PR #37

- `2026-07-21T07:28:49Z`: Der normale Exact-Head-geschützte Merge des
  PR-#37-Source-Heads `1e9fa0d22639517193d450b05eb7b07193e41257` erzeugte den
  aktuellen Framework-master `f73f8842f45318e2df8aff1d31855eeb7c20a22f`. Der
  PR-Head bestand sein getrenntes SonarQube-Cloud-Quality-Gate; alle
  anwendbaren resultierenden Master-Actions und CodeQL-Checks bestanden.
- Resulting-Master-SonarCloud scheiterte ausschließlich an New Security Rating
  C (Actual `3`, Threshold `1`). Die neun offenen Gate-treibenden Inputs sind
  unveränderte read-only-MRTS-Records, die vor PR #37 erstellt wurden. Die
  statische Source-/Control-/Sink-Triage klassifiziert alle neun als
  `needs_review`: CLI-/YAML-gesteuerte Datei-/Process-Sinks existieren, aber
  kein aktueller untrusted Framework-Aufruf ist etabliert.
- Das aufbewahrte Post-Merge-Artefakt ist
  `analysis/postmerge-master-sonar-triage.md`, SHA-256
  `a9a312f1ba760030ceb45644ced6b0d533fe01b9a4d2f8e19c1e832dc54b5830`.
  Die historische nur-PR-#36-Akzeptanz wird nicht erweitert; FND-SONAR-0002
  bleibt ohne MRTS-Aktion, Scanner-/Gate-Änderung oder neue Risikoentscheidung
  `blocked`.

## Aktuelle eng begrenzte Nutzerakzeptanz für PR #42

- `2026-07-23T07:01:16Z`: Der Nutzer wies ausdrücklich an: “kannst den
  FND-SONAR-0002 ausen vor lassen und den pr 42 in den master übernehmen”.
  Das aufbewahrte payload-sichere Akzeptanz-Receipt ist
  `/var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/fnd-sonar-0002-pr42-risk-acceptance.md`,
  SHA-256 `5f087611098d039da1c73f128bc442efecf24f25df9f145fcef2a97ec6107642`.
- Sie akzeptiert nur den aktuellen Framework-master
  `f73f8842f45318e2df8aff1d31855eeb7c20a22f`, dessen master-only-SonarQube-
  Cloud-Quality-Gate ausschließlich an Security C (Actual `3`, Threshold `1`)
  scheitert, mit neun vorbestehenden read-only-MRTS-Signalen, die `needs_review`
  bleiben und in einem anderen Trust-Kontext real sein können.
- Die Akzeptanz gilt nur für die normale geschützte Framework-PR-#42-
  Integration nach frischer Exact-Head-Verifikation. Sie waived weder
  PR-Head-Sonar, Actions, CodeQL, Reviews, Dokumentation, Security,
  `FND-GITHUB-0007`-Cloudflare, die Merge-Methoden-Wahl, Resulting-Master-
  Validierung, Parent-/MRTS-Grenzen, Direct-Push-/Bypass-Verbote,
  Scanner-/Gate-Controls, künftige Bedingungen noch Finding-Closure. Das
  globale Finding bleibt `blocked` und `release_blocker`.

## Resulting-Master-Verifikation nach PR #42

- 2026-07-23T07:51:09Z: Der exakte PR-#42-Head
  dc6cf411e78b3f37f1e4be52edef59894560b1ae wurde normal mit
  Exact-Head-Schutz als Framework-master
  935cf14c676a24672be5c336e92cd13457cc35c8 gemergt. Sein Tree entspricht
  dem geprüften PR-Head; acht exakte Master-GitHub-Actions-Workflows endeten
  erfolgreich.
- SonarQube-Cloud-Analyse dda3ea04-2721-4ee6-a9c1-74bd2925f139 ist an die
  exakte resultierende Revision gebunden. Ihr Quality Gate ist terminal ERROR
  ausschließlich auf New Security Rating C (Actual 3, Threshold 1);
  Reliability und Maintainability sind A, Duplikation ist 0.0 und
  Hotspot-Review ist 100.0. Das ist dieselbe dokumentierte Restbedingung,
  die nur für diese abgeschlossene PR-#42-Delivery akzeptiert wurde, keine
  False-Positive-Disposition oder Closure.
- Zurückgehaltenes Post-Merge-Receipt:
  /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md,
  SHA-256 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
  Parent, sein Framework-Gitlink und MRTS blieben unverändert. Das globale
  P1-Finding bleibt für jeden anderen Scope blocked und Release-Blocker.

## Aktuelle eng begrenzte Nutzerakzeptanz für PR #44

- `2026-07-24T03:51:41Z`: Nachdem das präzise aktuelle master-only-Restrisiko
  und der normale Merge-Scope vorgelegt wurden, antwortete der Nutzer mit
  „ja“. In diesem direkten Gesprächskontext akzeptiert dies ausschließlich die
  normale exact-head-geschützte Delivery von Framework-PR #44.
- Das aufbewahrte Akzeptanz-Receipt ist
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a/evidence/pr44-master-sonar-risk-acceptance-retained.md`,
  SHA-256 `bd07be75f13798ab168cfb6994961c453a035b9781ab657cb72a69d0b1302819`.
- Frische Final-Pre-Merge-Evidence um `2026-07-24T03:56:04Z` dokumentiert
  exakten PR-#44-Head `3b67efb8534fb56a93f085897417ada449ff1a39`, ein
  bestandenes PR-Quality-Gate und grüne anwendbare Checks, keine
  Reviews/Threads sowie aktuellen Master
  `f98a8739cb13b583f23d646784b144e596b61441`, der weiter nur an Security C
  (Actual `3`, Threshold `1`) scheitert. Die öffentliche Issue-API meldet neun
  offene Vulnerability-Signale; sie bleiben `needs_review`, keine False
  Positives.
- Das aufbewahrte Pre-Merge-Receipt ist
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a/evidence/pr44-final-premerge-readback.md`,
  SHA-256 `d677a3638802a06251d91b3d1d2f00634bd34814baf041eb1c472619d9efaf2c`.
- GitHub mergte den exakten geprüften Head am `2026-07-24T04:11:49Z` normal
  mit `--match-head-commit` als Framework-master
  `4c9753291d26d92f2d7e51ae425dedb79666fd5e`; sein Tree entspricht dem
  geprüften Head. Resulting-Master-CodeQL actions/C++/Python,
  current-revision advisory, common-structure und scaffold-lint bestanden; der
  PR-only-Head-Job war absichtlich übersprungen. SonarCloud scheiterte nur an
  derselben Security-C-Bedingung (`3` gegen `1`) mit neun `needs_review`-
  read-only-MRTS-Signalen.
- Aufbewahrtes Resulting-Master-Receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a/evidence/pr44-resulting-master-verification.md`,
  SHA-256 `71228129d8b0a24706a35219fb568679ef7be0e7a47a615cb7f5abcc167c1f3f`.
- Dies waived weder PR-Head-CI/Sonar/Review/Dokumentation/Security-Controls,
  Exact-Head-Schutz, Post-Merge-Validierung, Parent-/MRTS-Grenzen,
  Direct-Push-/Bypass-Verbote, Scanner-/Gate-Änderungen, künftige Heads/
  Master-Bedingungen noch Finding-Closure. Das globale Finding bleibt
  `blocked` und `release_blocker`.

## Resulting-Master-Verifikation nach PR #43

- `2026-07-23T11:24:30Z`: GitHub mergte den exakten PR-#43-Head
  `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` normal mit Exact-Head-Schutz als
  Framework-master `f98a8739cb13b583f23d646784b144e596b61441`.
- Die exakte Master-Analyse `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` ist an
  diese Revision gebunden. Sie ist ausschließlich wegen New Security Rating C
  (Actual `3`, Threshold `1`) `ERROR`; Reliability und Maintainability sind A,
  Duplikation ist `0.0`, Hotspot-Review ist `100.0`, und das Inventar hat neun
  read-only-MRTS-Vulnerability-Signale. `test-common`, OpenSSF Scorecard, lint
  und CodeQL analysis schlossen erfolgreich ab; der PR-only-Head-Job war beim
  Nicht-PR-Trigger übersprungen.
- Dieselbe Analyse hat null offene `python:S3415`-Issues, daher ist die
  Quality-Gate-Bedingung unabhängig von der Assertion-Order-Remediation von
  PR #43. Die nur-PR-#42-Risikoakzeptanz schließt künftige PRs und
  Master-Bedingungen ausdrücklich aus; sie deckt #43 oder `f98a873…` nicht ab.
  Es erfolgten keine Parent- oder MRTS-Aktion, Scanner-/Gate-Änderung,
  Suppression, False-Positive-Disposition oder Finding-Closure. Das Finding
  bleibt global `blocked` und P1-Release-Blocker, bis ein Passing Gate,
  separat autorisierte externe Remediation oder eine aktuelle exakte
  Nutzer-Risikoentscheidung vorliegt.
- Aufbewahrtes Receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-postmerge-master-verification.md`,
  SHA-256 `d8a63662d10def3118b5795c90474a0c63ab9a96a82d5e93debb8436c79bd79c`.
