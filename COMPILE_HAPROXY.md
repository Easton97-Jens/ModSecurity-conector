# Compile HAProxy

## Purpose

This document describes the repository-supported HAProxy build, local runtime
smoke flow, and evidence paths. It is written for a clean clone: initialize the
framework submodule, build under `/src`, run smoke checks, and read generated
evidence from the build tree and reports.

## Current Connector Status

- Production path: `haproxy-modsecurity-spoa`, HAProxy SPOE/SPOP, and
  libmodsecurity.
- Default runtime smoke: `55/55 PASS`.
- Force-all runtime evidence: `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED /
  6 NOT_EXECUTABLE`.
- Implemented phases: request phases 1/2, implemented phase 3 response-header
  processing, and bounded phase 4 strict-abort evidence.
- Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence
  is documented as runtime evidence only.
- HAProxy reports are generated from runtime artifacts. There is no synthetic
  matrix writer.

## What This Builds

- A local HAProxy binary staged under `BUILD_ROOT`.
- The `haproxy-modsecurity-spoa` production SPOA runtime.
- A local libmodsecurity binding self-test binary.
- Runtime directories, logs, `decision.jsonl`, audit logs, and JSON summaries
  under `BUILD_ROOT`.

## What Not Prove

- It does not install HAProxy or libmodsecurity into the operating system.
- It does not make RESPONSE_BODY a promoted connector capability.
- It does not claim every force-all row is production-ready.
- It does not replace the generated coverage reports as the source of truth.

## Repository Layout

