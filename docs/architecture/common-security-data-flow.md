# Common security data-flow contract

This document describes connector-neutral Common SDK scaffolding only. It does not claim production runtime, CRS, full-matrix, or connector capability until a connector is explicitly migrated.

Data flow: untrusted input -> bounded parse -> validate -> immutable view -> phase guard -> decision -> integrity event -> JSONL -> cleanup.

Hard resource limits protect header counts and sizes, body buffers, event JSON, transaction IDs, rule IDs, and log messages. Events and JSONL records must not contain request or response body payloads.

Memory ownership terms: borrowed data is caller-owned, owned data must be freed by the owner, static data must not be freed, and arena data is released with its arena. The checked allocator accounts owned allocations with no global mutable state.

The `non_crypto_hash` FNV-1a chain is deterministic tamper-evidence for CI and smoke tests only. Real manipulation resistance requires a future HMAC or signature with secure key handling and append-only storage.
