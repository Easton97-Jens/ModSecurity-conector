# CI security tooling

**Language:** English | [Deutsch](ci-security-tooling.de.md)

## Scope

This document describes repository CI controls. It does not establish runtime
security, connector correctness, or a production-security certification.

## Immutable action and tool provenance

Every remote action reference in `.github/workflows/` is pinned to an immutable
commit SHA with its stable release tag in a comment. The revalidation date,
official upstream, release version, immutable commit, binary release asset,
SHA-256 digest, license, purpose, and minimum permissions are recorded in
`ci/tooling/security-tools.lock.yml`.

`ci/tools/fetch_security_tool.py` accepts only the recorded official release
asset, verifies the SHA-256 digest before extraction, rejects absolute and
traversal archive paths, and extracts exactly one declared executable. It does
not install dependencies or modify repository files.

## Constrained workflow/tool updater

`.github/workflows/update-workflow-tools.yml` keeps `resolver`, `validator`,
`publisher`, and `outcome` as separate jobs. The first two jobs are read-only;
the publisher obtains a short-lived, repository-limited GitHub App token only
after candidate and proposed-tree validation. It creates Draft pull requests
only after explicit path, symlink, staged-scope, and candidate-SHA-256 checks.

The checked-in `ci/tooling/security-tools.lock.yml` remains the only lockfile
and source of truth. Its on-disk `pinned_actions` records use `commit_sha` and
`upstream`; tool records use `release_commit`, `url`, and `upstream`. The
updater adapts those fields only in memory, so existing Connector consumers do
not need a parallel lock schema.

| Action | Version | Immutable commit |
| --- | --- | --- |
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/create-github-app-token` | `v3.2.0` | `bcd2ba49218906704ab6c1aa796996da409d3eb1` |
| `actions/download-artifact` | `v8.0.1` | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` |
| `actions/github-script` | `v9` | `3a2844b7e9c422d3c10d287c895573f7108da1b3` |
| `actions/setup-go` | `v7.0.0` | `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e` |
| `actions/setup-python` | `v7.0.0` | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| `actions/upload-artifact` | `v7.0.1` | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` |
| `github/codeql-action` | `v4.37.4` | `f205ea1c3313d32999d8d6a48b4f6530d4437b38` |
| `google/osv-scanner-action` | `v2.3.8` | `9a498708959aeaef5ef730655706c5a1df1edbc2` |
| `ossf/scorecard-action` | `v2.4.4` | `2d1146689b8cda280b9bc96326124645441f03bc` |

For hosted execution, configure the repository variable
`WORKFLOW_UPDATER_APP_CLIENT_ID` and the repository secret
`WORKFLOW_UPDATER_APP_PRIVATE_KEY`. Do not place either value in the
repository. The GitHub App must be limited to this repository and grant only
`Contents: write`, `Pull requests: write`, and `Workflows: write`.

## Workflow linting

`ci-security-workflow-lint.yml` runs checksum-verified `actionlint` and passes
the runner's `ShellCheck` path when available. It also runs checksum-verified
`zizmor` offline against all workflow files. A deliberately insecure fixture
must fail and a safe fixture must pass; neither fixture is executable product
configuration.

## Secret and dependency scanning

For a pull request, Gitleaks computes `git merge-base` from the exact base and
head SHAs, scans only that commit range, and enables redaction. Scheduled and
manually dispatched full-history Gitleaks scanning is advisory until historic
findings have been triaged; it must not silently block unrelated work.

OSV scans the exact pull-request base SHA and exact pull-request head SHA,
compares their results, and reports newly introduced findings. It performs no
automatic dependency update or dependency remediation. The scheduled scan is
also advisory so that a repository-wide historical dependency finding can be
triaged before it becomes a blocking policy.

## CodeQL and Scorecard boundaries

CodeQL analyzes Actions, each Go module through the exact root
<code>.go-version</code> selector (currently Go <code>1.26.5</code>), and a
bounded C/C++ scope. That scope runs <code>make check-common-helpers-c17</code>
plus a bounded 15-second libFuzzer run for the Common HTTP header parser
with C17, AddressSanitizer, and UndefinedBehaviorSanitizer. The central
selector is a CI toolchain contract; each module's <code>go.mod</code> still
owns its Go language baseline. The updater proposes only a same-minor stable
patch in a Draft PR after read-only candidate validation and cannot alter
module or dependency files. The C/C++ result does not claim full connector
coverage; expanding it requires reproducible builds for the selected connector
scope.

Scorecard uses read-only permissions for same-repository pull requests and
checks out the exact pull-request head. Fork pull requests are intentionally
not analyzed by that job because their head is not a trusted same-repository
ref. Default-branch Scorecard uploads SARIF with the separate
`security-events: write` permission only.

## Validation and limitations

Run `make check-ci-security-contract` for focused static contracts and lock
record validation. GitHub Actions, CodeQL, OSV, Gitleaks, and Scorecard results
are evidence only for their workflow, event, exact SHA, and permissions. They
do not create automatic fixes, alter branch protection, bypass reviews, or
replace connector/runtime testing.
