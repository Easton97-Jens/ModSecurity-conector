# Connector CRS/MRTS Matrix Policy

## Baseline assessment model

When a complete CRS/MRTS matrix is required, assess the six selected Parent connector routes against four independent profiles:

- no CRS / no MRTS
- CRS / no MRTS
- no CRS / MRTS
- CRS / MRTS

This is a 24-cell assessment model. Each cell is a distinct claim; no connector/profile/transport result proves another.

## Scope selection

A full assessment is normally required for common/cross-connector runtime-contract changes, shared lifecycle/body/header/intervention/evidence changes, reusable Framework matrix/runner/normalizer changes, relevant release/readiness work, cross-connector security effects, or an explicit complete-matrix request.

A connector-local change normally assesses the four profiles for that connector and any shared/indirectly affected routes.

## Execution availability

Do not hard-code point-in-time runnable connector counts in this policy. Before execution inspect the current root `Makefile`, matrix runners, Framework contracts, and connector-specific targets. A mandatory cell whose current runner/prerequisite is unavailable receives `blocked`/`not_run` with its exact reason; it is not silently omitted or inferred from another runner.

## Evidence

For every required cell record connector/profile, current revisions, command actually executed, run ID, relevant host/transport identity, start/end/exit/result, isolated paths/evidence, limitations, and exact reason for every non-passing status.

Run/evidence roots, ports, logs, and process ownership must be isolated. Use `resources-and-storage.md` before large matrices.

The baseline matrix transport does not automatically multiply into H2/H3. Additional transport dimensions follow `protocol-and-hardening.md`.
