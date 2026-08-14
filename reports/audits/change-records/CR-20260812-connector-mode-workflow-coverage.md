# Change Record: static connector-mode workflow coverage

**Language:** English | [Deutsch](CR-20260812-connector-mode-workflow-coverage.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260812-connector-mode-workflow-coverage |
| Date (UTC) | 2026-08-12, reconciled 2026-08-14 |
| Base revision | `ea3b48abab7940de49997a371f9117b409c05a2a` |
| Delivery status | Draft PR [#279](https://github.com/Easton97-Jens/ModSecurity-conector/pull/279) remains at remote head `63ad4f5ed359ba2be9abe955cb1c82e7dfcb3846`. The local task branch normally merged current master in `4e224b23c5973c34be3ef4f336b7772a0b13c094` and contains the locally validated Parent CRS-acquisition repair above it. No corrected head has been pushed, no Ready-for-Review transition occurred, and the remaining clean-worktree runtime controls plus all exact-head hosted evidence are pending. |

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

The focused no-CRS/with-MRTS HAProxy branch sets the existing literal
`RUNTIME_COMPONENT_TARGET=haproxy` selector before its native case target.
That branch does not need CRS and can therefore avoid the unrelated Apache
archive without changing its real HAProxy runtime path. The two with-CRS
HAProxy branches deliberately retain the existing all-components preparation:
the current runtime snapshot binds their CRS source to that preparation cache,
and a separate fresh CRS fetch would not become part of the target-scoped
snapshot. Apache intentionally remains on its ordinary native path, which
still requires its reviewed APR-util tuple.

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
each passed with HTTP `403` under the repaired source topology. An initial
canonical Apache no-CRS run executed both legitimate cases but its evidence
finalizer correctly refused `PASS` because the source worktree was dirty. It
is diagnostic-only; the full eight-mode fresh clean-worktree series remains
required before publication.

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

`FND-PARENT-0128` is locally fixed but remains a release/integration blocker
until the clean-worktree eight-mode runtime series and all exact-head hosted
cells pass. Framework/MRTS source and the fail-closed provenance guard remain
unchanged. Actionlint/zizmor, required checks, Sonar disposition, and all
hosted matrix evidence are still unverified. Envoy, Traefik, and lighttpd MRTS
cells remain explicitly unsupported until an independently authorized
capability and evidence change exists. No failure may be hidden by weakening
negative, static-contract, cleanup, or security guards.

## Checks not run and rationale

- Local actionlint, actionlint-mediated ShellCheck, and zizmor scans: their
  pinned binaries are absent and fetching tools is outside this task's local
  validation authority. Exact-head hosted checks are required instead.
- Full clean-worktree eight-mode local runtime series and exact-head hosted
  connector matrix: both are pending the focused local commit that the native
  no-CRS evidence finalizer requires before it can attest a clean checkout.
- Corrected-head PR checks, SonarQube Cloud applicability, and Ready-for-Review
  disposition: no corrected commit was pushed, so no exact new PR head exists;
  merge and auto-merge remain explicitly out of scope.

## Final diff and review status

This is an in-progress local-remediation record. The normal master merge
retained the current recorded Framework Gitlink and no task-owned Gitlink diff
exists. The Parent CRS repair, its focused regressions, the current APR-util
provenance, and the initial repaired focused controls passed locally. A later
final review must verify the clean-worktree runtime series, a published exact
committed head, remote branch, PR head, four workflow runs, all 20 cells,
actionlint, ShellCheck, zizmor, required checks, and Sonar applicability
before PR #279 is marked Ready for Review. No push, Ready transition, merge,
or auto-merge is recorded here.
