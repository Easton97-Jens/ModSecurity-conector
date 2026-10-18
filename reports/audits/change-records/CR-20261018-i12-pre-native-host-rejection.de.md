# Change Record: CR-20261018-i12-pre-native-host-rejection

**Sprache:** [English](CR-20261018-i12-pre-native-host-rejection.md) | Deutsch

Dedizierter Evidence-Umfang für Host-Ablehnungen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-pre-native-host-rejection |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `2c38d0ff2960a9ff2a76291955e808683febf06e` |

## Motivation und Problemstellung

Die vier ursprünglichen Apache-Verträge für fehlerhafte Header erlauben eine Host-Ablehnung vor der Connector-Allokation mit sichtbarem Status 400 und logischer Phase 1. Ein normales natives Lifecycle-Paket mit 35 Feldern kann das Fehlen einer nativen Allokation nicht wahrheitsgemäß beschreiben. Diese Änderung ergänzt einen eng begrenzten Validator, ohne das ursprüngliche Oracle zu ändern oder eine native Transaktion zu erfinden.

## Akzeptanzkriterien

Nur `invalid_content_length`, `conflicting_content_length`, `duplicate_transfer_encoding` und `content_length_overflow` mit ihren exakten ursprünglichen Mappings und Oracles dürfen den dedizierten Umfang verwenden. Erforderlich sind eine separate Root-Quellenfreigabe sowie physische Prozess-, Wire-, Core-, Backend-, Image-, Config-, Isolations-, Native-, Ereignisfenster-, Cleanup- und Kontrollnachweise. `full_case_qualified` ist nur für `host_pre_native_rejection` wahr; `full_lifecycle_qualified` bleibt falsch. Die bestehenden Prüfungen für normale 35-Feld-Pakete und Konfigurationsfälle bleiben unverändert.

## Implementierungsentscheidung und Begründung

Der neue Validator `reviewed_pre_native_packet` liest die bestehenden Apache-Datensatzformen für Client, Prozess, `native-lifecycle-v1`, Host und Backend. Er verlangt eine vollständige Sequenz des nativen Observers, null native Aufrufe für den Hauptfall, positive Konstruktor- und API-Kontrollen davor und danach, ein unabhängiges Ereignisfenster ohne Hauptfall-Ereignis mit tatsächlichen Common-JSONL-Kontrolldatensätzen, die mit beobachteten nativen Allokationen verbunden sind, tatsächliche 400-Header, null Backendrequests, eine passende Core-Diagnose im UTC-Fenster des Clients sowie Bindungen an Quelle, Konfiguration, Regeln, Images, UID, PID und Cleanup. `build_ledger` verzweigt nur für den expliziten `execution_kind` und zählt vollständige Fälle getrennt von vollständigen Lifecycles. Der benachbarte Validator für typisierte Abwesenheiten akzeptiert nun die tatsächliche native Identität und die exakten Wörterbücher für Finish-/Free-Zähler. Eine physische Nullereignis-Behauptung liest die unveränderlichen Sink-Bytes, prüft begrenzte gleiche Offsets für den Hauptfall und die vollständige Abdeckung des Clientfensters und verbindet nicht leere Common-JSONL-Kontrollbereiche davor und danach mit erfolgreichen nativen Allokationen; Observer-Receipts, die nur Flags enthalten, werden verworfen.

## Geänderte Dateien

`ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`; `tests/test_i12_lifecycle_ledger.py`; `ci/evidence/reports/generate-pr382-i12-oracle-reconciliation.py`; `tests/test_i12_oracle_reconciliation.py`. Dieses Change-Record-Paar dokumentiert den dedizierten Pre-Native-Umfang. Der integrierte Change Record für Capture und Abwesenheiten gehört dem Koordinator.

## Ausgeführte Befehle

`rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/resume-20261018 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i12_lifecycle_ledger tests.test_i12_oracle_reconciliation` — 54 Tests bestanden, Exit 0. Ein AST-Vergleich mit der Basis bestätigt, dass die Konstanten und bestehenden Validatorfunktionen für normale 35-Feld-Pakete und Konfigurationsfälle unverändert sind. `rtk proxy git diff --check` bestand. Der Koordinator verantwortet die abschließende Prüfung des integrierten Diffs. `rtk proxy python3 ci/tools/new-change-record.py check` bestand und prüft nur die Struktur. Der Koordinator band den exakten Gitlink des Frameworks `99a7985c1be92a2297b1b59208f64df6768f2cbf` in einen privaten schreibgeschützten Namespace ein und führte `make check-bilingual-docs` sowie `make check-doc-links` erneut aus; beide bestanden mit Exit 0. Das Namespace-Receipt bestätigt den unveränderten Gitlink und das Ausbleiben entwichener Mounts. Das englische und deutsche Dokument wurden manuell auf sachliche Parität geprüft.

## Security-Auswirkung

Die Grenze schützt die Integrität der Evidence: Eine fehlende native Allokation oder fehlende Observer-, Cleanup- oder Core-Daten können nicht als bestandener nativer Lifecycle gelten. Root-Review, unveränderliche ausgewählte Verträge und unabhängige revisionsgebundene Quellenbeweise bleiben verpflichtend. Kein Produktparser und keine Authentifizierungs-, Isolations-, Compiler- oder CI-Kontrolle wird geschwächt.

## Runtime-Evidence

Es wurde kein Host gestartet und weder ein Runtime-PASS noch eine Root-Freigabe erzeugt. Die schreibgeschützte Prüfung der Baseline verwirft alle vier Kandidaten des dedizierten Umfangs: `invalid_content_length`, `conflicting_content_length` und `content_length_overflow` lieferten 400, besitzen aber keine positive Konstruktor-/API-Kontrolle vor dem Hauptfall. `duplicate_transfer_encoding` lieferte 500 und weist native Aktivität im Hauptfall auf. Diese Fälle sind keine qualifizierten Pre-Native-PASS. Die Evidence liegt unter `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/resume-20261018/`.

## Bekannte Einschränkungen

Der neue Umfang qualifiziert ausschließlich eine unabhängig belegte Host-Ablehnung vor der nativen Verarbeitung. Jedes andere Verhalten behält seinen ursprünglichen Vertrag und benötigt den passenden nativen Lifecycle- oder Fehlernachweis. Core-Diagnosen verlangen derzeit das tatsächliche Apache-Zeitformat in UTC. Den Baseline-Captures fehlen die erforderlichen positiven Kontrollen vor dem Hauptfall sowie unabhängige Nachweise für Ereignisfenster und Core-Diagnose. Physische Wiederholungstests und Root-Freigaben bleiben Integrationsarbeit.

## Verbleibende Risiken

Synthetische positive und negative Tests belegen das Verhalten des Validators, nicht die Semantik eines laufenden Hosts. Root muss die Herkunft der physischen Beobachtungen und die Quellenfreigabe vor der Qualifikation prüfen. Kein vorhandenes 500-Ergebnis wird in 400 umgedeutet.

## Nicht ausgeführte Prüfungen mit Begründung

Host-Retests wurden nicht ausgeführt, weil dieser Worker keine Berechtigung zum Hoststart hatte. Ruff wurde mit der virtuellen Umgebung des Parent-Repositories aufgerufen, ist dort aber nicht verfügbar (`No module named ruff`); es wurde kein Paket installiert. Es fanden keine Git-Lieferung und keine Schreibzugriffe auf Framework oder MRTS statt; die Dokumentationsprüfungen verwendeten ausschließlich private schreibgeschützte Bindings.

## Finaler Diff- und Review-Status

Der begrenzte Code- und Testumfang wurde gegen die ursprünglichen Verträge geprüft; nicht zugehörige ausstehende Capture-Dateien wurden bewahrt. Die ASTs der Validatoren für normale 35-Feld-Pakete und Konfigurationsfälle sind unverändert. Alle neuen Ergebnisse bleiben von der Anrechnung eines vollständigen Host-Lifecycles getrennt. Es wurde weder committet noch gepusht, kein PR aktualisiert und nichts gemergt.
