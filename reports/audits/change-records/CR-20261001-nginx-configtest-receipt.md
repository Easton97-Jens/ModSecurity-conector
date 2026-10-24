# Change Record: NGINX configuration-only receipt

**Language:** English | [Deutsch](CR-20261001-nginx-configtest-receipt.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261001-nginx-configtest-receipt` |
| Date (UTC) | `2026-10-01` |
| Base revision | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |

## Motivation and problem statement

The selected required `invalid_boolean` record lacked a concrete configuration
invocation and a canonical configuration-evidence contract. Treating it as an
HTTP case, or requiring a fabricated request event, would confuse test layers.

## Acceptance criteria

Run the closed `modsecurity maybe;` input through actual NGINX configuration
testing. Accept only exit 1 with both exact boolean-rejection diagnostics.
Retain digest-bound operation artifacts; preserve FAIL for missing evidence,
wrong exits, unrelated module errors, and mismatches. Do not alter selection
or claim requests, startup, listeners, workers, reload, or complete coverage.

## Implementation decision and rationale

The Parent owns the actual driver and selected-invocation wiring. The separate
[collector record](CR-20261001-nginx-configtest-collection.md) describes artifact
verification at the source-collection boundary.
The companion Framework owns the explicit closed configuration contract and
receipt validation. The driver executes retained `nginx-binary` and
`nginx-module.so` snapshots under a fresh external root and supplies
`nginx.conf`, `stdout.log`, `stderr.log`, `source-result.json`, and one actual
raw record in `source-result.jsonl`. The five retained operation files are
bound by receipt digests; no native event is synthesized. `-e stderr` prevents
bootstrap logging through a cached compile-prefix path. Snapshot reads use
non-following regular-file descriptors with a 64 MiB bound per artifact;
captures share a 64 KiB bound and the operation has a 10-second deadline.

## Security impact

Symlink, checkout and reused output paths are rejected. Child execution uses
an explicit argument vector and minimal environment, with an optional explicit
library directory, not a shell or environment dump. Only matched allowlisted
diagnostic fragments enter the receipt; bounded raw logs remain external.
Expected rejection is not blanket nonzero-to-PASS conversion. No Framework
guardrail, native-event validator, Common event producer, or MRTS source is
weakened or changed by this Parent slice.

## Changed files

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh` (configuration wiring only;
  previously prepared protocol edits are excluded from this slice)
- `tests/test_nginx_configtest_driver.py`
- `tests/test_nginx_selected_configtest_wiring.py`
- `docs/testing-and-evidence.md` / `.de.md`
- This paired Change Record and archive index pair

## Commands executed

All shell validation uses RTK. The driver first failed dynamically without its
implementation; the retained-artifact assertion separately failed before
snapshot binding. The driver suite passes 12 tests, including expected
rejection, wrong exit/diagnostic, missing/symlink/oversized module, fresh and
checkout-path guards, bounded capture and timeout controls. The final combined
driver/collector command uses the existing Framework virtual environment:
`rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python -m unittest tests.test_nginx_configtest_driver tests.test_nginx_configtest_collection -v`.
This final combined rerun passes 18 tests in 12.304 seconds.
The task coordinator initially observed 18 selected-wiring tests, 6 collector
tests and 58 neighboring Parent tests passing. Its subsequent broader Parent
focus passes 186 tests in 57.106 seconds, including the 12 driver controls,
6 collector controls, 7 new configuration-wiring controls and neighboring
NGINX/path/lifecycle tests. The latest companion Framework focus passes 27
tests in 3.144 seconds, including the bounded secure-copy control; independent
review observes the same 27 passing in 3.651 seconds. The frozen No-CRS suite
passes 159 tests in 112.402 seconds with exit 0. Full Framework `make lint`
also completes with exit 0 (session 8526). Python
compilation and whitespace checks pass for the driver slice. RTK-wrapped
`make PYTHON=/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/.venv/bin/python check-bilingual-docs check-doc-links` passes with external
`TMPDIR`/`BUILD_ROOT` and the unchanged physical Parent Framework pin. The first
documentation check exposed missing exact German record headings/metadata;
they were corrected before the passing rerun. No unobserved result is reported
as green.

## Runtime evidence

The actual retained diagnostic
`runs/diagnosis/nginx-configtest-retained-jaYdBrvH`, under external task storage,
executes real NGINX. The positive case produces canonical `invalid_boolean`
PASS with observed exit 1 and the exact boolean diagnostic. The negative
control uses that actual executable with a controlled non-ELF module: exit 1
remains case FAIL with `unexpected_config_error`, not an expected rejection.
Framework finalization creates five managed artifacts for each control and
the strict check rehashes them. Both have zero native events and no daemon
startup or request execution. Source and canonical aggregates remain FAIL
because other required requests were deliberately not run. The strict checker
for `analysis/nginx-configtest-retained-check-20261001.json` exits 0. This
retained-build diagnostic is not exact-head full-lifecycle PASS.

## Checks not run and rationale

No full E2E, push, PR mutation, gitlink update, protocol run, or merge is
included. The full required-coverage gate is not green; independent
source-SHA/run binding is required before exact-head
claims. Root-master/nobody-worker checks are not applicable to `nginx -t`.
The Framework-specific Change Record checker applied to the Parent is
inapplicable: Parent records use the current Parent template and native
bilingual/path/link checks, not the different Framework headings. No historical
Parent records or validators are changed to make that cross-owner check pass.

## Known limitations

Only `invalid_boolean` is implemented by this initial contract. Nine other
configuration-related required records remain outside this slice; HTTP,
startup, reload and fault/protocol requirements are not fulfilled by this
receipt. The overall missing-path count requires a separate measured update.

## Remaining risks

The cached executable, module and explicit library directory must be trusted.
Receipts do not sign source identities: caller-provided SHAs need independent
run-provenance comparison. Snapshots bind executed bytes but do not establish
that a retained C build was produced from the current Parent source revision.

## Final diff and review status

This is a local bounded implementation under review. Prepared protocol work
remains uncommitted and outside the slice. Framework changes have separate
ownership; Parent Framework/MRTS gitlinks remain unchanged. No full-E2E PASS,
delivery or merge outcome is asserted.
