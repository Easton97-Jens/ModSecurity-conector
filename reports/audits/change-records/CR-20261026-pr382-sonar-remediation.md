# Change Record: CR-20261026-pr382-sonar-remediation

**Language:** English | [Deutsch](CR-20261026-pr382-sonar-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261026-pr382-sonar-remediation |
| Date (UTC) | 2026-10-26 |
| Base revision | `67e363d44d5f6be7119eb6d76ade11ac75e95f42` |

## Motivation and problem statement

At the base revision, required Sonar failed with 118 new findings and 0.81499% New-Code coverage against 80%; analysis `e407faad-955f-49f0-9c6e-443e0629cd1c`, CE `AaF2y9jpF1KaAz-cccYD`. The user explicitly requested targeted findings/coverage remediation while preserving the integrated master pipeline and unchanged gates. Twenty other workflows and manual No-CRS run `40277060029` passed only at that historical head.

## Acceptance criteria

Preserve master `7a44f18edac729291d6551d068da64fa3fec4e1e`, mandatory C++17 and advisory C++20/23, genuine report provenance and all gates. Authorize additional offline Python units explicitly while retaining the 100-case core/2 MiB limits. Preserve E2E 26, closed I12 campaigns and read-only Framework/MRTS/gitlinks. Completion still requires a fresh full retention measurement, at least 80% actual New-Code coverage and current published-head required CI/Sonar; these are not yet satisfied.

## Implementation decision and rationale

Apply focused native/Python quality fixes and root/path/metadata/recipe boundary controls. Extend the master coverage producer with exact admitted offline IDs, real child branch tracing and independent raw witness SHA/size receipts. Keep `xml --keep-combined` after reproducing implicit-combine deletion despite `combine --keep`. Preserve fixed 13-entry `PYTHON_TESTS`, 37 Go selectors and native assessment; classify all CFamily MAIN and 16 actual CI Python unittest modules TEST. Increase timeout 30→60 minutes because the measured offline collection/reporting interval alone was at least 1216.9 seconds. Schema 3 deduplicates 592 source records without removing full maps/selectors/cases/validation; schemas 1/2 remain readable. Admission is 1346 cases / 796 executions = 97 core / 77 + 1249 offline / 719. File size is 1,329,032 versus 2,096,001 bytes. Reference graph validation precedes children; publisher proof/no-op behavior and all previous IDs/scenarios remain.

## Changed files

- `.github/workflows/sonarqube.yml`, `sonar-project.properties`, `ci/sonar-coverage.ini`, `ci/checks/analysis/check-sonar-scope.py`, `ci/checks/analysis/run-sonar-coverage.py`.
- `ci/lib/active_test_inventory.py`, `ci/lib/active_inventory_updates.py`, `config/testing/active-cases.json`, generated `reports/testing/test-selection-archive.generated.json`.
- Selected native connector sources and lifecycle fixtures/helpers; Python lifecycle, inventory, updater, coverage and scope controls under `ci/`, `connectors/`, `scripts/`, `tests/`. The final coordinator diff owns the exact source list.
- `docs/pr-382-merge-readiness.md` / `.de.md`, `docs/testing-and-evidence.md` / `.de.md`, `docs/sonarqube-analysis.md` / `.de.md`, and this pair. Historical records are retained.

## Commands executed

The coordinator observed phase 1 PASS: 105 executions / 115 cases, zero skips; strict Apache/NGINX/HAProxy C17 and three SDK C++17 syntax checks passed. Phase 2 union PASS: 182 distinct executions / 314 cases across two inventory digests, including all 145 new executions / 275 cases. An initial fixture namespace literal failed; two test-only paths now derive the configured private root, retaining six scenarios/assertions. Continuation: 74 executions / 168 cases PASS, zero skips, including four reruns. This is not one clean final-revision run. The first actual master Python coverage producer passed 92 methods plus 955 offline cases, 568 child-branch witnesses and one separate untraced timing control; XML contains 374 files. Two targeted raw-retention controls passed. Documentation worker used RTK-wrapped source/text reads, standard-library static heading/link checks and scoped `git diff --check`; no project imports, tests, generator or provider writes. Exact coordinator commands remain in run-scoped evidence; no reconstructed command is asserted here.

The Go static-contract failure came from an exact three-line body expectation rejecting legitimate reviewed cache suffixes. The guard now accepts only that canonical body or the exact Envoy `go.mod` + `go.sum` / Traefik `native/go.mod` job-cache suffix; trusted Go output, pins and resolver are unchanged. Checker CLI plus five selected executions / 18 expanded cases passed with zero skips, rejecting 12 selector/cache drift variants. Actual repository bilingual, documentation-link and path-reference checks passed; actionlint wrapper passed, zizmor reported zero findings, and project pins, Python `3.15.1` / 50 jobs and Go contract checks passed.

At published checkpoint `bcde66f2cf88130c57c7e49a0d5d2a22150948da`, all 20 other automatic PR workflows succeeded. Required Sonar run [40298184503](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40298184503), job `121489276419`, failed before scanning because the isolated Sonar environment lacked PyYAML when admitted selector `offline.maintenance.043` imported `update-workflow-tools.py`. The workflow follow-up invokes existing `ci/tools/install-ci-dependencies.py` in that same virtual environment. It uses the existing hash-bound official PyYAML `6.0.3` source build already approved for Python `3.15.1`; locks and gates are unchanged. The coordinator observed installation PASS in a fresh isolated `3.15.1` environment, then the exact admitted selector PASS: one method, two expanded cases, zero skips. Evidence under `/var/tmp/codex/ModSecurity-conector/runs/pr382-master421-resume-20261026`: `sonar-bootstrap/ci-dependency-build-kgjzjuxb/receipt.json` and `sonar-bootstrap/targeted/active-tests-_766u92i/summary.json`. This targeted prerequisite check does not prove full post-fix measurement, witness retention or a new-head Quality Gate.

## Security impact

Static review found no concrete source-backed bypass; an independent schema-3 candidate review likewise found no concrete bypass/regression, with static-only limits. Nineteen context findings retain source-backed decisions without server dispositions. Offline guards, lexical root/path authorization, full inventory validation and existing gate thresholds remain. No broad exclusion, baseline shift, custom collector restoration or Framework/MRTS authority expansion.

## Runtime evidence

No host campaign was launched for this remediation. E2E remains 26 and historical I12 host/matrix/oracle work remains closed without new `I12_COMPLETE`. Historical No-CRS success at the base proves only that run/head; PR #421 evidence remains bound to its original revisions.

## Known limitations

First local SCM changed-Python coverage is 24.791%: 10,867/41,669 lines plus 3,112/14,718 conditions covered. This is not a Sonar metric or an 80% pass. Dirty reports are not import-eligible. The full producer must be rerun after raw-retention correction. PR #421 gates and parsing/include quality cannot qualify this remediation. Architecture HTTP 415 and CFamily/Python/FIFO/TLS analyzer limitations remain separately documented.

## Remaining risks

Actual terminal server processing, issue dispositions, coverage import and Quality Gate for a new published remediation head remain missing. Further coverage work is necessary; no Ready/verified_pr claim is justified.

## Checks not run and rationale

No fresh full post-retention measurement or clean-head scanner import is available yet; required Sonar at `bcde66f2` failed before analysis as recorded above. No additional host/matrix/oracle campaign is required or authorized by this scoped remediation. Repository bilingual/link/path checks passed as recorded above; further final source validation and missing coverage/server evidence remain the coordinator’s responsibility after source freeze.

## Final diff and review status

Checkpoint `bcde66f2cf88130c57c7e49a0d5d2a22150948da` was committed and pushed normally; its bootstrap correction is being prepared as a follow-up. Current central state: [PR #382 status](../../../docs/pr-382-merge-readiness.md). PR #382 stays Draft; no Ready, merge into master, release or deployment is claimed. Overall remediation remains partial until the acceptance evidence above exists.
