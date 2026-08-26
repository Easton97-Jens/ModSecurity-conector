# P1–P4 connector parity: scoped security-scan milestone

**Language:** English | [Deutsch](p1-p4-connector-security-scan.de.md)

## Purpose, scope, and evidence boundary

This report records the completed standard security-scan milestone for the
user-requested P1–P4 connector-parity program. It covers Parent `common/` and
`connectors/` at the task-worktree revision rooted in
`2bd99f47d61c7dc9d7db847112725d60b49dc1f4`; it does not claim final
connector parity or a real-host matrix result.

The scan is retained and sealed in run
`20260826T175448Z-p1-p4-connector-parity-20260826-ea15c4bb`. Its canonical
`findings.json` SHA-256 is
`18d6248c2d85ce0e1457a62a6682fe8e3abd567af47ed430945ec01788e8c35d`.
Framework, MRTS, CI workflows, GitHub configuration, remote deployment, and
hosted tests were excluded. No raw request or response body was retained.

## Result and disposition

The scan contains eleven security records. One is locally reproduced and
release-blocking; eight are source-confirmed candidates awaiting the recorded
host/runtime controls; two enrich existing canonical findings.

| Finding(s) | Disposition | Evidence boundary |
| --- | --- | --- |
| `FND-PARENT-0958` | P0/high, locally reproduced, `validated`, release blocker | A public-API Go reproduction shows a nonempty Traefik Native UDS request reaching an unread downstream handler, returning HTTP 204 with zero P2 body callbacks and no request EOS. |
| `FND-PARENT-0959`, `FND-PARENT-0960` | P1/medium, `triaged` candidates | HAProxy SPOP deadline and peer-disconnect/SIGPIPE paths require selected runtime proof. |
| `FND-PARENT-0961` | P2/medium, `triaged` candidate | NGINX callback logging must be exercised with `modsecurity_use_error_log` both off and on. |
| `FND-PARENT-0962`–`FND-PARENT-0964` | P1/P2 candidates | Common header syntax, host-action event association/integrity, and JSONL UTF-8 require parser and consumer controls. |
| `FND-PARENT-0965`, `FND-PARENT-0966` | P1/medium, `triaged` candidates | Traefik C-engine result-write deadline and Envoy ext_proc forced-shutdown drain require controlled peer/stream tests. |
| `FND-PARENT-0007`, `FND-PARENT-0135` | Existing records enriched | The scan adds source evidence for Traefik worker admission and the ext_proc plaintext non-loopback boundary without strengthening their lifecycle disposition. |

The P0 finding blocks verified PR status and any master integration. The
candidate records do not claim a runtime exploit, a completed repair, or a
fully runtime-verified connector.

## Validation actually performed

| Check | Actual result |
| --- | --- |
| Traefik Native UDS `go test -count=1 -race ./...` | Passed using task-owned Go cache and temporary storage. |
| Traefik Native UDS `go vet ./...` | Passed. |
| Envoy ext_proc `go test -count=1 -race ./...` | Passed for command, composite, and processor packages using task-owned cache/module-cache/tmp paths. |
| Envoy ext_proc `go vet ./...` | Passed. |
| Isolated unread-body public-API reproduction | Passed while observing HTTP 204, zero request-body callbacks, and `RequestEOS=false`; evidence is retained separately from versioned documentation. |
| Standard scoped Codex Security scan | Completed and sealed; manifest, coverage, report, findings JSON, and SARIF are retained locally. |

These checks are source-level or isolated controls. They do not substitute for
Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd real-host evidence.

## Source-ownership and remediation gate

No product source repair is included in this milestone. The required Common
and connector paths overlap unmerged Draft PRs #344, #345, and #346. The
current task must not copy, rebase, merge, or silently duplicate their source
changes. A current user decision selecting integration or supersession is
required before a competing repair can be written.

Once selected, repair and independently verify `FND-PARENT-0958` first:
configured body inspection must deliver P2 and exactly one request EOS before
downstream execution or fail safely; unread, normal-read, empty-body,
cancellation, later-request, real Traefik/UDS, and cleanup controls must pass.
Then promote each candidate only after its documented negative and legitimate
host controls establish reachability and impact.

## Known limitations and next milestone

The current environment has no selected Apache, NGINX, HAProxy, Envoy,
Traefik, or lighttpd host executable and the Framework Gitlink is not
initialized. Therefore all real-host P1–P4 evidence remains unrun, not
inapplicable. The repository documentation-wide bilingual and link checks
remain blocked by pre-existing absent Framework targets; this milestone does
not modify Framework/MRTS, CI, Gitlinks, dependencies, branch protection, or
required checks.

The Draft PR is updated with this evidence-bounded documentation milestone.
It remains a Draft; no merge, direct `master` push, hosted-check claim, or
final parity claim is made.
