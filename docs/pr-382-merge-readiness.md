# PR #382: review and merge-decision status

**Language:** English | [Deutsch](pr-382-merge-readiness.de.md)

## Current snapshot

PR #382 remains Draft. A retained earlier published Parent checkpoint is `542a98bc20a16f885f114375bfa5225a9364dcf2`: all three broad Sonar jobs (C++17/20/23) completed `SUCCESS` in [run 40355343071](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40355343071). This result belongs to that revision. The current twelve-target native security and Ubuntu 26.04 changes have no published-head Hosted proof and do not inherit its success.

Coverage is excluded from the user's security and merge criteria. `sonar.coverage.exclusions=**` affects coverage only. The authoritative master pipeline, source analysis, security rules, profiles and gates remain; only root `modules/**` and root `reports/**` are excluded from source/test scope. Genuine code/security findings and applicable current-head verification remain the priority.

The twelve development captures total 611 Parent TU compilations, with repeated Common inputs, and remain `import_eligible=false`. They prove build contexts rather than Hosted taint/CTU, parse/index quality or terminal server/gate completion. See the [native security guide](sonarqube-native-security.md) and [native Change Record](../reports/audits/change-records/CR-20261026-sonar-native-security.md).

## Local validation and delivery boundaries

Core selection remains 97 cases / 77 executions; connector E2E remains 26 cases. Historical I12 host, matrix and Oracle campaigns stay closed, without `I12_COMPLETE`. Parent's Framework gitlink remains unchanged; MRTS remains read-only.

The post-master integrated selection passed **94 executions / 342 expanded cases, zero skips**, at inventory `e13c73b981fd1399fbe0c161a8abd753d6cbc4d429957caa86d7c33e1f59bf7c`. The inventory declares 1992 cases / 918 executions: 97 core cases / 77 executions plus 1895 authorized offline cases / 841 executions, with 614 source bindings and 1,672,802 bytes. The selection includes eight inventory controls including overflow rejection and seven broker selectors / 36 cases, as well as the corrected helper capture-path and isolated NGINX archived-contract controls. The earlier 79/298 pass at `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be` is a pre-merge checkpoint. Local green results do not prove Hosted native12 analysis.

The user-approved broker [PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422) was normally squashed at expected head `3d633ee27b48b64b940042e278c157f1aa629679` into master revision `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`; provider readback verified the merge. Independent final review of all seven files found no concrete finding. All six PR ruleset checks and terminal C++17/20/23 Sonar results passed at that exact PR head. The Parent caller now pins broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` and its actual Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; the Parent gitlink is unchanged. Protected self-hosted labels and the master uniform-runner validator remain intact; the duplicate coverage exclusion property was reduced to one declaration. No protected broker manual runtime or expanded connector E2E was run. Authorization covered only #422 and the caller-pin follow-up, not a #382 merge.

All six master ruleset checks passed at `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`. Master C++17 Sonar actually failed with Security E / Reliability E against a `previous_version` baseline from May 14; read-only review found 20 pre-existing security/reliability issues, none introduced by #422; five native triggers are already removed in #382. No passing master Sonar gate is claimed. These master results are separate from the successful exact PR-head analysis. The PR delivery record must bind the exact Parent native12/Ubuntu commit and fresh CI without transferring older successes.

Separate [Framework Draft PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) is now published at `5bffa21d3dd49d3ca647e89eebe005b8421b0812`, retaining 31 Ubuntu 26.04 runner fields. The coordinator passed 86 local methods with zero skips; at last readback ten of twelve CI workflows succeeded, with Sonar SDK and scaffold checks pending. The earlier `5ef4dc3c815c97121578cd34382b80088b9c61ec` analysis genuinely executed C/Python taint and its gate became `OK` after source-backed false-positive readback, but that result is stale for the new head. No current Framework final gate or Parent gitlink import is claimed.

## Retained historical evidence

- At `c924e7585fc0bd197fbefa0ba0f8bbc8cb39aea7`, [run 40301499973](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40301499973) reached terminal server processing `SUCCESS` with gate `ERROR`, 10 open new findings and 26.409% new-code coverage against the then-applicable 80% condition. Twenty other automatic workflows passed. Nineteen individually justified context findings were read back as `RESOLVED` / `FALSE-POSITIVE`. These are historical dispositions and results, not current-head closure.
- At `67e363d44d5f6be7119eb6d76ade11ac75e95f42`, Sonar failed with 118 new findings and 0.81499% new-code coverage. Twenty other workflows and manual [No-CRS run 40277060029](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40277060029) passed at that revision.
- PR #421 source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8` had passing gates and native parsing/include quality 100/100. Its [closeout](sonarqube-pr421-closeout.md) preserves exact receipts and separate architecture, analyzer and taint limitations. Its coverage figures are historical, with no current acceptance role.

The [historical checklist](pr-382-checklist.md), [handoff](pr-382-i12-handoff.md), [reduced I12 closeout](pr-410-i12-closeout-20261024.md), [master-integration record](../reports/audits/change-records/CR-20261026-pr382-master421-merge.md) and [remediation record](../reports/audits/change-records/CR-20261026-pr382-sonar-remediation.md) retain revision-bound details; #410 is integrated. No historical PASS transfers to the dirty integration tree. Fresh final inventory admission, targeted regressions, published-head CI/native analysis and fresh verification of the integrated broker pins remain necessary before readiness changes. No Ready/`verified_pr`, master merge, release or deployment is established.

[Testing and retained archive](testing-and-evidence.md) · [Broad Sonar analysis](sonarqube-analysis.md).
