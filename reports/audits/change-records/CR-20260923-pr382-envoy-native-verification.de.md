# Change Record: Verpflichtende native Envoy-Brückenprüfung

**Sprache:** [English](CR-20260923-pr382-envoy-native-verification.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260923-pr382-envoy-native-verification` |
| Datum (UTC) | `2026-09-23` |
| Basis-Revision | `ee33afc5bbb961f2d0d612c5ff591eb073fd02ce` |
| Umfang | Parent-PR #382; I09/I10-Verifikation und V20 |

## Motivation und Problemstellung

Die eingecheckten Antwortbeginn-Tests verwenden das libmodsecurity-Buildtag.
Der bisherige Envoy-Workflow prüfte Quellcodeverträge und Hostvoraussetzungen,
nicht diese nativen Tests. Ein grüner Job belegte daher nicht die Fehlerweitergabe
vom Go-Empfänger über die geprüfte C-ABI zur echten Common-Zustandsmaschine.

## Akzeptanzkriterien

Echte Brücke und native Go-Suite einschließlich beider Antwortbeginn-Regressionen
prüfen. Fehlende Voraussetzungen müssen fehlschlagen statt übersprungen zu werden.
Toolchain-Auswahl, geprüfte Engine-Herkunft, Abhängigkeiten und exakte Sonar-
Nullprüfungen erhalten. Live-Transportnachweise bleiben getrennt.

## Implementierungsentscheidung und Begründung

Den bestehenden Envoy-Job nach seinen Quellcodeprüfungen erweitern. Gepinnte
setup-go-Action und Root-Go-Auswahl ohne geteilten Go-Cache nutzen. Der erste
Versuch bei `6092c1b0` verwendete das ältere native Distributionspaket 3.0.12;
der echte strikte Build wies dessen inkompatible C-API zurück. Dies war eine
falsche Auswahl der Testumgebung, kein bestandener nativer Regressionstest.

Die Korrektur verwendet das vorhandene with-runtime-components.sh mit Target
shared. Framework-eigene Engine-Provenienz, private Cacheprüfung und aufrufgebundene
Umgebung bleiben maßgeblich. Buildvoraussetzungen nur im kurzlebigen Runner
installieren; kein Rückfall zur Distributionsengine, keine API-Nachbildung,
Const-Casts oder abgeschalteten Warnungen. Der unveränderte native Builder
kompiliert mit ENVOY_EXT_PROC_COMMON_TEST=1 Common-Archiv und CGo-Dienst und
prüft alle nativen Pakete mit count=1. Der zusätzliche ShellCheck-Befund zur
kombinierten Deklaration/Zuweisung entfällt mit der falschen festen Bibliotheksauswahl.

## Geänderte Dateien

Envoy-Workflow und dieser zweisprachige Bericht. Keine Connector-Quelldateien,
Framework-/MRTS-Dateien, Lockdateien, Scannerregeln oder Abhängigkeitsversionen.

## Ausgeführte Befehle

Verpflichtender entfernter Befehl mit ENVOY_EXT_PROC_COMMON_TEST=1:

```sh
sh ci/provisioning/cache/with-runtime-components.sh sh connectors/envoy/build/build_ext_proc.sh
```

Bei `6092c1b0` erreichte Job 107129310702 (Lauf 35845121593) echte Kompilierung
und scheiterte vor den Go-Tests an der alten API. Actionlint meldete zusätzlich
SC2155. Keines der Ergebnisse gilt als bestanden. Nach der korrigierten
Bereitstellung sind frische Nachweise erforderlich. RTK regelt diesen entfernten
Connector-/CI-Ausführungsweg nicht.

## Security-Auswirkung

contents:read, persist-credentials:false und gepinnte Actions bleiben erhalten.
Bereitstellung nutzt geprüfte Quellen und Cacheprüfungen in privaten Runnerpfaden.
Keine Credentials in Testargumenten, kein pull_request_target, keine Scanner-
Unterdrückung, geteilte Cacheveröffentlichung, Deployment oder dauerhafte Installation
auf dem Nutzerrechner. Fehlende Voraussetzungen und Build-/Testfehler bleiben Fehler.

## Runtime-Evidence

Ein erfolgreicher nativer Lauf belegt tatsächliche Common-/libModSecurity-/CGo-
Ausführung, keinen Envoy-Server, keine physische gRPC-Lieferung oder alle Routen.
Vorabprüfungsartefakte behalten ihre begrenzte Aussage und werden nicht hochgestuft.
Kompilierung allein erfüllt V20 nicht.

## Bekannte Einschränkungen

I09/I10 dürfen aus diesem Testjob einer Route nicht insgesamt als erledigt gelten.
Andere Adapterlücken und I11/I12-Log-/Hostnachweise bleiben offen. Der ursprüngliche
3.0.12-Fehler bleibt dokumentiert statt durch Überspringen verborgen zu werden.

## Verbleibende Risiken

Die erstmals verpflichtende native Suite kann bisher unausgeführte Fehler zeigen.
Ursachen ohne schwächere Assertions oder Compilerwarnungen beheben. Sonar muss
null neue Befunde und exakt null neue doppelte Zeilen und Blöcke bestätigen.

## Nicht ausgeführte Prüfungen mit Begründung

Kein vollständiger lokaler Checkout oder nativer Lauf: Die Sandbox kann GitHub
nicht auflösen. Stattdessen GitHub-Quelldatenzugriff und CI verwenden. Keine
Live-Hostmatrix behauptet. Neue Tests und Sonar müssen zur neuen Revision passen.

## Finaler Diff- und Review-Status

Nur im bestehenden Draft-PR fortsetzen. Parallele Apache-Änderungen erhalten;
kein Merge, Master-/Force-Push oder Deployment in diesem Änderungsschritt.
