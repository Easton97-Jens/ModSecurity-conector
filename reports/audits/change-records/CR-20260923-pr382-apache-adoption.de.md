# Change Record: Native Apache-Adoption und echter Diagnoseabgleich

**Sprache:** [English](CR-20260923-pr382-apache-adoption.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260923-pr382-apache-adoption` |
| Datum (UTC) | `2026-09-23` |
| Basis-Revision | `cac867da7292f6ca82fc76fee3b974382881c5b1` |

## Motivation und Problemstellung

Der neue Apache-Lifecycle-Collector war implementiert; seine 20 kompilierten
APR-/Common-Regressionen bestanden. Die zusätzliche Adoption-Assertion verlangte
noch den alten Null-Rücksprung ohne Bereinigung und die Redirect-Ausgabe direkt
im Collector statt im geprüften Helfer. Damit scheiterten Root-Quick-Check,
Common-, Apache- und NGINX-Jobs nach ansonsten bestandenen Assertions.

## Akzeptanzkriterien

Den echten sicheren Collector akzeptieren und fehlende Bereinigung, unbekannte
native Werte, falsche Fehlerklassen, fehlende Callback-Sperre und Headeränderung
nach Antwortbeginn zurückweisen. Alle übrigen Assertions, vorhandenen Mutationen,
Compilerwarnungen und Sonar-Null-/Duplikationsgates erhalten. Kein Laufzeitumbau.

## Implementierungsentscheidung und Begründung

Vorhandenen kommentar-/literalbereinigten Funktionsparser und Redirect-Prüfer
wiederverwenden. Ein begrenzter Kontrollflussprüfer verlangt geordnete exakte
Rückgaben, erste Fehlerursache, neutrale Ergebniszuweisung und gemeinsame
Bereinigung. Nach dem nativen Aufruf ist nur ein Return erlaubt; der Schluss
muss Puffer freigeben, Callback-Sperre lösen und das erfasste Ergebnis zurückgeben.

Neun neue isolierte Quellcodetests nutzen die bestehende Testumgebung. Negative
Fälle verlangen Exitcode eins und die genaue FAIL-Zeile. Die bisherigen
Adoptiontests laufen daneben im Apache-Job; kein alter Test entfällt.

## Geänderte Dateien

Apache-Review-Checker, neues Neun-Fälle-Testmodul, bestehender Apache-Workflow
und dieser zweisprachige Bericht. Die vorherige einzeilige Bootstrap-Korrektur
ist unten erfasst; dieser Teil ändert keine Produktivquelle oder Abhängigkeit.

## Ausgeführte Befehle

Verpflichtender entfernter Befehl, für den neuen Commit noch ausstehend:

```sh
python3 -m unittest -v tests.test_apache_common_adoption tests.test_apache_native_adoption
```

Bei Basis cac867da bestand Job 107132681171 in Lauf 35846145029: acht Cleanup-
Quellcodefälle, 20 echte APR-/Common-Lifecycle-Fälle und tatsächlicher Apache-
Modulbuild aus versionierten Quellen mit Laden und Loopback-Smoke. Der getrennte
Strukturjob scheiterte an der alten Interventionsassertion. Frische Gesamt-CI bleibt nötig.

## Security-Auswirkung

Der angepasste Checker verstärkt Bereinigung und typisierte Fehlerprüfung und
akzeptiert weder Kommentar- noch konstant-falsche Attrappen. Der echte Bootstrap
behält 200/403-Kontrollen, ungültige-ID-500, Connection:close, Ausschluss des
Dokumenthandlers und genau zwei Diagnosen. Dessen alte Suchzeichenfolge wurde
in cac867da an die tatsächliche allgemeine Operation-Diagnose angepasst.

## Runtime-Evidence

Der Basis-Bootstrap führt für die genannten Fälle echtes httpd/libModSecurity aus.
Native Fehlerinjektion kontrolliert Engine und Ereignisausgabe; APR und Common
sind echt. Mutationen bleiben Quellcodenachweise. Keine dieser Ebenen beweist
alle Routen, physische JSONL-Ausgaben oder sämtliche späten Transportreaktionen.

## Bekannte Einschränkungen

I09/I10 sind insgesamt noch offen. Traefiks Antwortbeginn-Handler nutzt weiterhin
die void-Kompatibilitätsschnittstelle und meldet danach Erfolg: Hier fehlen Code-
Korrektur und Fehlerinjektion, nicht nur Hostbestätigung. Weitere Routen bleiben
getrennt. Der verpflichtende native Envoy-Build läuft bei Vorbereitung noch.

## Verbleibende Risiken

Weitere Integrationstests können eigenständige alte Annahmen zeigen. Echte Fehler
und vorhandene Schutzprüfungen erhalten. Secret-Scanning bleibt ein unabhängiger
Blocker und wird nicht durch ein grünes Sonar-Ergebnis erledigt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokale Repository-Ausführung; die Sandbox kann keinen vollständigen Checkout
abrufen. Entfernte CI liefert den Ausführungsweg. Neue Tests und Sonar-Metriken
erst nach tatsächlicher Abfrage als bestanden melden. RTK blockiert entfernte APIs/CI nicht.

## Finaler Diff- und Review-Status

Nur Draft-PR #382. Parallele Arbeit, Produktivquellen und Berechtigungen bleiben
erhalten. Kein Merge, Master-/Force-Push, Release oder Deployment.
