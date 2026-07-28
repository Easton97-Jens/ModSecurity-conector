# Change Record: Parent Apache H2 transport-result literal ownership for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260728-sonar-apache-h2-transport-s1192.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-apache-h2-transport-s1192 |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Candidate designation | Parent #155 candidate. This local designation does not claim a hosted PR, remote head, review, Quality Gate, or delivery outcome. |
| Tracking | `AZ98JczJLJyjbmyNA5LW`, `AZ98JczJLJyjbmyNA5LO`, `AZ98JczJLJyjbmyNA5LS`, and `AZ98JczJLJyjbmyNA5LU`; all are live Parent `shelldre:S1192` findings before this candidate. |
| Boundary | Parent Apache Phase-4 H2 smoke harness, this English/German Change Record pair, and its two indexes. Framework, MRTS, Gitlinks, workflows, reports, scanner policy, and hosted state are unchanged. |

## Motivation and problem statement

Five Apache H2 smoke paths repeat the same curl feature expression, status and
version write-out grammar, and first-record awk programs. SonarQube Cloud
reports the four repeated literals as S1192 maintainability findings. The code
is on a fail-closed Phase-4 transport boundary, so literal ownership must not
alter whether a missing H2-capable curl blocks a case, what curl writes, or how
the first transport record is parsed.

## Acceptance criteria

- Each selected literal has one immutable file-local owner and is used at the
  five existing H2 sites only.
- All H2 support checks retain `grep -E ... || blocked` behavior.
- Curl retains its exact status/version write-out argument, argument ordering,
  output sink, and the same single-URL two-field record grammar.
- The two awk programs still select fields one and two of the first tab-
  delimited record only.
- Shell syntax, focused Apache Phase-4 wiring, whitespace, bilingual
  documentation, and exact-head hosted evidence must be recorded truthfully.

## Implementation decision and rationale

The harness now declares four POSIX `readonly` values near its other file-
local configuration:

- `CURL_HTTP2_FEATURE_PATTERN`
- `CURL_HTTP_STATUS_VERSION_FORMAT`
- `AWK_FIRST_TAB_RECORD_STATUS`
- `AWK_FIRST_TAB_RECORD_VERSION`

They are initialized from the exact former single-quoted literals and used
only through double-quoted expansions. This preserves one shell argument for
each grep, curl, or awk invocation while avoiding word splitting, globbing, or
shell interpretation of the embedded awk field references. The distinct
multi-URL transfer grammar elsewhere in the harness is deliberately not
combined with this two-field H2 result contract.

## Changed files

- `connectors/apache/harness/run_apache_smoke.sh`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-h2-transport-s1192.md`
- `reports/audits/change-records/CR-20260728-sonar-apache-h2-transport-s1192.de.md`

## Commands executed

| Command or control | Actual result |
| --- | --- |
| `sh -n connectors/apache/harness/run_apache_smoke.sh` in the exact task worktree | passed. |
| `/root/git/ModSecurity-conector/.venv/bin/python -B tests/test_apache_phase4_response_regression_wiring.py` with bytecode/user-site disabled in the exact task worktree | passed: 10/10 tests. |
| `git diff --check` | passed; no whitespace error. |
| Focused shell/protocol security review | approved; no plausible or validated finding. |

## Security impact

The candidate affects shell arguments used for HTTP/2 capability detection,
curl transport-result output, and awk parsing. The reviewed invariant is that
H2-only cases remain blocked unless curl exposes H2 support and that the
response privacy checks consume the same status/version record without moving
response bodies, headers, trace data, or stderr into a shell-evaluated
context.

The values are fixed source literals, declared before every use, and always
expanded double quoted. The review found that POSIX `readonly` syntax, curl
argument ordering, write-out bytes, first-record parsing, and existing output
sinks remain unchanged. No controlled request, response, environment value, or
command substitution becomes a grep regex or awk program. No security finding
was identified by this focused review.

## Runtime evidence

No Apache host runtime, connector matrix, Framework, or MRTS runtime was
started. The shell syntax and focused source-wiring test are local contract
evidence only; they do not establish deployment compatibility or a promoted
runtime capability.

## Known limitations

This record has no hosted exact-head PR, SonarQube Cloud post-change issue,
Quality Gate, workflow, review, merge, or default-branch evidence. It does not
claim a full Apache H2 runtime result. The pre-existing pipeline-status
characteristic of `curl --version | grep` was reviewed but is unchanged and no
concrete new fail-open path was shown.

## Remaining risks

A future harness change could introduce a new hard-coded equivalent literal,
change a curl record grammar, or alter an H2 gate outside this scope. Fixed
literal owners, direct wiring coverage, shell syntax, and the focused review
reduce that risk. A fresh exact-head hosted analysis remains required before
the four cited receipts are treated as resolved.

## Checks not run and rationale

- No Apache host build, real H2 smoke runtime, full matrix, report generation,
  workflow execution, Framework source check, or MRTS check was run; each is
  outside this Parent-only literal extraction.
- Repository-wide documentation checks and hosted PR/Sonar evidence are not
  yet available for this candidate. A later disposable Parent/Framework
  documentation overlay and exact-head hosted cycle are required before
  delivery is considered verified.

## Final diff and review status

The local candidate changes only the four literal owners and their twenty H2
call sites, plus this paired traceability update and its indexes. The focused
syntax/test/whitespace/security evidence above passed. No commit, push, PR,
hosted check, Quality Gate, review, merge, master change, Framework/MRTS
change, Gitlink update, workflow change, or scanner-policy action is claimed.
