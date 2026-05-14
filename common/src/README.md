# common/src

Status: scaffolded

This directory is reserved for connector-neutral implementation files only.

Allowed here:

- Helpers that operate only on `common/include/msconnector/*` types.
- Pure parsing, normalization, or formatting code that does not include server or proxy headers.
- Code that can be built without any connector-specific SDK.

Not allowed here:

- Server/proxy hook code.
- Build glue for a specific runtime.
- Includes from any connector implementation.

TODO:

- Add implementation files only after a concrete connector-neutral need is identified.
