# Vorgeschlagene Masterprüfungen

**Sprache:** [English](rules-review.md) | Deutsch

Status: **PROPOSED_NOT_APPLIED**. Der Vorschlag vom 2. November 2026 wurde am 3. November 2026 um 13:32 MEZ (12:32 UTC) aktualisiert. Administrative Anwendung benötigt weiterhin gesonderte Freigabe. Keine Rulesets, Schutzregeln, Workflows oder Remoteeinstellungen geändert. Die ausdrücklich ausgenommene lokale Sonar-Vorprüfung lässt gehostete Sonar-/CodeQL-Prüfungen bestehen.

[Vorher-Snapshot](rules-before.json) enthält frisch gelesene sichtbare Rulesets. [Nachher-Vorlage](rules-after-proposal.json) erhält diese exakten bestehenden Objekte und ergänzt ausschließlich die unveränderten [15 Connector-Kontexte](connector-ruleset-create-proposal.json) und [6 Framework-Kontexte](framework-ruleset-create-proposal.json). Exakte Namen und GitHub-Actions-Integration 15368 wurden erneut belegt; bestätigte Anlagevorlagen benötigen keine künstlichen Änderungen.

## Aktueller Schutzregelstand

Live-Master: Parent `11fab78a5447f75cb254ddf963eca770fa04ba04`, Framework `bb6c7580208a05c17d6d6674571731b6a71028cb`. Connector-GET der Rulesetlisten mit `includes_parents=true` liefert je ein aktives Repository-Ruleset. Einzelheiten und authentifizierter lesender CLI-GET der effektiven Masterregeln stimmen überein:

