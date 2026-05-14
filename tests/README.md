# Tests

Status: scaffolded

## Boundaries

`tests/common/` contains only portable engine, rule, and behavior tests that can
run through libmodsecurity v3 public APIs without a server/proxy runtime.

`tests/<connector>/` contains connector-specific behavior tests.

If a test depends on hook order, buffering, streaming, reload, local ports,
server config, module loading, or server/proxy log format, it is not portable
until proven otherwise.

## Categories

- engine-core tests
- connector-specific tests
- audit-log tests
- request-body tests
- response-body tests
- streaming/buffering tests
- capability-dependent tests

## Status

No test runner executes real connector behavior yet.
