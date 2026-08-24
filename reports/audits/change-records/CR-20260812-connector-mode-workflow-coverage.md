# Change Record: static connector-mode workflow coverage

**Language:** English | [Deutsch](CR-20260812-connector-mode-workflow-coverage.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260812-connector-mode-workflow-coverage |
| Date (UTC) | 2026-08-12, reconciled 2026-08-14 |
| Base revision | `ea3b48abab7940de49997a371f9117b409c05a2a` |
| Delivery status | Draft PR [#279](https://github.com/Easton97-Jens/ModSecurity-conector/pull/279) remains at remote head `63ad4f5ed359ba2be9abe955cb1c82e7dfcb3846`. The local task branch normally merged current master in `338985e5329076d42bb23cdeac8260f72b68b71d` and contains the locally validated Parent CRS-acquisition repair plus workflow corrections above it. No corrected head has been pushed, no Ready-for-Review transition occurred, and exact-head hosted evidence remains pending. |

## Motivation and problem statement

The current connector state needs an explicit, truthful workflow surface for
the four CRS/MRTS mode combinations without claiming capabilities that are not
implemented. Apache and HAProxy have native runtime paths for all four modes.
Envoy, Traefik, and lighttpd have a no-CRS/no-MRTS runtime path, a static
Framework contract for with-CRS/no-MRTS, and no supported MRTS full-matrix
route. NGINX is deliberately excluded because its protected broker has a
separate trust boundary.

## Acceptance criteria

- Four named top-level workflows each contain one direct, static five-row
  `strategy.matrix.include` and collectively implement the required twenty
  cells without NGINX or `_template` rows.
- Runtime cells invoke existing native controls and preserve cleanup and exit
  status. Contract cells run the existing static Framework contract and retain
  its `CONTRACT_VALIDATED`/`UNATTESTED` distinction.
- Expected-unsupported cells invoke the real full-matrix runner for the
  selected connector, `unknown`, and `_template`; each must reject with exit
  `2`, the invalid-choice diagnostic, and no build root.
- Workflow security remains read-only and fail-closed, with immutable action
  pins, no secrets or write token, no persisted checkout credentials, no
  `pull_request_target`, no cache, no privilege escalation, and no broad
  artifact publication.
- Every Framework Python dependency installation in the new workflows uses
  `requirements-ci.lock` with `--require-hashes` and `--only-binary=:all:`;
  none invokes `make setup-dev`, `bootstrap-python.sh`,
  `requirements-dev.txt`, or an unpinned Pip upgrade.
- On a pull request, checkout and the recorded Parent revision use the event's
  immutable head SHA; `github.sha` is only the manual-dispatch fallback.
- Parent and Framework/MRTS Gitlinks stay fixed at the current master-recorded
  `1260aaae411ecf88cf50dc480b80e2e20ac47901` and
  `615b13bacbd008562c17408246c41ab27dca3104` respectively.

## Implementation decision and rationale

The four workflows use exactly the five non-NGINX connectors: `apache`,
`envoy`, `haproxy`, `lighttpd`, and `traefik`. Their static mapping is:

| Connector | no-crs/no-mrts | with-crs/no-mrts | no-crs/with-mrts | with-crs/with-mrts |
| --- | --- | --- | --- | --- |
| apache | runtime | runtime | runtime | runtime |
| haproxy | runtime | runtime | runtime | runtime |
| envoy | runtime | contract | expected_unsupported | expected_unsupported |
| traefik | runtime | contract | expected_unsupported | expected_unsupported |
| lighttpd | runtime | contract | expected_unsupported | expected_unsupported |

The implementation reuses existing Parent entry points only. It does not add a
connector capability, alter the full-matrix allowlist, write Framework or MRTS
source, or modify the existing workflow-tool updater. The latter's unrelated
all-workflow inventory regression already fails for an action-free local
reusable caller on the clean base; this task does not weaken or alter that
test oracle.

All four path filters now include their direct interpreter, provisioning,
provenance, report-helper, and `.gitmodules` dependencies. The focused contract
requires the same closed trigger set in every workflow; NGINX remains excluded.

The three workflows that directly call `verified-haproxy-case` derive
`haproxy_source_root="$CACHE_ROOT/shared/sources"`, reject a root outside
`$CACHE_ROOT`, and pass it only to that Make target. This aligns the caller with
the component snapshot's `SOURCE_ROOT` and `CRS_SOURCE_DIR`; it does not change
the separate no-CRS/no-MRTS five-connector HAProxy path or weaken the Framework
containment guard.

The eleven runtime cells and the three static Framework-contract cells install
their required Python dependency from the Framework's hash-locked
`requirements-ci.lock`. Each uses `--require-hashes`, `--only-binary=:all:`,
and `pip check`, rather than `make setup-dev`, the Framework development
bootstrap, or a mutable dependency path. The checked-out Parent, Framework,
and MRTS revisions are verified against the recorded immutable SHAs before
that lockfile is read. This avoids the previously identified mutable-Pip
pattern tracked by `FND-PARENT-0052` without changing a dependency lock or
Framework source.

With-MRTS runtime cells use the existing native `action_allow_phase1_pass`
control and explicitly report DetectionOnly semantics; they do not claim
enforcement. The separate no-MRTS runtime cells retain
`action_deny_phase1`/HTTP `403` as the enforcement proof. The focused
no-CRS/with-MRTS HAProxy branch sets the existing literal
`RUNTIME_COMPONENT_TARGET=haproxy` selector before its native case target.
That branch does not need CRS and can therefore avoid the unrelated Apache
archive without changing its real HAProxy runtime path. The two with-CRS
HAProxy branches deliberately retain the existing all-components preparation.
For the with-CRS/with-MRTS Apache and HAProxy cells, the fresh CRS checkout is
first acquired below the private verified run root. After the Framework fetch
and provenance checks succeed, an atomic no-replace rename transfers it into
`$CONNECTOR_COMPONENT_CACHE/sources`; the final path is then verified again
with the Framework provenance guard. This makes the fresh checkout available
to the HAProxy snapshot without reusing or overwriting an existing cache entry.
Apache intentionally remains on its ordinary native path, which still requires
its reviewed APR-util tuple.

The Parent component preparer now records whether a Git source was acquired
recursively. Only `coreruleset` selects `--no-recurse-submodules`; all generic
Git components retain their existing recursive clone and submodule-update
path. The CRS cache identity includes the non-recursive mode, so a legacy
recursive CRS checkout cannot be reused. Fresh and reused non-recursive CRS
checkouts fail closed when null-delimited local `submodule.*` metadata or a
`.git/modules` registry is present. This prevents the condition at the source;
it does not delete configuration after acquisition or alter the Framework
provenance guard.

## Changed files

- Four `test-connectors-*.yml` workflows.
- `ci/provisioning/components/prepare-runtime-components.py` and focused
  workflow/Python/cache-contract tests, including
  `tests/test_runtime_component_cache_contract.py`.
- `ci/runtime/lifecycle/promote-fresh-crs-source-to-component-cache.sh` and
  `.py`, plus `tests/test_runtime_env_snapshot_contract.py`, for the bounded
  fresh-CRS transfer and post-transfer provenance check.
- This English/German Change Record pair and its existing archive indexes.

No connector source, capability manifest, lifecycle runner, Framework/MRTS
source, Gitlink, dependency lock, ruleset, or NGINX workflow changes are part
of this change.

## Commands executed

- `ConnectorModeWorkflowContractTest` plus `PythonVersionContractTest` passed:
  `31` tests. They assert the closed 20-cell topology, current Gitlinks,
  hash-locked install, direct trigger set, static negative routes, and the
  HAProxy snapshot source-root guard.
- APR-util/provenance/static/snapshot controls passed: `43` tests.
- `RuntimeComponentCacheContractTest` passed: `47` tests. The focused
  preparation suite passed: `41` tests. They cover the CRS-only
  non-recursive acquisition, null-safe local-config check, exact pinned
  revision, repeat/reuse, tainted legacy-cache rebuild, failed staging cleanup,
  and a genuinely recursive generic-component control.
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract` passed: `97` tests and `4` expected
  environment-capability skips; its tool lock validation is validate-only.
- Focused Python compilation and `git diff --check` passed.
- PyYAML parsed all four workflows. ShellCheck received all `42` literal Bash
  `run:` blocks through stdin and returned `0` for each. GitHub-expression
  blocks remain authoritative only under hosted actionlint.
- A fresh private virtual environment installed Framework
  `requirements-ci.lock` with `--require-hashes` and `--only-binary=:all:`,
  loaded PyYAML `6.0.3`, and passed `python -m pip check`.

## Security impact

The workflows are pull-request-safe by construction: top-level
`permissions: contents: read`, immutable full-SHA action pins, recursive
checkout with `persist-credentials: false`, and no user-controlled ref in a
shell command. The event head SHA is used only as the declarative checkout and
revision-equality input, never interpolated into a shell body. Unsupported routes execute only a parser rejection under the
private runner temporary root; a rejection log is diagnostic-only and no
build/evidence artifact is uploaded. Static contract routes do not pretend to
be host runtime evidence. Each of the eleven runtime cells and three contract
cells uses the Framework's hash-locked CI requirements and fails closed on an
invalid dependency set after the immutable Gitlink revisions have been
verified. No new workflow route invokes the mutable development bootstrap.

## Runtime evidence

Before implementation, all 18 selected/`unknown`/`_template` negative runner
attempts for the six unsupported cells rejected with exit `2` and created no
build root. The Framework static contract remains static evidence only.

Fresh current-master all-target component preparation was run in a new private
build/source/cache root. Framework
`1260aaae411ecf88cf50dc480b80e2e20ac47901` selected APR-util `1.6.5`; its
fresh archive SHA-256 was
`96de1dd6f6a0476d2d2e7964926d8c1ddc3bb0e210e1b1812d3ba5a454a392e2`.
Apache/no-CRS/no-MRTS `action_deny_phase1` then passed with HTTP `403`. The old
PR-head APR-util `1.6.4` HTTP `404` is therefore superseded by current-master
evidence; `FND-FRAMEWORK-0067` is not changed by this Parent task.

The preceding recursive CRS acquisition was reproduced against the approved
`55b09f5acfd16413e7b31041100711ceb7adc89c` revision: it created local
`submodule.active .`, and the unchanged Framework guard correctly rejected the
checkout with exit `77`. The new CRS-only non-recursive path reaches the same
approved commit, returns `recursive_submodules=false`, leaves
`git config --local --null --get-regexp '^submodule\\.'` empty (Git exit `1`),
creates no `.git/modules`, and is accepted by the unchanged Framework
`prepare-crs.sh` guard. The deliberately tainted negative fixture still exits
`77`; generic components that require submodules remain recursive. This is the
local repair for `FND-PARENT-0128`, not a guard bypass.

Apache and HAProxy `with-crs/no-mrts` focused `action_deny_phase1` controls
each passed with HTTP `403` under the repaired source topology. The clean
worktree runtime evidence then completed all eight Apache/HAProxy mode cells:
the four no-MRTS enforcement controls returned HTTP `403`, while the four
with-MRTS DetectionOnly controls ran `action_allow_phase1_pass` and returned
HTTP `200` with the live native control executed and no enforcement claim.
The HAProxy workflows now place `BUILD_ROOT` below
`$cell_root/verified/build`, satisfying the existing verified-root guard; no
`XDG_STATE_HOME` workaround was added. This local eight-mode evidence is
retained for the task, but does not substitute for exact-head hosted runs.

### Old hosted diagnostics

| Old run | Jobs / first causal step | Classification on current master |
| --- | --- | --- |
| `31616687887` | Apache `94181133426`, Provision host component: APR-util `1.6.4` HTTP `404` | superseded by current Framework APR-util `1.6.5` preparation and Apache runtime proof |
| `31616687903` | Apache/HAProxy runtime jobs: APR-util `1.6.4` HTTP `404`; Envoy/Traefik/lighttpd contract jobs: `ModuleNotFoundError: No module named 'yaml'` | APR failure superseded; YAML dependency path locally fixed with hash-locked `requirements-ci.lock` |
| `31616687995` | Apache/HAProxy runtime jobs: APR-util `1.6.4` HTTP `404` | superseded; the repaired local CRS path supports a required fresh exact-head rerun |
| `31616688052` | Apache/HAProxy runtime jobs: APR-util `1.6.4` HTTP `404` | superseded; the repaired local CRS path supports a required fresh exact-head rerun |

## Known limitations

Local `actionlint` and `zizmor` binaries are unavailable and were not
downloaded or installed. The installed ShellCheck binary cannot replace
actionlint's workflow/YAML analysis. A local static result does not prove
GitHub-hosted runner behavior, connector runtime success, or exact PR-head
security enforcement.

The local CPython used for fresh controls was `3.14.4`; hosted workflows expect
`3.14.6`, so this record does not claim exact interpreter equivalence.

The pre-existing updater exact-inventory regression remains outside the
authorized path list: correcting it would require an unrelated test-oracle
change and modifying an existing updater workflow/tool.

## Remaining risks

`FND-PARENT-0128` is locally fixed, and the related with-MRTS semantic and
HAProxy root corrections are locally exercised, but release/integration remains
blocked until exact-head hosted cells pass. Framework/MRTS source and the
fail-closed provenance guard remain unchanged. Actionlint/zizmor, required
checks, Sonar disposition, and all hosted matrix evidence are still
unverified. Envoy, Traefik, and lighttpd MRTS cells remain explicitly
unsupported until an independently authorized capability and evidence change
exists. No failure may be hidden by weakening negative, static-contract,
cleanup, or security guards.

## Checks not run and rationale

- Local actionlint, actionlint-mediated ShellCheck, and zizmor scans: their
  pinned binaries are absent and fetching tools is outside this task's local
  validation authority. Exact-head hosted checks are required instead.
- Exact-head hosted connector matrix: pending a pushed corrected head; the
  clean-worktree eight-mode local runtime series is complete, but local
  evidence does not attest hosted runner behavior.
- Corrected-head PR checks, SonarQube Cloud applicability, and Ready-for-Review
  disposition: no corrected commit was pushed, so no exact new PR head exists;
  merge and auto-merge remain explicitly out of scope.

## Final diff and review status

This remains a local-remediation record. The normal master merge retained the
current recorded Framework Gitlink and no task-owned Gitlink diff exists. The
Parent CRS repair, its focused regressions, current APR-util provenance, the
HAProxy verified-root correction, and the complete clean-worktree eight-mode
runtime controls passed locally. Final review must still verify a published
exact committed head, remote branch, PR head, four hosted workflow runs, all
20 cells, actionlint, ShellCheck, zizmor, required checks, and Sonar
applicability before PR #279 is marked Ready for Review. No push, Ready
transition, merge, or auto-merge is recorded here.

## 2026-08-15 follow-up: Sonar duplication and Draft retention

### Motivation

The previous PR #279 head displayed `1.6%` new-code duplication beside `0 New
issues`, `0 Security Hotspots`, and `0.0% Coverage on New Code`. The user
requested literal zero displayed values, a current-`master` refresh, and Draft
retention while further work remains.

### Acceptance criteria

- Remove only the proven task-owned duplicate, without a Sonar configuration,
  exclusion, suppression, `NOSONAR`, test weakening, or coverage shortcut.
- Merge `origin/master` `55e45726a39bebd3f33aea87807419a882cd3ea8` normally
  into the existing branch, without rebase, force-push, default-branch push,
  merge, or auto-merge.
- Keep PR #279 open as Draft and obtain a new exact-head Sonar result after
  publication; a local calculation is not represented as a Sonar result.

### Technical decisions

Sonar located all 32 duplicate new-code lines in
`tests/test_runtime_component_cache_contract.py`: two local Git-command mocks
were equivalent. Commit `f1f7bb615f89a8d17e0e1193d368ecae79d3a805` extracts
them into `_local_component_runner`; each test still supplies its own upstream,
pinned commit, branch, expected URL, original command runner, and
`clone_modes` receipt. `--no-recurse-submodules` and `--recursive` therefore
remain independently asserted.

The normal refresh merge is `c6045f289b1b92d062732d552968c170f1c23a0f`, with
parents `dd92b27c4f5189abc4e0658df01ad1995a65209d` and
`55e45726a39bebd3f33aea87807419a882cd3ea8`. PR #279 was converted to Draft.
Framework and MRTS source and Parent Gitlinks remain outside this follow-up.

### Security impact

This test-only maintainability refactor preserves provenance, runtime-root,
dependency-lock, CI-permission, negative-control, and cache-integrity
assertions. No security control, workflow permission, download rule, or test
expectation was relaxed.

### Changed files

- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/CR-20260812-connector-mode-workflow-coverage.md`
- `reports/audits/change-records/CR-20260812-connector-mode-workflow-coverage.de.md`

### Tests and actual results

`/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q
tests.test_runtime_component_cache_contract` passed: 47 tests in 39.718s.
`git diff --check` passed before documentation edits. Sonar's prior exact
measurement was 32 new duplicated lines, `1.6129032258064515%`; the next
hosted analysis must verify `0.0%` for the new exact PR head.

### Runtime evidence

No connector runtime ran for this test-only refactor. The contract test
validates mocked checkout paths, not hosted-runner or connector runtime
behavior.

### Checks not run

New exact-head GitHub Actions, SonarQube Cloud, actionlint,
actionlint-mediated ShellCheck, and zizmor results do not yet exist at this
record update and must be observed after the normal branch push. No package or
tool download substituted for hosted checks.

### Known limitations

The existing `0.0%` coverage display reflects no imported new-code coverage
report, not runtime coverage. Only the post-push exact-head Sonar analysis can
verify the remote duplication calculation.

### Residual risks

Sonar could classify the updated source differently. Regardless of passing
checks, PR #279 remains Draft because the user states further work is required
before any master integration.

### Final review status

The source refactor is locally committed, its focused test passes, and the
normal master merge is present locally. Publication and exact-head verification
remain pending; no Ready transition, merge, or auto-merge is authorized.

## 2026-08-15 second follow-up: master-refresh Framework pin

### Motivation

The first refreshed head, `e0845a6e0f5ce37b713007640c7f68231b26c2fb`, achieved
SonarQube Cloud Quality Gate `OK`, zero new duplicated lines, `0.0%`
duplication, zero new issues, and zero new security hotspots. Its four
connector-mode matrices and `actionlint` nevertheless failed before runtime:
the normal master merge had changed the Parent Framework gitlink to
`01952978772995c054ba6a4cba86adc5d0cd1e7d`, while the PR workflows and their
contract still expected `1260aaae411ecf88cf50dc480b80e2e20ac47901`.

### Acceptance criteria

- Preserve the existing exact, fail-closed Parent-to-Framework and
  Framework-to-MRTS revision checks.
- Align every connector-mode workflow and its security contract with the
  already-merged Parent gitlink only.
- Re-run the local security contract and obtain new exact-head hosted evidence
  after the correction; keep the PR Draft.

### Technical decisions

Commit `1855ed8bc9e6485d80ecdf373d33a6a0118b4646` changes only the four
`EXPECTED_FRAMEWORK_SHA` values and
`CONNECTOR_MODE_FRAMEWORK_SHA` to
`01952978772995c054ba6a4cba86adc5d0cd1e7d`. The checked Framework commit has
the unchanged nested MRTS gitlink `615b13bacbd008562c17408246c41ab27dca3104`,
so `EXPECTED_MRTS_SHA` remains exact and unchanged. This is not a Framework,
MRTS, or Parent Gitlink source change.

### Security impact

The correction restores, rather than bypasses, the immutable revision check.
It leaves the PR trigger, read-only permissions, exact PR-head checkout,
`persist-credentials: false`, SHA-pinned actions, and no-secret/no-write
boundary unchanged.

### Changed files

- `.github/workflows/test-connectors-no-crs-no-mrts.yml`
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `.github/workflows/test-connectors-with-crs-with-mrts.yml`
- `tests/test_ci_security_workflows.py`
- this English/German Change Record pair

### Tests and actual results

`/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q
tests.test_ci_security_workflows` passed: 35 tests in 2.631s.
`make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
check-ci-security-contract` passed: 110 tests in 34.308s, with four expected
environment-capability skips. The cache contract also passed: 47 tests in
34.140s. `git diff --check` passed before this documentation update.

### Runtime evidence

The failed first refreshed-head matrix jobs did not reach connector runtime;
the later missing-evidence variables were cascade failures after the intended
revision assertion stopped setup. The corrected head needs fresh hosted runtime
evidence.

### Checks not run

The corrected exact-head GitHub Actions, SonarQube Cloud, actionlint/ShellCheck,
and zizmor outcomes are pending the normal branch push. The first refreshed
Sonar result is evidence for the duplication repair, not evidence that the
corrected Framework pin has completed all hosted jobs.

### Known limitations

Sonar's `new_coverage` measure remains absent; its displayed `0.0%` coverage
is not a runtime coverage claim. No local check can replace the corrected
head's hosted matrix and scanner results.

### Residual risks

The selected Framework revision may reveal an independent runtime compatibility
issue after revision verification succeeds. No such issue is assumed or hidden;
PR #279 remains Draft while the user completes further work.

### Final review status

The failure has an exact, security-reviewed root cause and a narrow locally
validated correction. Normal publication and new exact-head verification are
the remaining steps; no Ready transition, merge, or auto-merge is authorized.

## 2026-08-23 interim update: canonical connector coverage view

### Motivation

The user requested a current-`master` intermediate PR update that shows what
each connector can achieve by Framework phase and area, rather than a
ten-case-looking smoke result. MRTS connector support remains work in progress,
so missing host or MRTS evidence must not become a pass.

### Acceptance criteria

- Bring PR #279 forward through the normal local merge of `origin/master`
  `7c403fada21de4547259fef1dc4a1b079cb0cb25`, retaining Draft status.
- Use the canonical Framework No-CRS selection for the no-CRS/no-MRTS native
  route, and render every selected catalogue case by connector, phase, and
  area in every mode-workflow summary.
- Distinguish `PASS`, `FAIL`, `BLOCKED`, `UNSUPPORTED`, `NOT_EXECUTED`, and
  `NOT_APPLICABLE`; do not represent selection or missing MRTS routes as
  execution.
- Preserve native routes, revision pins, PR safety, and the protected NGINX
  boundary without changing Framework/MRTS source or Gitlinks.

### Technical decisions

The normal local merge is `e8c391843beb1306f16d67e0e58e234d9b7a1548`. The
Parent Gitlink now records Framework
`c40e924ec5c341032908e0082feba1d37ed1dfda`, whose MRTS Gitlink remains
`615b13bacbd008562c17408246c41ab27dca3104`.

`test-connectors-no-crs-no-mrts.yml` now invokes
`make "no-crs-baseline-$CONNECTOR"`, replacing only its former two-case
runtime smoke. The new Parent helper
`ci/runtime/lifecycle/summarize-connector-mode-coverage.py` uses the pinned
Framework selector and current connector capability manifest; it does not copy
the Framework case corpus. The canonical No-CRS catalogue has 166 cases across
phases `0` through `5` and 24 areas, all rendered with selection status and
reason.

Only ten catalogue entries provide a `runner_case`; 156 have no materializable
runner fixture. The native route therefore runs its materializable selected
fixtures, and other rows remain `NOT_EXECUTED`, `UNSUPPORTED`,
`NOT_APPLICABLE`, or `BLOCKED` as applicable. CRS/MRTS summaries show the
complete No-CRS catalogue as inventory, not CRS/MRTS runtime evidence.

The 20 existing workflow cells remain five non-NGINX connectors across four
profiles. Their summary lists all 24 connector/profile routes: NGINX is
`PROTECTED_SEPARATE`, not scheduled here, and never a pass. Envoy, Traefik,
and lighttpd CRS/no-MRTS rows are `RUNTIME_ROUTE`; their MRTS rows remain
`EXPECTED_UNSUPPORTED`. No provisioning target, connector source, capability
manifest, dependency, Framework/MRTS source, or Gitlink changed.

### Security impact

All four summaries execute only after exact Framework/MRTS revision validation.
The helper reuses the safe GitHub Step Summary writer; it reads runtime evidence
only after successful canonical validation, binds `result.json` and every
`results.jsonl` record to selected connector, phase, and area, rejects duplicate
or out-of-plan records, and retains `PASS` only with `live_executed=true`.
The canonical final status is allowlisted before the legacy direct summary
write. The workflows retain `pull_request`, `permissions: contents: read`,
immutable action pins, `persist-credentials: false`, fixed matrix values, no
secrets, and no write token. The focused workflow review confirmed no
high- or critical-impact finding.

### Changed files

- `.github/workflows/test-connectors-no-crs-no-mrts.yml`
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `.github/workflows/test-connectors-with-crs-with-mrts.yml`
- `ci/runtime/lifecycle/summarize-connector-mode-coverage.py`
- `tests/test_connector_mode_coverage_summary.py`
- `tests/test_ci_security_workflows.py`
- this English/German Change Record pair

### Tests and actual results

`/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v
tests.test_connector_mode_coverage_summary tests.test_ci_security_workflows`
passed: 48 tests. They cover an all-166-like plan, fabricated-`PASS` demotion,
valid live `PASS`, route classifications, duplicate-evidence rejection,
validation-outcome reporting, and the hardened summary-writer path.

`make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
check-ci-security-contract` passed: 133 tests with five expected
environment-capability skips; validation-only checks completed for `actionlint`,
`zizmor`, and `gitleaks`. PyYAML parsed all four workflows, and
`git diff --check` passed.

### Runtime evidence

No new local connector-host runtime is claimed for this intermediate summary
change. The selector proves the complete 166-row view, not live execution of
all 166 cases. Exact-head hosted evidence is required for actual materialized
results.

### Checks not run

Direct local `actionlint` and `zizmor` runs were not possible because their
binaries are absent; no tool was downloaded. Full connector runtime and the
complete live 166-case run cannot be established from this task worktree,
which intentionally has no initialized Framework submodule and does not alter
Framework/MRTS. Hosted Actions, SonarQube Cloud, and exact-head
coverage/duplication evidence remain pending the normal PR-branch push.

### Known limitations

The Framework currently lacks runner fixtures for 156 canonical catalogue rows.
The complete summary is a capability/evidence view, not a claim that every
connector live-ran every Framework case. MRTS connector coverage remains
interim, and the user requested PR #279 remain Draft pending separate work.

### Residual risks

The hosted run may reveal connector/runtime incompatibilities once native routes
consume the updated baseline. SonarQube Cloud can classify the new helper or
tests differently. Neither is hidden by the summary; the PR remains Draft and
no master integration, Ready transition, merge, or auto-merge is authorized.

### Final review status

The local master refresh, workflow change, summary contract, focused security
review, normal branch publication, and PR-head verification are complete.
Exact-head GitHub Actions exposed a narrow native-target caller omission,
described below. The PR remains Draft while that correction and its exact-head
hosted evidence are completed.

### Hosted remediation follow-up

The published PR #279 head
`4a10ec0b71b97fa75ce179f904158f26ab1b1b9f` exposed three genuine runtime
failures before their selected non-NGINX runtime controls: no-CRS/with-MRTS
Apache in run `32642702812` (job `97202139589`), and with-CRS/with-MRTS Apache
and HAProxy in run `32642702949` (jobs `97202140143` and `97202139952`).
Each stopped at `nginx_pinned_provenance_ref_mismatch`.

The direct workflow callers did not set `RUNTIME_COMPONENT_TARGET`. The
provisioner therefore correctly selected its fail-closed default `all` and
validated the protected NGINX provenance tuple before a non-NGINX native
control. This is a workflow-caller scope defect, not a reason to alter the
NGINX tuple, its guard, the Framework, MRTS, or a Gitlink.

The correction explicitly selects `apache` for Apache and `haproxy` for
HAProxy in both MRTS profile workflows, with a contract regression requiring
those exact values and prohibiting `all`. It is a diagnostic follow-up, not
closure: the focused local contracts and a new exact-head hosted run are still
required before this remediation is considered verified.

### SonarQube Cloud maintainability follow-up

At exact Draft PR #279 head
`ca085bdc1a826271f88192f99441ac9aa81b14d6`, the public SonarQube Cloud
Quality Gate passed while its New-Code issue query still returned two
task-owned code smells: `python:S3776` in
`ci/runtime/lifecycle/summarize-connector-mode-coverage.py:99` (Cognitive
Complexity 28 where 15 is allowed) and `python:S5778` in
`tests/test_connector_mode_coverage_summary.py:135`. The same measurement
returned `0` for new bugs, vulnerabilities, security hotspots, duplicated
lines, and duplicated-line density. `new_coverage` was absent from the
response, so this record makes no coverage inference.

This follow-up extracts the existing JSONL line parser and evidence-record
validator into two small helpers, retaining the original fail-closed ordering
for malformed JSON, non-objects, unknown cases, duplicate records,
connector/phase/area mismatches, and invalid statuses. The exception test now
materializes its safe temporary input before entering the assertion context.
It introduces no `NOSONAR`, exclusion, rule change, threshold change, or
Quality-Gate change.

Focused local validation of
`tests.test_connector_mode_coverage_summary` and
`tests.test_ci_security_workflows` passed with 48 tests. A fresh independent
security review found no new candidate or bypass: the structured evidence
boundary and safe summary path remain unchanged. This is still an interim
update: SonarQube Cloud and hosted checks must be re-observed on the normal
successor PR head before the two findings are considered fixed. PR #279
remains Draft; no Ready-for-review transition, merge, auto-merge, Framework
write, or MRTS write is authorized.

### Exact-head runtime follow-up: truthful partial status, CRS setup, and Lighttpd stock build

Exact hosted head `56b1f984759389cf63eb6f3eda4add1962a21491` exposed three
separate Parent-owned follow-ups. The No-CRS publication gate accepted only
`PASS`, even after canonical validation. A valid `NOT_EXECUTED` result for the
complete catalogue inventory could therefore fail generically rather than be
shown as a non-promoting partial result. The correction preserves only a
validated `NOT_EXECUTED` as `partial`; `PASS` stays the sole `complete` state,
and `FAIL`, `BLOCKED`, `UNSUPPORTED`, `NOT_APPLICABLE`, invalid evidence,
symlinked results, or a failed validator remain failing.

The updated aggregate preserves each connector status and reports `PARTIAL`
when any validated row is `NOT_EXECUTED`. It does not promote a not-executed
case to `PASS`. The summary renderer now also preserves Framework phase `0`
instead of treating it as `unknown`. A catalogue-backed contract loads the
current read-only Framework catalogue and requires every current case ID to
have a terminal row for every connector, with a concrete phase and area.

The with-CRS/with-MRTS Apache and HAProxy cells had initialized a private source
root but had not provisioned CRS or exported `CRS_SOURCE_DIR`. The first
successor head `c098b52cad2faf8d4238315842b52c3c22df746e` corrected that
omission: its bounded fresh-CRS step completed and Apache reached its runtime
control. The HAProxy control then correctly rejected that initial fresh source
because it still lived below `verified/crs-fresh-source` instead of the
snapshot-required `$CONNECTOR_COMPONENT_CACHE/sources` root. The pending
Parent-only remediation retains the existing pinned fetch and its provenance
checks, then performs an atomic no-replace transfer into that private cache
root and reruns the Framework provenance verifier before exporting the final
paths. Expected-unsupported Envoy, Lighttpd, and Traefik rows do not enter this
branch. No Framework/MRTS source, Gitlink, NGINX guard, pin, provenance, or
cache-containment control is weakened. Hosted successor proof for that transfer
remains pending.

For an existing No-CRS result whose canonical validator did not succeed, the
summary now exposes only a bounded, non-promoting terminal signal: the
allowlisted final status and, when structurally bound, the first failing or
blocked case ID with its phase, area, and status. It never publishes raw runner
reasons or logs, never changes a terminal or case status, and tolerates
malformed non-UTF-8 JSONL as an absent optional detail. `FND-PARENT-0217`
tracks the missing hosted diagnostic evidence that led to this limited Parent
summary correction.

The same exact head showed a Lighttpd stock-build failure: the generic
response-start path called a host-transaction emitter whose definition was
inside the patched streaming-hook conditional. The narrow C correction moves
only the generic header helpers into common compilation scope and keeps
response-body helpers ABI-guarded. It preserves opt-in behavior, a
server-generated bounded identifier, `http_header_response_set`, and the
pre-commit guard.

Current focused local validation passed: 88 summary/matrix/catalogue/workflow/
CRS tests and 85 Lighttpd/workflow-security tests with two expected namespace
skips. `git diff --check` passed. The isolated task worktree correctly blocks a
native Lighttpd build at its intentionally uninitialized Framework harness
(`common.sh`, exit `77`); it did not initialize Framework or MRTS and did not
simulate a build. A fresh combined security review found no reportable finding.

`FND-PARENT-0213`, `FND-PARENT-0214`, and `FND-PARENT-0215` remain
`in_progress`; `FND-PARENT-0216` separately records the hosted no-CRS/with-MRTS
HAProxy dependency-download rate limit, while `FND-PARENT-0217` records the
No-CRS terminal-diagnostic evidence gap. Exact-successor hosted Lighttpd,
No-CRS, and with-CRS/with-MRTS Apache/HAProxy evidence, plus successor-head
SonarQube Cloud evidence, are still required. This is an intermediate Draft
update only: no Ready transition, merge, auto-merge, Framework write, MRTS
write, or Gitlink update is authorized.

## 2026-08-23 follow-up: Sonar zero-state correction for the cache-and-summary update

The exact Draft PR #279 head
`d636753043d4e3fca7df421fce65bbc5b16a8c62` passed the public SonarQube Cloud
Quality Gate, but its New-Code endpoints still reported two OPEN code smells:
`python:S1192` at
`ci/runtime/lifecycle/summarize-connector-mode-coverage.py:138` for four
`result.json` literals, and `python:S5713` at `:199` for a redundant
`UnicodeError` next to `ValueError`. New bugs, vulnerabilities, security
hotspots, and duplicated-line density were zero; `new_coverage` was absent and
is not inferred. This is the separate `FND-SONAR-0054`, not a reopening of the
earlier cognitive-complexity/test-assertion finding.

The narrow Parent-only correction adds one `RESULT_FILE_NAME` constant and uses
it for the four runtime result-file references. It also removes `UnicodeError`
from the optional JSONL catch tuple because `UnicodeError` and
`UnicodeDecodeError` derive from the already caught `ValueError`. This preserves
the non-UTF-8 fail-soft behavior, evidence-validation order, status allowlist,
symlink rejection, bounded terminal diagnostic, and non-promoting PASS policy.
No Sonar suppression, false-positive marking, source exclusion, rule/threshold
change, Quality-Gate change, Framework/MRTS write, or Gitlink update is used.

The focused 24 summary/cache-promotion/workflow contracts, Python compilation,
and the full 133-test CI-security contract (five expected capability skips)
passed locally. The bilingual documentation checker remains blocked only by 20
pre-existing links into the intentionally uninitialized Framework submodule;
the English/German additions have matching technical literals and structure.
The normal successor commit and exact-successor SonarQube Cloud/hosted evidence
remain required before `FND-SONAR-0054` can be fixed. PR #279 remains Draft:
no Ready transition, merge, auto-merge, or master integration is authorized.

## 2026-08-23 follow-up: connector-specific CRS/no-MRTS job summary

### Goal and scope

This Parent-only interim update makes the
`.github/workflows/test-connectors-with-crs-no-mrts.yml` job summary describe
the current matrix connector rather than the whole connector set. It changes
only the Parent workflow, its two Summary helpers, focused contracts, and this
English/German Change Record pair. Framework and MRTS sources, Gitlinks, pins,
Actions, permissions, concurrency, runtime targets, and the HAProxy artifact
boundary remain unchanged.

### Summary and evidence behavior

`summarize-connector-mode-coverage.py` now renders exactly the four ordered
`PROFILES` for the validated current connector, without a redundant Connector
column. `route_state()` is unchanged, including the `nginx` contract. The
complete Framework selection and its evidence validation remain internal, but
the Markdown output is now the deterministic `Framework case counts by phase
and area` aggregation, numerically sorted by phase, with a Phase `0` row and
an exact total. It contains no case IDs, evidence paths, or long reasons.

`summarize-with-crs-no-mrts-workflow.py` renders separate configuration/start,
request/CRS, and no-MRTS/cleanup assertion rows. A `PASS` comes only from a
fixed, strictly validated structured record: Envoy, Lighttpd, and Traefik use
`evidence/normalized/<connector>/<run-id>/event.json` together with
`evidence/runtime/<connector>/<run-id>/runtime.json`; Apache and HAProxy use
only their fixed local `apache-summary.json` or `haproxy-summary.json` one-case
contract. The latter requires an explicit `live_executed` attestation before
the CRS block row can be `PASS`; all unsupported configuration, allow, rule,
bypass, no-MRTS, and cleanup claims remain `NOT_AVAILABLE`.

The reader derives its root from `RUNNER_TEMP`, the expected Parent and
Framework SHAs, and the fixed run ID. It uses descriptor-anchored no-follow
directory traversal, requires private owner-controlled directories and one
regular non-hardlinked bounded file, verifies identity across the read, and
validates JSON types, connector/profile/run identity, and relevant status
fields. It never consumes raw logs, an evidence-supplied path, or an unbounded
glob, and the existing safe `GITHUB_STEP_SUMMARY` writer is unchanged. Missing
or malformed evidence yields `PARTIAL`, `NOT_AVAILABLE`, `NOT_RUN`, or
`CANCELLED`, never an invented capability `PASS`.

The workflow passes only the controlled `--runner-temp`, `--parent-sha`,
`--framework-sha`, and `--run-id` arguments while retaining `if: always()`.
The HAProxy upload remains excluded and appears as
`skipped_by_security_policy`; the local structured summary remains a separate,
fail-closed assessment.

### Validation and limitations

The focused command below passed with 107 tests:

```text
python -B -m unittest -v tests.test_connector_mode_coverage_summary tests.test_with_crs_no_mrts_runtime tests.test_ci_security_workflows
```

It covers connector-only routes, deterministic aggregation, all three complete
normalized fixtures, conservative Apache/HAProxy behavior, live-attestation
gating, skipped/failed/cancelled runtime states, malformed/wrong-identity JSON,
unsafe path, symlink, hardlink, writable-file, and size rejection, the HAProxy
upload boundary, and the unchanged secure Summary writer. Local evidence does
not replace an exact successor hosted runtime or SonarQube Cloud analysis; both
remain pending until a normal successor push. PR #279 remains Draft with no
Ready-for-review transition, merge, auto-merge, or master integration.

## 2026-08-24 interim update: Framework scenario coverage and independent No-CRS validation

This section supersedes the earlier connector-specific summary description for
the current PR #279 follow-up only. It remains a Parent-only interim change:
the Framework and MRTS sources and Gitlinks stay unchanged, and PR #279 stays
Draft without a Ready transition, merge, auto-merge, rebase, or force-push.

The visible heading is now exactly `### Framework test scenario coverage` for
every connector/profile route. The old phase/area and CRS-family headings are
not rendered. The read-only pinned Framework commit is
`c40e924ec5c341032908e0082feba1d37ed1dfda`: No-CRS selection comes from
`tests/cases/no-crs-baseline/catalog.json` through
`ci/checks/catalog/no_crs_baseline.py`; the current CRS profile fixture is
`tests/cases/security/crs/crs_sqli_anomaly_block.yaml`. The strict Parent
display index `ci/runtime/scenarios/framework-display-index.json` is bound to
that exact Framework revision and maps only this actual fixture to `SQL
Injection`. No CRS rule family, filename, log line, or free text creates a
visible category.

All four workflows pass controlled Parent/Framework SHAs, profile run ID, and
separate selection, execution, and validation outcomes to the one renderer.
The summary distinguishes `Framework test selection`, `Framework test
execution`, and `Framework evidence validation`; it computes selected,
executed, passed, failed, unsupported, not-applicable, cancelled, and
not-executed counts from the bound plan/results. `RUN` and `PASS` require real
live evidence and a successful independent validation, not a successful
GitHub step.

The focused review found that the No-CRS renderer had still trusted a
`success` outcome plus self-consistent minimal JSON. The local correction now
directly calls the exact pinned Framework `validate_command(..., check="all")`
before No-CRS evidence can be promoted. A retained incomplete synthetic
control is rejected with exit code `2`; a canonical Framework `NOT_EXECUTED`
control validates without a host-runtime `PASS` claim. This local fix is
tracked as `FND-PARENT-0219` and requires exact-successor hosted proof before
it can be verified.

Apache and HAProxy now use the same strict normalizer and summary layout, but
their existing harnesses still only produce per-case `result.json` summaries.
They do not produce the required correlated `runtime-observation.json` for
configuration/start/reachability, allow/block/bypass, no-MRTS, and cleanup.
The workflows therefore remain fail-closed and render incomplete states rather
than fabricating `PASS`; `FND-PARENT-0218` records this blocked evidence gap.
The HAProxy raw-runtime artifact exclusion remains unchanged.

Focused local validation passed with 102 tests:

```text
python -m unittest -v tests.test_connector_mode_coverage_summary tests.test_with_crs_no_mrts_runtime tests.test_ci_security_workflows
```

The three changed Python lifecycle helpers also passed `py_compile`. A broader
Apache No-CRS selector suite has two environment-blocked tests because the
task worktree deliberately has no initialized Framework submodule; no recursive
Framework/MRTS initialization or simulated runtime was performed. The final
local security diff reviewed the 12 changed paths and found no remaining
reportable finding. Local workflow and exact-successor hosted checks remain
required before the PR can be considered verified.

The read-only Framework workflow YAML checker passed for every changed
workflow. The checker run through `make check-bilingual-docs` reported missing
Framework link targets and `make` exited `2`; `make check-doc-links` likewise
exited `2`. The deliberately uninitialized task-worktree Framework submodule
provides no local targets for those links, and neither result is a Change-
Record language or content mismatch. These documentation checks are recorded
as `blocked_environment`, not as a passing proof.

## 2026-08-24 follow-up: exact-head Sonar New-Code remediation

The exact Draft PR #279 head
`58f970b624bf3bc2be8db232911d62e6858eed27` passed its SonarQube Cloud Quality
Gate, but check run `97347899010` still reported `21 New issues`. The same
published result explicitly reported zero accepted issues, zero security
hotspots, and `0.0%` New-Code coverage and duplication. The nonzero issue
count does not meet the requested zero-state and is tracked locally by
`FND-SONAR-0054`, `FND-SONAR-0056`, and `FND-SONAR-0057`.

This narrow Parent-only successor refactors only the reported maintainability
surfaces: the common summary renderer centralizes repeated safe labels and
splits detail rendering; the CRS/no-MRTS normalizer separates source-pin,
runner-evidence, host-fact, record, and writer responsibilities while keeping
the strict Apache/HAProxy `runtime-observation.json` validation; and the
focused renderer tests use direct assertions and precomputed exceptional
inputs. It does not suppress a Sonar rule, mark a false positive, change a
Quality Gate, threshold, exclusion, action pin, workflow permission,
concurrency rule, Framework/MRTS Gitlink, NGINX boundary, or HAProxy raw-
artifact exclusion.

The current local successor passed `py_compile` for all three lifecycle
helpers and the focused Summary, runtime, and workflow contracts with `102`
tests. A new normal push and an exact-successor SonarQube Cloud analysis remain
required before any zero-issue claim. PR #279 remains OPEN and Draft: no Ready
transition, merge, auto-merge, rebase, force-push, or master integration is
authorized.
