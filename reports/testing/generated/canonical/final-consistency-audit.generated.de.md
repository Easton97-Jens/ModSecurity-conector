> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:59:06Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-final-consistency-audit.py`
> Ziel erstellen: `generate-final-consistency-audit`
> Besitzer: `connector`
> Schweregrad: `critical`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Abschließendes Konsistenzaudit

**Sprache:** [English](final-consistency-audit.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Generierte Datei – nicht manuell bearbeiten.

- Erstellt unter: `2026-06-19T16:59:06Z`
- Release-Bereitschaft: `needs_attention`
- Empfohlener nächster Fix-Cluster: `multipart_files`
- Empfehlung begründet: `no`
- Grund: Die verbleibende aktive Body-Prozessor-Arbeit ist jetzt nur noch mehrteilig, nachdem URL-codiert und XML Metadaten aufgeteilt wurden

## Git und Submodule
- Konnektor HEAD: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
- Framework-HEAD: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`

| Submodule status |
|---|
| dc19582d89bd8ef50463c5a9c5a0271cc37bb958 modules/ModSecurity-test-Framework (heads/master) |
|  13aa91291adea12d5c607fdd165d010fcfb1da78 modules/ModSecurity-test-Framework/tools/MRTS (heads/main) |

## Vollständige Matrix-Zusammenfassung
- Versucht: **3928**
- PASS: **3157**
- FAIL: **771**
- BLOCKED: **0**
- NOT_EXECUTABLE: **0**
- Ausstehend: **2298**
- Full-Matrix wurde für diese Prüfung nicht erneut ausgeführt; Die Zahlen basieren auf vorhandenen Nachweisen.

## Prioritätsverteilung
- P0/P1/P2/P3/report_only nicht PASS: **6 / 0 / 60 / 168 / 537**
- Warteschlangensummen und neu berechnete Nicht-PASS-Prioritäten stimmen überein: `yes`
- Nicht bestandene Warteschlangensummen: `{'P0': 6, 'P2': 60, 'P3': 168, 'report_only': 537}`
- Neuberechnetes Nicht-PASSEN: `{'P0': 6, 'P2': 60, 'P3': 168, 'report_only': 537}`
- Nur FAIL neu berechnet: `{'P0': 6, 'P2': 60, 'P3': 168, 'report_only': 537}`
- P0/P1 fehlerhafte Zeilen: **6**
- P2 Zeilen sind Antwort-Header DetectionOnly/report-only Reste: `yes`

## Verbleibende Kategorien
- Aktive, zur Laufzeit reparierbare Cluster: **1**
- Nur Berichtszeilen: **609**
- Semantisch ausstehende Zeilen: **42**
- Ausstehende Zeilen zum Fähigkeitsnachweis: **72**
- Verbindungslückenzeilen: **42**
| Category | Count | Connectors | Disposition | Recommended next step |
|---|---|---|---|---|
| with_mrts_detection_only_non_disruptive | 519 | apache, haproxy, nginx | report_only | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 72 | apache, nginx | capability_evidence_pending | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | report_only | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| phase4_connector_gap | 42 | apache, haproxy, nginx | connector_gap | document connector gap unless implementation can prove a real hard abort |
| collection_name_normalization_semantics | 30 | apache, haproxy, nginx | semantic_pending_native_or_libmodsecurity_comparison | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| xml_processor_activation_missing | 18 | apache, haproxy, nginx | report_only | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| transformation_semantics | 12 | apache, haproxy, nginx | semantic_pending_native_or_libmodsecurity_comparison | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| multipart_files | 6 | apache, haproxy, nginx | review_required | compare multipart variable population across connectors with one representative request |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | report_only | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report_only | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |

## Überprüfung auf veraltete Cluster
| Cluster | Remaining category | FAIL work direction | FAIL classification | Status | Detail |
|---|---|---|---|---|---|
| audit_log_evidence | 0 | 0 | 0 | clear | no active rows |
| intervention_blocking | 0 | 6 | 0 | review | nonzero remaining, work-direction, or classification count |
| request_body_processor | 0 | 0 | 0 | clear | no active rows |
| multipart_files | 6 | 0 | 0 | review | nonzero remaining, work-direction, or classification count |
| xml_processor | 0 | 0 | 0 | clear | no active rows |
| phase4_hard_abort_supported | 0 | 0 | 0 | clear | no active rows |
| rule_chain_semantics | 0 | 0 | 0 | clear | runtime_fixable_candidates=0 |
| response_header_backend_setup | 0 | 0 | 0 | clear | no active rows |
| response_header_hook | 0 | 0 | 0 | clear | no active rows |
| response_header_multi_value_gap | 0 | 0 | 0 | clear | no active rows |

