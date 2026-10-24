# Change Record: CR-20261009-nginx-early-mapper-event-selection

**Sprache:** [English](CR-20261009-nginx-early-mapper-event-selection.md) | Deutsch

Wahrheitsgetreue Pre-Mapping-Event-Metadaten bleiben erhalten, während exakt
der native Protokollfehler ausgewählt wird.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-early-mapper-event-selection |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `407b647ce007daae5340cb87d2ead57f7ab4a730` |

## Motivation und Problemstellung

Der echte NGINX-R7-Lifecycle führte beide Common-Input-Fault-Operationen aus,
aber ihre Driver endeten mit 1. Die echten `protocol_error`-Records enthielten
korrekte Transaction, Producer, Phase und Klassifikation; `method` und `uri`
waren leer, weil die Common-Mapper-Validierung vor der Aufnahme kanonischer
Request-Metadaten scheiterte. Der Parent-Selector verlangte fälschlich `POST`
und den Case-Pfad und projizierte deshalb kein Protokoll-Event.

## Akzeptanzkriterien

Genau ein Source-Event mit geschlossenem Producer/Klassifikation, Transaction
und ausdrücklich leerer Pre-Mapping-Methode/URI auswählen. Nichtleere, fremde,
doppelte oder anderweitig abweichende Events ablehnen. Die vollständigen
JSONL-Rohbytes sowie die unabhängigen Access-, Fault-Ledger-, Konfigurations-
und Cleanup-Bindungen erhalten. Den getrennt veröffentlichten kompatiblen
Framework-Reader auf `567d36acc010a68882462b5ffe23b9e94bff5d73` pinnen,
MRTS auf `8a6bb546c4c81d8ffc7be801dceac60c6925685f` belassen und Produkt-
Event-Erzeugung sowie Required-Umfang nicht ändern.

## Implementierungsentscheidung und Begründung