- [Parent 19138299](https://api.github.com/repos/Easton97-Jens/ModSecurity-conector/rulesets/19138299): Lösch-/Force-Push-Schutz, aufgelöste Reviewthreads, null Pflichtfreigaben, strikt aktueller Basisstand und `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, `zizmor`; keine Bypassakteure.
- [Framework 19700778](https://api.github.com/repos/Easton97-Jens/ModSecurity-test-Framework/rulesets/19700778): Lösch-/Force-Push-Schutz, aufgelöste Reviewthreads, null Pflichtfreigaben; keine Required-Status-Check-Regel oder Bypassakteure.

Klassischer Branchschutz bleibt **über den Connector nicht lesbar** (403, Resource not accessible by integration). Der vorhandene authentifizierte CLI-GET liefert jeweils 404, Branch not protected; kein klassisches Konfigurationsobjekt wurde geliefert. Beide Zugriffsergebnisse bleiben erhalten und werden nicht zu „kein Schutz“ zusammengezogen: effektive Rulesets gelten. Administrative UI-/Einstellungsebenen außerhalb dieser lesbaren Antworten bleiben **ungeprüft**. Der Connector verweigerte effektive Branchregel-URLs aufgrund seiner Endpoint-Allowlist; der dokumentierte reine GET-CLI-Fallback lieferte diese Antworten.

## Exakte Checklieferung

Frische API-Checkruns wurden über Actions-Run-ID, App-ID und exakten Head-SHA mit Workflowruns des Ereignisses `pull_request` korreliert. Alle 42 Kontext-/PR-Zeilen enthalten echte abgeschlossene Ausführung; kein Skip ersetzt Ausführung. Geprüfte PRs stammen aus demselben Repository:

- Parent [442](https://github.com/Easton97-Jens/ModSecurity-conector/pull/442), Head `4fcf094b7b93deda07c9b990d113f32d5d6a62da`; [440](https://github.com/Easton97-Jens/ModSecurity-conector/pull/440), Head `6e72c42133ad4a9b9ddeb964724cb95805d27b84`.
- Framework [165](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/165), Head `44ce463261d1a4617d136580c6b61df4285d54b5`; [164](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/164), Head `6ac8c947b8a1f84a5d4cc79d05ee61bd7222430c`.

| Exakter Kontext | Workflow | PR 442 | PR 440 |
| --- | --- | --- | --- |
| `scaffold-lint` | `lint.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921495/job/125764045488) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802514/job/125377424853) |
| `common-structure` | `test-common.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921243/job/125764044568) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802290/job/125377421781) |
| `apache-autotools-bootstrap` | `test-apache.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921226/job/125764044736) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802162/job/125377421385) |
| `apache-structure` | `test-apache.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921226/job/125764044385) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802162/job/125377421044) |
| `nginx-structure` | `test-nginx.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921322/job/125764044920) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802413/job/125377423128) |
| `nginx-exact-head` | `test-nginx-exact-head.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921331/job/125764044911) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802341/job/125377424639) |
| `haproxy-structure` | `test-haproxy.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921428/job/125764045090) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802086/job/125377420617) |
| `envoy-contract` | `test-envoy.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921203/job/125764044402) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802430/job/125377425651) |
| `lighttpd-contract` | `test-lighttpd.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921357/job/125764045299) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802178/job/125377422143) |
| `traefik-contract` | `test-traefik.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921310/job/125764044724) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802094/job/125377420195) |
| `quick-check` | `quick-framework-check.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921262/job/125764044623) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802518/job/125377427397) |
| `report-governance` | `verified-report-governance.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921246/job/125764044728) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802406/job/125377424863) |
| `protocol-contract` | `protocol-contract.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921312/job/125764044814) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802165/job/125377421228) |
| `apr-util-provenance` | `ci-security-workflow-lint.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921343/job/125764045127) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802084/job/125377421862) |
| `pull-request-range` | `ci-security-secrets.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41589921257/job/125764044969) | [success](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/41474802117/job/125377421757) |

| Exakter Kontext | Workflow | PR 165 | PR 164 |
| --- | --- | --- | --- |
| `scaffold-lint` | `lint.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537426/job/125756418317) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468640209/job/125356060906) |
| `common-structure` | `test-common.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537773/job/125756419391) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468640054/job/125356059827) |
| `CodeQL PR (actions)` | `ci-security-codeql-pr.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537447/job/125756418387) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468639916/job/125356059652) |
| `CodeQL PR (python)` | `ci-security-codeql-pr.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537447/job/125756418598) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468639916/job/125356060366) |
| `CodeQL PR (c-cpp)` | `ci-security-codeql-pr.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537447/job/125756419300) | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468639916/job/125356059948) |
| `pull-request-range` | `ci-security-secrets.yml` | [success](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41587537446/job/125756419351) | [failure](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/41468640416/job/125356061346) |

Framework 164 führte `pull-request-range` aus und **scheiterte**; die Aktualisierung schreibt diesen Verlauf nicht um. Der ausgewählte Head von Framework 165 bestand. Eine Pflichtprüfung erzwingt das tatsächliche Ergebnis am später ausgewählten PR-Head; sie bedeutet nicht, dass alle historischen Läufe bestanden.

Die 18 verantwortlichen Workflows wurden aus exakten Master-Gitobjekten gelesen. Ausgewählte PR-Jobs besitzen keine Pfad-/Fork-Ausnahme; reine PR-Gates erlauben das passende Ereignis. Zehn gepinnte Framework-Composite-Actions hinter Parentjobs enthalten keine Fork-/Event-Bedingung oder Continue-on-error-Markierung. Dies stützt die konfigurierte kontinuierliche Master-PR-Lieferung. Die zwei gleichrepositoryinternen Stichproben belegen **keine** Forkausführung, Docs-only-PR-Abdeckung, Merge-Queue-Lieferung oder Ergebnisse des aktuellen Taskheads. Keine Mergequeue wird vorgeschlagen; ausgewählten Workflows fehlt `merge_group`.

## Ausdrückliche Ausschlüsse

