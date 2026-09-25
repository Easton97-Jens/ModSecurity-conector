# Change Record: Terminale Envoy-Bridge-Fehler und Antwortbeginn

**Sprache:** [English](CR-20260922-pr382-envoy-bridge.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-envoy-bridge` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `57d42c575372edca0149465038d8a683a11d494d` |

## Motivation und Problemstellung

I09/I10 und routenspezifische I12-Nachweise in PR #382 fortführen. Die C-Bridge
von ext_proc verwarf Common-Commitfehler und konnte nach fehlgeschlagenem Append
oder EOS erneut Common aufrufen. Auch leeres Antwort-EOS markierte Bodybeginn.
Der Go-Aufrufer meldete nach der bisherigen void-API stets Erfolg. Common-
Profiltests allein prüfen diese Adapterfehler nicht.

## Akzeptanzkriterien

Nur Common-Rückgabe eins ist erfolgreich. Erste Adapterursache erhalten, native
Wiederholungen nach Fehlern sperren, EOS nur nach Erfolg und Bodybeobachtung
monoton markieren. Technische Fehler dürfen keine alte Regel für späteres
Log-only behalten. Alte void-ABI erhalten und Fehler sofort bis Go weitergeben.

## Implementierungsentscheidung und Begründung

Ein privater Fehlercode markiert den terminalen Zustand vor Common-Fehler- und
Ereignisaufrufen. Kein fremder Fehlertext wird gespeichert. Common erhält eine
bereits vorhandene native Ursache; neue Connector-Fehler bekommen eine kanonische
Fehlermarkierung. Ein geprüfter privater Commithelfer stoppt vor Bodyübernahme.
Request- und Response-EOS teilen eine Implementierung bei erhaltenen Helfernamen.
Ein neuer öffentlicher geprüfter Wrapper gibt dasselbe Ergebnis weiter; der
Go-Empfänger gibt Fehler sofort zurück. Alte void-Aufrufer behalten Fehlerzustand.

## Geänderte Dateien

- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- Öffentlicher Header und Go-Aufrufer `common_runtime_engine.go`.
- `common_runtime_commit_test.go` für echte Common-/Go-Regressionen.
- `tests/test_envoy_bridge_failures.py` und `.github/workflows/lint.yml`.
- Dieser zweisprachige Bericht.

## Ausgeführte Befehle

```sh
python -m unittest -v tests.test_envoy_bridge_failures
```

Alle zehn Tests bestanden bei `31200e8c` im Lint-Job 106891644804, Lauf
35770777984. Vollständige produktive C-Bridge mit eingecheckten Headern,
kontrollierten Common-Aufrufen, C17 und Wall/Wextra/Werror. Bestehende Tests
und Sonar-Befundnull bestanden ebenfalls; Duplikationsabfrage scheiterte wegen
geändertem PR-Head. Neue Go-/API-Folgeprüfungen stehen bei Vorbereitung aus.

## Security-Auswirkung

Commitfehler erreichen kein Body-Append. Fehlerwiederholung ruft weder Ausgabe
erneut auf noch ersetzt sie die erste Adapterursache. Alte Regelmetadaten werden
bei technischen Fehlern gelöscht, nicht zu gültigen Regeln umgedeutet. Leeres
EOS behauptet keine Bodylieferung. Keine neue Host-Resetfähigkeit wird behauptet.

## Runtime-Evidence

Die zehn Tests verwenden öffentliche C-Bridge-Aufrufe und echten Kontrollfluss.
Common Runtime und physischer Envoy-Transport sind dabei kontrollierte Grenzen.
Zwei neue Go-Fälle mit libmodsecurity-Buildtag prüfen frühen Commitfehler bis Go
und gültigen leeren Abschluss mit echtem Common-Vertrag. Vorhandensein beweist
keine Ausführung; ein nativer Go-Testlauf ist separat erforderlich.

## Bekannte Einschränkungen

I09, I10 und I12 bleiben für andere Routen und reale Transportfälle offen.
Dies ist kein ext_authz-/Companion- oder Sechs-Familien-Nachweis. Close bleibt
Besitzbereinigung, kein Nachweis physisch persistierter Auditdaten.

## Verbleibende Risiken

Common-Fehler-/Ereignisausgabe kann selbst scheitern; erste Adapterfehler müssen
ohne unbegrenzte Rekursion sichtbar bleiben. Native Bereinigung bleibt beim
vorhandenen Close-Pfad. Unabhängiges Secret-Scanning und Sonar bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projektbefehle oder gofmt, da RTK fehlt. GitHub-CI muss frische
Formatierungs-/Build-/Testnachweise liefern. Echtes gRPC, Live-Hosts und
physischer Logspeicher werden durch diese Grenztests nicht geprüft.

## Finaler Diff- und Review-Status

Parallele Sonar-Arbeit auf dem Branch erhalten. Kein Merge, Master-/Force-Push,
Framework-/MRTS-Eingriff, Abhängigkeitsupdate oder Scanner-Ausnahme.