Den ungenutzten Case-Pfad-Parameter aus `select_protocol_events` entfernen und
die ausdrückliche Produktform des frühen Fehlers abgleichen: `method == ""`
und `uri == ""`. Der versiegelte Access-Record, die exakt konfigurierte
Transaction, das Own-Worker-Fault-Ledger und das Cleanup-Event bleiben für die
Request-/Case-Korrelation verantwortlich. Der Framework-Reader wird getrennt
in seinem eigenen Repository geändert und veröffentlicht; diese Parent-
Änderung zeichnet den exakten kompatiblen Gitlink auf.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-common-input-fault.py`,
`tests/test_nginx_common_input_fault_driver.py` und dieses englisch/deutsche
Change-Record-Paar sowie ausschließlich der Framework-Gitlink. MRTS bleibt
unverändert.

## Ausgeführte Befehle

Fokussiertes RED: Ein Parent-Selection-Test schlug fehl, weil das authentische
leere Event als `[]` projiziert wurde (Log-SHA-256
`461c1b8193183251ed41e95b0f9137c1bef5299bfc1f663a4be8452fd60754f9`).
Fokussiertes GREEN: Alle 9 Input-Fault-Driver-Tests bestanden (Log-SHA-256
`4fc5dc5e0134547ada5ff1d3b174710981eb12804e0d87bf10178de687ee5088`).
Die erweiterte Authority-, Collection-, Dispatch-, Request-Result-, Projection-
und Wiring-Gruppe bestand alle 81 Tests in 49,519 Sekunden (Log-SHA-256
`9bf62d552ae05062da7bde89b92b22879f4e3e37375e27b7863c6403dd8fd7f4`).
Ein read-only Reproducer wählte für beide aufbewahrten R7-JSONL-Dateien exakt
ein Event aus, ohne einen der Roh-Digests zu verändern (Log-SHA-256
`742bc003f771892d75dc9424ab7f0028f8b44407c47b08f94dc212f6ddd7ee9b`).
Die nativen Change-Record-, bilingualen Dokumentations- und Linkprüfungen
bestanden.
Nach Installation des veröffentlichten Framework-Pins ließ ein absichtlich
langer Temp-Root drei unabhängige Unix-Socket-Fixtures vor ihren Assertions
scheitern (Log-SHA-256
`f5aca42afed70e7e972036ebee5c9f417cc91a9bbf611e60bcd57fa6214220c7`);
das ist weder Source-Fehler noch PASS. Der unveränderte Wiederholungslauf unter
einem kurzen zulässigen externen Root bestand alle 92 Tests in 31,976 Sekunden
(Log-SHA-256
`abfb3ca8b01569172a21bc185a05168e4c2df884fd6e24c8d6f0d0a787381f97`).
`make lint` vor dem Commit endete nach dem finalen Whitespace-Check mit Exit 0;
neun Tests wurden jedoch korrekt übersprungen, weil der committed Parent-HEAD
noch den alten Framework-Gitlink nannte, während der Worktree bereits den neuen
nannte (Log-SHA-256
`4b48d52e6c1364096cc1a313612a76201c11d88891ea4e9dc2e817fac7b725dc`).
Das ist nicht der finale Clean-Head-Lint-Nachweis und wird nach dem Commit
wiederholt.

## Security-Auswirkung

Die Änderung synthetisiert keine Request-Metadaten und lockert keine Receipt-,
Pfad-, Ownership-, Seal-, Transaction-, Worker- oder Cleanup-Prüfung. Sie
verengt die akzeptierte Event-Form auf die exakten leeren Pre-Mapping-Strings
des Produkts; nichtleere oder fremde Methode/URI sind Negativkontrollen. Die
unabhängige Security-Prüfung fand einen Evidence-Vertragsdefekt, keine
validierte Schwachstelle.

## Runtime-Evidence

Die aufbewahrte R7-Evidence belegt HTTP 400, Root-Master/nobody-Worker, Common
Return 0, exakte Mapper-Diagnose, Access-/Fault-Transaction-Bindung und Cleanup
für beide Cases. R7 bleibt FAIL mit Supervisor-/Native-Exit 2 und ohne finales
`result.json`; er wird weder umetikettiert noch wiederverwendet. Nach dem Fix
lief noch keine Native-Runtime.

## Bekannte Einschränkungen

Pure und versiegelte Fixture-Tests belegen keinen gehosteten Runtime-PASS. Ein
neues exaktes Parent-/Framework-Tupel, neu gebaute Artefakte und ein frischer
isolierter Root/nobody-Lifecycle bleiben erforderlich.

## Verbleibende Risiken

Fehlende, veränderte oder mehrdeutige Access-/Fault-/Config-/Cleanup-Evidence
muss weiterhin fehlschlagen, statt das frühe Protokoll-Event zu übernehmen. Der
frische Clean-Head-Build und Lifecycle muss außerdem jede Source-/Artefakt-
Identität neu binden.

## Nicht ausgeführte Prüfungen mit Begründung

Finaler Clean-Head-Parent-Lint, frischer Build, vollständiger 97-Record-
Lifecycle, Remote-CI/Sonar für den künftigen Head und geschützter Exact-Head
wurden an diesem Checkpoint noch nicht ausgeführt. Ruff bleibt nicht verfügbar
und getrennt NOT RUN.

## Finaler Diff- und Review-Status

Der fokussierte Implementierungs-Diff und unabhängige Code-/Security-Review
fanden kein handlungsrelevantes Problem. Der Post-Pin-Parent-Fokus mit 92
Tests, die Dokumentationsprüfungen und der Whitespace-Check sind grün. Die
Framework-Auslieferung wurde normal gepusht und auf exakt
`567d36acc010a68882462b5ffe23b9e94bff5d73` zurückgelesen; PR #137 bleibt
OPEN/DRAFT. Parent-Commit, Clean-Head-Lint und Remote-Readback stehen aus. Kein
Amend, Force-Push, Merge, Retarget oder geschützter Dispatch erfolgte.
