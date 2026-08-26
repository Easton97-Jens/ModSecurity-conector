# Change Record CR-20260826: P1–P4 connector-parity security-scan milestone

**Language:** English | [Deutsch](CR-20260826-p1-p4-connector-security-scan.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260826-p1-p4-connector-security-scan` |
| Date (UTC) | `2026-08-26` |
| Base revision | `2bd99f47d61c7dc9d7db847112725d60b49dc1f4` |
| Scope | Parent-only security-scan milestone report, German companion, paired Change Record, and bilingual archive indexes. No connector/Common source, Framework/MRTS source, Gitlink, dependency, CI/workflow, branch-rule, required-check, or hosted-test configuration change. |

## Motivation and problem statement

The user requested a step-by-step ten-connector P1–P4 parity program with a
regularly updated task-owned Draft PR. The baseline established that this work
crosses request/response, UDS, gRPC, event, lifecycle, and resource-security
boundaries. This milestone records a completed scoped security scan before
competing source implementation is permitted.

## Acceptance criteria

This milestone is accepted only if it:

- runs and seals a scoped Parent `common/`/`connectors/` security scan;
- records concrete evidence and distinguishes reproduced, validated, and
  source-only candidate dispositions;
- creates or enriches canonical bilingual finding records, index, backlog, and
  remediation roadmap entries;
- preserves the no-CI, Parent-only, no-Framework/MRTS/Gitlink scope;
- does not silently write a competing source repair over unmerged Draft PR
  ownership; and
- updates the user-authorized Draft PR only with truthful results.

## Implementation decision and rationale

- The scan is sealed in task run
  `20260826T175448Z-p1-p4-connector-parity-20260826-ea15c4bb`; canonical
  `findings.json` SHA-256 is
  `18d6248c2d85ce0e1457a62a6682fe8e3abd567af47ed430945ec01788e8c35d`.
- A retained isolated public-API reproduction established
  `FND-PARENT-0958`: a nonempty Traefik Native UDS request can return HTTP 204
  after an unread downstream body without P2 callbacks or request EOS.
- `FND-PARENT-0959`–`FND-PARENT-0966` remain triaged source-confirmed
  candidates, not runtime-exploit claims. Existing `FND-PARENT-0007` and
  `FND-PARENT-0135` were enriched rather than duplicated.
- Source repair is intentionally not written because the affected product
  paths overlap unmerged Draft PRs #344, #345, and #346. The next source step
  requires a current user integration or supersession decision.

## Security impact

This documentation-only change records one P0/high locally reproduced bypass
and related candidate boundaries. It changes no product security control. The
P0 finding blocks verified delivery and master integration until a repair is
fully verified, it is proven inapplicable, or the current user explicitly
risk-accepts the exact remaining risk. No candidate is represented as a fixed
or completed host-runtime result.

## Changed files

- `reports/audits/p1-p4-connector-security-scan.md`
- `reports/audits/p1-p4-connector-security-scan.de.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-security-scan.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-security-scan.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| `go test -count=1 -race ./...` in `connectors/traefik/native_middleware` | Passed with task-owned cache and tmp paths. |
| `go vet ./...` in `connectors/traefik/native_middleware` | Passed. |
| `go test -count=1 -race ./...` in `connectors/envoy/ext_proc` | Passed for command, composite, and processor packages with task-owned cache/module-cache/tmp paths. |
| `go vet ./...` in `connectors/envoy/ext_proc` | Passed. |
| Isolated unread-body public-API Go control | Passed while observing HTTP 204, zero P2 callbacks, and `RequestEOS=false`; retained separately as payload-safe local evidence. |
| Standard scoped Codex Security scan | Completed and sealed; 11 records, including one locally reproduced P0/high finding. |
| Finding JSON/backlog/roadmap consistency checks | Passed locally for the eleven synchronized records. |

## Runtime evidence

The isolated unread-body control is a focused Go-level reproduction, not a
real Traefik host result. No selected Apache, NGINX, HAProxy, Envoy, Traefik,
or lighttpd host was started. Accordingly, no connector is promoted and no
P1–P4 real-host acceptance cell is claimed.

## Checks not run and rationale

- Real-host P1–P4 matrix, selected connector builds, host configuration, and
  protocol controls are not run. The required host binaries are unavailable
  and product repair awaits the ownership decision for Draft PRs #344, #345,
  and #346.
- `make check-bilingual-docs` and `make check-doc-links` remain blocked by
  pre-existing absent Framework-Gitlink targets in this Parent-only worktree.
  Initializing Framework or changing Gitlinks is outside scope.

## Known limitations

The scan has partial coverage because real host binaries and the selected
Framework material are unavailable. Source evidence is not elevated to an
exploit or runtime claim. The canonical local finding system and retained scan
evidence remain outside the versioned product diff.

## Remaining risks

`FND-PARENT-0958` remains a P0/high delivery blocker. `FND-PARENT-0959`–
`FND-PARENT-0966` require their recorded runtime controls. The user must
select a clean integration or supersession path before a repair can be written
without competing with Draft PRs #344, #345, and #346. No merge, direct
`master` push, CI change, Framework/MRTS change, Gitlink update, or hosted
success claim is authorized or asserted.

## Final diff and review status

The paired report and Change Record record only observed scan/test outcomes
and the delivery gate. After narrow documentation validation, they are ready
for the next Draft-PR update. The wider P1–P4 parity program remains active
and cannot be reported complete.
