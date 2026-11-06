# Change Record: CR-20261103-framework-projection-decode-boundary

**Sprache:** [English](CR-20261103-framework-projection-decode-boundary.md) | Deutsch

Die Framework-Identitätsprojektion bleibt erhalten; ihre Dekodierungsgrenze wird vereinfacht.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261103-framework-projection-decode-boundary |
| Datum (UTC) | 2026-11-03 |
| Basis-Revision | `1232018b0c4b0b90d4255b7f5d8890a3d17f8e81` |

## Motivation und Problemstellung

Connector PR #443 meldet aktuell kognitive Komplexität16 oberhalb der erlaubten15 in `_render_framework_sha_projection_targets`. Die Schleife registrierter Ziele vermischte Identitätsrendering mit verschachtelter UTF-8-Dekodierung und Fehlerübersetzung.

## Akzeptanzkriterien

Alle geschlossenen Registry-, Quell-, Pfad- und Provenienzprüfungen sowie Fehlerergebnisse erhalten. Generierte Bytes und No-op-Verhalten beibehalten; bestehende gezielte Updater-/Callerregressionen und direkte Negativkontrollen verwenden. Frische gehostete Analyse muss die endgültig veröffentlichte Quelle bestätigen.

## Implementierungsentscheidung und Begründung

Nur UTF-8-Dekodierung und bestehender verketteter SyncError werden nach `_decode_framework_workflow` ausgelagert. Reihenfolge, erlaubte Syntaxmenge, reguläre Dateizugriffe, vertrauenswürdige Originalbytes und typisiertes Caller-/Workflowrendering bleiben in der Schleife erhalten. Mechanisches Inlining stellt den vollständigen ursprünglichen Funktions-AST wieder her. Keine Pins, Workflows, unveränderlichen Quellidentitäten oder Scannerregeln ändern sich.

## Geänderte Dateien

`ci/tools/sync-framework-component-versions.py` und dieses englisch/deutsche Change-Record-Paar. Bestehende wiederverwendbare Framework-Regressionen werden unverändert gegen den ausgewählten Parent ausgeführt.

## Ausgeführte Befehle

RTK-gekapseltes Parent-eigenes CPython3.15.2 führte sieben bestehende Tests für unveränderliche Caller/Projektionen und acht ausgewählte Updater-/Pfad-/Lock-/Transaktionsregressionen aus:15 PASS in14.364s. Eine private Strukturprüfung belegt vollständige Funktions-AST-Gleichheit nach einmaligem Helper-Inlining; direkte UTF-8-, ungültige Dateisystem-/vertrauenswürdige Originalbyte- und unbekannte Syntaxkontrollen erhalten Ausgabe, Fehler, Ursache und Schreibfreiheit. Exakte argv/cwd/Exit-Nachweise liegen unter `parent-fix` im Integrationstask. Native Dokumentations- und unveränderte Pinprüfungen stehen in den Übergabereceipts.

## Security-Auswirkung

Reine Refaktorierung der Dekodierungs-/Fehlergrenze. Kandidatendaten werden nicht ausgeführt. Exakte Quellen, Provenienz, Pfad-/Typgrenzen, unveränderliche geschützte Brokeridentitäten und transaktionale Publikationskontrollen bleiben unverändert. Ungültiges UTF-8 erzeugt weiterhin denselben von UnicodeDecodeError verketteten SyncError vor Schreibzugriffen.

## Runtime-Evidence

Dieser Refaktorierungslauf umfasst keine Host- oder Runtimeausführung. Caller-Parsertests belegen nur Kompatibilität und qualifizieren keinen geschützten Brokerlauf. Endgültige integrierte Protokollnachweise werden getrennt koordiniert.

## Bekannte Einschränkungen

Diese Änderung aktualisiert keine Parent-/Framework-/MRTS-Pins und führt keine Integration aus. Der gehostete Sonar-Komplexitätsnachweis benötigt Veröffentlichung und frische Analyse desselben Heads; kein lokales Scannerergebnis wird behauptet.

## Verbleibende Risiken

Der Integrationskoordinator muss die endgültige Quelle prüfen, über den bestehenden Branch veröffentlichen und aktuelle CI abwarten. Unabhängige historische Advisory-Befunde bleiben getrennt und werden hier weder geschlossen noch neu eingestuft.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Sonar-Vorprüfung/Scans, Installation und Authentifizierungsreparatur bleiben gemäß aktueller Benutzeranweisung ausgesetzt. Dieser begrenzte Sourceworker führte keine breite Suite, Hosts, Publisher, geschützten Brokerdispatch, administrative Aktion oder Befunddisposition aus.

## Finaler Diff- und Review-Status

Minimale Quellauslagerung gegen den exakten Basisstand geprüft; gezielte Tests und Strukturkontrollen bestanden. Commit/Push, gehostete Prüfungen am exakten Head und die getrennt freigegebene Integrationsreihenfolge gehören dem Koordinator.
