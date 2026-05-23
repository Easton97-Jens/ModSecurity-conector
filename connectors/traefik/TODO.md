# Traefik Planning

Status: unknown

Tracked in `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`.

- Decide integration path: Yaegi middleware or Wasm middleware.
- Determine whether selected path can support libmodsecurity v3, including any
  C/C++ library boundary constraints.
- Define capability flags for request body, response body, intervention, logs,
  and reload.
- Document plugin packaging before implementation.
