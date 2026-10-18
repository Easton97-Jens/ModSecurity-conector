# Change Record: CR-20261015-i12-parser-packets-workflow-pin

**Sprache:** [English](CR-20261015-i12-parser-packets-workflow-pin.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-parser-packets-workflow-pin |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `850879e82ea729f274cb383507b05938df06027a` |

## Motivation und Problemstellung

Ursprüngliche Konfigurationstestverträge benötigen ihren bestehenden Parser-Paketpfad im aktuellen Ledger; reine HTTP-Lifecycle-Regeln beschreiben Parserkontrollen nicht. Zwei HAProxy-Workflow-Assertions erwarten zusätzlich einen abgelösten Upload-Artifact-Pin.

## Akzeptanzkriterien

Konfigurationskontrollen getrennt qualifizieren, unabhängig geprüfte physische Parserevidence verlangen, ursprüngliche IDs/Verträge/Historie erhalten und ausschließlich veraltete Testerwartungen auf den bereits eingesetzten Upstream-Pin korrigieren. Aus Validatortests kein Host-Lifecycle-PASS vergeben.

## Implementierungsentscheidung und Begründung

Das aktuelle I12-Abnahmeledger leitet ursprüngliche `actual_configtest`-Verträge
jetzt an den bestehenden Qualifier für `configuration_parser`-Pakete weiter.
Die veröffentlichte Paket-API und ihr Ergebnis
`configuration_control` / `full_case_qualified` bleiben erhalten. HTTP-Hostpakete
benötigen weiterhin ihre ursprünglichen 35 Beobachtungen.

Die Parserqualifikation erfordert eine Root-Prüfung der exakten Original-ID und
Route, revisionsgebundene Quell-/Konfigurations-/Regeleingaben, physische Bytes des
tatsächlich aufgerufenen Hosts und nativen Moduls, einen separaten physischen
Parserprozessbeleg, physisches stdout und stderr, Cleanup- und Isolationsbelege
sowie eine getrennte versionierte unabhängige Erwartungsquelle. Der Prozessbeleg
muss mit exakten argv, cwd, abgewartetem Exit, Signal, Imagehash und Lauf-/
Eingabeidentitäten des Pakets übereinstimmen. Controllerexits und selbstreferenzielle
Belege ersetzen keine Parsermessung.

Die drei ursprünglichen Pflichtbeobachtungen werden ohne Änderung des ausgewählten
Vertrags abgebildet: Parserausführung auf `parser_process`; Quell-/Host-/Modul-/
Konfigurationsidentität auf `invocation_identity` und `source_config_binding`;
erwartete Annahme/Ablehnung auf das unabhängig geprüfte effektive Oracle und
seinen Hash. Ein Parser-PASS hat `full_lifecycle_qualified=false`, steht unter
`current_configuration_packet` und zählt ausschließlich zur getrennten aktuellen
Konfigurationsbilanz. Historische Zeilen, Original-IDs und ursprüngliche
Erwartungen bleiben unverändert.

Erwartete Annahme verlangt normalen Exit 0; erwartete Ablehnung den ursprünglichen
exakten Exit 1. Exit 77 wird nicht zur erfolgreichen Ablehnung. Eine gemessene
Abweichung kann als FAIL erhalten bleiben; eine widersprüchliche PASS-Behauptung
wird zurückgewiesen. Beim ursprünglichen Vertrag für fehlende Regeln wird kein
Dateihash erfunden: `rules_sha256` ist null und `rules_absence_sha256` bindet einen
physischen `lstat`-/ENOENT-Beleg mit dem exakten versuchten absoluten Pfad, ohne
beobachtete Symlinkkomponenten und mit passender Prozess-/Laufidentität. Fälle mit
vorhandenen Regeln behalten die physische Regeldateibindung.

Validierung: Die exakten Belege unter `qualifier-config/` enthalten den erfassten
pytest-Lauf mit Python 3.14.7, Regressionen gegen den Ausgangsstand, Prüfungen der
unveränderlichen 1.484 IDs und Quellauswahl, Dateihashes und Whitespaceprüfung.
Diese Qualifierkontrollen sind synthetisch und vergeben selbst keinen HAProxy-
Parser- oder Lifecycle-PASS.

## Geänderte Dateien

`ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`, `tests/test_i12_lifecycle_ledger.py`, `tests/test_haproxy_evidence_workflow_contract.py` und dieses EN/DE-Change-Record-Paar. Keine Änderung an Workflow, Security-Lock, Produkt oder gemeinsamer Paket-API.

## Ausgeführte Befehle

Tatsächliches Parser-/Ledger-pytest unter CPython 3.14.7: 33 Tests und 57 Subtests bestanden, Exit 0. Exakter Befehl: `rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m pytest -q tests/test_i12_lifecycle_ledger.py tests/test_i12_oracle_reconciliation.py`. Receipt: `qualifier-config/integrated-after.json`; Quellinvarianten, Basisfehler und Ausgabehashes liegen daneben. Workflowtests: 12 bestanden; exakter Befehl/Exit und Upstream-Tagbytes liegen in `workflow-pin/after-receipts.json`. Die kanonische Vorlage wurde mit `rtk proxy python3 ci/tools/new-change-record.py create --name i12-parser-packets-workflow-pin --base-revision 850879e82ea729f274cb383507b05938df06027a --date 2026-10-15` erstellt.

## Security-Auswirkung

Der veraltete erwartete `actions/upload-artifact`-Pin in den HAProxy-Evidence-
Workflow-Vertragstests wurde von v7.0.1 auf v7.0.2 mit Commit
`cf430e030ddbb5b0abf93d22962f4752f3646cd9` korrigiert. Der offizielle GitHub-API-
Endpunkt `https://api.github.com/repos/actions/upload-artifact/git/ref/tags/v7.0.2`
bestätigt unabhängig, dass das Upstream-Tag direkt auf diesen Commit verweist.
Der versionierte Security-Tools-Lock und der bestehende Workflow verwenden
bereits genau diese Version und SHA. Workflow, Lock, Upload-Grenzen und Assertions
wurden nicht abgeschwächt.

Die beiden Tests mit veraltetem Pin schlugen vor der Korrektur fehl. Anschließend
bestand der gezielte pytest-Lauf mit Python 3.14.7 alle 12 Tests. Exakte Befehle,
Prozessexits, Upstream-Antwortbytes und Quell-/Ausgabehashes liegen unter
`workflow-pin/`.

## Runtime-Evidence

Validator-Regressionskontrollen sind synthetisch. Hier wird kein frisches HAProxy-Parser-Host-PASS oder vollständiges Lifecycle-PASS vergeben. Aktuelle Konfigurationspakete zählen ausschließlich in der Konfigurationsspalte mit `full_lifecycle_qualified=false`; HTTP-Pakete behalten ihr ursprüngliches Gate mit 35 Beobachtungen.

## Bekannte Einschränkungen

Parsereingaben verlangen ein separates physisches Prozessreceipt und eine unabhängige Erwartungsquelle. Reine Controllerexits, Selbstreferenzen und Exit 77 belegen keine erfolgreiche Ablehnung. Evidence fehlender Regeln erfasst physische Abwesenheit statt eines erfundenen Dateihashes.

## Verbleibende Risiken

Integrierte Runtimequalifikation hängt weiterhin von tatsächlichen neu gebauten Host-/Modulimages und unabhängig gemessenem Parser- oder Transportverhalten ab. Historische Zeilen und unveränderliche 1.484-ID-/Quellauswahlen bleiben erhalten; die gezielten Tests belegen nicht die Runtimebereitschaft aller Connectoren.

## Nicht ausgeführte Prüfungen mit Begründung

Diese Parser-/Pintests beanspruchen keine frische private Hostabnahme, Hosted CI am finalen Head oder serverseitiges Sonar-Ergebnis. Diese benötigen eigene beobachtete Ausführung und Qualifikation.

## Finaler Diff- und Review-Status

Nur die drei aufgeführten Quell-/Testdateien und dieses Record-Paar gehören zum Umfang. Quellgebundene Parserprüfungen, ursprüngliche Auswahlinvarianten und Workflow-Pin-Regressionen bestehen auf ihren berichteten Ebenen; finale Runtimeabnahme und Gitlieferung bleiben separat. Kein Gate, keine Assertion und keine ursprüngliche Anforderung wird geschwächt.
