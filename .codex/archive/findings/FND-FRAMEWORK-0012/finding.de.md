# FND-FRAMEWORK-0012 — Framework-CI fehlte durchsetzbare Coverage für Security-Scanner und Workflow-Evidence

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0012` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P2` / `not_applicable` |
| Confidence / Status | `validated` / `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung

Die ursprünglichen Framework-CI-Security-Checks stellten immutable Pins und
grundlegende Workflow-Struktur her, bewiesen aber nicht semantisch, dass
erforderliche Scanner- und Evidence-Befehle auf dem vorgesehenen PR-Pfad
ausführbar waren.

## Evidence

- Run-ID: `20260718T084030Z-expand-framework-ci-security-be8fb24d`
- Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T084030Z-expand-framework-ci-security-be8fb24d/evidence/final-framework-ci-security-local-validation.md`
- Typ: `final_local_ci_security_validation`; SHA-256:
  `979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`
- Validierung: Der exakte lokale Framework-HEAD
  `15e9a034e929fc56bd77c92d783ca2637042e24e` bestand `make lint`, 64
  CI-Security-Tests, Semantic-Contract sowie gelockte Ruff-, actionlint- und
  zizmor-Kontrollen.

## Remediation und Validierung

`ci/checks/security/check-ci-security-evidence-contract.py` validiert jetzt
semantische Workflow-Kontrollen, exakte Checkout-Mappings, Artefakt-/Cache-/
SARIF-Grenzen und erreichbare erforderliche Scanner-Befehle. Regressionstests
decken Kommentare, tote Kontrollfluss-Bodies, direkte Exits, nicht aufgerufene
POSIX-/Bash-Helper und legitime verschachtelte OSV-Helper ab. Die Source-
Remediation ist als `768a06b5b734547f8213cc6918c26ef4a8ef9f67` committet.

## Akzeptanzkriterien

- Erforderliche Scanner- und Evidence-Befehle können nicht durch Kommentare,
  nicht aufgerufene Helper oder erkannten Kontrollfluss erfüllt werden.
- Legitime aktuelle Framework-Workflows und ihr verschachtelter OSV-Helper-
  Fluss bestehen.
- Exakte Final-PR-Head-CI- und Review-Evidence bestätigt die committete Kontrolle.

## Restrisiko und Historie

Die lokale Reparatur ist verifiziert; Remote-Exact-Head-CI, SonarQube Cloud,
Review- und Thread-Evidence stehen nach dem normalen Push noch aus.
`2026-07-18T15:18:00Z`: erstellt und lokal mit aufbewahrter Validierungs-
Evidence repariert.
