# FND-GITHUB-0008 — Framework-Workflow-Tool-Publisher bleibt bis zur Konfiguration seiner dedizierten GitHub-App blockiert

## Identität

| Feld | Wert |
| --- | --- |
| Kategorie | `ci_failure` |
| Repository / Ownership | `framework` / `github_configuration` |
| Priorität / Schweregrad / Konfidenz | `P1` / `not_applicable` / `confirmed` |
| Status / Machbarkeit | `accepted_risk` / `out_of_scope` |
| Release-Blocker / Security-relevant | `true` / `true` |
| Historischer Run / Source-Revision | `30190898961` / `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` |
| Aktueller Run / Source-Revision | `30195702432` / `c27c644e088904b71b8380d16ee34f1b36f2c001` |
| Aktueller fehlgeschlagener Job / Step | `89776795329` / `Mint repository-limited workflow publisher App token` |

## Zusammenfassung

Der ursprüngliche Native-Token-Fehler ist in der Source behoben: Framework-PR
[#46](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/46)
wurde als `c27c644e088904b71b8380d16ee34f1b36f2c001` gemergt. Seine Source hält
das native Publisher-Token auf `contents: read` und verwendet ein gepinntes,
kurzlebiges repository-limited GitHub-App-Token nur in vier überprüften
Publisher-Consumern.

Der manuelle `workflow_dispatch`-Run #2 erreichte Publisher nach erfolgreichen
Resolver- und Validator-Jobs, scheiterte aber fail closed vor der Ausgabe eines
Tokens. Sein notwendiger Input `WORKFLOW_UPDATER_APP_CLIENT_ID` ist leer. Das
secret-freie Name-only-Inventar lieferte außerdem keine Repository-Variablen-
oder Secret-Namen. Dies ist derselbe externe GitHub-App-Konfigurations-
Lifecycle wie beim ersten Fehler, kein neuer Framework-Source-Defekt. Parent,
sein Framework-Gitlink und MRTS bleiben out of scope und unverändert.

## Beobachtetes und erwartetes Verhalten

Der historische Run `30190898961` validierte einen Fünf-Dateien-Kandidaten,
aber GitHub lehnte seinen Native-`github.token`-Workflow-Datei-Push wegen
fehlendem App-Level-`Workflows: write` ab. Die gemergte Source-Remediation
ersetzte diesen nativen Publisher-Pfad durch:

```yaml
permissions:
  contents: read
uses: actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1 # v3.2.0
with:
  client-id: ${{ vars.WORKFLOW_UPDATER_APP_CLIENT_ID }}
  private-key: ${{ secrets.WORKFLOW_UPDATER_APP_PRIVATE_KEY }}
  owner: ${{ github.repository_owner }}
  repositories: ${{ github.repository }}
  permission-contents: write
  permission-pull-requests: write
  permission-workflows: write
```

Der aktuelle Run `30195702432` (Run #2, `workflow_dispatch`, Framework-
`master` `c27c644e088904b71b8380d16ee34f1b36f2c001`) beendete Resolver und
Validator. Publisher-Job `89776795329` scheiterte nur beim Token-Minting; alle
späteren API-, Branch-, Push- und Draft-PR-Steps wurden übersprungen. GitHub
meldete:

```text
The 'client-id' (or deprecated 'app-id') input must be set to a non-empty string.
If using a secret or variable, ensure it is available in this workflow context.
```

Erwartet ist, dass ein gültiger allowlisted Workflow-Pin-Kandidat nach
autorisierter externer Konfiguration das eingeschränkte App-Token mintet, nur
den festen Maintenance-Branch pusht und genau einen passenden Draft-PR erzeugt
oder aktualisiert. Resolver und Validator müssen read-only und credential-frei
bleiben; der Updater darf `master` nicht ändern.

## Auswirkung, betroffene Fläche und Voraussetzungen

Die automatisierte Veröffentlichung geprüfter Immutable-Action-/Tool-
Maintenance bleibt bis zur externen App-Konfiguration nicht verfügbar. Das
Fail-closed-Verhalten verhindert, dass ein breites Token, direkter `master`-
Push oder unbeabsichtigte Secret-Offenlegung diese Konfiguration ersetzt.

Betroffene Source ist `.github/workflows/update-workflow-tools.yml`; relevante
Symbole sind `Mint repository-limited workflow publisher App token`,
`WORKFLOW_UPDATER_APP_CLIENT_ID` und `WORKFLOW_UPDATER_APP_PRIVATE_KEY`.
Voraussetzungen sind erfolgreiche Resolver-/Validator-Completion und ein
Publisher-Versuch, das dedizierte App-Token zu minten. Ein späterer Kandidat
kann einen allowlisted `.github/workflows/*`-Pfad ändern.

## Evidenz und Reproduktion

| Feld | Historischer Run #1 | Aktueller Run #2 |
| --- | --- | --- |
| Run-ID | `20260726T063152Z-framework-update-pinned-workflow-tools-1` | `20260726T090147Z-framework-update-pinned-workflow-tools-2` |
| GitHub-Run | `30190898961` | `30195702432` |
| Artifact-Pfad | `.codex/runs/20260726T063152Z-framework-update-pinned-workflow-tools-1/evidence/framework-update-pinned-workflow-tools-run-1-receipt.md` | `/var/tmp/codex/ModSecurity-conector/runs/20260726T090147Z-framework-update-pinned-workflow-tools-2/evidence/framework-update-pinned-workflow-tools-run-2-receipt.md` |
| Artifact-Typ | `github_actions_workflow_publisher_permission_failure_receipt` | `github_actions_workflow_publisher_missing_client_id_receipt` |
| SHA-256 | `310ff8dc82ce5b3bb58d1da7ed93b16b8fb5231b757af6000f6125a71df9254f` | `537bf3001c99be6615a9ea0c02b091556baa3ef0a5758177d28ec8931c890592` |
| Beobachtet am | `2026-07-26T06:31:52Z` | `2026-07-26T09:07:01Z` |
| Retention | `retained_sealed_local_control_plane` | `retained_sealed_external_task_evidence` |

Der aktuelle Receipt liegt im task-owned externen Root, weil der kanonische
`.codex/runs`-Mount read-only ist; das kanonische Finding enthält seinen exakten
Pfad und Checksum. Keiner der Receipts behält einen Credential-Wert.

Sicher reproduzieren mit `rtk proxy -- gh run view 30195702432 --repo
Easton97-Jens/ModSecurity-test-Framework --log-failed`, `rtk proxy -- git
show origin/master:.github/workflows/update-workflow-tools.yml`, `rtk proxy --
gh variable list --repo Easton97-Jens/ModSecurity-test-Framework` und `rtk
proxy -- gh secret list --repo Easton97-Jens/ModSecurity-test-Framework`.
Die Inventare sind name-only und dürfen niemals zum Lesen oder Ableiten von
Secret-Werten verwendet werden.

## Root Cause und Remediation

Der vorherige Native-Token-Autoritätsdefekt wurde durch den gemergten PR #46
korrigiert. Run #2 beweist, dass die aktuelle Source bei ihrer ersten externen
Voraussetzung stoppt: Die Repository-Variable
`WORKFLOW_UPDATER_APP_CLIENT_ID` fehlt. Private-Key-Secret, dedizierte App-
Installation und exakte App-Permissions bleiben unverifiziert, weil Token-
Minting ohne diese Client-ID nicht beginnen kann.

Ein autorisierter Repository-Owner muss:

1. Eine dedizierte GitHub-App erstellen oder konfigurieren und sie **nur** auf
   `Easton97-Jens/ModSecurity-test-Framework` installieren.
2. Genau `Contents: write`, `Pull requests: write` und `Workflows: write` als
   Repository-Permissions geben.
3. Repository-Actions-Variable `WORKFLOW_UPDATER_APP_CLIENT_ID` und
   Repository-Actions-Secret `WORKFLOW_UPDATER_APP_PRIVATE_KEY` setzen, ohne
   den Private Key an Codex, Source, Logs oder Evidenz offenzulegen.
4. Den Updater erneut ausführen und seinen eingeschränkten Maintenance-Branch
   sowie passenden Draft-PR verifizieren.

Keinen `github.token` oder `GITHUB_TOKEN`-Publisher-Fallback zurückbringen,
kein Personal-Access-Token nutzen, keinen breiteren Installations-Scope geben,
keine Workflow-Checks abschwächen und `master` nicht direkt pushen.

## Akzeptanzkriterien und Validierungsplan

1. Die dedizierte App ist nur auf diesem Repository mit `Contents`, `Pull
   requests` und `Workflows` Write-Permission installiert; kein Credential-
   Wert erreicht Source, Evidenz, Logs, Resolver oder Validator.
2. Der autorisierte Owner konfiguriert `WORKFLOW_UPDATER_APP_CLIENT_ID` und
   `WORKFLOW_UPDATER_APP_PRIVATE_KEY`, ohne den Private Key offenzulegen.
3. `master` behält die gepinnte App-Token-Source und hat keinen
   `github.token`- oder `GITHUB_TOKEN`-Publishing-Fallback.
4. Ein neuer Updater-Run erzeugt oder aktualisiert genau einen passenden Draft-
   PR über den eingeschränkten Maintenance-Branch, ohne direkte `master`-
   Änderung.
5. Der Draft-PR bleibt innerhalb der validierten allowlisted Kandidatenfläche.

Validierung besteht aus dem name-only Konfigurations-Readback, Source-Review
und einem neuen kontrollierten Updater-Run. Der Security-Control-Case ist ein
Workflow-Pin-Kandidat, der den Draft-PR ohne Credential-Offenlegung oder
`master`-Änderung erzeugt. Regression-Evidenz sind die CI-Security-/Action-
Pin-Validierung von PR #46 und sechs erfolgreiche merge-triggered Framework-
`master`-Push-Workflows auf `c27c644e088904b71b8380d16ee34f1b36f2c001`; sie
ersetzen den erforderlichen End-to-End-Updater-Rerun nicht.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Abhängigkeiten sind aktuelle Repository-Owner-Autorisation für GitHub-App-
Installation plus Actions-Variable-/Secret-Konfiguration und eine repository-
limited App mit den genannten Permissions. Blocker sind die fehlende
`WORKFLOW_UPDATER_APP_CLIENT_ID`, das leere name-only Repository-Actions-
Secret-Inventar (also ist `WORKFLOW_UPDATER_APP_PRIVATE_KEY` nicht konfiguriert)
und unverifizierte App-Installation/-Permissions.

Verwandte Findings sind `FND-GITHUB-0005`, `FND-FRAMEWORK-0047` und
`FND-FRAMEWORK-0048`. Restrisiko ist der weiter fehlende automatisierte
Security-Maintenance-Veröffentlichungspfad. Dieses aktuelle Diagnosetask führte
keine Risiko-Akzeptanz, Source-Workaround-, GitHub-Setting-, Secret-, Branch-,
PR-, Merge-, Parent-Gitlink- oder MRTS-Änderung aus.

## Source-Remediation- und Historie-Update

PR #46 mit finalem Head `781b5603975369dd9b9a1661edc417dd37f5dfa7` wurde um
`2026-07-26T08:58:11Z` als Framework-`master`
`c27c644e088904b71b8380d16ee34f1b36f2c001` gemergt. Seine normalen Exact-
Head-PR-Checks bestanden; alle sechs merge-triggered `master`-Push-Workflows
bestanden ebenfalls. Der manuelle Updater-Run #2 ist ein separates
`workflow_dispatch`-Event und bleibt die erforderliche End-to-End-Validierung.

- `2026-07-26T06:21:44Z`: Historischer Publisher-Push wurde wegen fehlender
  nativer App-`Workflows: write`-Autorität abgelehnt.
- `2026-07-26T08:58:11Z`: PR #46 mergte die Source-only-App-Token-Grenze.
- `2026-07-26T09:01:47Z`–`2026-07-26T09:02:36Z`: Run #2 scheiterte fail closed,
  weil `WORKFLOW_UPDATER_APP_CLIENT_ID` leer war; keine spätere Publisher-
  Aktion lief.
- `2026-07-26T09:07:01Z`: Secret-freier Receipt und dieses kanonische Finding
  wurden aktualisiert. Der historische Status blieb `blocked` /
  `blocked_permissions`.

## Aktuelle Nutzer-Accepted-Risk-Archiv-Disposition — 2026-07-26

Um `2026-07-26T14:18:25Z` akzeptierte der aktuelle Nutzer dieses exakte
Restrisiko ausdrücklich für die lokale Archivierung. Die automatisierte
Veröffentlichung geprüfter unveränderlicher Workflow-/Tool-Wartungsupdates
bleibt nicht verfügbar, weil dedizierte GitHub-App, Client-ID-Variable und
Private-Key-Secret nicht konfiguriert sind. Der fail-closed Workflow darf
keinen `github.token`-, Personal-Token-, Pin-, Validierungs-, Scope-,
Credential-Isolation- oder Default-Branch-Protection-Workaround erhalten. Der
Status ist `accepted_risk`, nicht `closed`; vor Produktion, Veröffentlichung
oder Release muss der Record wiederhergestellt und neu validiert werden.
