# Change Record: Required native Envoy bridge verification

**Language:** English | [Deutsch](CR-20260923-pr382-envoy-native-verification.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260923-pr382-envoy-native-verification` |
| Date (UTC) | `2026-09-23` |
| Base revision | `ee33afc5bbb961f2d0d612c5ff591eb073fd02ce` |
| Scope | Parent PR #382; I09/I10 verification and V20 |

## Motivation and problem statement

The checked-in response-commitment tests carry the libmodsecurity build tag.
The previous Envoy workflow ran source contracts and host preflight, not these
native tests. A successful job therefore could not establish propagation from
the Go receiver through the checked C ABI to the real Common state machine.

## Acceptance criteria

Compile the real bridge and execute its tagged Go suite, including both
commitment regression cases. Missing native prerequisites must fail, not skip.
Preserve the repository toolchain selector, dependency graph and exact-head
Sonar findings/duplication gates. Keep live Envoy transport evidence separate.

## Implementation decision and rationale

Extend the existing Envoy job after its source-contract checks. Use the already
pinned setup-go action and root Go selector, disable shared Go caching, and
install only build-essential and libmodsecurity-dev on the disposable runner.
Call the existing build_ext_proc.sh with ENVOY_EXT_PROC_COMMON_TEST=1 directly:
its validated native prerequisites cannot take the optional test script's skip
path. The existing builder compiles the Common archive and CGo service and runs
all packages with the libmodsecurity tag and count=1 using readonly modules.
No runtime capability or production error policy is changed in this slice.

## Changed files

The Envoy workflow and this paired Change Record. No connector source,
Framework/MRTS files, lock files, scanner rules or dependency versions change.

## Commands executed

The required remote step invokes:

```sh
sh connectors/envoy/build/build_ext_proc.sh
```

It uses ENVOY_EXT_PROC_COMMON_TEST=1, the distribution native headers/library,
and private runner-temporary build/cache paths. Execution is pending when this
commit is prepared; read back the published revision before recording V20.
The user clarified that RTK is not a blocker for this remote workflow.

## Security impact

Keep contents:read and persist-credentials:false. No credentials reach test
process arguments, no pull_request_target, no shared build-cache writes, no
service deployment and no persistent user-machine package installation. Native
prerequisite absence and compilation/test failures remain failing results.

## Runtime evidence

A successful tagged run demonstrates real Common/libmodSecurity/CGo execution,
not a running Envoy server, physical gRPC delivery, or all integration routes.
Preflight artifacts retain their original limited meaning and are not promoted
by the additional native step.

## Known limitations

I09/I10 cannot be marked globally complete from this one route's test job.
Other adapter source gaps and I11/I12 physical-log/live-host proof remain open.
The distribution library is not a replacement for release-pinned host testing.

## Remaining risks

The newly enforced native suite can expose previously unexecuted failures.
Classify and repair those failures without weakening assertions or compiler
warnings. Sonar must report zero new findings and exact zero new duplication.

## Checks not run and rationale

No local full checkout or native suite: the sandbox cannot resolve GitHub.
Remote GitHub source access and CI are used instead. No live-host matrix is
claimed. New execution and Sonar evidence must be tied to the new revision.

## Final diff and review status

Continue the existing Draft PR only. Preserve concurrent Apache changes; no
merge, master update, force push or deployment is authorized by this change.
