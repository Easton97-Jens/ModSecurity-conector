# Change Record: F-GS-002 Lighttpd configure bootstrap validation

**Language:** English | [Deutsch](CR-20260814-f-gs-002-lighttpd-autogen-bootstrap.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260814-f-gs-002-lighttpd-autogen-bootstrap |
| Date (UTC) | 2026-08-14 |
| Base revision | `ea3b48abab7940de49997a371f9117b409c05a2a` |
| Delivery status | Pre-merge follow-up for Parent PR [#285](https://github.com/Easton97-Jens/ModSecurity-conector/pull/285). Its first validated evidence head was `62e226bd016c01231d6cbb7da6bb8f552441f7ab`; this required record creates a new candidate head, so its protected-check and review round must be repeated before any merge. No merge is claimed here. |

## Motivation and problem statement

The verified Lighttpd 1.4.84 release tree can legitimately omit generated
`configure`. The patched-core builder previously failed before the real Core
and Host build in that state, even though the release supplies upstream
`autogen.sh` and its Autotools input files. F-GS-002 / FND-PARENT-0129 tracks
that reproducible build blocker.

## Acceptance criteria

- Reuse an existing executable `configure` without bootstrap.
- Otherwise run upstream `autogen.sh` only in the disposable patched external
  source copy, preserve its failure status, and require an executable result.
- Verify the official `lighttpd-1.4.84.tar.xz` release with the pinned
  SHA-256 `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70`
  and the official checksum line before use.
- Demonstrate Fresh Core, patched Host, and same-root Reuse builds without
  network access; prove that Reuse does not run `autogen.sh` again.
- Prove that the original verified source tree is unchanged before, during,
  and after the builds; update FND-PARENT-0129 to `fixed` only after those
  gates pass.

## Implementation decision and rationale

`build_patched_core.sh` keeps the executable-`configure` fast path. If it is
absent or non-executable, `ensure_configure` accepts an executable
`autogen.sh`, or a non-executable script with exactly `#!/bin/sh` or
`#!/usr/bin/env sh`; it runs the selected upstream entry point inside
`PATCHED_SOURCE_DIR`. The bounded `autogen.log` preserves diagnostics. A
non-zero bootstrap result, an unsupported non-executable script, or a missing
executable generated `configure` fails closed with the existing blocked exit
semantics.

The implementation never alters the supplied original tree. The repository
copies it into a managed external patched tree, applies the pinned connector
patch there, and bootstraps only that copy. The real source acquisition used
only the authorized official archive and checksum; the source path and full
command inventory are retained in the validation receipt. No package was
installed and no bootstrap logic was changed during the real validation.

The ignored local `.codex` Backlog/Roadmap corpus was not force-added: doing so
would import hundreds of unrelated local control-plane records. The canonical
FND EN/DE/JSON records and its retained receipt are the scoped versioned
evidence for this fix; the limitation is explicit rather than hidden.

## Security impact

The change touches a build-script execution boundary. Its security invariant
is that only a previously verified Lighttpd 1.4.84 tree is copied to the
external patched workspace, and only that copy may execute `autogen.sh`.
Original-tree no-follow manifests before and after the builds were identical.
Bootstrap failures are not suppressed, no package or network step is added,
and an executable generated `configure` is required before configuration and
compilation. This is a build/lifecycle defect remediation, not a claimed
security vulnerability or a runtime exploit fix.

## Changed files

- `connectors/lighttpd/build/build_patched_core.sh`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `scripts/generate_compiler_guides.py`
- `tests/test_compiler_guides.py`
- `docs/build/compilers/lighttpd.md`
- `docs/build/compilers/lighttpd.de.md`
- `.codex/findings/FND-PARENT-0129/finding.json`
- `.codex/findings/FND-PARENT-0129/finding.md`
- `.codex/findings/FND-PARENT-0129/finding.de.md`
- `.codex/runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md`
- this English/German Change Record pair and its English/German archive index
  entries.

No Traefik, Framework, MRTS, Gitlink, archive, binary, build product, cache,
or credential is included.

## Commands executed

- The official archive and checksum were acquired with the user-authorized
  fail-closed HTTPS `curl` commands; the exact invocations and exit codes are
  retained in the validation receipt.
- Fresh and Reuse used `env LIGHTTPD_SOURCE_DIR="$LIGHTTPD_SOURCE_DIR" make -C connectors/lighttpd check-lighttpd-patched-host` with the recorded external build roots and ModSecurity include/library paths.
- Network-isolated Fresh and Reuse repeated that command through
  `unshare --net -- env`, with the same recorded inputs.
- Focused checks used `sh -n connectors/lighttpd/build/build_patched_core.sh`,
  `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh`,
  `python3 connectors/lighttpd/tests/test_patched_host_contract.py`, and the
  recorded focused `CompilerGuideGenerationTest` controls.
- Documentation and final consistency checks used `make check-compiler-guides`,
  `make check-bilingual-docs`, `make check-doc-links`, relevant JSON checks,
  and `git diff --check`.

## Tests and actual results

The complete command inventory, working directories, environment values,
exit codes, bounded log excerpts, and source-manifest files are retained in
`.codex/runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md`.
Observed results are:

| Check | Actual result |
| --- | --- |
| Official archive and checksum acquisition | passed; XZ size `895228`; expected and actual SHA-256 matched `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70` |
| Archive/member and source identity checks | passed; safe 361-member archive; `AC_INIT([lighttpd],[1.4.84]`; original `configure` absent |
| Fresh `make -C connectors/lighttpd check-lighttpd-patched-host` | passed, exit 0; patch, bootstrap, Core, Host, config check, and host contract passed |
| Same-root Reuse command | passed, exit 0; `mode=reused`; `autogen.log` hash, size, and timestamp unchanged |
| Fresh and Reuse under `unshare --net` | both passed, exit 0; no network interface was available |
| Original-source preservation | passed; before/after/final manifests have SHA-256 `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb`, 361 entries, and bytewise `cmp` exit 0 |
| `sh -n connectors/lighttpd/build/build_patched_core.sh` | passed, exit 0 |
| `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh` | passed, exit 0 |
| `python3 connectors/lighttpd/tests/test_patched_host_contract.py` | passed, 26 tests, exit 0 |
| Four focused `CompilerGuideGenerationTest` controls | passed, exit 0 |
| `make check-compiler-guides` | passed, 21 tests, exit 0 |
| Focused Lighttpd guide/link and relevant JSON controls | passed, exit 0 |
| `git diff --check` | passed, exit 0 |

## Runtime evidence

The Fresh and Reuse runs are real Core and patched-Host build evidence,
including the repository host contract. They are not a claim of live HTTP
traffic or a production service runtime exercise.

## Checks not run and rationale

Optional GPG verification was not run because no pre-trusted upstream key
fingerprint was available; the pinned archive digest and official checksum line
remain the mandatory verification. In the clean task worktree,
`make check-bilingual-docs` and `make check-doc-links` stopped with exit 2
only because its deliberately uninitialized Framework gitlink was absent. The
same targets passed read-only in the existing Parent checkout with that gitlink
present. No Framework action was taken.

## Known limitations

The upstream `autogen.sh` emitted `trap: ERR: bad trap` under the system POSIX
shell, then completed successfully; the resulting `configure`, Core, Host,
and contract checks passed. This is retained as bounded upstream diagnostic
evidence, not masked as a success-only log.

FND-PARENT-0129 is `fixed`, not `verified` or `closed`. Post-merge verification
must confirm the merged `master` SHA and rerun the strongest appropriate
reproduction before its later lifecycle transition.

## Remaining risks

`autogen.sh` remains upstream-defined code execution, as does the subsequent
existing `configure`/`make` path. The control is source provenance, exact
archive verification, external-copy isolation, fail-closed result checks, and
the original-source preservation proof; it is not a substitute for a caller
that bypasses verified-source provisioning.

## Final diff and review status

The first full final review found PR #285 open, Ready, mergeable, clean, and
based on `master`; its required checks `actions`, `bounded-c-cpp`, `envoy-go`,
`traefik-go`, `actionlint`, and `zizmor` passed for
`62e226bd016c01231d6cbb7da6bb8f552441f7ab`. SonarCloud passed; no approvals
were required; there were no reviews, inline comments, or review threads.
Repository settings allow squash only. This required record changes the PR
head, so those facts are pre-follow-up evidence only. A new exact-head check,
review, base-freshness, and protected squash-merge round is required before
delivery.
