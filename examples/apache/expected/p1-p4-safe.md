# Apache P1--P4 Safe intent

**Language:** English | [Deutsch](p1-p4-safe.de.md)

The Safe reference configures native httpd-module processing for P1 through P4
and bounds response-body input at 1048576 bytes. A P4 decision that happens
after response commitment is expected to be handled as Safe log-only behavior;
it must not be documented as a visible HTTP 403 without matching host evidence.

This file records configuration intent, not a run result. The native path does
not promise per-chunk rule evaluation, a full connector response buffer, or a
Strict post-commit abort. No Strict example is supplied here.
