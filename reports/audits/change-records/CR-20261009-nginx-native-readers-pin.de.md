# Change Record: CR-20261009-nginx-native-readers-pin

**Sprache:** [English](CR-20261009-nginx-native-readers-pin.md) | Deutsch

Protokoll des separat veröffentlichten Framework-Abhängigkeitsupdates; kein nativer PASS wird behauptet.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-native-readers-pin |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `e319c932db7da011feca54fcb1fc5d2ab5d6018f` |

## Motivation und Problemstellung

Parent an den belegten Paket-Bootstrap der eigenständigen nativen Finalisierung und den strikten case-/run-gebundenen Projection-Reader binden. Die Parent-Producer-Fixes besitzen separate Commits.

## Akzeptanzkriterien

Parent verzeichnet das remote verfügbare Framework b283851c1fd70a031832d2e95e10dfcc4bc4f068. MRTS bleibt 8a6bb546c4c81d8ffc7be801dceac60c6925685f; alle 97 selektierten Required-Records bleiben erforderlich.

## Implementierungsentscheidung und Begründung

Nur den Framework-Gitlink von 7db219af6b6e911b73de8b437f82e63efdb06bde nach normalem Branch-Push und frischem Branch-/PR-Readback aktualisieren. Dieser Commit benötigt weder eine gemergte master-Abhängigkeit, Historienumschreibung noch eine Parent-Dispatch-Änderung.

## Geänderte Dateien

Gitlink modules/ModSecurity-test-Framework und dieses EN/DE-Änderungsprotokollpaar.

## Ausgeführte Befehle

Alle Befehle RTK-proxied. Am exakten b283851 bestand die Framework-Unittest-Discovery unter tests/no_crs: 405 Tests / 182,368s / Exit 0; Repository make lint endete 0. Dedizierter kombinierter CLI-/Reader-Fokus: 32 Tests und vollständige vier Dokumentationschecks endeten 0. git push war ein normaler Fast-Forward 7db219a..b283851; git ls-remote und gh pr view 137 lieferten unabhängig b283851, OPEN/DRAFT/Basis master. Verschachteltes Parent-Framework-Checkout und unveränderter tatsächlicher MRTS-HEAD wurden zurückgelesen. Externe Evidenz-Run-ID: nginx-all-required-20261008T124555Z; Dateien framework-integrated-suite-r1.log/.exit und framework-integrated-lint-r1.log/.exit. Dies sind Quellgates, keine Runtime-Evidenz.

## Security-Auswirkung

Autorität, Quellseals, strikte Status-/Evidenzprüfungen und Projection-Freshness bleiben verpflichtend. Kein Legacy-Namensfallback, keine Payload-Synthese und keine Required-Verkleinerung.

## Runtime-Evidence

Der vorherige lokale f639 R3-Lauf endete 2; die Finalisierung erzeugte kein originales Canonical-Ergebnis. Seine Projection-/Importfehler und Originalbytes bleiben historische Diagnoseevidenz, nicht Evidenz für diesen Pin.

## Bekannte Einschränkungen

Frischer Parent-Post-Pin-Fokus, vollständiger nativer Lint, neue NGINX-/Modul-/Interposer-Artefakte und echter Root/nobody-Lebenszyklus aller97 Records stehen aus.

## Verbleibende Risiken

Aktuelle revisionsgebundene PR-CI/Sonar, echte Runtime, vollständiger Canonical-Nachweis und Prüfsummenvalidierung bleiben erforderlich. Geschützte Trusted-Base-/Runner-/Admin-Voraussetzungen sind unabhängig blockiert.

## Nicht ausgeführte Prüfungen mit Begründung

An diesem Pin lief kein frisches vollständiges 97-Native-E2E und kein geschützter Dispatch; Voraussetzungen werden vorher geprüft. Separater Ruff-Lint bleibt nicht verfügbar und wird nicht erlassen.

## Finaler Diff- und Review-Status

Gitlink-only-Diff geprüft; normale Framework-Delivery gegenüber aktuellem Branch und Draft-PR #137 verifiziert. Parent-PR #396 bleibt Draft. Keine MRTS-Source-/Git-Änderung und kein Merge.
