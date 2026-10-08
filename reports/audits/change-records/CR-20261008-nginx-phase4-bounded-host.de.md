# Änderungsnachweis: CR-20261008-nginx-phase4-bounded-host

**Sprache:** [English](CR-20261008-nginx-phase4-bounded-host.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-phase4-bounded-host |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `b7403e30111688da00d8e7ce376ea91ced1c6145` |

## Motivation und Problemstellung

Ausgewählten Phase-4-Split-, EOS-, Engine-Limit- und Metadaten-Operationen fehlen echte eigene Aufrufe. Deklarierte Fixtures oder HTTP-Status allein belegen diese Verträge nicht.

## Akzeptanzkriterien

Begrenzte Loopback-Chunks und EOS müssen tatsächlich gesendet werden; fehlende Freigabe muss scheitern. Host-Aufrufe behalten exakte Configtest-/Client-Exits, Artefakte, native Records, beobachtete Root/nobody und PIDFD-gebundenen Cleanup. Keine drivergenerierten nativen Events oder vorzeitigen kanonischen PASS.

## Implementierungsentscheidung und Begründung

Der neue `ci/runtime/common/nginx_phase4_upstream.py` sendet maximal acht Chunks und 8192 Bytes über einen zugewiesenen IPv4-Loopback-Listener. Eine ausdrückliche Barriere begrenzt das Split-Timing; Beobachtungen betreffen nur erfolgreiche Sendungen und EOS, nicht native Inspektion. Der eigene `ci/runtime/lifecycle/run-nginx-phase4-cases.py` importiert bestehende sichere Snapshot-/Projektions- sowie Rollen-/PIDFD-Cleanup-Helfer statt Autorität zu duplizieren. Geschlossene Framework-Eingaben, `proxy_buffering off`, exakte stdout/stderr/Config/Regeln/native Events und Digests werden verwendet. Bis zur unabhängigen strengen kanonischen Validierung bleibt `canonical_status=NOT_EXECUTED`. Die neueste ausdrückliche Benutzerentscheidung migriert die alte Required-Identität auf bestehendes `safe`; kein Modus `minimal` wird wiederhergestellt, Off-Legacy-Verhalten bleibt unverändert. Frühere Off-Fokusartefakte bleiben historische Diagnosedaten, keine Safe-Evidence.

## Geänderte Dateien

Fortsetzung am 2026-10-08: Der eigene curl-Aufruf bewahrt jetzt
`response.headers` aus der tatsächlichen `--dump-header`-Ausgabe auf und bindet
deren Bytes in `raw_sha256`. Damit kann der unabhängige Framework-Validator
Wire-Status, MIME und Framing neben dekodiertem Body und curl-Ergebnis prüfen.
Die Aufzeichnung verändert keine nativen Beobachtungen oder kanonischen Status.
Zwei vorhandene Driver-Grenztests bestehen nach der fokussierten Änderung;
der neue native Produzent benötigt weiterhin Koordinatorintegration und Neubau.

Die vom Koordinator genehmigte Schnittstelle `run_operation` verwendet diese
Laufzeit zusätzlich für einen separat verantworteten MIME-Adapter. Aufrufer
liefern ihre vorvalidierte geschlossene Spezifikation, den tatsächlichen Pfad
der Eingabequelle, begrenzte Upstream-/Konfigurationsfabriken und den tatsächlichen
Upstream-Quellpfad. Receipts hashen diese gelieferten Quellen; der Standardaufruf
lädt weiterhin seine ursprüngliche geschlossene Phase4-Eingabequelle. Artefakt-
Snapshot, native Rollenbeobachtung und PIDFD-Cleanup bleiben in der gemeinsamen
Laufzeit. Vier fokussierte Driver-/Charakterisierungstests bestehen; kein nativer
MIME-Lauf wird behauptet.

Die beiden neuen Helfer, `tests/test_nginx_phase4_upstream.py`, `tests/test_nginx_phase4_driver.py` und dieses EN/DE-Paar. Zentrale Dispatcher/Collector/Schema/native Producer sind Integrationsabhängigkeiten des Koordinators.

## Ausgeführte Befehle

RTK-gekapselte Parent-Python-Unittests: drei echte Loopback-Wire-Tests und zwei Driver-Grenztests bestehen mit Exit 0. Der erste Upstream-Test scheiterte wegen fehlender Implementierung. Ein breites bestehendes Phase4-Testmuster bestand mit 25 Tests und drei bestehenden SKIPs; diese SKIPs sind keine Host-Evidence. Syntax/Hilfe und `git diff --check` bestehen. Nativer NGINX-Fokus, Dokumentationsprüfung und finale Integration stehen bei Erstellung noch aus.

## Security-Auswirkung

Keine Veränderung fremder Prozesse, Listener, Netzwerke oder globaler Rechte. Root/nobody-Operationen benötigen isolierte Task-Attempts; Signale treffen beobachtete eigene Prozesse und gebundene Kinder. Ausgabe-Roots bleiben frische private externe Kinder; Docroot-Projektionen frische direkte autorisierte Kinder. Rohe Fixture-Antworten bleiben begrenzt; keine Bodies gelangen in Events oder Upstream-Metadaten.

## Runtime-Evidence

Socket-Tests beweisen tatsächliche lokale HTTP-Chunk-Frames und Timeout-Verhalten, keine NGINX-Coverage. Der externe Entwicklungsfokus `stream-c-r1` führte acht echte isolierte Operationen mit Read-only-Quellen und Baseline-Artefakten aus: alle Configtests Exit 0, Root 0/nobody 65534 beobachtet, Cleanup verifiziert. Split/EOS und ProcessPartial-Requests lieferten Client 0/HTTP 200 mit tatsächlicher nativer Rule 1100301. Reject erzeugte Client 18 mit nativem Invalid-Engine-Response-Abort; off nach Commit Client 18 mit nativem Connector-Error-Abort. Keiner davon gilt als PASS. Bestehende Zähler melden weiterhin an Append übergebene Bytes, nicht die Engine-Inspektionslänge. Der übernommene Proc-Observer erfasste Master-/Kind-Maps vor Privilegabgabe, keine Nobody-UID-Maps; die spätere bereite Worker-Identität ist unabhängig durch Rollen-/PIDFD-Receipt gebunden. Echte Host-Beobachtungen erhalten auf dieser Eingabe-/Driver-Schicht bewusst keinen PASS. Operationsspezifische strenge Interpretation und finale integrierte Ausführung bleiben Pflicht.

## Bekannte Einschränkungen

Upstream-Chunk-Grenzen allein beweisen keine mehreren ModSecurity-Append-Aufrufe. Bestehende Append-Byte-Zähler beweisen nicht die Engine-Inspektionslänge nach ProcessPartial. Native Producer und ausdrückliche deterministische Quellenzuordnung bleiben Integrationsarbeit. Die gemeinsame Required-Selection bleibt unverändert; kein finaler Exact-Head- oder Protected-Nachweis wird behauptet.

## Verbleibende Risiken

Erfolgreiche Helferausführung bedeutet keinen validierten nativen Limit- oder EOS-Vertrag. Finale integrierte strenge kanonische Validierung und negative Artefaktkontrollen bleiben Pflicht.

## Nicht ausgeführte Prüfungen mit Begründung

Privilegierter Fokus wartet auf den serialisierten Runtime-Slot des Koordinators. Finaler nativer Lint, kombinierte Regressionen und frische CI/Sonar gehören dem Koordinator.

## Finaler Diff- und Review-Status

Exklusiver Parent-Task-Worktree; keine Parent-Gitlink-, MRTS-, Veröffentlichungs- oder Protected-Infrastruktur-Änderung.
