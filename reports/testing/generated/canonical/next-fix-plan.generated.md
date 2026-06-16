> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T07:21:25Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Make target: `generate-remaining-failure-analysis`
> Owner: `connector`
> Severity: `important`
> Connector SHA: `1e0c825de82d1325b5e7b070a4916de2f5af2207`
> Framework SHA: `unknown`
> Input status: `complete`

# Next Fix Plan

Generated at: `2026-06-16T07:21:25Z`

Native MRTS Apache/NGINX remains separate infrastructure evidence; this plan targets connector Full-Matrix leftovers only.

## Recommendation
- Empfohlener nächster Fix-Cluster: `nginx_with_crs_with_mrts_http500_cluster`
- Begründung: largest verified Full-Matrix blocker; all HTTP-500 rows share the /index.html redirect-cycle/docroot-permission signature
- Nicht als nächstes bearbeiten: `phase4_hard_abort_capability`, weil requires transport-abort proof plus Phase 4 intervention logs; do not solve with Expected/PASS changes.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil large count but likely semantic; needs native/libmodsecurity comparison before fixes.
- Nicht als nächstes bearbeiten: `nolog_expected_no_audit`, weil classification-only: explicit nolog means the matching rule should not emit audit evidence.
- Nicht als nächstes bearbeiten: `response_header_mrts_detection_only`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action.
- Nicht als nächstes bearbeiten: `with_mrts_detection_only_non_disruptive`, weil classification-only: with-MRTS DetectionOnly overlay suppresses disruptive request-side action.
- Nicht als nächstes bearbeiten: `xml_processor_activation_missing`, weil classification-only: XML body and Content-Type exist, but these fixtures do not enable ctl:requestBodyProcessor=XML.
- Nicht als nächstes bearbeiten: `multipart_processor_activation_missing`, weil classification-only: multipart body, Content-Type, and boundary exist, but these fixtures do not enable request body access before expecting FILES/ARGS_NAMES collections.
- Nicht als nächstes bearbeiten: `collection_name_normalization_semantics`, weil metadata-only: loaded rules have no match evidence; needs native/libmodsecurity comparison before runtime fixes.

## P0
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| nginx_with_crs_with_mrts_http500_cluster | 510 | nginx | largest verified Full-Matrix blocker; all HTTP-500 rows share the /index.html redirect-cycle/docroot-permission signature | move NGINX Full-Matrix harness roots out from under /root or block inaccessible worker docroots before runtime classification | medium | targeted NGINX with-crs/with-mrts case, make verified-full-matrix-job CONNECTOR=nginx CRS=with-crs MRTS=with-mrts |
| nginx_actual_500 | 1138 | mixed | previously resolved cluster reappeared | stop and triage regression before new work | high | regenerate full matrix, targeted smoke for affected connector |

## P1
- None.

## P2
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| response_header_backend_setup | 12 | apache, nginx | specialized Phase 3 response-header probes need deterministic backend headers before connector behavior can be judged | add or route deterministic Content-Type, Location, and Set-Cookie response headers in the harness/backend path | low to medium | targeted response-header cases, make smoke-apache, make smoke-nginx |
| multipart_files | 46 | apache, nginx, haproxy | remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits | compare multipart variable population across connectors with one representative request | medium | targeted multipart cases, connector smoke for touched connector, full matrix if parser behavior changes |

## P3
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| phase4_hard_abort_capability | 352 | apache, nginx, haproxy | Phase 4/RESPONSE_BODY now requires hard-abort evidence, not status-only denial | stabilize NGINX strict evidence; classify Apache/HAProxy gaps until real transport abort evidence exists | high if promoted prematurely or faked | phase4 hard-abort report regeneration, targeted strict Phase 4 connector evidence, native report regeneration |
| transformation_semantics | 88 | apache, nginx, haproxy | largest semantic cluster; likely needs native/libmodsecurity comparison before any fix | deeper semantic evidence, not harness routing | high | targeted transformation cases, native comparison where available |

## P4
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| rule_chain_semantics and small single-connector leftovers | 110 | mostly nginx for connector-only leftovers | small connector-only leftovers after report-only and not-next groups are excluded | focused per-case triage only when runtime-fixable evidence remains | low to medium | targeted single-case smokes |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `7f47c0da56cd0c800820d9694f15ad2735f15195e17ba8122a73c033f330de6a` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
