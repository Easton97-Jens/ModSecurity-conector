# Änderungsnachweis: CR-20261008-nginx-phase4-completion-observation

**Sprache:** [English](CR-20261008-nginx-phase4-completion-observation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-phase4-completion-observation |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `0981e437968a3d0df5cd6200f4d55b0128e4874e` |

## Motivation und Problemstellung

Interventionsereignisse allein beweisen weder erfolgreiche native Phase-4-Ausführung noch tatsächlich von der Engine behaltene Länge.

## Akzeptanzkriterien

Native Rückgabe1 und abgeschlossene Common-P4-Maske/letzte Phase ohne aktive Phase verlangen. Inkonsistente/überdimensionierte Zähler ablehnen; null Append-Aufrufe nur bei vollständig leerer Antwort.

## Implementierungsentscheidung und Begründung

Der neue NGX-Konstruktor leiht Event-/Reason-/Header-Speicher des Aufrufers. Er setzt phase4_completion, response_body, echtes EOS und gelieferte Bytezähler. Tatsächlich behaltene Länge und Append-Aufrufe stehen in einer begrenzten payloadfreien Begründung. Aktionen/Status/Identitäten bleiben erhalten; keine abgeleiteten Marker-Split-/MIME-Flags.

## Geänderte Dateien

Neuer Beobachtungsheader, kompilierte C-Fixture, Python-Harness und dieses EN/DE-Paar. Gemeinsame Modul-/Bodyfilter-/Kontext-/Source-Map-Dateien gehören dem Koordinator.

## Ausgeführte Befehle

Kompiliertes RED wegen fehlendem Header. Striktes C17 -Wall -Wextra -Werror -pedantic-errors für sanity0/1 und echte Common-JSONL-Serialisierung bestehen. Ungültige Rückgaben, Phasen/Masken, Zähler, Zeiger und kleine Puffer werden getestet.

## Security-Auswirkung

Kein Payload, erfundene Regel, neuer Modus, umgedeuteter Common-Zähler oder abgeschwächter Validator. Ungültiger Abschluss verändert das Event nicht; Reason-Speicher gehört weiter dem Aufrufer.

## Runtime-Evidence

Die kompilierte Fixture beweist Konstruktor und echte Common-Serialisierung, nicht laufende Engine/NGINX. Tatsächliche CAPI-Länge und Append-Zahl muss der Adapter nach erfolgreichem nativen Abschluss liefern.

## Bekannte Einschränkungen

Kein integrierter Adapteraufruf. Der Event-Speicher muss initialisiert sein; geliehene Werte müssen die Serialisierung überleben.

## Verbleibende Risiken

Falsche Messung beim Aufrufer kann der Konstruktor nicht korrigieren. Runtime und strikte kanonische Zuordnung bleiben separat erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Frische Runtime und neu gebautes Modul warten auf Koordinatorintegration. Kein Exact-Head oder kanonisches PASS behauptet.

## Finaler Diff- und Review-Status

Nur exklusive neue Dateien; keine Common-/Modul-/Bodyfilter-/Gitlink-/MRTS-/Publikationsänderungen.
