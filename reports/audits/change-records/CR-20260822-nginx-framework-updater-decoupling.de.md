# Change Record

**Sprache:** [English](CR-20260822-nginx-framework-updater-decoupling.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260822-nginx-framework-updater-decoupling |
| Datum (UTC) | 2026-08-22 |
| Basis-Revision | `c8881eaadf7d3ef5d4173d581a62726a2df3fdf2` |
| Delivery-Status | In einem dedizierten Draft-Pull-Request vorbereitet; kein Merge wird behauptet. |

## Motivation und Problemstellung

Der Framework-Update-Lauf `32557767129` validierte ein NGINX-Tupel
`release-1.31.4` aus dem Framework-Commit
`52fe6ee334f1381c35d5c3b7140433c626469523` und versuchte es zu
veröffentlichen. Der Push scheiterte, weil der allgemeine Publisher
`.github/workflows/nginx-root-broker.yml` ändern wollte. Eine spätere
Upstream-Provenienzprüfung stellte fest, dass `1.31.4` am 22.08.2026 kein
offiziell veröffentlichtes NGINX-Release war; die neueste veröffentlichte
Mainline-Version blieb `1.31.3`, die der geschützte Parent-Broker bereits nutzte.

## Akzeptanzkriterien

Der allgemeine Framework-Synchronisierer muss jede `NGINX_*`-Zuweisung
ignorieren, darf keine NGINX-Parent-Projektion und kein NGINX-Workflow-Ziel
enthalten und muss alle NGINX-eigenen Parent-Dateien byte-identisch lassen,
wenn sich ausschließlich Framework-NGINX-Daten ändern. Der dedizierte,
geschützte NGINX-Root-Broker bleibt vorhanden und auf das geprüfte
`1.31.3`-Release-Tupel gepinnt.

## Implementierungsentscheidung und Begründung

NGINX-Source-Felder, semantische Validierung, abgeleitete Werte und
Parent-Ziele werden aus dem allgemeinen Framework-zu-Parent-Synchronisierer
entfernt. Importzeit-Ownership-Guards und Regressionstests verhindern die
erneute Aufnahme eines NGINX-Feldes oder -Ziels. Damit entfällt der
Workflow-Write-Fehler, ohne dem allgemeinen Submodule-Publisher die
Berechtigung zum Ändern von Workflow-Dateien zu geben. Der Root-Broker bleibt
bestehen, weil er die privilegierte und unabhängig geprüfte
Ausführungsgrenze ist.

## Geänderte Dateien

- `ci/tools/sync-framework-component-versions.py`: entfernt allgemeine
  NGINX-Aufnahme und -Projektion, dokumentiert die Ownership-Grenze und ergänzt
  statische Registry-Guards.
- `tests/test_update_framework_versions.py`: beweist, dass feindliche oder
  zukünftige Framework-NGINX-Daten ungenutzt bleiben und NGINX-eigene
  Parent-Dateien nicht ändern können.
- Dieser zweisprachige Change Record und die Archiveinträge dokumentieren
  Autorisierung und Validierungs-Evidence.

## Ausgeführte Befehle

- `python3 -m py_compile ci/tools/sync-framework-component-versions.py tests/test_update_framework_versions.py`
- `python3 -m unittest -v tests.test_update_framework_versions tests.test_update_submodules_local_git tests.test_ci_security_workflows`
- `make PYTHON="$(command -v python3)" check-ci-security-contract`
- `make PYTHON="$(command -v python3)" check-bilingual-docs`
- `git diff --check`

## Runtime-Evidence

Der begrenzte Bootstrap führt die fokussierten Synchronisierer-, Local-Git-
Updater- und CI-Security-Suites auf dem exakten Branch-Head aus, bevor er den
finalen einzelnen Commit erzeugt. Nach dem Selbstentfernen des temporären
Bootstrap-Workflows bleiben die Hosted-PR-Checks maßgeblich.

## Bekannte Einschränkungen

Diese Änderung erfindet oder veröffentlicht keine unveröffentlichte
NGINX-Version und mergt zukünftige NGINX-Updates nicht automatisch. Ein
zukünftiges offizielles NGINX-Release benötigt weiterhin eine eigene geprüfte
NGINX-Änderung und die Validierung des geschützten Brokers.

## Security-Auswirkung

Der allgemeine Submodule-Publisher verliert vollständig die Möglichkeit,
NGINX-Pins einschließlich Workflow-Dateien abzuleiten oder zu schreiben. Es
werden weder ein breiterer Token-Scope noch veränderliche Reusable-Workflow-
Referenzen, Auto-Merge oder PR-kontrollierte Root-Ausführung eingeführt. Die
unveränderliche geschützte Root-Broker-Grenze bleibt bestehen.

## Verbleibende Risiken

Ein zukünftiger NGINX-spezifischer Updater muss einen offiziellen Release-Tag,
das exakte Release-Asset und den SHA-256 unabhängig verifizieren, bevor er
einen Broker-Repin vorschlägt. Das Framework-Repository kann weiterhin
NGINX-Metadaten enthalten; dieser Parent-Updater behandelt sie als ungenutzte
Daten.

## Nicht ausgeführte Prüfungen mit Begründung

Merge, Protected-master-Ausführung und Post-Merge-NGINX-Lifecycle-Evidence
können vor der geprüften Integration nicht behauptet werden. Sie bleiben
Branch-Protection- und Protected-Workflow-Gates.

## Finaler Diff- und Review-Status

Der Ersatz-Pull-Request bleibt Draft. Der finale Branch wird auf einen Commit
direkt auf der angegebenen Basis-Revision umgeschrieben, enthält keinen
temporären Bootstrap-Workflow und ändert die vorhandenen NGINX-`1.31.3`-Pins
nicht.
