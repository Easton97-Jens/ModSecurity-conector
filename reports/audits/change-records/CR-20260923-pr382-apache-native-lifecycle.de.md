# Change Record: Apache-Grenzen für native Fehler und Lebenszyklus

**Sprache:** [English](CR-20260923-pr382-apache-native-lifecycle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260923-pr382-apache-native-lifecycle` |
| Basis-Revision | `ad22918e92849a10483439d72ac9a50154ec00be` |
| Umfang | Parent-Repository, Draft-PR #382, Implementierung I09/I10 |

## Motivation und Problemstellung

Der aktuelle Auftrag verlangt, I09 und I10 so weit zu bringen, dass nur echte
Hostnachweise fehlen. Im Apache-Code bestanden konkrete Lücken: ungeprüfte
Nichtnull-Interventionsrückgaben, bei Null nicht freigegebene native Puffer,
ungeprüfte Kopien, spätes Ändern von Location, Audit-Wiedereintritt und fehlende
Prüfung der Engine-Initialisierung. Das sind Codefehler, keine fehlenden
Hostberichte. Dieser Schritt bearbeitet sie, nicht pauschal alle anderen Routen.

## Akzeptanzkriterien

Operationsspezifische Rückgaben, erste Fehlerursache, Request-Besitz, gültige
Regelstatus und Body-Limits erhalten. Native Puffer auf jedem Ausgang nach dem
Aufruf freigeben; keine Änderung bereits gesendeter Header oder ausführbare
Intervention aus der Logphase. Fehlgeschlagenen Start ablehnen und Bereinigung
an die besitzende Konfigurationsgeneration binden. Alle Scannerregeln, null neue
Sonar-Befunde und exakt null neue Duplikation erhalten. Checkliste nur anhand
geprüfter Implementierung und tatsächlich ausgeführter Tests aktualisieren.

## Implementierungsentscheidung und Begründung

Ein privater Fehlermapper leert alte Regelmetadaten und übergibt die erste
kanonische Ursache an die vorhandene Einmal-Ereignisgrenze. Der native Collector
trennt exakte 0/1-Rückgaben von Fehlern; Kopien und Redirect-Speicher müssen vor
Headeränderungen vorhanden sein. Native und Hostfehler nutzen getrennte Aufrufer
desselben Mappers. Die Regelabbildung lehnt vorherige technische Fehler ab.
Audit markiert seinen Versuch vor nativen Callbacks und erhält Fehler. Der
Start veröffentlicht nur eine gültige Engine, prüft APR-Verwaltungsergebnisse
und verhindert, dass alte Konfigurationsbereinigung eine neue Engine zerstört.

## Geänderte Dateien

Apache-Modul und privater Zustand, Quellcodevertragsregressionen, kompilierte
native/APR-Lebenszyklustests und vorhandener Apache-CI-Job. Keine Abhängigkeits-
oder Framework-/MRTS-Änderungen. Physische Ereignisausgabe bleibt der getrennte
Implementierungspunkt I11.

## Ausgeführte Befehle

Keine lokalen Projektbefehle, da der verpflichtende RTK-Wrapper fehlt. Der
vorhandene GitHub-Workflow führt nach seinen bereits vorgesehenen Apache-/APR-
Installationen zusätzlich die neue Testsuite aus:

```sh
python3 -m unittest -v tests.test_apache_intervention_cleanup
python3 -m unittest -v tests.test_apache_native_lifecycle
make check-apache-autotools-bootstrap
```

Neue Ausführung und Sonar für den exakten Head stehen bei Vorbereitung aus.
Quellcodetests erhalten Besitz-/Reihenfolgeprüfungen und folgen dem echten Helfer;
die frühere Assertion zugunsten des undichten Null-Frühausgangs wird korrigiert.

## Security-Auswirkung

Technische Fehler übernehmen keine alte Regelkennung oder Redirect-Aktion.
Native Puffer besitzen genau einen Freigabepfad. Native und Host-Allokationsfehler
bleiben verschieden. Keine zusätzlichen Nutzdatenlogs, Fähigkeitsaufwertung,
Scanner-Ausnahmen, akzeptierten Befunde, Zugangsdatenänderung oder breiteren
CI-Berechtigungen.

## Runtime-Evidence

Zwanzig kompilierte Tests verwenden tatsächlich ausgewählte Produktfunktionen,
den eingecheckten Apache-Zustand, echte APR-Pools/-Tabellen und die echte Common-
Zustandsmaschine. Native Ergebnisse, Allokationsfehler, Diagnosen und abschließende
Ereignisausgabe sind kontrollierte Grenzen. Eine kompilierte Null-Cleanup-
Negativkontrolle reproduziert das ursprüngliche Leck. Kein Live-httpd-,
physischer Logpersistenz- oder Client-I/O-Nachweis.

## Bekannte Einschränkungen

I09/I10 bleiben während dieses Schritts insgesamt in Bearbeitung. Filter-/API-
Ausgänge außerhalb dieses Moduls, andere Integrationsrouten und die vorhandene
native Go-Verifikation müssen abgeglichen werden, bevor nur Hostnachweise offen
sein dürfen. I11-Ausgabelücken und I12-Routennachweise werden nicht umbenannt
oder als erledigt dargestellt.

## Verbleibende Risiken

Frische vollständige Modulkompilierung, Quellcode-/Adoptionsprüfungen, kompilierte
Tests und exakte Sonar-Nachweise bleiben erforderlich. Audit kann keine bereits
gesendete Antwort zurückholen. Ein unabhängiger Secret-Scan bleibt Freigabeblocker.

## Nicht ausgeführte Prüfungen mit Begründung

Keine lokalen Build-/Test-/gofmt-/Diff-Befehle wegen fehlendem verpflichtendem RTK.
Keine Live-Hosts oder vollständige Transportmatrix. Remote-Ergebnisse müssen für
den tatsächlich veröffentlichten Stand abgerufen werden; frühere grüne Läufe
sind kein Nachweis späterer Revisionen.

## Finaler Diff- und Review-Status

Nur bestehender Draft-PR-Branch; kein Merge, Master-/Force-Push oder Deployment.
