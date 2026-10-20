# Change Record: CR-20261020-request-body-retained-telemetry

**Sprache:** [English](CR-20261020-request-body-retained-telemetry.md) | Deutsch

Request-Telemetrie trennt angebotene Bytes vom SDK-eigenen gespeicherten Präfix und unbelegter Inspection.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261020-request-body-retained-telemetry |
| Datum (UTC) | 2026-10-20 |
| Basis-Revision | `12cc380c3749fd76c246c05ce479f51446127880` |

## Motivation und Problemstellung

Traefik forwardAuth Request-v20 bot Chunks mit 8 und 9 Bytes an. ProcessPartial speicherte 16 Bytes, erlaubte den Request und erzeugte kein Body-Limit-Event. Reject speicherte 8 Bytes, meldete jedoch 17 inspizierte Bytes ohne Trunkierung. Common zählte angebotene Append-Bytes als inspiziert und aktualisierte die Request-Limit-Metadaten nicht.

## Akzeptanzkriterien

Angebotene und vom SDK gespeicherte Bytes getrennt erfassen, Inspection niemals aus Speicherung ableiten, native Statuswerte und Entscheidungen erhalten, nicht disruptive ProcessPartial-Evidence nur aus nativem Append `0` erzeugen und technische/Accessor-/Sink-Fehler weitergeben. Echte SDK-Grenz- und Negativtests müssen bestehen.

## Implementierungsentscheidung und Begründung

`msc_get_request_body_length` unter dem bestehenden nativen Operation-Lock lesen. `bytes_retained` hinten an die Progress-Struktur anfügen und bestehende Member-Offsets erhalten; Consumer müssen mit dem aktualisierten C-Header neu gebaut werden. Request-`bytes_inspected=0` bedeutet unbekannt/unbelegt, auch nach erfolgreichem P2/EOS: Die Kontrolle mit deaktiviertem Body-Zugriff speichert ebenfalls alle 17 Bytes. Reject und ProcessPartial behalten das native Verhalten; Partial-Telemetrie fordert keine Ablehnung. Reject-Telemetrie erfasst Trunkierung und natives Ergebnis. Eine unmögliche Accessor-Länge lässt die Transaktion fehlschlagen. Response-Semantik und Wire-/Event-Feldschemas bleiben unverändert.

## Geänderte Dateien

`common/runtime/msconnector_runtime.c`, `common/runtime/msconnector_runtime.h`, `tests/request_body_telemetry_test.c`, `tests/engine_response_limit_test.c`, `tests/engine_http_request_stream_test.c`, `tests/test_engine_response_limits.py`, `tests/test_native_api_fail_closed_contract.py`, `tests/test_i09_body_phase.py`, `docs/body-inspection-review-matrix.md`, die deutsche Fassung und dieses Change-Record-Paar.

## Ausgeführte Befehle

Alle Befehle verwendeten `rtk proxy`. Echte Engine-/Native-API-/Snapshot-/Traefik-P2-/Adapter-Regressionssuite: 41 Tests bestanden. Der fokussierte Telemetrie-Test deckt Reject, ProcessPartial, vollständigen Body, deaktivierten Zugriff, unmögliche Accessor-Länge, fehlgeschlagenes P2 und Sink-Fehler ab; alle sieben Szenarien bestanden auch ASan/UBSan. Die ursprüngliche Accounting-Assertion schlug vor der Korrektur fehl. `make check-common-sdk-contract check-common-security-contract check-common-flow-integrity check-i10-common-callers PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` bestand (11 I10-Tests); `make check-common-memory-safety` und `make check-i09-native-routes` (33 Tests) bestanden. Change-Record-Struktur sowie Sprachpaare/geänderte Links bestanden. Vollständige Dokumentationsprüfungen trafen ausschließlich auf fehlende Framework-Basisziele im nicht initialisierten Worktree; finale integrierte Prüfungen bleiben erforderlich.

## Security-Auswirkung

Verhindert falsche Inspection-Aussagen und trennt native Policy-Ablehnung von technischen Fehlern. Limits, Authentifizierung, Isolation und Validierung werden nicht abgeschwächt. Neue Schreibfehler des Partial-Events werden weitergegeben und nicht zu erfolgreicher Autorisierung.

## Runtime-Evidence

Original-Evidence verbleibt im Run `i12-traefik-acceptance-20261015`, Request-v20-Versuch `attempt-1792515659749428431`. Dieser Patch führte echte libModSecurity-/C-Runtime-Tests aus, einschließlich bestehender MRC1- und HTTP-Authorization-Streaming-Tests. Er führte keinen neuen Traefik-Hostlauf aus und qualifiziert allein keine I12-ID.

## Bekannte Einschränkungen

Die öffentliche SDK-C-API zeigt nicht, ob gespeicherte Request-Bytes semantisch inspiziert wurden. Null inspizierte Bytes bedeutet unbekannt, nicht deaktivierte Inspection. Aussagen zur vollständigen Inspection benötigen weiterhin unabhängig gebundene native Regel-/Source-/Runtime-Evidence. Eine BodyAccess-Abweichung allein ist kein Body-Limit-Signal. Response-Accounting bleibt unverändert.

## Verbleibende Risiken

Neue Traefik-Host-Evidence muss neu gebaute Binaries und neu versiegelte Producer-Eingaben verwenden. Bestehende C-Binary-Consumer müssen neu gebaut werden; für vergrößerte Progress-/Snapshot-Strukturen wird keine stabile Binary-ABI-Kompatibilität behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Neue Traefik-Hosts, Go race/vet, Remote-CI am aktuellen Head und Sonar-Readback gehören zum integrierenden Traefik-Abnahmetask. Dieser fokussierte Patch ändert kein Go und führt keine SDK-/C++-Bridge ein.

## Finaler Diff- und Review-Status

Nur fokussierte Runtime, Tests und zweisprachige Dokumentation. Keine Änderungen an Framework/MRTS, zentraler Matrix/Generator, Hostproducer, Abhängigkeiten oder master. Lieferung über #382 ist autorisiert; Integration über #410/#413 und finale Hostvalidierung bleiben separat.
