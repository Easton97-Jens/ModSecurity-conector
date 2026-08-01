# FND-SONAR-0013 — Common-Runtime-CRS- und Direct-Output-Integritätskandidat

## Klassifikation

- **Kategorie:** `security_candidate` (`python:S5443` und `pythonsecurity:S8707`)
- **Repository / Ownership:** `parent` / `parent`
- **Priorität / Schwere / Confidence:** `P1` / `high` / `candidate`
- **Status / Verifikation:** `accepted_risk` / `current_source_already_safe_pending_hosted_per_rule_and_live_smoke_evidence`
- **Release-Blocker / Security-relevant:** ja / ja
- **Delivery-Status:** vollständiger geschützter Merge `7f72325cbd177e4bd98b3511a58344c04d41b06b` ist vom aktuellen Parent `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd` lokal erreichbar; Hosted-Per-Rule- und Live-Smoke-Receipts bleiben ausstehend.

## Zusammenfassung

Der lokale PR-#97-Snapshot zeigt einen lokalen Cross-User-
Konfigurationsintegritätskandidaten bei der Common-Runtime-CRS-Quellenauswahl,
generierter Konfigurations-/Audit-Ausgabe und direkten CLI-Ausgabepfaden.
`crs_source_candidate_roots()` konsultiert nicht mehr `RUNNER_TEMP`, `TMPDIR`,
`/tmp` oder `/var/tmp`; ausgewählte Bäume werden validiert, bevor sie
ModSecurity-`Include`-Input erzeugen können.

Der gleiche Diff validiert die sechs direkten Ausgabeziele `evidence_root`,
`results_dir`, `tmp_root`, `log_root`, `log_dir` und `config_root`, bevor
`run_smoke()` einen schreibfähigen Pfad fortsetzt. Der gepaarte Change Record
meldet 26 bestandene fokussierte lokale Tests. Parent-bereitgestellte Current-
Exact-Head-Evidenz für `b3860aac005a98244f5e880efc26a74449b11989` meldet
außerdem `compileall`, `--help`, erforderliche Checks und alle aktuellen
PR-Checks als bestanden; das SonarQube-Cloud-Quality-Gate ist `OK` und acht
aktuelle PR-Issues sind `CLOSED/FIXED`, einschließlich `pythonsecurity:S8707`
`AZ-PstOVmYfklgBeDadY`. Dies ist keine Verifikation eines geschützten Merges
oder resultierenden masters; die folgende Current-Local-Revalidierung ergänzt
einen Full-SHA-Ancestry-Nachweis und aufbewahrte Source-/Control-/Sink-Evidenz.

## Aktuelle lokale Revalidierung — 2026-07-26

`git merge-base --is-ancestor` bestätigt, dass der vollständige geschützte
Merge `7f72325cbd177e4bd98b3511a58344c04d41b06b` vom aktuellen Parent
`3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd` erreichbar ist. Aufbewahrte
Task-Evidenz führte alle 26 fokussierten CRS-/Output-Fälle, 6
Runtime-Path-Policy-Fälle, Syntax-Kompilierung, CLI-Hilfe und Whitespace-Review
erneut aus; der Source-/Control-/Sink-Review fand den einzelnen Production-
Entry-Point `main() -> run_smoke()` und keinen nicht validierten Production-
Caller der genannten Controls.

An der angegebenen Cross-User-POSIX-Owner-/Mode-Grenze ist der Kandidat
`already_safe`: Nur explizite CRS-Kandidaten werden akzeptiert, Source-/
Generation-Pfade sind vertrauenswürdig und symlinkfrei, und alle sechs
CLI-Output-Roots werden vor schreibfähigen Operationen validiert. Dies
beansprucht keinen Live-CRS-/libmodsecurity-/Connector-Smoke, keinen
Same-UID-Race- oder Filesystem-ACL-Nachweis und keine Hosted-Per-Rule-
SonarQube-Evidenz. Der aktuelle Nutzer wählte für diese verbleibenden
Evidenzlücken eine ausschließlich lokale Archiv-Disposition `accepted_risk`;
weder eine Source-Änderung noch eine PR ist erforderlich, und es wird kein
technischer Abschluss behauptet.

## Beobachtetes und erwartetes Verhalten

