# FND-CROSS-0008 — Cache-backed Apache and NGINX refreshes lose their owner-root contract in the Parent runtime matrix

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-CROSS-0008` |
| Category | `ci_failure` |
| Repository / ownership | `parent_and_framework` / `cross_repository` |
| Priority / severity / confidence | `P1` / `not_applicable` / `confirmed` |
| Status / feasibility | `fixed` / `feasible_now` |
| Release blocker / security relevance | yes / yes |

## Observation and impact

Exact Parent PR #74 hosted run `30197684223`, job `89782035387`, for head
`6809e348ad043bf3fcfd9b90d963882cc2fb2cb2` passed runtime-component
preparation and readiness. Its Apache proof built and loaded
`mod_security3.so`. The required runtime matrix then rejected both cache-backed
connector build directories during `REFRESH=1`: their owner root was the
job-local verified `build` directory, while their paths were below the managed
component cache.

The fail-closed decisions prevented the matrix from producing complete
connector summaries and the strict terminal evidence gate was skipped. PR #74
therefore cannot yet produce fresh legitimate runtime evidence or integrate.
No failed evidence was accepted.

## Cause and affected boundaries

Parent `ci/runtime/lifecycle/run-full-matrix-parallel.sh` forwards prepared
cache-backed `APACHE_BUILD_ROOT` and `NGINX_BUILD_DIR` into a matrix that gives
each job a distinct `BUILD_ROOT`. For Apache it explicitly uses that unrelated
`SHARED_BUILD_ROOT` as `APACHE_BUILD_OWNER_ROOT`. This Parent matrix hand-off
is incorrect.

At the Parent #74 observation, Framework
`ci/provisioning/prepare-nginx-build.sh` had no independent NGINX owner-root
input. Its `safe_remove_dir` always used `BUILD_ROOT` as the owner for
`safe_remove_runtime_path`. This was a Framework-owned missing parameter and
test contract. Framework PR #48 has now repaired that historical Framework
half; the incorrect Parent matrix hand-off remains. The combined cause is not
a duplicate of the prior Parent observability record `FND-PARENT-0054`.

The control itself is security-relevant: it prevents a refresh path from
deleting a directory outside its declared owner root. The correct repair must
preserve, not widen or bypass, that containment.

The controlled values are the prepared runtime snapshot's
`APACHE_BUILD_ROOT`/`NGINX_BUILD_DIR` and the matrix `REFRESH` decision. The
trusted inputs are the verified Parent component cache and Framework
`safe_remove_runtime_path` helper; the deletion guard is the sink. No
attacker-controlled path or runtime exploit is claimed. The security invariant
is that a refresh target must be an absolute safe generated path contained by
an explicitly validated connector-cache owner root; neither a job-local
`BUILD_ROOT` nor a cache root may silently authorize a sibling, symlink,
relative, or system path.

## Evidence and reproduction

Retained bounded evidence is
`.codex/runs/20260726T103539Z-pr74-cache-owner-root/evidence/hosted-cache-owner-root-blocker.md`
(SHA-256 `aeeb731c3c4b3eb5902b6624b5a5c7db41fb3367f01c2ca594735195181a3d9a`). It records the exact run/job, the two
fail-closed owner-root decisions, and the source-to-sink split without
credentials or a destructive reproduction.

Retained Framework integration evidence is
`.codex/runs/20260726T115300Z-framework-pr48-master-integration/evidence/framework-pr48-master-integration.md`
(SHA-256 `2460d2f15a027e79f08aee120ce487a6ff2714d882fa46b15786d2615d43c7c3`). It records the protected refresh, exact-head checks,
normal merge, result-tree equality, master workflows, and exact master
SonarQube Cloud analysis without credentials or payloads.

Reproduce by inspecting that exact hosted job and tracing the Parent matrix
invocations and Framework NGINX `safe_remove_dir`. Do not disable `REFRESH`,
expand `BUILD_ROOT`, delete cache content, or change the terminal gate merely
to obtain a green run.

## Required remediation and validation

Framework PR [#48](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/48)
is now merged. GitHub refreshed it to exact head
`19ec85c5359e83d3da59213e03bbeae9ac6c8ede` on base
`ab7374e08f12f80b1e6a7224418e4e04ca19ddc6`, then normally merged it with
exact-head protection as `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`. The
result tree equals the reviewed head tree `a6d405c6bc2ff8af689989fbee2d2505389f8f18`.
The cache-contained positive control and outside-owner, symlink, and relative
owner-root negatives passed; all refreshed-head checks and all resulting-master
workflows passed. PR and master SonarQube Cloud Quality Gates are `OK` with
zero open issues and `0.0` new duplicated-lines density.

Parent PR #74 head `093df42d8773c3d0a5c843225fe7c3575fa4e67f` now derives
`CONNECTOR_COMPONENT_CACHE/builds/connectors`, validates every Apache/NGINX
build root canonically below it, and passes it explicitly to both refresh
guards while keeping the per-job `BUILD_ROOT` isolated. The real matrix runner
has local same-boundary positive controls for both connectors at `REFRESH=1`
and an outside-owner rejection before `make`. The normal branch update carries
Parent PR #125's Framework Gitlink. Fresh exact-head hosted producer and strict
terminal-gate evidence remains required; MRTS remains unchanged because no
MRTS-owned remedy is evidenced.

## Residual risk and history

### Continuation — 2026-07-26

The bounded a0f NGINX configure log has now classified the remaining source-
build error. The separately remediable Parent-only omission is
`FND-PARENT-0056`: cache preparation passed `MSCONNECTOR_COMMON_SRC`, but the
ready invocation-local snapshot did not. Framework's normal `env` inheritance
does not clear that value. Parent now derives it only from
`CONNECTOR_ROOT/common/src`; no job override, fallback, guard relaxation,
Framework change, or MRTS action is used. The retained classification evidence
is `.codex/runs/20260726T135925Z-pr74-nginx-common-source-snapshot/evidence/parent-nginx-common-source-snapshot-root-cause.md`
(SHA-256 `f9b8c36c52f41e9fda2535ffa7522033f06b9e52bfe21e61a6d1e5c25ed5f52a`).
This finding still owns the independent owner-root containment issue and its
fresh exact-head producer requirement.

The Framework containment repair is verified without a guard relaxation and
the Parent hand-off is implemented at the published #74 exact head, but the
strict terminal gate remains unproven for that head. No suppression,
owner-root broadening, guard bypass, or risk acceptance occurred; MRTS source
and Gitlink remain unchanged. `FND-CROSS-0001`, `FND-PARENT-0053`,
`FND-PARENT-0054`, and `FND-SONAR-0016` are related.

- 2026-07-26 — Exact hosted #74 evidence established the Parent/Framework
  owner-root contract split and its fail-closed release blocker.
- 2026-07-26 — The current user explicitly authorized an isolated Framework
  branch, commit, push, and Draft PR (and an MRTS PR only if necessary). The
  Framework repair is therefore `feasible_now`; its merge and the later Parent
  Gitlink action remain intentionally deferred to user review/reporting.
- 2026-07-26 — Framework Draft PR #48 was opened at exact head
  `f98c4b58f4dbbf8e15064f4ae1139a470529bd9f`. It adds the defaulted and
  validated NGINX owner root only to the existing refresh-deletion guard and
  the same-boundary positive/negative controls. It is open, Draft, and has
  current-head checks pending; Codex did not merge it.
- 2026-07-26 — Exact-head SonarQube Cloud for Framework PR #48 passed with 0
  OPEN/CONFIRMED issues, `new_duplicated_lines=0`, and
  `new_duplicated_lines_density=0.0`. CodeQL, Secret scanning, OSV, OpenSSF,
  and common-structure are terminal successes; lint remains pending, so the PR
  is not yet `verified_pr`.
- 2026-07-26 — PR #48 was protectedly refreshed to `19ec85c…`, all exact-head
  checks passed after one successful retry of an external OSV-service outage,
  and the user-authorized normal merge created Framework master
  `a7ebf5a…`. The merge tree equals reviewed tree `a6d405c6…`; master lint,
  test-common, OpenSSF, CodeQL, SonarQube Cloud Quality Gate, and leak-period
  open-issue query all passed. The Framework half is verified, but the Parent
  #74 source hand-off and exact-head runtime evidence remain the release
  blocker. Parent PR #125's bot Gitlink advance is observed external state,
  not a substitute for that validation.
- 2026-07-26 — Parent #74 head
  `093df42d8773c3d0a5c843225fe7c3575fa4e67f` was normally merged with current
  `master` and pushed. It implements the narrow Parent owner-root hand-off and
  focused cache-contained/outside-owner regression controls. Shell syntax, 18
  focused runtime/path tests, runtime-path policy, CI-security contract,
  bilingual documentation, document links, Framework fixture syntax, and
  whitespace checks passed locally. Exact-head hosted closure remains pending.
- 2026-07-26 — Exact-head producer runs `30201764369`/`89792783415` and
  `30201763067`/`89792780237` both completed preparation/readiness but
  fail-closed in direct `runtime-matrix-all-runtime`: the local snapshot lacked
  `NGINX_BUILD_OWNER_ROOT`, so Framework correctly rejected the cache build
  against the job root. Parent's successor remediation publishes the narrow
  `CONNECTOR_COMPONENT_CACHE/builds/connectors` owner root for both connector
  builders and snapshot consumers. Three direct/full-matrix controls, 27
  cache-contract controls, runtime path policy, CI-security contract,
  bilingual documentation, fixture syntax, document links, and whitespace
  passed locally; fresh successor-head hosted evidence is required.
- 2026-07-26 — Exact hosted producers `30203025925`/`89796178895` and
  `30203024433`/`89796175146` for successor head
  `ece2d335c7106a38bf51feb3f9937ec3b9e09ef1` passed component preparation
  and readiness, then reached NGINX source-build `configure` rather than the
  historical owner-root rejection. The fixed configure log was absent from the
  bounded Parent failure summary, so its source-build cause is not inferred.
  Retained summary
  `.codex/runs/20260726T132600Z-pr74-nginx-configure-observability/evidence/hosted-nginx-configure-observability-gap.md`
  has SHA-256 `a89b41b87ea076a5a83e29e19fcfa490f8fba1ce327157cff649d884ab3bebbe`.
  Parent head `a0f337b8e45e5661b1ed09c7bf39b958548fbd14` adds only that fixed
  regular-file/non-symlink, command-masked log diagnostic and its 20-test
  workflow-security regression; full exact-head evidence remains required.
