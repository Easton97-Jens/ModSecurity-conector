# Change Record: CR-20261008-nginx-native-authority-producer

**Sprache:** [English](CR-20261008-nginx-native-authority-producer.md) | Deutsch

Expliziter Authority-Producer; ausschließlich Unit-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-authority-producer |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `9ecd63fce94d424526fe6a70da1021c8f0d02681` |

## Motivation und Problemstellung

Explizite Autorität muss tatsächliche aktuelle saubere Parent-, Framework- und MRTS-Identitäten sowie die übergebenen Artefaktbytes binden, ohne einem Receipt zu vertrauen.

## Akzeptanzkriterien

Unterschiedliche explizite Quellwurzeln, aktuelle HEAD40 und beide aktuellen Gitlinks verlangen; unsaubere Quellen, unsichere Pfade, veränderte Beobachtungen und vorhandene Ausgabe ablehnen.

## Implementierungsentscheidung und Begründung

produce_native_authority prüft das tatsächliche Git-Tupel vor und nach stabilen begrenzten Hashes und schreibt das geschlossene schema_version-1-Original exklusiv als native-operation-authority.json mit Modus 0400. Alle CLI-Wurzeln, Run-ID, Binary-/Modulpfade und fünf Fault-Libraries sind Pflicht. Die Ausgabe liegt unter der expliziten externen Artefaktwurzel in einem bestehenden privaten 0700-Verzeichnis. Acht Case-Digests folgen aus der geschlossenen Zuordnung input/begin/finish/write/budget.

## Geänderte Dateien

Nur die neue ci/runtime/lifecycle/nginx_native_authority.py, tests/test_nginx_native_authority.py und dieser zweisprachige Record.

## Ausgeführte Befehle

RTK-verpacktes unittest scheiterte zuerst am fehlenden Producer; danach bestanden die ersten fünf echten Git-Tests. Erweiterte Producer-/Configtest-Prüfungen bestanden 30 Tests; Runtime-Pfadsicherheit bestand 21 Tests. Die Eigentümerablehnung verwendet explizit injizierte fremde fstat-Metadaten, da dieser Container chown65534 mit EINVAL ablehnt. Der Repository-Generator erstellte dieses Paar mit dreizehn Überschriften; die Archivprüfung bestand und git diff --check meldete keine Whitespace-Fehler.

## Security-Auswirkung

NOFOLLOW gilt für jede Pfadkomponente; Artefakte müssen dem aktuellen Benutzer gehören, non022, begrenzt, nichtleer, regulär und einfach verlinkt sein sowie stabile Metadaten und Bytes besitzen. FIFO wird nichtblockierend geöffnet. Root-eigene Sticky-Vorfahren sind erlaubt, finale Verzeichnisse bleiben owned/non022. Git-Umgebungsüberschreibungen werden entfernt. Kein Receipt liefert vertrauenswürdige Digests.

## Runtime-Evidence

Keine. Kontrollierte temporäre Git-Repositories und Dummy-Artefaktbytes sind nur Unit-Evidence. Kein Build, Compilerlauf, nativer Aufruf oder Host-Runtime-Lauf.

## Bekannte Einschränkungen

Jedes Artefakt ist auf 64 MiB, JSON auf 16 KiB begrenzt. Git-Snapshots und wiederholte Hashes erkennen beobachtete Änderungen, ersetzen keinen atomaren Snapshot aller Repositories. Dateimodi schützen nicht vor privilegierten Eigentümern. Hashes belegen weder Compiler, Engine-Library, Release noch natives Verhalten.

## Verbleibende Risiken

Der Koordinator muss tatsächliche Build-Bereitschaft separat prüfen und das zurückgegebene aktuelle Tupel an seinen ausgewählten Run-Kontext binden. Retention muss Originalbytes und Digest erhalten; kanonisches PASS bleibt außerhalb dieses Producers.

## Nicht ausgeführte Prüfungen mit Begründung

Native Builds/Runtime, Engine-/Archivbereitschaft und integrierte kanonische Retention lagen außerhalb dieses Slice. Drei vorhandene Execute-only-Tests aus test_runtime_path_utils scheiterten bereits im Setup, da chown65534 EINVAL liefert. Ein zuerst falsch benanntes Runtime-Pfadtestmodul wurde nicht importiert; das korrekte test_runtime_path_security bestand danach. Keine Paketinstallation oder Remote-Analyse.

## Finaler Diff- und Review-Status

Fokussierte eigene Dateien geprüft; bestehende Quellen, Gitlinks und Commits erhalten. Der Producer aktualisiert keine Gitlinks und entdeckt keine ersatzweise vertrauenswürdigen Wurzeln.
