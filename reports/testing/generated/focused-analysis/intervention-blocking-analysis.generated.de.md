> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:52Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-intervention-blocking-analysis.py`
> Ziel erstellen: `generate-intervention-blocking-analysis`
> Besitzer: `connector`
> Schweregrad: `informational`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

<!-- retained-historical-generated-output -->
> Aktueller Refresh-Status: `skipped_stale_input`. Dieser Report bewahrt einen früheren evidenztragenden Snapshot, weil keine neuen verifizierten Eingaben vorliegen. Grund: required generated input is stale.

# Interventionsblockierungsanalyse

**Sprache:** [English](intervention-blocking-analysis.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

- Erstellt unter: `2026-06-19T16:58:52Z`
- Erwartete `403` / tatsächliche `200` Zeilen in Prüfung: **562**.
- Interventionsblockierende echte Kandidaten: **6** zur Laufzeit korrigierbare Zeilen.
- Verbleibende P0/P1 eingriffsblockierende Zeilen: **6**.
- DetectionOnly überlagert unterbrechungsfreie Zeilen: **514** Nur-Berichtszeilen.
- no-MRTS-semantische No-Match-Zeilen: **42** Nur-Metadaten-Zeilen.
- Regel in der generierten Ladedatei: **372**
- Fehler beim Laden strenger Regeln: **0**
- Regel erfüllt: **198**
- Nachweise für störende Intervention: **0**
- Connector hat Interventionsbeweise verloren: **0**
- Der Connector hat 403 von diesem Nachweis zurückgegeben: **0**
- Backend/client 200 erreicht: **562**

## Schlüsselaufteilung

- with-MRTS DetectionOnly Overlay-Zeilen: **514**
- with-MRTS-Zeilen mit protokollierter Zielregelübereinstimmung, die durch dieses Overlay unterdrückt wird: **198**
- No-MRTS-Zeilen mit geladener Regel, aber keinem Übereinstimmungsnachweis: **48**

## A-H-Gruppen

| group | label | count | connectors | variants | suspected cause | fixability | risk |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| A | Rule not loaded | 190 | nginx | no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts | Rule-load evidence is missing or startup logs show a strict rule-load error. | fixable if generated loadfile path is wrong | low to medium |
| B | Rule loaded, no match | 32 | apache, haproxy | no-crs/no-mrts, with-crs/no-mrts | The rule is present and no strict load error is visible, but no target rule hit appears in logs or HAProxy decisions. | not a safe intervention fix; requires semantic/native comparison | medium to high |
| C | Rule matched, no intervention created | 0 | - | - | - | - | - |
| D | Intervention created, connector did not set 403 | 0 | - | - | - | - | - |
| E | Intervention created, runner/evidence missed it | 0 | - | - | - | - | - |
| F | Expected block, but effective runtime is non-disruptive | 340 | apache, haproxy | no-crs/with-mrts, with-crs/with-mrts | with-MRTS loads MRTS INIT, which sets ctl:ruleEngine=DetectionOnly; disruptive actions are intentionally non-blocking in this overlay. | classification/report-only unless the MRTS overlay policy changes | low for report-only, high if expectations are changed |
| G | CRS changed behavior | 0 | - | - | - | - | - |
| H | Connector-specific blocking gap | 0 | - | - | - | - | - |

## Repräsentative Nachweise

### A. Regel nicht geladen

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| duplicate_args_encoded_separator_edge | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| duplicate_header_case_normalization_gap | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| edge_semicolon_query_args_names | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| files_empty_part_future_compatibility | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| unicode_double_encoded_uri_runtime_difference | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| unicode_whitespace_normalization_gap | nginx | no-crs/no-mrts | - | 2 | `-` | `-` | `-` | no | no | no | yes |
| v3_request_cookies_names_case_runtime_difference | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |
| v3_request_headers_names_lowercase_runtime_difference | nginx | no-crs/no-mrts | - | 1 | `-` | `-` | `-` | no | no | no | yes |

### B. Regel geladen, keine Übereinstimmung

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| duplicate_args_encoded_separator_edge | apache | no-crs/no-mrts | 4608 | 2 | `ARGS_NAMES` | `@contains b` | `/?a=1%3Bb=2&a=3` | yes | no | no | yes |
| duplicate_header_case_normalization_gap | apache | no-crs/no-mrts | 4607 | 1 | `REQUEST_HEADERS_NAMES` | `@contains x-demo` | `/` | yes | no | no | yes |
| edge_semicolon_query_args_names | apache | no-crs/no-mrts | 4513 | 2 | `ARGS_NAMES` | `@contains b` | `/?a=1;b=2` | yes | no | no | yes |
| files_empty_part_future_compatibility | apache | no-crs/no-mrts | 4706 | 2 | `FILES` | `@rx ^$` | `/` | yes | no | no | yes |
| unicode_double_encoded_uri_runtime_difference | apache | no-crs/no-mrts | 4707 | 1 | `REQUEST_URI` | `@contains café` | `/?q=%25u0063%25u0061%25u0066%25u00E9` | yes | no | no | yes |
| unicode_whitespace_normalization_gap | apache | no-crs/no-mrts | 4708 | 2 | `ARGS:q` | `@streq a b` | `/?q=a%E2%80%83b` | yes | no | no | yes |
| v3_request_cookies_names_case_runtime_difference | apache | no-crs/no-mrts | 4403 | 1 | `REQUEST_COOKIES_NAMES` | `@contains user_token` | `/` | yes | no | no | yes |
| v3_request_headers_names_lowercase_runtime_difference | apache | no-crs/no-mrts | 4401 | 1 | `REQUEST_HEADERS_NAMES` | `@contains x-smoke-header` | `/` | yes | no | no | yes |

### F. Erwarteter Block, aber die effektive Laufzeit ist unterbrechungsfrei

| case | connector | variant | rule | phase | target | operator | request | loaded | matched | intervention | backend |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| action_deny_phase1 | apache | no-crs/with-mrts | 2101 | 1 | `-` | `-` | `/` | yes | yes | no | yes |
| action_deny_phase2 | apache | no-crs/with-mrts | 2102 | 2 | `-` | `-` | `/` | yes | yes | no | yes |
| audit_log_empty_sections_future_target | apache | no-crs/with-mrts | 4605 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |
| audit_log_matched_var_encoded_value | apache | no-crs/with-mrts | 4603 | 2 | `ARGS:q` | `@contains a b` | `/?q=a+b` | yes | yes | no | yes |
| audit_log_message_presence_connector_gap | apache | no-crs/with-mrts | 4602 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |
| audit_log_multiline_message_normalization | apache | no-crs/with-mrts | 4604 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |
| audit_log_phase1_block | apache | no-crs/with-mrts | 1401 | 1 | `ARGS:audit` | `@streq trigger` | `/?audit=trigger` | yes | yes | no | yes |
| audit_log_rule_id_presence_runtime_difference | apache | no-crs/with-mrts | 4601 | 1 | `ARGS:a` | `@streq block` | `/?a=block` | yes | yes | no | yes |

## Sicherer Subcluster

- Ausgewählt: **nein**
- Name: `none`
- Anzahl: **0**
- Grund: Keine Zeile zeigt einen echten Störeingriff, der später durch Connector oder Runner verloren geht
- Empfohlene Maßnahme: connector/core-Code noch nicht bearbeiten; Entscheiden Sie, ob eine separate Klassifizierung mit MRTS DetectionOnly-Overlay erfolgen soll, und führen Sie einen native/semantic-Vergleich für No-MRTS-No-Match-Fälle durch

## Aktueller nächster Fixplan

- Empfohlener nächster Cluster: `multipart_files`
- Grund: Die verbleibende aktive Body-Prozessor-Arbeit ist jetzt nur noch mehrteilig, nachdem URL-codiert und XML Metadaten aufgeteilt wurden

## Hinweise zur Leitplanke

- Dieser Bericht ändert keine erwarteten Status, Testfallregeln, MRTS-Definitionen oder PASS/FAIL-Werte.
- Keine Zeile belegt derzeit einen störenden Eingriff, der später durch Connector oder Runner verloren ging.
- Die With-MRTS-Gruppe ist classification/report-only, sofern die Overlay-Richtlinie MRTS nicht absichtlich geändert wird.
- Behandeln Sie die No-MRTS-Gruppe als semantic/native-comparison-Arbeit, nicht als Interventionsweiterleitungs-Fix.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `c581790d4581ac9cf843e973f127b274784caf286d1661d72b5144f078049165` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
