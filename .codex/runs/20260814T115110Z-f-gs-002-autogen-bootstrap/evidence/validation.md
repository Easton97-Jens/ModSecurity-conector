# F-GS-002 Lighttpd autogen bootstrap — validation receipt

- Run ID: `20260814T115110Z-f-gs-002-autogen-bootstrap`
- Validation date: `2026-08-14`
- Parent scope only; clean PR #285 worktree started at `521173b12c13bd1bb575c0bcfcb685ec06a5eb6f`.
- `FND-PARENT-0129` is `fixed` from the real Fresh/Core/Host/Reuse evidence. It is not `verified` or `closed`; those are post-delivery states.
- The immutable analysis-only F-GS-002 record was not modified.

## Source acquisition and identity

| Item | Result |
| --- | --- |
| Official archive | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.tar.xz` |
| Official checksum | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.sha256sum` |
| Archive path and size | `/var/tmp/codex/f-gs-002-lighttpd-1.4.84/lighttpd-1.4.84.tar.xz`; `895228` bytes (expected `895228`) |
| Expected and actual SHA-256 | `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70` / `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70` |
| Official checksum line | `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70  lighttpd-1.4.84.tar.xz` |
| `LIGHTTPD_SOURCE_DIR` | `/var/tmp/codex/f-gs-002-lighttpd-1.4.84/extracted/lighttpd-1.4.84` |
| Version/source shape | `configure.ac` contains `AC_INIT([lighttpd],[1.4.84]`; `autogen.sh`, `Makefile.am`, and `src/` exist (all exit `0`). |
| Initial state | `test ! -x "$LIGHTTPD_SOURCE_DIR/configure"` exit `0`. |
| Repository integrity | `SOURCE_MAP.json` pins Lighttpd `1.4.84` and the official location; `apply_core_patch.sh` enforced patch SHA-256 `e9bad85fe2f740350e090947f1dcebd2d7111c76b6914f80328ae49d1aad106d`. |

Only the authorized XZ archive and checksum were downloaded. The two `curl` calls and their promotion from temporary names each returned exit `0`; no other source, version, package install, or download was used.

A local `tarfile` preflight returned exit `0` with `members=361 regular=340 directories=21 symlinks=0 hardlinks=0`. It rejected absolute/traversal paths, escaping links, special files, and entries outside `lighttpd-1.4.84/`. The authorized `tar --no-same-owner --no-same-permissions` extraction returned exit `0`.

The full `sha256sum --check --strict lighttpd-1.4.84.sha256sum` returned exit `1` because that official file also lists deliberately un-downloaded `lighttpd-1.4.84.tar.gz`. It is not counted as a pass. A targeted fail-closed verifier parsed exactly one XZ line and required that official value and the actual XZ digest to equal the pinned digest; exit `0`.

## Original-source integrity

A no-follow, raw-byte sorted depth-first `lstat` manifest records path, type, mode, size, regular-file SHA-256, link target, and empty directories. These are tree manifests, never archive-hash claims.

| File | SHA-256 |
| --- | --- |
| `evidence/source-before.tsv` | `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb` |
| `evidence/source-after.tsv` | `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb` |
| `evidence/source-after-final.tsv` | `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb` |

Both before/after `cmp` commands returned exit `0`. The original tree still lacks `configure` after both Fresh/Reuse pairs. The original was neither patched nor bootstrapped; only disposable copies under the external build roots changed.

## Real Fresh/Core/Host and Reuse

The ordinary Fresh target returned exit `0`:

```sh
rtk proxy env LIGHTTPD_SOURCE_DIR=/var/tmp/codex/f-gs-002-lighttpd-1.4.84/extracted/lighttpd-1.4.84 BUILD_ROOT=/var/tmp/codex/f-gs-002-lighttpd-1.4.84/build MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu LIGHTTPD_MAKE_JOBS=2 make -C connectors/lighttpd check-lighttpd-patched-host
```

The decisive Fresh proof repeated that exact target in a network namespace with `BUILD_ROOT=/var/tmp/codex/f-gs-002-lighttpd-1.4.84/build-network-isolated`; exit `0`. It produced:

```text
lighttpd_core_patch: PASS mode=apply version=1.4.84 patch_sha256=e9bad85f...
lighttpd_patched_core_build: PASS mode=build binary=.../stage/bin/lighttpd
lighttpd_connector_build: PASS output=.../stage/modules/mod_msconnector.so
lighttpd_patched_host_build: PASS binary=.../stage/bin/lighttpd module=.../mod_msconnector.so
lighttpd_patched_host_check: PASS ... phase4=not-executed
```

The original lacks `configure`, and the builder can create `autogen.log` only in its copied patched tree. The copied-tree log exists at `.../build-network-isolated/lighttpd-core-patched/autogen.log`, has SHA-256 `60040f093546e8d3d754b4a6fb3ab962abba12031cad677fa603c0e0635b48f6`, and the generated copied-tree `configure` is executable. Its bounded upstream log shows successful `autoreconf` and ends with `Now type './configure ...' and 'make' to compile.`

