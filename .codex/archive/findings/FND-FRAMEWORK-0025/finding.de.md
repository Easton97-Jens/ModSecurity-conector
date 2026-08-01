# FND-FRAMEWORK-0025 — Codex-Security-Rank-Input-Helper lässt alle gestagten CI- und Testdateien von Framework-PR #30 aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-FRAMEWORK-0025 |
| Kategorie | tooling |
| Repository / Ownership | framework / external_tool |
| Priorität / Severity | P2 / not_applicable |
| Confidence / Status | reproduced / accepted_risk |
| Feasibility | blocked_external_dependency |
| Release-Blocker | false |
| Security-relevant | true |

## Zusammenfassung, Beobachtung, erwartetes Verhalten und Auswirkung

Der Codex-Security-Rank-Input-Helper wurde im Local-Patch-Modus für
Framework-PR #30 erfolgreich beendet, gab aber null Worklist-Zeilen aus,
obwohl Git vierzehn explizit gestagte Refaktor-Dateien meldete. Seine statische
EXCLUDED_DIRS schließt ci und tests aus und entfernt dadurch die geänderten
ausführbaren CI-Helfer und Regressionstests aus der generierten Worklist.

Die generierte Worklist hätte daher die folgenden gestagten Dateien ausgelassen:

| Pfad |
| --- |
| ci/lib/generated_report_utils.py |
| ci/lib/report_output_paths.py |
| ci/lib/runtime_path_safety.py |
| ci/provisioning/import-mrts-cases.py |
| ci/reporting/generate-case-matrix.py |
| ci/reporting/generate-connector-work-queue.py |
| ci/reporting/generate-mrts-native-report.py |
| ci/reporting/generate-phase-work-queue.py |
| ci/reporting/update-runtime-snapshot.py |
| reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.de.md |
| reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.md |
| tests/protocol_client/test_check_protocol_evidence.py |
| tests/security_regression/git_provenance_test_support.py |
| tests/security_regression/test_modsecurity_v3_git_ref_provenance.py |

Eine manuell rekonstruierte exakte Staged-File-Inventur führte alle vierzehn
Dateien wieder in rank_input.jsonl und deep_review_input.jsonl über. Jede Datei
hat nun einen Full-File-Review-Receipt, sodass kein PR-#30-Code ungeprüft blieb.
Der externe Tool-Defekt bleibt dennoch unabhängig bearbeitbar.

Für einen Local-Patch-Security-Diff-Scan muss der Helper für jede geänderte
CI- und Testdatei, einschließlich Pfaden unter ci und tests, eine Review-Zeile
ausgeben oder mit einer Coverage-Diagnose laut und nichtnull fehlschlagen. Eine
automatisierte Regression muss die ausgegebene Worklist mit der autoritativen
Staged-Git-Inventur vergleichen, bevor die Downstream-Review sie verwendet.

Eine erfolgreich beendete, aber leere Worklist kann fälschlich nahelegen, dass
kein relevanter Code vorhanden ist, und sicherheitssensitive CI-Helfer oder
Regression-Controls aus dem Review auslassen. Dieser Record belegt keine
ausnutzbare Framework-Schwachstelle. Die manuelle Recovery grenzt den aktuellen
PR-#30-Scan ein, daher ist dieser Befund kein Release-Blocker für den PR;
zukünftige Scans bleiben bis zur Korrektur des externen Helpers und seiner
Regression-Coverage gefährdet.

## Aktuelle lokale Archiventscheidung des Nutzers vom 2026-07-26

Der aktuelle Nutzer hat angewiesen, diesen Befund aus dem aktiven lokalen
Backlog zu nehmen, weil derzeit kein Framework-eigener Reparaturpfad verfügbar
ist. Sein Status ist deshalb `accepted_risk` ausschließlich für ein **lokales
test-only Archiv**, nicht `closed`, `fixed` oder `verified`. Der exakte
Decision-Receipt ist
`.codex/runs/20260726-framework-archive-current-dispositions/evidence/archive-decision.md`
(SHA-256 `4f314bd2ca703eb0509d71546648bfb0367c3d35f2ff1a1e13c56b7f9bedcc30`).

Der externe Codex-Security-Helper kann weiterhin geänderte `ci`- und
`tests`-Pfade stillschweigend auslassen. Vor einer Produktions-,
Veröffentlichungs- oder Reliance-Entscheidung diesen vollständigen Triplet nach
`.codex/findings/` zurückholen und eine externe Helper-Reparatur samt
Coverage-Regression beschaffen. Kein Fixture-Digest, Release-Tag oder anderer
Ersatz ist als Evidence für einen echten normalen NGINX-Upstream-Digest
akzeptiert.

