# Apache Architecture

Status: adapter-owned runtime path, evidence-scoped

The Apache connector is an Apache httpd module using libmodsecurity v3 public C
APIs. Productive source lives under `connectors/apache/src/`; build metadata and
Autotools/APXS inputs live under `connectors/apache/`.

## Runtime Shape

```text
HTTP client -> Apache httpd -> mod_security3.so -> libmodsecurity -> HTTP response
```

Apache owns server-specific behavior:

- pre/post config hooks
- request early and late hooks
- input filters
- output filters
- log transaction hook
- per-directory configuration and merge
- intervention mapping
- bounded Phase 4 response buffering and strict-abort evidence

These surfaces are not connector-neutral and must remain under
`connectors/apache/`.

## Current Evidence

- Default runtime smoke: `54/54 PASS`.
- Force-all runtime evidence: `133 attempted / 100 PASS / 27 FAIL /
  0 BLOCKED / 6 NOT_EXECUTABLE`.
- Build and smoke flow: `COMPILE_APACHE.md`.
- Generated detail report:
  `reports/testing/generated/apache-runtime-results.generated.md`.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

## Boundaries

The shared `common/` layer may contain directive names, option defaults, and
data shapes. It does not own Apache hooks, filters, bucket brigades, request
body handling, response body handling, transaction ownership, or server
lifecycle behavior.
