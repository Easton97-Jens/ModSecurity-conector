# FND-PARENT-0129 — Patched Lighttpd core build requires automatic Autotools bootstrap when the verified 1.4.84 release lacks configure

| Field | Value |
| --- | --- |
| ID / source input | `FND-PARENT-0129` / `F-GS-002` |
| Category | `build_defect` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `confirmed` / `fixed` |
| Feasibility | `feasible_now` |
| Release blocker / candidate integration blocker | yes / no |
| Security relevant | yes; source/bootstrap execution boundary, no exploit claimed |

## Summary

The official Lighttpd `1.4.84` XZ archive was acquired only from the
authorized official release host, verified against the pinned SHA-256
`076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70`,
safely extracted, and used through the required absolute
`LIGHTTPD_SOURCE_DIR`. Its original tree did not contain executable
`configure`.

The repaired Parent builder copied and patched that original tree only into a
disposable external work area, ran upstream `autogen.sh` there, verified the
generated executable `configure`, built the patched Core and Host, and passed
the host contract. A second invocation of the same build root emitted
`mode=reused`, left the `autogen.log` hash/mtime unchanged, and did not
bootstrap again. Original-source manifests before and after both Fresh/Reuse
pairs are byte-identical. The finding is therefore `fixed`; it is not yet
`verified` or `closed`, which require the authorized delivery and
post-merge master evidence.

## Observed and expected behavior

The immutable analysis-only record
`.codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/`
records the original defect: a fresh patched copy of verified Lighttpd
`1.4.84` lacked executable `configure`, so the former builder stopped
before configuration. The retained observation also showed that a task-local
upstream bootstrap permitted the subsequent real Core and Host build.

After source/patch verification, the builder must reuse existing executable
`configure`; otherwise it must run `autogen.sh` only in the patched source
copy and require executable generated `configure` before Core output exists.
Missing `autogen.sh`, an unsupported non-executable interpreter, a bootstrap
failure, or a missing/non-executable generated `configure` must retain the
native precise exit-`77` failure path.

## Real source and integrity evidence

| Control | Result |
| --- | --- |
| Archive identity | Official XZ SHA-256 and size passed: `076dd43…26f70`, `895228` bytes. |
| Source identity | `configure.ac` contains `AC_INIT([lighttpd],[1.4.84]`; `autogen.sh`, `Makefile.am`, and `src/` are present. |
| Fresh condition | Original `configure` was absent/non-executable before the build. |
| Patch identity | `e9bad85fe2f740350e090947f1dcebd2d7111c76b6914f80328ae49d1aad106d`. |
| Original-source manifest | Before, after, and final-after SHA-256 all equal `65da21d0e8e18198fd84f7deb6d014bd6c4cb582869318d0e9e13fc7144566fb`; both `cmp` checks exit `0`. |
| Fresh Core/Host/contract | Passed with exit `0`, including a repeat inside a network namespace. |
| Reuse | Passed with exit `0`; core emitted `mode=reused`. |
| No second bootstrap | `autogen.log` SHA-256 `60040f093546e8d3d754b4a6fb3ab962abba12031cad677fa603c0e0635b48f6`, size `916`, and mtime `1786717176` were unchanged across Reuse. |

The full evidence, exact paths, commands, exit codes, bounded log references,
and the distinction between archive and tree hashes are retained in
[the validation receipt](../../runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md).

## Security invariant and implementation

The security-relevant boundary is upstream bootstrap execution from a
caller-controlled source path. The preserved invariant is that only an already
verified Lighttpd `1.4.84` source becomes a patched disposable copy; bootstrap
can execute only there, failures remain visible, and an executable
`configure` is mandatory before the Core build. The original source remains
unmodified, and no package installation, chmod, hash weakening, or network
acquisition was added.

The real Fresh and Reuse targets were executed in a no-network namespace.
The upstream script wrote `trap: ERR: bad trap` under `/bin/sh`, but returned
`0`, generated `configure`, and completed the real Core/Host path; this
does not justify another bootstrap-logic change.

## Affected files and symbols

- `connectors/lighttpd/build/build_patched_core.sh`: `run_autogen`,
  `ensure_configure`, and `verify_core`.
- `connectors/lighttpd/tests/test_patched_host_contract.py`: focused
  bootstrap, error, and Reuse controls.
- `scripts/generate_compiler_guides.py` and generated Lighttpd EN/DE guides.
- `tests/test_compiler_guides.py`: generated-guide regression controls.

## Acceptance criteria and validation

1. Existing executable `configure` skips bootstrap.
2. Missing `configure` bootstraps only the patched copy and yields executable
   `configure`.
3. Missing script, unsupported interpreter, failed bootstrap, and missing
   output all fail closed before Core output.
4. Fresh verified-source Core/Host/contract and same-root Reuse pass.
5. Original source remains unchanged and Reuse does not rerun `autogen.sh`.
6. Focused contract, guide, syntax, JSON, and scoped documentation checks pass.

Observed local results:

- `sh -n connectors/lighttpd/build/build_patched_core.sh`: passed.
- `shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh`: passed.
- `python3 connectors/lighttpd/tests/test_patched_host_contract.py`: 26 tests passed.
- Four selected Lighttpd guide idempotence/EN-DE/shell/parity controls: passed.
- `make check-compiler-guides`: 21 tests passed.
- The two Lighttpd guide links passed in the clean PR worktree.
- `make check-bilingual-docs` and `make check-doc-links` passed in the
  existing checkout where the Framework gitlink is present. The same generic
  targets are environmentally blocked in the clean PR worktree because that
  gitlink is deliberately uninitialized; their failures concern root/example
  Framework links, not this Lighttpd change.
- Relevant JSON parsing and `git diff --check` passed.

## Dependencies, blockers, and residual risk

The former external-source blocker is resolved. No F-GS-002 acceptance
criterion remains blocked. The generic ignored Backlog/Roadmap corpus is not
part of the PR baseline and was not force-added because it would import
unrelated findings.

Residual risk is lifecycle-only: this finding remains `fixed`, not
`verified` or `closed`, until the current PR head is merged, the exact
`origin/master` result and required workflows are checked, and the original
reproduction or strongest equivalent is rerun on master. No Traefik, Framework,
or MRTS file was changed.

## History

- `2026-08-14T11:58:05Z`: implemented the narrow patched-copy bootstrap,
  six real-script scenarios, and generated bilingual guide updates.
- `2026-08-14T12:15:11Z`: added explicit non-executable-`configure` and
  unsupported-interpreter controls; 26 focused tests, shell syntax, and
  ShellCheck passed.
- `2026-08-14T14:23:16Z`: verified official archive/source identity,
  original-source integrity, real Fresh Core/Host/contract, and same-root
  no-network Reuse without a second bootstrap; status changed to `fixed`.
- `2026-08-14T15:08:19Z`: added the required paired Change Record and archive
  index entries; the receipt now records strict Change-Record documentation
  checks, including the temporary-overlay passes without Parent, Framework, or
  MRTS source changes.
- `2026-08-14T15:17:30Z`: narrowed the Change-Record wording to the actual
  before/after/final manifest evidence and repeated both standard documentation
  targets in a freshly recreated task-owned overlay; both passed and the copy
  was removed without source changes.
