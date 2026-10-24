# Change Record: CR-20261009-nginx-driver-quality-boundaries

**Sprache:** [English](CR-20261009-nginx-driver-quality-boundaries.md) | Deutsch

Verhaltensgleiche Qualitätskorrekturen der Treiber; Runtime- und Remote-Nachweise bleiben getrennte Gates.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-driver-quality-boundaries |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Die revisionsgebundene Parent-Analyse meldet wiederholte Literale,
verschachtelte Routenauswahl und überhöhte Client-Komplexität. Der Umbau muss
exakte Operationen, Source-Receipts und begrenzte HTTP-Beobachtungen erhalten.

## Akzeptanzkriterien

Die geschlossenen42 Native-Routen, Required-Auswahl, unveränderliche Omission-
Tupel-API, Strict-Abbruch nur der ersten Antwort, ursprüngliche deklarierte
Länge, Body-Grenzen, kein versteckter Reconnect und Marker-Barriere bleiben erhalten.

## Implementierungsentscheidung und Begründung

Explizite geschlossene Routentabellen, unveränderliche gemeinsame Fault-Werte
und benannte Artefaktkonstanten ersetzen Wiederholungen. Eingabeprüfung,
Request-Aufbau, begrenztes Antwortlesen und Marker-Freigabe werden in der
ursprünglichen Reihenfolge extrahiert. Socket-Erzeugung und finally-Cleanup
bleiben im Client. Variable Omission-/Event-Tupel bleiben Sammlungen ohne
erfundene Füllfelder.

## Geänderte Dateien

`ci/runtime/common/response_fixture_omission.py`; Lifecycle-Module
`nginx_sequence_client.py`, `nginx_sequence_upstream.py`,
`run-selected-nginx-native-operations.py`, `run-nginx-event-boundary-cases.py`,
`run-nginx-raw-h1.py`, `run-nginx-mime-cases.py`, `run-nginx-phase4-cases.py`;
`tests/test_response_fixture_omission.py`, `tests/test_nginx_sequence_client.py`,
`tests/test_nginx_dispatch_routes.py`, `tests/test_nginx_sequence_upstream_barrier.py`;
dieses englisch/deutsche Record-Paar. Die Lifecycle-Module liegen unter
`ci/runtime/lifecycle/`.

## Ausgeführte Befehle

Alle Befehle nutzten RTK und die vorhandene Parent-Python-Umgebung mit externen
Temporärdaten und explizitem Framework-Katalog. Die ursprünglichen37 Tests
bestanden. Fokusprüfungen für einfache Treiber21, geschlossenen Dispatch10,
Client/Transport13 und unabhängige Routen/Barrieren7 bestanden jeweils mit
Exit0. Die Teilmengen überlappen; ihre Zahlen werden nicht zu einer Suite
addiert. Record- und integrierte Gesamt-Gates folgen der Integration; keine
Remote-Schließung wird hier behauptet.

## Security-Auswirkung

Validierung, Source-Authority, Isolation, Body-Grenzen und Required-Vertrag
werden nicht abgeschwächt. Kontrollen lehnen fehlende/relative Fault-Libraries
und doppelte Katalogidentitäten ab. Socket-/Callback-Fehler werden weitergereicht
und schließen die ursprüngliche Verbindung; Fehlerbeobachtungen ergeben keinen
erfolgreichen Abbruchnachweis.

## Runtime-Evidence

Unit-Loopback-Fixtures und kontrollierte Antwort-/Barrieren-Kollaboratoren sind
keine NGINX-Runtime-Evidence. Für diesen Kandidaten wird kein nativer Request
oder Canonical PASS behauptet.

## Bekannte Einschränkungen

Ein zwischenzeitlicher neuer Test nahm fälschlich an, eine kurze Content-Length-
Lesung sei bereits geschlossen. Die Fehlerlogs bleiben erhalten; der
korrigierte Test erhält die Ablehnung einer ungeschlossenen Nachricht. Das ist
kein nachgewiesener Produktdefekt. Frische Sonar-Analyse und gemeinsame native
Evidence stehen aus.

## Verbleibende Risiken

Der reale Host muss Framing, Root-/nobody-Identitäten, native Fault-Zustellung,
Evidence aller selektierten Required-Records und Cleanup am integrierten Tupel
weiterhin nachweisen.

## Nicht ausgeführte Prüfungen mit Begründung

Ruff fehlt in der vorhandenen Umgebung und wurde nicht installiert. Voller
integrierter Lint, revisionsgebundene CI/Sonar, vollständige native Runtime und
geschützter Exact-Head-Nachweis werden durch die Fokustests nicht zertifiziert.

## Finaler Diff- und Review-Status

Die unabhängige read-only Prüfung fand keine konkrete Verhaltensregression,
identifizierte fehlende Snapshot-/Callback-/Barrieren-/Routen-Kontrollen;
diese wurden ergänzt und ausgeführt. Integration und finaler Diff-Review
bleiben Aufgaben des Koordinators.
