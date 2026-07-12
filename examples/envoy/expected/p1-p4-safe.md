# Envoy P1--P4 Safe intent

**Language:** English | [Deutsch](p1-p4-safe.de.md)

The ext_proc reference sets both body modes to STREAMED and the service policy
to safe. It is the native full-lifecycle reference. A P4 result after the
response begins is represented as Safe log-only behavior, not as a claimed
late HTTP status change or deterministic stream reset.

The separate ext_authz configuration cannot observe upstream response headers
or bodies and therefore is intentionally not described as a P3/P4 core path.
No Strict example is supplied.
