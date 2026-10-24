# Change Record: CR-20261008-nginx-adoption-timing-dependency-boundaries

**Sprache:** [English](CR-20261008-nginx-adoption-timing-dependency-boundaries.md) | Deutsch

Explizite begrenzte Dependency- und Deklarations-Guard-Korrektur.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-adoption-timing-dependency-boundaries |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `2ee41e347b8d6c7ac3eabc91aa3aa05f1690b279` |

## Motivation und Problemstellung

Nach Reparatur der URI-Extraktion belegten sieben Assertions zwei veraltete Guard-Grenzen: drei Standard-Includes und eine nichtinitialisierte Timing-Deklaration. Externer Restbericht vor Bearbeitung gespeichert.

## Akzeptanzkriterien

Nur inttypes.h, stdbool.h und time.h über die vorhandene Shadow-sichere Include-Grenze zulassen; nur die exakte nichtinitialisierte Measurement-Deklaration erkennen; Ordnung und Mutationskontrollen erhalten.

## Implementierungsentscheidung und Begründung

Endliche bestehende Whitelist um drei Einträge und exaktes Deklarationsmuster um eine Deklaration erweitern. Fünf tatsächlich eingebundene Source-Header in Unit-Fixtures kopieren, sodass Dependencies geprüft bleiben.

## Geänderte Dateien

Nur Adoption-Checker, dessen bestehendes Unit-Testmodul und dieses generierte EN/DE-Record-Paar; Produkt-Source unverändert.

## Ausgeführte Befehle

RTK-gekapseltes Parent-Python reproduzierte Baseline-RED (Exit 1), danach echte Checker-CLI PASS (Exit 0). Vollständige Adoption-Suite: 105 Tests PASS, 490,913 s, Exit 0. Drei Fokustests PASS, 22,724 s. Python-Syntax, git diff --check und generierte ChangeRecord-Struktur bestanden. Logs extern unter analysis/nginx-all-required-20261008T124555Z/stream-d-nginx-adoption-* erhalten.

## Security-Auswirkung

Lokale Header-Shadows und Symlinks bleiben für jeden neuen Header abgelehnt. Initialisierungsseiteneffekte und Timing-Aufrufe vor Mappervalidierung bleiben abgelehnt; bestehende Macro-Decoys erhalten.

## Runtime-Evidence

Keine: begrenzte statische Checker- und synthetische Source-Unit-Tests, kein Native-Runtime- oder Build-Nachweis.

## Bekannte Einschränkungen

Vorheriger URI-Commit beließ absichtlich sieben rote unabhängige Assertions; dieser Folgeslice behebt nur ihre belegten Ursachen.

## Verbleibende Risiken

Künftige Source-Deklarationen/Dependencies benötigen explizite Guard-Prüfung; keine allgemeine Statement- oder Include-Ausnahme ergänzt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Native-Build/Runtime, Installation, Push, MRTS-Änderung oder vollständiger fremder Lint; außerhalb dieser statischen Checker-Aufgabe. Vollständiger bilingualer Checker ausgeführt: Exit 1 nur wegen fremder fehlender Framework-Links; dessen Gitlink ist im isolierten Worktree nicht initialisiert. Keine neuen Record-Fehler; keine kaschierende Dependency-Änderung.

## Finaler Diff- und Review-Status

Diff auf vier exakte Checker-Ergänzungen und begrenzte Fixture-/Kontrollergänzungen geprüft. Vollständige Suite mit 105 Tests und allen bisherigen Negativkontrollen vor separatem normalem Folgecommit bestanden. Produkt-Source unverändert.
