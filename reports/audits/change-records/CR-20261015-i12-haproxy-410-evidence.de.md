# Change Record: CR-20261015-i12-haproxy-410-evidence

**Sprache:** [English](CR-20261015-i12-haproxy-410-evidence.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-haproxy-410-evidence |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation und Problemstellung

Die bestehende Evidence von #410 qualifiziert neun HAProxy-Lifecycle-Fälle. Die drei getrennten Routeninventare enthalten 112/94/72 Pflicht-IDs und 48/44/32 ursprüngliche Oracles; im Ausgangsledger bleiben 43/41/31 ursprüngliche Oracles offen. Diese Änderung verbessert unabhängig gemessene Abdeckung, ohne reine HTTP-Beobachtungen zu Lifecycle-PASS hochzustufen.

## Akzeptanzkriterien

Native HTX-, SPOP-Request- und Companion-Urteile getrennt halten; geänderte Prädikate ursprünglicher Oracles an Quellen und Fixture-Verhalten binden; Host-/native-/Konfigurations-/Frame-/Client-/Backend-/Sink-/Finish-/Free-Evidence sowie exakte argv, Exits und Hashes bewahren. Produkt, zentrale Matrix, gemeinsame Captures, Generatoren und andere Connectoren unverändert lassen. Einen autorisierten Draft gegen `work/pr382-i12-host-evidence-20261011` liefern; unaufgelöste Fälle bleiben ausdrücklich offen.

## Implementierungsentscheidung und Begründung

Aufgabenspezifische HAProxy-Harnesses und Fixtures ergänzen und dabei die drei bestehenden unveränderlichen Capture-Varianten in Wegwerfkopien verwenden. Beobachtungsassertionen von Lifecycle-Qualifikation und Quell-Oracle-Auflösung trennen. Nur den veralteten HAProxy-spezifischen SPOP-Testaufrufervertrag korrigieren. Logischen Commit von positivem Clienttransport unterscheiden; native disruptive Ergebnisse erhalten, auch wenn Safe-Modus die ursprüngliche Response sendet.

## Geänderte Dateien

- `connectors/haproxy/harness/i12_native_cases.py`
- `connectors/haproxy/harness/i12_native_observe.py`
- `connectors/haproxy/harness/i12_spop_host.py`
- `connectors/haproxy/harness/i12_spop_sink_capture.py`
- `connectors/haproxy/harness/i12_spop_wire.py`
- `connectors/haproxy/harness/i12_companion_host.py`
- `tests/test_haproxy_i12_native_cases.py`
- `tests/test_haproxy_i12_spop_samples.py`
- `tests/test_haproxy_i12_spop_wire.py`
- `tests/test_haproxy_i12_companion_host.py`
- `tests/haproxy_spop_request_target_test.c`
- `docs/pr-410-i12-haproxy-20261015.md`
- `docs/pr-410-i12-haproxy-20261015.de.md`
- `reports/testing/i12-haproxy-410-20261015.json`
- `reports/audits/change-records/CR-20261015-i12-haproxy-410-evidence.md`
- `reports/audits/change-records/CR-20261015-i12-haproxy-410-evidence.de.md`

## Ausgeführte Befehle

Alle Shellbefehle verwenden RTK. Frische receiptbelegte Befehle umfassen `rtk proxy make check-haproxy-c17`, `rtk proxy make check-haproxy-htx-overlay`, `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify` und Capture-Mutations-Unittests. Vollständige argv, Build-root-/Python-Parameter, stdout-/stderr-Hashes und Exits liegen unter `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-410-20261015/verification/summary.json`. Native und Hosttreiber bewahren zusätzliche exakte argv und Exits in eigenen Receipts. Das Change-Record-Paar wurde mit `rtk proxy python3 ci/tools/new-change-record.py create --name i12-haproxy-410-evidence --base-revision f27eb59b53beff6f65384fc2e5037881a3052c01 --date 2026-10-15` erstellt.

Change-Record-Archivstruktur und beide EN/DE-Strukturparitätsprüfungen bestehen. `rtk git diff --check` besteht. `rtk make check-bilingual-docs` und `rtk make check-doc-links` scheitern an fehlenden Framework-Submodul-Linkzielen; die Aufgaben-JSON-Links sind jetzt auflösbar.

## Security-Auswirkung

Keine Änderungen produktiver Sicherheitskontrollen. Tests untersuchen fail-closed begrenzte SPOP-Samples, beschädigtes Framing, Sinkfehler, Transaktions-Cleanup und die Reihenfolge der Responseautorisierung. Unbekanntes/chunked Framing und nicht unterstützte HTTP/2-Abbildungen bleiben außerhalb vollständiger Inspektionsqualifikation. Ein grüner Request-ACK belegt keine Companion-Sicherheit. Produktabweichungen bleiben für separate Folgearbeit in #382 erhalten.

## Runtime-Evidence

Frische Hostbuilds verwenden HAProxy `3.2.25` und libModSecurity `3.0.14`. Aufgaben-Rohdatenwurzel: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-410-20261015`. Der [Aufgabenbericht](../../../docs/pr-410-i12-haproxy-20261015.de.md) erklärt jede Route und die Beobachtungsgrenzen; [JSON-Evidence](../../testing/i12-haproxy-410-20261015.json) enthält geprüfte Dispositionen je Lauf. Nativer Request-only-SPOP-Abschluss liefert `-3` mit Phasenmaske `3`, daraus ACK/Client `503` und null Backendrequests; ein separater kombinierter Request erreicht Maske `15`, Finish `0`, ACK `200` und einen Backendrequest. Das native Response-Reject-Limit beobachtet disruptives `403`, während Safe-Clienttransport `200` und 27 Bytes liefert. Keine Abweichung wird zu erfolgreichem vollständigem Lifecycle umgeschrieben.

Das echte HTTP/2-Content-Length-Sample sendet `http_version=2.0` und erhält ACK `200`/einen Backendrequest, aber das native Audit erfasst `HTTP/1.1`. Request-only-Finish- und HTTP-Versionsabweichung sind in [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194176740) gemeldet. Ein separater Companion-P3-Deny-Hostlauf erfasst `1→2→8→7`, Client `403`, kein COMMIT/BODY/EOS und eine native Freigabe je Transaktion; der unabhängige Safe-Lauf erfasst `1→2→5→3→4→8→7`, `log_only`, Client `200` und 33 Bodybytes. Abgelaufene Korrelation liefert CLAIM→RESULT-Fehler/Client `503`; zwei idempotente Common-Cleanup-Aufrufe bei einem nativen Cleanup beweisen keinen Double-free.

Der akzeptierte Strict-Zweig versucht einen Abbruch nach P4-Deny `403`, dennoch erreicht die gemessene gepufferte 33-Byte-Response den Client vollständig als HTTP `200` mit TLS-Close. Quellverfolgung `companion/strict-transport-cause.json` bestätigt, dass asynchrones `stream_shutdown` plus positives `http_end` Warteschlangenausgabe vor Taskabschaltung zulässt; das nachfolgende positive `SSL_write` umfasst 210 Bytes mit Client-SHA-256 `9b6e9773ad3ed4e42cfc54373d5769e9d393f634124bf5667b54be2cc8ab8176`. Diese begrenzte Produktabweichung benötigt Korrektur in #382. Die ursprüngliche No-ACK-Erwartung für beschädigtes NOTIFY war ein `HARNESS_DEFECT`: tatsächliches ACK `400`/`block=true`, Client `503` und Backend null bleiben erhalten und werden nur in quellgebundener Offlineauswertung ohne frische Hostanrechnung korrigiert. Phase-four-Diagnosen und als Datei benannte Payload-Fixtures belegen keine Katalog-ID- oder native File-API-Abdeckung.

Die Hauptprüfung akzeptiert 22 frische native Läufe einschließlich zweier Basiswiederholungen: 20 neu qualifizierte IDs, aktuell nativer Lifecycle `25/112`, 87 unqualifizierte Pflicht-IDs und `25/48` aufgelöste ursprüngliche Oracles bei 23 offenen. SPOP bleibt bei Lifecycle `3/94`, 91 unqualifizierten Pflicht-IDs; vier reine Quell-Oracle-Auflösungen ergeben `7/44` aufgelöst und 37 offen ohne neue Lifecycle-Anrechnung. Der unabhängige V7-Companion-Lauf `NEED-client-response-bytes` besteht unveränderte ursprüngliche Oracle- und Lifecycle-Ledger-Gates: aktueller Companion-Lifecycle `2/72`, 70 unqualifizierte Pflicht-IDs und 30/32 ursprüngliche Oracles offen. Gesamtergebnisse sind 30/278 vollständige Lifecycle-PASS (+21), 248 unqualifizierte Pflicht-IDs sowie 34/124 aufgelöste ursprüngliche Oracles bei 90 offenen (Basis 115 offen). Die 23 frisch qualifizierten Versuche sind 22 native Läufe einschließlich zweier Basiswiederholungen plus ein unabhängiger Companion-Lauf mit unterschiedlichen Nonces; kein Request wird dreifach gezählt. SPOP hat 13 gültige private Hostläufe; die finale Abweichungswiederholung beendet den Controller mit `0`, ACK/Client `503`, null Backendrequests und null nativen Allokationen. Die schreibgeschützte Speicherfinalisierung besteht mit ungefähr 0.475 GiB aufbewahrten Daten und 184 GiB freiem Speicher. Die 25 neuen HAProxy-Unittests bestehen.

V8-Parallel-Controllerexit `0` qualifiziert den Fall nicht: 16 Clients liefern vier vollständige `200`, ein gekürztes `200`, zwei `503` und neun `502`. Null lebende Mappings/ausstehende Aufrufe und acht native Freigaben stützen nur die Cleanup-Beobachtung. Fehlgeschlagene V4-/Controller-`77`-Versuche bleiben neben späteren Wiederholungen erhalten. Nativer Snapshot v2 stärkt den ausdrücklichen 16-Byte-`ProcessPartial`-Umfang unter Erhalt alter unveränderlicher Artefakte. Der aufgabeneigene Controller ändert ausschließlich das RUN-Wurzel-Literal. Der Strict-Produktbefund ist separat in [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194270431) gemeldet.

## Bekannte Einschränkungen

Die breite bestehende Suite führt 256 Tests aus: zwei veraltete Workflow-Upload-Pin-Fehler, ein Unix-Socketpfadfehler und 12 Skips. Der Socketfall besteht mit kürzerem aufgabeneigenem temporärem Pfad. Die veralteten Workflow-Pins bleiben unverändert. Alle 31 einfachen pytest-artigen Funktionen bestehen über einen minimalen Adapter, einschließlich ASAN-/UBSAN-Pfaden nach Korrektur des veralteten SPOP-Testaufrufers. Der gewöhnliche pytest-Befehl scheitert, weil pytest fehlt; keine Abhängigkeit wird installiert. C17, HTX-Overlay, Capture-Registry und Mutationsprüfungen bestehen. Vollständige Qualifikation beschränkt sich auf tatsächlich geprüfte Evidence.

## Verbleibende Risiken

Unaufgelöste ursprüngliche Oracles, nicht unterstütztes H2/Framing, fehlende physische CommonAllow-Sinkevidence und unqualifizierte Companion-Reihenfolge bleiben offen. Native Audit-/Debugausgabe ersetzt kein fehlendes CommonAllow-Sinkereignis. Es wird weder vollständige 278-ID-Abdeckung noch drei unabhängige Läufe aus einem gemeinsamen Request behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Pytest selbst wurde mangels Installation nicht erfolgreich ausgeführt; ein separater minimaler Adapter führte die 31 Funktionen aus. Connectorübergreifende, Framework- oder MRTS-Änderungen/-Tests gehören nicht zu diesem Umfang. Hosted CI/Review/Sonar am finalen Head und Draft-Veröffentlichung müssen anhand tatsächlicher Lieferbeobachtungen erfasst werden; sie werden nicht aus lokalen Prüfungen abgeleitet.

## Finaler Diff- und Review-Status

Die lokale Dokumentation bewahrt Umfang, Ergebnisse und Grenzen zweisprachig. Der angeforderte Branch ist `codex/i12-haproxy-410-20261015` auf Basis von `f27eb59b53beff6f65384fc2e5037881a3052c01`; der angeforderte Drafttitel lautet `test(i12/haproxy): complete HTX SPOP and companion lifecycle evidence`. Dieser Record behauptet keine veröffentlichte PR-Nummer, abgeschlossene Hosted-Prüfungen, Merge, Force-Push oder Produktkorrektur. Die finale Qualifikation ist oben erfasst; autorisierte Draft-Lieferung und Hosted-Review bleiben getrennte beobachtete Lifecycle-Fakten.
