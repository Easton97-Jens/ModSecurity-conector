# KI-Übergabe

**Sprache:** [English](AI-HANDOFF.md) | Deutsch

## Stand und Ziel

PREPUBLICATION-Snapshot, **2026-11-22 UTC**. Die ausdrücklich autorisierte geprüfte Kette MRTS #7 → Framework-Pinfolge → Parent-Pinfolge einschließlich regulärer Squash-Merges am exakten Head nach geltenden Prüfungen fortsetzen. Parent-Branch: `codex/inheritance-pin-chain-20261122`; ausgewählte Basis: `60a7b74e057769503d6b4cb01b2cc9ba8da875c8`. Dieser Snapshot behauptet keinen Parent-Commit, PR oder Merge. Aktuellen HEAD, Index, Remote-Stand und Quellnachweise vor Fortsetzung abgleichen.

| Repository-Grenze | Beobachteter Stand |
| --- | --- |
| [MRTS #7](https://github.com/Easton97-Jens/MRTS/pull/7) | Review-Head `9a855b092645733ea8ff73a512aff7bfe916407e` als tatsächlicher Main `488e75388d917615feecab91650c3278b9c78b1e` gemerged; geprüfter Tree erhalten, einziger Parent `ee2174431c4edf97e66afe32558ce8454deb2397`. |
| [Framework #187](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/187) | Review-Head `0cf20b680bef0ba5dd635f874cea1626de8bdef3` als tatsächlicher Master `b4d619127a3fbd2a4074998e874c592d693413b9` gemerged; geprüfter Tree erhalten, einziger Parent `e1964415efcd3cda11614ce13b7d34331ee0cf06`, verschachteltes MRTS `488e75388d917615feecab91650c3278b9c78b1e`. |
| Parent | #458 erhielt `TMPDIR`; #459 übernahm bereits Framework `e1964415efcd3cda11614ce13b7d34331ee0cf06`. Diese Folgeänderung bereitet Framework `b4d619127a3fbd2a4074998e874c592d693413b9` / MRTS `488e75388d917615feecab91650c3278b9c78b1e` aus der ausgewählten Basis vor. Veröffentlichung und exakte Operator-Freigabe stehen aus. |

Bei Auftragsübernahme hatte der ursprüngliche Nutzercheckout fremde `.gitignore`-Konflikte und eine parallele `Makefile`-Änderung. Dieser Auftrag änderte oder restaurierte diesen Checkout nicht. Die Arbeit läuft im isolierten Task-Worktree; vor jeder Bereinigung den aktuellen ursprünglichen Checkout-Stand erneut prüfen.

## Relevante Komponenten und umgesetzte Arbeit

MRTS ändert nur die geerbten Digests `PARENT-ARCHITECTURE-AND-BOUNDARIES` und `PARENT-COMMAND-EXECUTION`. Historische Quellpreimages wurden rekonstruiert und geprüft: Entfernung eines beispielhaften Architektur-Leselisteneintrags und Präzisierung des Starterpfads automatischer Secrets-Hooks. Dies erweitert keine Schreib-, Installations-, Authentifizierungs-, Merge- oder MCP-Berechtigung. Keine blinde Prüfsummenaktualisierung.

Framework ändert zwischen `e1964415efcd3cda11614ce13b7d34331ee0cf06` und `b4d619127a3fbd2a4074998e874c592d693413b9` nur `tools/MRTS` und seinen zweisprachigen Integrationsbericht. Produkt-/Test-/Analyse-/SDK-Helfer sind in diesem Intervall unverändert. Das Inventar bleibt bei 100 Core-Fällen, 80 Selektoren und 1144 Offline-Ausnahmen. Frühere SDK-Layout-/PCRE2-Änderungen sind bereits in der Parent-Basis; diese Folgeänderung führt keinen neuen Laufzeit- oder Readerpfad ein.

Der native Parent-Synchronisierer aktualisierte zwei Lock-Felder und 22 registrierte Framework-Referenzen. Kandidatenprüfung vor Synchronisation und nach exakter verschachtelter Materialisierung bestanden; native `--validate`, `--sync` und `--check` bestanden. Der anfängliche Objektverfügbarkeitsfehler nach Synchronisation bleibt als Vorbereitungsfehler erhalten und wird nicht durch Code- oder Guard-Änderung verborgen. Siehe [aktuellen Change Record](../reports/audits/change-records/CR-20261122-reviewed-mrts-pin-chain.de.md).

## Für den PR ausgewählte Änderungen

Die Auswahl umfasst Framework-Gitlink, `ci/tooling/project-versions.lock.json`, 22 registrierte `.github/workflows/`-Projektionen, `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` und das aktuelle Change-Record-Paar. Produktquellen, Testdefinitionen, generierte Messberichte und Repository-Regeln werden nicht geändert. Generierte Metadaten stammen aus `ci/tools/sync-framework-component-versions.py`; das Change-Record-Paar verwendet Vorlagen von `ci/tools/new-change-record.py`.

## Entscheidungen, verworfene Ansätze und offene Arbeit

Gemeinsamen Framework-/MRTS-Vertrag erhalten: explizite `--mrts-sha`, `--expected-candidate-mrts-sha`, strikter Fünf-Schlüssel-Lock und vorhandene Toolchains. Geschützter Broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` und geschütztes Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` bleiben unverändert. Kein Publisher, Rootbroker oder geschützter Dispatch wurde aufgerufen; kein Gate und kein administrativer Schutz wurde abgeschwächt.

Der installierte Pre-Commit-Guard verlangt operatorseitige V2-Freigabe für exakten Worktree, HEAD, vollständigen gestagten Index, ausgewählten Gitlink und vollständige Framework-/MRTS-Nachweise. Das neue exakte Tupel ist nicht installiert. Private Nachweisvorbereitung autorisiert keine geschützte Installation. Konkreten Vorschlag und erforderliche Nachweise vor der Operator-Freigabefrage vorbereiten; normale Task-Branch-Auslieferung und reguläre Merges sind bereits autorisiert.

## Ausgeführte Prüfungen und Grenzen

| Umfang | Ergebnis und Grenze |
| --- | --- |
| MRTS am tatsächlichen Main | Vier Checks und zwei Workflows erfolgreich; vollständiges revisionsgebundenes Sonar-Gate OK, fünf Bedingungen OK, keine ignoriert; insgesamt/neu Reliability A, Security A, Maintainability A; null ungelöste/neue Issues oder Hotspots. |
| Framework #187 am Review-Head | 17 terminale Checks: 14 erfolgreich, drei erwartete Advisory-Skips; vollständiges stabiles Sonar-Gate OK, vier zurückgegebene Bedingungen OK, keine ignoriert; insgesamt/neu Reliability A, Security A, Maintainability A; null ungelöste/neue Issues oder Hotspots. |
| Inheritance | Ursprünglicher Validator sowohl auf privater Kandidatenkomposition als auch im tatsächlichen materialisierten Parent-Worktree bestanden: 27 Parent-/21 Framework-/12 MRTS-Einträge; keine Verstöße oder Warnungen. Der tatsächliche Worktree verwendet die obige exakte Basis und physische Framework-/MRTS-Auswahl, weiterhin uncommittet; dies bestätigt keinen künftigen Parent-Commit. |
| Native Parent-Vorbereitung | Kandidat vorher/nachher und Synchronisierer-Validierung/-Sync/-Check alle Exit 0; unabhängiger Vergleich bestätigt ausschließlich gewöhnliche Framework-Ersetzungen in 22 Workflows, zwei geänderte Lock-Felder und unveränderte geschützte Tupel; vier vorhandene Handoff-Regressionsmethoden in 27.632s an `94ce9c76eab09420d5a58f2f9b6b412405d70cbb` bestanden, relevante Werkzeugquellen an aktueller Basis unverändert. Gestagte primäre Verifikation und vollständige native Bilingual-/Archivprüfungen bestanden vor dieser Status-Textaktualisierung; abschließende Wiederholung folgt. |
| Gezielte Framework-Prüfungen | Lineage-/Security-Regressionen und nativer Security-Vertrag bestanden. Bindings-/Archiv-/Aktivprüfungen mit `CONNECTOR_TEST_PROFILE=parent` bestanden; Abweisung bei fehlendem Profil erhalten. Framework-Dokumentationsprüfungen vor Veröffentlichung bestanden. |

Der tatsächliche Framework-Master `b4d619127a3fbd2a4074998e874c592d693413b9` hat jetzt neun terminale Checks: acht erfolgreich, einen erwarteten PR-Kontext-Skip; alle fünf Workflows bestanden. Vollständiges stabiles revisionsgebundenes Sonar-Gate OK, alle zurückgegebenen Bedingungen OK, keine ignoriert; insgesamt/neu Reliability A, Security A, Maintainability A; null Bugs, Schwachstellen oder Hotspots. Ein offener MINOR `go:S8209` bleibt an `compositeenvoy/server_test.go:756`, erstellt `2026-11-01T10:10:38`. Schlüssel, Regel, Meldung, Positionen/Flow und vollständiger Datei-Blob entsprechen Basis `e1964415efcd3cda11614ce13b7d34331ee0cf06`; sämtlicher regulärer Code ist über den Pinübergang unverändert. Der Server zählt diesen Befund auch zur New Code Period. Er ist unabhängig vorbestehend, ohne False-Positive-, Akzeptanz- oder andere Disposition; dies behauptet weder einen Master ohne Befunde noch globale Fehlerfreiheit.

Native Compiler-Guide-Regenerierung mit `scripts/generate_compiler_guides.py` und vollständigem Framework-Kontext ergab Exit 0; alle 18 Ausgaben blieben bytegleich. Workflow-Dateimodi blieben ebenfalls unverändert.

Native Parent-Prüfungen vor dieser Status-Textaktualisierung bestanden: vollständiger ursprünglicher Bilingual-Prüfer Exit 0 (6.739s), `ci/tools/new-change-record.py check` Exit 0 (0.865s), Synchronisierer `--verify-primary --base 60a7b74e057769503d6b4cb01b2cc9ba8da875c8 --staged` Exit 0 (1.571s) für die exakte Framework-/MRTS-Auswahl. Tatsächliche Worktree-Inheritance bestand bereits mit 27/21/12 Einträgen. Belege: `parent-final-prechecks/native-final-checks.json`. Abschließende Wiederholung nach dieser Textaktualisierung bleibt erforderlich; diese Ergebnisse qualifizieren keinen unveröffentlichten Parent-Commit.

Exakte Befehle und Belege liegen unter Run-ID `20261122-readiness-continuation`, einschließlich `parent-pin-sync/commands.json` und `parent-pin-sync/candidate-after-materialization.json`. Kein aktuelles Parent-PR/Quality Gate wird behauptet. Exaktes lokales MRTS-CPython 3.14.6 fehlt; 3.14.4 wurde nicht ersatzweise verwendet. Gehostete 3.14.6-Governance-Tests verwenden isolierte Policy-Fixtures und bleiben von tatsächlicher Parent-Inheritance getrennt.

Für diesen Metadatenübergang lief kein neuer Produkt-Build, keine Host-/Protokollqualifikation und keine umfassende Abnahmekampagne. H2/H3-Reader-/Executor-/Collector-/Schemapfade sind unverändert. Der [Readiness-Bericht vom 2026-11-03](../reports/audits/change-records/CR-20261103-runtime-readiness-prerequisites.de.md) ist historisch, mit älteren Revisionen und bei Arbeitsbeginn fehlenden Rohnachweisen; seine Ergebnisse nicht umetikettieren und daraus keine aktuelle Build-Wiederverwendung ableiten.

## Aus dem Repository ermittelte Start-, Build- und Testbefehle

Aktuelle `AGENTS.md`, geroutete Policies, Root-`Makefile` und ausgewählte Framework-Verträge verwenden. Relevante nächste Prüfungen sind nativer Kandidatenprüfer, Synchronisierer `--check` / `--verify-primary`, Inheritance-Validierung und Dokumentationsprüfungen: `rtk make check-bilingual-docs`, `rtk make check-doc-links`, `rtk make check-variable-documentation` und `rtk bypass git diff --cached --check`. Vorgesehene Interpreter, vollständigen Framework-Kontext und externe beschreibbare Wurzeln bereitstellen. Ausgewählte neue Berichte vor Prüfungen mit Suche versionierter Git-Dokumente stagen. Beobachtete Erfolge vor der Aktualisierung sind oben erfasst; abschließende Wiederholung folgt dieser Status-Textaktualisierung.

Historische Auslieferungsdetails bleiben im [Handoff-Change-Record vom 2026-11-14](../reports/audits/change-records/CR-20261114-ai-handoff-and-framework-pin.de.md) und [Security-Change-Record vom 2026-11-19](../reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.de.md). Deren alte Draft-, Pin-, Operator- und CI-Stände sind historisch. Parent #454–#456 und Framework #179–#183 sind inzwischen gemerged; sie nicht als offene Drafts fortsetzen.

## Nächste Schritte

1. Aktuelle Parent-Basis und exakte Framework-/MRTS-Trees, Lock, Referenzen und gestagten Umfang abgleichen. Bestandene gestagte native primäre/Inheritance-/Dokumentationsprüfungen nach dieser abschließenden Status-Textaktualisierung wiederholen; Fehler und korrigierte Ergebnisse erhalten.
2. Terminale CI und vollständiges revisionsgebundenes Quality Gate am tatsächlichen Framework-Master sind wie oben erfasst zurückgelesen, einschließlich des erhaltenen MINOR-Befunds. Vollständige Quellnachweise abschließen, exakten Operator-Freigabevorschlag vorbereiten und dessen gesondert nötige Installationsfreigabe einholen; vorhandene Guards erhalten.
3. Normalen Parent-Commit und vorhandenen oder neuen Task-PR mit wahrheitsgemäßer EN/DE-Beschreibung erstellen. Dessen Checks am exakten Head, Reviews, Gespräche und vollständiges geltendes Sonar-Gate vor dem autorisierten regulären Squash-Merge prüfen; resultierenden Master und tatsächliches Commitpaar zurücklesen.
4. Übergabe und erhaltenen Abschlussbericht mit beobachteter Veröffentlichung, Merge und Prüfergebnissen aktualisieren. Fremde Arbeitsbereichsänderungen und historische Nachweise erhalten; ausschließlich eigene Prozesse und entbehrliche Laufartefakte bereinigen.
