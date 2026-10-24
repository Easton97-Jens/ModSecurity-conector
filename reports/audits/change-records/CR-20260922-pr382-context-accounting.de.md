# Change Record: native Kontextgruppe für Zähler

**Sprache:** [English](CR-20260922-pr382-context-accounting.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-context-accounting` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `96c41eb287778e807daeba5b28f97bd5d86fbc0a` |

## Motivation und Problemstellung

Sonar meldete nach der Request-Fehlerarbeit 21 oberste Kontextfelder. Die
begrenzten Header-/Body-Zähler bilden eine zusammengehörige Gruppe gleicher Lebensdauer.

## Akzeptanzkriterien

Alle Feldnamen, Zählerreihenfolge, Nullinitialisierung und unabhängigen Request-
Fehler-/Response-Terminalzustände erhalten. Keine Sonar-Ausnahme oder Zustandsentfernung.

## Implementierungsentscheidung und Begründung

Eine anonyme C17-Wertegruppe fasst die sieben aufeinanderfolgenden Zähler zusammen.
Dies folgt dem vorhandenen Common-Vertragsstil, ohne Zugriffsmakros oder zusätzliche
Allokation. Native Helfer verwenden unverändert dieselben Mitgliedsnamen.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_nginx_context_accounting.py`
- `.github/workflows/lint.yml`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Die neue verpflichtende CI-Prüfung lautet:

```sh
python -m unittest -v tests.test_nginx_context_accounting
```

Sie kompiliert die echte Kontextdeklaration in C17 mit Warnungen als Fehlern und
pedantischer Prüfung, jeweils mit und ohne Sanity-Checks. Sie prüft unabhängige
Zähler- und Terminalzustandsänderungen. Ausführung steht bei Vorbereitung aus.

## Security-Auswirkung

Kein Verhalten, keine Grenzen, Bereinigungszuständigkeit, Compilerwarnung oder
Scannerregel wird entfernt. Keine Ereignisnutzdaten oder neue externe Schnittstelle.

## Runtime-Evidence

Der Deklarationstest ist kein laufender Server. Bestehende native Request- und
Spätfehlerprüfungen sowie frische exakte Sonar-Nachweise bleiben erforderlich.

## Bekannte Einschränkungen

Diese Strukturkorrektur erledigt weder I09-I12 noch den vollständigen Live-Host-Vergleich.

## Verbleibende Risiken

Alle nativen Übersetzungseinheiten müssen nach internen Layoutänderungen gemeinsam
neu gebaut werden. Keine Kompatibilität mit früher gebauten Modulobjekten wird behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projektbefehle, da der vorgeschriebene RTK-Wrapper fehlt. Der
unabhängige Secret-Scan-Fund bleibt ungeklärt.

## Finaler Diff- und Review-Status

Nur für den bestehenden Draft-PR vorbereitet; kein Merge, Master-Push, Force-Push,
keine Scanner-Ausnahme, Issue-Akzeptanz oder Abhängigkeits-/Framework-/MRTS-Änderung.
