# Connector Contract

Status: evidence-scoped contract for the productive Apache, NGINX, and HAProxy
connectors.

## Purpose

The connector contract defines one vocabulary for productive connectors without
changing runtime behavior, YAML expectations, generated PASS/FAIL values, or
report classifications. It exists to:

- describe uniform minimum requirements for `connectors/apache`,
  `connectors/nginx`, and `connectors/haproxy`;
- provide a reusable acceptance baseline for future connectors;
- define the evidence that must exist before a connector can be considered
  `verified-case` or full-matrix ready;
- keep runtime behavior, harness evidence, native oracle evidence, and generated
  report classification separate; and
- prevent local diagnostic artifacts from being counted as official runtime
  evidence.

Capability claims are valid only when backed by live connector evidence or by a
generated report produced from verified inputs. This document may describe known
boundaries, but it must not be used to hide failing checks, alter expected
statuses, or mark incomplete evidence as PASS.

## Connector Lifecycle

| State | Minimum requirements | Required artifacts | Allowed reports | Claims not allowed yet |
| --- | --- | --- | --- | --- |
| `skeleton` | Repository path exists with ownership/provenance notes and a planned integration model. | `README.md`, `ORIGIN.md` or equivalent provenance notes, preliminary docs. | Design notes only. | Buildability, runtime execution, request blocking, full-matrix readiness. |
| `buildable` | Connector source or integration glue builds reproducibly outside the checkout or in an approved build root. | Build target, source metadata, build logs under the runtime/build root. | Build/cache reports if generated from real inputs. | Runtime-startable, verified-case-ready, production-verified. |
| `runtime-startable` | Local server/runtime can start and serve a readiness endpoint without claiming ModSecurity enforcement. | Runtime config, startup logs, access/error or equivalent operational logs. | Runtime readiness notes. | Request blocking, request-body processing, CRS/MRTS support. |
| `verified-case-ready` | `make verified-case CONNECTOR=<name> ...` writes the standard case envelope and either a real runtime result or a diagnostic classification. | `case-run.json`, `case-run.md`, `result.json`, copied logs under `VERIFIED_RUN_ROOT`. | Targeted diagnostic or targeted runtime evidence. | Official matrix counts unless the corresponding full-matrix job is refreshed. |
| `full-matrix-ready` | Full-matrix jobs complete with fresh inputs, complete job metadata, copied logs, no timeout-as-success, and generated reports pass layout/governance checks. | Full-matrix job directories, per-case result JSON, `job.json`, logs, manifest-backed reports. | Full-matrix reports generated from verified inputs. | Production verification beyond the tested matrix surface. |
| `production-verified` | Connector has sustained full-matrix evidence plus documented operational boundaries, failure modes, and release readiness. | Full evidence set plus production validation notes. | Release/production readiness reports. | Unlimited capability claims outside documented evidence. |

A connector can move forward only with evidence. A connector can move backward
if evidence becomes stale, missing, blocked, or superseded by targeted findings.

## Existing Connector Status

