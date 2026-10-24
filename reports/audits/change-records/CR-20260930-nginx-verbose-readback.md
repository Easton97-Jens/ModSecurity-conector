# Change Record: accept exact NGINX version with verbose build metadata

**Language:** English | [Deutsch](CR-20260930-nginx-verbose-readback.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-nginx-verbose-readback |
| Date (UTC) | 2026-09-30 |
| Base revision | `e14e2a7d2e3d6f4be8d7ff50d1e387d3e553fa8e` |

## Motivation and problem statement

Continue the owner's requested repair in PR #393. In
[run 36713711425, job 109881375276](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36713711425/job/109881375276),
both On/Off runtime cells passed before evidence publication failed.
The harness records `nginx -V`, while the writer required a one-line `-v`
readback. Compiler and configure metadata therefore caused a false rejection.

## Acceptance criteria

Accept the exact reviewed first version line with ordinary verbose build
metadata; reject wrong, missing, duplicated or conflicting version lines and
unexpected metadata. Preserve all existing evidence and publication checks.
Verify the successor commit through the existing hosted workflow.

## Implementation decision and rationale

Extract the byte parser into a small predicate. Keep the first line exact and
allow only printable compiler, TLS-build, SNI and configure metadata lines
after it. Metadata is still source-hashed, never copied into public evidence.
Two regressions exercise verbose success and malformed inputs in both modes.

## Changed files

`ci/runtime/lifecycle/write-nginx-functional-a-evidence.py`,
`tests/test_nginx_functional_evidence.py`, and this EN/DE record pair.

## Commands executed

An isolated in-process Python 3.13.5 unittest run used byte-verified current
writer/test sources and a minimal workflow-version fixture. The new verbose
success regression failed twice with the old writer. With the corrected
writer, all 11 tests passed with no failures, errors or skips. AST parsing
and whitespace checks passed. Uploaded source blobs are compared with those
tested bytes. This is not a full-checkout or local RTK test.

## Security impact

No version pin, source identity, policy, permission, sandbox, protected broker
or Sonar configuration changes. Wrong releases and matching prefixes remain
rejected. Bounds, safe file reads, identity checks, redaction, callback
validation, lifecycle markers and one-shot publication remain unchanged.

## Runtime evidence

The baseline hosted job proves the On/Off cells passed, but its publication
failed. A successful native run after this correction is not asserted here;
the successor workflow and PR readback must provide that evidence.

## Known limitations

Local GitHub DNS and the project RTK wrapper are unavailable. Full hosted CI,
native evidence publication and fresh Sonar results must be read for the
actual successor commit, not inferred from isolated tests.

## Remaining risks

A future upstream change to verbose metadata may require a reviewed parser
update. Unexpected lines are intentionally rejected rather than ignored.

## Checks not run and rationale

No local full-checkout build or native runtime execution because the required
checkout/tooling is unavailable. Existing hosted workflows are unchanged and
will independently validate the pushed commit.

## Final diff and review status

Scoped follow-up to the applied Framework and ModSecurity guard changes.
No merge, master push, force push or old local script execution is authorized.
