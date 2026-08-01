# FND-PARENT-0020 — Traefik native middleware UDS tests exceeded the AF_UNIX pathname limit under the approved temporary root

## Classification

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0020 |
| Category | test_failure |
| Repository / ownership | parent / parent |
| Priority | P1 |
| Severity | not_applicable |
| Confidence | reproduced |
| Status | fixed |
| Feasibility | feasible_now |
| Release blocker | false |
| Security relevant | false |
| Connector / profile | Traefik / native-traefik-middleware |
| Protocol | AF_UNIX pathname length in the Go UDS test harness |

## Summary

The focused native-middleware Go target could not exercise its UDS protocol
assertions when TMPDIR was the required private external project root. Go
testing's t.TempDir() inserted a long test identifier and made engine.sock
exceed the AF_UNIX pathname bound before any test protocol action ran.

## Observed and expected behavior

Before the correction, the target exited with code 2. Multiple tests reached
net.Listen("unix", socketPath) and failed with bind: invalid argument for paths
below /var/tmp/codex/ModSecurity-conector/tmp/TestUDSEngine.../001/engine.sock.
No middleware/session assertion had run.

The focused UDS tests must run under the approved external TMPDIR, bind a
socket path inside the AF_UNIX bound, preserve the temporary-root policy, and
remove only their own private test directory.

## Impact and scope

A mandatory focused regression target was unavailable in the authorized storage
configuration, leaving UDS protocol and middleware behavior unvalidated. This
is test-harness infrastructure only: no production request path or runtime UDS
listener was shown to be affected.

Affected file and symbols:

- connectors/traefik/native_middleware/engine_uds_test.go
- startUDSTestServer
- newUDSTestSocketPath

Preconditions are the configured
TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp, use of testing.T.TempDir(), and
a resulting pathname beyond the platform AF_UNIX limit.

## Root cause and remediation

startUDSTestServer constructed its socket path from t.TempDir(). The Go
framework includes the test name and a numeric component, so deliberately long
test names plus the approved TMPDIR exceeded AF_UNIX capacity. The production
runner is not involved.

The focused correction uses os.MkdirTemp("", "uds-") to allocate a short,
private child below the same configured TMPDIR, registers t.Cleanup to remove
that exact created directory, and constructs engine.sock below it. It does not
select a global or unapproved temporary root.

## Evidence

Run ID: 20260718T053406Z-pr-51-master-integration-546d9dc2

| Stage | Artifact | SHA-256 | Exit | Result |
| --- | --- | --- | ---: | --- |
| Pre-fix reproduction | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-native-middleware-long-tmpdir-regression.log | f960246f3e6052e1da13d960e8d647c660b39ec5bd47bd308b3e9f4117b2306c | 2 | UDS bind failed before protocol assertions. |
| Post-fix validation | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-native-middleware-long-tmpdir-regression.log | f960246f3e6052e1da13d960e8d647c660b39ec5bd47bd308b3e9f4117b2306c | 0 | go test ./... and go vet ./... passed. |
| Focused security review | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-test-harness-security-review.md | 0ec987bc3e4e70f9e2dc7dc144d9feb44b2e2b0aa315a5897d99bcc3ed18d684 | 0 | Private test path and exact cleanup are already safe; no reportable security finding. |
| Exact committed SHA | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/go-native-middleware-exact-2589c08.log | c244e81ed67a49158d2e5d6238371eb8f8b20dc83e33f91a25dcf1e0dad67920 | 0 | Commit 2589c085a1ed7bbb2c2033635f06e71f5f75fb8b reran tests without the Go test cache and passed. |
| Current master | /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/master-c8ca0d9-traefik-regressions.log | 1f766b416d36f8f0ce35e7e904e8e3f50b57d1e80af1571e2cc9e59c164004af | 0 | Merged master c8ca0d92b630c18232b881855c4f5d1482568ea6 reran the original target without cache and passed. |

Both stages used:

~~~text
rtk env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/build TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/build/native-middleware GOCACHE=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/cache/go-build GOMODCACHE=/var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/cache/go-mod GOTOOLCHAIN=local GOWORK=off GO=go TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp make -C connectors/traefik test-native-middleware
~~~

The post-fix directory listing showed no uds-* child under the configured
temporary root.

## Acceptance and validation

1. The exact pre-fix focused Go target passes with
   TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp.
2. Its go test ./... and go vet ./... stages pass.
3. No uds-* directory remains under the configured TMPDIR.
4. The change remains test-harness-only and git diff --check passes.
5. The exact final PR head and current master retain the passing result.

The validation plan is to rerun the same target, review the helper's
path/cleanup boundary, bind the result to the pushed PR head, and repeat it on
the merged master SHA.

## Dependencies, related records, and residual risk

Current-master verification is complete. FND-FRAMEWORK-0008 is related because it covers a distinct
production UDS pathname boundary; this record is a separate test-harness cause
and remediation.

The correction is test-only and validates the available native Go harness. A
genuine Traefik host binary remains unavailable for the separate full lifecycle
test. No security risk has been accepted.

## History

- 2026-07-18T06:14:59Z — The original focused target failed with exit code 2
  under the approved external TMPDIR before UDS protocol assertions.
- 2026-07-18T06:14:59Z — The short os.MkdirTemp child and exact test cleanup
  made the same target pass; no uds-* child remained.
- 2026-07-18T06:26:39Z — Commit
  2589c085a1ed7bbb2c2033635f06e71f5f75fb8b reran the target with
  GOFLAGS=-count=1 under the approved external TMPDIR; Go test and vet passed.
- 2026-07-18T06:40:39Z — Merged master
  c8ca0d92b630c18232b881855c4f5d1482568ea6 reran the original target
  without the Go test cache; Go test and vet passed and no uds-* child remained.
