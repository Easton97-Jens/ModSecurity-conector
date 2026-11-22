# Change Record: CR-20261119-local-prerequisite-autoprovision

**Language:** English | [Deutsch](CR-20261119-local-prerequisite-autoprovision.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261119-local-prerequisite-autoprovision |
| Date (UTC) | 2026-11-19 |
| Base revision | `b79c3d93efbb8330f121caf8fb7c1a7874195e57` |

## Motivation and problem statement

Local runs depended on two manually prepared prerequisites.

- Python: the root Makefile selected `.venv/bin/python` only when a manually
  prepared `.venv` existed and otherwise fell back to `python3`, which lacks the
  locked PyYAML dependency. The Framework `doctor`/`doctor-quick` diagnostics
  stopped with `BLOCKED: venv missing (.venv/bin/python); run make setup-dev`
  (observed at the base revision: exit 77 from the Framework target, make exit
  2). The documented `make setup-dev` path installs an unpinned `pip` upgrade and
  a PyYAML version range, which the repository Python policy does not allow as an
  automatic source.
- Security tools: the workflow fixture checks read only the checksum-verified
  `$RUNNER_TEMP/security-tools/zizmor`. Locally nothing provided it, so `make
  test` stopped with `FAIL: checksum-verified zizmor executable is unavailable`
  (observed: exit 2 after 282 s). A `zizmor` on `PATH` (observed `1.29.0`, while
  the lock pins `v1.32.0`) is deliberately not used. The Go analysis tools were
  not pinned in the repository at all; a locally installed older `staticcheck`
  could not read Go 1.27 export data.

Both must instead always match the current version contract and be created
only where a local run needs them.

## Acceptance criteria

- A local `make` invocation of any Framework-delegated target, and of
  `framework-native-selftest`/`framework-go-test`, first ensures a Python
  environment for the exact `.python-version` interpreter; no manual step.
- The environment receives dependencies only through the Framework-owned,
  hash-verifying `install-ci-dependencies.py`.
- A changed `.python-version`, Framework lock, Framework installer or helper, and
  drifted installed contents, each lead to a newly provisioned environment; an
  interrupted provisioning is retried, not reported as unmanaged.
- A missing exact interpreter is `BLOCKED` (exit 77); nothing is substituted.
- Environments can be kept outside the checkout (`PYTHON_ENV_ROOT`); the checkout
  then carries only an ignored `.venv` link. A separate Framework-owned
  environment is available on request.
- With `RUNNER_TEMP` set, delegated targets first install the locked release
  tools and the newly locked Go tools at run time into the run-private
  `$RUNNER_TEMP/security-tools`, as regular files matching the lock; nothing is
  installed elsewhere.
- CI (`CI` or `GITHUB_ACTIONS` is `true`) and an explicitly selected `PYTHON`
  keep their previous behavior.
- Existing unmanaged `.venv` directories, foreign links and symlinked tool
  directories are never modified.
- The existing Framework Makefile contracts remain satisfied.

## Implementation decision and rationale

- `ci/tools/ensure-python-env.py` (standard library only). Its identity is the
  SHA-256 over the exact interpreter version and real path, `.python-version`,
  the helper itself and the pinned Framework inputs
  `connector_suite/requirements-ci.lock`, `connector_suite/requirements-ci-build.lock`,
  `connector_suite/modsecurity_connector_ci/tools/install-ci-dependencies.py` and
  `requirements-ci.lock`. A stamp records identity, inputs, installer receipt and
  an installed-distribution probe; the fast path accepts only a matching identity
  with an unchanged probe. A provisional stamp (`state: incomplete`) is written
  before old helper-owned contents are removed. Cleanup preserves this stamp,
  unlinks symlinks without following them and invokes `venv` without `--clear`.
  Failed creation and interrupted cleanup retain ownership for the next retry.
- Without `PYTHON_ENV_ROOT` the environment is `.venv` in the checkout. With it,
  versioned environments `<role>-<version>-<identity>` live in that store, the
  links `parent`/`framework` point to the latest provisioned one and are repaired
  when missing, and `.venv` links to this checkout's exact environment; an
  existing helper-created link selects its store automatically. Provisioning
  holds an exclusive `flock` on the store (or checkout) directory.
- `ci/tooling/go-tools.lock.json` pins `staticcheck` (`honnef.co/go/tools`
  `v0.8.2`, MIT) and `govulncheck` (`golang.org/x/vuln` `v1.10.0`,
  BSD-3-Clause) with their `h1:` module sums.
- `ci/tools/ensure-security-tools.py` installs every release tool of
  `ci/tooling/security-tools.lock.yml` through the existing checksum-verifying
  `fetch_security_tool.py`, and every Go tool by `go install` with the Go of
  `.go-version` (`GOTOOLCHAIN=local`, `CGO_ENABLED=0`, `-trimpath`) after
  verifying the module sum, then verifies the binary's build information. A stamp
  per tool records the producing lock entry; missing, changed, symlinked or
  unstamped binaries are replaced atomically through a staging directory under an
  exclusive `flock`. A different Go toolchain blocks only the Go tools.
- Root `Makefile`: `PYTHON_ENV_AUTO`, `PYTHON_ENV_ROOT`, `PYTHON_BASE` and
  `SECURITY_TOOLS_AUTO`; `FORCE` (prerequisite of the unchanged `%` forwarder)
  depends on `python-env` and `security-tools-auto`, and the two direct Framework
  entries on `python-env`, so the Framework sub-make's existing `.venv/bin/python`
  default finds the provided environment. `security-tools` is the strict explicit
  form; the automatic step reports a tool it cannot install as a warning, so only
  the checks that need that tool fail. Locally, `setup-dev`/`install-dev-deps`
  resolve to the managed Python step instead of the Framework's unpinned
  bootstrap. The `%` forwarder and `framework-native-selftest` recipe lines that
  the Framework contract pins are unchanged.
- `python-env-framework` provisions a separate environment validated with
  `--framework-lock modules/ModSecurity-test-Framework/requirements-ci.lock`; it
  requires a store and is created only when requested.
- `.gitignore` ignores `.venv` as a directory or link.
- No Framework or MRTS file changed. The Framework `doctor.sh` path check is
  satisfied by the provided `.venv`; decoupling it is a separate Framework task.

## Changed files

- `.gitignore`
- `Makefile`
- `ci/tools/ensure-python-env.py` (new)
- `ci/tools/ensure-security-tools.py` (new)
- `ci/tooling/go-tools.lock.json` (new)
- `ci/README.md`, `ci/README.de.md`
- `docs/build/README.md`, `docs/build/README.de.md`
- `docs/getting-started.md`, `docs/getting-started.de.md`
- `docs/reference/variables.md`, `docs/reference/variables.de.md`
- `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`
- `reports/audits/change-records/CR-20261119-local-prerequisite-autoprovision.md`,
  `reports/audits/change-records/CR-20261119-local-prerequisite-autoprovision.de.md`

## Commands executed

All commands ran through `rtk bypass` in a task worktree at the base revision
with the pinned Framework `95f228936efe17fda24f21323ad87cd698940b48` and MRTS
`ee2174431c4edf97e66afe32558ce8454deb2397`, without a `PYTHON` override and with
external build/temporary roots. The scenario suites ran against the final helper
versions.

| Command | Result |
| --- | --- |
| `make doctor-quick` before the change | exit 2: `BLOCKED: venv missing (.venv/bin/python)` and missing PyYAML with `PYTHON=python3` |
| `make test` with an empty `RUNNER_TEMP`, before the security-tool helper | exit 2 after 282 s: `FAIL: checksum-verified zizmor executable is unavailable` |
| Python scenario suite, 22 checks | all passed: in-checkout provisioning (`pip 26.2.2`, `pyyaml 6.0.3`, receipt `libyaml_extension: false`); fast path about 0.6 s; `doctor-quick` exit 0 with `venv: detected`; drift reprovisioned; `.python-version` `3.15.9` blocked (77, make 2); store migration, detection and `parent`/`framework` links; Framework environment, and `BLOCKED` without a store; CI and explicit `PYTHON` not managed; unmanaged directory and foreign link blocked and unchanged; concurrent runs provision once; missing links repaired without provisioning; an interrupted run (download through an unreachable proxy) retried successfully |
| same interrupted-run scenario with the helper before the provisional stamp | retry `BLOCKED: ... is an unmanaged environment` (defect reproduced, then fixed) |
| `make security-tools RUNNER_TEMP=<fresh>` | exit 0: `actionlint 1.7.12`, `zizmor 1.32.0`, `gitleaks 8.30.1`, `staticcheck 2026.2.2 (0.8.2)`, `govulncheck v1.10.0`; directory mode `0700`; repeat about 0.4 s |
| security-tool scenario suite, 12 checks | all passed: unstamped tools replaced; a stale stamp reinstalls only that tool; a symlinked tool is replaced without touching its target; a different Go blocks only the Go tools (77) while the automatic hook warns and the target runs; a symlinked destination is refused; no automatic install in CI or without `RUNNER_TEMP`; concurrent runs install once; `check-workflow-fixture.sh insecure`/`safe` report `reject`/`accept` |
| locked `staticcheck` on `connectors/envoy/ext_proc` | runs on Go 1.27 code (no export-data error); reports existing `ST1005`/`U1000` findings, not changed here |
| `make check-remaining-connectors-build-wiring`, `check-repository-architecture`, `check-python-version-contract`, `check-project-versions`, `check-active-inventory`, `check-framework` | exit 0 each |
| `ci/tools/new-change-record.py check`; `make check-variable-documentation`; `make check-doc-links`; `make check-bilingual-docs` | exit 0 each |
| `make quick-check` on the final diff, environment from the local `msc-test-env.sh` with a fresh `RUNNER_TEMP` | exit 0 after 814 s; the automatic step installed all five tools first, the Python step took the fast path |
| `make test` with an earlier helper revision | exit 2 after 1808 s; the four workflow fixture executions passed with the run-private `zizmor`; `runtime.no-crs.apache` ran with 0 failed cases but its evidence gate refused PASS because the worktree was not clean; the cached `httpd` also resolved `libpcre2-8` from the system library path, so this run is not valid runtime evidence |

## Provisioning retry follow-up, 2026-11-21

The published helper wrote its incomplete stamp after `venv --clear`. A failure
during that subprocess could leave a partially created environment without a
stamp, so the next attempt refused it as unmanaged. The follow-up preserves the
stamp while clearing the old contents and creating the environment.

A task-owned standard-library regression suite outside the checkout reproduced
the missing stamp against the published helper. All five cases passed after the
change. They cover failed creation followed by retry, interrupted cleanup,
preservation of an unmanaged environment, safe symlink removal and real local
venv creation with `pip check`. The reviewed dependency installer was stubbed
only in the real-venv case, and no packages were downloaded. The Parent-owned
Python environment ran these checks. Ruff was unavailable in that environment.

## Security impact

Dependency and tool installation is narrowed for local runs: Python packages
come only from the Framework installer's exact official URLs and SHA-256 pins
(pure-Python PyYAML, no C extension); release tools only from their locked
official assets with SHA-256 verification; Go tools only from exact module
versions whose `h1:` sum is checked before and whose build information is checked
after the build. The first installation downloads these locked artifacts
(`files.pythonhosted.org`, GitHub releases, the Go module proxy with the checksum
database). The unpinned `setup-dev` bootstrap is no longer used locally. The
helpers refuse a store inside the checkout or a symlinked tool directory, replace
only their own links and stamped artifacts, and never delete unmanaged
environments. CI behavior, workflows, scanners and quality gates are unchanged.

## Runtime evidence

Not applicable: no connector product code, host configuration or runtime path
changed. The checks above are local tooling evidence only.

## Known limitations

- The first local run, and each identity or lock change, needs network access
  and about half a minute for Python and up to about a minute for the Go builds.
- An exact `.python-version` interpreter must exist; otherwise every delegated
  target is `BLOCKED` until `PYTHON_BASE` or an explicit `PYTHON` is set. The Go
  tools need the exact `.go-version` toolchain.
- Superseded environments in a store are not removed automatically.
- Inside the Framework sub-make, `bootstrap-all` and `cloud-quick-check` still
  call the Framework's own `setup-dev`; a later run detects the drift and
  provisions again. The Framework's standalone Makefile provisions nothing.
- Each delegated local target adds both checks (together about 1 s).

## Remaining risks

A provider-side removal of a locked artifact would block new installations until
the locks are updated. `govulncheck` results depend on the online vulnerability
database at run time.

## Checks not run and rationale

- The current SonarCloud findings and CI results must be verified after publishing the follow-up.
- `make test` on a clean committed revision with the pinned PCRE2/APR runtime
  libraries was not run; the earlier runs above are not counted as passed.
- Hosted CI runs only after the push.
- The local Git pre-commit/pre-push Secrets hook could not run because its
  integration receipt was missing; by explicit user decision the commit and push
  bypassed it. A manual Secrets scan of every staged blob passed.

## Final diff and review status

Task branch `claude/python-env-autoprovision-20261119`, delivered as a draft
pull request for review; no merge is part of this change.

The security-tool helper binds the canonical destination to the independently configured `RUNNER_TEMP/security-tools` directory and checks the checkout boundary before installation. The root Makefile exports this run context. Direct helper calls must configure it, and `--base` confirms the interpreter already running the Python-environment helper. `PYTHON_BASE` still selects the interpreter used by the Makefile to launch the helper. Eight destination checks, five interpreter-identity checks, five provisioning-retry checks and the Makefile environment-export check passed. The SonarCloud result for this follow-up remains to be verified after publication.
