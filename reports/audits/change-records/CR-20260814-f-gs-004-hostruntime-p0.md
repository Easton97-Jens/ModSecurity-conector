# Change Record: F-GS-004 hostruntime P0 hardening

**Language:** English | [Deutsch](CR-20260814-f-gs-004-hostruntime-p0.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260814-f-gs-004-hostruntime-p0 |
| Date (UTC) | 2026-08-14 |
| Base revision | ea3b48abab7940de49997a371f9117b409c05a2a |
| Delivery status | The current user explicitly authorized integration of Parent [PR #287](https://github.com/Easton97-Jens/ModSecurity-conector/pull/287) into `master`. The code-and-Sonar follow-up immediately before this delivery-record update is head `04f1fb81549360b22719344dee90ec0196d63f19`: all current PR checks were terminal and passing, SonarQube Cloud reported Quality Gate `OK` with zero new/accepted issues and zero security hotspots, and there were no reviews or review threads. This paired record update requires a fresh exact-head verification before the authorized merge; no pull request has been merged as of this commit. |

## Motivation and problem statement

F-GS-004 had a blanket hostruntime-coverage blocker despite a historically
successful HAProxy HTX host run. Runtime component versions also drifted across
the Parent and Framework documentation, and CI lacked one safe, machine-readable
preflight and runtime-evidence projection.

## Acceptance criteria

- The Framework owns one validated lock for the seven named runtime profiles;
  Parent-derived version documentation matches it without changing the
  unmerged Parent Gitlink.
- Parent preflight results use only the bounded status vocabulary and classify
  missing host prerequisites as `BLOCKED`.
- Incomplete host evidence cannot become `PASS`; workflow uploads remain
  sanitized and run for blocked results.
- Distribution ModSecurity headers and libraries are discovered for HAProxy
  HTX with validated precedence, architecture, linkability, and safe output.
- A fresh real HAProxy 3.2.21 HTX host run proves process start, configuration,
  loopback requests, result checks, and cleanup.

## Implementation decision and rationale

Framework Draft PR #79 introduces the canonical runtime-component lock and
hardened download behavior. Parent consumes that lock by profile at preflight
time, keeps the current Framework Gitlink unchanged, and records the dependency
instead of copying framework-owned versions.

The Parent preflight produces a bounded JSON/Markdown projection. The four
connector workflows emit a separate runtime record with `NOT_RUN` unless a
complete host lifecycle supplies the required evidence. Connector Makefile
wrappers delegate to the root preflight target without a raw shell-argument
channel. HAProxy resolves explicit paths first, then `pkg-config`, then known
distribution paths; symlink targets, architecture, `ldd` dependencies, and
the generated environment-file input are validated fail-closed.

## Changed files

- Parent preflight and lifecycle evidence: `Makefile`,
  `ci/runtime/common/hostruntime_preflight.py`,
  `ci/runtime/common/hostruntime-preflight.py`,
  `ci/runtime/lifecycle/write-hostruntime-record.py`, and
  `ci/runtime/lifecycle/run-no-crs-baseline.sh`.
- Parent workflows: `.github/workflows/test-nginx.yml`,
  `.github/workflows/test-haproxy.yml`, `.github/workflows/test-envoy.yml`,
  and `.github/workflows/test-traefik.yml`.
- HAProxy integration: `connectors/haproxy/Makefile`,
  `connectors/haproxy/htx-overlay/resolve-modsecurity.sh`, and the HTX harness
  helper/runtime scripts.
- Connector Makefile integration: `connectors/envoy/Makefile` and
  `connectors/traefik/Makefile`.
- Versioned documentation/configuration: compiler guides, Envoy, Traefik, and
  HAProxy reader documentation plus `scripts/generate_compiler_guides.py` and
  this paired English/German Change Record.
- Focused tests: hostruntime preflight, workflow-evidence, lifecycle-record,
  HAProxy resolver, and HTX harness coverage.

No Parent Gitlink, Framework source, MRTS source, cache, build output, secret,
or runtime log is included in the Parent change.

## PR #287 SonarQube Cloud and submodule follow-up

The public SonarQube Cloud PR endpoint reported three task-owned open New
Issues at the initial follow-up head:

- `python:S1192` in `ci/runtime/common/hostruntime_preflight.py`: the
  `"runtime lock"` diagnostic literal was repeated three times. The module now
  uses the single `RUNTIME_LOCK_LABEL` constant without changing diagnostics.
- `python:S1481` in the same preflight module: an unused `summary` local was
  removed; the existing output path expression remains unchanged.
- `python:S9073` in `tests/test_hostruntime_record.py`: the import bootstrap
  now uses an explicit `SPEC`/loader guard, preserving fail-fast behavior even
  when Python assertions are optimized out.

The reported recursive-submodule failure was reproduced only in the registered
isolated Parent worktree, never in the authoritative checkout. At the declared
Parent Gitlink `1260aaae411ecf88cf50dc480b80e2e20ac47901`, both
`git submodule sync --recursive` and `git submodule update --init --recursive`
exited zero and materialized the recorded Framework and MRTS revisions. The
original error text was unavailable and no failure reproduced, so no Gitlink,
Framework/MRTS source, or submodule-update-path change is justified.

The local follow-up validation passed `git diff --check`, external-cache Python
compilation, the combined preflight/record suite (38 tests), the record suite
under `python -O` (11 tests), and `make test-hostruntime-preflight` (27 tests).
At exact source follow-up head `04f1fb81549360b22719344dee90ec0196d63f19`, all
current hosted PR checks were terminal and passing; SonarQube Cloud reported
Quality Gate `OK`, zero new/accepted issues, and zero security hotspots; no
review or review thread remained. This paired delivery-record update changes
the PR head, so its fresh exact-head validation is required before the
authorized merge. No merge has occurred as of this documentation commit.

## Commands executed

- Focused Parent unittest suite for preflight, resolver, lifecycle record,
  workflow evidence, compiler guides, and bilingual documentation: passed,
  77 tests.
- `make test-hostruntime-preflight`: passed, 14 tests.
- `sh -n` for each changed Parent shell script: passed.
- `make -C connectors/haproxy check-htx-overlay`: passed.
- Each connector Makefile wrapper was exercised with the Framework PR lock;
  the underlying preflight returned `BLOCKED`/exit 77 for its intentionally
  missing host binary and recorded `runtime_status=NOT_RUN`.
- A bounded fresh
  `make -C connectors/haproxy runtime-smoke-haproxy-htx` run with isolated
  external roots passed; its host evidence is described below.

These are observed local results, not hosted CI or PR-check evidence.

## Security impact

Framework download changes retain mandatory TLS verification and SHA-256
validation, bounded timeouts, and cleanup of empty, partial, or mismatched
artifacts. Parent does not introduce an insecure download option.

Parent artifacts use an allowlisted projection and do not upload raw payloads,
URLs, credentials, or full host paths. A focused review found that a malicious
versioned library name could previously break the quoted generated resolver
environment file. The resolver now accepts only `libmodsecurity.so`,
`libmodsecurity.a`, or numeric dotted `libmodsecurity.so.<version>` names; a
regression test proves a quote/metacharacter name is blocked without executing
its marker. The root and connector Make targets also no longer append raw
preflight arguments to a shell recipe.

## Runtime evidence

The fresh retained run at
`/var/tmp/codex/ModSecurity-conector/runs/f-gs-004-parent-20260814/htx-rerun-4`
exited zero. Its `runtime-summary.txt` records HAProxy `3.2.21`,
`status=PASS`, `runtime_verified=true`, `requests_sent=true`, expected
allow/block statuses `200`/`403`, and `processes_stopped=yes`. It uses the
Framework PR #79 canonical No-CRS rules read-only. The HTX result is genuine
host evidence but remains capability-non-promoted by the existing connector
policy.

The current component preflights retain NGINX, HAProxy SPOE/SPOP, Envoy, and
Traefik as `BLOCKED`, not `FAIL`, because their expected binary and source are
absent. Envoy `ext_authz` and Traefik `forwardAuth` retain non-applicable
response-body/P4 semantics.

## Known limitations

- Framework PR #79 is merged as Framework `master`
  `01952978772995c054ba6a4cba86adc5d0cd1e7d`. The Parent Gitlink remains
  intentionally unchanged; no Parent pointer update is selected in this task.
- Hosted PR evidence at the immediately prior exact source head does not
  substitute for the fresh exact-head validation required by this paired
  delivery-record update.
- No NGINX, HAProxy SPOE/SPOP, Envoy, or Traefik host process was started:
  their required binary/source prerequisites are absent.

## Remaining risks

The authorized Parent integration remains gated by fresh exact-head PR checks,
review/thread and protection evidence after this paired delivery-record update,
then by resulting-`master` workflows. Platform-specific package layouts beyond
the exercised Linux distribution layout need their normal CI coverage. The
non-HTX components remain environment-blocked rather than validated runtime
passes.

## Checks not run and rationale

- Full host smokes for NGINX, HAProxy SPOE/SPOP, Envoy, and Traefik were not
  run because their reviewed binaries and sources are unavailable locally;
  each preflight has a retained `BLOCKED` record.
- `actionlint` was not run because it is not installed locally; workflow YAML
  parsing and the workflow-contract tests passed.
- The current user has authorized the Parent merge, but no merge or
  resulting-`master` check is claimed as of this record commit. The fresh
  exact-head PR validation required by this documentation update must complete
  first. A Parent Gitlink update remains out of scope.

## Final diff and review status

The final scoped Parent diff check, 77-test focused suite, HTX overlay check,
shell syntax/ShellCheck checks, compiler-guide check, and sealed scoped
security-diff review passed. The Sonar follow-up at
`04f1fb81549360b22719344dee90ec0196d63f19` also passed its focused local and
hosted exact-head checks. The Framework and Parent remain separate Git
boundaries; Framework PR #79 is merged, while this Parent change deliberately
does not stage a Gitlink update. This paired record update requires one fresh
exact-head verification before the authorized Parent merge. No pull request
has been merged as of this record commit.
