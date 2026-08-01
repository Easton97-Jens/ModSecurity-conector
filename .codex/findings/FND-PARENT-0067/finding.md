# FND-PARENT-0067 — Apache name_for_debug uses an unowned strdup allocation across configuration lifecycle

- Category: `lifecycle_defect`
- Repository / ownership: `parent` / `parent`
- Priority / severity / confidence: `P2` / `not_applicable` / `validated`
- Status / feasibility: `validated` / `feasible_now`
- Release blocker / security relevance: `false` / `false`
- Security assessment: `not_applicable_trusted_apache_configuration_lifecycle_no_attacker_boundary`
- Connector / protocol / profile: `apache` / `Apache configuration-pool lifecycle and graceful restart` / `Private Apache graceful-restart Memcheck control`

## Summary

A private Apache graceful-restart Memcheck run validates a separate Parent
lifecycle leak. Parent master assigns `strdup(path)` to `name_for_debug` in
`msc_hook_create_config_directory` at
`connectors/apache/src/msc_config.c:416`. The retained log reports `66` bytes
definitely lost in `3` blocks, with both allocation stacks passing through
`strdup` and connector DSO address `0x53D1BEB`.

The log contains no Invalid free/read/write or use-after-free diagnostic. The
Memcheck command exits `99` because it deliberately treats definite leaks as
errors. This is a P2 trusted-configuration lifecycle defect, not a security
finding or release blocker. It is independent of `FND-PARENT-0064` RulesSet
cleanup, and no source repair is included in the current task.

## Observed and expected behavior

At Parent master `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`, the non-null
`path` branch uses:

```c
cnf->name_for_debug = strdup(path);
```

The task-owned private Apache graceful-restart run reports two definite-leak
contexts: `22` bytes in one block and `44` bytes in two blocks. Both stacks
include `strdup`, connector DSO address `0x53D1BEB`, and Apache configuration
traversal. The diagnostic totals `66` bytes in `3` blocks.

Debug-name storage associated with a configuration generation must have an
explicit owner and be released when that generation is destroyed, while any
legitimate debug-name reads remain valid for that generation's normal lifetime.

## Impact and boundary assessment

The observed private run leaks `66` bytes in `3` blocks. Repeated configuration
creation and graceful restarts can accumulate this trusted-lifecycle allocation.
The result does not establish attacker control, external exploitability,
corruption, invalid free, UAF, a release blocker, or a security impact.

## Affected scope, preconditions, and reproduction

- File: `connectors/apache/src/msc_config.c`.
- Symbols: `msc_hook_create_config_directory`, `msc_conf_t.name_for_debug`,
  and `strdup`.
- Preconditions: Parent Apache connector is loaded privately; Apache creates
  per-directory configurations with non-null paths; the process runs a
  `SIGUSR1` graceful restart and termination under Memcheck.
- Inspect current master lines `414`–`417`, then run the retained private
  Memcheck control with `--leak-check=full`,
  `--show-leak-kinds=definite`, `--errors-for-leak-kinds=definite`, and
  `--error-exitcode=99`.
- `memcheck.8.log` reports `22` plus `44` bytes definitely lost and no invalid
  memory-access diagnostic.

## Evidence

| Type | Artifact | SHA-256 | Exit | Result |
| --- | --- | --- | ---: | --- |
| Private graceful Memcheck | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/graceful-memcheck/memcheck.8.log` | `a49ca3a72f06aef4f4e67bab0b57056fe785c95a1dfba2361a892fbbf497b931` | 99 | `66` bytes definitely lost in `3` blocks through `strdup` and `0x53D1BEB`; no Invalid free/read/write or UAF. |
| Private restart log | `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/validation/apache-runtime/logs/apache-runtime/error.log` | `d65d607196ecc06f09179a5db5cc11ffb5fa332185d0f4d5125a3f47923165b4` | 0 | `AH00493` SIGUSR1 restart, `AH00489` resumed operation, and `AH00491` clean termination. |

## Root cause and remediation direction

The configuration factory allocates `name_for_debug` through libc `strdup`
rather than storage owned by the APR configuration pool, and current source
has no dedicated cleanup owner. The Memcheck allocation stacks correlate this
path with Apache configuration traversal.

Choose a separate lifecycle-safe ownership contract before source modification:
determine whether the debug name should be APR-pool-owned or receive a narrow
cleanup; verify creation, merge, error, shutdown, and every later debug-use
path; then add a focused regression and rerun the same private Memcheck
control. The current task deliberately includes no source repair for this
finding.

## Acceptance criteria and validation plan

1. A separately reviewed ownership design establishes one valid cleanup owner
   without shortening a legitimate debug-name lifetime.
2. Focused tests cover non-null creation, merge/error paths, pool destruction,
   and legitimate debug-name access where applicable.
3. The private Apache graceful-restart Memcheck reproduction no longer reports
   the `strdup`-backed `66`-byte definite leak.
4. The resulting change receives focused lifecycle/security review and
   exact-head validation before `fixed` or `verified`.

## Dependencies, related findings, and residual risk

- Follow-up needs a task-owned Parent worktree and private Apache/APXS/APR/
  libmodsecurity/Valgrind environment.
- Related finding: `FND-PARENT-0064`. It owns RulesSet heap cleanup; this
  finding owns `name_for_debug` string storage. The two fixes must remain
  independently safe and independently tested.
- Residual risk: this P2 leak remains on Parent master and in the current
  RulesSet-cleanup candidate. It is not a security or release-blocker claim,
  and no source repair, PR, merge, or master disposition is claimed here.

## History

- `2026-07-29T09:04:55Z`: private graceful-restart Memcheck evidence validated
  the distinct `strdup(path)` lifecycle leak and allocated this canonical ID.
