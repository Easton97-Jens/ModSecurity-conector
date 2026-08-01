# FND-FRAMEWORK-0021 — Externe Python-Versionsänderung bricht den hash-gesperrten Framework-CI-Abhängigkeitsvertrag

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0021` |
| Kategorie | `ci_failure` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Severity | `P1` / `not_applicable` |
| Confidence / Status | `confirmed` / `verified` |
| Feasibility | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung, Beobachtung und Auswirkung

Nach dem nutzerautorisierten PR-#27-Merge änderten externe Framework-master-
Commits beginnend mit `6cfe9cdb97d807ec265aec45da3d13fa4f2c28a7` und bis
`4dee26fcff988fd408bc7df577de772373c4b765` zwölf geprüfte
`actions/setup-python`-Werte in acht Workflows von `3.12.13` auf `3.13`. Sie aktualisierten
`requirements-ci.lock` nicht; dessen Header und einziger PyYAML-Eintrag binden
den CI-Vertrag ausdrücklich an CPython `3.12.13`, das CP312-Wheel und SHA-256
`ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc`.

Auf dem exakten späteren Master `4dee26fcff988fd408bc7df577de772373c4b765`
verwendet der Hosted Runner Python `3.13.14`, lädt das CP313-Wheel von PyYAML
6.0.3 herunter und lehnt dessen SHA-256
`0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6` korrekt
als nicht zum CP312-only-Lock passend ab. `actionlint-and-contract`, `zizmor`,
`scaffold-lint` und `current-revision-advisory` scheitern alle bei **Install
hash-locked CI dependency**, bevor ihre vorgesehenen Controls laufen.

Dies ist eine spätere externe Master-Regression, kein Defekt des gemergten
PR-#27-Trees. Das strikte Hash-Control arbeitet fail closed. Der Befund ist ein
P1-Release-Blocker, weil vier Pflicht-Controls nicht laufen; er rechtfertigt
aber nicht, `--require-hashes` zu löschen, dem CP313-Wheel unter dem
CP312-Digest zu vertrauen oder einen Workflow- oder Security-Check
abzuschwächen.

## Scope, Reproduktion und Evidence

Betroffen sind die acht extern geänderten Workflow-Dateien
`.github/workflows/ci-security-workflow-lint.yml`, `.github/workflows/lint.yml`,
`.github/workflows/check-action-versions.yml`,
`.github/workflows/check-common-versions.yml`, `.github/workflows/ci-security-osv.yml`,
`.github/workflows/ci-security-quality.yml`,
`.github/workflows/ci-security-scorecard.yml`,
`.github/workflows/ci-security-secrets.yml` und `requirements-ci.lock`.
Betroffene Controls sind die `actions/setup-python`-`python-version`-Werte und
der hash-gesperrte Install-Schritt.

Nur lesende Reproduktionen:

```text
rtk git -C /var/tmp/codex/worktrees/framework-ci-security show --format= --unified=20 6cfe9cdb97d807ec265aec45da3d13fa4f2c28a7
rtk git -C /var/tmp/codex/worktrees/framework-ci-security show --format= --unified=20 8572da580e11bc3c62f6ef559152f49b30650056
rtk git -C /var/tmp/codex/worktrees/framework-ci-security show 8572da580e11bc3c62f6ef559152f49b30650056:requirements-ci.lock
rtk gh run view 29702454427 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
rtk gh run view 29702454412 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
```

Die GitHub-Evidence ist extern und wurde bewusst nicht in ein lokales Artifact
kopiert; ihr `sha256` ist daher `null`, statt einen Digest zu erfinden. Die
fehlgeschlagenen Job-Seiten sind [CI security workflow lint `29702454427`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29702454427)
und [lint `29702454412`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29702454412).
Der spätere Current-Snapshot bewahrt sie auch auf dem exakten Master
`4dee26...` in `actionlint-and-contract`, `zizmor`, `scaffold-lint` und
`current-revision-advisory`.

## Grundursache und erwartetes Verhalten

Die späteren Workflow-Edits behandelten `3.13` in acht Workflows als Ersatz für
den ausdrücklich geprüften Interpreter `3.12.13`, ohne die interpreter-spezifischen
PyYAML-Wheel-Lock-Metadaten zu aktualisieren und jeden Consumer zu validieren.
PyPI liefert korrekt ein anderes CP313-Wheel, dessen Digest nicht zum
CP312-Lock-Eintrag passen kann.

Jede Interpreterversion und jeder Wheel-Hash müssen einen geprüften, intern
konsistenten Vertrag bilden. Alle vier Controls müssen ihr beabsichtigtes
geprüftes Artifact installieren und anschließend laufen. Ein nicht passendes
Interpreter-/Artifact-Paar muss weiterhin von `pip --require-hashes`
abgelehnt werden.

## Remediation, Akzeptanz und Validierung

Der aktuelle Nutzer autorisierte einen normalen Framework-Master-Integration-
PR, und der Task wählte den kohärenten CPython-`3.13.14`-Pfad: Alle zwölf
aktiven `setup-python`-Werte verwenden exaktes `3.13.14` mit
`check-latest: false`, und Lock-Header sowie der einzige PyYAML-Eintrag
verwenden den geprüften CP313-Artifact-Hash
`0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6`.

Er bewahrt `--require-hashes`, Security-Tooling-Review, Workflow-Permissions,
Parent-Grenzen und die MRTS-Read-only-Grenze. Er pusht `master` nicht direkt,
unterdrückt den Fehler nicht und vertraut keinem nicht passenden Artifact.

- [verifiziert] Framework-PR #33 machte Interpreter- und Lock-Vertrag
  konsistent, ohne `--require-hashes` abzuschwächen.
- [verifiziert] Exakter PR-Head
  `e94029f5b893ef6a8efa118d21698426a43c82dd` bestand die anwendbaren Actions,
  CodeQL und das SonarQube-Cloud-Quality-Gate ohne Review oder Review-Thread.
- [verifiziert] Exakter resultierender Master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` führte
  `actionlint-and-contract`, `zizmor`, `scaffold-lint` und
  `current-revision-advisory` nach Installation des beabsichtigten Artifacts
  erneut erfolgreich aus.
