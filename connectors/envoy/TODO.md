# Envoy TODO

Status: unknown

- Decide integration path: native C++ HTTP filter, ext_authz service, Lua, or
  Wasm.
- Determine whether selected path can support request body, response body,
  intervention, audit artifacts, and logging.
- Define capability flags before adding connector tests.
- Document Envoy build constraints before implementation.
