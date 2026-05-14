# Runners

Status: scaffolded

The runner layer defines the adapter shape expected by future connector tests.
It does not implement a real server/proxy adapter.

Required adapter methods:

- `prepare()`
- `start()`
- `stop()`
- `reload()`
- `apply_config()`
- `apply_rules()`
- `endpoint()`
- `send_request()`
- `collect_artifacts()`
- `cleanup()`

Unimplemented adapters must raise `NotImplementedError`.
