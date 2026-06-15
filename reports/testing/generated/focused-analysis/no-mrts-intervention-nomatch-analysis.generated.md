> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:30Z`
> Generator: `ci/generate-no-mrts-intervention-nomatch-analysis.py`
> Make target: `generate-no-mrts-intervention-nomatch-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# No-MRTS Intervention No-Match Analysis

- Generated at: `2026-06-15T10:40:30Z`
- no-MRTS expected `403` / actual `200` rows with loaded rule and no match: **0**
- Unique cases: **0**
- Rule not loaded: **0**
- Rule loaded, no match: **0**
- Rule matched, no intervention: **0**
- Intervention created but connector did not return 403: **0**
- Backend reached: **0**

## Cause Groups

| Cause | Count | Likely cause | Safe fixability | Risk | Examples |
|---|---|---|---|---|---|

## Connector / Phase / Target / Operator

### Connectors
| Value | Count |
|---|---|

### Phases
| Value | Count |
|---|---|

### Targets
| Value | Count |
|---|---|

### Operators
| Value | Count |
|---|---|

### Source categories
| Value | Count |
|---|---|

### Classifications
| Value | Count |
|---|---|

### Work directions
| Value | Count |
|---|---|

### Priorities
| Value | Count |
|---|---|

## Native Comparator

- Status: `no native comparator`
- Matching native case IDs: `-`
- Reason: Native MRTS reports cover upstream MRTS target cases; these 105 rows are framework-owned no-MRTS connector cases.
- Native Apache status: `NOT_RUN`
- Native NGINX status: `NOT_RUN`

## Safe Subcluster Decision

- Selected: **no**
- Cluster: `none`
- Count: **0**
- Reason: No small safe harness/evidence fix was identified. The smallest clear group is phase1_request_body_unavailable_or_empty_body, but changing its body would change the test definition.
- Action: analysis only; no runtime, rule, expected-status, or PASS/FAIL change

## Before / After

| Metric | Before | After |
|---|---|---|
| no-MRTS no-match |  |  |
| intervention_blocking true candidates |  |  |
| P0/P1 intervention_blocking rows |  |  |
| full-matrix pass | 3074 | 3074 |
| full-matrix fail | 782 | 782 |
| full-matrix blocked |  |  |

## Representative Records

| Case | Connector | Variant | Rule | Phase | Target | Operator | Request | Expected value | Classification | Work direction | Priority | Cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Guardrails

- Analysis-only report: no Expected status, runtime PASS/FAIL, rule, request, or MRTS definition was changed.
- No connector/core code fix is recommended from this evidence alone.
- No row shows a generated disruptive intervention that a connector later lost.

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
