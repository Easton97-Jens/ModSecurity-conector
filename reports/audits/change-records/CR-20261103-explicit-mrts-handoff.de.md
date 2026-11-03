# Change Record: CR-20261103-explicit-mrts-handoff

**Sprache:** [English](CR-20261103-explicit-mrts-handoff.md) | Deutsch

Expliziten geprüften Übergang des verschachtelten MRTS-Pins ermöglichen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261103-explicit-mrts-handoff |
| Datum (UTC) | 2026-11-03 |
| Basis-Revision | `0a7fae33cd9ccb09c11ca58ea6c13d206cfff478` |

## Motivation und Problemstellung

Der bisherige Synchronizer änderte die Framework-Auswahl und behielt den verschachtelten MRTS-Lock. Der Kandidatenprüfer wies einen Kandidaten mit abweichendem MRTS-Gitlink korrekt zurück. Die ausdrücklich freigegebene gemeinsame Integration benötigt daher einen geprüften Übergang statt einer manuellen Lockänderung.

## Akzeptanzkriterien

Eine ausdrückliche MRTS-Freigabe mit exakt 40 kleinen Hexadezimalzeichen zusammen mit der Framework-SHA verlangen. Vor Schreibzugriffen den alten Lock gegen das alte Framework-Gitobjekt und die freigegebene MRTS-Revision gegen das Kandidatenobjekt prüfen. Defaultverhalten, geschlossene Lockschlüssel, Toolchains, geschützte Brokeridentitäten und transaktionale Veröffentlichung erhalten.

## Implementierungsentscheidung und Begründung

Synchronizer --mrts-sha und Prüfer --expected-candidate-mrts-sha durch API, CLI und verify-primary führen. Der vorhandene unveränderliche Gitreader belegt beide Gitlinks. Die ausdrückliche Freigabe verlangt ein echtes Framework-Objektverzeichnis; ungültige, fehlende, widersprüchliche oder unehrliche Provenienz wird abgelehnt. Ohne Freigabe behält der Synchronizer den MRTS-Lock und der Kandidatenprüfer verlangt weiterhin diese Auswahl. Das Flag ist eine geprüfte Eingabe, keine Remote-Freigabeautorität.

## Geänderte Dateien

Parent ci/tools/sync-framework-component-versions.py und ci/tools/verify-framework-candidate-contract.py; docs/security/ci-security-tooling.md mit deutscher Begleitdatei; dieses Change-Record-Paar. Die vorhandenen Framework-Dateien test_update_framework_versions.py und test_verify_framework_candidate_contract.py erhalten gezielte Regressionen in ihrem separaten Repository.

## Ausgeführte Befehle

RTK-gekapseltes explizites Framework-CPython3.15.2 führte die unittest-Module modsecurity_connector_tests.test_update_framework_versions und modsecurity_connector_tests.test_verify_framework_candidate_contract aus: 79 Tests PASS in 158.096s. Der tatsächliche Kandidat 00de6d61122c85120c3a06e84e46906f87165744 / MRTS ee2174431c4edf97e66afe32558ce8454deb2397 bestand trockenes Rendering und den öffentlichen Prüfer; alle ursprünglichen primären Parentbytes blieben unverändert. Die Defaultablehnung blieb erhalten. Exakte Aufrufe, Ergebnisse und unveränderliche Fixtureprovenienz liegen im Integrationsverzeichnis parent-mrts-handoff. Ruff meldete dieselben 17 bestehenden Diagnosen über die vier Quellen, keine neuen gegenüber den exakten Parent-/Framework-Basen.

## Security-Auswirkung

Keine automatische MRTS-Übernahme und kein beliebiger Lockschreibzugriff. Fehlende Freigabe, ungültige Eingaben, Kandidatenkonflikte, unehrliche alte Locks, fehlende Objekte und Symlinkautorität besitzen No-write-Regressionen. Geschützte Identitäten und transaktionale Sperren bleiben erhalten. Drei bestehende Fixtureannahmen wurden anhand exakter Basisbytes korrigiert: ein geschlossener Inline-Caller-Registryeintrag, Keywordweitergabe bei erhaltener flock-Prüfung und eine durchgängig reale Caller-Git-SHA für Rendering und Veröffentlichungsprüfung.

## Runtime-Evidence

Keine Hosts gestartet. Dieser Quellvertragsnachweis ersetzt nicht die finalen integrierten Protokollläufe des Koordinators.

## Bekannte Einschränkungen

Der tatsächliche Kandidatennachweis verwendet einen Framework-Commit vor dem Merge, nicht die spätere Merge-SHA. Der Koordinator muss den tatsächlichen Framework-Merge und freigegebenen MRTS-Merge nativ binden sowie abhängige Inventare und Archive regenerieren.

## Verbleibende Risiken

Aktuelle Hosted-Checks, finale Pinübernahme, Metadatenregeneration und integrierte Laufzeitnachweise bleiben Lieferungsgates des Koordinators. Unabhängige Altbefunde bleiben separat.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Worker führte keine Vollsuite, lokale Sonarprüfung, Installations-/Anmeldereparatur, Publisher-/geschützte Broker-Ausführung, administrative Aktion, Commits oder Gitlieferung aus. Lokale Sonaraktionen bleiben auf Benutzeranweisung ausgesetzt.

## Finaler Diff- und Review-Status

Der begrenzte Quell-/Testdiff bestand alle 79 betroffenen Regressionen. Die unabhängige lesende Prüfung fand keinen materiellen Befund. Finale Metadaten und Hosted-Validierung des exakten Heads bleiben Aufgabe des Koordinators.