Der geprüfte exakte PR-Head ist `b3860aac005a98244f5e880efc26a74449b11989`
gegen lokale Basis `38752600e4823fc5a16f3e155047da2d660b9897`; der ursprüngliche
Feature-Commit ist `2fb994324c097a846ed6f6d93126cb8def391f0d`. Der Parent hat
die genannten Exact-Head-Lokal- und Hosted-Aggregatergebnisse bestätigt, aber
keinen geschützten Merge oder eine Validierung auf resultierendem master gemeldet.

Der Diff führt ausgewählte CRS-Quellverzeichnisse durch Prüfungen für Besitzer,
Modus, Symlink-Komponenten und Ancestor-Replacement. Er erzeugt generierte
CRS-Setup-, Rule-, Payload- und Audit-Dateien mit `O_NOFOLLOW` und exklusiver
Erstellung und validiert die generierte Rule vor der Evaluator-Nutzung erneut.
Direkte Output-Pfade müssen absolut, symlinkfrei und unter einer sicheren
`VERIFIED_RUN_ROOT` enthalten sein; abgewiesene Inputs müssen `SmokeBlocked` /
Exit `77` vor einem Runner-Write liefern.

Nur explizites `CRS_SOURCE_DIR` oder aus einer expliziten
`--runtime-lookup-root` abgeleitete Pfade dürfen CRS-Input werden. Eine gültige
vertrauenswürdige Quelle und ein gültiges enthaltenes Verified-Runtime-
Output-Layout müssen akzeptiert bleiben.

## Auswirkung und Scope

Wenn die direkte Pfadauswahl vor dem Follow-up erreichbar wäre, könnte ein
anderer lokaler Benutzer mit der Möglichkeit, einen gemeinsam genutzten
temporären Pfad oder unsicheres Output-Ziel vorzubereiten, Konfigurationsinput
oder den direkten Output-Ort beeinflussen. Die betroffene Grenze ist:

`CRS-/Output-CLI- oder Umgebungsselektion → Common Runtime Smoke → generierte Konfigurations-/Audit-Artefakte → lokaler Evaluator oder Result Writer`

Dies ist ein lokaler Konfigurations-/Dateiintegritätskandidat. Es belegt
**nicht** einen Remote-Request-zu-Parser-Pfad, beliebige CRS-Code-Ausführung,
einen Current-Master-Exploit oder einen erfolgreichen Runtime-Angriff.
Same-UID-Races und Filesystem-ACL-Semantik liegen außerhalb des angegebenen
POSIX-Owner-/Mode-Claims.

Betroffene Parent-Pfade und Symbole sind:

- `common/scripts/run_local_runtime_smoke.py` —
  `crs_source_candidate_roots`, `resolve_crs_source_dir`,
  `validate_crs_source_dir`, `prepare_crs_smoke_config`,
  `validate_runtime_output_paths`, `require_verified_runtime_output_path`,
  `secure_crs_output_file`, `write_trusted_crs_output` und `run_smoke`.
- `tests/test_common_runtime_smoke_crs_source_security.py`.
- Die gepaarten Variablen-Dokumentationen und Change-Record-Dateien aus dem
  JSON-Record.

## Reproduktion und Evidenz

Den lokalen PR-#97-Diff von Basis `38752600e4823fc5a16f3e155047da2d660b9897`
zu Snapshot `b3860aac005a98244f5e880efc26a74449b11989` prüfen. Danach ausführen:

```text
env PYTHONDONTWRITEBYTECODE=1 python -m unittest -v tests.test_common_runtime_smoke_crs_source_security
```

Der gepaarte Change Record meldet 26 bestandene fokussierte Fälle, einschließlich
Ambient-CRS-Kandidaten, unsicherer Source-/Generated-Output-Varianten, aller
sechs direkten Output-Roots, relativer und breiter Verified-Roots,
Symlink-Escapes/-Loops, eines vorhandenen CRS-Suffix-Symlinks und Legitimate
Controls. Diese begrenzte Record-Aufgabe führte die Tests nicht erneut aus und
bewahrte keinen Raw-Test-Log auf.

Evidenzquelle: `/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/worktrees/pr55/reports/audits/change-records/CR-20260723-sonar-common-crs-source-integrity.md`, SHA-256
`d07f3fb43265c7acfad64934c0b73c859ac3c30a048fff0b7e6064a0e334a8c9`,
Run `20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b`,
beobachtet mit `git diff --name-status`, `git diff --check` und `sha256sum`
am `2026-07-24T07:58:00Z`, Exit `0`. Das deutsche Paar hat SHA-256
`e7b9461f09f84cb43b8f736806743d0d83b7ea028507e25b88666f4c22182e24`.
Beide sind volatile Worktree-Quellen, keine versiegelten Execution-Receipts.
Die Parent-bereitgestellte Exact-Head-Hosted-Zusammenfassung hat in dieser
begrenzten Record-Aufgabe keinen angegebenen Raw-Receipt-Pfad oder vollständige
Per-Key-Response.

