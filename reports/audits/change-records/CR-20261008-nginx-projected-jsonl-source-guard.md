# Change Record: CR-20261008-nginx-projected-jsonl-source-guard

**Language:** English | [Deutsch](CR-20261008-nginx-projected-jsonl-source-guard.de.md)

Bounded static Source-checker correction; product Source unchanged.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-projected-jsonl-source-guard |
| Date (UTC) | 2026-10-08 |
| Base revision | `8004340da887d143bc5e850822ac122eb5ce8b59` |

## Motivation and problem statement

The Source now projects a bounded URI before Common serialization; a stale literal search crashed with ValueError.

## Acceptance criteria

Accept the actual active projected-event pipeline, reject bypasses/decoys and preserve warning-only request and strict phase tails.

## Implementation decision and rationale

Use lexical function extraction and a full ordered pipeline check; missing helpers fail closed without an import traceback.

## Changed files

Only the NGINX adoption checker, its unit tests, and this generated EN/DE record pair.

## Commands executed

RTK-wrapped Parent Python ran three focused tests: all passed (27.899 s). Actual checker CLI exited 1 with both URI assertions PASS; independent residual guards remain FAIL.

## Security impact

No product Source or runtime behavior changed. Active raw-event serialization, projection bypass, early writes and success-on-failure remain rejected.

## Runtime evidence

None: synthetic Source mutation tests and static checker CLI are not runtime evidence.

## Known limitations

Seven independent residual assertions remain red: explicit standard-header dependency whitelist and exact timing declaration boundary; detailed external residual report records each cause.

## Remaining risks

Whole adoption gate is not green yet; the separately authorized dependency/declaration follow-up remains required.

## Checks not run and rationale

No build, native runtime, full lint, installation, push or MRTS mutation; this is a bounded Source-checker slice.

## Final diff and review status

Reviewed scoped diff; URI-only focused validation passed. Full existing suite was invoked; its residual baseline results are retained externally and follow-up must reconcile them.
