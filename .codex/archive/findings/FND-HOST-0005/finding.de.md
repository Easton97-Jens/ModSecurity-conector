# FND-HOST-0005 — Historische gemeinsame temporäre-Root-Nutzung blockiert die Storage-Finalisierung für den GitHub-Code-Scanning-Dispositionsrun nicht mehr

## Identität

| Feld | Record |
| --- | --- |
| Kategorie | storage_cleanup |
| Repository / Ownership | host_environment / host_environment |
| Priorität / Severity / Confidence | P2 / not_applicable / confirmed |
| Lifecycle-Status | verified |
| Feasibility / Storage-Status | already_fixed / ok |
| Aktueller-Task-Status | verified_current_storage_target |
| Release-Blocker / Security-Relevanz | false / false |
| Verwandte Findings | FND-PARENT-0021, FND-PARENT-0022 |

## Zusammenfassung und beobachtetes Verhalten

Der historische Run 20260718T084215Z-github-code-scanning-disposition-14-15-babc842c überschritt das 15-GiB-Finalziel, ohne einen registrierten Cleanup-Pfad zu besitzen. Am 2026-07-26 meldete ein aktueller read-only storage-budget Check den Status ok bei 9,570 GiB. Die ursprüngliche Kapazitätsbedingung reproduziert daher nicht mehr.

Der historische Dry-Run endete bei 15,630 GiB mit Exit 2 und leerem Löschplan. Der task-eigene aktuelle Evidence-Run schloss Dry-Run und Apply-Finalisierung bei 9,572 GiB mit Status ok, leerem Plan und null gelöschten Pfaden ab. Es wurde kein gemeinsamer, fremder, Cache-, Evidence-, Framework-, MRTS-, Produkt- oder Gitlink-Pfad gelöscht.

## Erwartetes Verhalten und Controls

Die Storage-Finalisierung darf nur aktuelle, im Manifest registrierte und task-eigene temporäre Pfade entfernen, nachdem Fail-Closed-Checks bestanden sind. Gemeinsame, fremde, Cache-, retained-Evidence-, Framework-, MRTS-, Produkt- und Gitlink-Pfade dürfen niemals allein zur Erreichung eines Kapazitätsziels gelöscht werden.

Das historische Dispositionsrun-Manifest hat weiterhin keine registered_paths oder managed_paths. Es wurde nicht rückwirkend verändert. Der Helper behält seinen leeren Plan bei, statt Cleanup-Autorität auf gemeinsame Daten auszuweiten.

## Evidence und Reproduktion

- Historische Run-ID: 20260718T084215Z-github-code-scanning-disposition-14-15-babc842c
  - Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260718T084215Z-github-code-scanning-disposition-14-15-babc842c/evidence/storage-finalize-dry-run.md
  - SHA-256: 773148f2094aba5b2bb9ac51516a7caee7e682859fe46fe9d27cf953eb484855
  - Ergebnis: Dry-Run Exit 2, temporary_exceed, kein Löschplan.
- Aktuelle Revalidierungs-Run-ID: 20260726T171843Z-fnd-host-remediation-20260726-cf748da4
  - Artefakt: /var/tmp/codex/ModSecurity-conector/runs/20260726T171843Z-fnd-host-remediation-20260726-cf748da4/evidence/fnd-host-0001-0005-current-revalidation.md
  - SHA-256: eec6402faaa6981206613db5d9368f1298c7f4e0216fc8e21f2522de29f9e852
  - Aufgezeichnete Commands: storage-budget check --json; task-eigene Dry-Run- und Apply-Finalisierung.
  - Ergebnis: Check Exit 0 / Status ok bei 9,570 GiB; Finalisierung Exit 0 / Status ok bei 9,572 GiB; leerer Plan und null gelöschte Pfade.
- Die fokussierte Storage-Helper-Suite bestand alle 49 Tests, einschließlich Controls für Symlink, Spezialdatei, registered-only, retained-Evidence, Ownership, Mount und Foreign Process.

Nur mit einem read-only Check reproduzieren. Vor jeder künftigen Apply-Aktion ein task-eigenes Run-Manifest und den Dry-Run-Plan prüfen. Keine historischen Cleanup-Registrierungen hinzufügen und keine gemeinsamen Daten löschen.

## Grundursache, Remediation und Validierung

Die historische Kapazitätsbedingung entstand durch Shared-Root-Nutzung über dem Ziel, während der historische Run keinen Cleanup-Pfad besaß. Die aktuelle Root-Nutzung liegt unter dem Ziel; eine Parent-Quellcodeänderung ist nicht erforderlich.

Akzeptanz-Evidence:

1. Ein aktueller read-only Check liegt unter dem konfigurierten Finalziel.
2. Eine task-eigene Dry-Run- und Apply-Finalisierung hatten einen leeren Löschplan.
3. Retained Evidence sowie alle Parent-, Framework-, MRTS-, Shared-, Cache-, Produkt- und Gitlink-Pfade blieben unberührt.

Sicheres read-only Monitoring fortsetzen. Jedes künftige Cleanup bleibt eine separat autorisierte Host-/Storage-Owner-Aktion, begrenzt auf im Manifest registrierte task-eigene Pfade.

## Regression und legitime Controls

- Regression: .codex/tests/test_storage_budget.py bestand 49 Tests.
- Legitimer Control: Ein registrierter privater Task-Pfad kann nur geplant werden, wenn alle Fail-Closed-Checks bestanden sind.
- Negativer Control: Nicht registrierte gemeinsame, fremde, Cache-, Evidence-, Symlink-, Spezial-, Mount- oder von Foreign Processes gehaltene Pfade bleiben für automatisches Cleanup unzulässig.

## Abhängigkeiten, Blocker und Restrisiko

Es gibt keine aktive Kapazitätsabhängigkeit und keinen aktiven Blocker. Der historische Run bleibt absichtlich unverändert, weil er keine Cleanup-Registrierung besitzt. Künftiges Wachstum der Shared-Root-Nutzung muss überwacht werden; jedes ownership-bewusste Cleanup benötigt eine separate Autorisierung.

## Aktuelles nutzergerichtetes Archiv

Der aktuelle Nutzer ordnete das verlustfreie Archiv dieses nicht blockierenden
verified Storage-Capacity-Findings an. Sein Lifecycle bleibt `verified`; dies
ist weder ein neuer Abschluss noch eine Release-Freigabe oder Autorisierung zum
Cleanup gemeinsamer Daten. Wenn die Kapazitätsbedingung wieder materiell wird,
das vollständige Tripel wiederherstellen und die read-only Storage- sowie
sicheren Finalisierungs-Controls erneut ausführen.

Archiventscheidungs-Evidence: Run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, Artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.

## Historie

- 2026-07-18T09:43:15Z: als blocked_environment / temporary_exceed erfasst, nachdem ein retained Dry-Run keinen Löschplan zeigte.
- 2026-07-26T17:20:59Z: aktuelle Kapazitätsbedingung verifiziert. Die Root lag unter dem Ziel und die task-eigenen Finalisierungs-Controls endeten mit leerem Plan und null Löschungen. Status auf verified, nicht closed, geändert.
