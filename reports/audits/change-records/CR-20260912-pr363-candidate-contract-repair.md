# Change Record: PR #363 candidate-contract and latest-Go repair

**Language:** English | [Deutsch](CR-20260912-pr363-candidate-contract-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260912-pr363-candidate-contract-repair |
| Date (UTC) | 2026-09-12 |
| Base revision | 2eb08da41a224c52c57856b355a21fb4a22f693a |
| Delivery status | Parent-only correction is delivered to Draft PR #366 from task branch agent/pr363-candidate-contract-repair. This record does not assert a merge or master write and does not treat pending hosted checks as passed. |

## Motivation and problem statement

The user asked for the reviewed PR #363 correction in an own worktree and PR because other work is blocked. The earlier explicit requirement remains that the Go updater and verification always use the newest Go version, and that the remaining contracts are adapted to the new structure.

PR #363 advances the Framework gitlink but leaves static Parent CRS/no-MRTS SHA consumers and separately maintained unprotected NGINX handoff projections stale. The generic Framework synchronizer deliberately does not own NGINX. Independently, CodeQL accepted only the valid committed .go-version selector even though the bounded updater can resolve the latest stable Go release.

## Scope and non-goals

This Parent-only record covers the Framework gitlink candidate d4f7b69dc264852eac74e1439c0887fcb9fbe372, Parent SHA/fixture and unprotected NGINX contract alignment, a read-only candidate verifier, dynamic trusted-base Go resolution for CodeQL, focused tests, paired documentation, and generated compiler guides.

It does not modify Framework or MRTS source, grant generic NGINX ownership to sync-framework-component-versions.py, alter the independently pinned protected NGINX broker chain, install a Go toolchain, change workflow permissions or action pins, modify PR #363, or authorize a merge or master write.

## Implementation decision and rationale

A new bounded read-only verifier parses candidate Framework common.sh strictly as data. Candidate validation and the publisher both require every Parent CRS/no-MRTS SHA consumer and the test fixture to equal the candidate SHA, and every unprotected NGINX handoff projection to equal the canonical candidate tuple. It also requires `NGINX_REQUIRE_PINNED_PROVENANCE: "1"` in both unprotected NGINX workflows and rejects every candidate attempt to assign that Parent-owned policy. The protected NGINX broker remains deliberately outside this check.

The generic synchronizer continues to update only its registered Envoy and HAProxy projections. The separately owned Parent NGINX tuple is manually aligned to Framework d4f release-1.31.5. The NGINX body-buffer fixture follows the same unprotected exact-head release tuple.

For CodeQL, the trusted-base job runs scripts/update-go-version.py --check --json, validates strict numeric versions, monotonicity, update_available, and status, and publishes only latest_version. Envoy and Traefik setup-go steps consume that trusted output. The committed selector remains a trusted lower-bound input; prereleases, malformed reports, downgrades, and inconsistent reports fail closed.

The initial exact PR #366 SonarCloud analysis found verifier quality findings. The verifier now validates the checksum separately, compares every canonical tuple field without a whole-dictionary condition, and names the four repeated Parent paths. The release-tag grammar remains ASCII-only while using the concise digit class. A subsequent focused review found that an indented duplicate, declaration, append, unset, or parameter-expansion assignment could evade the former line matcher; the data-only parser now requires exactly one unindented plain assignment for each candidate tuple field and rejects any candidate mutation of the Parent-owned provenance flag. New negative controls cover those forms, malformed checksums, noncanonical tuples, and drift of either Parent policy projection before publication.

## Security impact

The change strengthens CI provenance and release freshness without weakening validation, permissions, immutable action pins, bounded updater transport, or protected NGINX broker provenance. It adds no generic NGINX writer. The verified candidate-contract gap could otherwise let a sourced candidate turn off the Parent full-smoke native-artifact provenance guard; it does not demonstrate unpinned archive acquisition or a protected-broker bypass.

## Compatibility impact

The selected Framework handoff uses NGINX release-1.31.5 with SHA-256 e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279, Envoy 1.39.1, and HAProxy 3.2.23. The live bounded Go updater reported current_version=latest_version=1.27.1.

## Changed files and documentation

The scoped change includes:
- update-submodules, CodeQL, CRS/no-MRTS, full-smoke, exact-head, and CI-security workflow contracts;
- the new ci/tools/verify-framework-candidate-contract.py verifier;
- Parent NGINX preparation, readiness, lifecycle, and body-buffer fixture contracts;
- Envoy and HAProxy component projections and their focused tests;
- Go version contract checker and focused tests;
- generated English/German compiler guides and paired variable and CI-security documentation;
- this English/German Change Record pair and both Change-Record indexes.

The full final file list is verified from the scoped task diff before delivery.

## Acceptance criteria

- Matching Framework candidate SHA, unprotected NGINX tuple, and Parent-owned provenance policy pass without Parent writes.
- Stale workflow SHA, fixture SHA, malformed or alternate candidate assignment syntax, Parent-owned policy mutation, and representative unprotected NGINX or policy drift fail closed before publication.
- Generic synchronization remains NGINX-unowned and protected broker pins remain unchanged.
- Trusted CodeQL uses only the bounded latest stable Go resolver output, rejects incoherent reports, and retains pinned trusted-base and setup-go controls.
- English/German documentation and generated guides match the implementation.

## Commands executed

| Check | Actual result |
| --- | --- |
| Focused candidate, updater, Go, workflow, and NGINX evidence suite | Passed: 40 tests. |
| Broader CI-security, NGINX, cache, snapshot, evidence, and presentation suite | Passed: 226 tests; 27 expected Framework-dependent skips before the task gitlink commit. |
| Exact-gitlink Framework APR/protected-NGINX snapshot suite | Passed: 38 tests using the clean reviewed Framework checkout at the committed gitlink. |
| Additional candidate-verifier and executable Go-resolver controls | Passed: 16 tests. |
| Focused post-review candidate/workflow controls | Passed: 66 tests. |
| Native-override provenance guard control | Passed: 1 test; a native NGINX override is blocked while the Parent policy is `1`. |
| make check-ci-security-contract | Passed: 138 tests with 5 expected unavailable namespace/identity skips after the verifier and provenance-policy remediation; validated actionlint, zizmor, and gitleaks tool locks. |
| actionlint for every changed workflow | Passed with no output. |
| zizmor --offline .github/workflows | Passed: no findings; 95 existing repository suppressions reported. |
| Focused independent post-patch security review | Passed after remediation: it reproduced the alternate-assignment and Parent-owned provenance-policy gaps, and the verifier now rejects both without sourcing candidate data. |
| check-go-version-contract.py --json | Passed with version 1.27.1 and no violations. |
| scripts/update-go-version.py --check --json | Passed with current_version=latest_version=1.27.1. |
| make check-compiler-guides | Passed: 22 tests. |
| git diff --check and Python compilation of changed Python paths | Passed. |
| make check-bilingual-docs | Blocked only by pre-existing missing links into the intentionally uninitialized task Framework submodule; no task-specific pair failure was reported. A root-checkout retry was interrupted after repeated no-output polling and is not asserted as passed. |

## Runtime evidence

This static source record contains no connector runtime or matrix result. The
initial exact PR head's SonarCloud Quality Gate is observed as failed and is
not treated as a passing control; the follow-up exact-head readback is pending.
Local contract evidence does not substitute for hosted runtime evidence.

## Known limitations

Framework-dependent tests must be rerun after the task commit records the
exact gitlink and a clean read-only Framework checkout is supplied. The local
Python environment is suitable for focused tests but is not a substitute for
the exact hosted workflow environment.

## Remaining risks

The remaining risk is hosted and runtime evidence, not a reason to alter
protected-broker ownership or claim a merge. The task worktree and remote
branch must be retained while the resulting Draft PR remains open.

## Checks not run and rationale

No final fully passing hosted GitHub Actions, SonarQube, connector build,
runtime matrix, scheduled updater execution, PR #363 mutation, or merge result
is claimed. The initial exact PR head had a SonarCloud reliability-gate failure;
the follow-up head requires external-runner readback. These checks therefore
are not represented as final passing controls.

## Findings and residual risk

FND-PARENT-1086 tracks the candidate-contract release blocker, including the Parent-owned full-smoke provenance-policy guard; FND-PARENT-1087 tracks dynamic latest-Go CodeQL freshness; and FND-SONAR-0085 tracks the new exact-PR-head verifier Quality-Gate findings. They remain in_progress until exact task-PR-head and applicable hosted controls are observed. FND-PARENT-1085 remains a separate fixed earlier cross-series grammar defect.

## Final diff and review status

The scoped diff, explicit staging list, worktree boundary, gitlink SHA, static
tests, actionlint, and an independent post-patch security review are complete.
The SonarCloud follow-up exact-head result remains required before the PR is
considered fully verified.
