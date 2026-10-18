# Änderungsnachweis: CR-20261018-i12-current-traefik-capture

**Sprache:** [English](CR-20261018-i12-current-traefik-capture.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-current-traefik-capture |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `a311c725c44a7a4da95acb1a4818f66bd56c462a` |

## Motivation und Problemstellung

Die aktuelle Produktintegration machte drei historische Repository-Objektreferenzen ungültig; die exakten historischen Observer-Eingabepins wiesen vollständige aktuelle Traefik-Exporte zurück.

## Akzeptanzkriterien

Alle historischen Quell-/Ergebnisidentitäten bleiben exakt; zusätzlich werden nur geprüfte aktuelle Observer-Basen nach vollständiger v2-Prüfung zugelassen; Negativkontrollen verwerfen alternative Legacy-Basen und unabhängige Manipulation.

## Implementierungsentscheidung und Begründung

Die drei authentifizierten historischen Byteströme als verlustfreie text_lines einfrieren. Historische Pins und Ergebnisbytes erhalten. Exakte current_before_sha256-Alternativen nur für die beiden Observer-Ziele jedes vorhandenen Traefik-Profils ergänzen und tatsächliche Eingabe-Hashes im Beleg erfassen.

## Geänderte Dateien

`ci/runtime/lifecycle/i12/capture_sources.py`, `manifest.json`, `test_capture_sources.py`, `README.md`, `README.de.md`, three `objects/*.lines.json`, and this Change Record pair.

## Ausgeführte Befehle

`rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py verify`: passed, 155 objects and 9 profiles. `rtk proxy python3 -B -m unittest discover -s ci/runtime/lifecycle/i12 -p test_capture_sources.py -q`: passed, 51 tests.

## Security-Auswirkung

Keine UID-, Namespace-, Peer-, Admission-, Dateisystem- oder Hashprüfung wird abgeschwächt. Die aktuelle Alternative ist im Manifest gepinnt und erfordert vollständige Inventarprüfung vor jedem Capture-Schreibzugriff.

## Runtime-Evidence

Kein Host wurde gestartet. Quellprüfung belegt ausschließlich die Quellanwendung.

## Bekannte Einschränkungen

Die erhaltenen instrumentierten Ergebnisbytes besitzen ihre historische Observer-ABI. Jeder neue Build muss sein tatsächliches SDK und seine geladene Instrumentierung binden und prüfen.

## Verbleibende Risiken

Eine gültige Quellanwendung belegt keine Host-Lifecycle-Qualifikation. Neue integrierte Builds und Beobachtungen bleiben Aufgabe des Hauptauftrags.

## Nicht ausgeführte Prüfungen mit Begründung

Hostausführung und gehostete CI/Sonar wurden in dieser reinen Quellteilaufgabe nicht ausgeführt; sie folgen der Integration.

## Finaler Diff- und Review-Status

Gezielte Quelltests bestanden. Root-Integration und unabhängiges Review stehen aus; unabhängige Gate-Änderungen im gemeinsamen Worktree blieben erhalten.
