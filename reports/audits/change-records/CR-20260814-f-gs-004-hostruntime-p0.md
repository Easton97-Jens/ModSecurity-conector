# Change Record: F-GS-004 hostruntime P0 hardening

**Language:** English | [Deutsch](CR-20260814-f-gs-004-hostruntime-p0.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260814-f-gs-004-hostruntime-p0 |
| Date (UTC) | 2026-08-14 |
| Base revision | ea3b48abab7940de49997a371f9117b409c05a2a |
| Delivery status | Local implementation, validation, and scoped security review complete; Parent Draft PR pending creation. Framework Draft PR #79 is a required dependency. |

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
  HAProxy reader documentation plus `scripts/generate_compiler_guides.py`.
- Focused tests: hostruntime preflight, workflow-evidence, lifecycle-record,
  HAProxy resolver, and HTX harness coverage.

No Parent Gitlink, Framework source, MRTS source, cache, build output, secret,
or runtime log is included in the Parent change.

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

- The Framework lock is supplied from unmerged Framework Draft PR #79. The
  current Parent Gitlink must remain unchanged until the Framework lifecycle
  completes through its own authorized merge process.
- No hosted workflow, exact Parent PR-head check, or hosted artifact was
  observed locally.
- No NGINX, HAProxy SPOE/SPOP, Envoy, or Traefik host process was started:
  their required binary/source prerequisites are absent.

## Remaining risks

The Parent Draft PR remains dependent on Framework PR #79 and will require
fresh exact-head hosted checks after both PRs exist. Platform-specific package
layouts beyond the exercised Linux distribution layout need their normal CI
coverage. The non-HTX components remain environment-blocked rather than
validated runtime passes.

## Checks not run and rationale

- Full host smokes for NGINX, HAProxy SPOE/SPOP, Envoy, and Traefik were not
  run because their reviewed binaries and sources are unavailable locally;
  each preflight has a retained `BLOCKED` record.
- `actionlint` was not run because it is not installed locally; workflow YAML
  parsing and the workflow-contract tests passed.
- Hosted CI, PR checks, review, merge, and a Parent Gitlink update are not
  claimed because delivery has not occurred and merge is not authorized.

## Final diff and review status

The final scoped Parent diff check, 77-test focused suite, HTX overlay check,
shell syntax/ShellCheck checks, compiler-guide check, and sealed scoped
security-diff review passed. Separate commits and the Parent Draft PR remain
pending. The Framework and Parent remain separate Git boundaries; Framework
Draft PR #79 must merge first, and this Parent change deliberately does not
stage a Gitlink update. No pull request has been merged.
