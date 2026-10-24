# Change Record: CR-20261018-haproxy-native-sequence-fixtures

**Sprache:** [English](CR-20261018-haproxy-native-sequence-fixtures.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-native-sequence-fixtures |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `8582074ce1efc0df330277c1c2514d762f17afab` |

## Motivation und Problemstellung

Vorhandene Fixtures mit einer einzelnen Antwort belegen weder drei unabhängige Transaktionslebenszyklen noch die Wiederverwendung einer TLS-Verbindung. Eingaben für die Originalfälle `multiple_sequential_requests` und `keep_alive_requests_if_supported` werden vorbereitet, ohne ihre ausgewählten Anforderungen zu ändern.

## Akzeptanzkriterien

Original-IDs und Vertragshashes erhalten. Getrennte Allow/Deny/Allow-Fixtures vorbereiten, jede HTTP-Antwort und tatsächliche Socket-Identität erfassen, unvollständiges oder mehrdeutiges Framing ablehnen und unabhängige native Allocation-/Finish-/Free-Aufzeichnungen erhalten. Vorbereitung und Komponentenprüfungen dürfen keinen Host- oder Lifecycle-PASS vergeben.

## Implementierungsentscheidung und Begründung

Den versiegelten v7-`allow`-Capture-Launcher und seinen vorhandenen Observer wiederverwenden. Ein Fixture-eigenes HAProxy-`errorfile 403` definiert unabhängig die Denial-Payloadbytes. Die sequenzielle Variante nutzt drei Verbindungen; die Keepalive-Variante sendet alle drei Requests über genau ein tatsächliches SSLSocket und verbindet sich nach Close/Fehler nicht erneut. Das Backend nutzt persistentes Content-Length-Framing und ThreadingHTTPServer. Die native Zuordnung akzeptiert nur eine tatsächliche Allocation pro gemessenem Request-Zeitfenster; fehlende Aufrufe bleiben fehlend und zusätzliche Cleanup-Aufrufe sichtbar.

## Geänderte Dateien

Neu: `connectors/haproxy/harness/i12_native_sequences.py`, `tests/test_haproxy_i12_native_sequences.py` und dieses EN/DE-Change-Record-Paar. Keine Änderungen an Produkt, gemeinsamen Captures, zentraler Matrix, Framework oder MRTS.

## Ausgeführte Befehle

`rtk proxy <run>/test-env/bin/python -m pytest -q tests/test_haproxy_i12_native_sequences.py`: 10 bestanden unter CPython 3.14.7, Exit 0. Exakte umhüllte argv, cwd, Zeiten und Ausgabehashes: `<run>/commands/native-sequences-components-v4-20261018.json`. Fixture-Erzeugung mit `--base <run>/native/original-fixtures-v7/allow --plans <run>/native/original-fixtures-v7/original-case-plans.json --output <run>/native/sequence-fixtures-v4` endete mit Exit 0; exakte argv: `<run>/commands/native-sequences-prepare-v4-20261018.json`. `<run>` bezeichnet `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015`. Beide Fixtures enthalten sechs SHA-256-gebundene reguläre Dateien mit Modus 0444 und Fallverzeichnisse mit 0555. Die frühere v1-Vorbereitung bleibt historisch erhalten.

## Security-Auswirkung

Keine Änderung des Produktverhaltens. Der begrenzte Client verlangt einen dezimalen Content-Length und lehnt Transfer-Encoding, doppelte Längen sowie zu große oder unvollständige Nachrichten ab. Die Vorbereitung nutzt den vorhandenen Helfer für zugelassene externe Ausgaben. Socket-Close wird nicht als native EOS oder Transport-Reset behauptet.

## Runtime-Evidence

Kein HAProxy-Host wurde gestartet. Zwei vorbereitete Fixtures und 10 Komponententests ergeben null unabhängige Hostläufe und null Lifecycle-PASS. `join_native` legt tatsächliche native Zeilen und Rückkehrzähler offen; es ersetzt weder den vorhandenen Qualifier noch ergänzt es fehlende Finish-/Free-Aufrufe.

## Bekannte Einschränkungen

Das tatsächliche HAProxy-Keepalive-Verhalten nach lokalem Deny muss gemessen werden. Eine geschlossene Verbindung bleibt als fehlgeschlagene Ausführung erhalten und wird nicht automatisch als Host-Unsupported oder N/A eingestuft. Der vorhandene Einzelrequest-Extractor verarbeitet das Sequenz-JSON nicht direkt; jeder zugeordnete Request und die originalen physischen Sink-/Host-Aufzeichnungen müssen geprüft werden.

## Verbleibende Risiken

Frische integrierte native Binaries, private Hostausführung, physische Sink-Beobachtungen, Commit-/EOS-Reihenfolge, Descriptor-Cleanup und unabhängige Qualifikation der Original-Oracles bleiben erforderlich. Das gezielte Errorfile macht Denial-Bytes deterministisch, belegt allein jedoch kein natives Deny.

## Nicht ausgeführte Prüfungen mit Begründung

Private Hostausführung und finales CI/Sonar wurden in dieser begrenzten Fixture-Aufgabe nicht ausgeführt; Root verantwortet Hostausführung und Lieferung. Kein neues natives oder Transportergebnis wird behauptet.

## Finaler Diff- und Review-Status

Nur die eigenen neuen Dateien wurden geändert. Komponentenvalidierung und Hash-/Modusprüfung der versiegelten Fixtures bestanden; unabhängiger Root-Review, Hostausführung und Git-Lieferung stehen aus.
