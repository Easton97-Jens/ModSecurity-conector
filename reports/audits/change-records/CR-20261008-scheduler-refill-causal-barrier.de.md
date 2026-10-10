# Change Record: CR-20261008-scheduler-refill-causal-barrier

**Sprache:** [English](CR-20261008-scheduler-refill-causal-barrier.md) | Deutsch

Nur kausale Fixture-Synchronisierung; keine produktive Scheduleränderung.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-scheduler-refill-causal-barrier |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `d76cb01c84350dbaeb380929bcc80a9c7719789e` |

## Motivation und Problemstellung

Der Refill-Test verglich Fake-Make-Timestamps über ein Sleep-Fenster von
0.8/0.05 Sekunden. Echte Metadatenarbeit und Subprozessstarts konnten dieses
Fenster ohne belegte Scheduler-Verletzung aufbrauchen. Ein fester Sleep
belegt keine kausale Überlappung.

## Akzeptanzkriterien

Die erste Apache-Fixture darf erst erfolgreich enden, nachdem der wartende
Apache tatsächlich gestartet ist, während der frühere NGINX-Job einen Slot
freigibt. Cap 2, vier Starts/Ends, ursprüngliche Timestamp-Relation, maximale
Aktivität 2, finale Aktivität 0 und vier Manifeste erhalten. Fehlender Queued-
Start muss innerhalb eines begrenzten Intervalls fehlschlagen.

## Implementierungsentscheidung und Begründung

Markerbasierte Synchronisierung nur in der Fake-Make-Fixture verwenden. Der
erste Apache veröffentlicht seinen Start und wartet auf den wartenden Apache;
der erste NGINX wartet vor seinem Abschluss auf diesen ersten Start. Der
wartende Apache veröffentlicht seinen tatsächlichen Start nach dem Activity-
Event. Kein produktiver Scheduler wird verändert. Die positive Fixture hat
eine 15-Sekunden-Barriere und eine äußere Grenze von 60 Sekunden. Eine separate
0.1-Sekunden-Negativkontrolle beweist Exit 97 bei fehlendem Queued-Start und
stellt Fixture-Aktivität auf null zurück, statt Batch-Verhalten still zu akzeptieren.

## Geänderte Dateien

`tests/test_full_matrix_parallel_scheduler.py` und dieses EN/DE-Record-Paar.
Locks, Scheduler-Implementierung, produktive Timeout-/Cap-Policy, Required-
Selection, Connector-Source, Framework, MRTS und Validatoren bleiben unverändert.

## Ausgeführte Befehle

Alle Payloads liefen über `rtk proxy` mit externen neutralen Testroots.
`python -m unittest -v` für den Marker-verlangenden Refill-Test vor Fixture-
Unterstützung: 1 Fehler, 4.898 Sekunden, Exit 1. Danach: 1 Test, 5.433 Sekunden,
Exit 0. Vollständiges `tests.test_full_matrix_parallel_scheduler`: 16 Tests,
29.728 Sekunden, Exit 0, einschließlich Lost-Job-/Lock-Prüfungen und Barrieren-
Fehlfall. `make check-bilingual-docs check-doc-links`, archivbezogenes
`new-change-record.py check` und `git diff --check`: Exit 0.

## Security-Auswirkung

Keine produktive Isolation, Lock-, Guardrail- oder Concurrency-Prüfung wird
gelockert. Die Fake-Fixture stärkt die kausale Aussage und prüft begrenztes
Fehler-Cleanup. Kein Service, Netzwerk, Toolchain oder globale Konfiguration.

## Runtime-Evidence

Echte Scheduler-Subprozesse mit kontrollierten Fake-Smoke-Jobs belegen diese
Testschicht. Sie sind keine NGINX-HTTP-, Native-Fault-, Canonical- oder geschützte
Evidence. Alle 97 selektierten Required-Finalrecords benötigen frische
laufgebundene Nachweise.

## Bekannte Einschränkungen

Marker-Synchronisierung bleibt absichtlich Fixture-only. Der ursprüngliche
Gesamtfehler belegte unzuverlässiges Timing, keinen produktiven Scheduling-
Defekt. Vollständige Parent-Validierung und NGINX-Ausführung folgen weiterhin.
Die negative Fixture-Kontrolle ist kein Lauf eines absichtlich defekten
produktiven Batch-Scheduler-Mutanten.

## Verbleibende Risiken

Unabhängige integrierte Runtime- oder CI-Fehler können verbleiben. Ursprüngliche
52 Baseline-IDs und 45 Missing-Record-Ziele bleiben erhalten. Vorhandene echte
Artefakte behalten ihre ursprünglichen Build-Identitäten; keine Source- oder
Release-Umetikettierung erfolgt.

## Nicht ausgeführte Prüfungen mit Begründung

Frischer vollständiger Parent-Fokus, nativer NGINX-E2E, aktuelle Remote-CI/Sonar
und geschützter Exact-Head-Lauf werden durch diese Tests nicht zertifiziert.
Sie benötigen eigene Clean-Tuple- und Artefakt-Gates. Ruff bleibt separat
nicht verfügbar.

## Finaler Diff- und Review-Status

Nur Testfixture und Record-Paar gehören zu diesem separaten Teil.
Unabhängiger Read-only-Review fand keine Regression; Dokumentations-/Archiv-/
Diff-Gates bestanden vor Commit. PR #396 bleibt Draft; kein Merge, Force-Push
oder History-Rewrite.
