> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:59:03Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-body-processor-analysis.py`
> Ziel erstellen: `generate-body-processor-analysis`
> Besitzer: `connector`
> Schweregrad: `informational`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Fehleranalyse des Körperprozessors

**Sprache:** [English](body-processor-analysis.generated.md) | Deutsch

- Erstellt unter: `2026-06-19T16:59:03Z`
- Vor dem ausgewählten Metadaten-Fix: request_body_processor **6**, multipart_files **6**, xml_processor **12**, kombiniert **24**.
- Nach der ausgewählten Metadatenkorrektur: request_body_processor **0**, multipart_files **6**, xml_processor **0**, kombiniert **6**.
- Ausgewählte Subclusterzeilen: **6**
- URL-codierte Formularzeilen wurden aus der Arbeit des aktiven Textprozessors verschoben: **12** -> **0**.
- XML Prozessoraktivierungsfehlende Zeilen wurden aus der aktiven xml_processor-Arbeit verschoben: **12** -> **0**.
- Zeilen mit fehlender Multipart-Prozessoraktivierung wurden aus der aktiven multipart_files-Arbeit verschoben: **0** -> **0**.
- Durch Regel geladene Nachweiszeilen: **8**
- Mit der Zielregel übereinstimmende Zeilen: **2**
- Backend erreichte Zeilen: **12**
- Body-Zugriff explizit anfordern für: **4**
- Collection/target Nachweiszeilen: **2**

## Ausgewählter Subcluster

- Fall: `phase1_vs_phase2_request_body_gap`
- Anzahl: **6**
- Aktion: Nur-Metadaten-Klassifizierung: request_body_processor -> Connector_gap
- Warum sicher: Der Fall hat einen leeren Anforderungstext und die vorhandenen Quellmetadaten lauten „Connector-Gap“; Keine Anfrage, Regel, erwarteter Status oder PASS/FAIL-Wert geändert
- Grundursache: Phase:1 REQUEST_BODY kann nicht mit dem erwarteten Bodyhit übereinstimmen, da der YAML-Anfragetext leer ist
- Körper angekommen: leer durch Vorrichtung
- Prozessor aktiv: nicht relevant für die ausgewählte Nur-Metadaten-Klassifizierung
- Erstellte Sammlungen: Keine Nachweise für Zielregelübereinstimmung

## URL-codierter Formular-Subcluster

- Anzahl: **12**
- Aktive request_body_processor-Zeilen vor der Berichtssynchronisierung: **12**
- Aktive request_body_processor-Zeilen nach der Berichtssynchronisierung: **0**
- Klassifizierung: `with_mrts_detection_only_non_disruptive`
- Arbeitsrichtung: `classification_only`
- Priorität: `report_only`
- Text gesendete Zeilen: **12**
- Korrekte Inhaltstypzeilen: **12**
- SecRequestBodyAccess In Zeilen: **12**
- Regelgeladene Zeilen: **12**
- Mit der Regel übereinstimmende Zeilen: **8**
- Collection/target Nachweiszeilen: **8**
- Backend erreichte Zeilen: **12**
- Grundursache: Die URL-codierten Körper und der Inhaltstyp sind vorhanden. Bei diesen Zeilen handelt es sich um Overlay-Fälle mit MRTS DetectionOnly, sodass störende Aktionen nicht blockierend bleiben und zur Nur-Bericht-Klassifizierung gehören.
- Fix: metadata/report-only; Kein Anforderungstext, Inhaltstyp, Regel, erwarteter Status oder PASS/FAIL-Wert geändert
- Risiko: gering, wenn es von der aktiven Arbeit des request_body_processors ferngehalten wird; hoch, wenn ohne störende Runtime-Nachweise zu PASS hochgestuft wird

| field | distribution |
| --- | --- |
| connectors | `apache`: 6, `haproxy`: 6 |
| variants | `no-crs/with-mrts`: 6, `with-crs/with-mrts`: 6 |
| case_ids | `pr70_phase2_audit_urlencoded_body`: 4, `request_body_args_post_names_block`: 4, `request_body_urlencoded_block`: 4 |
| rule_ids | `5702`: 4, `2204`: 4, `1200`: 4 |
| targets | `ARGS_POST:arg1`: 4, `ARGS_POST_NAMES`: 4, `ARGS_POST:test`: 4 |
| operators | `@streq pr70phase2`: 4, `@streq arg1`: 4, `@streq attack`: 4 |
| body_lengths | `26`: 4, `19`: 4, `11`: 4 |
| request_body_seen | `unknown`: 6, `yes`: 6 |

## XML Prozessoraktivierung – fehlender Subcluster

- Anzahl: **12**
- Aktive xml_processor-Zeilen vor der Berichtssynchronisierung: **12**
- Aktive xml_processor-Zeilen nach der Berichtssynchronisierung: **0**
- Klassifizierung: `xml_processor_activation_missing`
- Arbeitsrichtung: `classification_only`
- Priorität: `report_only`
- Text gesendete Zeilen: **12**
- XML Inhaltstypzeilen korrigieren: **12**
- SecRequestBodyAccess In Zeilen: **4**
- XML Aktive Prozessorzeilen: **4**
- Regelgeladene Zeilen: **12**
- Mit der Regel übereinstimmende Zeilen: **0**
- XML Sammlungsnachweiszeilen: **0**
- Backend erreichte Zeilen: **12**
- Grundursache: Die XML-Körper und der Inhaltstyp sind vorhanden, aber diese Vorrichtungen aktivieren SecRequestBodyAccess/ctl:requestBodyProcessor=XML nicht, daher ist die XML-Sammlungspopulation kein erwarteter Nachweis.
- Fix: metadata/report-only; Kein XML-Körper, Regel, erwarteter Status, Connector-Core-Verhalten oder PASS/FAIL-Wert geändert
- Risiko: gering, wenn nur Berichtspflicht besteht; hoch, wenn es als Connector behandelt wird XML Parserfehler ohne Prozessoraktivierung

| field | distribution |
| --- | --- |
| connectors | `apache`: 6, `haproxy`: 6 |
| variants | `no-crs/no-mrts`: 6, `with-crs/no-mrts`: 6 |
| case_ids | `parser_xml_partial_body_future_target`: 4, `xml_deep_nesting_future_target`: 4, `xml_request_body_malformed_connector_gap`: 4 |
| rule_ids | `4610`: 4, `4712`: 4, `4408`: 4 |
| targets | `XML`: 12 |
| operators | `@contains root`: 4, `@contains deepnode`: 4, `@contains broken`: 4 |
| content_types | `application/xml`: 12 |
| body_lengths | `9`: 4, `50`: 4, `21`: 4 |
| body_hashes | `a1cbdf58569b7f77dd47ef83641e48fe830098618b019034b88563050b12eb06`: 4, `9aab1567b5d32b5a5a60ad9f5f6f8f8cf485dbf9aa938905e71a0e88b009f011`: 4, `0c13b76b5721981c5ae77b5629399200d777a7e3b54e6c6d1dbbd43b0d5b75d6`: 4 |
| request_body_seen | `unknown`: 6, `yes`: 6 |

## Mehrteilige Prozessoraktivierung – fehlender Subcluster

- Anzahl: **0**
- Aktive multipart_files-Zeilen vor der Berichtssynchronisierung: **0**
- Aktive multipart_files-Zeilen nach der Berichtssynchronisierung: **0**
- Klassifizierung: `multipart_processor_activation_missing`
- Arbeitsrichtung: `classification_only`
- Priorität: `report_only`
- Vom Text gesendete Zeilen: **0**
- Korrekte Multipart-Content-Type-Zeilen: **0**
- Grenze gültiger Zeilen: **0**
- SecRequestBodyAccess In Zeilen: **0**
- Aktive Zeilen des Multipart-Parsers: **0**
- Regelgeladene Zeilen: **0**
- Mit der Regel übereinstimmende Zeilen: **0**
- FILES/FILES_NAMES Nachweiszeilen: **0**
- ARGS/ARGS_NAMES Nachweiszeilen: **0**
- Collection/target Nachweiszeilen: **0**
- Backend erreichte Zeilen: **0**
- Grundursache: Die mehrteiligen Körper, der Inhaltstyp, die Grenzen, die Feldnamen und die Dateinamen sind vorhanden, aber diese Vorrichtungen aktivieren SecRequestBodyAccess nicht, bevor FILES/ARGS_NAMES-Erfassungsnachweise erwartet werden.
- Fix: metadata/report-only; Kein mehrteiliger Körper, Inhaltstyp, Grenze, Regel, erwarteter Status, Connector-Core-Verhalten oder PASS/FAIL-Wert geändert
- Risiko: gering, wenn nur Berichtspflicht besteht; hoch, wenn es als Connector-Multipart-Parser-Fehler ohne Aktivierung des Anforderungstexts behandelt wird

| field | distribution |
| --- | --- |
| connectors | - |
| variants | - |
| case_ids | - |
| rule_ids | - |
| targets | - |
| operators | - |
| content_types | - |
| boundaries | - |
| boundary_status | - |
| part_counts | - |
| field_names | - |
| filenames | - |
| body_lengths | - |
| body_hashes | - |
| request_body_seen | - |

## Verteilungen aktiver Körperprozessoren

### Connectors

| value | count |
| --- | ---: |
| `apache` | 2 |
| `nginx` | 2 |
| `haproxy` | 2 |

### Varianten

| value | count |
| --- | ---: |
| `no-crs/no-mrts` | 3 |
| `with-crs/no-mrts` | 3 |

### Körperarten

| value | count |
| --- | ---: |
| `multipart` | 4 |
| `empty` | 2 |

### Inhaltstypen

| value | count |
| --- | ---: |
| `multipart/form-data; boundary=----AaB03x` | 4 |
| `-` | 2 |

### Ziele

| value | count |
| --- | ---: |
| `FILES` | 4 |
| `-` | 2 |

### Fehlerkategorien

| value | count |
| --- | ---: |
| `multipart_files` | 6 |

## Gruppierte Zeilen

| count | connector | body kind | content-type | phase | target | status | category | variants | matched | cause | fixability |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 2 | apache | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES` | 403->200 | multipart_files | no-crs/no-mrts, with-crs/no-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | haproxy | multipart | `multipart/form-data; boundary=----AaB03x` | 2 | `FILES` | 403->200 | multipart_files | no-crs/no-mrts, with-crs/no-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |
| 2 | nginx | empty | `-` | 2 | `-` | 403->200 | multipart_files | no-crs/no-mrts, with-crs/no-mrts | 0 | Multipart FILES/FILES_NAMES population differs by case; some rows match but with-MRTS prevents blocking, others lack collection evidence. | requires targeted native/connector comparison before code changes |

