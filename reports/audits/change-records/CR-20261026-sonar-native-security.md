# Change Record: CR-20261026-sonar-native-security

**Language:** English | [Deutsch](CR-20261026-sonar-native-security.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261026-sonar-native-security |
| Date (UTC) | 2026-10-26 |
| Base revision | `542a98bc20a16f885f114375bfa5225a9364dcf2` |

## Motivation and problem statement

The broad CFamily AutoConfig scan cannot perform C/C++ taint analysis. The user requested a full security assessment across the maintained languages, including genuine C/C++ build contexts, while preserving the authoritative master pipeline. Coverage is explicitly irrelevant to the security and merge decision.

## Acceptance criteria

Preserve broad Parent analysis and its root modules/reports exclusions. Capture each of twelve independent native targets with real compiler arguments, exact source/header membership and a clean analyzed revision; keep SDK identity and credentials confined. Completion requires actual Hosted taint/CTU, parse/index and terminal server/gate evidence, followed by source-based finding treatment. Preserve the shared 100-case automatic cap, connector E2E 26, closed historical I12 campaigns, unchanged Parent gitlink and read-only MRTS. The final delivery decision must use current-head evidence on PR #382.

## Implementation decision and rationale

Add a separate twelve-project native workflow instead of replacing the broad scan with a partial or combined database. Use the canonical shared ModSecurity 3.0.17 SDK and same-run artifact ID/producer-root outputs. Verify revision, source/build provenance and archive/library digests; reject escaping archive members/links and unsafe external output ancestry. Capture successful real compiler invocations, preserve pre-execution original-source/include equivalence and validate one declared link graph per target. Request taint and CTU with filesystem cache, resource preflight and gate waiting. Coverage-only exclusion follows the explicit user decision; no security rule/profile/gate is relaxed.

## Changed files

- `.github/workflows/sonar-native-security.yml`; `ci/checks/analysis/prepare-sonar-native-ci.py`; the seven helpers under `ci/checks/analysis/sonar-native-security/`.
- Five focused test modules: `tests/test_sonar_native_security.py`, `tests/test_sonar_native_security_capture.py`, `tests/test_sonar_native_security_go.py`, `tests/test_sonar_native_security_mapping.py`, `tests/test_sonar_native_ci.py`; existing `tests/test_ci_security_workflows.py`.
- Exact updater allowlist/staging entries in `ci/tools/update-workflow-tools.py` and `.github/workflows/update-workflow-tools.yml`; coordinator-owned inventory and generated archive refreshed through their contracts.
- `docs/sonarqube-native-security.md` / `.de.md`, narrow current-mode corrections in `docs/sonarqube-analysis.md` / `.de.md`, and this record pair. The final coordinator diff defines the complete delivered source set.

## Commands executed

The documentation worker created this pair through `rtk bypass` and `ci/tools/new-change-record.py create --name sonar-native-security --base-revision 542a98bc20a16f885f114375bfa5225a9364dcf2 --date 2026-10-26`. Source/workflow and retained JSON reads used RTK. Native documentation checks passed: `rtk make check-bilingual-docs` and `rtk make check-doc-links` with explicit Parent interpreter `PYTHON=/var/tmp/codex/ModSecurity-conector/runs/pr382-integrate410-20261024/python315/venv/bin/python`; link checking additionally used `FRAMEWORK_ROOT=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework`. The RTK-wrapped `ci/tools/new-change-record.py check` passed (structure only), and scoped `git diff --check` passed.

Observed coordinator summary: 34 executions / 98 expanded cases passed with zero skips at inventory `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578`; the summary was read from the retained external run. That checkpoint includes native12 integration but predates Ubuntu migration and later helper changes; it does not validate the current dirty tree. Twelve development build/exports cover 611 Parent TU compilations in aggregate, not unique files. The C++17 evaluator canonical artifact comparison passed without executing the evaluator; SHA-256 `6846b788f1eb1f56e0514ed8e49130d2c045e09e852726683bb2beb4f87e24a4`. Exact build/test procedures and receipts remain with the coordinator; no reconstructed command is presented as executed.

The automatic selection is now 100 expanded cases / 80 executions, including three guard controls. A further 1893 cases / 839 executions are available only through explicit on-demand selection. Automatic coverage catalogue commands were removed; the retained collector requires `--on-demand`. Coverage is irrelevant to merge by user instruction. Broad source/scanner/gate analysis remains enabled, with only root `modules/**` and root `reports/**` excluded.

Framework revision `03da9353561bf632a1f7bfc71b0a2671ec7aa257` passed all twelve CI workflows and Sonar and is Ready; no Framework merge was performed. Parent keeps Framework gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS is unchanged. Broker PR #422 is already user-authorized and merged at `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`; no further master merge is authorized. Protected manual runtime, connector E2E expansion and historical I12 campaigns were not run.

## Security impact

The source/credential contract rejects changed checkout, source-replacing steps, unreviewed environments, alternate scanner/project/SCM settings and token reuse. SDK restoration is constrained to the verified same-run prefix. Parent headers must be actual compiler dependencies, not scope-only aliases. Go producer transitions and the narrow Apache internal-LTO limit retain explicit evidence boundaries. Negative controls address real admission paths; this configuration is not a proof that the application is vulnerability-free.

## Runtime evidence

At published Parent `011cb197`, [run 40392396874](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40392396874) completed SDK preparation and all twelve native build/capture/index/CTU/taint analyses: 611 aggregate compilation units, zero partial units and 100% indexing in each target. Before individual triage, three native gates passed and nine failed. Twenty of 22 workflows passed; the broad C++17/20/23 gates failed. Source review validated 12 Python security issues and 39 native issue instances as false positives; all 36 main/advisory Python instances and 39 native instances are individually resolved as false positive with fresh readback. Original job conclusions remain unchanged. This analysis predates the finite closure commit and is not final-head acceptance. See [central status](../../../docs/pr-382-merge-readiness.md).

No application, evaluator, connector host, lifecycle, matrix or Oracle campaign was executed for these captures. Development compilation/export and C++ artifact parity prove their own build layers only. They produce neither I12_COMPLETE nor host qualification.

## Known limitations

The historical development captures use product revision `542a98bc20a16f885f114375bfa5225a9364dcf2` with development helper revisions and `import_eligible=false`. Apache uses installed APXS/APR context and does not retain internal GCC LTO/debug temporary bytes. External SDK/upstream implementation, Go/C cross-language taint, unconsumed header-only C++ wrappers and three I12 instrumentation C++ sources are outside the new native taint proof; the maintained Parent files remain in the broad source scope. Full limits and derived capture counts are in the paired native guide.

## Remaining risks

The observed twelve-target analysis is complete at `011cb197`; all individually source-reviewed Python/native dispositions have confirming readback; the old job conclusions remain unchanged. No final-head gate pass or application vulnerability-free claim follows from the build/analyzer proof. Central readiness binds the exact final delivery.

## Checks not run and rationale

This documentation update ran no functional tests, builds, scanner or provider/Git mutations. Hosted analysis was observed at the published revision; final-head acceptance and disposition readback remain in [central status](../../../docs/pr-382-merge-readiness.md). Historical I12 campaigns stay closed.

## Final diff and review status

Published Parent `011cb197` has observed twelve-target analysis, not final-head acceptance. Source-reviewed false-positive dispositions have fresh individual readback; final published-head checks remain the delivery criterion. No Parent #382 merge, release or deployment is authorized.
