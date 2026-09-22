# Change Record: PR #382 native Rückgaben und Ereignisse

**Sprache:** [English](CR-20260921-pr382-native-results-events.md) | Deutsch

## Fortsetzung 2026-09-22: NGINX-Adoption-/Mutationsreparatur

Die Change-ID bleibt `CR-20260921-pr382-native-results-events`.
Getestete Revision: `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d`.
Der eingegrenzte nächste Schritt, Checklistenpunkt V06b, ist `passed`; der
Gesamt-PR bleibt `partial` und Draft. Die älteren Abschnitte unten bewahren die
historische Fortsetzung für `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` und ihre
Fehler. Dieser Abschnitt ersetzt nur deren NGINX-Adoption-/Mutationsstatus.

Der Checker erwartete ein einfaches `return ret`, obwohl der geprüfte Code nun
das Ergebnis der terminalen `ngx_http_modsecurity_phase4_fail_control`-Behandlung
zurückgibt. Zwei Mutationen suchten weiterhin das alte Fragment, und die isolierte
Repository-Kopie enthielt `ngx_http_modsecurity_phase4_error.h` nicht. Der fehlende
Header verursachte zusätzliche Makro-/Include-Fehler, die das eigentliche
Ergebnis einer Mutation verdecken konnten.

Geänderte Validierungsdateien:

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`: Exakte terminale Weiterleitung mit ihren Argumenten verlangen, statt beliebige Fehlerbehandlung zu akzeptieren.
- `tests/test_nginx_common_adoption.py`: Tatsächlichen privaten Header kopieren, beide veralteten Anker reparieren, Exitstatus 1 und genaue `FAIL:`-Zeile verlangen, alle 96 vorhandenen Tests erhalten und vier Regressionstests für Testkopie und Fehlerweiterleitung ergänzen.

Neue Regressionen prüfen byteidentisches Kopieren des Headers, fehlenden Header,
verbotene Makroänderung darin und Verwerfen des terminalen Rückgabewerts mit
anschließender Erfolgsrückgabe. Laufzeitcode, Workflows, Abhängigkeiten,
Compilerwarnungen, Scannerregeln und Sicherheitseinstellungen blieben unverändert.
Die zwischenzeitlich eingegangene identische Checker-Korrektur
`7bd3b2355c84bc6bd630de6b19ea6115b5eb64f2` blieb als Elterncommit der
Testkopie-Korrektur erhalten; kein Force-Push wurde verwendet.

[Lint-Lauf 35696836181, Job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958)
bestand den vollständigen Schritt
`python -m unittest -v tests.test_nginx_common_adoption` für die getestete
Revision. Native-/Event-, Request-Native-, Spätfehler-/Wiedereintritts-,
Phase-4-/Sicherheits-, Konfigurationsreferenz- und exakte Head-Sonar-Null-Schritte
bestanden ebenfalls. **Der Gesamtjob scheiterte später bei `Run lightweight lint`.**
Dessen Ursache ist durch das Mutationsergebnis nicht geklärt und bleibt ein
getrennter offener Punkt.

[NGINX-Lauf 35696836186, Job 106645456976](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836186/job/106645456976)
bestand Scaffold- und Common-Vertragsprüfungen, scheiterte danach jedoch an
seiner separaten nativen Syntax-/Regressionsprüfung. Eine Request-Body-Assertion
erwartet weiterhin `if (ret != 1)`; ihre Quelldatei wurde in diesem Schritt
nicht repariert. Keiner der fehlgeschlagenen Workflows wird als grün dargestellt.

[Sonar-Check 106645541548](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106645541548)
schloss für die exakte getestete SHA mit **0 neuen Issues, 0 akzeptierten Issues,
0 Security Hotspots und 0 Annotationen** erfolgreich ab. Die Coverage für neuen
Code bleibt 0.0%; eine Verbesserung gemessener Testabdeckung wird nicht behauptet.

Die zweisprachige Checkliste markiert V06b als abgeschlossen und dokumentiert
diese Ergebnisse. Gemeinsame Validierung V06, sämtliche erforderlichen Prüfungen
V07, verbleibende Implementierung, Erzeuger-/Ausgabe- und echte Host-/Profil-/
Transportkriterien bleiben offen. Lokale Projektbefehle wurden wegen des fehlenden
vorgeschriebenen RTK-Pfads nicht ausgeführt; die Nachweise stammen aus GitHub-CI.
Der reine Dokumentations-Nachfolgecommit benötigt eigene frische CI-/Sonar-
Prüfungen und darf die Ergebnisse dieser getesteten SHA nicht übernehmen. Kein
Merge, Master-Push, Deployment, Framework-/MRTS-Schreibzugriff oder Akzeptieren
von Issues wurde durchgeführt.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260921-pr382-native-results-events` |
| Datum (UTC) | `2026-09-21` |
| Basis-Revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| Aktuelle Fortsetzungsbasis | `83c5f88179f0f33be66c68913f4b0ce694cd19f2` |
| Getestete Implementierungsrevision | `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` |
| Branch | `fix/unified-native-results-events-20260921` |
| Pull Request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

