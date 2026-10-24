# Evidence-Based Quality Scoring Policy

## Purpose

Use this policy only when the user requests a scored security/quality/readiness assessment. Scoring does not replace test results, code coverage, SonarQube Quality Gate, finding status, or practical connector readiness.

## Predeclare the score

Before scored execution create `scoring-spec.json` containing scope ID/version, criteria IDs, applicable acceptance conditions, maximum points, required check IDs, concrete expectations, and evidence requirements. Do not remove or weaken criteria after seeing results merely to improve the score.

## Fixed 100-point framework

Four areas, each 25 points. Each criterion is worth at most 5 points.

### Framework / integration

- F1 interfaces/CLI/schema compatibility across Parent/Framework/MRTS
- F2 complete relevant discovery with unique IDs and orphan/duplicate detection
- F3 runners execute real assertions; negative controls detect wrong behavior; no empty-run promotion
- F4 correct repository/version/path/environment handoff without silent substitution
- F5 isolation, repeatability, output ownership, and cleanup

### CI / delivery

- C1 workflow syntax/triggers/filters/dependencies/matrix consistency
- C2 permissions, secret handling, and untrusted-input boundaries
- C3 pinned/provenance-controlled actions/images/caches/artifacts and isolation
- C4 applicable local equivalents of CI build/test/security steps actually execute with meaningful assertions
- C5 current remote results/revisions/job scope/quality decisions are correctly attributed; repeated failures/flakiness are investigated

### Dependencies / supply chain

- D1 direct/transitive dependencies and tools inventoried with actual versions/provenance
- D2 locks/pins/hashes/signatures/download/archive controls satisfy the declared contract
- D3 Python/Go/C/C++/host/library/API/ABI compatibility is execution-backed
- D4 current advisories for the concrete inventory have no unresolved applicable risk above the declared threshold
- D5 materialization/installation is reproducible, task-local, and free of silent global fallback

### Code quality / security

- Q1 compiler/syntax/lint checks satisfy unchanged project requirements
- Q2 type/API/error/edge-case contracts are validated
- Q3 memory/lifetime/bounds/concurrency/trust-boundary checks and validated security findings are reconciled
- Q4 complexity/duplication/maintainability satisfy predeclared measurable thresholds using current metrics
- Q5 critical functional/error/regression paths have meaningful tests and fresh coverage/Quality-Gate evidence where applicable

## Criterion calculation

For criterion `i`:

`p_i = 5 × fulfilled_applicable_conditions / applicable_conditions`

No evidence for an applicable condition earns zero points for that condition; it is not automatically a product failure.

For the displayed assessment score:

`score = 100 × earned_points / applicable_max_points`

True `not_applicable` criteria leave the denominator only with concrete technical justification. Missing tools, access, time, test environment, or implementation are not automatically non-applicable.

100% means all applicable declared acceptance conditions are evidenced. It does not mean universal security or production approval.

## Separate metrics

Report separately:

- test completeness;
- test success rate;
- measured code coverage;
- SonarQube Quality Gate;
- security findings;
- connector practical readiness;
- assessment score.

Do not convert one into another.

## Validation

Calculate programmatically from `scoring-spec.json` and actual results. Validate at least: all conditions fulfilled -> 100%; none -> 0% with positive denominator; 4/5 -> 80%; true N/A denominator reduction; missing relevant evidence remains in denominator; all N/A -> no percentage; duplicate criteria/cases rejected; values just below 100% are not rounded to 100%.
