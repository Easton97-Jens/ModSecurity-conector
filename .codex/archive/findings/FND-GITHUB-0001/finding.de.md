# FND-GITHUB-0001 — GitHub-Scorecard-Governance-Baseline hat unvollständige Controls und Folge-Evidence

## Identity / Identität

| Feld / Field | Wert / Value |
| --- | --- |
| ID | `FND-GITHUB-0001` |
| Titel / Title | `GitHub-Scorecard-Governance-Baseline hat unvollständige Controls und Folge-Evidence` |
| Kategorie / Category | `github_governance` |
| Repository / Repository | `github` |
| Ownership / Ownership | `github_configuration` |
| Priorität / Priority | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `closed` |
| Release-Blocker / Release blocker | `false` |
| Security-Relevanz / Security relevance | `true` |

## Zusammenfassung / Summary

Live-GitHub-Evidence deckt alle angefragten Scorecard-/Governance-Bereiche ab. Actions verwendet jetzt default `read`, `master` hat no-bypass Ruleset `19138299` und Repository-Vulnerability-Alerts sind aktiviert. Der exakte Head `57c411eeca7be024e5718d560e26e4bc051b92ae` von Draft-PR [#120](https://github.com/Easton97-Jens/ModSecurity-conector/pull/120) liefert Quellremediation für FuzzingID #11 und VulnerabilitiesID #12; alle 33 anwendbaren terminalen Hosted-Checks bestanden gegen seine damals aktuelle Basis. Master rückte danach nicht überlappend auf `9e788057d2b551ba51ad7c4e6e1d8c5198b77834` vor, daher meldet GitHub den Draft-PR als `BEHIND` und er muss vor Review/Merge normal aktualisiert und erneut validiert werden. Die aktuellen Master-Alerts bleiben offen; die übrigen Governance-, Review-, Alters- und CII-Anforderungen behalten ihre tatsächlichen externen Blocker und Evidence.

## Beobachtetes Verhalten / Observed behavior

Vor der Remediation hatte `master` kein sichtbares/effektives Ruleset und keine klassische Protection, Actions verwendete default `write` und Vulnerability Alerts waren endpoint-bestätigt deaktiviert. Die derzeit sichtbaren Scorecard Alerts stammen vom `2026-07-16`, also vor dieser Remediation; bis GitHub eine spätere Analyse veröffentlicht, wird keine Score-Änderung behauptet.

## Erwartetes Verhalten / Expected behavior

`master` akzeptiert Änderungen nur über no-bypass Pull Requests mit gelösten Konversationen, strikten Checks für den aktuellen Head, ohne Force Push und ohne Löschung. Eine gemergte Richtlinie bietet einen vertraulichen Meldeweg; eine Human Approval wird erst nach Verfügbarkeit eines unabhängigen Reviewers konfiguriert.

## Auswirkung / Impact

Ungeschützte Branches und breite Workflow-Defaults können Governance-Grenzen umgehen. Fehlende Disclosure-, Dependency-, SAST- und Fuzzing-Entscheidungen begrenzen Assurance. Scanner-/Advisory-Leads werden ohne Repository-Beweis nicht als bestätigte Runtime-Schwachstellen dargestellt.

## Disposition der Governance-Punkte / Governance-point disposition

| Finding | Initial state | Action | Final state | Evidence | Remaining risk |
| --- | --- | --- | --- | --- | --- |
| Branch-Protection | `nicht konfiguriert` | Ruleset `19138299` erstellt: deletion, non-fast-forward, pull request, gelöste Konversationen, strikte Checks, kein Bypass. | `bereits korrekt` / `verified` | `current_user_can_bypass: never`; `master.protected: true`; PR #53 `d5781bd` ist `CLEAN`, alle sechs exakten Checks sind erfolgreich, null Review-Threads. | Unabhängige Human Review bleibt separat offen; Check-Stabilität muss überwacht werden. |
| Code-Review | `nicht konfiguriert` | Aussperrungsanalyse dokumentiert; keine Approval-Anzahl und kein Bypass. | `muss geändert werden` / `blocked` | Einziger direkter Collaborator ist Owner/Admin; kein Team; PR #51 ohne Review. | Keine unabhängige Approval bis ein Reviewer existiert. |
| Security-Policy | `nicht konfiguriert` | Bilinguale Richtlinie und Change Record erstellt; PR #53 wurde autorisiert, per Squash gemergt und auf master verifiziert. | `bereits korrekt` / `verified` | PR #53 `d5781bd` bestand alle sechs exakten Checks ohne Bypass und wurde als `a589cb6` gemergt; sein Master-Tree entspricht dem geprüften Head und alle 14 beobachteten Master-Workflows bestanden. GitHub liefert `securityPolicyUrl` `https://github.com/Easton97-Jens/ModSecurity-conector/security/policy`; Private Reporting ist `enabled=true`. | Dieser verifizierte Punkt beseitigt nicht die separaten Lücken bei unabhängiger Review, CII, Dependencies, SAST oder Fuzzing; URL nach späteren Repository-Änderungen erneut prüfen. |
| Maintained | `nicht anwendbar` | Keine künstliche Aktivität oder Setting-Änderung. | `nicht anwendbar` / `not_applicable` | Scorecard-Grund ist Repository-Alter unter 90 Tagen. | Nach `2026-08-12` erneut prüfen. |
| CI-Best-Practices | `muss geändert werden` | Actions-Default `write` auf `read` geändert; explizite Scheduled-Writer-Permissions warten auf getrennten Nachweis. | `muss geändert werden` / `in_progress` | API-Post-Readback ist `read`; CII Alert ist fehlendes externes Badge. | CII- und Token-Permissions-Arbeit bleiben abgegrenzte Entscheidungen. |
| SAST | `muss geändert werden` | Reale partielle CodeQL- und actionlint/zizmor-Coverage festgestellt; kein Platzhalter. | `muss geändert werden` / `triaged` | Vier CodeQL- und zwei Workflow-Lint-Checks sind stabil; der sichtbare Scorecard Alert meldet Score 8 und 5/12 historische Commits. | Voller Connector-C/C++-Scope benötigt getrennte Machbarkeit. |
| Fuzzing | `nicht konfiguriert` | Echten C/libFuzzer-Common-HTTP-Header-Parser-Target, begrenzten Runner, Make-Target und die Invocation im bestehenden CodeQL-Job in Draft-PR #120 geliefert; kein Detektor-Marker und keine Unterdrückung. | `verified_draft_pr_behind_current_master_requires_update_and_revalidation` / `in_progress` | Exakter Head `57c411eeca7be024e5718d560e26e4bc051b92ae` bestand 33 anwendbare terminale Hosted-Checks; CodeQL-bounded-c-cpp-Job `89542295414` führte den Fuzzer erfolgreich aus. Der aktuelle Master rückte danach nicht überlappend vor, und GitHub meldet den PR als `BEHIND`. | Ein getrennt autorisiertes normales Branch-Update, frische Exact-Head-Checks, unabhängige Review, Merge und eine Scorecard-Analyse des resultierenden Default-Branches sind nötig, bevor Alert #11 neu bewertet werden kann. |
| Vulnerabilities | `muss geändert werden` | Exakten sicheren Development-Pin `PyYAML==6.0.3` in Draft-PR #120 geliefert, ausgerichtet auf den bestehenden CI-Hash-Lock; kein OSV-Ignore und keine Unterdrückung. | `verified_draft_pr_behind_current_master_requires_update_and_revalidation` / `in_progress` | Der exakte Head bestand OSV und SonarCloud zusammen mit allen anderen anwendbaren Checks; der Pin verhindert, dass der Parser `>=6,<7` als Literalversion `6,<7` behandelt. Der aktuelle Master rückte danach nicht überlappend vor, und GitHub meldet den PR als `BEHIND`. | Ein getrennt autorisiertes normales Branch-Update, frische Exact-Head-Checks, unabhängige Review, Merge und eine Scorecard-Analyse des resultierenden Default-Branches sind nötig, bevor Alert #12 neu bewertet werden kann. |

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `SECURITY.md`, `SECURITY.de.md`
- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/dependabot.yml`
- `connectors/envoy/ext_proc/go.mod`
- `fuzz/common_http_headers_fuzz.c`
- `ci/checks/common/check-common-http-header-fuzz.sh`
- `Makefile`, `requirements-dev.txt`, `tests/test_ci_security_workflows.py`

### Symbole / Symbols

- `GitHub ruleset 19138299 Protect master`
- `GitHub Actions default workflow permissions`
- `GitHub vulnerability alerts`
- `GitHub Dependency Graph SBOM`
- `Scorecard alerts #1, #7-#13`
- `Dependabot alert #1`
- `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, `zizmor`
- `LLVMFuzzerTestOneInput`, `msconnector_headers_parse_content_length`, `PyYAML==6.0.3`

## Voraussetzungen / Preconditions

- GitHub-Administration und stabile sechs Check-Contexts bleiben verfügbar.
- Ein unabhängiger Reviewer wird hinzugefügt, bevor eine Approval-Anzahl erzwungen wird.
- Dieses Finding autorisiert keine Produkt-, Framework- oder MRTS-Änderung.

## Reproduktion / Reproduction

- `gh api repos/Easton97-Jens/ModSecurity-conector/rulesets/19138299`
- `gh api repos/Easton97-Jens/ModSecurity-conector/rules/branches/master`
- `gh api repos/Easton97-Jens/ModSecurity-conector/actions/permissions/workflow`
- `gh api repos/Easton97-Jens/ModSecurity-conector/vulnerability-alerts --include`
- `gh api repos/Easton97-Jens/ModSecurity-conector/code-scanning/alerts?tool_name=Scorecard&state=open`

## Evidence / Evidence

- Run ID: `20260718T081034Z-github-scorecard-governance`
  - Artifact: `.codex/runs/20260718T081034Z-github-scorecard-governance.json`
  - Type: `sanitized_github_governance_receipt_and_static_triage`; SHA-256: `3822662f25f4517cbb4ebe668ffd55941edcf827dbc7b4b0ee46f0531b8805ce`
  - Command: `gh api governance and security endpoints; static Dependabot-alert triage`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-18T09:21:20Z`; retention: `retained_local_receipt`

## Grundursachenanalyse / Root-cause analysis

Dem Repository fehlten vollständige Branch-/Governance-Konfiguration, eine auffindbare Richtlinie und evidenzbasierte Entscheidungen für jede Scorecard-Heuristik. Solo-Ownership macht eine verpflichtende Approval ohne Reviewer oder Bypass unsicher.

## Vorgeschlagene Remediation / Proposed remediation

Das verifizierte Ruleset `19138299` und die von GitHub erkannte Sicherheitsrichtlinie beibehalten, vor `required_approving_review_count` eins einen unabhängigen Reviewer hinzufügen und CII, Dependency-Remediation, erweiterte SAST und Fuzzing als getrennte evidenzbasierte Arbeit behandeln.

## Akzeptanzkriterien / Acceptance criteria

- Ruleset `19138299` beweist per Readback die beabsichtigten Controls auf `master`.
- PR #53 bei `d5781bd15cd286608168b952dfeb7f2d7ab29772` zeigte sechs exakte Required Checks ohne Bypass, und sein autorisierter Squash-Merge erzeugte master `a589cb662fb03deb764f78eefbb1056bc64d63e2`.
- Ein Reviewer existiert, bevor eine Human Approval erzwungen wird.
- `SECURITY.md` und `SECURITY.de.md` sind über den reviewed PR #53 gemergt; GitHub GraphQL liefert `https://github.com/Easton97-Jens/ModSecurity-conector/security/policy` als `securityPolicyUrl`, und Private Vulnerability Reporting ist aktiviert.
- Jede Tabellenzeile behält Evidence, Validierung und Restrisiko.

## Validierungsplan / Validation plan

- Ruleset, effektive Regeln, Actions-Permission, Alerts, master und GitHub-`securityPolicyUrl` nach relevanten Änderungen erneut lesen.
- Exakte Check-Contexts und Mergeability ohne Merge oder Bypass beobachten.
- Abgegrenzte Bilingual-/Link- und Diff-Checks für die Richtlinie ausführen, die Framework-Gitlink-Limitierung festhalten und den resultierenden Master-Inhalt verifizieren.
- Scorecard erst nach einer späteren GitHub-Analyse erneut ausführen.
- Vor SAST-Erweiterung oder Fuzzing getrennte Machbarkeits-Evidence verlangen.

## Regressionstests / Regression tests

- Ruleset- und Effective-Rules-API-Readback für `master`.
- Required-Check-Beobachtung auf einem realen Same-Repository-PR.
- Zielgerichtete Bilingual-/Link-Kontrolle für Richtlinien- und Change-Record-Paare.

## Legitime Kontrolltests / Legitimate control tests

- Ein sauberer PR-Head erfüllt sechs Required Checks ohne Bypass.
- GitHub akzeptiert einen privaten Vulnerability Report ohne öffentliche Offenlegung.
- Dependabot-Alert-Inventar bleibt nach Aktivierung erreichbar.

## Abhängigkeiten / Dependencies

- Unabhängiger Reviewer, stabiles SonarCloud-Ergebnis und die externe CII-Best-Practices-Registrierungs-/Attestierungsentscheidung.
- Unabhängige Review und Merge von Draft-PR #120, danach eine frische Default-Branch-Scorecard-Analyse für #11 und #12.

## Blocker / Blockers

- Eine verpflichtende Approval würde den einzigen Owner/Admin ohne verbotenen automatischen Bypass aussperren.
- CII-Registrierung erfordert externe Owner-Attestation.
- Full-Tree-Dokumentations-Checks können den nicht populierten Framework-Gitlink im temporären Clone nicht auflösen.
- Scorecard #11 und #12 sind auf Master `9e788057d2b551ba51ad7c4e6e1d8c5198b77834` weiter offen; Draft-PR #120 ist jetzt `BEHIND` und muss normal aktualisiert sowie erneut validiert werden, bevor er über einen späteren Merge Default-Branch-Alerts aktualisieren kann.

## Verwandte Findings / Related findings

- `FND-PARENT-0001`, `FND-PARENT-0003`, `FND-PARENT-0018`, `FND-SONAR-0001`

## Restrisiko / Residual risk

Die aktive Konfiguration verbessert den `master`-Schutz, ersetzt aber keine unabhängige Review, keine stabile SonarCloud-Evidence, keine externe CII-Attestierung, kein normales Branch-Update und keine erneute Validierung von PR #120 oder den für seine Quellremediation benötigten Resulting-Default-Branch-Scan. Der aktuelle Benutzer akzeptiert kein Risiko.

## Aktueller maßgeblicher Abgleich / Current authoritative reconciliation

Dieser Abschnitt ersetzt die historische Scorecard-Currentness-Aussage oben.
Aktuelle Scorecard-Alerts sind an resultierenden Parent-Master
`cbd8385ce1b34318c84cf8f4a5a92ef98c83f82a` gebunden:
`BranchProtectionID #1`, `CodeReviewID #7`, `MaintainedID #8`,
`CIIBestPracticesID #10`, `FuzzingID #11` und `VulnerabilitiesID #12`.
Alert #1 meldet fehlende Approvers, CODEOWNERS-Review und Last-Push-Approval;
#7 meldet `0/27` approved changesets; #8 ist die Unter-90-Tage-Bedingung; #10
benötigt externe OpenSSF-Best-Practices-Registrierung; #11 hat keine
Fuzzer-Integration und #12 meldet zehn OSV-Advisory-IDs.

Dependabot #1 bleibt offen für runtime/transitives `golang.org/x/net v0.48.0`
in `connectors/envoy/ext_proc/go.mod`; sein Safe-Floor `v0.55.0` verlangt Go
`1.25`, während Modul und CI Go `1.24.0` deklarieren. Er ist nicht
dismisssed und benötigt eine benutzerkompatible Go-Baseline-Entscheidung.
CodeQL- und Secret-Scanning-Inventare sind jeweils `0` open; sie sind
unabhängige Controls, aber kein Abschluss der Dependabot-, Scorecard- oder
Sonar-Bedingungen. Evidence:
`post-merge-master-reconciliation-20260720T202018Z.json`
(`sha256:797efffded6d99d9d5cedb2c092547f7fb812e8a09b18f0cbd11c3cf0c6e514c`)
unter
`/var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/`.

## Finaler Parent-Master-Abgleich / Final Parent master reconciliation

Dieser Abschnitt ersetzt den vorhergehenden Current-State-Abschnitt. Der
exakte aktuelle Parent-Master ist `f2376bb3e39ffbe9d36faca8bcd7397477eadd10`.
Er behält einen offenen runtime/transitiven Dependabot-Alert für
`golang.org/x/net v0.48.0` und dieselben sechs Scorecard-Rule-IDs:
`BranchProtectionID`, `CodeReviewID`, `MaintainedID`, `CIIBestPracticesID`,
`FuzzingID` und `VulnerabilitiesID`. CodeQL- und Secret-Scanning-Inventare
sind jeweils `0` open. Die sicheren Dependency-Versionen erfordern weiterhin
Go `1.25`, während Modul und CI Go `1.24.0` deklarieren; kein Alert wurde
dismissed und kein Governance-Bypass eingeführt. Evidence:
`post-pr70-master-reconciliation-20260720T204648Z.json`
(`sha256:ac9753d9ba2bb2326ce53c1d9d9e160bb89ca429a18abfd9e0729a0c53366dd5`).

## Abgleich des resultierenden Parent-Masters nach PR #71 / Resulting Parent master reconciliation after PR #71

Dieser Abschnitt ersetzt die vorhergehende Current-Master-Aussage. Der
PR-#71-Head `b1eef0a087432aa9bf9bc1243a34b0b0d8f6080e` wurde am
`2026-07-20T22:16:36Z` regulär per Squash als Parent-Master
`929fe60dfca30787947027e5bd49003581a5b080` gemergt; der resultierende Tree
`fae388da52f5d660c8e18f06b058ec67b38adfd7` entspricht dem geprüften
PR-Head-Tree.

- Der Resulting-Master-CodeQL-Lauf `29783353825` war erfolgreich und die
  GitHub-API meldet null offene CodeQL-Alerts.
- Der Resulting-Master-Scorecard-Lauf `29783353831` war erfolgreich, aber
  dieselben sechs Scorecard-Alerts bleiben offen: `BranchProtectionID #1`,
  `CodeReviewID #7`, `MaintainedID #8`, `CIIBestPracticesID #10`,
  `FuzzingID #11` und `VulnerabilitiesID #12`.
- Die dynamischen Dependabot-Läufe `29783426906` und `29783429481` waren
  erfolgreich, aber der runtime/transitive Dependabot-Alert #1 für
  `golang.org/x/net v0.48.0` bleibt offen. Seine unterstützte Mindestversion
  erfordert Go 1.25; bis zur Baseline-Entscheidung wird er weder dismisssed
  noch als Risiko akzeptiert.
- GitHub Secret Scanning hat null aktive Alerts. Der getrennte Secret-Workflow
  `29783388295` belegt nur Advisory-Wrapper-Erfolg; kein Raw-Gitleaks-Ergebnis
  oder Count ist zurückgehalten, daher bleibt die Raw-Scanner-Disposition
  unbekannt.
- Die Sonar-Analyse `ee3e3400-36fb-452f-b396-775b6c4c2040` bleibt Quality Gate
  `ERROR` wegen `new_security_rating=5` und null geprüften neuen
  Security-Hotspots, mit 220 ungelösten `VULNERABILITY`-Issues und drei
  `TO_REVIEW`-Hotspots.

Evidence-Artefakt:
`/var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/resulting-master-go12413-delivery-and-scan-reconciliation-20260720T221900Z.json`
(SHA-256 `f8e8fa49a9aa8639b61946b49fca49bc0fc06623a80554f4145f78ade6ad71b2`).
`FND-GITHUB-0001` bleibt `in_progress`; kein offener externer Alert wurde
geschlossen.

## Historie / History

- `2026-07-17T10:43:59Z`: `bootstrap_created` — retained-evidence Bootstrap; keine Remediation, Verifikation, Schließung oder Risikoakzeptanz.
- `2026-07-18T08:49:52Z`: `governance_inventory_and_bounded_remediation` — zum Live-Acht-Punkte-Aggregat aktualisiert. Der bestehende `.codex`-Mount verweigert das Anlegen zusätzlicher kanonischer Finding-Verzeichnisse; Punkt-Records bleiben hier, ohne separate Directory-Allocation falsch zu behaupten.
- `2026-07-18T09:21:20Z`: `post_write_readback_and_pr_control_validation` — Ruleset, effektive Regeln, Actions-Permissions, Vulnerability Alerts, Dependabot-Inventar und der Dependency-Graph-SBOM wurden erneut gelesen. Der SBOM-Endpunkt gab `200` zurück und erfasste `golang.org/x/net v0.48.0`. PR #53 bei `d5781bd15cd286608168b952dfeb7f2d7ab29772` war `CLEAN`/mergeable mit sechs erfolgreichen exakten Required Checks, keinen Reviews und null Review-Threads. Die sichtbaren Scorecard Alerts berichten weiterhin die Pre-Remediation-Analyse vom `2026-07-16`; kein Score-Ergebnis wurde abgeleitet.
- `2026-07-19T10:48:14Z`: `security_policy_master_merge_and_recognition_verified` — der autorisierte PR #53 wurde am `2026-07-19T10:42:53Z` als master `a589cb662fb03deb764f78eefbb1056bc64d63e2` per Squash gemergt. Der Remote-Master-Inhalt entsprach dem geprüften Head `d5781bd15cd286608168b952dfeb7f2d7ab29772`; alle 14 beobachteten Master-Push-Workflows bestanden. Private Vulnerability Reporting las `enabled=true`, und GitHub GraphQL lieferte `securityPolicyUrl` `https://github.com/Easton97-Jens/ModSecurity-conector/security/policy`. Dies verifiziert nur den Security-Policy-Punkt; der aggregierte Befund bleibt `in_progress`.
- `2026-07-20T22:19:00Z`: `post_pr71_resulting_master_github_sonar_reconciled` — PR #71 wurde geschützt per Squash als `929fe60dfca30787947027e5bd49003581a5b080` gemergt; Resulting-Master-CodeQL ist clear, während Dependabot #1, sechs Scorecard-Alerts, die Raw-Secret-Scan-Evidence-Lücke und das Sonar-Quality-Gate offen beziehungsweise blockiert bleiben. Kein Alert wurde geschlossen oder als Risiko akzeptiert.

## Aktueller Abgleich — 2026-07-23

Die authentifizierte GitHub-Inventur auf dem aktuellen Master
`a308d7b414f0859490fe7253e0683a4bde80b563` bestätigt exakt zwei offene
Dependabot-Alerts (#1 `golang.org/x/net`, #2 `google.golang.org/grpc`) und sechs
offene Scorecard-Alerts (#1 BranchProtectionID, #7 CodeReviewID, #8 MaintainedID,
#10 CIIBestPracticesID, #11 FuzzingID und #12 VulnerabilitiesID). Kein Alert
wurde geschlossen, verworfen oder als gefixt behandelt.

Das effektive Ruleset schützt weiterhin gegen Löschung, Non-fast-forward-Updates
und direkte Änderungen außerhalb von Pull Requests, verlangt aber null
Approvals sowie keine Code-Owner- oder Last-Push-Approval. Eine sofortige
Settings-Änderung bleibt unsicher: Es ist nur ein direkter
Administrator/Reviewer belegt, daher würde eine Pflicht-Approval einen
Merge-Lockout erzeugen. CII bleibt eine externe OpenSSF-Registrierungs- und
Attestierungsentscheidung; Maintained bleibt eine altersabhängige
Scorecard-Metrik.

Fuzzing ist kein Target-Definitions-Blocker mehr. Die Traefik-native Middleware
hat einen begrenzten benutzerdefinierten UDS-Result-Frame-Parser, der sich für
ein echtes Go-Fuzz-Target mit gültigen Allow-/Deny-/Redirect-Seeds und einem
auf 10 Sekunden begrenzten Aufruf im bestehenden `traefik-go`-CI-Job eignet.
Es muss in einem separaten Parent-Draft-PR geliefert werden und kann Alert #11
erst schließen, nachdem es Master erreicht hat und ein Default-Branch-
Scorecard-Refresh beobachtet wurde.

VulnerabilitiesID bleibt offen: Nur die zwei aktuellen Go-Dependency-Roots sind
individuell gemappt; der aggregierte Alert enthält weitere IDs, die Raw-
Scanner-/Package-Evidence benötigen. Die erforderliche Go-Dependency- und
Fuzz-Validierung ist durch die fehlende Go-`1.26.5`-Toolchain des Hosts
blockiert; eine ausdrückliche Freigabe des aktuellen Benutzers ist für die
isolierte offizielle Toolchain-Beschaffung/-Nutzung erforderlich.

Aufbewahrte aktuelle Inventur:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/github/09-current-github-alert-inventory.json`
(SHA-256 `50921ba77734f5a5e219ee65c4e1813daf96f18956f41876298f43eb599e3a5c`).

## Draft-PR-Delivery-Update — 2026-07-23

Die aktuelle Task-Evidence ersetzt nur die oben genannten task-lokalen
Toolchain- und Target-Definitions-Blocker. Der aktuelle Benutzer autorisierte
eine Side-by-Side-offizielle Go-`1.26.5` im registrierten privaten Task-Cache;
die Archiv-SHA-256 stimmte mit
`5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053` überein.

- Draft PR [#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99)
  mit Head `2f0d8a234f984b731229aca01d43caf2749a7d61` behebt die
  Envoy-gRPC-/x-net-/x-sys-/x-text-Grenzen. Seine exakten Head-CodeQL-, OSV-,
  SonarCloud-, Secret-Scan-, Scorecard-PR-, Lint- und Projektprüfungen bestanden.
- Draft PR [#100](https://github.com/Easton97-Jens/ModSecurity-conector/pull/100)
  mit Head `4602c573b86b397712a2528bbce67fd3af891396` ergänzt den begrenzten
  Traefik-UDS-Parser-Fuzz-Target und seinen bestehenden CodeQL-Job-Aufruf.
  Sein identisches exaktes Head-Prüfset bestand.

Frische authentifizierte Post-Delivery-Reads zeigen weiterhin Dependabot #1/#2
und alle sechs Scorecard-Alerts auf Master
`a308d7b414f0859490fe7253e0683a4bde80b563`. Alle 13
VulnerabilitiesID-Zeilen sind nun gemappt: Draft PR #99 adressiert die
Go-Grundursachen; die zwei PyYAML-Zeilen sind unter aktueller Deklaration/
CI-Lock/Nutzung bereits sicher. FuzzingID wird nur durch Draft PR #100 behoben.
Keiner der Draft PRs erreicht Master, daher ist kein Alert für Schließung,
Dismissal oder Fixed-Status berechtigt. Die getrennten Governance-/Alters-/CII-
External-Requirements bleiben unverändert.

Aufbewahrte Delivery-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T165434Z-github-alert-remediation-go1265-4fc93743/evidence/delivery/20260723-draft-pr-delivery-alert-state.md`
(SHA-256 `7508110eef978259f0b9757df675844535b44bd5e6a4dc30c92d265da05110de`).

## Exact-Head-Traefik-Fuzz-Timing-Beobachtung für PR #111 — 2026-07-24

Der berechtigte reine-Parent-PR #111 mit Head
`2549d15f3181d236eeb83829818a6b03b273edcd` auf Basis von
`5f831257949f4b2655347e2f8bcb2dd5e094a260` ändert weder
`.github/workflows/ci-security-codeql.yml` noch
`connectors/traefik/native_middleware`. Sein erster Exact-Head-CodeQL-Versuch
(Run `30102616292`, Job `89512179584`) erreichte den begrenzten Befehl
`GOTOOLCHAIN=local go test -mod=readonly -run='^$' -fuzz='^FuzzUDSFrameAndResult$' -fuzztime=15s -parallel=1 .`
und endete nach `15.06s` mit `context deadline exceeded`.

Der unmittelbar vorherige resultierende Master
`5f831257949f4b2655347e2f8bcb2dd5e094a260` bestand denselben Traefik-Fuzz-Job
(`89507225557`) im CodeQL-Run `30101153404`. Eine gemäß Repository-Policy
zulässige diagnostische Einmalwiederholung des fehlgeschlagenen Jobs, ohne
Source-Änderung, bestand auf demselben PR-Head als Job `89513231832`; der
Fuzz-Schritt lief von `14:54:00Z` bis `14:54:36Z`, und CodeQL-Run
`30102616292` Versuch 2 endete um `14:55:06Z` erfolgreich.

Die aktuelle Disposition ist ein temporärer CI-Timing-Vorfall, kein Source-
oder Workflow-Defekt von PR #111. Kein Security-Control wurde geschwächt; es
sind weder Code-Änderung noch Risikoakzeptanz erforderlich, und
`FND-GITHUB-0001` bleibt `in_progress`. Die CI-Stabilität wird nur bei
Wiederholung dieses begrenzten Fuzz-Jobs untersucht. Die lokale Go-Bestätigung
ist `blocked_environment`: Der Host versuchte Go 1.26.5 unter dem read-only
Pfad `/root/go` zu beschaffen und gilt daher nicht als Product-Evidence.

Evidence-Artefakt:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/evidence/pr111-traefik-go-timing-retry.json`
(SHA-256 `1cf369ee311f012a9a584bd30cc535b0061ec9eb2e072e431307aa3b6cd4f8fe`).

## Alert-Schließungsabgleich auf aktuellem Master — 2026-07-24

Der maßgebliche Parent-Master ist
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7`. PR
[#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99) wurde von
`2f0d8a234f984b731229aca01d43caf2749a7d61` als
`5b8db00d44ab24f3a9f4216a00f7edee977b6898` gemergt; PR
[#100](https://github.com/Easton97-Jens/ModSecurity-conector/pull/100) wurde
von `dace5ca118a89a91c33fde952a6282f9c391ee10` als
`6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d` gemergt. Beide exakten Heads
haben 33 erfolgreiche und sechs scope-gerechte übersprungene Prüfungen. Alle
14 beobachteten Push-Workflows auf aktuellem Master sind erfolgreich,
einschließlich CodeQL Security Analysis und OpenSSF Scorecard; ein
erfolgreicher Scorecard-Workflow beseitigt keinen einzelnen aktiven
Scorecard-Alert selbst.

GitHub meldet Dependabot #1 (`golang.org/x/net`) und #2
(`google.golang.org/grpc`) nun als `fixed`, mit `dismissed_at = null`; die
aktuelle Abfrage offener Dependabot-Alerts liefert `[]`. Dieser verifizierte
Go-Geltungsbereich ist in `FND-PARENT-0001` geschlossen, nicht hier manuell
dismissed.

Alle sechs Scorecard-Alerts bleiben auf demselben aktuellen Master-SHA `open`
und werden daher beibehalten:

| Alert | Rule | Aktuelle Disposition |
| ---: | --- | --- |
| #1 | `BranchProtectionID` | Fehlende Approver, CODEOWNERS-Review und Last-Push-Approval erfordern eine Governance-Entscheidung. |
| #7 | `CodeReviewID` | Scorecard beobachtet 0/26 approved Changesets; echte unabhängige Review-Historie ist erforderlich. |
| #8 | `MaintainedID` | Das Repository ist jünger als 90 Tage; dies ist zeitbasiert. |
| #10 | `CIIBestPracticesID` | Externe OpenSSF-Best-Practices-Registrierung/-Attestierung ist erforderlich. |
| #11 | `FuzzingID` | Meldet weiterhin keine Fuzzer-Integration. Die gemergte begrenzte `FuzzUDSFrameAndResult`-Kontrolle bestand 15 Sekunden mit 99.749 Ausführungen, aber ein aktives aktuelles Scanner-Ergebnis wird nicht manuell dismissed. |
| #12 | `VulnerabilitiesID` | Meldet weiterhin die zwei PyYAML-Advisory-IDs; ein aktives aktuelles Scanner-Ergebnis wird nicht manuell dismissed. |

Kein Scorecard-Alert wurde geschlossen, dismissed, unterdrückt oder
risikoakzeptiert. Das Finding bleibt `in_progress`, bis jede aktive externe
Bedingung tatsächlich behoben und neu gescannt ist oder eine getrennte,
ausdrückliche, evidenzbasierte Disposition erhält.

Aufbewahrte Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/github-alert-closure-verification.md`
(SHA-256 `20ea82fbd04cc7ea672a644c4c5c5621b38b6fc29ce76ed9c54f028ca458afdf`).

## Historien-Update — 2026-07-24

- `2026-07-24T15:43:59Z`: `current_master_alert_closure_reconciled` —
  Dependabot-Schließung und die Beibehaltung aktiver Scorecard-Alerts auf
  aktuellem Master wurden erneut validiert. Der geschlossene Go-Dependency-
  Geltungsbereich wechselte zu `FND-PARENT-0001`; dieses Aggregat-Finding
  bleibt ohne unsichere externe Schließung `in_progress`.

## Post-Master-Advance-Recheck — 2026-07-24

Der maßgebliche Parent-`master` rückte anschließend um einen Commit auf
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` vor. Der Vergleich ab
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7` ändert nur den bilingualen Change
Record/Index und `tests/test_full_lifecycle_evidence.py`; die Envoy-Go-Module
und das Traefik-Fuzz-Target bleiben unverändert. Dependabot #1/#2 bleiben ohne
Dismissal `fixed`, das offene Inventar bleibt leer und alle 14 beobachteten
Push-Workflows auf aktuellem Master sind erfolgreich.

Dieselben sechs aktuellen Scorecard-Alerts bleiben auf diesem neueren Master
offen: `BranchProtectionID #1`, `CodeReviewID #7`, `MaintainedID #8`,
`CIIBestPracticesID #10`, `FuzzingID #11` und `VulnerabilitiesID #12`.
Folglich bleibt `FND-PARENT-0001` geschlossen und dieses Aggregat-Finding
`in_progress`; kein Scorecard-Alert wurde dismissed, unterdrückt, geschlossen
oder risikoakzeptiert.

Aufbewahrte Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-advance-recheck.md`
(SHA-256 `c099c32564c1a78e60f98a61ba350904669d9c7231459c4109587088e31f915f`).

- `2026-07-24T16:00:01Z`: `post_master_advance_alert_rechecked` — der
  aktuelle maßgebliche Zustand wurde nach einem für den Scope irrelevanten
  Master-Vorrücken erneut gelesen; Schließungs- und Retention-Dispositionen
  bleiben unverändert.

## Zweiter Post-Master-Advance-Recheck — 2026-07-24

Der maßgebliche Parent-`master` rückte erneut auf
`185fd358bcfabe63464ab0e135eecedf24c9a699` vor. Der Ein-Commit-Vergleich ab
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` ändert nur einen bilingualen
Change Record/Index und `tests/test_full_lifecycle_profiles.py`; Envoy-Go-
Module und Traefik-Fuzz-Target bleiben unverändert. Dependabot #1/#2 bleiben
ohne Dismissal `fixed`, und das offene Inventar bleibt leer.

Die sechs offenen Scorecard-Alerts bleiben offen, ihre neuesten Alert-Instanzen
sind weiter an `a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` gebunden; GitHub hat
keine neuere Scorecard-Alert-Instanz für den aktuellen Master veröffentlicht.
Der aktuelle Master hat 14 abgeschlossene Push-Workflow-Läufe: 13 Erfolge und
einen fehlgeschlagenen OpenSSF-Scorecard-`default-branch`-Lauf (`30107490735`);
sein Check-Inventar zeigt außerdem eine fehlgeschlagene SonarCloud Code
Analysis. Keine dieser Bedingungen wurde dismissed, unterdrückt, geschlossen
oder risikoakzeptiert. `FND-PARENT-0001` bleibt geschlossen; dieses Aggregat
bleibt `in_progress`.

Aufbewahrte zweite Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-second-advance-recheck.md`
(SHA-256 `17f4abdf4be2939aca498746e9e345d0e33566580adbee0b6e92427bf73b1c8b`).

- `2026-07-24T16:07:44Z`: `post_master_second_advance_alert_rechecked` —
  letzter Master-Scope, Alert-Instance-Currentness, Dependabot-Zustand und die
  Scorecard-/Sonar-Workflow-Fehler wurden ohne unsichere Schließung erfasst.

## Finaler Current-Master-Recheck nach Scorecard-Wiederholung — 2026-07-24

Der maßgebliche Parent-`master` bleibt
`185fd358bcfabe63464ab0e135eecedf24c9a699`. Dependabot #1/#2 bleiben ohne
Dismissal `fixed`, und es gibt keine offenen Dependabot-Alerts. OpenSSF-
Scorecard-Run `30107490735`, Versuch 3, war erfolgreich, daher haben alle 14
beobachteten GitHub-Actions-Push-Workflows nun die Conclusion `success`.

GitHub hat alle sechs weiter offenen Scorecard-Alerts auf diesen selben
aktuellen Master-SHA aktualisiert: `BranchProtectionID #1`, `CodeReviewID #7`,
`MaintainedID #8`, `CIIBestPracticesID #10`, `FuzzingID #11` und
`VulnerabilitiesID #12`. SonarCloud Code Analysis bleibt fehlgeschlagen. Die
erfolgreiche Workflow-Wiederholung beseitigt keinen aktiven Scorecard-Alert;
kein Alert wurde dismissed, unterdrückt, geschlossen oder risikoakzeptiert.
`FND-PARENT-0001` bleibt geschlossen und dieses Aggregat-Finding bleibt
`in_progress`.

Aufbewahrte finale Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-scorecard-retry-final-recheck.md`
(SHA-256 `2a788454ba88bcd90add62b5eae3545d83a53180f7aefe8c72ffc864a2959746`).

- `2026-07-24T16:14:53Z`: `post_master_final_current_alert_rechecked` — die
  Scorecard-Wiederholung und alle Actions-Workflows sind erfolgreich;
  aktualisierte aktive Scorecard-Alerts und der fehlgeschlagene SonarCloud-
  Check bleiben erfasstes Follow-up.

## Exact-Head-Validierung von Draft-PR #120 — 2026-07-24

Ein frischer authentifizierter GitHub-Readback meldet dieselben sechs
Scorecard-Alerts auf dem maßgeblichen Parent-Master
`30ee953b57f4aafebaa0e6ed565a80f6500db1de` als `open`:
`BranchProtectionID #1`, `CodeReviewID #7`, `MaintainedID #8`,
`CIIBestPracticesID #10`, `FuzzingID #11` und `VulnerabilitiesID #12`.

Draft-PR [#120](https://github.com/Easton97-Jens/ModSecurity-conector/pull/120)
ist gegen diesen Master `OPEN`, `CLEAN` und mergeable. Sein exakter Head
`57c411eeca7be024e5718d560e26e4bc051b92ae` bestand alle 33 anwendbaren
terminalen Hosted-Checks, mit sechs scope-angemessenen Skips; OSV und SonarCloud
bestanden. CodeQL-Lauf `30111632630`, bounded-c-cpp-Job `89542295414`, führte
**Fuzz Common HTTP header parser** von `2026-07-24T17:06:15Z` bis
`2026-07-24T17:06:42Z` erfolgreich aus.

Der PR ergänzt einen echten C/libFuzzer-Harness unter
`fuzz/common_http_headers_fuzz.c` für den Common-HTTP-Header-Parser, begrenzt
durch einen External-Build-Runner und im bestehenden CodeQL-Job aufgerufen. Er
pinnt außerdem Development-PyYAML auf `PyYAML==6.0.3`, passend zum CI-Hash-Lock
und mit einer eindeutigen sicheren Version für den OSV-Parser. Dies ist die
engste source-owned Remediation für #11 und #12; es gibt keine Scanner-
Unterdrückung, keinen künstlichen Marker und keine Abschwächung eines
Quality-Gates.

Der PR-Event-Scorecard-Lauf `30111632360`, Job `89542294656`, bestand, aber
sein `default-branch`-Schritt wird bei einem `pull_request`-Event korrekt
übersprungen. Er kann kein SARIF aktualisieren und keine Default-Branch-Alerts
schließen. Daher sind #11 und #12
`verified_draft_pr_pending_resulting_master_scorecard_refresh`, nicht
geschlossen. Die anderen vier Alerts liegen außerhalb dieses PRs: #1 benötigt
eine Ruleset-/unabhängige-Review-Konfigurationsentscheidung, #7 echte
unabhängige Review-Historie, #8 ist bis `2026-08-12` altersgebunden und #10
benötigt eine Owner-geführte OpenSSF-Best-Practices-Registrierung und
Attestierung.

Kein Scorecard-Alert wurde geschlossen, dismissed, unterdrückt oder
risikoakzeptiert. Der nächste legitime Schritt ist die unabhängige Review und
der Merge des Draft-PRs, gefolgt von einer frischen Default-Branch-Scorecard-
Analyse des resultierenden Masters.

Aufbewahrte Exact-Head-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T164102Z-scorecard-alert-remediation-pr-7c78e095/evidence/pr120-exact-head-validation.md`
(SHA-256 `24225b5a3c44a960dcaf3e0dc595a8560546058b019da63d99ce898dcfe9e453`).

- `2026-07-24T17:13:44Z`: `draft_pr120_exact_head_verified` — #11 und #12
  sind exact-head-verifizierte Draft-PR-Quellremediationen, die auf unabhängige
  Review, Merge und Scorecard-Refresh des resultierenden Masters warten.
  #1/#7/#8/#10 bleiben externe Anforderungen; alle sechs Alerts bleiben offen.

## Base-Advance-Recheck von Draft-PR #120 — 2026-07-24

Nach der Exact-Head-Validierung rückte Remote-Master um einen nicht
überlappenden Commit von `30ee953b57f4aafebaa0e6ed565a80f6500db1de` auf
`9e788057d2b551ba51ad7c4e6e1d8c5198b77834` vor. Der Vergleich ändert nur
`ci/checks/common/check-adapter-helpers.sh` und seinen gepaarten bilingualen
Change Record/Index; er überlappt nicht mit C-Header-Fuzzer, begrenztem Runner,
CodeQL-Integration, PyYAML-Pin, fokussiertem Test oder Change Record in PR #120.

PR #120 bleibt `OPEN`/Draft beim exakten Head
`57c411eeca7be024e5718d560e26e4bc051b92ae`. GitHub meldet
`mergeable=MERGEABLE`, aber `mergeStateStatus=BEHIND`. Das frühere Hosted-
Ergebnis mit 33 Erfolgen bleibt gültige Evidence für genau diese Source-
Revision, ist aber kein exaktes Current-Merge-Candidate-Ergebnis mehr. Ein
frischer authentifizierter Scorecard-Readback bindet alle sechs offenen
Scorecard-Alerts #1/#7/#8/#10/#11/#12 an aktuellen Master
`9e788057d2b551ba51ad7c4e6e1d8c5198b77834`.

Es erfolgten kein PR-Branch-Update, kein Rebase, kein Force Push, kein
Merge-Commit, kein Master-Merge, kein Dismissal, keine Unterdrückung, keine
Schließung und keine Risikoakzeptanz. Die Aufgabe verbietet Merge und Force
Push. Ein getrennt autorisiertes normales Branch-Update und frische Exact-
Head-Validierung sind nötig, bevor der Draft-PR als aktuell reviewt und später
gemergt werden kann. #11 und #12 bleiben daher source-remediated, aber
`behind_current_master`; alle sechs Alerts bleiben offen.

Aufbewahrte Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T164102Z-scorecard-alert-remediation-pr-7c78e095/evidence/pr120-base-advance-recheck.md`
(SHA-256 `c47ae53a06ddf584a0edac3ddacbfea168a7cc8edb9029a082ef4a0535b57e6f`).

- `2026-07-24T17:25:15Z`: `draft_pr120_base_advance_rechecked` — aktueller
  Master rückte ohne Source-Überlappung vor. Der PR bleibt ein gültiger
  Source-Patch, benötigt aber ein autorisiertes normales Update und frische
  Exact-Head-Checks; keine verbotene Merge- oder Force-Operation erfolgte.

## Aktueller GitHub-Abgleich und Schließung — 2026-07-26

Dieser Abschnitt ersetzt die vorherige Current-State-Erzählung. Der nur
lesende GitHub-Abgleich um 2026-07-26T13:29:40Z gegen Parent-Master
`6ca7e1536ce7e93da68099db9c586b88852ff13e` lieferte keine offenen
Scorecard-Alerts. Die sechs verfolgten Source-Alerts sind terminal:

- `BranchProtectionID #1`, `CodeReviewID #7` und
  `MaintainedID #8`: als False Positive dismissed.
- `CIIBestPracticesID #10`: als used in tests dismissed.
- `FuzzingID #11` und `VulnerabilitiesID #12`: fixed.

Parent-PRs #99, #100 und #120 sind gemergt. Das aktuelle Protect-master-
Ruleset ist aktiv, hat keine Bypass-Akteure und behält strikte Required Checks
sowie Deletion-/Non-fast-forward-Controls. Die Actions-Default-Permission ist
read, Private Vulnerability Reporting ist aktiv und die Security-Policy-URL des
Repositorys ist vorhanden.

Die aggregierte GitHub-Source-Bedingung ist damit `closed`; das vollständige
EN/DE/JSON-Tripel wird mit seiner historischen Evidence archiviert. Dies ist
keine Production-Governance-Zertifizierung: Vor Produktion, Veröffentlichung
oder Release diesen Record wiederherstellen und Approvals, CODEOWNERS,
Attestierung sowie die dann aktuellen Scorecard-Anforderungen erneut
validieren.
