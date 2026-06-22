# Connector Contract

Connector implementations must preserve the evidence gates in
[new connector onboarding](new-connector-onboarding.md). New connectors start as
roadmap-only candidates or skeletons and become runtime connectors only after
real runtime artifacts prove the behavior being claimed.

This contract is intentionally evidence-first:

- connector-neutral code stays in `common/`;
- adapter-owned code stays in `connectors/<name>/`;
- generated reports must be produced by generators, not edited manually;
- runtime claims require `result.json` plus logs/evidence;
- full-matrix claims require generated Full-Matrix evidence;
- OpenResty is covered by NGINX unless a future decision explicitly changes that.

## Purpose

The connector contract defines the minimum, connector-neutral obligations for
the productive Apache, NGINX, and HAProxy connectors. It is also the baseline
for any future connector before it can move from planning into verified runtime
evidence.

The contract keeps four concerns separate:

- runtime behavior: what the server, proxy, module, or sidecar actually did;
- harness evidence: the files written by the local or CI runner;
- report classification: how generated reports describe known gaps and
  non-critical boundaries;
- readiness claims: whether targeted or Full-Matrix evidence is complete enough
  to affect official counts.

This separation is what keeps Full-Matrix readiness honest. A connector can have
real targeted evidence without changing official runtime counts. A native
oracle can clarify libmodsecurity semantics without replacing connector matrix
evidence. A local diagnostic smoke can expose missing runtime components without
becoming a PASS.

## Connector Lifecycle

| State | Minimum requirements | Required artifacts | Allowed reports | Not allowed claims |
| --- | --- | --- | --- | --- |
| `skeleton` | Directory or starter exists; scope, source ownership, and non-runtime status are documented. | `README.md`, `ORIGIN.md` or equivalent provenance, metadata or source map when code exists. | Roadmap-only docs or generated roadmap entries. | Runtime PASS/FAIL, verified-case readiness, Full-Matrix readiness, production verification. |
| `buildable` | Connector component, module, or diagnostic starter builds reproducibly outside the checkout. | Build command, build logs under the verified runtime/build root, source ownership notes. | Build/readiness notes and roadmap reports that do not assert runtime behavior. | Traffic handling, request blocking, CRS support, or capability support without runtime artifacts. |
| `runtime-startable` | Server/proxy/module/sidecar can start and stop deterministically in a safe runtime path. | Minimal runtime config, start/stop script or harness command, process logs, cleanup evidence. | Runtime producer readiness and diagnostic startup reports. | Verified blocking, request-body support, audit behavior, or CRS support without `result.json` and logs. |
| `verified-case-ready` | At least one targeted real runtime case runs through the connector. | `result.json`, `case-run.json`, `case-run.md`, copied access/error/audit/decision logs under `VERIFIED_RUN_ROOT`. | Targeted evidence and diagnostic generated summaries. | Broad phase coverage, official count changes, Full-Matrix PASS, merge-ready contribution. |
| `full-matrix-ready` | All connector/CRS/MRTS matrix jobs are schedulable and can produce complete job artifacts. | Complete `job.json`, summary/results JSONL, run logs, build manifests, copied logs for every matrix job. | Full-Matrix completeness and mismatch reports generated from real inputs. | Treating timeouts, partial rows, empty summaries, or stale reports as fresh completion. |
| `production-verified` | Verified evidence pipeline is complete and governance gates pass without critical blockers. | Full generated report set, critical mismatch analysis, merge-readiness dashboard, system environment proof. | Critical generated reports with complete inputs. | Any production claim when inputs are blocked, stale, missing, manually patched, or refresh-needed. |

The lifecycle is monotonic only when evidence is fresh. A connector can regress
from `full-matrix-ready` to a diagnostic state if required inputs are missing,
stale, blocked, or produced from an unsafe runtime path.

## Required Directory Layout

The target layout for productive and future connectors is:

```text
connectors/<name>/
  README.md
  config/
  scripts/
  harness/
  logs/
  examples/
```

The current productive connector tree does not exactly match that ideal shape,
and this document does not authorize moving files just to satisfy a cosmetic
layout:

