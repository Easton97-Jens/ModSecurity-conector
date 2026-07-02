**Language:** English | [Deutsch](new-connector-contract.de.md)

# New connector contract

A future connector should declare complete metadata, connector capabilities,
configuration mapping, request/response mapping, decision mapping, event/log
mapping, and artifact layout before claiming support.

This document is a contract guide only. It does not migrate any existing
connector and does not claim runtime behavior, capability support, or production
readiness.

## Common package expectations

Future connector adoption should map host requests/responses through the common
request and response helpers, expose manifests and origin governance, use the
build-contract target vocabulary where adopted, and keep runtime reports honest.
No existing connector is adopted by this documentation-only update.
