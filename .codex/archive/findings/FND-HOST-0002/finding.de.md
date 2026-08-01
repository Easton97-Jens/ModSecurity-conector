# FND-HOST-0002 — Host-Prerequisites und optionale Analyse-Tools blockieren ausgewählte Evidence

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0002` |
| Title / Titel | `Host-Prerequisites und optionale Analyse-Tools blockieren ausgewählte Evidence` |
| Category / Kategorie | `tooling` |
| Repository / Repository | `host_environment` |
| Ownership / Ownership | `host_environment` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `not_applicable` |
| Current scope disposition / Aktueller Scope-Status | `user_directed_current_local_test_scope` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Host und lokale Virtual Environment bleiben bei Python 3.14.4, während der
Parent-Contract 3.14.6 deklariert, und Native-/optionale Tools bleiben nicht
verfügbar. Der aktuelle Nutzer schließt exakte lokale
Python-/Native-/Optional-Tool-Parität aus dem aktuellen lokalen Testumfang aus;
dies ist weder ein Produktdefekt noch Evidence für ein exaktes gehostetes
CI-Ergebnis.

## Observed behavior / Beobachtetes Verhalten

Die kanonische `.python-version` enthält 3.14.6 und der Workflow übergibt sie
an `actions/setup-python`, aber der aktuelle Host und die lokale Virtual
Environment melden Python 3.14.4 und kein `python3.14.6`-Executable löst über
`PATH` auf. Native Host-Prerequisites und ausgewählte optionale Tools bleiben
nicht verfügbar.

## Expected behavior / Erwartetes Verhalten

Das Finding ist für den aktuellen lokalen Testumfang nicht anwendbar. Wenn
exakte lokale Python-/Native-/Optional-Tool-Parität zu einem Akzeptanz- oder
Release-Kriterium wird, ist dieses Tripel wiederherzustellen und seine
ursprünglichen Controls in einer genehmigten isolierten Umgebung erneut
auszuführen.

## Impact / Auswirkung

Die nicht verfügbaren lokalen Prerequisites blockieren den nutzergewählten
aktuellen Scope nicht. Sie bleiben unverifiziert und können keinen lokalen
Exact-Python- oder Hosted-CI-Claim stützen.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `C++ evaluator`
- `apxs`
- `NGINX headers/source`
- `HAProxy headers/source`
- `Ruff`
- `Pyright`
- `actionlint`
- `zizmor`
- `gitleaks`
- `exakte Python-3.14.6-CI-Lane`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '248,264p' .codex/reports/repository-full-assessment.md`
- `sed -n '1p' .python-version; python3 --version; command -v python3.14.6 || true`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:248-264`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '248,264p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/136-python313-ci-lane-availability-final.log`; SHA-256:
    `36b6be11baae984e34c1babd5dcc4daa2bac83dbc2772756bfa36c99773ddaba`
  - Command: `python3 --version; command -v python3.13; if present,
    python3.13 --version; otherwise record unavailable`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T17:20:47Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.
Die Python-CI-Lane-Lücke ist eine Host-Environment-/Versionsverfügbarkeitsgrenze,
kein Produktdefekt.

## Proposed remediation / Vorgeschlagene Remediation

Für den nutzergewählten aktuellen Scope ist keine lokale Provisionierung
erforderlich. Diesen Record wiederherstellen und einen reproduzierbaren
isolierten Host-/Tool-Bundle nur bereitstellen, wenn exakte lokale Parität
erforderlich wird.

## Acceptance criteria / Akzeptanzkriterien

- Der archivierte Record bewahrt den beobachteten Host-/Tool-Zustand und die
  aktuelle Nutzer-Scope-Entscheidung, ohne einen Pass zu behaupten.
- Kein lokales Exact-Python-/Native-/Optional-Tool- oder Hosted-CI-Ergebnis
  wird als beobachtet dargestellt.
- Wenn exakte lokale Parität erforderlich wird, ist das vollständige Tripel
  wiederherzustellen und seine ursprünglichen Approved-Environment-Controls
  erneut auszuführen.

## Validation plan / Validierungsplan

- Verlustfreies Archivtripel, Manifest-Hash und Entfernung aus aktiven
  Finding-Übersichten prüfen.
- Bei Reaktivierung des Scope Tool-Versionen, Commands, Exits und legitime
  Controls in einer genehmigten isolierten Umgebung aufzeichnen.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- Keine für den nutzergewählten aktuellen lokalen Scope. Diesen Record vor der
  Anforderung einer isolierten exakten Python-/Native-/Optional-Tool-Umgebung
  wiederherstellen.

## Blockers / Blocker

- Keine innerhalb des aktuellen lokalen Scope. Die beobachteten Lücken bleiben
  für die Reaktivierung aufbewahrt und werden nicht als bestanden dargestellt.

## Related findings / Verwandte Findings

- `FND-PARENT-0008`
- `FND-CROSS-0004`

## Residual risk / Restrisiko

Es wird kein Risiko akzeptiert. Exakte lokale
Python-/Native-/Optional-Tool-Validierung und ein Hosted-CI-Ergebnis bleiben
unbeobachtet; vor ihrer Nutzung als Akzeptanz- oder Release-Claim
wiederherstellen und neu validieren.

