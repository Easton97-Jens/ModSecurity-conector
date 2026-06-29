# Template Evaluation

**Language:** English | [Deutsch](template-evaluation.de.md)

Status: reviewed

Template status: suitable scaffold, not runtime-verified

`connectors/_template` is evaluated as a scaffold for future connectors, not as
a completed connector. It intentionally contains no productive adapter source,
no local executable test suite, and no runtime claim. Runtime evidence belongs
to concrete connectors and must be recorded with commands, counts, summary JSON,
logs, and per-case expected/actual status.

## Verdict

- [x] Suitable as a connector scaffold.
- [x] Does not claim Apache, NGINX, HAProxy, or any other runtime behavior.
- [x] Documents that executable tests are framework-owned.
- [x] Keeps `connectors/_template/tests` absent.
- [x] Defines per-connector gates for origin, metadata, build, No-CRS,
  With-CRS, coverage matrix, RESPONSE_BODY, and promotion.
- [ ] Runtime verified: not applicable to the Template.
- [ ] Build verified: not applicable to the Template.
- [ ] RESPONSE_BODY verified: not applicable to the Template.

## Checklist Evidence

| Area | Result | Evidence | Notes |
| --- | --- | --- | --- |
| README | [x] Present | `connectors/_template/README.md` | Describes purpose, required files, non-claims, and per-connector evidence. |
| TODO | [x] Present | `connectors/_template/TODO.md` | Phase checklist exists for future connector work. |
| Architecture docs | [x] Present | `connectors/_template/docs/architecture.md` | Requires connector-specific architecture proof. |
| Build docs | [x] Present | `connectors/_template/docs/build.md` | Treats build evidence as per-connector. |
| Validation docs | [x] Present | `connectors/_template/docs/validation.md` | Requires executed runtime commands and result files. |
| Coverage matrix docs | [x] Present | `connectors/_template/docs/coverage-decision-matrix.md` | Separates framework coverage from runtime verification. |
| Harness contract | [x] Present | `connectors/_template/harness/README.md` | Harness implementation remains per-connector. |
| Source placeholder | [x] Present | `connectors/_template/src/README.md` | No productive source claim. |
| Local tests folder | [x] Absent | `test ! -d connectors/_template/tests` | Executable tests stay in `modules/ModSecurity-test-Framework/tests/cases/`. |
| Runtime proof | [ ] Not applicable | This report | A Template cannot be runtime-verified. |

## Phase Matrix

| Phase | Gate | Template status | Promotion meaning |
| --- | --- | --- | --- |
| Phase 0 | Scaffold files | [x] Complete | Suitable scaffold. |
| Phase 1 | Origin/license | [ ] Per-connector gate | Future connector must provide `ORIGIN.md` and provenance. |
| Phase 2 | Metadata | [ ] Per-connector gate | Future connector must provide metadata in the repo's expected form. |
| Phase 3 | Build | [ ] Per-connector gate | Future connector must provide command, result, artifact, and log path. |
| Phase 4 | Harness | [ ] Per-connector gate | Future connector must implement the harness contract. |
| Phase 5 | No-CRS runtime | [ ] Per-connector gate | No-CRS evidence cannot be inherited from the Template. |
| Phase 6 | With-CRS runtime | [ ] Per-connector gate | CRS evidence must be scoped to executed With-CRS cases. |
| Phase 7 | Coverage matrix | [x] Scaffold rule | Matrix shape is documented; rows must be filled by each connector. |
| Phase 8 | RESPONSE_BODY | [ ] Runtime promotion gate | Blocking RESPONSE_BODY evidence is required before any verified claim. |
| Phase 9 | Negative/pass-through | [ ] Per-connector gate | Required before promotion beyond partial. |
| Phase 10 | Audit/log | [ ] Per-connector gate | Required before promotion beyond partial. |
| Phase 11 | More than partial | [ ] Blocked by design | Requires a concrete connector and complete runtime evidence. |

## Non-Claims

- The Template is not an Apache, NGINX, HAProxy, Envoy, lighttpd, or Traefik
  runtime implementation.
- Generated coverage reports are planning/reporting aids, not runtime proof.
- A PASS for one concrete connector does not transfer to the Template or to a
  different connector.
- No RESPONSE_BODY blocking support is claimed by the Template.
- No local `connectors/_template/tests` directory is required or allowed for
  executable cases.

## Per-Connector Gates

Concrete connectors must provide:

- [ ] `ORIGIN.md`, license, source map, imported files, and local changes.
- [ ] Metadata source or the repository's equivalent metadata form.
- [ ] Build command, exit status, artifact path, include/library paths, and log.
- [ ] Harness command and summary JSON path.
- [ ] No-CRS and With-CRS results documented separately.
- [ ] Per-case PASS/FAIL/BLOCKED/NOT_EXECUTABLE counts where a matrix is run.
- [ ] CRS verification scoped only to executed CRS cases.
- [ ] RESPONSE_BODY blocking evidence before verified RESPONSE_BODY claims.
- [ ] Negative/pass-through and audit/log evidence before promotion beyond
  partial.

## Decision

The Template is suitable as a scaffold and remains not runtime-verified. Missing
origin, metadata, build, No-CRS, With-CRS, RESPONSE_BODY, audit/log, and runtime
evidence are per-connector gates, not Template defects.
