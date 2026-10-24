# Change Record: CR-20261009-native-python-quality-sink

**Sprache:** [English](CR-20261009-native-python-quality-sink.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-native-python-quality-sink |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Frische PR396-Befunde betreffen Python-Quellenautorität, Komplexität, doppelte Literale und Klarheit von Ausnahmetests. Lokale Request-Guards sind Defense in Depth; die zugelassene CLI begrenzt bereits die zwei Fälle, ein Command-Injection-Exploit ist nicht nachgewiesen.

## Akzeptanzkriterien

Autorität, exakte typisierte Identitäten, Fehlerreihenfolge, Original-Seals und von null verschiedene Driver-Exitcodes erhalten; Qualitätsverhalten vor Refactoring charakterisieren und lokale Sink-Guards mit fehlschlagenden und anschließend erfolgreichen kontrollierten Tests belegen.

## Implementierungsentscheidung und Begründung

Identische feste Storage-Policy über bestehenden umgebungsunabhängigen Helfer ableiten, ohne Vorfahrenprädikate zu ändern. Source-/Collector-Prüfungen in ursprünglicher Reihenfolge extrahieren; doppelte JSON-Schlüssel weiterhin ablehnen. Exakte Request-Pfade und Integer-Ports lokal prüfen und -- vor die URL setzen.

## Geänderte Dateien

Vier zugewiesene Lifecycle-Module und ihre vier bestehenden dedizierten Testdateien. Sourceadapter-Tests bleiben in tests/test_nginx_native_operation_dispatch.py; Dispatcher-Source, Runtime-Utilities, Framework und MRTS bleiben unverändert. Die getrennte FD-Änderung hat einen eigenen Record.

## Ausgeführte Befehle

RTK-proxied bestehendes Parent-Python mit externem TMPDIR und expliziten aktuellen Framework-Wurzeln: python -m unittest tests.test_nginx_native_authority tests.test_nginx_native_operation_dispatch tests.test_nginx_common_input_fault_driver tests.test_nginx_native_operation_collection -v. Baseline33 Tests Exit0; Zwischenstand40 Tests Exit0. Korrigierte reale Baseline-Request-Kontrollen scheitern an12 Assertions; Guards bestehen. Evidenz: python-sonar-slice-baseline.log, python-sonar-quality-green.log, python-sonar-request-baseline-red-r2.log und python-sonar-request-green.log.

## Security-Auswirkung

Keine Freigabe öffentlicher Verzeichnisse, umgebungsgewählte Autorität, Validierungslockerung oder Unterdrückung. Policy-Routing des Literals ist keine Exploit-Remediation-Behauptung. Vorfahrenpolicy des Source-Verzeichnisses bleibt unverändert.

## Runtime-Evidence

Keine Native-Runtime-/E2E-Evidenz erzeugt; kontrollierte Subprocess-Ergebnisse prüfen ausschließlich argv und Retention.

## Bekannte Einschränkungen

Remote-Sonarauflösung benötigt einen Scan der integrierten Revision; die aktuellen81 Befunde werden durch lokale Unit-Ergebnisse nicht als aufgelöst bezeichnet.

## Verbleibende Risiken

Koordinator muss integrierten Source, vollständigen Lint und neuen exakten Revisionsscan unabhängig prüfen. Native Admission und Transportevidenz bleiben getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Native-Build/Runtime, Paketinstallation, Authentifizierungswechsel, Veröffentlichung oder Git-Schreibzugriff; diese Schritte gehören dem Koordinator.

Finaler fokussierter Sechs-Modul-Lauf am aktuellen Source:58 Tests,48.211s, Exit0 ohne Skips (python-sonar-slice-final-focus-r2.log), einschließlich Duplicate-Keyword-Erhaltung und Pointer-Driver-Kontrollen mit explizitem FRAMEWORK_ROOT. Frühere Nachprüfung9 Tests Exit0 mit einem Framework-abhängigen Skip wegen fehlendem FRAMEWORK_ROOT (python-sonar-slice-final-refinement.log). Record-Archiv und lokale Pfadprüfung aller vier neuen Records Exit0; vollständige Repository-Pfadprüfung Exit2 ausschließlich wegen fehlender isolierter Framework-Submoduldateien. Ruff Exit1, da das Modul in bestehender Parent-Umgebung fehlt; keine Installation versucht.

## Finaler Diff- und Review-Status

Begrenzten Diff auf Prädikate, exakte Fehlerreihenfolge, unveränderte Raw-Retention und tatsächliche Exits geprüft. Nur uncommittete isolierte Übergabe; keine Integration oder Remoteauflösung behauptet.
