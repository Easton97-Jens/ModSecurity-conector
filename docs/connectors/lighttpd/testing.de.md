<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# lighttpd-Tests

**Sprache:** [English](testing.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Ebenen

Führen Sie `make build-lighttpd`, `make check-config-lighttpd`, einen vorhandenen Start-/Runtime-Smoke und `make full-lifecycle-lighttpd` als getrennte Ebenen aus. Build, Config und Start sind kein Rule-Engine-PASS.

## No-CRS-Kernregeln und Cases

Diese Rule-IDs gehören zum repository-eigenen No-CRS-Testprofil, nicht zu OWASP CRS.

| Rule-ID | Phase | Zweck |
| ---: | --- | --- |
| `1100001` | P1 | Request-Header deny |
| `1100101` | P2 | Request-Body deny |
| `1100201` | P3 | Response-Header deny |
| `1100301` | P4 | Response-Body deny oder Safe-Late-Intervention |

## Evidence und Run-Grenze

Case-IDs beschreiben eine Capability und den erwarteten Zustand. Ein ausgewählter Case benötigt zurechenbare Result-/Event-Evidence, Profilidentität und die konfigurierte Run-ID. Ein `PASS`-Aggregat darf nicht aus Build-Ausgabe abgeleitet werden.

## Statuswerte

`PASS`, `FAIL`, `BLOCKED`, `NOT EXECUTED`, `NOT APPLICABLE` und `UNSUPPORTED` stehen unter [Testebenen](../../testing/test-levels.de.md).
