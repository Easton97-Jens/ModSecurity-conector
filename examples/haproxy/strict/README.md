# HAProxy Strict profile boundary

**Language:** English | [Deutsch](README.de.md)

## Status

The native HTX parser accepts `phase4-mode strict`, but the current host path
records the requested abort as `not_attempted`. Strict is optional and no
runnable profile is claimed here.

## Use

Set the optional argument on the native filter, validate with `haproxy -c -f
<config>`, and do not represent it as a client-visible abort without new host
evidence.
