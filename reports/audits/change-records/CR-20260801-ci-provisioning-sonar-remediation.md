# Change Record: Parent CI provisioning SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-ci-provisioning-sonar-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-ci-provisioning-sonar-remediation` |
| Date (UTC) | `2026-08-01` |
| Base revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | Current open SonarQube Cloud inventory beneath `ci/provisioning`: 21 `python:S3776`, 10 `python:S1192`, 3 `pythonsecurity:S6549`, 2 `python:S3358`, 1 `python:S1066`, 1 `python:S8786`, and two duplicate blocks (25 lines). Local record: `FND-SONAR-0030`. |
| Boundary | Parent `ci/provisioning` and direct Parent regression tests only. Framework, MRTS, both Gitlinks, workflow configuration, scanner configuration, and `master` are unchanged. |

## Motivation and problem statement

The selected current SonarQube Cloud directory reported 38 open source rows in
`ci/provisioning/components/prepare-runtime-components.py` and two duplicate
report-formatting blocks. The provisioner is security-sensitive build plumbing:
it reads cache manifests, accepts configured paths and URLs, prepares source
trees and archives, invokes tools, and publishes artifacts. The remediation
therefore removes the complexity, repeated-literal, conditional, regular-
expression, and duplication causes without using suppressions or weakening a
path, ownership, provenance, staging, or publication control.

## Acceptance criteria

- The current 38-row source inventory and both provisioning-side duplicate
  blocks are replaced by behavior-preserving, reviewable code rather than by
  `NOSONAR`, exclusions, rule changes, Quality-Gate changes, or code moves.
- Managed-cache containment, marker ownership, legacy-deletion-only behavior,
  fresh staging, atomic publication, HTTPS/provenance checks, Framework V3
  provenance validation, and connector-specific runtime semantics remain
  effective.
- Focused normal and negative controls pass, including all three independently
  configurable Expat override paths.
- A fresh SonarQube Cloud analysis of the exact Draft-PR head is obtained
  before claiming that the inventory is resolved or that the directory has no
  new issues or duplicate blocks.

## Implementation decision and rationale

The large provisioner is decomposed at its existing semantic boundaries. Small
private helpers make cache-manifest matching, cache-entry preparation, archive
validation, source hashing, Expat override handling, ModSecurity preparation,
connector planning, report assembly, and CLI composition independently
readable. Repeated operational filenames and status labels have one private
owner. The nested connector expressions are explicit branches, while the
Apache failure diagnostic uses bounded, line-local matching rather than the
former broad regular-expression shape.

The report representation is assembled through private formatting helpers but
remains byte-identical for a representative complete payload. This removes the
two provisioning-side duplicate blocks without changing the independently
owned evidence-report implementation. A silent non-zero Git-submodule result
now carries an explicit failure status instead of relying on diagnostic text;
the caller fails closed even when both output streams are empty.

The first exact PR-head analysis after that broader refactor reported eight
further source-level maintainability issues in the newly factored provisioner:
four repeated literals, two unused private parameters, one nested conditional,
and one redundant NGINX protocol-profile parameter. The same candidate now
gives those literals one private owner, removes the unobserved parameters,
short-circuits the Expat `autoreconf` failure without changing branch order,
and derives the NGINX build profile from the already resolved protocol inputs.
This follow-up preserves every cache, provenance, and build contract; it is not
a Sonar rule, Quality-Gate, exclusion, or suppression change.

The next exact PR-head SonarQube Cloud readback found two S3415 test
diagnostics in the two newly added assertions: they supplied expected value
before actual value. Both calls now use the framework's actual-then-expected
order. This corrects diagnostic/reporting semantics only; it does not change
the tested Expat failure or NGINX profile contract. The exact-head hosted
rerun remains required before the candidate is reported verified.

## Security impact

No trust boundary is relaxed. Manifest path values are compared as data only;
filesystem deletion, publication, copy, directory creation, and build sinks
continue to require managed-root containment and ownership markers. Git and
archive inputs retain URL, ref, digest, lock, staging, clean-tree, submodule,
and `git fsck` checks before publication. The Framework V3 provenance guard
still runs before all ModSecurity build sinks, and normal-prefix publication
continues to precede build-root publication.

The Expat controls now prove each of `EXPAT_PREFIX`, `EXPAT_BUILD_DIR`, and
`EXPAT_SOURCE_COPY` separately: a legitimate marked managed child is accepted,
while an external path, canonical traversal, and symlink escape are rejected
before build or publication. A completed baseline scoped security scan found
no reportable issue; the required post-change security-diff review is retained
as a separate exact-diff verification step.

## Changed files

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_prepare_runtime_components tests.test_runtime_component_cache_contract tests.test_runtime_component_cache_identity tests.test_runtime_env_snapshot_contract tests.test_runtime_artifact_utils tests.test_runtime_path_policy` | passed: 90 focused provisioner, cache, environment, artifact, and path-policy tests. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/provisioning/components/prepare-runtime-components.py` | passed. |
| `make check-runtime-path-policy PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` | passed. |
| `git diff --check` | passed before documentation authoring; repeated after the final documentation/security review. |

## Runtime evidence

The Parent-pinned Framework revision was initialized only inside the isolated
task worktree as a test fixture, allowing the focused Parent tests to exercise
the normal cache/provisioning contracts. It did not change Framework source,
MRTS source, or either Gitlink. No real network download, package installation,
or native connector build was run in this task; those operations are outside
the deterministic local regression suite and require their own controlled
environment evidence.

## Exact PR-head delivery evidence

At record authoring, no commit, push, Draft PR, hosted CI result, or hosted
SonarQube Cloud result is claimed. The task is prepared on an isolated branch
from the listed base revision. The PR description and final delivery evidence
must identify the exact local, remote, and PR-head SHA and then record the
fresh hosted result for that exact head.

## Checks not run and rationale

- A full real provisioning build was not run because it downloads and builds
  third-party runtime components; that is broader than the requested static
  remediation and not needed to validate the changed local contracts.
- The broad `make lint` aggregate did not pass locally. With writable task-
  owned output roots it reaches the unmodified Apache C17 lint path and fails
  on existing warnings-as-errors in
  `connectors/apache/src/mod_security3.c` and `connectors/apache/src/msc_config.h`.
  The same command at the current root `master` produces the same failures,
  and those three Apache paths have no diff from this task's base. This is
  recorded as an external baseline limitation, not as a passing provisioner
  lint result and not corrected by weakening `-Werror`.

## Known limitations

Focused local tests and source review demonstrate the changed control paths,
but they are not a hosted SonarQube Cloud analysis. The final post-change
security-diff scan, bilingual-documentation check, commit, Draft PR, and
exact-head hosted verification remain required before the remediation can be
reported as fully verified.

## Remaining risks

The current project-wide SonarQube Cloud backlog outside `ci/provisioning` is
not part of this change. The three existing S6549 alerts are not dismissed by
this record: their claimed path-escape outcome is covered by source/sink
review and dedicated negative controls, while the exact PR-head analysis must
still determine their current hosted disposition. No master integration is
authorized by this Change Record.

## Final diff and review status

This is a pre-delivery record for the isolated remediation candidate. Its
final status is contingent on an exact-head security review, a final scoped
diff check, local documentation validation, and a truthful Draft-PR delivery.
It does not claim mergeability or authorize a merge.
