> Generated capability snapshot — do not edit runtime status manually.

# Apache No-CRS Baseline

**Language:** English | [Deutsch](apache-no-crs-baseline.de.md)

Generated on `2026-07-10` from the checked-in `connectors/<name>/capabilities.json` manifests. No canonical No-CRS `result.json` was used because no canonical run had been executed.

Overall canonical status: `NOT EXECUTED`

Host model: `native Apache httpd module`

| Dimension | Canonical status | Manifest boundary |
|---|---|---|
| Source contract | IMPLEMENTED, NOT ASSERTED | Source, metadata, and host wiring are present |
| Build / link | IMPLEMENTED, NOT ASSERTED | A current canonical build result is absent |
| Config load | IMPLEMENTED, NOT ASSERTED | A current canonical config result is absent |
| Request-free start | IMPLEMENTED, NOT ASSERTED | A current canonical start result is absent |
| Minimal runtime | IMPLEMENTED, NOT ASSERTED | Earlier targeted evidence is not imported into this baseline |
| No-CRS baseline | NOT EXECUTED | No canonical `result.json` exists |
| Phase 1 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 2 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 3 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 4 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only JSONL must be asserted by a canonical run |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup and failure cases require canonical case results |
| Status | NOT EXECUTED | Missing evidence is never inferred as PASS |

## Architecture boundary

Buffered request and response paths are implemented; streaming paths and drop are not implemented.

Phase-4 intervention timing depends on whether Apache has committed the response.

Expected evidence root:

```text
$EVIDENCE_ROOT/apache/<run-id>/
```

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- extended/full-matrix verification
- response-body verification across all connectors
- a canonical No-CRS PASS
