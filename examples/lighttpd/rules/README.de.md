# lighttpd-Regelreferenz

**Sprache:** [English](README.md) | Deutsch

Das native Modul liest die geprüfte installierte Regeldatei, die von
msconnector.config-file benannt wird. Die Repositoryquelle für das
No-CRS-Profil ist
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Regel-ID | Phase | Zweck |
| ---: | ---: | --- |
| 1100001 | P1 | Request-Header-Deny |
| 1100101 | P2 | Request-Body-Deny |
| 1100201 | P3 | Response-Header-Deny |
| 1100301 | P4 | Response-Body-Entscheidung für die Safe-Grenze |