## Cluster sind nicht mehr die nächsten
| Cluster | Count | Reason |
|---|---|---|
| phase4_hard_abort_capability | 120 | requires transport-abort proof plus Phase 4 intervention logs; do not solve with Expected/PASS changes |
| transformation_semantics | 12 | large count but likely semantic; needs native/libmodsecurity comparison before fixes |
| nolog_expected_no_audit | 6 | classification-only: explicit nolog means the matching rule should not emit audit evidence |
| response_header_mrts_detection_only | 60 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action |
| with_mrts_detection_only_non_disruptive | 519 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive request-side action |
| secaction_detection_only_overlay | 0 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive SecAction intervention |
| xml_processor_activation_missing | 18 | classification-only: XML body and Content-Type exist, but these fixtures do not enable ctl:requestBodyProcessor=XML |
| multipart_processor_activation_missing | 0 | classification-only: multipart body, Content-Type, and boundary exist, but these fixtures do not enable request body access before expecting FILES/ARGS_NAMES collections |
| collection_name_normalization_semantics | 30 | metadata-only: loaded rules have no match evidence; needs native/libmodsecurity comparison before runtime fixes |

## Bekannte Lücken
| Gap | Rows |
|---|---|
| phase4_missing_abort_evidence | 72 |
| phase4_connector_gap | 42 |
| transformation_semantics | 12 |
| collection_name_normalization_semantics | 30 |
| connector_gap | 0 |

## Benutzerentscheidungen
| Area | Reason | Safe next |
|---|---|---|
| phase4_hard_abort | Apache has implementation-path evidence but no runtime hard-abort proof; HAProxy remains a connector gap. | collect real transport-abort evidence or keep these rows as capability/gap classifications |
| transformation_and_collection_semantics | remaining no-match rows need native/libmodsecurity comparison before runtime changes. | decide whether to build comparator evidence; do not change Expected statuses or rules. |
| phase1_request_body_connector_gap | three rows remain classified as phase1 request-body unavailable connector gap. | treat as connector capability discussion before core behavior changes. |

## Native MRTS
- Der native MRTS-Nachweis bleibt von der Konnektor-Vollmatrix PASS/FAIL. getrennt.
| Target | Status | Attempted | PASS | FAIL | BLOCKED | Failed cases | Classification |
|---|---|---|---|---|---|---|---|
| apache2_ubuntu | FAIL | 13 | 12 | 1 | 0 | 100003-1 | native_modsecurity_semantics / phase4_native_limitation |
| nginx-pr24 | FAIL | 13 | 12 | 1 | 0 | 100003-1 | native_modsecurity_semantics / phase4_native_limitation |

## Phase 4 Hard-Abbruch
- Zeilen: **868**
- Nachweiszeilen für einen harten Abbruch: **0**
- Zeilen mit sensiblen Protokolllecks: **0**
| Connector | Capability status | Hard-abort evidence rows |
|---|---|---|
| apache | implementation_path_present_no_runtime_hard_abort_evidence | 0 |
| haproxy | connector_gap_no_hard_abort_evidence | 0 |
| nginx | connector_gap_no_hard_abort_evidence | 0 |

## Frische
| Input | Present | Generated at |
|---|---|---|
| reports/testing/generated/canonical/full-runtime-matrix.generated.json | yes | 2026-06-19T16:57:56Z |
| reports/testing/generated/work-queues/connector-work-queue.generated.json | yes | 2026-06-19T16:58:08Z |
| reports/testing/generated/work-queues/phase-work-queue.generated.json | yes | 2026-06-19T16:58:16Z |
| reports/testing/generated/canonical/remaining-failure-analysis.generated.json | yes | 2026-06-19T16:58:27Z |
| reports/testing/generated/canonical/next-fix-plan.generated.json | yes | 2026-06-19T16:58:27Z |
| reports/testing/generated/canonical/full-run-evidence.generated.json | yes | 2026-06-19T16:58:45Z |
| reports/testing/generated/mrts-native/mrts-native-summary.generated.json | yes | 2026-06-19T16:58:10Z |
| reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json | yes | 2026-06-19T16:58:23Z |
| reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json | yes | 2026-06-19T16:58:12Z |
| reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json | yes | 2026-06-19T16:58:16Z |
| reports/testing/generated/focused-analysis/body-processor-analysis.generated.json | yes | 2026-06-19T16:59:03Z |
| reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json | yes | 2026-06-19T16:58:52Z |
| reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json | yes | 2026-06-19T16:58:53Z |
| reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json | yes | 2026-06-19T16:59:05Z |

## Leitplanken
| Guardrail | Value |
|---|---|
| expected_status_changed | False |
| runtime_pass_fail_manually_changed | False |
| mrt_definitions_changed | False |
| tools_mrts_changed | False |
| rules_changed | False |
| connector_core_changed | False |
| full_matrix_rerun_required | False |
| matrix_counts_source | existing full-runtime-matrix evidence |

## Freigabeprüfungen
| Check | Pass |
|---|---|
| recommended_next_fix_cluster_none | no |
| blocked_zero | yes |
| queue_totals_consistent | yes |
| p0_p1_failure_rows_zero | no |
| p2_rows_are_response_header_mrts_detection_only | yes |
| active_runtime_fixable_clusters_zero | no |
| intervention_blocking_true_candidates_zero | no |
| audit_log_evidence_after_zero | yes |
| body_processor_active_after_zero | no |
| response_header_backend_setup_zero | yes |
| rule_chain_runtime_fixable_zero | yes |
| phase4_supported_label_absent | yes |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `c581790d4581ac9cf843e973f127b274784caf286d1661d72b5144f078049165` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `df4c56d7bd0afa823a2a90b4808120369d1c8281b8a00eed7266f1654369c62a` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