The upstream shell also emitted `trap: ERR: bad trap` under `/bin/sh`; it nevertheless returned `0`, created executable `configure`, and the complete Core/Host target passed. This is an upstream diagnostic, not a new bootstrap failure, so the production logic was not changed again.

The net-isolated Reuse invocation used the same source and build root and returned exit `0`. It emitted `lighttpd_patched_core_build: PASS mode=reused`, then successful Host and host-contract checks. Before and after reuse, `autogen.log` had the same SHA-256 above, size `916`, and mtime `1786717176`; copied-tree `configure` remained executable. The existing-core-manifest fast path precedes `ensure_configure`, so no second `autogen.sh` ran.

Retained bounded raw logs and manifests are external and text-only:

```text
/var/tmp/codex/f-gs-002-lighttpd-1.4.84/build-network-isolated/lighttpd-core-patched/
  autogen.log
  build-1.4.84/configure.log
  build-1.4.84/make.log
  build-1.4.84/install.log
  patched-core-build-info.txt
  patched-host-build-info.txt
```

## No-network and error propagation

`rtk proxy unshare --net true` returned exit `0`, and both decisive Fresh and Reuse targets returned `0` inside that network namespace. No build command invoked a download client, installer, package manager, or network configuration command. The 26-case contract suite exercises bootstrap failure and confirms the native fail-closed exit-`77` path; errors are not suppressed.

## Focused/local validation matrix

| Command | Exit | Result |
| --- | ---: | --- |
| `sh -n connectors/lighttpd/build/build_patched_core.sh` | `0` | passed |
| `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh` | `0` | passed |
| `python3 connectors/lighttpd/tests/test_patched_host_contract.py` | `0` | `Ran 26 tests ... OK` |
| Four selected Lighttpd guide idempotence/EN-DE/shell/parity tests | `0` | `Ran 4 tests ... OK` |
| `make check-compiler-guides` | `0` | `Ran 21 tests ... OK`; no Traefik file changed |
| Focused link check for the two Lighttpd guides in the clean PR worktree | `0` | `PASS focused_lighttpd_doc_links documents=2` |
| `make check-bilingual-docs` in clean PR worktree | `2` | independent missing Framework-gitlink environment; only root/example non-Lighttpd links failed |
| `make check-doc-links` in clean PR worktree | `2` | same independent missing-Framework-gitlink environment |
| `make check-bilingual-docs` in existing checkout with Framework present | `0` | `bilingual docs ok` |
| `make check-doc-links` in existing checkout with Framework present | `0` | `repository path references: PASS`; `doc links ok` |
| `make check-bilingual-docs` in clean PR worktree after adding the Change Record | `2` | the Change Record itself satisfied its strict heading checks; only the same absent Framework-gitlink targets failed |
| `make check-doc-links` in clean PR worktree after adding the Change Record | `2` | the same independent missing-Framework-gitlink targets failed |
| `make check-bilingual-docs` in a task-owned temporary overlay containing a local Framework test copy | `0` | `bilingual docs ok` |
| `make check-doc-links` in that task-owned temporary overlay | `0` | `repository path references: PASS`; `doc links ok` |
| `make check-bilingual-docs` in a freshly recreated task-owned overlay after the receipt/Change-Record clarification | `0` | `bilingual docs ok` |
| `make check-doc-links` in that freshly recreated task-owned overlay after the receipt/Change-Record clarification | `0` | `repository path references: PASS`; `doc links ok` |
| Generator/guide-test syntax compilation; Lighttpd source-map/finding JSON parse | `0` | passed |
| `git diff --check` before tracking updates | `0` | passed |
| `python3 -m json.tool .codex/findings/FND-PARENT-0129/finding.json` after the evidence clarification | `0` | passed |
| `git diff --check` after the evidence clarification | `0` | passed |

The generic Backlog and Roadmap JSON corpus is ignored and absent from the PR baseline (about 497 KB and 434 KB in the unrelated shared control plane). It is intentionally not force-added or rewritten: importing it would add unrelated findings. The tracked FND and this receipt are the scoped F-GS-002 closure evidence.

Each temporary overlay was created only below the registered external task
root, used a local copy of the existing Framework solely to satisfy repository
link resolution, and was removed after exact-path verification. It changed
neither the Parent worktree nor the original Framework or MRTS repository.

## GitHub state

PR #285 is `https://github.com/Easton97-Jens/ModSecurity-conector/pull/285`.
At the pre-clarification delivery review it was open, Ready, cleanly mergeable,
and targeted `master` at head `7549c5ca7650d05eb0a1fcef4b90e842b27ea44d`.
Required checks `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`,
`actionlint`, and `zizmor` passed; Lighttpd contract, CodeQL, and SonarCloud
also passed. There were zero reviews and zero review threads; the only PR
comment was the SonarCloud Quality Gate passed report with zero new issues and
zero Security Hotspots. This receipt clarification creates a subsequent
candidate head, so current checks/reviews, final PR head, and merge result must
be reread after it. No merge is claimed by this local receipt.
