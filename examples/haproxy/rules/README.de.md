# HAProxy-Regelreferenz

**Sprache:** [English](README.md) | Deutsch

Die nativen HTX-Referenzen verwenden eine installierte Kopie der
repository-eigenen [No-CRS-Baseline-Regeln](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Der rules-file-Wert im HAProxy-Filter ist ein Host-Installationspfad, kein
relativer Pfad zum HAProxy-Prozess.

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |
