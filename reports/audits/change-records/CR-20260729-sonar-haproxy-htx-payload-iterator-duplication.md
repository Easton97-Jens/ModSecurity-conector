# Change Record: Parent HAProxy HTX payload-iterator deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-htx-payload-iterator-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-htx-payload-iterator-duplication |
| Date (UTC) | 2026-07-29 |
| Base revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Tracking | One current SonarQube Cloud CPD pair: two 35-line HTX request/response body-slice iterators. |
| Boundary | Parent HAProxy HTX overlay source and paired Change Record indexes. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The HTX filter had two structurally identical loops for request and response
payload slices. Both must retain HAProxy's current-buffer borrowing rule,
offset trimming, unsigned-size bounds, non-data-block accounting, and complete
`remaining` consumption. The only intended difference is the existing binding
entry point for the request versus response phase.

## Acceptance criteria

- A shared iterator preserves every input guard, offset, bound, borrowed-pointer,
  block-accounting, and return-value path from both former loops.
- Explicit request and response wrappers retain their existing names and select
  only their respective binding function.
- The HTX static lifecycle contract passes without weakening precommit deny,
  phase finalization, or forward-first behavior.
- Exact-head hosted checks and SonarQube Cloud still must prove zero New Issues,
  zero New-Code Duplicate Lines, and a lower total duplicate count.

## Implementation decision and rationale

The common iterator accepts a typed callback matching the two existing binding
APIs. The callback is validated before parsing begins and is called only after
the same existing HTX slice validation. The request and response wrappers pass
the existing phase-specific function directly. This removes duplication without
introducing a body buffer, changing ownership, or merging the distinct phases.

## Changed files

- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c` — one
  typed common payload iterator and two explicit phase wrappers.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `make check-haproxy-htx-overlay` | passed; all static HTX lifecycle, borrowed-slice, phase-finalization, host-action, and build-boundary controls passed. |
| `git diff --check` | passed. |
| Focused Codex Security diff scan | passed with zero reportable findings; the sealed report is at `/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/dbbc9c6-haproxy-htx-payload-20260729T052500Z/report.md`. |

## Security impact

This source processes HTTP-derived body chunks at an untrusted host-protocol
boundary. The refactor preserves the existing borrowed-pointer rule, rejects
the same invalid offsets and lengths, does not retain body bytes, and still
calls separate request/response binding APIs. No authorization, validation,
isolation, late-intervention policy, or Quality Gate control is relaxed.

## Runtime evidence

The static HTX lifecycle contract directly checks the version-pinned overlay
source. It is not a live HAProxy plus libmodsecurity runtime. No host-runtime
promotion or phase claim is made.

## Known limitations

- The local worktree does not contain a built HAProxy 3.2.21 source tree, so a
  full overlay compilation or runtime smoke is not available here.
- Hosted checks and a fresh exact-head SonarQube Cloud analysis are pending.

## Remaining risks

- The generic callback must remain limited to the two semantically compatible
  body-chunk binding functions; future use for any other phase needs a new
  lifecycle review.

## Checks not run and rationale

No live HAProxy/libmodsecurity HTX runtime or full connector matrix was run
because their version-pinned external source and runtime fixtures are not
present. The source contract is the strongest available local control.

## Final diff and review status

The candidate is confined to the Parent HAProxy overlay and bilingual
traceability. It removes one confirmed 70-line duplication pair. The local
review is complete; a separate Draft PR and exact-head hosted verification are
still required before any delivery or merge claim.