## Scope, Voraussetzungen, Reproduktion und Evidence

Die Reproduktion erfordert den Framework-PR-#30-Task-Worktree mit vierzehn
explizit gestagten ACMR-Refaktor-Dateien relativ zu
504c8f164d4dab4bc857718af0233557ad48f727 sowie den Codex-Security-Helper
generate_rank_input.py mit make-diff-rank-input im Local-Patch-Modus. Der
Helper behält statische EXCLUDED_DIRS-Einträge für ci und tests.

1. generate_rank_input.py make-diff-rank-input --repo /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master --base 504c8f164d4dab4bc857718af0233557ad48f727 --mode local-patch
2. rtk git -C /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master diff --cached --name-only --diff-filter=ACMR 504c8f164d4dab4bc857718af0233557ad48f727
3. rtk wc -l /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/rank_input.jsonl /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/deep_review_input.jsonl

Aufbewahrte Evidence:

- Run: 20260719T230508Z-framework-pr30-duplication-master-37469460
- Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/plugin_rank_input_zero_result.md
- SHA-256: da798f36a3f592140bdbae7e167cea0675bcaf5a3ce0cac679502a4f74ec6ffe
- Command: generate_rank_input.py make-diff-rank-input --repo /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master --base 504c8f164d4dab4bc857718af0233557ad48f727 --mode local-patch
- Working Directory: /root/git/ModSecurity-conector
- Exit-Code: 0
- Beobachtet: 2026-07-19
- Retention: retained
- Ergebnis: Der Helper wurde trotz vierzehn gestagter Framework-PR-#30-
  Refaktor-Dateien mit null Zeilen erfolgreich beendet; das aufbewahrte
  Ergebnis dokumentiert die statische ci- und tests-Exclusion als Ursache.

- Run: 20260719T230508Z-framework-pr30-duplication-master-37469460
- Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/manual_worklist_recovery.md
- SHA-256: 58ac2336e4a735138bed74717eb3af37698f99a4e2ca9c22b400029859f666ac
- Command: rtk git -C /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master diff --cached --name-only --diff-filter=ACMR 504c8f164d4dab4bc857718af0233557ad48f727; recover rank_input.jsonl and deep_review_input.jsonl from the exact sorted inventory
- Working Directory: /root/git/ModSecurity-conector
- Exit-Code: 0
- Beobachtet: 2026-07-19
- Retention: retained
- Ergebnis: Die manuelle Recovery bestätigt, dass alle vierzehn gestagten
  Dateien bewusst wieder in die Downstream-Security-Diff-Worklist überführt
  wurden.

## Grundursache und vorgeschlagene Remediation

Der externe Codex-Security-Helper wendet im Local-Patch-Modus eine statische
Directory-Exclusion-Policy an, die ci und tests als nicht reviewbar behandelt.
Diese Policy ist mit diesem Framework-Repository unvereinbar, in dem
CI-Helfer und Regressionstests sicherheitsrelevante Controls implementieren und
verifizieren. Die erfolgreiche Beendigung vergleicht ihre leere Auswahl nicht
mit der autoritativen Staged-Git-Inventur und schlägt daher nicht fail closed
fehl.

Im externen Codex-Security-Tooling die bedingungslose Local-Patch-Exclusion
geänderter ci- und tests-Pfade entfernen oder eine Zero-Coverage-Bedingung mit
präziser Diagnose als nichtnullen Fehler behandeln. Eine automatisierte Fixture
hinzufügen, die geänderte ci- und tests-Dateien staged, vollständige
Rank-Input-Coverage prüft und verifiziert, dass der Downstream-Deep-Review-Input
dieselbe Pfadmenge bewahrt. Keine externe Tool-Remediation liegt im Scope von
Framework PR #30.

## Akzeptanzkriterien und Validierungsplan

- [pending] Der Local-Patch-Rank-Input-Helper gibt für jede geänderte CI- und
  Testdatei, einschließlich aller Pfade unter ci und tests, Zeilen aus oder
  endet mit einer präzisen Coverage-Diagnose nichtnull.
- [pending] Eine automatisierte Regression staged repräsentative ci- und
  tests-Dateien und beweist, dass rank_input.jsonl und deep_review_input.jsonl
  die vollständige autoritative Git-Pfadmenge bewahren.
- [pending] Der Scanner validiert seine generierte Worklist gegen die
  autoritative Staged-Git-Inventur, bevor er ein No-Files-Ergebnis melden kann.
- [pending] Ein Rerun auf der vierzehn-Dateien-PR-#30-Fixture meldet alle
  vierzehn reviewbaren Pfade ohne manuelle Ersetzung.
