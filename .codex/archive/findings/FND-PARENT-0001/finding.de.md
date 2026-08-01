# FND-PARENT-0001 — Go-Advisory-Ergebnisse erfordern eine Entscheidung für eine unterstützte gepatchte Go-Linie

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0001` |
| Title / Titel | `Go-Advisory-Ergebnisse erfordern eine Entscheidung für eine unterstützte gepatchte Go-Linie` |
| Category / Kategorie | `dependency_risk` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `validated` |
| Status | `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Der OSV-Workflow-Lauf 29783388062 auf dem resultierenden Master meldet 15 unknown vulnerabilities in den Go-Modulen von Envoy und Traefik; die 18 mit Go 1.24.13 kompatiblen Vorkommen fehlen in diesem Ergebnis, während jedes verbleibende Vorkommen Go 1.25.8 oder neuer erfordert und entscheidungsabhängig bleibt.

## Observed behavior / Beobachtetes Verhalten

PR #71 mit Head b1eef0a087432aa9bf9bc1243a34b0b0d8f6080e wurde am 2026-07-20T22:16:36Z per Squash als Master 929fe60dfca30787947027e5bd49003581a5b080 gemergt; dessen Tree fae388da52f5d660c8e18f06b058ec67b38adfd7 entspricht dem geprüften Head-Tree. Der OSV-Workflow-Lauf 29783388062 schloss seinen Wrapper erfolgreich ab, aber der Scanner endete mit 1 und meldet 15 unknown vulnerabilities; die 18 mit Go 1.24.13 kompatiblen Vorkommen fehlen und alle verbleibenden Vorkommen erfordern Go 1.25.8 oder neuer.

## Expected behavior / Erwartetes Verhalten

Eine unterstützte Kompatibilitäts- und Dependency-Entscheidung für Go 1.25.8 oder neuer muss getroffen und validiert werden, bevor dieser validierte P1-Release-Blocker fortschreiten kann.

## Impact / Auswirkung

Der validierte P1-Release-Blocker bleibt bestehen: 15 vom Scanner gemeldete unknown vulnerabilities können ohne die Entscheidung für Go 1.25.8 oder neuer keine unterstützte Disposition erhalten.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `Envoy Go module`
- `Traefik Go module`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '83,86p;216p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:83-86,216-216`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '83,86p;216p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Der aktuelle Abgleich ersetzt die historische Baseline oben: Die Go-1.24.13-Änderung entfernte die 18 kompatiblen Scanner-Vorkommen, aber jedes verbleibende Vorkommen erfordert Go 1.25.8 oder neuer; eine Produktcode-Grundursache wird nicht behauptet.

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Eine ausdrückliche unterstützte Kompatibilitätsentscheidung für Go 1.25.8 oder neuer treffen, Dependencies nur innerhalb dieser Entscheidung aktualisieren und den exakten OSV-Scan sowie Modultests erneut ausführen.

Eine für die gemeldeten Advisories geeignete unterstützte gefixte Go-Patch-Linie auswählen und govulncheck sowie Modultests erneut ausführen.

## Acceptance criteria / Akzeptanzkriterien

- A supported Go patch line covers the retained advisory IDs or each remaining item has an explicit supported disposition.
- govulncheck result data and Go tests are retained for the exact toolchain.

## Validation plan / Validierungsplan