| Connector | Current layout | Contract delta | Roadmap cleanup |
| --- | --- | --- | --- |
| Apache | `README.md`, `build/`, `docs/`, `harness/`, `src/`, Autotools files. | No separate `config/`, `scripts/`, `logs/`, or `examples/` directory. Runtime logs are copied under `VERIFIED_RUN_ROOT`, not stored in the checkout. | Document any future harness/config split before moving build-sensitive Autotools files. |
| NGINX | `README.md`, root-level dynamic-module `config` file, `docs/`, `harness/`, `src/`. | `config` is a build metadata file, not a `config/` directory; no separate `scripts/`, `logs/`, or `examples/` directory. | If examples or runtime configs are split out later, preserve the module `config` path contract and source map. |
| HAProxy | `README.md`, `docs/`, `harness/`, `poc/`, `src/`. | No separate `config/`, `scripts/`, `logs/`, or `examples/` directory. SPOE/SPOP examples and diagnostics are currently documented under `docs/` and `poc/`. | Move or split examples only after keeping existing SPOA/SPOP evidence references stable. |

Generated logs and runtime outputs must not be committed under connector
directories. They belong under `VERIFIED_RUN_ROOT`.

## Required Runtime Artifacts

A complete verified connector runtime case must write or copy at least:

- `result.json`;
- access log or equivalent request log;
- error log or equivalent server/proxy diagnostic log;
- audit log when supported by the connector and case;
- decision stream when the connector has one;
- `case-run.json`;
- `case-run.md`;
- copied logs under `VERIFIED_RUN_ROOT`.

`missing_result` is useful diagnostics, but it is not a completed runtime smoke.
A case with no real runtime `result.json` must be classified as
`diagnostic_only_missing_runtime_components` or the closest diagnostic-only
reason. It must never be counted as Runtime PASS.

### HAProxy Runtime Artifacts

HAProxy has an additional SPOE/SPOP evidence contract:

- `decision.jsonl` is the primary structured decision stream;
- HAProxy logs and SPOA/SPOP logs must be copied when present;
- `intervention_status` records the ModSecurity intervention status;
- `decision=pass` means the request was not blocked;
- `decision=deny` plus `intervention_status` is blocking evidence;
- `rule_id=0` means no ModSecurity rule match was observed.

### NGINX Runtime Artifacts

NGINX runtime evidence must include:

- NGINX error log;
- ModSecurity audit evidence when the case expects it;
- Phase 4 response-body match notes when the case exercises response bodies.

NGINX can show response-body rule-match/audit evidence while late disruptive
Phase 4 response-body enforcement remains bounded and may leave the HTTP status
at `200`.

### Apache Runtime Artifacts

Apache runtime evidence must include:

- Apache error log;
- ModSecurity audit log when expected;
- notes for cases where rule-match detail is less structured than the
  HAProxy/NGINX decision streams.

Apache is reference-near for this repository, but it is not an automatic oracle
for every libmodsecurity semantic edge.

## Normalized Decision Model

Every generated runtime report should normalize connector-specific observations
into the same fields:

| Field | Meaning |
| --- | --- |
| `expected_status` | HTTP status expected by the test case. |
| `actual_status` | HTTP status observed from the connector runtime. |
| `status` | Runtime result such as `PASS`, `FAIL`, `BLOCKED`, or `MISSING_RESULT`. |
| `rule_id` | Matched ModSecurity rule id when known; connector-specific unknowns must stay explicit. |
| `decision` | Normalized decision: `pass`, `deny`, or `unknown`. |
| `intervention_status` | ModSecurity intervention status when the connector exposes it. |
| `classification` | Generated report classification for known gaps, overlays, or semantics. |
| `critical` | Whether the row blocks merge readiness. |
| `evidence_scope` | Evidence source: `targeted`, `full-matrix`, `native`, or `diagnostic`. |

Connector-specific fields may be preserved, but report decisions must be made
from the normalized model above.

## Evidence Scope Rules

| Evidence scope | Definition | Can change official runtime counts? |
| --- | --- | --- |
| `full-matrix evidence` | Complete generated evidence from all scheduled connector/CRS/MRTS matrix jobs, including complete `job.json` and runtime summaries. | Yes. |
| `targeted evidence` | One or more explicitly selected verified cases used to prove or disprove a focused fix. | No, except as supporting evidence for a later Full-Matrix refresh. |
| `native evidence` | Native ModSecurity, native connector, or oracle-style comparison used to understand semantics. | No. It can explain semantics but does not replace connector matrix evidence. |
| `diagnostic-only evidence` | Local smoke, startup, or missing-runtime output that helps diagnose setup but lacks complete runtime artifacts. | No. |
| `stale evidence` | Evidence generated against old code, old framework inputs, or stale runtime artifacts. | No. |
| `refresh-needed evidence` | Evidence that indicates `full_matrix_refresh_needed=true` after real runtime or input changes. | No, until fresh Full-Matrix evidence turns it back to `false`. |

Strict rules:

- only Full-Matrix evidence may change official runtime counts;
- targeted evidence may justify a fix, but it does not automatically make
  official generated reports green;
