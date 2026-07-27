# Change Record: Parent-Compiler-Guide-Metadatenliterale für SonarQube Cloud S1192

**Sprache:** [English](CR-20260727-sonar-compiler-guide-metadata-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-compiler-guide-metadata-literals |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-Sonar-Code-Smells AZ9cRzBeHhV2CayPTP5m, AZ9cRzBeHhV2CayPTP54, AZ9cRzBeHhV2CayPTP5S und AZ9cRzBeHhV2CayPTP5n (python:S1192). |
| Grenze | Parent-Compiler-Guide-Metadaten und Guide-Tests, dieses englisch/deutsche Paar und seine Indizes. Commands, URLs, Paketnamen, Source-Map-Pfade, deutsche Labels, Source-/Provenance-Verhalten, Guide-Semantik, Scanner-Konfiguration, externer Sonar/GitHub-Status, Framework/MRTS-Inhalt und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Vier aktuelle Sonar-Befunde kennzeichnen duplizierte Closed-Set-
Dokumentationsmetadaten: zwei Paketstatus, den gepatchten Lighttpd-
Host-Source-Wert und die englische Source-mapping-Überschrift. Moduleigene
Konstanten geben jedem Wert einen Besitzer und bewahren allen generierten
Guide-Text und Link-Ziele.

## Akzeptanzkriterien

- Konstanten nur für die vier ausgewählten Metadatenwerte ergänzen.
- Nur ihre exakten Value-/Key-/Heading-Uses ersetzen.
- Gerenderte englische und deutsche Guides byte-genau bewahren.
- Source-Map-Pfade, Commands, URLs, Paketnamen und Host-/Provenance-
  Beschreibungen bewahren.
- Dieses englisch/deutsche Paar und die Indizes pflegen, dann Paar und
  Diff-Hygiene validieren.

## Implementierungsentscheidung und Begründung

Zwei Paketstatus-Konstanten bleiben im bestehenden Status-Set, die gepatchte
Host-Source-Konstante bleibt im Lighttpd-Modell und beiden Translation-Maps,
und die englische Heading-Konstante ersetzt nur sechs Präsentationslabels. Die
deutsche Überschrift bleibt explizit und unverändert. Ein fokussierter
Metadatentest prüft exakte Werte und Stellen; bestehende idempotente,
bilinguale und Repository-Link-Tests beweisen aktuelle generierte Ausgabe.

## Geänderte Dateien

- scripts/generate_compiler_guides.py
- tests/test_compiler_guides.py
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- Die fokussierten Metadaten-, idempotenten Generated-File-, bilingualen
  Struktur- und Repository-Link-Controls bestanden: 4 Tests in 0.039s.
- Das AST-Ownership-Prädikat bestand mit vier exakten Werten und jeweils
  sieben, fünf, drei und sechs Constant-Loads.
- Der Guide-Test verwendete ein task-eigenes temporäres compiler-guides-
  Verzeichnis unter der Evidence-Root und ließ kein passendes Verzeichnis
  zurück.
- Paar-Validierung und Diff-Hygiene laufen nach Anlegen dieses Paars; es wird
  kein unbeobachtetes CI-, Runtime-, Review- oder Delivery-Ergebnis behauptet.

## Security-Auswirkung

Nicht anwendbar auf die Produktsicherheitsgrenze: Der Patch zentralisiert nur
statische Dokumentationsmetadaten. Er ändert weder Command, URL, Checksum,
Source-Map-Pfad, Hostauswahl, Provenance-Validierung, Filesystem-Verhalten,
Netzwerkverhalten noch Security-Control-Wortlaut.

## Runtime-Evidence

Es liefen kein realer Host-Build, keine Paketoperation, keine Connector-
Runtime, kein Framework, kein MRTS und keine Host-Runtime. Die Tests rendern
Guides nur im Speicher und in ein privates test-eigenes Temporary-Verzeichnis.

## Bekannte Einschränkungen

Der lokale Interpreter ist Python 3.14.4, während CI Python 3.14.6 verlangt;
das Ergebnis ist daher same-minor lokale Evidence. Dieser Batch behandelt vier
aktuelle Code-Smells; der öffentliche Endpunkt meldet weiter 1.125 OPEN-Issues
und dieser uncommittete Kandidat ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Guide-Labels können Statusvergleiche und gerenderten Inhalt speisen. Die
Konstanten behalten die exakten alten Bytes, Status-Set und Translation-Maps
bleiben abgedeckt, und der idempotente Guide-Test vergleicht generierte Dateien
mit den committeten Dokumenten. Exakte Delivered-Head-Sonar-Analyse bleibt
erforderlich, bevor die Keys extern aufgelöst sind.

## Nicht ausgeführte Prüfungen mit Begründung

- Reale Compiler-, Paket-, Connector- und Framework-Operationen liegen
  außerhalb dieses reinen Metadaten-Batches.
- Vollständige Dokumentations-/Link-Checks liegen außerhalb dieses Batches;
  frühere vollständige Läufe sind durch den absichtlich nicht initialisierten
  Framework-Gitlink blockiert.
- Es gab keine GitHub-CI, keine Sonar-PR-Analyse, kein Review, keinen Pull
  Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B21-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
