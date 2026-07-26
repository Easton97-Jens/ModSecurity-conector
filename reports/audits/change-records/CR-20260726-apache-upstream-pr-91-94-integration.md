# Change Record: Selective Apache upstream PR #91–#94 integration

**Language:** English | [Deutsch](CR-20260726-apache-upstream-pr-91-94-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260726-apache-upstream-pr-91-94-integration` |
| Date (UTC) | `2026-07-26` |
| Base revision | `02642a466c94cbae58a9208868e75b6781074c58` |
| Boundary | Parent Apache source, Parent harness/tests/runtime/CI/provenance documentation only; Framework, MRTS, dependencies, Gitlinks, and submodule URLs remain unchanged. |
| Upstream base | ModSecurity-apache `0488c77f69669584324b70460614a382224b4883` remains the base origin. |
| Finding linkage | `FND-PARENT-0043` is retained for intervention ownership; `FND-PARENT-0055` records repaired adapter preflight defects; native prerequisites remain separately blocked by `FND-HOST-0002`. |

## Motivation and problem statement

The user selected a narrow integration from current [ModSecurity-apache PRs
#91–#94](https://github.com/owasp-modsecurity/ModSecurity-apache/pulls):
port #94A RulesSet APR-pool ownership, retain the existing safe #94B
intervention ownership, adapt #91/#92 request-body coverage without the
upstream production-handler or Docker stack, and create a Parent-native #93
Memcheck/Helgrind soak route. The supplied historical analysis commit and
decision matrix could not be recovered from local, remote, or GitHub evidence,
so the explicit current user selection remained the binding scope decision.

## Acceptance criteria

- `msc_config.c` registers every non-null fresh directory RulesSet for
  cleanup in its APR config pool, including merged configurations; no manual
  duplicate cleanup is added.
- #94B direct `free(intervention.url/log)` logic is not ported. Existing
  request-owned copies and one native cleanup remain the intervention model.
- The local Apache input-filter/EOS/drain/fail-closed path remains productive;
  no #91 `ap_get_client_block()` handler implementation is introduced.
- Parent-owned controls cover allow, deny, large/multi-bucket, split-trigger
  chunked, unread handler, empty body, keep-alive repeat, and deterministic
  lower-filter read-error behavior; no Docker/Compose stack is added.
- Parent-native manual Memcheck/Helgrind wiring has bounded roots, process and
  evidence controls, and cannot report a blocked or uninstrumented run as a
  pass.
- `SOURCE_MAP.json` attributes only the direct #94A source transplant to
  `src/msc_config.c`; Parent-owned test adaptations are not upstream imports.

## Implementation decision and rationale

The #94A adaptation adds a small `msc_rules_set_cleanup()` APR wrapper and
registers it only after `msc_create_rules_set()` returns non-null. Each
directory configuration, including a merge destination, owns its RulesSet
through the same APR-pool lifecycle. The native harness covers normal pools,
null creation, clear/destroy, successful merge, two RulesSet merge failures,
and a common-config merge failure. Its compile path explicitly undefines
`NDEBUG` so assertion-based controls cannot become vacuous.

The existing `process_intervention()` already copies retained log and redirect
values into `r->pool` before one native cleanup. #94B was therefore
deliberately not transplanted, avoiding duplicate or double-free ownership.

Request-body coverage stays in the Parent harness. A test-only lower input
filter returns `APR_EGENERAL` only on its dedicated read-error route and is
installed after the connector, exercising the existing fail-closed discard
path without changing productive filtering. The adapter registers its generated
external YAML through Framework's supported `EXTRA_CASE_ROOTS` interface and
selects its no-CRS baseline. The #92 Docker/Compose architecture is not
imported.

The #93 runner keeps Apache lifecycle ownership in the Parent harness. It adds
a verified Valgrind wrapper, hard timeout, bounded task-owned reports, a
payload-free upload bundle, and strict PASS evidence. A preflight repair uses
distinct POSIX-shell variables so a validated external soak root cannot
collapse to `/`.

## Changed files

- `connectors/apache/src/msc_config.c`
- `ci/checks/connectors/apache/apache_rules_set_cleanup.c`,
  `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`, and
  `tests/test_apache_rules_set_cleanup.py`
- `connectors/apache/harness/mod_phase4_terminal_rogue.c` and
  `connectors/apache/harness/run_apache_smoke.sh`
- `ci/runtime/lifecycle/run-apache-request-body-regression.sh` and
  `tests/test_apache_request_body_regression_wiring.py`
- `connectors/apache/harness/apache_soak_workload.py`,
  `ci/runtime/lifecycle/run-apache-soak.sh`,
  `tests/test_apache_soak_wiring.py`, and
  `.github/workflows/apache-soak.yml`
- `Makefile`, `connectors/apache/SOURCE_MAP.json`,
  `connectors/apache/ORIGIN.md`, and `connectors/apache/ORIGIN.de.md`
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Command or control | Result |
| --- | --- |
| `rtk make check-apache-ruleset-cleanup` | Static RulesSet contract passed (4 tests); native APR/APXS helper blocked because `apxs`/usable Apache headers are unavailable. GNU Make returned `2` after child exit `77`. |
| `rtk make check-apache-ruleset-cleanup-lint` | Passed: the 4 static RulesSet tests pass and the configured native preflight is truthfully recorded as allowed `blocked` for missing Apache development prerequisites. |
| `rtk make check-apache-intervention-cleanup` | Passed: 5 existing ownership-contract tests. |
| `rtk make check-apache-c-standard-wiring` | Passed. |
| `rtk make check-apache-request-body-regression-wiring` | Passed: 8 tests plus shell syntax. |
| `rtk make check-apache-request-transaction-cleanup` | Static transaction-cleanup suite passed (5 tests); the native helper is blocked by missing `apxs`/usable Apache headers. GNU Make returned `2` after child exit `77`. |
| `rtk make apache-request-body-small-allow APACHE_REQUEST_BODY_ROOT=…/request-body-retry` | Resolved the generated external case, then blocked at the absent configured Apache `httpd`; GNU Make returned `2` after child exit `77`. |
| `rtk make check-apache-soak-wiring` | Passed: 12 tests plus shell syntax. |
| `rtk make apache-soak-memcheck APACHE_SOAK_ROOT=…/soak-retry` | Created a bounded report/upload bundle, then blocked because Valgrind is unavailable; GNU Make returned `2` after child exit `77`. |
| `rtk make apache-soak-helgrind APACHE_SOAK_ROOT=…/soak-retry` | Created a bounded report/upload bundle, then blocked because Valgrind is unavailable; GNU Make returned `2` after child exit `77`. |
| `rtk make check-bilingual-docs` and `rtk make check-doc-links` | Blocked solely by the isolated worktree's intentionally absent Framework submodule targets; neither command reported a Change-Record-specific defect. The focused bilingual checker unit suite passed (11 tests). |
| Canonical Codex Security diff-scan finalization | Passed: sealed complete working-tree coverage for all 14 executable/structured-provenance files and 0 reportable findings. The sole command-path candidate was dynamically rejected before the execution sink. |

## Security impact

RulesSet destruction is now tied to the owning APR config pool, reducing a
native lifetime leak/cleanup risk without adding a second owner. Intervention
ownership remains safe because Apache retains request-pool copies before the
existing single native cleanup. The test-only read-error filter is route-scoped
and verifies a fail-closed `400`; it does not alter the production handler
model. External case and soak roots are constrained, and the manual workflow
remains least-privilege, dispatch-only, and uploads only bounded report
material. A sealed focused security-diff review covers the executable and
structured-provenance changes completely and reports no vulnerability. Its one
command-path hypothesis was safely falsified: traversal segments are rejected
before the harness-execution sink.

## Runtime evidence

Native Apache request-body, APR lifecycle, Memcheck, and Helgrind evidence is
not available in this environment. The strongest executed preflight evidence
shows that the request-body adapter resolves its external fixture and then
fails closed at the missing Apache executable; both soak modes create bounded
task-local evidence and then fail closed at absent Valgrind. These outcomes are
blockers, not passing runtime or sanitizer results.

## Known limitations

The historical analysis commit/matrix named in the request was unavailable,
although current upstream PR heads and stack relationships were revalidated.
The large-body control exercises a payload larger than 1 MiB but does not
measure a native APR bucket count. No native graceful-reload cycle, HTTP/2, or
HTTP/3 assertion is claimed. The RulesSet harness uses controlled stubs and
cannot prove libmodsecurity production allocation behavior.

## Remaining risks

The current host cannot prove the Apache/APR/libmodsecurity ABI path, actual
request-body response semantics, or Valgrind leak/race results. Existing
`FND-PARENT-0043` remains blocked pending native intervention validation. No
safety control, test, scanner, workflow permission, or branch protection was
weakened, and no risk acceptance is recorded.

## Checks not run and rationale

- Native RulesSet/APR C17 execution is blocked by missing Apache development
  prerequisites (`apxs`/headers).
- Full request-body mode execution and ordinary Apache smoke are blocked by the
  absent prepared Apache executable and connector runtime.
- Actual Memcheck and Helgrind are blocked by unavailable Valgrind; no
  substitute report is instrumentation evidence.
- Full `lint`, full `smoke-all`, HTTP/2, and HTTP/3 matrices are not
  substitutes for the scoped controls and retain their Framework/native
  prerequisites.

## Final diff and review status

The scoped security-diff review is finalized with complete coverage and zero
reportable findings. Repository-wide bilingual and link checks were executed
but are blocked only because the isolated worktree deliberately has no
Framework submodule contents; the focused Change-Record parity suite passed.
Only this reader-facing record changed after the executable scan snapshot.

Delivery update (observed before this self-updating documentation follow-up):

- Branch: `codex/apache-upstream-pr-91-94-integration`.
- Implementation commits: `3193b0ab44163f3c291f184f8d077adef602f943`,
  `73241f2634c4c52ee1c593a5f84b122d226d60ed`, and
  `325581ea12586f894431ccd33cc0d3cbdfb0701d`.
- Draft PR: [#124](https://github.com/Easton97-Jens/ModSecurity-conector/pull/124)
  against `master`.
- At PR creation, local head, `origin/codex/apache-upstream-pr-91-94-integration`,
  and the PR head were all
  `325581ea12586f894431ccd33cc0d3cbdfb0701d`.

This follow-up record deliberately does not self-reference its future commit
SHA; the final local/remote/PR-head equality is retained in the PR and task
delivery evidence. The PR remains Draft while native Apache/APR and Valgrind
runtime prerequisites are unavailable, and its CI/review results are pending.
No merge, direct default-branch push, Framework/MRTS delivery, Gitlink update,
or risk acceptance is authorized by this record.
