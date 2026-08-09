# Change Record CR-20260809-001: Sonar-Duplikatreduzierung

**Sprache:** [English](CR-20260809-001-sonar-duplication-reduction.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260809-001` |
| Datum (UTC) | `2026-08-09` |
| Basis-Revision | `cc58f94e6a0dd17eea651cd46376843472b83f7c` |
| Umfang | Nur Parent-Repository; keine Änderung an Framework, MRTS, Gitlink, Lock-Datei oder Quality Gate; ein benutzerautorisierter exakter Publisher-Staging-Eintrag |

## Motivation und Problemstellung

SonarCloud meldete eine Duplikatcodedichte oberhalb des angeforderten
Grenzwerts im Workflow-Tool-Updater und seinem Testmodul sowie zwei doppelte
C-Quellcode-Parserhelfer in NGINX-Vertragstests. Die Änderung entfernt nur
nachgewiesene strukturelle Duplikate und erhält die Sicherheitsprüfpunkte des
Updaters.

Die vor der Änderung erfassten SonarCloud-Metriken waren:

| Komponente | Duplizierte-Zeilen-Dichte | Duplizierte Zeilen | Duplizierte Blöcke |
| --- | ---: | ---: | ---: |
| `tests/ci_security/test_update_workflow_tools.py` | 67.2% | 709 | 13 |
| `ci/tools/update-workflow-tools.py` | 62.1% | 1,305 | 15 |
| `tests/test_nginx_intervention_url_ownership.py` | 18.1% | 25 | 2 |
| `tests/test_nginx_upstream_security_contract.py` | 6.6% | 25 | 2 |

## Akzeptanzkriterien

- Ausschließlich den freigegebenen Parent-Quell- und Testumfang mit kleiner
  gemeinsamer Testunterstützung bei Bedarf refaktorieren.
- Update-CLI-Flags, YAML-/Lock-Serialisierung, kanonisches Candidate-JSON,
  SHA-256-Eingaben, Exit-Codes, Ablehnungsverhalten und Ausgabepfade erhalten.
- Strenge Vertrauensgrenzen für Action-/Tool-Identität, unveränderliche Pins,
  Release-Commits, URLs, Asset-Pfade, Hashes und Runner-Temporärpfade erhalten.
- Kein `NOSONAR`, keine Sonar-Ausschlüsse, Suppression-Anmerkungen,
  Testlöschung, schwächeren Assertions, Quality-Gate-Änderungen oder
  generischen Lock-Record-Merges verwenden.
- Fokussierte Tests, Kompilierung, Vertragsprüfungen, Dokumentationsprüfungen,
  einen Security-Diff-Scan und gehostete PR-/SonarCloud-Validierung ausführen.

## Implementierungsentscheidung und Begründung

- `CandidateGroupSpec` und unveränderliche Candidate-Payload-Konstruktion
  hinzugefügt, um das geprüfte Action-/Tool-Schema zu zentralisieren und die
  getrennten Action-/Tool-Identitäts- und Release-Auflösungspfade explizit zu
  lassen.
- Alle öffentlichen Hilfsfunktionsnamen an ihren bestehenden Aufrufstellen
  beibehalten; ihre Implementierungen delegieren an eng abgegrenzte
  unveränderliche Boundary-Objekte für Runner-Temporärpfade,
  Workflow-Inventar und die GitHub-API.
- `tests/c_source_contract.py` für ausgeglichene C-Definitions-Extraktion und
  seine Unit-Tests hinzugefügt und beide NGINX-Tests auf diesen Helfer umgestellt.
- Wiederholte Test-Fixture-Maps durch explizite Fixtures und tabellengesteuerte
  Fälle ersetzt. Bestehende Testmethoden bleiben vorhanden; zusätzliche
  Ablehnungs- und Unveränderlichkeitsfälle wurden ergänzt.
- Ein reiner Test-Follow-up teilt Connector-spezifische Proposed-Tree- und
  Generated-Branch-Fixtures, während unabhängige Assertions für Lock,
  RUNNER_TEMP, exakte Blobs und einen bösartigen Publisher erhalten bleiben.
  Zusätzlich wird eine Release-Fixture vor dem Exception-Kontext aufgebaut;
  dadurch ist S5778 ohne Änderung des Negativtests behoben.

## Security-Auswirkung

Der geänderte Updater überschreitet Eingabe-, Dateisystem-, Netzwerk-,
Serialisierungs- und Lock-Datei-Vertrauensgrenzen. Der Refaktor erhält strenge
Candidate-Gruppen-Felder, die Validierung unveränderlicher Action-Pins und
Tool-Release-Commits, die Prüfung vertrauenswürdiger GitHub-Origins und
Redirects, URL-, Asset- und SHA-256-Prüfungen, kanonisches Candidate-JSON,
sichere Relative-Pfad- und Symlink-Ablehnung sowie atomaren Lock-Datei-Ersatz.

Der fokussierte Security-Diff-Scan deckte alle sechs geänderten Codedateien ab
und lieferte null berichtspflichtige Kandidaten. Er identifizierte keinen neuen
Angriffspfad und keine abgeschwächte Kontrolle.

Nach dem Rebase auf current `origin/master` machte der bereits vorhandene
vertrauenswürdige NGINX-Root-Broker-Workflow eine Fail-Closed-Lücke sichtbar:
Seine gesperrten Action-Pins fehlten im endlichen Publisher-Pfadset des
Updaters. Der Benutzer autorisierte die einzige vollständige Begleitreparatur:
denselben Literalpfad in der bestehenden Publisher-`git add --`-Liste. Die
Source-/Staging-Gleichheitskontrolle, der reale Coverage-Test und das bestehende
Fail-Closed-Negative-Control bestehen. Ein zweites fokussiertes Zwei-Dateien-
Security-Diff-Review hat ebenfalls null berichtspflichtige Findings.

SonarCloud meldete zunächst einen aufgabeneigenen S5778-Test-Smell. Sein
Exception-Kontext mit zwei Aufrufen wurde in explizites Setup und die einzelne
Operation unter Assertion aufgeteilt; die ursprüngliche Immutable-Release-
Ablehnung bleibt abgedeckt. Der resultierende PR-Code-Head hat Quality Gate OK,
null ungelöste Issues, null Security Hotspots und kein akzeptiertes Issue. Der
historische S5778-Record ist FIXED, nicht akzeptiert oder offen.

## Geänderte Dateien

- `ci/tools/update-workflow-tools.py`
- `.github/workflows/update-workflow-tools.yml` (ein benutzerautorisierter passender Staging-Pfad)
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/c_source_contract.py`
- `tests/test_c_source_contract.py`
- `tests/test_nginx_intervention_url_ownership.py`
- `tests/test_nginx_upstream_security_contract.py`
- `reports/audits/change-records/CR-20260809-001-sonar-duplication-reduction.md`
- `reports/audits/change-records/CR-20260809-001-sonar-duplication-reduction.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Unittest-Suite | Bestanden: 51 Tests in 11.926 s |
| Follow-up-Suite für Updater/NGINX/Helper | Bestanden: 51 Tests in 12.602 s; das Updater-Modul behält 34 Testmethoden |
| Fokussierte Unittest-Suite auf rebased current master vor der engen Reparatur | Historische Reproduktion: 50 Tests bestanden und ein Fail-Closed-Publisher-Allowlist-Error nannte nur `.github/workflows/nginx-root-broker.yml` |
| Benutzerautorisierte Einpfad-Publisher-Reparatur | Bestanden: fokussierte Suite 51 Tests in 11.394 s; realer Coverage- und Fail-Closed-Negative-Controls für unzulässige/YAML-unsafe Workflows bestehen |
| `python -m py_compile` für die geänderten Python-Module | Bestanden |
| `make check-ci-security-contract` | Bestanden: 23 Tests; checksum-gesperrte actionlint-, zizmor- und gitleaks-Validierung bestanden |
| checksum-gesperrtes actionlint mit ShellCheck | Bestanden für `.github/workflows/*.yml` |
| checksum-gesperrtes `zizmor --offline .github/workflows` | Bestanden: keine Findings (88 vom Repository unterdrückte Findings wurden von zizmor gemeldet) |
| checksum-gesperrtes diff-range gitleaks | Bestanden: sechs Task-Commits gescannt, keine Leaks gefunden |
| `git diff --check HEAD` | Bestanden |
| Fokussierter Security-Diff-Scan | Bestanden: vollständige Sechs-Dateien-Abdeckung und null berichtspflichtige Findings |
| Fokussierter Security-Diff-Scan des autorisierten Workflows | Bestanden: vollständige Zwei-Dateien-Abdeckung und null berichtspflichtige Findings |
| Hosted-Checks für PR 256 Code-Head | Bestanden: alle anwendbaren Checks einschließlich SonarCloud Code Analysis, CodeQL, actionlint, zizmor, Pull-Request-Diff/Range, Struktur- und Connector-Contract-Checks |
| SonarCloud-Readback für PR 256 Code-Head | Quality Gate OK; 0 ungelöste Issues; 0 Security Hotspots; der einzige zwischenzeitliche S5778-Record ist FIXED |
| `make check-bilingual-docs` | Nur durch 20 fehlende Framework-Link-Ziele im nicht materialisierten Task-Worktree-Gitlink blockiert; der Change Record gab keinen Überschriften-/Identitätsfehler aus |
| `make check-doc-links` mit autoritativem `FRAMEWORK_ROOT` | Nur durch dieselben lokalen Gitlink-Link-Ziele blockiert |

Die fokussierte Suite umfasst die Updater-Tests, beide NGINX-Vertragstests und
die neuen C-Quellcode-Helfertests. Sie prüft kanonische Candidate-Payload-Bytes
und SHA-256-Eingabestabilität, CLI-Parsing, Validierungs-Ablehnungspfade,
Ausgabepfade und Lock-Datei-Anwendungsverhalten.

## Runtime-Evidence

Es war keine produktive Connector-Laufzeit erforderlich oder ausgeführt, weil
dies ein Python-Refaktor statischer CI-Sicherheitswerkzeuge und Vertragstests
ist. Die anwendbare Evidenz ist die fokussierte Unit-/Vertragssuite und der
versiegelte Security-Diff-Scan unter
`/var/tmp/codex/ModSecurity-conector/tmp/codex-security-scans/ModSecurity-conector/27e8756e212fd9452d99e285743dbadc43c814a6_20260809T053956Z/report.md`.

Auf dem Code-Change-Head c43df1b01771523a9f8903a252232a9002786cdd bestehen
gehostete GitHub Actions und die SonarCloud-PR-Analyse. Der PR bleibt
Draft/offen; daraus folgt keine Merge-Autorisierung.

## Nicht ausgeführte Prüfungen mit Begründung

- Das Repository hat keine Targets namens `test-ci-security-contract`,
  `test-workflow-action-pins`, `check-github-actions-workflows` oder
  `check-documentation`; die nächstliegenden vorhandenen Targets wurden, wo
  anwendbar, verwendet.
- `ruff` und `pyright` sind lokal nicht installiert und das Repository enthält
  kein konfiguriertes Ersatz-Target. Es wurde kein Tool installiert oder
  umgangen.
- actionlint, zizmor und gitleaks waren nicht vorinstalliert. Sie wurden
  ausschließlich über den checksum-gesperrten Repository-Fetcher in das
  externe Task-Verzeichnis geladen; alle drei anwendbaren Prüfungen bestanden
  anschließend.
- Der erste `make lint`-Lauf endete mit Exit 2, weil ein Parent-Test einen
  Framework-Quellpfad relativ zum isolierten Task-Worktree fest kodiert. Der
  gepinnte Framework-Quellcode existiert im autoritativen Checkout, aber dieser
  Test ignoriert die dokumentierte `FRAMEWORK_ROOT`-Überschreibung. Weder
  Framework-Inhalt noch Gitlink wurden zur Umgehung geändert.

## Bekannte Einschränkungen

Die angeforderte gehostete Analyse ist als maßgebliche Messung dokumentiert.
Das vollständige lokale Lint-Target ist weiterhin durch die
nicht materialisierte Framework-Gitlink-Abhängigkeit des Task-Worktrees
blockiert. Die nach dem Rebase erkannte Publisher-Pfad-Lücke ist unter der
ausdrücklichen Einpfad-Workflow-Autorisierung des Benutzers repariert.

Beide NGINX-Dateien stehen bei 0.0% Duplikation. Der Updater-Test erreicht
21.0% und 252 duplizierte Zeilen, eine Reduktion um 64.5% von 709 und unter dem
angeforderten 25%-Ziel. Der Produktions-Updater verbessert sich von 1,305 auf
951 Zeilen bei 41.5%, erreicht aber weder 50% noch das Unter-20%-Ziel. Jeder verbleibende
Block ist ein exaktes Parent-gegen-separat-gehörendes-Framework-Gegenstück. Die
Blöcke decken Pfad-/Symlink-Grenzen, Release-Provenance, Candidate-Schemas,
unveränderliche Lock-Mutation, Publisher-Scope und Reusable-Branch-
Verifikation ab. Ein Rewrite nur für CPD wäre eine sicherheitssensitive
Reimplementierung; ein Teilen erfordert eine koordinierte Framework-
Auslieferung außerhalb dieser Aufgabe. Exakte rohe Block-Evidenz liegt extern
im Task-Sonar-Evidence-Verzeichnis.

## Verbleibende Risiken

Das wichtigste Restrisiko ist Verhaltensdrift im sicherheitssensitiven Updater.
Es wird durch Erhaltungstests, explizite unveränderliche Schemaobjekte, ein
unabhängiges Diff-Audit, den fokussierten Security-Diff-Scan sowie die
beobachteten Hosted-Checks und SonarCloud-Neumessung reduziert. Das Audit
notierte, dass ein künstlicher, nicht normalisierter In-Memory-Action-Record
eine abgeleitete Release-URL als geändert einstufen könnte, bevor die
Same-Version-Validierung sie ablehnt. Gültige Lock-Normalisierung leitet diese
URL deterministisch ab; dies ist daher kein erreichbarer Lock-Datei-Pfad.

## Finaler Diff- und Review-Status

Die Refaktor-Commits sind überprüfbar und basieren auf current master. Die
benutzerautorisierte Zwei-Zeilen-Publisher-Reparatur stellt den endlichen
Source-/Staging-Vertrag wieder her, ohne Action-Pin, Berechtigung, Lock,
Framework, MRTS oder Gitlink zu ändern. PR 256 ist ein einzelner Draft-PR und
bleibt ungemergt. Die NGINX- und Updater-Test-Ziele sind erreicht; das
Updater-Source-Ziel ist durch die unabhängige Framework-Ownership-Grenze als
teilweise blockiert dokumentiert. Dieser Record autorisiert keinen Merge.