- `connectors/haproxy/` contains HAProxy connector source and local Makefile
  targets.
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` builds the
  production SPOA/SPOP runtime binary.
- `connectors/haproxy/harness/run_haproxy_smoke.sh` runs live HAProxy runtime
  evidence.
- `examples/haproxy/` contains production-style HAProxy, SPOE, and agent
  configuration examples.
- `modules/ModSecurity-test-Framework/` owns shared runtime generation,
  snapshots, and matrix reporting.

## Prerequisites

- `git`, `make`, `cc`, `c++`, `curl`, `tar`, `sha256sum`, `python3`, and
  `curl` for runtime probes.
- A checkout path that can read the framework submodule.
- Writable `/src` for default source and build roots.

## Required Submodules

Initialize the framework before building:

```bash
git submodule update --init --recursive
```

The supported source pins for HAProxy, CRS, and ModSecurity live in
`modules/ModSecurity-test-Framework/ci/common.sh`. Update that file first when
a pin changes.

## Build Variables

Supported variables are variables read by the top-level Makefile, HAProxy
Makefile, framework helpers, harness scripts, or checked-in example configs.
Unsupported or historical aliases are listed separately below the table.

## Full Variable Reference Table

| Variable | Required | Default | Example | Used by | Meaning | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `SOURCE_ROOT` | No | `/src` | `/src` | top-level Makefile, `prepare-haproxy-runtime.sh` | Source checkout/download root for generated dependency sources. | Must stay under `/src`. |
| `BUILD_ROOT` | No | `/src/ModSecurity-conector-build` | `/src/ModSecurity-conector-build` | top-level Makefile, HAProxy Makefile, harness, framework helpers | Build, runtime, log, and result root. | Must stay under `/src`; not inside the connector checkout. |
| `FRAMEWORK_ROOT` | No | `$(CURDIR)/modules/ModSecurity-test-Framework` | `/work/repo/modules/ModSecurity-test-Framework` | top-level Makefile, harness, framework helpers | Location of the shared test framework. | Required only when the framework is outside the default submodule path. |
| `CONNECTOR_ROOT` | No | current repository root | `/work/ModSecurity-conector` | framework helpers and harness | Location of this connector repository. | Exported by the top-level Makefile. |
| `TMP_ROOT` | No | `$BUILD_ROOT/tmp` | `/src/ModSecurity-conector-build/tmp` | harness and framework helpers | Temporary runtime files. | Must stay under `BUILD_ROOT`. |
| `LOG_ROOT` | No | `$BUILD_ROOT/logs` | `/src/ModSecurity-conector-build/logs` | harness and framework helpers | Log root. | Per-run logs are created under this directory. |
| `LOG_DIR` | No | `$LOG_ROOT/haproxy-runtime` | `/src/ModSecurity-conector-build/logs/haproxy-runtime` | harness and prepare helper | Current HAProxy run log directory. | Must stay under `BUILD_ROOT`. |
| `RESULTS_DIR` | No | `$BUILD_ROOT/results` or `$BUILD_ROOT/results/force-all` | `/src/ModSecurity-conector-build/results/with-crs` | harness and matrix runner | Destination for JSONL and summary evidence. | Matrix variant runners override this for `no-crs`, `with-crs`, and force-all runs. |
| `RUNTIME_BASE` | No | `$BUILD_ROOT/haproxy-runtime-cases` | `/src/ModSecurity-conector-build/haproxy-runtime-cases` | harness | Per-case runtime root parent. | The harness creates one runtime directory per case. |
| `RUNTIME_ROOT` | No | empty | `/src/ModSecurity-conector-build/haproxy-runtime-cases/case` | harness | Explicit runtime directory for one run. | Usually left empty. |
| `PYTHON` | No | `python3` or `.venv/bin/python` | `.venv/bin/python` | top-level Makefile and harness | Python interpreter. | Exported as `PYTHON`; harness stores it as `PYTHON_BIN`. |
| `PYTHONDONTWRITEBYTECODE` | No | `1` | `1` | top-level Makefile and harness | Avoids writing Python bytecode in the checkout. | Keep enabled for clean working trees. |
| `REFRESH` | No | unset / `0` | `REFRESH=1` | prepare helpers | Re-downloads or rebuilds generated dependencies. | Safe removal is restricted to generated roots. |
| `MAKE_JOBS` | No | framework default CPU count | `8` | `prepare-haproxy-runtime.sh` | Parallelism for building HAProxy. | Used only by the HAProxy source build helper. |
| `HAPROXY_VERSION` | No | from framework `common.sh` | `3.2.19` | top-level Makefile, `prepare-haproxy-runtime.sh` | HAProxy upstream version. | Keep with URL and checksum in `common.sh`. |
| `HAPROXY_SOURCE_URL` | No | from framework `common.sh` | `https://www.haproxy.org/download/3.2/src/haproxy-3.2.19.tar.gz` | `prepare-haproxy-runtime.sh` | HAProxy source archive URL. | Checksum is verified before extraction. |
| `HAPROXY_SHA256_URL` | No | `$HAPROXY_SOURCE_URL.sha256` | `https://www.haproxy.org/.../haproxy-3.2.19.tar.gz.sha256` | `prepare-haproxy-runtime.sh` | Official checksum URL. | Must name the archive. |
| `HAPROXY_SHA256` | No | from framework `common.sh` | `b08ebbd57f575012e4a5eb5b772721531fbacf6913ffd334f0281736a1ad78b6` | `prepare-haproxy-runtime.sh` | Expected HAProxy archive digest. | Source download is blocked on mismatch. |
| `HAPROXY_SOURCE_ROOT` | No | `$SOURCE_ROOT/haproxy` | `/src/haproxy` | `prepare-haproxy-runtime.sh` | Root for HAProxy downloads and extracted source. | Must stay under `SOURCE_ROOT`. |
| `HAPROXY_DOWNLOAD_DIR` | No | `$HAPROXY_SOURCE_ROOT/downloads` | `/src/haproxy/downloads` | `prepare-haproxy-runtime.sh` | HAProxy archive and checksum cache. | Must stay under `SOURCE_ROOT`. |
| `HAPROXY_SOURCE_DIR` | No | `$HAPROXY_SOURCE_ROOT/haproxy-$HAPROXY_VERSION` | `/src/haproxy/haproxy-3.2.19` | `prepare-haproxy-runtime.sh` | Extracted HAProxy source tree. | Must stay under `SOURCE_ROOT`. |
| `HAPROXY_RUNTIME_BUILD_DIR` | No | `$BUILD_ROOT/haproxy-runtime-build` | `/src/ModSecurity-conector-build/haproxy-runtime-build` | `prepare-haproxy-runtime.sh` | HAProxy build workspace root. | Must stay under `BUILD_ROOT`. |
| `HAPROXY_RUNTIME_BUILD_WORKTREE` | No | `$HAPROXY_RUNTIME_BUILD_DIR/worktree` | `/src/ModSecurity-conector-build/haproxy-runtime-build/worktree` | `prepare-haproxy-runtime.sh` | Copied HAProxy source used for compilation. | Recreated by the helper. |
| `HAPROXY_RUNTIME_DIR` | No | `$BUILD_ROOT/haproxy-runtime/haproxy` | `/src/ModSecurity-conector-build/haproxy-runtime/haproxy` | `prepare-haproxy-runtime.sh` | Staged HAProxy runtime directory. | Contains `sbin/haproxy`. |
| `HAPROXY_BIN` | No | `$HAPROXY_RUNTIME_DIR/sbin/haproxy` | `/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy` | top-level Makefile, harness, prepare helper | HAProxy executable used by runtime tests. | The helper stages this binary when missing or `REFRESH=1`. |
| `HAPROXY_BUILD_DIR` | No | `$BUILD_ROOT/haproxy-build-starter` | `/src/ModSecurity-conector-build/haproxy-build-starter` | `connectors/haproxy/Makefile` | Starter metadata build directory. | Local-only generated output. |
| `HAPROXY_SPOA_RUNTIME_DIR` | No | `$BUILD_ROOT/haproxy-spoa-runtime` | `/src/ModSecurity-conector-build/haproxy-spoa-runtime` | `connectors/haproxy/Makefile` | Directory for `haproxy-modsecurity-spoa`. | Contains runtime object files and binary. |
| `HAPROXY_MODSECURITY_BINDING_DIR` | No | `$BUILD_ROOT/haproxy-modsecurity-binding` | `/src/ModSecurity-conector-build/haproxy-modsecurity-binding` | `connectors/haproxy/Makefile` | Directory for binding self-test and `paths.env`. | Distinct from harness `MODSECURITY_BINDING_DIR`. |
| `SPOA_RUNTIME_BIN` | No | `$BUILD_ROOT/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | harness and HAProxy Makefile | SPOA runtime executable. | This is the production SPOA binary path used in runtime smoke. |
| `MODSECURITY_BINDING_DIR` | No | `$BUILD_ROOT/haproxy-modsecurity-binding` | `/src/ModSecurity-conector-build/haproxy-modsecurity-binding` | harness | Local libmodsecurity binding directory. | Must contain `paths.env` after build. |
| `MODSECURITY_INCLUDE_CANDIDATES` | No | build output and `/src/ModSecurity_V3/headers` candidates | `/src/ModSecurity_V3/headers` | `connectors/haproxy/Makefile` | Header search locations for libmodsecurity. | Space-separated list. |
| `MODSECURITY_LIB_CANDIDATES` | No | build output and ModSecurity `.libs` candidates | `/src/ModSecurity_V3/src/.libs` | `connectors/haproxy/Makefile` | Library search locations for libmodsecurity. | Space-separated list. |
| `MODSECURITY_RULE_PREAMBLE_FILE` | No | empty, or `$BUILD_ROOT/crs/modsecurity-crs-preamble.conf` for with-CRS matrix | `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf` | matrix runner, harness, binding CRS self-test | Rule preamble used for CRS runs. | Created by `prepare-crs.sh` when needed. |
| `MODSECURITY_TEST_VARIANT` | No | `no-crs` | `with-crs` | matrix runner and harness | Selects no-CRS or with-CRS runtime behavior. | Usually set by `test-haproxy-no-crs` and `test-haproxy-with-crs`. |
| `HAPROXY_MATRIX_VARIANT` | No | `all` | `with-crs` | `run-haproxy-runtime-matrix.sh` | Matrix variant selector. | Supports `all`, `no-crs`, and `with-crs`. |
| `FORCE_ALL_CASES` | No | `0` | `FORCE_ALL_CASES=1` | top-level Makefile, matrix runner, harness | Attempts force-all evidence rows. | Force-all evidence is reported separately from default smoke. |
| `SMOKE_CASES` | No | empty | `phase1_header_block,crs_sqli_anomaly_block` | top-level Makefile and harness | Comma-separated selected cases. | Empty means the harness uses its default scope. |
| `TEST_CASE` | No | empty | `tests/cases/request/headers/phase1_header_block.yaml` | harness | Runs one framework case. | Resolved by the shared case CLI. |
| `CASE_SCOPE` | No | `all` | `runtime` | top-level Makefile and harness | Case selection scope for the shared case CLI. | `smoke-haproxy` sets `CASE_SCOPE=all`. |
| `RUN_ONE_CASE` | No | `0` | `1` | harness | Internal single-case mode. | Usually set by harness flow, not by users. |
| `PORT` | No | `18082` | `19082` | harness | Base HAProxy listener port. | Harness searches for a free port from this base. |
| `PORT_SEARCH_LIMIT` | No | `100` | `20` | harness | Number of ports to scan. | Blocks if no free port is found. |
| `PORT_RETRY_LIMIT` | No | `1` | `3` | harness | Retry count for port-related run setup. | Usually left as default. |
| `CURL` | No | first `curl` in `PATH` | `/usr/bin/curl` | harness | HTTP client used for probes. | Blocks when no curl is available. |

Unsupported or legacy aliases: `HAPROXY_BINARY`, `HAPROXY_CONFIG`,
`HAPROXY_MODSECURITY_CONF`, `HAPROXY_SPOE_CONF`, `HAPROXY_LOG_DIR`,
`HAPROXY_DECISION_LOG`, `HAPROXY_AUDIT_LOG`, `HAPROXY_REQUEST_BODY_LIMIT`,
and `HAPROXY_RESPONSE_BODY_TIMEOUT` are not environment variables consumed by
the current Makefiles or harness scripts. Use the supported variables above,
or edit `examples/haproxy/modsecurity-agent.conf` and the HAProxy/SPOE example
files when configuring a production-style deployment.

## Minimal Local Build

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
```

