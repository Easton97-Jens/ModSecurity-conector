# Change Record: CR-20261114-preparation-master-integration

**Sprache:** [English](CR-20261114-preparation-master-integration.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261114-preparation-master-integration |
| Datum (UTC) | 2026-11-14 |
| Basis-Revision | `34a924ec602826e87f74e8fb986486d5fced7e8b` |

## Motivation und Problemstellung

Parent #445 ohne Warten auf einen anderen PR integrieren. Master enthält den extern integrierten #448 bereits als `d420a12c4155a4bc2b9ea63ee5cef633085705e7`. Der reguläre Abgleichscommit lautet `34a924ec602826e87f74e8fb986486d5fced7e8b`; doppelte private C/Go-Vorschläge wurden nicht angewandt. Framework #169 ist tatsächlich als `452f7fc7ca1d9c44c9e768cef565f52882a40e2d` integriert und besitzt denselben geprüften Kandidatenbaum.

## Akzeptanzkriterien

Die endgültige eingecheckte Kette muss Framework `452f7fc7ca1d9c44c9e768cef565f52882a40e2d` und MRTS `9a855b092645733ea8ff73a512aff7bfe916407e` auswählen; Versionslock und alle22 Workflow-Projektionen müssen übereinstimmen. Der separate Pin benötigt passende vollständige Quellnachweise und reguläre Zulassung des exakten Index. Erforderliche CI/Reviews/Gates am aktuellen Head,92 Host-Ausführungen,195 Go-Szenarien samt `go vet`, frische Apache2.4.71-Artefaktzulassung/Build/CRS und ein echtes Fünfer-Aggregate müssen vor der Parent-Integration geprüft sein.

## Implementierungsentscheidung und Begründung

Beide Eltern durch einen regulären Merge erhalten. Reine SHA-Konflikte auf den kohärenten f13/M9a-Stand des ersten Elterncommits auflösen und den tatsächlichen Framework-Master anschließend separat nativ pinnen. Upstream-Sättigung der Response-Zähler und native Fehlerklassifikation zusammen mit dem Late-Action-Verhalten dieses PRs erhalten. Die Common-Runtime-Sperre für `strict_post_commit_action=0` bleibt; das ausgewählte Envoy-Profil deklariert `strict_post_commit_action=1`. Ein erfolgreiches `strict_immediate_response_sent` dokumentiert einen Sendevorgang, keinen Downstream-Reset. Die Toleranz optionaler später Safe-Ereignisse umfasst keine nativen Rejects, technischen oder Auditfehler.

## Geänderte Dateien

Der Abgleich ändert61 reguläre Pfade gegenüber seinem ersten Elterncommit und lässt die24 Pinpfade unverändert. Vier aufgelöste Dokumentationsdateien sind die EN/DE-Paare unter `connectors/envoy/ext_proc/` und `connectors/traefik/native_middleware/`. Vorhandene Upstream-Common-/Connector-Quellen und Change Records bleiben erhalten. Dieses Record-Paar dokumentiert den Abgleich sowie die separate beabsichtigte Änderung von `modules/ModSecurity-test-Framework`, `ci/tooling/project-versions.lock.json` und22 Workflow-Projektionen.

## Ausgeführte Befehle

Reguläres `git fetch origin master`, `git merge --no-commit --no-ff origin/master`, gezieltes Staging der Konfliktauflösung, `git diff --cached --check` und ein normaler Commit mit aktivem Hook waren erfolgreich. Die Merge-Eltern sind `5bab6e9da4ea63a4e53c432d3c433ff9f6d00072` und `d420a12c4155a4bc2b9ea63ee5cef633085705e7`; sein Baum lautet `7b83d86c6685ad8e6b5bec02bdb0251d847e4a57`. Die native Vorlagenerstellung mit `python3 ci/tools/new-change-record.py create --name preparation-master-integration --base-revision 34a924ec602826e87f74e8fb986486d5fced7e8b --date 2026-11-14` war erfolgreich. Exakte Secrets-Prüfungen regulärer Dateien waren erfolgreich; unvollständige automatische Apply-Hooks wurden separat aufgearbeitet und gelten nicht als automatisch bestanden.

## Security-Auswirkung

Keine Autorisierung, Isolation, Quellzulassung, Fehlerbehandlung, Prüfung, CI-Anforderung oder Quality Gate wird abgeschwächt. Verpflichtendes Audit/Cleanup erhalten und optionale späte Safe-Ereignisse von nativen/technischen Fehlern unterscheiden. Es erfolgt keine pauschale False-Positive-Entscheidung. Das neue unveränderliche Framework-Ziel benötigt eine separat passende reguläre Zulassung; ein Beleg für ein früheres Ziel ist keine Freigabe des neuen Commits.

## Runtime-Evidence

Bei Erstellung dieses Records wird keine neue Host- oder Go-Ausführung am endgültigen Paar behauptet. Der vollständige Framework-Master-Quellnachweis erhält2622 Pfade und57 authentische Belege des geprüften identischen Baums; er belegt ausschließlich die Quell-/Secrets-Ebene. Kandidaten-CI oder ein Secrets-Erfolg belegen weder Host-Reset-/Abbruchverhalten noch ersetzen sie die Prüfungen des endgültigen Paars.

## Bekannte Einschränkungen

Die Framework-Master-Sonar-Analyse wird abgeschlossen, ihr Gate scheitert jedoch an der Sicherheitsbewertung. Bereits der vorherige Master `939d1718b7548a36ff7a550080ed8b811aad8a98` meldete dieselbe E-Sicherheitsbedingung. Die115 offenen Master-Befunde werden einzeln gegen Ausgangsstand und Umfang verglichen. Damit werden weder ein grünes Master-Gate noch alle Befunde als falsch behauptet. Nach dem endgültigen Pin-Commit bleiben frische Parent-Ergebnisse erforderlich.

## Verbleibende Risiken

Strict-Host-/Wire-Ergebnisse benötigen unabhängige Nachweise für Target, Peer und Folgezugriff. Native ABI-Verbraucher gegen passende Common-Header und das erforderliche ModSecurity3.0.17-SDK neu bauen. Alte SDK3.0.14-Diagnosen und HTTPD2.4.70-Vorbereitungsfehler qualifizieren das endgültige Paar nicht. Alle100 Standardfälle und80 Selektoren erhalten.

## Nicht ausgeführte Prüfungen mit Begründung

Der separate endgültige Pin samt Zulassung, CI/Sonar am eingecheckten Paar,92 Hosts,195 Go-Szenarien samt `go vet`, frische Apache2.4.71-Zulassung/Build/CRS und echtes Fünfer-Aggregate wurden bei Record-Erstellung noch nicht ausgeführt; ihre endgültige unveränderliche Eingabe ist noch nicht committed. Die umfassende Abnahme bleibt ein anschließender Schritt. Keine nicht ausgeführte Prüfung wird als bestanden gemeldet.

## Finaler Diff- und Review-Status

Ein unabhängiger begrenzter statischer Review der vier automatisch zusammengeführten Produktdateien fand keinen zusätzlichen belegten Mergefehler. Die EN/DE-Konfliktauflösungen folgen tatsächlichem Profil- und Safe-Ereignisverhalten. Der Abgleichscommit ist bei Record-Erstellung lokal, sauber und ungepusht; Parent #445 ist nicht integriert. Der Pin bleibt eine separate begrenzte Änderung, damit sein normaler Hook die exakte Veröffentlichung prüfen kann. Abschließender Review und Delivery-Nachweise am aktuellen Head bleiben erforderlich.
