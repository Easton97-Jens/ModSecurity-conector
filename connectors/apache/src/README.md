# Apache Source

Status: adapter-owned Apache connector source

Apache-specific adapter source belongs here. The monorepo-default Apache smoke
build materializes this tree under `$BUILD_ROOT/apache-build/connector-src` and
builds the Apache module from that generated copy.

Current files include:

- Apache connector module sources derived from ModSecurity-apache base commit
  `0488c77f69669584324b70460614a382224b4883`;
- Autotools/APXS inputs required by the Apache connector build;
- the `.in` templates referenced by `configure.ac`;
- adapter metadata helpers used by report and drift checks;
- `SOURCE_MAP.json`, which records base provenance per file.

This migration does not alter Apache hooks, filters, bucket brigades,
transaction ownership, intervention semantics, or response-body behavior.
`RESPONSE_BODY` remains xfail/mapped-only until separate real-world Apache and
NGINX evidence proves stable blocking behavior.
