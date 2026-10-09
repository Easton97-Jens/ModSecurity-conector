# Change Record: CR-20261009-nginx-native-receipt-single-write

**Language:** English | [Deutsch](CR-20261009-nginx-native-receipt-single-write.de.md)

Publish each native child receipt exactly once after all source-bound fields
have been assembled.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-native-receipt-single-write |
| Date (UTC) | 2026-10-09 |
| Base revision | `e5e8569eaf0f0ce1cdc8b56e3181d872d03eb9a8` |

## Motivation and problem statement

The genuine R8 NGINX lifecycle completed sixteen smoke cases, the synchronized
first-byte probe, six native cases and the first event-boundary request with a
Root master, nobody worker, HTTP 200 and verified cleanup. It then stopped
because the event adapter tried to add `variant` and `request_headers` by
rewriting an already published `source-result.json`. The exclusive freshness
guard correctly rejected the second write with `EEXIST`; the MIME adapter
contained the same latent post-publication pattern for its source digests and
fixture hash.

## Acceptance criteria

Preserve one exclusive receipt publication, existing-file rejection and all
path, ownership, symlink and bounded-capture checks. Assemble the exact Event
or MIME adapter fields before publication, seal their final bytes, and retain
the existing Framework validation and Required scope unchanged. Demonstrate
the original failure with RED tests and cover successful Event/MIME assembly,
metadata rejection, unsafe capture rejection and receipt-reuse rejection.

## Implementation decision and rationale

Add one closed pre-publication assembly seam to the shared Parent Phase-4 host
runtime. Event and MIME adapters pass bounded metadata and the one literal MIME
fixture leaf into that runtime; they no longer read and rewrite the receipt.
The shared runtime hashes the actual bounded fixture bytes, merges fields with
the observations and calls the unchanged exclusive `HOST.write_json` exactly
once. This keeps the producer authoritative and fixes orchestration rather than
weakening a freshness or Canonical validator.

## Changed files

`ci/runtime/lifecycle/run-nginx-phase4-cases.py`,
`ci/runtime/lifecycle/run-nginx-event-boundary-cases.py`,
`ci/runtime/lifecycle/run-nginx-mime-cases.py`,
`tests/test_nginx_phase4_driver.py`,
`tests/test_nginx_event_boundary_driver.py`,
`tests/test_nginx_mime_driver.py`, and this English/German Change Record pair.
Framework and MRTS are unchanged.

## Commands executed

The retained focused RED run failed all ten new assertions because the assembly
helper did not exist (8 tests total, exit 1; log SHA-256
`91f03f90041bd3c83580d3391b63d052770626ad4b53807bc713e54058c44bd0`).
The focused GREEN run passed all 15 tests (exit 0; log SHA-256
`fa6a6d03abd87d37beaf313bcd1d79bdf8a8b46b47ec1a036a17bb8e0e2e093f`).
The expanded driver set passed 134 tests with one explicit-Framework-root skip
(exit 0; log SHA-256
`555c2ebab5ce7075aa5271cb41704ff4d6911e602835f8946627ef82e5a16b5a`);
the skipped module was then rerun against the exact current Framework checkout
and passed all 9 tests without skips (exit 0; log SHA-256
`264942505cba8da96814e0afab6d3317390731642300098072815e81224a42bd`).
Python syntax and `git diff --check` passed. At that point, broader source gates
and a fresh post-fix lifecycle remained pending. The independently chosen
focused matrix then passed 112 Parent and 74 Framework tests with no skips;
documentation regressions passed 48 tests and lifecycle Shell-environment
regressions passed 11 tests, also without skips. `bash -n` passed for all
adjacent lifecycle entry points, and ShellCheck at the repository's warning
threshold passed for the baseline, first-byte and connector-stage scripts.
The complete Parent `make lint` gate passed with no skip/failure markers (exit
0; log SHA-256
`3e601d7c75b4ffd43dfd03eed26c627284c0aa1e4195e0c97bfd279a3a049a3b`).
Two unchanged-content attempts are retained separately: the first used an
unauthorized historical Apache output default; the second passed `BUILD_ROOT`
as a Make command-line override and thereby defeated six tests' intentional
case-local roots. The corrected environment-scoped invocation first passed all
20 optional-prerequisite tests and then the complete lint gate.

## Security impact

The change preserves exclusive/no-follow receipt creation, private runtime-root
authority, bounded capture and existing-child rejection. Adapter metadata uses
a closed field set with bounded Event identities/headers and exact lowercase
SHA-256 values; the only extra captured leaf is the literal MIME fixture.
Independent security review found no actionable issue. It noted that direct
hardlink/ownership and racing-replacement tests for the capture are not added;
the fixture remains created by the trusted adapter inside the private
root-owned runtime directory, and descriptor-level `O_NOFOLLOW`/regular-file
checks remain active.

## Runtime evidence

R8 is retained as original failure evidence and remains Canonical `FAIL` with
supervisor/native exit 2; it is not reused or relabeled. The first failing
event child proves configtest 0, client exit 0, HTTP 200, Root master, nobody
worker and verified cleanup before the receipt rewrite failed. No post-fix
native runtime has run yet.

## Known limitations

Pure driver tests cannot prove native product behavior or Canonical completion.
A separate commit, freshly built exact-Head artifacts and a new isolated
Root/nobody lifecycle are required. Ruff remains unavailable and not run.

## Remaining risks

The fresh lifecycle may reveal independent downstream evidence/validation
defects after all intended requests execute. Such failures must remain separate
and must not be hidden by changing Required selection or validators. R8 showed
eight existing Canonical failures and stopped with 52 selected records without
PASS; those counts are failure evidence, not a post-fix conclusion.

## Checks not run and rationale

Clean-Head Parent lint, current remote CI/Sonar, the post-fix NGINX build and
full 97-record local lifecycle, and protected Exact-Head were not yet run at
this checkpoint. The completed lint above is a frozen-worktree pre-commit gate.
A raw default-severity ShellCheck over the unchanged large NGINX smoke harness
still reports its existing warnings; the
repository warning-level lifecycle checks are green, and unrelated shell
cleanup is outside this fix. The protected path remains blocked by its
independently approved Trusted Base, matching Gitlink, runner/environment and
administrative Host-Gate prerequisites.

## Final diff and review status

The six-file implementation/test diff and paired Change Record passed focused,
expanded and complete lint gates, syntax, documentation and whitespace checks.
Independent security and code review found no
actionable issue. Code review noted exact adapter-profile partitioning as an
optional hardening refinement, not a demonstrated defect: all actual callers
are fixed and incomplete records remain rejected by Framework validation. No
commit, push, PR-state change, merge, retarget, protected dispatch or
Framework/MRTS change has occurred for this fix at this checkpoint.
