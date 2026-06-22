# Capability Model

Capabilities describe what a YAML case exercises. They are evidence labels, not
automatic skips. A capability is counted as verified only when a real connector
case produces complete runtime evidence through Apache, NGINX, or HAProxy.

Capability metadata is not connector proof on its own. API-only smokes,
mapped-only inventory entries, former expected-failure probes, blocked cases, and generated
coverage rows do not add verified variables.

The connector evidence contract is defined in
[connector contract](connector-contract.md). That contract owns the lifecycle,
required runtime artifacts, normalized decision model, and evidence-scope rules
for the productive connectors.

## Capability Claim Levels

Capability language must be precise:

| Claim level | Meaning |
| --- | --- |
| `supported` | Covered by complete connector runtime evidence for the named scope. |
| `bounded` | Implemented or observable only inside documented limits. |
| `evidence-scoped` | True for the cited targeted, Full-Matrix, or native evidence, but not a broad claim. |
| `not-promoted` | Observed or planned behavior that must not become official support without more evidence. |
| `diagnostic-only` | Useful setup or missing-runtime evidence that cannot count as Runtime PASS. |

Only `supported` claims backed by fresh Full-Matrix evidence may affect official
runtime counts. Targeted evidence can justify a fix, native evidence can explain
semantics, and diagnostic-only evidence can explain local setup, but none of
those scopes replaces a connector matrix.

## Productive Connector Capability Summary

| Capability | Apache | NGINX | HAProxy | Evidence Basis |
| --- | --- | --- | --- | --- |
| request blocking | supported | supported | supported | Verified runtime matrix and targeted `verified-case` evidence when `result.json` and logs exist. |
| request body | supported for covered cases | supported for covered cases | bounded for covered SPOE/SPOP cases | Full-Matrix rows plus connector harness artifacts. |
| XML body processor | evidence-scoped | evidence-scoped | evidence-scoped | XML cases and native/libmodsecurity comparisons; do not promote semantic edges without evidence. |
| JSON body processor | evidence-scoped | evidence-scoped | evidence-scoped | JSON/raw-body cases that produce complete runtime artifacts. |
| multipart | bounded | bounded | bounded | Remaining multipart review work must not be hidden by Expected-status edits. |
| response body match | bounded | supported for observed match/audit evidence | bounded | Phase 4 reports and connector logs; match evidence is not the same as enforcement. |
| response body enforcement | not-promoted without abort evidence | bounded by `nginx_phase4_response_body_enforcement_gap` | bounded and not broadly promoted | Full-Matrix classifications plus targeted Phase 4 evidence requirements. |
| audit log | supported, with less structured rule detail in some cases | supported for covered audit evidence | supported with audit plus `decision.jsonl` | Audit/log reports and copied runtime artifacts. |
| CRS | evidence-scoped | evidence-scoped | evidence-scoped | Full-Matrix CRS variants only; targeted cases do not imply broad CRS support. |
| MRTS | evidence-scoped | evidence-scoped | evidence-scoped | Full-Matrix MRTS variants and generated overlay classifications. |
| DetectionOnly overlay | supported as classification | supported as classification | supported as classification | `with_mrts_detection_only_overlay` and related DetectionOnly classifications. |
| verified-case | supported only with complete artifacts | supported only with complete artifacts | supported only with complete artifacts | `result.json`, `case-run.*`, and copied logs under `VERIFIED_RUN_ROOT`. |
| full-matrix | supported only from generated matrix evidence | supported only from generated matrix evidence | supported only from generated matrix evidence | Complete `job.json`, summaries, logs, and generated report inputs. |
| native oracle relevance | evidence-scoped, not replacement | evidence-scoped, not replacement | evidence-scoped, not replacement | Native evidence may explain semantics; it never replaces connector evidence. |

The table is deliberately conservative. A row marked `bounded` or
`evidence-scoped` is not a request to skip tests or rewrite expectations. It is
a reminder that capability support must be read together with the evidence
scope.

## Known Capability Boundaries

- Apache is reference-near and has strong request/request-body coverage, but
  audit-log rule detail is not always as structured as HAProxy or NGINX
  decision evidence.
- NGINX can produce Phase 4 response-body match/audit evidence while late
  disruptive enforcement can remain client-visible as HTTP `200`; generated
  reports classify this as `nginx_phase4_response_body_enforcement_gap`.
