# FND-PARENT-0064 — Apache RulesSet allocation lacks an APR config-pool cleanup binding

- Category: `lifecycle_defect`
- Repository / ownership: `parent` / `parent`
- Priority / severity / confidence: `P1` / `not_applicable` / `validated`
- Status / feasibility: `verified` / `feasible_now`
- Release blocker / security relevance: `false` / `true`
- Security assessment: `validated_lifecycle_ownership_defect_no_attacker_controlled_boundary_established`
- Connector / protocol / profile: `apache` / `Apache configuration-pool lifecycle and graceful restart` / `resulting master 154ee724eba4653fa6378fc3c8729ae433e65697, tree-identical to final PR #183 head 4e4dfb36e1b05f7eda38450fd3710e3a04905118`

## Summary

**Current resulting-master disposition — 2026-07-29T11:27:25Z.** PR #183
merged as Parent master `154ee724eba4653fa6378fc3c8729ae433e65697`; its tree
`c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0` equals final head
`4e4dfb36e1b05f7eda38450fd3710e3a04905118`. All 14 master-SHA GitHub Actions
workflows succeeded. A detached exact-master worktree passed
`make check-apache-ruleset-cleanup` (five Python contracts plus the native GCC
APR harness), so the original APR failure/control boundary is `verified`.
Historical candidate-only wording below is retained as chronology and is
superseded by this disposition. It is not `closed`: the broader live Apache
configuration/readiness/phase-2/`SIGUSR1` sequence was not rerun on resulting
master.

Parent master creates a per-directory `RulesSet` without binding that allocation
to APR configuration-pool destruction.  The retained baseline APR harness
aborts with exit `134` at
`ci/checks/connectors/apache/apache_rules_set_cleanup.c:205`, because it
observes no cleanup where it expects `native_cleanup_calls == 1`.  The
uncommitted task candidate registers a cleanup only after successful RulesSet
creation, and its GCC harness passes.

The task-owned private Apache build also loads the configuration, serves the
HTTP/1.1 readiness control, returns the expected phase-2 `403` denial,
completes a `SIGUSR1` graceful restart, and terminates cleanly.  The candidate
is not committed, reviewed, hosted-validated, or merged; therefore this is
`in_progress`, not `fixed`, `verified`, or `closed`.

## Observed and expected behavior

At Parent master `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`,
`msc_hook_create_config_directory` in
`connectors/apache/src/msc_config.c` creates `cnf->rules_set` with
`msc_create_rules_set()` at line `402` but registers no RulesSet-specific
`apr_pool_cleanup_register` callback.  The baseline APR harness compiled
against that source exits `134` at line `205` while asserting
`native_cleanup_calls == 1`.

The candidate adds `msc_rules_set_cleanup()` and registers it immediately
after the successful non-null RulesSet guard.  Its GCC harness passes the
exact-once ownership, null-RulesSet, pool-clear, successful-merge, and
merge-failure paths.

A RulesSet created for one Apache configuration generation must be released
exactly once when that generation's APR configuration pool is destroyed, while
configured rules remain usable for the normal lifetime of that generation.

## Impact and boundary assessment

Without the pool binding, retired configuration generations can retain
RulesSets across graceful restarts and contribute to process-memory growth or
availability degradation.  The source/lifecycle defect is validated by the
baseline/candidate APR harness pair and the private Apache lifecycle controls.

The relevant source is trusted Apache operator configuration and process
lifecycle.  No attacker-controlled source, supported attacker-facing boundary,
externally exploitable memory-safety condition, or release blocker has been
established.  This is nevertheless security-relevant lifecycle/ownership work
and needs a focused ownership review before integration.

## Affected scope, preconditions, and reproduction

- File: `connectors/apache/src/msc_config.c`.
- Symbols: `msc_hook_create_config_directory`, `msc_create_rules_set`,
  `msc_rules_cleanup`, and `apr_pool_cleanup_register`.
- Preconditions: Parent Apache connector is loaded; a non-null RulesSet is
  created for a per-directory configuration; Apache eventually clears or
  destroys the configuration pool, including on graceful restart.
- Reproduce the baseline with the retained APR cleanup harness.  It exits
  `134` at `apache_rules_set_cleanup.c:205` because the master source leaves
  `native_cleanup_calls` at zero.
- Run the candidate harness and private Apache control in the same retained
  task root.  Candidate ownership controls pass; the runtime control proves
  configuration load, HTTP/1.1 readiness, phase-2 denial, graceful restart,
  and clean shutdown.

## Evidence

