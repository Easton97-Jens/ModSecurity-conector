# Change Record: Parent NGINX maintainability remediation

**Language:** English | [Deutsch](CR-20260730-sonar-nginx-maintainability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-nginx-maintainability` |
| Date (UTC) | `2026-07-30` |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Source revision assessed | Local task patch against the stated base revision. |
| Boundary | Parent `connectors/nginx/` sources, one direct NGINX source-contract check, this EN/DE pair, and paired indexes only. No `.github`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, `NOSONAR`, direct default-branch action, or unrelated merge. The current user authorized only PR #206's controlled GitHub integration after a fresh exact-head verification. |
| SonarQube Cloud linkage | Targets 16 open current-master C code smells: `c:S3776` at access, Phase-4 and intervention paths; `c:S134` in request-header traversal; `c:S3358` in Phase-4 event selection; and `c:S1134`/`c:S1135` deferred-work markers. |

## Motivation and problem statement

The current Parent `connectors/nginx/` inventory reports 16 open
maintainability findings, while reporting zero bugs, vulnerabilities, security
hotspots, and duplicate lines. Three NGINX lifecycle functions exceed Sonar's
cognitive-complexity threshold, request-header traversal nests a second branch,
Phase-4 event construction uses two nested ternaries, and ten legacy
`FIXME`/`TODO` comments no longer describe pending actionable work.

The selected code handles request, response, and intervention state. The
remediation must lower function complexity without moving ModSecurity calls
across NGINX lifecycle boundaries or changing an intervention result, log
reason, status, or response-commit decision.

## Implementation decision and rationale

The access handler delegates connection, URI, header-list traversal, header
processing, body acquisition, stream-body append, and final body processing to
narrow helpers. Each retains the prior phase marker, PCRE pool pairing,
ModSecurity call order, event reason literal, and NGINX return condition. An
explicit header-part advance removes the former nested branch without changing
list iteration.

Phase-4 event construction now uses explicit status, message-ID, transport,
response-start, content-type, and bounded intervention-identifier helpers.
They retain the original values for `abort_connection`, `log_only`, `deny`,
`redirect`, and other actions. Redirect and status paths are separated while
the existing one cleanup tail remains.

Legacy deferred-work markers now state the supported lifecycle behavior. No
condition, request method, response filter, or runtime behavior is introduced
or removed. The direct source-contract test now extracts the access event by
balanced function scope rather than its previous adjacency to the handler;
this preserves its metadata-only logging assertion as helpers evolve.

## Acceptance criteria

- Every listed NGINX Sonar issue is removed by source change, without a
  suppression, policy, exclusion, Quality-Gate, or scanner change.
- Connection, URI, request-header, request-body, Phase-4 event, redirect, and
  status-intervention paths retain their original call order and returns.
- The direct NGINX Common-adoption and C-standard wiring controls pass.
- The exact future PR head has zero new SonarQube Cloud issues and `0.0%`
  New-Code duplication.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- this English/German Change Record pair and its indexes

## Commands executed

| Command or control | Result |
| --- | --- |
| `make check-nginx-common-adoption` | passed after the scoped function-extraction test update; mapper, Phase-3/4 event, bounded rule-ID, and response-body controls remain asserted. |
| `make check-nginx-c-standard-wiring` | passed; C17 remains mandatory and the source list is complete. |
| `make check-nginx-c17-lint` | passed its wiring/lint control and correctly reported native compilation blocked without NGINX headers/source. |
| Native `make check-nginx-c17` | `blocked_external_dependency`: the isolated task environment has no NGINX or libmodsecurity headers. Hash-checked task-local provisioning did not produce headers; no foreign cache or global installation was used. |
| `git diff --check` | passed. |

## Security impact

This is security-relevant because it refactors HTTP request, response, and
intervention handling. It introduces no new input, file, network, subprocess,
authorization, or logging-data path. Every ModSecurity phase call retains its
phase marker and PCRE pairing; the established connection/URI/body event
reasons, redirect allocation and `Location` construction, status update,
header-sent rejection, single cleanup tail, and metadata-only Phase-4 mapping
remain unchanged. A focused exact-diff security review is required before
delivery.

## Runtime evidence

No NGINX runtime or native C17 translation-unit compile ran. The dedicated
control correctly blocked before compilation because NGINX/libmodsecurity
headers were unavailable; constrained task-local provisioning did not establish
them.

## Known limitations

Source contracts are the strongest available local control, but do not replace
a hosted exact-head C17 build or SonarQube Cloud reanalysis. The repository-
wide documentation control also sees pre-existing missing Framework-submodule
link targets in this isolated worktree; it reports no other changed-record
error after the required sections are present.

## Remaining risks

Local NGINX runtime and native C17 translation remain unavailable as stated
above. The previously verified PR head is based on
`caddd86d1eede95de53aa1bc971dd26d875df21c`, while current `master` is
`4e5d45072bf32ff822f4b1039517026416259493`; strict rules therefore require a
task-branch update and a new exact-head review, GitHub-check, SonarQube Cloud,
and review-thread cycle before integration. This record does not claim a merge
or resulting-master state.

## Checks not run and rationale

- No NGINX runtime or native C17 translation-unit compile ran because the
  required NGINX/libmodsecurity headers are unavailable in this task-local
  environment and provisioning did not establish them.
- Resulting-master workflows and any resulting-master SonarQube Cloud analysis
  cannot run until PR #206 is actually merged at its final exact head.

## Delivery status

Draft PR [#206](https://github.com/Easton97-Jens/ModSecurity-conector/pull/206)
exists against `master`. Its final pre-integration head
`9746d81cd73c54300d709357db453a93f4f358df` had matching local, remote, and
GitHub heads; 33 hosted checks passed with zero failures, no review or review
thread existed, the Quality Gate was `OK`, and SonarQube Cloud reported zero
OPEN/CONFIRMED PR issues, zero new violations, and `0.0%` / zero New-Code
duplication. Those facts apply only to that exact head and its then-current
base. Because `master` subsequently advanced, they do not authorize a merge
until the task branch is updated and the full verification cycle is repeated.

## Master-integration authorization

On `2026-07-30` the current user explicitly authorized: “bringe das pr 206 in
den master”. The authorized repository is
`Easton97-Jens/ModSecurity-conector`; the inventory is this single task-owned
Parent PR #206; it has no authorized dependent Framework, MRTS, Gitlink, or
other-PR action; and its merge order is therefore one item. The active ruleset
allows `merge`, `squash`, and `rebase`; the repository's current default is
`squash`, which will be used only with GitHub exact-head protection after all
current preconditions pass. No direct `master` push, administrator bypass,
auto-merge, or unobserved merge result is authorized or claimed.

## Final diff and review status

The local source diff passed whitespace, NGINX Common-adoption,
C-standard-wiring, and C17-lint controls. A focused security review found no
plausible diff-induced candidate. Native C17 compilation remains blocked as
stated above. The final pre-integration PR head passed hosted checks and exact
Sonar readback. The necessary branch-base and Change-Record update must now
receive the same controls on its new exact head; no master claim is made until
the post-merge result is observed.
