# Change Record: CR-20261102-master-reconcile

**Language:** English | [Deutsch](CR-20261102-master-reconcile.de.md)

Reviewed partial change with explicitly retained evidence gaps.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261102-master-reconcile |
| Date (UTC) | 2026-11-02 |
| Base revision | `430d3194fa04ca4aafcdaef6aeb256d21dc18f0c` |

## Motivation and problem statement

Reconcile stale Framework integration identity, Apache documentation and inherited policy metadata, and make current evidence gaps reviewable. The source review separates actual behavior from target policies and historical runtime receipts.

## Acceptance criteria

Use one reviewed, already integrated Framework commit consistently in gitlink, lock and fixed workflow projections; correct Apache EN/DE behavior claims; validate reviewed inheritance updates; publish actual coverage, bounded dependency inventory and unapplied rules proposals. The PR440 repair adopts an actual integrated Framework revision after the separate Framework/MRTS merges; new-head hosted CI must qualify the resulting pair.

## Implementation decision and rationale

The original selection was Framework91145b7. The PR440 CI repair selects integrated Framework03fa02bacfc327863d91723fdc77a4888a33f0a8, including separately merged155/159/162/158/163 and MRTS75394f9a687ca2f09fd7623b23ac527bba10d7d9 with mergedMRTS5. Parent master1a1023b92eb30ef73546cd2a2c3e84b39d34a153 is incorporated regularly into the PR branch. Its erroneous pre-squash Framework158 heada26b028104b28ddd980290b5af7b3fb195c43f9a fails the unchanged ancestry guard; select the integrated identity instead. Framework164 at1b0885 is excluded because NGINX1.31.8 conflicts with the independently checked1.31.6 handoff. Use sync-framework-component-versions.py with its fixed target registry, not blanket string replacement. Parent Python3.15.1 and Framework Python3.15.2 keep their independently pinned interpreter contracts. Preserve source policy bodies after substantive inheritance review; refresh only reviewed digests/templates and update the host-context guide. The separate maintenance integrations are consumed without reimplementing their source changes;157 remains closed unmerged.

## Changed files

Framework gitlink, ci/tooling/project-versions.lock.json and the generator-owned Framework action/workflow references; docs/architecture.md and docs/connectors/apache.md with German companions; .codex/context/security-runtime-preflight.md, inheritance catalog/templates; reports/audits/master-reconcile-20261102/* and this Change Record pair. No connector runtime product source changed.

## Commands executed

RTK-wrapped native operations: sync-framework-component-versions.py --sync/--check with exact selected SHA and a git-extracted common.sh below RUNNER_TEMP; --check returned no changes. Explicit on-demand test_update_framework_versions and test_project_toolchain_pins:55 tests passed. make check-bilingual-docs check-doc-links passed before final report additions; final checks are recorded in the closeout. Parent validate-codex-inheritance.py --check --repository parent passed. For the new selected revision, the native projection generator check reports no changes and candidate verification passes; check-python-version-contract passes (Python3.15.1,53 jobs),94 existing pin/toolchain/projection/candidate regressions pass (133.158s), and the updated Parent inheritance validator passes. All active hosted checks and SonarCloud for selected Framework03fa02b passed; new Parent-head hosted CI is pending at this update. Actual measured counts/provenance are in coverage-summary.json; no overall full-Python PASS is claimed.

## Security impact

Retain every existing admission, identity, socket, artifact, compiler and CI control. The Sonar exception changes no general repository rule or GitHub workflow behavior. Rule JSONs are proposals only. Source/advisory assessment records unresolved NGINX/Envoy/Python update applicability and incomplete native transitive linkage rather than declaring them clean. No credential values or unrestricted logs are recorded.

## Runtime evidence

No fresh connector-host or H2/H3 campaign. Common/gcov and Go coverage establish selected test execution only. The host-context guide identifies integrated preflight implementation and real same-context requirements; dated2026-11-01 receipts remain historical.

## Known limitations

The user selected targeted coverage measurement with documented limitations.
The116 named Python tests plus actual Go/Common measurements satisfy that
measurement scope; completing or rerunning the full977-execution specialist
assessment is not required. Its historical failure and the independent broker,
runtime and dependency findings remain documented; CI gates are unchanged.

Hosted Parent440 CI at38ebc633 rejects the selected91145 Framework common.sh
binding before selected execution:156 changed the Python patch pin without
refreshing that digest. All28 inspected individual failed jobs share this
admission cause; the five-cell aggregate additionally fails after incomplete
failure-receipt retention. The exact-head JSON and EN/DE closeout preserve
diagnostics and source hashes. Framework159 regenerated the binding through
the existing tool and is now separately merged, included in selected03fa02b; no
guard is weakened. The reported master run41470651827/job125363368715 instead
correctly rejects the pre-squash158 identity. The PR440 repair adopts integrated
03fa02b and must qualify its new committed head; historical snapshots remain unchanged.

Full Traefik auth preparation still fails closed on a sealed profile;10/19 historical registry repository objects drifted. The full Python specialist measurement failed after 56 completed cases on the protected caller contract; timing was not reached. The current thin Parent wrapper is incompatible with the immutable protected broker's historical inline admission contract. Current integrated-child inheritance qualification must be assessed separately from the historical failed check.

## Remaining risks

Current-host qualification, exhaustive native/container SBOM and distro-patch advisory analysis, reviewed runtime tuple builds, classic branch protection visibility (HTTP 403), and new-head hosted CI qualification remain open. Existing green broad CI is not used to close these gaps.

## Checks not run and rationale

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt. No local Sonar repair or replacement mandatory gate. Sonar analyzer import, full H2/H3 acceptance and a fresh final merged-pair host run were not performed; the historical measurements do not qualify the newly selected pair. Administrative proposals were not applied because separate approval is required.

## Final diff and review status

Task-owned changes are isolated from existing checkouts/worktrees. ParentPR440 remains unmerged. Framework159 and minimal test-only MRTS5 were delivered separately and subsequently integrated by other work; their original delivery identities are retained in the closeout. This task performs no PR merge, force-push, direct master/main push or protection change; the regular master-to-PR-branch integration preserves history. Overall outcome remains partial until recorded mandatory gaps are resolved.
