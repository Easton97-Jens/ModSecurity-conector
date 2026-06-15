> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T08:49:03Z`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Make target: `generate-remaining-failure-analysis`
> Owner: `connector`
> Severity: `important`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `unknown`
> Input status: `complete`

# Full Run Evidence

Generated file - do not edit manually.

<!-- no-mrts-intervention-nomatch-analysis:start -->
## No-MRTS Intervention No-Match Analysis
- Report: `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md`
- Scope: 105 no-MRTS expected 403 / actual 200 rows where the rule is loaded but no match evidence is visible.
- This is analysis-only evidence; Expected statuses and runtime PASS/FAIL values remain unchanged.
<!-- no-mrts-intervention-nomatch-analysis:end -->

<!-- remaining-failure-analysis:start -->
## Remaining Failure Analysis
- Remaining failure analysis: `reports/testing/generated/canonical/remaining-failure-analysis.generated.md`
- Next fix plan: `reports/testing/generated/canonical/next-fix-plan.generated.md`
- Phase 4 hard-abort capability: `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md`
- Nolog audit evidence: `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md`
- Response header hook analysis: `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md`
- These reports analyze connector Full-Matrix leftovers and keep Native MRTS evidence separate.
<!-- remaining-failure-analysis:end -->

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |

<!-- body-processor-analysis:start -->
## Body Processor Analysis
- Body processor analysis: `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md`
- URL-encoded/form rows: **0** -> **0** active request_body_processor rows after report sync.
- XML processor activation-missing rows: **0** -> **0** active xml_processor rows after report sync.
- Multipart processor activation-missing rows: **0** -> **0** active multipart_files rows after report sync.
- The URL-encoded rows have body and Content-Type evidence and are kept as report-only with-MRTS DetectionOnly overlay cases.
- The XML rows have body and XML Content-Type evidence, but their fixtures do not enable the XML request body processor.
- The Multipart rows have body, Content-Type, and boundary evidence, but their fixtures do not enable request body access before expecting FILES/ARGS_NAMES collection evidence.
<!-- body-processor-analysis:end -->

<!-- rule-chain-semantics-analysis:start -->
## Rule Chain Semantics Analysis
- Report: `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md`
- Rule-chain failure rows: **6**
- Runtime-fixable candidates: **0**
- The report keeps Expected status and runtime PASS/FAIL unchanged while classifying report-only Rule-Chain and single-connector leftovers.
<!-- rule-chain-semantics-analysis:end -->

<!-- final-consistency-audit:start -->
## Final Consistency Audit
- Report: `reports/testing/generated/canonical/final-consistency-audit.generated.md`
- Recommended next fix cluster: `none`
- Release readiness: `ready_with_known_reported_gaps`
- This is an audit-only report; Expected statuses and runtime PASS/FAIL values remain unchanged.
<!-- final-consistency-audit:end -->
