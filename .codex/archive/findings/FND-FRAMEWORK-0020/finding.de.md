# FND-FRAMEWORK-0020 — Framework-PR #27: CI-Security-Python-Quality-Fehler ist am exakten PR-Head behoben, Verifikation des resultierenden Masters steht aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0020` |
| Kategorie | `ci_failure` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Severity | `P1` / `not_applicable` |
| Confidence / Status | `validated` / `fixed` |
| Feasibility | `requires_user_decision` |
| Release-Blocker | `true` |
| Security-relevant | `true` |

## Zusammenfassung und eigenständige Grenze

Framework-PR #27 scheiterte im obligatorischen CI-Security-Python-Quality-Job
zuerst an Ruff-Formatierung und danach an einer deterministischen
Pyright-Mapping-Key-Diagnose. Der aktuelle exakte PR-Head
`6a4e057b2cef1f911ba25ab9f95e1b01b390691b` enthält den Reparatur-Commit
`82a091a3b6c3e5005126966bf3c6900208c8632b` ohne Abschwächung eines Qualitäts-
oder Security-Controls: Er typisiert den bestehenden PyYAML-Boolean-Key-
Fallback als `dict[Any, Any]`, während Runtime-Body und die fail-closed
Workflow-Event-Prüfungen erhalten bleiben.

Frische GitHub-Check-Runs für genau diesen Head sind terminal und erfolgreich,
einschließlich `python-ci-security-quality`, aller drei `CodeQL PR`-Sprachen,
Dependency Review, PR-Range-Secret-Scan, actionlint, zizmor und SonarCloud-
PR-Analyse. Das Finding ist `fixed`, nicht `verified`: Ein normaler Merge und
die Verifikation des resultierenden Framework-`master` bleiben durch eine
separate ausdrückliche Nutzerentscheidung zu GitHub Code Scanning Default Setup
blockiert.

Der aktuelle Exact-Head-Receipt ist
`evidence/pr27-6a4e057-exact-head-validation.md`, SHA-256
`cca00d78d239b9f2dc21b2ff4f7bf3ed75a0390eeff726254fa8153633b97f58`.

Dieses Finding ist von `FND-FRAMEWORK-0012` verschieden, das semantische
Erreichbarkeit/Durchsetzung des CI-Security-Evidence-Contracts abdeckt. Dieser
Record behandelt den unabhängig behebbaren CI-Typqualitätsfehler in diesem
Checker.

## Betroffener Scope, Voraussetzungen und Reproduktion

Betroffene Source: `ci/checks/security/check-ci-security-evidence-contract.py`.
Relevante Symbole: `workflow_events`, `Mapping.get`, `reportArgumentType`,
`ruff format --check` und `ruff check`.

Der historische Pyright-Fehler trat am exakten Head
`55a46ce68b69c8b6ef758ee94e184688aab995a4`, GitHub-Actions-Run `29696794348`,
Job `88218830400` auf. Die Reparatur ist Commit
`82a091a3b6c3e5005126966bf3c6900208c8632b`, ein direkter Nachfolger des
Ruff-only-Follow-ups `55a46ce68b69c8b6ef758ee94e184688aab995a4`.

Zur Reproduktion des historischen Fehlers
[`29696794348 / 88218830400`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29696794348/job/88218830400)
prüfen. Zur Validierung der Reparatur die Exact-Head-Check-Runs für
`82a091a…` und nach einem autorisierten normalen Merge die äquivalente
Master-Evidence prüfen. Ältere Heads ersetzen diese Evidence nicht.

## Evidence und Einschränkungen

- Historischer Fehler: exakter Head `55a46ce68b69c8b6ef758ee94e184688aab995a4`,
  Run `29696794348`, Job `88218830400`, beobachtet `2026-07-19T17:28Z`.
  Pyright meldete: `check-ci-security-evidence-contract.py:424:42 Argument
  of type Literal[True] cannot be assigned to parameter key of type str in
  function get (reportArgumentType)`. Ruff bestand.
- Reparatur-Evidence: exakter Head
  `82a091a3b6c3e5005126966bf3c6900208c8632b`; GitHubs Commit-Check-Runs-API
  wurde um `2026-07-19T17:37Z` mit Exit-Code `0` gelesen. Alle nicht
  advisory Checks waren terminal `success`; die drei absichtlich advisory
  Jobs waren terminal `skipped`. `python-ci-security-quality` bestand bei
  [Run `29697123197`, Job `88219679430`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29697123197/job/88219679430).
- Scoped lokale Evidence: Der exakte Source-Diff `55a… -> 82a…` besteht aus
  einer Annotation-Zeile; `git diff --check` bestand; der Framework-MRTS-
  Gitlink blieb `13aa91291adea12d5c607fdd165d010fcfb1da78`; die fokussierte
  Sicherheitsprüfung fand keinen reportierbaren Befund.
- Einschränkung: Externe GitHub-Ausgabe wurde live geprüft und nicht als
  hash-adressiertes lokales Artefakt aufbewahrt. Es wird keine SHA-256
  erfunden. Dem lokalen Runner fehlt Node.js; daher konnte das SHA-locked
  Pyright-Bundle dort nicht ausgeführt werden. Ein nicht unterstützter
  Interpreter wurde nicht ersetzt. Das exakte Hosted-Pyright-Ergebnis ist die
  autoritative Validierung.

## Grundursache, Auswirkung und implementierte Remediation

PyYAML kann einen nicht quotierten Workflow-Key `on` als Boolean `True`
parsen. Der Checker unterstützt diesen Kompatibilitäts-Fallback bereits bewusst
mit `data.get("on", data.get(True))`, seine Annotation versprach jedoch
fälschlich `dict[str, Any]`; deshalb wies Pyright den Boolean-Key ab.

