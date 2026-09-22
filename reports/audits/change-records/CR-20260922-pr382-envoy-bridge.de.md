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
Diese Adapterfehler werden durch Common-Profiltests allein nicht abgedeckt.

## Akzeptanzkriterien

Nur Common-Rückgabe eins ist erfolgreich. Erste Adapterursache erhalten, native
Wiederholungen nach Fehlern sperren, EOS nur nach Erfolg und Bodybeobachtung
monoton markieren. Technische Fehler dürfen keine alte Regel für späteres
Log-only behalten. Öffentliche void-Kompatibilität und Hostgrenzen erhalten.

## Implementierungsentscheidung und Begründung

Ein privater Fehlercode markiert den terminalen Zustand vor Common-Fehler- und
Ereignisaufrufen. Kein fremder Fehlertext wird gespeichert. Common erhält eine
bereits vorhandene native Ursache; neue Connector-Fehler bekommen eine kanonische
Fehlermarkierung. Ein geprüfter privater Commithelfer stoppt vor Bodyübernahme.
Request- und Response-EOS teilen eine Implementierung bei erhaltenen Helfernamen.
Die void-Kompatibilitätsfunktion merkt Fehler für folgende Bridge-Aufrufe.

## Geänderte Dateien

- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- `tests/test_envoy_bridge_failures.py`
- `.github/workflows/lint.yml`
- Dieser zweisprachige Bericht.

## Ausgeführte Befehle

Neuer erforderlicher CI-Befehl; bei Commitvorbereitung noch ausstehend:

```sh
python -m unittest -v tests.test_envoy_bridge_failures
```

Zehn Tests kompilieren die vollständige produktive C-Bridge mit eingecheckten
öffentlichen Headern und kontrollierten Common-Runtime-Aufrufen. C17,
Wall/Wextra/Werror und normale Linker-Sektionsauswahl; keine Produktivverzweigung
wird entfernt oder ersetzt. Common-Fehlerinjektion ist kein libModSecurity-Lauf.

## Security-Auswirkung

Commitfehler erreichen kein Body-Append. Fehlerwiederholung ruft weder Ausgabe
erneut auf noch ersetzt sie die erste Adapterursache. Alte Regelmetadaten werden
bei technischen Fehlern gelöscht, nicht zu gültigen Regeln umgedeutet. Leeres
EOS behauptet keine Bodylieferung. Keine neue Host-Resetfähigkeit wird behauptet.

## Runtime-Evidence

Dieser Schritt prüft öffentliche C-Bridge-Aufrufe und echten Bridge-Kontrollfluss.
Engine, Common-Ausgabe und physischer Envoy-Transport sind kontrollierte Grenzen.
Dies ist kein ext_authz-/Companion- oder Sechs-Familien-Laufzeitnachweis.

## Bekannte Einschränkungen

Der Go-Kompatibilitätsaufrufer nutzt noch den void-Commitaufruf: Für unmittelbare
Go-Fehlerweitergabe fehlen additive geprüfte API und Aufruferanpassung. Der
C-Fehlermarker verhindert inzwischen weitere Body-/Hostaktionsverarbeitung.
I09, I10 und I12 bleiben für weitere Routen und echte Transportfälle offen.

## Verbleibende Risiken

Common-Fehler-/Ereignisausgabe kann selbst scheitern; erste Adapterfehler müssen
ohne unbegrenzte Rekursion sichtbar bleiben. Native Bereinigung bleibt beim
vorhandenen Close-Pfad. Unabhängiges Secret-Scanning und Sonar bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projektbefehle, da RTK fehlt. Frische Build-/Testnachweise müssen
aus GitHub-CI kommen. Echtes gRPC, Live-Hosts und physischer Logspeicher werden
durch diese kontrollierten Grenztests nicht geprüft.

## Finaler Diff- und Review-Status

Parallele Sonar-Arbeit auf dem Branch erhalten. Kein Merge, Master-/Force-Push,
Framework-/MRTS-Eingriff, Abhängigkeitsupdate oder Scanner-Ausnahme.