Umfang: nur Parent-Repository. Der PR bleibt Draft; kein Merge oder Master-Push.
Frühere Fortsetzungsnachweise bleiben in Git-Historie und Checkliste erhalten.

## Motivation und Problemstellung

Null beim nativen Byte-Append kann konfiguriertes `ProcessPartial` bedeuten;
Phasenauswertung verlangt eins. Frühere PR-Commits ergänzten gemeinsame
Prädikate, typisierte Fehler und JSONL-/Hash-Normalisierung. Damit waren noch
nicht alle Connector-Routen und Prüfungen abgeschlossen.

Diese Fortsetzung behebt einen echten Metadatenfehler: `not_observable` wurde
als Nachweis einer Hostaktion behandelt. Sie repariert veraltete Apache-
Adoption-Erwartungen ohne Entfernung von Negativtests, erhält das HAProxy-
Verhalten bei reduzierter gemeldeter Komplexität und setzt die ausdrückliche
Nutzervorgabe null neuer Sonar-Befunde um. Die Gesamtmigration bleibt unfertig.

## Akzeptanzkriterien

Die [zweisprachige Checkliste](../../../docs/pr-382-checklist.de.md) trennt
implementierte, verifizierte und offene Punkte. Bekannte unbeobachtete Ereignisse
dürfen keine ausgeführten Aktionen behaupten; tatsächliche Nachweisfelder und
Anwendungsereignisse müssen die Normalisierung überstehen. Gemeinsame Prädikate
dürfen nicht auf fremde API-Konventionen angewendet werden. Apache-
Sicherheitsmutationen und HAProxy-Aufruf-/Bereinigungsreihenfolge müssen getestet
bleiben. Sonar muss null neue Issues und Hotspots für den exakten Head melden,
nicht nur ein grünes Quality Gate. Verbleibende Routen-, Host-, Logausgabe- und
End-Head-Anforderungen bleiben offen.

## Implementierungsentscheidung und Begründung

Bekannte Regelereignisse ohne Beobachtung verwenden nun
`MSCONN_EVENT_ENGINE_DECISION`, eine leere `actual_action` und eine neutrale
Meldung. Bekannte technische Fehler behalten Ursache und Fehlerstatus. NULL,
leer und `not_observable` bedeuten jeweils fehlende Beobachtung. Zeitstempel,
HTTP-Beobachtungen, Zähler, EOS und Transportflags werden nicht erfunden.
Echter JSONL- und Integritätscode verwenden nach ursprünglicher Eingabevalidierung
dieselbe idempotente Ansicht. Unbekannte Anwendungsereignisse behalten ihre Semantik.

Apache-Prüfungen betrachten jetzt gemeinsame Rückgabeprädikate, typisierten
Ereignisstatus und einen einzigen begrenzten kanonischen Writer. Veraltete
Assertions verlangen den entfernten handgeschriebenen JSON-Fallback nicht mehr.
Neue Mutationen erkennen invertierte Append-/Phasenbedingungen, fehlende
Serialisierungsfehler-Rückgaben und als Regelblockierung geloggte technische
Fehler. Eine spätere lineare Statuszuweisungsprüfung entfernt ein gemeldetes
Risiko des regulären Ausdrucks.