## Aktueller nächster Fixplan

- Empfohlener nächster Cluster: `multipart_files`
- Grund: Die verbleibende aktive Body-Prozessor-Arbeit ist jetzt nur noch mehrteilig, nachdem URL-codiert und XML Metadaten aufgeteilt wurden

## Hinweise zur Leitplanke

- Durch diese Analyse werden keine erwarteten Status, Testfallregeln, Anforderungstexte, MRTS-Definitionen oder PASS/FAIL-Werte geändert.
- Der ausgewählte Subcluster ist nur für Metadaten bestimmt und bleibt eine Laufzeit FAIL; es wird nicht mehr als Arbeit des Körperprozessors gezählt.
- URL-encoded/form Zeilen sind reine Berichtszeilen mit MRTS DetectionOnly-Overlay-Nachweisen; Für sie wird kein Harness- oder Connectorkernwechsel vorgenommen.
- XML-Zeilen im Subcluster mit fehlender Aktivierung sind nur berichtspflichtig, da ihre Fixtures den XML-Anforderungskörperprozessor nicht aktivieren.
- Mehrteilige Zeilen im Untercluster mit fehlender Aktivierung sind nur berichtspflichtig, da ihre Fixtures keinen Zugriff auf den Anforderungstext ermöglichen, bevor FILES/ARGS_NAMES-Erfassungsnachweise erwartet werden.
- Die verbleibenden aktiven Body-Prozessor-Zeilen sind nach der Aufteilung der URL-codierten, XML und Multipart-Metadaten Null.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `c581790d4581ac9cf843e973f127b274784caf286d1661d72b5144f078049165` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
