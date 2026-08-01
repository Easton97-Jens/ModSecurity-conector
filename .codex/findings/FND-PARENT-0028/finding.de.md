# FND-PARENT-0028 — SHA-gepinnte Parent-Scanner-Actions behalten mutable Docker-Image-Abhängigkeiten

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0028 |
| Titel | SHA-gepinnte Parent-Scanner-Actions behalten mutable Docker-Image-Abhängigkeiten |
| Kategorie | security_hardening |
| Repository | parent |
| Ownership | parent |
| Priorität | P2 |
| Schweregrad | medium |
| Konfidenz | confirmed |
| Status | triaged |
| Machbarkeitsstatus | requires_user_decision |
| Security-Bewertung | validated |
| Release-Blocker | false |
| Security-Relevanz | true |
| Protokoll/Profil | GitHub Actions CI / OSV- und OpenSSF-Scorecard-Scanner-Workflows |

## Zusammenfassung

Der Parent pinnt die äußeren OSV- und OpenSSF-Scorecard-Git-Action-
Repositories auf vollständige Commit-SHAs, aber die Action-Metadaten an genau
diesen Revisionen führen Docker-Images aus, die über mutable Versionstags
ausgewählt werden. Die äußere Git-SHA bindet damit nicht den endgültigen
ausführbaren Container-Payload.

## Beobachtetes Verhalten

Auf Parent `origin/master`
`c8ca0d92b630c18232b881855c4f5d1482568ea6`:

- `.github/workflows/ci-security-osv.yml` ruft
  `google/osv-scanner-action/osv-scanner-action` und
  `google/osv-scanner-action/osv-reporter-action` auf
  `9a498708959aeaef5ef730655706c5a1df1edbc2` auf.
- Die Metadaten an genau dieser Git-Revision deklarieren `runs.using: docker`
  und `docker://ghcr.io/google/osv-scanner-action:v2.3.8` sowohl für die
  Scanner- als auch für die Reporter-Action.
- `.github/workflows/ci-security-scorecard.yml` ruft
  `ossf/scorecard-action` auf `4eaacf0543bb3f2c246792bd56e8cdeffafb205a`
  auf. Deren exakte `action.yaml` deklariert `runs.using: docker` und
  `docker://ghcr.io/ossf/scorecard-action:v2.4.3`.
- Der OSV-Pull-Request-Job und der Scorecard-Default-Branch-Job vergeben
  `security-events: write`.
- `ci/tooling/security-tools.lock.yml` erfasst die äußeren Git-SHAs, aber
  keine unveränderliche Identität für diese verschachtelten Images.

## Erwartetes Verhalten

Jeder ausführbare Scanner-Payload muss an eine unveränderliche, unabhängig
verifizierbare Artefaktidentität gebunden sein. Eine vollständige äußere Git-
Action-SHA allein ist unzureichend, wenn die Action-Metadaten die Ausführung an
einen mutablen Container-Tag delegieren. Job-Berechtigungen müssen für den
gewählten Reporting-Mechanismus minimal bleiben.

## Auswirkung

Ein späteres Tag-Retargeting, ein kompromittierter Registry-Publisher oder ein
Registry-Supply-Chain-Vorfall kann den von diesen Jobs ausgeführten Code
ändern, ohne dass sich Parent-Workflow oder äußere Action-SHA ändern. Die
betroffenen Jobs verarbeiten Repository-Inhalte und können in den genannten
Kontexten Security Events schreiben. Dieser Record behauptet nicht, dass ein
Retagging oder eine Kompromittierung erfolgt ist.

## Betroffene Dateien und Symbole

### Dateien

- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`

### Symbole und Action-Metadaten

- `google/osv-scanner-action/osv-scanner-action`
- `google/osv-scanner-action/osv-reporter-action`
- `ossf/scorecard-action`
- `runs.using: docker`
- `runs.image`

### Herkunft

- Parent-Source-Commit: `c8ca0d92b630c18232b881855c4f5d1482568ea6`
- OSV-Action-Revision: `9a498708959aeaef5ef730655706c5a1df1edbc2`
- Scorecard-Action-Revision: `4eaacf0543bb3f2c246792bd56e8cdeffafb205a`

## Voraussetzungen

- Ein Parent-OSV- oder -Scorecard-Workflow führt die benannte SHA-gepinnte
  äußere Action aus.
- GitHub Actions löst das in diesen Action-Metadaten deklarierte Docker-Image
  auf.
- Der referenzierte Image-Tag wird nach dem Pinning der Action-Git-Revision
  retargetet, oder seine Publisher-/Registry-Trust-Grenze wird kompromittiert.

## Reproduktion

1. `rtk git show origin/master:.github/workflows/ci-security-osv.yml` und
   `rtk git show origin/master:.github/workflows/ci-security-scorecard.yml`
   ausführen.
2. Die vollständigen äußeren Action-SHAs und die OSV-Pull-Request- oder
   Scorecard-Default-Branch-Berechtigung `security-events: write` beobachten.
3. Die Action-Metadaten an exakt
   `9a498708959aeaef5ef730655706c5a1df1edbc2` und
   `4eaacf0543bb3f2c246792bd56e8cdeffafb205a` abrufen; `runs.using: docker`
   und Image-Werte mit `:v2.3.8` oder `:v2.4.3`, nicht mit Image-Digest,
   beobachten.
4. Den äußeren Git-Pin mit der verschachtelten Tag-Auflösungsgrenze
   vergleichen: Der Workflow enthält keinen unveränderlichen Digest für das
   ausgeführte Image.

## Evidence

- Run-ID: `20260718T110742Z-fnd-parent-0028-mutable-action-images`
  - Artefakt:
    `.codex/runs/20260718T110742Z-fnd-parent-0028-mutable-action-images/validation.md`
  - Typ: `parent_ci_supply_chain_validation_receipt`
  - SHA-256:
    `2f1016917d0a0e1dc46bdd8901a4e4f6860d48ba5cdc25d0d0b698c7f16db732`
  - Command: `rtk git rev-parse origin/master`; RTK-vermitteltes `git show`
    der Parent-OSV-, Scorecard- und Action-Lock-Dateien; RTK-vermittelter Abruf
    der exakten Upstream-Action-Metadaten an den gepinnten Commits.
  - Working directory: `/root/git/ModSecurity-conector`; Exit-Code: `0`;
    beobachtet `2026-07-18T11:07:42Z`; Retention:
    `retained_local_evidence`.
- Source-Inventar:
  `.codex/runs/20260718T110742Z-fnd-parent-0028-mutable-action-images/source-inventory.json`
  (SHA-256
  `32714b3b8dab1eda6cbeadf365e2bdbdc969877221d6d166e684763833bac781`).
- Vollständiger Command-Record:
  `.codex/runs/20260718T110742Z-fnd-parent-0028-mutable-action-images/command-record.md`
  (SHA-256
  `c100a6e4fea8b27f48ab24d487a6b16996eac24fd775cc022b4e6732af0a5b2c`).

## Grundursachenanalyse

Das Parent-Modell für immutable Actions und Lock-Dateien erfasst den äußeren
Git-Repository-Commit, modelliert oder verifiziert aber nicht die in Docker-
basierten Action-Metadaten deklarierte Docker-Image-Identität. Ein Git-SHA-Pin
endet daher an der Action-Repository-Grenze, während die Container-Runtime
später einen mutablen Tag auflöst.

## Vorgeschlagene Remediation

Eine separate Parent-eigene Remediation-Aufgabe erstellen. Bevorzugt einen
checksum-verifizierten eigenständigen OSV-Scanner- und Scorecard-CLI aus
explizit gelockten offiziellen Release-Assets verwenden, mit task-spezifischer
tokenloser lokaler Ausgabe. Falls eine Docker-Action erforderlich bleibt, einen
unveränderlichen Image-Digest samt Provenienz- und Erneuerungsvalidierung
erfassen und erzwingen. `security-events: write` entfernen, wenn lokale JSON-/
Advisory-Ausgabe keinen SARIF-Upload benötigt; nur für das gewählte Verhalten
erforderliche Berechtigungen beibehalten.

## Akzeptanzkriterien

- Die Parent-OSV- und -Scorecard-Ausführungspfade lösen zur Job-Laufzeit keinen
  mutablen Container-Tag mehr auf.
- Jedes ausgeführte Scanner-Artefakt hat eine exakte unveränderliche Identität
  mit aufbewahrter Provenienz- und Verifikations-Evidence.
- Der Parent-Lock/-Vertrag erkennt künftig eine mutable verschachtelte Docker-
  Image-Abhängigkeit oder dokumentiert den verifizierten unveränderlichen
  Ersatzmechanismus.
- Job-Berechtigungen sind auf den gewählten Reporting-Pfad beschränkt;
  `security-events: write` existiert nur, wenn ein verifizierter SARIF-Upload-
  Pfad dies erfordert.
- Fokussierte Contract-Tests, actionlint/ShellCheck, Zizmor, Scanner-
  Kontrollfälle, Exact-Head-CI, CodeQL, Security-Checks, Scorecard, SonarQube
  Cloud, Reviews und Review-Thread-Checks bestehen auf dem Parent-
  Remediation-PR.

## Validierungsplan

- Vor jeder Parent-Source-Änderung exakte Parent-Master-Workflow-Source und
  verschachtelte Action-Metadaten/Image-Identität erneut validieren.
- Einen fokussierten Parent-CI-Security-Contract-Test ergänzen, der eine
  Docker-basierte Scanner-Action mit mutablem Tag ablehnt und mit dem gewählten
  unveränderlichen Ersatz besteht.
- Parent-CI-Security-Contract-Checks, actionlint/ShellCheck, offline Zizmor,
  Gitleaks/OSV/Scorecard-legitime Kontrollen sowie Dokumentations-/Change-
  Record-Checks ausführen.
- Für den Parent-Remediation-PR lokale SHA = Remote-SHA = PR-Head verifizieren
  und danach Exact-Head-CI, CodeQL, Security-Checks, Scorecard, SonarQube
  Cloud, Reviews und ungelöste Review-Threads prüfen.

## Regressionstests

- Ein Parent-CI-Security-Contract-Test lehnt mutable verschachtelte Docker-
  Image-Tags für OSV- und Scorecard-Ausführungspfade ab.
- Der Parent-Immutable-Action-Registry/-Contract-Test deckt die Ersatz-
  Artefaktidentität ab.
- Eine Negativ-Fixture beweist, dass eine äußere Git-SHA die verschachtelte
  Image-Invariante nicht fälschlich erfüllt.

## Legitime Kontrolltests

- Der gewählte OSV-Scan analysiert weiterhin den vorgesehenen Dependency-
  Scope und meldet sein dokumentiertes Ergebnis.
- Der gewählte Scorecard-Check erzeugt weiterhin das dokumentierte lokale oder
  SARIF-Ergebnis mit nur den benötigten Berechtigungen.
- Eine bekannte sichere Workflow-Fixture mit unveränderlicher Scanner-
  Artefaktidentität besteht den fokussierten Contract.

## Abhängigkeiten

- Eine separat autorisierte Parent-eigene CI-Remediation-Aufgabe und ihr
  Delivery-Lifecycle.

## Blocker

- Die aktive Framework-CI-Security-Aufgabe schließt Parent-Produkt- und
  Workflow-Änderungen ausdrücklich aus.

## Verwandte Findings und Deduplizierung

- `FND-PARENT-0018`
- `FND-GITHUB-0001`
- Dies ist kein Duplikat von `FND-PARENT-0018`: Dieser Record betrifft äußere
  CodeQL-Action-Version- und Registry-Konsistenz, während der vorliegende
  Record die mutable Auflösung ausführbarer Docker-Images innerhalb separat
  SHA-gepinnter OSV- und Scorecard-Action-Metadaten betrifft.

## Restrisiko

Die aktuellen Parent-Workflows behalten die verschachtelte mutable Image-Tag-
Grenze, bis eine separat autorisierte Parent-Remediation verifiziert ist. Die
vollständigen äußeren Git-SHAs bleiben ein partielles Control, binden aber nicht
das ausgeführte Image. Es wurde kein Risiko akzeptiert.

## Historie

- `2026-07-18T11:07:42Z`:
  `validated_nested_mutable_docker_image_dependency` — aktuelle Parent-OSV-
  Scanner/Reporter- und Scorecard-Workflows wurden auf
  `c8ca0d92b630c18232b881855c4f5d1482568ea6` inspiziert. Exakte Upstream-
  Action-Metadaten an ihren äußeren Git-SHAs lösen v2.3.8- und v2.4.3-Docker-
  Image-Tags statt unveränderlicher Digests auf. Es wurde keine Produkt-, Git-,
  Framework- oder MRTS-Änderung vorgenommen.
