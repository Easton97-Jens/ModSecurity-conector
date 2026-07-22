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
bounded C/C++ scope limited to <code>make check-common-helpers-c17</code>. The
central selector is a CI toolchain contract; each module's <code>go.mod</code>
still owns its Go language baseline. The updater proposes only a same-minor
stable patch in a Draft PR after read-only candidate validation and cannot
alter module or dependency files. The C/C++ result does not claim full
connector coverage; expanding it requires reproducible builds for the selected
connector scope.

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
