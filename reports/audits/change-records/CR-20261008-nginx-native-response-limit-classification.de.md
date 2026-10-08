# Änderungsnachweis

**Sprache:** Deutsch | [English](CR-20261008-nginx-native-response-limit-classification.md)

## Identität

| Feld | Wert |
| --- | --- |
| Change ID | CR-20261008-nginx-native-response-limit-classification |
| UTC-Datum | 2026-10-08 |
| Parent-Basisrevision | `8b575c09` |

## Motivation und Problemstellung

Ein natives Response-Body-Reject besitzt keine Regelkorrelation und darf weder den regelbasierten SAFE-Log-only-Pfad benutzen noch Engine-EOS behaupten.

## Betroffene Komponenten und Sicherheitsgrenzen

NGINX-Intervention-Collector, Kontext-Beobachtungsfelder, Materialisierungsmap und kontrollierte C17-Tests. Framework, MRTS, generische Validatoren und Gitlinks unverändert.

## Akzeptanzkriterien

Nur die exakte native Limit-Signatur akzeptieren; BODY_LIMIT ohne Regel versiegeln, Downstream-Weitergabe verhindern und unerwartete Append-Regelentscheidungen vor echter Engine-Completion ablehnen.

## Untersuchte Alternativen

Jedes regelose403 als Body-Limit oder mit SAFE-Semantik zu behandeln, würde beliebige Engine-Antworten falsch klassifizieren.

## Implementierungsentscheidung

Vorhandenes geschlossenes natives Prädikat vor dem Regel-Dispatch anwenden. Request-Ownership im echten Kontext erfassen und vorhandene Response-Limit-/P4-Beobachtungsheader materialisieren.

## Geänderte Dateien und Tests

SOURCE_MAP, gemeinsame Kontextfelder, nativer Module-Interventionspfad, zwölf Source-C17-Collector-Kontrollen und zweisprachiger Nachweis.

## Befehle und Ergebnisse

Zwölf gezielte Collector-Tests bestehen frisch mit C17 -Wall -Wextra -Werror. Gültige SAFE-/STRICT-/off-Kontrollen und falsche Signatur, frühe Regel, ungültige Returns und fehlende Korrelation bleiben abgedeckt.

## Sicherheitsauswirkung

Keine synthetische Regel oder EOS; keine Body-Weitergabe nach technischem Reject. Framework-Containment/Freshness, Required-Auswahl und strikte Event-Validatoren unverändert.

## Dokumentation und Runtime-Evidenz

Source-Zustands-/Serializer-Unit-Nachweis, kein frischer Artefakt- oder nativer Request-Nachweis.

## Nicht ausgeführte Prüfungen

Frischer vollständiger Modul-/Binary-Build, integrierte native Requests, vollständige Required-Canonical-Validierung und Remote-CI/Sonar.

## Einschränkungen und Restrisiko

Engine-spezifische Signatur und echte Body-Completion brauchen Runtime-Validierung mit neuen Builds. Parallele Budget-/Cleanup-Änderungen gehören nicht zu diesem Commit.

## Finaler Diff- und Review-Status

Gezielter Stage-Umfang geprüft; fremde Orchestrierung und nicht gestagte Source-Arbeit erhalten.

