# Selective Apache upstream PR #91-#94 integration

**Language:** English | [Deutsch](CR-20260726-apache-upstream-pr-91-94-integration.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260726-apache-upstream-pr-91-94-integration` |
| Date (UTC) | `2026-07-26` |
| Base revision | `02642a466c94cbae58a9208868e75b6781074c58` |
| Boundary | Parent Apache source, tests, runtime harness and provenance only; Framework/MRTS unchanged. |

## Motivation and problem statement

Open upstream PRs #91-#94 contain one needed lifetime fix plus approaches that conflict with Parent ownership and runtime architecture. The supplied assessment commit `116193c8007173534707a908d48388738a2aa5f8` was unavailable from the fetched repository/API; its stated decisions were retained and current heads were independently verified.

## Acceptance criteria

Bind every connector-created RulesSet exactly once to its owning APR config pool; retain intervention and EOS behavior; adapt body regressions and a bounded Parent-native soak; preserve Framework/MRTS and security controls.

## Implementation decision and rationale

Parent base and branch are `02642a466c94cbae58a9208868e75b6781074c58` and `codex/apache-upstream-pr-91-94-integration`. Verified heads are #91 `230e14d755bc5912d96e13947aa4b8ef73dbb4fa`, #92 `7d408a10d359601d5771f0446a81284be17fbf29`, #93 `8221baee1f349e3954043dc0d8102b119b9a04bf`, and #94 `1e07559819163e4c23338d646859422b0efd5c0e`; #94 stacks on #91 and #93 on #92. #94A was semantically ported. #91 production handler consumption, #92 Docker/Compose, #93 Docker/workflow, and #94B direct frees were not ported. The `mp` owner pool now registers one null-safe cleanup after successful creation; merge creates an independently owned object.

## Changed files

`connectors/apache/src/msc_config.c`; Parent request-body and Valgrind harnesses; focused tests and Make targets; Apache origin/source maps; Change Record pair and indexes. Framework and MRTS are unchanged.

## Commands executed

`make check-apache-ruleset-cleanup`, `make check-apache-request-body-regressions`, `make check-apache-valgrind-soak`, `make check-apache-intervention-cleanup`, request-transaction unittest, C-standard wiring, bilingual checks, doc links, JSON validation, Python compilation, and Git diff checks.

## Security impact

The RulesSet leak across configuration-pool destruction is closed without shared-pointer cleanup or manual competing destruction. Existing request-pool intervention copies and the single `msc_intervention_cleanup()` remain unchanged, avoiding double-free. EOS, drain, append-after-EOS guard, fail-closed behavior and central status handling remain unchanged.

## Runtime evidence

Focused source contracts passed. Native C17 was BLOCKED by the absent Framework content. Live body, smoke, Memcheck and Helgrind were BLOCKED by missing rendered native runtime and Valgrind; they are not PASS. The soak emits external JSON/Markdown/log evidence and reports definite, indirect, possible, reachable, invalid-access, use-after-free and double-free categories separately.

## Known limitations

Static contracts cannot demonstrate allocator behavior, real multi-bucket scheduling or graceful-restart concurrency. Native evidence is required before merge.

## Remaining risks

No broad Helgrind suppressions exist. Library-origin reports must be triaged. `still reachable` is not described as leak-free. The unavailable analysis object is recorded rather than silently substituted.

## Checks not run and rationale

`make check-apache-c17`, `make smoke-apache`, `make smoke-all`, live `apache-request-body-regressions`, `apache-soak-memcheck`, and `apache-soak-helgrind` were not executable because Framework/runtime/Valgrind prerequisites were absent. Documentation aggregate failures after task-local corrections are limited to pre-existing missing Framework link targets.

## Final diff and review status

Focused diff review found one RulesSet creation, one registration, one adapter cleanup call, no shared RulesSet, no manual cleanup race, no intervention change, no second body consumer, no workflow/security-control or Gitlink change. Native blockers require a Draft PR.