`build-spoa-runtime` produces
`/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa`
by default.

## Rebuild / Refresh

Use `REFRESH=1` when generated dependency directories should be recreated:

```bash
REFRESH=1 make smoke-haproxy
REFRESH=1 make runtime-matrix-haproxy
```

The cleanup logic refuses to remove paths outside `SOURCE_ROOT` and
`BUILD_ROOT`.

## Manual Build Flow

```bash
make smoke-haproxy
make test-haproxy-no-crs
make test-haproxy-with-crs
make runtime-matrix-haproxy
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
```

The matrix helper prepares HAProxy, prepares CRS for with-CRS runs, runs the
same harness used by `make smoke-haproxy`, updates the runtime snapshot, and
then report generation consumes that snapshot.

## Production-Style Install / Deploy

The example deployment path is:

- HAProxy loads `examples/haproxy/spoe-modsecurity.conf` through
  `filter spoe engine modsecurity`.
- HAProxy connects to the SPOA service over SPOP.
- The SPOA service runs `haproxy-modsecurity-spoa`.
- `haproxy-modsecurity-spoa` loads libmodsecurity and a rules file.
- Decisions are written to `decision.jsonl`.
- Audit events are written through the configured audit log path.

Example production-style paths:

- `/usr/local/sbin/haproxy-modsecurity-spoa`
- `/etc/haproxy/haproxy.cfg`
- `/etc/haproxy/spoe-modsecurity.conf`
- `/etc/haproxy/modsecurity-agent.conf`
- `/etc/modsecurity/haproxy-rules.conf`
- `/var/log/haproxy-modsecurity/decision.jsonl`
- `/var/log/haproxy-modsecurity/audit.log`

