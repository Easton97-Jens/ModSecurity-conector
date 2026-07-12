# Traefik P1--P4 Safe intent

**Language:** English | [Deutsch](p1-p4-safe.de.md)

The native local-plugin reference uses engineMode uds and a private local
engine socket. Its service configuration selects streaming body modes and
phase4_mode safe. A post-commit P4 result is intended to remain Safe log-only;
it is not a claimed response rewrite or Strict connection abort.

The forwardAuth files are request-only compatibility material. They must not be
used to describe P3/P4 coverage. The [Strict directory](../strict/README.md)
documents the optional boundary; it is not a host-abort claim.
