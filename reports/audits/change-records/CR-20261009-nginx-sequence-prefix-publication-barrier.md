# Change Record: CR-20261009-nginx-sequence-prefix-publication-barrier

**Language:** English | [Deutsch](CR-20261009-nginx-sequence-prefix-publication-barrier.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-sequence-prefix-publication-barrier |
| Date (UTC) | 2026-10-09 |
| Base revision | `fabc2b7b436cf1fe276a4fc681e8edc1221145b7` |
| Framework revision | `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9` |
| MRTS revision | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |

## Motivation and problem statement

The genuine R12 Full97 lifecycle reached real Root-master/nobody-worker traffic but stopped at `keepalive_after_strict_new_connection` before its second request. The Parent fixture wrote the initial HTTP headers and prefix through an unbuffered `SocketWriter`, then set `prefix_sent` only after `flush()`. The client could therefore observe valid headers first and reject them as `client headers preceded the upstream prefix`.

## Acceptance criteria

The publication event must happen before the initial header/prefix write can become client-visible. Initial write or flush failure must clear that event and skip the marker barrier. Suffix failures, barrier timeout, pre-publication callbacks and follow-up requests must retain their existing fail-closed behavior. Framework validators, Required selection, product source, Root/nobody controls and MRTS remain unchanged.

## Implementation decision and rationale

For late-response fixtures, the Parent upstream arms `prefix_sent` immediately before the unbuffered initial write. It clears the event if that write or its flush fails, and enters `send_marker()` only after both complete. Marker write failures retain the successfully published prefix while leaving `marker_sent=false`. This creates the required happens-before relation without waiting in the client, which could deadlock while the deliberately large backpressure prefix is still inside `sendall()`.

## Changed files

- `ci/runtime/lifecycle/nginx_sequence_upstream.py`
- `tests/test_nginx_sequence_upstream_barrier.py`
- `reports/audits/change-records/CR-20261009-nginx-sequence-prefix-publication-barrier.md`
- `reports/audits/change-records/CR-20261009-nginx-sequence-prefix-publication-barrier.de.md`

## Commands executed

Commands ran through RTK. Parent commands ran from the Parent worktree; the unchanged Framework validator command ran from the exact Framework worktree:

```sh
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_nginx_sequence_upstream_barrier.py -v
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_nginx_sequence_*py' -v
rtk run -- env PYTHONDONTWRITEBYTECODE=1 FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 python3 -m unittest -v tests.test_nginx_dispatch_routes tests.test_nginx_driver_contract_tables tests.test_nginx_begin_driver_evidence tests.test_nginx_sequence_client tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases tests.test_nginx_sequence_transport tests.test_nginx_sequence_upstream_barrier
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.no_crs.test_nginx_lifecycle_sequence
rtk run -- env PYTHONDONTWRITEBYTECODE=1 python3 -c 'from pathlib import Path; [compile(Path(name).read_bytes(), name, "exec") for name in ("ci/runtime/lifecycle/nginx_sequence_upstream.py", "tests/test_nginx_sequence_upstream_barrier.py")]'
rtk run -- shellcheck ci/runtime/lifecycle/run-no-crs-baseline.sh
rtk run -- python3 ci/tools/new-change-record.py check
rtk make check-bilingual-docs PYTHON=python3
rtk make check-doc-links PYTHON=python3 FRAMEWORK_ROOT=modules/ModSecurity-test-Framework
rtk run -- env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/validation/r12-sequence-race-lint PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/framework-nginx-seven-contracts-20261008 FRAMEWORK_PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/validation/r12-sequence-race-lint/apache-c-standards make lint
rtk git diff --check
```

The authoritative focused RED ran ten tests and produced exactly two errors at the callback-during-write and callback-during-flush controls. After the source correction, the expanded sequence suite passed 51/51. The explicit-Framework-root Parent contract suite passed 64/64, and the Framework's unchanged strict sequence validator passed 18/18. Python compilation, the actual shell-wrapper ShellCheck, Change Record structure, bilingual documentation, link checks and `git diff --check` passed. Full Parent `make lint` terminated with exit 0 when all output roots were supplied as environment variables under `/var/tmp/codex`.

Three non-source invocations are retained rather than relabelled: the Parent venv has no `pytest`; ShellCheck against the Python driver returned `SC1071`; and two early lint attempts used first a blocked legacy output root and then command-line `BUILD_ROOT`, whose `MAKEFLAGS` propagation prevented synthetic tests from selecting their private roots. The corrected repository-native invocations above all passed without a source workaround.

## Security impact

No security check is relaxed. Early callbacks are still rejected unless the exact upstream publication has been armed; initial output failure clears that authority and is retained as `upstream_write_failed`. Path authority, projection freshness, Root/nobody isolation, evidence validation and Required scope are unchanged. No secrets are recorded.

## Runtime evidence

R12 remains an immutable terminal FAIL: supervisor exit 2, native Make exit 2 and no Canonical `result.json`. Its inner and outer SHA256 ledgers revalidate under actual root, its failed case records Root master and nobody worker identities plus successful cleanup, and no host nginx remains. Unit tests do not relabel R12 or establish a corrected Full97 PASS.

## Known limitations

The fixture event denotes that publication is armed immediately before the unbuffered write; successful final evidence still requires no write failure and actual client/native observations. No corrected exact-head Full97 run is claimed by this change record.

## Remaining risks

A fresh source-bound Root-master/nobody-worker lifecycle is still required to prove the corrected interleaving with NGINX 1.31.6 and to produce a Canonical result. Existing R12 evidence cannot satisfy that requirement.

## Checks not run and rationale

No fresh post-fix build, Full97 lifecycle, protected workflow or current-head remote CI/Sonar has run. The closure is intentionally limited to the established Parent race; no unrelated defect work is opened.

## Final diff and review status

The final pre-commit diff is limited to one Parent fixture, its deterministic regression controls and this EN/DE record. Framework and MRTS Gitlinks remain unchanged. Independent test, documentation and security reviews report GO with no blocker, and the final local validation is green. A separate commit and normal remote readback remain required; PR #396 remains Draft.
