# Change Record: CR-20261122-reviewed-mrts-pin-chain

**Sprache:** [English](CR-20261122-reviewed-mrts-pin-chain.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261122-reviewed-mrts-pin-chain |
| Datum (UTC) | 2026-11-22 |
| Basis-Revision | `60a7b74e057769503d6b4cb01b2cc9ba8da875c8` |

## Motivation und Problemstellung

Die geprüfte Inheritance-Korrektur aus [MRTS #7](https://github.com/Easton97-Jens/MRTS/pull/7) über [Framework #187](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/187) in Parent integrieren. Zwei geerbte Parent-Policy-Bindungen waren abgewichen. Das Quellreview klärte die semantischen Änderungen vor Übernahme ihrer Digests. Dieser Bericht ist ein PREPUBLICATION-Snapshot: Parent-Veröffentlichung und exakte Operator-Freigabe stehen aus.

## Akzeptanzkriterien

Parent-Gitlink, strikter Versionslock und alle registrierten Framework-Caller-Referenzen müssen mit den tatsächlich geprüften Framework-/MRTS-Commits übereinstimmen. Inheritance, Kandidatenverträge, primäre Verifikation, Dokumentation, normale Git-Hooks und frische geltende CI/Quality Gates müssen vor Integration bestehen. Die 100 Core-Fälle, 80 Selektoren, 1144 Offline-Ausnahmen, Integritätskontrollen und geschützten Broker-Identitäten erhalten. Kein Merge anhand eines älteren Heads.

## Implementierungsentscheidung und Begründung

MRTS-Review-Head `9a855b092645733ea8ff73a512aff7bfe916407e` wurde regulär per Squash zu `488e75388d917615feecab91650c3278b9c78b1e` gemerged, mit vorherigem Main `ee2174431c4edf97e66afe32558ce8454deb2397` als einzigem Parent und unverändertem geprüftem Tree. Nur die Bindungen `PARENT-ARCHITECTURE-AND-BOUNDARIES` und `PARENT-COMMAND-EXECUTION` änderten sich. Historische Parent-Preimages wurden rekonstruiert: Die Architekturänderung entfernt einen beispielhaften Leselisteneintrag; die Befehlsänderung präzisiert den direkten Starterpfad automatischer Secrets-Hooks. Ownership, RTK-Nutzung durch Agenten und Berechtigungsgrenzen bleiben erhalten. Keine blinde Prüfsummenreparatur wurde verwendet.

Framework-Review-Head `0cf20b680bef0ba5dd635f874cea1626de8bdef3` wurde zum tatsächlichen Squash `b4d619127a3fbd2a4074998e874c592d693413b9`, mit einzigem Parent `e1964415efcd3cda11614ce13b7d34331ee0cf06` und demselben Tree. Seine einzigen Änderungen sind `tools/MRTS` und der zweisprachige Integrationsbericht. Parent hatte Framework `e1964415efcd3cda11614ce13b7d34331ee0cf06` bereits durch #459 übernommen. Diese Folgeänderung setzt daher diesen Framework-Pin auf `b4d619127a3fbd2a4074998e874c592d693413b9` und MRTS von `ee2174431c4edf97e66afe32558ce8454deb2397` auf `488e75388d917615feecab91650c3278b9c78b1e`.

Der native Synchronisierer besitzt die generierten Projektionen. Explizite `--mrts-sha` und `--expected-candidate-mrts-sha` erhalten den gemeinsamen Vertrag; der Fünf-Schlüssel-Lock und Toolchains bleiben erhalten. Frühere SDK-/Ausgabelayout-Änderungen waren bereits in der ausgewählten Parent-Basis enthalten und werden durch diese Folgeänderung nicht eingeführt.

## Geänderte Dateien

| Pfade | Änderung |
| --- | --- |
| `modules/ModSecurity-test-Framework` | Tatsächlichen Framework-Squash und dessen verschachtelten MRTS-Commit auswählen. |
| `ci/tooling/project-versions.lock.json` | Native Aktualisierung von `framework_sha` und `mrts_sha`. |
| 22 registrierte Dateien unter `.github/workflows/` | Native Regenerierung der Framework-Referenzen. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Aktueller Integrationsstand und nächste Schritte. |
| `reports/audits/change-records/CR-20261122-reviewed-mrts-pin-chain.md`, `reports/audits/change-records/CR-20261122-reviewed-mrts-pin-chain.de.md` | Berichtspaar aus nativen Vorlagen. |

Produktquellen, Testdefinitionen, generierte Messberichte, Repository-Regeln und CI-Gates werden nicht geändert.

## Ausgeführte Befehle

Die Befehle liefen über RTK mit den vorgesehenen Interpretern und expliziter Framework-Umgebung. Exakte Argumente, Voraussetzungen und Belege liegen unter Run-ID `20261122-readiness-continuation`.

| Nativer Befehl oder Vorgehen | Beobachtetes Ergebnis |
| --- | --- |
| `ci/tools/new-change-record.py create` | Anfangs fehlendes `TEST_ROOT` abgewiesen; expliziter vollständiger Framework-Kontext bestand. Editierbare native Vorlagen erstellt. |
| `ci/tools/verify-framework-candidate-contract.py` vor Synchronisation | Exit 0 für den tatsächlichen Framework-/MRTS-Kandidaten. |
| `ci/tools/sync-framework-component-versions.py` mit `--validate`, `--sync`, `--check` | Alle Exit 0; zwei Lock-Felder und 22 registrierte Referenzen synchronisiert; abschließend `changed=[]`. |
| Kandidatenprüfung nach exakter verschachtelter Materialisierung | Exit 0. Anfangs Exit 2, `cannot read pinned Framework Git source`, bevor das neue Objekt im verschachtelten Objektspeicher verfügbar war; erhalten und durch Materialisierung der exakten Commits behoben. Kein Guard geändert. |
| Vier vorhandene explizite MRTS-Handoff-Regressionsmethoden | In 27.632s an `94ce9c76eab09420d5a58f2f9b6b412405d70cbb` bestanden; relevante native Werkzeuge sind an der Berichtsbasis bytegleich. Prüfungen der abschließend gestagten Kette bleiben gesondert. |
| Ursprünglicher Inheritance-Validator auf privater Kandidatenkomposition | Exit 0: 27 Parent-/21 Framework-/12 MRTS-Einträge, keine Verstöße oder Warnungen. Dies prüft die Komposition, keinen künftigen Parent-Commit. |
| Ursprünglicher Inheritance-Validator im tatsächlichen materialisierten Parent-Worktree | Exit 0: 27 Parent-/21 Framework-/12 MRTS-Einträge, keine Verstöße oder Warnungen; Parent-Basis und obige exakte physische Framework-/MRTS-Auswahl bestätigt, weiterhin uncommittet. |
| Unabhängiger Metadatenvergleich | Alle 22 Workflow-Diffs enthalten ausschließlich den ausgewählten gewöhnlichen Framework-Ersatz; genau zwei Lock-Felder geändert; geschützte Tupel unverändert. |
| Framework-Lineage-/Security-Tests und nativer Security-Vertrag | Exit 0. Bindings-/Archiv-/Aktivprüfungen mit `CONNECTOR_TEST_PROFILE=parent` bestanden; die frühere Abweisung bei fehlendem Profil bleibt erhalten. |
| MRTS-CI am tatsächlichen Main und vollständige Sonar-Rückmeldung | Vier erfolgreiche Checks, zwei erfolgreiche Workflows; alle fünf Gate-Bedingungen OK, keine ignoriert, insgesamt/neu Reliability A, Security A, Maintainability A; null ungelöste/neue Issues oder Hotspots an obiger exakter Revision. |
| Framework #187: CI am exakten Head und vollständige Sonar-Rückmeldung | 17 terminale Checks: 14 erfolgreich, drei erwartete Advisory-Skips; alle vier zurückgegebenen Gate-Bedingungen OK, keine ignoriert, insgesamt/neu Reliability A, Security A, Maintainability A; null ungelöste/neue Issues oder Hotspots am obigen Review-Head. |

Native Compiler-Guide-Regenerierung mit `scripts/generate_compiler_guides.py` und vollständigem Framework-Kontext ergab Exit 0; alle 18 Ausgaben blieben bytegleich. Workflow-Dateimodi blieben ebenfalls unverändert.

Native Parent-Prüfungen vor dieser Status-Textaktualisierung bestanden: vollständiger ursprünglicher Bilingual-Prüfer Exit 0 (6.739s), `ci/tools/new-change-record.py check` Exit 0 (0.865s), Synchronisierer `--verify-primary --base 60a7b74e057769503d6b4cb01b2cc9ba8da875c8 --staged` Exit 0 (1.571s) für die exakte Framework-/MRTS-Auswahl. Tatsächliche Worktree-Inheritance bestand bereits mit 27/21/12 Einträgen. Belege: `parent-final-prechecks/native-final-checks.json`. Abschließende Wiederholung nach dieser Textaktualisierung bleibt erforderlich; diese Ergebnisse qualifizieren keinen unveröffentlichten Parent-Commit.

## Security-Auswirkung

Keine Validierung und kein Gate wird abgeschwächt. Geschützter Broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` und geschütztes Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` bleiben unverändert. Keine Publisher-, Rootbroker-, geschützte Dispatch- oder administrative Regelaktion, Sonar-Installation oder Authentifizierungsreparatur wurde ausgeführt. Bestehende CI-Analyse bleibt aktiv.

## Runtime-Evidence

Dieser Pinübergang ändert keine H2/H3-Reader, Executor, Collector, Schemata oder Produktlaufzeitquellen. Keine neue Host-/Protokollqualifikation wird beansprucht. Historische Ergebnisse vom 2026-11-03 behalten ihre alten Revisionen; ihr Rohdaten-Nachweisort fehlte bei Arbeitsbeginn. Sie qualifizieren weder diese Kette noch die Wiederverwendung eines aktuellen SDK-/Build-Artefakts.

## Bekannte Einschränkungen

Der tatsächliche Framework-Master `b4d619127a3fbd2a4074998e874c592d693413b9` hat jetzt neun terminale Checks: acht erfolgreich, einen erwarteten PR-Kontext-Skip; alle fünf Workflows bestanden. Vollständiges stabiles revisionsgebundenes Sonar-Gate OK, alle zurückgegebenen Bedingungen OK, keine ignoriert; insgesamt/neu Reliability A, Security A, Maintainability A; null Bugs, Schwachstellen oder Hotspots. Ein offener MINOR `go:S8209` bleibt an `compositeenvoy/server_test.go:756`, erstellt `2026-11-01T10:10:38`. Schlüssel, Regel, Meldung, Positionen/Flow und vollständiger Datei-Blob entsprechen Basis `e1964415efcd3cda11614ce13b7d34331ee0cf06`; sämtlicher regulärer Code ist über den Pinübergang unverändert. Der Server zählt diesen Befund auch zur New Code Period. Er ist unabhängig vorbestehend, ohne False-Positive-, Akzeptanz- oder andere Disposition; dies behauptet weder einen Master ohne Befunde noch globale Fehlerfreiheit.

Primäre/Inheritance- und vollständige Bilingual-/Archivprüfungen für Parent bestanden wie oben erfasst vor dieser Status-Textaktualisierung; abschließende Wiederholung, Commit, PR und frische CI stehen aus. Exaktes lokales MRTS-CPython 3.14.6 fehlt; 3.14.4 wurde nicht ersatzweise verwendet. Gehostete 3.14.6-Governance-Tests verwenden eine isolierte Policy-Fixture und ersetzen die tatsächliche Parent-Kompositionsprüfung nicht.

## Verbleibende Risiken

Der installierte Pre-Commit-Guard verlangt operatorseitige V2-Freigabe für exakten Worktree, HEAD, gestagten Index und ausgewählte Framework-/MRTS-Quellnachweise. Dieses neue Tupel ist nicht installiert. Private Nachweisvorbereitung erteilt keine Installationsberechtigung. Parallele Parent-Fortschritte vor normaler Auslieferung abgleichen und betroffene Prüfungen wiederholen. Bei Auftragsübernahme hatte der ursprüngliche Arbeitsbereich fremde `.gitignore`-Konflikte und eine parallele `Makefile`-Änderung. Dieser Auftrag änderte oder restaurierte diesen Arbeitsbereich nicht; vor jeder Bereinigung dessen aktuellen Stand erneut prüfen.

## Nicht ausgeführte Prüfungen mit Begründung

Für diesen reinen Metadatenübergang wurde keine umfassende Abnahmekampagne, kein neuer Produkt-Build, Hostlauf oder geschützter Brokerlauf ausgeführt. Ein aktuelles Parent-PR-Gate existiert noch nicht. Native gestagte primäre und vollständige Bilingual-/Archivprüfungen bestanden nach Aufnahme der neuen Berichte in die Suche versionierter Dateien; abschließende Wiederholung folgt dieser Status-Textaktualisierung. Historische Basis-CI ersetzt diese Ergebnisse nicht.

## Finaler Diff- und Review-Status

Semantische MRTS-Korrektur und tatsächlicher Framework-Merge-Tree wurden geprüft; native Parent-Metadatensynchronisation und korrigierte Kandidatenprüfung bestanden. Dieser Snapshot dokumentiert ausschließlich die Vorbereitung. Exakter gestagter Diff, Quellfreigabe, normaler Commit/PR und frische Head-gebundene CI/vollständiges Quality Gate müssen vor dem autorisierten regulären Parent-Squash-Merge noch geprüft werden. Keine Parent-PR-Nummer und kein resultierender Commit werden behauptet.
