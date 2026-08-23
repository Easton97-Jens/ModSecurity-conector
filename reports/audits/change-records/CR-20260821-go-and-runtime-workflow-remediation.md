# Change Record: Go and runtime workflow remediation

**Language:** English | [Deutsch](CR-20260821-go-and-runtime-workflow-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260821-go-and-runtime-workflow-remediation |
| Date (UTC) | 2026-08-21 |
| Base revision | `57187eb210ab96b7e1eed22221fa367671d01820` |
| Delivery status | Parent Draft PR #313 is task-owned. Before this paired record correction its exact head was `d06528df0daca17c66c9771dad449b5e341ad986`; all applicable PR checks and SonarCloud passed, and controlled Five Connector No-CRS run `32582786272` completed. The current user explicitly authorizes protected integration of PR #313 and accepts only FND-PARENT-0148's stated missing r13 host-proof risk. This documentation correction creates a new PR head that must be rechecked before any merge; no merge is asserted here. |

## Motivation and problem statement

The `Update Go version` workflow stopped before its resolver because the shared
Go-version contract still required an obsolete Bash validator while CodeQL uses
the reviewed Awk validator. Three independently recorded runtime workflow
failures also needed a Parent-only remediation: a report root inside the source
checkout, incomplete five-connector failure evidence, and unavailable heavy
smoke component reports after the ModSecurity v3 provenance guard blocks.

The already confirmed `update-submodules.yml`, `update-python-version.yml`, and
`update-workflow-tools.yml` paths are intentionally unchanged. NGINX remains a
separate workflow path. Dependabot PRs #306, #307, and #308 were closed only
after their CodeQL v4.37.7 changes were verified on merged PR #311 and current
`master`; their remote branches were retained.

## Acceptance criteria

- The shared Go contract accepts the exact trusted Awk validator used by the
  checked-in CodeQL workflow and continues to reject invalid selectors, pins,
  and version files fail-closed.
- `open-connectors-smoke.yml` writes runtime reports only below its private
  verified build root, never below `$GITHUB_WORKSPACE`, and its initialization
  block succeeds under `set -eu` without an inherited `BUILD_ROOT`.
- The five-connector profile preserves canonical evidence validation while
  retaining bounded, private, failure-only diagnostic artifacts outside its
  success aggregate.
- Heavy smoke preserves the ModSecurity v3 provenance guard and exposes its
  private component reports in existing smoke artifacts; it does not weaken
  provenance or modify Framework/MRTS.
- Focused regression and security-contract checks pass. The final-head No-CRS
  run validates the follow-up capture correction; the complete baseline remains
  independently blocked by the Framework-owned provenance configuration.

## Implementation decision and rationale

- The Go checker now holds the exact reviewed Awk expression in
  `TRUSTED_VERSION_VALIDATOR`; tests cover the checked-in CodeQL workflow.
  `update-go-version.yml` itself remains publisher-gated and unchanged.
- The open-connectors initialization binds
  `build_root="$verified_root/build"` before exporting both `BUILD_ROOT` and
  `RUNTIME_REPORT_OUTPUT_ROOT`. Its regression executes the extracted shell
  block with `bash --noprofile --norc -eu` and no ambient `BUILD_ROOT`.
- The reusable five-connector profile writes identity-bound diagnostics only on
  failure below its private verified root. The artifact name is deliberately
  outside the canonical `five-no-crs-*` aggregate pattern.
- The first corrected No-CRS run proved that the capture step used `$CONNECTOR`
  under `set -u` without a step-local binding. It now receives the closed
  resolver matrix value explicitly; the contract test scopes that assertion to
  the capture step.
- Heavy smoke exports runtime component reports below its existing private
  build root and uploads them with the established diagnostic artifact path.
  The Framework-owned provenance guard remains fail-closed; no Framework,
  MRTS, Gitlink, cleanup, root broker, or NGINX workflow change is made.

### Continuation 2026-08-22: target-scoped NGINX isolation

After the normal base merge, controlled Five Connector No-CRS run `32577438675`
at `ec8cccc6211534e92eba7013cf76747c135d7a4a` reached the Parent preparation
boundary but failed all five selected non-NGINX jobs at
`nginx_pinned_provenance_ref_mismatch`. The Framework tuple supplies separately
managed `release-1.31.4` metadata while Parent retains its independently
reviewed `release-1.31.3` tuple. NGINX was not dispatched; therefore the
correct repair is target isolation rather than a NGINX repin.

`required_runtime_component_sources` now rejects unknown targets fail-closed
and consumes NGINX URL, provenance, and protocol metadata only for `all` and
`nginx`. It also creates an NGINX connector plan only for those targets. The
existing strict NGINX repository/tag/ref/asset/SHA-256 and protocol/TLS checks
are unchanged for `all` and `nginx`. This leaves NGINX separate, makes
`shared`, `apache`, and `haproxy` independent of unused NGINX metadata, and
does not modify Framework, MRTS, a Gitlink, an NGINX pin, a publisher, or a
cleanup workflow.

### Continuation 2026-08-22: canonical hostruntime projection and Lighttpd inventory

The exact-head follow-up run `32579807096` at
`679ae784db021d72343fdce693f3033969227960` passed the former non-NGINX NGINX
guard for all five selected connectors. Apache, Envoy, and HAProxy each
finalized a passing runtime result, but the unchanged Framework validator then
correctly rejected the two Parent-created files `hostruntime-record.json` and
`hostruntime-summary.md`: they were produced after finalization but were not
declared in the canonical manifest. The Parent now projects only these two
fixed relative files into both artifact maps with SHA-256 values and refreshes
the existing manifest result-artifact checksum only after verifying its prior
binding. Malformed maps, unsafe paths,
symlinks, non-regular files, checksum mismatches, and write failures remain
fail-closed; the Framework validator is unchanged.

The same run showed that the Lighttpd smoke itself passed its two requests,
but its final evidence could not pass because the version inventory used a
different cache path. For the generic profile, the runner now accepts only the
fixed staged path `CONNECTOR_BUILD_ROOT/lighttpd-connector/bin/lighttpd`, if
it is an absolute, regular, executable, non-symlink file. Every absent or
unsafe staged file leaves the version `not_provisioned`; inherited
`LIGHTTPD_BIN`, system, and shared-cache fallbacks are not consumed. The
full-lifecycle mapping remains unchanged. Traefik remains fail-closed and
outside this Parent-only fix because its Framework-provided binary violates a
separate trusted-root control.

### Continuation 2026-08-22: delivery authorization and FND-PARENT-0148 scope

The current user now explicitly authorizes protected Parent `master`
integration of task-owned PR #313 and accepts the exact residual
FND-PARENT-0148 risk for that integration only. No successful private Traefik
`no-crs/with-mrts` host receipt exists: r10--r12 failed closed before host
start, and the normal PR #313 run reobserved a trusted-root containment block
before requests. The acceptance neither verifies nor closes the finding,
relaxes no control, and expires with the first fresh r13 result. A failure
must be repaired through a new PR, never directly on `master`.

The historical r13 runner is not part of PR #313 and requires a separate
Parent runtime task with prepared read-only Framework/MRTS inputs. It cannot
be claimed as an exact PR #313 check or be started by this PR's checkout.
NGINX remains separate and was not dispatched.

## Security impact

This change touches GitHub Actions runtime paths, artifact evidence, and an
update contract. It retains pinned actions, read-only permissions, disabled
checkout credential persistence, fail-closed evidence aggregation, and the
ModSecurity v3 provenance guard. A focused diff review found that the initial
open-connectors patch referenced an unset shell `BUILD_ROOT`; the correction
binds the value to the trusted verified root and the strengthened regression
reproduces the `set -eu` control. The final focused review found no remaining
reportable security candidate.

## Changed files

- `.github/workflows/open-connectors-smoke.yml`
- `.github/workflows/reusable-five-connectors-profile.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `ci/checks/common/check-go-version-contract.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/runtime/lifecycle/resolve-lighttpd-host-binary.py`
- `ci/runtime/lifecycle/write-hostruntime-record.py`
- `tests/test_all_connectors_no_crs_workflow_contract.py`
- `tests/test_full_smoke_workflow_contract.py`
- `tests/test_go_version_contract.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_resolve_lighttpd_host_binary.py`
- `tests/test_hostruntime_record.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `tests/test_runtime_path_policy.py`
- this paired Change Record and `reports/audits/change-records/README.md` /
  `reports/audits/change-records/README.de.md`

## Commands executed

| Check | Actual result |
| --- | --- |
| Go/updater, five-connector, heavy-smoke, and open-connectors contracts | passed: 34 tests |
| `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-go-version-contract` | passed |
| CI security and Python version contracts | passed: 52 tests |
| Follow-up five-connector contracts after step-local matrix binding | passed: 17 tests |
| Follow-up CI-security contracts after step-local matrix binding | passed: 28 tests |
| `git diff --check` | passed |
| Focused open-connectors `set -eu` shell regression | passed: 1 test; the private report root was exported exactly |
| Focused security re-review | passed: no remaining candidate for the corrected open-connectors path |
| `python -m py_compile tests/test_prepare_runtime_components.py ci/provisioning/components/prepare-runtime-components.py` | passed |
| `python -m unittest -v tests.test_prepare_runtime_components` | passed: 43 tests; 5 expected skips because the task worktree does not initialize the Framework Gitlink |
| `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract` | passed: 123 tests; 5 expected namespace/identity skips; `actionlint`, `zizmor`, and `gitleaks` lock validation passed |

## Runtime evidence

The original hosted failures are retained as evidence: Go run `32006247568`,
open-connectors run `32485037344`, five-connector No-CRS run `32485072808`, and
heavy-smoke run `32485033800`. On exact Draft-PR head
`a0c527cdb57ec97c663e983c4fbe195a6f2361b0`, the corrected Go contract and
pull-request checks passed. Open-connectors run `32494251838` initialized its
private report root successfully before the independent provenance blocker;
heavy-smoke run `32494271540` retained both no-CRS and with-CRS reports and did
not request cleanup. The task dispatches only safe read-only/no-cleanup
workflows; no publisher, artifact deletion, root broker, or Framework/MRTS
action is included.

The first corrected Five Connector No-CRS run `32494262558` retained the new
private diagnostic artifacts and exposed the now-corrected unset `$CONNECTOR`
in the capture step. The successor final-code-head run `32495576734` at
`bf21d726f3d998a333ce57dc935efa2d8782a75c` completed Capture and Upload
bounded diagnostics for all five connectors. Its result-only aggregate failed
closed because all five still reached the shared
`modsecurity_v3_provenance_configuration_failed` blocker.

The later controlled Five Connector No-CRS run `32577438675` at merged-base
head `ec8cccc6211534e92eba7013cf76747c135d7a4a` is bounded evidence for a
separate Parent target-scope defect: Apache, HAProxy, Envoy, Traefik, and
Lighttpd all stopped at `nginx_pinned_provenance_ref_mismatch` before their own
runtime stages. The reusable workflow selected Apache/HAProxy or `shared` and
did not dispatch NGINX. Its secret-free retained diagnostic summary is
hash-bound in the task evidence manifest. A rerun on the subsequent exact PR
head then completed as `32582786272` at
`d06528df0daca17c66c9771dad449b5e341ad986`: Apache, HAProxy, Envoy, and
Lighttpd passed runtime smoke, canonical evidence, publish, and cleanup.
Traefik correctly stopped before requests at its separate trusted-root control
because the staged binary was below the required shared cache root, so the
aggregate failed closed. No NGINX, publisher, deletion, root-broker, Framework,
or MRTS workflow was dispatched for this continuation.

## Checks not run and rationale

`actionlint` and `zizmor` are not installed in the available environment.
Framework-dependent aggregate checks cannot run because the task worktree has
an uninitialized Framework Gitlink; it is intentionally not initialized or
modified. The controlled final-code-head No-CRS execution and applicable PR
checks completed before this documentation-only correction; the new head must
receive its own exact-head checks before merging.

The requested r13 proof is not run here: its historical runner is absent from
PR #313, lives on a separate historical Parent branch, and needs a separately
authorized runtime scope with prepared read-only Framework/MRTS inputs. It is
not safe or truthful to substitute the normal no-CRS run, initialize a nested
checkout, or treat a historical r13 result as PR #313 evidence.

## Known limitations

The five-connector and ModSecurity v3 findings are not declared fixed by the
new diagnostics alone. Their historical direct job logs are unavailable, and
the provenance guard is Framework-owned. The next corrected hosted runs must
classify the connector failures and expose the component report before any
underlying connector or Framework cause can be repaired.

The local runtime-path aggregate retains one environment-blocked self-test and
five Framework-Gitlink-dependent HAProxy skips; the task intentionally does
not initialize, update, or modify that submodule. These do not cover the new
target-scope regression, which has its own passing focused controls and a
passing full `tests.test_prepare_runtime_components` module.

## Remaining risks

Diagnostic artifacts contain bounded runtime/log/report evidence and must stay
free of secrets. Current workflows pass no repository secrets, retain
`contents: read`, and keep the diagnostic artifact separate from the canonical
success aggregate. The hosted runner remains the required final execution
boundary for the corrected workflow behavior.

For protected integration of PR #313 only, the current user accepted the
remaining FND-PARENT-0148 risk described above while r13 is pending. The risk
is limited to lack of a successful private Traefik no-CRS/with-MRTS receipt and
may include a later failure before or during transaction, audit/receipt, or
cleanup validation. It does not weaken the fail-closed controls or extend to
Framework, MRTS, Gitlinks, NGINX, another PR, or a direct master write.

## Final diff and review status

The Parent-only source change is in Draft PR #313. The three replaced
Dependabot PRs are closed with branches retained. The current user has
authorized protected integration of PR #313 only, subject to a fresh exact-head
PR verification after this record update. No branch deletion, Framework/MRTS
modification, NGINX consolidation, direct master write, or control weakening is
authorized or asserted. The continuation source and regression change has a
second focused security review with no high/critical finding beyond the
explicitly tracked and scoped FND-PARENT-0148 residual risk.
