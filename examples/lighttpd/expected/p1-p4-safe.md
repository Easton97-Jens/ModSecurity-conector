# lighttpd P1--P4 Safe intent

**Language:** English | [Deutsch](p1-p4-safe.de.md)

The Safe reference is limited to the matching patched lighttpd 1.4.84 native
host and identity HTTP/1.1 entity data through mod_proxy. It selects streaming
body modes and phase4_mode safe. It neither enables compressed entities nor
claims HTTP/2, HTTP/3, file, or zero-copy response inspection.

A late P4 decision is a Safe log-only boundary, not a claimed visible 403 or
Strict abort. The stock minimal reference keeps bodies disabled. No Strict
example is supplied.
