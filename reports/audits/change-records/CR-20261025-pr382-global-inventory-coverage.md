# Change Record: CR-20261025-pr382-global-inventory-coverage

**Language:** English | [Deutsch](CR-20261025-pr382-global-inventory-coverage.de.md)

Parent inventory/coverage migration. Exact published-head delivery evidence: [PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261025-pr382-global-inventory-coverage |
| Date (UTC) | 2026-10-25 |
| Base revision | `d510d21dba7eab3c9f0ccbe579fbc9c105eb3da1` |

## Motivation and problem statement

Older leading documents requested closed I12 work, automatic defaults selected thousands of test definitions, and Sonar Automatic Analysis imported no coverage. Preserve historical results while correcting their active status and selection/measurement producers.

## Acceptance criteria

One globally expanded inventory admits at most 100 behavioral cases before selected children start. All automatic defaults derive from it. Real reports must be generated/imported with plausible revision-bound metrics. Existing gates, including 80% New-Code coverage, remain unchanged. Ready requires exact local/remote/PR identity, current base, successful required CI/Sonar and resolved required feedback. Framework/MRTS and historical I12 qualification remain unchanged.

## Implementation decision and rationale

Use `config/testing/active-cases.json`, closed selectors and source hashes; reject overflow, unknown/empty selections, drift and alternative executable catalogs without truncation. Python discovery derives from the same targets. Retain specialists behind explicit `ON_DEMAND_TESTS=1` and generate a non-executable definition archive. Runtime collectors enumerate independent cases and reuse only an identical canonical readiness transaction.

Measure actual Python line events and eligible same-prefix/UID children, native profiles for four Go modules and actual GCC/gcov C/C++ units. Bind revision, inventory, source/report hashes, toolchains, SDK and role/config inputs; import requires clean matching source. Classify individually reviewed fixtures as TEST; mixed operational tooling stays MAIN. No production exclusion, artificial hit, baseline shift or gate relaxation.

## Changed files

Inventory/coverage: `config/testing/active-cases.json`, `ci/lib/active_test_inventory.py`, `ci/lib/active_coverage.py`, `ci/lib/python_coverage_bootstrap.py`, `ci/tools/run-active-tests.py`, `ci/tools/collect-active-coverage.py`, their two control modules, `tests/__init__.py` and lazy hooks in retained test modules. Integration: root/component Makefiles, workflows and nested build/runtime helpers. Analysis: both Sonar properties, `config/testing/sonar-source-roles.json`, its shared classifier/generator, scanner workflow and immutable action lock/updater allowlists. Archive: `ci/tools/update-test-archive.py` and `reports/testing/test-selection-archive.generated.json`.

EN/DE pairs: current closeout/source-role docs, historical checklist/handoff/matrix/event-contract/#410 closure and phase-4/body-inspection references, CI/testing/variable guides and this record. The Git diff is the complete file list.

## Commands executed

RTK wraps every local shell command. Observed procedures include `ci/tools/run-active-tests.py --check`, selected controls, `ci/tools/collect-active-coverage.py run --strict-skips --output-root <external-run-root>`, `ci/tools/sync-sonar-test-scope.py --check`, pinned actionlint/zizmor, workflow version contracts and `git diff --check`. Detailed run evidence is external under `/var/tmp/codex/ModSecurity-conector/runs/pr382-merge-readiness-20261025`.

Initial 21 controls passed, including synthetic 101-case rejection before a sentinel child starts. Actual loader-naming, Python 3.15 line-metadata and unrelated GCC-note failures were corrected and the affected same cases passed. The corrected native C++ allow plus four memory behaviors passed including ASAN without skip. A fresh collection generated 35 generic sources (11 Python, 24 native), 13 Go sources across four modules and 190 raw reports from 59 cases; the dirty local report is not import-eligible. A later audit identified and corrected an imprecise shell-negative result; its exact-cause proof is renewed separately. Final published-head results belong to current PR evidence.

The later 57-case collection also completed successfully and exposed a real measurement gap: the HTTP service child used `_exit`, so its counters were lost. The coverage-only fixture now flushes actual GCC counters before that exit. Both existing deadline/recovery cases passed again; actual service observations changed from 0 to 694 covered lines out of 1165 measured lines. These are local line observations, not Sonar project/New-Code percentages.

Source bindings explicitly name `path` and `sha256`; a source filename is never used as a credential-like field name. Twelve staged scanner findings were independently verified as public configuration text or exact current-source hashes. The structured representation and clearer property constant remove those false alarms without suppressions or scanner changes.

Hosted verification at `9736ba07cdf0f60488c0d07b2200eea867c02abb` exposed missing job prerequisites: Apache/APR headers and PyYAML, plus a header-wrapper output parent assumed present locally. Jobs now provision the actual required packages/hash-bound Python dependency; the wrapper validates an existing external temp parent and creates its private leaf. Its same two cases passed with `BUILD_ROOT` absent. The selected Stock-sidecar and descriptor-expiry cases also passed locally without skips. The clean 56-case report at that commit contains 77 generic sources (11 Python/66 native), 13 Go sources and 306 raw reports; it is historical after the follow-up and must not be imported for another revision.

The same Hosted round also identified an unselected old Go toolchain in the Envoy runtime job, an absent NGINX invocation temp directory, and the new runner’s generic ten-minute limit interrupting cold Apache provisioning. Runtime rows now select `.go-version` before provisioning; NGINX creates/revalidates its private temp directory. Only the three closed host-runtime scripts receive a 6000-second deadline inside the existing 120-minute jobs; ordinary controls retain 600 seconds and the one-second process-group cleanup control passed again.

Hosted verification at `71e9586607a66a5fc2c204df17f4436c41eb8411` passed the selected NGINX host cases and four CRS connector jobs at readback. It also exposed missing ModSecurity headers in Apache fixture callers, the CodeQL tracer conflicting with ASan, a standard-header search-order error and an unsupported older distro SDK. Callers now install the headers; admitted ASan cases precede CodeQL initialization while product compilation remains traced. C++ uses a private namespace-only include overlay. Coverage and Stock jobs use the existing pinned shared-component SDK builder, which runs no host campaign. Eighteen new Sonar findings prompted focused source refactoring, compiler admission and fixed exclusive trace-file publication; their server verification remains pending. The same 17 inventory/report controls and five native C++/memory behaviors passed locally without skips before the final helper extraction; the planned clean-head collection renews that evidence.

## Security impact

Validate the complete catalog before execution and reap owned process groups on timeout/termination. Reject unsafe report/source paths and changed artifacts. Child tracing preserves UID/prefix/isolation and records source-line counts only. CI validates its existing credential at the fixed Sonar origin without logging secrets. Static/security gate intentions and protected namespace boundaries remain substantive. The new scanner Action is immutable; signature verification stays enabled.

## Runtime evidence

Local observations prove only the selected unit/native/control layer and actual profiler output. Current CRS/No-CRS/NGINX host cases need their own Hosted artifacts. Historical I12 results retain their original revisions; no build/scanner/configuration result creates a new host or lifecycle qualification. No `I12_COMPLETE` is asserted.

## Known limitations

Line-only measurement does not provide branch coverage. Isolated/clean-environment/other-prefix/other-UID/killed Python children and unexecuted host paths may remain unmeasured. Extracted native snippets and external SDK execution are not assigned to Parent source. Local measured-file ratios are not Sonar project/New-Code coverage; generation, import and terminal server metrics are separate claims.

## Remaining risks

Reduced automatic selection deliberately loses specialist coverage; the closeout and generated archive document its disposition. Profile evidence never transfers to a sibling profile. Existing 80% New-Code coverage and all other mandatory conditions still govern Ready. Later trusted-master updater execution and genuinely created maintenance PRs require separate master-integration authority.

## Checks not run and rationale

No historical I12 campaign, full MRTS suite, archived broad catalog, restricted platform scan, master merge, release or deployment: outside task authority. Retained on-demand sources are not a new PASS. No default-branch live publication is claimed from configuration or simulation.

## Final diff and review status

Independent review checked default selection, report/source boundaries and original test preservation. All 436 pre-existing hook-manifest sources match the base; 435 differ only by their hook, and the one protected-workflow control adds explicit opt-in assertions. No original assertion was removed. Current PR evidence must identify final SHA, terminal required checks/Sonar, blockers and Ready state. This record alone does not declare `verified_pr`.
