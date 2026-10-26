# Change Record: CR-20261026-nginx-broker-ubuntu26-preparation

**Sprache:** [English](CR-20261026-nginx-broker-ubuntu26-preparation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261026-nginx-broker-ubuntu26-preparation |
| Datum (UTC) | 2026-10-26 |
| Basis-Revision | `7a44f18edac729291d6551d068da64fa3fec4e1e` |

## Motivation und Problemstellung

Die Umstellung des geschützten Aufrufers auf Ubuntu 26.04 benötigt einen geprüften vertrauenswürdigen Broker, der den vollständigen neuen Runner-Modus sowie den bestehenden alten Aufrufer akzeptiert.

## Akzeptanzkriterien

Alle drei unprivilegierten Jobs gemeinsam auf ubuntu-latest oder gemeinsam auf ubuntu-26.04 akzeptieren. Gemischte, unbekannte, Listen- und self-hosted-Werte ablehnen. Unveränderliche Pins und alle weiteren Prüfungen erhalten. Den Broker auf ubuntu-26.04 ausführen.

## Implementierungsentscheidung und Begründung

Vor den einzelnen Jobprüfungen einen gemeinsamen Runner-Modus des vollständigen Aufrufers prüfen. Exakte ergänzende Hosted-Labels ermöglichen älteren actionlint-Versionen die Erkennung von Ubuntu 26.04. Aufruferquelle und unveränderliche Revisions-Pins bleiben gleich.

## Geänderte Dateien

`.github/workflows/nginx-root-broker.yml`, `.github/actionlint.yaml`, `ci/runtime/broker/nginx_root_broker.py`, `tests/test_nginx_root_broker.py`, `sonar-project.properties` und dieser zweisprachige Change Record.

Der erste veröffentlichte Head `89e3342c112ad9c23821413243dd7586432528c6` erreichte die Sonar-Serververarbeitung ohne offene Befunde. Security, Reliability, Maintainability, Duplikation und geprüfte Hotspots bestanden; ausschließlich Coverage scheiterte mit 0% an 80%. Der Folgecommit übernimmt die bestehende Coverage-Abwahl des Nutzers über `sonar.coverage.exclusions=**`, wie bereits in #382. Quellumfang, Sicherheitsregeln, bestehendes Gate und terminales Gate-Warten bleiben erhalten. Frische CI- und Serverergebnisse des Folge-Heads sind erforderlich.

## Ausgeführte Befehle

Quellprüfung und native Change-Record-Vorlagenerzeugung über RTK; Python ast.parse für beide geänderten Python-Dateien erfolgreich; `/root/go/bin/actionlint -color .github/workflows/nginx-root-broker.yml` erfolgreich. Root ließ den eingefrorenen externen Deskriptor und die Quell-Hashes vor Import oder Ausführung zu. Der geschützte Lauf bestand alle sieben ausgewählten Methoden: 36 expandierte Fälle, 33 beobachtete Subtests, keine Skips, Fehler oder Fehlschläge. Sein Audit-Hook weist Prozess- und Netzwerkaufrufe ab. Der externe Beleg ist `runs/parent-ubuntu26-20261026/broker-preparation-result.json`. Der erste eigene Harness konnte wegen eines fehlenden Namespace-Package-Attributs alle sieben Selektoren nicht laden; der korrigierte Harness bestand. Der erste Fehler bleibt als Harness-Nachweis erhalten und ist kein Produktregressionsnachweis.

## Security-Auswirkung

Die akzeptierten Runner-Werte werden um exakt ein Hosted-Label erweitert, ausschließlich im einheitlichen Modus. Berechtigungs-, Gate-, Inventar-, Quell-, Artefakt- und unveränderliche Revisionsprüfungen bleiben erhalten. Keine Änderungen an Privilegien oder Vertrauensankern.

## Runtime-Evidence

Keine. Kein Broker-Dispatch, Dienst, Host-, Matrix-, Oracle- oder I12-Lauf gestartet.

## Bekannte Einschränkungen

Diese Vorbereitung migriert den Aufrufer nicht und aktualisiert seinen Broker-Pin nicht. Die getrennte Aufrufermigration benötigt eine geprüfte Broker-Revision nach genehmigter Master-Integration.

## Verbleibende Risiken

Das Laufzeitverhalten auf Hosted Ubuntu 26.04 ist noch nicht gemessen. Das gezielte Offline-Kompatibilitätsergebnis belegt keine geschützte Broker-Ausführung oder einen Hosted-Build.

## Nicht ausgeführte Prüfungen mit Begründung

Diese Basis enthält kein kanonisches Inventar aktiver Fälle; der extern zugelassene Deskriptor band die ausgeführte Auswahl. Hosted-Ausführung und Laufzeitkampagnen wurden nicht gestartet und bleiben außerhalb dieser Vorbereitung.

## Finaler Diff- und Review-Status

Der begrenzte Patch wurde in Draft-PR #422 veröffentlicht. Statische Python-Syntaxprüfung, actionlint und die zugelassene Offline-Auswahl erfolgreich. Die unabhängige statische Quellprüfung fand keinen konkreten Bypass. Der Nutzer autorisierte ausschließlich den Merge von #422 nach grünen Pflichtprüfungen und abschließendem Review sowie anschließend die Aktualisierung des geprüften Broker-Pins in #382. Diese Freigabe umfasst keinen Merge von #382 oder Framework #138. Noch kein Merge erfolgt; der Coverage-Folgecommit benötigt weiterhin die Verifikation seines exakten Heads.
