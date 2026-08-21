# Change Record: enable CRS runtime for Envoy, Traefik, and Lighttpd

**Language:** English | [Deutsch](CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd` |
| Date (UTC) | 2026-08-20 |
| Base revision | `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Observed current `origin/master` | `aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf` |
| Parent → Framework pin | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| Framework → MRTS pin | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery status | Draft [PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309) exists for `agent/crs-runtime-envoy-traefik-lighttpd-master-20260820`. The last hosted exact head is `75c3be54a4855e0c34ffeb30d0895c0fd840f313`; hosted run `32433856340` is not successful, and this follow-up awaits a fresh exact-head run. No merge or auto-merge is authorized. |

The task worktree was created from the recorded task base. `origin/master`
subsequently advanced to the separately recorded current value. This record
does not claim that the later base has been incorporated; that decision and any
required revalidation remain delivery-gated.

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
- Only Parent files change. Framework, MRTS, Gitlinks, dependency manifests,
  lockfiles, and toolchain selections remain unchanged.
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
  `ci/runtime/lifecycle/run-with-crs-no-mrts.sh`, and
  `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`;
- Envoy ext-proc runtime code, harness, and focused tests under
  `connectors/envoy/`;
- Traefik native middleware, runtime smoke, and focused tests under
  `connectors/traefik/`;
- Lighttpd module, lifecycle harness, trusted namespace runner,
  namespace/descriptor-I/O helpers, focused tests, and associated EN/DE
  documentation under `connectors/lighttpd/` and `docs/`;
- focused Parent test contracts under `tests/`, plus the repository `Makefile`;
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
| `test_collect` under the Framework override | passed: 42 tests; 3 Framework-gated skips |
| Python dependency validation | `pip check` passed |
| Shell/Python/YAML validation | shell syntax, Python compilation, YAML parsing, and diff checks passed |
| Cppcheck | existing style diagnostics outside changed hunks; no changed-hunk finding reported |
| Non-root user-namespace probe | blocked: `unshare --user --map-root-user` failed with `write /proc/self/uid_map: Operation not permitted` |

## Runtime evidence

Draft [PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309)
was evaluated at pushed exact head
`75c3be54a4855e0c34ffeb30d0895c0fd840f313` by hosted run `32433856340`.
Envoy and Traefik completed their runtime jobs successfully. Lighttpd reached
and completed its lifecycle, but the post-run normalizer rejected Curl 8.18's
`Connected` spelling, so its promoted cell is not verified. Apache lost its
freshly acquired CRS roots across the runtime snapshot. HAProxy was blocked
before runtime by the read-only Framework ordering, which invokes
`verify_build_target` before `prepare_build_worktree`. These failures prevent a
full-matrix or verified-PR claim.

The follow-up Parent fixes are narrowly scoped: accept the exact
documented Curl spelling; forward Apache's fresh CRS roots through
`GITHUB_ENV` with an explicit final environment override; and require the
PR-triggered Lighttpd namespace suite to fail when user, mount, or PID
namespace support is unavailable. The suite checks out and tests the exact PR
head. The local suite remains capability-gated and skips its integration cases
because the nested kernel rejects the user namespace with `EPERM`; hosted
evidence for this required suite is pending. No raw CI log or trace artifact
export was performed.

The failed exact-head Lighttpd job reached CRS acquisition and the pinned
`1.4.85` host build before its private Curl trace parser rejected an otherwise
unclassified structural row. The bounded follow-up accepts only Curl's
documented `<= Recv header, <decimal> bytes (0x<hex>)` transition as an
alternative request-completion boundary. It still rejects received data,
generic diagnostics, malformed records, and arbitrary star rows; the outgoing
offset/length checks and independent raw response-header validation remain
mandatory. This change is pending fresh exact-head runtime evidence.

This run is not final runtime evidence for all three promoted cells. Previous
hosted runs and their results are retained as historical context only and are
not reused for exact-head claims.

No final runtime evidence is asserted by this record. In particular, the
follow-up exact task head has no completed hosted workflow, SonarQube Cloud
analysis, or required-check result yet. Preliminary connector work and static
validation do not replace real host-runtime evidence for the three promoted
matrix cells.

## Checks not run and rationale

The following remain pending or unavailable: complete three-connector local
runtime validation in a non-root-capable namespace environment (the real
non-root namespace integration is pending on a hosted runner); full matrix
workflow validation; GitHub-hosted required checks; actionlint, zizmor, Ruff,
and Pyright were unavailable in the local environment; SonarQube Cloud; and
final PR exact-head verification. CodeQL, Secret Scanning, OSV, and zizmor
were observed only for the earlier PR head and are not reused as evidence for
the pending follow-up head.

## Known limitations

The observed non-root `unshare --user --map-root-user` probe fails with
`write /proc/self/uid_map: Operation not permitted`, preventing exercise of the
capability-gated Lighttpd namespace entry path as its intended non-root caller.
The real non-root namespace integration remains pending on a hosted runner.
This is an environment blocker for that integration test, not evidence that the
control is unnecessary or that a weaker cleanup path is permitted. The
bilingual documentation target is also blocked by the uninitialized Framework
Gitlink. The current task base also differs from observed `origin/master`; the
PR remains Draft and delivery requires renewed exact-head validation according
to the current base strategy. No Framework, MRTS, or Gitlink change is part of
this work.

## Remaining risks

Until the required non-root namespace integration and adversarial lifecycle
tests pass, the P1 remediation is not eligible for a verified-PR claim. The
implementation must continue to fail closed rather than fall back to path-based
deletion. Runtime promotion also remains contingent on real CRS rule evidence,
No-MRTS proof, cleanup evidence, exact-head hosted checks, and the required
quality/security gates. The HAProxy Framework ordering dependency currently
blocks full-matrix completion.

## Final diff and review status

Status: in progress; Draft PR #309 exists and exact-head hosted validation is
pending. This record documents an authorized Parent-only implementation effort
and its present blockers. It does not claim Ready-for-Review, hosted-check
success, merge, CI success, SonarQube success, a complete matrix, or risk
acceptance.
