> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:27Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-remaining-failure-analysis.py`
> Ziel erstellen: `generate-remaining-failure-analysis`
> Besitzer: `connector`
> Schweregrad: `important`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `stale`

<!-- retained-historical-generated-output -->
> Aktueller Refresh-Status: `skipped_stale_input`. Dieser Report bewahrt einen früheren evidenztragenden Snapshot, weil keine neuen verifizierten Eingaben vorliegen. Grund: required generated input is stale.

# Nächster Fixplan

**Sprache:** [English](next-fix-plan.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Erstellt unter: `2026-06-19T16:58:27Z`

Native MRTS Apache/NGINX bleibt ein separater Infrastrukturbeweis; Dieser Plan gilt nur für Connector-Full-Matrix-Reste.

## Empfehlung
- Empfohlener nächster Fix-Cluster: `multipart_files`
- Begründung: Die verbleibende aktive Body-Prozessor-Arbeit ist jetzt nur noch mehrteilig, nachdem URL-codiert und XML Metadaten aufgeteilt wurden
- Nicht als nächstes bearbeiten: `phase4_hard_abort_capability`, weil Transportabbruchnachweis plus Phase-4-Interventionsprotokolle erforderlich sind; Nicht mit Expected/PASS Änderungen lösen.
- Nicht als nächstes bearbeiten: `transformation_semantics`, weil große Anzahl, aber wahrscheinlich semantisch; erfordert native/libmodsecurity Vergleich vor Korrekturen.
- Nicht als nächstes bearbeiten: `nolog_expected_no_audit`, weil nur Klassifizierung: explizites Nolog bedeutet, dass die Übereinstimmungsregel keine Prüfnachweise ausgeben sollte.
- Nicht als nächstes bearbeiten: `response_header_mrts_detection_only`, weil Classification-only: with-MRTS DetectionOnly Overlay unterdrückt störende Phase-3-Aktion.
- Nicht als nächstes bearbeiten: `with_mrts_detection_only_non_disruptive`, weil Classification-only: with-MRTS DetectionOnly Overlay unterdrückt störende anforderungsseitige Aktionen.
- Nicht als nächstes bearbeiten: `secaction_detection_only_overlay`, weil Classification-only: with-MRTS DetectionOnly Overlay unterdrückt störende SecAction-Eingriffe.
- Nicht als nächstes bearbeiten: `xml_processor_activation_missing`, da nur Klassifizierung: XML Body und Content-Type existieren, aber diese Fixtures aktivieren ctl:requestBodyProcessor=XML nicht.
- Nicht als nächstes bearbeiten: `multipart_processor_activation_missing`, da nur Klassifizierung: mehrteiliger Körper, Inhaltstyp und Grenze vorhanden sind, diese Vorrichtungen jedoch keinen Zugriff auf den Anforderungskörper ermöglichen, bevor FILES/ARGS_NAMES-Sammlungen erwartet werden.
- Nicht als nächstes bearbeiten: `collection_name_normalization_semantics`, weil metadata-only: geladene Regeln haben keine Übereinstimmungsnachweise; benötigt native/libmodsecurity Vergleich vor Laufzeitkorrekturen.

## P0
- Keine.

## P1
- Keine.

## P2
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| multipart_files | 6 | apache, nginx, haproxy | remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits | compare multipart variable population across connectors with one representative request | medium | targeted multipart cases, connector smoke for touched connector, full matrix if parser behavior changes |

## P3
| Cluster | Count | Connector | Why | Likely change | Risk | Tests |
|---|---|---|---|---|---|---|
| phase4_hard_abort_capability | 120 | apache, nginx, haproxy | Phase 4/RESPONSE_BODY now requires hard-abort evidence, not status-only denial | stabilize NGINX strict evidence; classify Apache/HAProxy gaps until real transport abort evidence exists | high if promoted prematurely or faked | phase4 hard-abort report regeneration, targeted strict Phase 4 connector evidence, native report regeneration |
| transformation_semantics | 12 | apache, nginx, haproxy | largest semantic cluster; likely needs native/libmodsecurity comparison before any fix | deeper semantic evidence, not harness routing | high | targeted transformation cases, native comparison where available |

## P4
- Keine.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `3425a08630d7eee65c73745216c902a605453363e9b26c12d62d042fabddf0a0` | `2026-06-16T19-12-00Z-614c8049` | stale |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: connector_sha differs |
