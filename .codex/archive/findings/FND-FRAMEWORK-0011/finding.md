# FND-FRAMEWORK-0011 — Protocol URL command evidence can retain an opaque path segment

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0011` |
| Title / Titel | `Protocol URL command evidence can retain an opaque path segment` |
| Category / Kategorie | `security_candidate` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `candidate` |
| Status | `closed` |
| Feasibility / Machbarkeit | `requires_user_decision` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The public `protocol-client` target can retain a `PROTOCOL_URL` path segment in `client-command.txt` after only userinfo/query redaction, and a full-lifecycle path can copy the artifact into canonical evidence.

## Observed behavior / Beobachtetes Verhalten

`_safe_url_for_command()` retains `parsed.path`; `_redacted_command()` renders it; `_write_artifacts()` writes it; and `copy_protocol_client_artifacts()` can copy the command artifact without another path-redaction pass. Existing tests prove query redaction only.

## Expected behavior / Erwartetes Verhalten

Evidence command artifacts must not retain opaque URL path secrets or sensitive direct CLI resolution mappings. A useful non-sensitive endpoint representation may remain only when its safety is explicit.

## Impact / Auswirkung

A caller who embeds a token or personal value in a documented protocol URL path could cause retention and copying into evidence. Actual production path sensitivity and evidence-reader access were not established.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `ci/checks/protocol/protocol_client.py`
- `ci/checks/catalog/no_crs_baseline.py`
- `ci/checks/protocol/check_protocol_evidence.py`
- `tests/protocol_client/test_protocol_client.py`
- `docs/reference/variables.md`
- `docs/testing-and-evidence.md`

### Symbols / Symbole

- `_safe_url_for_command`
- `_redacted_command`
- `_write_artifacts`
- `copy_protocol_client_artifacts`
- `PROTOCOL_URL`

## Preconditions / Voraussetzungen

- A caller supplies a sensitive opaque path through documented `PROTOCOL_URL` or the direct CLI URL option.
- The protocol client writes its managed artifact bundle.
- The full-lifecycle artifact-copy path is selected for canonical retention.

## Reproduction / Reproduktion

- Inspect `protocol_client.py:589-631,1186-1201` and `no_crs_baseline.py:3956-3998`.
- Inspect query-only unit coverage in `tests/protocol_client/test_protocol_client.py`.
- Do not generate a live artifact containing a secret until a safe synthetic validation plan is approved.

## Evidence / Evidence

- Run ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/protocol-url-redaction-candidate.md`
  - Type: `static_source_to_sink_security_review`; SHA-256: `94fdd47764c82a3453e7b599212cd66f636f8d8468bcb57adef074894c7ad7bd`
  - Command: `rtk sed -n '589,631p;1186,1201p;1472,1475p' ci/checks/protocol/protocol_client.py; rtk sed -n '3956,3998p' ci/checks/catalog/no_crs_baseline.py`
  - Working directory: `/var/tmp/codex/worktrees/framework-common-structure`; exit code: `0`
  - Observed at: `2026-07-18T09:27:57Z`; retention: `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

Command-artifact redaction protects query strings and userinfo but preserves all path segments. The copier and validator provide no independent path or `--resolve` redaction control.

## Proposed remediation / Vorgeschlagene Remediation

After focused validation, reduce artifact URLs to a safe authority plus an explicit redacted path marker, redact direct `--resolve` values, add synthetic path/percent-encoded/IPv6 coverage, and preserve harmless diagnostics only where justified.

## Acceptance criteria / Akzeptanzkriterien

- Synthetic secret-like paths do not appear in `client-command.txt` or copied canonical evidence.
- Direct `--resolve` values are redacted or demonstrably excluded.
- Query, userinfo, harmless health path, IPv6, and legitimate protocol-client controls pass.
- No current user-approved remediation scope is exceeded.

## Validation plan / Validierungsplan

- Use Codex Security validation before a fix to establish boundary, synthetic artifact persistence, and reader-exposure assumptions.
- If confirmed and separately authorized, use `fix-finding` with focused protocol-client and artifact-copy regressions.
- Run the protocol-contract workflow on the exact future PR head.

## Regression tests / Regressionstests

- `tests/protocol_client/test_protocol_client.py` with synthetic opaque, percent-encoded, IPv6, and `--resolve` cases.
- A full-lifecycle copied-artifact redaction control.

## Legitimate control tests / Legitime Kontrolltests

- A harmless `/health` URL remains diagnostically useful without a sensitive path value.
- Existing query and userinfo redaction remains intact.

## Dependencies / Abhängigkeiten

- Current-user authorization for a separate remediation if validation confirms a reportable supported boundary.

## Blockers / Blocker

- The current task scope is the independent common-structure CI repair.
- Path sensitivity, evidence-reader access, and dynamic artifact persistence are not yet validated.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0001`
- `FND-SONAR-0002`

## Residual risk / Restrisiko

The resulting-master regression suite verifies redaction of opaque paths and `--resolve` values while retaining harmless health, query, userinfo, IPv6, and protocol-client controls. No risk acceptance was used.

## History / Historie

- `2026-07-18T09:27:57Z`: `current_task_static_candidate_triaged` — Static source-to-sink evidence found a public protocol URL path-retention candidate. No live secret artifact, exploit, or remediation was performed; it is separate from common-structure and Sonar remediation.
- `2026-07-26T16:13:56Z`: `remediation_fixed` and `resulting_master_verified_and_closed` — Framework PR #50 added bounded command-artifact and `--resolve` redaction plus an independent evidence validator. Exact Framework master `de705a5efb872f95f010346fe2e6143c88876ad4` passed 28 focused protocol/evidence tests; PR #50 SonarQube Cloud is `OK` with zero unresolved issues. Receipt: `.codex/runs/20260726T160903Z-framework-pr50-pr51-master-verification/finding-closure-evidence.md` (SHA-256 `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`).
