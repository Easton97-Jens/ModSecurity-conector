# Änderungsnachweis: CR-20261018-i12-lighttpd-pre-native-cl

**Sprache:** [English](CR-20261018-i12-lighttpd-pre-native-cl.md) | Deutsch

Exakter diagnostischer lighttpd-Prüfumfang für Content-Length-Zurückweisungen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-lighttpd-pre-native-cl |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `047d426b` |

## Motivation und Problemstellung

Die ursprünglichen Verträge von `lighttpd-stock-native-control` für `invalid_content_length`, `conflicting_content_length` und `content_length_overflow` erlauben HTTP400 vor einer Connector-Allokation. Der vorhandene gesonderte Validator wählt ausschließlich Apache-Verträge und dessen Logformat. Eine erfundene native Transaktion oder als Apache-Ausgabe umetikettierte lighttpd-Ausgabe belegt diese Diagnosefälle nicht.

## Akzeptanzkriterien

Genau diese drei unveränderten diagnostischen Mappings/Oracles zulassen. Separate Root-Freigabe von Quelle und Request, tatsächliches HTTP400, Backend0, vollständiger aktiver nativer Observer ohne Hauptaufrufe, gesunde Konstruktor-/P1-/P2-/Backend-Kontrollen sowie tatsächliche positive Common-Sinkkontrollen davor und danach, private physische Event-/Logfenster, geladene Images, alle vier Nonroot-UIDs, Prozessidentität und Cleanup bleiben Pflicht. Vollständige Lifecycle-Gutschrift bleibt falsch; verpflichtende Body-Routen erhalten keine zusätzliche Gutschrift.

## Implementierungsentscheidung und Begründung

Die ausdrückliche Profilauswahl erhält die vier bestehenden Apache-Verträge und ergänzt drei diagnostische lighttpd-Mappings. Gemeinsame Prüfungen für Quelle, Images, Isolation, native Sequenz, Events, Client und Cleanup bleiben Pflicht. lighttpd verwendet die tatsächlichen Zeilenformate seines Host-Observers und des unabhängigen Backends. Sein natives Core-Log enthält kein Apache-PID-/Clientpräfix: Der neue separate Producer bindet Device/Inode des privaten0600-Logs an den tatsächlich offenen Host-Deskriptor, umfasst das exakte Hauptintervall durch direkte Dateibeobachtungen und prüft Parserdiagnose sowie eindeutigen rohen Requestpfad/-Header mit UTC-Nanosekundenpräzision. Das Apache-Format dient nie als Fallback. Für den zurückgewiesenen Request werden weder native Allokation, Phasenaufruf, EOS, Finish noch Free erfunden.

## Geänderte Dateien

`ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`, `tests/test_i12_lifecycle_ledger.py` und dieses EN/DE-Paar. Änderungen an ursprünglicher Inventur, Oracle, Produkt, Framework/MRTS oder anderen Connectoren gehören nicht zu dieser Änderung.

## Ausgeführte Befehle

`rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/i12-lighttpd-412-completion-20261015/verification /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_i12_lifecycle_ledger tests.test_i12_oracle_reconciliation` —69 Tests bestanden, Exit0. Fünf neue lighttpd-Tests enthalten negative Mutationen für Geschwister-/TE-Verträge, veränderte Mappings, Apache-Schemaersatz, veraltete/ungenauere Zeitstempel, andere Requests, falsche FD-Inode/PID/UID/Modi, unvollständige Fenster und unkorrelierte Backends/Events. Die unveränderten vorhandenen Apache-, Normal35- und Parserregressionen bestanden ebenfalls.

## Security-Auswirkung

Dies ist eine begrenzte funktionale Reparatur des Evidenzvertrags. Produktionsparser, UID, Namespace, Dateisystemgrenzen, Compiler, CI und Quality Gate bleiben unverändert. Exploitentwicklung, Angriffspfadanalyse oder zusätzliche Sicherheitsscans finden nicht statt. Root-Quellenfreigabe und exakte Hashbindungen physischer Producer bleiben Pflicht.

## Runtime-Evidence

Externe Evidenzwurzel: `/var/tmp/codex/ModSecurity-conector/runs/i12-lighttpd-412-completion-20261015`. Der tatsächliche versiegelte Nonroot-Lauf `isolation/attempt-1792320135321593996` endete mit Controller0. Alle drei Fälle lieferten400, hatten keine nativen Hauptaufrufe und unveränderte, positive physische Eventoffsets, verwendeten davor/danach gesunde HTTP200-Kontrollen sowie separate echte403-Sinkkontrollen und beendeten die tatsächlichen Hosts mit0 und Cleanup. Device/Inode des nativen Log-FDs entsprach der direkt beobachteten Logdatei; die UIDs waren65534. Offizielle lighttpd1.4.85-Quellen `request.c`, `log.c`, `configfile.c` und unabhängige RFC9112-Bytes sind in den Quellenvorschlägen gebunden. RFC9112-SHA256: `e4f426bac6206b67fdf9e0da826154f70588db2133a0a86b15cde4ff725d8937`.

`diagnostic/proposals-pre-native-01` enthält normalisierte Receipts mit Verweisen auf direkte Producer. Die tatsächlichen gemeinsamen Prüfungen für natives Fenster, lighttpd-Core-Fenster und Producerbindung bestanden für alle drei Fälle. Dies sind Worker-Vorschläge: Dieser Worker erteilte weder Root-Freigabe noch vollständiges Fall-PASS oder Lifecycle-PASS. Die Captures behalten ihre tatsächliche Quellenidentität `2463b5d8` und Produktmodulidentität `6895649c`; sie behaupten keinen späteren P3-Fix-Build.

## Bekannte Einschränkungen

Ergänzt werden nur drei ursprüngliche diagnostische lighttpd-CL-Verträge. `duplicate_transfer_encoding`, andere Profile, Mappingfehler, reine Startfehler und Body-Streaming-Aussagen bleiben außerhalb dieses Prüfumfangs. Quellen-/Requestfreigabe, abschließende gemeinsame Qualifizierung und P3-Retakes des aktuellen Produkts bleiben Koordinatoraufgaben.

## Verbleibende Risiken

Die neuen synthetischen Tests belegen das Validatorverhalten; die getrennten physischen Captures belegen Hostbeobachtungen. Beides ersetzt keine unabhängige Root-Prüfung. Fehlende oder widersprüchliche Evidenz bleibt unqualifiziert.

## Nicht ausgeführte Prüfungen mit Begründung

Git-Lieferung oder CI-/Sonar-Ergebnisse werden nicht behauptet. Integrierte Dokumentationsprüfungen und die abschließende Diffprüfung liegen beim Koordinator. Abhängigkeiten wurden nicht installiert.

## Finaler Diff- und Review-Status

Worker-Implementierung, gezielte Regressionen und physische Helperprüfungen sind abgeschlossen. Root verantwortet Review, Quellenfreigabe, Commit, Push und Integration. Kein ursprünglicher Diagnose-Ledgerstatus wurde verändert.
