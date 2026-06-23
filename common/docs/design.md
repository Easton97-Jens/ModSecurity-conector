# Common Design

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

The project records the full C vs C++ decision in
`docs/architecture/c-vs-cpp-decision.md`. In short: product connector cores stay C-first,
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
source `modules/ModSecurity-test-Framework/ci/common.sh`. Connector smokes must
use common.sh-managed paths or explicit environment variables such as
`ENVOY_BIN`, `TRAEFIK_BIN`, and `LIGHTTPD_BIN`. They must not install runtime
components globally or silently fall back to system `PATH`.

The lookup order is the explicit binary environment variable first, then local
common.sh-managed roots such as `$CONNECTOR_COMPONENT_CACHE`,
`$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
`$VERIFIED_RUN_ROOT`, and `$SOURCE_ROOT`. If a dependency is absent, the smoke
must write BLOCKED evidence and exit 77. Envoy and Traefik may set
`runtime_verified=true` only after `common/scripts/run_local_runtime_smoke.py`
proves real local HTTP 200/403 behavior through the resolved binary.

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
source only and remains runtime-blocked until a local build and integration mode
exist.

Envoy and Traefik also support an optional targeted libmodsecurity-backed smoke
by setting `DECISION_BACKEND=libmodsecurity` or using the connector-specific
Make shortcuts. This is a second evidence level on top of the simple
decision-service smoke. The shared runner loads
`common/rules/modsecurity_targeted_smoke.conf`, builds a local test evaluator
against local common.sh-managed libmodsecurity headers and libraries, and sends
`X-Modsec-Smoke: block` through the proxy auth path. Only this targeted mode may
set `modsecurity_backend_verified=true`, and only when the decision log shows
libmodsecurity loaded rule `1000001` and returned a 403 intervention. Missing
local libmodsecurity headers/libraries produce Exit 77/BLOCKED evidence with
`decision_backend=libmodsecurity` and `modsecurity_backend_verified=false`.

Official source metadata for these open connector runtime components is tracked
in `modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
The fixed versions, official source URLs, download URLs, and SHA256 values are
defined in `common.sh`; the manifest mirrors them for machine-readable
inventory. Downloads are disabled by default and are allowed only through
explicit `ALLOW_RUNTIME_DOWNLOADS=1` prepare targets with SHA256 verification
into `$CONNECTOR_COMPONENT_CACHE`.

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

Tracked in `docs/roadmap/todo-inventory.md`:

- common ownership rules for header and body buffers;
- future adapter API use of neutral status values;
- compile tests proving Common headers remain independent of every connector.