Die historischen Regelreferenzen sind `AZ70UrU3IhrooTjfZnAX`,
`AZ70UrU3IhrooTjfZnAY`, `AZ70UrU3IhrooTjfZnAZ` (`python:S5443`) und
`AZ-PstOVmYfklgBeDadY` (`pythonsecurity:S8707`). Die bereitgestellte Exact-
Head-Zusammenfassung identifiziert den S8707-Key ausdrücklich als
`CLOSED/FIXED` und meldet das aggregierte Acht-Issue-Set als `CLOSED/FIXED`;
sie enthält keine aufbewahrte Raw-Per-Key-Zuordnung für jede historische
S5443-Referenz.

## Grundursache und vorgeschlagene Remediation

Vor dem geprüften Diff konnten Ambient-Temporary-Roots CRS-Kandidaten werden,
und ausgewählte/generierte Pfade hatten keine dokumentierte End-to-End-Grenze
für vertrauenswürdige Quelle, Symlinkfreiheit, Provenance und verifizierte
Output-Root.

Die PR-#97-Controls eng beibehalten: nur explizite Quellkandidaten akzeptieren,
ausgewählte Quellen und generierte Output-Komponenten validieren, No-Follow und
exklusive Erstellung verwenden, die Rule vor Evaluator-Nutzung erneut
validieren und alle sechs direkten CLI-Output-Roots vor der ersten schreibfähigen
Aktion validieren. Gültige explizite Quellen und Verified-Root-Controls bewahren.
Keine Sonar-Suppression, Exclusion, Regel-/Profil- oder Quality-Gate-Änderung,
False-Positive-Disposition oder Risikoakzeptanz darf technische Evidenz ersetzen.

## Akzeptanzkriterien und Validierungsplan

1. Der aktuelle exakte PR-#97-Head weist unsichere CRS-Source-/Generated-
   Output-Inputs vor der Evaluator-Rule-File-Nutzung zurück und hat keinen
   Ambient-Shared-Temporary-Source-Fallback.
2. Die sechs direkten Output-Pfade sind absolut, kanonisiert, symlinkfrei und
   unter einer sicheren `VERIFIED_RUN_ROOT` enthalten, bevor der Runner eine
   Filesystem-Operation ausführt; abgewiesener Input liefert Exit `77` ohne
   Runner-Write.
3. Legitime vertrauenswürdige Quellen und enthaltene Verified-Runtime-Output-
   Layouts bleiben über dieselbe Production-Grenze akzeptiert.
4. Fokussierte Suite, Syntax-/Help-Checks, exakter Diff-Review und
   Source-to-Sink-/Alternate-Bypass-Review bestehen für den exakten Head.
5. Der bestätigte exakte Head behält Quality Gate `OK` und das aktuelle PR-
   Issue-Set `CLOSED/FIXED` ohne Änderung von Sonar-Controls; jeder spätere
   Head benötigt frische Evidenz.
6. Ein echter CRS-/libmodsecurity-Smoke läuft nur bei dokumentierten
   Voraussetzungen; andernfalls bleibt er explizit `not_run` oder `blocked`.

Die Validierungsreihenfolge ist: Raw-Exact-Head-Test-/Hosted-Receipt bei
Verfügbarkeit aufbewahren; ihn nach jedem Head-Wechsel wiederholen; direkte
Caller und Overrides prüfen; den echten Smoke nur bei vorhandenen
Voraussetzungen ausführen; dann nach geschütztem Merge resultierenden-Master-
SHA, ursprüngliche Legitimate Controls und anwendbare Master-Checks prüfen,
bevor dieser Befund als verified markiert wird.

## Abhängigkeiten, Blocker und Restrisiko

Abhängigkeiten sind ein aktueller exakter PR-#97-Head, eine Parent-Python-
Umgebung, Read-Access zu GitHub und SonarQube Cloud für Exact-Head-Verifikation
und optionale lokale libmodsecurity-/CRS-/Host-Komponenten für einen echten
Smoke.