## Aktuelle nutzergerichtete Archiv- und Scope-Disposition — 2026-07-26

Der aktuelle Nutzer wählte einen lokalen Testumfang, in dem die exakte lokale
Python-3.14.6-/Native-/Optional-Tool-Parität kosmetisch statt blockierend ist,
weil GitHub der Host-Umgebung voraus sein kann. Daher ist dieser Record für
diesen Scope `not_applicable` und wird verlustfrei archiviert; er ist weder
technisch geschlossen noch auf einer exakten lokalen oder Hosted-CI-Lane
bewiesen.

Aktuelle Entscheidungs-Evidence: Run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, Artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.
Es erfolgten keine Tool-Provisionierung, Host-Mutation, Produktänderung oder
Hosted-CI-Ausführung. Vor jedem lokalen Paritäts-, Produktions-,
Veröffentlichungs- oder Release-Claim das vollständige Tripel wiederherstellen
und seine ursprünglichen Approved-Environment-Controls ausführen.

Archivpfad: `.codex/archive/findings/FND-HOST-0002/`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T17:20:47Z`: python_313_ci_lane_host_gap_recorded — Der Host
  lieferte Python 3.14.4 und kein `python3.13`-Executable. Fokussierte
  Python-Contracts bleiben gültige lokale Control-Evidence, belegen aber nicht
  die deklarierte Python-3.13-CI-Lane. Keine Interpreter-Installation wurde
  versucht.

## Aktueller Go-Toolchain-Blocker — 2026-07-23

Der aktuelle Master `a308d7b414f0859490fe7253e0683a4bde80b563` deklariert Go
`1.26.5` für die tatsächlichen Envoy- und Traefik-Module. Die installierte
Host-Executable ist `go1.26.0 linux/amd64`; ein kontrolliertes
`GOTOOLCHAIN=local go mod graph` im Envoy-Modul endet vor der
Dependency-Auflösung mit Exit `1`:

```text
go.mod requires go >= 1.26.5 (running go 1.26.0; GOTOOLCHAIN=local)
```

Es wurde weder eine lokale `go1.26.5`-Executable noch eine gecachte
Side-by-Side-Toolchain gefunden. Es wurde kein impliziter Download und keine
Installation versucht. Der sichere nächste Schritt erfordert eine ausdrückliche
Freigabe des aktuellen Benutzers für eine offizielle Go-`1.26.5`-Toolchain, die
nur unter dem registrierten Task-Cache genutzt wird; sie darf weder eine
System-/User-local-Toolchain ersetzen noch als Nebeneffekt Projektmanifeste
ändern.

Aufbewahrte Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/go/01-go-mod-graph-local-toolchain-block.log`
(SHA-256 `6fcac7c9821e4b4faf044b31777003615683879da3d4ad4b3042669d1a57e26c`).
## Auflösung des Go-Toolchain-Blockers für diesen Task — 2026-07-23

Der aktuelle Benutzer autorisierte ein offizielles Go-1.26.5-Archiv nur im
registrierten Task-Cache. Seine SHA-256 stimmte mit
5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053 überein,
und die task-lokale Executable meldete Go 1.26.5 linux/amd64. Sie lief mit
isoliertem GOCACHE, GOMODCACHE, GOPATH, GOTMPDIR, GOWORK=off,
GOTOOLCHAIN=local und GOFLAGS=-mod=readonly.

Dieser eng begrenzte Go-Blocker ist für den Task gelöst: Envoy-Dependency- und
Traefik-Fuzz-Validierung wurden abgeschlossen, und Draft PRs #99 und #100
bestanden ihre exakten Head-Prüfungen. Weder System-/User-Go-Installation noch
globale Konfiguration wurden geändert. Das löst nicht die verbleibenden
Python-3.13-, Native-Host- oder optionalen Tool-Lücken dieses Findings; sein
übergreifender blocked-Status bleibt daher unverändert.

Aufbewahrte Delivery-Evidence:
 /var/tmp/codex/ModSecurity-conector/runs/20260723T165434Z-github-alert-remediation-go1265-4fc93743/evidence/delivery/20260723-draft-pr-delivery-alert-state.md
(SHA-256 7508110eef978259f0b9757df675844535b44bd5e6a4dc30c92d265da05110de).

## Aktuelle Host-Prerequisite-Revalidierung — 2026-07-26

Das kanonische Parent-Ziel ist exaktes Python 3.14.6. Der aktuelle Host und die
lokale Virtual Environment melden nur Python 3.14.4, kein
`python3.14.6`-Executable löst auf, und das eingegrenzte Native-/Optional-Tool-
Inventar bleibt nicht verfügbar. Die aufbewahrte aktuelle Evidence ist Run
`20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`, Artifact
`evidence/fnd-host-0002-0003-0004-0006-current-revalidation.md`, SHA-256
`81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`.

Es erfolgten keine Installation, Host-Mutation, Produktänderung oder Delivery-
Aktion. Das Finding bleibt `blocked_environment`, bis ein ausdrücklich
autorisierter isolierter Tool-Bundle- oder Host-Owner-Setup vorliegt.
