# Change Record: Apache Phase-4 response enforcement

**Status:** PR #60 remains open and Draft. Its remote head is
`7c83583b4e208b8945daeec226d04abe364cbc8e`. The local delivery candidate is
based on the normal current-master merge
`93c5f30c181710f5c2cecf207fb92aaecb215035` and contains unpushed focused
Parent remediation. Historical remote checks apply only to `7c83583b4e208b8945daeec226d04abe364cbc8e`, not to the local candidate. Current exact-native validation has passed, but exact pushed-head CI, CodeQL, SonarCloud, review, thread, and protected-merge checks remain required. No merge is claimed.

**Language:** English | [Deutsch](CR-20260718-apache-phase4-response.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260718-apache-phase4-response |
| Date (UTC) | 2026-07-18; current evidence refreshed 2026-07-19 |
| Base revision | aabde81a9a315bf3e494e595ab0399357c596f9c |
| Scope | Parent repository only |
| Related finding | FND-PARENT-0038 |
| Related harness finding | FND-PARENT-0041 |
| Related capacity finding | FND-PARENT-0042 (locally fixed; delivery verification pending) |
| Framework / MRTS state | Parent gitlink `cdc91a398d6c156eaff927d742b23018a3817fb6`; MRTS gitlink `13aa91291adea12d5c607fdd165d010fcfb1da78`; no Framework, MRTS, or gitlink change |

## Problem and security invariant

Apache must not release a byte that Phase 4 can consider before
`msc_process_response_body` and its intervention resolve. A normal internal
redirect also cannot safely rebind the native transaction to the target URI,
rules, or request variables. Therefore an unsafe redirect must neither release
the protected response nor execute a target quick-handler or normal handler.

The only permitted redirect is one bounded local `ErrorDocument` transition:
Apache-core-derived `no_local_copy` and `REDIRECT_STATUS` evidence must match,
the shared Phase-4 state must be `EMITTING`, and the one-time permission is
bound to that exact request's fresh notes table.

## Current implementation

- `MODSECURITY_OUT` retains and normalizes every pre-EOS response brigade,
  performs the Phase-4 decision at EOS, and makes only one downstream release.
- `MODSECURITY_PHASE4_GUARD` remains in the protocol chain to seal later
  producer output after denial, EOS, or terminal failure.
- The redirect remediation adds an `APR_HOOK_REALLY_FIRST` quick-handler guard
  before Apache can invoke a target quick handler and an equally early normal
  handler fallback. Both return `DONE` for an unsafe `r->prev` request.
- The source sets a request-local permission note only after the existing
  core-shaped local-`ErrorDocument` proof succeeds. A later nested or normal
  redirect receives a new notes table and cannot inherit that allowance.
- To bound retained APR-object/setaside overhead as well as payload bytes, it
  counts normalized buckets across filter invocations; at 4,096 held buckets it
  fails closed before retaining another bucket, and resets the count on release
  or discard.
- No Framework, MRTS, or gitlink change is part of this repair.

## Current exact-native evidence

The task-owned external read-only copy of the Parent-recorded Framework commit
`cdc91a398d6c156eaff927d742b23018a3817fb6` built Apache connector component
`904cb576c6a344cb38f330d5842fe750fafc81041c459ce0dfcda4a75eabfbc3`.

The first exact target-handler control reproduced the incomplete redirect
closure: its H1 run exited `1`, and the retained log recorded both the
connector refusal and `ModSecurity Phase4 redirect target handler executed`.
The focused source repair was then rebuilt against the same exact Framework
revision.

The post-fix `redirect-target-handler-abort-h1` and
`redirect-target-handler-abort-h2` controls both passed. Their logs retain the
expected connector refusal and no target-handler marker. A serial 30-control
exact native matrix then exited `0`, covering deny, allow, log-only,
client-abort, empty responses, body limits, custom MIME, ProcessPartial,
redirect refusal, target configuration and URI variants, target-handler H1/H2,
upstream/downstream/nested/pre-output `ErrorDocument`, and H1/H2 late-producer
and Phase-3-header controls.

The final local security-diff validation additionally reproduced a distinct
availability condition: before the focused capacity repair, an actual Apache
handler released 4,097 one-byte response buckets (4,097 bytes, far below the
one MiB payload cap) as HTTP 200. The current rebuilt module rejects the same
4,097 buckets split over two filter calls with a pre-release HTTP 500 and a
specific bucket-limit diagnostic. Its 4,095-data-bucket-plus-EOS boundary
releases HTTP 200 with exactly 4,095 bytes. The serial safe matrix was rerun
with those two new controls and all 32 modes passed.

The earlier sealed 30-mode redirect receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260719T162259Z-pr60-exact-head-revalidation-dfba422e/evidence/pr60-exact-native-phase4-manifest.json`
with SHA-256
`1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548`.
It records the pre-fix log, post-fix H1/H2 logs, component manifest, rebuilt
module, command result, source state, and its 30-mode matrix scope.

The retained local security-diff validation for the 32-mode bucket rerun is
`/var/tmp/codex/ModSecurity-conector/runs/20260719T183551Z-pr60-final-security-diff-93404fdd/evidence/security-diff/artifacts/05_findings/CAND-PR60-001/validation_report.md`
with SHA-256
`79e7e1b3fcca6acdf8d02ed941eaadcea566258656abe269a54289a59e88db8c`.
It records the split-overflow and boundary logs and the 32-mode matrix driver;
it is retained local validation, not a sealed receipt.

Focused static validation also passed:

- `tests.test_apache_phase4_response_regression_wiring`: 10/10;
- shell syntax for the Phase-4 runner and Apache harness;
- `git diff --check`; and
- a full uninstalled Apache-module build against the exact Apache, APR, and
  libModSecurity headers.

## Evidence limits and remaining delivery gates

Historical prior-head runtime observations are not current exact-head evidence:
central artifacts were missing or unsealed and remain described only in
FND-PARENT-0038. The current matrix is the authoritative local native result.

There is no repository-native Apache Phase-4 ASan/UBSan route; the Common
allocator micro-smoke is not presented as Apache sanitizer evidence. The CRS
control is blocked by the current Framework provenance guard after it detects
the approved source's `.gitmodules`; that control was not bypassed. The MRTS
profile is not claimed as current until it runs from a task-owned read-only
materialization.

Before PR #60 can be readied or merged, the final local diff requires a fresh
Codex Security diff scan, and the pushed exact head requires terminal required
checks, CodeQL, SonarCloud, review/thread evidence, protected merge, and
resulting-master verification. The user authorized safe master integration,
not a bypass of any of these gates.