- Run govulncheck for Envoy and Traefik with the selected Go version.
- Run go test ./..., go vet ./..., and their legitimate controls.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0003`

## Residual risk / Restrisiko

Alle 15 verbleibenden vom Scanner gemeldeten Vulnerabilities bleiben offen und entscheidungsabhängig; der aktuelle Benutzer hat kein Risiko akzeptiert.

## Abgleich des resultierenden Parent-Masters nach PR #71 / Resulting Parent master reconciliation after PR #71

Die retained resulting-master Receipt dokumentiert, dass PR #71 mit Head b1eef0a087432aa9bf9bc1243a34b0b0d8f6080e am 2026-07-20T22:16:36Z per Squash als Master 929fe60dfca30787947027e5bd49003581a5b080 gemergt wurde und dass beide Trees fae388da52f5d660c8e18f06b058ec67b38adfd7 entsprechen. Der OSV-Workflow-Lauf 29783388062 hatte Advisory-Wrapper-Erfolg, Scanner-Exit 1 und 15 unknown vulnerabilities. Die 18 mit Go 1.24.13 kompatiblen Rows fehlen im Scanner-Ergebnis; alle verbleibenden Vorkommen erfordern Go 1.25.8 oder neuer und bleiben entscheidungsabhängig. Status bleibt validated und Priorität bleibt P1; keine Risikoakzeptanz, Verifikation oder Schließung wird behauptet.

Evidence-Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260720T164715Z-parent-security-reconciliation-5a22cbf5/evidence/resulting-master-go12413-delivery-and-scan-reconciliation-20260720T221900Z.json. SHA-256: f8e8fa49a9aa8639b61946b49fca49bc0fc06623a80554f4145f78ade6ad71b2. Producer Command: RTK-proxied exact resulting-master PR #71 delivery, OSV, secret-wrapper, GitHub security, and SonarQube Cloud reconciliation after squash merge.

## History / Historie

- 2026-07-20T22:19:00Z: post_pr71_resulting_master_osv_reconciled — Resulting-master Receipt ergänzt; P1-Status validated bleibt, ohne Verifikation, Schließung oder Risikoakzeptanz.
- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.

## Aktueller Abgleich — 2026-07-23

Dieser Abschnitt ersetzt für die aktuelle Alert-Entscheidung die historische
Go-1.24-Kompatibilitätsannahme. Der aktuelle Master
`a308d7b414f0859490fe7253e0683a4bde80b563` deklariert Go `1.26.5` für das
Envoy-ext_proc-Modul. Seine zwei aktuellen Dependabot-Alerts sind unabhängig
als offen bestätigt:

- `golang.org/x/net v0.48.0` (Alert #1) liegt unter Dependabots Advisory-Fix
  `v0.55.0`. Die aktuelle offizielle OSV-Antwort identifiziert zusätzlich neun
  verwundbare `x/net`-IDs; die kleinste vollständige Modulversion ist `v0.56.0`.
- Die direkte Runtime-Abhängigkeit `google.golang.org/grpc v1.79.3` (Alert #2)
  liegt unter dem offiziellen OSV-/Dependabot-Fix `v1.82.1`.

Beide Kandidatenmodule deklarieren Go `1.25.0`; damit ist die bereits im
Repository deklarierte Go-`1.26.5`-Baseline kompatibel. Die lokale Validierung
kann noch nicht starten: Die installierte Go-`1.26.0`-Executable verweigert
das Modul korrekt mit `GOTOOLCHAIN=local`, und es existiert keine lokale
`go1.26.5`-Toolchain. Die Policy verbietet einen impliziten Download; daher ist
eine ausdrückliche Freigabe des aktuellen Benutzers für eine isolierte offizielle
Go-`1.26.5`-Beschaffung/-Nutzung im registrierten Task-Cache erforderlich. Es
erfolgten keine Dependency-Mutation, Alert-Schließung, Risikoakzeptanz oder
Verifikation.

Aufbewahrte aktuelle Evidence:

- gRPC-OSV-Antwort:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/go/05-osv-grpc-v1.79.3.json`
  (SHA-256 `801a60594f60869ee48033d8bf7d9ad1248c3964752d10b19b143f0e158a4d61`).
- x/net-OSV-Antwort:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/go/06-osv-x-net-v0.48.0.json`
  (SHA-256 `b8f11f2a4b68c905d803f0d23e32666866935fe5a09a905518ed425841ec0a18`).
## Draft-PR-Remediation-Update — 2026-07-23

Der Benutzer genehmigte eine offizielle Go-1.26.5-Side-by-Side-Toolchain nur
im registrierten Task-Run. Ihre verifizierte Archiv-SHA-256 lautet
5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053; sie
änderte weder Host-/System-Toolchain noch die Go-Baseline des Repositorys.

Draft PR [#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99)
mit exaktem Head 2f0d8a234f984b731229aca01d43caf2749a7d61 wählt gRPC v1.82.1,
x/net v0.56.0, x/sys v0.46.0 und x/text v0.39.0 aus. Resolver-/Tidy-/Verify-,
Test-, Vet-, Build-, govulncheck-, ein 17-Test-Dependency-Floor-Vertrag sowie
alle exakten PR-Head-Prüfungen bestanden. Der unabhängige fokussierte
Security-Review fand keinen neuen berichtspflichtigen Befund.

Das Finding bleibt validated: Der aktuelle Master wählt weiterhin die
verwundbaren Versionen und GitHub meldet weiterhin beide Dependabot-Alerts. Der
PR ist als Draft offen und autorisiert weder Merge noch Alert-Schließung. Die
Runtime-Config- und Bilingual-Einschränkungen des isolierten Worktrees bleiben
dokumentierte Kontrollen, keine fehlgeschlagene Remediation-Evidence.

Aufbewahrte Delivery-Evidence:
 /var/tmp/codex/ModSecurity-conector/runs/20260723T165434Z-github-alert-remediation-go1265-4fc93743/evidence/delivery/20260723-draft-pr-delivery-alert-state.md
(SHA-256 7508110eef978259f0b9757df675844535b44bd5e6a4dc30c92d265da05110de).

## Verifikation auf aktuellem Master — 2026-07-24

Der historische Go-Advisory-Zustand ist auf dem aktuellen Parent-Master
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7` als behoben verifiziert.

