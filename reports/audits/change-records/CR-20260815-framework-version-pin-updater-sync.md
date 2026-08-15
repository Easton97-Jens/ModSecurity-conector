# Change Record: Framework-central version-pin updater synchronization

**Language:** English | [Deutsch](CR-20260815-framework-version-pin-updater-sync.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260815-framework-version-pin-updater-sync |
| Date (UTC) | 2026-08-15 |
| Base revision | `29a2a8bcab57e936c5274f8fe64a15c6fee879bd` |
| Delivery status | [PR #291](https://github.com/Easton97-Jens/ModSecurity-conector/pull/291) targets `master` and is ready for review. Its initial head `f804ed598d2515fc972b8f8308678d95a5584fb7` exposed ShellCheck `SC2006`, fixed in `52c25c08ac309ecbe7edb72baeeabb0841ddba30`; follow-ups then resolved the hosted nested-submodule fixture identity defect and 18 task-owned SonarQube Cloud New Issues with source-native root, symlink, argument, complexity, and contract fixes. The verified delivery round at `788c1a79f4ff36816141253515f1b9e5469e64ab` observed all applicable GitHub checks passing and SonarQube Cloud Quality Gate `OK` with 0 New Issues, 0 Accepted Issues, and 0 Security Hotspots. The branch was updated with one non-overlapping current-`master` commit before that round. No `master` integration was performed or is authorized by this record. |

## Motivation and problem statement

The Framework `ci/lib/common.sh` is the central version authority. The Parent
repository contained semantically corresponding component pins and contracts
that could drift when the Framework submodule was updated. The protected
Framework-update workflow therefore needs to carry the approved Framework
version tuples into the Parent atomically and fail closed when the source or a
mapped target is invalid.

## Acceptance criteria

- Framework declarations for Envoy, lighttpd, HAProxy, NGINX/QUIC, and CRS are
  mapped to every corresponding Parent-owned pin or contract.
- A Framework update extracts the exact candidate `common.sh` object as data,
  synchronizes the registered Parent targets, rechecks them, and stages only
  the explicit allowlist and generated compiler-guide outputs.
- The updater never sources or evaluates Framework shell input and rejects
  missing, duplicate, malformed, unrecognized, symlinked, or special-file
  inputs without an unintended partial write.
- Current Framework values are a stable no-op, valid changed values update all
  registered targets, and focused regression tests cover rollback and failure
  cases.
- Framework source, MRTS, and the Parent Framework gitlink remain unchanged.

## Implementation decision and rationale

`ci/tools/sync-framework-component-versions.py` implements a bounded literal
parser and an explicit target registry. It validates the complete Framework
version tuples, preserves target modes, uses containment and file-type checks,
and rolls back completed replacements if a later replacement fails. The
publisher in `.github/workflows/update-submodules.yml` initializes only the
trusted top-level Framework, reads the exact candidate `ci/lib/common.sh` Git
object, runs `--validate`, `--sync`, and `--check`, regenerates compiler guides,
and rejects changed paths outside its explicit allowlist.

The registered mappings cover Envoy `1.39.0`; lighttpd `1.4.85` and its source
metadata; HAProxy `3.2.22` and its HTX contract; the NGINX release tuple
`release-1.31.3`, NGINX QUIC TLS `4.0.1`, and their digests; and CRS
`v4.28.0` with commit `55b09f5acfd16413e7b31041100711ceb7adc89c` as represented by the retained Framework
input. Lighttpd and HAProxy build/lifecycle consumers now derive values from
their contracts. Compiler guides derive from bounded Parent contracts rather
than executing Framework shell.

## Security impact

This change protects a dependency-update and code-execution boundary. The
updater treats Framework shell as untrusted data, does not execute it, limits
writes to registered Parent files, validates URLs, references, digests, and
tuple consistency, rejects symlinks and special files, and provides atomic
rollback behavior. The workflow no longer recursively initializes
candidate-controlled nested submodules. No permission, scanner, test, or
quality-gate weakening was introduced.

The follow-up additionally confines extracted Framework data to the
runner-controlled temporary root, validates every Git subprocess root and
argument vector, and confines the HAProxy contract reader to its fixed overlay
root with no-follow regular-file access. The nested-submodule regression
fixture configures its local commit identity explicitly for hosted runners.
The updater regression fixture now also creates its temporary repository below
`RUNNER_TEMP` when that GitHub runner root is supplied, so its test data follows
the same root contract as the production invocation.
The reader canonicalizes both the checked candidate and its approved root at
the filesystem boundary, rejects any symlink resolution, and then retains the
component walk, no-follow descriptor opening, regular-file check, and size
bound.

## Changed files

The task-owned Parent diff is grouped below; the English and German records
describe the same coverage.

- Update and CI orchestration: `.github/workflows/ci-security-workflow-lint.yml`,
  `.github/workflows/nginx-root-broker.yml`,
  `.github/workflows/update-submodules.yml`, `Makefile`.
- Synchronizer and validation: `ci/tools/sync-framework-component-versions.py`,
  `ci/checks/connectors/all/check-remaining-connectors-common-adoption.py`,
  `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`,
  `ci/checks/evidence/check-runtime-producer-readiness.py`,
  `ci/provisioning/components/prepare-runtime-components.py`,
  `ci/runtime/broker/nginx_root_broker.py`,
  `ci/runtime/broker/protected_nginx_broker_caller.py`,
  `ci/runtime/lifecycle/resolve-full-lifecycle-profile.py`,
  `ci/tools/validate-submodule-candidate-state.py`.
- Connector contracts and consumers: `connectors/envoy/ext_proc/README.md`,
  `connectors/envoy/ext_proc/README.de.md`, the modified HAProxy files under
  `connectors/haproxy/` including `htx-overlay/haproxy-makefile.patch`,
  `htx-overlay/version-contract.json`, and `htx-overlay/version_contract.py`,
  the modified lighttpd files under `connectors/lighttpd/` including
  `build/read_version.sh`, `lighttpd-version.contract`, and
  `patches/0001-lighttpd-msconnector-stream-hooks.patch`, and the modified
  NGINX README files under `connectors/nginx/`.
- Documentation and generated evidence: modified files under
  `docs/build/compilers/`, `docs/reference/variables.*`,
  `docs/security/trusted-nginx-root-broker.*`, modified lighttpd example
  READMEs and `examples/lighttpd/safe/lighttpd-http1-identity.conf`,
  `scripts/generate_compiler_guides.py`, and the three generated files under
  `reports/testing/generated/canonical/connector-capabilities.generated.*`.
- Regression coverage: `tests/test_ci_security_workflows.py`,
  `tests/test_full_lifecycle_profiles.py`,
  `tests/test_haproxy_modsecurity_resolver.py`,
  `tests/test_validate_submodule_candidate_state.py`, and
  `tests/test_update_framework_versions.py`.

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| `python3 ci/tools/sync-framework-component-versions.py --validate --repo-root . --framework-common <retained Framework common.sh blob>` | passed; returned `{"changed": [], "mode": "validate"}` |
| `python3 ci/tools/sync-framework-component-versions.py --check --repo-root . --framework-common <retained Framework common.sh blob>` | passed; returned `{"changed": [], "mode": "check"}` |
| Focused updater/workflow/compiler/lifecycle/HAProxy/submodule unittest suite | passed; 87 tests |
| Lighttpd patched-host contract tests | passed; 26 tests |
| NGINX root/protected broker tests | passed; 64 tests |
| Post-`actionlint` remediation workflow/submodule/updater unittest suite | passed; 52 tests |
| Current Sonar/actionlint remediation aggregate | passed; 140 tests with 4 expected capability skips under a task-owned writable `RUNNER_TEMP` simulation |
| Connector, shell-syntax, variable-documentation, no-CRS documentation, and evidence-output security checks | passed |
| `python3 -m py_compile` on changed relevant Python files | passed |
| `git diff --check 29a2a8bcab57e936c5274f8fe64a15c6fee879bd` | passed |
| Finalized security-diff scan | passed; 0 reportable findings |
| GitHub Actions delivery round | passed; all applicable current-head status checks, including `actionlint`, CodeQL-backed jobs, and connector contracts |
| SonarQube Cloud delivery round | passed; Quality Gate `OK`, 0 New Issues, 0 Accepted Issues, 0 Security Hotspots |

The exact Framework input was the retained `ci/lib/common.sh` object for
gitlink `1260aaae411ecf88cf50dc480b80e2e20ac47901`. The security scan report
is retained at the task-owned external evidence path under
`/var/tmp/codex/ModSecurity-conector/tasks/framework-version-pin-updater-sync-20260815/security-diff-scan/report.md`.

## Runtime evidence

The evidence is local static validation, contract tests, parser tests, upstream
patch compatibility checks, and observed GitHub-hosted PR check rounds. No
complete runtime matrix, production runtime, or true hosted Framework-update
publisher run was executed or claimed.

## Checks not run and rationale

- `actionlint` was not run locally because it is not installed in the
  environment; its hosted PR check passed in the verified delivery round.
- The scheduled/manual Framework-update publisher was not run: it is not
  PR-triggered and would require a separately authorized Framework update.
- Full Framework-dependent integration/runtime validation was not run because
  the exact Framework submodule checkout is intentionally absent from the task
  worktree.
- `make check-bilingual-docs` could not complete its pre-existing local
  Framework-link checks for the same absent submodule; no changed-document
  parity error remained.

## Known limitations

The exact Framework submodule checkout was unavailable in the task worktree,
so the full Framework integration and the Framework archive-to-source
extraction path could not be rerun. The independent security review recorded
this as partial coverage of a pre-existing integration evidence gap, not as a
new reportable finding. The local checks cannot independently prove a hosted
runner image, network condition, or cache state; the PR's hosted results were
directly observed in the verified delivery round.

## Remaining risks

The updater is deliberately fail closed if Framework declarations or mapped
Parent targets do not satisfy the bounded contract. The remaining risk is the
unobserved Framework-side archive extraction proof; no task-owned PR delivery
blocker remains from the observed GitHub and SonarQube results.

## Final diff and review status

The local final diff review found task-owned Parent changes only, with the
Framework source, MRTS, and Parent gitlink unchanged. The required local
validation and security-diff review passed as recorded above. PR #291 is open,
clean, mergeable, and ready for review; its verified delivery round passed the
applicable GitHub checks and SonarQube Cloud Quality Gate. No `master` merge
was performed.
