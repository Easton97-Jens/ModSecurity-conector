# Change Record: Parent-Common Event-JSON Optional-Field-Zerlegung

**Sprache:** [English](CR-20260730-sonar-common-event-json-complexity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-common-event-json-complexity` |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f` |
| Tracking | `FND-SONAR-0020`; SonarQube Cloud `AZ9cRy9OHhV2CayPTP4Y` / `c:S3776` bei `common/src/event.c:502`. |
| Grenze | Nur Parent-Common-Event-Serializer und seine gepaarten Change-Record-/Index-Dokumente. |

## Motivation und Problemstellung

`msconnector_event_write_json_ex` liegt weiter einen Punkt über der Cognitive-
Complexity-Grenze. Seine zwei optionalen JSON-Field-Formatierungsbranches haben
identische Bounded-Output- und Trunkierungssemantik.

## Akzeptanzkriterien

- Optionale JSON-Fragmente für `body_limit_outcome` und `late_intervention_mode`
  behalten Empty-, Valid- und Trunkierungsverhalten.
- QUIC-ID-Redaktion, begrenzte Transport-Metadatenvalidierung, Serializer-
  Return-Values und vorhandene JSON-Field-Namen bleiben unverändert.
- Der aktuelle C17-Common-Helper-Smoke besteht mit GCC und Clang.

## Implementierungsentscheidung und Begründung

Ein begrenzter Helper besitzt jetzt den gemeinsamen Empty-Field-, `snprintf`-,
Overflow- und Trunkierungspfad. Der Caller behält beide festen Field-Namen und
ihre Reihenfolge; damit sinken unabhängige Branches ohne Änderung des
Serializer-Vertrags.

## Geänderte Dateien

- `common/src/event.c`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `CC=gcc make check-common-helpers-c17` mit task-eigenen externen Build-/Runtime-Roots | bestanden mit `-std=c17 -Wall -Wextra -Werror`. |
| `CC=clang make check-common-helpers-c17` mit getrennten externen Roots | bestanden mit demselben C17-Vertrag. |
| `git diff --check` | vor der Record-Erstellung bestanden; läuft erneut vor Delivery. |

## Security-Auswirkung

Der Serializer escaped weiter Text vor dem Formatting, bewahrt Bounded-
Transport-Token-Handling und redigiert rohe QUIC-Connection-Identifier. Keine
Policy-, Input-Validation-, Logging-Content- oder SonarQube-Cloud-Control-
Änderung.

## Runtime-Evidence

Der Common-Helper-Smoke prüft normale JSON-Ausgabe, Trunkierung und Event-
JSONL-Serialisierung mit der realen C-Implementierung.

## Bekannte Einschränkungen

Dies ist fokussierte Common-Serializer-Evidence, keine Connector-Host-, CRS-,
MRTS-, HTTP/2- oder HTTP/3-Runtime-Matrix.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Connector-Matrix oder Repository-Security-Scan lief, weil
die Maintainability-Zerlegung vorhandene Serializer-Security-Controls bewahrt.
Hosted Actions, SonarQube Cloud und Review-Evidence stehen bis zur Draft-PR-
Delivery aus.

## Verbleibende Risiken

Das ursprüngliche Issue ist erst behoben, wenn die Current-Head-SonarQube-
Cloud-Analyse bestätigt, dass `AZ9cRy9OHhV2CayPTP4Y` fehlt; keine Suppression
wird genutzt.

## Finaler Diff- und Review-Status

Der Kandidat ist Source-lokal mit gepaarter Traceability. Delivery und Exact-
Head-Verifikation stehen aus; kein Merge oder `master`-Change wird behauptet.
