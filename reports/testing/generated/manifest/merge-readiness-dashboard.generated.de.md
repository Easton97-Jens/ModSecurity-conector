> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:59:10Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Ziel erstellen: `refresh-connector-reports`
> Besitzer: `manifest`
> Schweregrad: `critical`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Dashboard zur Zusammenführungsbereitschaft

**Sprache:** [English](merge-readiness-dashboard.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Zusammenführungsbereitschaft: `WARN`

## Zusammenfassung

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3157 FAIL=771 BLOCKED=0 |
| Runtime Mismatch Analysis | PASS | mismatches=771 critical=0 categories={'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 36, 'libmodsecurity_collection_semantics': 24, 'libmodsecurity_transformation_semantics': 24, 'libmodsecurity_xml_parser_semantics': 12, 'nginx_phase4_response_body_enforcement_gap': 22, 'nolog_expected_no_audit': 6, 'phase4_rule_match_no_disruptive_intervention': 6, 'secaction_detection_only_overlay': 6, 'with_mrts_detection_only_overlay': 533} |
| Final Consistency Audit | PASS | needs_attention |
| Missing Inputs / Skipped Reports | PASS | none |
| Optional Producer Evidence | PASS | available/not required |
| Stale Reports | PASS | none |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | PASS | fresh |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent |

## Entscheidung

Zusammenführungsbereitschaft: `WARN`

Grund: Es werden kanonische Kernberichte generiert. Warnbedingungen werden dokumentiert.

## Nachweise

- Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
- Konnektor SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
- Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
- Primärblocker: `unknown`
- Empfohlener nächster Fix-Cluster: `multipart_files`
- Nachweisumfang: `full`
- Vollständige Matrix: `True`
- Vollständigkeit der Matrix: `12` / `12`
- Fehlende Full-Matrix-Jobs: `-`
- Zeitüberschreitung bei der Aktualisierung der vollständigen Matrix: `False`
- Laufzeitkonflikte / kritisch: `771` / `0`
- Vollmatrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3157` / `771` / `0` / `0`

## Submodule

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `dc19582d89bd8ef50463c5a9c5a0271cc37bb958` | `master` | clean | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `340546dbab42432eef255f99fda65c0d4301db589d6ac5c9f2a201a94326420e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `d969736e6a6b68e331b83c17dd8edb8516314b1d78dd5e8c9ab41806bfea1502` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `df4c56d7bd0afa823a2a90b4808120369d1c8281b8a00eed7266f1654369c62a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `9398f825fbe26f5d562ba7cc7fc0e39d4cc3a59a9c35e5727d75e385d20fe9a4` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
