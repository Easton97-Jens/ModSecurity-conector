# Capability Model

Capabilities describe what a YAML case exercises. They are evidence labels, not
automatic skips. A capability is counted as verified only when a real connector
smoke case passes through Apache or NGINX.

Capability metadata is not connector proof on its own. API-only smokes,
mapped-only inventory entries, former expected-failure probes, blocked cases, and generated
coverage rows do not add verified variables.

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

## Connector Capability Boundaries

The productive connectors share the evidence and lifecycle contract in
`docs/architecture/connector-contract.md`. This model intentionally summarizes
capability status instead of duplicating the contract. The terms below are used
consistently:

| Term | Meaning |
| --- | --- |
| `supported` | Covered by current verified connector evidence for the documented cases. |
| `bounded` | Works only inside an explicitly documented limit, such as HAProxy SPOE frame/body limits. |
| `evidence-scoped` | Valid only for cases and variants represented by verified inputs or generated reports. |
| `not-promoted` | Evidence may exist, but the capability must not be advertised as generally supported or counted as a verified variable. |
| `diagnostic-only` | Useful troubleshooting evidence, such as `missing_result`, that must never count as runtime PASS. |

| Capability | Apache | NGINX | HAProxy | Evidence Basis |
| --- | --- | --- | --- | --- |
| Request blocking | supported / evidence-scoped | supported / evidence-scoped | supported / evidence-scoped | Live connector runtime cases and full-matrix evidence. |
| Request body | supported / evidence-scoped | supported / evidence-scoped | bounded / evidence-scoped | Verified URL-encoded/body cases; HAProxy bounded by request buffering and SPOE framing. |
| XML body processor | evidence-scoped | evidence-scoped | bounded / evidence-scoped | Body-processor cases and generated body-processor analysis. |
| JSON body processor | evidence-scoped | evidence-scoped | bounded / evidence-scoped | Request-body cases and runtime matrix evidence. |
| Multipart | evidence-scoped | evidence-scoped | bounded / evidence-scoped | Multipart/files cases; HAProxy limited to proven request-body transport size/framing. |
| Response body match | not-promoted except focused evidence | supported for phase-4 match evidence | bounded / evidence-scoped | Focused phase-4/response-body evidence and audit/decision artifacts. |
| Response body enforcement | not-promoted | not-promoted for late disruptive phase-4 hard blocking | bounded strict-abort only / not-promoted generally | `nginx_phase4_response_body_enforcement_gap` and bounded HAProxy phase-4 evidence. |
| Audit log | evidence-scoped; less structured in some cases | evidence-scoped with rule/audit messages | evidence-scoped paired with decisions | Audit artifacts copied by runtime/verified-case jobs. |
| CRS | evidence-scoped | evidence-scoped | evidence-scoped | With-CRS matrix variants. |
| MRTS | evidence-scoped | evidence-scoped | evidence-scoped | With-MRTS matrix variants and MRTS native/focused evidence. |
| DetectionOnly overlay | classified boundary | classified boundary | classified boundary | `with_mrts_detection_only_overlay`; not a connector bug when DetectionOnly is applied. |
| `verified-case` | complete only with real runtime `result.json`; otherwise diagnostic-only | complete only with real runtime `result.json`; otherwise diagnostic-only | complete only with real runtime `result.json`; otherwise diagnostic-only | `case-run.json`, `case-run.md`, copied logs, and runtime `result.json`. |
| Full matrix | official counts only from complete fresh jobs | official counts only from complete fresh jobs | official counts only from complete fresh jobs | Full-matrix manifests, per-job `job.json`, copied logs, and generated reports. |
| Native oracle relevance | explanatory only | explanatory only | explanatory only | Native evidence can explain libmodsecurity semantics but cannot replace connector matrix evidence. |

Known boundaries remain:

- NGINX can produce phase-4 response-body rule-match and audit evidence, but
  late disruptive response-body enforcement can still return HTTP 200. This is
  classified as `nginx_phase4_response_body_enforcement_gap`.
- MRTS `with-mrts` runs may set `ctl:ruleEngine=DetectionOnly`; disruptive
  actions are then intentionally non-blocking and classified as
  `with_mrts_detection_only_overlay`.
- HAProxy uses SPOA/SPOP `decision.jsonl` records as structured decision
  evidence. `rule_id=0` means no rule match; `decision=pass` or `deny` and
  `intervention_status` are central fields.
- Apache remains the reference-near control connector for many cases, but some
  harness logs expose less structured rule-match details than NGINX/HAProxy.

These notes document evidence boundaries only. They do not change YAML
expectations, generated PASS/FAIL values, report classifications, or connector
request processing.
