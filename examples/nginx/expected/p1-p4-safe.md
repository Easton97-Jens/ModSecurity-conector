# NGINX P1--P4 Safe intent

**Language:** English | [Deutsch](p1-p4-safe.de.md)

The Safe config enables the native module, scopes response inspection to the
listed content types, and uses Safe for a late P4 decision. A late match is not
a promise that the client sees a replacement 403. The reference also keeps
gzip off so the inspected byte representation is not assumed.

The Strict config is an available configuration shape only. It does not prove
a client-observed abort, status rewrite, or complete response buffering.