- [verifiziert] Der CP313-Lock löst unter `--require-hashes` auf, während die
  bestehende negative Contract-Suite einen absichtlichen Provisioning-Mismatch
  weiterhin ablehnt.

## Abhängigkeiten, Blocker, verwandte Findings, Restrisiko und Historie

Die abgeschlossene Remediation hing von der geprüften Interpreter-/PyYAML-
Artifact-Entscheidung, GitHub-gehosteter Linux-Wheel-Verfügbarkeit,
Exact-Head-Validierung und resultierender-Master-Verifikation ab. Sie wurde
durch einen normalen Exact-Head-PR-Merge ausgeliefert; sie autorisierte oder
führte keinen direkten Push, keine GitHub-Setting-Änderung, kein Parent-Update
und keine MRTS-Mutation aus.

`FND-FRAMEWORK-0017` und `FND-FRAMEWORK-0020` bleiben eigenständige frühere
PR-#27-Controls. Ihre ursprüngliche Source-Evidence wird nicht ungültig; ihre
breite Current-Master-Verifikation ist lediglich kein Ersatz für die später
hier fehlgeschlagenen Controls. Dieses Finding ist kein Duplikat beider
Records.

Restrisiko: Auf Framework-master
`9a729226d2e040d07d7e7a4acebf201faf06ab37` verbleibt kein Defekt aus diesem
Finding. Der strikte Lock bleibt fail closed, und gehostete CPython-3.13.14-
Controls bestehen nun. Der unabhängige Master-SonarQube-Cloud-Backlog wird
getrennt als `FND-SONAR-0002` verfolgt und nicht dieser Reparatur zugeschrieben.

- `2026-07-19T20:32:09Z`: `external_post_merge_python_lock_regression_validated`
  — externe Commits änderten geprüfte Workflow-Werte `3.12.13` auf `3.13` und
  behielten den CP312-only-Lock. Exakter Master `8572da...` scheiterte in allen
  drei benannten Controls am strikten Install. In diesem Task wurde keine
  Remediation durchgeführt oder autorisiert.
- `2026-07-19T20:47:56Z`: `external_master_ci_regression_reconfirmed_and_expanded`
  — weitere externe Commits führten Master auf `4dee26...` weiter, änderten
  zwölf geprüfte Werte in acht Workflows und reproduzierten dieselbe strikte
  Abweichung in `actionlint-and-contract`, `zizmor`, `scaffold-lint` und
  `current-revision-advisory`. Dieser Task hat diese Änderungen weder erstellt,
  gemergt noch behoben.
- `2026-07-19T21:31:45Z`: `authorized_python_313_14_lock_remediation_started`
  — der aktuelle Nutzer autorisierte normale Framework-Integration. Der Task
  band alle zwölf aktiven Workflow-Uses an exaktes `3.13.14` mit
  `check-latest: false`, aktualisierte den Lock auf den verifizierten
  CP313-PyYAML-Digest und bestand die fokussierte lokale CI-Security-Matrix
  sowie die Target-Wheel-`--require-hashes`-Auflösung. Exact-Head- und
  resultierende-Master-Hosted-Evidence stehen aus.
- `2026-07-19T22:18:45Z`: `verified_after_exact_pr33_merge_and_master_reproduction`
  — Framework-PR #33 bestand seine Exact-Head-Actions und das SonarQube-Cloud-
  Quality-Gate ohne Reviews oder Threads und wurde dann normal am erwarteten
  Head `e94029f5b893ef6a8efa118d21698426a43c82dd` als Master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` gemergt. Alle vier ursprünglich
  betroffenen Controls bestanden; der CP313-versus-CP312-Mismatch reproduziert
  nicht mehr. Kein Hash-, Permission-, Parent- oder MRTS-Control wurde
  abgeschwächt.
