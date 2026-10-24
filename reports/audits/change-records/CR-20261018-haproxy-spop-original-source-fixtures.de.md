# Change Record: CR-20261018-haproxy-spop-original-source-fixtures

**Sprache:** [English](CR-20261018-haproxy-spop-original-source-fixtures.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-spop-original-source-fixtures |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `8582074ce1efc0df330277c1c2514d762f17afab` |

## Motivation und Problemstellung

Quellgebundene Ausführungsdefinitionen für die 94 eingefrorenen Original-IDs von `haproxy-spop-request` vorbereiten: 91 Transaktionsfälle und drei Konfigurationsfälle. Jeder Originalvertrag bleibt erhalten; konkrete Quellerwartungen werden von späteren Hostbeobachtungen getrennt. Die beschädigte NOTIFY-Kontrolle wird korrigiert, ohne einen historischen Harnessfehler einer neuen Original-ID zuzuordnen.

## Akzeptanzkriterien

Alle 94 Originalzugehörigkeiten und Hashes prüfen; ungeklärte native Erwartungen oder Injektionen erhalten; tatsächliche SPOP-Tags, Body-Samplelänge, `req.body_size`, HTTP-Version und Frameidentitäten erfassen; Hauptverkehr und gesunden Nachbarn trennen. Unittests müssen abgeschnittene Frames, widersprüchliche Metadaten, Inspektionsbehauptungen für ungeframtes HTTP/2 und unvollständiges Response-Framing zurückweisen. Echte Hostabnahme bleibt eine separate Anforderung.

## Implementierungsentscheidung und Begründung

Das Quellmodul bindet jeden Originalvertrag an seinen Hash und erhält dessen Original-Oracle. Kanonische Regeln und YAML-Regeln bleiben quellgebunden. Explizite native Requestlimits verwenden `Reject` oder `ProcessPartial`. Der Treiber erfasst einen unabhängig abgewarteten Client, korrelierte NOTIFY-/ACK-Identitäten, rohe Wirebytes, Backendrequests, Prozesszustände und Shutdown-Belege. Eine Diagnose-ID erhält durch ein eingehendes historisches `case_id` keine Originalzugehörigkeit.

Samplefehler gelten nur für den Hauptrequest. TTL-Fixtures mit gehaltener Transaktion verwenden für den Nachbarn ein separates sauberes Frontend im selben Host und Agenten; daraus folgt keine Response-Companion-Qualifikation dieses Requestprofils. Konstruierte Pakete sind als Komponentenfixtures gekennzeichnet und niemals Hostbeobachtungen.

Die Prüfung vor Hoststart fand einen Harness-Oraclefehler in `source-fixtures-v1`: Erwartete Interventionsphase 1 wurde fälschlich als Phasengrenze behandelt. Der tatsächliche öffentliche Aufrufer `begin_atomic_request` überspringt die Requestbody-Finalisierung nur nach einer tatsächlichen disruptiven P1-Entscheidung. Version 2 ändert 17 ausgewählte Definitionen einschließlich unkritischer Transaktions-ID- und Sequenzfälle; alle Originalvertragshashes bleiben erhalten. Version 1 bleibt unveränderlich und erhält die Einstufung `HARNESS_DEFECT`; Hostresultate werden nicht übertragen. Neue Kontrollen unterscheiden P1 Allow von P1 Deny/Redirect und binden dies an den primären Aufruferquelltext.

Eine weitere unabhängige Prüfung vor Hoststart fand, dass Version 2 plausible verwaiste ACKs akzeptierte, zusätzliche/doppelte ACKs und Aktionstypen ignorierte, Integer-/String-IP-Metadaten entgegen dem nativen `read_typed_ip_to_buffer` akzeptierte und Dateien ohne Verzeichnisse versiegelte. Version 3 weist diese Beobachtungen zurück, verlangt übereinstimmende Verbindung/Stream/Frame sowie gültige Richtungen/Envelopes/Typen/Scopes, prüft endliche Inspektionsbehauptungen gegen tatsächliche Samples, erzeugt echte gepackte IPv4-/IPv6-Tags `6`/`7` und versiegelt den gesamten physischen Baum. Negativtests prüfen den tatsächlichen Evaluator mit korrekten HTTP-/Backenddaten plus verwaistem ACK und verlangen einen Fehler. Alle 94 ausgewählten Originaldefinitionen und Oracles bleiben gegenüber Version 2 identisch.

Version 4 ergänzt die in Version 3 fehlende explizit aktivierte native Audit-/Debug-Beobachtungskonfiguration: `SecAuditEngine On`, `SecAuditLogType Serial`, `SecAuditLogParts ABFHZ`, `/task/native-audit.log`, `/task/native-debug.log` und `SecDebugLogLevel 9`. Kanonische Regeln und native Bodylimits bleiben erhalten. Audit-Teile `C` und `E` sind ausgeschlossen. Die Regression prüft nur die Konfiguration, schlägt mit Version 3 fehl und besteht mit Version 4; sie erfindet und behauptet keine Auditdatei. Tatsächliche native Dateierzeugung sowie Regel-/Body-/MIME-Beobachtungen benötigen weiterhin frische Hostläufe durch Root.

## Geänderte Dateien

- `connectors/haproxy/harness/i12_spop_cases.py`
- `connectors/haproxy/harness/i12_spop_host.py`
- `connectors/haproxy/harness/i12_spop_wire.py`
- `tests/test_haproxy_i12_spop_wire.py`
- `tests/test_haproxy_i12_spop_samples.py`
- `reports/audits/change-records/CR-20261018-haproxy-spop-original-source-fixtures.md`
- `reports/audits/change-records/CR-20261018-haproxy-spop-original-source-fixtures.de.md`

## Ausgeführte Befehle

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m unittest discover -s tests -p test_haproxy_i12_spop_wire.py -v
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/spop/prepare-source-fixtures-v4.py
```

Python 3.14.7: 37 fokussierte Tests bestanden. Die neue P1-Allow-Regression schlägt mit dem unveränderlichen Modul aus Version 1 fehl (erwarteter Exit 1) und besteht mit Version 2. Die Quellvorbereitung erzeugte 729 unveränderliche Dateien; alle 728 Ledger-Einträge wurden in beiden Versionen unabhängig und fehlerfrei neu gehasht. Alle 94 Originalzugehörigkeiten wurden validiert. Ledger-SHA-256 von Version 4: `1cd048e2890d4a1faf9a3079c9149486adb8ece26471c7f2f091190d615858c8`. Alle 107 Verzeichnisse besitzen Modus `0555`; alle 729 regulären Dateien besitzen Modus `0444`. Die beiden neuen Wire-Regressionen schlagen mit den unveränderlichen Modulen aus Version 2 fehl (erwarteter Exit 1); die korrigierte Suite besteht (Exit 0). Die Auditkonfigurations-Regression schlägt außerdem mit Version 3 fehl (erwarteter Exit 1) und besteht mit Version 4. Der abgegrenzte Lauf von `git diff --check` bestand. Der gespeicherte Testbeleg liegt unter `spop/fixture-tests-v4.json` im externen Abnahmelaufverzeichnis. Die Change-Record-Archivprüfung, `make check-bilingual-docs` und `make check-doc-links` bestanden über RTK mit derselben Python-3.14.7-Umgebung.

Nach Änderung der Bedeutung des bisherigen Mutanten durch den expliziten HTTP-Versionsguard wurde auch der historische native Admission-Mutationstest korrigiert. Sein erzeugter C-Treiber setzt vorübergehend `Content-Length: 0`, um die fehlende Versionspräsenz isoliert zu prüfen, und stellt vor der HTTP/2-Kontrolle ungeframtes Input wieder her. Drei unabhängige C17-Builds liefern jetzt die geprüften Werte: aktueller Quelltext `0`, Mutant des Fallbacks für ungeframtes HTTP/2 `4` und Mutant der erforderlichen Versionspräsenz `3`. Bestehende Kontrollen für doppelte Längen, Transfer-Encoding, Größe und typisierte Werte wurden nicht entfernt. Der fokussierte Unittest schlug vor dieser Testkorrektur fehl (Exit 1) und bestand danach (Exit 0) unter Python 3.14.7. Belege und vorherige/nachherige Quellkopien liegen unter `spop/sample-mutation-review-20261018`. Der eingefrorene Hostharness aus Version 4 und der Produktcode bleiben unverändert.

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m unittest discover -s tests -p test_haproxy_i12_spop_samples.py -v
```

## Security-Auswirkung

Keine Änderungen an Produkt-, Common-, gemeinsamen Capture-, zentralen Matrix-, Framework- oder MRTS-Quellen. Endliche Authorization-Samples belegen niemals unbegrenzte Streaminginspektion. HTTP/2 oder unbekanntes/chunked Framing erhalten durch einen ACK keine Inspektionsbehauptung. Tatsächliches Clientframing und Beobachtungen eines gesunden Nachbarn bleiben erforderlich; Fehler dürfen den Nachbarn nicht unbemerkt beeinträchtigen.

## Runtime-Evidence

Externes Verzeichnis: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015`. Aktuelle Quelldefinitionen und Komponentenpakete: `spop/source-fixtures-v4`; Versionen 1, 2 und 3 bleiben unverändert. Korrekturprüfungen: `spop/source-fixtures-v1-harness-defect-eos.json`, `spop/source-fixtures-v2-harness-defects.json` und `spop/source-fixtures-v3-observation-gap.json`. Root meldete die Ablehnung des ursprünglichen Version-2-Bindings vor Hoststart wegen schreibbarer Verzeichnisse und beobachtete anschließend eine fehlende native Auditdatei in seinem separat zugelassenen Version-2-Allow-Probelauf. Dies ist keine vollständige Lifecycle-Qualifikation. Dieser Worker startete keinen privaten Host, behauptet keinen erfolgreichen Controllerlauf von `read_spec` und erzeugt keinen Lifecycle-PASS. Belege der Quellvorbereitung und Konfigurationstests bleiben von physischen nativen Ereignissen getrennt.

## Bekannte Einschränkungen

68 Transaktionsdefinitionen sind für Captures vorbereitet; 23 behalten explizite Lücken bei gemessenen Injektionen oder Quellen. Die drei Konfigurationsoriginale benötigen den tatsächlichen Treiber zur Agentkonfigurations- und nativen Regelzulassung. ACK-/Clientabbildung nativer Bodylimit-Rejects sowie erste Ursachen an Framegrenzen bleiben ohne unabhängiges Oracle ungeklärt. Physische Sinkfehler, tatsächliche Pointer-/Allokations-/Finishfehler, geordnete erste Ursachen, Cancel/Reset/Timeout und Postcommit-Szenarien benötigen weiterhin ihre echten Mechanismen.

## Verbleibende Risiken

Frische zugelassene Läufe müssen erzeugte HAProxy-Konfiguration, typisierte Samples, echte Responsebytes, nativen Requestumfang, physische Sinkereignisse und genau einmaliges Cleanup prüfen. Quellerwartungen und Unittests ersetzen diese Messungen nicht. Die Parent-Orchestrierung verantwortet die Qualifikation anhand des Messvertrags mit 35 Feldern.

## Nicht ausgeführte Prüfungen mit Begründung

Private HAProxy-/Agentbuilds und Hosts, Controllerzulassung, Sanitizer-/Mutationsläufe für Produktcode, SonarQube und vollständige CI wurden im abgegrenzten Auftrag zur Quellvorbereitung nicht ausgeführt. Parent verantwortet diese separaten Ausführungen und die Lieferung. Es wurden keine Git-Schreiboperation und kein Hoststart ausgeführt.

## Finaler Diff- und Review-Status

Die vier zugewiesenen SPOP-Dateien und dieses EN/DE-Paar wurden auf die Trennung von Quellen und Evidence geprüft. Native- und Companion-Änderungen anderer Worker bleiben unberührt. Lieferung, unabhängiges Runtime-Review und vollständige Qualifikation der Original-IDs stehen aus.