Changing HAProxy, SPOE, or agent configuration requires reloading HAProxy and
restarting the SPOA process.

## Test / Smoke Validation

```bash
make smoke-haproxy
make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

Expected current generated counts:

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default HAProxy smoke | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all | 133 | 104 | 23 | 0 | 6 |

Default smoke excludes former-XFAIL force-all rows. Force-all rows remain
runtime evidence and stay in the HAProxy detail report.

## Runtime Evidence Paths

- `/src/ModSecurity-conector-build/results/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/haproxy-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime/decision.jsonl`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime/audit.log`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

## Generated Artifacts

Generated Markdown reports are not edited by hand. Update the generator or
runtime snapshot flow, then run:

```bash
make generate-test-matrix
make check-test-matrix
```

## Logs

- HAProxy stderr: per-case `haproxy.stderr.log`.
- SPOA runtime log: per-case `spoa-agent.log`.
- Decision evidence: per-case and aggregate `decision.jsonl`.
- Audit evidence: `audit.log` and configured audit directories.
- Prepare logs: `$BUILD_ROOT/logs/haproxy-prepare`.

## Troubleshooting

- `BLOCKED: libmodsecurity headers missing`: build Apache or NGINX
  libmodsecurity first, or set `MODSECURITY_INCLUDE_CANDIDATES` and
  `MODSECURITY_LIB_CANDIDATES`.
- `BLOCKED: CRS preamble missing`: run a with-CRS target so
  `prepare-crs.sh` creates the preamble, or set `MODSECURITY_RULE_PREAMBLE_FILE`.
- `no free localhost port found`: set `PORT` or increase
  `PORT_SEARCH_LIMIT`.
- Wrong counts in root reports: regenerate from the generator flow instead of
  editing Markdown by hand.

## Common Failures

- Missing submodule: run `git submodule update --init --recursive`.
- Missing `/src` write access: set `SOURCE_ROOT` and `BUILD_ROOT` to writable
  paths under `/src`.
- Runtime binary missing: run `make -C connectors/haproxy build-spoa-runtime`.
- HAProxy binary missing: run `make smoke-haproxy` or set `HAPROXY_BIN`.

## Cleanup

```bash
make -C connectors/haproxy clean
rm -rf /src/ModSecurity-conector-build/haproxy-runtime-cases
rm -rf /src/ModSecurity-conector-build/results/no-crs
rm -rf /src/ModSecurity-conector-build/results/with-crs
rm -rf /src/ModSecurity-conector-build/results/force-all
```

Avoid deleting `/src/ModSecurity-conector-build` while another connector build
is using it.

## Best Practices

- Keep source pins in `modules/ModSecurity-test-Framework/ci/common.sh`.
- Keep production examples under `examples/haproxy/`.
- Keep root summaries connector-neutral and use generated detail reports for
  row-level HAProxy evidence.
- Preserve decision and audit logs when comparing runtime behavior.
- Treat bounded Phase 4 strict-abort evidence as runtime evidence only.

## Related Docs / Examples

- `examples/haproxy/README.md`
- `reports/testing/haproxy-poc.md`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
