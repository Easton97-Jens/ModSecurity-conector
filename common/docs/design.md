# Common Design

**Language:** English | [Deutsch](design.de.md)

Status: scaffolded

## Boundary

`common/` is connector-neutral. It may define request, response, transaction,
intervention, status, origin, logging, and capability types that can be used by
tests and connector adapters, but it must not include or depend on any
server/proxy SDK.

## C-first interface

The shared headers are C-first because the locally analyzed Apache and NGINX
connectors call libmodsecurity through its C API. The C++ headers are thin
aliases over the C structs, not a separate ownership model.

This does not implement a complete connector API. It defines neutral data shapes
that later connector adapters can translate to libmodsecurity v3 calls.

The project records the C-vs-C++ decision in the
[architecture guide](../../docs/architecture.md). In short: product connector cores stay C-first,
C++ remains limited to thin wrappers, build/test utilities, and optional helper
programs, and C++ objects must not cross Apache, NGINX, or future server ABI
boundaries.

## Phase 1 foundation

The first controlled refactor phase adds only small connector-neutral data
shapes:

- `intervention.h` represents the data returned from an intervention check, but
  does not decide how a server sends the response.
- `status.h` defines generic operation outcomes, not HTTP status codes.
- `origin.h` records source/version/license metadata and does not imply code
  ownership or import status.

Existing `request.h`, `response.h`, `transaction.h`, `logging.h`, and
`capabilities.h` remain connector-neutral. `capabilities.h` is the canonical
capability header; no duplicate `capability.h` is introduced.

`transaction.h` also owns the small `msconnector_decision` shape used by open
connector adapters to return neutral status, intervention, rule ID, and reason
data without creating connector-local Result types.

## Runtime-smoke evidence helpers

Connector-neutral smoke result helpers live under `common/scripts/`, not the
public C headers. They centralize Result/Evidence JSON writing for open
connector harnesses while keeping the runtime ABI focused on request, response,
intervention, status, logging, capabilities, origin, transaction, and decision
data.

These helpers may write common smoke artifacts such as `result.json`,
`summary.json`, `summary.txt`, and `results.jsonl`. They must not include
server-specific terms or depend on Envoy, Traefik, lighttpd, Apache, HAProxy, or
Nginx SDKs.

Runtime dependency discovery belongs to the test-framework shell helpers that
source `modules/ModSecurity-test-Framework/ci/lib/common.sh`. Connector smokes must
use common.sh-managed paths or explicit environment variables such as
`ENVOY_BIN`, `TRAEFIK_BIN`, and `LIGHTTPD_BIN`. They must not install runtime
components globally or silently fall back to system `PATH`.

The lookup order is the explicit binary environment variable first, then local
common.sh-managed roots such as `$CONNECTOR_COMPONENT_CACHE`,
`$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
`$VERIFIED_RUN_ROOT`, and `$SOURCE_ROOT`. If a dependency is absent, the smoke
must write BLOCKED evidence and exit 77. Envoy, Traefik, and lighttpd may set
`runtime_verified=true` only after `common/scripts/run_local_runtime_smoke.py`
proves real local HTTP 200/403 behavior through the resolved binary and the
selected integration mode.

`common.sh` also owns the open-connector component defaults: `ENVOY_*`,
`TRAEFIK_*`, and `LIGHTTPD_*` component roots, runtime roots, config roots, log
roots, result roots, binary defaults, smoke ports, upstream/authz ports, and
integration-mode defaults. It defines these values only; it does not create
directories, validate runtimes, download artifacts, or install dependencies.

Local component staging is handled by explicit prepare scripts:
`prepare-envoy-runtime.sh`, `prepare-traefik-runtime.sh`, and
`prepare-lighttpd-runtime.sh`. Without `ALLOW_RUNTIME_DOWNLOADS=1`, these
scripts report an existing local binary when present and otherwise exit 77
without downloading. With explicit opt-in they download only the pinned
component artifact, verify the `common.sh` SHA256 before staging, and write only
under `$CONNECTOR_COMPONENT_CACHE`. Envoy stages a direct binary; Traefik
extracts only the expected `traefik` binary from its tarball; lighttpd stages
verified source and supports an explicit `ALLOW_RUNTIME_BUILDS=1` local build
under `$CONNECTOR_COMPONENT_CACHE/lighttpd`. Lighttpd Phase 1 uses
`integration_mode=sidecar_proxy`: the smoke starts a local lighttpd upstream and
a local sidecar decision proxy before setting runtime evidence.

Envoy, Traefik, and lighttpd also support an optional targeted
libmodsecurity-backed smoke by setting `DECISION_BACKEND=libmodsecurity` or
using the connector-specific Make shortcuts. This is a second evidence level on
top of the simple decision-service smoke. The shared runner loads
`common/rules/modsecurity_targeted_smoke.conf`, builds a local test evaluator
against local common.sh-managed libmodsecurity headers and libraries, and sends
`X-Modsec-Smoke: block` through the proxy auth path. Only this targeted mode may
set `modsecurity_backend_verified=true`, and only when the decision log shows
libmodsecurity loaded rule `1000001` and returned a 403 intervention. Missing
local libmodsecurity headers/libraries produce Exit 77/BLOCKED evidence with
`decision_backend=libmodsecurity` and `modsecurity_backend_verified=false`.
The resolver is shared in `connector-smoke-common.sh`; it accepts only explicit
local overrides or common.sh-managed external runtime/component roots, and
rejects system/PATH fallbacks for libmodsecurity. The exact invocation root is
recorded as run metadata rather than documented as a developer-local path.

The same open-connector runner also supports minimal and secondary CRS smokes
with `DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs` or the
connector-specific CRS Make targets.
CRS source-of-truth remains in `common.sh`: `CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR`, and `CRS_RUNTIME_DIR`. The runner may resolve an already
staged CRS checkout only from common.sh-managed verified external roots; it
does not download CRS, install CRS globally, or search system paths. The
generated smoke config is written under
the connector runtime/result root as `crs-smoke/` for the minimal case and
`crs-secondary-smoke/` for the secondary case.

The minimal CRS smoke reuses the existing `crs_sqli_anomaly_block` payload,
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`. A PASS requires an
allowed request with HTTP 200, a CRS-backed blocked request with HTTP 403, and
an observed CRS rule ID/message from libmodsecurity intervention evidence. Only
that evidence may set `crs_minimal_smoke_verified=true`. It must not set
`crs_complete=true`, `production_ready=true`, `full_matrix_ready=true`, or
`response_body_verified=true`. CRS runs write `crs-result.json` and
`crs-decision.log`; targeted libmodsecurity runs keep `targeted-result.json`
and `modsecurity-decision.log`.

