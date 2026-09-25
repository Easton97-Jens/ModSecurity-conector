# Change Record: native Interventionsabfrage und späte Weiterleitung

**Sprache:** [English](CR-20260922-pr382-native-intervention.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-native-intervention` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `7a52a55cfa4eb4c4c85ed44396e7137ef013f5aa` |

## Motivation und Problemstellung

Der native NGINX-Interventionswrapper akzeptierte jede Rückgabe ungleich null.
Bei einem gültigen späten Regeltreffer versuchte er außerdem, die bereits begonnene
Antwort zu ersetzen. Die negative Hostrückgabe wurde vor der Safe-/Strict-Policy
vom P4-Aufrufer als technischer Fehler behandelt. Ein Test mit vorgegebener
Wrapperrückgabe konnte diese Verwechslung nicht erkennen.

## Akzeptanzkriterien

Nur native null und eins gelten als gültig. Veraltete Regel-/Statusmetadaten bei
Abfrage löschen, native Ausgaben auf jedem Rückweg einmal freigeben und nicht-
disruptive Ergebnisse erhalten. Gültige späte P4-Regeln müssen ohne vorherigen
Headerersatz zur Safe-/Strict-Zuständigkeit gelangen. Off und gültige Weiterleitung
vor Antwortbeginn behalten ihr natives Verhalten. Echte Fehler geben keinen Body weiter.

## Implementierungsentscheidung und Begründung

Kleinen nativen Rückgabekollektor und Fehleradapter ergänzen; nur bereits begonnene
P4-Antworten in Safe/Strict werden nach Regelkorrelationsprüfung weitergereicht.
Der bestehende Bodyfilter bleibt für späte Policy zuständig. Ein gemeinsamer
Bereinigungsausgang bleibt erhalten. Keine überschatteten nativen APIs oder erfundenen
Transportfähigkeiten.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `tests/test_nginx_native_intervention_chain.py`
- `.github/workflows/lint.yml`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Der verpflichtende CI-Befehl enthält:

```sh
python -m unittest -v tests.test_nginx_native_intervention_chain
```

Zehn Testmethoden kompilieren echten Kollektor, Wrapper, Statusweiterleitung,
P4-Aufrufer und späte Policy mit echtem Common-Lebenszyklus und Regelkorrelation.
Engine und abschließende Hostausgabe sind kontrollierte Testgrenzen. Ausführung
steht bei Vorbereitung aus.

## Security-Auswirkung

Undokumentierte native Ergebnisse, fehlender erforderlicher Kontext und ungültige
Korrelation werden nicht zu erfolgreicher Regelbehandlung. Gültige späte Regeln
werden nicht allein wegen gesendeter Header als technische Fehler eingestuft.
Bereinigungszuständigkeit, begrenzte Metadaten und Fehlerweitergabe bleiben aktiv.

## Runtime-Evidence

Dies sind kompilierte native Aufrufkettennachweise, kein Live-Host, keine vollständige
native Engine oder HTTP/2-/HTTP/3-Transportprüfung. Bestehende fokussierte Tests bleiben Pflicht.

## Bekannte Einschränkungen

Die vollständigen I09-I12-Anforderungen an Erzeuger/Ausgaben und Integrationsrouten
bleiben in der Hauptcheckliste. Native Auditlog-Rückgaben und unabhängige Logausgaben
benötigen eigene Prüfung. Nicht alle Routen werden hierdurch vollständig.

## Verbleibende Risiken

Ein später Abbruch holt gesendete Bytes nicht zurück. Off behält bewusst den alten
nativen Pfad nach Antwortbeginn. Sichtbare Hostaktionen benötigen getrennte Beobachtung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Projektbefehle, da RTK fehlt. Der neue Commit benötigt eigene CI-
und exakte Sonar-Null-Ergebnisse. Der unabhängige Secret-Scan-Fund wird durch diese
Änderungen weder gelöst noch unterdrückt.

## Finaler Diff- und Review-Status

Nur für Draft-PR #382 vorbereitet. Kein Merge, Master-Push, Force-Push, keine
Abhängigkeits-/Framework-/MRTS-Änderung oder abgeschwächte Scanner-/Testpolicy.
