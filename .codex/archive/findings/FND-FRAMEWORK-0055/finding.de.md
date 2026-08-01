# FND-FRAMEWORK-0055 — Framework-Policy-Auditor konnte die aktive Git-Policy auslassen und trotzdem breite Control-Plane-Coverage melden

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0055` |
| Kategorie | `security_hardening` |
| Repository | `framework` |
| Ownership | `framework` |
| Priorität | `P2` |
| Schweregrad | `low` |
| Konfidenz | `verified` |
| Status | `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-Relevanz | `true` |

## Zusammenfassung und Verhalten

Der lokale Framework-Policy-Auditor bildete seine Lesemenge aus `DOMAIN_SPECS`, enthielt aber die aktive `git-policy.md` nicht. Eine Direct-Master-Push-Abschwächung ausschließlich dort konnte aus dem `all_text`-Forbidden-Language-Scan ausfallen, während das Audit breite Coverage meldete.

Das Security-Review bestätigte, dass `DOMAIN_SPECS` `git-policy.md` ausließ; die Forbidden-Weakening-Schleife las diese Git-Autorität daher nicht. Eine lokale Governance-Änderung konnte Git-Safety abschwächen und irreführende Audit-Evidence erzeugen. Kein automatisierter Delivery-Sink verbrauchte das Audit-Ergebnis; dies ist Low-Severity-Control-Coverage-Hardening, kein nachgewiesener Exploit.

## Erwartetes Verhalten und Scope

Ein Framework-Policy-Audit mit Delivery-/Git-Safety-Coverage muss die aktive `git-policy.md` lesen und dort verbotene Abschwächung zurückweisen, während seine ausschließlich strukturelle Beweisgrenze erhalten bleibt.

Betroffene Dateien: `modules/ModSecurity-test-Framework/.codex/bin/audit-policies`, `modules/ModSecurity-test-Framework/.codex/tests/test_audit_policies.py` und `modules/ModSecurity-test-Framework/.codex/context/git-policy.md`. Betroffene Symbole: `DOMAIN_SPECS.delivery`, `FORBIDDEN_PATTERNS` und `test_git_policy_weakening_is_not_omitted_from_audit`.

## Voraussetzungen und Reproduktion

Voraussetzung ist eine Framework-Control-Plane-Änderung, die `git-policy.md` mit verbotener Git-Abschwächung verändert, während eine Aufgabe auf das alte Audit-Konsistenzergebnis vertraut. Den aufbewahrten Scan-Report und das Pre-Fix-Inventar prüfen. Das neue Fixture führt `Direct push to master is permitted.` nur in `git-policy.md` ein und muss `forbidden_weakening_language` als conflicting liefern. Das normale Framework-Audit muss die gültige Control Plane weiterhin als consistent melden.

## Evidence

- Run-ID: `20260724T170026Z-worktree-cleanup-governance`
  - Pfad: `/var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-conector/30ee953b_20260724T170026Z-worktree-cleanup-governance/report.md`
  - Typ: `scoped_governance_security_scan_final_report`
  - SHA-256: `83f0006b91b2831ce0b8067c07e3af13b7be55fb82af957bdd2eba6465c5d914`
  - Befehl: RTK-wrapped scoped Codex Security review of Framework audit source, policy authority, and focused test coverage
  - Arbeitsverzeichnis: `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework`
  - Exit-Code: `0`; beobachtet: `2026-07-24T17:00:26Z`; Aufbewahrung: `external_retained_task_evidence`

Das Audit ist absichtlich ein lokales strukturelles Konsistenzwerkzeug. Sein Pass-Ergebnis beweist weder Runtime-Git, GitHub, Access-Control noch Sandbox-Enforcement.

## Grundursache und Remediation

Die Delivery-Domain führte `delivery-and-ci-policy.md`, aber nicht `git-policy.md` auf; ihr Forbidden-Pattern-Scan untersuchte nur Text aus deklarierten Domains.

Die lokale Remediation nimmt `git-policy.md` und `fork-and-upstream-policy.md` in das Delivery-Dateiinventar auf und ergänzt Fixtures, die Direct-Master-Push-Abschwächung erkennen und bei fehlender `git-policy.md` Delivery-Coverage als missing melden.

## Akzeptanz und Validierung

- `DOMAIN_SPECS` liest `git-policy.md` als Delivery-Coverage.
- Ein verbotener Direct-Master-Push-Satz erzeugt dort conflicting `forbidden_weakening_language`.
- Das Entfernen der Datei erzeugt missing Delivery-Coverage.
- Normales Framework-Audit und fokussierte Tests bestehen ohne Abschwächung der strukturellen Scope-Aussage.

Abgeschlossene Validierung: Framework-Audit bestand mit allen Domains covered; 22 fokussierte Tests bestanden, einschließlich `test_git_policy_weakening_is_not_omitted_from_audit` und `test_missing_git_policy_is_missing_delivery_coverage`. Legitime Controls waren das vollständige gültige Fixture und das normale Framework-Control-Plane-Audit.

## Abhängigkeiten, Restrisiko und Historie

Abhängigkeiten und Blocker: keine. Verbundenes Finding: `FND-CROSS-0007`. Das Audit liest nun die aktive Git-Autorität, bleibt aber eine textuelle Konsistenzprüfung; eine künftige Aufgabe braucht weiterhin reale Worktree-, Remote-, PR- und Gitlink-Evidence vor Delivery/Löschung.

- `2026-07-24T17:00:26Z` — `scoped_governance_scan_validated_audit_omission`: Das deterministische Review erfasste diese Audit-Auslassung.
- `2026-07-24T18:15:00Z` — `audit_inventory_and_negative_regressions_added`: Die Delivery-Domain liest Git-/Fork-Policy; neue Negative-Fixtures und normales Audit bestanden.

Finale Disposition: `fixed_local_audit_coverage_pending_future_delivery_context`.
