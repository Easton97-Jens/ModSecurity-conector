# Change Record: Parent HAProxy complete SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-haproxy-complete-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260801-sonar-haproxy-complete-remediation |
| Date (UTC) | 2026-08-01 |
| Base revision | `f70110536cd163cebce5f57ccd8ca95d5cf9f02b` |
| Tracking | Complete current `connectors/haproxy/` SonarQube Cloud remediation. Hosted verification passed for refreshed PR head `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198`; this delivery-record correction requires one further exact-head cycle before merge. |
| Boundary | Parent `connectors/haproxy/`, its direct tests/checks, and this bilingual Change Record/index pair. Framework, MRTS, Gitlinks, other connectors, workflows, Sonar configuration, suppressions, and direct `master` writes remain out of scope. The current user authorized only controlled PR #210 integration into `master`. |

## Motivation and problem statement

The current-master SonarQube Cloud inventory filtered by the canonical
`connectors/haproxy/` component prefix contains 33 open/confirmed rows: one
`python:S5332` security signal and 32 maintainability rows. The task requires
that entire current scope to be remediated in one focused PR without changing
Sonar rules, exclusions, quality gates, or scanner suppressions.

The first exact-head analysis of Draft PR #210 identified three additional
PR-owned reliability rows in the refactored runtime: two `c:S995` constness
rows and one `c:S836` uninitialized-value error path. This follow-up commits
the narrow type/initialization repair before a new exact-head analysis.

| Rule | Count | Remediation disposition |
| --- | ---: | --- |
| `python:S5332` | 1 | Replaced the generic URL opener with the already constrained direct loopback HTTPS client. |
| `python:S9073` | 3 | Split compound module-loader assertions into explicit preconditions. |
| `c:S107` | 1 | Replaced the wide legacy-server parameter list with a typed configuration object. |
| `c:S134` | 9 | Moved nested SPOP and lifecycle branches into named helpers. |
| `c:S1820` | 2 | Grouped cohesive C17 runtime/config members without changing their direct access contract. |
| `c:S3358` | 5 | Replaced nested conditionals with explicit branches and accessors. |
| `c:S3776` | 5 | Separated request, response, parser, server, and command-dispatch responsibilities. |
| `c:S5350` | 1 | Restored a read-only configuration value pointer. |
| `c:S5955` | 2 | Replaced fragile indexed command loops with an explicit cursor helper. |
| `c:S886` | 4 | Kept loop-control variables local to their command-parser helpers. |
| `c:S995` (PR follow-up) | 2 | Marks read-only notify inputs as `const`. |
| `c:S836` (PR follow-up) | 1 | Initializes the error-path value pointer before it can be logged. |

## Acceptance criteria

- Cover every currently inventoried HAProxy row with a source-level change or
  an explicit, testable disposition.
- Preserve bounded SPOP parsing, transaction cache lifecycle, ModSecurity
  request/response processing, private runtime-file behavior, and loopback
  TLS confinement.
- Compile changed C as C17 with `-Wall -Wextra -Werror`.
- Keep PR new-code violations and duplication at zero, as verified only by a
  fresh SonarQube Cloud analysis of the exact PR head.
- Keep all changes Parent-only; integrate only through the current authorized,
  exact-head-protected PR #210 workflow.

## Implementation decision and rationale

The HTX smoke helper now sends its already-validated local HTTPS request with
`http.client.HTTPSConnection`, the existing private-root certificate loader,
and an explicit response/connection cleanup path. It does not reintroduce
redirect handling or relax the credential-free `https://127.0.0.1` predicate.

The native binding extracts its repeated request lifecycle into helpers that
retain the original defaults, libmodsecurity invocation order, disruptive
decision checks, and one final cleanup path. The SPOP runtime separates typed
HELLO parsing, request/response construction, transaction completion, notify
dispatch, runtime-file setup, and command-line parsing. The helpers preserve
the prior bounded parser primitives and the distinction between request body
limits, optionally configured response body limits, and legacy unbounded
evaluation.

The PR follow-up makes the two helper input pointers read-only and initializes
the configuration-loader value pointer to a known null value. The latter keeps
the existing error message deterministic when a trailing `--config` lacks its
argument; it does not change accepted command-line syntax.

## Security impact

The changed paths process untrusted SPOP frames, HTTP request metadata/body,
local runtime-root paths, and a loopback TLS endpoint. The security invariant
is preserved: only bounded typed frame data reaches request fields; the
transaction lifecycle cannot skip its existing abort/store/finish rules; TLS
probes remain credential-free HTTPS to literal loopback with the verified
private-root certificate; and evidence retains metadata rather than payloads.
No authentication, parser, TLS, file-containment, logging, test, scanner, or
quality-gate control was weakened. No `NOSONAR`, suppression, exclusion, or
Sonar configuration change was used.

