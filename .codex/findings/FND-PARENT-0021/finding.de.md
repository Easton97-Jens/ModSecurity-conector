# FND-PARENT-0021 — Storage-Budget-Finalisierung kann task-eigene Validierungs- und Build-Artefakte nicht bereinigen

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | FND-PARENT-0021 |
| Titel / Title | Storage-Budget-Finalisierung kann task-eigene Validierungs- und Build-Artefakte nicht bereinigen |
| Kategorie / Category | storage_cleanup |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priorität / Priority | P2 |
| Schweregrad / Severity | not_applicable |
| Konfidenz / Confidence | reproduced |
| Status | blocked |
| Machbarkeitsstatus / Feasibility status | out_of_scope |
| Release-Blocker / Release blocker | false |
| Security-Relevanz / Security relevance | false |

## Zusammenfassung / Summary

Aktuelle Integrations-Runs können durch den repository-lokalen
Storage-Budget-Helper nicht versiegelt werden. Er scheitert korrekt geschlossen,
statt Daten zu löschen: validation-tmp kann nicht rekursiv registriert werden,
erzeugte Engine-Binaries und der Go-Cache sind für eine automatische Bereinigung
nicht privat genug, und ein task-eigener Framework-Source-Worktree enthält einen
getrackten Symlink, dem die rekursive Bereinigung nicht folgen darf. Die
task-eigene Evidence bleibt aufbewahrt; es gab keine automatische oder manuelle
Löschung.

## Beobachtetes Verhalten / Observed behavior

Nachdem die Evidence-Prüfsumme aktualisiert und die fünf Build-Verzeichnisse
als rekursive temporäre Pfade neu registriert waren, hatte ein Dry-Run null
geplante Löschungen. Er lehnte das nichtleere Verzeichnis validation-tmp ohne
rekursive Registrierung ab und lehnte build/engine-service/traefik-engine-service,
build/engine-service-clang/traefik-engine-service und
build/native-middleware/gocache ab, weil ihre Berechtigungen nicht privat genug
waren.

Am 2026-07-20 machte die PR-#34-Aufgabe ihren registrierten Framework-Worktree
privat und führte die Finalisierung erneut aus. Der Helper lehnte daraufhin
ohne ihm zu folgen den getrackten Symlink
`tests/mrts/infra-overlays/nginx-pr24/infra/modules-enabled/mod-http-geoip2.conf`
ab und erzeugte keinen Löschplan.

## Erwartetes Verhalten / Expected behavior

Der Helper muss für nicht vertrauenswürdige oder nicht private Pfade weiterhin
geschlossen scheitern. Eine separat autorisierte Storage-Control-Plane-Änderung
darf die dokumentierten task-eigenen Validierungs- und Build-Outputs nur mit
einer exakten rekursiven Pfad-Policy, privaten Artefaktberechtigungen,
erhaltener Evidence-Integrität sowie unveränderten No-Symlink-,
No-Foreign-Process- und Root-Containment-Controls für eine sichere
Finalisierung zulassen.

## Auswirkung / Impact

Die Task-Runs bleiben aktiv statt finalisiert und ihre registrierten temporären
Artefakte bleiben auf dem Datenträger. Der aktuelle PR-#34-Run liegt bei 8,429
GiB mit 54,245 GiB frei und erfüllt das 15-GiB-Finalziel; daher sind weder
Fremdbereinigung noch Lösch-Bypass gerechtfertigt. Dies ist eine lokale
Tooling-/Cleanup-Grenze, kein Produkt- oder Sicherheitskontrollfehler.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- .codex/bin/storage-budget
- .codex/context/storage-policy.md

### Symbole / Symbols

- command_register
- RECURSIVE_DIRECTORY_NAMES
- removal_plan_no_follow
- assert_private_owned

## Voraussetzungen / Preconditions

- Ein privater aktueller Task-Run enthält validation-tmp und Build-Artefakte,
  die durch die autorisierten Validierungskommandos angelegt wurden.
- Das aktive Manifest registriert validation-tmp als nicht rekursives
  temporäres Verzeichnis und die dokumentierten Build-Verzeichnisse als
  rekursive temporäre Pfade.
- Der Storage-Budget-Helper erzwingt seine Allowlist für rekursive
  Verzeichnisse und Private-Ownership-Checks.
