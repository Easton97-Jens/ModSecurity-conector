# Apache Strict profile boundary

**Language:** English | [Deutsch](README.de.md)

## Status

`modsecurity_phase4_mode strict` is parser-supported, but this repository has
no Apache host evidence for a client-visible late abort. Strict is therefore
optional and intentionally has no runnable configuration here.

## Use

Start from `../safe/httpd.conf`, set `modsecurity_phase4_mode strict`, validate
with `apachectl -t`, and record host-specific evidence before relying on a
post-commit action.
