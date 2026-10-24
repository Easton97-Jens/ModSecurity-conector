# Change Record: CR-20261008-common-mapper-body-pointer-invariant

**Sprache:** [English](CR-20261008-common-mapper-body-pointer-invariant.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-common-mapper-body-pointer-invariant |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `85397f4d621c568316566faccac6c217fc5315d8` |

## Motivation und Problemstellung

Common-request_validate verwirft Nichtnull-Body-Größe bei Null-Daten; exportiertes request_mapper_validate_output akzeptierte dieselbe ungültige Anfrage.

## Akzeptanzkriterien

Diese bestehende Invariante am tatsächlichen Mapper verwerfen; gültige/leere Requests und Unsupported-/Oversized-Fehlerreihenfolge erhalten.

## Implementierungsentscheidung und Begründung

Eine begrenzte Body-Pointer-Konsistenzprüfung nach den bestehenden Body-Policy-Prüfungen ergänzen. Keine neue Host-Policy oder synthetische Runtime-Beobachtung.

## Geänderte Dateien

common/src/request_mapper_contract.c; tests/fixtures/nginx_common_input_validation.c; tests/test_nginx_common_input_validation.py; EN/DE-Nachweis.

## Ausgeführte Befehle

Echter Source-Probe mit C11 Wall/Wextra/Werror: RED1 (Mapper1 gegen Request-Validator0), dann GREEN4. Native make check-common-helpers (C17) und check-adapter-contracts Exit0; Diff und Record-Struktur vor Commit geprüft.

## Security-Auswirkung

Ungültige Adapter-Ausgabe wird wie beim bestehenden Request-Helfer sicher abgelehnt. Header-Prüfung und bestehende Body-Policy-Fehler unverändert.

## Runtime-Evidence

Nur echte Common-Validatoren kompiliert; kein HTTP-/Daemon-/Canonical-PASS behauptet. Frischer integrierter NGINX-Fault-Aufruf bleibt erforderlich.

## Bekannte Einschränkungen

Katalog und native Fault-Verdrahtung gehören dem Koordinator. Bestehende NGINX-Mapper-Ablehnung ist Phase1/HTTP400, keine erfundene Phase2/500.

## Verbleibende Risiken

Interposer muss exakt eigenen Worker, native Transaktion und URI binden. Fault-Ablehnung und Cleanup vor Coverage-Promotion beobachten.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger Lint, neu gebauter nativer Connector-Fault-Lauf und Remote-CI/Sonar fehlen. Kein altes Binary umetikettiert.

## Finaler Diff- und Review-Status

Ein Produkt-Guard mit Fokustests und zweisprachigem Nachweis; separater lokaler Commit, kein Push, Historienänderung, Gitlink- oder MRTS-Eingriff.
