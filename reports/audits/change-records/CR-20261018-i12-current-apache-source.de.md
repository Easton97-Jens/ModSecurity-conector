# Change Record: CR-20261018-i12-current-apache-source

**Sprache:** [English](CR-20261018-i12-current-apache-source.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-current-apache-source |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `2c38d0ff2960a9ff2a76291955e808683febf06e` |

Verantwortung: Parent-PR #410; Verbraucher: Apache-PR #414.

## Motivation und Problemstellung

Das historische Apache-Capture-Profil bindet native Observer-Eingabebytes seines
ursprünglichen Exports. Seine Anwendung auf den aktuellen committeten Observer
scheitert korrekt. Ein aktueller Vollbuild braucht ein eigenes streng gebundenes
Quellanwendungsprofil.
Die Integration änderte außerdem fünf Repository-Basisquellen von HAProxy und
lighttpd. Ihre historischen Inhalts-Hashes müssen weiterhin die Originalbytes liefern.

## Akzeptanzkriterien

Einen vollständigen aktuellen Git-Export ausschließlich mit seinem v2-Inventar
akzeptieren. Historische Objekte und Profile, Capture-Ergebnisbytes und Runtime-
Routen-IDs erhalten. Eine ersetzte v1-Identität, geänderte Quellbytes und unbekannte
Formate vor jedem Schreiben ablehnen. Quellanwendung allein qualifiziert keinen
Hostfall.

## Implementierungsentscheidung und Begründung

Das zusätzliche Profil `apache-current` ändert die beiden nativen C-/Header-
Eingabehashes und verlangt das vorhandene v2-Format. Ergebnis-Hashes, drei Apache-
Produkt-Overlays und SDK-ABI bleiben mit `apache` identisch. Die Registry lehnt
unbekannte Pflichtformate ab; die Anwendung prüft die Profilanforderung vor ihrem
ersten Schreibzugriff. Vollständiges Inventar und Einzeldatei-Hashes bleiben Pflicht.
Die integrierte gemeinsame Korrektur sichert bereits die fünf historischen Objekte
als verlustfreie Textzeilenobjekte. Alle 155 bisherigen Inhalts-Hashes bleiben
unverändert. Das Apache-Profil benötigt keine doppelten Sicherungsobjekte; kein
historisches Overlay wird stillschweigend auf eine geänderte Basis angewendet.

## Geänderte Dateien

Gemeinsame Capture-Registry, Manifest, Negativkontrollen und EN/DE-Anleitung. Keine historischen Inhaltsbytes,
Produktquellen oder Framework-/MRTS-Gitlinks werden geändert.

## Ausgeführte Befehle

RTK-gekapselte Unittest-Discovery mit Parent-Python für `test_capture_sources.py`:
54 Tests bestanden, Exit 0. Die Kontrollen exportieren den gesamten committeten
Parent-Gitbaum, binden tatsächliche Revision/Baum/Modi/Hashes und prüfen die echte
Anwendung. Historische Profilgleichheit und sämtliche Ergebnis-Hashes werden geprüft.
Registry-Prüfung: 155 Inhaltsobjekte, zehn Quellprofile, Exit 0. Der erste Lauf auf
dem aktuellen Head scheiterte an geänderten Repository-Basen; behoben wurde dies
durch Erhaltung ihrer historischen Bytes, ohne Hashprüfungen zu umgehen.

## Security-Auswirkung

Keine Validierung, Compilerwarnung, Isolation, Authentifizierung oder Quality Gate
wird abgeschwächt. Das Profil verlangt stärkere Herkunft als der historische v1-Pfad.

## Runtime-Evidence

Dies sind Quellintegritätskontrollen mit null Runtime-PASS. Frischer Apache-Build,
geladene Images und fallbezogene Qualifikation benötigen eigene Beobachtungen.

## Bekannte Einschränkungen

Zukünftige Quelländerungen werden bis zur Prüfung ihrer exakten Eingabebytes und
Capture-Kompatibilität abgelehnt. Alte Läufe werden nicht aktualisiert.

## Verbleibende Risiken

Erfolgreiche Quellanwendung belegt weder Buildreproduzierbarkeit noch Hostverhalten.
PR #414 muss diese Beobachtungen auf der integrierten Revision liefern.

## Nicht ausgeführte Prüfungen mit Begründung

Diese gemeinsame Profiländerung führt keine Connector-Hostmatrix, Bereitstellung,
Veröffentlichung oder Master-Integration aus. Hosted Checks folgen dem normalen Push.

## Finaler Diff- und Review-Status

Begrenzter Profil-Diff und Ablehnungskontrollen sind geprüft. Historische Evidenz
bleibt ihrer tatsächlichen Quellrevision und instrumentierten Binary zugeordnet.
