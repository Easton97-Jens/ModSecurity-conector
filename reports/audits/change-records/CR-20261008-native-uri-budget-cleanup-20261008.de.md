# Change Record: CR-20261008-native-uri-budget-cleanup-20261008

**Sprache:** [English](CR-20261008-native-uri-budget-cleanup-20261008.md) | Deutsch

Begrenzter Parent-Dokumentationsslice; keine Runtime-Promotion.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-native-uri-budget-cleanup-20261008 |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `7c169f5bbe946650431f8e0cdbe2ddc63d3e85c1` |

## Motivation und Problemstellung

Die geprüften URI-, ausgewählten Phasenbudget- und Cleanup-Reihenfolgeverträge des Koordinators dokumentieren, ohne Compile-Evidenz als Laufzeiterfolg darzustellen.

## Akzeptanzkriterien

Gleichwertige EN/DE-Leserdokumentation nennt alle vier gemessenen Aufrufe und alle ungemessenen API-Gruppen, exakte URI-Grenzen, Parserregeln und das ausstehende Runtime-Tupel. Keine Source- oder Framework-Änderung.

## Implementierungsentscheidung und Begründung

NGINX-spezifische URI-Projektion (256-Byte-Rohpuffer/255 escapte Bytes), festen 4096-Byte-Schreibpuffer, erhaltenen Query-Marker und strikte andere Common-Felder dokumentieren. CLOCK_MONOTONIC-Budget je Aufruf nach Rückkehr, deaktivierten geerbten Standard 0, strikt elapsed > budget und exakten nativen Erfolg 1 dokumentieren. Ungültige langsame Ergebnisse 0/2 sind keine positiven Timeouts. Common-Cleanup erfolgt vor dem nativen void-Aufruf; kein neuer Rückkehr-Cleanup-Receipt oder HTTP-Nachweis wird behauptet.

## Geänderte Dateien

`connectors/nginx/README.md` / `README.de.md`, `docs/connectors/nginx.md` / `nginx.de.md` und dieser EN/DE-Record. Keine generierte Konfigurationsreferenz bearbeitet.

## Ausgeführte Befehle

RTK-gewrapte Source-/Dokumentationslesevorgänge und der native Scaffold-Befehl `ci/tools/new-change-record.py create` wurden ausgeführt. Portable Validierungsbefehle/Ergebnisse:

- `rtk proxy "${PARENT_PYTHON}" ci/tools/new-change-record.py check`: Exit 0, Struktur PASS (keine Evidenzvalidierung).
- `rtk proxy make check-bilingual-docs PYTHON="${PARENT_PYTHON}"`: Exit 2; Checker-Exit 1 mit 22 bestehenden fehlenden Framework-Submodul-Linkzielen im isolierten Worktree, keine in geänderten Dateien.
- Direkter Aufruf `check_pairs_and_switches(Path.cwd())` des nativen Bilingual-Checkers: Exit 0, leere Fehlerliste.
- `rtk git diff --check`: Exit 0.

## Security-Auswirkung

Keine ausführbare Änderung. Verdeutlicht payloadfreie URI-Redaktion, unveränderte strikte Validierung und Grenzen weicher Budgets. Keine harte Unterbrechung und keine Timeout-Garantie für alle C-APIs.

## Runtime-Evidence

Kein nativer Laufzeittest für diesen Slice ausgeführt. Der Koordinator meldet fünf grüne URI-Query-Redaktionstests und fünfzehn grüne kompilierte Budget-Bridge-Tests; dies ist zugeordnete Unit-/Compile-Evidenz, kein lokal beobachtetes Laufzeitergebnis. Ursprüngliche 97 RequiredIDs/45 offene Einträge bleiben bestehen; neues Tupel NOT_RUN.

## Bekannte Einschränkungen

Source im Integrations-Worktree des Koordinators geprüft; dieser Dokumentationscommit integriert diese Source nicht. Die generierte Direktivreferenz bleibt Verantwortung des Koordinators. Bestehende historische Laufzeitaussagen sind keine Evidenz für das neue Tupel.

## Verbleibende Risiken

Ein hängender synchroner Aufruf bleibt nicht unterbrechbar. Ungemessene APIs haben kein ausgewähltes Aufrufbudget. Echte Host-, Cleanup-Rückkehr- und exakte Build-Receipts bleiben vor einer Laufzeit-Promotion erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Build/Laufzeittest, keine Framework-Tests, kein MRTS und keine Veröffentlichung: ausschließlich eigener Dokumentationsumfang und kein serialisierter nativer Slot. Root führt die abschließende integrierte Dokumentationsprüfung durch.

## Finaler Diff- und Review-Status

Lokaler EN/DE-Umfangs- und Diff-Review abgeschlossen; Record-Struktur- und Paarprüfungen bestanden, Einschränkung der vollständigen Linkprüfung oben festgehalten. Root übernimmt den integrierten Abschlussreview. Kein PR, Merge, Push oder externer Review behauptet.
