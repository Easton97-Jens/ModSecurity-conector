# Change Record: Preserve optional Apache prerequisite status in CI

**Language:** English | [Deutsch](CR-20260714-optional-apache-prerequisite-ci.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Preserve optional Apache prerequisite status in CI |
| Change ID | CR-20260714-optional-apache-prerequisite-ci |
| Date (UTC) | 2026-07-14T15:36:31Z |
| Author or executing agent | Codex |
| Base revision | `be0356af96ef582c3a7dbc0169c7c8b27b7b6b34` |
| Related issue or pull request | None; the separate documentation-only PR #42 is intentionally not modified. |
| Final revision | Pending commit, push, and exact-SHA CI verification. |

## Motivation and problem statement

Five pre-existing Push workflows failed when their shared `make lint` path
encountered a missing `apxs` or usable Apache development headers. The direct
Apache cleanup harness deliberately reported `BLOCKED` with exit `77`, but
`check-apache-request-transaction-cleanup-lint` first invoked it through a
recursive GNU Make target. GNU Make reported its failed recipe as exit `2`, so
the wrapper that only recognized `77` never ran.

The failure predates the documentation-only commit
`2a3788dc20f93bb14f0c2fc784444402c3e3f64b` and PR #42. The same five failures
occurred on the base revision: [lint](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329968), [test-common](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329953), [test-apache](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329928), [test-nginx](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329926), and [quick-framework-check](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29332329950). The corresponding five runs for the delivery-smoke commit also failed: [lint](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695839), [test-common](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695813), [test-apache](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695806), [test-nginx](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695931), and [quick-framework-check](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29342695753).

## Affected components and security boundaries

- Parent-only CI orchestration: the root `Makefile`, the Apache cleanup lint
  target, a small Parent `ci/tools/` status runner, and root contract tests.
- Reader-facing Parent CI, testing/evidence, variable-reference, and Change
  Record documentation are updated in English and German.
- The Framework remains unchanged and its Gitlink is not modified. Its
  `skip_blocked` contract correctly emits `BLOCKED` and exit `77`; the loss was
  exclusively in the Parent recursive Make boundary.
- The JSON record is payload-free CI-control evidence below an external
  `BUILD_ROOT`, not canonical runtime evidence. It stores no request data,
  credentials, or build outputs.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| A direct optional Apache prerequisite block remains visible and does not falsely fail generic lint. | met locally | `make check-apache-request-transaction-cleanup-lint` records `blocked` with direct exit `77` and `CHECK_STATUS_REASON apache_development_prerequisite`, then returns `0` only under that exact contract. |
| Python source checks and genuine native-check failures remain red. | met locally | The strict target stays nonzero without `apxs`; synthetic `apxs`-present failures, unknown exits, and an unclassified Framework block are regression-tested. |
| A missing mandatory prerequisite does not become success. | met locally | Synthetic strict Make fixture keeps `blocked` evidence and a nonzero result. |
| Recursive Make cannot silently erase the classification. | met locally | Synthetic nested Make fixture retains JSON `blocked` evidence while the explicitly allowed wrapper alone returns `0`. |
| Other Common or connector checks are not skipped. | met locally | Separate synthetic `common` and `connector` recipes remain nonzero after an allowed optional block. |
| The status model and public Make contract are documented in both languages. | met locally | `ci/README.*`, `docs/testing-and-evidence.*`, and `docs/reference/variables.*`. |
| Required exact-SHA Push and Pull Request workflow outcomes are recorded. | pending delivery | Performed after the task branch is pushed. |

## Scope and workflow decision

The investigation resolved the requested questions before implementation:

| Question | Decision and repository evidence |
| --- | --- |
| Is `apxs` optional for every affected workflow? | Yes, only for the embedded native Apache/APR cleanup harness. Each affected step is a generic lint, structure, or dry-run path; none is an Apache native build job. |
| Which jobs may skip on missing `apxs`? | No whole job is skipped. Only the direct native cleanup harness may be recorded as `blocked` and allowed by `check-apache-request-transaction-cleanup-lint` when no usable `apxs` with `httpd.h` is found. |
| Which jobs must fail on missing `apxs`? | The strict `make check-apache-request-transaction-cleanup` target and actual Apache native build/verification paths remain nonzero. The mandatory Python source contract remains nonzero on failure in every path. |
| Is the blocked state public Make behavior? | Yes. The direct scripts and CI documentation use `BLOCKED`/exit `77` for a declared unavailable optional prerequisite; the strict and lint targets now document their distinct contracts. |
| Is exit `77` reliable outside recursive Make? | Yes. The direct shell harness emits `77`, and adjacent direct lint wrappers already classify it. Recursive GNU Make converts the failed child recipe to its own `2`. |
| Was a machine-readable status format already available for this check? | No dedicated record existed. The repository had human-readable `BLOCKED` output and broader evidence formats, so this change adds a focused payload-free JSON status record plus `CHECK_STATUS` JSON output. |

| Workflow | Job and Push step | Make-target chain | Apache prerequisite disposition |
| --- | --- | --- | --- |
| `lint` | `scaffold-lint` / `Run lightweight lint` | `make lint` → `check-apache-request-transaction-cleanup-lint` | Only an absent usable `apxs`/`httpd.h` preflight is optional; Python source contract mandatory. |
| `test-common` | `common-structure` / `Lightweight framework checks` | `make quick-check` → `lint` → cleanup lint target | Only that Apache preflight is optional; Common checks remain mandatory. |
| `test-apache` | `apache-structure` / `Syntax and dry-run checks` | `make quick-check` → `lint` → cleanup lint target | This is not a native build; only that preflight is optional and source contract mandatory. |
| `test-nginx` | `nginx-structure` / `Syntax and dry-run checks` | `make quick-check` → `lint` → cleanup lint target | Only that Apache preflight is optional; NGINX checks remain mandatory. |
| `quick-framework-check` | `quick-check` / `Lightweight connector/framework checks` | `make quick-check` → `lint` → cleanup lint target | Only that Apache preflight is optional; all other quick checks remain mandatory. |

The direct harness emits its missing-prerequisite status through
`ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh` and
the Framework's `skip_blocked`. The old Parent lint target then crossed the
recursive Make boundary before trying to inspect it, which produced the false
exit `2` in each chain above.

## Alternatives investigated

- Preserving the old recursive wrapper was rejected because GNU Make does not
  retain the child process's `77` as the recursive Make process's exit code.
- A broad workflow `continue-on-error`, `|| true`, or job-level skip was
  rejected because it could hide real source, configuration, Common, or
  connector failures.
- Installing Apache development packages was rejected because it would mask a
  CI classification defect and change the environment rather than the
  documented contract.
- A Framework change was rejected because its `skip_blocked` implementation
  is correct and the validated fault is Parent-only.

## Implementation decision and rationale

`ci/tools/run-check-status.py` executes the native harness directly, maps
direct exit `0` to `passed`, direct `77` to `blocked`, and every other exit to
`failed`, then writes a JSON record before returning to Make. It also defines
explicit `not_applicable` and `not_executed` dispositions. A blocked command
returns success only when its direct output has exactly the caller-approved
`CHECK_STATUS_REASON` marker; `not_applicable` likewise needs an explicit
caller allow option, and `not_executed` never succeeds implicitly.

The runner accepts no caller-selected status-file path. It derives the fixed
`apache-request-transaction-cleanup.json`-style filename from the validated
check identifier under the external `BUILD_ROOT/check-status` directory. It
rejects a missing, relative, noncanonical, checkout-local, or symlinked output
location, opens the validated directory before the child runs, and uses that
anchored directory handle for an exclusively created temporary file and final
replacement.

`ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
now obtains `apxs` through `framework_find_apxs`, which verifies a usable
`httpd.h`, and emits `CHECK_STATUS_REASON apache_development_prerequisite`
only when that discovery fails. The lint target continues to execute the
mandatory Python source-contract tests, then invokes the direct status runner
with `--allow-blocked-reason apache_development_prerequisite`. Missing
Framework, compiler, APR, or libmodsecurity prerequisites emit no approved
marker and remain nonzero. The strict target is not changed. The status file
is fixed at `$(BUILD_ROOT)/check-status/apache-request-transaction-cleanup.json`
for this check and must remain outside the checkout. `CHECK_STATUS` emits the
same JSON into local and GitHub Actions logs, allowing a reviewer to distinguish
`blocked` from `passed` even when the aggregation target exits successfully.

The documented status values are `passed`, `failed`, `blocked`,
`not_applicable`, and `not_executed`. A successful generic workflow may carry
only a specifically allowed `blocked` or `not_applicable` subcheck; it does not
relabel that subcheck as passed.

## Changed files

- `Makefile`
- `ci/tools/run-check-status.py`
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`
- `tests/test_optional_prerequisite_status.py`
- `ci/README.md` and `ci/README.de.md`
- `docs/testing-and-evidence.md` and `docs/testing-and-evidence.de.md`
- `docs/reference/variables.md` and `docs/reference/variables.de.md`
- This Change Record pair and its bilingual index entries

No Framework file, Framework commit, submodule Gitlink, workflow trigger, or
PR #42 file is changed.

## Tests added or changed

`tests/test_optional_prerequisite_status.py` uses synthetic `PATH` fixtures
and temporary direct commands to cover:

1. `apxs` present and the dependent check passing;
2. `apxs` present and the dependent check failing;
3. missing optional `apxs` classified as allowed `blocked`;
4. missing mandatory `apxs` remaining nonzero through Make;
5. a recursive Make call retaining persisted `blocked` classification;
6. an unknown exit code remaining `failed`;
7. an unapproved `framework_unavailable` marker remaining nonzero;
8. subsequent Common and connector checks each remaining nonzero; and
9. explicit `not_applicable` and `not_executed` disposition behavior; and
10. rejection of missing, checkout-local, noncanonical, legacy arbitrary-path,
    and symlinked status-output requests while preserving an untouched target;
    and
11. a child-driven `BUILD_ROOT` replacement after preparation, which must not
    redirect the already anchored status output.

It also invokes the real lint target with an executable synthetic `apxs` whose
include directory lacks `httpd.h`, confirming that the direct preflight emits
the sole approved marker and persists its allowed `blocked` result. A separate
real-target case with a missing Framework root remains nonzero with an
unclassified `blocked` record.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| `make check-apache-request-transaction-cleanup-lint` on the base code before the fix | `2` | Five Python source tests passed; native harness returned `77`; recursive Make reported `2`. | None | None |
| `make check-optional-prerequisite-status` | `0` | Sixteen focused status-contract regression tests passed, including status-path boundary and child-path-swap regressions. | None | None |
| `make check-apache-request-transaction-cleanup-lint` after the fix | `0` | Five Python source tests passed; missing `apxs` wrote `blocked`, direct exit `77`, and allowed workflow exit `0`. | `$(BUILD_ROOT)/check-status/apache-request-transaction-cleanup.json` | None |
| `make check-apache-request-transaction-cleanup` after the fix | `2` expected negative control | Five Python source tests passed; missing `apxs` remained `BLOCKED` and nonzero. | None | None |
| `make lint` | `failed` (exit `2`, local-only) | The unchanged Apache C17 preflight attempted local runtime provisioning and stopped at `missing_local_httpd_build` before the modified cleanup target. | None | None |
| `CI=true make lint` | `0` | CI-mode local run took the same unavailable-prerequisite branch used by GitHub Actions: the existing C17 check was visibly skipped and the modified cleanup check emitted its allowed `blocked` record. | None | None |
| `make quick-check` | `failed` (exit `2`, local-only) | It inherits the same unchanged local Apache C17 provisioning failure from `lint`, before the modified cleanup target. | None | None |
| `CI=true make quick-check` | `0` | CI-mode quick-check passed; this is local contract evidence, not a substitute for exact-SHA GitHub Actions. | None | None |
| `make check-bilingual-docs` | `0` | Bilingual documentation check passed. | None | None |
| `make check-doc-links` | `0` | Repository-path-reference and documentation-link checks passed. | None | None |
| `make check-variable-documentation` | `0` | Variable documentation check passed. | None | None |
| `make -n test-common`, `make -n test-apache`, `make -n test-nginx`, `make -n quick-framework-check` | `not_applicable` | The root Makefile defines no targets with those workflow names; their real chains are documented above. | None | None |
| `make -n check-repository-path-references` | `not_applicable` | No standalone target exists; `make check-doc-links` invoked the actual repository-path-reference check. | None | None |
| `git diff --check` | `0` | No whitespace errors at the recorded local-review point. | None | None |

## Security impact

No product security behavior, host action, authentication, authorization, or
runtime data boundary changes. The runner is fail-closed for every unrecognized
nonzero command exit and every `77` without its caller's exact approved marker.
Its status sink has no arbitrary-path interface: a validated identifier selects
a fixed filename below a canonical external build root, while checkout-local,
noncanonical, and symlinked roots or targets are rejected. The runner anchors
the verified directory before running the child, so a child cannot redirect the
temporary creation or final replacement by swapping the build-root path. It
persists only a fixed check identifier, status, command and workflow exit codes,
and a non-sensitive disposition reason when applicable.

## Documentation changes

- `ci/README.*` defines the status runner, its JSON status contract, and the
  strict-versus-lint Make behavior.
- `docs/testing-and-evidence.*` adds `NOT APPLICABLE` and distinguishes the
  lowercase CI control statuses from runtime evidence.
- `docs/reference/variables.*` documents the external status-root variables.
- This Change Record pair captures the root cause, workflow scope, tests, and
  final-delivery follow-up.

## Runtime evidence

No runtime evidence was collected or claimed for this change. The tests are
source, process-control, and CI-contract tests only; neither a successful lint
run nor a JSON status record proves Apache runtime behavior.

## CRS/MRTS and protocol disposition

| Scope | CRS/MRTS combinations | H1/H2/H3 | Status | Reason |
| --- | --- | --- | --- | --- |
| Apache cleanup status transfer | `no_crs_no_mrts`, `with_crs_no_mrts`, `no_crs_with_mrts`, `with_crs_with_mrts` | H1, H2, H3 | `not_applicable` | The change alters only Parent CI control flow before a native harness could run; it changes no ruleset selection, request/response behavior, or transport. |
| NGINX, HAProxy, Envoy, Traefik, and lighttpd | `no_crs_no_mrts`, `with_crs_no_mrts`, `no_crs_with_mrts`, `with_crs_with_mrts` | H1, H2, H3 | `not_applicable` | No connector product code, build contract, configuration, or runtime path changed. |

## Known limitations

- The local environment lacks `apxs` and usable Apache development headers, so
  the native Apache/APR harness remains `blocked` locally.
- Plain local `make lint` and `make quick-check` use the unchanged Framework
  local-provisioning policy, which attempts to construct missing Apache
  components and currently stops at `missing_local_httpd_build` before this
  change's cleanup target. The CI-mode branch returns the declared unavailable
  prerequisite instead and passed locally; remote exact-SHA runs remain the
  authoritative CI evidence.
- The record preserves a control-plane disposition only; the detailed direct
  prerequisite diagnostic remains in the harness log output.
- Pull-request instances of the five workflows intentionally skip their heavy
  Push-only step; their successful scaffold result is not a substitute for the
  Push evidence.
- CRS/MRTS and H1/H2/H3 runtime matrices are `not_applicable`: this task
  changes neither connector runtime behavior nor ruleset or transport
  selection; the explicit dispositions are recorded above.

## Remaining risks

The explicit allowance is intentionally narrow: only missing discovery of a
usable `apxs`/`httpd.h` pair currently carries
`apache_development_prerequisite`. Future callers of `run-check-status.py`
must document their own exact allowed marker or `not_applicable` contract
rather than reuse it as a global bypass. Exact-SHA GitHub Actions verification
remains required before delivery completion.

The directory-FD defense assumes the invocation-owned `BUILD_ROOT` path is not
being concurrently replaced by an equally privileged external process before
the runner opens its status directory. Once opened, the child-path-swap
regression proves that the child cannot redirect the status write. Componentwise
directory opening from a separately trusted base would be required for a
stronger hostile-parent-filesystem model.

## Checks not run and rationale

- No Apache native build, APR lifecycle binary execution, runtime smoke, or
  protocol test ran because the local Apache build prerequisite is absent; the
  expected status is `blocked`, and the focused synthetic regression tests
  cover the status-transfer contract.
- No `make test-common`, `make test-apache`, `make test-nginx`,
  `make quick-framework-check`, or `make check-repository-path-references`
  target ran because those target names do not exist; their applicable real
  checks are listed above.
- Exact final Push and Pull Request workflow commands are pending branch
  delivery and are not represented as local passing evidence. `CI=true` local
  runs exercise the Framework CI branch only and do not replace them.

## Final diff and review status

At this local-review point, `git diff --check` passes and the reviewed scope is
limited to the Parent CI classification contract, its regression tests, paired
documentation, and this record. Before delivery, this record will be
reconciled with the staged diff, commit SHA, Draft PR, and exact-SHA GitHub
Actions outcomes. No Framework state or PR #42 change is included.