- Ein registrierter task-eigener Framework-Source-Worktree kann einen
  getrackten Symlink enthalten, dem der Helper bei der rekursiven Bereinigung
  nicht folgen darf.

## Reproduktion / Reproduction

1. Das aufbewahrte Evidence-Verzeichnis nach allen Evidence-Schreibvorgängen
   registrieren.
2. Die fünf dokumentierten Build-Roots als rekursive temporäre Pfade
   registrieren und validation-tmp als normalen temporären Pfad registriert
   lassen.
3. Ausführen:
   rtk run '/root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260718T053406Z-pr-51-master-integration-546d9dc2 --dry-run --json'
4. Null geplante Löschungen sowie die fail-closed Fehler für validation-tmp und
   private Berechtigungen beobachten.
5. Für den privaten registrierten Framework-PR-#34-Worktree ausführen:
   rtk proxy /root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260720T042405Z-framework-pr-34-master-integration-31a1528d --dry-run --json
6. Exit 2, null geplante Löschungen und die fail-closed Ablehnung von
   `tests/mrts/infra-overlays/nginx-pr24/infra/modules-enabled/mod-http-geoip2.conf`
   als Symlink beobachten.

## Evidence / Evidence

- Run-ID: 20260718T053406Z-pr-51-master-integration-546d9dc2
  - Artefakt:
    /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/storage-finalization-fail-closed.md
  - Typ: storage_finalization_fail_closed_record; SHA-256:
    146abee82f088548838293ceb760e7d919611cc39f9549832e7b400e61032719
  - Kommando:
    rtk run '/root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260718T053406Z-pr-51-master-integration-546d9dc2 --dry-run --json'
  - Arbeitsverzeichnis: /root/git/ModSecurity-conector; Exit-Code: 2
  - Beobachtet am: 2026-07-18T07:05:32Z; Aufbewahrung:
    retained_task_evidence
- Run-ID: 20260720T042405Z-framework-pr-34-master-integration-31a1528d
  - Artefakt:
    /var/tmp/codex/ModSecurity-conector/runs/20260720T042405Z-framework-pr-34-master-integration-31a1528d/evidence/storage-finalization-fail-closed.md
  - Typ: storage_finalization_fail_closed_record; SHA-256:
    d71163521ee4d7d01fce2fe728bee6b5bfa1a44ec1c7facf66c89f40e643d100
  - Kommando:
    rtk proxy /root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260720T042405Z-framework-pr-34-master-integration-31a1528d --dry-run --json
  - Arbeitsverzeichnis: /root/git/ModSecurity-conector; Exit-Code: 2
  - Beobachtet am: 2026-07-20T05:05:00Z; Aufbewahrung:
    retained_task_evidence

## Grundursachenanalyse / Root-cause analysis

Die Allowlist des Cleanup-Helpers für rekursive Registrierung schließt
validation-tmp aus, und seine Private-Ownership-Sicherung lehnt mit nicht
privaten Berechtigungen erzeugte Build-Outputs ab. Separat lehnt seine
No-Symlink-Sicherung korrekt einen getrackten Symlink innerhalb eines
task-eigenen Framework-Source-Worktrees ab. Beide Schutzmechanismen funktionieren
wie vorgesehen, aber ihre kombinierte Policy unterstützt die Finalisierung
dieser ansonsten task-eigenen Layouts nicht.

## Vorgeschlagene Remediation / Proposed remediation

In einer separaten ausdrücklich autorisierten Control-Plane-Aufgabe bestimmen,
ob validation-tmp zu einer sicheren rekursiven temporären Klasse gehört,
sicherstellen, dass betroffene Test-/Build-Outputs mit für den Helper
akzeptablen privaten Berechtigungen erzeugt werden, und eine unterstützte
Retained-Disposition für Source-Worktrees mit getrackten Symlinks definieren.
Fokussierte Storage-Budget-Regressions- und legitime Kontrolltests ergänzen.
Evidence-Prüfsummen, Descriptor-Anchoring, Symlink-/Spezialdatei-Refusal,
Prozess- und Mount-Checks oder die Dry-Run/Apply-Trennung nicht abschwächen.

