# Refactor Phase 6 Review

Status: implemented

Phase 6 introduces adapter-owned source skeletons only. It does not replace any
productive Apache or NGINX connector path.

## Added

| Area | Files | Reason |
| --- | --- | --- |
| Apache adapter metadata | `connectors/apache/metadata.h`, `connectors/apache/metadata.c` | Stable repo-owned descriptor for the Apache connector source and license origin |
| NGINX adapter metadata | `connectors/nginx/metadata.h`, `connectors/nginx/metadata.c` | Stable repo-owned descriptor for the NGINX connector source and license origin |
| Adapter helper validation | `ci/check-adapter-helpers.sh` | Compiles adapter metadata under `$BUILD_ROOT` and checks required fields |
| Lint integration | `Makefile` | Runs the adapter helper smoke as part of `make lint` |

After Phase 13, adapter metadata lives at the connector roots while
`connectors/nginx/src/ddebug.h` remains the debug compatibility header that
participates in generated NGINX build copies.

## Deliberately Unchanged

- Apache hook registration.
- Apache bucket brigades and output helpers.
- NGINX module registration.
- NGINX access/header/body filters.
- Request and response body handling.
- libmodsecurity transaction ownership and lifecycle.
- Runtime intervention behavior.
- YAML cases, xfail/mapped-only classifications, and `verified_variables`.

## Evidence

The new adapter metadata is checked independently by
`ci/check-adapter-helpers.sh`. Real-world Apache and NGINX smokes remain the
regression proof that the unchanged productive connector paths still behave as
before.

## Risks

- Metadata can drift from `connectors/*/ORIGIN.md` and `licenses/`. The helper
  smoke catches empty or changed required fields, while docs remain the source
  of detailed attribution.
- Adapter-owned files can be mistaken for active runtime replacements. The
  current build scripts do not link `metadata.c` into Apache or NGINX modules.
- Future replacement work may be tempted to touch filters or lifecycle code too
  early. Those candidates remain deferred until a dedicated adapter-owned
  implementation and smoke proof exist.

## Next Phase Recommendation

The next safe phase should keep adapter work metadata- or report-adjacent. A
productive replacement should be attempted only after one narrow behavior has:

- a repo-owned adapter implementation;
- build integration isolated to `$BUILD_ROOT`;
- before/after real-world Apache and NGINX smoke evidence;
- updated origin and pruning documentation.

## Phase 7 Follow-On

Phase 7 is the first report-path use of these skeletons. It may serialize and
compare adapter metadata in build/runtime summaries, but it still must not link
the metadata helpers into productive connector modules or alter connector
request/response behavior.

## Phase 9 Follow-On

Phase 9 expands the NGINX adapter-owned tree from metadata/debug helpers to the
full NGINX module source. That follow-on remains NGINX-specific; it does not
make the NGINX filters, phase handlers, response-body behavior, or transaction
lifecycle part of Common.
