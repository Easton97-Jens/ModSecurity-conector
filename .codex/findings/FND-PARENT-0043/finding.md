# FND-PARENT-0043 — Apache intervention buffers require request-owned copies before native cleanup

## Classification

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0043` |
| Category | `security_validated` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity | `P2` / `medium` |
| Confidence / status | `validated` / `blocked` |
| Feasibility | source correction merged through PR #72; native verification `blocked_environment` |
| Release blocker | no |
| Security relevant | yes |
| Source base / exact PR head | `929fe60dfca30787947027e5bd49003581a5b080` / `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` |
| Delivery state | PR #72 squash-merged as Parent master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`; exact resulting-master Actions passed, native verification remains blocked |

## Summary and security invariant

`process_intervention()` bridges libModSecurity-owned `url` and `log` buffers
into Apache request state. For every nonzero `msc_intervention()` result,
Apache must first copy each retained value into `r->pool`, then call
`msc_intervention_cleanup()` exactly once. `apr_table_setn()` must never retain
`intervention.url` directly. The zero-result path directly returns
`N_INTERVENTION_STATUS` and performs no cleanup.

This is a request-facing native lifetime boundary: a remote request that
satisfies a configured disruptive rule can reach it without local privilege.

## Observed behavior, cause, and impact

At source base `929fe60dfca30787947027e5bd49003581a5b080`,
`process_intervention()` passed `intervention.url` directly to non-copying
`apr_table_setn()` and returned without a nonzero cleanup funnel. Its missing-
log fallback also assigned a static literal into `intervention.log`.

The read-only shared libModSecurity source states that nonzero intervention
results initialize their fields and that `msc_intervention_cleanup()` frees
both `url` and `log`. Apache therefore cannot safely retain either native
pointer through cleanup: direct cleanup would leave a dangling `Location`
value, and freeing a fallback literal would be invalid. The base source avoids
the immediate dangling pointer only by leaking the native buffers rather than
by establishing an ownership transfer.

Final PR #72 head `486aef56424f5bf33bcd7396f6dc2f881f7f3bdd` copies the log
and redirect URL into `r->pool`, retains the fallback only in a local variable,
directs every nonzero result through one cleanup label, and preserves the
direct zero-result allow return. It was normally squash-merged as Parent
master `0e8be81d14ee9a6ae0497b9ab67e58ba2def1fd3`. Its test-only follow-up
removed the task-owned SonarQube Cloud `python:S8786` issue without a
suppression.

The current evidence supports a medium-impact memory-lifecycle and response-
integrity finding. Native exploitability and sanitizer behavior remain
unverified because the required Apache/APR/libModSecurity environment is not
available.

## Reproduction and evidence

Preconditions are a valid Apache request and transaction, a nonzero
`msc_intervention()` result, and a disruptive rule path. A redirect result
supplies a 3xx status and URL; logging may supply or omit a log buffer.

- Final payload-safe receipt: run
  `20260720T225753Z-apache-intervention-cleanup-40c97373`, artifact
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-final-local-validation-20260720T232020Z.json`,
  SHA-256 `349f0a11ed98ad68bf3cbd881599bf7381aba253462113d42e7cf948ed7bf1b6`.
  It was retained by
  `rtk run '/root/git/ModSecurity-conector/.codex/bin/storage-budget retain-evidence ...'`
  from `/root/git/ModSecurity-conector`, exit `0`, observed
  `2026-07-20T23:20:20Z`, retention `retained_local_evidence`.
- The receipt records `rtk make check-apache-intervention-cleanup` passed five
  source-contract tests; `rtk make check-apache-c-standard-wiring` passed;
  `rtk env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_apache_request_transaction_cleanup tests.test_bilingual_docs`
  passed 16 tests; `rtk git diff --check` passed; and an independent focused
  security diff review found no local delivery blocker.
- The same receipt records the native limits accurately:
  `rtk make check-apache-request-transaction-cleanup` first passed five Python
  assertions, then lacked `apxs`/usable Apache headers and returned `2`;
  `rtk run 'APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/apache-c17 make check-apache-c17'`
  was blocked before compilation by unavailable Apache/libModSecurity
  prerequisites and returned `2`.
- Read-only upstream ownership evidence is `src/transaction.cc`, SHA-256
  `b148564757d12e9bbe55c65df26d6465d662cb4213a7cd90e9ad4aa9a4a929a7`,
  and `headers/modsecurity/intervention.h`, SHA-256
  `42eca68546bb2a1172b6d5d35c00d5e9aaa2c0649cbacb0cf984bb2a0645fd1d`.
  The RTK-proxied hash inspection exited `0` at `2026-07-20T23:11:09Z`.
- Current PR and Change Record receipt: artifact
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-pr72-c761-validation-20260720T234605Z.json`,
  SHA-256 `51f57e94617426d9e811b015cd2baae57631a9799741ec31831cd69edf9551bd`.
  It records that exact PR #72 head `c761a13` had six required checks passed,
  SonarQube Cloud Quality Gate passed, zero new issues/hotspots, and `0.0%`
  duplication. It also records five focused source-contract and eleven
  bilingual-documentation unit tests passed after the local EN/DE Change
  Record correction; full documentation and native checks remain blocked.
