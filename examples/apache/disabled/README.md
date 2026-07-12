# Apache disabled profile

**Language:** English | [Deutsch](README.de.md)

## Behavior

`disabled/httpd.conf` sets `modsecurity off`, so Apache creates no connector transaction. This is distinct from `SecRuleEngine Off`, which leaves an
active host connector but disables rule evaluation inside the engine.

## Validation

Use the connector validation command named in the parent README after adapting
the host paths. Do not infer P1–P4 behavior from a disabled profile.
