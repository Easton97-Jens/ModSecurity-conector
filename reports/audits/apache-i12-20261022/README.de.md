# Apache-I12-Hostkampagne — 22. Oktober 2026

**Sprache:** [English](README.md) | Deutsch

Die aktuelle Kampagne erfasste für jede der 155 Apache-I12-Pflichtanforderungen
eine Haupt- oder Kontrollausführung. Die unabhängige Prüfung qualifiziert
**vier vollständige native Lifecycle-PASS; 151 Ergebnisse bleiben null/offen**.
`i12_complete` ist false. Dieser Bericht erteilt keine Release- oder
Mergefreigabe. Frühere Ergebnisse bleiben im
[Bericht vom 15. Oktober](../../../docs/i12-apache-native-evidence-20261015.de.md) erhalten; ihre
Qualifikation überträgt sich nicht automatisch auf dieses Produkt und diesen Lauf.

Das maschinenlesbare [Fallledger](case-ledger.json) bewahrt die exakten
freigegebenen Entscheidungen für 155 Fälle, Original-Oracles, Einzelprädikate,
Lücken und physischen Referenzen. Der [Ausführungsindex](execution-index.json)
bewahrt die exakte unsignierte U6-Extraktion. Der
[Evidence-Index](evidence-index.json) enthält Artefakthashes und die
Kampagnenübersicht. Beobachtete Ausführung, erfüllter Fallvertrag und
qualifiziertes PASS sind getrennte Tatsachen.

## Produkt-, Prüf- und Laufidentität

