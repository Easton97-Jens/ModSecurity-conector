# FND-SONAR-0014 — PR-#97-Common-Runtime-Smoke-Maintainability-Follow-up

## Klassifikation

- **Kategorie:** `sonarqube_finding` (`maintainability_code_smells`)
- **Regeln:** `python:S1192` und `python:S3415`
- **Repository / Ownership:** `parent` / `parent`
- **Priorität / Schwere / Confidence:** `P3` / `major` / `candidate`
- **Status / Verifikation:** `accepted_risk` / `current_parent_semantics_revalidated_pending_hosted_per_rule_receipt`
- **Release-Blocker / Security-relevant:** nein / nein
- **Delivery-Status:** vollständiger geschützter Merge `7f72325cbd177e4bd98b3511a58344c04d41b06b` ist vom aktuellen Parent `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd` lokal erreichbar; der Hosted-Per-Rule-Receipt bleibt ausstehend.

## Zusammenfassung

Der gepaarte PR-#97-Change-Record meldet zwei `python:S1192`-
Beobachtungen zu doppelten Literalen und vier `python:S3415`-Beobachtungen zur
Assertion-Argumentreihenfolge auf der ersten Draft-PR-Analyse. Das lokale
Follow-up führt benannte Runtime-/CRS-Konstanten ein und korrigiert vier
Assertion-Reihenfolgen. Die bereitgestellte fokussierte Suite meldet 26
bestandene Fälle.

Parent-bereitgestellte Exact-Head-Evidenz für
`b3860aac005a98244f5e880efc26a74449b11989` meldet die 26 fokussierten Tests,
`compileall`, `--help`, erforderliche/aktuelle PR-Checks und SonarQube-Cloud-
Quality-Gate als bestanden; acht aktuelle PR-Issues sind aggregiert
`CLOSED/FIXED`. Der aktuelle Nutzer wählte eine ausschließlich lokale
Archiv-Disposition `accepted_risk` für den fehlenden aufbewahrten Hosted-Per-
Rule-S1192/S3415-Receipt; die aktuellen lokalen Merge- und Semantik-Evidenzen
stehen unten, ohne einen Quality-Gate-Pass, Fix oder Release-Ergebnis zu
behaupten.

## Aktuelle lokale Revalidierung — 2026-07-26

Der vollständige geschützte Merge `7f72325cbd177e4bd98b3511a58344c04d41b06b`
ist ein Ancestor des aktuellen Parent
`3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd`. Der aufbewahrte Task-Report
führte die 26 fokussierten Controls, Syntax, CLI-Hilfe und Whitespace-Review
erneut aus. `CRS_SETUP_TEMPLATE_NAME`, `RUNTIME_PATH_DEPENDENCY` und
`RUNTIME_OUTPUT_PATH_FIELDS` bleiben benannte Konstanten; die vier
korrigierten Assertion-Controls bewahren ihr Rejection- und Legitimate-
Control-Verhalten. Die Sicherheitsgrenze von FND-SONAR-0013 wurde im selben
Report unabhängig revalidiert. Weder eine Source-Änderung noch eine PR ist
erforderlich; Hosted-Per-Rule-S1192/S3415-Evidenz bleibt die einzige
Completion-Lücke.

## Beobachtetes und erwartetes Verhalten

Der geprüfte exakte PR-Head ist `b3860aac005a98244f5e880efc26a74449b11989`
gegen Basis `38752600e4823fc5a16f3e155047da2d660b9897`; ursprünglicher
Feature-Commit `2fb994324c097a846ed6f6d93126cb8def391f0d`. Der Parent hat das
aktuelle Exact-Head-Aggregatergebnis bestätigt; der spätere geschützte Merge
und die Master-Workflows stehen im Delivery-Update.

Der Diff führt `CRS_SETUP_TEMPLATE_NAME`, `RUNTIME_PATH_DEPENDENCY` und
`RUNTIME_OUTPUT_PATH_FIELDS` für wiederholten Text ein und ändert vier
unittest-Assertion-Argumentreihenfolgen. Die Korrekturen müssen dasselbe
Rejection- und Legitimate-Control-Verhalten bewahren, die Path-/Provenance-
Grenze von FND-SONAR-0013 bewahren und dürfen niemals Sonar-Regel, Profil,
Suppression, Exclusion oder Quality Gate ändern. Die nutzerbeauftragte lokale
Archiv-Disposition ersetzt keine technische Evidenz und schwächt diese Grenze
nicht ab.

## Auswirkung und betroffener Scope

