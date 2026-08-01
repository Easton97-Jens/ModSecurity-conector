# FND-PARENT-0063 — Normal runtime provisioning executes release-selected mutable upstream source

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0063` |
| Category | `security_validated` |
| Repository / ownership | Parent / Parent |
| Priority / severity / confidence | P3 / low / validated |
| Status / feasibility | `validated` / `requires_user_decision` |
| Release blocker / security relevant | false / true |

## Summary

The ordinary non-strict component provisioner accepts the mutable tag returned
by GitHub `releases/latest`, records an expected-latest difference only as
metadata, and then builds the selected source on a trusted runner.

## Observed behavior and source-to-sink path

At Parent master `8e8acb8dab1cd03723de269cab7da7dd62e5e010`,
`prepare_release_git_component` passes the runtime latest-release tag directly
to `prepare_git_component` even with `strict=True`. A mismatch with
`expected_prompt_latest` sets `release_tag_deviation` but does not block. The
affected entry point/control is
`ci/provisioning/components/prepare-runtime-components.py:1504-1579`; sinks
are the Expat source build at `:2709-2768` and the Go package build at
`:4292-4312`.

Expected behavior is an explicit reviewed immutable provenance contract before
checkout and build. A changed latest release must fail closed rather than be
merely reported.

## Impact, preconditions, and attack-path scope

An attacker needs to compromise a configured upstream GitHub release maintainer
or its mutable `releases/latest` state, then await a scheduled or trusted-manual
`make prepare-runtime-components` run. The repository threat model expressly
includes imported-upstream provenance and CI supply chain.

The reviewed provisioner workflows are scheduled or manual, have
`permissions: contents: read`, and use `persist-credentials: false`. No
`pull_request_target`, secret reference, writable repository token, or
production/deployment impact was found. The strong external precondition and
bounded runner/cache/network impact make this a reportable low/P3 finding, not
high or critical.

## Evidence and reproduction

Run `sonar-652-duplication-zero-20260728-W8wqjk` retained an offline fixture:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 .venv/bin/python -B \
  validation_artifacts/validate_mutable_release_execution.py \
  --repo-root /root/git/ModSecurity-conector \
  --artifact-root validation_artifacts
```

It passed. The fixture supplied a synthetic changed tag to the production
module, proved that it reaches the Git-preparer with `strict=True`, and built
an executable harmless local Git-backed Go fixture through the real build sink.
It contacted no network endpoint and executed no upstream source. The result
SHA-256 is
`515ef4bcaa82ffd0bf33925cf5c3091c3050d76e4db51dc6637539abed50113d`.

The attack-path report SHA-256 is
`cedea4cfe9d493d3cf6cc692f8112fd0ac2c91cffc6729eaefa1cb6193974d8f`.
It records the in-scope decision, counterevidence, and low/P3 calibration.

## Root cause and proposed remediation

`prepare_release_git_component` is designed for compatibility tracking of
current GitHub releases. It reuses latest-release selection for Expat outside
strict evidence runs and for go-ftw/albedo, while expected latest is an
observation rather than an admission control.

Select and document one immutable provenance contract for every
release-resolved component: reviewed full Git commit, verified signed tag, or
immutable source archive digest. Parent admission must reject an unexpected
latest tag before checkout/build. A Framework-owned default pin may be changed
only through a separately authorized Framework PR.

## Acceptance criteria and validation plan

1. The selected immutable contract is explicit for Expat non-strict
   compatibility, go-ftw, and albedo.
2. A release-tag deviation is rejected before checkout or source build.
3. Existing safe cache, URL allowlist, clean checkout, submodule, and `git
   fsck` controls remain intact.
4. Focused tests cover a rejected changed latest release and a legitimate
   approved immutable source.
5. Exact-head hosted workflow and SonarQube Cloud proof pass without weakening
   scanner, gate, permission, or provenance controls.

## Dependencies, blockers, related findings, and residual risk

The selected immutable contract is a current-user decision. Framework write
scope is not selected for this task if the default pins belong to Framework.
Related records are `FND-PARENT-0050`, `FND-PARENT-0052`, and
`FND-SONAR-0016`. This is not a duplicate of `FND-PARENT-0052`, which owns the
strict full-evidence producer's Expat/Python contract, whereas this finding
owns normal release-tracking provisioning.

Until remediation, a compromised upstream release-selection state can run its
source build behavior in scheduled or trusted-manual provisioning. No risk is
accepted.

## History

- `2026-07-28T10:16:00Z`: no-network selector/build-sink fixture passed.
- `2026-07-28T10:20:00Z`: attack-path analysis confirmed the in-scope path and
  calibrated it low/P3.
