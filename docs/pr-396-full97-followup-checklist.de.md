# PR #396 — Full97-Folgearbeit

**Sprache:** [English](pr-396-full97-followup-checklist.md) | Deutsch

Aktualisiert: 2026-10-10. [Draft PR #396](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396).
Nur die freigegebene NGINX-R13-Folgearbeit; die [übergeordnete PR-382-Checkliste](pr-382-checklist.de.md) bleibt unverändert. Keine I09–I12-/Cross-Connector-/Secret-Scan-Abnahme.

## Revisions- und Evidence-Vertrag

- Tested baseline Parent: `dca17fd5690c2ec2b8806024d1061744db8c3ad8`.
- Tested baseline Framework: `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9`.
- MRTS: `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.
- Current Parent: `dca17fd5690c2ec2b8806024d1061744db8c3ad8`.
- Current Framework: `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9`.

R13 bleibt unverändert: 97 Required = 80 originale Case-PASS / 9 FAIL / 8 NOT_EXECUTED; zusätzlich vier Aggregat-Schemafehler für zwei dieser MIME-Case-PASS. Make/Supervisor 2, Canonical FAIL, Validator 1. Kein neuer Full97; Freigabe **NEIN**. Protected **BLOCKED / NOT RUN**.

Code implementiert, Fokus geprüft und Full97 bestätigt sind verschiedene Meilensteine. Dokumentationscommits erben keinen Runtime-Nachweis. Jeder erledigte Punkt verweist auf einen SHA-gebundenen Nachweis; lokale Dateien sind keine öffentlichen GitHub-Downloads.

Lokaler Task-Nachweis: `/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-followup-20261010T084822Z/`. `baseline-reconciliation.json` und `issue-record-matrix.csv` lesen ausschließlich historische Inputs; **NOT A NEW RUNTIME RUN**. B0–B3, D1, E1–E2: Parent/Framework-Baseline-SHAs oben; Readback und Originalvergleich bestehen, kein Fixcommit, keine neue Runtime. Originalbericht: `/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-dca17fd5-20261009T225409Z/report.md`.

## B — Baseline

- [x] B0: Aktuelle Revisionen, Branches, Gitlinks und erhaltenes R13 prüfen. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] B1: Alle neun ursprünglichen FAIL-Records zuordnen. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] B2: Alle acht ursprünglichen NOT_EXECUTED ihrer ersten fehlenden Grenze zuordnen. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] B3: Vier verschachtelte Fehler den zwei MIME-Allow-Case-PASS zuordnen. (`baseline-reconciliation.json`; baseline SHA binding above).

## A — Interventionswerte

- [ ] A1: Ungültige Eventsequenz reproduzieren.
- [ ] A2: Producer, überschriebene Felder und maßgeblichen Beobachtungszeitpunkt bestimmen.
- [ ] A3: Rote Regressionen nachweisen.
- [ ] A4: Minimale identitätsgebundene Korrektur implementieren.
- [ ] A5: Positiv-, technische Fehler-, Cross-TX- und Prioritätskontrollen bestehen.
- [ ] A6: Echten begrenzten Host-Fokus prüfen.
- [ ] A7: Integrieren und getesteten SHA binden.
- [ ] A8: Originalstatus in neuem Full97 bestätigen (Freigabe erforderlich).

## B — First-Byte-Snapshot

- [ ] B4: Invocation-/Zeit-/Countervertrag bestimmen.
- [ ] B5: Fehlerhafte Snapshotbindung und rote Kontrollen reproduzieren.
- [ ] B6: Korrigieren und veraltete/falsche Zeit-/TX-/Invocation-Snapshots ablehnen.
- [ ] B7: Echten kausalen First-Byte-Fokus mit vollständiger Safe-Antwort ausführen.
- [ ] B8: Integrieren und getesteten SHA binden.
- [ ] B9: In neuem Full97 bestätigen (Freigabe erforderlich).

## C — Native H1-Bindung

- [ ] C1: Beobachtetes Protokoll über Operation/Receipt/Event nach Canonical verfolgen.
- [ ] C2: Erste fehlende Identitätsbindung reproduzieren.
- [ ] C3: Strikt korrigieren; Protokoll-/Identitäts-/Artefakt-Negativkontrollen erhalten.
- [ ] C4: Echten nativen H1-Fokus prüfen.
- [ ] C5: Framework und Parent konsistent integrieren.
- [ ] C6: In neuem Full97 bestätigen (Freigabe erforderlich).

## D — MIME-Gesamtschema

- [x] D1: Vier Fehler getrennt von zwei Case-PASS erfassen. (`baseline-reconciliation.json`; baseline SHA binding above).
- [ ] D2: Case-Result, Producer, verschachteltes Aggregat und Validator verfolgen.
- [ ] D3: RED über tatsächliche dynamische Aggregation nachweisen.
- [ ] D4: Eng begründeten schemakonformen Vertrag implementieren.
- [ ] D5: Beide echten MIME-Allow-Cases und Mismatchkontrollen prüfen.
- [ ] D6: Integrieren und getesteten SHA binden.
- [ ] D7: Neues Full97-Aggregat validieren (Freigabe erforderlich).

## E — Acht abgeleitete Records

- [x] E1: Jeden Record seiner ersten blockierten Grenze zuordnen. (`baseline-reconciliation.json`; baseline SHA binding above).
- [x] E2: A–D-Abhängigkeiten von unabhängigen Ursachen unterscheiden. (`baseline-reconciliation.json`; baseline SHA binding above).
- [ ] E3: Freigegebene Korrekturen und begrenzte Fokusnachweise abschließen.
- [ ] E4: Frische Originalstatus im Full97 messen (Freigabe erforderlich).

## Q — Integration und Qualität

- [ ] Q1: Erfolgreiche bestehende Regressionen erhalten.
- [ ] Q2: Erforderliche Parent-/Framework-Tests und Lint bestehen.
- [ ] Q3: Gitlinks und verifizierte Remote-Heads binden.
- [ ] Q4: Frische CI/Sonar des aktuellen Heads zurücklesen.
- [ ] Q5: EN/DE-Checkliste und PR-Beschreibung abgleichen.

## F — Gesamtabnahme

- [ ] F1: Ausdrückliche Freigabe für einen neuen Full97 erhalten.
- [ ] F2: Neuen Full97 tatsächlich ausführen.
- [ ] F3: Gesamtes frisches Aggregatschema validieren.
- [ ] F4: Gültige Evidence für jeden Required-Record prüfen.
- [ ] F5: Canonical PASS und tatsächliche Lifecycle-/Validator-Exits prüfen.
- [ ] F6: Vollständiges Cleanup und frische Prüfsummen prüfen.

## P — Protected, separat

- [ ] P1: Trusted Base unabhängig freigeben.
- [ ] P2: Zulässige Basis-/Gitlink-/Workflow-Bindung prüfen.
- [ ] P3: Runner und Environment administrativ prüfen.
- [ ] P4: Exact-Base-Host-Gate prüfen.
- [ ] P5: Zulässigen geschützten Lauf starten und auswerten.

## Record-Zuordnung und Rest

A: `phase3_deny_before_commit`, `phase3_redirect_before_commit`, `phase4_deny_after_commit_log_only`, `phase4_deny_after_commit_abort`, `phase4_deny_after_commit_log_only_safe`. A+B: `phase4_rule_observed`, `phase4_no_full_response_buffering`, `phase4_first_byte_before_response_end`. C: `phase4_strict_http1_client_abort`.

Die acht Pending sind geschlossene Ableitungen blockierter Basis-Records, keine pauschal fehlenden Drivers:

| Record | Basis / Grenze |
| --- | --- |
| phase4_event_contains_original_status | A: phase4_deny_after_commit_log_only / phase4_deny_after_commit_abort |
| phase4_event_contains_late_intervention_action | A: phase4_deny_after_commit_log_only / phase4_deny_after_commit_abort |
| event_has_no_response_body_payload | A+B: phase4_rule_observed |
| phase3_original_and_visible_status | A: phase3_deny_before_commit |
| phase4_deny_after_commit_abort_strict | A: phase4_deny_after_commit_abort |
| phase4_status_metadata | A: phase4_event_contains_original_status |
| phase4_action_metadata | A: phase4_event_contains_late_intervention_action |
| phase4_no_payload_event | A+B: event_has_no_response_body_payload |

D: `phase4_out_of_scope_content_type` und `phase4_missing_content_type` bleiben Case-PASS. Je `requested_action` und `actual_action` = String `allow` verletzen das verschachtelte Enum in `$.phase4_case_results[17]` / `[18]`, insgesamt vier Schemafehler. Kein vierfacher Runtime-FAIL.

Offen: A/B/C/D test-first reparieren, reale begrenzte Fokusproben, konsistente Integration, aktuelle Qualitätsgates. `issue-record-matrix.csv` enthält alle 97 Records samt Originalstatus, Operation, Raw-Evidence, Grenze, Owner und Abhängigkeit; neue Fokus-/Full97-Spalten bleiben separat. Keine Required-Verkleinerung und keine historischen Statusänderungen.

