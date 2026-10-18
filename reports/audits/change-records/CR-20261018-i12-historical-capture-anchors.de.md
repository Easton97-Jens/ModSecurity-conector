# Change Record: CR-20261018-i12-historical-capture-anchors

**Sprache:** [English](CR-20261018-i12-historical-capture-anchors.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-i12-historical-capture-anchors |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `2c38d0ff2960a9ff2a76291955e808683febf06e` |

## Motivation und Problemstellung

Die normale autorisierte Produktintegration änderte fünf Live-Dateien, die weiterhin als historische Capture-Objektspeicher dienten. Registry.verify wies dadurch jedes Profil einschließlich lighttpd vor dem Hostbuild zurück. Der erhaltene Fehler lautet Source byte hash mismatch: ba8fe2b69ace0e6dae345b59bc20ddc09594a5e2426a16209ee4d0e72b19baa6.

## Akzeptanzkriterien

Jede historische Objektidentität, jedes Profilziel, jedes Delta und Byte erhalten. Die vollständige Registryprüfung ohne Änderung aktueller Produktquellen oder Annahme abweichender Bytes wiederherstellen.

## Implementierungsentscheidung und Begründung

Fünf historische Repositoryobjekte verwenden nun den vorhandenen verlustfreien text_lines-Speicher. Jede Quelle wurde aus exakter Gitrevision9980eb049dde0643da6a4f04e3b6712801b670b3 wiederhergestellt und unabhängig gegen ihren ursprünglichen SHA256 geprüft. Die fünf Quellidentitäten und alle Profilzuordnungen bleiben unverändert. Dies ist eine Reparatur des Messarchivs; Produktänderungen bleiben in ihren zuständigen Branches.

## Geänderte Dateien

ci/runtime/lifecycle/i12/manifest.json und fünf begrenzte objects/text/*.lines.json-Dateien; dieser zweisprachige Change Record. Drei historische HAProxy- und zwei lighttpd-Snapshots werden erhalten; keine HAProxy- oder andere Connector-Produktdatei wird bearbeitet.

## Ausgeführte Befehle

Alle Befehle verwenden RTK. capture_sources.py verify besteht155 Objekte und9 Profile, source_only=true/runtime_qualified=false. Exakte Gitblob-SHA256-Vergleiche bestehen für alle fünf Snapshots. Die vorhandenen48 negativen Capturekontrollen für Ownership/Hash/Delta bestehen; EN/DE- und Repositorylinkprüfungen bestehen.

## Security-Auswirkung

Quellregistry, aktuelle exportierte Baumprüfung, Textgrößenlimit, Symlink-/Hardlinkverbote und exakte Patchprüfung bleiben unverändert. Historische Instrumentierung wird nicht als aktuelle Produktquelle ausgegeben.

## Runtime-Evidence

Run i12-lighttpd-412-completion-20261015/shared/historical-anchors-20261018.json bindet ursprüngliche Revision, Pfade, Identitäten, Bytezahlen und neue Speicherpfade. Die gescheiterte Diagnosevorbereitung bleibt erhalten. Frische Hostvorbereitungen müssen tatsächliches aktuelles Produktmodul und Patch weiterhin getrennt binden.

## Bekannte Einschränkungen

Registryerfolg belegt ausschließlich die Quellmaterialisierung; er ergänzt keinen Lifecycle-PASS und keine Original-Oracleklärung.

## Verbleibende Risiken

Künftige aktuelle Produktvarianten benötigen weiterhin ausdrückliches hashgeprüftes Rebasing der Beobachtungsinstrumentierung; unveränderliche historische Quellen dürfen einen Produktfix niemals still ersetzen.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Hostausführung anderer Connectoren, Framework/MRTS-Änderung, Veröffentlichung, Bereitstellung oder Masterintegration. Gehostete CI am exakten Head bleibt nach normaler Publikation separat.

## Finaler Diff- und Review-Status

Root prüfte alle fünf alten/neuen Objektzuordnungen und unveränderte Profilziele. Diese notwendige gemeinsame Reparatur wird über den bestehenden#410 veröffentlicht und durch normalen Merge in#412 übernommen.
