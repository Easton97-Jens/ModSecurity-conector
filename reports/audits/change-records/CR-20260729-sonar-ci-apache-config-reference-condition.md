# Change Record: Parent CI Apache config-reference condition remediation

**Language:** English | [Deutsch](CR-20260729-sonar-ci-apache-config-reference-condition.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-apache-config-reference-condition` |
| Date (UTC) | `2026-07-29` |
| Base revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` |
| Source revision assessed | Local task patch against the stated base revision |
| Boundary | Only Parent `ci/checks/documentation/connector_config_reference.py`, its direct Parent regression test, this English/German Change Record pair, and the paired indexes. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, generated configuration-reference output, SonarQube Cloud configuration, Quality Gate, exclusion, suppression, default-branch, or merge action is included. |
| SonarQube Cloud linkage | Remediates the current `python:S3358` nested conditional at the Apache directive example-file selector. No scanner control is changed. |

## Motivation and problem statement

The Parent CI configuration-reference inventory selected the Apache example
file through a nested conditional. SonarQube Cloud reports that construction
under `python:S3358`. Although the three outcomes are simple, they are part of
the source-backed configuration reference: changing their partition could make
a directive point at a wrong configuration example without changing its parser
registration.

The required behavior has three exact cases: one source-file directive, three
minimal-configuration directives, and all remaining registered Apache
directives using the safe configuration example.

## Acceptance criteria

- The nested condition is replaced with an explicit safe default plus two
  clearly named exceptional branches.
- `modsecurity_phase4_content_types_file` continues to reference
  `connectors/apache/src/msc_config.c`.
- Only `modsecurity`, `modsecurity_rules_file`, and
  `modsecurity_use_error_log` reference `examples/apache/minimal/httpd.conf`.
- Every other extracted Apache directive continues to reference
  `examples/apache/safe/httpd.conf`.
- The focused test, non-writing generator/checker controls, syntax, whitespace,
  bilingual documentation, security review, and an exact Draft-PR head provide
  the recorded evidence. Hosted SonarQube Cloud must show zero new issues,
  zero new duplicated lines, and `0.0%` New-Code duplication without weakening
  scanner controls.

## Implementation decision and rationale

The selector now starts at the safe Apache example and overrides it only for
the source-file directive and the explicit minimal-example directive set. This
is clearer than nesting one conditional in another while retaining the same
priority and output bytes for all registered directives.

The focused regression test derives its mapping from `extract_apache()` and
asserts all three partitions. It prevents a future directive addition from
silently inheriting an unexpected example-file category.

## Changed files

- `ci/checks/documentation/connector_config_reference.py`
- `tests/test_connector_config_reference.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-apache-config-reference-condition.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-apache-config-reference-condition.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

### Tests and actual results

| Command or control | Result |
| --- | --- |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> <repository-venv-python> -m unittest -v tests.test_connector_config_reference` | passed: 1 focused mapping test. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make check-connector-config-reference` | passed: the non-writing generator reported 21 current generated files; the reference checker reported `apache=14, nginx=18, haproxy=41, envoy=141, traefik=71, lighttpd=19, common=25, engine=12`. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> <repository-venv-python> -m py_compile ci/checks/documentation/connector_config_reference.py tests/test_connector_config_reference.py` | passed. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> find ci/checks/documentation -type f -name '*.py' -exec <repository-venv-python> -P -m py_compile {} +` | passed: the complete selected `ci/checks/documentation/` Python syntax scope. |
| `git -C <task-worktree> diff --check` | passed for the currently tracked source and index patch. The final staged all-file whitespace check remains required for the untracked regression test and Change Record pair. |
| `git -C <task-worktree> diff --cached --check` | passed for the exact six task-owned staged source, test, Change Record, and index files. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make check-bilingual-docs` | `blocked_external_dependency`: no error names this Change Record pair; every reported missing link is an existing target under the intentionally absent Framework submodule. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make check-doc-links` | `blocked_external_dependency`: every reported target is an existing reference under the intentionally absent Framework submodule; no new Change Record target is reported. |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> make lint` | `blocked_external_dependency`: Parent shell syntax and CI Python compilation ran, then an existing no-CRS check could not import the intentionally absent Framework `ci/checks/catalog/no_crs_baseline.py`. |
| Independent scoped security/diff review | passed: no plausible reportable diff-induced security candidate; the review traced the complete source/minimal/safe mapping, immediate renderer/checker consumers, and the direct regression test. |

## Security impact

The changed code reads repository-owned Apache registration data and assigns a
documentation-example path; it neither opens a file nor changes a parser,
command, network, credential, or runtime request path. The relevant invariant
is that every registered Apache directive keeps its exact source/minimal/safe
example-file category. The focused test exercises the exceptional categories
and the complementary safe-default category.

The focused security preflight and independent final scoped source/test diff
review found no plausible reportable issue. This maintenance remediation does
not claim a runtime security fix.

## Runtime evidence

No connector runtime, networked host, or generated configuration-reference
write is claimed. The non-writing generator/checker validates the repository
inventory and the direct unit test validates the complete Apache mapping
partition. These are source-level evidence only.

## Known limitations

The task worktree intentionally has no populated Framework submodule, so
broad targets that import Framework checks cannot complete locally. This does
not affect the focused Parent mapping test or the non-writing configuration-
reference controls, but it limits local broad-lint evidence.

## Remaining risks

The explicit source branches preserve the selected output mapping locally, but
the final result is not yet verified on an exact hosted Draft-PR head. Any
behavior outside this Parent CI extractor, including generated output and
connector runtime configuration parsing, remains unchanged and is not claimed
by this record.

## Checks not run and rationale

- The broad connector runtime suite and `make test` run Framework-owned
  provisioning and runtime paths that are unavailable in this intentionally
  unpopulated worktree and outside this non-writing CI selector's scope.
- The full connector runtime matrix, generated-output writes, and networked
  host checks are out of scope for this non-writing CI inventory selector.
- Hosted GitHub Actions, SonarQube Cloud PR analysis, review, approval, merge,
  and master verification do not exist yet and are not inferred locally.

## Final diff and review status

The source patch, focused direct mapping test, selected syntax compilation,
tracked-patch whitespace check, and native non-writing configuration-reference
controls passed. The final staged all-file whitespace check passed for the
complete six-file task-owned diff. The two broad documentation targets and
broad lint target are blocked only by the intentionally absent Framework
submodule, with no error for this record pair. Exact-head hosted and SonarQube
Cloud evidence is added only after it is observed. The final security review
found no plausible reportable diff-induced candidate. No commit, push, pull
request, hosted check, review, approval, merge, or `master` change is claimed
by this initial record.
