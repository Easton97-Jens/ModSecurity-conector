# HAProxy Build

Status: production SPOA runtime build available

The complete repository-supported HAProxy compile and local verification flow
is documented in the root guide:

- [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md)

## Current Build Path

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
make smoke-haproxy
```

The production SPOA binary is staged at:

```text
/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa
```

The HAProxy binary is prepared under:

```text
/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy
```

## Current Runtime Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default HAProxy smoke | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all | 133 | 104 | 23 | 0 | 6 |

Evidence is summarized in:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` strict-abort sample is disabled, legacy, and
noncanonical; it is not current runtime evidence.

## Full-lifecycle-selected native HTX transport build

The full-lifecycle profile selects this separate observer-mode path through
`full-lifecycle-haproxy-htx`. It builds a disposable, patched HAProxy 3.2.21
worktree and does not replace the SPOE/SPOP binary:

```sh
HAPROXY_HTX_SOURCE_DIR=/absolute/path/to/haproxy-3.2.21 \
  MODSECURITY_INCLUDE_DIR=/absolute/path/to/include \
  MODSECURITY_LIB_DIR=/absolute/path/to/lib \
  BUILD_ROOT=/var/tmp/haproxy-htx-smoke \
  make -C connectors/haproxy runtime-smoke-haproxy-htx
```

The target checks the source version, applies the patch only in the disposable
worktree, writes overlay/binary SHA-256 provenance, validates a generated
`filter modsecurity-htx` configuration, and starts HAProxy against a local
upstream. It records real P1–P4 libmodsecurity observations without buffering
bodies, but is explicitly `observer_nonpromoted`: no client-visible deny,
redirect, abort, Common-runtime bridge, or selected-path capability is claimed.
Use a fresh `BUILD_ROOT`; the overlay builder refuses to reuse a worktree.
