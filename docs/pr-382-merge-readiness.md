# PR #382: review and merge-decision status

**Language:** English | [Deutsch](pr-382-merge-readiness.de.md)

## Current instruction and Sonar authority

The resumed user instruction requires integration of fresh master `7a44f18edac729291d6551d068da64fa3fec4e1e` (PR #421) first. The normal merge from PR #382 head `209ab41a16cc34c88e3dc23d312eada0a38a8169` was published as `c7c60a8300c57f8b0ccd9bd5c35bc4af93c678ba`. The earlier pause is superseded. Follow-up heads and provider results are bound in the PR; no passing final gate or delivery approval is claimed here.

The master-owned Sonar workflow, scope guard, native-context preparation and `run-sonar-coverage.py` are authoritative. C++17 remains required; C++20/23 remain advisory. Each scanner waits for its actual Quality Gate. The integrated toolchain retains Python `3.15.1`, Go `1.27.3`, module language `1.26.9` and setup-python `7.1.0`; Scanner CLI is now `8.2.0.6438`.

Master selects Python behavior recorded in PR #421 as 80 methods, 37 named Go scenarios and native Common helper/constructor/intervention coverage. Methods are not expanded case counts. This assessment remains outside the Parent inventory. Each matrix variant repeats execution cost, not an independently enlarged case catalogue. Guarded default discovery remains; only the fixed 13-entry `PYTHON_TESTS` selection receives a child-only explicit `ON_DEMAND_TESTS=1` environment. No global bypass is enabled. These process/Go/native selections are not the Python offline exception and do not reopen historical I12 campaigns.

The removed PR-specific collector, artifact transport/verifier, source-role generator/alternate properties and custom zero-findings/duplication gates remain removed. Master #421 coverage is its own implementation, not restoration of that pipeline. Earlier unpublished work remains secured in the named stash/checkpoint and is not restored.

## Retained Parent work

The Parent inventory remains **938 expanded cases / 541 executions**: **89 core cases / 69 executions** and **849 explicitly authorized offline Python exceptions / 472 executions**. The core ceiling remains 100; admission rejects overflow before selected processes. Master Sonar selectors are separate, so no global 100-case claim includes them. Remaining inventory source bindings and the specialist archive must match the merged sources.

Connector E2E remains at **26 cases**. Historical I12 host/matrix/oracle campaigns remain closed, with no new `I12_COMPLETE`. Framework/MRTS checkouts and gitlinks are unchanged. Reading the exact pinned Framework contract for approved native headers is passive provenance input, not Framework/MRTS write or qualification authority. Go/Python/Actions maintenance, the inventory runner and offline process/network guards remain in place.

## Evidence and delivery limits

PR #421 source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8` had three successful terminal analyses and gates `OK`: 83.5% PR / 84.6% advisory New-Code coverage, 179 `FIXED` plus 24 `FALSE_POSITIVE` IDs and zero OPEN/CONFIRMED findings/hotspots. Its 136 native units reached parsing/include quality 100/100. These are source-bound PR #421 observations, not evidence for PR #382, the merge result or the larger Parent scope. The [PR #421 closeout](sonarqube-pr421-closeout.md) retains the exact task/analysis bindings and limits.

Architecture application remains externally blocked by HTTP 415; CFamily AutoConfig taint, independent targets/variants, Python/FIFO analyzer limits and the TLS changed-lines warning remain explicit. PR #421 runtime evidence belongs separately to source `900dddb49c43ec4479c4b75a91071cadb97893c4` and proves only its selected runtime scope. No result transfers to the merged head.

The last custom-pipeline analysis remains historical pre-merge `3baaffb7b5dd30f05fc9d81ea58da5bd06a2244f`, analysis `c460fc88-86c3-48eb-87da-e795b94b0990`: 12.9% overall / 31.0583541721% New-Code coverage and 17 findings. It does not qualify the master pipeline. New reports, analyzer import, gate status and runtime qualification require their own revision-bound evidence; no threshold, rule, baseline or finding is changed by this merge documentation.

[Historical checklist](pr-382-checklist.md), [handoff](pr-382-i12-handoff.md) and [reduced I12 closeout](pr-410-i12-closeout-20261024.md) retain their original revisions. #410 is integrated. The [PR description and checks](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) will bind the actual published merge head and provider status. PR #382 remains Draft; no Ready/`verified_pr`, merge into master, release or deployment is claimed.

[Merge Change Record](../reports/audits/change-records/CR-20261026-pr382-master421-merge.md) · [Testing and retained archive](testing-and-evidence.md) · [Master Sonar implementation](sonarqube-analysis.md).

## Compatibility fixes after the first merge

The first hosted merge analysis passed Python coverage and failed before scanner upload because Master selected a Go test name absent from this product branch. The one-for-one selector now uses the existing `TestCheckForwards33ByteBodyWithoutConnectorPolicy`, matching the retained 33-byte forwarding contract. The actual local master Go producer passed all 37 named selectors across four modules and wrote four profiles; its dirty local reports are not import evidence for a published head.

Two report-input regressions were reproduced before their fixes: an explicit external commands receipt was ignored and a separately configured build root lost its diagnostic log. The fixes authorize only the invocation’s exact receipt and configured build root. Manifest-selected external paths and final/intermediate symlinks remain rejected. Five admitted offline executions cover six explicit cases; all passed after the corrections. These six cases explain the increase from the initial merge’s 932 to 938 Parent cases, with no new connector E2E or host campaign. The existing 80-method master Python assessment passed again (118 observed test/subtest cases); the earlier 21 Parent controls also passed. Current-head automatic CI/scanner import and final metrics remain separate required evidence.
