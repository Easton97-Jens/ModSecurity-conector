# Change Record: CR-20261018-i12-traefik-preallocation

**Sprache:** [English](CR-20261018-i12-traefik-preallocation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-traefik-preallocation |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `a311c725c44a7a4da95acb1a4818f66bd56c462a` |

## Motivation und Problemstellung

Eine ursprüngliche HTTP-Parserzurückweisung kann vor Anlage einer nativen Transaktion erfolgen. Die normalen Pflichtbeobachtungen für Transaktions-ID, Phase und Free würden dort erfundene Aufrufe erzwingen. Unabhängig davon konnte Parser-Exit 1 allein einen fremden Loaderfehler fälschlich als benannte Konfigurationszurückweisung akzeptieren.

## Akzeptanzkriterien

Alle Original-IDs und alle 35 Beobachtungsfelder des normalen Lebenszyklus bleiben erhalten. Ein eigener Geltungsbereich gilt ausschließlich für die exakten ursprünglichen Traefik-Parser-, NULL-Eingabe-, frühen Mapping-/Begin-Cleanup- und Sink-Open-Anforderungen mit unabhängig genehmigtem Nichtallokationsvertrag. Er zählt niemals als vollständiger nativer Lebenszyklus. Pflicht sind physische Clientbytes, unabhängiger Backend-Ausschluss bereits bei Headerankunft, aktive native Instrumentierung, Nullallokation mit gesunden Kontrollen, Quell-/Image-/Konfigurations-/Run-/UID-Identität und tatsächliches Cleanup. Zurückgewiesene Konfigurationen benötigen zusätzlich zum exakten Exit-/Signalvertrag die erwartete quellgebundene Diagnose und erste Fehlerursache.

## Implementierungsentscheidung und Begründung

Das bestehende Ledger bleibt alleiniger Qualifier. Seine normalen `host_http`-Messregeln und ALWAYS_APPLICABLE bleiben unverändert. `host_preallocation_control` ist auf die acht Parser-IDs, vier NULL-Eingabe-IDs, sechs frühen Mapping-/Begin-Cleanup-IDs und drei Sink-Open-IDs ihrer ursprünglichen zulässigen Traefik-Routen beschränkt. Zulässigkeit allein qualifiziert keine Ausführung.

Root-Freigabe bindet exakten Originalvertragsdigest und wirksames unabhängiges Oracle. Die native Phase bleibt darin null; ursprüngliche Erwartungen werden nicht geändert. Beobachtungen zu nicht angelegter Transaktion, Phase, EOS, Finish und Free bleiben mit Begründung null. Tatsächliche native/Runtime-API-Rückgaben bleiben erhalten und müssen exakt mit dem Target-Observerstream übereinstimmen; ohne API-Aufruf ist dies eine leere Liste. Separat aus Messungen abgeleitete native SDK-Konstruktorversuche und erfolgreiche Allokationen bleiben unterschiedliche Zähler. Jedes vorgeschriebene Beobachtungsfeld bleibt vorhanden.

Selektoren binden bestehende physische JSON-Felder oder exakte JSONL-Zeilen; sie erzeugen keine Producer-Messwerte. Native Observerrecords müssen Aktivierung, unterbrechungsfreie Sequenz je Prozess, gültige Identität und Abschlussabdeckung belegen. Kontrollen davor/danach benötigen tatsächliche native Allokation/Freigabe, erfolgreiche Clientantworten und unabhängige Backendheader. HTTP-/Parser-/Mapping-Kontrollen nutzen denselben lebenden nativen Prozess. Ein Konstruktorfehler vor Listenerstart verwendet einen aufgenommenen Fehlerprozess und getrennte gesunde Prozesse mit identischen geladenen Image-/Observerhashes.

Rohe fehlerhafte Requests müssen ihren exakten ursprünglichen Headerfall auslösen. Rohe Antworten binden Status, Entitybytes/Hash und Framing; eine zweite Antwort kann nicht bestehen. Unabhängige Backendrecords werden bereits bei Headerankunft vor vollständigem Body geprüft. NULL-Pointerpfade benötigen tatsächliche Pointer-/Größenmessungen und echte API-Rückgaben. Natives Setup-Resultat 1 ist kein Fehlerbeleg; die unabhängig beobachtete Runtime-Begin-Rückgabe ist Pflicht. API-errno bleibt ausdrücklich abwesend. Sink-Open-Kontrollen erfordern echte fehlgeschlagene Open-Syscalls/errno sowie Exit/Diagnose des Fehlerprozesses. Run-Cleanup erfasst Descriptoren, Sockets, Prozesse und einen Cleanup-Vorgang; natives Finish/Free werden nie erfunden.

Konfigurationszurückweisung bindet nun eine getrennt geprüfte Diagnose-/First-Cause-Quelle an den exakten Originalvertrag und das Oracle. Ein echter Exit 1 mit anderer Ursache kann nicht PASS werden. Akzeptierte Konfigurationen behalten ihr Verhalten.

## Geänderte Dateien

- `ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py`: zusätzlicher begrenzter Geltungsbereich, physische Bindungen, Bilanzierung und strenge Konfigurationszurückweisung.
- `tests/test_i12_traefik_preallocation.py`: Producerformat- und Manipulationskontrollen, alle acht Parseridentitäten, Startup-/Kontrollprozessunterscheidung und Ledgerzählung.
- `tests/test_i12_lifecycle_ledger.py`: Zurückweisungskontrollen enthalten nun unabhängig gebundene Diagnose/First-Cause.
- Dieses EN/DE-Change-Record-Paar.

## Ausgeführte Befehle

Alle Shellbefehle nutzten RTK und das Parent-Virtualenv. Der kombinierte Befehl lautete `rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_i12_traefik_preallocation tests.test_i12_lifecycle_ledger tests.test_i12_traefik_absence_oracles tests.test_i12_oracle_reconciliation`. Zusätzlich mit `tests.test_bilingual_docs tests.test_change_record` bestanden 101 Tests in 3,187 Sekunden. Der externe Aufgabenbeleg `preallocation/unit-final-v2-20261018.json` enthält den exakten Befehl, Quellhashes sowie jeweils null Hostläufe/ID-Hochstufungen. Change-Record-Struktur, AST-Syntax für drei Python-Dateien, `git diff --check` und RTK-Prüfung bestanden getrennt.

## Security-Auswirkung

Normale Lebenszyklusanforderungen, UID 65534, Prüfung physischer Referenzen und Originalkatalogintegrität bleiben verbindlich. Der Patch erteilt keine Runtime-Admission, ändert keinen Produktcode und verändert weder Isolation noch Sonar-Zustände. Fehlende oder widersprüchliche Quell-/Observer-/Client-/Backend-/Cleanupbelege verhindern Qualifikation.

## Runtime-Evidence

Die Unit-Fixtures modellieren bestehende physische Producerformate und sind ausdrücklich synthetisch. Sie validieren Qualifierentscheidungen; sie sind keine neuen Hostaustausche oder qualifizierten Originalfälle. Tatsächliche neue Hostbelege, unabhängige Oracle-Reconciliation und Root-Prüfung bleiben Voraussetzung für die Aufnahme einer Original-ID in diesen Geltungsbereich.

## Bekannte Einschränkungen

Der Decoder für Antworten vor Allokation akzeptiert vollständige Content-Length- oder verbindungsbegrenzte Entitybytes. Transfer-Encoding-Antworten benötigen einen unabhängig unterstützten Entitydecoder und scheitern derzeit an der Qualifikation. Ein leeres Observerfile belegt keine Nichtallokation. Ein Startupfehler ohne aufgenommene Instrumentierung kann diesen Geltungsbereich nicht verwenden. Nur vollständig belegte passende Kontrollen erhalten PASS; unvollständige oder abweichende Kontrollen bleiben unqualifiziert statt eine Lebenszyklusbehauptung zu erhalten.

## Verbleibende Risiken

Frische echte Hostausführungen können fehlende Producerbeobachtungen zeigen. Diese müssen physisch ergänzt und geprüft werden; Paketmetadaten ersetzen sie nicht. Abschließende gehostete Checks benötigen weiterhin den veröffentlichten integrierten Head.

## Nicht ausgeführte Prüfungen mit Begründung

Diese Qualifieränderung startet keine Hosts, lädt keinen Scan hoch, veröffentlicht kein Git und stuft keine Original-ID hoch. Integrierte Hostproducer und endgültige gehostete Abnahme gehören zur übergeordneten Aufgabe.

## Finaler Diff- und Review-Status

Der normale Lebenszykluspfad bleibt erhalten. Tests für getrennten Dispatch und Zusammenfassung belegen, dass Preallocation-PASS die passende Originalfallqualifikation erhöht, während vollständige Lebenszykluszahlen unverändert bleiben. Das unabhängige Abschlussreview bestand nach Korrektur der aktuellen nativen Pointer-Rückgabebindung und Zurückweisung fehlerhafter Content-Length-Antwortwerte; seine getrennten 26 fokussierten Kontrollen bestanden. Integration und echte Hostabnahme verantwortet weiterhin die übergeordnete Aufgabe.
