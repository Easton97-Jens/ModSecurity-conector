# Change Record: CR-20261015-i12-capture-current-export-sdk-compat

**Sprache:** [English](CR-20261015-i12-capture-current-export-sdk-compat.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-capture-current-export-sdk-compat |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation und Problemstellung

Native Evidence-Tests schlugen mit der öffentlichen libModSecurity-3.0.12-API fehl; die Capture-Installation akzeptierte nur ihre historische Revision.

## Akzeptanzkriterien

Beide unterstützten ID-Argumentsignaturen ohne Casts oder deaktivierte Warnungen kompilieren. Alle historischen Capture-Bytes erhalten. Vor jedem Overlay-Schreibzugriff einen vollständigen aktuellen Git-Export prüfen.

## Implementierungsentscheidung und Begründung

C17-Generic-Auswahl der ausgewählten öffentlichen Deklaration und explizite Ownership der Intervention-Strings verwenden. Eine strikte v2-Quellinventur ergänzen; v1-Validierung und alle neun historischen Profile erhalten. Die versionierte Controller-Verlagerung ändert nur ihre autorisierte Run-Wurzel.

## Geänderte Dateien

`ci/runtime/lifecycle/native-lifecycle-observer.[ch]`, dessen native Tests, Apache-Headerprobe/-Tests, `ci/runtime/lifecycle/i12/{capture_sources.py,test_capture_sources.py,manifest.json,objects/}`, beide I12-README-Sprachdateien und dieses Change-Record-Paar.

## Ausgeführte Befehle

`rtk proxy python3 -B -m unittest discover -s ci/runtime/lifecycle/i12 -p test_capture_sources.py -v`: 48 Tests, Exit 0. Native Observer- und Apache-Headertests: 38 Tests, Exit 0 mit expliziten SDK-Include-/Bibliothekswurzeln. `rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py verify`: Exit 0, 155 Objekte und neun Profile. `rtk proxy git diff --check`: Exit 0.

## Security-Auswirkung

Zusätzliche/fehlende Dateien, doppelte Felder, Spezialdateien, Links, geänderte Modi/Hashes und Git-Metadaten vor Schreibzugriffen ablehnen. Keine Credential-, Isolations-, Compiler-, Scanner- oder Gate-Kontrolle wird abgeschwächt. Ein vertrauenswürdiger Git-Exportproduzent bleibt erforderlich; ein Revisionsstring allein ist nicht authentifiziert.

## Runtime-Evidence

Diese Änderung belegt nur Kompilierung und Capture-Integrität. Die native Headerprobe verwendet tatsächliche APR- und SDK-Bibliotheken; Kompilierung mit Legacy-Headern belegt keine 3.0.12-Runtime. Die aktuelle Apache-Hostqualifikation bleibt eine getrennte Lieferung von PR #414.

## Bekannte Einschränkungen

Keine Apache-Abnahme oder I12_COMPLETE-Behauptung. Historische Quelloverlays behalten ihre ursprüngliche Semantik und Before-Hash-Prüfungen. Der Controller bleibt ein geprüftes externes Ausführungsverfahren ausschließlich für Tests.

## Verbleibende Risiken

CI und SonarCloud für den exakten Head müssen nach normaler Lieferung an #410 und Integration in #414 noch laufen.

## Nicht ausgeführte Prüfungen mit Begründung

Die erste zweisprachige Dokumentationsprüfung scheiterte, weil dieser isolierte Worktree keinen befüllten Framework-Checkout enthält. Die finale Prüfung `make check-bilingual-docs check-doc-links` bestand mit Exit 0 und schreibgeschützter Framework-Bindung im privaten Mount-Namespace; Gitlinks und äußere Mounts blieben unverändert. Diese Reparatur behauptet keinen Hostlauf.

## Finaler Diff- und Review-Status

Root prüfte die begrenzten SDK-/Capture-Änderungen und die Invarianten historischer Rekonstruktion. Normaler Commit/Push und finale Remote-Rückprüfung werden getrennt verfolgt; kein Merge ist autorisiert.
