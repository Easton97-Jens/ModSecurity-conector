# FND-FRAMEWORK-0003 — Framework-Workflow-Actions verwenden mutable Major-Tags

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0003` |
| Title / Titel | `Framework-Workflow-Actions verwenden mutable Major-Tags` |
| Category / Kategorie | `security_hardening` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `validated` |
| Status | `fixed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Die Framework-Action-Pin-Kontrolle ist lokal remediiert: Jede beobachtete
externe Action-Referenz ist auf einen überprüften immutable vollständigen
Commit-SHA gepinnt, und ein nativer regressionsgetesteter Validator erzwingt die
Grenze.

## Observed behavior / Beobachtetes Verhalten

Auf der Framework-Basis `cdc91a398d6c156eaff927d742b23018a3817fb6`
akzeptierte der bisherige Inline-Validator sieben mutable Major-Tags. Der
geänderte Framework-Workflow-Baum validiert nun nur externe Full-SHA-Referenzen.

## Expected behavior / Erwartetes Verhalten

Jede externe ausführbare Workflow-Action muss vor ihrer Ausführung durch einen
Framework-Job zu einem überprüften vollständigen 40-stelligen Git-Commit-SHA
auflösen; lokale `./`-Referenzen bleiben ein eigenständiger legitimer
Kontrollfall.

## Impact / Auswirkung

Der mutable-Action-Supply-Chain-Pfad ist lokal entfernt. Die Delivery-Assurance
bleibt begrenzt, weil verpflichtende statische Tools und unabhängige
Framework-Delivery-Gates ungelöst sind.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `modules/ModSecurity-test-Framework/.github/workflows/check-action-versions.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/check-common-versions.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/cleanup-artifacts.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/lint.yml`
- `modules/ModSecurity-test-Framework/.github/workflows/test-common.yml`
- `modules/ModSecurity-test-Framework/ci/checks/security/check-workflow-action-pins.py`
- `modules/ModSecurity-test-Framework/tests/security_regression/test_workflow_action_pins.py`
- `modules/ModSecurity-test-Framework/Makefile`

### Symbols / Symbole

- `check-workflow-action-pins.py`
- `external uses: full 40-character Git commit SHA`
- `test-workflow-action-pins`

## Preconditions / Voraussetzungen

- Die Framework-Basis `cdc91a398d6c156eaff927d742b23018a3817fb6` und die
  zurückgehaltene Validierungs-Evidenz bleiben verfügbar.
- Die sieben Action-Commit-SHAs wurden aus ihren Upstream-Action-Repositories
  überprüft, ohne die beabsichtigten Major-Versionen zu ändern.

## Reproduction / Reproduktion

- Die extrahierte Pre-Fix-Current-Master-Kontrolle akzeptierte
  `actions/checkout@v7`, `actions/setup-python@v6`, `actions/github-script@v9`
  und `peter-evans/create-pull-request@v8`.
- `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python ci/checks/security/check-workflow-action-pins.py`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:159-177,228-228`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '159,177p;228p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058/evidence/fnd-framework-0003-validation-summary-retained.md`
  - Type: `retained_validation_summary`; SHA-256: `b45fb9acc7a9ed5f12e5b49bce0669b815730b2cde9ee116c77b82f8240a8ba5`
  - Command: `rtk proxy .codex/bin/storage-budget retain-evidence --run 20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058 --source /var/tmp/codex/ModSecurity-conector/runs/20260718T092013Z-fnd-framework-0003-actions-sha-pins-41e9a058/tmp/fnd-framework-0003-validation-summary-source.md --destination evidence/fnd-framework-0003-validation-summary-retained.md --json`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-18T10:27:28Z`; retention: `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

Die Framework-Action-Pin-Kontrolle erlaubt ausdrücklich mutable Major-Tags; dadurch können geplante oder manuell gestartete Jobs extern aufgelösten Action-Code ohne immutable Action-Identität ausführen.

## Proposed remediation / Vorgeschlagene Remediation

