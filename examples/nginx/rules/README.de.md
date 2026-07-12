# NGINX-Regelreferenz

**Sprache:** [English](README.md) | Deutsch

Die wiederverwendbare No-CRS-Quelle ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Eine geprüfte Kopie am in der NGINX-Konfiguration gewählten Rules-Dateipfad
installieren.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |

Die illustrative Datei p1-p4-safe.conf verwendet 9001801 nur als lokales
Beispiel. Es ist weder eine OWASP-CRS- noch eine No-CRS-Baseline-ID.