Die Auswirkung sind Maintainability-Schulden und künftiges Review-/Static-
Analysis-Rauschen; es ist kein belegter Runtime- oder Sicherheitsdefekt und
blockiert eine Release-Integration nicht eigenständig. Der P1-
Sicherheitskandidat-Status von `FND-SONAR-0013` ändert sich dadurch ebenfalls
nicht.

Betroffene Pfade und Symbole sind:

- `common/scripts/run_local_runtime_smoke.py` —
  `CRS_SETUP_TEMPLATE_NAME`, `RUNTIME_PATH_DEPENDENCY` und
  `RUNTIME_OUTPUT_PATH_FIELDS`.
- `tests/test_common_runtime_smoke_crs_source_security.py` — vier Korrekturen
  der Assertion-Argumentreihenfolge.
- Die gepaarten PR-#97-Change-Record-Dateien.

## Reproduktion und Evidenz

Den lokalen PR-#97-Diff und seinen gepaarten Change Record prüfen, dann:

```text
env PYTHONDONTWRITEBYTECODE=1 python -m unittest -v tests.test_common_runtime_smoke_crs_source_security
```

Sicherstellen, dass die geänderten Assertions dasselbe Control-/Rejection-
Verhalten behalten. Der Change Record meldet 26 bestandene fokussierte Fälle,
aber diese Record-Aufgabe führte die Tests nicht erneut aus und bewahrte keinen
Raw-Test-Log auf. Eine spätere Exact-Head-SonarQube-Cloud-Abfrage muss Regel,
Komponente und Disposition für `python:S1192` und `python:S3415` ohne
Änderung eines Sonar-Controls vergleichen.

Evidenzquelle: `/var/tmp/codex/ModSecurity-conector/runs/20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b/worktrees/pr55/reports/audits/change-records/CR-20260723-sonar-common-crs-source-integrity.md`, SHA-256
`d07f3fb43265c7acfad64934c0b73c859ac3c30a048fff0b7e6064a0e334a8c9`,
Run `20260724T064103Z-sequential-non-mrts-pr-master-integration-9f1bf22b`,
beobachtet am `2026-07-24T07:58:00Z` mit `git diff --name-status`, `git diff
--check` und `sha256sum`, Exit `0`. Der SHA-256 des deutschen Paars ist
`e7b9461f09f84cb43b8f736806743d0d83b7ea028507e25b88666f4c22182e24`.
Beide sind volatile Worktree-Quellen, keine versiegelten Execution-Receipts.
Die Parent-bereitgestellte aggregierte Hosted-Zusammenfassung hat in dieser
begrenzten Record-Aufgabe keinen angegebenen Raw-Per-Rule-Receipt-Pfad.

## Grundursache und vorgeschlagene Remediation

Die erste Draft-PR-Analyse identifizierte laut Bericht wiederholten Literaltext
und Assertion-Argumentreihenfolge, die konfigurierte Sonar-Maintainability-
Regeln nicht erfüllten. Die begrenzte Evidenz belegt keinen breiteren Runtime-
Defekt oder eine Verhaltensänderung über diese Muster hinaus.

Die benannten gemeinsamen Konstanten und die semantisch äquivalente Assertion-
Reihenfolge beibehalten. Das aktuelle aggregierte Exact-Head-Ergebnis meldet
acht PR-Issues als `CLOSED/FIXED`; einen Per-Rule-Receipt aufbewahren, um die
zwei S1192- und vier S3415-Beobachtungen spezifisch zu verifizieren. Die
Path-/Provenance-Controls
von FND-SONAR-0013 dürfen nicht abgeschwächt werden, um einen Maintainability-
Befund zu reduzieren.

## Akzeptanzkriterien und Validierungsplan

1. Der aktuelle exakte PR-#97-Head bewahrt Common-Runtime-Smoke-Rejection- und
   Legitimate-Control-Verhalten nach Literal-Deduplizierung und Assertion-
   Reihenfolgekorrektur.
2. Fokussierte Tests, Syntax-/Help-Checks, Bilingual-Change-Record-Review und
   `git diff --check` bestehen für diesen exakten Head.
3. Der bestätigte exakte Head behält Quality Gate `OK` und aggregierte aktuelle
   PR-Issues `CLOSED/FIXED` ohne Control-Änderung; ein aufbewahrter Per-Rule-
   Receipt verifiziert die zwei S1192- und vier S3415-Beobachtungen spezifisch.
4. Die Path-/Provenance-Grenze von FND-SONAR-0013 bleibt intakt und unabhängig
   validiert.