Verbleibende Blocker sind das Fehlen eines aufbewahrten Raw-Per-Key-Receipts
für jede historische S5443-Referenz und das Fehlen eines echten Evaluator-/
Host-Connector-Smokes in dieser begrenzten Aufgabe. Full-SHA-Reachability des
geschützten Merges und der aktuelle fokussierte Source-/Control-/Sink-Rerun
sind jetzt lokal aufbewahrt. Der aktuelle Nutzer akzeptiert diese Lücken nur
für das lokale Archiv; keine Entscheidung für Produktion, Veröffentlichung,
Release oder technischen Abschluss ist autorisiert. Verwandter Befund:
`FND-SONAR-0014`.

## Verlauf

- `2026-07-24T07:58:00Z`: Aus dem lokalen PR-#97-Diff und gepaartem Change
  Record als `in_progress` / `unverified` Kandidat angelegt. Die 26-Fälle-
  Local-Test-Aussage ist mit ihrer Grenze festgehalten; Hosted- und Merge-
  Ergebnisse werden bewusst nicht behauptet.
- `2026-07-24T08:04:28Z`: Parent bestätigte exakten Head `b3860aac005a98244f5e880efc26a74449b11989`; 26 fokussierte Tests, `compileall`, `--help`, erforderliche/aktuelle PR-Checks bestanden, Quality Gate war `OK` und acht aktuelle PR-Issues waren `CLOSED/FIXED`, einschließlich S8707-Key `AZ-PstOVmYfklgBeDadY`. PR #97 bleibt ungemergt.
- `2026-07-26T17:18:12Z`: Local Git bestätigt, dass der vollständige Merge
  `7f72325cbd177e4bd98b3511a58344c04d41b06b` ein Ancestor des aktuellen Parent
  `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd` ist. Der aufbewahrte Task-Report
  enthält 26 fokussierte CRS-/Output-Tests, 6 Runtime-Path-Policy-Tests,
  Syntax/Hilfe, Whitespace und statischen Source-/Control-/Sink-Review. Die
  Current-Source-Sicherheitsbewertung ist an der dokumentierten Cross-User-
  POSIX-Owner-/Mode-Grenze `already_safe`; Hosted-Per-Rule-SonarQube- und
  Live-Smoke-Evidenz bleiben offen.

## Delivery-Update

Der Parent bestätigte zuvor geschützten Merge und 14 grüne Master-Push-
Workflows. Diese Aufgabe dokumentiert jetzt den vollständigen Merge-SHA
`7f72325cbd177e4bd98b3511a58344c04d41b06b`, seine Reachability vom aktuellen
Parent-Head und einen aufbewahrten aktuellen lokalen Rerun. Der Befund ist nur
für dieses lokale Archiv `accepted_risk`, weil ein aufbewahrter Hosted-Per-Rule-
SonarQube-Receipt oder Live-CRS-/libmodsecurity-/Connector-Smoke fehlt. Weder
ein Remote-Exploit, ein Fix, ein verifizierter Abschluss, Produktionssicherheit
noch Release-Freigabe werden behauptet.

## Nutzerbeauftragte lokale Archiv-Disposition — 2026-07-26

Nach dem Abgleich des aktuellen SonarQube-Cloud-/GitHub-Status wählte der
aktuelle Nutzer dieses exakte Tripel für einen verlustfreien lokalen
Archiv-Move. Der aufbewahrte Entscheidungs-Receipt ist
`/var/tmp/codex/ModSecurity-conector/runs/20260726T182851Z-user-selected-parent-sonar-archive/decision.md`
mit SHA-256 `d5dc1ed08dfca22b841c02eee45e0459665f026924ff531f158d1e5dd0145cdf`.

Der Nutzer akzeptiert nur die dokumentierte Restunsicherheit für dieses Archiv:
fehlende Hosted-Per-Rule-SonarQube-Evidenz, einen nicht ausgeführten realen
CRS-/libmodsecurity-/Connector-Smoke, breitere Dateisystem-/Identitätsannahmen
und aktuelle Static-Analyzer-Signale. Der Record ist nicht fixed, verified
oder closed. Vor jeder Produktions-, Veröffentlichungs-, Release- oder
technischen Abschlussentscheidung das vollständige Tripel nach
`.codex/findings/` zurückverschieben und seine bestehenden Akzeptanzkriterien
erneut ausführen.
