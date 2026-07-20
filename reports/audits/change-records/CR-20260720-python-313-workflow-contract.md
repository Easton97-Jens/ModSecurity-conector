# Change Record: Parent Python 3.13 workflow contract and safe patch updater

**Language:** English | [Deutsch](CR-20260720-python-313-workflow-contract.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260720-python-313-workflow-contract` |
| Date (UTC) | `2026-07-20` |
| Base revision | `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` |
| Tracking | Parent Python-version/workflow contract. This record intentionally contains no commit, pull-request, CI, review, or delivery result. |
| Boundary | Parent Python-version source, workflow contracts, updater validation, and bilingual documentation only; Framework and MRTS are out of scope and unchanged by this documentation work. |

## Motivation and problem statement

The baseline uses a mixture of minor-only `3.13` setup steps and ambient or
bootstrapped Python execution paths. A minor-only declaration can drift to a
later patch release, while an ambient interpreter is neither a reproducible
version source nor evidence that `python` and `python3` name the same runtime.

The Parent also needs a safe way to propose, but never automatically apply, a
new stable Python 3.13 patch. Discovery of network metadata, compatibility
validation, and a write-capable pull-request publisher must not share one trust
boundary.

## Acceptance criteria

- One committed root `.python-version` file contains exactly stable
  `3.13.14` and is the only machine-readable interpreter source.
- Each of the 22 inventoried Parent Python-executing jobs sets up that source
  with `python-version-file: .python-version` and `check-latest: false` before
  its first Python use, then validates `python`/`python3` equivalence.
- Floating `3.13` is rejected for patch drift; an exact version plus a
  permanent canary is rejected because an independent read-only candidate
  validation stage supplies the required compatibility control.
- The updater uses only `https://www.python.org/api/v2/downloads/release/?is_published=true`, validates HTTPS, exact host `www.python.org`, no redirects,
  `application/json`, bounded data, and schema before selecting the highest
  published non-prerelease stable `3.13.N` patch. It cannot downgrade or cross
  a minor series.
- `--check` is read-only and separate from publisher-only `--update`; the
  three jobs are `resolve-python-patch`, `validate-python-patch`, and
  `create-python-update-pr`.
- The updater is triggered only by its Monday schedule and manual
  `workflow_dispatch`; every job is default-branch-ref gated and checks out
  the trusted default branch without submodules or persisted credentials.
- The resolver and validator remain read-only. Only the default-branch-gated
  publisher receives `contents: write` and `pull-requests: write`, and it may
  create a proposed pull request only after candidate re-resolution with
  `--expected-version`.
- The publisher uses the constant `automation/update-python-313` branch and
  stable title `chore(ci): propose Python 3.13 patch update`. It creates a
  Draft pull request once or safely updates only the existing repository-owned
  Draft update pull request for that branch after checking its head, default
  base, and disabled automatic merge; it refuses an existing branch without
  that exact pull request, so it neither duplicates proposals nor force-pushes.
- The generated English/German pull-request body records the prior and
  proposed versions, official release identity, metadata source, validation
  workflow/run URL, `.python-version` as the only changed file, retained
  Python 3.13 minor version, and no automatic merge.
- No auto-merge, default-branch write, force-push, repository or user-provided
  `secrets.*` consumption, submodule initialization, or arbitrary project
  workload execution is part of the updater contract. The publisher uses only
  GitHub's automatically provided job token, limited to its two job-scoped
  write permissions, for pull-request creation.
- English and German documentation and Change Record pairs have equivalent
  technical facts, limits, and evidence boundaries.

## Implementation decision and rationale

The selected strategy is exact stable `3.13.14` from the committed
`.python-version` file. `actions/setup-python` must consume it through
`python-version-file` with `check-latest: false`; a workflow must not carry a
second interpreter-version literal. This stops patch drift while retaining a
single reviewable version change.

| Strategy | Disposition | Reason |
| --- | --- | --- |
| Floating `3.13` | Rejected | Future runner/tool-cache resolution may change the patch without a reviewed source change. |
| Exact `3.13.14` from `.python-version` | Selected | One committed source produces deterministic setup for every covered job. |
| Exact version plus permanent canary | Rejected | The isolated candidate-validation job exercises the actual proposed patch before publishing, so a permanent canary would duplicate the relevant control. |

The complete baseline inventory is maintained in
[the Parent CI Python-version contract](../../../docs/build/README.md#parent-ci-python-version-contract): 22 Python-executing jobs, comprising 12
former minor-only setup paths and 10 formerly ambient or bootstrapped paths
that needed explicit setup before this implementation. The table identifies
each workflow, job, and direct or indirect Python execution chain. It
intentionally excludes jobs with no proven Python execution path.

The new updater workflow is deliberately separate from that inventory:

| Job | Contract |
| --- | --- |
| `resolve-python-patch` | Runs the current canonical interpreter, queries and strictly validates the fixed official structured API, then uses read-only `--check` to emit at most a higher stable `3.13.N` candidate. |
| `validate-python-patch` | Sets up the independently resolved candidate patch and validates it read-only before any publisher starts. |
| `create-python-update-pr` | Runs the current canonical interpreter, re-resolves the candidate with `--expected-version`, and uses publisher-only `--update` to create a PR from a default-branch-gated context. |

The only triggers are the scheduled Monday run and manual `workflow_dispatch`;
there is no push or pull-request trigger. Each job is default-branch-ref gated
and checks out the trusted default branch without submodules or persisted
checkout credentials. The candidate-validation job re-resolves the candidate,
runs the fail-closed static contract and compilation checks, and runs focused
Parent-native tests before the publisher becomes eligible.

This is a check/update separation: the candidate cannot be written merely
because it appeared in response metadata, and the publisher revalidates it at
the write boundary. The resolver and validator have no write role. The
publisher uses only `contents: write` and `pull-requests: write`; it has no
authority to merge, write the default branch, force-push, consume repository
or user-provided `secrets.*`, initialize submodules, or execute arbitrary
project workloads. Its repository execution is limited to the fixed
interpreter-verification and updater paths, and its GitHub-provided job token
is used only for pull-request creation.

The publisher uses the constant branch `automation/update-python-313` and a
stable title. It creates a Draft pull request if that branch is absent; for an
existing repository-owned Draft update pull request it verifies the exact head
repository, default base, and disabled automatic merge before restricting the
merge-base diff to `.python-version`, then updates that same pull request
without a force push. A pre-existing remote branch without that exact open
update pull request is a fail-closed error rather than a target for overwrite.
The English/German body always covers the prior and proposed versions, release
identity, metadata source, validation workflow/run URL, changed-file scope,
retained minor version, and absence of automatic merge.

## Security impact

The controlled input is release metadata from the fixed official API. The
trusted sink is a proposed `.python-version` update in a pull request, not a
default-branch mutation. Strict URL, transport, content-type, size, schema,
published/non-prerelease, exact-series, monotonic-patch, and expected-version
checks constrain that input before it reaches the write-capable publisher.

The independent validation job prevents the publisher from treating resolver
output as sufficient compatibility evidence. Default-branch gating, job-scoped
write permissions, no external or named `secrets.*`, no submodules, and no
arbitrary project workloads keep untrusted repository or metadata content from
sharing the publisher trust boundary. The GitHub-provided job token is limited
to pull-request creation. This is the checked-in static security contract, not
a claim that a GitHub Actions runtime control has already been observed.

## Changed files

The checked-in Parent implementation changes these path groups:

- `.python-version` as the sole machine-readable exact-version source.
- The 18 existing Python-executing workflows listed in the inventory and the
  new `.github/workflows/update-python-version.yml` updater workflow.
- `ci/checks/common/check-python-version-contract.py` and
  `ci/checks/common/check-python-interpreter-contract.py`, with the
  `Makefile` entry point that invokes the static contract.
- `scripts/update-python-version.py`, Parent-native updater/contract test
  modules, and their fixtures.
- `docs/build/README.md`
- `docs/build/README.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260720-python-313-workflow-contract.md`
- `reports/audits/change-records/CR-20260720-python-313-workflow-contract.de.md`

Framework and MRTS are not changed. This record reports only the observed
local implementation evidence below; it does not infer any remote result.

## Commands executed

| Command | Result |
| --- | --- |
| Isolated Python 3.13.14 running `check-python-version-contract.py --json`, `check-python-interpreter-contract.py`, and `make check-python-version-contract` | passed: the static inventory and the exact interpreter identity are valid. |
| Isolated Python 3.13.14 running `scripts/update-python-version.py --check --json` against the live fixed official API | passed: it reported `current` with current and latest version `3.13.14`; it did not modify `.python-version`. |
| `python3 -m unittest -v tests.test_update_python_version` | passed: 21 updater unit tests. |
| `actionlint -shellcheck=/usr/bin/shellcheck .github/workflows/*.yml ci/fixtures/workflow-permission-contract/*.yml` | passed. |
| `zizmor --offline .github/workflows` | passed with no findings. |
| Isolated Python 3.13.14 running `python3 -m unittest discover -s tests -v` | blocked/non-green: 355 tests ran; 13 failures and four errors depend on absent Framework files in this sparse worktree, including Framework runners, checks, and provisioning scripts. |
| `make setup-dev` with the isolated Python | blocked, exit 2: the Framework bootstrap attempted to create the unavailable local `.venv` development environment. |
| `make lint` with the isolated Python | blocked, exit 2: shell syntax and Python compilation checks ran, then the absent Framework `ci/checks/catalog/no_crs_baseline.py` stopped the target. |
| `make check-bilingual-docs` and the direct repository-path checker | blocked by the same pre-existing missing Framework documentation-link targets; none of this documentation deliverable's paths appears in the reported errors. |

These local results validate the checked-in static contract and updater paths.
They do not constitute a GitHub Actions run, pull-request, review, or delivery
result.

## Runtime evidence

Not applicable. This is a Parent CI/workflow and documentation contract; it
does not start a connector or establish HTTP/1.1, HTTP/2, HTTP/3, CRS,
Framework, MRTS, or host-runtime compatibility evidence.

## Checks not run and rationale

- `make check-doc-links` includes the Framework link checker. Its Parent path
  checker is also blocked by the same sparse-worktree Framework links; no
  workaround changes Framework or MRTS for this Parent task.
- GitHub Actions, pull-request, review, SonarQube, and merge evidence require
  an observed exact delivery head; none is inferred from this documentation.
- No connector build, runtime, Framework, or MRTS check is selected for this
  workflow-contract implementation. Framework and MRTS remain out of scope.

## Known limitations

This record documents a static contract and local checks. It cannot prove
GitHub-hosted runner behavior, future API availability, or a candidate patch's
compatibility until the independent validation stage actually runs. The base
inventory identifies the known Python execution chains; a later workflow that
introduces Python use must be added to the validator and documentation.

## Remaining risks

An official API response can be unavailable or change schema, and a valid
candidate patch can still expose a compatibility regression. Fail-closed API
validation, strict parsing, no-downgrade rules, independent candidate setup,
and PR-only publication reduce but do not eliminate those risks. There is no
risk acceptance, runtime result, or delivery result in this record.

## Final diff and review status

The bilingual documentation and Change Record reflect the checked-in
implementation and observed local validation. Framework-dependent link and
full-suite checks remain blocked as recorded above; commit, pull request,
exact-head CI/review/SonarQube evidence, and delivery state are intentionally
not asserted until observed.
