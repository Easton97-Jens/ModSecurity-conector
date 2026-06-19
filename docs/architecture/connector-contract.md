# Connector Contract

Status: evidence-scoped contract for the productive Apache, NGINX, and HAProxy
connectors.

This contract describes the artifact and evidence shape that a connector must
provide to participate in `verified-case` and the full runtime matrix. It does
not promote new behavior and it must not be used to edit expected statuses or
PASS/FAIL values. Capability claims are valid only when backed by live runtime
evidence or generated reports that were produced from verified inputs.

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

## Required Connector Artifacts

A productive connector must keep the following repository shape:

- `connectors/<name>/src/` for adapter-owned or adapter-integrating source.
- `connectors/<name>/harness/` for connector-local runtime entrypoints and
  README notes.
- `connectors/<name>/docs/` for build, validation, architecture, and capability
  boundaries.
- `connectors/<name>/metadata.c` and `metadata.h` for connector metadata.
- `connectors/<name>/ORIGIN.md` and source-map/license records for imported or
  adapted source provenance.

Runtime evidence is written outside the checkout, normally below
`/var/tmp/ModSecurity-conector-verified`, and versioned generated reports under
`reports/testing/generated/` are refreshed only through generators.

## Required Case Evidence

Each `verified-case` run should provide:

| Artifact | Requirement |
| --- | --- |
| `case-run.json` | Run envelope with connector, case, CRS/MRTS variant, command, duration, copied artifacts, official mismatch context, and `full_matrix_refresh_needed`. |
| `case-run.md` | Human-readable summary with request metadata, evidence links, rule evidence, log excerpt, and next-step commands. |
| `result.json` | Machine-readable outcome with `status`, `expected_status`, `actual_status`, and a clear `reason` or connector-specific evidence fields. |
| Logs | Connector runtime logs sufficient to explain the observed status: access/error/audit for Apache and NGINX; HAProxy/SPOP/backend/audit logs for HAProxy. |
| Decision stream | Use `decision.jsonl` or an equivalent structured artifact when the connector has a decision transport separate from HTTP status. HAProxy uses this as primary evidence. |

`result.json` must never be hand-edited to force PASS/FAIL. If the harness
cannot produce a runtime result, it may write `status: missing_result` with a
reason, but that is diagnostic evidence rather than a passing runtime case.

## Decision Evidence Model

The normalized decision model is:

| Field | Meaning |
| --- | --- |
| `expected_status` | YAML expected HTTP status for the selected case and variant. |
| `actual_status` | HTTP status observed through the live connector path. |
| `status` | Harness outcome such as `pass`, `fail`, `blocked`, or `missing_result`. |
| `rule_id` | Matched rule identifier when known; for HAProxy `rule_id=0` means no rule match. |
| `decision` | Connector decision label, for example HAProxy `pass` or `deny`. |
| `intervention_status` | ModSecurity disruptive intervention status when available. |
| `classification` | Generated report classification for known boundaries; not a replacement for raw evidence. |

## Capability Boundaries

| Boundary | Classification | Contract |
| --- | --- | --- |
| NGINX late phase-4 response-body enforcement | `nginx_phase4_response_body_enforcement_gap` | Phase-4 response-body rule matches and audit/rule evidence can exist, but late disruptive enforcement may still return HTTP 200. Do not promote this as hard blocking without targeted evidence. |
| MRTS DetectionOnly overlay | `with_mrts_detection_only_overlay` | `with-mrts` can set `ctl:ruleEngine=DetectionOnly`; disruptive actions are intentionally non-blocking in those variants. |
| HAProxy no-match decision records | Decision evidence, not a mismatch | In `decision.jsonl`, `rule_id=0` means no rule match. `decision=pass`/`deny` and `intervention_status` are central to interpretation. |
| Apache rule-detail shape | Capability note | Apache is the reference-near control connector for many cases, but some harness logs expose less structured rule-match detail than NGINX/HAProxy. |

## Full-Matrix Readiness

A connector is full-matrix-ready when all of the following are true:

1. The framework can discover and materialize the selected YAML cases without
   connector-local duplication of rule/request/expected-status data.
2. Runtime jobs write per-case `result.json` files and copy logs/audit/decision
   evidence into stable artifact directories.
3. Generated reports are refreshed by `make refresh-connector-reports` or the
   relevant generator targets, not by manual edits.
4. Critical mismatch count remains zero and merge-readiness remains PASS.
5. New behavior changes have targeted before/after evidence and affected
   full-matrix jobs are rerun with `--force` or the documented equivalent.
