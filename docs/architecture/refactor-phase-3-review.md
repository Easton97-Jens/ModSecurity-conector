# Refactor Phase 3 Review

Status: implemented

## Extracted

Phase 3 extracted only connector-neutral helper logic:

| Area | Common helper | Reason |
| --- | --- | --- |
| Status metadata | `common/src/status.c` | Maps runtime result words to `msconnector_status` names |
| Intervention metadata | `common/src/intervention.c` | Builds the neutral intervention data shape |
| Origin metadata | `common/src/origin.c` | Represents provenance without connector ownership |
| Capability descriptors | `common/src/capabilities.c` | Names and composes connector-neutral capability flags |

The Python harness layer mirrors those concepts in
`tests/runners/msconnector_models.py`; it does not use FFI, `ctypes`, or a C
bridge binary.

## Deferred

The following candidates remain connector-specific:

- Apache hook registration and filters.
- Apache bucket/error helpers, including `send_error_bucket()`.
- NGINX module registration and body/header filters.
- NGINX request string conversion, PCRE pool helpers, and log callback.
- Server-specific configuration parsing.
- Request/response body ownership and buffering.
- libmodsecurity transaction lifetime.
- `RESPONSE_BODY` blocking behavior.

Phase 5 confirmed that these are not safe second replace-and-reduce candidates.
Even when a helper is small, it is embedded in config, request/response,
lifecycle, audit, or Apache bucket behavior. Future work should first introduce
repo-owned adapter code around one narrow behavior, then prove equivalence with
real-world Apache and NGINX smoke runs.

## Risks

- C and Python metadata names can drift. `ci/check-common-helpers.sh`,
  `make lint`, and summary schema checks are the current guardrails.
- A future connector may need additional capability names; those should be
  added append-only and mirrored in the Python model.
- The Common helpers are not product connector code yet. Any production use must
  be introduced with separate smoke evidence.
- Phase 6 added adapter-owned metadata skeletons outside `common/`. Those files
  may name Apache or NGINX as components, but they still avoid server headers,
  libmodsecurity ownership, and productive runtime paths.
