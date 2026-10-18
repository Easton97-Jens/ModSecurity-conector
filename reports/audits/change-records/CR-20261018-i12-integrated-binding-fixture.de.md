# Change Record: CR-20261018-i12-integrated-binding-fixture

**Sprache:** [English](CR-20261018-i12-integrated-binding-fixture.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-integrated-binding-fixture |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `f9a5ed7112c1c8ab468892d813ac60891567dcab` |

## Motivation und Problemstellung

Das integrierte HAProxy-Binding liest jetzt request.http_version. In seiner synthetischen Evaluierungsfixture fehlte dieses Feld; sie scheiterte bereits vor dem ersten Test beim Kompilieren und blockierte damit auch die Checks des integrierten Traefik-PRs.

Auch der I09-Hostresult-Fixture fehlte ihre neu ausgelagerte Response-Abbruchabhängigkeit. Die Aufruferregression modelliert diese Transportabhängigkeit jetzt mit dem bestehenden Shutdown-Zähler; dieser Unit-Test behauptet keine Prüfung von HTX-Queue- oder Transportinternals.

## Akzeptanzkriterien

Das synthetische Request-Layout wiederherstellen und die HTTP-Version explizit initialisieren. Compilerwarnungen, Evaluierungsreihenfolge, sämtliche Fehlerpfadtests und Produktverhalten erhalten.

## Implementierungsentscheidung und Begründung

Nur den fehlenden const-char-Zeiger und den Fixturewert 1.1 ergänzen. Keine Produktverhaltensänderung oder neue HAProxy-Funktion.

## Geänderte Dateien

tests/test_haproxy_binding_refactor.py, tests/test_haproxy_host_native_results.py und dieses EN/DE-Nachweispaar.

## Ausgeführte Befehle

RTK-umhülltes unittest tests.test_haproxy_binding_refactor in der Parent-venv reproduzierte vor dem Fix den Compilerfehler des fehlenden Feldes (null Tests ausgeführt); danach bestanden alle acht Tests. Exakte Befehle, Exits und Loghashes bleiben als root-haproxy-fixture-before-20261018 und root-haproxy-fixture-after-20261018 im Abnahmelauf erhalten.

Der zweite Compilerfehler wurde separat reproduziert und als root-haproxy-host-fixture-before-20261018 erhalten. Die kombinierte Wiederholung beider Module bestand alle neun Tests; root-haproxy-fixtures-integrated-after-20261018 enthält ihren exakten Befehl und die Hashes. EN/DE-, Link- und Nachweisprüfungen bestanden separat.

## Security-Auswirkung

Die Fixture kompiliert wieder und prüft bestehende Cleanup-/Fehlerpfade des Bindings. Keine Sicherheitskontrolle, Warnung oder Prüfung wird entfernt.

## Runtime-Evidence

Diese synthetische Fixturereparatur behauptet keine Hostausführung oder Originalfallqualifikation.

## Bekannte Einschränkungen

Die Fixture bleibt ein Evaluierungsmodell auf Unit-Ebene; echte Host-Lifecycle-Belege bleiben separat erforderlich.

## Verbleibende Risiken

Abschließende gehostete Checks müssen auf dem danach integrierten veröffentlichten Head laufen.

## Nicht ausgeführte Prüfungen mit Begründung

Zum Nachweis dieses reinen Fixture-Kompilierfehlers war kein weiterer Hostlauf nötig. Gehostete CI und Sonar folgen der Veröffentlichung.

## Finaler Diff- und Review-Status

Die begrenzte Fixtureänderung aus zwei Zeilen wurde gegen das aktuelle Binding geprüft und bestand dessen acht Tests. Die Integration erhält veröffentlichte Historie.
