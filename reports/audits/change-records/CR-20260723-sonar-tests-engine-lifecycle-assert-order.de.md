# Change Record: Engine-Lifecycle-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260723-sonar-tests-engine-lifecycle-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260723-sonar-tests-engine-lifecycle-assert-order` |
| Datum (UTC) | `2026-07-23` |
| Basis-Revision | `5b8db00d44ab24f3a9f4216a00f7edee977b6898` |
| Grenze | Ausschließlich Parent-Testquelle, dieses englische/deutsche Change-Record-Paar und Indizes. Framework, MRTS, Gitlinks, produktiver Connector-Quellcode, Scanner-Konfiguration, Quality Gates, Suppressions und Runtime-Verhalten bleiben unverändert. |
| Finding-Verknüpfung | `FND-SONAR-0030`; 33 offene Parent-`python:S3415`-Code-Smells in `tests/test_engine_lifecycle_artifacts.py`. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Analyse meldet 33 `python:S3415`-Befunde in einem
Parent-Testmodul. Die betroffenen `unittest.TestCase.assertEqual`-Aufrufe sowie
ein `assertNotEqual`-Aufruf setzten einen festen erwarteten Wert vor das
beobachtete Prozessergebnis, geparste Payload oder einen Lifecycle-Zähler. Die
Vergleiche enthielten bereits die beabsichtigten Testprädikate; lediglich ihre
Diagnosereihenfolge nicht.

Die Live-Scoping-Abfrage lieferte genau 33 offene `MAJOR`-Code-Smells für diese
Datei. Sie liegen auf den Zeilen 115, 117, 128–145, 188, 193–198, 226,
230–232, 241 und 253 in der stabilen Key-Gruppe
`AZ-KYVW0fYmbqbBXVNJ*`/`...VNK*`. Ihre Issue-Flows kennzeichnen den ersten
Operanden als Expected und den zweiten als Actual.

## Akzeptanzkriterien

- Ausschließlich bei den 33 ausgewählten Assertion-Aufrufen die ersten beiden
  Operanden tauschen, sodass der beobachtete Wert zuerst und der feste Expected-
  Wert danach steht.
- Alle Prädikate, optionalen Fehlermeldungen, Subprocess-Aufrufe,
  Temporary-Artifact-Eingaben, Lifecycle-Felder, Expected-Werte und
  Testergebnisse bewahren.
- Die drei nicht ausgewählten mehrzeiligen Hash-Assertions unverändert lassen,
  weil sie nicht im Live-Sonar-Umfang dieses Batches liegen.
- Das vollständige betroffene Parent-Testmodul und ein AST-/Source-Inventar
  bestehen lassen, das alle 33 ausgewählten Aufrufe als Actual-first belegt.
- Beide Change-Record-Sprachen und beide Indizes äquivalent halten.
- Frische exakte-Head-SonarQube-Cloud- und Hosted-Check-Evidence erhalten,
  bevor ein ausgewählter Key im Draft-PR als gelöst bezeichnet wird.

## Implementierungsentscheidung und Begründung

Der Patch tauscht nur die ersten zwei Positionsargumente. Prozess-Returncodes,
der Engine-Version-String, Transaction-/Lifecycle-Werte und der Returncode der
Payload-Eingabeablehnung stehen nun als beobachteter Wert zuerst; ihre
vorhandenen Integer-, String- oder Listenkonstanten bleiben Expected-Werte. Das
Returncode-Meldungsargument verbleibt an dritter Stelle. Kein
Assertion-Prädikat, keine Fixture, kein Event, kein Temporary-Pfad, kein
Executable und kein Writer-Aufruf änderte sich.

Dies ist absichtlich ein Single-File-Maintainability-Batch. Die 33 Live-Zeilen
teilen ein Testmodul und dieselbe `actual, expected`-Korrektur, während die
unberührten Hash-Assertions ausgeschlossen bleiben, damit der Umfang nicht
über den aktuellen Scanner-Befund hinausgeht.

## Geänderte Dateien

- `tests/test_engine_lifecycle_artifacts.py`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Offizielle SonarQube-Cloud-`api/issues/search` für die 33 stabilen Keys | bestanden: genau 33 offene Parent-`python:S3415`-Code-Smells in der ausgewählten Datei. |
| Fokussierte Parent-Baseline `tests.test_engine_lifecycle_artifacts` in einem sauberen aktuellen-Master-Worktree | bestanden: 5 Tests. |
| Kandidat des fokussierten Parent-Testmoduls mit explizitem `.venv`, isoliertem `TMPDIR` und deaktiviertem Bytecode | bestanden: 5 Tests. |
| In-Memory-AST-Inventar aller ausgewählten Source-Zeilen | bestanden: genau 33 ausgewählte `assertEqual`-/`assertNotEqual`-Aufrufe sind Actual-first. |
| `git diff --numstat` auf die Testdatei begrenzt | bestanden: genau 33 Hinzufügungen und 33 Entfernungen, ein Operandentausch pro ausgewähltem Aufruf. |
| `tests.test_bilingual_docs` | bestanden: 11 Tests. |
| Repository-Bilingual-Dokumentations- und Link-Checks | `blocked_environment`: ausschließlich die 20 bereits bestehenden fehlenden Framework-Gitlink-Ziele wurden gemeldet; keine Diagnose nannte einen geänderten Change Record. |
| AST-Syntax-Parse, `git diff --check` und Bytecode-Artefakt-Scan | bestanden: Source wurde geparst, keine Whitespace-Diagnose und kein `*.pyc`-Artefakt im Worktree. |
| Exact-Head-Hosted-Checks | ausstehend: Der bestehende Draft PR #109 muss nach seiner normalen Branch-Aktualisierung sämtliche Evidence erneut ausführen; spätere Ergebnisse müssen diesem exakten Head zugeordnet sein. |

