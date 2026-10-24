# Change Record: CR-20261008-nginx-projected-jsonl-source-guard

**Sprache:** [English](CR-20261008-nginx-projected-jsonl-source-guard.md) | Deutsch

Begrenzte statische Source-Checker-Korrektur; Produkt-Source unverändert.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-projected-jsonl-source-guard |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `8004340da887d143bc5e850822ac122eb5ce8b59` |

## Motivation und Problemstellung

Die Source projiziert nun eine begrenzte URI vor der Common-Serialisierung; eine veraltete Literal-Suche löste ValueError aus.

## Akzeptanzkriterien

Aktive Projektion akzeptieren, Bypässe/Decoys ablehnen und warnende Request- sowie strikte Phase-Tails erhalten.

## Implementierungsentscheidung und Begründung

Lexikalische Funktionsextraktion und vollständige geordnete Pipeline-Prüfung; fehlende Helfer scheitern geschlossen ohne Import-Traceback.

## Geänderte Dateien

Nur NGINX-Adoption-Checker, dessen Unit-Tests und dieses generierte EN/DE-Record-Paar.

## Ausgeführte Befehle

RTK-gekapseltes Parent-Python: drei Fokustests bestanden (27,899 s). Echte Checker-CLI Exit 1 mit beiden URI-Assertions PASS; unabhängige Restguards bleiben FAIL.

## Security-Auswirkung

Keine Produkt-Source oder Runtime-Semantik geändert. Aktive Roh-Event-Serialisierung, Projektionsbypass, frühe Writes und Erfolg im Fehlerpfad bleiben abgelehnt.

## Runtime-Evidence

Keine: synthetische Source-Mutationstests und statische Checker-CLI sind kein Runtime-Nachweis.

## Bekannte Einschränkungen

Sieben unabhängige Assertions bleiben rot: explizite Standardheader-Whitelist und exakte Timing-Deklarationsgrenze; externer Restbefundbericht belegt jede Ursache.

## Verbleibende Risiken

Gesamter Adoption-Gate noch nicht grün; separat freigegebener Dependency-/Deklarations-Folgeslice bleibt erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, Native-Runtime, vollständiger Lint, Installation, Push oder MRTS-Änderung; begrenzter Source-Checker-Slice.

## Finaler Diff- und Review-Status

Begrenzten Diff geprüft; URI-Fokusvalidierung bestanden. Vollständige bestehende Suite gestartet; Baseline-Restresultate extern erhalten und im Folgeslice abzugleichen.
