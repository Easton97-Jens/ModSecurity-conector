# Memory, Ownership, and Lifecycle Check

Map ownership and lifetime of host objects, connector contexts, Common/libmodsecurity transactions, borrowed buffers/ranges, files, sockets, sessions, goroutines/threads, and cleanup hooks.

Check applicable use-after-free, double free/finish/destroy, invalid free, out-of-bounds access, integer/signedness errors, pointer-length mismatch, stale borrowed data, cleanup ordering, callback-after-finalization, cross-request state reuse, goroutine/thread/channel/FD/socket/session leaks, panic/error cleanup, and subsequent legitimate request behavior.

Use language/runtime-specific tooling only when it applies and is safely executable.