HAProxy lagert begrenzte Rule-ID-Dekodierung und abhängigkeitsgeordnete
Ressourcenbereinigung aus. Ein entfernter Commit-Diff bestätigte 36 hinzugefügte
und 22 entfernte Binding-Zeilen bei erhaltener Auswertungsreihenfolge. Neue
kompilierte Tests prüfen den echten ausgewählten Quellcode mit kontrollierten
API-Grenzen und dem echten Common-Rule-ID-Dekodierer.

Die Sonar-Prüfung liest ausschließlich GitHub Checks mit jobbezogenen
Leserechten. Sie verlangt exakte SHA und Anbieter, eine erfolgreich abgeschlossene
Analyse und explizit null Issues/Hotspots/Annotationen. Fehlende oder mehrdeutige
Nachweise schlagen fehl. Antworten, Polling und Diagnoseausgabe sind begrenzt;
Weiterleitungen werden zurückgewiesen. Scanner-Ausnahmen, akzeptierte Befunde
und unterdrückte Regeln werden nicht verwendet. Repository-Identität verhindert
Pfadtraversal und bleibt ASCII-beschränkt.

## Geänderte Dateien

Diese Fortsetzung ändert folgende Code- und Validierungsbereiche:

- `common/include/msconnector/event_protocol.h`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `ci/checks/common/check-sonar-zero.py`
- `ci/checks/connectors/apache/apache_common_adoption_base.py`
- `ci/checks/connectors/apache/check-apache-common-adoption.py`
- `tests/test_apache_common_adoption.py`
- `tests/test_event_transport_observation.py`
- `tests/test_sonar_zero_gate.py`
- `tests/test_haproxy_binding_refactor.py`
- `.github/workflows/lint.yml` und `.github/workflows/test-haproxy.yml`
- `docs/pr-382-checklist.md` und `docs/pr-382-checklist.de.md`
- `docs/pr-382-event-contract.md` und `docs/pr-382-event-contract.de.md`
- diesen Change Record und seine englische Begleitdatei.

Frühere Native-Result-, Common-Fehlerklassifizierer-, Apache-/NGINX- und
Serializer-/Hash-Änderungen bleiben im PR. Abhängigkeiten, erzeugte Konfiguration,
Framework, MRTS, Branchschutz und Scanner-Konfiguration wurden nicht geändert.

## Ausgeführte Befehle

