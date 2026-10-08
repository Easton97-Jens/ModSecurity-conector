# Change Record: CR-20261008-nginx-event-boundary-driver

**Language:** English | [Deutsch](CR-20261008-nginx-event-boundary-driver.de.md)

Local source implementation; integrated native validation remains pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-event-boundary-driver |
| Date (UTC) | 2026-10-08 |
| Base revision | `bc9587f086b1e4ff558a870f2d5020aa22f72b64` |

## Motivation and problem statement

Two Required event records need true phase1 rule1100402 callbacks and fixed source-bound URI/writer limits, including independent at255 and over256 requests.

## Acceptance criteria

Closed nonsensitive long query and exact boundary inputs; actual rule/pass events, HTTP200, explicit truncation/redaction, bounded payload-free JSONL and independently sealed child artifacts. Native execution remains coordinator work.

## Implementation decision and rationale

A thin adapter reuses run_operation and real request-header/callback-selection hooks. Each child gets a fresh output/projection root and run identity. The aggregate seals exact child receipt bytes and source identities. Limits are fixed NGX URI256 and writer4096 source constants, not invented configurable directives. The callback is request_rule_match/pass, not a log_only intervention.

## Changed files

ci/runtime/lifecycle/run-nginx-event-boundary-cases.py, tests/test_nginx_event_boundary_driver.py and this EN/DE pair. Shared runtime and Root event projection remain separately owned dependencies.

## Commands executed

RTK-wrapped Parent-owned Python `-m unittest discover -s tests -p 'test_nginx_event_boundary_driver.py' -v`:3 pure tests passed, exit0. No listener or native process was started. Final record/diff checks are recorded in the external coordinator handoff.

## Security impact

No Required shrinking or Common validator changes. Inputs are nonsensitive; events require query redaction and exclude body/query payload. Canonical readers must safely reopen sealed receipts/raw children and authenticate actual source/build/process identity.

## Runtime evidence

No native run or module build occurred for these cases. Unit observations demonstrate helper invariants only. The adapter preserves NOT_EXECUTED until canonical validation.

## Known limitations

Requires shared C runtime hooks and Framework event-boundary helper before invocation. Catalog configured-limit wording must be reconciled to fixed source constants by Root; no configurable product limit exists.

## Remaining risks

Actual projected native URI/flags, at/over callbacks, real header-trigger and fresh module/artifact identity remain unverified pending coordinator slot.

## Checks not run and rationale

Native runtime/build, integrated canonical97, full Parent suite and remote CI/Sonar await Root integration/serialized runtime authority. Full Parent bilingual target retains missing Framework-submodule link limitation in this isolated worktree.

## Final diff and review status

Only new delegated adapter/test/ENDE files; local commit without push/Gitlink/merge/MRTS changes. Runtime outcome partial.