- native evidence may validate semantic expectations, but it does not replace a
  connector matrix;
- diagnostic-only evidence, including `missing_result`, must never count as
  Runtime PASS;
- `full_matrix_refresh_needed=true` must be cleared only by a real fresh rerun,
  not by editing reports or documentation.

## Capability Boundary Model

### Apache

Apache is the reference-near control connector in this repository. It has strong
request and request-body coverage and supports audit logging for the covered
cases. Its known boundary is evidence shape: audit logs are present, but
rule-match details are not always as structured as HAProxy `decision.jsonl` or
NGINX Phase 4 notes. Apache must not be promoted as a perfect oracle for every
libmodsecurity semantic edge.

### NGINX

NGINX request blocking is evidence-based for the covered request-side cases.
Request-body behavior is supported for the checked cases. Phase 4 response-body
rule matching can be observed through audit/log evidence.

The bounded gap is late disruptive Phase 4 response-body enforcement: a
response-body rule can match, while the client-visible HTTP status remains
`200`. This is classified as:

```text
nginx_phase4_response_body_enforcement_gap
```

Audit log and rule evidence may still be present. The gap is non-critical while
it remains evidence-based, generated, and not promoted into a false blocking
claim.

### HAProxy

HAProxy uses a SPOE/SPOP-based model. `decision.jsonl` is the primary structured
evidence stream and must be read alongside HAProxy logs, SPOA/SPOP logs, audit
logs, and normalized `result.json`.

Decision semantics:

- `rule_id=0` means no rule match;
- `decision=pass` means no block;
- `decision=deny` with `intervention_status` is block evidence;
- response-body support is bounded and must not be broadly promoted without
  targeted before/after evidence and Full-Matrix confirmation.

### MRTS

MRTS is connector-crossing overlay behavior. The `with-mrts` variant can set:

```text
ctl:ruleEngine=DetectionOnly
```

When that overlay applies, disruptive actions intentionally become non-blocking.
The generated classification is:

```text
with_mrts_detection_only_overlay
```

That is not a connector bug. It is a report classification for the selected
MRTS mode and must not be fixed by Expected-status edits.

## Full-Matrix Readiness Criteria

A connector is Full-Matrix-ready only when all of the following are true:

- runtime startup is deterministic in safe runtime paths;
- `verified-case` can write at least diagnostic artifacts, and complete cases
  write real `result.json`;
- every scheduled Full-Matrix job writes complete artifacts;
- `job.json` is complete for every job;
- no timeout is counted as fresh completion;
- logs are copied under `VERIFIED_RUN_ROOT`;
- reports are generated from real current inputs;
- `check-generated-report-layout` still passes;
- stale, blocked, partial, or `missing_result` rows are classified honestly.

Full-Matrix readiness is not a documentation claim. It is a generated-evidence
claim.

## New Connector Acceptance Criteria

Before a new connector can enter the Full-Matrix, it must prove at least:

```text
build target exists
runtime start target exists
verified-case works
result.json produced
logs copied
request blocking smoke passes
request-body smoke evaluated
capability notes documented
```

Before real Full-Matrix evidence exists, the following claims are forbidden:

```text
production_verified
full_matrix_ready
merge_ready
critical_free
```

See [new connector onboarding](new-connector-onboarding.md) for future connector
planning and first-proof constraints.

## Future Generated Report

A connector capability summary report may be useful later:

```text
reports/testing/generated/manifest/connector-capability-summary.generated.md
reports/testing/generated/manifest/connector-capability-summary.generated.json
```

Do not create or commit that report until complete verified runtime inputs are
available and the generator can derive it from current manifests/reports without
blocking report governance. If local runtime components are missing, keep the
work documented here and do not commit a blocked generated report.

The future report should summarize only evidence-based capabilities:

| Connector | Request Blocking | Request Body | Response Body Match | Response Body Enforcement | Audit Log | CRS | MRTS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence |
| NGINX | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence |
| HAProxy | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence | generated from evidence |

## Small Hardening Roadmap

Future hardening should stay small and evidence-bound:

1. Add a generator-backed connector capability summary only after complete
   runtime evidence exists.
2. Split connector examples/configs only when doing so preserves existing build
   and harness paths.
3. Improve Apache rule-detail extraction without changing runtime behavior.
4. Keep NGINX Phase 4 response-body enforcement classified until targeted
   before/after evidence proves a real enforcement change.
5. Keep HAProxy response-body support bounded until `decision.jsonl`,
   intervention, audit, and HTTP evidence agree.
6. Evaluate any new connector candidate separately and do not refactor the three
   productive connectors while the evidence baseline is stable.