The secondary CRS smoke reuses the same CRS resolver and runner, selected with
`CRS_SMOKE_CASE=secondary` or the `smoke-envoy-crs-secondary`,
`smoke-traefik-crs-secondary`, `smoke-lighttpd-crs-secondary`, and
`smoke-open-connectors-crs-secondary` Make targets. It sends
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E` and must extract the observed CRS
rule ID/message from libmodsecurity audit/intervention evidence. A successful
secondary run may set `crs_secondary_smoke_verified=true` and writes
`crs-secondary-result.json`, `crs-secondary-decision.log`, and
`crs-secondary-audit.log`. If CRS, libmodsecurity, and the runtime are present
but the secondary probe is not blocked, the result is FAIL. Missing CRS,
missing libmodsecurity, or missing runtime dependencies remain Exit 77/BLOCKED
evidence.

Official source metadata for these open connector runtime components is tracked
in `modules/ModSecurity-test-Framework/ci/provisioning/runtime-components.manifest.json`.
The fixed versions, official source URLs, download URLs, and SHA256 values are
defined in `common.sh`; the manifest mirrors them for machine-readable
inventory. Downloads are disabled by default and are allowed only through
explicit `ALLOW_RUNTIME_DOWNLOADS=1` prepare targets with SHA256 verification
into `$CONNECTOR_COMPONENT_CACHE`.

The manual GitHub Actions workflow
`.github/workflows/open-connectors-smoke.yml` first runs the existing
`prepare-runtime-components` target to stage shared local libmodsecurity and CRS
inputs under common.sh-managed roots, then prepares Envoy, Traefik, and Lighttpd
runtime components before running simple runtime, targeted libmodsecurity,
minimal CRS, and secondary CRS smokes with `TMPDIR=/tmp`. It copies
`/tmp/ModSecurity-conector-verified/` into `ci-artifacts/open-connectors/` and
uploads that directory as `open-connectors-smoke-evidence`, including after
prepare or smoke failures. The temporary narrow `push` trigger on the workflow
file is a diagnosis aid only. The workflow artifact is evidence only; it does
not promote production readiness, full-matrix readiness, CRS completeness, or
response-body support.

## libmodsecurity v3 alignment

The phase names mirror the public v3 transaction sequence:

- connection metadata
- URI
- request headers
- request body
- response headers
- response body
- logging

The actual calls to libmodsecurity belong in connector adapters or a future
engine-facing layer with explicit ownership rules. They are not hidden in
`common/` until their lifetime, error, and cleanup contracts are documented.

## Open Work

Open work is bounded by the repository
[operations and security guide](../../docs/operations-and-security.md):

- common ownership rules for header and body buffers;
- future adapter API use of neutral status values;
- compile tests proving Common headers remain independent of every connector.
