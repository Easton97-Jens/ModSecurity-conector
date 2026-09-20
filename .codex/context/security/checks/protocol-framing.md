# Protocol Framing and Session-State Check

Use for connector paths that exchange structured frames/messages across SPOE/SPOP, gRPC/ext_proc, private response companions, UDS engine protocols, or other local protocol boundaries.

Assess protocol/version/magic fields, operation/type, transaction/session identifiers, declared versus actual length, zero/oversized/truncated payloads, integer/signedness arithmetic, flags/status, partial reads/writes, multiple frames per read, one frame across reads, extra bytes, unknown operations, malformed responses, and explicit EOS/finish/destroy/cancel semantics.

Assess sequencing such as message before session open, duplicate open, body before headers, response before request completion, duplicate/missing EOS, finish/destroy ordering, data after destroy, unknown/colliding transaction IDs, stale response after reconnect/restart, and cross-session state leakage.

For each failure path record whether it fails closed, cleans up exactly once, preserves unrelated sessions, and allows a subsequent legitimate transaction.
