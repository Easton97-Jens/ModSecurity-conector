# Change Record: CR-20261010-nginx-first-byte-snapshot-binding

**Language:** English | [Deutsch](CR-20261010-nginx-first-byte-snapshot-binding.de.md)

Focused collector repair; fresh runtime confirmation remains pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261010-nginx-first-byte-snapshot-binding |
| Date (UTC) | 2026-10-10 |
| Base revision | `b0d75ef6bbc33228423aef65d8ea3409387ab30f` |

## Motivation and problem statement

The historical Full97 on `dca17fd5690c2ec2b8806024d1061744db8c3ad8` had 80 Case-PASS, nine FAIL and eight NOT_EXECUTED. The host snapshot was taken after upstream release; its final counters were merged into every Phase-4 event.

## Acceptance criteria

Capture counters at the paused first byte, bind exact invocation/event bytes, retain later counters, and reject mismatches.

## Implementation decision and rationale

NGINX captures host metadata and barrier evidence before upstream release. A separate metadata-only receipt binds original paused bytes, log prefix, event index/hash, transaction, snapshot hash and exact paths. Only the unique matching append is enriched; later events retain their own counters. Apache behavior remains unchanged.

## Changed files

`ci/lib/first_byte_binding.py`, `ci/runtime/lifecycle/collect-no-crs-source.py`, `ci/runtime/lifecycle/write-first-byte-host-metadata.py`, `ci/runtime/lifecycle/write-first-byte-source-results.py`, `connectors/nginx/harness/run_nginx_smoke.sh`, `tests/test_nginx_first_byte_binding.py`, this EN/DE record pair.

## Commands executed

`rtk proxy env PYTHONNOUSERSITE=1 /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.test_nginx_first_byte_binding tests.test_no_crs_outcome_projection tests.test_collect_no_crs_source_helpers tests.test_collect_no_crs_source tests.test_native_first_byte_shell_environment`: 86 tests passed, exit 0. Initial B RED exit 1 reproduced post-release capture and the missing bound-merge API.

## Security impact


No validator, privacy allowlist, Required scope or product semantics weakened. No response payload is retained in the receipt. MRTS unchanged.

## Runtime evidence

Historical R13 is unchanged. Offline fixtures are not a new runtime run. Fresh real bounded focus and integrated-SHA evidence remain coordinator-owned and are not yet claimed here.

## Known limitations

Unit regressions are not Full97 or protected Exact-Head proof. Tests ran against the uncommitted source overlay on the base revision, not as exact-head runtime. Listed test payloads were executed inside `rtk proxy bash -c` with log/exit capture. Python compilation, shell syntax, Change Record structure and `git diff --check` passed. ShellCheck with `--severity=warning` reported the same seven existing warnings on baseline and changed harness, both exit 1; no suppression.

## Remaining risks

Fresh First-Byte focus must verify pause ordering, full Safe response, exact snapshot assignment, roles and cleanup. Receipt ordering uses observed file timestamps in addition to hashes and exact paths.

## Checks not run and rationale

New Full97 is not authorized. Protected/admin operations are out of scope. Full lint, fresh CI/Sonar and publication are not claimed by this worker.

## Final diff and review status

Focused source changes prepared for independent review and separate commit. No commit, push, merge, retarget or Undraft performed by this worker.
