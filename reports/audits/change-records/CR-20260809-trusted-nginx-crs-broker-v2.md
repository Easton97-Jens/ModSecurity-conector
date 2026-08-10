# Change Record

**Language:** English | [Deutsch](CR-20260809-trusted-nginx-crs-broker-v2.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260809-trusted-nginx-crs-broker-v2 |
| Date (UTC) | 2026-08-09 |
| Base revision | cc58f94e6a0dd17eea651cd46376843472b83f7c |

## Motivation and problem statement

The historical trusted NGINX broker records `with-crs` only as a matrix label
and always uses its broker-owned `/blocked` rule. That cannot demonstrate a
real NGINX OWASP CRS block. The authorized v2 change extends the existing
narrow broker contract before PR #240 may consume a new protected merge SHA.

## Acceptance criteria

Schema v1 remains a reproducible no-CRS control. Schema v2 supplies only closed
`no-crs` and `owasp-crs` profiles; the caller selects neither a CRS path nor a
rule, ref, or digest. The protected workflow must build a fresh CRS bundle from
the reviewed repository/tag/commit, root must admit only its exact
digest-verified contents, and `owasp-crs` must prove its own NGINX allow/block,
CRS rule, audit, identity, evidence, and cleanup result. No PR #240,
Framework-in-PR, or caller code may execute as root.

## Implementation decision and rationale

The existing SHA-bound reusable workflow and Python broker are extended rather
than adding a second root runner. The v2 broker independently pins
https://github.com/coreruleset/coreruleset.git, tag `v4.28.0`, commit
`55b09f5acfd16413e7b31041100711ceb7adc89c`, and expected blocking rule
`949110`. A protected unprivileged fresh-source stage produces a sorted
manifested bundle. Root uses descriptor-relative no-follow admission with
owner/mode/device/link-count/inode/size and before/after digest checks, then
generates fixed root-local ModSecurity includes and portable serial audit
configuration.

## Changed files

- `.github/workflows/nginx-root-broker.yml`
- `ci/runtime/broker/nginx_root_broker.py`
- `ci/runtime/lifecycle/prepare-fresh-crs-source.sh`
- `tests/test_nginx_root_broker_crs_profile.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_ci_security_workflows.py`
- `docs/security/trusted-nginx-root-broker.md` and `.de.md`
- this Change Record and its German companion

## Commands executed

Observed so far: Python compilation of the broker and the focused broker,
v2-profile, workflow-contract, and CI-security suite. The focused suite ran
53 tests successfully. Further project-native quality, documentation, shell,
security-diff, and hosted checks remain required before delivery.

## Security impact

The change preserves the fixed action allowlist and refuses caller command,
shell, configuration, rule, CRS-source, and binary inputs at the root
boundary. The new root input is only a protected-build bundle whose topology
and content are revalidated before materialization. The CRS profile cannot
claim PASS from the broker-owned no-CRS `/blocked` rule: it requires the
canonical CRS request, a real audit record, exact rule `949110`, and the bound
tuple/digest. Cleanup stays descriptor-relative and removes only the fixed run
root.

## Runtime evidence

No protected-master hosted v2 lifecycle has been observed. Local focused tests
do not prove GitHub reusable-workflow semantics, a real NGINX root master,
non-root worker, real CRS evaluation, audit output, listener release, or the
uploaded cleanup record. Those are mandatory resulting-master validations
after a normal protected merge and before PR #240 changes.

## Known limitations

The v2 profile is intentionally not a general CRS execution platform. It
admits only the fixed reviewed CRS tuple, selected file topology, fixed
loopback requests, and fixed evidence allowlist. It does not add caller
overrides, dynamic includes, archive input, or arbitrary privileged actions.

## Remaining risks

GitHub Actions context values, current hosted image behavior, Framework fetch
behavior, NGINX/ModSecurity/CRS runtime compatibility, and artifact upload
must still be proven on the protected resulting master. A failure blocks the
merge or post-merge validation; it never authorizes a fallback to PR-branch
root execution or a synthetic CRS PASS.

## Checks not run and rationale

At this local implementation point, actionlint, ShellCheck, zizmor, the full
project-native local gate, the focused security-diff scan, hosted checks,
CodeQL, SonarQube Cloud, review/branch-protection gates, and protected-master
runtime validation have not yet been observed. They are intentionally not
claimed before they run on the final exact head.

## Final diff and review status

This record describes an uncommitted v2 implementation in the separate branch
`fix/ci-trusted-nginx-crs-broker-v2`, based on
`cc58f94e6a0dd17eea651cd46376843472b83f7c`. No new pull request, push,
merge, PR #240 update, Framework source change, MRTS change, force-push,
history rewrite, or auto-merge has occurred. The new broker PR remains
delivery-blocked until all required local, security, hosted, Sonar, review,
and branch-protection evidence is recorded.
