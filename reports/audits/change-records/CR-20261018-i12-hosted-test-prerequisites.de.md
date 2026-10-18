# Change Record: CR-20261018-i12-hosted-test-prerequisites

**Sprache:** [English](CR-20261018-i12-hosted-test-prerequisites.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-hosted-test-prerequisites |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `57ba18ce45f56b0febc5396f3753407e9d23e213` |


## Motivation und Problemstellung

Der Hosted-Scaffold-Job für a29019558678222b88913be0e202db3c9d14323a scheiterte vor den beabsichtigten Prüfungen: Sonar-Unittests importieren yaml vor der PyYAML-Installation; Capture-Fixtures rufen ein auf dem Hosted-Runner nicht deklariertes rtk-Programm auf. Die vorhandene Abhängigkeit muss vor ihren Verbrauchern installiert und testinternes Git vom Workstation-Werkzeug entkoppelt werden.

## Akzeptanzkriterien

Vorhandene requirements-ci.lock ohne Versions- oder Hashänderungen verwenden. Binär-Wheels mit verpflichtender Hashprüfung vor Sonar-Unittests installieren. Sämtliche Gate-/Security-Assertions erhalten. Vollständige Capture-Tests mit PATH ohne RTK ausführen und Vorher-/Nachher-Receipts erhalten. Den ersten fehlerhaften YAML-Versuch historisch behalten.

## Implementierungsentscheidung und Begründung

Der Scaffold-Workflow installiert das vorhandene PyYAML-6.0.3-Wheel für CPython 3.14 mit --only-binary=:all: und --require-hashes unmittelbar nach der Interpreter-Vertragsprüfung. Eine Regression verlangt genau einen unbedingten Lock-Installationsschritt vor dem Sonar-Testverbraucher. Vier testinterne lesende Git-Aufrufe für Revision, Tree, Archiv und Listing verwenden direkt das durch Checkout verfügbare Git. Lokale äußere Befehle bleiben RTK-gekapselt. Keine Gate-Implementierung oder Abhängigkeitspins werden geändert.

## Geänderte Dateien

Root verantwortet .github/workflows/lint.yml, tests/test_sonar_zero_gate.py und ci/runtime/lifecycle/i12/test_capture_sources.py. Diese Doku-Aufgabe ändert ausschließlich das EN/DE-Paar. Separat lesend geprüft wurde 37bb49612fbecbd3cdf18fba986757d39f6d7915: Die HAProxy-Binding-Fixture erhält das reale Request-Feld http_version samt Initialisierung; die Host-Result-Fixture ergänzt ihren Transport-Abbruch-Kollaborator über den bestehenden Shutdown-Zähler. Die separat dokumentierten Fixture-Änderungen ersetzen keine reale Transportabdeckung.

## Ausgeführte Befehle

Reale Diffs und externe Receipts wurden über RTK gelesen. Das Paar wurde mit dem nativen new-change-record.py create und der angegebenen Basisrevision erzeugt; dessen check bestand. Frische tests.test_bilingual_docs und tests.test_change_record bestanden 42 Tests in 0,430 Sekunden; git diff --check bestand. root-scaffold-dependency-order-before-20261018 enthält einen erwarteten Regressionstestfehler vor Ergänzung des Installationsschritts. root-capture-hosted-path-before-20261018 enthält FileNotFoundError für rtk im Setup bei null ausgeführten Tests. root-capture-hosted-path-after-20261018 führt die gesamte Capture-Suite über äußeres RTK mit PATH=/usr/bin:/bin aus: 57 Tests PASS in 38,670 Sekunden. root-scaffold-gates-security-retake-20261018 führt Sonar-Zero-, Duplication- und Workflow-Security-Module aus: 73 Tests PASS in 2,606 Sekunden. Exakte argv, Exitcodes und Loghashes liegen in den zugehörigen JSON-Receipts im externen Task-Verzeichnis checks.

## Security-Auswirkung

Vorhandener Lock-Digest sowie Binärpflicht und verpflichtende Hashprüfung bleiben erhalten. Diese Doku-/Reviewaufgabe installierte keine Pakete. Lesende testinterne Git-Aufrufe entfernen eine nicht deklarierte Hosted-Abhängigkeit; lokale RTK-Regeln bleiben erhalten. Keine Abschwächung oder Änderung von Gates, Validierung, Authentifizierung, Branchschutz, CI-Assertions oder Sonar-Zustand.

## Runtime-Evidence

Der Retake mit begrenztem PATH belegt alle 57 Capture-Tests ohne installiertes RTK im Kindprozess-PATH. Der 73-Test-Retake belegt gültiges Workflow-YAML und erhaltene Gate-/Security-Kontrollen. Das sind lokale Test- und Workflow-Vertragsbelege, kein Nachweis eines neuen Hosted-PASS oder Connector-Host-Lifecycles.

## Bekannte Einschränkungen

Der erste Versuch root-scaffold-gates-security-after-20261018 scheiterte an einem unquotierten YAML-Skalar mit --only-binary=:all:: 73 Tests, ein Fehler und zwei Exceptions. Dieser Beleg bleibt unverändert erhalten. Der endgültige Workflow verwendet einen Blockskalar; ausschließlich der separat benannte Retake ist PASS. Die lokale Reihenfolgenprüfung führt pip nicht aus und belegt keine Downloadverfügbarkeit.

## Verbleibende Risiken

Ein frischer Hosted-Lauf auf dem integrierten Head muss Installation, vollständigen Scaffold-Job und exakte Sonar-Headbindung prüfen. Der Requirements-Lock bleibt bytegleich; lokale Tests belegen weder Netzwerkverfügbarkeit noch Hosted-Erfolg.

## Nicht ausgeführte Prüfungen mit Begründung

Diese Aufgabe installiert keine Pakete, wiederholt keine schweren Hosts, verändert weder Git noch Sonar und editiert keinen CI-Code. Root verantwortet Implementierungstests und Integration. Diese Aufgabe liest Rohbelege unabhängig und prüft Dokumentationsvertrag sowie Whitespace. Go/Race/Vet und native Hostbelege gehören zur übergeordneten Abnahme.

## Finaler Diff- und Review-Status

Die lesende Prüfung fand keinen konkreten Fehler in den drei aktuellen CI-Änderungen oder den beiden HAProxy-Fixture-Änderungen aus 37bb4961. Die neue Reihenfolgenregression scheitert vorher und besteht im erhaltenen Retake. Dieses EN/DE-Paar dokumentiert die reale Fehlerhistorie und trennt lokale Ergebnisse von ausstehender Hosted-Verifikation.
