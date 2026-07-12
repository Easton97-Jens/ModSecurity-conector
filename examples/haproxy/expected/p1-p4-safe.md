# HAProxy P1--P4 Safe intent

**Language:** English | [Deutsch](p1-p4-safe.de.md)

The native HTX Safe reference selects phase4-mode safe. It is meant for the
patched native filter path, not the SPOE/SPOP compatibility service. A P4
decision after a response has started is recorded as Safe log-only behavior;
the configuration does not promise a status replacement or a Strict abort.

The minimal reference exposes the parser-supported minimal mode. There is no
Strict example because a checked-in filter option is not proof of a
client-observed post-commit abort.