| Bindung | Wert |
| --- | --- |
| Ausgeführter Produktquellstand | `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38` |
| Veröffentlichter Prüferquellstand | `de23f2fa4b490c66f15ac97f2646434351f05c5e` |
| Head des PR-Zielbranches | `76672071c3f7665dfde3340bef9e64271d6f6e70` |
| Framework-Pin | `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| MRTS-Pin, ausschließlich Identitätsmetadaten | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Run-ID | `apache-i12-batch` |
| Aufbewahrter Versuch | `attempt-1792695566065515062` |
| SHA256 der Apache-2.4.66-Binärdatei | `6e9f25c01b14cf5fb3450fdbd268d784b1d38e377a523a345dd406a4055d81ff` |
| SHA256 des beobachteten Connector-Moduls | `6d8b7bb5fb4424e0a5e2aa90f629e92efe4713faa7a387fdc62473771794daf8` |
| SHA256 von libModSecurity 3.0.14 | `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407` |

Die aufbewahrten physischen Beweise liegen unter
`/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/`.
Runtime-Controller und Treiber lieferten Exit 0, keinen Timeout, 155 stdout-Zeilen
und eine Laufzeit von 1046,93 Sekunden. Ihre Cleanup-Prüfungen bestanden.
Die Ausführungsarten waren 141 `host_http`, zehn `configtest` und vier
`host_pre_native_rejection`. Alle 155 unsignierten Zeilen melden
`execution_observed=true`; der anwendbare Lifecycle-Fallvertrag wurde in 115
Zeilen erfüllt und schlug in 26 fehl. Bei den 14 typisierten Kontrollen fehlt
dieses Prädikat beziehungsweise ist es nicht anwendbar. Exit 0 überschreibt
diese Fallergebnisse nicht.

## Qualifizierte Ergebnisse und Original-Oracles

Die vier unabhängig freigegebenen vollständigen Lifecycle-Fälle sind:

- `I12::apache-native::NEED-request-empty`
- `I12::apache-native::NEED-request-single-chunk`
- `I12::apache-native::NEED-request-csv`
- `I12::apache-native::NEED-request-eos-once`

Bei jedem dieser vier Fälle bindet das freigegebene Paket alle 35 anwendbaren
physischen Rollen an den Hauptfall; die nativen Beobachtungen sind an dieselbe
PID, denselben Lauf und dieselbe native Allokation gebunden.
Das Prüfverfahren kontrolliert getrennt P1-Sentinel-Regel, erfolgreiche native
Requestbody-Verarbeitung, Body-Append-Zahlen, Response-Verarbeitung, APR-EOS,
logischen Commit, physische Auslieferung, Finish, natives Logging, Cleanup,
Freigabe und Retirement der Zuordnung. Bei nichtleeren Requests liegt EOS vor
P2; beim leeren Request liegt der erfolgreiche P2-Return vor dem ersten leeren
APR-EOS, und dieses EOS meldet den Body als verarbeitet. Response-EOS liegt vor
P4. Präfix-/Socket-Ausgabe darf vor P4 liegen, während das logische Commit-Flag
vor der Ausgabe liegt; Terminalfreigabe folgt auf erfolgreiches P4, Cleanup auf
P4, Terminalfreigabe und physischen Socket-Return. Folge- und Nachbarkontrollen
sind unabhängige physische Requests.

Dieser begrenzte Nachweis überträgt sich nicht auf ProcessPartial, natives
Reject, Transport-Trunkierung, MIME-/Charset-Mapping oder andere Body-/Chunk-
Familien. Diese Zeilen behalten ihre einzelnen null-Ergebnisse und fehlenden
Prädikate.

Der unveränderte gemeinsame Lifecycle-Validator akzeptierte alle vier geprüften
Pakete. Das gemeinsame Ledger meldet vier frisch ausgeführte vollständige
Lifecycle-PASS sowie vier gelöste ursprünglich offene Oracles von 54;
**50 ursprünglich offene Oracles bleiben offen**. Quellenbasierte Oracle-Prüfung
und physische Lifecycle-Qualifikation sind getrennte Anforderungen.
Originalerwartungen und frühere Fehlerbeweise bleiben erhalten; allein das
Ändern einer Erwartung erzeugt kein PASS.

Das Prüfinventar für 155 Zeilen enthält 74 Fälle mit fehlender unabhängiger
Erwartungs- und Familienprüfung, elf mit zusätzlichen fehlenden
Familienprädikaten, 14 typisierte Kontrollen, 24 physische Fehlerfälle,
24 Sonderoperationsfälle, vier registrierte Request-Fälle und vier fehlende
unabhängige native Header-/MIME-Weitergabebeweise. Diese Kategorien beschreiben
Prüfabdeckung und Lücken, keine weiteren PASS-Ergebnisse.

## Verbleibende Beweislücken und Widersprüche

Keine der zehn Konfigurations- oder vier Pre-Native-Kontrollen qualifiziert sich
in dieser Kampagne. Allen zehn Konfigurationsprozessbelegen fehlen acht
geforderte Bindungsfelder und unabhängige Erwartungsquellen. Der Fall mit
unsicherem Eventpfad meldet tatsächlich `Syntax OK` und widerspricht seinem
Reject-Oracle. Der Fall mit ungültiger Größe und die zwei Scope-Fälle scheitern
an einer unbekannten Direktive; das belegt ihre beabsichtigte
Konfigurationssemantik nicht.

Die Pre-Native-Fälle 017, 018 und 020 liefern HTTP 400, enthalten jedoch nicht
die geforderte Apache-Diagnose und zeigen doppelte native Sequenzen. Fall 019
liefert HTTP 500 mit nativer Allokation, P1, Finish und Cleanup sowie
Proxy-Diagnose `AH01093`; er belegt weder eine Pre-Native-Ablehnung noch die
ursprüngliche HTTP-400-Erwartung. Dies sind beobachtete Widersprüche oder
fehlende Beweise, keine freigegebenen Produktkorrekturen.

Die Duplicate-Header-Qualifikation bleibt offen. Der Apache-2.4.66-Core-Quellcode
stützt den versionsgebundenen HTTP/1.x-APR-Mergewert `one, two`; die aktuelle
Prüfung hat die vollständige unabhängige Kette aus Wire, Core, Connector-Mapper
und nativer Engine nicht freigegeben. Original-Oracle und Fehler bleiben
erhalten. Die fünf bekannten physischen Sinkfälle—ungültiger Eventpfad,
`/dev/full`, nicht beschreibbarer Sink, geschlossener Descriptor und ENOSPC—wurden
erneut ausgeführt. Ihre aktuelle Prüfkategorie bleibt unqualifiziert; eine
Ausführung belegt nicht sämtliche geforderten APR-Rückgaben, Hostaktionen,
Clientverhalten, physisches JSONL, Cleanup- und Wiederherstellungsbeobachtungen.

Die frischen physischen Beobachtungen haben in allen fünf Fällen dieselbe
Client- und Wiederherstellungsform: Der Hauptclient endete mit Exit 0, HTTP 500
und 571 Entity-Bytes; seine Backendanzahl war null. Getrennte Folge- und
Nachbarclients endeten jeweils mit Exit 0, HTTP 200, drei Entity-Bytes und einem
Backendrequest. Common- und natives Cleanup wurden jeweils einmal beobachtet,
über den Hauptrequest kam kein Descriptor hinzu, und der Controller meldete
weder verbleibende Namespace-Prozesse noch Lecks außerhalb des Mounts.

| Fehler | Frische physische Grenze | Vertrags-/Prüfgrenze |
| --- | --- | --- |
| Ungültiger Eventpfad | Kein APR-Aufruf erfasst | Unabhängige Common-/POSIX-Erstursache und Verbindung zu nativer Regel `120016` fehlen |
| `/dev/full` als konfigurierter Sink | Kein APR-Aufruf erfasst | Dieselbe fehlende Erstursachen-/Regelverbindung |
| Nicht beschreibbarer Sink | Kein APR-Aufruf erfasst | Dieselbe fehlende Erstursachen-/Regelverbindung |
| Geschlossener Descriptor | `apr_file_write_full` lieferte 9/`EBADF`, 0 von 1067 Bytes; Close lieferte 9 | Ausgeführter Fallvertrag vollständig, aber keine unabhängige Freigabe der physischen Fehlerfamilie |
| Physisches ENOSPC | `apr_file_write_full` lieferte 28/`ENOSPC`, 0 von 1065 Bytes; Close lieferte 0 | Ausgeführter Fallvertrag vollständig, aber keine unabhängige Freigabe der physischen Fehlerfamilie |

Alle fünf zeigen im aktuellen Capture null Common-Finish-Aufrufe und einen
nativen Logging-Aufruf; deshalb wird keiner zum vollständigen Lifecycle-PASS.
Das Fehlen einer APR-Zeile bei den ersten drei bleibt fehlende Evidence und wird
nicht aus der historischen Kampagne ergänzt.

Weitere Qualifikation benötigt unabhängige familienbezogene Prüfung und dort,
wo den gemeinsamen Produzenten geforderte typisierte Beobachtungen fehlen,
eine getrennt abgegrenzte Integration. Fehlende Beobachtungen bleiben null.
Dieser Evidence-Bericht gibt keine produktive Apache-Korrektur frei.

## Verifikation und Freigabegrenze

| Prüfung | Beobachtetes Ergebnis |
| --- | --- |
| Vollständige Apache-I12-Testsuche | 387 Tests, Exit 0; fünf ausdrückliche Skips |
| Fokussierte Batch-/Finalprüfer-Tests | 52 Tests, Exit 0; zwei ausdrückliche Skips |
| Native-/Helper-Regressionen | insgesamt 67 Tests, Exit 0; ein Root-DAC-Skip |
| Gemeinsame Lifecycle-Ledger-Regressionen | 40 Tests, Exit 0 |
| Python-Kompilierung und `git diff --check` | Exit 0 |

Die fokussierten Negativtests umfassen mehrdeutige Observer-Finals,
EOS-Reihenfolge bei leerem Body, Terminalfreigabe nach Finish, ungültige
physische Socket-Beobachtungen, Änderung des Prüferquellcodes und unveränderliche
Retest-Referenzen. Synthetische Tests prüfen das Prüferverhalten; sie erzeugen
keine nativen Host-PASS.

Die TAC-Abfrage vom `2026-10-22T20:59:23.107554+00:00` meldete `granted`, `tac1`,
Quelle `user`. Diese Kampagne behandelt das als die genannte DrayTek-Blue-Grenze
und führt defensive Test-, Build- und Evidence-Arbeit im autorisierten privaten
Umfeld aus. Keine fehlende Sicherheitsfreigabe blockiert die hier berichtete
Arbeit. Die verbleibenden Grenzen sind fehlende oder widersprüchliche Beweise
und getrennt abzugrenzende gemeinsame Produzentenarbeit. Offensive Vertiefung
wurde weder ausgeführt noch als erledigt dargestellt.