The sealed local security-diff review of the initial exact four-file patch and
the subsequent three-file PR follow-up both recorded zero new reportable
security findings. Their retained reports are
`/var/tmp/codex/ModSecurity-conector/runs/haproxy-complete-sonar-pr-20260801/security-diff-scan-c3319575/report.md`
and
`/var/tmp/codex/ModSecurity-conector/runs/haproxy-complete-sonar-pr-20260801/security-diff-scan-follow-up-4b364607/report.md`.

## Changed files

- `connectors/haproxy/harness/haproxy_htx_smoke_helper.py`
- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- This English/German Change Record pair and both Change Record indexes.

## Commands executed

| Control | Result |
| --- | --- |
| `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only -Icommon/include -Iconnectors/haproxy/src connectors/haproxy/src/haproxy_modsecurity_binding.c` | blocked: installed libmodsecurity headers do not declare `msc_get_rules_messages_rule_ids` |
| `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only -Icommon/include -Iconnectors/haproxy/src connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | passed |
| `python3 -m unittest tests.test_sonar_reliability_contract tests.test_haproxy_htx_transaction_id` | passed: 15 tests |
| `python3 ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | passed |
| `python3 ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | passed: 26 checks |
| `python3 -m py_compile connectors/haproxy/harness/haproxy_htx_smoke_helper.py connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` | passed |
| `python3 ci/checks/documentation/check-bilingual-docs.py` | blocked only by missing links into the deliberately uninitialized Framework submodule; no error named either new Change Record or index |
| `git diff --check` | passed |
| Codex Security security-diff finalization | passed: initial four-file and follow-up three-file coverage, zero reportable findings |
| `gh pr checks 210` at `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` | passed: 33 checks, 0 failed |
| SonarQube Cloud PR #210 at `4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` | passed: Quality Gate `OK`, 0 new issues, 0.0% new-code duplication |

## Runtime evidence

`tests.test_haproxy_htx_transaction_id` performs the legitimate loopback TLS
probe and the unsafe-URL control. The contract checks cover static parser,
transaction, HTX, and Common-adoption invariants. They do not claim a full
native HAProxy-plus-libmodsecurity runtime result.

## Checks not run and rationale

`make -C connectors/haproxy build-modsecurity-binding` is
`blocked_external_dependency`: the project-native target cannot find
libmodsecurity development headers or the library under `/src` or the
registered task build root. The focused harness module is also not run as one
whole module because it imports a deliberately uninitialized Framework
submodule in this Parent-only worktree. No Framework source, Gitlink, stub,
or bypass was introduced to alter that boundary. The local Sonar scanner is
not installed; therefore SonarQube Cloud verification occurs on the exact
published PR head. The refresh head
`4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` passed; this documentation-only
delivery-record correction creates a new head that must receive the same
hosted evidence before merge.

The independent Binding syntax command reaches the installed, incompatible
libmodsecurity declaration set: it lacks
`msc_get_rules_messages_rule_ids`. This is also an external dependency limit;
no artificial declaration or compiler-warning relaxation was added.

The whole-tree bilingual-documentation checker was run after this record was
added. It reports only existing links into the same deliberately uninitialized
Framework submodule; no new Change Record or index diagnostic remains. The
Framework was not initialized merely to make a Parent-only documentation check
green.

## Known limitations

Draft PR #210 was created from the initial remediation commit. Its first
exact-head analysis correctly exposed the three PR-owned rows documented above.
After the current-master refresh, head
`4dbd7c0e2bf49374c4d1e70e2cfc0fb51c060198` passed all 33 hosted checks and
the SonarQube Cloud Quality Gate with zero new issues and zero new-code
duplication. The present documentation-only delivery-record correction changes
the PR head again, so its final exact-head checks and Quality Gate must be
observed before the authorized merge. No review or merge is claimed here.

## Remaining risks

The final documentation-correction head may receive a different hosted result.
Any nonzero new violation, new duplicated line, new-code duplication density,
failed required check, blocking review, or unresolved conversation requires
task-owned follow-up before the PR can be merged.

## Final diff and review status

The local diff is limited to the Parent HAProxy scope and Change Record pair.
The current user explicitly authorized `bringe das pr 210 in den master`.
After the documentation-only follow-up commit, its new exact head requires a
fresh final checks, review, conversation, and SonarQube Cloud round. The
authorized integration then uses the repository's established squash method
with exact-head protection; no direct `master` write, bypass, or auto-merge is
allowed.
