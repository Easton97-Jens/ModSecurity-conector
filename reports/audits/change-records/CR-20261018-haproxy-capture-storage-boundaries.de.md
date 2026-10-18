# Change Record: CR-20261018-haproxy-capture-storage-boundaries

**Sprache:** [English](CR-20261018-haproxy-capture-storage-boundaries.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-capture-storage-boundaries |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation und Problemstellung

Zehn zugewiesene Sonar-Befunde betreffen Capture-Komplexität, wiederholte Pfade, eine Exception-Prüfung und die Quellenzulassung. Eine begrenzte Regression zeigte, dass ein Archivaustausch nach der Hashprüfung die eingelesenen Quellen änderte. Eine zweite Regression zeigte die Zulassung eines beschreibbaren Quellenankers.

## Akzeptanzkriterien

Die authentifizierten Bytes müssen den eingelesenen Bytes entsprechen. Eingabe und Materialisierung müssen gehaltene Verzeichnisdeskriptoren ohne Linkverfolgung verwenden. Der private Storage-Eigentümer muss geprüft werden. Bestehende Capture-Quellbytes, Modi und Normalisierungsbelege müssen identisch bleiben; alle ursprünglichen Oracle-Lücken bleiben unverändert.

## Implementierungsentscheidung und Begründung

Das Archiv wird relativ zu einem gehaltenen Storage-Deskriptor geöffnet, als reguläre Datei geprüft und einmal gelesen. Der geprüfte Puffer wird über `BytesIO` eingelesen. Ausgabeverzeichnisse und exklusiv erzeugte reguläre Dateien werden relativ zu gehaltenen Deskriptoren angesprochen; ein Austausch des sichtbaren Quellenverzeichnisses führt zur Ablehnung. Der abschließende Build-Beleg verwendet den authentifizierten Archivhash. Die native Quellenzulassung leitet Komponenten aus `relative_to` ab und prüft den gehaltenen privaten Root. Export und Portierung verwenden kleine Hilfsfunktionen; wiederholte Pfade verwenden Konstanten.

## Geänderte Dateien

- `connectors/haproxy/harness/i12_current_capture.py`
- `connectors/haproxy/harness/i12_native_contracts.py`
- `tests/test_haproxy_i12_current_capture.py`
- `tests/test_haproxy_i12_native_source_paths.py`
- `reports/audits/change-records/CR-20261018-haproxy-capture-storage-boundaries.md`
- `reports/audits/change-records/CR-20261018-haproxy-capture-storage-boundaries.de.md`

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_current_capture tests.test_haproxy_i12_native_source_paths
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_native_cases
```

Die beiden Basisregressionen scheitern an den vorgesehenen Assertions; 19 gezielte Tests und 19 bestehende native Tests bestehen. Ein Export der exakten Basisrevision ausschließlich zur Vorbereitung und eine Release-Extraktion vergleichen Bytes und Modi mit dem eingefrorenen Build. Exakte Argumente, Exits und Rohdatenhashes bleiben in den Laufbelegen erhalten.

## Security-Auswirkung

Dies ist eine begrenzte defensive Harness-Korrektur. Sie enthält keinen Scan, keine Ausnahme, Unterdrückung, Gate-Änderung oder Änderung der Produkt-Autorisierung. Es werden keine durch die Shell expandierten Archivpfade eingeführt. Die Deskriptoroperationen benötigen die bestehende Linux-Laufzeit und einen privaten Storage-Root im Eigentum des ausführenden Nutzers.

## Runtime-Evidence

Es wird kein Hostlauf und keine neue Kompilierung beansprucht. Die Vorbereitung stimmt mit 2173 Dateien der aktuellen Basis, 1944 Dateien der historischen Basis und je 2175 Dateien der drei Capture-Varianten einschließlich Inventarmetadaten überein. Nur pfadabhängige Belegmetadaten und zwei bestehende generierte Staging-Helfer sind ausdrücklich ausgenommen. Alle 1391 Upstream-Dateien stimmen in Bytes und Modi überein; alle 11 Normalisierungseinträge sind identisch. Evidence-Root: `R2/sonar-haproxy/7ad-capture-boundaries-20261018`.

## Bekannte Einschränkungen

Der Root-Operator und die ausgewählte Quellrevision bleiben vertrauenswürdig. Dies begründet keinen unveränderlichen Storage gegenüber demselben privilegierten Operator und qualifiziert keine Lifecycle-Route. Der eingefrorene Build und historische Fixtures bleiben unverändert.

## Verbleibende Risiken

Die Sonar-Server-Rücklesung steht noch aus. Lokaler Code und Regressionen belegen Verhalten, jedoch keinen serverseitigen Abschluss. Künftige Consumer-Builds müssen ihre eigene exakte Quellrevision erfassen; der bestehende Build bezeichnet weiterhin seinen eingefrorenen Producer.

## Nicht ausgeführte Prüfungen mit Begründung

Es liefen kein Hostverkehr, kein neuer Produktbuild und keine breite Sicherheitsbewertung: Dieser Auftrag betrifft ausschließlich die angegebenen Harness-Befunde und Prüfungen zur Quellerhaltung. Root verantwortet Host-Abnahme, Veröffentlichung und Server-Rücklesung.

## Finaler Diff- und Review-Status

Die eigenen Änderungen bewahren die ursprünglichen Quellverträge und verwenden die bestehende Capture-Infrastruktur. Unabhängige Root-Prüfung und Veröffentlichung bleiben erforderlich. Git-Mutationen gehören nicht zu dieser Arbeit.
