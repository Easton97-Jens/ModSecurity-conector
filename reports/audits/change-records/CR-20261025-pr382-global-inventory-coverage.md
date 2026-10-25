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

One inventory enforces at most 100 core behavioral cases before all selected children start; the subsequent explicit user authorization adds separately counted guarded offline Python exceptions. All automatic defaults derive from it. Real reports must be generated/imported with plausible revision-bound metrics. Existing gates, including 80% New-Code coverage, remain unchanged. Ready requires exact local/remote/PR identity, current base, successful required CI/Sonar and resolved required feedback. Framework/MRTS and historical I12 qualification remain unchanged.

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

At `73f52b6c751b5bbffa70aca96effa6d8f323ed79`, the clean local 56-case collection and identity verification passed (308 raw reports), full local lint passed, and Hosted collection/verification passed (309 raw reports). Both measured 77 generic sources and 13 Go sources/four modules. All five CodeQL jobs and the Stock SDK job passed. AutoScan resolved 17 of 18 findings; the remaining compiler argument finding prompted a closed positive grammar and bounded source/SDK/output roles. The Hosted HTTP Basic probe returned authentication `valid=false` for `MODSECURITYCONECTOR`; no scanner/import/coverage percentage is claimed. The repository owner subsequently configured dedicated `SONAR_TOKEN` through GitHub settings; the workflow validates it before provisioning, without exposing its value. An intermediate lookup of the removed legacy name failed before collection. At that intermediate revision, AutoScan remained enabled pending valid CI authentication. Source-only updater validation now copies and re-admits the complete inventory source closure without widening publisher mutation authority. Its existing seven selected contract cases passed in the private proposed tree. Eighteen instrumented native cases passed after the APR linker-input correction. One new control rejected a text linker script disguised as an object before any compiler process; it replaces an optional valid-positive inventory probe retained on demand. That intermediate inventory was 100/81; the later regenerated archive retains 5,924 on-demand definitions. The Basic probe alone did not prove generic token invalidity; the renewed credential is now checked with Bearer authentication before provisioning. Final-head provider verification remains separate.

## Current selection and observed CI import

The same schema-2 inventory now transparently declares 1000 expanded cases / 580 executions: 100 core cases / 80 executions (including the original eight offline cases) and 900 user-authorized source-bound Python offline exceptions / 500 executions. The core ceiling remains 100 and is enforced before all children; exception variants are explicitly counted. Offline children deny process creation and network access before imports, and package-level discovery defers offline imports to that child. Raw `unittest discover -s tests` initially imports modules in the parent to find their hooks; reviewed top levels have no eager process/host activity, and actual tests then run only in guarded children. These are current-selection counts, not final acceptance. Native/Go/connector scenarios do not qualify for this exception.

Coverage currently selects 964 cases / 558 executions. One active offline timing case runs separately in Sonar CI without instrumentation: its unchanged one-second assertion failed under tracing (2.551 s) and passed without tracing (0.034 s). It remains selected and asserted; this changes measurement only, with no case removal, source exclusion or gate relaxation. Child tracing filters fixture line callbacks and retains only real positive hits for Parent MAIN sources.


Connector selection remains 26 cases: 13 No-CRS, 11 CRS and two NGINX callbacks. Eight separate config/start stages remain archived; minimal profiles still perform real config/start/request/shutdown, without separate request-free startup/isolation qualification. No historical I12 host/matrix/oracle campaign or new `I12_COMPLETE` follows. Coverage selects 964 cases / 558 executions, unverified. All 21 inventory/coverage controls passed, including exception admission/guards; the existing 101-core overflow control remains. Source roles include 45 reviewed fixtures. The current generated archive reports 5541 retained definitions; source-hash verification is still in progress.

The earlier 65-case local collection passed with 94 generic sources (28 Python/66 native), 13 Go sources and 327 raw reports. Its dirty local changed-line intersection increased from 1935 to 4489 covered generic lines (+2554). These are local observations, not server coverage percentages.

At published head `6026cb7d72947e0f7c0ab4d5f72ce180ae2c7557`, the previous 56-case coverage selection was actually imported by CI: all nine Go reports, 77 generic sources and 120 CFamily translation units. Compute Engine task `AaFzJIJFF1KaAz-ccBDH` completed successfully and published analysis `f68c295c-a7b7-499c-b7e3-b59b7a734cb4`. Observed server measures were 5.3% New-Code coverage, 3.6% overall coverage, 40,481 new lines to cover and 38,331 uncovered new lines, with 28 findings. The dedicated `SONAR_TOKEN` passed CI authentication before provisioning. AutoScan is now OFF after the authenticated switch to CI analysis. This proves actual import at that head, not acceptance of the changed inventory or final head.

PR #382 remains Draft / `remediation_required`. The unchanged 80% New-Code threshold, zero required findings and successful terminal required checks must be demonstrated at the actual final head. No final success, Ready state or `verified_pr` is claimed.


