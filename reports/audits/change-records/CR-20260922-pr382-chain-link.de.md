# Change Record: Verlinkung des nativen Interventionstests

**Sprache:** [English](CR-20260922-pr382-chain-link.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-chain-link` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `3730eaa03b2f76ccac3baebfc862d8a8417c99ef` |

## Motivation und Problemstellung

Die native Interventionsketten-Suite scheiterte beim Linken, bevor ihre zehn
Verhaltenstests laufen konnten. Die Testdatei linkte `block_statuses.c`, aber
nicht dessen echte Abhängigkeit `http_status.c`. Dieser Fehler besteht bereits
bei `7fe606c5` in [CI-Job 106698812691](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35713306728/job/106698812691).

## Akzeptanzkriterien

Die tatsächlich fehlende Abhängigkeit linken und die vorhandenen zehn Tests
ungeändert ausführen: keine Stubs, entfernten Assertions oder gelockerten
Compilerflags. Native/Hostfehler, gültige Regeln, Bereinigung und Safe-/Strict-/
Off-Kontrollen bleiben erhalten.

## Implementierungsentscheidung und Begründung

Nur `http_status.c` zur vorhandenen Testquellenliste hinzufügen. Produktivquellen
bleiben unverändert. Die Linkerdiagnosen benennen diese Abhängigkeit ausdrücklich.

## Geänderte Dateien

- `tests/test_nginx_native_intervention_chain.py`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Der vorhandene CI-Einstiegspunkt lautet:

```sh
python -m unittest -v tests.test_nginx_native_intervention_chain
```

Die Ausführung nach der Korrektur steht bei Vorbereitung aus. Der vorherige
CI-Fehler betraf unaufgelöste Symbole, keine fehlgeschlagene Verhaltensassertion.

## Security-Auswirkung

Die ursprünglichen Sicherheitsregressionen wieder ausführbar machen, statt den
fehlgeschlagenen Aufbau zu umgehen. Produktivlogik, Flags, Scannerregeln und
Berechtigungen bleiben unverändert.

## Runtime-Evidence

Die Testdatei kompiliert echten Collector, Dispatcher, P4-Aufrufer und Common-
Lebenszyklus mit kontrollierten nativen und abschließenden Host-I/O-Schnittstellen.
Dies ist kein laufender Host.

## Bekannte Einschränkungen

Dies schließt nicht alle I09-I12-Kriterien ab. Nach dem Linken sichtbar werdende
Verhaltensfehler müssen unabhängig untersucht werden.

## Verbleibende Risiken

Bestandene kontrollierte Aufrufkettentests beweisen keine Client-Transportergebnisse.

## Nicht ausgeführte Prüfungen mit Begründung

Wegen des fehlenden vorgeschriebenen RTK-Wrappers wurden keine lokalen Befehle
ausgeführt. Frische CI- und exakte Head-Sonar-Nachweise bleiben erforderlich.

## Finaler Diff- und Review-Status

Einzeilige Test-Build-Korrektur samt zweisprachiger Nachverfolgbarkeit nur im
bestehenden Draft-PR. Kein Merge, Master-Push, Force-Push oder Versionswechsel
von Abhängigkeiten.