| Area | Apache | NGINX | HAProxy | Gap |
| ---- | ------ | ----- | ------- | --- |
| Build layout | Adapter-owned source under `connectors/apache/src/` with Autotools metadata and `Makefile.am`. | NGINX dynamic-module source under `connectors/nginx/src/` with `config` metadata. | SPOA/SPOP runtime and ModSecurity binding sources under `connectors/haproxy/src/` with a connector `Makefile`. | Layouts are server-native; only evidence artifacts are normalized. |
| Runtime config | Harness materializes `apache_smoke.conf` and per-case rules in the build root. | Harness materializes `nginx_smoke.conf` and per-case rules in the build root. | Harness starts HAProxy, local backend, and SPOP runtime from generated HAProxy/SPOE config. | HAProxy has an extra decision transport layer. |
| Harness scripts | `connectors/apache/harness/run_apache_smoke.sh` plus framework verified runners. | `connectors/nginx/harness/run_nginx_smoke.sh` plus framework verified runners. | `connectors/haproxy/harness/run_haproxy_smoke.sh` plus framework verified runners. | Keep framework entrypoint variables aligned; avoid duplicate case parsing. |
| Log paths | Per-case runtime logs under the verified/build log root; Apache access, error, and audit evidence are copied into case artifacts when present. | Per-case runtime logs under the verified/build log root; NGINX access, error, and audit evidence are copied into case artifacts when present. | Per-case runtime logs under the verified/build log root; HAProxy, SPOP, backend, audit, and `decision.jsonl` evidence are copied when present. | Not every connector emits the same structured fields. |
| Audit-log handling | Audit logs are connector evidence when configured and present; some rule-match details can be less structured than NGINX/HAProxy. | Audit logs can contain phase/rule evidence, including phase-4 response-body matches. | Audit evidence is paired with SPOP decision records for request-side and bounded response-side cases. | Audit presence is capability evidence, not a blanket behavior guarantee. |
| Access/error logs | Access and error logs are collected as operational evidence. | Access and error logs are collected as operational evidence. | HAProxy/SPOP/backend logs replace traditional web-server error/access pairing where applicable. | Consumers must tolerate connector-specific log names. |
| Decision/evidence output | HTTP status and copied logs are primary; rule evidence can be derived from audit/error details when present. | HTTP status, access/error logs, and audit/rule messages are primary. | `decision.jsonl` is primary structured decision evidence; `rule_id=0` means no rule match, and `decision`, `intervention_status`, and HTTP status drive classification. | HAProxy has the most structured decision stream. |
| Phase support | Reference-near request phases 1/2 and broad phase coverage; response-body enforcement is evidence-scoped, not blanket-promoted. | Phase-4 response-body rule matches can be evidenced, but late disruptive enforcement can still return HTTP 200. | Request phases 1/2 are live-evidenced; phase 3 and bounded phase 4 are evidence-scoped through SPOE/SPOP. | Full response-body hard-abort behavior is not uniformly promoted. |
| Request body support | URL-encoded, JSON, XML, and multipart evidence follows framework case coverage. | URL-encoded, JSON, XML, and multipart evidence follows framework case coverage. | URL-encoded, JSON, XML, and multipart evidence is request-buffer/SPOE-frame bounded. | HAProxy large/streaming/multi-frame bodies remain outside the proven surface. |
| Response body support | Non-promoted except where generated focused evidence says otherwise. | Rule match evidence is possible; late phase-4 disruptive enforcement gap is classified separately. | Bounded strict-abort evidence exists; full-body response support is not promoted. | Response body capability must be stated per case/evidence source. |
| CRS/MRTS handling | No-CRS and With-CRS variants are matrix dimensions; `with-mrts` can overlay `ctl:ruleEngine=DetectionOnly`. | Same matrix dimensions and MRTS overlay behavior. | Same matrix dimensions and MRTS overlay behavior. | DetectionOnly overlay intentionally makes disruptive actions non-blocking. |
| DetectionOnly overlay behavior | Classified as `with_mrts_detection_only_overlay` when MRTS sets DetectionOnly and a disruptive case returns 200. | Same. | Same. | This is a known overlay boundary, not PASS fabrication. |
| `verified-case` integration | Must emit `case-run.json`, `case-run.md`, `result.json`, copied logs, and official mismatch context when available. | Same. | Same, plus `decision.jsonl` when emitted by SPOP runtime. | Missing framework/runtime components may produce diagnostic evidence but not complete runtime evidence. |
| Full-matrix integration | Full-matrix-ready when connector jobs have fresh result JSON, copied logs, no critical mismatches, and merge-readiness remains PASS. | Same. | Same, with structured SPOP decisions included. | Full-matrix refresh is required only after behavior/evidence producer changes. |

## Required Directory Layout

The target contract for a productive connector is:

```text
connectors/<name>/
  README.md
  config/      # static connector/server module config when applicable
  scripts/     # connector-owned helper scripts when needed
  harness/     # smoke and verified runtime entrypoints
  logs/        # documentation/examples only; runtime logs stay outside checkout
  examples/    # minimal example configs and deployment snippets
  docs/        # architecture, build, validation, and capability notes
  src/         # connector source or integration glue
```

The current repository intentionally does not force all existing connectors into
that shape:

| Connector | Current shape | Difference from target | Roadmap note |
| --- | --- | --- | --- |
| Apache | `src/`, `harness/`, `docs/`, build metadata, provenance files. | No connector-local `config/`, `scripts/`, `logs/`, or `examples/` directory. | Add README links or examples only when needed; do not move working Autotools/build files without targeted tests. |
| NGINX | `src/`, `harness/`, `docs/`, `config`, provenance files. | Has NGINX module `config` file rather than a `config/` directory; no connector-local `scripts/`, `logs/`, or `examples/` directory. | Keep NGINX-native module metadata in place; document examples before restructuring. |
| HAProxy | `src/`, `harness/`, `docs/`, `poc/`, connector `Makefile`, provenance files. | No top-level `config/`, `scripts/`, `logs/`, or `examples/` directory; SPOE examples live under `poc/`. | Preserve SPOE/SPOP history; consolidate examples only after evidence-preserving cleanup. |

