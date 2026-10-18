# Change Record: CR-20261018-i12-historical-capture-anchors

**Language:** English | [Deutsch](CR-20261018-i12-historical-capture-anchors.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-historical-capture-anchors |
| Date (UTC) | 2026-10-18 |
| Base revision | `2c38d0ff2960a9ff2a76291955e808683febf06e` |

## Motivation and problem statement

Normal authorized product integration changed five live files that were still used as historical capture object storage. Registry.verify consequently rejected every profile, including lighttpd, before any host build. The retained failure is Source byte hash mismatch: ba8fe2b69ace0e6dae345b59bc20ddc09594a5e2426a16209ee4d0e72b19baa6.

## Acceptance criteria

Preserve every historical object identity, profile target, delta and byte. Restore full registry verification without changing current product source or accepting mismatched bytes.

## Implementation decision and rationale

Five historical repository objects now use the existing lossless text_lines store. Each source was recovered from exact Git revision9980eb049dde0643da6a4f04e3b6712801b670b3 and independently matched its original SHA256. The five source identities and all profile mappings remain unchanged. This is archival measurement repair; product changes stay in their owning branches.

## Changed files

ci/runtime/lifecycle/i12/manifest.json and five bounded objects/text/*.lines.json files; this paired Change Record. Three HAProxy and two lighttpd historical snapshots are retained; no HAProxy or other-connector product file is edited.

## Commands executed

All commands use RTK. capture_sources.py verify passes155 objects and9 profiles, source_only=true/runtime_qualified=false. Exact Git blob SHA256 comparisons pass for all five snapshots. The existing48 capture ownership/hash/delta negative controls PASS; EN/DE and repository-link checks PASS.

## Security impact

The source registry, current exported tree validation, bounded text limit, no-symlink/no-hardlink checks and exact patch enforcement are unchanged. Historical instrumentation is not claimed to be current production code.

## Runtime evidence

Run i12-lighttpd-412-completion-20261015/shared/historical-anchors-20261018.json binds original revision, paths, identities, byte counts and new storage paths. The failed diagnostic preparation is preserved. Fresh host preparations must still bind their actual current product module and patch separately.

## Known limitations

Registry success proves source materialization only; it adds no lifecycle PASS and no original oracle resolution.

## Remaining risks

Future current-product variants still require explicit, hash-verified observation rebasing; immutable historical source must never silently replace a product fix.

## Checks not run and rationale

No other-connector host execution, Framework/MRTS change, release, deployment or master integration. Exact-head hosted CI remains separate after normal publication.

## Final diff and review status

Root reviewed all five old/new object mappings and unchanged profile targets. This necessary shared repair is published through existing#410 and consumed by normal merge into#412.