| Type | Artifact | SHA-256 | Exit | Result |
| --- | --- | --- | ---: | --- |
| Static comparison | `.codex/runs/merge-pr171-apache-pr91-94-comparison-20260729/evidence/fnd-parent-0064-static-triage.md` | `acd1923243fb4b46894959c5b9b08cf99f9d7478aa524e07fe008ecdf0357b59` | 0 | Parent allocation and upstream #94A cleanup direction match statically. |
| Baseline APR harness | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/baseline-apr/apache-rules-set-cleanup` | `030144bc518ad0ab9549858fbcc3cb8fdecb380b46d95822a4cea183f233c2df` | 134 | Fails at `apache_rules_set_cleanup.c:205`: `native_cleanup_calls == 1`. |
| Candidate GCC APR harness | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/ruleset-gcc/apache-rules-set-cleanup` | `6b1dfd3ab32b36cf2efa74c08fde14237b87bcc6949a2efe8a5e2998d0ff7415` | 0 | Exactly-once, null, pool-clear, merge, and failure-path controls pass. |
| Private Apache HTTP/1.1 control | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/apache-runtime/result.json` | `4b56897c87aa87b4b10d6a56bcc36b7fa60e91cd938a76cd1eb22d5ad7d83bf5` | 0 | Readiness is HTTP `200`; configured phase-2 deny is HTTP `403`. |
| Restart/shutdown log | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/apache-runtime/error.log` | `d65d607196ecc06f09179a5db5cc11ffb5fa332185d0f4d5125a3f47923165b4` | 0 | `AH00493` SIGUSR1 restart, later `AH00489` normal operation, PID removal, and `AH00491` clean SIGTERM shutdown. |
| Memcheck diagnostic | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/graceful-memcheck/memcheck.8.log` | `a49ca3a72f06aef4f4e67bab0b57056fe785c95a1dfba2361a892fbbf497b931` | 99 | No Invalid free/read/write or UAF diagnostic; exit `99` is the separate `strdup` leak tracked by `FND-PARENT-0067`. |
| Resulting-master verification | Parent-supplied PR #183 resulting-master delivery and focused-cleanup summary | n/a | 0 | Master `154ee724eba4653fa6378fc3c8729ae433e65697` is tree-identical to final head `4e4dfb36e1b05f7eda38450fd3710e3a04905118`; all 14 workflows and the focused APR regression pass. No broad live Apache rerun is claimed. |

The upstream sources remain [PR #94](https://github.com/owasp-modsecurity/ModSecurity-apache/pull/94),
[commit `5ea3fc9`](https://github.com/owasp-modsecurity/ModSecurity-apache/commit/5ea3fc9da876195706375cf35f321de2a1f35ce1),
and [issue #82](https://github.com/owasp-modsecurity/ModSecurity-apache/issues/82).

## Root cause and remediation direction

The adapter-owned Parent source still reflects a baseline before upstream
commit `5ea3fc9da876195706375cf35f321de2a1f35ce1`.  It creates a RulesSet but
does not bind cleanup to the APR configuration pool.  The current candidate
adds only a callback that invokes `msc_rules_cleanup()` and its registration
after the successful non-null allocation guard.

Commit and review only that focused correction and its regression harness.
Then rerun the APR harness, focused C checks, private Apache configuration /
request / restart controls, a security-diff review, and exact-head hosted
checks.  Do not merge stale Parent PR #123 or #124 wholesale.  Do not fold the
separate `name_for_debug` leak into this correction without a distinct,
lifecycle-safe ownership decision; it is `FND-PARENT-0067`.

## Acceptance criteria and validation plan

1. Cleanup is registered only after successful non-null `msc_create_rules_set()`
   and calls `msc_rules_cleanup()` exactly once per retired configuration
   generation.
2. The focused APR ownership regression passes on the committed candidate.
3. Private Apache configuration load, HTTP/1.1 readiness, phase-2 denial,
   graceful restart, and clean shutdown pass on the committed candidate.
4. Focused security review finds no double-free, premature cleanup, stale-pool,
   or error-path ownership regression.
5. Fresh exact-head hosted CI, review, and SonarQube Cloud evidence exists
   before a `fixed`, `verified`, or `closed` disposition.

## Dependencies, related findings, and residual risk

Current residual risk: a controlled resulting-master Apache/APXS, APR,
libmodsecurity, and Valgrind environment must rerun the broader live Apache
configuration/readiness/phase-2/`SIGUSR1` sequence before `closed` status.
The historical candidate-only residual-risk wording below is superseded.

- Dependencies: task-owned candidate worktree; local Apache/APXS, APR,
  libmodsecurity, GCC, and Valgrind prerequisites; fresh hosted exact-head
  evidence after commit/publish.
- Related findings: `FND-PARENT-0055` and the independent
  `FND-PARENT-0067` `name_for_debug` leak.
- Parent PR #123 and #124 are stale conflicting source inputs, not merge
  targets.  Upstream Apache PR #94 supplies the selectively revalidated
  cleanup direction.
- Residual risk: Parent master still lacks the cleanup binding.  The candidate
  is local-only and unmerged; no fixed/verified/master claim is made.

## History

- `2026-07-29T07:53:18Z`: static upstream/Parent comparison triaged.
- `2026-07-29T09:04:55Z`: baseline APR failure, candidate GCC success, and
  private Apache lifecycle evidence recorded; the independent `strdup` leak
  received `FND-PARENT-0067`.
- `2026-07-29T11:27:25Z`: resulting master
  `154ee724eba4653fa6378fc3c8729ae433e65697` was confirmed tree-identical to
  final head `4e4dfb36e1b05f7eda38450fd3710e3a04905118`; all 14 workflows and
  the focused APR regression passed. The finding is `verified`, not `closed`.
