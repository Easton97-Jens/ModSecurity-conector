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

`ci/tools/fetch_security_tool.py` starts only from the exact recorded
`https://github.com/.../releases/download/...` URL. It follows at most two
HTTPS redirects: the first only from that GitHub origin to the explicit
official release-asset host allowlist, and an optional second only within that
same allowlist (`release-assets.githubusercontent.com` and the legacy
`github-releases.githubusercontent.com`). It rejects any foreign or insecure
redirect/final host and verifies the locked SHA-256 digest before
extraction, rejects absolute and traversal archive paths, and extracts exactly
one declared executable. It does not install dependencies or modify repository
files.

The workflow-key verifier parses every workflow's YAML node tree and requires
each decoded `uses` key to be written as the canonical unquoted block
`uses:` key, so YAML quoting, escape, tag, explicit-key, and flow-map syntax
cannot hide an action reference. Its parser wheel is pinned with an exact
SHA-256 in `ci/tooling/python-ci-requirements.lock` and is installed from the
fixed PyPI index with hash enforcement; it is not taken implicitly from the
hosted runner.

Before the privileged Parent tooling publisher can create or refresh a draft
PR, the read-only validator rebuilds the candidate in a disposable trusted
tree and checksum-downloads/extracts each candidate security tool. After the
SHA-256 and extraction checks, it runs only bounded, 30-second version smoke
checks (`actionlint --version`, `zizmor --version`, and `gitleaks version`).
It does not use those downloaded binaries to inspect repository content or to
publish changes.

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

CodeQL analyzes Actions, each Go module with the exact pinned Go `1.26` patch
declared in its `go.mod` and mirrored in the CodeQL setup, and a bounded C/C++
scope limited to `make check-common-helpers-c17`. The patch-only updater
accepts only official stable releases in that `1.26` series; it does not float
to a new minor release. Its machine-readable result distinguishes `current`,
`patch_update_available`, and `newer_minor_available`; it fails closed with
`blocked_metadata`, `blocked_network`, `no_stable_release`,
`invalid_current_version`, or `candidate_failed`. The C/C++ result does not
claim full connector coverage; expanding it requires reproducible builds for
the selected connector scope.

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
