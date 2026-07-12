# Envoy DetectionOnly profile

**Language:** English | [Deutsch](README.de.md)

## Behavior

`detection-only/msconnector-runtime.conf` is used with the selected ext_proc YAML and selects DetectionOnly rules. DetectionOnly loads and evaluates engine rules and records
matches, but it does not apply disruptive engine actions.

## Validation

Use the connector validation command named in the parent README after adapting
the host paths. This profile is configuration guidance, not runtime evidence.
