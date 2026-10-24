# Change Record: eindeutige Assertions für die drei Sonar-Befunde in PR 393

**Sprache:** [English](CR-20260929-sonar-test-assertions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260929-sonar-test-assertions |
| Datum (UTC) | 2026-09-29 |
| Basis-Revision | `e8dfd50cb604c575dbf6d36b41eef91fee968c88` |

## Motivation und Problemstellung

Der Benutzer hat die Behebung der drei Sonar-Befunde in PR #393 angefordert.
Die vollständige öffentliche Antwort enthielt drei offene MAJOR-Befunde:
`AaDuoPI6WRbu3JJPyreg` und `AaDuclXM-TCTlyo6I0zq` (`python:S9073`)
sowie `AaDuclXM-TCTlyo6I0zr` (`python:S5778`).
Sie betreffen die beiden Modul-Loader-Assertions und den Ausnahme-Test für
ein fehlendes Quellfeld, nicht den Produktcode.

## Akzeptanzkriterien

Alle drei Befunde ohne Unterdrückung beheben, die geprüften Verträge erhalten,
betroffene Tests ausführen und frische Sonar-Ergebnisse am nachfolgenden PR-Head prüfen.

## Implementierungsentscheidung und Begründung

Jede Verknüpfung von `SPEC` und Loader in zwei geordnete Assertions aufteilen.
Die sichere Kurzschlussreihenfolge bleibt erhalten; die verletzte Vorbedingung
ist eindeutig. Das Fixture mit fehlendem Feld vor `assertRaisesRegex`
vorbereiten, sodass nur `structure_digest(previous)` im Ausnahmebereich steht.
Die erwartete Klasse `RepairError` und der Meldungstest `Incomplete` bleiben erhalten.

## Geänderte Dateien

`tests/test_change_record.py` und
`tests/test_prepare_reviewed_framework_handoff.py` sowie dieser EN/DE-Record.
Den in Commit `eff6c291de6aa6cb494c12606e3d9c8c83cfca1f` nur zum Abruf
öffentlicher Befunddetails ergänzten temporären Workflow entfernen;
er ist im finalen PR-Diff nicht enthalten.

## Ausgeführte Befehle

In-Process-Prüfung des geänderten Handoff-Testmoduls mit Python 3.13.5:
19 Tests bestanden. AST-Parsing, Leerzeichen- und Abschlusszeilenprüfung bestanden.
Der Loader-Guard wurde mit fehlendem Spec, fehlendem Loader und gültigem
Loader geprüft: Ablehnung/Ablehnung/Erfolg bleiben unverändert. Der ausgewählte
Ausnahmebereich enthält nach der Änderung einen Aufruf statt zuvor zwei.

Die ursprünglichen Test-/Quelldateien wurden vor der Änderung anhand ihrer
GitHub-Git-Blob-Hashes abgeglichen. Weder lokale projektnative Ausführung noch
lokale Sonar-Ausführung werden behauptet. Die gehostete Prüfung verwendet den
bestehenden frühen CI-Schritt und
`python3 -m unittest -v tests.test_change_record tests.test_prepare_reviewed_framework_handoff`.
Das tatsächliche Ergebnis und die frische Sonar-Verifikation gehören zu den
PR-Checks/-Kommentaren des Folgecommits, nicht als Vorhersage in diesen Record.

## Security-Auswirkung

Keine Änderung an Produktcode, Freigabehash, Abhängigkeitspin, Submodul,
Prüfer, Workflow-Berechtigung, Sonar-Regel, Ausschluss, Unterdrückung oder
Quality Gate. Die temporäre Diagnose verwendete weder Token, Secret, Checkout
noch Schreibzugriff auf das Repository.

## Runtime-Evidence

Für diese Testkorrektur weder erforderlich noch behauptet. Die ursprüngliche
Framework-Handoff-Reparatur bleibt unangewendet und ist nicht Teil der Behebung
dieser drei Befunde.

## Bekannte Einschränkungen

Lokale GitHub-DNS-Auflösung und lokale RTK-/Sonar-Werkzeuge waren nicht verfügbar.
[Diagnoselauf 36628373759 / Job 109611057786](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36628373759/job/109611057786)
lieferte alle drei öffentlichen Befunde und scheiterte danach mit HTTP 400
bei einer separaten Regelbeschreibungsanfrage. Er wird nicht als vollständig
erfolgreicher Job ausgegeben.

## Verbleibende Risiken

Erfolgreiche Unit-Tests allein belegen keine saubere Sonar-Analyse.
Ein grüner Vorbereitungs-PR belegt nicht die Behebung des ursprünglichen Updaters.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Connector-Build und keine Laufzeitmatrix: Diese Teständerungen
betreffen beides nicht. Kein lokaler Sonar-Scan oder vollständiger lokaler
Checkout-Test, da Werkzeuge/Netzwerkzugriff nicht verfügbar waren.
Frische gehostete Ergebnisse müssen zum finalen PR-Head gehören,
nicht zu einem früheren Commit.

## Finaler Diff- und Review-Status

Die Quellkorrektur ist auf die drei identifizierten Teststellen begrenzt.
PR #393 bleibt wegen der separaten unangewendeten Framework-Reparatur ein Draft.
Weder Merge noch direkter Master-Push oder Umschreiben der Historie sind autorisiert.
