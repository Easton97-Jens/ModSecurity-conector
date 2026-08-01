# FND-CROSS-0007 — Parent- und Framework-Task-Delivery band das effektive Origin-Push-Ziel nicht an das erwartete Benutzer-Repository

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-CROSS-0007` |
| Kategorie | `security_hardening` |
| Repository | `parent_and_framework` |
| Ownership | `cross_repository` |
| Priorität | `P2` |
| Schweregrad | `low` |
| Konfidenz | `validated` |
| Status | `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-Relevanz | `true` |

## Zusammenfassung und Verhalten

Der normale Parent- und Framework-Task-Branch-Delivery-Pfad zeigte die
Remote-Konfiguration an, verlangte aber vor Branch-Erstellung, Push, PR oder
Remote-Löschung nicht sowohl Origin-Fetch- als auch effektive Push-URL,
erwartete GitHub-Identität, Schreibberechtigung, Archivstatus und
Default-Branch. Ein abweichendes `origin.pushurl` konnte damit einen reinen
Anzeige-Preflight umgehen.

Der Governance-Scan fand vor `git push -u origin` und PR-Erstellung reine
`git remote`-Anzeige-Evidence ohne Invariante für das effektive Push-Ziel zum
erwarteten `Easton97-Jens`-Repository. Ein lokaler Bedienfehler oder eine
bösartige Git-Konfiguration könnte Task-Branch-Delivery/-Löschung umleiten.
Kein angreiferkontrollierter Delivery-Sink oder ausgehender Missbrauch wurde
nachgewiesen; dies ist Low-Severity-Governance-Hardening, kein Runtime-Exploit.

## Erwartetes Verhalten und Scope

Vor jeder Delivery-Branch-Erstellung, jedem Push, jeder PR-Aktion oder
Remote-Branch-Löschung prüft das besitzende Repository Origin-Fetch- und
effektive Push-URL, GitHub-Identität, nicht archivierten beschreibbaren Status
und Default-Branch gegen das exakte erwartete Benutzer-Repository. Jede
Abweichung endet als `blocked_remote_mismatch`.

Betroffen sind `AGENTS.md`, `.codex/context/git-policy.md`,
`.codex/context/fork-and-upstream-policy.md`,
`.codex/context/delivery-and-ci-policy.md` und die entsprechenden Framework-
Pfade unter `modules/ModSecurity-test-Framework/`. Betroffene Kontrollen sind
Parent-/Framework-Delivery-Destination-Preflight, effektive Origin-Push-URL
und `blocked_remote_mismatch`.

## Voraussetzungen und Reproduktion

Die Lücke setzt eine autorisierte Parent-/Framework-Delivery-Aktion und eine
vom erwarteten Repository abweichende Origin-Fetch-URL,
`origin.pushurl`/effektive Push-URL oder GitHub-Identität voraus, wenn die
Aufgabe nur Anzeige-Evidence verwendet. Den aufbewahrten Scan-Report und die
Pre-Fix-Policies prüfen, dann die fokussierten Audits und das Framework-
Negative-Fixture ausführen. Keine Remote-Konfiguration ändern und keinen
ausgehenden/bösartigen Push zur Demonstration durchführen.

## Evidence

- Run-ID: `20260724T170026Z-worktree-cleanup-governance`
  - Pfad: `/var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-conector/30ee953b_20260724T170026Z-worktree-cleanup-governance/report.md`
  - Typ: `scoped_governance_security_scan_final_report`
  - SHA-256: `83f0006b91b2831ce0b8067c07e3af13b7be55fb82af957bdd2eba6465c5d914`
  - Befehl: RTK-wrapped scoped Codex Security review of the 35 governance paths; final report and deterministic work ledger
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector`; Exit-Code: `0`
  - Beobachtet: `2026-07-24T17:00:26Z`; Aufbewahrung: `external_retained_task_evidence`

Das Review änderte absichtlich weder `origin.pushurl` noch führte es einen
Push aus oder behauptete Runtime-Enforcement. Es belegt nur frühere Policy-
Auslassung und aktuelle lokale Policy-/Audit-Remediation.

## Grundursache und Remediation

Die Parent-Policy bezeichnete ihre Git-Autorität falsch und verwies auf
fehlende Routen; Parent- und Framework-Delivery behandelten Remote-Anzeige als
ausreichende Evidence. Die Remediation ergänzt repository-lokale Fork-and-
Upstream-Policies mit akzeptierten HTTPS/SSH-URLs, effektiver Push-URL sowie
GitHub-Identitäts-/Berechtigungs-/Default-Branch-Preflight, routet AGENTS/Git/
Delivery/Restoration darüber und verlangt bei jeder Abweichung
`blocked_remote_mismatch`. Sie bewahrt normale Task-Branch-Origin-Delivery und
verbietet Upstream-Delivery/-Löschung.

## Akzeptanz und Validierung

- Parent- und Framework-Anweisungen verlangen exakte Origin-Fetch-/effektive
  Push-URLs sowie GitHub-Readback vor Delivery-Branch, Push, PR-Aktion oder
  Remote-Löschung.
- Abweichungen werden ohne Remote-Umschreibung, Fallback-Push, PR-Erstellung
  oder Remote-Löschung blockiert.
- MRTS behält die `Easton97-Jens/MRTS`-Origin-only-Regel; keine Policy erlaubt
  Upstream-Push/-Löschung oder Gitlink-Update.
- Parent- und Framework-lokale Policy-Audits und fokussierte Tests bestehen.

Parent-Audit `all` und 57 fokussierte Audit-Tests bestanden. Framework-Audit
und 22 fokussierte Audit-Tests bestanden, einschließlich des
`git-policy.md`-Abschwächungs-Fixtures. Regressionstests sind Parent
`.codex/tests/test_audit_policies.py`, Framework
`.codex/tests/test_audit_policies.py::test_git_policy_weakening_is_not_omitted_from_audit`
und Framework
`.codex/tests/test_audit_policies.py::test_missing_git_policy_is_missing_delivery_coverage`.

Legitime Controls zeigten erwartete Parent-, Framework- und MRTS-Origin-Fetch-
/effektive-Push-URLs und ein gültiges Framework-Fixture, das konsistent bleibt,
während eine Direct-Master-Abschwächung erkannt wird.

## Abhängigkeiten, Restrisiko und Historie

Abhängigkeiten und Blocker: keine. Verbundenes Finding:
`FND-FRAMEWORK-0055`. Die Policies/Audits sind Governance-Kontrollen, keine
Host-seitigen Interceptoren. Eine künftige autorisierte Delivery muss
Live-Remote-/GitHub-Readback aufbewahren; hier erfolgten weder Remote-
Umschreibung noch Upstream- oder Default-Branch-Push.

- `2026-07-24T17:00:26Z` — `scoped_governance_scan_validated_control_gap`: Das deterministische 35-Pfad-Security-Review erfasste diese Low-Severity-Lücke.
- `2026-07-24T18:15:00Z` — `local_policy_remediation_and_audit_passed`: Parent-/Framework-Kontrollen wurden aktualisiert; Audits/Tests bestanden ohne Remote-Statusänderung.

Finale Disposition: `fixed_local_governance_controls_pending_future_live_delivery_proof`.
