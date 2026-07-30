# Change Record: Parent NGINX maintainability remediation

**Language:** English | [Deutsch](CR-20260730-sonar-nginx-maintainability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-nginx-maintainability` |
| Date (UTC) | `2026-07-30` |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Source revision assessed | Local task patch against the stated base revision. |
| Boundary | Parent `connectors/nginx/` sources, one direct NGINX source-contract check, this EN/DE pair, and paired indexes only. No `.github`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, `NOSONAR`, default-branch action, or merge. |
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

The required final security-diff review, exact-head hosted checks, SonarQube
Cloud issue readback, and new-code duplication result remain pending. This
record does not claim a review approval, merge, or resulting-master state.

## Checks not run and rationale

- No NGINX runtime or native C17 translation-unit compile ran because the
  required NGINX/libmodsecurity headers are unavailable in this task-local
  environment and provisioning did not establish them.
- Hosted GitHub Actions, SonarQube Cloud, review, approval, merge, and master
  checks cannot run until the exact Draft-PR head exists.

## Delivery status

Draft PR [#206](https://github.com/Easton97-Jens/ModSecurity-conector/pull/206)
exists against `master`. Its initial source head was
`33d05fd3d2acf3db792b350cefe22c937cdc2377`; local, remote, and GitHub heads
matched, all observed required checks were terminal without a failure, the
Quality Gate was `OK`, and SonarQube Cloud reported zero OPEN/CONFIRMED PR
issues, zero new issues, and `0.0%` New-Code duplication. This delivery-status
update creates a new exact PR head, which must receive fresh hosted and Sonar
verification before the PR can be treated as verified. No merge or master
action is authorized or implied.

## Final diff and review status

The local source diff has passed whitespace, NGINX Common-adoption,
C-standard-wiring, and C17-lint controls. A focused security review found no
plausible diff-induced candidate. Native C17 compilation remains blocked as
stated above. The initial PR head passed hosted checks and exact Sonar readback;
this documentation-only update requires the same controls on its new exact
head. No master claim is made.
