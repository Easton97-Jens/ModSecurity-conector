# PR #382: review and merge-decision status

**Language:** English | [Deutsch](pr-382-merge-readiness.de.md)

## Current instruction and Sonar authority

The user requested removal of the PR-specific Sonar work, use of the mandatory master implementation, a normal push and then a pause. This supersedes the custom coverage completion and Sonar-remediation plan. Master `9f44647593bac7947113558c6ad183ab118e80af` (#420) remains merged.

`.github/workflows/sonarqube.yml`, the scope checker, its tests and scanner properties follow that master implementation. Only the existing canonical Python minor (3.15), setup-python pin (7.1.0) and action-owner casing are aligned with this PR’s toolchain and central lock. C++17 remains required; C++20/23 remain advisory. Its scanner still waits for the actual Quality Gate. The additional PR coverage producer, artifact transport/verifier, source-role generator/alternate properties and custom zero-findings/duplication gates are removed.

The master workflow intentionally retains its own Python scope tests and four explicit Go tests. They are not replaced by the Parent inventory. Its actual server processing, imported coverage and final Quality Gate require current-head provider evidence; earlier measurements do not prove this change passed.

## Retained Parent work

The one Parent inventory now contains **932 expanded cases / 536 executions**: **89 core cases / 69 executions** and **843 explicitly authorized offline Python exceptions / 467 executions**. The core ceiling remains 100 and admission still rejects overflow before starting selected processes. Deleted custom Sonar controls and the scope tests now owned by master were retired from that inventory; remaining source bindings and the non-executable specialist archive are regenerated. No global 100-case claim includes the mandatory, separate master Sonar selection.

Connector E2E remains at **26 cases**. Historical I12 host/matrix/oracle campaigns remain closed, with no new `I12_COMPLETE`. Framework/MRTS repositories and gitlinks remain unchanged. Go, Python and Actions maintenance updates, the inventory runner and its offline process/network guards remain in place. The unpublished pre-pause work is retained in a named stash and checksum-verified external checkpoint rather than included in this correction.

## Evidence and delivery limits

The last completed custom-pipeline analysis is historical `3baaffb7b5dd30f05fc9d81ea58da5bd06a2244f`, analysis `c460fc88-86c3-48eb-87da-e795b94b0990`: 12.9% overall / 31.0583536721% New-Code coverage and 17 findings. It is not evidence for the restored master pipeline. No coverage target, Quality Gate, baseline or server finding is changed by this correction.

The [historical checklist](pr-382-checklist.md), [handoff](pr-382-i12-handoff.md) and [reduced I12 closeout](pr-410-i12-closeout-20261024.md) retain their original revisions. #410 is integrated. Repository and Dependabot `SONAR_TOKEN` metadata were verified earlier without reading values. Actual future maintenance PR creation remains a separate operation after authorized master integration.

After the correction is pushed, work pauses at the user’s request. The [PR description and checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) bind the actual published head and provider status. The PR remains Draft; no Ready/`verified_pr`, merge into master, release or deployment is claimed.

[Restoration Change Record](../reports/audits/change-records/CR-20261025-pr382-master-sonar.md) · [Testing and retained archive](testing-and-evidence.md) · [Master Sonar implementation](sonarqube-analysis.md).
