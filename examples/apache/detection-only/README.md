# Apache DetectionOnly profile

**Language:** English | [Deutsch](README.de.md)

## Behavior

`detection-only/httpd.conf` keeps `modsecurity on` and selects the DetectionOnly rules file. DetectionOnly loads and evaluates engine rules and records
matches, but it does not apply disruptive engine actions.

## Validation

Use the connector validation command named in the parent README after adapting
the host paths. This profile is configuration guidance, not runtime evidence.
