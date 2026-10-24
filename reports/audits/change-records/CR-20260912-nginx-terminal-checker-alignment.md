# Change Record: NGINX terminal response-header checker alignment

**Language:** English | [Deutsch](CR-20260912-nginx-terminal-checker-alignment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260912-nginx-terminal-checker-alignment |
| Date (UTC) | 2026-09-12 |
| Base revision | `a24d22da8e11cd99ba05f24f9f53f92a792591c4` |
| Delivery status | Local successor patch only. No successor commit, remote branch, pull request, or successor merge has occurred. PR #360 was already squash-merged at the base revision; a distinct successor PR needs separate exact merge authorization. |

## Motivation and problem statement

After PR #360 was merged, five resulting-master workflows failed through the
same NGINX Common-adoption checker. The checker still expected the earlier
two-guard header-filter form and a collection-failure branch without the new
sticky failure flag. The production source is intentionally stricter: a
terminal response-header processing failure returns `NGX_ERROR` on filter
re-entry instead of forwarding to the next header filter.

## Acceptance criteria

- The current fail-closed header-filter source is accepted by
  `check-nginx-common-adoption.py`.
- The checker requires one direct `response_headers_processing_failed` guard
  returning `NGX_ERROR` before the permissive intervention guard.
- The collection-failure branch sets that sticky flag before its terminal
  `NGX_ERROR` return.
- Isolated mutations that make the retry guard permissive or remove the
  collection-failure assignment are rejected.
- Existing NGINX source-contract, fixture-contract, and CI-security contract
  checks remain green; no runtime source or CI-control is weakened.

## Implementation decision and rationale

Only the NGINX Common-adoption checker and its isolated mutation coverage are
changed. The checker recognizes three ordered top-level guards: missing
context, sticky terminal failure, then intervention. It also requires the
sticky assignment in the direct response-header collection failure branch.

No NGINX C runtime source, Framework/MRTS source, Gitlink, workflow, ruleset,
branch protection, SonarQube setting, exclusion, suppression, or dependency is
changed. The direct wrapper, exact `ret != 1` native-error contract, and
anti-bypass structural checks remain intact.

## Security impact

This static-checker correction strengthens the proof of existing fail-closed
behavior. A persistent response-header processing failure must not be converted
into the intervention path that forwards to the next header filter. The new
mutation tests prove that the checker rejects a permissive replacement of this
guard and removal of the collection-failure sticky assignment.

An adjacent negative-intervention re-entry path was inspected but not proven
reachable with the available source-only evidence. It is an unresolved
validation question, not a demonstrated vulnerability or a reason to change
runtime source speculatively.

## Changed files

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20260912-nginx-terminal-checker-alignment.md`
- `reports/audits/change-records/CR-20260912-nginx-terminal-checker-alignment.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or check | Result | Observed result |
| --- | --- | --- |
| `python -m py_compile ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` | passed | Python syntax validation passed. |
| `make check-nginx-common-adoption` | passed | All emitted NGINX Common-adoption assertions passed. |
| focused checker and upstream-security tests | passed | 20 focused checker and upstream-security tests passed. |
| full checker, upstream-security, and fixture-contract suite | passed | 115 tests passed. |
| `python -m unittest -v tests.test_ci_security_workflows` | passed | 30 CI-security contract tests passed. |
| `git diff --check` | passed | No whitespace errors in the local successor diff. |

## Runtime evidence

No native NGINX runtime was built or executed for this checker-and-test-only
change. The existing fixture contract covers zero, negative, and reinvocation
scenarios structurally; it is not host-runtime evidence.

## Checks not run and rationale

`make lint` was not run because it requires the Framework submodule in this
isolated Parent worktree. `make check-bilingual-docs` and `make check-doc-links`
were run and failed only on pre-existing links into that uninitialized
submodule. The Parent boundary policy prohibits automatic initialization
without a separate explicit user decision. Exact successor-head hosted checks,
SonarQube Cloud analysis, review disposition, and resulting-master workflows
cannot exist until a successor PR is authorized and created.

## Known limitations

The base revision remains red in five workflow call chains until the successor
is delivered and its exact-head checks run. Local evidence proves only the
checker/test boundary, not NGINX host-runtime behavior. The adjacent
negative-intervention re-entry question remains unproven.

## Remaining risks

The correction deliberately requires the currently reviewed C shape. A future
legitimate refactor of the header-filter guards or collection-failure branch
must update the checker and its negative controls in the same change. No
security finding is closed solely on this local evidence.

## Final diff and review status

The local two-file implementation diff was independently reviewed for security
and test coverage. The review found no weakening or direct checker bypass. The
checker requires the terminal guard and sticky assignment; scoped mutation and
contract evidence passed. Delivery, hosted validation, SonarQube Cloud, and a
successor merge are pending separate authorization.
