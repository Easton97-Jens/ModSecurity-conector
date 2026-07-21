# Change Record: Parent CI tooling and Go 1.26.5 update

**Language:** English | [Deutsch](CR-20260721-parent-ci-tooling-go-update.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260721-parent-ci-tooling-go-update` |
| Date (UTC) | `2026-07-21` |
| Base revision | `5fa90474a79eaee2df034bf1c4389572fdcca42f` |
| Boundary | Parent CI workflows, locks/updaters, the two Parent Go modules, their EN/DE documentation/tests, and this record pair only. The Framework gitlink remains `784977615acfc55567e37b863309abc4a38ac877`; Framework and MRTS are untouched. |

## Motivation and problem statement

The Parent repository needed current immutable Action provenance and a current
Go baseline, but only with maintenance automation that cannot write the default
branch, force-push, merge, make a Draft non-Draft, or apply a stale candidate
to a newer default revision. The previous Go directive was `1.24.13` in both
actual modules, and checkout/Python setup pins predated their reviewed stable
releases.

## Acceptance criteria

- Changed Action references are full lower-case SHA pins with matching release
  comments and official tag/release-to-commit provenance.
- Generic Action/tool, Go, Python, and submodule publishers are Draft-only,
  normal-push-only, default-branch-gated, and bound to an exact fresh default
  base before a candidate can be reconstructed, committed, or pushed.
- Resolver/validator outputs are confined, candidate tool assets are
  SHA-256/archival-layout checked and only then receive bounded 30-second
  version smoke checks.
- Both Parent Go modules and CodeQL Go jobs select `go 1.26.5`; dependency
  selection and `go.sum` remain unchanged.
- EN/DE guides and this record state observed evidence, limits, and the
  Parent/Framework/MRTS boundary without claiming hosted results.

## Implementation decision and rationale

The Go baseline changes from `1.24.13` to `1.26.5` in
`connectors/envoy/ext_proc/go.mod`,
`connectors/traefik/native_middleware/go.mod`, and both CodeQL Go jobs.
The official archive used for local validation was
`go1.26.5.linux-amd64.tar.gz`, SHA-256
`5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053`, from
the official [Go download metadata](https://go.dev/dl/?mode=json&include=all)
and [archive](https://go.dev/dl/go1.26.5.linux-amd64.tar.gz).
`GOTOOLCHAIN=local` keeps CodeQL bound to the setup-go selection.

The workflow lock and matching references refresh, including
`actions/checkout` v7.0.1 at
`3d3c42e5aac5ba805825da76410c181273ba90b1` and
`actions/setup-python` v7.0.0 at
`5fda3b95a4ea91299a34e894583c3862153e4b97`. New generic Action/tool and
Go updaters split public resolution, isolated validation, and a narrowly
profiled publisher. The existing Python and submodule updaters receive the
same no-force/Draft/base-binding controls.

The Python contract now traverses YAML semantics rather than fragile textual
layout. It permits exactly one canonical pinned setup in each inventoried
Python job and rejects interpreter selection through other shells, PATH,
environment-file or `tee` writes, dynamic output targets, alternate setup
steps, and dynamic launchers. Publisher candidates retain and recheck one
captured default-base SHA after every relevant fetch; fresh branches start
explicitly at that remote-tracking revision.

## Security impact

This is CI supply-chain and delivery hardening. It prevents mutable pins,
unverified redirects/assets, stale candidate/default mixing, force/default
pushes, auto-merge/non-Draft maintenance delivery, and tested Python
interpreter-selection bypasses. It creates no direct default-branch write path
and changes no Framework gitlink or MRTS content.

## Changed files

- Parent GitHub workflows, including the generic Action/tool, Go, Python, and
  submodule maintenance publishers; CodeQL selectors and full-SHA pins.
- `scripts/update-github-actions-versions.py`, `scripts/update-go-version.py`,
  safe tool fetching, workflow contracts, lock data, and focused fixtures/tests.
- The two Parent Go module declarations only; no dependency, source, or
  `go.sum` update is intended.
- EN/DE CI-tooling and compiler/build guides, generators/tests, plus this
  English/German record pair and index entries.

## Commands executed

| Command or control | Result |
| --- | --- |
| Go 1.26.5 `go mod verify` and `go mod tidy -diff` in both actual modules | passed; no tidy or `go.sum` drift. |
| Go 1.26.5 `go test -mod=readonly ./...`, `go vet ./...`, and `go build -mod=readonly ./...` | passed for the direct modules; Envoy uses documented `-buildvcs=false` in the isolated worktree. |
| Go 1.26.5 `go list -m all` and `go mod graph` | passed; selected dependencies remain unchanged while the root Go directive becomes 1.26.5. |
| Go 1.26.5 `govulncheck` for Envoy | exit 0, no code-reachable vulnerabilities; two import-level and six required-module advisories were not called and remain explicit evidence. |
| Go 1.26.5 `govulncheck` for Traefik | exit 0, no vulnerabilities found. |
| Traefik native middleware script test/build with Go 1.26.5 | passed. |
| `tests.test_python_version_contract` and real Python contract checker | 30/30 passed; 30 jobs, zero violations. |
| CI-security, Action/Go/Python updater, bilingual documentation, and semantic publisher/TOCTOU tests | focused runs passed: 51 Action/Go/CI-security, 22 Python-updater, and 48 documentation/CI-security/Action-updater tests. |
| Full `unittest discover -s tests -q`, Actionlint for all four publishers, Action-version verifier, and `git diff --check` | passed; the test discovery emitted only the expected connector-capabilities usage diagnostic. |

## Runtime evidence

The direct module and Traefik native middleware results establish build/test
behavior only. This CI/toolchain change claims no connector request, protocol,
CRS, Framework, or MRTS runtime result.

## Checks not run and rationale

- `make check-bilingual-docs` was run, but returns only the existing missing
  Framework link targets because this worktree deliberately leaves the
  Framework gitlink uninitialized. The new Change Record pair itself passes
  the checker; neither the gitlink nor Framework files were initialized or
  changed to make this check pass.
- Envoy native bridge/runtime was not run because this isolated Parent worktree
  has no initialized Framework gitlink or libmodsecurity/host prerequisites.
  It is not inferred from the direct Envoy module result.
- Exact-Draft-PR-head CodeQL, OSV, Gitleaks, Scorecard, SonarQube Cloud, and
  other hosted checks are post-publication evidence.
- No Dependabot alert or dependency graph was revalidated, closed, or
  dismissed by this change; the exact-PR-head OSV result is likewise not yet
  observed.
- No dependency upgrade, `go.sum` rewrite, Framework gitlink update, MRTS
  initialization, or automatic merge is in scope.

## Known limitations

Updater profiles deliberately support only reviewed paths, workflow shapes,
asset layouts, and shell policy. A new Action/tool type or maintenance file
needs an explicit profile/contract review. The static workflow contract cannot
prove runtime behavior of arbitrary third-party actions or opaque executables;
its stated boundary is pinned workflow source and tested interpreter/path
surfaces.

## Remaining risks

The non-code-reachable Envoy `govulncheck` advisory rows remain dependency and
import evidence. Hosted PR-head security checks and the unavailable Envoy native
runtime still need separately observed evidence. Neither is dismissed, hidden,
or treated as merge authorization.

## Final diff and review status

This record is written before Parent staging, commit, push, PR creation, and
hosted-check evidence. It records only observed local evidence and reserves the
requested Draft-only delivery and exact-head review for subsequent controlled
steps.
