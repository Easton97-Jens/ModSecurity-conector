# Runners

Status: scaffolded

The runner layer defines the adapter shape expected by future connector tests.
It does not implement a complete server/proxy adapter suite.

Implemented now:

- `case_cli.py materialize` reads a shared YAML case, writes a connector runtime
  rule file, and writes shell-safe request/expectation variables.
- `case_cli.py assert-status` compares a real connector HTTP status with the
  shared YAML case expectation.
- `runner_core.py` validates the minimal shared case schema and provides the
  status assertion used by the Apache harness.

The Apache PoC uses this runner so
`tests/common/cases/minimal/phase2_args_block.yaml` is the single source for
the rule, request, and expected HTTP status.

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

Example:

```sh
python3 tests/runners/case_cli.py materialize \
  --case tests/common/cases/minimal/phase2_args_block.yaml \
  --rules-file "$BUILD_ROOT/rules.conf" \
  --env-file "$BUILD_ROOT/case.env"

python3 tests/runners/case_cli.py assert-status \
  --case tests/common/cases/minimal/phase2_args_block.yaml \
  --actual-status 403
```
