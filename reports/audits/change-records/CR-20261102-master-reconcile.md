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

Use one reviewed, already integrated Framework commit consistently in gitlink, lock and fixed workflow projections; correct Apache EN/DE behavior claims; validate reviewed inheritance updates; publish actual coverage, bounded dependency inventory and unapplied rules proposals. Final adoption of newly repaired Framework code requires its separately authorized merge and a subsequent exact merge-SHA pin.

## Implementation decision and rationale

Select Framework 91145b7ba721bdec4e89af754cf40bf496fd2a08, including merged TLS-floor#154 and Python-patch#156. Use sync-framework-component-versions.py with its fixed target registry, not blanket string replacement. Parent Python 3.15.1 remains independent of Framework 3.14.10. Preserve source policy bodies after substantive inheritance review; refresh only reviewed digests/templates and update the host-context guide. Existing maintenance#155/#157/#158 remains separately owned.

## Changed files

Framework gitlink, ci/tooling/project-versions.lock.json and the generator-owned Framework action/workflow references; docs/architecture.md and docs/connectors/apache.md with German companions; .codex/context/security-runtime-preflight.md, inheritance catalog/templates; reports/audits/master-reconcile-20261102/* and this Change Record pair. No connector runtime product source changed.

## Commands executed

RTK-wrapped native operations: sync-framework-component-versions.py --sync/--check with exact selected SHA and a git-extracted common.sh below RUNNER_TEMP; --check returned no changes. Explicit on-demand test_update_framework_versions and test_project_toolchain_pins:55 tests passed. make check-bilingual-docs check-doc-links passed before final report additions; final checks are recorded in the closeout. Parent validate-codex-inheritance.py --check --repository parent passed. Actual measured counts/provenance are in coverage-summary.json; no overall full-Python PASS is claimed.

## Security impact

Retain every existing admission, identity, socket, artifact, compiler and CI control. The Sonar exception changes no general repository rule or GitHub workflow behavior. Rule JSONs are proposals only. Source/advisory assessment records unresolved NGINX/Envoy/Python update applicability and incomplete native transitive linkage rather than declaring them clean. No credential values or unrestricted logs are recorded.

## Runtime evidence

No fresh connector-host or H2/H3 campaign. Common/gcov and Go coverage establish selected test execution only. The host-context guide identifies integrated preflight implementation and real same-context requirements; dated2026-11-01 receipts remain historical.

## Known limitations

Hosted Parent440 CI at38ebc633 rejects the selected91145 Framework common.sh
binding before selected execution:156 changed the Python patch pin without
refreshing that digest. All28 inspected individual failed jobs share this
admission cause; the five-cell aggregate additionally fails after incomplete
failure-receipt retention. The exact-head JSON and EN/DE closeout preserve
diagnostics and source hashes. Framework159 regenerates the binding through
the existing tool; no guard is weakened. After authorized Framework integration,
pin its actual merge commit and qualify the final committed pair.

Full Traefik auth preparation still fails closed on a sealed profile;10/19 historical registry repository objects drifted. The full Python specialist measurement failed after 56 completed cases on the protected caller contract; timing was not reached. The current thin Parent wrapper is incompatible with the immutable protected broker's historical inline admission contract. Native full inheritance against the currently pinned nested Framework/MRTS remains pending.

## Remaining risks

Current-host qualification, exhaustive native/container SBOM and distro-patch advisory analysis, reviewed runtime tuple builds, classic branch protection visibility (HTTP 403), and final repaired-Framework merge/pin remain open. Existing green broad CI is not used to close these gaps.

## Checks not run and rationale

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt. No local Sonar repair or replacement mandatory gate. Sonar analyzer import, full H2/H3 acceptance and a fresh final merged-pair host run were not performed; that pair does not yet exist. Administrative proposals were not applied because separate approval is required.

## Final diff and review status

Task-owned changes are isolated from existing checkouts/worktrees. Framework and Parent delivery remain separate Draft PRs, with MRTS minimal test-only DraftPR#5 independently approved and delivered at bf756a403ead39863cc15a81b5608e2b6062435d. No merge, force-push, direct master/main push or protection change is authorized or performed. Overall outcome remains partial until recorded mandatory gaps are resolved.