Lokal implementiert: Für jede externe Workflow-Action überprüfte vollständige
Commit-SHAs verlangen, die Pin-Kontrolle als Framework-nativen Checker
bereitstellen und fokussierte Regression sowie Update-Review-Evidenz
zurückhalten.

## Acceptance criteria / Akzeptanzkriterien

- Jede externe Framework-Workflow-Action ist auf einen überprüften immutable
  vollständigen 40-stelligen Commit-SHA gepinnt.
- Der Checker deckt `.yml` und `.yaml` Workflow-Orte rekursiv ab und lehnt
  mutable oder nicht unterstützte Action-Referenz-Formen fail-closed ab.
- Fokussierte Mutable-Tag- und Syntax-Bypass-Regressionen schlagen vor der
  Kontrolle fehl und bestehen danach; Full-SHA-Kontrollfälle bleiben gültig.
- Der Action-Update-Prozess hält Source-, Review- und Validierungs-Evidenz
  zurück.

## Validation plan / Validierungsplan

- Die fokussierte Pin-Suite, die breitere Framework-Security-Regression-Suite,
  den Real-Workflow-Checker, Framework-Lint und Framework-Dokumentationschecks
  ausführen.
- actionlint, ShellCheck, zizmor, SonarQube Cloud und unabhängige Codex-
  Security-Revalidierung mit faktischen pass/fail/blocked-Dispositionen ausführen.

## Regression tests / Regressionstests

- `tests/security_regression/test_workflow_action_pins.py`: 21 fokussierte
  Fälle für mutable Tags, Syntax-Bypässe und legitime Kontrollen.
- `tests/security_regression`: 34 Fälle bestanden.

## Legitimate control tests / Legitime Kontrolltests

- Eine zitierte oder unzitierte externe Full-SHA-Referenz und ein externer auf
  einen Full-SHA gepinnter reusable Workflow validieren.
- Lokale `./`-Action- und lokale reusable-Workflow-Referenzen validieren als
  nicht-externe Kontrollen.

## Grundursachen-Triage / Root-cause triage

- Framework-SHA: `cdc91a398d6c156eaff927d742b23018a3817fb6`
- Urteil: `confirmed`; statische Confidence: `medium`.
- Grundursachen-Gruppe: `RC-FW-001-action-reference-immutability`; Singleton. Mit keinem anderen Finding sind ein gemeinsamer Patch oder dieselben Regressionstests nachgewiesen, daher ist ein separater Framework-PR erforderlich.
- Entry Points: `.github/workflows/check-common-versions.yml:3-10,20-24,106-115` und `.github/workflows/cleanup-artifacts.yml:3-18`.
- Source → Broken Control / Sink: mutable externe `uses:`-Major-Tags → `.github/workflows/check-action-versions.yml:27` akzeptiert `@vN` → ein geplanter oder manuell gestarteter Runner führt den Action-Code aus, einschließlich eines Jobs mit `contents: write` und `pull-requests: write`.
- Angreifervoraussetzungen: Ein Action-Publisher oder dessen Tag-Autorität verändert ein referenziertes Major-Tag vor dem Workflow-Lauf. Ein Tag-Rewrite oder Workflow-Lauf wurde nicht reproduziert.
- Vorhandene Gegenkontrollen: explizite Job-Permissions und ein Pin-Checker existieren, aber dieser akzeptiert bewusst mutable Major-Tags.
- Auswirkung: veränderter Action-Code kann die GitHub-Token-Permissions des betroffenen Jobs nutzen und workflow-kontrollierten Repository- oder Artifact-State verändern.
- Erforderliche Regression / legitimer Kontrollfall: `@vN` in allen unterstützten Workflow-Dateien ablehnen; einen überprüften 40-hex-SHA akzeptieren und gültige Workflow-Syntax sowie Trigger bewahren.
- Bypass-Review: zitierte/auskommentierte Entries, `.yaml`-Dateien, reusable Workflows, lokale/Docker-Actions, verkürzte Hashes und künftige Workflow-Pfade.
- Parent-Auswirkung: keine in dieser Triage; ein späteres Framework-Delivery kann Parent nur über ein separat autorisiertes Gitlink-Update erreichen. MRTS-Auswirkung: keine; kein MRTS-Source- oder Checkout-Zugriff ist erforderlich.
- Delivery-Grenze: ausschließlich Framework-Branch und Draft-PR; Parent-Gitlink unverändert; MRTS unberührt. Aktuelle Framework-CI-/Sonar-Blocker benötigen vor verified delivery eigene evidenzbasierte Dispositionen.
- Evidenzlücken: kein anwendbares Framework-`SECURITY.md` und kein dynamischer Action-Tag-Rewrite verfügbar. Der vollständige Folgeauftrag steht in `.codex/roadmap/framework-security-root-cause-triage.de.md`.

