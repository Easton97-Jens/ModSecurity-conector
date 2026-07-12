# lighttpd Strict profile boundary

**Language:** English | [Deutsch](README.de.md)

## Status

Common Runtime accepts `phase4_mode=strict`, but the native lighttpd module
does not implement a strict transport abort. Strict is optional and no runnable
strict host profile is supplied.

## Use

Validate the matching host/module pair and Common Runtime configuration before
testing a strict value; do not describe it as an implemented client abort.