## Akzeptanzkriterien / Acceptance criteria

- Ein Dry-Run für einen repräsentativen privaten Task-Run liefert einen exakten
  sicheren Plan für alle beabsichtigten task-eigenen temporären Pfade oder
  erläutert eine unterstützte Retained-Disposition.
- Die zugehörige Apply-Operation finalisiert das Manifest erst, nachdem
  derselbe Plan alle No-Symlink-, No-Foreign-Process-, Ownership-, Mount- und
  Evidence-Integrity-Checks bestanden hat.
- Kein Parent-, Framework-, MRTS-, Retained-Evidence-, Shared-Cache- oder
  fremder Task-Pfad ist für Löschung berechtigt.
- Das bestehende fail-closed Verhalten bleibt für nicht private, verlinkte,
  spezielle, gemountete, von fremden Prozessen gehaltene und Out-of-Run-Pfade
  abgedeckt.
- Ein task-eigener Source-Worktree mit getrackten Symlinks hat entweder eine
  verifizierte sichere Retained-Disposition oder einen separat autorisierten,
  gleichwertig sicheren Bereinigungspfad; der Helper folgt dem Symlink nie.

## Validierungsplan / Validation plan

- Einen isolierten privaten Test-Run mit den dokumentierten Validierungs- und
  Build-Formen anlegen.
- Den Storage-Budget-Dry-Run ausführen und jeden geplanten Löschpfad vor Apply
  untersuchen.
- Apply erst ausführen, nachdem der Plan sicher ist, ein finalisiertes
  Manifest, die Prüfsumme der aufbewahrten Evidence und die Abwesenheit nur der
  erlaubten temporären Pfade verifizieren.
- Die fokussierte Storage-Budget-Test-Suite sowie negative Controls für nicht
  private und fremde Pfade erneut ausführen.

## Regressionstests / Regression tests

- .codex/tests/test_storage_budget.py
- Ein fokussierter Test für die rekursive validation-tmp-Policy und für
  Helper-akzeptable Berechtigungen task-eigener Build-Artefakte.

## Legitime Kontrolltests / Legitimate control tests

- Ein normaler privater task-eigener Validierungs-/Build-Run finalisiert nur
  seine registrierten temporären Pfade, während seine Evidence intakt bleibt.
- Nicht private, verlinkte, spezielle, gemountete, von fremden Prozessen
  gehaltene und Out-of-Run-Pfade scheitern weiterhin geschlossen.

## Abhängigkeiten / Dependencies

- Ausdrückliche Benutzerautorisierung für eine lokale
  Storage-Control-Plane-Änderung.

## Blocker / Blockers

- Die aktuelle PR-#51-Integrationsaufgabe autorisiert keine Änderungen an
  .codex/bin/storage-budget oder storage-policy.md.
- Die aktuelle Framework-PR-#34-Integrationsaufgabe autorisiert keine Änderungen
  an .codex/bin/storage-budget oder storage-policy.md.

## Verwandte Findings / Related findings

- FND-HOST-0001
- FND-PARENT-0014

## Restrisiko / Residual risk

Die Task-Runs sind nicht versiegelt und ihre temporären Artefakte bleiben
erhalten, aber es fand keine unsichere Löschung statt. Evidence ist aufbewahrt
und das finale Speicherziel ist erfüllt. Es gibt keine Risikoakzeptanz.

## Historie / History

- 2026-07-18T07:05:32Z: current_task_storage_finalization_blocked_fail_closed —
  Die Dry-Run-Finalisierung dokumentierte null geplante Löschungen und lehnte
  das nichtleere nicht rekursive Verzeichnis validation-tmp sowie drei nicht
  private erzeugte Build-/Cache-Pfade ab. Es gab kein --apply und keine
  manuelle Löschung.
- 2026-07-20T05:05:00Z:
  framework_pr34_worktree_storage_finalization_blocked_fail_closed — Nachdem
  der registrierte private Framework-PR-#34-Worktree den Ownership-Check
  bestanden hatte, lehnte die Dry-Run-Finalisierung seinen getrackten
  mod-http-geoip2.conf-Symlink ohne ihm zu folgen ab. Es gab kein --apply,
  keine manuelle rekursive Löschung und keine direkte Worktree-Entfernung.
