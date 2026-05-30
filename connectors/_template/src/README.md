# src - Connector Template

This directory is reserved for productive source code of a concrete connector
after its origin, license, metadata, design, and validation evidence are known.

## Current state

- The template contains no productive C/C++ source code.
- The template makes no runtime claims.
- The template is not `adapter-owned` until concrete source, origin, metadata,
  and build evidence exist for a real connector.

## Before adding source

- [ ] Upstream source and license documented in `ORIGIN.md`.
- [ ] Imported files documented in `SOURCE_MAP.json` or equivalent.
- [ ] Local changes documented.
- [ ] Server hook/lifecycle model documented.
- [ ] Build command and include/library paths documented.
- [ ] Runtime validation plan documented.

## Warning

Do not copy Apache or NGINX runtime code into a new connector without proving
that the target server has compatible lifecycle, hook, filter, body handling,
logging, and intervention behavior.
