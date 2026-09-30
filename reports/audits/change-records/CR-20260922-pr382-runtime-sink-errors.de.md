# Change Record: Erhalt von Runtime-Ereignisausgabefehlern

**Sprache:** [English](CR-20260922-pr382-runtime-sink-errors.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-runtime-sink-errors` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9` |

## Motivation und Problemstellung

Die Runtime speicherte Ereignisfehler als Boolean und meldete jeden Folgefehler
als `MSCONNECTOR_ERROR_EVENT_TOO_LARGE`. Physische Schreib-/Flushfehler verloren
dadurch ihre I/O-Klasse. Ein bereits ausgegebenes terminales Ereignis konnte
außerdem einen späteren Hostaktions-Ereignisfehler beim Abschluss übergehen.
Snapshot-Bereinigung ersetzte weitergegebene Fehler durch einen generischen
Fehler wegen unvollständigem Snapshot.

## Akzeptanzkriterien

Ursprüngliche Ereignisfehlerklasse auch ohne Fehlerausgabe des Aufrufers erhalten.
Fehlgeschlagene Ereignisse nicht wiederholen und den Hash bei Fehlern nicht
fortschreiben. Frühere terminale Ausgabe darf späteren Ereignisfehler nicht
verdecken. Abschluss, Abschluss nach Hostablehnung, Hostaktionsaufzeichnung und
geprüfte Bereinigung müssen Fehler statt Erfolg erhalten. Ursprüngliche
Transaktionsursache, erfolgreicher Normalabschluss und Ressourcenfreigabe bleiben.

## Implementierungsentscheidung und Begründung

Privaten Boolean durch den vorhandenen Enum-Fehlercode ersetzen; keine geliehenen
Meldungen speichern. Beide Erzeuger verwenden denselben geprüften Schreiber mit
stets vorhandener lokaler Fehlerausgabe. Wiederholung verwendet statischen
Standardtext und ursprünglichen Code. Fehlervorrang vor terminale
Erfolgsabkürzungen setzen und geprüfte Bereinigung von Snapshot-Validierung
trennen. Besitz der Ausgabe, Grenzen, JSONL-/Hash-Format und Profilfähigkeiten
bleiben unverändert.

## Geänderte Dateien

- `common/runtime/msconnector_runtime.c`
- `tests/test_runtime_event_sink_failures.py`
- `.github/workflows/lint.yml`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Erforderlicher CI-Einstieg:

```sh
python -m unittest -v tests.test_runtime_event_sink_failures
```

Ausführung steht bei Vorbereitung aus. Acht Testmethoden kompilieren echte
Runtime-Strukturen, Erzeuger, Schreiber und Abschlussfunktionen mit echten
Common-Fehler-, Allokator-, Serialisierungs-, Hash- und Lebenszyklusmodulen.
GNU-stdio-Cookies injizieren physische Schreib-, Kurzschreib- und Flushfehler.
Eine getrennt kompilierte Negativkontrolle reproduziert die ursprüngliche
Fehlerklassifikation. Native Audit-/Freigabe-Callbacks sind kontrollierte
Schnittstellen, keine echte Engine-Ausführung.

## Security-Auswirkung

Fehlerhafte Metadatenausgabe kann keinen erfolgreichen Transaktionsabschluss
vortäuschen. Keine rohen Nutzdaten, Zugangsdaten, Scanner-Ausnahmen oder nicht
unterstützten Fähigkeiten werden ergänzt. Ursprüngliche Transaktionsursachen
und unabhängige Grenzen bleiben unverändert.

## Runtime-Evidence

Testebene ist kompilierte Runtime-/stdio-Integration, nicht laufende HTTP-Hosts
oder eine Routenmatrix für sechs Familien. Erfolgreiches stdio-Flush ist kein
Persistenz-/fsync-Nachweis. Kompilierung der Negativkontrolle ersetzt keine Tests
des aktuellen Codes.

## Bekannte Einschränkungen

Dies korrigiert die gefundenen Runtime-I11-Fehlermarker- und Abschlusslücken.
Physische Apache-/SPOP-Ausgabewege brauchen weiterhin eigene Änderungen und Tests.
Wiederholte Abbruch-/phasenungültige Operationen behalten ihre API-Verträge;
damit wird keine vollständige Gleichheit jedes Fehlerausgangs aller Routen behauptet.

## Verbleibende Risiken

Nach fehlerhaftem erforderlichem Ereignis meldet der Abschluss Fehler, ohne einen
weiteren nativen Auditversuch zu starten. Best-Effort-Zerstörung gibt weiterhin
nativen und kanonischen Zustand frei. Wiederherstellung der gemeinsamen Ausgabe
zwischen verschiedenen Transaktionen und alle Hostinterpretationen bleiben
gesonderte Verifikationsarbeit.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projektbefehle wegen fehlendem vorgeschriebenem RTK-Wrapper.
Aktuelle GitHub-CI, exakte Sonar-Null-Prüfung und tatsächliche Hostergebnisse
brauchen frische Verifikation. Unabhängiges Secret-Scanning bleibt ungeklärt.

## Finaler Diff- und Review-Status

Als eingegrenzte Produktiv-/Testfortsetzung in Draft-PR #382 vorbereitet. Kein
Merge, Master-Push, Force-Push, Abhängigkeits-, Framework-/MRTS- oder Scannerwechsel.
