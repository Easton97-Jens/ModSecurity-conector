# FND-PARENT-0056 — Ready NGINX runtime snapshots omit the Parent Common source root

## Identity

| Field | Value |
| --- | --- |
| Category | `ci_failure` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P1` / `not_applicable` / `confirmed` |
| Status / feasibility | `fixed` / `feasible_now` |
| Release blocker / security relevance | yes / yes |
| Scope | Parent #74 NGINX runtime-snapshot publication; Framework and MRTS source remain unchanged |

## Observation, impact, and preconditions

The exact Parent PR #74 head `a0f337b8e45e5661b1ed09c7bf39b958548fbd14`
completed component preparation and readiness in both hosted producers. NGINX
then failed configuration with `ngx_http_modsecurity: missing Common source
root; set MSCONNECTOR_COMMON_SRC`; the strict terminal evidence gate was
skipped and accepted no failed evidence.

The direct matrix consumes an invocation-local snapshot after NGINX cache
preparation. Framework materializes the adapter away from Parent Common source
files, and NGINX configure compiles those Common C sources. The omission blocks
fresh legitimate evidence and protected #74 integration. No production exploit
is claimed; the relevant security boundary is the Parent-controlled build
environment, which must not accept a job-supplied source path or a fallback.

## Cause, source-to-sink, and remediation

Parent cache preparation supplies a controlled Common source directory while
building the managed NGINX entry. Its later `runtime_env` reconstruction
published the ready binary, module, build directory, and owner root but omitted
`MSCONNECTOR_COMMON_SRC`. `with-runtime-components.sh` sources that local
snapshot for the direct matrix. Framework's `run_blocked ... env` normally
inherits the value when it is present; it neither clears nor replaces it.

The Parent-only repair uses `nginx_runtime_environment` to derive
`MSCONNECTOR_COMMON_SRC` only from the resolved
`CONNECTOR_ROOT/common/src` for a ready NGINX record. An unready record
publishes no NGINX runtime values. The existing cache-owner containment and
Framework fail-closed missing-source check remain unchanged. Framework and
MRTS source, heads, Gitlinks, branches, and delivery state remain untouched.

The newer exact Parent #74 head
`c6db0f8ab5b95be67a92ba925a1f4caa3d3d0a1d` demonstrates that the original
missing-Common-source condition no longer reproduces: Apache and NGINX
preparation completed and NGINX configured the module. The producer then
reached the distinct Framework case-schema failure tracked as
`FND-FRAMEWORK-0057`. Framework PR #51 is now merged as `de705a5` and Parent
PR #126 already adopts that Gitlink, so this Parent finding remains open only
until the updated complete producer and terminal gate rerun.

## Evidence and reproduction

Retained evidence:
`.codex/runs/20260726T135925Z-pr74-nginx-common-source-snapshot/evidence/parent-nginx-common-source-snapshot-root-cause.md`
(SHA-256 `f9b8c36c52f41e9fda2535ffa7522033f06b9e52bfe21e61a6d1e5c25ed5f52a`).
It records the exact diagnostic and source-to-sink classification without a
runner environment, credentials, payloads, or full hosted logs.

Reproduce by inspecting that exact bounded NGINX configure diagnostic; then
trace `prepare_nginx_runtime`, `runtime_env`,
`with-runtime-components.sh`, and Framework `prepare-nginx-build.sh`. Do not
disable the terminal gate, substitute a cache path, forward a caller value, or
modify Framework/MRTS to make the producer pass.

## Acceptance and validation

1. A ready NGINX snapshot contains the exact Parent-derived Common source
   root; an unready record contains no NGINX runtime values.
2. The direct Framework runtime-matrix boundary receives that value through
   the sourceable invocation-local snapshot.
3. Cache-contained refresh remains accepted, while an outside owner root is
   rejected before `make`.
4. Focused tests pass, then a new exact #74 hosted producer and its strict
   terminal gate pass without a fallback or weakened control.
5. Exact-head SonarQube Cloud, reviews, protection, and integration evidence
   remain required; no MRTS action is allowed or needed.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
tests.test_runtime_env_snapshot_contract
tests.test_full_matrix_cache_owner_root
tests.test_runtime_component_cache_contract` passed all 38 tests. The first
two cover snapshot publication and Framework-runner propagation; the third
retains the component-cache contract. They do not claim a native NGINX build
or hosted producer success.

## Dependencies, residual risk, and history

`FND-CROSS-0008` owns the separate cache deletion-owner containment defect;
this is a distinct Parent-only snapshot-source omission. The original hosted
failure no longer reproduces on exact head `c6db0f8`; Framework PR #51 is now
merged and Parent #126 already adopts its gitlink. The remaining acceptance
evidence is a fresh exact-head producer and terminal gate on the normally
updated #74 branch. No risk is accepted.

- 2026-07-26 — Bounded exact-head NGINX diagnostic and source review identify
  the Parent snapshot omission; focused repair and local controls begin.
- 2026-07-26 — Exact head `c6db0f8` completes Apache/NGINX preparation and
  configures the NGINX module, so the original condition no longer reproduces.
  The next failure is the independently tracked Framework schema blocker
  `FND-FRAMEWORK-0057`; this record cannot be verified closed before the full
  producer and strict terminal gate complete.
- 2026-07-26 — Framework PR #51 merged as `de705a5` and Parent PR #126
  adopted the Gitlink. The external dependency is resolved; Parent #74 now
  needs only its normal base update and fresh exact-head producer, strict gate,
  Sonar, review, protection, and integration evidence.
