# Change Record: Parent-Repository-Organisation-Regex und Routing für SonarQube Cloud

**Sprache:** [English](CR-20260727-sonar-organization-regex-routing.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-organization-regex-routing |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-Sonar-Code-Smells AZ9cRzA4HhV2CayPTP49 (python:S6035), AZ9cRzA4HhV2CayPTP4- und AZ9cRzA4HhV2CayPTP4_ (python:S5843) sowie AZ9cRzA4HhV2CayPTP5C (python:S8513). |
| Grenze | Parent-Metadatenklassifizierer und reiner Unit-Test, dieses englisch/deutsche Paar und seine Indizes. Tracked-File-Subprocesses, Temporary-Output-Allokation, Datei-Lese-/Schreibzugriffe, Framework-Discovery, Scanner-Konfiguration, externer Sonar/GitHub-Status, Framework/MRTS-Inhalt und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Das temporäre Repository-Organisations-Inventar verwendete vermeidbare
Regex-Alternationskomplexität und äquivalente verkettete Prefix-Checks. Die
vier Sonar-Befunde kennzeichnen diese reinen Klassifizierer-Ausdrücke. Die
Änderung muss aktuelle Metadaten-Matches, einschließlich akzeptierter
Legacy-Unmatched-Brace-Formen, und das Framework-Catalog-Routing bewahren.

## Akzeptanzkriterien

- Das gemeinsame Dollar-Prefix sowie gemeinsame Reference-Boundary/-Suffix
  faktorisieren.
- Nur die drei äquivalenten einzeichenlangen Assignment-Alternativen und die
  gepaarte Check-Prefix-Chain ersetzen.
- Positive, negative und Legacy-Regex-Matches sowie Catalog-Routing bewahren.
- Den bestehenden privaten Temporary-Output-Symlink-/Permission-Control
  bewahren.
- Dieses englisch/deutsche Paar und die Indizes pflegen, dann Paar und
  Diff-Hygiene validieren.

## Implementierungsentscheidung und Begründung

VARIABLE_RE teilt sein Dollar-Prefix und verwendet eine äquivalente Character
Class für die drei Assignment-Operatoren. REFERENCE_RE teilt Word-Boundary und
Directory-Suffix und behält die fünf Prefixe. Der Routing-Zweig verwendet ein
Tuple-Argument für startswith. Der neue reine Test prüft Legacy-Brace-Matches,
abgelehnte Near-Misses, Reference-Boundaries und beide Check-Prefix-
Schreibweisen. Temporary-Directory-, Subprocess- und Framework-Verhalten
blieben unverändert.

## Geänderte Dateien

- scripts/generate_repository_organization_inventory.py
- tests/test_repository_organization_inventory.py
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Ein In-Memory-Baseline-Import hielt repräsentative alte Regex-Matches und
  Catalog-Destinations vor der Änderung fest.
- Die fokussierte Repository-Organisation-Suite bestand: 3 Tests in 0.001s.
- Der bestehende RuntimePathSecurity-Temporary-Writer-Symlink-Test bestand: 1
  Test in 0.418s. Er verwendete und entfernte ein task-eigenes temporäres
  Verzeichnis unter der Evidence-Root; der exakte Pfad wurde als nicht
  vorhanden bestätigt.
- Das AST-Regex-/Tuple-Routing-Ownership-Prädikat bestand.
- Paar-Validierung und Diff-Hygiene laufen nach Anlegen dieses Paars; es wird
  kein unbeobachtetes CI-, Runtime-, Review- oder Delivery-Ergebnis behauptet.

## Security-Auswirkung

Risikoarme Metadatenklassifizierer-Wartung, keine Lockerung eines
Security-Controls. Die ASCII-Identifier- und Reference-Character-Classes
bleiben erhalten. Der Patch ändert weder Subprocess-Command, private
mkdtemp-Allokation, Pfadverhalten noch Write-Permissions; der bestehende
Symlink-/Permission-Control bestand.

## Runtime-Evidence

Die neue Suite importiert das Modul und ruft nur Regex-/Routing-Funktionen im
Speicher auf. Der etablierte Security-Control ruft main mit gemockten
Tracked-Files auf, benutzt nur test-eigene temporäre Reports, führt kein
echtes Git-Listing aus und hinterlässt keine Ausgabe. Es liefen keine
Connector-, Framework-, MRTS- oder Host-Runtime.

## Bekannte Einschränkungen

Der lokale Interpreter ist Python 3.14.4, während CI Python 3.14.6 verlangt;
das Ergebnis ist daher same-minor lokale Evidence. Dieser Batch behandelt vier
aktuelle Code-Smells; der öffentliche Endpunkt meldet weiter 1.125 OPEN-Issues
und dieser uncommittete Kandidat ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Regex-Refactoring kann Edge-Matches ändern. Der Test bewahrt aktuelle
ungewöhnliche akzeptierte Klammerbehandlung, weist beabsichtigte Near-Misses
ab und behält keine Capturing-Groups, daher gibt findall weiter vollständige
Matches zurück. Eine Sonar-Analyse auf exaktem ausgeliefertem Head bleibt
erforderlich, bevor diese Keys extern aufgelöst sind.

## Nicht ausgeführte Prüfungen mit Begründung

- Das reale Inventory-main wurde nicht gegen Tracked-Files ausgeführt, weil es
  Git abfragt und einen Planning-Snapshot außerhalb dieses Classifier-only-
  Batches schreibt.
- Vollständige Dokumentations-/Link-Checks liegen außerhalb dieses Batches;
  frühere vollständige Läufe sind durch den absichtlich nicht initialisierten
  Framework-Gitlink blockiert.
- Es gab keine GitHub-CI, keine Sonar-PR-Analyse, kein Review, keinen Pull
  Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B20-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
