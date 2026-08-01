# FND-PARENT-0004 — HAProxy HTX cap error can conditionally resume the original backend path

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0004 |
| Title / Titel | HAProxy HTX cap error can conditionally resume the original backend path |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P3 |
| Severity / Severity | not_applicable |
| Confidence / Confidence | validated |
| Status | not_applicable (archived) |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

The over-cap URI capture failure still disables the connector context and
continues the host callback, but the exact HAProxy HTX route is affirmatively
non-promoted observer/reference code with loopback-only checked-in examples. It
is not currently a reportable Parent product vulnerability.

## Observed behavior / Beobachtetes Verhalten

At target 5a22cbf5206dbc2b7f53a9f961d72e37d567e188, URI capture above 8192
bytes returns failure, abort_context marks the transaction disabled, and the
header callback returns normal continuation instead of the pre-commit
reply-and-close path.

## Expected behavior / Erwartetes Verhalten

If the HTX overlay is promoted to a supported enforcement route, capture or
transaction-begin failures must fail closed before any backend forwarding and
must retain a host-specific regression/control suite.

## Impact / Auswirkung

The static control-flow defect is real, but current repository evidence
establishes neither a meaningful supported production surface, host acceptance
of an over-cap URI, nor a protected backend operation. No present Parent
product-security impact is claimed.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c
- connectors/haproxy/SOURCE_MAP.json
- docs/connectors/haproxy.md

### Symbols / Symbole

- haproxy_modsecurity_htx_dup_ist
- haproxy_modsecurity_htx_capture_request
- haproxy_modsecurity_htx_request_headers
- abort_context

## Preconditions / Voraussetzungen

- The custom pinned HAProxy 3.2.21 overlay is promoted or deployed as a supported enforcement route.
- A meaningful Phase-1 URI rule is configured.
- The host accepts and forwards a URI above the connector's 8192-byte snapshot cap.
- An untrusted client can reach the selected listener.

## Reproduction / Reproduktion

- Review connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c:49-99,279-291,346-376,635-688.
- Read the retained attack-path report for CAND-HAPROXY-HTX-001.
- If the route is promoted, run the documented native HAProxy over-cap URI, ordinary deny, boundary, and allow controls.

## Evidence / Evidence

- Run ID: 20260716T193351Z-repository-full-assessment-0cb855ad
  - Artifact: .codex/reports/repository-full-assessment.md:224-227,238-244
  - Type: bilingual_assessment_report; SHA-256: 5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4
  - Command: sed -n '224,227p;238,244p' .codex/reports/repository-full-assessment.md
  - Working directory: /root/git/ModSecurity-conector; exit code: 0
  - Observed at: 2026-07-16T22:46:50Z; retention: retained_local_report
- Run ID: 20260720T164715Z-parent-security-reconciliation-5a22cbf5
  - Artifact: retained CAND-HAPROXY-HTX-001/attack_path_analysis_report.md
  - Type: attack_path_analysis_report; SHA-256: 61da851e8b66dcceab11c4b19c233cf89bf4194f088188a756ea8b2e986f0b01
  - Command: rtk run -c 'sha256sum artifacts/05_findings/CAND-HAPROXY-HTX-001/attack_path_analysis_report.md'
  - Working directory: /root/git/ModSecurity-conector; exit code: 0
  - Observed at: 2026-07-20T19:24:00Z; retention: retained_task_artifact

## Root-cause analysis / Grundursachenanalyse

The 8192-byte snapshot cap correctly bounds allocation, but its failure path
calls abort_context and continues the callback rather than selecting the
existing pre-commit host denial path. The current route is not a promoted
supported product surface.

## Proposed remediation / Vorgeschlagene Remediation

Conditional future hardening only: if the route is promoted, preserve the cap
and convert capture/begin failure to an explicit fail-closed reply-and-close
path before forwarding.

## Acceptance criteria / Akzeptanzkriterien

- If promoted, over-cap HTX input cannot reach the original/backend path.
- If promoted, a normal in-cap request remains available and correctly enforced.
- Host acceptance is recorded separately from connector enforcement.

## Validation plan / Validierungsplan

- Use a task-owned pinned HAProxy 3.2.21 build and local backend receipt marker.
- Run over-cap URI, normal-size matching deny, boundary-size, and non-matching allow controls.
- Re-triage the finding before release if the route is declared supported or exposed beyond loopback.

## Regression tests / Regressionstests

- No current product regression is required while the route remains non-promoted.
- Add a native over-cap URI fail-closed regression before any promotion.

## Legitimate control tests / Legitime Kontrolltests

- Use normal deny, boundary-size, and non-matching allow controls in the same native host profile.

## Dependencies / Abhängigkeiten

- Supported-route promotion or concrete deployment evidence.
- Pinned HAProxy 3.2.21 and libmodsecurity runtime.

## Blockers / Blocker

- The exact route is non-promoted observer/reference code.
- No native host acceptance or backend-forwarding evidence exists.

## Related findings / Verwandte Findings

- FND-PARENT-0010

## Residual risk / Restrisiko

The static fail-open path must be reopened if the HTX overlay is promoted,
exposed beyond loopback, or shown to forward an over-cap URI while inspection
is disabled. No risk is accepted.

## History / Historie

- 2026-07-17T10:43:59Z: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- 2026-07-20T19:30:00Z: attack_path_retriaged_not_applicable — Current-target attack-path analysis retained the static connector control-flow evidence but established that the exact HTX route is non-promoted observer/reference code with loopback checked-in references. The lifecycle status is not_applicable_with_evidence, not a false-positive or fixed claim.