- PR [#99](https://github.com/Easton97-Jens/ModSecurity-conector/pull/99)
  wurde vom exakten Head
  `2f0d8a234f984b731229aca01d43caf2749a7d61` als
  `5b8db00d44ab24f3a9f4216a00f7edee977b6898` gemergt; seine exakten
  Head-Prüfungen hatten 33 erfolgreiche und sechs scope-gerechte Skips.
- PR [#100](https://github.com/Easton97-Jens/ModSecurity-conector/pull/100)
  wurde vom exakten Head
  `dace5ca118a89a91c33fde952a6282f9c391ee10` als
  `6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d` gemergt; seine exakten
  Head-Prüfungen hatten ebenfalls 33 erfolgreiche und sechs scope-gerechte
  Skips.
- GitHub meldet Dependabot #1 (`golang.org/x/net`) und #2
  (`google.golang.org/grpc`) unabhängig seit `2026-07-23T20:14:31Z` als
  `fixed`, mit `dismissed_at = null`; das aktuelle offene Dependabot-Inventar
  ist leer. Der aktuelle Master wählt `x/net v0.56.0` und `grpc v1.82.1`.
- Mit der aufbewahrten offiziellen task-lokalen Toolchain
  `go1.26.5 linux/amd64` und task-eigenen Caches bestanden Envoy und Traefik
  `go test ./...` und `go vet ./...`. Beide Läufe von
  `govulncheck -show verbose ./...` meldeten `No vulnerabilities found.` Auch
  die begrenzte Traefik-Fuzz-Kontrolle auf aktuellem Master bestand (99.749
  Ausführungen in 15 Sekunden, ein Worker).

Damit ist die ursprüngliche Reproduktion nicht mehr vorhanden, während die
legitimen Modul-/Test-Kontrollen funktionsfähig bleiben. Die separaten aktuellen
Scorecard-Alerts einschließlich des PyYAML-Berichts gehören nicht zu diesem
Go-Finding und bleiben in `FND-GITHUB-0001` erfasst; keiner wurde dismissed
oder risikoakzeptiert.

Aufbewahrte Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/github-alert-closure-verification.md`
(SHA-256 `20ea82fbd04cc7ea672a644c4c5c5621b38b6fc29ce76ed9c54f028ca458afdf`).

## Historien-Update — 2026-07-24

- `2026-07-24T15:39:43Z`: `current_master_go_dependency_remediation_verified`
  — Dependabot-Neuauswertung auf gemergtem Master, Tests mit der ausgewählten
  Toolchain, Vet, govulncheck und die begrenzte Fuzz-Kontrolle bestanden. Das
  Finding wechselt von `validated` zu `verified`; sein Lifecycle-Close folgt
  erst nach EN/DE/JSON-Paritätsvalidierung.

## Schließung — 2026-07-24

Um `2026-07-24T15:43:59Z` wurden die EN/DE/JSON-Parität und die Checksumme der
aufbewahrten Evidence validiert. Das Finding wechselt von `verified` zu
`closed`: Der aktuelle Master reproduziert den ursprünglichen Go-Dependency-
Zustand nicht mehr, die legitimen Kontrollen bestehen und GitHub meldet beide
betroffenen Dependabot-Alerts unabhängig ohne manuelles Dismissal als fixed.
Die aktiven Scorecard-Alerts liegen außerhalb dieses Findings und bleiben in
`FND-GITHUB-0001` erfasst.

## Maßgeblicher Post-Closure-Master-Recheck — 2026-07-24

Nachdem die Closure-Evidence aufbewahrt wurde, rückte der maßgebliche Parent-
`master` um einen Commit von `8e36b86ac17bce06003b0505fe26f6bb60c3cec7` auf
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` vor. Der GitHub-Vergleich enthält
nur den bilingualen Change Record/Index und
`tests/test_full_lifecycle_evidence.py`; weder eines der betroffenen Go-Module
noch das Traefik-Target `FuzzUDSFrameAndResult` wurden geändert. Ein frischer
maßgeblicher Read meldet Dependabot #1/#2 weiter als `fixed`,
`dismissed_at = null` und keine offenen Dependabot-Alerts. Alle 14
beobachteten Push-Workflows auf aktuellem Master sind erfolgreich. Der
ursprüngliche Zustand bleibt damit nicht reproduzierbar und die geschlossene
Disposition ist weiter aktuell.

Aufbewahrte Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-advance-recheck.md`
(SHA-256 `c099c32564c1a78e60f98a61ba350904669d9c7231459c4109587088e31f915f`).

- `2026-07-24T15:55:37Z`: `post_closure_authoritative_master_rechecked` —
  ein Master-Vorrücken nur mit Dokumentations-/Teständerungen wurde verglichen;
  relevante Go-Remediation, maßgeblicher Dependabot-Zustand und erfolgreiche
  Workflow-Menge blieben unverändert.

## Zweiter maßgeblicher Post-Closure-Master-Recheck — 2026-07-24

Der Parent-`master` rückte anschließend um einen weiteren Commit auf
`185fd358bcfabe63464ab0e135eecedf24c9a699` vor. Sein Vergleich ab
`a99bd0bb1c28ab3842f021b9234c6209dbe1f8c0` ändert nur einen bilingualen
Change Record/Index und `tests/test_full_lifecycle_profiles.py`; die
betroffenen Envoy-Go-Module und das Traefik-Target `FuzzUDSFrameAndResult`
bleiben unverändert. Dependabot #1/#2 bleiben mit `dismissed_at = null`
`fixed`, und das offene Dependabot-Inventar bleibt leer.

Der neue Master hat 14 abgeschlossene Push-Workflow-Läufe: 13 Erfolge und
einen fehlgeschlagenen OpenSSF-Scorecard-Lauf (`default-branch`, Run
`30107490735`); sein Check-Inventar meldet zusätzlich eine fehlgeschlagene
SonarCloud Code Analysis. Diese externen Workflow-/Quality-Zustände bleiben in
ihren bestehenden GitHub-/Sonar-Follow-up-Records erfasst. Sie führen den
unabhängig behobenen Go-Dependency-Zustand nicht erneut ein; dieses Finding
bleibt daher geschlossen.

Aufbewahrte zweite Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-second-advance-recheck.md`
(SHA-256 `17f4abdf4be2939aca498746e9e345d0e33566580adbee0b6e92427bf73b1c8b`).

- `2026-07-24T16:07:44Z`: `post_closure_second_authoritative_master_rechecked`
  — das zweite scope-irrelevante Master-Vorrücken, der gefixte Dependabot-
  Zustand und aktuelle externe Workflow-Fehler wurden erfasst, ohne die
  geschlossene Go-Remediation erneut zu öffnen oder zu schwächen.

## Finaler Current-Master-Recheck nach Scorecard-Wiederholung — 2026-07-24

Der Parent-`master` bleibt `185fd358bcfabe63464ab0e135eecedf24c9a699`; sein
Scope für Go-Module und Traefik-Fuzz-Target ist unverändert. Dependabot #1/#2
bleiben mit `dismissed_at = null` `fixed`, und das offene Dependabot-Inventar
ist leer. OpenSSF-Scorecard-Run `30107490735`, Versuch 3, war um
`2026-07-24T16:14:21Z` erfolgreich; damit sind alle 14 beobachteten
GitHub-Actions-Push-Workflows erfolgreich.

GitHub hat alle sechs Scorecard-Alert-Instanzen auf diesen exakten aktuellen
Master aktualisiert; sie bleiben separat offen. SonarCloud Code Analysis bleibt
ebenfalls ein separater fehlgeschlagener Check. Keine dieser Bedingungen führt
den behobenen Go-Dependency-Zustand erneut ein, daher bleibt
`FND-PARENT-0001` ohne Alert-Dismissal oder Control-Schwächung geschlossen.

Aufbewahrte finale Recheck-Evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260724T152905Z-pr99-pr100-alert-closure-20260724-23a1b3b3/evidence/post-master-scorecard-retry-final-recheck.md`
(SHA-256 `2a788454ba88bcd90add62b5eae3545d83a53180f7aefe8c72ffc864a2959746`).

- `2026-07-24T16:14:53Z`: `post_closure_final_current_master_rechecked` —
  alle aktuellen Actions-Workflows bestehen nach der Scorecard-Wiederholung;
  aktualisierte Scorecard-Alerts und der fehlgeschlagene SonarCloud-Check
  bleiben getrenntes Follow-up.
