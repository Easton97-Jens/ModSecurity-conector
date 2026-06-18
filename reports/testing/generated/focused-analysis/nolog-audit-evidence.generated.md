> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:14:49Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-nolog-audit-evidence-analysis.py`
> Make target: `generate-nolog-audit-evidence-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
> Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
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
- `classification_only` rows before: **597**
- `classification_only` rows after: **603**

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

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `688762427074ee4fe85f65bae9343d7793d418a3c486e220b368ec833bb59fa3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `94ef7376661e451a7c3a25bd98cb9b769096cd64fe85684fa62e6cef951a017e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `ec48bccf0bc05f6f9659cedf12e644480f3377e42f8120d2c55df42d4e910970` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