The earlier 756-case offline selection passed all eight private batches (385 executions); all 21 inventory/coverage controls passed. The `integrated-offline-control-fixed` run passed all 37 cases across 34 executions with zero skips: 16 integrated Envoy/lighttpd/Apache orchestration cases using actual validators and simulated external seams, 18 helper/security cases including two static publisher contracts, and three cache cases. This is offline evidence, never host qualification. Raw Python observations from the earlier 756-case run intersect 8102 local changed lines; this is not the Sonar denominator or proof of 80% coverage. A coherent actual 964-case collection, clean-head CI and the unchanged 80% gate remain pending.


## Derived maintenance metadata and remaining prerequisites

Maintenance may derive exactly two companion files: `config/testing/active-cases.json` (existing SHA fields only) and `reports/testing/test-selection-archive.generated.json` (`inventory_sha256` only). Selectors, cases, profiles, source paths and subtest metadata cannot change through this mechanism. Trusted-base reconstruction must reproduce exact bytes and regular stage-0 mode `100644` before staging, publication or reuse. The primary Actions publisher allowlist is unchanged. Three focused regressions now pass: a future Go minor 1.28 is eligible, rollback preserves a foreign companion change, and rollback restores its own companion larger than 4 KiB.

Four `go.mod` declarations and `requirements-ci.lock`, `requirements-ci-build.lock`, `requirements-dev.txt` are seven non-executable dependency declarations, not collector source bindings. Go module/sum files and the three requirements remain bound by actual build identity and pre/post source snapshots. This avoids dependency-metadata churn without removing controller or executable-code bindings.

Sonar's job budget is now 120 minutes instead of 45 for the explicitly larger selection; individual 600-second limits and the one-second timing assertion remain unchanged. Observed profiles reduced 429 AST parses to 41 and 6841 source reads to a few hundred. The earlier 15.723 s measurement had nine concurrent workloads, whereas the later 1.788 s measurement was idle: these different conditions do not establish a controlled speedup.

After the user marked configuration complete, observed Dependabot secret metadata lists exactly one name: `SONAR_TOKEN`. The earlier zero-name/pending-secret state is historical and resolved at the metadata layer. No token value was read, and neither live bot authentication nor a successful Dependabot PR is claimed. That execution proof still requires separately authorized default-branch maintenance checks; current PR authentication is a separate result. [GitHub's Dependabot-on-Actions rules](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-on-actions) describe that separate secret context. No secret or provider setting is changed by this documentation.

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

Independent review checked default selection, report/source boundaries and original test preservation. The earlier hook-only preservation check covered 436 pre-existing sources. Subsequent explicitly authorized offline fixture changes preserve their assertions and are described above; the earlier hook-only comparison is historical, not a claim about the new final source state. Current PR evidence must identify final SHA, terminal required checks/Sonar, blockers and Ready state. This record alone does not declare `verified_pr`.

At published head `6ede6d91d2feab6f887fbe977033f26c49f9c993`, Hosted coverage collection failed before scanner import: `BackendDecodingTests` tried to create fixtures under a local-only storage directory. Its setup now uses the runner-owned private temporary root, without changing the decoding assertions. The three corrected local follow-up batches passed 65 executions / 99 expanded cases with zero skips, including 41 newly admitted offline artifact-validation cases. Apache negative fixtures now mutate the actual independently bound source ledger and mapped SDK image hash; no simulated result is build or host evidence. The interrupted local clean-head collection is incomplete and is not import evidence. A fresh clean-head collection and server analysis remain required.

## Integration of master #420

The normal merge includes master `9f44647593bac7947113558c6ad183ab118e80af`. The full Parent scope, explicit scanner configuration, generic JSON/YAML opt-in and separate C++20/23 advisory projects are retained. CFamily fixtures remain MAIN for actual static analysis; their reviewed fixture purpose and caller evidence are preserved. Thirty exact Python fixtures remain analysis TEST sources. C++17 is required; C++20/23 reuse the same immutable, fully verified reports through read-only advisory jobs. No extra Go/native scenarios or historical I12 campaigns are selected.

The merge adds 66 explicitly counted offline controls across 40 executions: 14 scope cases, 16 real-file artifact identity cases, 17 workflow-boundary cases and 19 CFamily codec/snapshot/classification inputs. These and the 21 existing admission/import controls passed locally with zero skips. Full properties/source-role/Python contracts and actionlint passed. Eight CFamily suffixes now share one coverage/snapshot contract, including all eight tracked `.hpp` files. The two tracked `.codex/bin` Python controls remain unmeasured under the existing privacy filter; they remain in Sonar scope.

The last published-head analysis is historical `3baaffb7b5dd30f05fc9d81ea58da5bd06a2244f`: CE `AaF0MvFOdkEpBguA0kSU`, analysis `c460fc88-86c3-48eb-87da-e795b94b0990`, 12.9% overall / 31.0583536721% New-Code coverage (45,070 new lines; 31,072 uncovered), 17 findings, zero new duplication/hotspots. Nine Go reports and 139 generic files were imported; 118 CFamily units were analyzed under the previous scope. This does not verify the merged 185-unit full scope or its final gate. The unchanged 80% and zero-findings requirements remain pending. Unpublished pre-pause work remains separately secured and must be reconciled after this merge.
