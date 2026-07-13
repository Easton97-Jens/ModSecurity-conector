> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:12Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-nolog-audit-evidence-analysis.py`
> Ziel erstellen: `generate-nolog-audit-evidence-analysis`
> Besitzer: `connector`
> Schweregrad: `informational`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

<!-- retained-historical-generated-output -->
> Aktueller Refresh-Status: `skipped_stale_input`. Dieser Report bewahrt einen früheren evidenztragenden Snapshot, weil keine neuen verifizierten Eingaben vorliegen. Grund: required generated input is stale.

# Nolog-Audit-Nachweisanalyse

**Sprache:** [English](nolog-audit-evidence.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Generierte Datei – nicht manuell bearbeiten.

## Umfang
- Fall: `v3_action_nolog_pass_no_audit`
- Extrahierte Laufzeitzeilen: **12**
- Nur für Metadaten neu klassifizierte Zeilen: **6**
- Konnektoren: Apache, Haproxy, Nginx
- Varianten: no-crs/no-mrts, no-crs/with-mrts, with-crs/no-mrts, with-crs/with-mrts

## Regelsemantik
- Regel ID: `3326`
- Phase: `1`
- Ziel: `ARGS:foo`
- Aktionen: `id:3326, phase:1, nolog, pass, msg:'v3 imported nolog pass no audit'`
- has_nolog / has_auditlog: **Wahr / Falsch**
- Anfrage: `GET /?foo=bar&a=xxx`
- Body/content-type: `<empty>` / `-`
- Fazit: Explizites `nolog` bedeutet, dass von dieser Regel erwartet wird, dass sie keinen eigenen Prüfeintrag erzeugt. Ein With-CRS-Prüfdatensatz für eine andere CRS-Regel ist kein Nachweis dafür, dass die Nolog-Regel protokolliert wurde.

## Before/After
- `audit_log_evidence` Zeilen vor: **6**
- `audit_log_evidence` Zeilen nach: **0**
- `classification_only` Zeilen vor: **597**
- `classification_only` Zeilen nach: **603**

## Laufzeitzeilen
| Connector | Variant | Status | Expected | Actual | Audit IDs | Decision IDs | Target Rule Logged | Backend | Classification |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | PASS | 200 | 200 | - | - | False | True | nolog_expected_no_audit |
| nginx | no-crs/no-mrts | PASS | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | no-crs/no-mrts | PASS | 200 | 200 | - | 0 | False | True | nolog_expected_no_audit |
| apache | no-crs/with-mrts | PASS | 200 | 200 | - | - | False | True | nolog_expected_no_audit |
| nginx | no-crs/with-mrts | PASS | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | no-crs/with-mrts | PASS | 200 | 200 | - | 0 | False | True | nolog_expected_no_audit |
| apache | with-crs/no-mrts | FAIL | 200 | 200 | 920350 | - | False | True | nolog_expected_no_audit |
| nginx | with-crs/no-mrts | FAIL | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | with-crs/no-mrts | FAIL | 200 | 200 | 920350 | 920350 | False | True | nolog_expected_no_audit |
| apache | with-crs/with-mrts | FAIL | 200 | 200 | 920350 | - | False | True | nolog_expected_no_audit |
| nginx | with-crs/with-mrts | FAIL | 200 | 200 | - | - | False | False | nolog_expected_no_audit |
| haproxy | with-crs/with-mrts | FAIL | 200 | 200 | 920350 | 920350 | False | True | nolog_expected_no_audit |

## Nachweisfelder
| Connector | Variant | Method | Path | Query | Expected evidence | Actual evidence | Audit log | Error log | Run log |
|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | no-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | no-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |
| apache | no-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | no-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | no-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |
| apache | with-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | with-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | with-crs/no-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |
| apache | with-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/error.log | <runtime-artifact>/run.log |
| nginx | with-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log absent or empty | - | - | <runtime-artifact>/run.log |
| haproxy | with-crs/with-mrts | GET | / | foo=bar&a=xxx | rule 3326 must not create an audit entry because the action list contains nolog | audit log contains unrelated rule(s): 920350 | <runtime-artifact>/audit.log | <runtime-artifact>/spoa-agent.log | <runtime-artifact>/run.log |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d710463ce1770cc3b0d756f58baac88a9ae4702344ca82110d4828eb82e0245` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `6c36afa87a2f63eaa9ff2df91e08759b8f657ee9a8090112afcc534174e98e70` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
