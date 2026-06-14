# NGINX Validation

Status: evidence-scoped

NGINX runtime claims require a concrete smoke or matrix command and generated
evidence. A successful build alone is not a runtime pass.

## Commands

```bash
git submodule update --init --recursive
make smoke-nginx
make generate-test-matrix
make check-test-matrix
FORCE_ALL_CASES=1 make runtime-matrix-all
```

## Current Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default NGINX smoke | 60 | 60 | 0 | 0 | 0 |
| NGINX force-all | 140 | 95 | 39 | 0 | 6 |

Executable YAML cases are owned by the framework module:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Generated evidence is recorded in:

- `reports/testing/generated/nginx-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`
- `reports/testing/test-coverage-overview.md`

## Not Claimed

- No broad NGINX regression-suite pass is claimed without a matching runtime
  command and generated result.
- Force-all FAIL rows are not hidden by the default smoke summary.
- Full RESPONSE_BODY support is not promoted.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
