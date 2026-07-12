# Apache rules reference

**Language:** English | [Deutsch](README.de.md)

The reusable No-CRS source is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
It is repository-relative and should be copied or installed by the operator as
a reviewed host rules file, for example /etc/modsecurity/no-crs-baseline.conf.

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

The checked-in p1-p4-safe.conf is an illustrative Apache rules file. Its
9002801 rule is local to that example and is not an OWASP CRS or No-CRS
baseline ID.
