# FND-PARENT-0005 — Slow authorization readers can retain service capacity

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0005 |
| Title / Titel | Slow authorization readers can retain service capacity |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P3 |
| Severity / Severity | low |
| Confidence / Confidence | validated |
| Status | fixed |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

When the supported authorization-service 0.0.0.0 bind is directly reachable by
untrusted clients, one incomplete HTTP request can retain the only synchronous
receive loop and delay authorization-dependent traffic. Shipped Envoy and
Traefik profiles keep this service loopback-only.

## Observed behavior / Beobachtetes Verhalten

The listen parser accepts 0.0.0.0, accepted connections are processed
synchronously, and header/body receive loops block without an absolute
elapsed-time deadline, accepted-socket timeout, nonblocking state machine, or
bounded admission control.

## Expected behavior / Erwartetes Verhalten

A directly exposed authorization-service listener must bound complete-request
receipt time and preserve capacity for ordinary authorization clients without
weakening existing fail-closed host semantics.

## Impact / Auswirkung

Conditional Low/P3 availability risk for one configured service process and
its authorization-dependent traffic. No authorization bypass, confidentiality
loss, integrity impact, secret exposure, code execution, or cross-tenant effect
is established.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- common/runtime/http_authorization_service.c
- connectors/envoy/src/envoy_ext_authz_service_main.c
- connectors/traefik/src/traefik_forwardauth_service_main.c
- connectors/envoy/config/envoy-ext-authz-smoke.yaml.in
- connectors/traefik/scripts/start-smoke.sh

### Symbols / Symbole

- parse_listen_spec
- recv_more
- read_request_body
- read_http_request
- serve_authorization

## Preconditions / Voraussetzungen

- An operator selects the supported 0.0.0.0 authorization-service bind.
- The service port is directly reachable by untrusted clients.
- No effective outside-repository proxy, network admission, or timeout control terminates the slow connection first.

## Reproduction / Reproduktion

- Review common/runtime/http_authorization_service.c:134-165,190-203,370-480,604-786.
- Read the retained attack-path report for CAND-5A22CBF5-COV003-AUTH-SLOWLORIS-001.
- In an authorized local-only harness, hold one incomplete bounded request and issue a normal complete authorization request concurrently.

## Evidence / Evidence

- Run ID: 20260716T193351Z-repository-full-assessment-0cb855ad
  - Artifact: .codex/reports/repository-full-assessment.md:225-227,241-244
  - Type: bilingual_assessment_report; SHA-256: 5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4
  - Command: sed -n '225,227p;241,244p' .codex/reports/repository-full-assessment.md
  - Working directory: /root/git/ModSecurity-conector; exit code: 0
  - Observed at: 2026-07-16T22:46:50Z; retention: retained_local_report
- Run ID: 20260720T164715Z-parent-security-reconciliation-5a22cbf5
  - Artifact: retained CAND-5A22CBF5-COV003-AUTH-SLOWLORIS-001/attack_path_analysis_report.md
  - Type: attack_path_analysis_report; SHA-256: e899028b6b59363903a6c50056db15f0616e2b4303ec60d1778dccbdd57bf9b6
  - Command: rtk run -c 'sha256sum artifacts/05_findings/CAND-5A22CBF5-COV003-AUTH-SLOWLORIS-001/attack_path_analysis_report.md'
  - Working directory: /root/git/ModSecurity-conector; exit code: 0
  - Observed at: 2026-07-20T19:16:00Z; retention: retained_task_artifact

## Root-cause analysis / Grundursachenanalyse

The public bind parser allows 0.0.0.0 while the sole accept loop synchronously
performs unbounded blocking reads on each accepted socket. Byte limits and the
caller-side Envoy timeout do not impose an absolute deadline on a directly
connected slow client.

## Proposed remediation / Vorgeschlagene Remediation

Add an absolute monotonic complete-request deadline and a bounded
admission/concurrency design that retains ordinary-client capacity. Keep
loopback/private binding as the default and preserve fail-closed Envoy
behavior.

## Acceptance criteria / Akzeptanzkriterien

- Slow-reader pressure cannot retain unbounded authorization capacity.
- Normal authorization traffic remains available under the configured budgets.
- A directly held incomplete request is closed or receives the documented timeout result within the absolute deadline.
- Existing Envoy failure_mode_allow false semantics remain unchanged.

## Validation plan / Validierungsplan

- Use an authorized isolated loopback-only harness with a non-sensitive rule configuration.
- Hold one bounded incomplete header or body request and send a complete authorization request concurrently.
- Verify timeout/closure for the stalled client, timely expected decision for the ordinary client, queue/admission bounds, and loopback defaults in both wrappers.

## Regression tests / Regressionstests

- Add a deterministic slow partial request timeout/control test.
- Add a concurrent ordinary authorization allow/block control under the same configured budget.
- Retain wrapper configuration assertions that shipped authorization endpoints remain loopback.

## Legitimate control tests / Legitime Kontrolltests

- Run a complete ordinary authorization request through both selected wrapper profiles.
- Verify the existing Envoy fail-closed timeout and Traefik loopback defaults remain intact.

## Dependencies / Abhängigkeiten

- Task-owned local socket/control harness.
- Documented request-deadline and admission policy.

## Blockers / Blocker

- Direct public deployment reachability is unobserved.
- No authorized slow-client versus ordinary-client runtime control has yet run.

## Related findings / Verwandte Findings

- None / Keine

## Residual risk / Restrisiko

The service remains Low/P3 conditional risk if an operator directly exposes its
supported public bind. Shipped profiles are loopback-only but that does not
remove the explicitly supported public-bind path. No risk is accepted.

## History / Historie

- 2026-07-17T10:43:59Z: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- 2026-07-20T19:30:00Z: attack_path_enriched — Current-target analysis identified the specific 0.0.0.0 direct-bind, synchronous receive, and serial accept path. It remains validated Low/P3, not a claim that shipped Envoy or Traefik default profiles expose the service publicly.
