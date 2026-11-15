# Change Record: CR-20261115-decouple-updater-mrts

**Sprache:** [English](CR-20261115-decouple-updater-mrts.md) | Deutsch

Vom Nutzer angeforderte Änderung der Connector-Updater-Verantwortung; der Prüfstatus steht unten.

**Prüfsnapshot vor der Veröffentlichung.** Dieser Record erfasst die lokalen Prüfungen vor der Auslieferung über Aufgabenbranch und Draft Pull Request. Exakter ausgelieferter Head und aktuelle CI-Ergebnisse sind im daraus entstehenden Pull Request zu verfolgen. Eine Integration in `master` liegt außerhalb der Autorisierung dieser Aufgabe.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261115-decouple-updater-mrts |
| Datum (UTC) | 2026-11-15 |
| Basis-Revision | `3b47c48e58caad35dc66f7e5b6786f81ed7fed9b` |

## Motivation und Problemstellung

Der Lauf Update submodules `43708408697` lehnte einen Framework-Nachfolgecommit ab, weil dessen MRTS-Gitlink rückwärtsging. Der Nutzer verlangte, dass der Connector-Updater keine eigenständige MRTS-Auswahlentscheidung mehr trifft.

## Akzeptanzkriterien

Einen exakten Framework-Nachfolgekandidaten unabhängig von der Abstammung seines verschachtelten MRTS-Pins akzeptieren. `mrts_sha` im Lock aus diesem Kandidaten ableiten, ohne MRTS herunterzuladen. Framework-Abstammung, exakte Identitäten, verschachtelte Topologie-/URL-Prüfungen, isolierte Validierung und eingeschränkte Veröffentlichung erhalten.

## Implementierungsentscheidung und Begründung

MRTS-Remote-Fetch und Abstammungsvergleich des Updaters entfernen. In Validierer und Publisher den verschachtelten Pin mit dem vorhandenen Gitlink-Leser aus dem exakten Framework-Objekt lesen. Diesen abgeleiteten Wert an alle drei Vertragsprüfer-Aufrufe mit `--expected-candidate-mrts-sha` und alle fünf Synchronisierungs-/Primärprüfungsaufrufe mit `--mrts-sha` übergeben. So bleibt das Revisions-Lock-Paar ohne eigene MRTS-Releaseentscheidung konsistent. Die Standardregeln anderer Aufrufer und das Lock-Schema bleiben unverändert.