## Dependencies / Abhängigkeiten

- `FND-FRAMEWORK-0001`
- `FND-SONAR-0002`

## Blockers / Blocker

- `actionlint` und `zizmor` sind durch die Aufgabe erforderlich, aber nicht
  verfügbar; es gibt keinen repository-genehmigten oder benutzerautorisierten
  Provisionierungsweg.
- `FND-FRAMEWORK-0001` und `FND-SONAR-0002` bleiben unabhängige
  Verified-Delivery-Gates.

## Related findings / Verwandte Findings

- `FND-GITHUB-0001`
- `FND-FRAMEWORK-0004`

## Residual risk / Restrisiko

Die lokale Action-Pin-Kontrolle ist behoben, aber es existieren kein Commit,
Push, Draft-PR, Current-Head-CI, SonarQube-Cloud-Ergebnis und keine exakte
SHA-Gleichheit. `actionlint`/`zizmor` sind nicht verfügbar, ShellCheck behält
unabhängige Baseline-Diagnosen, und `FND-FRAMEWORK-0001`/`FND-SONAR-0002`
bleiben getrennte Delivery-Gates. Es wurde kein Risiko akzeptiert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T08:09:21Z`: root_cause_triaged — Aktuelle statische Evidence bestätigte die mutable-Major-Tag-Control-Lücke; sie bleibt eine offene Singleton-Gruppe ohne Delivery oder Risikoakzeptanz.
- `2026-07-18T10:27:28Z`: local_remediation_validated_delivery_blocked — Die Framework-Action-Pin-Kontrolle wurde lokal mit überprüften Full-SHA-Pins, einem nativen Checker, einer 21-Fälle-fokussierten Suite, einer 34-Fälle-breiteren Security-Regression-Suite, Framework-Lint, Dokumentationschecks und unabhängiger Codex-Security-Revalidierung ohne konkreten Bypass remediiert. Delivery bleibt blockiert: `actionlint`/`zizmor` sind nicht verfügbar, ShellCheck behält Baseline-Diagnosen, und `FND-FRAMEWORK-0001`/`FND-SONAR-0002` sind unabhängige Gates; es erfolgten kein Commit, Push, Draft-PR, Merge, Parent-Gitlink-Änderung oder MRTS-Änderung.

## Direkte Stale-PR-Rückeinführungsgefahr vom 2026-07-19

Der direkte Vergleich von aktuellem Framework-`master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` mit dem veralteten PR #24
bestätigt, dass der ungemergte Head den Full-SHA-Action-Parser, die
Regressionssuite und den Makefile-Hook löscht und sie durch einen Major-Tag-
toleranten Check ersetzt. PR #27 besitzt zusätzlich einen separat geprüften
Parser-Regressionskandidaten. Dies sind nur Merge-Blocker; Master bleibt
`fixed`. Der Ersatzchecker von PR #29 wird nicht als Rückeinführung erfasst.

Zurückgehaltene Evidence: Run
`20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
beobachtet am `2026-07-19T12:01:55Z` durch RTK-präfixierte Direct-Diff- und
statische Action-Control-Review.
