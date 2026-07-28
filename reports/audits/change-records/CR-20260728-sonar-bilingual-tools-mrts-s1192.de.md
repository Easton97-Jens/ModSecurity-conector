# Change Record: Parent-`tools/MRTS`-Literalextraktion und direkte Git-Fixture-Abdeckung für SonarQube Cloud S1192

**Sprache:** [English](CR-20260728-sonar-bilingual-tools-mrts-s1192.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-bilingual-tools-mrts-s1192 |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Tracking | Parent-SonarQube-Cloud-`python:S1192`-Kandidat für das wiederholte operative `tools/MRTS`-Literal. Die aktuelle Aufgabe bezeichnet einen Parent-only-PR-#157-Kandidaten; sie belegt weder einen gehosteten Pull Request noch eine externe SonarQube-Cloud-Auflösung. |
| Grenze | Parent-`ci/checks/documentation/check-bilingual-docs.py`, Parent-`tests/test_bilingual_docs.py`, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Framework/MRTS-Inhalt und Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, externer SonarQube-Cloud-Status, GitHub-Status, Connector-/Runtime-Verhalten und Delivery liegen außerhalb dieses begrenzten Parent-only-Kandidaten. |

## Motivation und Problemstellung

`check_tools_mrts_clean()` verwendete den festen `tools/MRTS`-Pfadstring an
drei operativen Stellen: beim Parent-`git status`-Pathspec, beim Framework-
Presence-Guard und beim Framework-`git status`-Pathspec. SonarQube-Cloud-Regel
`python:S1192` identifiziert dieses wiederholte Literal. Die Extraktion muss
die bestehende Pathspec-Reihenfolge und alle Diagnosen bewahren, während direkte
Fixtures beweisen müssen, dass der Checker nicht zugehörigen Dirty-State
ignoriert und Parent- sowie Framework-`tools/MRTS`-Dirty-State über echte
Git-Repositories meldet.

## Akzeptanzkriterien

- `TOOLS_MRTS = "tools/MRTS"` definieren und nur an den drei bestehenden
  operativen Stellen in `check_tools_mrts_clean()` verwenden.
- Die Parent- und Framework-`git status`-Argumentreihenfolge sowie die exakten
  `tools/MRTS`-Diagnosen bewahren.
- Direkte temporäre Nested-Git-Fixtures für nicht zugehörigen Dirty-State,
  Parent-`tools/MRTS`-Dirty-State und Framework-`tools/MRTS`-Dirty-State
  ergänzen.
- In jedem direkten Fixture-Test die vollständigen geordneten
  `CHECKER.git_status`-Aufrufe einschließlich ihrer Working-Directory-`Path`-
  Argumente prüfen.
- Dieses englisch/deutsche Change-Record-Paar und beide Indizes pflegen, ohne
  unbeobachtete gehostete PR-, CI-, SonarQube-Cloud-, Review- oder Merge-Fakten
  zu behaupten.

## Implementierungsentscheidung und Begründung

`TOOLS_MRTS = "tools/MRTS"` ist ein moduleigener Owner für das duplizierte
operative Pfadliteral. Es ersetzt nur den Parent-Status-Pathspec, den
Framework-Directory-Presence-Join und den Framework-Status-Pathspec. Der
kombinierte Parent-Framework-Pathspec bleibt
`modules/ModSecurity-test-Framework/tools/MRTS`, daher bleiben Befehlsreihenfolge
und bestehender Fehlertext unverändert.

Die additiven Tests initialisieren temporäre Parent- und verschachtelte
Framework-Git-Repositories mit committed, getrackten Baselines einschließlich
des Parent-Framework-Gitlinks und wrappen anschließend das echte
`CHECKER.git_status`. Sie decken nicht zugehörige schmutzige Markdown-Dateien
als legitimen Clean-Control, eine schmutzige Parent-`tools/MRTS/.gitkeep` und
eine schmutzige Framework-`tools/MRTS/.gitkeep` ab. Jeder vergleicht die
gesamte geordnete `call_args_list` einschließlich der tatsächlichen
`cwd`-`Path`-Werte und hard-codiert die erwarteten Git-Argumente und Diagnosen,
statt sie aus `TOOLS_MRTS` abzuleiten oder nur einen mock-spezifischen Helper zu
testen.

## Geänderte Dateien

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_bilingual_docs` bestand im isolierten Parent-Worktree: 21 Tests in 0.259s, `OK`.
- `rtk proxy -- git diff --check` bestand für den finalen vollständigen Kandidaten nach den Source/Test-Änderungen, diesem Dokumentationspaar und beiden Indexaktualisierungen; es gab keine Whitespace-Diagnosen.
- `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/checks/documentation/check-bilingual-docs.py` endete mit Exit 1, `blocked_external_dependency`: Es meldete nur fehlende `modules/ModSecurity-test-Framework`-Dokumentations-/Regellinkziele in diesem isolierten Worktree, ohne Fehler für das geänderte Change-Record-Paar oder die Indizes.
- `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/checks/documentation/check-repository-path-references.py` endete mit Exit 2, `blocked_external_dependency`, wegen derselben fehlenden Framework-Linkziele und ohne Fehler für das geänderte Change-Record-Paar oder die Indizes.
- Eine schreibfreie enge Strukturprüfung, die `check-bilingual-docs.py` lädt, bestand: erforderliche Change-Record-Überschriften und Identitäten, wechselseitige Sprachumschalter, beide Indexreferenzen und die ausgewählten gemeinsamen technischen Literale sind vorhanden.
- Ein disposable Exact-Candidate-Parent-/Framework-Overlay bestand die vollständige Dokumentationsroute: Parent-bilinguale Dokumentation (`bilingual docs ok`), Parent-Repository-Path-Referenzen (`repository path references: PASS`) und Framework-Dokumentlinks (`doc links ok`). Es verwendete nur das read-only Parent-gepinnte Framework-Archiv `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` und temporäre lokale Git-Baselines, die der Checker benötigt; weder Framework-Source noch ein Gitlink wurden geändert.

## Security-Auswirkung

Dies ist sicherheitsrelevante Checker-Wartung:
`check_tools_mrts_clean()` ruft `git`-Subprozesse auf und schützt die
Parent/Framework/MRTS-Cleanliness-Grenze. Ein fokussierter Command-/Path-
Integrity-Review war erforderlich und genehmigt. Seine Invariante ist, dass
source-controlled Pathspecs in den exakten Parent- und Framework-Working-
Directories laufen, schmutzige geschützte Pfade melden und den geprüften Scope
nicht erweitern. Der Review stellte fest, dass `TOOLS_MRTS` source-controlled
ist sowie dass die exakte bestehende argv-Reihenfolge, die `cwd`-Werte, die
Diagnosen und die fail-closed Dirty-Path-Controls bewahrt bleiben. Die direkten
Git-Fixtures prüfen den legitimen Unrelated-Dirt-Control und beide geschützten
Dirty-Path-Fehler. Es wurde kein neues Finding identifiziert.

Ein bereits bestehender Silent-Nonzero-`git`-Edge-Case, bei dem ein
fehlgeschlagener Befehl weder stdout noch stderr an `git_status()`
zurückgeben könnte, bleibt
unverändert und liegt außerhalb dieses Literal-only-Kandidaten. Dieser Record
behauptet nicht, dass dieser Edge-Case behoben wurde. Die Fixtures verwenden
lokale temporäre Repositories ohne Credentials oder Netzwerkanbindung.

## Runtime-Evidence

Es wurde keine Connector-, Protokoll-, Host-, Framework-, MRTS-, Report-
Generator- oder Produktions-Runtime ausgeführt oder geändert. Die fokussierte
Unit-Suite prüft nur statische Checker-Logik und temporäre lokale Git-
Repositories; sie ist keine Runtime-Evidence.

## Bekannte Einschränkungen

Die direkten Fixture-Tests benötigen ein lokales `git`-Executable; es war im
beobachteten fokussierten Lauf verfügbar. Sie führen keinen gehosteten PR,
keine GitHub Actions, keine SonarQube Cloud, keinen Produktions-Connector und
keine bereitgestellte Framework/MRTS-Runtime aus. Die vollständigen Parent-
Bilingual- und Repository-Path-Skripte sind in diesem isolierten Worktree durch
fehlende Framework-Dokumentations-/Regellinkziele blockiert. Derselbe exakte
Kandidat bestand diese Prüfungen im oben festgehaltenen disposable
Parent-/Framework-Overlay; das isolierte Worktree-Ergebnis belegt daher keinen
Fehler im geänderten Change-Record-Paar oder den Indizes.
Ein bereits bestehender Silent-Nonzero-`git`-Edge-Case bleibt unverändert und
außerhalb dieses Literal-only-Scopes.

## Verbleibende Risiken

Eine nicht getestete Git-Implementierung, Status-Darstellung oder ein Aufrufer
außerhalb der drei Testfälle könnte ein Verhalten offenlegen, das von den
temporären Fixtures nicht dargestellt wird. Die direkten Fixtures bewahren und
prüfen die exakten aktuellen Aufrufe und Diagnosen für die begrenzten
Parent/Framework-Fälle. Der `python:S1192`-Kandidat darf nicht als extern
gelöst beschrieben werden, bis SonarQube Cloud den exakten ausgelieferten Head
analysiert.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Builds, Linter, Integrations-/Runtime-Matrizen und nicht
  zugehörige Test-Suites liegen außerhalb dieses kleinen Parent-only-
  Dokumentations-/Checker-Kandidaten.
- `make check-doc-links` wird nicht ausgeführt, weil es zuerst
  `check-framework` und den Framework-Dokumentations-Link-Checker aufruft; der
  aktuelle Scope ist Parent-only. Sein Parent-Repository-Path-Static-Checker
  wurde direkt ausgeführt, ist aber durch dieselben fehlenden Framework-
  Linkziele blockiert.
- Keine GitHub-CI, Remote-SonarQube-Cloud-PR-Analyse, kein gehosteter Pull
  Request, Review, Commit, Push, Merge, Default-Branch-Update, Framework-
  Aktion, MRTS-Aktion oder Gitlink-Update ist als Teil dieses Kandidaten erfolgt.

## Finaler Diff- und Review-Status

Dies ist ein lokaler Parent-only-Kandidat auf
`agent/sonar-652-bilingual-tools-mrts-s1192-20260728`, basierend auf
`8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Delivery steht aus. Die
PR-#157-Bezeichnung der Aufgabe ist nur ein Kandidatenlabel: Es werden kein
gehosteter PR, keine Remote-Head-SHA, kein CI-Ergebnis, kein Quality Gate, kein
Review und kein Merge belegt. Bevor dieser Kandidat als extern verifiziert
beschrieben wird, müssen lokale, Remote- und gehostete PR-Head-SHAs als gleich
beobachtet werden und die erforderlichen gehosteten Prüfungen für genau diesen
Head festgehalten sein. Diese Dokumentationsbeitrag führt kein Staging, keinen
Commit, keinen Push, keinen Merge, keine Parent-`master`-Änderung, keine
Framework/MRTS-Änderung und kein Gitlink-Update aus.
