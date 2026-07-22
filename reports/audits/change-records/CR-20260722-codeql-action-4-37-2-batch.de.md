# Change Record: CodeQL-Action-4.37.2-Batch

**Sprache:** [English](CR-20260722-codeql-action-4-37-2-batch.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260722-codeql-action-4-37-2-batch` |
| Datum (UTC) | `2026-07-22` |
| Basis-Revision | `1e5e2fefce12ef455f4fdbc9a0afb7bb09ab4e7d` |
| Grenze | Nur Parent-CI-Security und Nachvollziehbarkeit; Framework, MRTS, Gitlinks und die Dependabot-PRs #82, #83 und #84 bleiben unverändert. |

## Motivation und Problemstellung

Die Dependabot-PRs #82, #83 und #84 aktualisierten jeweils unabhängig einen
Teil von `github/codeql-action` von v4.37.1 auf v4.37.2. Die
Immutable-Action-Registry lehnte jede Teilaktualisierung korrekt ab; außerdem
erzeugt die Aktualisierung nur von `init` oder `analyze` eine
CodeQL-Konfigurationsversionsabweichung. Dieser task-owned Ersatz wendet das
offizielle Release als einen konsistenten Batch an.

## Akzeptanzkriterien

- Jede Referenz von `github/codeql-action/init`,
  `github/codeql-action/analyze` und `github/codeql-action/upload-sarif`
  löst auf den vollständigen Commit
  `e0647621c2984b5ed2f768cb892365bf2a616ad1` mit ihrem v4.37.2-Kommentar auf.
- `ci/tooling/security-tools.lock.yml` enthält denselben v4.37.2-Commit.
- In den abgegrenzten Workflows bleibt keine CodeQL-Action-Referenz v4.37.1,
  kein veränderliches Action-Tag, keine gemischte CodeQL-Action-Version, keine
  unerwartete Action-Quelle, Permissions-Änderung, Trigger-Änderung oder
  Matrix-Änderung zurück.
- Fokussierte lokale Verträge und exakte PR-Checks bestehen vor der Delivery;
  Master-Ergebnisse werden ohne Zuschreibung eines unabhängigen Baseline-
  Fehlers an diesen Batch wahrheitsgemäß festgehalten.

## Implementierungsentscheidung und Begründung

Die Releasequelle ist das offizielle annotierte Tag `v4.37.2` von
`github/codeql-action`. Sein Tag-Objekt
`26dfab68fffc1cbc36c56970c32f0e53cf1fcc01` zeigt auf den offiziellen Commit
`e0647621c2984b5ed2f768cb892365bf2a616ad1`; das offizielle Release wurde am
2026-07-21 veröffentlicht. Die zehn bestehenden unveränderlichen
Workflow-Referenzen und der zugehörige Registry-Eintrag werden atomar
aktualisiert. Die unabhängigen Dependabot-PRs bleiben offen und sind erst nach
Delivery des Ersatz-Pull-Requests Kandidaten für eine später verifizierte
Supersedure-Disposition.

## Geänderte Dateien

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Offizielle GitHub-API-Inspektion von Release, Tag-Objekt und Ziel-Commit für `github/codeql-action` v4.37.2 | bestanden: Das offizielle annotierte Tag zeigt auf `e0647621c2984b5ed2f768cb892365bf2a616ad1`; seine Tag-Signatur ist unsigned. |
| CodeQL-Referenzinventur auf aktuellem `master` | bestanden: Vor diesem atomaren Update wurden genau zehn v4.37.1-Referenzen identifiziert, vier `init`, vier `analyze` und zwei `upload-sarif`. |
| `make check-ci-security-contract` | bestanden: die fokussierte Workflow-Security-Suite sowie die Lock-Parser-Validierungen für actionlint, zizmor und gitleaks bestanden. |
| Scoped-v4.37.2-Referenzinventur und `git diff --check` | bestanden: genau zehn Ersatzreferenzen bleiben (vier `init`, vier `analyze`, zwei `upload-sarif`), keine v4.37.1-SHA bleibt in den abgegrenzten Workflows, und das Registry-Paar stimmt überein. |
| Codex-Security-Diff-Scan | bestanden: alle acht geänderten Dateien erhielten vollständige Review-Receipts; der einzige Kandidat wurde mit Evidence unterdrückt, und kein reportable Finding überlebte. |
| `make check-bilingual-docs` | blocked_environment: Der absichtlich nicht ausgefüllte Framework-Gitlink hat bereits fehlende Link-Ziele; der Checker meldete keinen Fehler für dieses neue englisch/deutsche Change-Record-Paar. |

## Security-Auswirkung

Dies ist eine Supply-Chain- und CI-Security-Änderung. Jeder CodeQL-Action-Aufruf
bleibt ein offizieller vollständiger unveränderlicher Release-Commit; Registry,
`init`, `analyze` und `upload-sarif` verwenden dasselbe Release. Bestehende
minimale Permissions, Action-Quellen, CodeQL-Scope, Trigger, Secret-Handling
und Security-Checks bleiben erhalten. Kein Scanner, Quality Gate oder Schutz
wird abgeschwächt.

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Die aktuellen Dependabot-Job-
Logs zeigten, dass Teilaktualisierungen an der Immutable-Action-Registry
scheitern und Teilaktualisierungen von `init` oder `analyze` die
CodeQL-Versionskonsistenz verletzen; dieser Batch beseitigt beide Teilzustände
konstruktiv.

## Bekannte Einschränkungen

Der GitHub-Signaturstatus des offiziellen annotierten Tags ist `unsigned`.
Die Verifikations-Evidence stützt sich daher auf das offizielle
Upstream-Repository, Release, annotierte Tag-Ziel und den vollständigen
Commit-SHA statt auf eine Tag-Signaturbehauptung.

Das lock-weite `checked_at` bleibt auf `2026-07-16`. Dieser Batch hat die
CodeQL-Zuordnung einzeln revalidiert, aber nicht jeden Lock-Eintrag; ein
Verschieben des globalen Datums würde daher eine falsche Gesamtbestätigung des
Locks behaupten.

## Verbleibende Risiken

Der Batch kann Upstream-Action-Risiko nicht eliminieren. Das Pinnen des
offiziellen vollständigen Release-Commits, das Beibehalten der Registry-Evidence
und die unveränderten bestehenden CI-Security-Kontrollen begrenzen dieses
Dependency-Risiko. Es wird kein Risiko akzeptiert.

## Delivery- und finales Review-Ergebnis

Die aktuelle Benutzeranweisung wählte die Parent-PRs #55, #73, #74, #77, #79,
#80, #82, #83 und #84 ausdrücklich für die `master`-Integration aus. Der
task-owned Ersatz-PR [#85](https://github.com/Easton97-Jens/ModSecurity-conector/pull/85)
verwendete `agent/codeql-action-v4372-batch`; lokale, Remote- und PR-Heads
stimmten vor dem geschützten Squash-Merge auf
`35914dccb6e5406fb753d7fbb184b12dfbfe45d5` überein. Die erforderlichen
Checks `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint` und
`zizmor` bestanden; ebenso PR-CodeQL, OSV und das SonarQube-Cloud-Quality-Gate
mit null neuen Issues/Hotspots. GitHub meldete null Reviews und Threads.

GitHub mergte #85 am `2026-07-22T16:57:14Z` als Master
`784d79b4e399e2cb64314a3ba63dcf1633c672bd`. GitHub Actions, CodeQL, OSV,
Scorecard-, Connector-, Governance- und drei Dependabot-Update-Checks
bestanden. Das externe Master-Sonar-Quality-Gate scheiterte nur wegen dreier
bereits bestehender `TO_REVIEW`-`python:S5332`-Hotspots aus `FND-SONAR-0001`,
keiner im Acht-Dateien-Batch-Diff. Es gab kein Hotspot-Review, keine
Unterdrückung, keine Quality-Gate-Änderung und keine Source-Änderung. Die
Wiederherstellung der Parent-Wurzel wurde nicht versucht, weil das unabhängige
Gate weiter fehlschlägt; Originale #82/#83/#84 wurden nicht geändert oder
geschlossen und avancierten später unabhängig auf v4.37.3.

## Nicht ausgeführte Prüfungen mit Begründung

Der vollständige Bilingual-Check ist wegen des absichtlich nicht ausgefüllten
Framework-Gitlinks umgebungsbedingt blockiert und nicht als bestanden markiert.
Alle beobachteten #85-PR- und resultierenden-Master-Ergebnisse stehen oben.

## Finaler Diff- und Review-Status

Der ausgelieferte v4.37.2-Diff war auf zehn koordinierte CodeQL-Pins, den
passenden Immutable-Lock-Eintrag, dieses bilinguale Paar und dessen Indizes
begrenzt. Fokussierte Security-Diff-Analyse und lokale Validierung bestanden.
Sein Master-Sonar-Fehler ist eine separat getrackte bestehende Baseline-
Bedingung und keine erfolgreiche vollständige Master-Verifikation.
