# HAProxy Connector Origin

Status: live-yaml-spoa-runtime (partial)
Runtime status: live request-side YAML execution through HAProxy, SPOA/SPOP,
and libmodsecurity.

No upstream HAProxy connector source has been imported into this repository.
No HAProxy source tree, HAProxy headers, or SPOE/SPOA protocol library is
vendored under `connectors/haproxy`. The repo-authored libmodsecurity binding
source is used by the local SPOP runtime for live request-side framework YAML
execution; it is not a productive HAProxy runtime adapter.

## Native HTX transport smoke for the full-lifecycle profile

The repository does not vendor HAProxy source. `htx-overlay/` instead copies a
repo-authored filter, binding sources, and a narrow Makefile patch into an
isolated, version-checked HAProxy 3.2.21 worktree. The separate
`full-lifecycle-haproxy-htx` profile selects this connector-local smoke. It
validates `filter modsecurity-htx`, loads canonical No-CRS rules, and exercises
P1–P4 through real HAProxy. P1/P3 native deny decisions are converted into
client-visible replies (403 and the canonical P1 429 alternative); P2/P4 are
kept observation-only. It does not implement redirect or post-commit abort,
does not alter the SPOP compatibility claims, and does not promote a lifecycle
capability.

The selected profile records a real-host native precommit route, not an
alternate SPOP deployment. The standard SPOP compatibility path remains
separate; no HTX host record may be reused as SPOP enforcement, safe/strict
late-action, or full-response-body evidence.

## Current Source Provenance

| Path | Origin | License status | Notes |
| --- | --- | --- | --- |
| `connectors/haproxy/metadata.c` | repo-authored starter metadata | not selected | Does not implement HAProxy API, SPOE/SPOA protocol, or libmodsecurity calls. |
| `connectors/haproxy/metadata.h` | repo-authored starter metadata | not selected | Declares metadata accessors only. |
| `connectors/haproxy/Makefile` | repo-authored starter build file | not selected | Compiles metadata and local starter binaries only. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | repo-authored SPOA agent starter | not selected | Local synthetic request-decision logic only; no SPOP parser or HAProxy runtime. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | repo-authored SPOA agent starter | not selected | Local starter declarations only. |
| `connectors/haproxy/src/haproxy_spoa_main.c` | repo-authored SPOA agent starter CLI | not selected | Supports `--describe` and `--self-test` only. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | repo-authored SPOP runtime | not selected | Parses live HAProxy request-side SPOE arguments, feeds libmodsecurity, and returns set-var ACKs for 403 disruptive decisions; not a full SPOA agent implementation. |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | repo-authored ModSecurity binding | not selected | Uses locally verified libmodsecurity C API signatures for materialized rules, URI, headers, request body bytes, and CRS SQLi decisions. |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | repo-authored ModSecurity binding | not selected | Declares the request/evaluation shape used by the binding self-test and SPOP runtime. |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | repo-authored ModSecurity binding self-test CLI | not selected | Supports `--describe` and `--self-test`; live HAProxy runtime enforcement is handled by the framework smoke harness. |
| `connectors/haproxy/htx-overlay/` | repo-authored HAProxy 3.2.21 overlay source and build patch | selected only by the non-promoted full-lifecycle profile | Copied into a disposable verified HAProxy source worktree; native P1/P3 deny replies are exercised with real host traffic, while P2/P4 remain observation-only. |
| `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` | repo-authored native HTX transport smoke | selected only by the non-promoted full-lifecycle profile | Builds/starts a patched HAProxy, loads canonical No-CRS rules, and records real P1/P3 status replies plus payload-free P2/P4 observations without capability promotion. |
| `connectors/haproxy/docs/` | repo-authored documentation | not selected | Documents open HAProxy integration options and blockers. |
| `connectors/haproxy/harness/README.md` | repo-authored documentation | not selected | Harness contract only. |

## Upstream Selection

- HAProxy upstream source: not selected.
- HAProxy integration API/header set: not selected.
- SPOE/SPOA protocol dependency: not selected.
- SPOP frame implementation: request-side runtime subset only.
- ModSecurity/libmodsecurity binding for HAProxy: live enforcement verified for
  shared request-side YAML cases in No-CRS and With-CRS runs.
- Imported productive source files: none.

## Evidence Boundary

The current starter/runtime proves that metadata and local binaries can be
compiled, that the SPOA starter can run a local synthetic request-decision
self-test, and that `make smoke-haproxy` can execute shared request-side YAML
cases through live HAProxy, the SPOP runtime, and libmodsecurity. Current
evidence covers `REQUEST_URI`, `REQUEST_HEADERS`, `REQUEST_HEADERS_NAMES`,
`ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`, `REQUEST_COOKIES_NAMES`,
`REQUEST_BODY`, `FILES`, `XML`, and the CRS SQLi anomaly case. It does not
prove a productive HAProxy adapter build, full SPOE/SPOA protocol completeness,
canonical selected-path response-phase enforcement, audit-log assertions,
non-403 disruptive status mapping, redirects, or `RESPONSE_BODY` blocking.
