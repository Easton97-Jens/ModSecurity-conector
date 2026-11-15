# Change Record: CR-20261108-preparation-publisher-mode

**Sprache:** [English](CR-20261108-preparation-publisher-mode.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261108-preparation-publisher-mode |
| Datum (UTC) | 2026-11-08 |
| Basis-Revision | `6ceeb7a729faa541a5048d7018c2f70e5c72fcea` |

## Motivation und Problemstellung

Der Framework-Publisher ließ bei einem registrierten Begleitpfad den Wechsel vom regulären Modus `100644` zu `100755` zu, obwohl diese Grenze Inhaltsänderungen mit bestehendem Modus vorsieht. Der tatsächliche Lockdatei-Übergang reproduzierte den Defekt; unveränderter regulärer Modus bestand und ein Symlink-Übergang scheiterte.

## Akzeptanzkriterien

Status `M` für registrierte reguläre Begleitpfade nur bei gleichem altem und neuem Modus akzeptieren. Beide Ausführbarkeitswechsel, Symlink-/Typ-/Anlageübergänge, unbekannte und stillgelegte Pfade zurückweisen. Bestehende Gitlink-, Validator-/Publisher-, App-Token-, Berechtigungs- und genaue Staging-Grenzen erhalten. Die unveränderten 100 Standardfälle erhalten.

## Implementierungsentscheidung und Begründung

Die Gleichheit des alten und neuen Modus zum bestehenden AWK-Guard für rohe Git-Diffs in `.github/workflows/update-submodules.yml` ergänzen. Das alte Modusfeld enthält den führenden Doppelpunkt; es wird mit dem um einen Doppelpunkt ergänzten neuen Modus verglichen. Die vorhandenen Prüfungen für reguläre Modi und Status bleiben erhalten. Das Framework besitzt die zugehörigen positiven und negativen Tests; keine Connector-Produktquellen ändern sich.

## Geänderte Dateien

`.github/workflows/update-submodules.yml` und dieses englisch/deutsche Change-Record-Paar. Der getrennt committete Parent-Governance-Updater, Katalog/Vorlagen und Verweiskorrekturen sind Abhängigkeiten und keine zusätzlichen Dateien dieser fokussierten Modusänderung. Framework-Quellen, Tests und Records bleiben im eigenen Repository.

## Ausgeführte Befehle

Der native Befehl `ci/tools/new-change-record.py create --name preparation-publisher-mode --base-revision 6ceeb7a729faa541a5048d7018c2f70e5c72fcea --date 2026-11-08` endete unter dem Parent-Interpreter mit ausdrücklichen `TEST_ROOT`, `FRAMEWORK_ROOT`, `FRAMEWORK_REVISION`, `CONNECTOR_ROOT`, `CONNECTOR_REVISION` und Python-Suchpfaden für Framework-Wurzel/`connector_suite` mit Exit 0. Frühere Aufrufe mit fehlendem Kontext/Import erzeugten keine Vorlage und bleiben als Diagnosen erhalten. `rtk bypass git diff --check` bestand vor dem Quellreview. Die Framework-eigene vollständige Klasse führte alle 48 ursprünglichen Methoden zweimal ohne Failures, Errors oder Skips aus; der strukturierte Lauf verzeichnet 222 Subtest-Ausführungen innerhalb dieser Methoden. Der unabhängige Review führte sechs wesentliche Methoden erfolgreich aus, einschließlich 26 nativer Workflow-Mutationen und acht Sonar-Kontextmutationen. Das sind Ausführungen und keine zusätzlichen Standardfälle. Nachweise: `$EVIDENCE_ROOT/workflow-tests/publisher-mode-repro.json`, `full-class-result.json`, `final-default100-scope.json` und `reviews/workflow-qualified-review.json`.

## Security-Auswirkung

Schließt die Moduswechsel-Lücke für registrierte Begleitpfade. Beide Moduswechselrichtungen und alternative Symlink-/Status-/Pfadübergänge werden weiterhin abgelehnt; zulässige Änderungen mit unverändertem Modus bleiben erlaubt. Bestehende Credentials, Trigger, Schreibrechte, unveränderlich gepinnte Actions, vertrauenswürdige Validierung und Publisher-Trennung bleiben erhalten.

## Runtime-Evidence

Diese Validierung betrifft Workflow-Verträge und lokale Git-Diff-Kontrollen. Es wird kein neues Connector-Host-Runtime-Ergebnis behauptet.

## Bekannte Einschränkungen

Die gesamte Vorbereitung bleibt unvollständig. Der reguläre zentrale Pre-Commit-Handler benötigt weiterhin die vom Betreiber verantwortete Gitlink-Zulassung. Die endgültigen veröffentlichten Parent-/Framework-/MRTS-Pins sind nicht eingefroren. Der separate MRTS-Governance-Draft-PR #7 veröffentlicht `9a855b092645733ea8ff73a512aff7bfe916407e`; seine Framework-Übergabe steht noch aus. Dies ist eine externe Governance-Abhängigkeit und keine durch diesen Record gelieferte MRTS-Produktänderung.

## Verbleibende Risiken

Ein geprüfter, nicht installierter Betreiber-Vorschlag beweist keine erfolgreiche reale Übergabe. Endgültige separate Secrets-Nachweise und native Pin-Prüfung müssen die tatsächlich gestagten Commits binden. FIFO-/JSON-Lücken im Analyseumfang bleiben separate Vorbereitungsblocker. Keine Abschwächung von Hooks, Trust, Gates, Baselines oder Ausschlüssen.

## Nicht ausgeführte Prüfungen mit Begründung

Aktuelle Hosted-CI-/Sonar-Prüfungen des endgültigen Paars und die geforderten 92 Host-Ausführungen, 195 Go-Szenarien/vet, Reader-/Registry- und vollständige Konsistenzwiederholung benötigen eine regulär eingecheckte, veröffentlichte und eingefrorene Kette. Sie werden hier nicht behauptet. `READY_FOR_FULL_ACCEPTANCE=false`; die umfassende Gesamtabnahmekampagne bleibt `NOT_RUN`. Kein Merge oder direkter Master-Push ist autorisiert.

## Finaler Diff- und Review-Status

Der fokussierte Guard wurde gegen den reproduzierten Defekt geprüft und unabhängig anhand der tatsächlich aktuellen Workflow-Verträge kontrolliert. Dieses Paar folgt den nativen Vorlagenüberschriften. Secrets-Prüfung der geänderten Dateien, bilinguale/Archivprüfungen und der reguläre Commit werden nach tatsächlichem Abschluss getrennt dokumentiert; keine Freigabe des endgültigen veröffentlichten Paars wird behauptet.
