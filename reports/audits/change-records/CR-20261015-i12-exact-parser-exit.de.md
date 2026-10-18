# Change Record: CR-20261015-i12-exact-parser-exit

**Sprache:** [English](CR-20261015-i12-exact-parser-exit.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-exact-parser-exit |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `a2d545ac7ec4abce23595e1c033f094104617201` |

## Motivation und Problemstellung

Der strengere Parserqualifier ließ nur Zurückweisungsexit1 zu. Offizielles lighttpd1.4.85 server.c liefert nach gescheitertem Modul-set-default-1 und damit tatsächlichen POSIX-Prozessexit255. Exakte quellgeprüfte255-Erwartungen müssen ohne Änderung gemessener Exits oder Normalisierung aller Fehlerwerte darstellbar sein.

## Akzeptanzkriterien

Exakten ganzzahligen Exit in0..255 verlangen, Annahme0, Zurückweisung1..255. Tatsächliche Exitgleichheit, unabhängige Erwartungsprovenienz, ausdrückliche Rootprüfung, physische Parserreceipts und sämtliche vorhandenen Pflichtproducer erhalten.

## Implementierungsentscheidung und Begründung

Das Erwartungstupel mit zwei Werten wird durch begrenzte typisierte Annahme-/Zurückweisungsvalidierung ersetzt. Boolesche und Float-Exiterwartungen werden zurückgewiesen. Eine quellgeprüfte255-Erwartung akzeptiert nur tatsächliche255; tatsächliche1 bleibt FAIL. Keine Änderung des HTTP-/Body-Lifecyclescopes.

## Geänderte Dateien

ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py und tests/test_i12_lifecycle_ledger.py; dieser EN/DE-Record.

## Ausgeführte Befehle

Zwei neue RTK-gekapselte Regressionen reproduzieren die Baselinezurückweisung von255 und fälschlich zulässige Bool-/Float-Oracles. Nach Korrektur: gemeinsame Lifecycle-/Oracle-/Workflowsuiten47 PASS. Actionlint für den SDK-Workflow besteht ebenfalls.

## Security-Auswirkung

Alle exakten Prozess-/Quell-/Image-/Abwesenheits-/Cleanupguards bleiben erzwungen. Die Implementierung genehmigt keine Oraclekorrektur; jede Original-ID benötigt eigene unabhängige Reconciliation. Keine Lockerung von Gate, Warnung oder Isolation.

## Runtime-Evidence

Run i12-lighttpd-412-completion-20261015/shared/parser-exact-exit-final.log enthält47 erfolgreiche Tests. Vorhandene sieben diagnostische Parserreceipts beobachten255; strengere frische Pakete und getrennte Korrekturen je ID bleiben Folgearbeit in#412. Synthetische Validatorfixtures belegen ausschließlich den Validator.

## Bekannte Einschränkungen

Parserqualifikationen bleiben configuration_control mit full_lifecycle_qualified=false. Diese Änderung ergänzt keinen Host-PASS und keine automatische Original-Oracleklärung.

## Verbleibende Risiken

Geprüfte Quellerwartungen können weiterhin falsch sein; physische exakte Receipts und unabhängige Rootquellprüfung bleiben verpflichtend.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Veröffentlichung, Masterintegration, Framework/MRTS-Änderung oder Hostmatrix anderer Connectoren. Gehostete CI am finalen Head steht nach normaler Publikation aus.

## Finaler Diff- und Review-Status

Root prüfte den engen gemeinsamen Fehler und erhielt parallele Parserhärtung auf Remote#410 durch normalen Merge. Produktfixes werden getrennt über#382 integriert.
