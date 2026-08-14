# FND-PARENT-0129 — Patched Lighttpd core build requires manual Autotools bootstrap when the verified 1.4.84 release lacks configure

| Field | Value |
| --- | --- |
| ID / source input | `FND-PARENT-0129` / `F-GS-002` |
| Category | `build_defect` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `validated` / `in_progress` |
| Feasibility | `blocked_external_dependency` |
| Release blocker / candidate-integration blocker | yes / no |
| Security-relevant | yes; source/bootstrap execution boundary, no exploit claimed |

## Summary

The pinned, verified Lighttpd `1.4.84` release can omit generated executable
`configure`. The previous patched-core builder stopped before configuration,
although the retained analysis showed that a task-local `sh autogen.sh` enabled
the real core and host build. The source repair adds the same decision to the
builder: reuse executable `configure`; otherwise bootstrap only the disposable
patched source copy, then require an executable result. Six real-script
contract scenarios and generated English/German guide checks pass. The finding
remains `in_progress`: the allowed storage has no verified `1.4.84` tree or
archive for the required final clean core/host proof, and no network workaround
is authorized.

## Observed and expected behavior

The analysis-only record
`.codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/`
records the original blocked build from a verified source followed by a
successful task-local `sh autogen.sh`, core build, and host build. The old
builder had only an executable-`configure` gate.

After existing source validation and patching, an executable `configure` must
be reused. Otherwise `autogen.sh` must exist in the patched copy and run there.
An executable script runs directly; a non-executable script is accepted through
`sh` only with an exact `#!/bin/sh` or `#!/usr/bin/env sh` first line. A missing
script, unsupported interpreter, bootstrap failure, or non-executable generated
`configure` stops with a precise exit-77 diagnostic before core-build output.

## Impact and security assessment

The fresh patched Lighttpd core/host build was not reproducible without manual
intervention. This is a P1 release-build boundary, not a demonstrated exploit.
The changed path executes an upstream-maintained bootstrap script, so it is
security-relevant: bootstrap remains limited to the patched disposable copy;
the original verified source is not modified; no package installation, network
action, hash change, mode change, or ignored failure was introduced.

Security invariant: after existing source validation and patch application,
bootstrap runs only inside the disposable patched tree; it must preserve the
original source, perform no installer/network action, surface failures, and
produce executable `configure` before core output is created.

## Affected files and symbols

- `connectors/lighttpd/build/build_patched_core.sh`: `run_autogen` and
  `ensure_configure`.
- `connectors/lighttpd/tests/test_patched_host_contract.py`: six real-script
  bootstrap scenarios.
- `scripts/generate_compiler_guides.py` and generated
  `docs/build/compilers/lighttpd.md` / `.de.md`: same explicit decision.
- `tests/test_compiler_guides.py`: generated documentation regression.

## Preconditions and reproduction

1. The caller supplies absolute external `LIGHTTPD_SOURCE_DIR` containing
   verified Lighttpd `1.4.84` source.
2. Existing patch application copies that source into the managed external
   patched root.
3. The upstream tree has executable `configure` or an `autogen.sh` that can
   generate it with its declared tooling.
4. Run `make -C connectors/lighttpd check-lighttpd-patched-host` with a clean
   private `BUILD_ROOT`. Before this repair the absent-configure source blocks;
   after it the patched copy bootstraps and the core/host succeeds.

## Evidence

- Original failure and manual-bootstrap success:
  `.codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/artifacts/build-observation.json`,
  SHA-256 `ccb6ed179d61f716e5035fbed0376469432a98233da96966621c7f310cbd117c`.
- Local remediation receipt:
  `.codex/runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md`,
  SHA-256 `e4e16d93f787ef22e954abf33051ca72e60446662d8aa5d0f4751726fe796cbc`.
  It records the current 26 patched-host contract tests, four Lighttpd guide
  controls, the full 21-test compiler-guide suite, bilingual docs, doc links,
  shell checks, JSON parsing, and diff check as passed. `LIGHTTPD_SOURCE_DIR`
  is unset; the prior target attempt stopped fail closed at the missing-input
  gate (Make exit `2`, underlying builder exit `77`), not at a real-source
  core/host result.

## Root cause and remediation

The previous builder assumed generated `configure` existed in the copied,
patched source even though the pinned release can omit it. The repair adds a
narrow bootstrap step after existing patch/stamp verification and before the
first configure invocation. It writes bounded `autogen.log` output on failure
and requires executable `configure` before `mkdir` creates the core build
directory. It does not guess Autotools subcommands: upstream `autogen.sh`
remains authoritative.

## Acceptance criteria and validation plan

1. Existing executable `configure` skips `autogen.sh`.
2. Missing `configure` bootstraps only the patched copy, including an exact
   POSIX-shebang non-executable script.
3. Missing script, failed bootstrap, unsupported interpreter, and missing
   generated `configure` fail closed before core output exists.
4. Original source, patch/hash controls, and no-install/no-network policy stay
   intact; English/German instructions stay synchronized.
5. With a supplied verified source, a fresh real core and host build and a
   repeat reuse run pass with retained raw evidence.

The next required control is a clean external source build under a new private
`BUILD_ROOT`, retaining stdout, stderr, exit code, `autogen.log`, patch/core
manifests, staged binary, and host manifest. Then rerun all focused tests and
documentation/static checks.

## Regression and legitimate controls

The focused builder test covers existing configure, missing configure with
POSIX non-executable autogen, non-executable configure, both files missing,
bootstrap failure, no generated configure, unsupported interpreter, and repeat
reuse. The current four targeted Lighttpd generator controls, the full
`make check-compiler-guides` suite, shell syntax, ShellCheck, bilingual docs,
doc links, JSON parsing, and `git diff --check` passed. A supplied real source
must still prove patch identity, binary version, hook symbols, host
construction, original-source preservation, no network action, and no second
bootstrap on reuse.

## Dependencies, blockers, and residual risk

The final proof depends on a caller-provided verified Lighttpd `1.4.84` tree or
separately approved verified archive extraction. The promised absolute
`LIGHTTPD_SOURCE_DIR` is unset, and targeted local discovery found no matching
tree/archive; the user prohibited a network acquisition step. Do not call this
finding fixed, verified, or closed until the real clean core/host/reuse control
passes. `FND-PARENT-0090` cites a different historical
`F-GS-002` from a 2026-08-02 HAProxy/libModSecurity dependency boundary; it is
not a duplicate of this Lighttpd record.

## History

- `2026-08-14T11:58:05Z`: implemented the patched-copy bootstrap decision,
  six scenario controls, and bilingual generated documentation. The actual host
  target began its core prerequisite but stopped at the intentional missing
  `LIGHTTPD_SOURCE_DIR` gate; no unsafe workaround was used.
- `2026-08-14T12:15:11Z`: added explicit non-executable-`configure` and
  unsupported-interpreter controls. All 26 focused contract tests, shell
  syntax, and ShellCheck passed; only the approved real-source core/host proof
  remains blocked.
- `2026-08-14T12:48:43Z`: reran the 26-test contract suite, four
  Lighttpd-specific guide controls, full compiler-guide suite, bilingual docs,
  doc links, shell checks, JSON parsing, and diff check successfully. The
  requested source input remained absent, so fresh/core/host/reuse E2E and the
  original-source fingerprint were not claimed and status remains
  `in_progress`.
