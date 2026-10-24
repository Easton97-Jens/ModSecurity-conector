# Change Record: CR-20261018-traefik-own-scope-ledger

**Sprache:** [English](CR-20261018-traefik-own-scope-ledger.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-traefik-own-scope-ledger |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `782f31ed78353b59a0dcd63978638ae5b107f8cf` |

## Motivation und Problemstellung

Gültige Konfigurations- und Preallocation-Pakete wurden zentral akzeptiert, vom Traefik-Consumer jedoch als unvollständige HTTP-Lifecycles abgelehnt.

## Akzeptanzkriterien

Die bestehenden zentralen Validatoren verwenden. Inventur und Lifecycle-Zähler bewahren; fehlende Producer und Scope-Ersetzung ablehnen.

## Implementierungsentscheidung und Begründung

Originalverträge mit `actual_configtest` verwenden `reviewed_configuration_packet`; explizite `host_preallocation_control`-Pakete verwenden `reviewed_preallocation_packet` mit exakter ID-Beschränkung. Andere Pakete behalten den Validator für 35 Felder. `fresh_configuration`, `fresh_preallocation` und `fresh_lifecycle` werden getrennt gespeichert. PASS/FAIL-Zähler je Scope sowie `case_qualified_pass`, `case_qualified_fail`, `case_unqualified_ids` kommen hinzu. Lifecycle-Zähler behalten ihre Bedeutung. Historische Konfigurationsergebnisse werden nicht als aktuelle Qualifikation übernommen.

## Geänderte Dateien

`connectors/traefik/harness/i12_ledger.py`, `tests/test_traefik_i12_ledger.py` und dieses EN/DE-Paar. Keine Änderungen an gemeinsamen Generatoren, Produktionsquellen oder eingefrorener Inventur.

## Ausgeführte Befehle

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_traefik_i12_ledger tests.test_i12_lifecycle_ledger tests.test_i12_traefik_preallocation`: 70 Tests bestanden. Der vorherige Reproducer mit fünf Kontrollen scheiterte zweimal an gültigen Paketen mit eigenem Scope.

## Security-Auswirkung

Ausschließlich funktionale Korrektur des Evidence-Consumers. Unabhängige Parser-/Quell-/Prozessbelege und exakte Preallocation-ID-Beschränkungen bleiben verpflichtend. Kein Sicherheitsscan, keine Capability-Ausnahme, keine Abschwächung.

## Runtime-Evidence

Keine Hostausführung. Synthetische Producer-Kontrollen belegen Consumer-Verhalten und qualifizieren keine tatsächlichen Original-IDs.

## Bekannte Einschränkungen

Der Preallocation-Test verwendet den eingefrorenen Originalvertrag und ein synthetisch geprüftes effektives Oracle an der Consumer-API. Er genehmigt oder löst kein echtes Oracle. Laufzeitpakete benötigen getrennte Root-Prüfung.

## Verbleibende Risiken

Tatsächliche Abnahme und gehostete Prüfungen des exakten Heads bleiben getrennte Arbeit. Kein Auslieferungs- oder Laufzeit-PASS wird behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Go/race/vet und Hosttests wurden für die reine Python-Consumer-Änderung nicht erneut ausgeführt; integrierte Validierung bleibt Aufgabe des Task-Verantwortlichen.

## Finaler Diff- und Review-Status

Fokussiertes Diff auf Scope und Bewahrung der unveränderlichen Basis geprüft. Kein Git-Commit, Push, PR-Merge oder gehostetes Gate-Ergebnis durch diesen Worker.
