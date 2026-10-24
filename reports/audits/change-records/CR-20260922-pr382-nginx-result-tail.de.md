# Change Record: Gemeinsame Verbindungs- und URI-Rückgabebehandlung

**Sprache:** [English](CR-20260922-pr382-nginx-result-tail.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-nginx-result-tail` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `81e53a943fb149a92eb4214091f81a217c567f8b` |

## Motivation und Problemstellung

Die exakte Sonar-Abfrage für `84c378ac` zeigte zwei doppelte Blöcke in
`ngx_http_modsecurity_access.c`, beginnend bei Zeile 391 und 469. Sechs neue
Zeilen waren doppelt; die New-Code-Dichte betrug 0,09965122072745392 Prozent.
Beide Blöcke behandelten dieselben Verbindungs-/URI-Rückgaben und Interventionen.

## Akzeptanzkriterien

Doppelten Code durch gemeinsame tatsächliche Logik entfernen, nicht durch
Scannereinstellungen oder veränderte Schreibweise verschleiern. Nativer
Phasenerfolg bleibt exakt eins. Native Fehler dürfen keine Interventionsabfrage
auslösen. Positive Hoststatus bleiben unverändert, negative ergeben terminal 500.
Beide Aufrufer müssen PCRE und die URI-Ereignisklammer vorher wiederherstellen.

## Implementierungsentscheidung und Begründung

Der private Helfer `ngx_http_modsecurity_request_native_result()` besitzt den
gemeinsamen Abschluss. Native Verbindungs-/URI-Aufrufe, Metadatenkonvertierung
und Phasenklammern bleiben getrennt. Die Diagnosephase ist ein statisches Literal,
kein Request-Inhalt. Byte-Append und strikter Dateileser bleiben unverändert.

## Geänderte Dateien

NGINX-Access-Quelltext, `tests/test_nginx_request_phase_completion.py`, Pflicht-
Lint-Schritt und dieser zweisprachige Change Record. Parallele Envoy-/CGo-Arbeit bleibt erhalten.

## Ausgeführte Befehle

Die Pflicht-CI führt `python -m unittest -v tests.test_nginx_request_phase_completion`
aus. Sechs Tests kompilieren beide tatsächlichen Aufrufer und den echten Helfer
mit `-std=c17 -Wall -Wextra -Werror`. Ergebnisse für die neue SHA stehen aus.
Kein lokaler Projektbefehl wurde ohne vorgeschriebenen RTK-Wrapper ausgeführt.

## Security-Auswirkung

Strikter nativer Erfolg, ursprüngliche kanonische Ursache, terminale Hostrückgaben
und Konvertierungs-/Puffergrenzen bleiben erhalten. Keine Ausnahmen, akzeptierten
Befunde, erweiterten Berechtigungen oder sachfremden nativen Änderungen.

## Runtime-Evidence

Tests verwenden echten Aufrufer-/Helfercode mit kontrollierter nativer Engine,
Adresskonvertierung, kanonischer Fehlermeldung und Hostweiterleitung. Geprüft werden
Fehler/Noop, positive HTTP-Statuswerte, negative Rückgaben, erste Ursache und
Konvertierungsfehler. Vorhandene Request-, Phasen- und Mutationstests bleiben Pflicht.

## Bekannte Einschränkungen

Dies ist ein verhaltenserhaltendes I09-Refactoring, kein Nachweis für sämtliche
Request-API-Fehlerausgänge oder alle I10-/I12-Adapterrouten. Kein Live-NGINX-Transportlauf.

## Verbleibende Risiken

Frische Sonar-Zähler und betroffene Gesamt-CI bleiben erforderlich. Eine gerundete
Zusammenfassung beweist keine null doppelten Zeilen. Apache-/Routenlücken bleiben getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale Builds und Hosttests benötigen die nicht verfügbare RTK-Umgebung.
Verifikation nutzt GitHub-CI. Kein Ergebnis wird von früheren Commits übernommen.

## Finaler Diff- und Review-Status

Nur Draft-PR #382; kein Merge, Master-/Force-Push oder Submodul-/Abhängigkeitswechsel.
