> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:39:59Z`
> Generator: `ci/generate-nolog-audit-evidence-analysis.py`
> Make target: `generate-nolog-audit-evidence-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# Nolog Audit Evidence Analysis

Generated file - do not edit manually.

## Scope
- Case: `v3_action_nolog_pass_no_audit`
- Extracted runtime rows: **12**
- Metadata-only reclassified rows: **6**
- Connectors: apache, haproxy, nginx
- Variants: no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts

## Rule Semantics
- Rule ID: `3326`
- Phase: `1`
- Target: `ARGS:foo`
- Actions: `id:3326, phase:1, nolog, pass, msg:'v3 imported nolog pass no audit'`
- has_nolog / has_auditlog: **True / False**
- Request: `GET /?foo=bar&a=xxx`
- Body/content-type: `<empty>` / `-`
- Conclusion: explicit `nolog` means this rule is expected not to produce its own audit entry. A with-CRS audit record for a different CRS rule is not evidence that the nolog rule logged.

## Before/After
- `audit_log_evidence` rows before: **6**
- `audit_log_evidence` rows after: **0**
- `classification_only` rows before: **591**
- `classification_only` rows after: **597**

## Runtime Rows
| Connector | Variant | Status | Expected | Actual | Audit IDs | Decision IDs | Target Rule Logged | Backend | Classification |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | PASS | 200 | 200 | - | - | False | True | nolog_expected_no_audit |
| nginx | no-crs/no-mrts | PASS | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | no-crs/no-mrts | PASS | 200 | 200 | - | 0 | False | True | nolog_expected_no_audit |
| apache | no-crs/with-mrts | PASS | 200 | 200 | - | - | False | True | nolog_expected_no_audit |
| nginx | no-crs/with-mrts | PASS | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | no-crs/with-mrts | PASS | 200 | 200 | - | 0 | False | True | nolog_expected_no_audit |
| apache | with-crs/no-mrts | FAIL | 200 | 200 | 920350 | - | False | True | nolog_expected_no_audit |
| nginx | with-crs/no-mrts | FAIL | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | with-crs/no-mrts | FAIL | 200 | 200 | 920350 | 920350 | False | True | nolog_expected_no_audit |
| apache | with-crs/with-mrts | FAIL | 200 | 200 | 920350 | - | False | True | nolog_expected_no_audit |
| nginx | with-crs/with-mrts | FAIL | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | with-crs/with-mrts | FAIL | 200 | 200 | 920350 | 920350 | False | True | nolog_expected_no_audit |

## Evidence Fields
| Connector | Variant | Method | Path | Query | Expected evidence | Actual evidence | Audit log | Error log | Run log |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | no-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | no-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |
| apache | no-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | no-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | no-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |
| apache | with-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | with-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | with-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |
| apache | with-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | with-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | with-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
