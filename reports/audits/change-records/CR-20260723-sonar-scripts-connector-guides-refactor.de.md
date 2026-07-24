# Change Record: Parent-Connector-Guide-Renderer-Zerlegung für SonarQube Cloud S3776 und S1481

**Sprache:** [English](CR-20260723-sonar-scripts-connector-guides-refactor.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-scripts-connector-guides-refactor |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Parent-`python:S3776` `AZ9cRzBCHhV2CayPTP5L`, `python:S1481` `AZ9cRzBCHhV2CayPTP5K` sowie die zwei PR-erzeugten `python:S1172`-Zeilen `AZ-Qn4qN18-5KNpatmRP`, `AZ-Qn4qO18-5KNpatmRQ` in `scripts/generate_connector_guides.py`. |
| Grenze | Parent-Generator/-Test sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und eingecheckter Connector-Dokumentationsinhalt bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet für `content()` kognitive Komplexität 38 bei erlaubten
15 sowie die unbenutzte lokale Variable `suffix`. Die Funktion kombiniert
gemeinsames Setup, acht Dokumenttyp-Renderer, bilinguale Behandlung und die
abschließende Structural-Parity-Umwandlung, wodurch künftige Edits schwer zu
reviewen sind.

## Entscheidung

`content()` als öffentliche Rendering-Schnittstelle bewahren, aber an kleine
Dokumenttyp-Helper delegieren. Das gemeinsame Title-/Scope-Setup und die
deutsche Label-Umwandlung in benannte Helper und Konstanten verschieben. Die
unbenutzte lokale Variable entfernen. Einen fokussierten Regressionstest
hinzufügen, der beweist, dass alle sechs Connectoren × acht Dokumenttypen ×
zwei Sprachen den aktuellen deterministischen Aggregate-SHA-256 bewahren und
dass `main()` exakt dieselben 96 Dateien in einen kontrollierten temporären
Root schreibt.
Diese Regression in den bestehenden `lint`-Vertrag einbinden. Nachdem die
erste Exact-Draft-PR-Analyse zwei durch die Zerlegung eingeführte unbenutzte
private-Helper-Parameter meldete, nur diese Parameter und die passenden
Dispatch-Argumente entfernen.

## Scope und Non-Goals

Die Source-Änderung reorganisiert nur `scripts/generate_connector_guides.py`
und fügt `tests/test_connector_guides.py` hinzu. Sie ändert keinen gerenderten
String, kein Path-Layout, keinen Dokumenttyp, keine Sprachpaarung, kein File-
Encoding, keinen Connector-Input, keine eingecheckte Dokumentation, keinen
Subprocess, keine Netzwerkaktion, keine Security-Control, keine Sonar-Regel/
kein Profil, kein Quality Gate, kein Framework, kein MRTS und keinen Gitlink.

Der Change Record und sein englisches Gegenstück sind die einzigen
versionierten Dokumentationsänderungen. Die gemeinsamen Indizes werden zur
Traceability aktualisiert. Kein Merge und kein Default-Branch-Write sind Teil
dieses Changes.

`Makefile` erhält nur den benannten Test-Target und seinen `lint`-Aufruf. Der
Task-Branch enthält außerdem einen normalen Synchronisations-Merge des
aktuellen `master`; die gepaarten bilingualen Change-Record-Indizes wurden
automatisch gemergt. Dieser Merge ändert weder `master` noch schreibt er
veröffentlichte Historie um.

## Output-Kompatibilität und Testgrenze

Der Pre-Edit- und Post-Edit-Aggregate-Digest ist
`b98dae8bd83ebb0ee3f6694269b29d0ee1f97a26ec7aba8aaa054eac749d4728` für
exakt 96 Renders. Der permanente Test berechnet denselben Keyed Digest und
patcht außerdem den Generator-Root nur innerhalb von `TemporaryDirectory`; er
vergleicht jede generierte Datei bytegenau mit `content()`-Output und erwartet
exakt 96 Markdown-Dateien. Er ruft `main()` nie gegen den Checkout auf.

## Sicherheit und Kompatibilität

Dies ist kontrolliertes Dokumentations-Rendering-Refactoring. Es führt weder
untrusted Input noch benutzergewählte Pfade, Subprocesses, Credentials,
Netzwerkzugriff, Berechtigungen, Memory Safety oder Host-Runtime-Enforcement
ein bzw. ändert sie nicht. Der temporäre Output-Root bleibt test-eigen und wird
durch den Standard-Temporary-Directory-Kontext entfernt. Dieser Delta löst
keinen Security-Workflow aus.

## Validierung und Delivery-Status

Der fokussierte Renderer-Test, `make check-connector-guides`, In-Memory-
Syntax-Compile, Output-Digest-Vergleich, AST-Dispatch-Inspektion und Diff-
Check bestanden lokal. Gezielte bilinguale Dokumentationstests bestanden. Die
vollständigen Dokumentations-/Link-Kommandos sind nur durch vorbestehende
fehlende Framework-Gitlink-Targets blockiert und meldeten keinen task-eigenen
Change-Record-Fehler. Die erste Exact-Head-Draft-PR-Analyse bestand ihr Quality
Gate und entfernte die ursprünglichen zwei Zeilen, meldete aber zwei
task-eingeführte unbenutzte private-Helper-Parameter. Ihr fokussierter
Follow-up ist lokal validiert; frische Exact-Head-Hosted- und SonarCloud-
Ergebnisse stehen aus.

### Aktuelle Parent-master-Aktualisierung — 2026-07-24

Der bestehende Draft PR #106 bleibt das Delivery-Vehikel. Sein vorheriger
Remote-Head `619e27f8890fcdb1a47dea21ff804e66743ce154` wurde ohne Rebase durch
das Mergen von Parent-master
`26f0eb9cff2f1c69ba7be9cfc5fd609659e3041f` normal aktualisiert. Der
resultierende lokale Merge-Commit
`20ad9b6a9341f13f553e28edb2eb471d170c7fd8` übernahm die gemeinsamen Change-
Record-Indizes automatisch. Er ändert weder Framework noch MRTS, sondern
übernimmt lediglich bestehende Master-Historie. Der aktuelle PR-Base-Diff
bleibt beim Parent-Generator, seinem Parent-Test, dem benannten Make-Target,
diesem englisch/deutschen Change-Record-Paar und den Indizes, ohne von diesem
PR-Update verfasste Framework-, MRTS-, Gitlink-, eingecheckte-Guide-, Scanner-,
Gate-, Suppression- oder Security-Control-Änderung.

Der aktuelle Renderer-Test im gemergten Baum und der benannte Make-Target
bestanden jeweils zwei Tests; die unabhängige AST-Prüfung bestätigte alle acht
Renderer-Arten, einen branch-freien öffentlichen `content()`-Dispatcher und
keine `suffix`-Zuweisung. Hosted-Check-, SonarQube-Cloud-, Quality-Gate-,
Review-, Ready- und Merge-Ergebnisse werden nur durch beobachtete Exact-Head-
PR-Delivery-Metadaten beansprucht.

## Akzeptanzkriterien

- Die unbenutzte lokale Variable `suffix`, die zwei task-eingeführten
  unbenutzten private-Helper-Parameter entfernen und die markierte
  `content()`-Ladder ohne Suppression oder Scanner-Konfigurationsänderung
  zerlegen.
- Alle 96 Keyed Rendered Outputs exakt bewahren und exakt diese Dateien nur in
  einem kontrollierten temporären Test-Root schreiben.
- Diese Output-Regression über den benannten Repository-`lint`-Target
  ausführen.
- Beide Change-Record-Sprachen und beide Indizes gleichwertig halten.
- Exact-Draft-PR-Head-SonarQube-Cloud- und Hosted-Check-Evidence einholen,
  bevor einer der ausgewählten Keys als behoben gilt.

## Implementierungsentscheidung und Begründung

Die öffentliche `content()`-Schnittstelle berechnet jetzt ihren Partnernamen
und delegiert an einen kleinen Renderer-Dispatch. Jeder Dokumenttyp hat einen
fokussierten Helper mit nur den von ihm verwendeten Inputs; die zwei zunächst
redundanten Helper-Inputs wurden nach der ersten PR-Analyse entfernt.
`_finish_content()` bewahrt die vorhandene deutsche Structural-Parity-
Umwandlung. Ein globales Dokumenttyp-Tuple wird von Dispatch, Writer und Test
geteilt, damit der 96-Output-Vertrag explizit bleibt.

## Geänderte Dateien

- scripts/generate_connector_guides.py
- tests/test_connector_guides.py
- Makefile
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Fokussierter `tests.test_connector_guides`: bestanden (2 Tests).
- `make check-connector-guides`: bestanden (2 Tests) und wird von `lint`
  aufgerufen.
- In-Memory-Syntax-Compile: bestanden (2 Python-Dateien).
- Renderer-Output-Parität: bestanden (96 Renders, aufgezeichneter SHA-256).
- AST-Dispatch-Inspektion: bestanden; `content()` hat keinen Branch-Node, alle
  acht Renderer-Helper existieren und keine `suffix`-Zuweisung verbleibt.
- `tests.test_bilingual_docs`: bestanden (11 Tests; 13 kombinierte fokussierte
  Tests).
- `git diff --check`: bestanden.
- Vollständige Dokumentations-/Link-Checks: nur durch bekannte fehlende
  Framework-Gitlink-Targets blockiert; kein task-eigener Change-Record-Fehler
  wurde gemeldet.
- Erste Draft-PR-SonarQube-Cloud-Analyse: Quality Gate `OK`; die ursprünglichen
  zwei Zeilen fehlen, sie meldete aber zwei task-eingeführte `python:S1172`-
  Zeilen.
- Frische vollständige Draft-PR-Hosted-/SonarQube-Cloud-Analyse: für den
  fokussierten S1172-Follow-up-Head ausstehend.

## Security-Auswirkung

Keine Security-Verhaltensänderung. Der temporäre Output-Test begrenzt Writes
auf eine test-eigene `TemporaryDirectory`; der Generator wird während der
Validierung nicht gegen den Checkout ausgeführt. Es wird kein Security-Finding
als behoben beansprucht.

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und es wird keines
beansprucht. Dies ist ein Offline-Dokumentationsgenerator- und Unit-Test-
Change, kein Host-/Runtime-Deployment und kein Framework-/MRTS-Lauf.

## Bekannte Einschränkungen

Dieser Batch behandelt die zwei ausgewählten SonarQube-Cloud-Observations und
die zwei direkt task-eingeführten S1172-Observations. Er beansprucht weder,
den breiteren SonarCloud-Backlog zu
leeren, noch Connector-Builds, Host-Konfigurationen oder Production-
Dokumentationsdeployment zu validieren.

## Verbleibende Risiken

Ein zukünftiger Renderer-Edit könnte generierten Text oder Output-Layout
unbeabsichtigt ändern. Der Keyed-96-Render-Digest und der Byte-Vergleich des
temporären Baums reduzieren dieses Risiko; frische Hosted-Exact-Head-Analyse
bleibt vor verifizierter Delivery erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Connector-Build und keine Runtime-Matrix: Der Delta ist reines
  kontrolliertes Dokumentations-Rendering und sein vollständiger fokussierter
  Unit-Test besteht.
- Kein Framework- oder MRTS-Test und keine -Änderung: beide sind aus diesem
  Parent-only-Task ausgeschlossen.
- Kein aktueller vollständiger Dokumentations-/Link-Sweep: er kann Framework-
  Gitlink-Targets außerhalb dieses Parent-only-Tasks ausführen; gezielte
  bilinguale Dokumentationsvalidierung ist die passende lokale Kontrolle.
- Frische vollständige Hosted-Checks und SonarQube-Cloud-PR-Analyse: ein Draft
  PR existiert, aber sein S1172-Follow-up-Head benötigt noch eine neue
  Exact-Head-Analyse.

## Finaler Diff- und Review-Status

Der bestehende Parent-only-PR #106 ist das Delivery-Vehikel. Sein task-eigener
Branch enthält den normalen Current-Master-Update-Merge
`20ad9b6a9341f13f553e28edb2eb471d170c7fd8` sowie gepaarte Delivery-Evidence-
Dokumentation. Dieser Record beansprucht weder Review-Freigabe noch Merge oder
Default-Branch-Änderung. Vor einem geschützten Merge muss der PR nicht mehr
Draft sein und sein aktueller Exact-Remote-Head muss bestehende Hosted-Checks
und SonarQube-Cloud-Analyse sowie einen aktualisierten Review-Status aufweisen;
diese beobachteten Fakten gehören zu Delivery-Metadaten und nicht zu einer
unbeobachteten Behauptung in diesem Record.
