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
- NGINX module registration and body/header filters.
- Server-specific configuration parsing.
- Request/response body ownership and buffering.
- libmodsecurity transaction lifetime.
- `RESPONSE_BODY` blocking behavior.

## Risks

- C and Python metadata names can drift. `ci/check-common-helpers.sh`,
  `make lint`, and summary schema checks are the current guardrails.
- A future connector may need additional capability names; those should be
  added append-only and mirrored in the Python model.
- The Common helpers are not product connector code yet. Any production use must
  be introduced with separate smoke evidence.