- HAProxy's primary structured evidence is `decision.jsonl`; `rule_id=0` means
  no match, `decision=pass` means no block, and `decision=deny` with
  `intervention_status` is block evidence.
- MRTS `with-mrts` can set `ctl:ruleEngine=DetectionOnly`, so non-blocking
  disruptive rows are classified as `with_mrts_detection_only_overlay` rather
  than connector bugs.
- `missing_result` is always diagnostic-only unless a real runtime `result.json`
  exists for the same case run.

## Active Capability Names

| Capability | Meaning | Verified variable mapping |
| --- | --- | --- |
| `multipart` | Deterministic multipart/form-data request generation | none by itself |
| `files` | `FILES_*` multipart collections | `FILES` |
| `xml` | XML body processor and XML collection behavior | `XML` |
| `json` | JSON or raw JSON request-body behavior | `REQUEST_BODY` |
| `response-body` | Response-body access/pass-through behavior | not `RESPONSE_BODY` until blocking passes |
| `audit-log` | Stable audit-log fields are asserted | `AUDIT_LOG` |
| `audit-log-absent` | Expected audit-log absence; currently used only for former expected-failure/probes | none |
| `collections` | ModSecurity collection behavior | none by itself |
| `request-cookies` | Cookie value/name collections | `REQUEST_COOKIES` |
| `args-names` | Argument-name collection | `ARGS_NAMES` |
| `request-uri` | Raw request URI variable | `REQUEST_URI` |
| `response-headers` | Response header phase/filter behavior | `RESPONSE_HEADERS` |
| `request-headers` | Request header values or names | `REQUEST_HEADERS` |
| `request-body` | Request body access | `REQUEST_BODY` |
| `query-args` / `form-urlencoded` | Query or URL-encoded body args | `ARGS` |

`RESPONSE_BODY` is intentionally not emitted in `verified_variables` while
`response_body_basic_block` remains former expected-failure/mapped-only.

## Collection Semantics Decisions

`ARGS_NAMES` is verified by active control cases such as
`v3_args_names_get_block`, where a normal ampersand-separated query reaches
libmodsecurity and produces a disruptive intervention through the real
connector path.

Semicolon query separator probes are tracked separately. When Apache, NGINX,
and HAProxy all execute the semicolon collection probes with expected `403` and
actual `200`, while the `ARGS_NAMES` control case passes in the no-MRTS
variants, the mismatch is classified as
`libmodsecurity_collection_semantics`. That classification is report-only: it
does not change YAML expectations or PASS/FAIL values, and it does not count as
a connector-specific runtime regression unless new evidence shows a connector
diverges from the shared libmodsecurity behavior.

## Validation Rules

YAML cases may express capabilities as a list or as a mapping of booleans.
Underscore aliases such as `request_body` normalize to dash names such as
`request-body`. Unknown capability names fail materialization.

Capabilities do not decide whether a case is active. Discovery is path and
status based:

- `modules/ModSecurity-test-Framework/tests/cases/minimal`, `imported`, `v2-imported`, and `v3-imported`
  are active common scopes.
- `modules/ModSecurity-test-Framework/tests/cases/former expected-failure` is excluded from normal discovery and must be
  selected explicitly with `SMOKE_CASES`.
- Connector-specific cases are active only for their matching connector.

## Summary Representation

Connector summaries expose Common metadata by name, not by C/Python FFI. The
harnesses keep using shell and Python, but their JSON records declare:

- `status_model: "msconnector_status"`
- `origin_model: "msconnector_origin"`
- `intervention_model: "msconnector_intervention"`

That makes the evidence shape line up with the C-first headers while keeping
the runtime harness independent of compiled adapter code.

`common/src/capabilities.c` provides C-first descriptor helpers for future
connector code. The active Python/Shell runners mirror the same metadata names
without FFI.

## New Connector Capability Claims

Future connectors must follow the lifecycle and evidence rules in
[new connector onboarding](new-connector-onboarding.md) before adding capability
claims. A skeleton or roadmap-only connector may describe intended capabilities,
but those descriptions are not verified variables, runtime support, CRS support,
or Full-Matrix coverage. Capability support begins only when a targeted runtime
case produces `result.json` plus logs/evidence, and production capability status
requires Full-Matrix evidence.
