# FND-CROSS-0006 — Framework-autoritärer Phase-4-Checker bindet promotete Events nicht an die ausgewählte Workload-Identität

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-CROSS-0006 |
| Titel / Title | Framework-autoritärer Phase-4-Checker bindet promotete Events nicht an die ausgewählte Workload-Identität |
| Kategorie / Category | security_validated |
| Repository / Repository | parent_and_framework |
| Ownership / Ownership | framework |
| Priorität / Priority | P1 |
| Schweregrad / Severity | high |
| Konfidenz / Confidence | verified |
| Status | verified |
| Machbarkeitsstatus / Feasibility status | already_fixed |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | true |

## Zusammenfassung / Summary

Framework-PR #34 bindet die autoritative strikte Phase-4-Promotion an die
Workload-Identität von ausgewähltem Resultat, Manifest, PASS-Record und Event.
Der ursprüngliche Reproducer für fremde oder fehlende Identität schlägt auf
Framework-master nun fail-closed fehl.

## Beobachtetes Verhalten / Observed behavior

Auf Framework-Revision cdc91a398d6c156eaff927d742b23018a3817fb6 akzeptiert
der strikte Checker ein Phase-4-Rule-1100301-Event anhand von Phase, Rule und
First-Byte-Metadaten ohne ausgewählte Run-, Connector-, Integrationsmodus- oder
Transaktionsidentität. Sein positives Fixture hat keine run_id und verwendet
integration_mode=unit-test-host-model.

## Erwartetes Verhalten / Expected behavior

Jedes autoritativ promotete Event muss mit seinem ausgewählten kanonischen
Resultat und Manifest nach Connector, Run-ID, ausgewähltem nativen Host/Profil
oder Integrationsmodus, Transaktion, Rule und Phase übereinstimmen. Fehlende
oder abweichende Felder schlagen geschlossen fehl.

## Auswirkung / Impact

Ein kopiertes oder vorab platziertes Event kann für die Framework-Komponente
eines strikten Gates akzeptabel bleiben, obwohl es keine Evidence des
ausgewählten Workloads ist. Parent-Consumer-Verdrahtung repariert diese
Framework-Grenze nicht.

## Betroffene Dateien und Symbole / Affected files and symbols

- modules/ModSecurity-test-Framework/ci/checks/evidence/check_full_lifecycle_evidence.py
- modules/ModSecurity-test-Framework/tests/no_crs/test_no_crs_baseline.py
- Makefile
- _matching_first_byte_event
- _strict_first_byte_errors
- first_byte_errors
- no_full_response_buffering_errors
- promotion_errors
- RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK
- Framework-Source-Commit: 428dfb2741785adabad7a6280882ea5251e00324

## Voraussetzungen / Preconditions

- Der Framework-Checker wird als autoritatives striktes Phase-4-Gate aufgerufen.
- Ein syntaktisch gültiges Event enthält erwartete Rule- und Kausalfelder, aber
  eine fremde oder fehlende Workload-Identität.

## Reproduktion / Reproduction

1. Die retained Security-Review und den Framework-Checker auf der aufgezeichneten
   Framework-Revision prüfen.
2. Vor einem Framework-Fix Fixtures für fremden Run, Connector,
   Profil/Integration, Transaktion und fehlende Identität ausführen.
3. Nach dem Fix die identitätskonsistente ausgewählte Native-Host-Kontrolle
   verifizieren.

## Evidence / Evidence

- Run-ID: 20260718T075200Z-parent-evidence-integrity-ade378cf
  - Fokussierte Security-Review:
    /var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/security_diff_review.md
  - Typ: focused_security_diff_review; SHA-256:
    3d5014e36faebffd46bcd83ed7ee59f8582d1ea9ec6e1b3dfe16e98444c6836e
  - Separater Framework-Task-Auftrag:
    /var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-CROSS-007-framework-phase4-authoritative-gate/framework_task_request.md
  - Typ: framework_task_request; SHA-256:
    ea1ff30c2a35514350b143f3b11b2befce60078886cdc468099d587ca11a63ef
- Run-ID: 20260720T042405Z-framework-pr-34-master-integration-31a1528d
  - Post-Merge-Receipt:
    /var/tmp/codex/ModSecurity-conector/runs/20260720T042405Z-framework-pr-34-master-integration-31a1528d/evidence/master-postmerge-verification.md
  - Typ: post_merge_framework_security_remediation_verification; SHA-256:
    7471054c232a5e2ad26c3327894535ff9d2245e3ec0f37ec60e077a57caea19a
  - Der exakte PR-#34-Head `4fc22651ab2da652cbcaa7026258506d79b9af9c` wurde
    normal als Framework-master
    `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` gemergt. PR-Checks und das
    SonarQube-Cloud-Quality-Gate bestanden; die vier fokussierten Phase-4-
    Tests für fremde/fehlende Identität und legitime Kontrolle bestanden erneut
    auf dem resultierenden master.