- [pending] Keine Framework-Source, kein Test, keine CI, keine
  SonarQube-Einstellung, kein Security-Control, kein Parent-Gitlink und kein
  MRTS-Zustand wird geschwächt oder geändert, um diesen Tool-Defekt zu
  verbergen.

Eine externe Tool-Regression-Fixture mit geänderten ci- und tests-Pfaden
ausführen und ihren Rank-Input-Output mit git diff --cached --name-only
--diff-filter=ACMR vergleichen. Sicherstellen, dass ein nichtleerer Staged-Diff
mit leerer generierter Worklist nichtnull endet und eine Coverage-Diagnose
enthält. Danach einen fokussierten Security-Diff-Scan erneut ausführen und
vollständige Work-Ledger-Receipts für jeden ausgegebenen Pfad verifizieren. Die
manuelle vierzehn-Dateien-Recovery-Evidence für Framework PR #30 beibehalten,
bis die externe Tool-Reparatur unabhängig bestanden hat.

## Regression- und Legitimate-Control-Tests

Regressionstests:

- Codex-Security-External-Tool-Local-Patch-Rank-Input-Coverage-Fixture für
  geänderte ci- und tests-Dateien.
- Codex-Security-External-Tool-Worklist-versus-Staged-Git-Inventory-Parity-
  Test.

Legitimate Controls:

- Ein nichtleerer Staged-Diff mit ci- und tests-Pfaden erzeugt passende
  Rank-Input- und Deep-Review-Worklist-Zeilen.
- Ein tatsächlich leerer Staged-Diff darf null Zeilen ohne falschen
  Coverage-Fehler melden.
- Ein nichtleerer Staged-Diff mit leerer generierter Worklist endet mit einer
  präzisen Coverage-Diagnose.

## Abhängigkeiten, Grenzen, verwandte Findings und Restrisiko

Abhängigkeiten sind der Codex-Security-External-Tool-Maintainer und
Release-Prozess, eine kontrollierte External-Tool-Regression-Fixture und die
aufbewahrte Framework-PR-#30-Local-Patch-Scan-Evidence. Es gibt keine aktuellen
Blocker oder Duplicate-Records.

Dies ist kein Duplicate von FND-FRAMEWORK-0023 oder FND-FRAMEWORK-0024. Diese
Findings besitzen eine SonarQube-Duplikations-Remediation beziehungsweise einen
Change-Record-Contract-Fehler in Framework PR #30. Dieser Befund besitzt den
unabhängig reproduzierbaren External-Scanner-Worklist-Selection-Defekt, der
ihren geänderten CI- und Testcode aus dem Security-Review hätte auslassen
können.

Bis der externe Helper repariert und regressionsgetestet ist, können zukünftige
Local-Patch-Security-Diff-Scans geänderte CI- und Test-Controls stillschweigend
auslassen. Der aktuelle PR-#30-Scan bleibt abgedeckt, weil die exakte
Staged-Git-Inventur manuell in vierzehn Worklist-Zeilen rekonstruiert wurde und
alle vierzehn Dateien Full-File-Review-Receipts zugeordnet sind. Dieser Befund
ist ausschließlich für lokales test-only Archiv risikoakzeptiert; er ist nicht
technisch fixed, verified oder closed.

## Verlauf

- 2026-07-19 — local_patch_rank_input_omission_reproduced: Der Codex-Security-
  Helper endete gegen Basis 504c8f164d4dab4bc857718af0233557ad48f727 mit
  Exit-Code 0 und null Zeilen, während der Framework-PR-#30-Task-Worktree
  vierzehn gestagte ACMR-Dateien hielt. Statische EXCLUDED_DIRS-Einträge für ci
  und tests verursachten die Auslassung.
- 2026-07-19 — manual_exact_inventory_recovery_completed: Die exakte sortierte
  Staged-Git-Inventur wurde mit jeweils vierzehn Zeilen in rank_input.jsonl und
  deep_review_input.jsonl wiederhergestellt. Der aktuelle PR-#30-Scan hat
  daher keinen ungeprüften Staged-Code, während die externe Tool-Remediation
  außerhalb des Scopes bleibt.
- 2026-07-26T18:48:26Z — current_user_local_archive_risk_accepted: Der aktuelle
  Nutzer akzeptierte das ungelöste Restrisiko des externen Helpers für ein
  lokales test-only Archiv. Produktions-, Release- und technische
  Closure-Claims bleiben untersagt, bis Helper und Coverage-Regression
  unabhängig repariert und verifiziert sind.
