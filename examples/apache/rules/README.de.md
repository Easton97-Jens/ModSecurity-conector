# Apache-Regelreferenz

**Sprache:** [English](README.md) | Deutsch

Die wiederverwendbare No-CRS-Quelle ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Sie ist repository-relativ und soll vom Betreiber als geprüftes Host-Ruleset,
zum Beispiel /etc/modsecurity/no-crs-baseline.conf, installiert oder kopiert
werden.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

Die eingecheckte Datei p1-p4-safe.conf ist eine illustrative Apache-
Regeldatei. Ihre Regel 9002801 gehört nur zu diesem Beispiel und ist weder
eine OWASP-CRS- noch eine No-CRS-Baseline-ID.
