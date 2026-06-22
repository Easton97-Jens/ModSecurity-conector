# common/src

Status: implemented conservative helper layer

This directory contains connector-neutral implementation files only. The Phase 3
helpers are a C-first reference model for metadata/status shapes that the
Python/Shell harnesses mirror in JSON without FFI.

Allowed here:

- Helpers that operate only on `common/include/msconnector/*` types.
- Pure parsing, normalization, or formatting code that does not include server or proxy headers.
- Code that can be built without any connector-specific SDK.
- Small neutral constructors for common status/intervention/decision values.

Not allowed here:

- Server/proxy hook code.
- Build glue for a specific runtime.
- Includes from any connector implementation.

Open work is tracked in `docs/roadmap/todo-inventory.md`:

- Keep these helpers limited to metadata and datatypes.
- Do not add server lifecycle, request body, response filter, or libmodsecurity
  ownership code here.
- Use `ci/check-common-helpers.sh` to compile and run the isolated C smoke under
  `BUILD_ROOT`.
