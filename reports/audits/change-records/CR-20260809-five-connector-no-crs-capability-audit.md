# Change Record CR-20260809: Five-connector No-CRS capability audit

**Language:** English | [Deutsch](CR-20260809-five-connector-no-crs-capability-audit.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260809-five-connector-no-crs-capability-audit` |
| Date (UTC) | `2026-08-09` |
| Base revision | `ef88a616498e0a2893cd3da54003dd7cdea57015` |
| Scope | Parent only; the Framework Gitlink remains `a7a8dcdd62da8d0e4d7ea36549f7c54c5d614e68` and MRTS was not changed. The base was merged locally as `d9f73ca0558ca499d92ae2736d1be642b9005ee7`. |
| Delivery status | Draft record. Local source, test, and fail-closed security-remediation commits precede this documentation update; no push, hosted workflow result, review result, or merge is recorded here. |

## Motivation and problem statement

PR #243 needs a least-privilege scheduled/manual No-CRS baseline whose scope
can be audited without implying a broader connector, protocol, CRS, MRTS, or
production claim.

## Acceptance criteria

- The visible caller selects only the closed `no-crs` profile and delegates to
  a reusable workflow with `contents: read` permissions.
- The profile contains exactly Apache, HAProxy, Envoy, Traefik, and lighttpd;
  unknown profiles and rows outside that map fail closed.
- Each aggregate input is bound to its connector, profile, run ID, Parent and
  Framework commits, and cleanup disposition; the aggregate requires exactly
  the five expected inputs.
- PR-owned NGINX privileged-handoff, owner-override, and projection changes
  are removed without altering the current-master protected NGINX broker.
- English/German documentation and this Change Record remain equivalent.

## Implementation decision and rationale

The caller hard-codes `no-crs`; the reusable workflow obtains its matrix from a
Parent-owned closed profile resolver. The runner uses unprivileged private
external roots and records a profile receipt through the existing Framework
result-artifact mechanism. A Parent-owned five-result verifier is used because
the checked Framework summarizer is a generic six-connector control and the
task does not authorize Framework or MRTS source/Gitlink changes.

The scope deliberately preserves generic six-connector Make targets and the
current-master NGINX broker/caller behavior. Neither is evidence that NGINX is
part of this five-connector profile.

### Capability audit

This table is a source/contract audit of the five selected connector rows, not
hosted evidence. `implemented` for No-CRS means the profile is implemented in
source and contracts only; hosted evidence remains pending. The other values
are intentionally not promoted from generic source targets or capability
metadata.

| Connector | No-CRS | With-CRS | No-MRTS | With-MRTS | Full lifecycle |
| --- | --- | --- | --- | --- | --- |
| Apache | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| HAProxy | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| Envoy | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| Traefik | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |
| lighttpd | `implemented` (source/contract only, hosted evidence pending) | `not_implemented` | `unknown_pending_audit` | `unknown_pending_audit` | `partially_implemented` (generic existing source targets, not activated/claimed by this profile) |

## Changed files

The in-progress implementation changes the caller and reusable workflow,
profile resolver/aggregator, lifecycle and collector wiring, focused contract
tests, and the following reader documentation pairs:

- `docs/build/README.md` and `docs/build/README.de.md`
- `docs/testing-and-evidence.md` and `docs/testing-and-evidence.de.md`
- `ci/README.md` and `ci/README.de.md`
- this Change Record pair

The final file inventory must be reconciled with the final diff before
delivery.

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| Focused suite | Passed: 200 current focused tests |
| `make check-ci-security-contract` | Passed |
| `make check-runtime-path-policy` | Passed |
| `make check-bilingual-docs` | Passed |
| `make check-doc-links` | Passed |
| `make check-no-crs-doc-consistency` | Passed |
| actionlint | Passed with the checksum-pinned repository release asset |
| zizmor | Passed with the checksum-pinned repository release asset (one existing suppression) |
| Shell syntax and Python AST | Passed |
| `git diff --check` | Passed |
| Python-version contract | The new caller/callee contract passed its 24 focused tests; the repository-wide target remains blocked by the identical unrelated inventory failures on `origin/master` |

These are local results observed during implementation. Hosted workflow,
pull-request, review, and SonarQube results remain pending; no push is claimed
by this record.

## Security impact

This change affects CI permissions, untrusted workflow inputs, external paths,
artifact provenance, and process cleanup. The profile is closed, uses
read-only contents permission, contains no privileged handoff, and rejects
unknown profile/connector values before profile evidence is accepted.

A focused security-diff review reproduced two candidate paths and the local
remediation was revalidated. First, an artifact rejected by the Framework
could otherwise have produced a five-result aggregate `PASS`; aggregation now
receives `passed` only from the immediately preceding successful canonical
validation and emits its fail diagnostic for every other outcome. Second, an
interrupted HAProxy runtime tree lacked registered cleanup authority; the
runtime child is now preclaimed under its managed build root, rejects
concurrent or unowned reuse, and preserves safe incomplete-tree cleanup.
Focused negative tests and independent reviews found no residual reportable
bypass in either path. Hosted end-to-end evidence remains pending.

## Runtime evidence

No hosted runtime run is recorded. Static workflow/profile contracts and any
local fixtures do not establish a hosted connector runtime result.

## Checks not run and rationale

Hosted GitHub Actions, review-thread, required-check, and SonarQube outcomes
are not available in this draft. They must not be inferred from local edits.

## Known limitations

The profile is intentionally No-CRS and HTTP/1.1-scoped. It does not establish
CRS, MRTS, HTTP/2, HTTP/3, full-matrix coverage, production readiness, or
unobserved response behavior.

## Remaining risks

Future profiles require a new closed map, capability and receipt validation,
aggregate expectations, tests, and complete English/German documentation.
Reusing this profile alone cannot promote those unsupported claims.

## Final diff and review status

The local security remediation and scoped local validation are complete. Final
delivery reconciliation still requires the exact pushed branch/PR head,
hosted workflow and required-check outcomes, review status, and delivery
disposition. The pull request remains Draft and is not authorized for merge.
