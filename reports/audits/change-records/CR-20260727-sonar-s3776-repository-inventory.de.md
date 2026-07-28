# Change Record: Parent-Repository-Inventar-Komplexitätsbehebung für SonarQube Cloud S3776

**Sprache:** [English](CR-20260727-sonar-s3776-repository-inventory.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-s3776-repository-inventory |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-Receipt-Keys `python:S3776` `AZ9cRzA4HhV2CayPTP5A` (`category`) und `AZ9cRzA4HhV2CayPTP5B` (`proposed_destination`). |
| Grenze | Parent-Inventar-Generator, sein direkter Parent-Test und dieses englisch/deutsche Change-Record-Paar. Produkt-Connectoren, Workflows, generierter Inventar-Output, Framework-Quellcode, MRTS-Quellcode, Gitlinks, SonarQube-Cloud-Konfiguration, Suppressions, externer Issue-Status und Master-Integration bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Inventur meldet zwei Befunde zur kognitiven
Komplexität in `scripts/generate_repository_organization_inventory.py`. Die
vorherigen Helfer kodierten Kategorie- und Zielpfadpriorität in langen
Conditional-Ketten, wodurch exaktes Routing und Fallback-Verhalten schwer zu
prüfen waren.

## Akzeptanzkriterien

- Beide Receipt-verbundenen öffentlichen Helfer bleiben verfügbar und sind
  strukturell einfacher.
- Kategoriepriorität, Zielpfadstrings, Inventarzeilenschema, Sortierung,
  Fallback-Verhalten, CLI-Verhalten und Datei-Schreibverhalten bleiben
  unverändert.
- Tabellengetriebene Tests decken Parent- und Framework-Zielpfade sowie
  Fallbacks ab, ohne das Framework zu verändern.
- Der JSON-Output des Generators über denselben aktuellen Korpus stimmt nach
  Normalisierung allein von `generated_at_utc` überein; beide erzeugten
  Markdown-Pläne sind byteidentisch.
- Außerhalb des abgegrenzten Parent-Generators/Tests und dieses
  Traceability-Paars ändert sich kein Source; kein Sonar-Befund wird vor einer
  Exact-Head-Analyse als geschlossen behauptet.

## Implementierungsentscheidung und Begründung

Der Refactor ersetzt die zwei hochkomplexen Ketten durch geordnete unveränderliche
Kategorie-/Routing-Tabellen und kleine private Resolver-Helfer. Die öffentlichen
Signaturen und Ergebniswerte von `category` und `proposed_destination` bleiben
unverändert. Die Reihenfolge ist in den Tabellen explizit, damit die Priorität
für generated, historical, security, evidence, testing, build-guide,
architecture, roadmap, connector, entry-point und Fallback überprüfbar bleibt.

## Geänderte Dateien

- scripts/generate_repository_organization_inventory.py
- tests/test_repository_organization_inventory.py
- reports/audits/change-records/CR-20260727-sonar-s3776-repository-inventory.md
- reports/audits/change-records/CR-20260727-sonar-s3776-repository-inventory.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -v -s tests -p test_repository_organization_inventory.py
rtk proxy git diff --check
```

Der isolierte Implementierungsvergleich führte den Basis- und den refaktorierten
Generator außerdem auf demselben aktuellen Korpus aus und verglich alle drei
temporären Outputs nach Normalisierung allein von `generated_at_utc` im JSON.

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussiertes Repository-Inventar-Testmodul | bestanden: 5 Tests. |
| Kategorie-/Zielpfad-Regressionsabdeckung | bestanden: Priorität, Parent-Routen, Framework-Routen und Fallbacks sind tabellengetrieben. |
| Generator-Outputvergleich über denselben Korpus | bestanden: JSON unterscheidet sich nur im normalisierten `generated_at_utc`; englische und deutsche Markdown-Pläne sind byteidentisch. |
| Receipt-/Symbol-Strukturprüfung | lokal bestanden: `category` und `proposed_destination` bleiben mit kleinen verzweigungsähnlichen AST-Zahlen vorhanden. Dies ist kein externes SonarQube-Cloud-Ergebnis. |
| `git diff --check` | bestanden: keine Whitespace-Fehler. |

## Security-Auswirkung

Die fokussierte Bewertung ist für eine neue Sicherheitsgrenze
`not_applicable`. Die Reads versionierter Dateien, private
Temporary-Root-Allokation, Subprocess-Nutzung, Fehler-Fallbacks und
Output-Schreibvorgänge des Generators sind unverändert. Der Outputvergleich
über denselben Korpus und die Route-/Fallback-Kontrollen liefern die relevante
Regressionsevidenz; es wurde kein neuer Sicherheitsbefund identifiziert.

## Dokumentationsstatus

Dieses vollständige englisch/deutsche Change-Record-Paar dokumentiert exakten
Umfang, Validierung, Grenzen und Delivery-Status. Die Record-Indizes sind in
beiden Sprachen aktualisiert. Kein generierter Inventar-Output wurde editiert.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll-, Report-Runtime- oder
Produktionsverhalten geändert oder behauptet. Generator-/Output-Äquivalenz
und fokussierte Unit-Tests sind keine Connector-Runtime-Evidence.

## Bekannte Einschränkungen

SonarQube Cloud hat den uncommitteten Kandidaten noch nicht analysiert. Die
zwei Receipt-basierten Befunde können erst nach einer Exact-Head-Analyse als
behandelt gelten; die breitere 1.022-Item-Remediation bleibt in Arbeit.

## Verbleibende Risiken

Die Tabellenreihenfolge ist der Verhaltensvertrag des Refactors. Eine spätere
Tabellenänderung könnte eine Routingpriorität ändern; die tabellengetriebenen
Route-/Prioritätstests und der Outputvergleich über denselben Korpus mindern
dieses Risiko. Daraus folgt keine Aussage über nicht verwandte Komplexitäts-,
Sicherheits- oder Duplikatbefunde.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Builds, Runtime-Smokes, Protokollmatrizen, Framework-Tests und
  MRTS-Tests sind nicht anwendbar, weil keine Connector-/Runtime- oder
  Cross-Repository-Quelle geändert wurde.
- GitHub Actions, gehostete SonarQube-Cloud-Analyse, Commit, Push, Pull
  Request und Merge sind noch nicht erfolgt. Dieser Record gibt keine
  Master-Merge-Autorisierung.

## Finaler Diff- und Review-Status

Der isolierte Task-Worktree enthält nur den abgegrenzten Generator, direkten
Test und erforderliches zweisprachiges Traceability-Material. Ein
Root-Agent-Source- und Diff-Review bestätigte, dass die geordneten Tabellen die
vorherigen Routingfamilien und Fallback-Pfade erhalten. Framework- und
MRTS-Quellcode, beide Gitlinks, Scanner-Controls, externe Issue-Disposition
und `master` bleiben unverändert. Delivery-Fakten werden erst nach ihrer
Beobachtung ergänzt.