## Security-Auswirkung

Der Test prüft weiterhin payload-freie Lifecycle-Artefakte, Payload-
Eingabeablehnung, Hashing einer verlinkten Library, Subprocess-Returncodes und
Lifecycle-Zählerverhalten. Diese Änderung ändert ausschließlich die
Diagnosereihenfolge einer Fehlermeldung; sie verändert keinen produktiven
Parser, keinen Untrusted-Input-Pfad, keine File-Access-Kontrolle, kein
Subprocess-Argument, keine Executable-Auswahl, keine Konfiguration,
Authentifizierung, Autorisierung, Netzwerkoperation, Artifact-Writer oder
Security-Assertion. Es wird kein Security-Finding als behoben beansprucht.

## Runtime-Evidence

Kein Connector-Runtime-Verhalten wurde geändert oder beansprucht. Das
vollständige Parent-Testmodul nutzt temporäre Fixtures zur Prüfung des
Artifact-Writer-Vertrags; es ist weder ein Host-Deployment noch ein Framework-
oder MRTS-Run.

## Bekannte Einschränkungen

Dieser Batch behandelt nur 33 geprüfte Parent-Testdiagnostik-Befunde. Er
beansprucht weder die Beseitigung des breiteren SonarQube-Cloud-Backlogs noch
die Behebung eines Framework- oder MRTS-Befunds oder den Nachweis von
Connector-Runtime-Verhalten über den vorhandenen fokussierten Testvertrag
hinaus.

## Verbleibende Risiken

Ein versehentlicher Tausch außerhalb einer ausgewählten Assertion könnte eine
Fehlermeldung irreführend machen. Das Live-Key-/Source-Inventar, die exakte
33-Zeilen-AST-Verifikation, der Single-File-Diff-Review und das vollständige
betroffene Testmodul reduzieren dieses Risiko. Hosted-Sonar-Analyse und CI
müssen noch auf dem exakten Draft-PR-Head laufen.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein voller Connector-Build oder Host-/Runtime-Matrix: Es ändert sich nur die
  Test-Diagnostik-Operandreihenfolge, und das vollständige betroffene Parent-
  Testmodul ist die enge Regression-Kontrolle.
- Kein Framework- oder MRTS-Test und keine -Änderung: Beide sind aus diesem
  Parent-only-Task ausgeschlossen.
- Noch keine exakte-Post-Update-Head-GitHub-Actions-, CodeQL-, Sonar-Quality-
  Gate-, PR-Issue-Query- oder Review-Thread-Prüfung; der bestehende Draft PR
  muss nach der normalen Branch-Aktualisierung erneut ausgewertet werden.

## Aktuelle normale Aktualisierung und Delivery-Status

Der bestehende Draft PR #109 wurde ohne Rebase durch den normalen Merge-Commit
`62eae66` aktualisiert, der Parent-`master`
`700e62e5c2287e10f8774757ffff7432753900c0` in seinen Branch übernommen hat.
Nur die beiden gemeinsamen Change-Record-Indizes hatten Konflikte; ihre
Auflösung bewahrt alle aktuellen `master`-Einträge sowie diesen Record.

Unter der aktuellen Parent-only-Autorisierung darf dieser normale Merge den
bereits in der `master`-Historie vorhandenen Framework-Gitlink erben. Der
finale PR-Diff darf und verändert keinen Gitlink. Es gab keinen Framework- oder
MRTS-Checkout, keine Änderung, keinen Test, keine Delivery und keinen Merge.

Die frische Validierung des dokumentationstragenden Post-Update-Heads sowie
anschließend exakte-Head-Hosted-Checks, SonarQube-Cloud-Evidence, Issue- und
Hotspot-Review und PR-Review-/Conversation-Checks stehen noch aus. Dieser
Record beansprucht weder eine Ready-Transition noch einen Merge.

## Finaler Diff- und Review-Status

Der geprüfte lokale Batch entstand bei
`a315a79ab485b1834939c4b9f90b53981151ff67` und wird nun durch den bestehenden
aktualisierten Draft PR #109 dargestellt. Der finale Diff enthält weiterhin
nur das ausgewählte Parent-Testmodul, dieses englische/deutsche Change-Record-
Paar und die beiden Indizes. Seine Delivery-Evidence bleibt unvollständig, bis
der exakte aktualisierte Head die erforderlichen lokalen und Hosted-Kontrollen
bestanden hat. Es werden weder Merge, Default-Branch-Update, Framework-/MRTS-
Änderung, Suppression noch Alert-Closure beansprucht oder autorisiert.
