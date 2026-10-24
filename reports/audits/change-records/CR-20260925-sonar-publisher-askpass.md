# Change Record: SonarCloud publisher credential-delivery remediation

**Language:** English | [Deutsch](CR-20260925-sonar-publisher-askpass.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260925-sonar-publisher-askpass |
| Date (UTC) | 2026-09-25 |
| Base revision | `92d4498b6f219704fee9363aa5c3ef7b5a2f7fb4` |
| Finding | Four Parent `yaml:S2068` findings: `AaDXyDL2LGpgyOOFVN7p`, `AaDXyDL2LGpgyOOFVN7q`, `AaDXyDIrLGpgyOOFVN7n`, `AaDXyDIrLGpgyOOFVN7o` |
| User authorization | Inspect the supplied SonarCloud project, fix findings safely on a separate branch, create a pull request if possible, and verify it. |
| Delivery status | Parent-only change on `fix/sonar-publisher-askpass`; Draft PR to `master` planned. No merge, direct `master` write, Framework/MRTS change, suppression, issue acceptance, or Quality-Gate change. |

## Motivation and problem statement

The exact `master` readback found eight unresolved SonarCloud issues. Four are
Parent `.github/workflows` `yaml:S2068` findings in these two updater
workflows. They match a custom Git credential helper that emits an App-token
credential response. The value is not hard-coded, but embedding the response
in local Git configuration is unnecessary and brittle.

The three Framework workflow `yaml:S2068` findings and one Framework
`python:S1192` code smell are outside this Parent-only boundary.

## Acceptance criteria

- Remove all four reported Parent `credential.helper` occurrences.
- Preserve the existing publisher-only repository-limited GitHub App-token source.
- Retain `persist-credentials: false`, trusted publisher gates, and non-interactive Git.
- Use only a short-lived, owner-readable askpass program for the Git password prompt and remove it on exit.
- Add a focused regression contract for both Parent publishers.
- Do not weaken SonarCloud, the Quality Gate, validation, token permissions, or repository protections.

## Implementation decision and rationale

Each affected publisher step creates a `0700` temporary `GIT_ASKPASS`
program below `$RUNNER_TEMP`. Its quoted heredoc retains only the variable
reference, not the token value. Each `publisher_git` network call supplies `-c credential.helper=` to reset
inherited helpers, command-local
`credential.https://github.com.username=x-access-token`, and
`credential.https://github.com.useHttpPath=false`. Before the wrapper exists,
the step verifies that `origin` is one of the two direct canonical GitHub URLs,
then uses the fixed canonical repository URL directly for every publisher fetch
and push. That prevents an `origin` push URL or extra remote URL from
redirecting a token-bearing operation. The token-free askpass program fails
closed unless the prompt identifies `github.com` with a host boundary.

`GIT_TERMINAL_PROMPT=0` and `GIT_ASKPASS` are command-local, not exported. An
EXIT trap removes the script. Existing checkout, branch
gate, App-token permission, path-validation, and force-with-lease controls
are unchanged.

## Security impact

The token's source, scope, and publisher-only boundary are unchanged. It is
not persisted in Git configuration or supplied in a remote URL or command-line
argument. Publisher fetches and pushes address the fixed canonical URL instead
of the `origin` alias, so configured push URLs cannot redirect the App token.
The existing trusted repository/default-branch event gates still prevent
untrusted events from reaching the publisher.

## Changed files

- `.github/workflows/update-workflow-tools.yml`
- `.github/workflows/update-python-version.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260925-sonar-publisher-askpass.md`
- `reports/audits/change-records/CR-20260925-sonar-publisher-askpass.de.md`

Framework source, gitlinks, MRTS source, SonarCloud settings, and GitHub
repository settings are unchanged.

## Commands executed

| Check | Result |
| --- | --- |
| Exact `master` SonarCloud issues before the patch | Eight unresolved issues: four Parent `yaml:S2068` in scope, three Framework `yaml:S2068`, one Framework `python:S1192`. |
| Exact `master` GitHub SonarCloud check before the patch | Failed: Security Rating on New Code `C`; required `A`. |
| Source transformation review | Four Parent helper occurrences are replaced by four askpass flows; checkout persistence and publisher App-token mappings remain. |
| Initial Draft-PR head hosted checks | Failed during repair: the bilingual-document validator required repository-specific Change Record headings and the existing no-`gh`-CLI contract matched a prose phrase. This successor corrects both; recheck is pending. |
| Hosted checks and PR analysis | Pending for the exact Draft-PR head at record creation; inspect PR checks before merge. |

## Runtime evidence

No connector runtime behavior changes. This only affects credential delivery
inside scheduled or manually dispatched maintenance publishers.

## Checks not run and rationale

Local repository commands were not run: this execution surface has no local
checkout or repository-required RTK command environment. The update publishers
were not manually dispatched because that could create or update a maintenance
branch or pull request outside the requested Sonar remediation.

## Known limitations

The Parent-only repair leaves four Framework-bound findings unchanged; those
require a separately scoped Framework task. An actual publisher Git push needs
a valid maintenance candidate, so static and hosted checks are the available
safe evidence for this change.

## Remaining risks

The temporary program is created on a trusted GitHub-hosted runner and removed
on EXIT, but a future workflow change could weaken that property. The source
regression test guards the intended form; hosted checks and SonarCloud analysis
must still pass for the exact PR head before merge.

## Final diff and review status

The scoped diff changes two Parent maintenance publishers, a focused regression
contract, and this bilingual Change Record. No merge is performed. Final status
depends on the exact Draft-PR head, not the pre-merge `master` analysis.