## Grundursachenanalyse / Root-cause analysis

Das Framework-Prädikat erhält oder leitet keine ausgewählte Resultatidentität
ab, und sein positiver Test verwendet ein unit-test-host-model-Event ohne
Run-ID.

## Vorgeschlagene Remediation / Proposed remediation

Durch Framework-PR #34 abgeschlossen: ausgewählte Identität aus Resultat und
Manifest ableiten, passende live-PASS-Record-Identität und gelieferte
Transaktionsidentität je promotiendem Claim verlangen und erst dann das Event
vor der First-Byte-Prüfung abgleichen. Der PR wurde normal ohne Parent- oder
MRTS-Änderung gemergt.

## Akzeptanzkriterien / Acceptance criteria

- Fremde/fehlende Run-, Connector-, Profil/Integrationsmodus- und
  Transaktionsidentität scheitert im Framework-autoritativen Checker.
- Resultat-, Event- und Manifestidentität sind ohne Filename/PASS-only-Logik
  gebunden.
- Eine ausgewählte Native-Host-Kontrolle besteht.
- Framework-Runtime-, Review-, CodeQL-, SonarQube-Cloud- und Exact-Head-
  Evidence wird zurückgehalten.

## Validierungsplan / Validation plan

- Abgeschlossen: Der exakte PR-#34-Head bestand fokussierte/vollständige
  Framework-Validierung, CodeQL, GitHub-Checks, Review-Inspektion und das
  SonarQube-Cloud-PR-Quality-Gate.
- Abgeschlossen: Der resultierende Framework-master
  `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` enthält den geprüften Head und
  führte die Foreign/Missing-Identity-Controls sowie die legitime Kontrolle
  erfolgreich erneut aus.
- Der unabhängige Default-Branch-SonarQube-Cloud-Backlog bleibt
  `FND-SONAR-0002`; er ist kein Beleg, dass dieses Finding weiter
  reproduzierbar ist.

## Regressionstests / Regression tests

- Framework-Full-Lifecycle-Evidence-Checker-Identity-Fixtures.
- Framework-No-CRS-Baseline-Native-Host-Kontrolle.

## Legitime Kontrolltests / Legitimate control tests

- Ausgewähltes Event, Resultat, Manifest, Connector, Run, Integrationsmodus und
  Transaktion stimmen überein.
- Native-Host-Evidence kann nicht durch unit-test-host-model-Metadaten ersetzt
  werden.

## Abhängigkeiten / Dependencies

- FND-PARENT-0027

## Blocker / Blockers

Keine für FND-CROSS-0006. Der separate Framework-master-SonarQube-Cloud-
Backlog wird weiter als FND-SONAR-0002 verfolgt.

## Verwandte Findings / Related findings

- FND-PARENT-0027
- FND-CROSS-0001
- FND-CROSS-0005
- FND-SONAR-0002

## Restrisiko / Residual risk

Auf Framework-master verbleibt kein beobachteter FND-CROSS-0006-Bypass. Das
fehlgeschlagene Default-Branch-SonarQube-Cloud-Gate ist der unabhängige
Multi-File-Backlog FND-SONAR-0002; er wird weder dieser Remediation zugeschrieben
noch für PR #34 stillschweigend risikoakzeptiert.

## Historie / History

- 2026-07-18T10:47:59Z: validated_framework_authoritative_gate_boundary —
  unabhängige Review identifizierte das ungebundene Framework-autoritative
  Prädikat; eine Parent-Consumer-Verdrahtungs-Remediation und ein separater
  Framework-Task-Auftrag wurden erstellt.
- 2026-07-20T04:52:04Z: verified_after_framework_pr_34_master_merge —
  Framework-PR #34 Head `4fc22651ab2da652cbcaa7026258506d79b9af9c` wurde
  normal als master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` gemergt.
  Exact-PR-Checks und SonarQube Cloud bestanden; die vier fokussierten
  Foreign/Missing-Identity- und legitimen Kontrolltests liefen erfolgreich
  erneut auf master. Der separate master-only FND-SONAR-0002-Gate-Fehler bleibt
  für diesen PR nicht waived und wird diesem Finding nicht zugeschrieben.
