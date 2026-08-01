# FND-HOST-0004 — NGINX HTTP/3 proof is blocked by unavailable HTTP/3 client capability

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0004` |
| Title / Titel | `NGINX HTTP/3 proof is blocked by unavailable HTTP/3 client capability` |
| Category / Kategorie | `protocol_gap` |
| Repository / Repository | `host_environment` |
| Ownership / Ownership | `external_tool` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `not_applicable` |
| Current task disposition / Aktueller Task-Status | `user_directed_not_applicable_current_local_test_scope` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

The current curl supports HTTP/2 but not HTTP/3, and no alternate H3 client or
forced protocol-correlated H3 harness case is available. The current user
excludes HTTP/3 from the current local test scope; this is not an NGINX
connector failure or an HTTP/3 validation result.

## Observed behavior / Beobachtetes Verhalten

The current curl supports HTTP/2 but not HTTP/3; this is a client-capability limitation, not an NGINX connector failure.

## Expected behavior / Erwartetes Verhalten

The finding is not applicable to the current local test scope. If HTTP/3
becomes an acceptance, production, publication, or release criterion, restore
this triplet and run an HTTP/3-capable client plus a protocol-correlated H3
allow/control.

## Impact / Auswirkung

The unavailable HTTP/3 route does not block the user-selected current scope. It
remains unverified and cannot support an HTTP/3 or connector-behavior claim.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `curl 8.18.0`
- `--http3-only`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '561,570p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:561-570`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '561,570p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

No HTTP/3 action is required for the user-selected current scope. Restore this
record and provide an authorized HTTP/3-capable client plus isolated
protocol-correlated route only if H3 becomes required.

## Acceptance criteria / Akzeptanzkriterien

- The archived record retains the unavailable HTTP/3 client/harness condition
  and the current user scope decision without claiming an H3 pass.
- No HTTP/3 client capability, H3 runtime, or connector behavior is represented
  as observed.
- If H3 becomes required, the complete triplet is restored and an HTTP/3-capable,
  protocol-correlated allow/control is run.

## Validation plan / Validierungsplan

- Verify the lossless archive triplet, manifest hash, and removal from active
  finding summaries.
- If the scope is reactivated, run an HTTP/3-capable client probe and
  protocol-correlated NGINX H3 allow/control.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None for the user-selected current local scope. Restore this record before
  seeking an isolated HTTP/3-capable client and NGINX H3 runtime.

## Blockers / Blocker

- None within the current local scope. The unavailable client/harness condition
  remains retained for reactivation and is not represented as passed.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0009`

## Residual risk / Restrisiko

No risk is accepted. HTTP/3 client capability, a protocol-correlated H3 harness
control, and connector behavior remain unobserved; restore and revalidate
before any H3, production, publication, or release reliance.

## Current task disposition / Aktueller Task-Stand

`not_applicable` for the user-directed current local test scope

The current curl 8.18.0 feature list contains HTTP2 but no HTTP3, and neither
`nghttp` nor `h3` resolves on `PATH`. The Parent harness intentionally records
only startup/TCP readiness for the H3 route and then reports `not_executable`
until a forced protocol-correlated case is wired. HTTP/2 availability is not
HTTP/3 proof.

Current evidence: run `20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`,
artifact `evidence/fnd-host-0002-0003-0004-0006-current-revalidation.md`,
SHA-256 `81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`.
No client installation, NGINX runtime, product change, or delivery action
occurred. The current user excludes HTTP/3 from the current local test scope;
this is not a pass or a technical closure. Restore this complete triplet and
run an HTTP/3-capable, protocol-correlated H3 allow/control before any H3,
production, publication, or release claim.

## Current user-directed archive and scope disposition — 2026-07-26

The current user selected a local test scope in which HTTP/3 is future work
rather than a current acceptance dimension. Accordingly, this record is
`not_applicable` for that scope and is archived losslessly; it is not
technically closed or proven over HTTP/3.

Current decision evidence: run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.
No H3 client installation, H3 runtime, connector validation, product change, or
delivery action occurred. Restore and revalidate before any future H3 or
release reliance.

Archive location: `.codex/archive/findings/FND-HOST-0004/`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: current_task_scope_recorded — `out_of_scope_for_current_task`
- `2026-07-26T17:34:26Z`: current_http3_capability_revalidation — curl 8.18.0
  remains HTTP2-capable but has no HTTP3 feature; no alternate local client
  resolves, and the Parent harness preserves `not_executable` rather than
  promoting a liveness result. The finding is `blocked_external_dependency`.