Do not blindly move files to satisfy the target shape. Any layout cleanup must be
a separate low-risk task with `make lint`, `make quick-check`, and affected
connector smoke evidence.

## Required Runtime Artifacts

A real connector runtime run must provide the following artifacts when the
runtime reaches the connector path:

| Artifact | Requirement |
| --- | --- |
| `result.json` | Machine-readable outcome with `status`, `expected_status`, `actual_status`, and a clear reason or connector-specific decision fields. |
| Access log | HTTP request/response trace when the server exposes one. |
| Error log | Server or runtime errors that explain startup, request handling, and ModSecurity messages. |
| Audit log | Required when supported/configured by the connector and test variant. Absence must be explicit when a case asserts no audit log. |
| Decision stream | Required when a connector has a structured decision transport separate from HTTP status. |
| `case-run.json` | Verified-case envelope with connector, case, CRS/MRTS variant, command, duration, copied artifacts, official mismatch context, and `full_matrix_refresh_needed`. |
| `case-run.md` | Human-readable run summary with request metadata, evidence paths, rule evidence, log excerpts, and next-step commands. |
| Copied logs | Relevant logs copied under `VERIFIED_RUN_ROOT` so reports do not depend on ephemeral process directories. |

Connector-specific additions:

| Connector | Additional required or expected evidence |
| --- | --- |
| Apache | Apache error log, access log when available, audit log when configured, and a documented limitation that some rule-match details are less structured than HAProxy/NGINX. |
| NGINX | NGINX error log, access log when available, ModSecurity audit evidence, and phase-4 response-body match notes for response-body cases. |
| HAProxy | `decision.jsonl`, HAProxy logs, SPOP/SPOA logs, backend logs, `decision=pass|deny`, `intervention_status`, and `rule_id`. |

`result.json` must never be hand-edited to force PASS/FAIL. If a harness cannot
produce a runtime result, it may write `status: missing_result`, but that run is
`diagnostic_only` and cannot count as a runtime smoke PASS.

## Normalized Decision Model

| Field | Meaning |
| --- | --- |
| `expected_status` | Expected HTTP status from the selected YAML case and variant. |
| `actual_status` | HTTP status observed through the live connector path. |
| `status` | Normalized outcome: `PASS`, `FAIL`, `BLOCKED`, `MISSING_RESULT`, or the connector-local equivalent before normalization. |
| `rule_id` | Matched ModSecurity rule when known; for HAProxy, `rule_id=0` means no rule match. |
| `decision` | Connector decision such as `pass`, `deny`, or `unknown`. |
| `intervention_status` | HTTP status requested by a ModSecurity disruptive intervention, when available. |
| `classification` | Report classification for known boundaries; it explains evidence but does not replace raw artifacts. |
| `critical` | Whether the classified outcome blocks merge readiness. |
| `evidence_scope` | `full-matrix`, `targeted`, `native`, `diagnostic`, `stale`, or `refresh-needed`. |

## Evidence Scope Rules

| Evidence type | Can change official counts? | Rules |
| --- | --- | --- |
| Full-matrix evidence | Yes | Only complete full-matrix jobs with fresh inputs may update official runtime counts, critical mismatch totals, and merge-readiness dashboards. |
| Targeted evidence | No, not by itself | Targeted runs can prove a fix or boundary before/after, but official reports become green only after affected matrix jobs are refreshed. |
| Native evidence | No | Native oracle runs can explain libmodsecurity semantics but do not replace connector matrix evidence. |
| Diagnostic-only evidence | No | `missing_result`, missing runtime components, startup blockers, or copied command logs are useful diagnostics but must never count as runtime PASS. |
| Stale evidence | No | Evidence from old inputs, old component caches, or superseded manifests cannot be used for current readiness claims. |
| Refresh-needed evidence | No until refreshed | `full_matrix_refresh_needed=true` requires real reruns and must return to `false` before the evidence is considered current. |

Only full-matrix evidence may change official runtime numbers. Diagnostic-only
verified-case output must be labelled with a classification such as
`diagnostic_only_missing_runtime_components` when local components are absent.

