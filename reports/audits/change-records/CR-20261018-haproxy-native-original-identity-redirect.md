# Change Record: CR-20261018-haproxy-native-original-identity-redirect

**Language:** English | [Deutsch](CR-20261018-haproxy-native-original-identity-redirect.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-native-original-identity-redirect |
| Date (UTC) | 2026-10-18 |
| Base revision | `fc7e0d25c6ed3240d6e257e92f25475e63f150c8` |

## Motivation and problem statement

All 80 prepared original native fixtures had observer labels differing from their original IDs. Global substring replacement also corrupted the selected receipt ID of `NEED-request-eos-once`. The named P3 fixture still declared 503 despite the source requirement for 302 and Location.

## Acceptance criteria

Bind full original IDs exactly once in observer CASE and selected receipt; preserve all 112 native original contracts and oracles plus the frozen 278-row inventory; derive P3 expectations independently; preserve sequence vectors and socket behavior; retain older snapshots. New fixture roots remain unsealed for Root review.

## Implementation decision and rationale

Context-specific exact-once anchors replace substring rewriting. The original named `NEED-p3-redirect` now uses `phase3_redirect_before_commit`, canonical rule `1100202`, and its YAML declaration: status 302 and `https://no-crs.invalid/phase3-redirect`. The client requires exactly one matching Location on main and no Location on neighbor. No P4 body predicate is declared for this P3 redirect. HAProxy 3.2.25 public `http_apply_redirect_rule` and current product source are separately hashed in the review receipt. Sequence preparation accepts only the contract-bound original allow base with known legacy `NEED-allow` or full original CASE; missing, repeated, mixed, or unknown anchors fail.

## Changed files

`connectors/haproxy/harness/i12_native_cases.py`, `connectors/haproxy/harness/i12_native_contracts.py`, `connectors/haproxy/harness/i12_native_sequences.py`, `tests/test_haproxy_i12_native_cases.py`, `tests/test_haproxy_i12_native_sequences.py`. This EN/DE record accompanies the focused harness and test changes. Existing source-descriptor and runtime socket-cleanup guards remain intact.

## Commands executed

Here `R2` denotes the external acceptance run. `rtk proxy R2/test-env/bin/python -m pytest -q tests/test_haproxy_i12_native_cases.py tests/test_haproxy_i12_native_sequences.py` passed 41 tests and 9 subtests on CPython 3.14.7; exact argv, exit and raw-output hashes are in `R2/commands/haproxy-native-v8-components-final-20261018.json`. Preparation receipts: `native-originals-prepare-v8-pinned-20261018`, `native-sequences-prepare-v5-final-20261018`. Comparison receipt: `native-v8-review-final-20261018`, exit 0. Earlier relative-path and wrong-capture attempts failed and remain retained; a command naming a nonexistent separate contracts test exited 4, then the actual two-file suite passed.

## Security impact

This repairs evidence identity and independently declared client expectations. It changes no product, shared capture, original inventory, authorization, isolation, or physical observer. Component success adds no lifecycle PASS.

## Runtime evidence

No hosts ran in this subtask. `R2/native/original-fixtures-v8` contains 80 original fixtures; `R2/native/sequence-fixtures-v5` contains two sequence fixtures. Both root directories are mode 0700 pending Root approval; member files retain producer sealing. `R2/native/identity-redirect-v8-review/review.json` and `native-v7-v8.diff` bind comparisons and independent source hashes. Native plan SHA256: `fbd1f780f5122eca0beed5e5a19278208644aa3b8f883e49496d38b767c3ae36`; sequence index: `8ebf64383be8a360d1fd9b5e32c51bf2e11cbbd5f32aa41639c9d964d3f741e0`; native diff: `29a12a7b4a6df6b56159ca53ac6a93119d355d0e3213109c77ce933163c6bb68`.

## Known limitations

Declared P3 expectations derive from rule/YAML and the public host API, not from measured status. Actual commit, client transport, EOS, logging, Finish and Free still require fresh independently observed hosts. Historical labels and evidence are preserved without rewriting.

## Remaining risks

Root must reconcile the new fixture diff and source bindings before sealing and execution. A real host failure must remain a failure. Shared requests must never be credited as independent native, SPOP and companion runs.

## Checks not run and rationale

No builds, host execution, Git delivery, CI or Sonar were run by this worker; Root owns those actions. This subtask prepares source-bound fixtures and component validation only.

## Final diff and review status

The worker reviewed the five focused source/test diffs and both complete language records. Source and fixture hashes are handed to Root. Root review, sealing, commits and host retakes remain pending; no merge or force push is authorized.