GitHub-CI [Lauf 35634888258, Job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690)
schloss folgende Einzelschritte für die getestete Implementierungs-SHA erfolgreich ab:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
python ci/checks/common/check-sonar-zero.py
```

Der gesamte Lint-Job scheiterte am NGINX-Adoption-/Mutationsschritt. Bestandene
Einzelschritte werden nicht als grüner Gesamtworkflow dargestellt. Neue Testdateien
kompilieren mit `-std=c17 -Wall -Wextra -Werror`; sie prüfen echten ausgewählten
Common-/nativen Code mit kontrolliertem Umfeld, nicht sechs echte Hosts.

GitHub-CI [Lauf 35634888103, Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189)
bestand für dieselbe Implementierungs-SHA folgende Befehle:

```sh
python3 -m unittest -v tests.test_haproxy_binding_refactor
python3 tests/test_haproxy_libmodsecurity_compat.py
```

Alle acht Auswertungs-/Bereinigungs-/Rule-ID-Tests und die bestehende Compile-/
Link-Kompatibilitätsprüfung bestanden. Native API-Grenzen dieser Tests sind
kontrolliert; dies ist kein echtes HAProxy-HTTP-Ergebnis.

Apache-Adoption-Prüfungen und alle 16 Mutationstests bestanden für
`1709e1def4706f0124d56fc687b3faf1fd8e2946` in
[Lauf 35633647191, Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579).
Der Job scheiterte danach am NGINX-Checker. Die spätere lineare Apache-
Quellcodeprüfung benötigt ihre eigene vollständige Validierung; ein früherer
Erfolg wird nicht als Nachweis dafür verwendet.

[Sonar-Check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547)
schloss für `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` mit **0 neuen Issues,
0 akzeptierten Issues, 0 Security Hotspots und 0 Annotationen** ab. Er meldet
0.0% Duplikation und 0.0% Coverage für neuen Code. Letzteres wird nicht als
gemessene Testabdeckung ausgegeben. Jeder spätere Head benötigt eine neue Analyse.

## Security-Auswirkung

Engine-Fehler dürfen nicht zu Allow/Log-only, falscher Regelblockierung oder
falscher erfolgreicher Untersuchung werden. Fehlende Hostbeobachtungen dürfen
nicht als ausgeführte Durchsetzung erscheinen. Ursprüngliche Eingabevalidierung
und Query-Redaktion bleiben erhalten. Rohe Bodys, Zugangsdaten und uneingeschränkte
Umgebungswerte werden nicht in Ereignisnachweise aufgenommen.

Die neue Sonar-Prüfung besitzt nur jobbezogene `checks: read` und `contents: read`.
Zugangsdaten werden weder ausgegeben noch bei Weiterleitungen übertragen oder
in Nachweise geschrieben. Die Prüfung ist strenger als das vorhandene grüne
Quality Gate und ersetzt keine Code-, Mutations-, Sicherheits- oder
Host-Integrationstests.

## Runtime-Evidence

Eine vollständige Live-HTTP-/Transportmatrix für sechs Familien wurde nicht
ausgeführt. Common-Testfamiliennamen sind keine unabhängigen Hostläufe.
HAProxy-Quellfunktionstests und Compile-/Link-Kompatibilität belegen nur ihre
genannten Ebenen. Gehostete CI-Builds und Preflight-Artefakte allein beweisen
kein clientseitiges Verhalten. Nicht unterstützte Strict-Profile oder
Reset-/Abbruchfähigkeiten werden nicht hochgestuft.

## Bekannte Einschränkungen

NGINX-Request-/Dateipfade und späte technische Interventionsfehler bleiben offen.
Der NGINX-Chain-Checker und veraltete Mutationsfragmente schlagen weiterhin fehl.
Vollständiger Erzeuger-/Ausgabevergleich, doppelte terminale Datensätze,
I/O-Fehler, weitere Ereignisklassen und Gleichheit direkter/Companion-Routen
benötigen weitere Arbeit. Umfassende Connector-Anleitungen und abschließende
Kompatibilitäts-/Versionierungsprüfung sind unvollständig.

## Verbleibende Risiken

Gültige Teilübernahme beweist nicht die Untersuchung aller übergebenen Bytes.
Ein später Abbruch kann gesendete Daten nicht zurückholen. Normalisierung kann
keine Hostbeobachtung erzeugen; Erzeuger benötigen weiter konsistente Flags und
Statuswerte. Neue Ereigniskennung, leere tatsächliche Aktion und normalisierte
Integritätsansicht betreffen Auswerter; die
[Vertragsanleitung](../../../docs/pr-382-event-contract.de.md) beschreibt die
Migration, ohne historische Formatkompatibilität als geklärt darzustellen.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale native Builds, lokale Projekttests und lokales `git diff --check` wurden
wegen des fehlenden vorgeschriebenen Ausführungswrappers nicht ausgeführt.
Validiert wurde durch die tatsächlichen GitHub-CI-Ergebnisse oben. Vollständige
Host-/Transportfehlerinjektion für sechs Familien, gleiche Logfehlerbehandlung
und vollständig grüne End-Head-CI bleiben offen. Der abschließende Dokumentations-
commit benötigt eigene Zweisprachigkeits-/Link-/CI-/Sonar-Ergebnisse.

## Finaler Diff- und Review-Status

Gesamt: `partial`. Metadatenkorrektur, Apache-Validierungsänderungen und
HAProxy-Refactoring sind mit den genannten Tests committed; Sonar-null ist für
den exakten Implementierungshead bestätigt. Die NGINX-Validierungslücke und
verbleibende Implementierungs-/Laufzeitkriterien verhindern den Abschluss.
Checklisten und Vertragsanleitung sind zweisprachig. Der PR bleibt Draft.
Merge, direkter Master-Push, Deployment, Abhängigkeits-/Framework-/MRTS-Änderung,
Issue-Akzeptanz oder Scanner-Unterdrückung wurden nicht durchgeführt.
