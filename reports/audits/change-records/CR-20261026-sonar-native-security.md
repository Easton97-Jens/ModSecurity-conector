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

Preserve broad Parent analysis and its root modules/reports exclusions. Capture each of twelve independent native targets with real compiler arguments, exact source/header membership and a clean analyzed revision; keep SDK identity and credentials confined. Completion requires actual Hosted taint/CTU, parse/index and terminal server/gate evidence, followed by source-based finding treatment. Preserve the 100-case core cap, connector E2E 26, closed historical I12 campaigns, unchanged Parent gitlink and read-only MRTS. These completion criteria are not yet all satisfied.

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

The post-master integrated selection passed **94 executions / 342 expanded cases, zero skips**, at inventory `e13c73b981fd1399fbe0c161a8abd753d6cbc4d429957caa86d7c33e1f59bf7c`. The inventory declares 1992 cases / 918 executions: 97 core cases / 77 executions plus 1895 authorized offline cases / 841 executions, with 614 source bindings and 1,672,802 bytes. The selection includes eight inventory controls including overflow rejection and seven broker selectors / 36 cases, as well as the corrected helper capture-path and isolated NGINX archived-contract controls. The earlier 79/298 pass at `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be` is a pre-merge checkpoint. Local green results do not prove Hosted native12 analysis.

The user-approved broker [PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422) was normally squashed at expected head `3d633ee27b48b64b940042e278c157f1aa629679` into master revision `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`; provider readback verified the merge. Independent final review of all seven files found no concrete finding. All six PR ruleset checks and terminal C++17/20/23 Sonar results passed at that exact PR head. The Parent caller now pins broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` and its actual Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; the Parent gitlink is unchanged. Protected self-hosted labels and the master uniform-runner validator remain intact; the duplicate coverage exclusion property was reduced to one declaration. No protected broker manual runtime or expanded connector E2E was run. Authorization covered only #422 and the caller-pin follow-up, not a #382 merge.

All six master ruleset checks passed at `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`. Master C++17 Sonar actually failed with Security E / Reliability E against a `previous_version` baseline from May 14; read-only review found 20 pre-existing security/reliability issues, none introduced by #422; five native triggers are already removed in #382. No passing master Sonar gate is claimed. These master results are separate from the successful exact PR-head analysis. The PR delivery record must bind the exact Parent native12/Ubuntu commit and fresh CI without transferring older successes.

Separate [Framework Draft PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) is now published at `5bffa21d3dd49d3ca647e89eebe005b8421b0812`, retaining 31 Ubuntu 26.04 runner fields. The coordinator passed 86 local methods with zero skips; at last readback ten of twelve CI workflows succeeded, with Sonar SDK and scaffold checks pending. The earlier `5ef4dc3c815c97121578cd34382b80088b9c61ec` analysis genuinely executed C/Python taint and its gate became `OK` after source-backed false-positive readback, but that result is stale for the new head. No current Framework final gate or Parent gitlink import is claimed.

## Security impact

The source/credential contract rejects changed checkout, source-replacing steps, unreviewed environments, alternate scanner/project/SCM settings and token reuse. SDK restoration is constrained to the verified same-run prefix. Parent headers must be actual compiler dependencies, not scope-only aliases. Go producer transitions and the narrow Apache internal-LTO limit retain explicit evidence boundaries. Negative controls address real admission paths; this configuration is not a proof that the application is vulnerability-free.

## Runtime evidence

No application, evaluator, connector host, lifecycle, matrix or Oracle campaign was executed for these captures. Development compilation/export and C++ artifact parity prove their own build layers only. They produce neither I12_COMPLETE nor host qualification.

## Known limitations

All twelve retained development captures use product revision `542a98bc20a16f885f114375bfa5225a9364dcf2` with development helper revisions and `import_eligible=false`. Apache uses installed APXS/APR context and does not retain internal GCC LTO/debug temporary bytes. External SDK/upstream implementation, Go/C cross-language taint, unconsumed header-only C++ wrappers and three I12 instrumentation C++ sources are outside the new native taint proof; the maintained Parent files remain in the broad source scope. First native project analyses may require genuine default-branch baselines and authorized tokens. Full limits and derived capture counts are in the paired native guide.

## Remaining risks

Hosted compiler/parser compatibility, retained CTU context, actual Parent indexing, taint enablement and live findings remain unverified. A successful upload or an older broad gate cannot close those gaps. No fake baseline, source mapping, whole-program claim or passing result may substitute for missing evidence.

## Checks not run and rationale

The documentation worker ran no functional tests, builds, scanner, provider mutations, Git writes or runtime campaigns. The current admitted offline selection passed; clean published-head Hosted/server results remain coordinator-owned and pending. Historical I12 campaigns remain intentionally closed. Framework CLI/updater work belongs to separate Framework PR #138; Parent gitlink and MRTS are unchanged.

## Final diff and review status

Prepared documentation and native implementation remain under coordinator integration and review. No native Hosted completion, Ready-for-review or verified_pr claim is made. No Parent PR #382 merge, release or deployment is authorized.