Vier Sandbox-Aufrufe verwiesen noch auf Parent-Skriptpfade, die bei der Migration der Testverantwortung entfernt wurden. Vorbereitung, Verifikation und Bereinigung werden über die vorhandene authentifizierte Brücke `ci/run-trusted-framework.py` mit `--tool readonly-prepare` geführt, die Namespace-Ausführung mit `--tool readonly-namespace`. `--connector-revision` wird an `EXPECTED_PARENT_HEAD` gebunden, Leser-UID/-GID und vertrauenswürdiges Framework-Objekt werden übergeben; der ausschließlich die Standardbibliothek verwendende Helfer wird auch bei ausgechecktem Kandidaten aus dem alten gepinnten Framework-Objekt geladen. Sandbox-Isolation und Ausgabeverträge bleiben unverändert. Das unabhängige Review der Helfer und ihrer Standardbibliotheksabhängigkeiten meldete keine Befunde.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`: Framework-eigene verschachtelte Auswahl, vollständige Weitergabe des Lock-Werts und authentifizierte Führung aller vier Sandbox-Helferaufrufe.
- `ci/README.md`, `ci/README.de.md`: gleichwertige Dokumentation von Verantwortung und Validierung.
- `reports/audits/change-records/CR-20261115-decouple-updater-mrts.md`, `reports/audits/change-records/CR-20261115-decouple-updater-mrts.de.md`: dieses Record-Paar.

## Ausgeführte Befehle

Der Nutzer erlaubte ausdrücklich die Windows-Ausführung ohne den fehlenden RTK-Wrapper und Linux-Startskill. Der native POSIX-Scaffolder lief im vorhandenen WSL Ubuntu mit explizitem Connector-/Framework-Kontext: `python3 -B ci/tools/new-change-record.py create --name decouple-updater-mrts --date 2026-11-15 --base-revision 3b47c48e58caad35dc66f7e5b6786f81ed7fed9b` (Exit 0; beide Vorlagen erstellt).

- Explizite `sonar analyze secrets`-Prüfungen bestanden für die ausgewählten Quell- und Prüfeingaben; rohe Scannerausgabe wurde unterdrückt. Für finale geänderte Bytes bleibt bei der Auslieferung die Pflicht zu Secrets-Prüfungen vor dem Lesen bestehen.
- Das vorhandene WSL Ubuntu führte das Secrets-geprüfte externe Aufgabenartefakt `verify_updater.py` mit `python3 -B` aus (Exit 0). Es parste das vollständige YAML, prüfte alle 26 `run`-Schritte mit `bash -n` und verifizierte die Argumentweitergabe an genau drei Vertragsprüfer- und fünf Synchronisierungsaufrufe.
- Seine Offline-Git-Fixtures bestanden gleiche, vorwärtsgerichtete, rückwärtsgerichtete und divergente MRTS-Auswahlen bei absichtlich unerreichbarem MRTS-Repository: Workflow-Checkout, beide Ableitungsblöcke, Struktur-/Zustandsvalidierung, Vertragsprüfung vor/nach der Synchronisierung und korrekte idempotente Lock-Projektion bestanden. Der Ausgangsworkflow reproduzierte die exakte MRTS-Rollback-Ablehnung. Ungültige Pins, ein inkonsistenter alter Lock und Framework-Commits ohne Nachfolgebeziehung wurden abgewiesen.
- Ein unabhängiges Workflow-Review meldete keine Befunde. `git diff --check` bestand (Exit 0) vor dieser Record-Aktualisierung.
- Der erste native Testlauf auf dem Windows-Mount traf auf einen Dateirechtefehler und wurde gestoppt. Der Ersatzlauf verwendete nativen Linux-Aufgabenspeicher unter `/var/tmp/codex/ModSecurity-conector/updater-20261115`: Alle drei vorhandenen Local-Git- und 15 Zustandsvalidierungstests bestanden (18 Tests, 110.948 Sekunden, Exit 0).
- Das externe Aufgabenartefakt `verify_updater_docs.py` bestand (Exit 0): native EN/DE-Sprachwechsel und Struktur, Change-Record-Schema/-Identität und sämtliche lokalen Links in allen vier geänderten Dokumentationsdateien.
- Nach der Änderung der Helferführung bestand `verify_updater.py --static` (Exit 0): vollständiges YAML, alle 26 Bash-Schritte, drei Vertragsprüfer-/fünf Synchronisierungsargumentpfade, vier vollständige authentifizierte Objektbrückenaufrufe und Existenz jedes direkt aufgerufenen Parent-Python-Pfads.
- Tatsächliche `--help`-Smoke-Aufrufe von `readonly-prepare` und `readonly-namespace` über `ci/run-trusted-framework.py` bestanden jeweils (Exit 0), mit exakter Parent-Revision, Leser-UID/-GID `1000`/`1000` und `--trusted-framework-object`. Sie belegen authentifiziertes Laden der Helfer und Argumentparsing, nicht die vollständige Namespace-Ausführung.
- Das unabhängige Helfer-/Standardbibliotheksreview meldete keine Befunde. `verify_updater_docs.py` bestand nach der Routingänderung erneut (Exit 0).

## Security-Auswirkung

Die MRTS-Releaseauswahl gehört zum Framework. Parent behält exakte Framework-Identität und Vorwärtsabstammung, Allowlists für verschachtelte Metadaten, Integrität des alten Lock-Paars, Read-only-Validierungsisolation und Veröffentlichungsbeschränkungen bei. Die Sandbox-Helferbrücke authentifiziert Parent-Ausgangsrevision und gepinntes Framework-Objekt vor dem Laden von Code; vom Kandidaten ausgewähltes Python wird nicht vertraut. Weder MRTS-Quellen noch das MRTS-Repository werden geändert. CI-Berechtigungen, Branchschutz, Scannerkonfiguration und Cloud-Gates bleiben unverändert.

## Runtime-Evidence

Für diese lokalen Änderungen wurde weder ein gehosteter Workflow erneut ausgeführt noch eine Connector-Runtime qualifiziert.

## Bekannte Einschränkungen

Dieser Prüfsnapshot vor der Veröffentlichung behauptet weder einen ausgelieferten Commit noch eine Pull-Request-Identität oder ein gehostetes CI-Ergebnis für den aktuellen Head. Die Auslieferung über Aufgabenbranch und Draft Pull Request wird separat verfolgt; eine Merge-Autorisierung wird nicht erteilt. Der historische fehlgeschlagene Lauf bleibt unverändert. Die getrennte Framework-/MRTS-Verantwortung und Repository-Struktur bleiben bestehen.

## Verbleibende Risiken

Der Updater akzeptiert jetzt Framework-eigene MRTS-Pinänderungen einschließlich rückwärtsgerichteter oder divergenter Auswahl ohne unabhängige Parent-Releasefreigabe. Framework-Maintainer verantworten diese Auswahl; Parent weist weiterhin fehlerhafte oder inkonsistente Projektionsdaten und unzulässige verschachtelte Topologieänderungen zurück.

## Nicht ausgeführte Prüfungen mit Begründung

Gehostete CI, Cloud-Analyse, Produktbuilds, vollständige Namespace-Ausführung und Runtime-Matrizen liefen für diesen Prüfsnapshot vor der Veröffentlichung nicht; diese Aufgabe ändert die Updater-Verantwortung statt des Connector-Runtimeverhaltens. Abgeschlossene lokale Helferführungsprüfungen und Smoke-Tests belegen ausschließlich die oben genannten Evidence-Schichten.

## Finaler Diff- und Review-Status

Unabhängige Workflow- und Helferreviews meldeten keine Befunde. Offline-Verhaltens-/Syntaxprüfungen, alle 18 ausgewählten nativen Tests, fokussierte Dokumentationsprüfungen, finale statische Brückenführungsprüfungen und beide authentifizierten Helferlade-Smoke-Tests bestanden. Dies ist der Prüfsnapshot vor der Veröffentlichung; exakter ausgelieferter Head und aktuelle CI sind aus dem daraus entstehenden Draft Pull Request zu ermitteln. Eine `master`-Integration liegt außerhalb des autorisierten Umfangs.
