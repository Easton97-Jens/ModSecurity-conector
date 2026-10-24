# Finding-linked NGINX decision precedence and source intake

**Language:** English | [Deutsch](CR-20260929-findings-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260929-findings-remediation` |
| Date (UTC) | 2026-09-29 |
| Base revision | `d56af0856507eb048987974d3960e301e7c24371` |
| Source finding | `B09` / `csf_110c7b683d38cd566861364f` |
| Delivery target | Parent Draft PR #391; no merge |

## Motivation and problem statement

The user requested source-grounded handling of the supplied findings and one
Draft PR per selected repository. This is the first bounded implementation,
not a claim that all 59 consolidated work items have been remediated.

The source-ID-only [intake](../findings/20260929-intake.json) preserves all
72 original records, their reported severities, source-export hashes and the
agreed mapping to 59 work items. It does not publish raw reports, private
paths, payloads or author information. A08 maps to two separate connector
items; partial overlaps remain explicit rather than erasing independent
body or stream boundaries. Earlier conversational assessments are not fresh
verification and are not used to close or downgrade source findings.

The first published workflow incorrectly used the runner context in job-level
environment values. CI remediation moves TMPDIR into the executing step,
where that context is supported, without removing the regression command.
The Change Record now follows the existing bilingual schema; the checker
and its required sections are not weakened.

## Acceptance criteria

- A positive native intervention remains active even on an error-page request.
- Negative native results retain the existing fail-closed result.
- A zero P1 result continues into P2 even when the request is an error page.
- Ordinary no-intervention behavior and negative-result handling remain intact.
- The separate P2 result handler must not suppress a positive result.
- Request-processing, terminal-state and error guards remain in place.
- The original native error-page routing scenario still requires a pinned
  live-host regression before B09 can be considered verified.
- The dedicated workflow must execute its tests and the existing documentation
  and workflow checks must pass on the repaired PR head.

## Implementation decision and rationale

The shared classifier no longer derives an engine decision from the general
error-page marker. A zero P1 result stays ALLOW so request-body processing runs.
P1 and P3 callers continue using that classifier. The independent P2 handler
no longer returns early solely because of the marker; its negative-result,
decision-event and terminal-state handling is preserved.

The added C17 regression seam compiles the actual classifier and actual P1/P2
result tails, with controlled native-return and event-sink doubles. It covers
positive 302/403/451, zero and negative results with the marker both clear
and set. It is not a live NGINX or libmodsecurity integration test.

An independent intake test checks all 72 source aliases and the 59-item map.
A bounded read-only GitHub workflow executes these new tests at the PR head,
using action pins already present in this repository. The temporary directory
is created with a private umask before test execution. Existing required
checks, dependency locks, token permissions and quality gates remain intact.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `tests/test_nginx_error_page_intervention.py`
- `tests/test_security_finding_intake.py`
- `.github/workflows/ci-findings-regressions.yml`
- `reports/audits/findings/20260929-intake.json`
- This English/German Change Record pair.

## Commands executed

| Check | Actual evidence and limitation |
| --- | --- |
| Original GitHub base-file transfer | Both complete C files matched their Git blob SHA-1 before the initial edit |
| Original source comparison | Only the stated classifier/P2 changes; no unrelated source replacement |
| Original Python syntax / intake JSON | Parsed as data; not execution of the candidate tests |
| Local compiled/unit regression | NOT RUN: required RTK wrapper is unavailable |
| Local native build / live host | NOT RUN: no complete checkout or host build in the editing environment |
| Local git diff --check | NOT RUN; this API-delivered correction does not imply a local Git check |
| Original exact-head workflow | Invalid runner context prevented the intended dedicated regression run |
| Repaired exact-head workflow and full CI | Pending fresh results after this commit; no pass claimed here |

The available code-work skill was loaded. The repository-referenced global
execution skill was not accessible in the editing environment. No local
project command was silently substituted for the mandatory RTK path.

## Security impact

A real blocking/redirecting decision is no longer treated as absent merely
because NGINX is processing an error page. A no-decision P1 result no longer
skips P2 on an error-page request. Re-entrant error-page routing and final
host/client behavior still need live-host confirmation. This does not change
unsupported streaming, endpoint, socket, supply-chain or other connector
behaviors. The CI correction does not alter the product decision logic.

## Runtime evidence

No original-scenario live-host reproduction is established by this record.
The extracted C seam exercises only its declared layer. A successful build,
fixture, unrelated workflow or configuration load does not establish a
recursion-safe B09 runtime fix. Fresh head-bound CI results must be reviewed
separately before any verification claim.

## Known limitations

B09 remains a candidate patch, not verified or closed. Every other Parent
work item is unchanged in this draft. B03's Framework-owned entrypoint
mitigation is delivered separately; the root-cause code belongs to MRTS and
is not modified.

## Remaining risks

The independent Draft PRs #382 and #370 overlap NGINX-related work; PR #392
also touches the classifier. Their branches and evidence are not imported.
Integration requires a later reviewed comparison. Error-page recursion and
the complete P1/P2/P3 host flow require their own acceptance evidence.

## Checks not run and rationale

Local repository tests, full native builds and live-host acceptance were not
run because the editing environment lacks the required RTK execution path
and a provisioned repository/host environment. No omitted check is a PASS.
Pending checks on the repaired head are not replaced by old-head successes.

## Final diff and review status

The CI-remediation slice changes only the dedicated workflow and this paired
record. It preserves the regression commands and all pre-existing checks.
The PR remains a draft until current-head checks and review are complete.

Parent and Framework commits/PRs are independent. Both gitlinks remain
unchanged. No default-branch push, force-push, merge, risk acceptance, raw scan
publication or security-gate relaxation is performed by this change.
