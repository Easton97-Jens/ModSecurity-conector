# HAProxy rules reference

**Language:** English | [Deutsch](README.de.md)

The native HTX references consume an installed copy of the repository-owned
[No-CRS baseline rules](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
The rules-file value in the HAProxy filter is a host installation path, not a
path relative to the HAProxy process.

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |
