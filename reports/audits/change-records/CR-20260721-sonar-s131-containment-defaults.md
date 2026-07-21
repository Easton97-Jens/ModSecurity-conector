# Change Record: Explicit Parent analysis-output containment defaults for SonarQube Cloud S131

**Language:** English | [Deutsch](CR-20260721-sonar-s131-containment-defaults.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260721-sonar-s131-containment-defaults |
| Date (UTC) | 2026-07-21 |
| Base revision | 2ade0d40983b7af21a65b8cd2884866b85626393 |
| Tracking | Five Parent-only shelldre:S131 Code Smells: AZ9dWh6Oxi9ITghe3pzl, AZ9dWh6Oxi9ITghe3pzm, AZ9dWiAVxi9ITghe3pzr, AZ9dWiAVxi9ITghe3pzs, and AZ9dWiAAxi9ITghe3pzn. |
| Boundary | Parent C/C++ analysis-output guards and their focused Python contract only; Framework, MRTS, gitlinks, connector runtime, scanner configuration, and Quality Gates remain unchanged. |

## Motivation and problem statement

Five negative checkout-output containment cases intentionally relied on unmatched
case fall-through when a normalized path was outside the checkout. SonarQube
Cloud rule shelldre:S131 reports those missing default arms. The existing
rejection behavior is an output-containment control and must remain fail-closed
for checkout-root and checkout-descendant paths.

## Acceptance criteria

- Keep every existing checkout-root and checkout-descendant rejection message,
  exit status, normalization step, and directory-creation ordering intact.
- Make only the permitted already-external route explicit with the POSIX no-op
  default branch: *) : ;;.
- Add a focused control that proves external outputs continue to their next
  missing-tool dependency gate, while checkout outputs remain rejected before
  directory creation.
- Obtain a fresh exact Draft-PR SonarQube Cloud analysis before claiming the
  five original keys are resolved.

## Implementation decision and rationale

Each selected case retains its existing matching branch, which exits with status
2 for an output inside the checkout. The added default branch invokes the POSIX
colon no-op and then falls through to the unchanged next instruction. This is
equivalent to the prior unmatched-case behavior but makes the permitted
continuation visible to the shell analyzer.

The focused Python contract uses a deliberately absent compiler name for an
external output request. It proves that each script passes its containment check,
creates only its external requested path, and reaches the next documented
dependency gate with status 77. The pre-existing rejection contract continues to
assert status 2, the containment message, and no checkout-local directory
creation.

## Security impact

This is a maintainability remediation around security-sensitive output
containment checks. It does not expand an accepted path set: a normalized
checkout path still exits before mkdir, while an already-external path still
continues. It adds no suppression, rule disablement, Quality-Gate change,
NOSONAR marker, authentication change, authorization change, runtime protocol
behavior, or Framework/MRTS change.

The first hosted analysis of the Draft PR closed the five S131 observations but
reported a new `python:S5443` issue in the newly added contract test. The test
had directly forwarded its mutable `TMPDIR` value to
`TemporaryDirectory(dir=...)`. The follow-up removes that explicit
source-to-sink edge and keeps the standard library's randomized,
process-owner-only `TemporaryDirectory` primitive. This is a narrowly scoped
scanner/security-hygiene remediation for a contract test, not a claim that the
test provisions a generally trusted parent or a change to a deployed connector
trust boundary.

## Changed files

- ci/checks/analysis/compile-db-cpp17.sh
- ci/checks/analysis/compile-db-nginx-c17.sh
- ci/checks/analysis/check-targeted-evaluator-cpp17.sh
- tests/test_c_cpp_diagnostics.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| rtk proxy sh -n ci/checks/analysis/compile-db-cpp17.sh | passed. |
| rtk proxy sh -n ci/checks/analysis/compile-db-nginx-c17.sh | passed. |
| rtk proxy sh -n ci/checks/analysis/check-targeted-evaluator-cpp17.sh | passed. |
| rtk proxy env TMPDIR=<task-owned external path> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics | passed: 6 tests, including checkout rejection and external-output continuation controls. |
| rtk proxy env TMPDIR=<task-owned path> PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics tests.test_bilingual_docs | passed after the S5443 follow-up: 17 tests, including the external-output continuation, checkout rejection, and documentation controls. |
| rtk proxy git diff --check | passed after the source and contract change. |

## Runtime evidence

No connector runtime behavior changes. The focused contract invokes only the
three local analysis scripts with an intentionally missing compiler after their
output-containment checks. It does not run a compilation database build, link
libmodsecurity, or start a connector.

## Exact PR-head delivery evidence

A Draft PR and exact-head GitHub Actions/SonarQube Cloud evidence are required
after the normal source commit and push. This record does not claim those future
results. The final PR description and retained task evidence will identify the
actual final SHA and exact hosted results without a self-referential commit
loop.

## Checks not run and rationale

- make compile-db-cpp17 and make compile-db-nginx-c17 were not run: they require
  Bear plus full C++/NGINX and libmodsecurity build prerequisites, while the
  focused test proves the selected default branches without pretending that an
  unavailable product build passed.
- check-targeted-evaluator-cpp17 with a real compiler was not run: it requires
  a usable MODSECURITY_INCLUDE_DIR and MODSECURITY_LIB_DIR. The focused external
  control instead reaches its documented missing-compiler gate.
- The complete repository bilingual checker is expected to be environment-
  blocked in the isolated Parent worktree by unpopulated Framework link targets;
  the focused bilingual documentation test and exact PR CI remain the available
  controls.

## Known limitations

The local validation proves the five shell branches and their immediate
containment/dependency behavior, not a full compilation database or connector
runtime. Hosted exact-head SonarQube Cloud evidence remains required.

## Remaining risks

Other shelldre:S131 observations have different policies for unknown values and
are intentionally not grouped here. The broader Parent SonarQube Cloud
vulnerability and maintainability backlog remains tracked separately. This
record does not authorize a merge.

## Final diff and review status

The intended diff consists of five explicit no-op default arms, one focused
contract test that relies on the standard secure temporary-directory API
without manually forwarding `TMPDIR`, and this traceability pair/index.
Before any Draft PR is considered verified, the final diff, exact
local/remote/PR SHA equality, GitHub Actions, SonarQube Cloud Quality Gate,
five-key and S5443 issue queries, and review state must be rechecked for the
current head.
