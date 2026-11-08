# Change Record: CR-20261108-sonar-pr-context

**Sprache:** [English](CR-20261108-sonar-pr-context.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261108-sonar-pr-context |
| Datum (UTC) | 2026-11-08 |
| Basis-Revision | `400c47ebd5a6fe32dc43ec6875968ce7ebae04d0` |

## Motivation und Problemstellung

C++20 und C++23 erzwangen auch bei Pull Requests ausdrücklich den Branch `master`. Ihre roten Master-Gates konnten den geforderten PR-Stand nicht belegen. Jede Variante erhält wieder den tatsächlichen GitHub-Ereigniskontext; alle Quelldateien und unabhängigen Projektschlüssel bleiben erhalten.

## Akzeptanzkriterien

Alle drei konfigurierten Standards müssen eine eigene PR-Analyse am aktuellen Head erzeugen. Fehlende PR-Kontexte bleiben fehlende Nachweise. Der Gesamtauftrag verlangt außerdem null offene/akzeptierte PR-Befunde, null ungeprüfte Hotspots und Gate OK in jedem zugehörigen Projekt sowie die getrennt dokumentierte vollständige Regression des endgültigen Paars.

## Implementierungsentscheidung und Begründung

Die drei Matrixfelder `branch_args` und ihre Scanner-Interpolation entfernen. Automatische GitHub-Ereigniserkennung, exakter Checkout-/SCM-SHA, Projektschlüssel, Standards, vollständiger Umfang, Secrets-Schutz und Gate-Warten bleiben erhalten. Die bestehenden Advisory-Flags bleiben erhalten; sie erfüllen nicht die unabhängige Auftragsanforderung, dass alle drei Gates bestehen. Eine separate Framework-Vertragsänderung verwirft wieder eingeführte Kontextüberschreibungen.

## Geänderte Dateien

- `.github/workflows/sonarqube.yml`
- `docs/sonarqube-analysis.md` und `docs/sonarqube-analysis.de.md`
- Dieses englisch/deutsche Change-Record-Paar.

Die anschließende Übergabe von Framework-Gitlink, Versionslock und registrierten Workflow-Projektionen verwendet den nativen Publisher; Framework-Tests und -Records bleiben in ihrem separaten Repository.

## Ausgeführte Befehle

`rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` endete für jede ausgewählte geänderte Datei mit Exit 0. Der native Vorlagenbefehl `ci/tools/new-change-record.py create --name sonar-pr-context --base-revision 400c47ebd5a6fe32dc43ec6875968ce7ebae04d0 --date 2026-11-08` endete mit ausdrücklichem Parent-/Framework-Kontext mit Exit 0. Sechs gezielte Framework-Sonar-Methoden bestanden am korrigierten Workflow, einschließlich acht tatsächlich wirksamer Kontextüberschreibungen als Negativkontrollen; der Framework-Record enthält den vollständigen Befehl und die Logs.

## Security-Auswirkung

Keine neuen Credentials, Secrets-Verbraucher, Berechtigungen, Trigger oder Source-Ausschlüsse. Das Scanner-Token bleibt auf seine bestehende gepinnte Action begrenzt. Ereignisbasierte PR-Zuordnung stellt die Nachweiszuordnung wieder her; sie verändert weder Neucode-Baseline noch Qualitätsregeln oder Gates.

## Runtime-Evidence

Diese Workflow-/Dokumentationsänderung behauptet kein frisches Host-Runtime-Ergebnis. Die geforderten Host-Ausführungen des endgültigen Paars werden nach dessen Fixierung getrennt dokumentiert.

## Bekannte Einschränkungen

Der ursprüngliche Cloud-Snapshot beschreibt weiterhin Parent `400c47ebd5a6fe32dc43ec6875968ce7ebae04d0` und Framework `d14937ce8fe7a534bb755cffa6597e62eadbb126`. Das Framework hat 29 OPEN-Vorkommen und Gate ERROR; keine serverseitige FP-Transition ist gespeichert. C++20-/C++23-PR-Kontexte müssen nach der Hosted-Analyse geprüft werden. Historische Master-Befunde bleiben getrennt.

## Verbleibende Risiken

Lokaler Vertragserfolg beweist weder Hosted-PR-Zuordnung noch ein bestandenes Gate. Der reguläre SSH-Receiver meldet `allowed_mutations=[]`; einzeln begründete Serverentscheidungen benötigen weiterhin eine vorhandene berechtigte Schreibsitzung. Keine Zugriffsbeschränkung wird umgangen.

## Nicht ausgeführte Prüfungen mit Begründung

Hosted-Analysen am endgültigen Head und die vollständige Regression mit 92 Host-Ausführungen, 237 betroffenen Methoden, 88 Reader-Methoden, Go/vet/native/CRS/CodeQL werden hier nicht behauptet: Sie benötigen das endgültige eingecheckte und veröffentlichte Paar. Die Gesamtabnahmekampagne bleibt `NOT_RUN`; beide PRs bleiben Draft und kein Merge ist erlaubt.

## Finaler Diff- und Review-Status

Der fokussierte Workflow-Diff entfernt ausschließlich die falschen Branch-Zuordnungsargumente. Die Dokumentation beschreibt den daraus entstehenden Kontextvertrag. Abschlussbericht und PR-Beschreibungen müssen tatsächliche Lieferung, Validierung und verbleibende Blocker abgleichen; dieser Record behauptet nicht, dass das SonarCloud-Nullziel erreicht ist.
