# ModSecurity rule examples

**Language:** English | [Deutsch](rule-examples.de.md)

## Quick orientation

The rule examples demonstrate **engine state**, not connector topology.
Enforcement can apply disruptive actions where the selected host phase allows
it; DetectionOnly still evaluates rules but does not apply disruptive engine
actions; engine Off disables rule evaluation while the host connector can
remain present. A disabled connector is different again because the connector
path itself is not active.

## Rule-engine modes

```apache
# Enforce an eligible pre-commit deny.
SecRuleEngine On

# Match and log without a disruptive action.
SecRuleEngine DetectionOnly

# Do not evaluate rules after they are loaded.
SecRuleEngine Off
```

`DetectionOnly` loads and evaluates rules and logs matches without applying disruptive actions. `Off` disables engine rule evaluation; a connector switch may still be active. Conversely, `SecRuleEngine On` reaches no traffic when the host connector is disabled.

## P1–P4 example

```apache
SecRequestBodyAccess On
SecResponseBodyAccess On
SecResponseBodyMimeType text/plain text/html application/json
SecResponseBodyLimit 1048576
SecResponseBodyLimitAction ProcessPartial
SecRule RESPONSE_BODY "@contains response-attack" \
    "id:1100301,phase:4,deny,log,status:403"
```

P1 is request headers, P2 request body, P3 response headers, and P4 response body. The P4 rule requests a 403 before commit; after commit the visible status remains host-dependent and must not be documented as guaranteed.
