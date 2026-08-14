# F-GS-002 Lighttpd autogen bootstrap — validation receipt

- Run ID: `20260814T115110Z-f-gs-002-autogen-bootstrap`
- Scope: Parent repository only. No Framework, MRTS, Traefik, package,
  download, source acquisition, Git delivery, or bootstrap-logic rewrite was
  performed in this continuation.
- Finding disposition: `FND-PARENT-0129` remains `in_progress` /
  `blocked_external_dependency`. The immutable analysis-only F-GS-002 record
  was not modified.

## Requested source input and preflight

| Item | Result |
| --- | --- |
| `LIGHTTPD_SOURCE_DIR` | **Not supplied:** `rtk proxy printenv LIGHTTPD_SOURCE_DIR` returned exit `1`; no absolute path was available. |
| Local source discovery | **No candidate:** targeted local searches under `/root` and `/var/tmp/codex/ModSecurity-conector` found no `lighttpd-1.4.84` tree, matching archive, or `configure.ac` containing `AC_INIT([lighttpd],[1.4.84]`. |
| Required source files, version, and identity | **Blocked:** without the supplied absolute tree, `configure.ac`, `autogen.sh`, `src/plugin.h`, and the upstream 1.4.84 identity cannot be checked. |
| Expected upstream archive SHA-256 | `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70`, as specified by the generated Lighttpd EN/DE guides. |
| Actual upstream archive/tree hash | **Unavailable:** no supplied archive or source tree exists locally. A directory-content hash must not be represented as the pinned archive SHA-256. |
| Repository patch integrity | **Passed:** current patch SHA-256 is `e9bad85fe2f740350e090947f1dcebd2d7111c76b6914f80328ae49d1aad106d`; it is the value enforced by `apply_core_patch.sh`. |

The repository builder validates Lighttpd version/source shape and the patch
hash after it receives a source tree. It does not itself prove a tarball hash
from an arbitrary extracted directory. Therefore the caller-provided source
archive/provenance remains an explicit acceptance prerequisite.

## Real end-to-end scenarios

| Scenario | Status | Evidence |
| --- | --- | --- |
| Fresh external work copy without executable `configure`: apply patch, bootstrap with `autogen.sh`, build core, build patched host, run relevant host checks | **blocked** | No verified absolute `LIGHTTPD_SOURCE_DIR` was supplied. No substitute or network download was used. |
| Repeat/reuse build: reuse executable `configure` and avoid a second `autogen.sh` run | **blocked** | It depends on the preceding real fresh build and its patched external copy. |
| Original source remains unchanged | **blocked** | No original source was available to fingerprint before/after. No source tree was copied, patched, bootstrapped, or otherwise written by this continuation. |
| Only patched external copy is bootstrapped | **blocked for real source; passed by focused control** | The 26-test real-script contract suite proves the selected builder path invokes bootstrap in its managed patched copy. The requested real-source observation awaits the supplied input. |
| No network access during real build | **blocked for real source; no network action performed** | No real build or source acquisition ran. The completed local checks invoke no download/provisioning command; no network client was started by this task. |
| Bootstrap failure codes are preserved | **passed (focused control)** | The contract suite covers a failing upstream bootstrap and verifies its output and status are reported through exit `77`. |

## Implemented boundary retained for validation

`build_patched_core.sh` applies the existing patch to a disposable external
copy first. It then reuses executable `configure`, or runs upstream
`autogen.sh` only in that patched copy, requires an executable result, and
fails closed before creating the core build directory. It does not modify
source modes, install packages, fetch inputs, or discard bootstrap failures.
The current source was not changed during this validation continuation.

## Commands and observed results

Private external task paths are written as `<private-run>` below. This retains
the exact command structure without placing unrelated machine-specific build
paths in durable repository evidence. The user-requested absolute source path
cannot be recorded because no source path was supplied.

