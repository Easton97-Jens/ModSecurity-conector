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

Echte Brücke kompilieren und ihre native Go-Suite einschließlich beider
Antwortbeginn-Regressionen ausführen. Fehlende native Voraussetzungen müssen
fehlschlagen statt übersprungen zu werden. Toolchain-Auswahl, Abhängigkeiten und
exakte Sonar-Nullprüfungen erhalten. Live-Envoy-Transportnachweise bleiben getrennt.

## Implementierungsentscheidung und Begründung

Den bestehenden Envoy-Job nach seinen Quellcodeprüfungen erweitern. Bereits
gepinnte setup-go-Action und Root-Go-Auswahl nutzen, geteilten Go-Cache abschalten
und nur build-essential sowie libmodsecurity-dev im kurzlebigen Runner installieren.
Das vorhandene build_ext_proc.sh direkt mit ENVOY_EXT_PROC_COMMON_TEST=1 aufrufen:
Seine geprüften Voraussetzungen können den optionalen Überspringpfad des anderen
Testskripts nicht nehmen. Der Builder kompiliert Common-Archiv und CGo-Dienst und
prüft alle Pakete mit libmodsecurity-Tag und count=1 bei unveränderbaren Modulen.
Dieser Teil ändert weder Hostfähigkeiten noch produktive Fehlerpolicy.

## Geänderte Dateien

Envoy-Workflow und dieser zweisprachige Bericht. Keine Connector-Quelldateien,
Framework-/MRTS-Dateien, Lockdateien, Scannerregeln oder Abhängigkeitsversionen.

## Ausgeführte Befehle

Der verpflichtende entfernte Schritt ruft auf:

```sh
sh connectors/envoy/build/build_ext_proc.sh
```

Mit ENVOY_EXT_PROC_COMMON_TEST=1, nativen Distributionsheadern/-bibliothek und
privaten temporären Build-/Cachepfaden des Runners. Bei Commitvorbereitung steht
die Ausführung aus; V20 erst nach Rücklesen der veröffentlichten Revision erfassen.
Der Nutzer hat klargestellt, dass RTK diesen entfernten Workflow nicht blockiert.

## Security-Auswirkung

contents:read und persist-credentials:false bleiben bestehen. Keine Credentials
in Testargumenten, kein pull_request_target, keine geteilten Build-Cache-Writes,
kein Deployment und keine dauerhafte Paketinstallation auf dem Nutzerrechner.
Fehlende native Voraussetzungen sowie Build-/Testfehler bleiben Fehler.

## Runtime-Evidence

Ein erfolgreicher nativer Lauf belegt echte Common-/libmodSecurity-/CGo-Ausführung,
keinen laufenden Envoy-Server, keine physische gRPC-Lieferung und nicht alle Routen.
Vorabprüfungsartefakte behalten ihre begrenzte Aussage und werden durch den
zusätzlichen Schritt nicht zu vollständigen Laufzeitnachweisen hochgestuft.

## Bekannte Einschränkungen

I09/I10 dürfen aus diesem Testjob einer einzelnen Route nicht insgesamt als
erledigt gelten. Andere Adapterlücken und I11/I12-Log-/Hostnachweise bleiben offen.
Die Distributionsbibliothek ersetzt keinen versionsgebundenen Freigabe-Hosttest.

## Verbleibende Risiken

Die erstmals verpflichtende native Suite kann bisher unausgeführte Fehler zeigen.
Diese ohne abgeschwächte Assertions oder Compilerwarnungen einordnen und beheben.
Sonar muss null neue Befunde und exakt null neue Duplikation bestätigen.

## Nicht ausgeführte Prüfungen mit Begründung

Kein vollständiger lokaler Checkout oder nativer Lauf: Die Sandbox kann GitHub
nicht auflösen. Stattdessen werden GitHub-Quelldatenzugriff und CI verwendet.
Keine Live-Hostmatrix behauptet. Neue Tests und Sonar müssen zur neuen Revision passen.

## Finaler Diff- und Review-Status

Nur im bestehenden Draft-PR fortsetzen. Parallele Apache-Änderungen erhalten;
kein Merge, Master-/Force-Push oder Deployment durch diese Änderung.
