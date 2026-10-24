# Change Record: NGINX configuration receipt collection

**Language:** English | [Deutsch](CR-20261001-nginx-configtest-collection.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261001-nginx-configtest-collection` |
| Date (UTC) | `2026-10-01` |
| Base revision | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |

## Motivation and problem statement

The source collector did not preserve the new explicit configuration receipt
and its retained-artifact reference. A configuration-only operation must not
be interpreted as request execution merely because a raw case record exists.

## Acceptance criteria

Preserve bounded allowlisted receipt/run fields and an authorized existing
five-file bundle reference. Reject missing authority, outside or relative
paths, symlinks, missing files and unexpected artifact keys. Configuration
records must not produce rule/transaction events or claim host startup or
requests. Existing HTTP evidence must retain its original interpretation.

## Implementation decision and rationale

Preserve the configuration receipt through `collect-no-crs-source.py` without
creating evidence or replacing FAIL. Accept `artifacts.configtest_dir` only
within the explicitly authorized source root and with the closed files
`nginx-binary`, `nginx-module.so`, `nginx.conf`, `stdout.log`, and `stderr.log`.
The companion Framework validates receipt semantics and rehashes managed
artifacts. The separate driver/wiring change owns actual configuration
invocation and selected-case dispatch.

## Security impact

The collector is a consumer, not an event producer. It preserves containment,
symlink rejection, bounded metadata and payload exclusions. A phase-0 receipt
cannot turn a request record into configuration proof. A config-only source
keeps `started=false` and `requests_sent=false`; a genuine HTTP case still
counts as request execution. Neither missing required cases nor unrelated
module errors are promoted to PASS.

## Changed files

- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `tests/test_nginx_configtest_collection.py`
- This EN/DE Change Record and archive index pair

## Commands executed

All shell commands use RTK. The task coordinator observed 6 collector tests
passing and a broader Parent focus with 186 tests passing in 57.106 seconds.
The final combined focused command uses the existing Framework interpreter:
`rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python -m unittest tests.test_nginx_configtest_driver tests.test_nginx_configtest_collection -v`.
The final combined rerun passes 18 tests in 12.304 seconds.
The focused rerun passes all 6 tests in 0.190 seconds. RTK-wrapped
`make PYTHON=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python check-bilingual-docs check-doc-links` passes with external
task `TMPDIR`/`BUILD_ROOT` and the unchanged physical Parent Framework pin.
The frozen Framework No-CRS suite passes 159 tests in 112.402 seconds, exit 0;
full `make lint` exits 0 (session 8526). Framework focus passes 27 tests in
3.144 seconds and 3.651 seconds in independent review. No unobserved check is
claimed.

## Runtime evidence

The real retained diagnostic `runs/diagnosis/nginx-configtest-retained-jaYdBrvH`
produces canonical `invalid_boolean` PASS only for exit 1 with exact boolean
rejection. Actual NGINX with a controlled non-ELF module also exits 1 but
produces case FAIL with `unexpected_config_error`. Framework finalization
retains and rehashes five managed artifacts for each control. Both produce
zero native events, no startup and no requests; source/canonical aggregates
remain FAIL because other required requests were deliberately omitted.
The strict checker for `analysis/nginx-configtest-retained-check-20261001.json`
exits 0. These are retained-build diagnostics, not exact-head E2E PASS.

## Checks not run and rationale

No full E2E, push, PR mutation, protocol run, gitlink update or merge. Required
coverage remains incomplete. The Framework-specific Change Record checker is
inapplicable to Parent templates; Parent native bilingual/path/link checks
apply, with no unrelated historical record or validator changes.

## Known limitations

Receipt semantics are Framework-owned; preserving a reference alone does not
establish a valid canonical PASS. This slice does not invoke cases. Nine other
configuration-related required records remain outside the initial
`invalid_boolean` implementation.

## Remaining risks

Retained artifact bytes and caller-supplied source identities require their
own verification. The diagnostic reused a cached C build, so it does not
establish a build from the current Parent exact head.

## Final diff and review status

This independent collector change is reviewed and committed separately from
the driver/wiring change when validation is complete. At record creation no
commit, push or merge is asserted. Prepared protocol work and all Gitlinks
remain outside this change.
