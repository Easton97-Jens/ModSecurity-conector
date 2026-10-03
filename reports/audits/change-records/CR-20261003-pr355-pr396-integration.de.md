# Change Record: Integration von PR #355 in den Nachfolger von PR #396

**Sprache:** [English](CR-20261003-pr355-pr396-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261003-pr355-pr396-integration` |
| Datum (UTC) | `2026-10-03` |
| Basis-Revision | `ac4c746f6a4c07006f25b078f660e31b16341479` |
| Ursprüngliche PR-#355-Base | `b779167ff979aa73cdd9321a829f9c693d943760` |
| Ursprünglicher PR-#355-Head | `b42ebda511cb9b6dca1de5c23b1b7b55ee400fd8` |
| Lokaler Checkpoint der geordneten Portierung | `0cfb8f900cbc3839c1590ba6f90683ab144ac7ef` |
| Framework-Head zu Beginn | `2e721082d2d2bdead188995aeb7c9151a6dd518b` |
| Aktueller Framework-Dokumentationsnachfolger | `b9b9534b7e0b15edad31393699ebd0617748148d` |
| Parent-Callback-Korrektur | `28ecd53d61f9b9065ba687ead373dcae53969368` |
| Strikte Parent-Artefakt-Korrektur | `3dcd9980cece2afec29dad61ec824b3f63cc84f7` |
| Parent-Abhängigkeitsbindungscheckpoint | `2c880b9319abb381daa29a073669d1668eba1a82` |
| Collector-Revision zu Beginn, Parent-Vorfahr | `8fe56043968fa4989f5dcf4f5b48f24dbeb3fe6f` |
| MRTS, nur lesend | `615b13bacbd008562c17408246c41ab27dca3104` |
| Zuletzt beobachteter Remote-Head von PR #396 | `2634d821acd80ad208a8e1cd3e4f49fd7e80c628` |
| Delivery-Status | Framework zu Draft PR #135 veröffentlicht; Parent-Remote-Delivery steht aus; PR #355 und PR #396 OPEN/DRAFT/UNMERGED |

## Motivation und Problemstellung

PR #355 enthält den geschützten NGINX-Exact-Head-Workflow und die privilegierte
Ausführungsgrenze. PR #396 ist der Nachfolger mit neuerer Lifecycle-,
Konfigurations- und Canonical-Arbeit. Ihre Historien sind divergiert; die
vollständige Integration des älteren Security-Vertrags muss das neuere
Verhalten erhalten und jeden ursprünglichen Commit und jede Datei nachweisen.
Das Schließen von PR #355 erfordert verifizierte Remote-Ablösung durch
PR #396 und nicht lediglich eine lokale Portierung.

## Akzeptanzkriterien

Alle 19 ursprünglichen Commits und 25 ursprünglich geänderten Dateien
nachweisen. Dispatcher, Trusted-Base-Identität, genaue Candidate-Head-Prüfung,
Artefakt-Digests, private Runner-/Root-Grenze, Launcher mit gehaltenen
Deskriptoren, Worker-Trennung, root-eigene Evidence, begrenztes Cleanup und
Fail-Closed-Prüfungen erhalten. Geschützte Tests und aktuelle
Parent-/Framework-/Collector-Regressionen erneut prüfen; die geschlossenen
Records `empty_header_value`, `invalid_boolean` und `invalid_size` erhalten.
Protocol-Wiring separat und MRTS unverändert halten. Erst nach bestandenen
Gates, korrekten Abhängigkeitsreferenzen, verifiziertem Push/Readback von
PR #396 und relevanter Remote-CI darf PR #355 ohne Merge geschlossen werden.
Weder ein Full-E2E-Lauf noch Exact-Head E2E PASS gehört zu dieser
Integrationsphase.

## Implementierungsentscheidung und Begründung

Ein isolierter autoritativer Parent-Worktree basiert auf dem committeten
lokalen Nachfolger; uncommittetes Protocol-Wiring bleibt im ursprünglichen
Checkout. Siebzehn Nicht-Merge-Commits von PR #355 wurden in Reihenfolge mit
`-x`-Provenance cherry-gepickt. Die beiden Upstream-Merge-Commits referenzieren
Vorfahren, die durch die neuere Base bereits erfüllt sind; sie werden separat
nachgewiesen und nicht als konkurrierender Branch-Merge wiederholt. Der
lokale Portierungscheckpoint ist `0cfb8f900cbc3839c1590ba6f90683ab144ac7ef`;
dies ist keine finale verifizierte oder remote verfügbare Nachfolgeridentität.
Ancestry, ursprüngliche Blobs und die Indexvereinigung erfassen alle 19 Commits
und 25 Nettopfade im finalisierten Maschinennachweis: 17 geordnete `-x`-
Portierungen, die beiden Upstream-Merge-Commits
(`5368569351e968e8ea641fc485590654df6a4336` und
`acc0ca1d22fd8a452453e66f51115ce026517b52`) als nachgewiesene Vorfahren,
23 bytegleiche Nettopfade und zwei Archivindizes mit
einer ausschließlich additiven Vereinigung. Die Abdeckung beträgt 19/19
Commits und 25/25 Dateien; dies bestätigt nicht alle semantischen oder
Delivery-Gates.

Der EN/DE-Archivindexkonflikt wird als Vereinigung gelöst: aktuelle Records,
Protected-Base-Eintrag und korrekten englischen Link erhalten. Die historische
23-Pfade-Checkliste wird um die beiden Review-Package-Pfade des finalen
25-Pfade-Umfangs präzisiert, ohne historische Evidence zu ändern.

Die aktuelle Kompatibilitätsprüfung fand einen `&&`/`||`-Callback-Guard, der
die gültige Kombination `on` mit Callback `1` in einer echten Shell-Reproduktion
ablehnte (Exit 19). Die Test-first-Korrektur bestand neun Callback-Kontrollen.
Die Builder-Anpassung erhält strikte Source-/Artefakt-Admission beim Abgleich
des aktuellen nativen Source- und Bibliothekseingabelayouts. Builder- und
Launcher-Prüfungen bestanden 23 und 46 Tests. Eine Collector-Regression
zwischen Produzenten schlug vor der Korrektur ebenfalls fehl und bestand
danach: Nur zwei Collector-Konstanten wurden auf NGINX `1.31.5` und den
Source-Digest `e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279`
abgeglichen; 19 Collector-Tests bestanden. Die Collector-Revision oben ist ein
Parent-Vorfahr und kein separates Repository oder eigenständige Delivery-Grenze.

Der historische Referenzaudit ergab, dass Framework
`2e721082d2d2bdead188995aeb7c9151a6dd518b` unveröffentlicht war und der damals
aktuelle Gitlink `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` die
Boolean-/Size-Belege nicht konsumieren konnte. Der ausschließlich
dokumentarische Nachfolger `b9b9534b7e0b15edad31393699ebd0617748148d`
wurde nun separat ohne Force-Push zu
[Framework Draft PR #135](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/135)
veröffentlicht, beobachtet OPEN/DRAFT/UNMERGED. Seine sechs Remote-CI-Jobs
sind queued und nicht PASS. Der dedizierte Parent-Gitlink-Commit
`2c880b9319abb381daa29a073669d1668eba1a82` bindet diesen Framework-Nachfolger
und unverändertes MRTS `615b13bacbd008562c17408246c41ab27dca3104`. Die
Master-Base- und Base-Equal-Gitlink-Anforderungen des geschützten Workflows
bleiben durchgesetzt. Der gestapelte PR #396 ist unter diesem unveränderten
Vertrag für manuelle geschützte Ausführung nicht zugelassen.
Der ausschließlich dokumentarische Framework-Nachfolger ist jetzt
`b9b9534b7e0b15edad31393699ebd0617748148d`; Code, Tests und Katalog bleiben
identisch zu `2e721082d2d2bdead188995aeb7c9151a6dd518b`.

## Security-Auswirkung

Keine Kontrolle darf für ein bestandenes Integrationsergebnis gelockert werden.
Candidate-Callback- oder JSONL-Werte bleiben untrusted Beobachtungen und keine
Root-Attestierung. Geschützte Workflow-Berechtigungen, Actor-/Repository-/
Base-Prüfungen, Runner-Preflight, genaue Artefakt-Admission, Evidence-Readback
und den privaten Root-Parent-Cleanup-Vertrag von FND-PARENT-1038 erhalten.
FND-PARENT-1038 bleibt `in_progress`; FND-PARENT-1036 bleibt
`blocked_external_dependency`. Portierte Quellen und lokale Tests erfüllen
keine externen Protected-Host- oder Security-Archiv-Anforderungen.

## Geänderte Dateien

Das ursprüngliche PR-#355-Nettoinventar enthält diese 25 Pfade; die lokale
Portierung liegt vor und ist durch den finalisierten Maschinennachweis
abgedeckt; verbleibende Validierungs- und Delivery-Gates sind separat:

- `.github/actionlint.yaml`
- `.github/workflows/run-protected-nginx-exact-head.yml`
- `ci/runtime/broker/nginx_exact_head_result_collector.py`
- `ci/runtime/broker/nginx_exact_head_root_launcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_builder.py`
- `ci/runtime/broker/protected_nginx_exact_head_dispatcher.py`
- `ci/runtime/broker/protected_nginx_exact_head_runner_preflight.py`
- `ci/runtime/broker/run_nginx_exact_head_cells.sh`
- `docs/security/protected-exact-head-host-gate.md`
- `docs/security/protected-exact-head-host-gate.de.md`
- `docs/security/protected-exact-head-nginx.md`
- `docs/security/protected-exact-head-nginx.de.md`
- `docs/security/protected-exact-head-review-package.md`
- `docs/security/protected-exact-head-review-package.de.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.md`
- `reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `tests/test_nginx_exact_head_base_helper.py`
- `tests/test_nginx_exact_head_result_collector.py`
- `tests/test_nginx_exact_head_root_launcher.py`
- `tests/test_protected_nginx_exact_head_builder.py`
- `tests/test_protected_nginx_exact_head_dispatcher.py`
- `tests/test_protected_nginx_exact_head_runner_preflight.py`
- `tests/test_protected_nginx_exact_head_workflow.py`

Dieses gepaarte Integrationsrecord ist zusätzliches Traceability-Material.
Externe Nachweisartefakte sind `pr355-full-integration.csv`,
`pr355-integration-summary.md`, `pr355-file-coverage.csv` und
`pr355-commit-coverage.csv` unter
`/var/tmp/codex/ModSecurity-conector/analysis/`. Der erforderliche Nachweis
erfasst 19/19 Commits und 25/25 Dateien ohne `UNKNOWN`, `IGNORED` oder
`DROPPED`. Der finalisierte Nachweis erfüllt beide Zahlen; dies behauptet
nicht, dass alle Verifikationsgates bestanden wurden.

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

Das ursprüngliche Inventar durch `rtk proxy git diff --name-only` bestätigte
25 geänderte Pfade. Der Koordinator beobachtete aktuelle RTK-verpackte Ergebnisse:

- Kombinierte geschützte Suite: 139 Tests bestanden; unabhängige fokussierte Suite: 75 Tests bestanden.
- Callback-Kontrollen: Test-first-Fehlschlag, dann neun bestandene Tests; Builder: 23 bestanden; Launcher: 46 bestanden; Collector zwischen Produzenten: Test-first-Fehlschlag, dann 19 bestanden.
- Parent-Security-Suite: 164 Tests, Exit 0, mit fünf übersprungenen Tests. Zwei benötigen die nicht verfügbare `nobody`-Identität in diesem User-Namespace; einer benötigt eine nicht verfügbare dedizierte unprivilegierte Identity-Capability; zwei benötigen nicht verfügbare Mount-/PID-Namespace-Capability. Genaue Skip-Evidence liegt in `analysis/pr355-parent-gates-20261003.log` unter externem Taskspeicher.
- actionlint, ShellCheck auf Fehlerstufe für die ermittelten tatsächlichen Pfade, Syntax- und Diff-Prüfungen: Exit 0. Der erste ShellCheck-Befehl mit fehlerhaften Pfaden bleibt als Diagnose erhalten und ist kein bestandener Nachweis.
- Native Bilingual- und Dokumentationslink-Prüfungen bestanden nach Materialisierung von Framework `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` im Worktree. Dies behebt die früheren fehlenden relativen Linkziele; es verifiziert nicht die Kompatibilität dieser alten Referenz mit neueren Belegen.
- Aktuelle Framework-No-CRS-Suite am finalen Head: 166 bestanden; API: 23 bestanden, bei `b9b9534b7e0b15edad31393699ebd0617748148d`.
- Framework-Lint scheiterte zunächst an einer bestehenden FIFO-/Spawn-Messung (Versuch 3 ohne Readiness). Drei isolierte Wiederholungen des unveränderten Tests bestanden alle neun strikten Versuche. Ein zweiter vollständiger Lint-Lauf bestand die schweren Provenance-/Archivfälle und scheiterte danach an einer falsch geerbten `FRAMEWORK_ROOT`-/Tool-Repository-Identität. Dieser Aufruffehler ist kein nachgewiesener neuer Source-Defekt. Der finale vollständige Lint-Lauf mit explizitem `FRAMEWORK_ROOT` und Environment-Roots (Session `60548`) endete mit Exit 0: PASS.
- Breitere Parent-Suite: terminal FAIL, 816 Tests. Im angeforderten 810-Test-Umfang waren 809 grün und ein Sandbox-UID-Test schlug fehl. Eine genaue Root-zu-`nobody`-Materializer-Unit-Wiederholung auf dem Host bestand ihren einen Test; sie erzeugte keine NGINX-Requests. Die sechs zusätzlichen Multi-Connector-Tests ergaben 14 Subtest-Fehlschläge und einen Fehler, reproduziert an Base `ac4c746f6a4c07006f25b078f660e31b16341479` mit unveränderten Quellen. Keine Regression im PR-#355-Umfang wurde nachgewiesen; das vollständige fehlgeschlagene Log bleibt erhalten und der breite Lauf wird nicht als PASS umbenannt.
- Zusätzliches natives Parent-Lint scheiterte zuerst an einer alten Apache-`OUT`-Bedingung; sein zweiter Lauf scheiterte an einer CLI-/Make-Root-Override-Fixture. Die isolierte 20-Test-Prüfung der Environment-Root-Bindung bestand. Der finale native Lint-Lauf (Session `20449`) wurde gemäß Job-Ressourcenvertrag absichtlich mit Exit 143 beendet: Die tatsächliche Host-Ausführung fand fehlende HAProxy-Header und begann einen großen libmodsecurity-Build trotz deaktivierter Runtime-Freigabe. Im ausgewählten Cache wurden keine echten HAProxy-Header für eine begrenzte Wiederholung gefunden. Zusätzliches vollständiges Parent-Lint bleibt UNVERIFIED; kein weiterer Source-Fix wird behauptet.
- Unabhängige native CI-konsumierte Targets `check-common-sdk-contract`, `check-adapter-contracts` und `check-directive-parity` bestanden jeweils mit Exit 0. Diese Targets rufen die sechs Baseline-Multi-Connector-Module nicht auf. Der angeforderte 810-Test-Umfang ist durch die 809 grünen Tests plus die genaue Host-Ownership-Wiederholung erfüllt; geschützte 139, Statik, Security, Dokumentation und vollständige Framework-Gates bestanden. Der separate breite 816-Test-Lauf bleibt FAIL.
- Die 47 Prüfsummen des ursprünglichen Size-Configtest-Bundles bestanden erneut. Dies revalidiert die ursprünglichen Source-/Artefakt-/Run-Identitäten und keine Runtime des aktuellen Heads.
- Der historische Parent-Abhängigkeitsfokus mit 99 Tests vor der Gitlink-Bindung endete mit drei korrekten Provenance-Guard-Skips. Die finale Wiederholung nach der Bindung (Session `21082`) bestand alle 99 Tests ohne Skips in 19.276 Sekunden, Exit 0; alle Identitätskontrollen wurden mit Framework-Gitlink `b9b9534b7e0b15edad31393699ebd0617748148d` ausgeführt.
- Der Sonar-Readback für den aktuellen Head von Framework PR #135 meldet Quality Gate `OK`, null Bugs und Vulnerabilities sowie 28 offene Wartbarkeitsbefunde. Dies ist kein Nullbefund- oder Runtime-Claim; Parent-Analyse am aktuellen Head und Remote-CI bleiben separate Delivery-Gates.

Nach dieser Record-Aktualisierung bestand
`rtk proxy make check-bilingual-docs check-doc-links PYTHON=python3 BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/build/pr355-integration-docs`
mit Exit 0, einschließlich Repository-Pfadreferenzen; die wiederholte
Prüfung `rtk proxy git diff --check` endete ebenfalls mit Exit 0.

Historische 98/99/129-Test- und Sonar-Checkpoints im älteren Change Record
bleiben historisch und beweisen den integrierten Nachfolger nicht.

## Runtime-Evidence

Es wird keine neue Protected-Host-Runtime oder unabhängige Host-Attestierung
behauptet. Die frühere ausgewählte Configtest-Evidence und ihre
Prüfsummenbelege behalten ihre eigene Source-/Artefakt-/Run-Identität;
sie beweisen keine Runtime dieser Integration. Exact-Head E2E PASS: NO.

## Nicht ausgeführte Prüfungen mit Begründung

Full Exact-Head E2E ist ausdrücklich aufgeschoben. Framework-Veröffentlichung
und lokale Parent-Gitlink-Bindung sind abgeschlossen; dieser Checkpoint
umfasst jedoch keinen Parent-Push, PR-#396-Nachfolger-Readback, bestandene
Remote-CI-Bestätigung oder Schließung von PR #355. Dies sind bedingte spätere
Delivery-Schritte. Protected-Host-Bootstrap, Environment, dedizierter Runner
und unabhängige Attestierung bleiben externe Voraussetzungen; fehlende
Host-Evidence kann nicht durch Source-Test, Build, Konfigurationsladen oder
ausschließlich clientseitige Beobachtung ersetzt werden.

## Bekannte Einschränkungen

Commit-Provenance und Dateipräsenz unterscheiden sich von vollständiger
Äquivalenz. Verbleibende Remote-Gates müssen vor der Remote-Ablösung
abgeschlossen sein.
Vollständiges Framework-Lint bestand; das zusätzliche optionale vollständige
Parent-Lint bleibt nach Beendigung gemäß Ressourcenvertrag UNVERIFIED.
Der breitere Parent-Lauf bleibt FAIL mit der oben beschriebenen fokussierten
Wiederholung und Baseline-Reproduktion.
Die Coverage zu Beginn betrug 97
ausgewählte, 51 offene Required- und 8 offene Konfigurationsrecords;
dies sind historische Startwerte und keine neue Messung.
Canonical-/MIME-Arbeit wird erst nach verifiziertem Schließen von PR #355
fortgesetzt.

## Verbleibende Risiken

Falsche Anpassung könnte aktuelle Source-Materialisierung, Lifecycle-
Containment, Projection-Freshness, Ownership-Reihenfolge, First-Byte-Verhalten,
native Events, Redirect Location, Port-Cleanup oder Konfigurationsbelege
regressieren. Der unprivilegierte lexikalische Artefakt-Handoff benötigt
weiterhin root-seitige Descriptor-/Digest-Re-Admission und spätere
Protected-Host-Evidence. Kein Sonar-Ergebnis oder Security-Finding-Status
wird für einen zukünftigen Head vorausgesagt.

## Finaler Diff- und Review-Status

INCOMPLETE: Geordnete lokale Portierung und finalisierte Maschinennachweise
für 19/19 Commits und 25/25 Dateien liegen vor; Framework-Veröffentlichung
und lokale Parent-Abhängigkeitsbindung sind abgeschlossen; auch der finale
99-Test-Identitätsfokus nach der Bindung bestand ohne Skips.
Remote-CI-Verifikation und Parent-Remote-Delivery-Gates
stehen jedoch aus. Die angeforderten lokalen Gates bestanden mit den oben
genannten Einschränkungen; das zusätzliche optionale vollständige Parent-Lint
bleibt UNVERIFIED und der breite 816-Test-Lauf bleibt FAIL.
Framework PR #135 bleibt OPEN/DRAFT/UNMERGED mit sechs CI-Jobs queued.
Der zuletzt beobachtete Remote-Head von PR #396 bleibt
`2634d821acd80ad208a8e1cd3e4f49fd7e80c628`; an diesem Checkpoint erfolgte
kein Parent-Push. PR #396 bleibt
OPEN/DRAFT/UNMERGED; PR #355 bleibt OPEN/DRAFT/UNMERGED und darf noch nicht
geschlossen werden. Kein Master-Merge, Protocol-Commit, MRTS-Schreibzugriff
oder Full E2E wird behauptet.
