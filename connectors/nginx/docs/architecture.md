# NGINX Architecture

Status: scaffolded

The local NGINX connector is an NGINX HTTP module using libmodsecurity v3 public
C APIs. Observed connector-specific concepts include:

- HTTP access phase handler.
- HTTP log phase handler.
- Header filter.
- Body filter.
- Main and location configuration creation/merge.
- Module ordering around response body filters.

These are not connector-neutral and must remain under `connectors/nginx/`.

Open work is tracked in `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`:

- Define the exact phase and filter ordering for this repo.
- Prove request/response body buffering behavior with connector tests.
- Document intervention handling before implementation.
