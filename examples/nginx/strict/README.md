# NGINX Strict profile boundary

**Language:** English | [Deutsch](README.de.md)

## Status

[nginx.conf](nginx.conf) is a parser-supported Strict configuration shape.
It does not claim a visible late status rewrite; post-commit Strict behavior
must be validated against the installed NGINX host.

## Use

Adapt paths and endpoints, run `nginx -t`, and treat an abort as a
host-specific outcome rather than a guaranteed later 403.
