# Change Record: Native Logging-Rückgabe und Wiedereintritt

**Sprache:** [English](CR-20260922-pr382-native-logging.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260922-pr382-native-logging` |
| Datum (UTC) | `2026-09-22` |
| Basis-Revision | `1ce569e1afce55e17c767e1e06b0266874fe8c3e` |

## Motivation und Problemstellung

Der native NGINX-Auditabschluss ignorierte Rückgaben von `msc_process_logging()`
und setzte keinen eigenen Marker für einen einmaligen Versuch. Fehlerhafter
nativer Abschluss konnte als Erfolg erscheinen; erneute Logphasen-Aufrufe konnten
die Engine nochmals aufrufen. Die native Upstream-Logging-API dokumentiert
booleschen Operationserfolg, nicht den Byte-Append-Vertrag für `ProcessPartial`.

## Akzeptanzkriterien

Nur native Rückgabe eins akzeptieren. Fehlgeschlagenen Abschluss beim
Wiedereintritt erhalten, doppelte native Aufrufe vermeiden, erste kanonische
Ursache und PCRE-Allokationsklammer bewahren. Fehlender nativer Zustand darf die
Engine nicht erreichen. Ein fehlgeschlagener kanonischer Abschluss darf nicht
wegen erfolgreichen Audit-Processings zum Erfolg werden.

## Implementierungsentscheidung und Begründung

Das vorhandene Feld `logged` reserviert den Versuch vor nativem Eintritt; ein
getrenntes Bit `native_logging_failed` hält ausstehenden/fehlerhaften Ausgang fest.
Statische native Betreiberdiagnosen melden Fehler ohne rekursive JSONL- oder
native Logaufrufe. Nach kanonischem Sequenzfehler läuft der Auditabschluss noch
einmalig zur nativen Erfassung; sein Erfolg repariert die Sequenz nicht. Aus der
Logphase wird keine Antwort ersetzt oder abgebrochen und keine frühere Lieferung
behauptet. Bisherige Early-Log-Aufrufer behalten ihre HTTP-Policy; das gespeicherte
Flag verhindert, dass ein späterer Logaufruf fehlerhaftes Audit als Erfolg ausgibt.

## Geänderte Dateien

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `tests/test_nginx_native_logging.py`
- `.github/workflows/lint.yml`
- Dieser Bericht und seine englische Begleitdatei.

## Ausgeführte Befehle

Das neue Modul gehört zum vorhandenen Request-/Native-CI-Schritt:

```sh
python -m unittest -v tests.test_nginx_native_logging
```

Die Ausführung steht bei Vorbereitung aus. Acht kompilierte Funktionstests
prüfen gültige, Null-, negative und undokumentierte Rückgaben, fehlenden Zustand,
fehlerhaften kanonischen Abschluss, Erhalt der ersten Ursache, rekursiven Eintritt
und wiederholte Aufrufe. C17-Kompilierung mit `-Wall -Wextra -Werror` ersetzt nicht
die geänderte Funktion.

## Security-Auswirkung

Native Auditfehler bleiben explizite Fehler, nicht Allow oder erfolgreiches
Audit. Keine rohen Nutzdaten, Zugangsdaten oder unbegrenzten Diagnosewerte werden
ergänzt. HTTP-Policy und vorhandene Rule-Match-Ereignissemantik bleiben unverändert.

## Runtime-Evidence

Kontrollierte Engine-, kanonische Operations- und abschließende Host-Schnittstellen
umgeben die tatsächlich geänderten Funktionen. Dies beweist keine Auditdatei-
Persistenz oder Behandlung der Log-Callback-Rückgaben durch einen laufenden Server.

## Bekannte Einschränkungen

Dies schließt eine native I09-Aufruflücke und doppelte Auditversuche, nicht alle
physischen I11-Ausgaberouten. Eine Logphase kann bereits gelieferte Bytes nicht
zurückholen. Andere Adapter und die vollständige direkte/Companion-Routenmatrix
bleiben getrennte Arbeit.

## Verbleibende Risiken

Das Auditfehler-Flag ist privater NGINX-Request-Zustand, kein öffentliches
Wire-Feld. API-Erfolg beweist nur nativen API-Erfolg, keinen unabhängigen fsync-
oder Client-Liefernachweis. Frühere Fehlerklassen bleiben maßgeblich.

## Nicht ausgeführte Prüfungen mit Begründung

Wegen des fehlenden vorgeschriebenen RTK-Wrappers wurden keine lokalen
Projektbefehle ausgeführt. Frische GitHub-CI und Sonar null für den exakten Head
bleiben erforderlich. Live-Host-Logging und routenübergreifende Vergleiche wurden
in dieser Änderung nicht ausgeführt.

## Finaler Diff- und Review-Status

Quellcode, Regressionstests und zweisprachige Dokumentation bleiben in Draft-PR
#382. Kein Merge, Master-Push, Force-Push, Scanner-Ausnahme oder Abhängigkeitsupdate.