| Checks | Aktueller Grund gegen Aufnahme |
| --- | --- |
| Framework actionlint-and-contract, zizmor, python-ci-security-quality, check-action-versions, portable-contract | Aktuelle PR-Pfadfilter können die Workflowlieferung verhindern. Erfolge interner PRs qualifizieren nicht jeden PR. |
| Parent go-candidate-Varianten, nginx-b09-regression, Fünf-Zellen-CRS-Aggregat | Aktuelle PR-Pfadfilter. Nicht allein aufgrund beider codeändernder Stichproben verpflichtend machen. |
| Framework OSV/Scorecard pull-request-head | Doppelte Checknamen in beiden ausgewählten Heads beobachtet; Produzenten vor Pflichtaufnahme unterscheiden. |
| Parent OSV pull-request-diff | Einzelne Scanschritte laufen bei Fehlern weiter; Fork-/Uploadsemantik unqualifiziert. Grüner Wrapper belegt keinen Findingsstatus. |
| Gehostetes Sonar/externes SonarCloud | Bestehende Checks und Delivery-Gates erhalten. Forkausnahmen oder Lieferung jenseits der Stichproben sind damit nicht qualifiziert. |
| Zeitpläne/Advisories, C++20/23, manueller Rootbroker, H2/H3-Preflight | Keine kontinuierliche verpflichtende PR-Ausführung. `nginx-profile-and-client-preflight` ist in beiden Parentstichproben übersprungen und bleibt ausgeschlossen. |

`nginx-exact-head` ist gewöhnliches gehostetes H1 und bleibt von manuellem geschütztem Broker sowie H2/H3-Qualifikation getrennt. Framework-CodeQL-PR verwendet `upload: never`; verpflichtende Ausführung beweist keine Findingsfreiheit. GitHub akzeptiert teilweise übersprungene/neutrale Ergebnisse als erfolgreiche Statuschecks; vorhandener Checkname allein beweist daher keine Ausführung. Siehe [GitHub-Prüfungsdiagnostik](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks) und [API effektiver Branchregeln](https://docs.github.com/en/rest/repos/rules#get-rules-for-a-branch).

## Anwendungsübergabe und Nachweisgrenzen

Repositoryintegration bleibt von Schutzregelanwendung getrennt. Parent erhält
seinen aktuellen Framework-Gitlink `bb6c7580208a05c17d6d6674571731b6a71028cb`;
keinen ungemergten Frameworkkandidaten pinnen. Der generierte Inline-Brokercaller
stammt bereits aus genau diesem kanonischen Blob und behält wahrheitsgemäß seinen
`bb6`-Quellheader. Framework-/MRTS-Draft-PRs haben getrennte Liefergrenzen.
Ausschließlich nach gesondert freigegebener Integration den tatsächlichen
Merge-SHA propagieren, Projektionen regenerieren und Generator-/Pinprüfungen am
exakten Paar wiederholen. Diese Prüfung autorisiert weder Merge noch Adminwrites.

Bestehende Archivzweige, Review-/Threadvorgaben, Striktheit, Lösch-/Force-Push-Schutz und fehlende Bypassakteure unverändert erhalten. Hypothetisch ergeben sich 21 sichtbare Pflichtkontexte für Parent und 6 für Framework; das ist eine Vorlage, kein Serverzustand. Vor administrativer Freigabe alle Schutzebenen erneut lesen und tatsächlichen finalen PR-Head, erwartete Appidentität, Forkregelung und anwendbares Sonar-Gate prüfen. Vor Mergequeue `merge_group` neu qualifizieren. Keine manuellen/regelmäßig übersprungenen Jobs verpflichtend machen oder grünes Aggregat erfinden.

Frische Tasknachweise unter genehmigter externer Speicherwurzel des aufrufenden Projekts: `runs/20261103T115937Z-runtime-readiness/github/governance`. Enthalten sind exakte GET-URLs, Zeitpunkte, unveränderliche Quellhashes, aktuelle Rulesetobjekte, klassische Zugriffsfehler und 42 Check-/Runkorrelationen. JSON-Prüfung bestätigt unverändert erhaltene Rulesets, identische Anlagevorlagen, exakte appgebundene Lieferung und keine ausgewählten Skips/fehlenden Ausführungen. Keine Geheimnisse, Adminschreiboperation, neue PRs, Commits oder Kampagne enthalten.
