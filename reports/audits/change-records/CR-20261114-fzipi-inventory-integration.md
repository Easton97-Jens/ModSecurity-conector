# Change Record: CR-20261114-fzipi-inventory-integration

**Language:** English | [Deutsch](CR-20261114-fzipi-inventory-integration.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261114-fzipi-inventory-integration |
| Date (UTC) | 2026-11-14 |
| Base revision | `80334858a1a1e1ad1ff65e647716584a18cf3e9c` |

## Motivation and problem statement

Parent `80334858a1a1e1ad1ff65e647716584a18cf3e9c` selected Framework `3ff8b75c9f4d2cb3614a4dcb7afd2e5360e074d8`; its inventory rejected reviewed test content before execution because seven schema-5 digest bindings still described older bytes. The necessary second pin integration selects merged Framework master `2cc331d8bc4c86592afd7219ddeaba1e60dc0ced` from [Framework PR 172](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/172).

## Acceptance criteria

Integrate the verified Framework inventory repair without changing product behavior, test source content, inventory membership or validation strength. Preserve every other component/tool/runtime version and MRTS. New-pin Parent checks and required CI must pass before any authorized Parent master integration; prior-head evidence is not transferred.

## Implementation decision and rationale

The existing native schema-5 updater refreshed exactly seven hash slots: two Envoy tests and one each for Traefik, Apache lifecycle, HAProxy binding, Runtime event sink and NGINX body-buffer fixture. All 529 bound Framework source files and all other inventory data remain byte-for-byte/semantically unchanged as recorded by the Framework comparison. Select the actual squash master rather than its distinct reviewed PR head `f2a44adbcaa9fee093093b21186e7e305b78a02c`.

## Changed files

The coordinator owns the Parent component lock, 22 workflow projections and Framework gitlink update from the previous pin to the selected master. This new EN/DE Change Record pair documents the combined pin update. Product source, Framework test implementations and MRTS contents remain unchanged.

## Commands executed

The native Parent scaffold was executed successfully through RTK with explicit Parent/Framework context and arguments `create --name fzipi-inventory-integration --base-revision 80334858a1a1e1ad1ff65e647716584a18cf3e9c --date 2026-11-14`. The observed Framework entry was `rtk bypass python3 -B -`, which spawned explicit-context children: native updater check exit 1 before / 0 after, full inventory verifier exit 2 before / 0 after, updater apply exit 0, six maintenance regressions PASS and Framework documentation PASS. Exact child argv and context are documented in the [Framework record](https://github.com/Easton97-Jens/ModSecurity-test-Framework/blob/2cc331d8bc4c86592afd7219ddeaba1e60dc0ced/reports/audits/change-records/20261114-01-fzipi-inventory-bindings.md); they are not re-labelled as direct RTK child invocations. The Parent orchestration through `rtk bypass python3 -` also launched the configured Framework-Python child commands through RTK. Native candidate verification before/after synchronization, synchronizer `--sync`/`--check`, and `--verify-primary --base 80334858a1a1e1ad1ff65e647716584a18cf3e9c` passed. The canonical inventory check and `modsecurity_connector_ci.lib.active_test_inventory --check` passed with explicit Parent/Framework context and profile `h1`. An initial exit 2 for a missing external output directory was a setup failure; after creating it, complete admission passed with 100 active cases at a limit of 100. The three selected Runtime event-sink, host-action and HAProxy regression modules passed 26 methods in 6.678 seconds. Native EN/DE/repository-path/link checks also passed.

## Security impact

The repair restores reviewed-source provenance; it does not relax digest, path, symlink, schema, selection or case-budget controls. The earlier exact operator approval `f94` is not transferred to the new gitlink. A new exact operator plan/admission may be required; none is installed, granted or bypassed by this record.

## Runtime evidence

Framework PR 172 passed all seven required checks and Sonar with zero open/unresolved issues and zero hotspots at exact head `f2a44adbcaa9fee093093b21186e7e305b78a02c` before squash merge. The selected Framework master is `2cc331d8bc4c86592afd7219ddeaba1e60dc0ced`. No new host runtime is performed for this digest-only repair. Parent main and all 12 native Sonar targets at `80334858a1a1e1ad1ff65e647716584a18cf3e9c` remain dated historical evidence of passing gates, zero unresolved issues and zero hotspots; they do not qualify a future Parent pin commit.

## Known limitations

Inventory admission proves the binding repair, not execution of every catalog case. The listed Parent local checks for the new pin passed; new-head CI requires a later normal commit/push. No future result is presented as observed evidence.

## Remaining risks

New source edits would require another reviewed binding refresh. Parent merge remains conditional on green required tests, final staged-byte checks and any applicable exact operator admission. Successful Framework checks alone do not establish Parent delivery readiness.

## Checks not run and rationale

No new-pin Parent CI, Parent commit or Parent master merge is claimed. Final staged-byte verification, the required exact operator admission and current-head CI evidence follow as separate delivery steps. MRTS remains read-only at `ee2174431c4edf97e66afe32558ce8454deb2397`; no MRTS mutation or full materialized-pin claim is made.

## Final diff and review status

The native scaffold identity, UTC date and Parent base are preserved. Scoped schema/EN-DE/link/whitespace and Secrets checks passed. The listed local results are observed; the final index must pass native verification and exact admission before normal commit/push. Parent merge remains conditional on the subsequent current-head CI gates.