- Resulting-master receipt: artifact
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-pr72-master-validation-20260721T000550Z-final.json`,
  SHA-256 `667e2642b90988cf25096ab96c176f6af66f22bb873b3eb6e937d8dc72a1b9f3`.
  It records final head `486aef`, normal squash merge #72 at
  `2026-07-21T00:01:04Z`, resulting master `0e8be81`, equal PR/master trees,
  and 14 successful resulting-master GitHub Actions workflows. The final PR
  Quality Gate passed with no task-owned new Sonar issue or hotspot. Sonar
  master remains `ERROR` only for proven pre-existing backlog; no scanner or
  quality-gate control was changed.
- Final exact-head local-validation receipt: artifact
  /var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/evidence/apache-intervention-final-pr-head-local-validation-20260721T002300Z.json,
  SHA-256 e75d97615af04cca6c26b40c61946660e5b83a5554e6c814790545b38f89a20e.
  At final PR #72 head 486aef, five Apache intervention-ownership contracts,
  Apache C-standard wiring, five request-transaction-ownership tests, eleven
  bilingual-documentation tests, and `git diff --check` passed. It does not
  create native-runtime evidence; that prerequisite remains blocked.

## Required remediation and acceptance criteria

1. The zero-result path returns `N_INTERVENTION_STATUS` directly, without
   cleanup.
2. Every nonzero result reaches exactly one cleanup after request-owned copies
   of every Apache-retained log and redirect URL.
3. `apr_table_setn()` never receives `intervention.url` directly, and fallback
   handling never assigns a static literal to `intervention.log`.
4. Redirect and nonredirect status results keep their intended semantics.
5. Focused source, C-standard-wiring, transaction-ownership, documentation,
   diff, final-PR-head, and Sonar controls pass without weakening any scanner,
   compiler, or test control.
6. A provisioned Apache/APR/libModSecurity environment repeats native compile,
   disruptive redirect/nonredirect, allow, missing-log, and available
   ASan/LSan controls.
7. The corrected EN/DE Change Record pair is included in final PR head
   `486aef`; resulting-master Actions and causal Sonar/Code-Scanning readbacks
   complete before verification or closure.

The focused regression is `tests/test_apache_intervention_cleanup.py`; the
existing non-duplicate transaction control is
`tests/test_apache_request_transaction_cleanup.py`. Legitimate controls cover
the direct zero return, nonredirect status after cleanup, request-owned
redirect storage, and a missing-log fallback safe to clean.

## Boundaries, blockers, uniqueness, and residual risk

This finding is `blocked`, not `fixed`, `verified`, or `closed`: the source
correction, test-only Sonar hardening, and corrected EN/DE Change Record were
delivered by PR #72, with exact-head and resulting-master evidence. The
stricter security workflow forbids a `fixed` outcome while relevant native
verification is unknown. Native validation is still `blocked_environment`:
Apache APXS, usable development headers, a compatible libModSecurity
runtime/headers, and a sanitizer-capable test environment are unavailable.
Sonar master is `ERROR`, but the immediately prior master was already failed
and the exact PR gate passed with zero new task-owned issues or hotspots; it is
unrelated backlog, not a passing master Sonar result. Six current GitHub
Code-Scanning rows are likewise pre-existing Scorecard leads unrelated to this
Apache change. Framework, MRTS, gitlinks, dependencies, and scanner controls
remain unchanged.

This is not a duplicate of the generic Apache request-transaction cleanup
contract, which owns `msc_t`/`msc_cleanup_request_transaction`; this finding
owns `ModSecurityIntervention.url`/`.log` lifetime across
`process_intervention()` and APR response retention. It is also distinct from
the Phase-4 response-commit boundary `FND-PARENT-0038` and the harness CLI
contract `FND-PARENT-0041`.

The corrected code is on Parent master, but native runtime and sanitizer proof
remain unavailable. A deployment-specific lifecycle or integration defect could
therefore remain undiscovered despite the focused source invariant, legitimate
controls, PR checks, and resulting-master GitHub workflow evidence. No risk
has been accepted.

## History

- `2026-07-20T23:20:20Z` — Final local source validation receipt retained:
  direct zero behavior, exact-once nonzero cleanup, focused controls, and
  independent review recorded; native runtime validation remains blocked.
- `2026-07-20T23:22:52Z` — Canonical Parent finding allocated after
  deduplication. This record update made no product, Framework, MRTS, gitlink,
  Git, or delivery change.
- `2026-07-20T23:43:04Z` — PR #72 exact head advanced to `c761a13`; six
  required checks and the SonarQube Cloud Quality Gate passed with zero new
  issues/hotspots and `0.0%` duplication. The PR remains Draft/open with no
  submitted review or resulting-master result.
- `2026-07-20T23:46:05Z` — The EN/DE Change Record pair was corrected locally
  to match the direct zero-result return. Five source-contract and eleven
  bilingual unit tests plus `git diff --check` passed; full documentation and
  native checks remain blocked. No Change Record commit, push, PR update, or
  merge occurred.
- `2026-07-21T00:00:58Z` — Corrected the finding outcome from `fixed` to
  `blocked`: the source correction and exact-head Sonar result remain valid,
  but native Apache/APR/libModSecurity and sanitizer verification is still
  unavailable.
- `2026-07-21T00:05:50Z` — PR #72 final head `486aef` was normally
  squash-merged as Parent master `0e8be81`; its tree matches resulting master
  and all 14 observed master GitHub Actions workflows passed. The final PR
  Sonar gate passed with no task-owned new issue or hotspot. Current master
  Sonar failure and six Scorecard Code-Scanning rows were independently shown
  to predate and be unrelated to this change.
- `2026-07-21T00:26:43Z` — Retained the lifecycle state as `blocked`:
  delivery and resulting-master evidence now exist, but the stricter security
  workflow forbids `fixed` while native Apache/APR/libModSecurity and sanitizer
  validation remain `blocked_environment`. The finding is not verified or
  closed.
- `2026-07-21T00:28:49Z` — Linked the retained final-PR-head local validation
  receipt for `486aef`: focused Apache intervention, C-standard wiring,
  request-transaction ownership, bilingual-documentation, and whitespace
  controls passed. This adds no native-runtime claim; the finding remains
  `blocked`.
