> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:59:05Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-rule-chain-semantics-analysis.py`
> Ziel erstellen: `generate-rule-chain-semantics-analysis`
> Besitzer: `connector`
> Schweregrad: `informational`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Analyse der Regelkettensemantik

**Sprache:** [English](rule-chain-semantics-analysis.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Erstellt unter: `2026-06-19T16:59:05Z`

## Zusammenfassung
| Rule-chain rows | Rule-chain groups | Single-connector groups | Single-connector rows | Runtime-fixable candidates | Report-only items | Parent matched | Child matched | Full chain matched | Name-only non-rule-chain rows |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 7 | 14 | 0 | 13 | 3 | 2 | 3 | 6 |

## Fazit
- Ausgewählter Subcluster: With-MRTS DetectionOnly-Redirect-Klassifizierung und Nur-Bericht-Rule-Chain-Triage.
- Grundursache: Die Semantik der Regelkette ist nicht der aktive Blocker: Zeilen ohne MRTS-Regelkette werden durchgelassen, während Fehler mit MRTS nicht störende Erkennungszeilen sind, die nur Overlay-Zeilen enthalten. Die verbleibenden Nur-NGINX-Zeilen sind entweder Phase-4-Not-Next-Evidence-Zeilen oder With-MRTS-DetectionOnly-Zeilen.
- Sicherer Wechsel: metadata/report-only Klassifizierung; Nein Erwarteter Status, Regel, MRTS-Definition oder Connector-Core-Änderung.

## Regelkettenfehlerzeilen
| Connector | Variant | Case | Parent | Children | Expected | Actual | Parent matched | Child matched | Full chain | Classification | Fixability |
|---|---|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | yes | yes | yes | with_mrts_detection_only_chain_non_disruptive | report_only |
| nginx | no-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| haproxy | no-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | yes | unknown | yes | with_mrts_detection_only_chain_non_disruptive | report_only |
| apache | with-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | yes | yes | yes | with_mrts_detection_only_chain_non_disruptive | report_only |
| nginx | with-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| haproxy | with-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |

## Nicht-Regelkettenzeilen mit Kettennamen
| Connector | Variant | Case | Category | Rules | Expected | Actual | Classification | Root cause |
|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| nginx | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| haproxy | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| apache | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| nginx | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| haproxy | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |

## Reste von Einzelsteckern
| Count | Connector | Case | Variants | Rules | Expected | Actual | Classification | Fixability | Root cause |
|---|---|---|---|---|---|---|---|---|---|
| 2 | nginx | nginx_phase4_content_type_out_of_scope | no-crs/with-mrts, with-crs/with-mrts | - | {'200': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_phase4_minimal_log_only | no-crs/with-mrts, with-crs/with-mrts | - | {'200': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_phase4_safe_log_only | no-crs/with-mrts, with-crs/with-mrts | - | {'200': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_phase4_strict_connection_abort | no-crs/with-mrts, with-crs/with-mrts | - | {'403': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_redirect_phase1_302 | no-crs/with-mrts, with-crs/with-mrts | - | {'302': 2} | {'200': 2} | with_mrts_detection_only_single_connector_non_disruptive | report_only | with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking. |
| 2 | nginx | nginx_tx_scoring_absolute_block | no-crs/with-mrts, with-crs/with-mrts | - | {'403': 2} | {'200': 2} | with_mrts_detection_only_single_connector_non_disruptive | report_only | with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking. |
| 2 | nginx | nginx_tx_scoring_iterative_block | no-crs/with-mrts, with-crs/with-mrts | - | {'403': 2} | {'200': 2} | with_mrts_detection_only_single_connector_non_disruptive | report_only | with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking. |

## Nächste Empfehlung
- Empfohlener nächster Cluster: `multipart_files`
- Grund: Die verbleibende aktive Body-Prozessor-Arbeit ist jetzt nur noch mehrteilig, nachdem URL-codiert und XML Metadaten aufgeteilt wurden

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `c581790d4581ac9cf843e973f127b274784caf286d1661d72b5144f078049165` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
