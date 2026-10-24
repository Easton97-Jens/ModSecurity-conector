# Change Record: CR-20261008-scheduler-lock-reuse-fixture-control

**Sprache:** [English](CR-20261008-scheduler-lock-reuse-fixture-control.md) | Deutsch

Nur Trennung von Fault und positiver Kontrolle im Test; keine Produkt-Runtime-Behauptung.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-scheduler-lock-reuse-fixture-control |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `5e22a9f0cc9b688ddc271012467b053bca8d1bfb` |

## Motivation und Problemstellung

Die Lost-Wrapper-Fixture übernahm ihren absichtlichen Ein-Sekunden-Job-Timeout
in die separate Lock-Reuse-Kontrolle. Exit 77 eines echten Completion-Timeouts
wurde als vermeintlicher Lock-Konflikt wiederholt; verworfene Diagnosen machten
den abschließenden Fehler irreführend. Kein verbleibender produktiver Lock-Defekt
ist damit belegt.

## Akzeptanzkriterien

Ursprünglichen Lost-Wrapper-Timeout und Live-Owner-/Descendant-Lock-Prüfungen
erhalten. Die Reuse-Kontrolle darf Fault-Eingaben nicht verändern und einen
Completion-Timeout nicht wiederholen. Eigenes begrenztes Job-Budget verwenden
und tatsächlich beobachtete Konfliktdiagnosen erhalten.

## Implementierungsentscheidung und Begründung

Fixture-Environment kopieren und die positive Reuse-Kontrolle auf 30 Sekunden
setzen. Exit 77 nur wiederholen, wenn stderr `another full-matrix run owns`
meldet. Den ursprünglichen Ein-Sekunden-Fault unverändert lassen. Drei
deterministische Kontrollen beweisen Eingabeerhalt, Timeout-Ablehnung und
zulässige Wiederholung bei tatsächlichem Lock-Konflikt.

## Geänderte Dateien

Nur `tests/test_full_matrix_parallel_scheduler.py` und dieses EN/DE-Change-
Record-Paar. Keine Änderungen an produktivem Scheduler, Lock, Timeout-Policy,
Connector, Framework, MRTS, Capability, Selection oder Canonical-Validator.

## Ausgeführte Befehle

Alle Befehlspayloads liefen über `rtk proxy` mit externen neutralen Testroots.
`python -m unittest -v` für die zwei neuen Negativkontrollen: 2 Fehler, Exit 1
vor der Helper-Korrektur. Der erste Green-Aufruf mit sechs Namen hatte fünf
bestandene Tests und einen Loader-Fehler wegen eines nicht vorhandenen Namens,
Exit 1; nicht als bestanden gewertet. Korrigierter Aufruf: 6 Tests,
11.709 Sekunden, Exit 0, einschließlich tatsächlichem Lost-Wrapper-Timeout,
Live-Owner-Ablehnung und Descendant-Lock-Lebensdauer.
`make check-bilingual-docs check-doc-links`, archivbezogenes `new-change-record.py
check`, Shell-Syntax/ShellCheck des externen Fokus-Launchers und
`git diff --check`: Exit 0. Begrenzter Diff und unabhängiger Read-only-Review
ergaben kein blockierendes Finding.

## Security-Auswirkung

Kein produktiver Lock oder Security-Check wird gelockert. Ein Nicht-Lock-
Exit 77 lässt den Test jetzt sofort fehlschlagen statt still wiederholt zu
werden. Fault- und positive Kontrolleingaben bleiben getrennt; die tatsächliche
Prüfung des vererbten Locks bleibt erhalten.

## Runtime-Evidence

Echte Scheduler-Subprozesse führten die fokussierten Prozess-/Lock-Kontrollen
aus. Dies sind Testfixtures, keine NGINX-Requests oder Coverage-Evidence. Alle
97 selektierten Required-Finalrecords benötigen weiterhin frische laufgebundene
Evidence; kein Canonical-PASS oder geschützter HostGate-Nachweis wird behauptet.

## Bekannte Einschränkungen

Das alte Gesamtlog unterscheidet tatsächlichen Lock-Konflikt nicht von einem
späteren Job-Timeout der positiven Kontrolle. Der separate Refill-Timing-Fehler
wird hier nicht behoben; der vollständige Parent-Fokus muss erneut laufen.

## Verbleibende Risiken

Ein vollständiger kombinierter Test-/Runtime-Lauf kann unabhängige Fehler
aufdecken. Ursprüngliche 52 Baseline-IDs und 45 Missing-Record-Ziele bleiben
unverändert. PR #396 bleibt Draft; dieser Record belegt weder Veröffentlichung
noch aktuelle CI- oder Sonar-Closure.

## Nicht ausgeführte Prüfungen mit Begründung

Kein frischer vollständiger Parent-Fokus, NGINX-E2E oder geschützter Exact-Head-
Lauf für diesen Teil; sie folgen unabhängigen Fixture-Reparaturen und finalen
Clean-Tuple-Gates. Ruff ist separat nicht verfügbar; keine Tool- oder
Dependency-Installation wird vorgenommen.

## Finaler Diff- und Review-Status

Begrenzter Test-only-Diff geprüft; unabhängiger Read-only-Review ohne blockierende Findings.
Archiv-, Bilingual- und Linkchecks bestanden vor dem separaten Commit.
Kein History-Rewrite, breites Staging, Framework-Pin oder MRTS-Eingriff.
