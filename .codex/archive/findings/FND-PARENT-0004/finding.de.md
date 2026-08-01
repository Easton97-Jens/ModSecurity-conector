# FND-PARENT-0004 — HAProxy-HTX-Cap-Fehler kann bedingt den ursprünglichen Backend-Pfad fortsetzen

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0004 |
| Title / Titel | HAProxy-HTX-Cap-Fehler kann bedingt den ursprünglichen Backend-Pfad fortsetzen |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P3 |
| Severity / Severity | not_applicable |
| Confidence / Confidence | validated |
| Status | not_applicable (archiviert) |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

Der Over-Cap-URI-Capture-Fehler deaktiviert weiterhin den Connector-Kontext und
setzt den Host-Callback fort. Der exakte HAProxy-HTX-Pfad ist jedoch
ausdrücklich nicht-promoteter Observer-/Referenzcode mit ausschließlich
loopbackgebundenen eingecheckten Beispielen. Er ist derzeit keine
berichtsfähige Parent-Produktvulnerabilität.

## Observed behavior / Beobachtetes Verhalten

Auf Target 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 führt URI-Capture oberhalb
von 8192 Byte zu einem Fehler, abort_context markiert die Transaktion als
deaktiviert und der Header-Callback kehrt zur normalen Fortsetzung statt zum
Pre-Commit-Reply-and-Close-Pfad zurück.

## Expected behavior / Erwartetes Verhalten

Wenn das HTX-Overlay zu einem unterstützten Enforcement-Pfad promotiert wird,
müssen Capture- oder Transaction-Begin-Fehler vor jedem Backend-Forwarding
fail-closed enden und eine host-spezifische Regression-/Control-Suite behalten.

## Impact / Auswirkung

Der statische Kontrollflussfehler ist real, aber die aktuelle
Repository-Evidence belegt weder eine bedeutsame unterstützte
Produktionsoberfläche noch Host-Akzeptanz einer Over-Cap-URI oder eine
geschützte Backend-Operation. Es wird kein aktueller
Parent-Produktsicherheitsimpact behauptet.

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

Die 8192-Byte-Snapshot-Grenze begrenzt die Allokation korrekt, aber ihr
Fehlerpfad ruft abort_context auf und setzt den Callback fort, statt den
vorhandenen Pre-Commit-Host-Deny-Pfad zu wählen. Der aktuelle Pfad ist keine
promotete unterstützte Produktschnittstelle.

## Proposed remediation / Vorgeschlagene Remediation

Nur bedingtes zukünftiges Hardening: Wenn der Pfad promotiert wird, die Grenze
beibehalten und Capture-/Begin-Fehler vor dem Forwarding in einen expliziten
fail-closed Reply-and-Close-Pfad überführen.

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

Der statische Fail-Open-Pfad muss erneut eröffnet werden, wenn das HTX-Overlay
promotiert, über loopback hinaus exponiert oder als Forwarder einer
Over-Cap-URI bei deaktivierter Inspektion nachgewiesen wird. Es wird kein
Risiko akzeptiert.

## History / Historie

- 2026-07-17T10:43:59Z: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- 2026-07-20T19:30:00Z: attack_path_retriaged_not_applicable — Current-target attack-path analysis retained the static connector control-flow evidence but established that the exact HTX route is non-promoted observer/reference code with loopback checked-in references. The lifecycle status is not_applicable_with_evidence, not a false-positive or fixed claim.
