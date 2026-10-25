# Sonar-Quellrollen

**Sprache:** [English](sonar-source-roles.md) | Deutsch

Der versionierte [Quellrollenvertrag](../config/testing/sonar-source-roles.json)
ist die maßgebliche Quelle für <code>sonar.test.inclusions</code> in der
[Automatic-Analysis-Konfiguration](../.sonarcloud.properties) und der
[CI-Scanner-Konfiguration](../sonar-project.properties). Er klassifiziert Quellcode;
er wählt keine Verhaltensfälle aus und führt keine aus. Das separate Aktivinventar
bleibt für die automatische Testausführung maßgeblich.

## Geprüfter Umfang

Der Vertrag erhält vier Standard-Testmuster, die drei bestehenden exakten
nativen C-Testdateien und die bestehende Fixture
<code>fuzz/common_http_headers_fuzz.c</code>. Zusätzlich bezeichnet er
45 einzeln geprüfte Fixture-Dateien. Für jede zusätzliche Datei enthält der
Vertrag den exakten Pfad, die Rolle TEST, den Zweck, die Quelle als
Nachweis und einen tatsächlichen Aufrufer oder Testverbraucher. Die Nachweise
enthalten exakte versionierte Zeilenanker; ein geänderter Anker lässt die
Umfangsprüfung scheitern und erfordert eine Quellprüfung.

| Zuständige Gruppe | Zusätzliche exakte Dateien | Geprüfter Zweck |
| --- | --- | --- |
| <code>common-http-authorization</code> | 1 | Regressionsfixture mit Stub-Runtime; tatsächliches <code>common/runtime/http_authorization_service.c</code> bleibt MAIN und wird getrennt gemessen. |
| <code>nginx-i12</code> | 4 | Versiegelter Fixture-Runner, Szenarioeingaben, begrenzter Wire-Client und expliziter Invalid-Return-Preload. |
| <code>apache-i12</code> | 14 | Private Fixture-Launcher/Clients/Backends, Fallmaterialisierung, Cancellation-/Keepalive-Operationen und reine Sink-/Host-/Multipart-Testbeobachter. |
| <code>traefik-native-i12</code> | 6 | Acceptance-Backend/Client/Driver, Fehlerrelays für ausgewählte Operationen und Syscall-Beobachter des eigenen Kindes. |
| <code>traefik-forwardauth-i12</code> | 7 | Synthetische physische Acceptance-Endpunkte, Client/Driver, expliziter Fehlerpeer, Autorisierungsrelay und private Fixture-CA. |
| <code>haproxy-i12</code> | 4 | Eingefrorene SPOP-Fixtures, private SPOP-/Companion-Captures und Materialisierung unveränderlicher nativer HTX-Fixtures. |
| <code>lighttpd-i12</code> | 7 | Begrenzte private Wire-Clients und explizite Spool-Floor-/Socket-Beobachtungsfixtures sowie der reine SDK-MIME-Testaccessor. |
| <code>native-observer</code> | 2 | Der optionale SDK-Accessor und der explizite GNU-Link-Wrap-Beobachter ausschließlich für Testartefakte. |

Dies ist eine Korrektur exakter Dateien. Es gibt keine pauschale Klassifikation
von <code>ci/**</code> oder Connector-Harness-Verzeichnissen. Gemischte operative
Werkzeuge, Vorbereitungs-/Provenienz-Builder und
<code>connectors/haproxy/harness/i12_spop_wire.py</code> behalten ihre
Produktionsrolle. Der genehmigte Materialisierer nativer HTX-Fixtures ist einzeln
aufgeführt, weil er ausschließlich unveränderliche Falleingaben vorbereitet.
Echter Produktquellcode bleibt MAIN, einschließlich
<code>common/src/headers.c</code>, <code>common/src/test_result.c</code> und
<code>common/scripts/modsecurity_targeted_eval.cc</code>.

## Synchronisierung und Berichtsklassifikation

Der [Generator](../ci/tools/sync-sonar-test-scope.py) besitzt ausschließlich die
einzelne Zeile <code>sonar.test.inclusions</code> in jeder Properties-Datei. Alle
anderen Projekt-, Quell-, Sprachversions-, Gate- und Baseline-Einstellungen
bleiben erhalten. Die nativen Befehle laufen durch einen gegebenenfalls von der
lokalen Arbeitsvereinbarung vorgeschriebenen Ausführungsproxy:

~~~sh
python3 ci/tools/sync-sonar-test-scope.py --write
python3 ci/tools/sync-sonar-test-scope.py --check
~~~

Der [Klassifikationshelper](../ci/lib/sonar_source_roles.py) liest denselben
Vertrag und stellt <code>is_test_source(relativepath)</code> bereit. Er lehnt
absolute, nichtkanonische, traversierende und symlinkbehaftete Eingaben ab.
Batch-Verbraucher können <code>SourceRoles</code> einmal laden und den geprüften
Vertrag an den Helper übergeben. Coverage-Produzenten nutzen dieselben Rollen,
statt Fixture-Treffer als Produktionsabdeckung zu behandeln. Eine Rollenprüfung
ist eine statische Quellprüfung, kein Testlauf und kein Coverage-Import.

## Nachweisgrenzen

Die historischen I12-Ergebnisse behalten ihre ursprünglichen Quell-/Laufidentitäten.
Die Auflistung dieser Fixtures eröffnet keine historische Kampagne, fügt keine
aktiven Fälle hinzu, behauptet kein <code>I12_COMPLETE</code> und belegt kein
Hostverhalten am aktuellen Head. TEST-Dateien bleiben als Tests analysiert; es
wird kein Produktionsausschluss eingeführt.

Die bestehende Sonar-Coverage-Anforderung bleibt
<code>new_coverage &gt;= 80</code>. Eine korrekte Klassifikation belegt weder, dass
diese Schwelle erreichbar ist, noch dass sie erfüllt wird. Tatsächliche
Berichtserzeugung, erfolgreicher Scanner-Import und revisionsgebundene Gesamt-/
New-Code-Messwerte benötigen eigene Ausführungs- und Servernachweise.
