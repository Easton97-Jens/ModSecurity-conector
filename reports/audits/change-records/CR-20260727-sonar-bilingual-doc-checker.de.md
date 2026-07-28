# Change Record: Parent-Bilingual-Dokumentationschecker-PR-Template-Literalextraktion und Erhalt der Diagnose-Reihenfolge für SonarQube Cloud S1192 und S3776

**Sprache:** [English](CR-20260727-sonar-bilingual-doc-checker.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-bilingual-doc-checker |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-`python:S1192` AZ9dAfch4Zz5JRbUl4id (wiederholtes PR-Template-Literal) und `python:S3776` AZ9dAfch4Zz5JRbUl4ie (kognitive Komplexität 18 > 15). |
| Grenze | Parent-`ci/checks/documentation/check-bilingual-docs.py`, sein Parent-Unit-Test, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Framework/MRTS-Inhalt und Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Status, GitHub-Status, Connector-/Runtime-Verhalten und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Der Bilingual-Dokumentationschecker wiederholte das PR-Template-Pfadliteral an
fünf Stellen: drei operative Pfadverwendungen und zwei Diagnosepräfixe.
Sonar-Regel `python:S1192` meldet diese Duplizierung. Dieselbe
Routine `check_change_record_pair()` verband Change-Record-Überschriftsprüfungen
mit Dateinamen- und Identitätsprüfungen, die Sonar-Regel `python:S3776` mit
kognitiver Komplexität 18 bei einem Schwellenwert von 15 maß. Der Batch muss
diese Verantwortlichkeiten explizit machen, ohne die PR-Template-
Inklusions-/Ausnahmesemantik oder die etablierte Diagnose-Reihenfolge zu ändern.

## Akzeptanzkriterien

- `PR_TEMPLATE_PATH` einführen und bei allen fünf bestehenden PR-Template-
  Pfadreferenzen verwenden.
- `.github/pull_request_template.md` von English/German-Companion-Pairing
  ausnehmen, aber seine Required-Template-Validierung und pfadqualifizierten
  Diagnosen beibehalten.
- Die Change-Record-Überschrifts- sowie Dateinamen-/Identitätsprüfungen in
  fokussierte Helper extrahieren, ohne die Early-Return-Regeln des Wrappers
  oder seine Diagnose-Reihenfolge zu ändern.
- Fokussierte Regressionen für das beibehaltene PR-Template-Verhalten und die
  exakte Change-Record-Diagnosesequenz ergänzen.
- Dieses englisch/deutsche Change-Record-Paar und beide Indizes pflegen und
  die Validierungen dieses Dokumentationssubtasks `tests.test_bilingual_docs`
  und `git diff --check` festhalten.

## Implementierungsentscheidung und Begründung

`PR_TEMPLATE_PATH = Path(".github/pull_request_template.md")` ist der einzige
Owner des PR-Template-Pfads. `pair_required()`, `checked_markdown_files()` und
`check_pr_template()` behalten ihr bisheriges Verhalten, indem sie denselben
relativen `Path` vergleichen oder anhängen; ausgegebene Diagnosen nennen weiter
denselben Pfad.

`check_change_record_headings()` führt die bestehenden English-then-German-
Überschriftsprüfungen aus. `check_change_record_filename_and_identity()` führt
anschließend die bestehenden Dateinamen- und Identitätsprüfungen aus.
`check_change_record_pair()` behält seinen Non-Record/README-Early-Return, das
Heading-only-Template-Verhalten und die geordnete Erweiterung um die Diagnosen
des zweiten Helpers bei. Die Extraktion bewahrt somit das Verhalten, statt die
Change-Record-Policy oder Validierungssemantik zu ändern.

## Geänderte Dateien

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Die anfängliche relative Worktree-Auswahl `.venv/bin/python` war
  `blocked_environment` (Exit 127): Dieser isolierte Worktree enthält keine
  solche Virtual-Environment-Executable; aus diesem Aufruf lief kein Test.
- Die Environment-Auswahl mit dem bestehenden Parent-Virtual-Environment
  bestand: Sein `sys.prefix` war das Parent-`.venv` und unterschied sich von
  `sys.base_prefix`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`
  bestand: 18 Tests in 0.043s.
- `rtk proxy git diff --check` bestand ohne Whitespace-Diagnosen.

## Security-Auswirkung

`not_applicable` für die Produkt-Sicherheitsgrenze: Dies ist ein
Maintainability-Refactoring der repository-eigenen Dokumentationsvalidierung.
Es ändert keine Input-Trust-Grenze, Path-Containment-Regel,
Link-Resolution-Regel, Subprocess-, Authorization-, Netzwerk- oder
Scanner-Control-/Suppression-Logik. Für diesen Wartungsbatch des
Dokumentationscheckers wird kein Codex-Security-Workflow ausgelöst.

## Runtime-Evidence

Es wurden keine Connector-, Protokoll-, Host-, Framework-, MRTS-, Report-
Generator- oder Produktions-Runtime ausgeführt oder geändert. Die fokussierte
Unit-Suite prüft nur Checker-Logik mit In-Memory-temporären Repository-Layouts;
sie ist keine Runtime-Evidence.

## Bekannte Einschränkungen

Dieser Dokumentationssubtask hält nur `tests.test_bilingual_docs` und
`git diff --check` fest. Repository-weite Dokumentations-/Link-Checks, Builds,
Linter, CI, Review, PR-Status und gehostete SonarQube-Cloud-Analyse bleiben
für die Primärkandidatenvalidierung ausstehend und werden hier nicht behauptet.

## Verbleibende Risiken

Ein nicht von der fokussierten Suite abgedeckter Aufrufer könnte von einer
subtilen Diagnose-Reihenfolge oder PR-Template-Pfaddarstellung abhängen. Die
ergänzten Regressionen sichern den PR-Template-Ausnahme-/Inklusionsvertrag und
die vollständige geordnete Change-Record-Diagnoseliste ab. Die zwei Sonar-
Receipt-IDs können nicht extern als gelöst behandelt werden, bis SonarQube
Cloud den exakten ausgelieferten Head analysiert.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Dokumentations-/Link-Checks, Builds, Linting und nicht
  zugehörige Unit-Suites sind für die Primärkandidatenvalidierung ausstehend;
  sie liegen außerhalb der scoped checks dieses Dokumentationssubtasks.
- Keine GitHub-CI, Remote-SonarQube-Cloud-PR-Analyse, kein Review, Pull
  Request, Commit, Push, Merge, Default-Branch-Update oder Framework/MRTS-
  Action ist als Teil dieses Dokumentationsbeitrags erfolgt.

## Finaler Diff- und Review-Status

Dies ist ein uncommitteter lokaler Kandidat auf
`agent/sonar-bilingual-doc-checker-20260727`, basierend auf
`1b0f8825f3510b99b603bb6cd6f0777e1710358e`. Delivery ist nur geplant: Falls
später autorisiert, ist sie auf einen Draft-Pull-Request begrenzt. Bevor einer
der beiden Receipts extern als gelöst beschrieben wird, müssen lokaler HEAD,
Remote-Task-Branch-SHA und Draft-PR-Head-SHA als gleich beobachtet werden und
SonarQube Cloud muss sein Ergebnis für genau diesen Head berichten. Es werden
kein Merge, keine Parent-`master`-Änderung und keine externe Sonar-Auflösung
behauptet.