## Capability Boundary Model

### Apache

- Apache is the reference-near control connector for many request and
  request-body cases.
- Request blocking and request-body behavior are evidence-scoped, not assumed
  from source layout alone.
- Audit log evidence can be present, but some harness logs contain less
  structured rule-match detail than HAProxy `decision.jsonl` or NGINX
  audit/error messages.
- Apache is not automatically a perfect oracle for every libmodsecurity
  semantic; native evidence and cross-connector matrix evidence remain separate.

### NGINX

- Request blocking works for the cases covered by verified evidence.
- Request-body behavior works for the checked URL-encoded, JSON, XML, and
  multipart cases.
- Phase-4 response-body rule-match evidence is possible.
- Late disruptive phase-4 response-body enforcement can leave the client-visible
  HTTP status at `200` even when audit/rule evidence exists.
- Classification: `nginx_phase4_response_body_enforcement_gap`.
- This boundary is non-critical while it is evidence-based, documented, and not
  misreported as hard response-body blocking.

### HAProxy

- HAProxy uses an SPOA/SPOP-based connector model.
- `decision.jsonl` is the primary structured decision evidence.
- `rule_id=0` means no ModSecurity rule match.
- `decision=pass` means no connector block was applied.
- `decision=deny` together with `intervention_status` shows disruptive blocking.
- Request-body support is bounded by request buffering and SPOE frame limits.
- Response-body support is bounded and must not be blanket-promoted.

### MRTS

- `with-mrts` can set `ctl:ruleEngine=DetectionOnly`.
- Disruptive actions are intentionally non-blocking under that overlay.
- Classification: `with_mrts_detection_only_overlay`.
- This is not a connector bug when the evidence shows DetectionOnly was applied.

## Full-Matrix Readiness Criteria

A connector is full-matrix-ready only when all criteria are met:

1. Runtime components are startable from approved runtime/build roots.
2. `verified-case` writes at least diagnostic artifacts and writes real runtime
   `result.json` for complete smoke claims.
3. Full-matrix job artifacts are complete for the connector/CRS/MRTS variant.
4. `job.json` is present and complete.
5. Timeout, interrupted, or missing-result jobs are not counted as fresh
   completion.
6. Logs and decision/audit evidence are copied under `VERIFIED_RUN_ROOT`.
7. Reports are generated from real current inputs, not hand-patched files.
8. `make check-generated-report-layout` remains PASS.
9. Critical mismatch count and merge-readiness status are read from generated
   evidence, never manually edited.

## New Connector Acceptance Criteria

Minimum before a new connector is admitted to the full matrix:

| Requirement | Acceptance rule |
| --- | --- |
| Build target exists | A documented build target can produce the connector or integration artifact. |
| Runtime start target exists | A documented target starts the runtime from approved paths. |
| `verified-case` works | The target writes `case-run.json`, `case-run.md`, copied logs, and `result.json`. |
| Request blocking smoke passes | A simple disruptive request case produces the expected runtime block. |
| Request-body smoke evaluated | At least one request-body case is run and classified. |
| Logs copied | Access/error/audit/decision logs are copied or explicitly classified unavailable. |
| Capability notes documented | Boundaries and non-promoted areas are documented before report promotion. |

Not allowed before real full-matrix evidence:

- `production_verified`
- `full_matrix_ready`
- `merge_ready`
- `critical_free`

## Future Generated Report

A generated connector capability summary would be useful only when complete
verified runtime inputs are available. The future report should be generator
backed and derive from current manifests/reports, not hand-written tables:

```text
reports/testing/generated/manifest/connector-capability-summary.generated.md
reports/testing/generated/manifest/connector-capability-summary.generated.json
```

Target columns:

| Connector | Request Blocking | Request Body | Response Body Match | Response Body Enforcement | Audit Log | CRS | MRTS |
| --- | --- | --- | --- | --- | --- | --- | --- |

Do not add or commit this report if it would create blocked generated reports or
if complete verified runtime inputs are unavailable.

## Low-Risk Hardening Roadmap

1. Add connector README links to this contract and the capability model.
2. Add a generator-backed connector capability summary after a clean verified
   runtime input set is available.
3. Improve copied-log labels in `case-run.md` without changing request
   processing.
4. Evaluate new connector candidates separately, using this lifecycle before any
   full-matrix promotion.
5. Avoid existing connector refactors while the verified evidence baseline is
   PASS unless a targeted before/after evidence plan exists.
