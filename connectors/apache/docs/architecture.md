# Apache Architecture

**Language:** English | [Deutsch](architecture.de.md)

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
- incremental Phase 4 bucket ingestion, EOS finalization, and strict-abort source wiring

These surfaces are not connector-neutral and must remain under
`connectors/apache/`.

## Current Evidence

- Default runtime smoke: `54/54 PASS`.
- Force-all runtime evidence: `133 attempted / 100 PASS / 27 FAIL /
  0 BLOCKED / 6 NOT_EXECUTABLE`.
- Build and smoke flow: `docs/build/compilers/apache.md`.
- Generated detail report:
  `reports/testing/generated/apache-runtime-results.generated.md`.

Phase 4 / RESPONSE_BODY remains non-promoted. The output filter forwards each
current brigade before EOS and has no connector-owned cross-call response
buffer; safe/strict behavior remains source-only until a real host run proves
the client-visible transport outcome.

## Boundaries

The shared `common/` layer may contain directive names, option defaults, and
data shapes. It does not own Apache hooks, filters, bucket brigades, request
body handling, response body handling, transaction ownership, or server
lifecycle behavior.

## Common SDK adoption boundary

The Apache connector adopts the Common SDK for semantic configuration storage
and merge/validation (`msconnector_config`), directive names/parser contracts,
request/response mapper contracts, rule-load stats, and metadata-only Phase-4
event JSONL emission. Apache code remains responsible for translating Apache
APIs into those Common models.

Still Apache-specific: `command_rec`, `request_rec`, hooks, filters, APR pools,
bucket brigades, APLOG, Apache return codes, and APXS/autotools build wiring.
This architecture note does not claim production readiness, CRS coverage,
full-matrix coverage, or additional runtime verification behavior.

## C standard compile boundary

The Apache/Common-adoption layer is covered by compile-only C standard smokes:
C17 is mandatory, while C23 and future-C are optional when the compiler supports
those modes. These checks compile Apache adoption sources and the Common sources
they consume as objects through APXS/APR include discovery. Missing APXS or
Apache/APR/libmodsecurity headers is a `BLOCKED` condition with exit code `77`.
This remains compile/structure evidence only and does not change Apache runtime,
production, CRS, or full-matrix claims.

## Review-fix boundaries

The response mapper now mirrors Apache response metadata from `err_headers_out`,
`headers_out`, and `content_type` into the Common response model without merging
multi-value headers or adding body payloads. Phase-4 intervention events use a
non-OK Common status and keep body truncation as metadata separate from JSON
writer truncation. These fixes do not expand runtime claims.
