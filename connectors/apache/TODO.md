# Apache TODO

Status: scaffolded

- Verify license requirements before importing or adapting any code.
- Decide whether to build with Autotools/apxs or a new wrapper build.
- Define capability flags for request body, response body, audit log, reload,
  and custom transaction ID.
- Port only proven Apache-specific tests into `tests/apache/`.
- Document every reused concept as `connector-specific` or `engine-specific`.
