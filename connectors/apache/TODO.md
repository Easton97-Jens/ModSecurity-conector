# Apache Planning

Status: scaffolded

Tracked in `docs/roadmap/todo-inventory.md`.

- Verify license requirements before importing or adapting any code.
- Validate the PoC Autotools/APXS helper on a host with Apache development
  tools installed.
- Define capability flags for request body, response body, audit log, reload,
  and custom transaction ID.
- Port only proven Apache-specific tests into `tests/apache/`.
- Document every reused concept as `connector-specific` or `engine-specific`.
- Turn the minimal smoke harness into a connector-specific regression test only
  after a real HTTP `403` pass is observed.
