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
Preserve toolchain selection, reviewed engine provenance, dependency graph and
exact-head Sonar findings/duplication gates. Keep live transport evidence separate.

## Implementation decision and rationale

Extend the existing Envoy job after its source-contract checks. Use the already
pinned setup-go action and root Go selector, with no shared Go cache. The first
attempt at `6092c1b0` used the distribution's older 3.0.12 native development
package; the actual strict build rejected its incompatible C API. This was a
test-environment selection error, not a successful native regression run.

The correction uses the repository's existing with-runtime-components.sh,
restricted to target shared. Framework-owned engine provenance, private cache
validation and the invocation-bound environment remain authoritative. Install
build prerequisites only on the disposable runner; no distribution-engine
fallback, API emulation, const cast or warning suppression is introduced.
The unchanged native builder runs ENVOY_EXT_PROC_COMMON_TEST=1, compiling the
Common archive and CGo service and testing all tagged packages with count=1.
The separate declaration/assignment issue reported by ShellCheck disappears
with removal of the incorrect hard-coded distribution-library selection.

## Changed files

The Envoy workflow and this paired Change Record. No connector source,
Framework/MRTS files, lock files, scanner rules or dependency versions change.

## Commands executed

Required remote command, with ENVOY_EXT_PROC_COMMON_TEST=1:

```sh
sh ci/provisioning/cache/with-runtime-components.sh sh connectors/envoy/build/build_ext_proc.sh
```

At `6092c1b0`, job 107129310702 (run 35845121593) reached real compilation and
failed on the old API before Go tests. Actionlint separately reported SC2155.
Neither result is marked passed. Fresh results after the provisioning correction
are required. RTK does not govern this remote connector/CI execution path.

## Security impact

Keep contents:read, persist-credentials:false and pinned actions. Provisioning
retains its reviewed-source and cache checks in runner-owned private directories.
No credentials reach test arguments, no pull_request_target, scanner suppression,
shared-cache publication, deployment or persistent user-machine installation.
Missing prerequisites and compilation/test failures remain failing results.

## Runtime evidence

A successful tagged run demonstrates actual Common/libModSecurity/CGo execution,
not a running Envoy server, physical gRPC delivery or all integration routes.
Preflight artifacts retain their limited meaning and are not promoted by the
additional native step. Compilation alone does not satisfy V20.

## Known limitations

I09/I10 cannot be marked globally complete from this one route's test job.
Other adapter source gaps and I11/I12 physical-log/live-host proof remain open.
The initial 3.0.12 failure is retained as history rather than hidden by a skip.

## Remaining risks

The newly enforced native suite can expose previously unexecuted failures.
Repair their causes without weakening assertions or compiler warnings. Sonar
must report zero new findings and exact zero duplicated new lines and blocks.

## Checks not run and rationale

No local full checkout or native suite: the sandbox cannot resolve GitHub.
Remote GitHub source access and CI are used instead. No live-host matrix is
claimed. New execution and Sonar evidence must be tied to the new revision.

## Final diff and review status

Continue the existing Draft PR only. Preserve concurrent Apache changes; no
merge, master update, force push or deployment is part of this change.
