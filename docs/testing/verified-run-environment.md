# Verified Run Environment

**Language:** English | [Deutsch](verified-run-environment.de.md)


Verified runs use a worker-compatible runtime root outside the source checkout
and outside `/root`.

`/root` is not a safe default for NGINX harness runtime data. On common Linux
runners `/root` is mode `0700`, while NGINX worker processes may run as
`nobody`. Even when generated files below the harness are readable, the worker
cannot traverse `/root`, so `htdocs/index.html` cannot be stated or read. In
that state `try_files $uri $uri/ /index.html` can turn a filesystem permission
problem into an HTTP 500 internal redirect cycle. The harness now preflights
worker access and reports:

```text
BLOCKED: nginx worker cannot access harness docroot
```

That status is environment evidence, not a connector runtime mismatch.

## Runtime Paths

The default root is:

```sh
VERIFIED_RUN_ROOT=${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified
```

Derived defaults:

```text
VERIFIED_STATE_ROOT=$VERIFIED_RUN_ROOT/state
VERIFIED_BUILD_ROOT=$VERIFIED_RUN_ROOT/build
VERIFIED_SOURCE_ROOT=$VERIFIED_RUN_ROOT/src
VERIFIED_TMP_ROOT=$VERIFIED_RUN_ROOT/tmp
VERIFIED_LOG_ROOT=$VERIFIED_RUN_ROOT/logs
VERIFIED_COMPONENT_CACHE=$VERIFIED_RUN_ROOT/component-cache
NGINX_HARNESS_PARENT=$VERIFIED_RUN_ROOT/nginx-harness
```

The compatibility variables `BUILD_ROOT`, `SOURCE_ROOT`, `TMP_ROOT`,
`LOG_ROOT`, and `CONNECTOR_COMPONENT_CACHE` default to those verified paths.
Runtime paths must not be in `/root`, the source checkout, or system locations
such as `/usr`, `/etc`, `/var/lib`, `/bin`, or `/sbin`. `/var/tmp/...` and
`${RUNNER_TEMP}/...` are valid runtime parents.

## Local Verified Run

```sh
export VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified
export VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=3600
make verified-runtime-producers
make verified-report-refresh
make verified-report-checks
```

For a cheaper local check:

```sh
export VERIFIED_RUN_ROOT=/var/tmp/ModSecurity-conector-verified
make verified-report-run-smoke
```

## CI Verified Run

CI jobs should use runner-owned temp storage:

```yaml
env:
  VERIFIED_RUN_ROOT: ${{ runner.temp }}/ModSecurity-conector-verified
  XDG_STATE_HOME: ${{ runner.temp }}/state
```

The repository keeps lightweight syntax/layout/report governance checks in CI.
Full verified runtime or full-matrix jobs should stay manual or explicitly
requested because they are expensive.

## Artifacts

Commit generated reports under `reports/testing/generated/` only when they were
refreshed from current verified inputs. Commit documentation and source changes
that define the workflow.

Do not commit runtime roots, component caches, build trees, temp directories,
logs, `verified-runs/` command logs, or source downloads from
`VERIFIED_RUN_ROOT`.

## Status Semantics

`PASS` means the checked input or command completed as required.

`WARN` means optional evidence or fallback validation is incomplete, but the run
can continue.

`FAIL` means a required check ran and produced a failing result.

`UNKNOWN` means no verified input was available to support a stronger claim.

`BLOCKED` means the run could not produce valid runtime evidence because a
precondition failed, such as an inaccessible NGINX docroot. BLOCKED data must
not be rewritten as PASS or runtime mismatch evidence.

## Helper Consolidation

| Duplicate Logic | Old Locations | New Helper | Behavior Changed? |
| --- | --- | --- | --- |
| Verified runtime path defaults and system-path checks | `Makefile`, `ci/run-verified-report-run.py`, `ci/run-full-matrix-job.py`, `ci/run-full-matrix-resume.py`, `ci/check-runtime-producer-readiness.py` | `ci/runtime_path_utils.py` and `modules/ModSecurity-test-Framework/ci/common.sh` | Defaults now use `VERIFIED_RUN_ROOT`; validation remains blocking for unsafe paths. |
| SHA256 file hashing | Verified manifest, full-matrix completeness, runtime mismatch generators | `ci/generated_report_utils.py` | No. |
| UTC generated timestamps | Verified manifest and full-matrix/mismatch generators | `ci/generated_report_utils.py` | No. |
| NGINX worker docroot access checks | Permission diagnostics in NGINX harness and later HTTP-500 analysis | `connectors/nginx/harness/run_nginx_smoke.sh` preflight records | Yes: inaccessible docroot now returns BLOCKED before NGINX request handling. |
