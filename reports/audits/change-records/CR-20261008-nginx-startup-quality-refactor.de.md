# Change Record: CR-20261008-nginx-startup-quality-refactor

**Sprache:** [English](CR-20261008-nginx-startup-quality-refactor.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-startup-quality-refactor |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `54877d2824c402a3912c71755bac7fcc884da5f4` |

## Motivation und Problemstellung

Sieben aktuelle Parent-Sonar-Findings betreffen Literal-Duplikate und kognitive Komplexität in strengem Startup-/Receipt-Code. Das achte Configtest-Driver-Finding gehört dem Koordinator.

## Akzeptanzkriterien

Exakte Operationen, Fehler, native Transaktions-/Regelbindung, PIDFD-Ownership-Cleanup, Capture-Grenzen und serialisierte Artefaktbytes bewahren.

## Implementierungsentscheidung und Begründung

Begrenzte Helfer für Startup-Captures, Rollenbeobachtung, geordnetes Master-Ende, gebundene Kindprozesse, echte native Probe und Receipt-Felder extrahieren. Konstanten nutzen, öffentliche Driver-Einstiegspunkte unverändert lassen.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-valid-rules.py; ci/runtime/lifecycle/collect-no-crs-source.py; tests/test_nginx_valid_rules_driver.py; dieses EN/DE-Paar.

## Ausgeführte Befehle

RTK-geprüftes Parent-Python: zwei fehlende Helfer RED, danach 23 Valid-Rules-Tests GREEN und zehn Config-Collection-Kontrollen GREEN. Collector-Suite60: zwei fehlende Framework-Kataloge und drei SKIPs im isolierten Worktree, kein Produkt-PASS. Git-Diff-Check vor Commit. Sonar-Regel-API400 verhindert frische Regeldetails; gemeldeter S3776-/S1192-Snapshot genutzt.

## Security-Auswirkung

Keine Ownership-, Containment-, Transaktions-, Integer-Regel-, Timeout-, Cleanup-, Event- oder Artefakt-Prüfung abgeschwächt. Erzwungenes Cleanup bleibt unverifiziert.

## Runtime-Evidence

Keine neue Runtime-Behauptung: Unit-Mocks prüfen Fehler und exakte erhaltene Argumente. MIME-Diagnose ist getrennt und validiert nicht diesen Startup-Refactor.

## Bekannte Einschränkungen

Remote-Sonar-Abschluss und echte integrierte Startup-Validierung sind Koordinator-Prüfungen. Der verschachtelte Framework-Checkout ist hier bewusst nicht initialisiert.

## Verbleibende Risiken

Integrationskonflikte mit neuen Receipt-Feldern benötigen semantisches Review; dieser Patch fügt keine Receipt-Felder hinzu.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständiger Parent-Lint und integrierte/Remote-Prüfungen hier nicht ausgeführt. Breite Collector-Suite findet keinen isolierten Katalog; integrierten Worktree ohne Prüfungsumgehung verwenden.

## Finaler Diff- und Review-Status

Nur explizite Task-Dateien; separater lokaler Commit, kein Push, Merge, Amend oder Gitlink-Update. Finale Akzeptanz weiterhin offen.
