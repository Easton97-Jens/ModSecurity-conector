# FND-PARENT-0042 — Parent runtime-component cache binds the NGINX release digest to a different tag archive

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0042 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | validated / blocked |
| Feasibility | blocked_environment after a locally evidenced source repair |
| Release blocker | yes |
| Security relevant | yes |

## Observation and impact

The isolated Parent PR #55 runtime-evidence preparation selected
`https://github.com/nginx/nginx/archive/refs/tags/release-1.31.2.tar.gz`, but
applied the reviewed SHA-256 for the different GitHub release asset
`nginx-1.31.2.tar.gz`. The retained manifest records expected
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c` and
observed `d886473e988ce6802d897310421e3ef038c06edc66c5424cd33ed1b15382e323`.
The checksum control correctly failed closed with `sha256_mismatch`.

No unverified archive was used. The impact is availability of legitimate
evidence: the required NGINX component cannot be prepared, so the current
runtime matrix for `FND-CROSS-0001` and protected integration of PR #55 cannot
proceed.

The local Parent correction now derives only
`https://github.com/nginx/nginx/releases/download/release-1.31.2/nginx-1.31.2.tar.gz`
after validating the complete pinned release identity. Its retained runtime
manifest records archive status `present`, checksum status `PASS`, and matching
expected/observed SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
The original `sha256_mismatch` therefore no longer reproduces. The legitimate
preparation then stops independently at `missing_nginx_modsecurity_module`
with NGINX build exit `77`; it is not complete native/runtime evidence.

## Evidence, cause, and source repair

- Run: `20260720T163253Z-pr55-runtime-evidence-refresh-698b1734`
- Retained artifact:
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T163253Z-pr55-runtime-evidence-refresh-698b1734/evidence/runtime-component-manifest-initial-failure.json`
- Artifact SHA-256:
  `d7e6517fe8be3a610dd51478cbb45c2fe9b4af3b1720562076129e24822efac3`
- Command: isolated `make prepare-runtime-components`, with every output root
  confined to the registered task run; exit code `2`.

- Corrected run: `20260721T005621Z-fnd-parent-0042-release-asset-b9e7172d`
- Corrected runtime manifest:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T005621Z-fnd-parent-0042-release-asset-b9e7172d/build/runtime-component-reports/reports/testing/generated/cache/runtime-component-cache.generated.json`
- Corrected manifest SHA-256:
  `3adf2284d3318cc35e690d319a84fe27200fe33047f43db22a328bf3c986253a`
- Final validation receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260721T005621Z-fnd-parent-0042-release-asset-b9e7172d/evidence/fnd-parent-0042-final-validation-20260721T014617Z.json`
- Final receipt SHA-256:
  `448fe124b2e1ed12a27e9402a38bc01d8809a2d7eee0fa9f14f9bcb0dbadf970`
- Corrected preparation result: the reviewed release asset passed its checksum
  boundary and then stopped at `missing_nginx_modsecurity_module`, NGINX build
  exit `77`.

At the source base, `resolve_nginx_archive` constructed a GitHub tag-archive
URL in `github-release` mode. Its shell wrapper did not pass the already
configured `NGINX_RELEASE_ASSET_NAME`, leaving the resolver unable to construct
and validate the matching release-download URL. The Framework direct NGINX
provisioner already uses the correct release asset; this is therefore a
separate Parent cache-provider defect, not a reopening of
`FND-FRAMEWORK-0006`.

The local implementation exports `NGINX_RELEASE_ASSET_NAME` and `NGINX_SHA256`,
uses `nginx_release_asset_identity()` to require the canonical HTTPS GitHub
repository, matching configured aliases, exact tag/ref, tag-derived asset
name, and lower-case 64-character SHA-256, and has no latest lookup or
tag-archive fallback. `github_repo_path()` now rejects percent-encoded,
reserved, dot-segment, malformed-owner, and overlong repository components
before generic GitHub URL construction. The URL-inclusive cache identity is
retained, so a same-basename tag-archive cache record cannot satisfy the
release-asset request.

## Implemented source controls and remaining validation

The implemented correction preserves the reviewed digest, derives the exact
release-download URL, rejects malformed/inconsistent release identities before
download, and does not change the digest to match the tag archive or fall back
to `/archive/refs/tags`.

Completed proof:

1. `rtk run /root/git/ModSecurity-conector/.venv/bin/python -B -s -m unittest -v tests.test_runtime_component_cache_contract`
   passed all `31` cache/provenance tests, including the exact release asset,
   malformed identity rejection, encoded/reserved/dot-segment path rejection,
   and stale tag-archive cache non-reuse.
2. Shell syntax, changed-Python AST syntax, variable documentation (`86`
   references), the bilingual documentation unit suite (`11` tests), and
   `rtk git diff --check` passed.
3. The isolated preparation retained the corrected manifest above and reached
   the independent NGINX module build boundary with the original reviewed
   SHA-256 unchanged.
4. Three independent review rounds closed encoded/reserved component and
   dot-segment canonicalization gaps; the final review found no remaining
   concrete GitHub URL parser/canonicalization bypass.

The legitimate control is the fixed `release-1.31.2` /
`nginx-1.31.2.tar.gz` configuration resolving to the exact
`releases/download` URL. A same-basename tag-archive cache record must not be
reused for that release-asset URL.

Still required before delivery, verification, or closure:

1. Provide an authorized environment with the missing
   `ngx_http_modsecurity_module` prerequisite and repeat the legitimate NGINX
   module/runtime preparation.
2. Repeat the downstream `FND-CROSS-0001` legitimate controls after the native
   prerequisite is available.
3. Rerun the broad documentation make checks only with the Framework boundary
   available through an authorized route; they currently exit `2` solely for
   existing links into the intentionally uninitialized Framework gitlink.
4. Only after these local gates pass, create a separate Parent delivery
   candidate and obtain its exact-head review, CI, SonarQube Cloud, and
   resulting-master evidence.

## Boundaries and disposition

This is `validated` and `blocked`, not fixed, verified, closed, or risk
accepted. The original checksum mismatch is locally remediated, but the
stricter workflow forbids a stronger outcome while native/runtime proof remains
`blocked_environment`. The evidence proves a fail-closed mismatch and its
corrected release-asset boundary, not a complete module build or full runtime
matrix. No staging, commit, push, pull request, merge, Framework change,
Parent gitlink update, or MRTS action has occurred.

The distinct Framework recursive-provenance blocker is `FND-FRAMEWORK-0030`.
Even after both source repairs, a full legitimate current runtime-evidence
chain and a fresh exact-head protected-delivery cycle remain required for
PR #55.

## History

- 2026-07-20T16:53:52Z — isolated evidence preparation recorded the tag
  archive/release-asset digest mismatch and stopped fail-closed.
- 2026-07-20T17:14:09Z — the Parent-only defect was deduplicated and allocated
  for remediation; no checksum weakening or delivery action occurred.
- 2026-07-21T01:46:17Z — the local Parent source repair and final validation
  receipt were recorded. The corrected release asset passed checksum
  verification and the `31` focused cache/provenance tests passed, but the
  preparation stopped independently at `missing_nginx_modsecurity_module`
  (NGINX build exit `77`). The finding is therefore `blocked`; no delivery was
  attempted.