| Command | Exit | Result / relevant output |
| --- | ---: | --- |
| `rtk proxy printenv LIGHTTPD_SOURCE_DIR` | `1` | Variable unset; no source input. |
| `rtk proxy env TMPDIR=<private-run>/tmp BUILD_ROOT=<private-run>/build LIGHTTPD_MAKE_JOBS=2 make -C connectors/lighttpd check-lighttpd-patched-host` | `2` | Prior retained run attempt: the actual core prerequisite returned `77` with `LIGHTTPD_SOURCE_DIR is required`; host did not run. It is a missing-input proof, not a real-source E2E result. |
| `rtk proxy find /root -type d -iname '*lighttpd*1.4.84*' -print` | `0` | No candidate. |
| `rtk proxy rg --hidden --no-ignore -l --glob configure.ac 'AC_INIT\(\[lighttpd\],\[1\.4\.84\]' /root /var/tmp` | `1` | No matching source identity. |
| `rtk proxy sha256sum connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch` | `0` | `e9bad85fe2f740350e090947f1dcebd2d7111c76b6914f80328ae49d1aad106d`. |
| `rtk proxy sh -n connectors/lighttpd/build/build_patched_core.sh` | `0` | Shell syntax passed. |
| `rtk proxy shellcheck -s sh connectors/lighttpd/build/build_patched_core.sh` | `0` | ShellCheck passed. |
| `rtk proxy env TMPDIR=<private-run>/tmp python3 connectors/lighttpd/tests/test_patched_host_contract.py` | `0` | `Ran 26 tests ... OK`. |
| `rtk proxy env TMPDIR=<private-run>/tmp python3 -m unittest tests.test_compiler_guides.CompilerGuideGenerationTest.test_prefix_and_cleanup_regressions_are_explicit tests.test_compiler_guides.CompilerGuideGenerationTest.test_every_generated_shell_block_is_syntactically_valid tests.test_compiler_guides.CompilerGuideGenerationTest.test_generated_files_are_complete_current_and_idempotent tests.test_compiler_guides.CompilerGuideGenerationTest.test_connector_structure_and_bilingual_technical_parity` | `0` | `Ran 4 tests ... OK`; covers Lighttpd guide wording, EN/DE parity, shell syntax, and idempotence. |
| `rtk proxy env TMPDIR=<private-run>/tmp make check-compiler-guides` | `0` | `Ran 21 tests ... OK`. The earlier foreign Traefik deviations did not reproduce in this current run; no Traefik file was changed by this task. |
| `rtk proxy env TMPDIR=<private-run>/tmp make check-bilingual-docs` | `0` | `bilingual docs ok`. Initial identical runner launches had no terminal status within their 30-second handoff; only this terminal result is recorded as passing. |
| `rtk proxy env TMPDIR=<private-run>/tmp make check-doc-links` | `0` | `repository path references: PASS`; Framework checker: `doc links ok`. |
| `rtk proxy git diff --check` | `0` | No whitespace errors. |
| `rtk proxy jq empty connectors/lighttpd/SOURCE_MAP.json .codex/findings/FND-PARENT-0129/finding.json .codex/findings/backlog.json .codex/roadmap/remediation-roadmap.json .codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/finding.json` | `0` | Relevant structured JSON parses. |

## Explicit non-results and next action

`make -C connectors/lighttpd build-lighttpd-patched-core`,
`build-lighttpd-patched-host`, and a new real-source
`check-lighttpd-patched-host` invocation were not started in this continuation
because their required verified source input is absent. The prior retained
missing-input target attempt is listed above. Starting a new run with a guessed
or empty input would neither validate the requested fresh/reuse scenarios nor
honor the source-integrity requirement.

To complete this receipt, provide the promised absolute external
`LIGHTTPD_SOURCE_DIR`. The next run will first verify its existence, upstream
files/identity, `1.4.84` version, and archive/provenance hash; fingerprint the
original tree before and after; then retain fresh-build and reuse-build logs,
exit codes, `autogen.log` evidence, and the source-unchanged comparison. Until
then neither FND-PARENT-0129 nor the historical F-GS-002 evidence is marked
`fixed`.