Commit `82a091a…` ändert nur die `workflow_events`-Parameterannotation zu
`dict[Any, Any]`. Er ändert weder Parsing, den Boolean-Fallback,
Permission-Logik, Workflow-Event-Akzeptanz, Error-Sinks noch die Workflow-
Matrix. PR-CodeQL verlangt weiterhin exakt `pull_request`; Trusted CodeQL
weist weiterhin `pull_request` ab und verlangt `push`, `schedule` und
`workflow_dispatch`.

Der historische obligatorische Fehler ist am PR-Head repariert. Er bleibt nur
bis zum normalen Merge und der Verifikation des resultierenden Framework-
Masters ein Release-Blocker. Pyright zu unterdrücken, Ruff zu deaktivieren oder
den CI-Security-Evidence-Contract abzuschwächen wurde nicht verwendet und
bleibt verboten.

## Akzeptanzkriterien und Validierungsplan

- [bestanden] `python-ci-security-quality` besteht am aktuellen exakten PR-Head `6a4e057…`.
- [bestanden] Ruff-Format und Ruff-Lint bestehen am selben Head.
- [bestanden] Die fokussierte Sicherheitsprüfung bestätigt unverändertes
  fail-closed Event-Verhalten, und es gibt keine Parent- oder MRTS-Änderung.
- [ausstehend] Der Nutzer autorisiert ausdrücklich die erforderliche Code-
  Scanning-Default-Setup-Konfigurationsänderung oder ein anderes genehmigtes
  Security-Design.
- [ausstehend] PR #27 wird mit seinem exakten verifizierten Head normal
  gemergt; der resultierende Master-SHA wird auf Reachability, Content,
  MRTS-Integrität und frische Master-Workflows geprüft.
- [ausstehend] Die ursprüngliche Pyright-Reproduktion und Legitimate Controls
  bestehen auf diesem resultierenden Master, bevor dieser Record `verified`
  wird.

## Regression- und Legitimate-Control-Tests

- `tests/ci_security/test_ci_security_evidence_contract.py`
- Hosted `python-ci-security-quality` Pyright, Ruff-Format und Ruff-Lint
- Exact-Head-GitHub-Check-Runs für PR #27
- Der Trusted-CodeQL-Negativ-Event-Control: Das Hinzufügen von `pull_request`
  bleibt durch den Evidence-Contract-Checker abgewiesen

## Abhängigkeiten, Blocker, Beziehungen, Restrisiko und Historie

Abhängigkeiten: normale PR-#27-Integration; exakte Verifikation des
resultierenden Masters; und eine ausdrückliche Nutzerentscheidung für GitHub
Code Scanning Default Setup. Verwandte Findings: `FND-FRAMEWORK-0012`,
`FND-GITHUB-0005`. Es gibt kein Duplikat.

Die blockierende Einstellung liest derzeit `state: configured` für Actions,
C/C++ und Python. Der vertrauenswürdige Advanced-CodeQL-Uploader würde nach
einem Master-Merge mit diesem Default Setup kollidieren. Dieses Finding
autorisiert keine Settings-Änderung, keinen Bypass, keinen direkten
Master-Push, kein Parent-Gitlink-Update und keine MRTS-Änderung.

- `2026-07-19T17:16Z`: Exakter Head `2f635be…` scheiterte nur, weil Ruff den
  Checker und den fokussierten Test formatieren würde; Ruff-Lint bestand.
- `2026-07-19T17:28Z`: Exakter Head `55a46ce…` bestand Ruff, scheiterte aber
  am deterministischen Pyright-`Literal[True]`-Mapping-Key-Check.
- `2026-07-19T17:35Z`: Normaler Reparatur-Commit `82a091a…` wurde nach einer
  fokussierten Sicherheitsprüfung ohne reportierbaren Befund gepusht.
- `2026-07-19T17:37Z`: Alle Exact-Head-Hosted-PR-Checks bestanden; Status
  wechselte zu `fixed`, bis zur Verifikation des resultierenden Masters und
  der Settings-Entscheidung.
- `2026-07-19T19:34:25Z`: Der aktuelle test-only Nachfolger `6a4e057…`
  bestand seine vollständige Exact-Head-GitHub-/Sonar-Validierung und behält
  die Pyright-Reparatur. Der Record bleibt `fixed` bis zur Settings-
  Entscheidung und dem resultierenden Master.

## Beobachtung auf dem resultierenden Master — 2026-07-19T20:00:39Z

PR #27 wurde als Squash-Merge `6de40c1714410241e917e9083ee890a82fb2fdbb`
gemergt; sein Tree entspricht dem exakten PR-Head
`6a4e057b2cef1f911ba25ab9f95e1b01b390691b`, und sein MRTS-Gitlink änderte sich
nicht. Das exakte Master-Control `python-ci-security-quality` bestand ebenso
wie `scaffold-lint`, `common-structure` und Workflow-Lint. Damit ist belegt,
dass der reparierte Pyright-Pfad im gemergten Source erhalten bleibt.

Der erforderliche vertrauenswürdige Advanced-CodeQL-Uploader schlug nach seiner
Analyse für alle drei Sprachen fehl, weil GitHub Default Setup aktiv bleibt,
obwohl die drei Default-Setup-CodeQL-Analysen auf demselben SHA bestanden.
Dieser externe Konfigurationsfehler ist `FND-GITHUB-0006`; deshalb bleibt dieses
Finding `fixed`, nicht `verified`. Die Merge-Autorisierung des Nutzers behielt
Default Setup bei; sie autorisierte keine Settings-Änderung, direkte Master-
Korrektur, Control-Abschwächung, Parent-Änderung oder MRTS-Aktion.
