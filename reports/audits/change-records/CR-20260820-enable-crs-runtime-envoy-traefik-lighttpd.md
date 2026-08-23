# Change Record: enable CRS runtime for Envoy, Traefik, and Lighttpd

**Language:** English | [Deutsch](CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd` |
| Date (UTC) | 2026-08-20 |
| Base revision | `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Observed current `origin/master` | `4e8560fdc8a2b737fca598522f8748a4d73857be` |
| Parent → Framework pin | `c40e924ec5c341032908e0082feba1d37ed1dfda` |
| Framework → MRTS pin | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery status | Draft [PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309) exists for `agent/crs-runtime-envoy-traefik-lighttpd-master-20260820`. The branch was normally synchronized with current `origin/master` through merge commit `0ae1ce0590f18b20a39903f2ce877d0280a6e5bd`. At pre-remediation head `fe74cb02876e9de16eaafc7b590f36b46348044a`, SonarQube Cloud still identified one new code smell and 18 duplicated New-Code lines; the exact successor analysis remains pending. The master-derived Framework pin remains read-only and resolves to the recorded MRTS pin. No merge or auto-merge is authorized. |

The task worktree was created from the recorded task base and later normally
merged with separately recorded current `origin/master` revisions, most
recently `4e8560fdc8a2b737fca598522f8748a4d73857be`. Earlier hosted results
remain historical only; all required revalidation remains delivery-gated.

## Motivation and problem statement

The Parent repository must turn the Envoy, Traefik, and Lighttpd
`with-crs/no-mrts` cells from contract-only validation into real host-runtime
execution without modifying Framework, MRTS, their Gitlinks, dependencies, or
toolchains. The work must retain CRS provenance, No-MRTS evidence, request-to-
decision correlation, and fail-closed cleanup.

During the Lighttpd No-CRS fixture analysis, a P1 same-UID TOCTOU was found in
the former pattern that checked a fixture inode and later deleted the same
pathname. A same-UID process could replace that pathname between those steps.
The authorized remediation makes namespace lifetime, rather than a final
attacker-writable pathname deletion, the cleanup boundary.

## Acceptance criteria

- Envoy, Traefik, and Lighttpd each execute a real `with-crs/no-mrts` host
  path with an allowed control request, a CRS-blocked request, correlated
  evidence, No-MRTS proof, and cleanup evidence.
- The `with-crs/no-mrts` workflow has those three cells classified as
  `runtime`; the six Envoy/Traefik/Lighttpd MRTS cells remain
  `expected_unsupported`.
- Lighttpd No-CRS fixture creation and use occur in a capability-gated private
  namespace with private mount propagation and no unsafe pathname-cleanup
  fallback.
- Same-UID adversarial replacement, success, error, timeout, signal, helper
  failure, partial-initialization, capability-failure, and teardown behavior
  have focused regression coverage.
- Only Parent-authored files change. Framework and MRTS source, dependency
  manifests, lockfiles, and toolchain selections remain unchanged. The normal
  current-master merge retains its master-derived Parent → Framework Gitlink
  update without making it a task-authored Gitlink change.
- A separate task branch and PR receive exact-head local and hosted validation
  before any Ready-for-Review claim. No merge, auto-merge, or risk acceptance
  is part of this change.

## Implementation decision and rationale

The Parent owns the connector runtime implementations, lifecycle scripts,
normalization, tests, and task documentation. Framework and MRTS remain
read-only validation boundaries. The recorded Parent → Framework and Framework
→ MRTS pins are preserved.

### Technical decisions

The runtime work uses the repository's existing CRS acquisition and provenance
contract. It does not add a dependency, download an unpinned artifact, change a
lockfile, or upgrade a compiler, Go, Python, or system toolchain.

For Lighttpd's No-CRS fixture, trusted root-owned setup programs form the
boundary: `/usr/bin/unshare` starts the private namespace and
`/usr/bin/unshare --propagation private` explicitly makes propagation private;
fixed `/usr/bin/dash` and `/usr/bin/mount` then create a private
`nosuid,nodev,noexec` tmpfs; `/usr/bin/bwrap` exposes only minimal read-only
system/runtime binds and the exact task-owned smoke root as writable. The
unprivileged harness continues only after capability-set, `no_new_privs`,
mount, and fixed fixture-root identity checks.

The final namespace-state verifier checks capability sets, `no_new_privs`,
mount state, and fixed fixture-root `dev:ino` identity. The descriptor-I/O
cleanup command separately verifies the allowlisted leaf inventory, retains all
leaves, and never performs a pathname or descriptor-relative deletion. Private
tmpfs namespace teardown removes the fixture directory and its leaves.

The descriptor-backed fixture server now publishes each control artifact
through the available one-shot `write_text_fresh` API. Its final leaf is
created with `O_EXCL|O_NOFOLLOW`; it does not depend on the previously missing
atomic-write interface or on a temporary leaf that would require cleanup.

## 2026-08-21 follow-up: namespace gate, workflow overview, and Sonar issues

The hosted Lighttpd namespace integration remains deliberately fail-closed.
The `ubuntu-latest` runner does not provide the required unprivileged
user/mount/PID namespace combination, and the test therefore fails at its
explicit availability assertion rather than falling back to pathname cleanup.
There is no safe Parent-only workflow adjustment for that missing kernel
facility: `sudo`, a privileged container, a setcap helper, disabling the gate,
or a check-then-`rmdir` fallback would either execute mutable PR code with
privilege or weaken the P1 control. The smallest prerequisite is an isolated,
non-root self-hosted Linux runner with those namespaces enabled, trusted
root-owned setup binaries, no secrets, no Docker socket, no persistent host
access, and a dedicated label. The Draft PR remains blocked on that external
runner capability.

The CRS/no-MRTS workflow now writes a final `if: always()` connector overview.
It reports only fixed GitHub step outcomes for checkout, locked dependencies,
revision/cell verification, private roots, CRS preparation, the real runtime
target, and evidence publication. Each connector shows passed, failed,
skipped, and cancelled stages plus the first non-passing stage. A failed,
skipped, or cancelled runtime target is displayed as such and is never
promoted to a connector capability pass. The existing HAProxy raw-artifact
upload exclusion is shown separately as `skipped_by_security_policy`; it is
not hidden as a runtime success or failure. The summary writer rejects unknown
outcomes, requires `O_NOFOLLOW`, opens the runner-provided parent directory
once, and appends through that directory descriptor.

At PR head `6c1fe074b1d3027a00228b1517e29e08b064eca3`, the official
SonarQube Cloud issue API reported eleven open new issues, despite a passing
Quality Gate: five regex-style findings and one cognitive-complexity finding
in the Parent normalizer, plus four exception-assertion findings in a Lighttpd
contract test. This follow-up repairs each finding without `NOSONAR`, rule or
quality-gate changes, exclusions, issue acceptance, dependency changes, or
test weakening. The normalizer keeps its ASCII wire-evidence restriction while
using explicit ASCII regex semantics, and the complexity split preserves the
same fail-closed trace validation. The next exact-head SonarQube analysis must
still demonstrate zero new issues before the requirement is considered met.

## 2026-08-22 follow-up: master refresh, Traefik deduplication, and hosted boundary

The branch now includes the normal merge commit `101df216` of current
`origin/master` `423abcc130cf5d29ccf15dd7d82e4e7d89d495d3`. The resulting
Parent → Framework pin is `c40e924ec5c341032908e0082feba1d37ed1dfda`, and the
Framework → MRTS pin remains `615b13bacbd008562c17408246c41ab27dca3104`. This
is a master-derived revision update, not a task-authored Framework or MRTS
change; the stale local nested checkout is not staged or used as authority.

The official SonarQube Cloud duplication API attributed all 20 duplicated New
Code lines to two equivalent Traefik engine/host-start blocks. They now share
the `running_traefik_host` context manager. It retains the process ownership,
arguments, working directory, log descriptor lifetime, readiness diagnostics,
and outer cleanup behavior of both the CRS and non-CRS runtime paths. A direct
regression test verifies those lifecycle properties, while the existing CRS
run-ID request test continues to cover request correlation. The fresh
exact-head SonarQube analysis must report `0.0%` New Code duplication before
that metric is claimed as satisfied.

The required Lighttpd namespace integration remains an external hosted-runner
blocker, not a safe Parent-only workflow bug. Its real entry path requires an
unprivileged user/mount/PID namespace chain and rejects host-root and set-ID
callers. `sudo`, a privileged container, or a setcap helper would not preserve
that boundary. The smallest safe remedy remains an isolated non-root
self-hosted Linux runner with the required namespaces, fixed root-owned setup
binaries, no secrets, no Docker socket, and a dedicated label.

## 2026-08-23 follow-up: zero-new-code Sonar remediation

At exact predecessor PR head `fe74cb02876e9de16eaafc7b590f36b46348044a`, the
public SonarQube Cloud API reported one open New-Code issue,
`AaAqpBihH7VZS0qiY-cu` / `python:S8714`, at
`connectors/lighttpd/tests/test_no_crs_fixture_namespace.py:230`. It also
reported `new_duplicated_lines=18` and
`new_duplicated_lines_density=0.1573701696100717` (shown as 0.2%) from two
overlapping Envoy header-table blocks in
`connectors/envoy/ext_proc/internal/processor/processor_test.go`.

The Parent-only follow-up removes the unnecessary exception wrapper from the
Lighttpd required-identity contract, so missing or malformed required numeric
environment values fail naturally. The non-root, exact UID/GID, empty-group,
`NoNewPrivs`, and Docker-socket assertions remain unchanged. The Envoy test
now constructs the two authority/Host order variants from one helper while
retaining all hostile cases: both orderings, duplicate Host, and duplicate
authority. It does not suppress Sonar, alter a rule/profile/threshold, exclude
a path, accept an issue, change a dependency, or weaken a runtime or security
control.

Before delivery, the focused Lighttpd namespace-contract test passed with
seven contract tests and ten expected capability-gated integration skips;
Envoy `go test ./...` and `go vet ./...` passed with the existing Go 1.26.6
toolchain and a private task cache; Python compilation and `git diff --check`
passed. The exact successor PR-head SonarQube Cloud issue and duplication
readback remains the final acceptance evidence; no zero result is claimed here
before that analysis completes.

## Security impact

The affected boundary spans untrusted HTTP input, connector-to-ModSecurity
decision paths, CRS provenance, evidence paths, process lifecycle, mounts, and
temporary fixtures. The same-UID adversary model permits rename, replacement,
and recreation of the legacy fixture pathname.

The remediation removes the security-relevant check-then-`rmdir` operation
from the fixture lifecycle. It uses a private mount namespace, explicitly
private propagation, a non-attacker-writable fixture root, bounded trusted
setup programs, capability removal, and `no_new_privs`. Failure to obtain or
verify a required capability, namespace, mount, or isolation property is
fail-closed. There is no risk acceptance and no manual-cleanup instruction as
a substitute for the technical control.

## Changed files

Task-owned implementation and tests currently span the following Parent areas;
the final staged inventory remains subject to the mandatory final diff review:

- `ci/provisioning/components/prepare-runtime-components.py`,
  `ci/runtime/lifecycle/run-no-crs-baseline.sh`,
  `ci/runtime/lifecycle/run-remaining-connector-target.sh`,
  `ci/runtime/lifecycle/run-with-crs-no-mrts.sh`,
  `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`, and
  `ci/runtime/lifecycle/summarize-with-crs-no-mrts-workflow.py`;
- Envoy ext-proc runtime code, harness, and focused tests under
  `connectors/envoy/`;
- Traefik native middleware, runtime smoke, and focused tests under
  `connectors/traefik/`;
- Lighttpd module, lifecycle harness, trusted namespace runner,
  namespace/descriptor-I/O helpers, focused tests, and associated EN/DE
  documentation under `connectors/lighttpd/` and `docs/`;
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`, focused Parent test
  contracts under `tests/`, plus the repository `Makefile`;
- this English/German Change Record pair.

No Framework or MRTS source file, Gitlink, dependency manifest, lockfile, or
toolchain selection is included in the authorized change scope.

## Commands executed

This record directly observed its own documentation checks. The task evidence
also contains the following recorded local core validations; their exact
invocation text is retained with the task evidence and is not reconstructed
here from memory:

- `make check-bilingual-docs` was executed before and after the record-heading
  correction. The later execution no longer reported a Change Record structural
  error, but remained blocked by pre-existing missing Framework-submodule
  documentation targets. That external missing-target condition is not changed
  by this record.
- `git diff --check -- reports/audits/change-records/CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.md reports/audits/change-records/CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.de.md`
  was executed without diff-whitespace output.
- `rg '^## '` was used on both records to compare their top-level heading
  sequence.

## Tests and actual results

The Lighttpd trusted-namespace integration is locally capability-gated. The
observed non-root probe `unshare --user --map-root-user` failed with
`write /proc/self/uid_map: Operation not permitted`, so the full intended
non-root production entry path cannot be exercised in this environment. The
required behavior therefore has not been promoted to a locally verified
production-runtime result here.

| Check | Actual result recorded here |
| --- | --- |
| Change Record `git diff --check` | passed; no diff-whitespace output |
| Lighttpd focused contracts | passed: 50 tests in the combined focused run; namespace integration remains locally capability-gated |
| Workflow security tests | passed: 30 tests |
| C module build | passed with `-Wall`, `-Wextra`, and `-Werror` |
| Clang static analyzer | passed: 0 diagnostics |
| Envoy and Traefik Go validation | `go mod verify`, dependency listing, tests, vet, and `govulncheck` passed; no vulnerabilities found |
| Parent runtime tests | passed: 34 tests; task-local Btrfs directory-durability barriers were slow but completed, with no atomicity control removed |
| Focused CRS/no-MRTS normalizer regression | passed: 44 tests, including semantic Lighttpd `status=blocked` plus strict numeric HTTP-status validation |
| `test_collect` under the Framework override | passed: 42 tests; 3 Framework-gated skips |
| Python dependency validation | `pip check` passed |
| Shell/Python/YAML validation | shell syntax, Python compilation, YAML parsing, and diff checks passed |
| Cppcheck | existing style diagnostics outside changed hunks; no changed-hunk finding reported |
| Non-root user-namespace probe | blocked: `unshare --user --map-root-user` failed with `write /proc/self/uid_map: Operation not permitted` |

## Runtime evidence

Draft [PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309)
was most recently evaluated at hosted exact head `e432b1e748dc8f49b98ed1a29e8d7277a40763a5`. Envoy and Traefik completed their
runtime jobs successfully. Apache failed because same-step `GITHUB_ENV`
temporal semantics did not make the freshly acquired CRS roots available to
the later step; this change adds a separate preparation step for that handoff.
Lighttpd completed its lifecycle and the Curl metadata validation, but then
the Parent attestation tried to parse Lighttpd's semantic `status=blocked`
action label as an integer before considering the host's numeric
`http_status=403` and `visible_http_status=403`. The follow-up accepts that
documented semantic label only when at least one strict JSON-integer HTTP field
is present, in range, and consistent; malformed strings, booleans, floats,
missing numeric evidence, and conflicts fail closed. A task-private copy of
the uploaded evidence validated against the unchanged pinned Framework as
`CONTRACT_VALIDATED`. The preceding Curl correction accepts only the
corresponding `Trying`, `Established`, and `Connected` spellings with literal
`127.0.0.1`, valid source and target ports, exactly one marker of each kind,
and matching attempted/connected target ports. HAProxy was blocked before
runtime by the old read-only Framework ordering at
`bd69ee96e0e7082317d4afe1232bee625665eb9a`, which invoked
`verify_build_target` before `prepare_build_worktree`. The current Parent pin
is `89881a1b33219fc18df3cf2f15dda53261d13443`, which contains Framework PR
#102's ordering correction. A fresh exact-head HAProxy runtime validation
remains mandatory; no successful result is asserted here.

The required PR-triggered P1 namespace test failed closed because the hosted
environment did not provide the required user, mount, or PID namespace
capability. This is a failed validation, not a successful fallback. These
observations prevent a full-matrix or verified-PR claim. No future test result
is asserted and no raw CI log or trace artifact was exported.

This run is not final runtime evidence for all three promoted cells. Previous
hosted runs and their results are retained as historical context only and are
not reused for exact-head claims. The status-normalization follow-up has not
yet received a hosted exact-head run.

No final runtime evidence is asserted by this record. In particular, the
hosted validation for the latest exact task head is unsuccessful and no
successful SonarQube Cloud analysis or required-check result is asserted.
Preliminary connector work and static validation do not replace real
host-runtime evidence for the three promoted matrix cells.

## Checks not run and rationale

The following remain pending or unavailable: complete three-connector local
runtime validation in a non-root-capable namespace environment (the hosted
namespace test failed closed because the runner lacked the required
capability); full matrix
workflow validation; GitHub-hosted required checks; actionlint, zizmor, Ruff,
and Pyright were unavailable in the local environment; SonarQube Cloud; and
final PR exact-head verification. CodeQL, Secret Scanning, OSV, and zizmor
were observed only for the earlier PR head and are not reused as evidence for
the pending follow-up head.

## Known limitations

The observed non-root `unshare --user --map-root-user` probe fails with
`write /proc/self/uid_map: Operation not permitted`, preventing exercise of the
capability-gated Lighttpd namespace entry path as its intended non-root caller.
The hosted namespace test has now failed closed because the runner did not
provide the required namespace capability.
This is an environment blocker for that integration test, not evidence that the
control is unnecessary or that a weaker cleanup path is permitted. The
bilingual documentation target still requires the exact pinned Framework
checkout for its repository-native validation. The task branch is now normally
synchronized with observed `origin/master`; the PR remains Draft and delivery
requires renewed exact-head validation. No Framework, MRTS, or task-created
Gitlink change is part of this work.

## Remaining risks

Until the required non-root namespace integration and adversarial lifecycle
tests pass, the P1 remediation is not eligible for a verified-PR claim. The
implementation must continue to fail closed rather than fall back to path-based
deletion. Runtime promotion also remains contingent on real CRS rule evidence,
No-MRTS proof, cleanup evidence, exact-head hosted checks, and the required
quality/security gates. The updated Framework revision removes the previously
known HAProxy ordering failure, but a fresh exact-head HAProxy run is still
required before it can cease to be a matrix blocker.

## Final diff and review status

Status: in progress; Draft PR #309 exists and exact-head hosted validation is
pending. This record documents an authorized Parent-only implementation effort
and its present blockers. It does not claim Ready-for-Review, hosted-check
success, merge, CI success, SonarQube success, a complete matrix, or risk
acceptance.

## 2026-08-21 exact-head remediation follow-up

The current Parent `origin/master` is
`c2e2c6a77edd0f1ccc3d41fc4e133974a630e518`, which records Framework
`798bff0c921ab8c7f10b2ca949304d58e7f205a2` and MRTS
`615b13bacbd008562c17408246c41ab27dca3104`. The task branch was normally
merged with that Parent master; this is a base synchronization and creates no
task-owned Gitlink difference.

The first exact-head run after that synchronization failed every
`with-crs/no-mrts` connector before host start because the workflow still
compared the checked-out Framework against the former `89881a…` pin. The
workflow contract and its regression test now use the Parent-recorded
`798bff…` revision. This is a consistency correction, not a Framework source
change.

SonarQube Cloud also identified two `pythonsecurity:S8707` findings in the
new connector-summary helper: a CLI-provided summary filename could reach a
filesystem sink. The helper no longer accepts a summary-file CLI argument. It
now accepts only the runner-provided `GITHUB_STEP_SUMMARY`, requires it to be
one `step_summary_*` regular file below the runner-owned
`RUNNER_TEMP/_runner_file_commands` directory, traverses directories by
non-symlink descriptor, and verifies ownership, non-writable directory/file
modes, and link count before appending. Missing capabilities, unsafe paths,
symlinks, missing files, or incorrect ownership fail closed. The added
regression test proves the legitimate runner file works while outside,
traversal, and symlink targets are rejected.

Focused post-fix validation passed: 49 CRS/no-MRTS runtime-contract tests,
30 CI-workflow tests, the 124-test CI-security-contract suite with 5 expected
environment-gated skips, actionlint, offline zizmor, bilingual documentation,
Python syntax compilation, and `git diff --check`. New exact-head hosted
runtime and SonarQube Cloud evidence is still required; this record does not
claim a zero-issue Sonar result or successful runtime cells yet.

The first SonarQube Cloud analysis for exact head `263f8806…` passed its
Quality Gate and closed the two security findings, but its official PR issue
query still returned one task-owned `python:S1192` code smell for the repeated
unsafe-path error literal. The literal is now a module constant, preserving
the fail-closed error semantics without a suppression. A new exact-head
analysis must prove the user-required zero-new-issue result.

## 2026-08-22 exact-head workflow revision correction

The fresh PR-head `93a007f7b858a09c5b527b5db4084e93add5da7b` SonarQube Cloud
analysis reports `0.0%` New Code duplication and zero duplicated lines. The
fresh runtime workflow `32578172744` nevertheless failed all five matrix jobs
before any connector host started. Every job failed at `Verify pinned Parent,
Framework, and MRTS revisions`: the normal master merge changed the Parent →
Framework Gitlink to `c40e924ec5c341032908e0082feba1d37ed1dfda`, while this
workflow and its contract test still expected the former
`798bff0c921ab8c7f10b2ca949304d58e7f205a2`; MRTS remains
`615b13bacbd008562c17408246c41ab27dca3104`.

The correction updates only that expected Framework identity in the workflow
and synchronized contract test. It retains the exact immutable Parent,
Framework, and MRTS comparison; it neither suppresses the gate nor permits
runtime execution on a mismatched checkout. Artifact-upload failures in Envoy,
Traefik, and Lighttpd were secondary to the skipped runtime and are not treated
as a distinct runtime failure. Fresh exact-head workflow and Sonar evidence
remain required after this correction.

## 2026-08-22 follow-up: trusted namespace dispatcher prerequisite

The earlier self-hosted-only prerequisite is superseded by a separately
reviewed Bootstrap Draft PR #320. It adds a `workflow_dispatch`-only workflow
to protected `master`; it is not part of this PR's `pull_request` workflow and
does not add `sudo`, AppArmor setup, a privileged container, or a fallback to
PR #309.

After PR #320 is independently reviewed and merged, the configured repository
owner must manually dispatch its trusted workflow from `master` with PR #309's
open canonical number or current full lowercase head SHA. The fixed dispatcher
first performs only root-owned Ubuntu-24.04 system setup, then uses the public
GitHub API to bind the input to exactly one open canonical master PR and its
exact head SHA. It checks out only that SHA without persistent credentials or
hooks, removes `.git`, and runs this PR's test source only as fresh `ns-test`
with empty supplemental groups and capability sets, `NoNewPrivs`, `env -i`, a
private temporary root, Docker-socket denial, and fail-closed user/mount/PID
namespace plus Bubblewrap probes.

PR #309 contains only the matching unprivileged test assertions for that outer
identity and temporary root. It remains Draft: no namespace runtime success,
quality result, Ready-for-Review state, or merge is claimed until the
protected-master workflow has produced an exact-head successful manual run.

## 2026-08-22 refresh: current master and Envoy authority coherence

A clean task worktree normally merged current `origin/master`
`4e8560fdc8a2b737fca598522f8748a4d73857be` through merge commit
`0ae1ce0590f18b20a39903f2ce877d0280a6e5bd`. The Parent → Framework pin remains
`c40e924ec5c341032908e0082feba1d37ed1dfda`, and the Framework → MRTS pin remains
`615b13bacbd008562c17408246c41ab27dca3104`; neither nested repository has a
task-authored source or Gitlink change.

The protected-master trusted namespace dispatcher described above is now part
of current master. It must still be manually dispatched against PR #309's
exact final head; the ordinary PR workflow remains unprivileged and this Draft
does not claim a namespace-runtime pass before that manual run succeeds.

Focused review found that the Envoy request-metadata parser previously retained
`:authority` and an ordinary `Host` header independently. It now rejects a
mismatch or duplicate authority/Host representation before opening the
transaction. One canonical case-insensitive matching pair remains accepted and
uses the original `:authority` value. Focused Go tests cover both header orders,
duplicate representations, and the legitimate matching control.
