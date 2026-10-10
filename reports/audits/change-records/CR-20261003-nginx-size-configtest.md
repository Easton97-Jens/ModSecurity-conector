# Change Record: selected NGINX size configuration rejection

**Language:** English | [Deutsch](CR-20261003-nginx-size-configtest.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261003-nginx-size-configtest` |
| Date (UTC) | `2026-10-03` |
| Base revision | `b1dd58a1289a84f15903fa0bb46474cf776e67db` |

## Motivation and problem statement

The required `invalid_size` record lacked a concrete selected NGINX invocation.
The previously closed Boolean rejection cannot prove size parsing.

## Acceptance criteria

Execute `modsecurity_phase4_body_limit maybe;` with actual `nginx -e stderr -t`.
Require exit 1 and both exact size diagnostics; preserve FAIL for wrong-module,
Boolean-diagnostic, wrong-exit and receipt mismatches. Independent selected
cases need fresh separate bundles. Do not shrink required selection or claim
HTTP, startup, reload or full E2E.

## Implementation decision and rationale

Extend the existing bounded driver with two explicit case descriptors, not a
generic phase-0 exemption. Dispatch selected `invalid_size` into its own fresh
`configtests/invalid_size` directory. Keep the prior Boolean realization and
the existing collector contract. The companion Framework independently owns
catalog/receipt validation and case-specific canonical retention.

## Security impact

Keep non-following regular-file snapshots, 64 MiB binary/module limits,
64 KiB combined captures, 10-second deadline, explicit argument vector and
minimal environment. PASS still requires the exact directive/value, exit and
both parser fragments. No guardrail, validator, Common or MRTS is weakened.

## Changed files

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-selected-nginx-configtests.py`
- `tests/test_nginx_configtest_driver.py`
- `tests/test_nginx_selected_configtest_wiring.py`
- `docs/testing-and-evidence.md` / `.de.md`
- This paired record and archive index pair

## Commands executed

The coordinator observed a fresh RTK-wrapped Parent focus: 191 tests pass in
65.658 seconds, exit 0; retained log and exit receipt are
`analysis/parent-config-size-focus-20261003.log` and `.exit` under external task
storage. The focused driver/wiring checks passed 24 tests. Fresh RTK-wrapped
Parent `check-bilingual-docs` / `check-doc-links` and repository path checks
passed with the owning interpreter and external build/temp roots. Both
repositories' `rtk proxy git diff --check` passed. The separate companion
Framework No-CRS suite passed 166 tests in 111.503 seconds, and its public API
suite passed 23 tests in 28.847 seconds, each exit 0; these do not certify
Parent host execution. Complete Framework precommit `make lint` exited 0;
the user-required postcommit repetition is a separate later verification.
Parent Python compilation, shell syntax and error-level ShellCheck passed.

## Runtime evidence

The real producer → collector → canonical finalizer diagnostic
`runs/diagnosis/nginx-config-size-retained-6si2byjk`, below
`/var/tmp/codex/ModSecurity-conector`, produces individual `invalid_size` PASS
and wrong-module FAIL. Both actual NGINX invocations exit 1. Each has five
retained operation files; all eight canonical validators report zero errors.
All 47 retained checksums were verified. Both aggregates remain FAIL, with no
startup, requests or events. This is precommit source-dirty, retained cached
C-artifact evidence, not a new Exact-Head build or Full-Lifecycle proof.

## Checks not run and rationale

Full E2E, protocol wiring, Gitlink updates, pushes, PR mutation and merge are
excluded from this slice. Root-master/nobody-worker proof is inapplicable to
pure `nginx -t`. Postcommit Framework lint is tracked separately, not forecast
as a future PASS by this record.

## Known limitations

Only `invalid_boolean` and `invalid_size` have implemented closed configtest
realizations. Fresh `measure-nginx-config-size.py` revalidates actual bytes,
run identities, all eight validators and all 47 checksums: open paths decreased
52 → 51, configuration 9 → 8, with 97 required selected records unchanged.
This does not fulfill the remaining paths.

## Remaining risks

Trusted cached C inputs and independent source/run identity binding remain
necessary. Executed byte snapshots do not prove a new source-exact C build.
Eight configuration paths and other required scenarios remain unfulfilled.

## Final diff and review status

Independent security review found no blocker. The permanent shared-finalizer
test passed: two cases retain ten distinct manifest entries; cross-case aliases
and bundle reuse remain rejected. The final scoped diff passed review for a
separate local Parent commit. Existing protocol
changes are outside this slice and must remain unstaged. Parent gitlinks and
MRTS are unchanged. PR #396 remains OPEN/DRAFT/UNMERGED; no remote delivery or
Exact-Head E2E PASS is asserted. No secrets or raw logs are recorded here.
