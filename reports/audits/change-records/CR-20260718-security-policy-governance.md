# Change Record: Security policy and governance baseline

**Language:** English | [Deutsch](CR-20260718-security-policy-governance.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-security-policy-governance` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Boundary | Parent documentation and GitHub repository governance only; product source, product tests, Framework, MRTS, gitlinks, and `master` remain unchanged. |

## Motivation and problem statement

The repository had no GitHub-recognized `SECURITY.md`, while private
vulnerability reporting was available. The current Scorecard Security-Policy
finding therefore lacked a discoverable confidential reporting path. This
change adds a truthful, public policy that routes reports to GitHub Private
Vulnerability Reporting without publishing private contact details or secrets.

## Acceptance criteria

- Root `SECURITY.md` and `SECURITY.de.md` provide equivalent English and German
  policy content with reciprocal language links.
- The policy directs reporters to the repository's GitHub private reporting
  URL, tells them not to disclose sensitive details publicly, and does not
  contain private contact data, credentials, or secrets.
- The documentation is created only on this dedicated branch and pull request.
- Bilingual documentation, link, whitespace, and scoped-diff controls pass
  before the pull request is reported as locally validated.

## Implementation decision and rationale

The root filename is GitHub's discoverable security-policy location. The
policy is intentionally concise: it describes the private reporting channel,
supported-version boundary, safe-research scope, and response/disclosure
expectations without an invented service-level commitment. The complete German
companion follows the repository's reader-facing documentation policy.

## Changed files

- `SECURITY.md`
- `SECURITY.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- This English/German Change Record pair.

## Commands executed

| Command | Result |
| --- | --- |
| `git status --short --branch` in the dedicated temporary clone | passed before editing: clean `master...origin/master`. |
| `git switch -c codex/security-policy-20260718` in the dedicated temporary clone | passed: created the task-owned branch from base revision `c8ca0d92b630c18232b881855c4f5d1482568ea6`. |
| GitHub repository governance readback | passed before documentation work: private vulnerability reporting is enabled, the active `Protect master` ruleset has no bypass actors, and the required-check PR behavior is pending this pull request. |
| `git diff --cached --check` | passed: no whitespace error in the six task-owned documentation files. |
| Targeted existing bilingual/link control | passed: the repository's `check-bilingual-docs.py` pair and link functions report no error for `SECURITY.md`, `SECURITY.de.md`, or this Change Record pair. |
| `make check-bilingual-docs` | blocked: the full-tree checker ran but reported only pre-existing missing Framework-gitlink targets in the isolated clone; no task-owned document error was reported. |
| `make check-doc-links` | blocked by the same unpopulated Framework gitlink; its reported paths do not include a task-owned document. |
| GitHub PR [#53](https://github.com/Easton97-Jens/ModSecurity-conector/pull/53) at initial head `002299a09bd2d9b6f640e9d29c2d8b5068700652` | passed: `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`, zero review threads, and all six exact required checks (`actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, `zizmor`) completed successfully from GitHub Actions app `15368`. No review, bypass, or merge occurred. |

## Security impact

This is a documentation and governance-hardening change. It gives reporters a
confidential, GitHub-hosted channel and warns against public disclosure of
secrets or exploit details. It does not change connector runtime behavior,
authentication, authorization, cryptography, dependency versions, or scanner
configuration.

## Runtime evidence

No connector runtime behavior changes. PR #53 supplied the observed control
evidence for GitHub's `pull_request` rule and its six exact required checks:
the initial delivery head was clean and mergeable with zero unresolved review
threads. Runtime evidence is not applicable.

## Known limitations

The repository has one direct administrator and no independent reviewer, so a
one-approval requirement is not enabled without an automatic bypass. The
SonarCloud result on `master` was failed during required-check preflight, so
it is not a required check even though PR #53 later reported a passing
SonarCloud result. Automated security fixes remain disabled by deliberate
scope decision.

## Remaining risks

The policy cannot guarantee response timing or fix every report. A collaborator
with review authority is still required before a one-human-review rule can be
enabled without a lockout. Fuzzing, expanded C/C++ SAST, CII badge registration,
and Scorecard vulnerability-lead triage require separate evidence-backed work.

## Checks not run and rationale

Full-tree documentation checks cannot pass in this isolated clone until the
pre-existing Framework gitlink is populated; no Framework materialization is
in this task's scope. Pull-request creation, exact required-check runs, and
review/thread state were recorded on PR #53; the final task receipt verifies
the final branch head after this Change Record update.

## Final diff and review status

Targeted bilingual/link control and the staged scoped-diff whitespace review
passed. The initial six-file delivery was committed at
`002299a09bd2d9b6f640e9d29c2d8b5068700652`, pushed to the dedicated branch,
and opened as PR #53. Its exact required checks succeeded, the PR became
clean and mergeable, and no review-thread, bypass, merge, or `master` change
occurred. This Change Record update preserves that observed delivery evidence;
the final branch-head status is retained separately in the task receipt. The
full-tree documentation checks remain environment-blocked only by the
unpopulated Framework gitlink.
