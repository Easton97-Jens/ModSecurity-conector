# Change Record: Parent-Python-3.13-Workflow-Vertrag und sicherer Patch-Updater

**Sprache:** [English](CR-20260720-python-313-workflow-contract.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260720-python-313-workflow-contract` |
| Datum (UTC) | `2026-07-20` |
| Basis-Revision | `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` |
| Tracking | Parent-Python-Version-/Workflow-Vertrag. Dieser Record enthält absichtlich kein Commit-, Pull-Request-, CI-, Review- oder Delivery-Ergebnis. |
| Grenze | Nur Parent-Python-Versionsquelle, Workflow-Verträge, Updater-Validierung und zweisprachige Dokumentation; Framework und MRTS liegen außerhalb des Scopes und bleiben durch diese Dokumentationsarbeit unverändert. |

## Motivation und Problemstellung

Die Baseline verwendet eine Mischung aus Minor-only-`3.13`-Setup-Schritten
und ambienten oder gebootstrappten Python-Ausführungspfaden. Eine Minor-only-
Deklaration kann auf ein späteres Patch-Release driften, während ein ambienter
Interpreter weder eine reproduzierbare Versionsquelle noch ein Nachweis ist,
dass `python` und `python3` dieselbe Runtime benennen.

Der Parent benötigt außerdem einen sicheren Weg, einen neuen stabilen
Python-3.13-Patch vorzuschlagen, ihn jedoch niemals automatisch anzuwenden.
Ermittlung von Netzwerk-Metadaten, Kompatibilitätsvalidierung und ein
schreibfähiger Pull-Request-Publisher dürfen nicht dieselbe Trust-Grenze
teilen.

## Akzeptanzkriterien

- Eine eingecheckte Root-Datei `.python-version` enthält exakt stabiles
  `3.13.14` und ist die einzige maschinenlesbare Interpreterquelle.
- Jeder der 22 inventarisierten Parent-Python-ausführenden Jobs richtet diese
  Quelle mit `python-version-file: .python-version` und `check-latest: false`
  vor seiner ersten Python-Nutzung ein und validiert danach die
  `python`/`python3`-Äquivalenz.
- Floating `3.13` wird wegen Patch Drift abgelehnt; eine exakte Version plus
  permanenter Canary wird abgelehnt, weil eine unabhängige schreibgeschützte
  Candidate-Validierungs-Stage die erforderliche Kompatibilitätskontrolle
  liefert.
- Der Updater verwendet nur `https://www.python.org/api/v2/downloads/release/?is_published=true`, validiert HTTPS, den exakten Host `www.python.org`, keine Redirects,
  `application/json`, begrenzte Daten und das Schema, bevor er den höchsten
  veröffentlichten Nicht-Prerelease-stabilen `3.13.N`-Patch auswählt. Er kann
  weder downgraden noch eine Minor-Serie überqueren.
- `--check` ist schreibgeschützt und von Publisher-only-`--update` getrennt;
  die drei Jobs sind `resolve-python-patch`, `validate-python-patch` und
  `create-python-update-pr`.
- Der Updater wird nur durch seinen Montags-Schedule und manuellen
  `workflow_dispatch` ausgelöst; jeder Job ist auf die Default-Branch-Ref
  gegatet und checkt den vertrauenswürdigen Default-Branch ohne Submodules oder
  persistierte Credentials aus.
- Resolver und Validator bleiben schreibgeschützt. Nur der Default-Branch-
  gated Publisher erhält `contents: write` und `pull-requests: write` und darf
  erst nach Candidate-Neuauflösung mit `--expected-version` einen
  vorgeschlagenen Pull Request erstellen.
- Der Publisher verwendet den konstanten Branch `automation/update-python-313`
  und den stabilen Titel `chore(ci): propose Python 3.13 patch update`. Er
  erstellt einen Draft Pull Request einmalig oder aktualisiert sicher nur den
  bestehenden repository-eigenen Draft-Update-Pull-Request für diesen Branch,
  nachdem Head, Default-Base und deaktivierter automatischer Merge geprüft
  wurden; einen vorhandenen Branch ohne diesen exakten Pull Request weist er
  zurück, sodass er weder doppelte Vorschläge erzeugt noch force-pusht.
- Die Auswahl eines bestehenden PR empfängt ihre begrenzte REST-Antwort direkt
  von `gh api` auf stdin und hat keinen aufrufergesteuerten Response-Dateipfad.
  Die strikte Duplicate-Key-JSON-Validierung überschreitet daher keine
  Response-Datei- oder Symlink/TOCTOU-Grenze.
- Der erzeugte englisch/deutsche Pull-Request-Body dokumentiert vorherige und
  vorgeschlagene Version, offizielle Release-Identität, Metadatenquelle,
  Validierungsworkflow/-Run-URL, `.python-version` als einzige geänderte Datei,
  die beibehaltene Python-3.13-Minor-Version und keinen automatischen Merge.
- Kein Auto-Merge, Default-Branch-Write, Force-Push, Konsum von Repository-
  oder benutzerbereitgestellten `secrets.*`, Submodule-Initialisierung oder
  Ausführung beliebiger Project-Workloads gehört zum Updater-Vertrag. Der
  Publisher verwendet für die Pull-Request-Erstellung nur GitHubs automatisch
  bereitgestelltes Job-Token, beschränkt auf seine zwei job-begrenzten
  Schreibrechte.
- Englische und deutsche Dokumentation sowie Change-Record-Paare enthalten
  gleichwertige technische Fakten, Grenzen und Evidence-Grenzen.

## Implementierungsentscheidung und Begründung

Die ausgewählte Strategie ist exaktes stabiles `3.13.14` aus der eingecheckten
Datei `.python-version`. `actions/setup-python` muss sie über
`python-version-file` mit `check-latest: false` verwenden; ein Workflow darf
kein zweites Interpreter-Versionsliteral enthalten. Das verhindert Patch Drift
und bewahrt eine einzelne reviewbare Versionsänderung.

| Strategie | Disposition | Grund |
| --- | --- | --- |
| Floating `3.13` | Abgelehnt | Künftige Runner-/Tool-Cache-Auflösung kann den Patch ohne reviewte Source-Änderung ändern. |
| Exaktes `3.13.14` aus `.python-version` | Ausgewählt | Eine eingecheckte Quelle erzeugt deterministisches Setup für jeden abgedeckten Job. |
| Exakte Version plus permanenter Canary | Abgelehnt | Der isolierte Candidate-Validierungsjob prüft den tatsächlich vorgeschlagenen Patch vor dem Publishing, daher würde ein permanenter Canary die relevante Kontrolle duplizieren. |

Die vollständige Baseline-Inventarisierung steht im
[Parent-CI-Python-Versionsvertrag](../../../docs/build/README.de.md#parent-ci-python-versionsvertrag): 22 Python-ausführende Jobs, bestehend aus 12
ehemaligen Minor-only-Setup-Pfaden und 10 ehemals ambienten oder
gebootstrappten Pfaden, die vor dieser Implementierung explizites Setup
benötigten. Die Tabelle identifiziert jeden
Workflow, Job und direkte oder indirekte Python-Ausführungskette. Sie schließt
Jobs ohne nachgewiesenen Python-Ausführungspfad absichtlich aus.

Der neue Updater-Workflow ist bewusst von dieser Inventarisierung getrennt:

| Job | Vertrag |
| --- | --- |
| `resolve-python-patch` | Läuft mit dem aktuellen kanonischen Interpreter, fragt die feste offizielle strukturierte API ab und validiert sie strikt; verwendet dann schreibgeschütztes `--check`, um höchstens einen höheren stabilen `3.13.N`-Candidate auszugeben. |
| `validate-python-patch` | Richtet den unabhängig aufgelösten Candidate-Patch ein und validiert ihn schreibgeschützt, bevor irgendein Publisher startet. |
| `create-python-update-pr` | Läuft mit dem aktuellen kanonischen Interpreter, löst den Candidate mit `--expected-version` erneut auf und verwendet Publisher-only-`--update`, um aus einem Default-Branch-gated Kontext einen PR zu erstellen. |

Die einzigen Trigger sind der geplante Montagslauf und manueller
`workflow_dispatch`; es gibt keinen Push- oder Pull-Request-Trigger. Jeder Job
ist auf die Default-Branch-Ref gegatet und checkt den vertrauenswürdigen
Default-Branch ohne Submodules oder persistierte Checkout-Credentials aus. Der
Candidate-Validierungsjob löst den Candidate erneut auf, führt den fail-closed
statischen Vertrag und Kompilierungsprüfungen aus und startet fokussierte
Parent-native Tests, bevor der Publisher berechtigt ist.

Dies ist eine Check/Update-Trennung: Der Candidate kann nicht allein deshalb
geschrieben werden, weil er in Response-Metadaten erschien, und der Publisher
validiert ihn an der Schreibgrenze erneut. Resolver und Validator haben keine
Schreibrolle. Der Publisher nutzt nur `contents: write` und
`pull-requests: write`; er hat keine Berechtigung zu mergen, den Default
Branch zu beschreiben, force-zupushen, Repository- oder
benutzerbereitgestellte `secrets.*` zu konsumieren, Submodules zu
initialisieren oder beliebige Project-Workloads auszuführen. Seine
Repository-Ausführung ist auf die festen Interpreter-Verifikations- und
Updater-Pfade begrenzt, und sein GitHub-bereitgestelltes Job-Token wird nur für
die Pull-Request-Erstellung verwendet.

Der Publisher verwendet den konstanten Branch `automation/update-python-313`
und einen stabilen Titel. Er erstellt einen Draft Pull Request, wenn dieser
Branch fehlt; bei einem bestehenden repository-eigenen Draft-Update-Pull-
Request prüft er zuerst das exakte Head-Repository, die Default-Base und den
deaktivierten automatischen Merge, beschränkt dann dessen Merge-Base-Diff auf
`.python-version` und aktualisiert denselben Pull Request ohne Force-Push. Ein
bereits vorhandener Remote-Branch ohne diesen exakten offenen Update-Pull-
Request ist ein fail-closed Fehler und wird nicht überschrieben. Der
englisch/deutsche Body umfasst stets vorherige und vorgeschlagene Version,
Release-Identität, Metadatenquelle, Validierungsworkflow/-Run-URL,
Changed-File-Scope, beibehaltene Minor-Version und das Fehlen eines
automatischen Merge.

## Security-Auswirkung

Die kontrollierte Eingabe sind Release-Metadaten der festen offiziellen API.
Der vertrauenswürdige Sink ist ein vorgeschlagenes `.python-version`-Update in
einem Pull Request, keine Default-Branch-Mutation. Strikte URL-, Transport-,
Content-Type-, Größen-, Schema-, Published-/Non-Prerelease-, Exact-Series-,
monotonic-Patch- und Expected-Version-Prüfungen begrenzen diese Eingabe, bevor
sie den schreibfähigen Publisher erreicht.

Der unabhängige Validierungsjob verhindert, dass der Publisher Resolver-Output
als ausreichende Kompatibilitäts-Evidence behandelt. Default-Branch-Gating,
job-begrenzte Schreibrechte, keine externen oder benannten `secrets.*`, keine
Submodules und keine beliebigen Project-Workloads halten nicht
vertrauenswürdige Repository- oder Metadateninhalte von der Publisher-Trust-
Grenze fern. Das GitHub-bereitgestellte Job-Token ist auf die Pull-Request-
Erstellung begrenzt. Dies ist der eingecheckte statische Sicherheitsvertrag,
keine Behauptung, dass bereits eine GitHub-Actions-Runtime-Control beobachtet
wurde.

## Geänderte Dateien

Die eingecheckte Parent-Implementierung ändert diese Pfadgruppen:

- `.python-version` als einzige maschinenlesbare Exact-Version-Quelle.
- Die 18 in der Inventarisierung aufgeführten bestehenden Python-ausführenden
  Workflows und den neuen Updater-Workflow
  `.github/workflows/update-python-version.yml`.
- `ci/checks/common/check-python-version-contract.py` und
  `ci/checks/common/check-python-interpreter-contract.py` samt dem
  `Makefile`-Einstiegspunkt, der den statischen Vertrag aufruft.
- `scripts/update-python-version.py`, Parent-native Updater-/Contract-
  Testmodule und deren Fixtures.
- `docs/build/README.md`
- `docs/build/README.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260720-python-313-workflow-contract.md`
- `reports/audits/change-records/CR-20260720-python-313-workflow-contract.de.md`

Framework und MRTS werden nicht geändert. Dieser Record berichtet nur die
unten beobachtete lokale Implementierungsevidenz; er leitet kein Remote-
Ergebnis her.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Isoliertes Python 3.13.14 mit `check-python-version-contract.py --json`, `check-python-interpreter-contract.py` und `make check-python-version-contract` | bestanden: die statische Inventarisierung und die genaue Interpreter-Identität sind gültig. |
| Isoliertes Python 3.13.14 mit `scripts/update-python-version.py --check --json` gegen die Live-feste offizielle API | bestanden: Es meldete `current` mit aktueller und höchster Version `3.13.14`; `.python-version` blieb unverändert. |
| `python3 -m unittest -v tests.test_update_python_version` | bestanden: 21 Updater-Unit-Tests. |
| `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml ci/fixtures/workflow-permission-contract/*.yml` | bestanden. |
| `zizmor --offline .github/workflows` | bestanden ohne Findings. |
| Isoliertes Python 3.13.14 mit `python3 -m unittest discover -s tests -v` | blockiert/nicht grün: 355 Tests liefen; 13 Failures und vier Errors hängen von fehlenden Framework-Dateien in diesem Sparse-Worktree ab, darunter Framework-Runner, -Checks und Provisioning-Skripte. |
| `make setup-dev` mit dem isolierten Python | blockiert, Exit 2: Der Framework-Bootstrap versuchte, die nicht verfügbare lokale `.venv`-Entwicklungsumgebung zu erstellen. |
| `make lint` mit dem isolierten Python | blockiert, Exit 2: Shell-Syntax- und Python-Kompilierungsprüfungen liefen, dann stoppte die fehlende Framework-Datei `ci/checks/catalog/no_crs_baseline.py` das Target. |
| `make check-bilingual-docs` und der direkte Repository-Pfadchecker | durch dieselben vorbestehenden fehlenden Framework-Dokumentationslink-Ziele blockiert; kein Pfad dieses Dokumentations-Deliverables erscheint in den gemeldeten Fehlern. |

Diese lokalen Ergebnisse validieren den eingecheckten statischen Vertrag und
die Updater-Pfade. Sie stellen keinen GitHub-Actions-Lauf, Pull Request, Review
oder Delivery-Erfolg dar.

## Runtime-Evidence

Nicht anwendbar. Dies ist ein Parent-CI-/Workflow- und Dokumentationsvertrag;
er startet keinen Connector und etabliert keine HTTP/1.1-, HTTP/2-, HTTP/3-,
CRS-, Framework-, MRTS- oder Host-Runtime-Kompatibilitäts-Evidence.

## Nicht ausgeführte Prüfungen mit Begründung

- `make check-doc-links` enthält den Framework-Link-Checker. Auch sein Parent-
  Pfadchecker ist durch dieselben Sparse-Worktree-Framework-Links blockiert;
  kein Workaround ändert Framework oder MRTS für diese Parent-Aufgabe.
- GitHub-Actions-, Pull-Request-, Review-, SonarQube- und Merge-Evidence
  benötigen einen beobachteten exakten Delivery-Head; keine davon wird aus
  dieser Dokumentation hergeleitet.
- Kein Connector-Build, Runtime-, Framework- oder MRTS-Check wird für dieses
  Workflow-Contract-Implementierung ausgewählt. Framework und MRTS bleiben
  außerhalb des Scopes.

## Bekannte Einschränkungen

Dieser Record dokumentiert einen statischen Vertrag und lokale Prüfungen. Er
kann weder das Verhalten von GitHub-gehosteten Runnern noch künftige API-
Verfügbarkeit oder die Kompatibilität eines Candidate-Patches beweisen, bis die
unabhängige Validierungs-Stage tatsächlich läuft. Die Baseline-
Inventarisierung identifiziert die bekannten Python-Ausführungsketten; ein
späterer Workflow, der Python-Nutzung einführt, muss zum Validator und zur
Dokumentation ergänzt werden.

## Verbleibende Risiken

Eine offizielle API-Response kann nicht verfügbar sein oder ihr Schema ändern,
und ein gültiger Candidate-Patch kann dennoch eine Kompatibilitätsregression
offenlegen. Fail-closed-API-Validierung, striktes Parsing, No-Downgrade-Regeln,
unabhängiges Candidate-Setup und PR-only-Publishing mindern diese Risiken,
beseitigen sie jedoch nicht. Dieser Record enthält keine Risikoakzeptanz,
Runtime-Ergebnis oder Delivery-Ergebnis.

## Finaler Diff- und Review-Status

Die zweisprachige Dokumentation und der Change Record spiegeln die
eingecheckte Implementierung und beobachtete lokale Validierung wider.
Framework-abhängige Link- und Full-Suite-Prüfungen bleiben wie oben festgehalten
blockiert; Commit, Pull Request, Exact-Head-CI-/Review-/SonarQube-Evidence und
Delivery-Status werden absichtlich erst nach Beobachtung behauptet.
