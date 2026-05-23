# Apache Architecture

Status: scaffolded

The local Apache connector is an Apache module using libmodsecurity v3 public C
APIs. Observed connector-specific concepts include:

- Apache pre/post config hooks.
- Request early/late hooks.
- Input and output filters for request and response bodies.
- Log transaction hook.
- Per-directory configuration and merge.

These are not connector-neutral and must remain under `connectors/apache/`.

Open work is tracked in `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`:

- Define the exact hook order to use for a new adapter.
- Prove request/response body handling with connector-specific tests.
- Document cleanup and intervention behavior before implementation.