Einen Raw-Per-Rule-Exact-Head-Receipt aufbewahren, ihn nach jedem Head-Wechsel
wiederholen, fokussiertes Semantik-/Syntax-/Help-/Bilingual-/Whitespace-
Prüfungen ausführen und den Diff auf unbeabsichtigte Security-Control-
Abschwächungen prüfen. Nach geschütztem Merge resultierenden-Master-SHA und
anwendbare Master-Checks prüfen, bevor dieser Befund als verified markiert wird.

## Abhängigkeiten, Blocker und Restrisiko

Abhängigkeiten sind Parent-Python für die fokussierte Suite und Lesezugriff auf
aktuelle SonarQube-Cloud-Ergebnisse. Full-Merge-/Current-Parent-Beziehung und
lokale Semantik sind jetzt belegt; der Blocker ist ein aufbewahrter Raw-
Per-Rule-S1192/S3415-Hosted-Receipt.

Das Restrisiko sind Maintainability-/Review-Unsicherheit, bis diese
verbleibenden Receipts vorliegen. Der aktuelle Nutzer akzeptiert diese
Unsicherheit nur für das lokale Archiv; der Merge ist im Delivery-Update
dokumentiert, und es werden kein Runtime-Exploit, keine eigenständige
Security-Remediation, kein Fix und keine Release-Disposition behauptet.
Verwandter Befund: `FND-SONAR-0013`.

## Verlauf

- `2026-07-24T07:58:00Z`: Aus dem gepaarten lokalen PR-#97-Change-Record als
  nicht blockierender `in_progress` / `unverified` S1192/S3415-Follow-up
  angelegt. Kein aktuelles Hosted-Ergebnis oder Merge-Ergebnis wird behauptet.
- `2026-07-24T08:04:28Z`: Parent bestätigte exakten Head `b3860aac005a98244f5e880efc26a74449b11989`; 26 fokussierte Tests, `compileall`, `--help`, erforderliche/aktuelle PR-Checks bestanden, Quality Gate war `OK` und acht aktuelle PR-Issues waren `CLOSED/FIXED`. PR #97 war zu diesem Zeitpunkt noch ungemergt.
- `2026-07-26T17:18:12Z`: Local Git bestätigt, dass der vollständige Merge
  `7f72325cbd177e4bd98b3511a58344c04d41b06b` ein Ancestor des aktuellen Parent
  `3c99b88e1c73dcf7b79c0ea6dd189cb4383d13dd` ist. Der aufbewahrte Task-Report
  enthält fokussierte Control-Semantik, Syntax/Hilfe, Whitespace und den Erhalt
  der benannten Literale und Assertion-Reihenfolge. Hosted-Per-Rule-
  S1192/S3415-Evidenz bleibt offen.

## Delivery-Update

Der Parent bestätigte zuvor geschützten Merge und 14 grüne Master-Push-
Workflows. Diese Aufgabe dokumentiert jetzt den vollständigen Merge-SHA und
seine Reachability vom aktuellen Parent-Head sowie lokale Semantik-Validierung.
Der nicht blockierende Follow-up ist nur für dieses lokale Archiv
`accepted_risk`, weil ein aufbewahrter Hosted-Per-Rule-S1192/S3415-Receipt
fehlt. Keine eigenständige Runtime- oder Sicherheitsauswirkung, kein
Quality-Gate-Pass, Fix, verifizierter Abschluss oder Release-Freigabe wird
behauptet.

## Nutzerbeauftragte lokale Archiv-Disposition — 2026-07-26

Nach dem Abgleich des aktuellen SonarQube-Cloud-/GitHub-Status wählte der
aktuelle Nutzer dieses exakte Tripel für einen verlustfreien lokalen
Archiv-Move. Der aufbewahrte Entscheidungs-Receipt ist
`/var/tmp/codex/ModSecurity-conector/runs/20260726T182851Z-user-selected-parent-sonar-archive/decision.md`
mit SHA-256 `d5dc1ed08dfca22b841c02eee45e0459665f026924ff531f158d1e5dd0145cdf`.

Der Nutzer akzeptiert nur den fehlenden aufbewahrten aktuellen Per-Rule-
S1192/S3415-SonarQube-Receipt für dieses lokale Archiv. Der Record ist nicht
fixed, verified oder closed. Vor jeder Produktions-, Veröffentlichungs-,
Release- oder technischen Abschlussentscheidung das vollständige Tripel nach
`.codex/findings/` zurückverschieben und seine bestehenden Akzeptanzkriterien
erneut ausführen.
