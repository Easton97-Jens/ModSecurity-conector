# Change Record: exakte Sonar-Befundzähler

**Sprache:** [English](CR-20260922-pr382-sonar-counts.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-sonar-counts` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `e8d5e5081f166e8a9b01bbb84ce4baf6530109d9` |

## Motivation und Problemstellung

Die entfernte Zusammenfassung verwendet `1 New issue`, nicht den erwarteten Plural.
Die Prüfung schlug korrekt fehl, aber vor der begrenzten Ausgabe der Fundstelle.
Akzeptierte Issues gehörten noch nicht zur erzwungenen Null-Bedingung.

## Akzeptanzkriterien

Singular und Plural eindeutig lesen. Jeden positiven Zähler neuer/akzeptierter
Issues, Hotspots oder Annotationen zurückweisen. Fehlende Nachweise bleiben Fehler.
Auch bei einem einzelnen Issue begrenzte Annotationen ohne Quelltextauszüge ausgeben.

## Implementierungsentscheidung und Begründung

Feste Beschriftungsmuster verwenden, beide Schreibweisen gemeinsam zählen und
Nachweis akzeptierter Issues verlangen statt null anzunehmen. Keine Scanneränderung.

## Geänderte Dateien

- `ci/checks/common/check-sonar-zero.py`
- `tests/test_sonar_zero_gate.py`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Der bestehende CI-Einstieg führt aus:

```sh
python -m unittest -v tests.test_sonar_zero_gate
```

Vier neue Regressionen prüfen Singular-Diagnosen, akzeptierte Befunde, mehrdeutige
Mischformen und fehlende Akzeptanzzähler. Ausführung bei Vorbereitung noch ausstehend.

## Security-Auswirkung

Dies verschärft die Null-Befund-Prüfung. Kein Befund wird akzeptiert, verborgen oder
unterdrückt. Exakte SHA, Anbieterprüfung und begrenzter Lesezugriff bleiben erhalten.

## Runtime-Evidence

Dies ist ein Parser für CI-Nachweise, kein Connector-Laufzeitnachweis.

## Bekannte Einschränkungen

Der von Sonar gemeldete Quellcodebefund benötigt eine separate Korrektur. Die
Parserreparatur allein erfüllt weder die Null-Vorgabe noch I09-I12.

## Verbleibende Risiken

Weitere Änderungen des Sonar-Zusammenfassungsformats müssen bis zur Prüfung fehlschlagen.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projekttests, da der vorgeschriebene RTK-Wrapper fehlt. Entfernte
CI-/Sonar-Ergebnisse müssen für den exakten neuen Commit gelesen werden.

## Finaler Diff- und Review-Status

Als eingegrenzte Fortsetzung in Draft-PR #382 vorbereitet. Kein Merge, Force-Push,
keine Scanner-Ausnahme, Issue-Akzeptanz oder Framework-/MRTS-Änderung.
