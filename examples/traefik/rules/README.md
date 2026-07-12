# Traefik rules reference

**Language:** English | [Deutsch](README.de.md)

The persistent local UDS engine service needs an installed reviewed rules file.
The repository source for the No-CRS profile is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |
