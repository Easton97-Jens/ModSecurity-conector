# Change Record: CR-20261009-nginx-native-collection-authority

**Sprache:** [English](CR-20261009-nginx-native-collection-authority.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-native-collection-authority |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `cf95e1e2519909d498a4a6fdb0e21db16b2ae3c4` |

## Motivation und Problemstellung

Der echte Root-Master-/nobody-Worker-Lauf `nginx_all_required_20261009_r6`
erreichte reale YAML-, Konfigurations- und Native-Invocations und stoppte dann
während der Collection mit `native bundle raw events cannot enter generic
collection or scrubbing`. Der Parent übergab die gesamte Stage
`nginx-host-work` als Native-Authority, obwohl gewöhnliche Harness-Protokolle
innerhalb dieser Stage Geschwister der geschützten Native-Operation-Bundles
sind.

## Akzeptanzkriterien

Das exakte invocationslokale Native-Operation-Verzeichnis an den Collector
übergeben. Gewöhnliche Geschwisterprotokolle müssen weiterhin sammelbar sein,
während Bytes von Native-Receipt und Raw-Events außerhalb der generischen
Collection und unverändert bleiben. Bestehende Negativkontrollen für Symlinks,
Ownership, Berechtigungen, Identität, Duplikate, Seals und Raw-Events müssen
weiterhin fail-closed arbeiten.

## Implementierungsentscheidung und Begründung

Nur das Parent-Lifecycle-Argument wird von `$STAGE_BUILD_ROOT` auf
`$STAGE_BUILD_ROOT/host-runtime/native-operations-$NO_CRS_RUN_ID` eingeengt.
Der Parent-Collector-Guard bleibt unverändert. Eine Wiring-Regression
fixiert das exakte Argument; eine Mixed-Topology-Regression beweist, dass ein
gewöhnliches Geschwisterprotokoll verbraucht wird, während Native-Receipt und
Raw-Event bytegleich bleiben.

## Geänderte Dateien

`ci/runtime/lifecycle/run-no-crs-baseline.sh`;
`tests/test_no_crs_native_authority_wiring.py`;
`tests/test_nginx_native_operation_collection.py`; dieses englisch/deutsche
Change-Record-Paar.

## Ausgeführte Befehle

Alle Befehle verwendeten `rtk proxy`. Die test-first Wiring-Regression führte
9 Tests aus und scheiterte mit genau 1 Assertion gegen das alte breite
Argument (Exit 1, SHA-256
`0c8617d82e8e2d7449293cbc9b28ceb8473bf7b1cf23a50bed75097566ef6b3c`).
Der fokussierte Wiring-/Collection-Lauf bestand 25 Tests (Exit 0, SHA-256
`0bc77456d0ef4950b8314c21b407c5ce918ec13158dc21788219a98b88c71cb4`).
Die erweiterte Collector-, Dispatcher-, Projection- und First-Byte-Matrix
bestand 117 Tests (Exit 0, SHA-256
`7cbd353497bffd4515198d396876536483e8a16fb85f9255dd18828d8dcf4f4a`).
`sh -n` und ShellCheck bestanden für das geänderte Lifecycle-Skript; `bash -n`
und ShellCheck bestanden für beide externen Test-Helper.

## Security-Auswirkung

Die Korrektur reduziert die geschützte Native-Authority von einer gesamten
Build-Stage auf den exakten Parent der versiegelten Bundles. Der Guard, der
unveränderliche Native-Raw-Events vom generischen Scrubbing fernhält, bleibt
intakt; dies umfasst auch die Ablehnung einer generischen Zeile, die auf einen
Pfad im Native-Subtree verweist. Kein Validator, keine Selection-Regel, keine
Source-Provenance sowie keine Framework- oder MRTS-Datei wird geändert.

## Runtime-Evidence

Der aufbewahrte R6-Lauf endete an der ursprünglichen Collector-Grenze mit Exit
2 nach echten Root-Master-/nobody-Worker-Requests; er ist Fehler-Evidence und
keine PASS-Evidence. Für diese Korrektur wurde noch kein Lifecycle-Rerun
ausgeführt.

## Bekannte Einschränkungen

Unit- und Vertragstests beweisen weder den gehosteten Lifecycle noch einen
Canonical PASS. Ein frischer revisionsgebundener Build und ein isolierter
Root-Master-/nobody-Worker-Lauf bleiben erforderlich.

## Verbleibende Risiken

R6 zeichnete außerdem nicht-null Driver-Exits für
`body_size_nonzero_with_null_data` und
`header_count_nonzero_with_null_headers` auf. Sie werden nicht mit diesem
Authority-Defekt vermischt und benötigen eine frische Klassifikation nach dem
Fix, falls sie erneut auftreten.

## Nicht ausgeführte Prüfungen mit Begründung

In dieser fokussierten Pre-Commit-Phase liefen die vollständige
Parent-Fokus-Suite, vollständiger Lint, frischer Build, frisches E2E,
Canonical-Finalisierung, CI/Sonar des aktuellen Heads und der geschützte
Exact-Head-Workflow noch nicht. Sie bleiben separate erforderliche Gates. Ruff
bleibt in der bestehenden Umgebung nicht verfügbar; es wurde keine Dependency
installiert.

## Finaler Diff- und Review-Status

Unabhängige Code- und Security-Reviews fanden keinen blockierenden Befund. Der
Task-Diff enthält die eine Parent-Argumentänderung, zwei Regressionstestdateien
und dieses zweisprachige Record-Paar. Bei Finalisierung des Records stehen
Commit, Push, Remote-Readback und gehostete Verifikation aus.
