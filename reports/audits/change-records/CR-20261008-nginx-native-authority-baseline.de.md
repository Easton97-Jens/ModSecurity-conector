# Change Record: CR-20261008-nginx-native-authority-baseline

**Sprache:** [English](CR-20261008-nginx-native-authority-baseline.md) | Deutsch

Explizites Baseline-Authority-Wiring; ausschließlich Unit-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-authority-baseline |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `6b069af4c2c87cdbddd7efc8867f642b1dd03098` |

## Motivation und Problemstellung

Die Baseline muss Collector und Finalizer explizite native Artefaktautorität liefern, ohne die rohe Evidence-Wurzel aufzuwerten oder globale Build-Wurzeln umzudefinieren.

## Akzeptanzkriterien

Für ausgewählte geschlossene native NGINX-Full-Lifecycle-Cases initialisierte Pflichtrecords erhalten, vorbereiteten tatsächlichen Prefix und alle fünf expliziten Fault-Libraries verlangen, ein frisches privates Authority-Unterverzeichnis erstellen und spätere Snapshot-Prefix-Abweichungen ablehnen.

## Implementierungsentscheidung und Begründung

prepare_nginx_native_authority läuft nach kanonischem init und vor der Stage. Die tatsächliche Katalogauswahl wird mit den geschlossenen CASE_IDS des Framework-Readers geschnitten; ausgewählte Deskriptoren sind Pflicht. Explizites NGINX_PREFIX liefert dieselben Pfade sbin/nginx und modules/ngx_http_modsecurity_module.so wie der native Dispatcher. Der Producer erhält aktuelle Parent-/Framework-Wurzeln und Framework/tools/MRTS, Run-Identität, fünf originale Library-Eingaben und artifact_root=STAGE_BUILD_ROOT. Ein exklusives 0700-Verzeichnis host-runtime/native-authority-<run> erhält das Original. Der Collector bekommt --allowed-native-operation-root STAGE_BUILD_ROOT; der Finalizer --native-operation-authority mit dem Originalpfad. Der später validierte Runtime-Snapshot muss dem versiegelten Prefix entsprechen.

## Geänderte Dateien

Nur ci/runtime/lifecycle/run-no-crs-baseline.sh, die neue tests/test_no_crs_native_authority_wiring.py und dieser zweisprachige Record.

## Ausgeführte Befehle

RTK-verpacktes unittest zeigte zuerst fünf Fehler wegen des fehlenden Helpers (RED). Die neuen acht extrahierten Shell-Kontrollen bestanden danach im kombinierten Wiring-Lauf. sh -n bestand. Kombinierte vorhandene/neue Wiring-Tests: 48 Tests, zwei Fehler wegen fehlender Apache-Fixtures und 26 vorhandene Dependency-Skips. Der Repository-Generator erstellte das Paar; Archiv- und abschließende Whitespace-Prüfungen sind im Handoff dokumentiert.

## Security-Auswirkung

Fehlender Prefix oder eine fehlende Fixture blockiert nach Initialisierung mit Fehlercode; kein ausgewählter Pflichtcase wird ausgeschlossen. Kein Legacy-Library-Fallback, keine Shell-Auswertung von Katalogdaten und keine erfundenen nativen Events. Frische Verzeichnisse werden per Descriptor und vorhandenen sicheren Parent-Verzeichnisprüfungen erzeugt. Der Producer validiert Quellen/Pfade/Digests unabhängig streng; Unit-Doubles belegen nur Wiring.

## Runtime-Evidence

Keine. Neue Tests verwenden begrenzte Auswahl- und Producer-Doubles; kein nativer Binary-Aufruf, Compilerlauf oder vollständige Baseline. Root-Hostrollen, Runtime-Provenienz und kanonisches PASS werden nicht belegt.

## Bekannte Einschränkungen

Der Authority-Producer verlangt saubere aktuelle gepinnte Quellwurzeln und explizite vorgebaute Artefakte. Der tatsächliche Invocation-Snapshot entsteht erst nach Stage-Provisioning; native Aufrufer müssen den vorbereiteten Prefix vorher übergeben. Vorhandene breite Tests sind wegen fehlender Framework-Fixtures in diesem isolierten Worktree nicht vollständig ausführbar.

## Verbleibende Risiken

Der Koordinator muss integriertes Wiring gegen tatsächliches Framework sowie Collector-/Finalizer-Commits erneut prüfen, vorbereitete Build-Bereitschaft verifizieren und frische autorisierte native Evidence erfassen. Hashing allein verifiziert keinen Build.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständige Baseline-Erfassung, native Builds/Runtime und kanonische Retention lagen außerhalb dieses Slice. Zwei vorhandene Apache-Phase4-YAML-Fixtures fehlen; 26 vorhandene Dependency-Tests wurden übersprungen. Das ist keine neue bestandene Evidence. Keine Paketinstallation.

## Finaler Diff- und Review-Status

Fokussierte Shell-/Test-/Record-Änderungen geprüft. Bestehende Warning-/Capability-/Payload-/Event-Behandlung, globales BUILD_ROOT und RAW_DIR-Collector-Grenze bleiben unverändert. Keine Schreibzugriffe auf Root-Worktree, zentrale Validatoren, Katalog, Schema, Gitlinks oder MRTS.
