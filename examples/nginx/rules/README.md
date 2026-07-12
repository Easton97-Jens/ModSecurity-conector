# NGINX rules reference

**Language:** English | [Deutsch](README.de.md)

The reusable No-CRS source is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Install a reviewed copy at the rules-file path selected in the NGINX
configuration.

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

The illustrative p1-p4-safe.conf uses 9001801 only as a local example. It is
not an OWASP CRS or No-CRS baseline ID.
