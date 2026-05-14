# Lighttpd Architecture

Status: unknown

Official source exposes native plugin hooks. Official `mod_magnet`
documentation describes Lua request manipulation.

Candidate approaches:

- Native Lighttpd plugin.
- Lua via `mod_magnet`.

No approach is selected yet. Response body support and blocking behavior are
unknown for this scaffold.
