# FND-PARENT-0045 — Update-submodules validation tests expect a prohibited shared-cache HAProxy runtime binary

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0045 |
| Category | ci_failure |
| Repository / ownership | parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | confirmed / fixed |
| Feasibility | feasible_now |
| Release blocker | yes |
| Security relevant | yes |

## Observation and impact

GitHub Actions run [29945542984](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29945542984)
successfully resolved and checked out Framework candidate
`f73f8842f45318e2df8aff1d31855eeb7c20a22f`, but its read-only
`make quick-check` failed three Parent HAProxy managed-cache tests. Each
fails with:

```text
haproxy_prepare: blocked HAPROXY_RUNTIME_BUILD_DIR must be under BUILD_ROOT
```

The publisher was correctly skipped. This is a CI-control compatibility
failure, not an exploit: it prevents a candidate publication rather than
giving a write-capable job an unsafe path.

## Cause and safe remediation boundary

The direct Parent test fixture constructs a runtime build directory, worktree,
runtime directory, and HAProxy binary below `cache-v2/shared`, while passing a
different `BUILD_ROOT`. Current Framework master correctly requires those
runtime outputs to remain below `BUILD_ROOT`; its security regression asserts
the same fail-closed behavior.

The Parent component preparer already uses its managed connector entry as the
effective `BUILD_ROOT` when invoking the Framework script. The direct test
fixture is therefore the divergent layer. The repair must replace its obsolete
positive reuse assertion with a legitimate managed-entry control and an
explicit separate-`BUILD_ROOT` rejection control.

It must not change Framework source, the Parent gitlink, MRTS, workflow
permissions, the read-only validation gate, or the publisher eligibility rule.

## Local remediation and required validation

The Parent fixture/invocation seam is now corrected in the isolated task
worktree. The focused suite ran 61 tests through the deliberately supplied
read-only Framework root at `f73f8842…` and passed. It includes legitimate
managed-entry reuse, a complete entry without cache marker, a no-rebuild
control, and explicit split-root exit-77 rejection. The Go/Python/CI contract
target passed, including the static proof that `update-submodules.yml` retains
resolve → read-only validation → narrow publisher ordering and permissions.
A focused security-diff scan was finalized with zero reportable findings.

Initial Draft PR #90 head `0acba7768848651758610928e89f4481dbb90c81`
reached five completed ordinary push workflows (29955277020, 29955277057,
29955276989, 29955277045, and 29955277071). Authenticated failed-log review
shows every one failed at the same obsolete assertion: the old Parent test
expected exit 77, while legacy gitlink `784977615acfc55567e37b863309abc4a38ac877`
legitimately returned exit 0 from managed-cache reuse. The current bounded
follow-up skips only that exact legacy revision, fails closed for unknown or
non-strict revisions, and runs the Exit-77 control against F73. It again
passed the focused 61 tests, 11 bilingual tests, the Go/Python/CI contracts,
and a complete final security scan with zero reportable findings.

The later exact PR #90 head
`06a4e71408a60e5a72a55065a653b9c4e79a1ecf` has local/remote/PR SHA equality,
ordinary GitHub checks terminal success or skipped, and SonarQube Cloud Quality
Gate `OK`. Its receipt is
hosted-pr90-06a4e71-validation.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/hosted-pr90-06a4e71-validation.json`)
(SHA-256 `db38c89e5c1646e343ec022466d7fec899998dda05558ccf85789196d273ea20`).

The current disposition is `fixed`, not verified or closed. The replacement
PR still needs exact-head hosted `Update submodules` validation before
verification or closure. The broad documentation target is blocked only by the
intentionally uninitialized Parent Framework gitlink. The installed Go 1.26.0
executable correctly blocks local `GOTOOLCHAIN=local` module test/vet because
both modules require 1.26.5; it did not download or mutate a toolchain.

The single later authorized current-master run `29981644356` reached the
read-only candidate checkout and interpreter contract, but then failed earlier
at the distinct PyYAML fixture-syntax prerequisite before it could supply the
remaining required evidence for this finding. The publisher was skipped. This
does not re-open the Parent HAProxy fixture root cause; it is separately
tracked as `FND-PARENT-0048`, whose corrective PR must be integrated and then
rerun on `master` before either record can be verified.

## History

- 2026-07-22T18:45:02Z — source and security-regression review proved the
  Framework containment check is intentional; the Parent fixture/invocation
  contract owns the correction.
- 2026-07-22T18:51:17Z — canonical Parent finding allocated before
  remediation, with no control weakening or cross-repository action.
- 2026-07-22T20:18:14Z — Parent-only remediation and focused local controls
  passed in the isolated worktree. The finding advances to `fixed`; hosted
  exact-head validation remains required, and no Framework, MRTS, gitlink,
  permission, or master action occurred.
- 2026-07-22T21:06:32Z — Initial PR #90 exact-head failure was directly
  attributed to the common legacy Parent assertion across all five runs. The
  SHA-specific follow-up is locally revalidated, but remains uncommitted and
  unpushed; a fresh exact-head hosted cycle remains required.
- 2026-07-22T21:25:24Z — The SHA-specific follow-up was committed and normally
  pushed as `d99eafd76d9fdbef5b63a19d084fd2d7caff6c08`; local, remote, and PR
  heads match and all applicable ordinary exact-head Actions passed. Separate
  task-owned Sonar Quality Gate `ERROR` is tracked by `FND-SONAR-0010`; no
  `Update submodules` dispatch, master action, Framework/MRTS action, or
  gitlink update occurred.
- 2026-07-22T23:02:27Z — Exact head `06a4e71` passed ordinary hosted checks
  and SonarQube Cloud Quality Gate. This finding remains `fixed`, not
  `verified`, because the separately authorized read-only `Update submodules`
  candidate validation has not been dispatched.
- 2026-07-23T05:15:37Z — The now-authorized current-master run `29981644356`
  retained fail-closed publisher behavior but failed at the distinct PyYAML
  fixture-syntax dependency preparation step. `FND-PARENT-0048` owns that
  correction; this finding remains `fixed`, not verified.
