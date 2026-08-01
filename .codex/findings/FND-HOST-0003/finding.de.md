# FND-HOST-0003 — NGINX-Non-Root-Worker-Isolation kann im aktuellen Sandbox nicht bewiesen werden

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0003` |
| Title / Titel | `NGINX-Non-Root-Worker-Isolation kann im aktuellen Sandbox nicht bewiesen werden` |
| Category / Kategorie | `lifecycle_defect` |
| Repository / Repository | `host_environment` |
| Ownership / Ownership | `host_environment` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `reproduced` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Die Sandbox verweigerte runuser group setup; dem Renderer fehlt eine user directive und es wurden kein Post-Start-Worker-PID, keine effective UID und kein capability set aufbewahrt.

## Observed behavior / Beobachtetes Verhalten

Die Sandbox verweigerte runuser group setup; dem Renderer fehlt eine user directive und es wurden kein Post-Start-Worker-PID, keine effective UID und kein capability set aufbewahrt.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über blocked hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `runuser cannot set groups`
- `worker PID/effective UID/capability set absent`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '528,533p;580,594p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:528-533,580-594`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '528,533p;580,594p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Einen separat autorisierten Harness/eine Konfiguration verwenden, die Non-Root-Worker-Ownership, Readability und Capabilities ohne unsicheren Bypass beweisen kann.

## Acceptance criteria / Akzeptanzkriterien

- A non-root NGINX worker is evidenced with PID, effective UID, and capability facts.
- Root control runtime is not promoted as non-root isolation proof.

## Validation plan / Validierungsplan

- Run the authorized non-root NGINX profile.
- Run the root control separately and retain both distinct results.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- Ausdrückliche aktuelle Nutzerautorisierung für eine isolierte NGINX-Runtime,
  die Worker-Identity- und Capability-Evidence aufbewahren kann.

## Blockers / Blocker

- Auf dem aktuellen Host ist kein `nginx`-Executable verfügbar, und der
  aktuelle Task autorisiert keinen Service-Start, keine Account-Änderung und
  keine Runtime-Provisionierung.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0009`
- `FND-CROSS-0004`

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## Current task update / Aktueller Task-Stand

Der aktuelle Source-Preflight fand einen reinen `runuser`-Access-Probe, aber
keine gerenderte NGINX-`user`-Directive und keine aktuelle Worker-PID-/Effective-
UID-/GID-/Capability-Evidence. Kein Benutzer, Namespace, Dateirecht,
NGINX-Source oder Host-Konfiguration wurde geändert.

- Feasibility: `blocked_missing_evidence`
- Next action: eine autorisierte Non-Root-Runtime mit gerenderter Config sowie
  getrennten Control-Runtime- und Worker-Identity-Fakten aufbewahren.
- Evidence: Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, Exit `0`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — aktuelle Evidence bleibt unzureichend; keine spekulative Privilegienänderung erfolgte.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Das aufbewahrte aktive Source-Preflight-Log wurde in die kanonische Evidence aufgenommen; `blocked_missing_evidence` bleibt unverändert.

## Aktuelle Non-Root-Worker-Revalidierung — 2026-07-26

Der Parent-Harness nutzt `NGINX_WORKER_USER` weiter nur als Access-Preflight-
Hinweis; sein generiertes NGINX-Template enthält keine Directive
`user <name> [group];`. Der aktuelle Host hat kein `nginx`-Executable, daher
können keine Post-Start-Worker-PID-, Effective-UID-/GID- oder Capability-Fakten
aufbewahrt werden. Die aktuelle Evidence ist Run
`20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`, Artifact
`evidence/fnd-host-0002-0003-0004-0006-current-revalidation.md`, SHA-256
`81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`.

Es erfolgten keine Privilegien-, Service-, Produkt-, Framework- oder MRTS-
Aktion. Das P1-Finding bleibt `blocked_missing_evidence`; eine ausdrücklich
autorisierte isolierte Non-Root-Runtime muss gerenderte Konfiguration,
Worker-Identity-/Capability-Fakten und eine getrennte Root-Control-Beobachtung
aufbewahren.
