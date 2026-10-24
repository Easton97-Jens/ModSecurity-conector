# Change Record: CR-20261009-nginx-fresh-raw-run-mode

**Language:** English | [Deutsch](CR-20261009-nginx-fresh-raw-run-mode.de.md)

Filesystem-contract fix; hosted integration pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-fresh-raw-run-mode |
| Date (UTC) | 2026-10-09 |
| Base revision | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |

## Motivation and problem statement

Caller umask 077 created the NGINX raw run as 0700 and blocked the nobody worker. Precreating the exact run correctly fails freshness.

## Acceptance criteria

Fresh NGINX full_lifecycle raw child is 0711. Existing/symlinked children remain rejected, logs/results private, and other routes unchanged.

## Implementation decision and rationale

After existing guards, mkdir -p creates only the parent; exclusive mkdir -m 0711 creates the exact raw child. No existing child is chmodded or reused. The caller supplies traversable ancestors.

## Changed files

`ci/runtime/lifecycle/run-no-crs-baseline.sh`; `tests/test_nginx_raw_run_creation.py`; this EN/DE Change Record pair.

## Commands executed

All shell commands were RTK-wrapped. Initial regression: five tests, one failure (0700 instead of 0711). Retained old-source regression: six tests, three expected failures (mode and late-created directory/symlink). Final command: python3 -m unittest -v tests.test_nginx_raw_run_creation tests.test_no_crs_baseline_shell_environment tests.test_runtime_path_security tests.test_runtime_path_utils tests.test_resolve_runtime_paths, with neutral external TMPDIR: 43 tests, exit 0, zero skips, 6.690s. sh -n, shellcheck -S warning, Change Record structure, and git diff --check passed. Initial sandbox chown errors passed in a privileged rerun. A broader run using a TMPDIR containing nginx correctly triggered foreign-connector rejection; the neutral TMPDIR rerun passed. Logs: raw-run-mode-red.log and raw-run-mode-green-neutral.log under /var/tmp/codex/ModSecurity-conector/analysis/nginx-all-required-20261008T124555Z.

## Security impact

The raw child gains execute-only traversal, no group/other read or write. Under umask 077 logs/results remain 0700. Exclusive mkdir rejects a child created after preflight. Existing path guards remain active.

## Runtime evidence

Filesystem regression evidence only; no HTTP, canonical result, build, or E2E PASS is claimed.

## Known limitations

The caller must supply safe traversable ancestors. Canonical evidence permissions are unchanged; the focused boundary only proves that canonical RUN_DIR is not created there, not its eventual mode. The root test run proves creation by EUID 0; a separate hosted run must prove Root/worker identities.

## Remaining risks

Hosted lifecycle verification remains required after integration.

## Checks not run and rationale

No build or E2E in this isolated worker worktree. Full documentation links need populated Framework checkout and remain for integration.

## Final diff and review status

Focused diff only. No commit/push or Framework/MRTS edits. Integration review pending.
