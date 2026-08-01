# FND-FRAMEWORK-0048 — Workflow-Tool-Publisher expandiert Default-Branch-Metadaten direkt im Shell-Source

- Kategorie: `security_hardening`
- Repository / Ownership: `framework` / `framework`
- Priorität / Schweregrad / Konfidenz: `P1` / `medium` / `reproduced`
- Status / Feasibility: `fixed` / `feasible_now`
- Release-Blocker / Sicherheitsrelevanz: `true` / `true`

## Zusammenfassung

Der eingeschränkte Framework-Workflow-Tool-Publisher expandierte
`github.event.repository.default_branch` direkt in zwei `run`-Blöcken.
Prüfsummenverifiziertes Zizmor meldete vier High-Confidence-
Template-Injection-Findings, weil GitHub-Expressions vor dem Shell-Parsing
gerendert werden. Die lokale Korrektur verwendet exakte step-lokale
`DEFAULT_BRANCH`-Environment-Mappings, gequotete Variablenreferenzen und
`git check-ref-format --branch` vor der Ref-Konstruktion; Publisher-Profil-
Hashes und Regressionstests binden diese Form.

## Beobachtetes und erwartetes Verhalten

Vor der Korrektur gab `zizmor --offline .github` den Exit-Code 1 mit vier
Findings in `.github/workflows/update-workflow-tools.yml` in den Zeilen 192,
202, 205 und 225 zurück. Die Metadaten standen direkt im Shell-Source für
Branch-Fetch, Existing-Branch-Validierung und Reusable-Branch-Validierung.

Der Publisher muss Repository-Metadaten als Daten und nicht als Script-Text
behandeln. Er muss den Wert durch ein überprüftes Environment-Mapping führen,
jede Shell-Verwendung quoten, ihn als Branch-Ref validieren und die bestehenden
read-only Resolver-/Validator-Abhängigkeiten erhalten, bevor der
schreibfähige Publisher laufen kann.

## Auswirkung, Grenzen und Voraussetzungen

Der betroffene Job besitzt `contents: write` und `pull-requests: write`. Ein
shell-signifikanter Wert über diese Grenze könnte einen Publisher-Shell-Befehl
verändern. Die aktuelle Evidence behauptet nicht, dass ein nicht
vertrauenswürdiger PR-Autor Default-Branch-Metadaten des Repositories ändern
kann; die Beobachtung bleibt dennoch ein erforderlicher CI-Security-Fehler und
eine release-blockierende Härtungslücke.

Sie erfordert eine geplante oder manuelle Updater-Ausführung nach erfolgreichem
Resolver und Validator sowie einen shell-signifikanten Metadatenwert oder eine
künftige Aufweitung der Metadaten-Vertrauensgrenze.

## Evidence und Reproduktion

- Run: `20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`
- Evidence: `evidence/zizmor-template-injection-remediation.md`
- SHA-256: `2c8ab7e8fc947188f9bd9ca312457a21042051580a2c18bafdfc368b7feac468`
- Vor Korrektur: prüfsummenverifiziertes `zizmor --offline .github`, Exit `1`
- Nach Korrektur: derselbe Befehl, Exit `0`, keine aktiven Findings
- Verifizierte PR-Remediation-Head: `1fd3b362e0fed9766c6920e3c7bd1939535850f2`

Bei der Reproduktion liefen kein Publisher, keine GitHub-Token-Operation,
keine Remote-Action und kein PR-Workflow.

## Root Cause und Remediation

Der Workflow nutzte GitHub-Expression-Syntax innerhalb des Shell-Sources. Die
Remediation ergänzt exakte `DEFAULT_BRANCH`-Environment-Mappings für die zwei
Publisher-Steps, validiert den Wert mit `git check-ref-format --branch`,
referenziert ihn nur als gequotete Shell-Variable und aktualisiert Contract-
Step-Profile und Body-Digests. Sie lockert weder Berechtigungen, Action-Pins,
Validator-Abhängigkeit, Branch-Bedingung noch Draft-only-Auslieferungscontrols.

## Akzeptanz und Validierung

Die direkte Expression darf in keinem Publisher-`run`-Body vorkommen; beide
Environment-Mappings müssen dem überprüften Profil entsprechen; Branch-
Validierung und gequotete Verwendungen müssen im gehashten Programmkörper
bleiben; statische Workflow-Contracts und Zizmor müssen bestehen. Der exakte
gehostete Konsolidierungs-PR muss die anwendbaren Workflow-Security-Checks
bestehen, bevor das Finding verifiziert oder geschlossen werden kann.

## Abhängigkeiten, Blocker und Restrisiko

Es bleibt keine Implementierungsabhängigkeit. Der exakte PR-#42-Head bestand
inzwischen Hosted-Workflow-Lint/Zizmor, das Sonar-PR-Quality-Gate und alle
anderen anwendbaren Controls. Dies stärkt den Status `fixed`, doch das Finding
ist erst nach normalem Master-Merge und resulting-master-Evidence `verified`
oder geschlossen. `FND-FRAMEWORK-0047` ist eine getrennte Action-Lock-
Provenance-Remediation; `FND-SONAR-0002` bleibt ein unabhängiger Master-
Integrationsblocker.

## Historie

- 2026-07-22T16:30:00Z: durch prüfsummenverifiziertes Zizmor reproduziert,
  im Framework-Konsolidierungsworktree korrigiert und lokal erneut ohne aktive
  Zizmor-Findings geprüft.
- 2026-07-22T17:24:06Z: die lokale Korrektur wurde in
  `22747d460a9f7be02760edf05c311be376492457` committed; Clean-Worktree-,
  Exact-Range-Whitespace- und native `make lint`-Checks bestanden. Hosted
  Exact-Head-Evidence bleibt erforderlich.
- 2026-07-22T17:42:25Z: PR #42 bei
  `1fd3b362e0fed9766c6920e3c7bd1939535850f2` bestand Hosted-Workflow-
  Lint/Zizmor, das Sonar-PR-Quality-Gate und alle anderen anwendbaren Controls.
