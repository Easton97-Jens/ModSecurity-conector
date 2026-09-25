# Change Record: Native Apache adoption and live diagnostic alignment

**Language:** English | [Deutsch](CR-20260923-pr382-apache-adoption.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260923-pr382-apache-adoption` |
| Date (UTC) | `2026-09-23` |
| Base revision | `cac867da7292f6ca82fc76fee3b974382881c5b1` |

## Motivation and problem statement

The new Apache lifecycle collector was already implemented and its 20 compiled
APR/Common regressions passed. The scoped adoption guard still demanded the old
zero-result return that bypassed cleanup, and native redirect storage inside
the collector rather than its checked helper. This stale guard failed root
quick-check, Common, Apache and NGINX jobs after other guards had passed.

## Acceptance criteria

Accept the actual safe collector while rejecting missing cleanup, unknown native
values, wrong error classification, missing callback latch and post-commit header
mutation. Retain every other review guard, all existing mutation cases, compiler
warnings and Sonar zero/duplication gates. Do not change production behavior.

## Implementation decision and rationale

Reuse the existing comment/literal-masked function parser and redirect-storage
predicate. Add a scoped native-flow guard requiring ordered exact result checks,
first-cause handoff, the neutral result assignment and common cleanup tail. Only
one return after the native call is permitted; the tail must release buffers,
clear the callback latch and return the collected result directly.

Nine new isolated source tests reuse the existing checker fixture. Each negative
case requires exit one and its exact FAIL line. The existing adoption suite is
executed alongside them in the Apache job; no old test is removed or disabled.

## Changed files

Apache review checker, nine-case native adoption module, existing Apache workflow
and this paired report. The earlier single-line bootstrap diagnostic fix is
recorded separately below; no source or dependency changes in this checker slice.

## Commands executed

Required remote command, pending for this new commit:

```sh
python3 -m unittest -v tests.test_apache_common_adoption tests.test_apache_native_adoption
```

At base cac867da, job 107132681171 in run 35846145029 passed the eight cleanup
source cases, 20 actual APR/Common lifecycle cases and the real tracked-source
Apache module build, load and loopback smoke. The separate structure job failed
only its outdated native-intervention guard. Fresh integrated CI remains required.

## Security impact

The repaired guard strengthens post-native cleanup and typed-error checks; it
cannot be satisfied by a comment or constant-false decoy. The live bootstrap
retains 200/403 controls, invalid-ID 500 responses, Connection:close, exclusion of
the document handler and exactly two diagnostics. Its old diagnostic literal
was updated in cac867da to the real typed boundary's generic operation message.

## Runtime evidence

The baseline bootstrap is actual httpd/libModSecurity execution for those narrow
cases. Native fault injection controls engine calls and event emission, while
APR and Common collaborators are real. Mutation results are source-level proof.
Neither establishes every route, physical JSONL sink or late transport behavior.

## Known limitations

I09/I10 remain incomplete globally. Traefik's response-commit handler still uses
the void compatibility setter and returns success; that requires source repair
and failure injection, not only a live-host confirmation. Other routes remain
separate. The enforced Envoy tagged build is still pending at preparation.

## Remaining risks

Further integration tests may expose independent old assumptions. Preserve real
failures and all existing safeguards. Secret scanning remains an independent
blocker; a green Sonar analysis does not resolve it.

## Checks not run and rationale

No local repository execution; the sandbox cannot retrieve a full checkout.
Remote CI provides the execution path. New-head Sonar metrics and test results
must be read back before claiming success. RTK is not a remote-API/CI blocker.

## Final diff and review status

Draft PR #382 only. Preserve concurrent work, unchanged production source and
permissions. No merge, master/force push, release or deployment.
