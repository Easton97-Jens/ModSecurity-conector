# Change Record: Vertrag für die neueste stabile Go-Release

**Sprache:** [English](CR-20260912-go-latest-release-contract.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260912-go-latest-release-contract |
| Datum (UTC) | 2026-09-12 |
| Basis-Revision | `3c3908dbb3a87a18d823ab8f1a286ba5b9c00e94` |
| Delivery-Status | Parent-PR #365 enthält diesen gekoppelten Record. Branch, exakter Head, Hosted-Checks, Reviews, Ready-Status und jedes Merge-Ergebnis sind Delivery-Lifecycle-Fakten, die erst nach Beobachtung behauptet werden; dieser Record selbst autorisiert oder behauptet keinen Merge. |

## Motivation und Problemstellung

In der Basisrevision war der eingecheckte Selector `1.27.0` bereits eine
exakte stabile Go-Release, aber Go-Updater, Source-Vertrag und der
Trusted-Base-Selector von CodeQL akzeptierten weiterhin nur die Serie
`1.26.N`. Der Updater hätte daher eine veraltete Serie gewählt, und die
CodeQL-Go-Jobs hätten den eingecheckten Selector vor der Analyse abgewiesen.
Dies wird als `FND-PARENT-1085` verfolgt.

PR #363 wird nur als Kontext geprüft: Er aktualisiert Submodule-Pointer und
enthält diese Parent-eigene Go-Updater-Korrektur nicht. Diese Änderung
modifiziert weder Framework- oder MRTS-Source, Gitlinks,
Modul-Sprachbaselines, Workflow-Berechtigungen, Action-Pins,
Dependency-Locks noch Repository-Merge-Einstellungen; sie schreibt nie direkt
nach `master`.

## Akzeptanzkriterien

- Der Updater akzeptiert exakte stabile numerische `MAJOR.MINOR.PATCH`-
  Releases, weist fehlerhafte, Prerelease- und nicht stabile Metadaten zurück
  und löst die höchste stabile numerische Release ohne feste Go-Minor-Serien-
  Annahme auf.
- Der eingecheckte Go-Vertrag und der Trusted-Base-CodeQL-Selector akzeptieren
  dieselbe exakte numerische Release-Grammatik und behalten fail-closed-
  Validierung sowie das gepinnte Trusted-Base-Checkout-Verhalten bei.
- Der planmäßige Updater trennt Read-only-Auflösung, Read-only-Validierung und
  eng begrenzte Veröffentlichung unter den umbenannten release-orientierten
  Jobs.
- Fokussierte Updater-, Contract-, Workflow-Security-, Python-Contract- und
  zweisprachige Dokumentationsprüfungen liefern aufgezeichnete lokale Evidence;
  nicht verfügbare Hosted- und lokal inkompatible Go-Modul-Prüfungen bleiben
  ausdrücklich begrenzt.
- Englische und deutsche Dokumentation sowie dieser gekoppelte Change Record
  beschreiben denselben aktuellen Selector und die release-orientierte
  Workflow-Struktur.

## Implementierungsentscheidung und Begründung

- Die höchste stabile numerische Release wird nur bei der begrenzten
  planmäßigen oder manuell ausgelösten Auflösung des Updaters bestimmt.
  Pull-Request-CodeQL verwendet den eingecheckten Trusted-Base-Selector statt
  bei jeder Analyse Live-Release-Metadaten abzufragen. Das bewahrt
  Reproduzierbarkeit und vermeidet eine neue externe Trust-Abhängigkeit.
- Der Python-Parser und die Checker-Grammatik werden auf positive Major-
  Versionen mit kanonischen Minor- und Patch-Komponenten generalisiert.
  Tupelordnung liefert explizite Monotonie über künftige Go-Release-Serien.
- Die Updater-Stufen heißen `resolve-go-release`, `validate-go-release` und
  `create-go-update-pr`; die Read-only-Grenze von Resolver/Validator und die
  eingeschränkte Publisher-Grenze bleiben erhalten. Der Publisher bleibt auf
  `.go-version` und das feste, unabhängig validierte Envoy-Komponenten-Bundle
  begrenzt.
- Modul-`go`- und `toolchain`-Direktiven bleiben unabhängig: Sie sind
  Modul-Kompatibilitätsverträge, nicht der Repository-CI-Toolchain-Selector.

## Security-Auswirkung

Die Korrektur stellt die Verfügbarkeit des Trusted-Selectors für die
CodeQL-Go-Analyse wieder her, ohne dessen Input-Validierung, Action-Pins,
Berechtigungen, Trusted-Base-Checkout oder die
`check-latest: false`-Reproduzierbarkeitskontrolle zu lockern. Der Updater
weist weiterhin Redirects, fehlerhafte oder zu große Metadaten, unerwartete
Versionsänderungen, unsichere Dateiziele und nicht erlaubte
Komponentenänderungen zurück. Eine source-only-Frage zum Verhalten von
`GOTOOLCHAIN=local` bleibt bis zu Hosted-Ausführungsevidence zurückgestellt;
diese Änderung lockert die Kontrolle nicht und behauptet kein Hosted-Ergebnis.

## Geänderte Dateien

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/update-go-version.yml`
- `ci/checks/common/check-go-version-contract.py`
- `ci/checks/common/check-python-version-contract.py`
- `scripts/update-go-version.py`
- `scripts/version_updater_common.py`
- fokussierte Updater-, Go-Contract- und CI-Security-Workflow-Tests
- gekoppelte englische/deutsche Build- und CI-Security-Dokumentation
- dieser gekoppelte Change Record und die Change-Record-Indizes

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Baseline-Go-Vertrag bei `3c3908dbb3a87a18d823ab8f1a286ba5b9c00e94` | wie erwartet fehlgeschlagen: Der alte Checker wies den eingecheckten Selector `1.27.0` zurück; im Task-Run-Evidence erhalten. |
| Live-Updater-Check | bestanden: Der offizielle Endpoint lieferte `current_version=latest_version=1.27.1`, `status=current` und `update_available=false`. |
| Fokussierte Updater-, Go-Contract-, Workflow-Security-, Python-Contract- und zweisprachige Unit-Suite | bestanden: 91 Tests. |
| Begrenzte Komponenten-Regressionssuite | bestanden: 15 Tests. |
| `make check-go-version-contract` und `make check-ci-security-contract` | bestanden; der CI-Security-Contract führte 125 Tests mit fünf dokumentierten Environment-Capability-Skips aus. |
| `actionlint` und Offline-`zizmor` für die geänderten Workflows | bestanden; zizmor meldete keine Befunde. |
| Workflow-äquivalente Go-Modulmatrix | bestanden für Envoy ext_proc und die drei Traefik-Module mit `GOTOOLCHAIN=local`, `GOWORK=off` und Task-eigenen externen Caches. |
| `make check-bilingual-docs` | nur durch vorbestehende fehlende Framework-Gitlink-Linkziele im bewusst nicht initialisierten Task-Worktree blockiert; kein Task-eigener Paardokument- oder Change-Record-Fehler blieb. |
| `make check-python-version-contract` | durch vorbestehende ungelistete/fehlerhafte Python-Shell-Workflow-Inventarverstöße außerhalb dieser Aufgabe blockiert; seine dedizierte Unit-Suite bestand. |
| Frisches Post-Patch-Sicherheitsreview | bestanden: kein plausibler neuer Security-Befund im begrenzten Diff. |

## Runtime-Evidence

Dieser statische Source-Record behauptet keinen bestimmten Hosted-Workflow,
keine CodeQL-Analyse, keine SonarQube-Cloud-Analyse, keine Runtime-Connector-
Matrix, keinen exakten PR-Head, kein Review und kein Merge-Ergebnis. Die lokale
Go-Executable ist `1.27.1` und entspricht dem gewählten CI-Selector; die vier
workflow-äquivalenten Go-Modulvalidierungen bestanden mit
`GOTOOLCHAIN=local` und `GOWORK=off` in Task-eigenen externen Caches.
Dieses lokale Ergebnis ersetzt keine Delivery-Evidence, die an den aktuellen
exakten PR-Head gebunden ist.

## Bekannte Einschränkungen

Die lokale Python-Executable ist `3.14.4` und liegt unter dem eingecheckten
`.python-version`-Selector `3.14.7`; die Go-Modul-Matrix nutzte dennoch die
passende lokale Go-`1.27.1`-Toolchain. Die eingecheckte Dokumentations-Link-
Inventur enthält außerdem Framework-Ziele, die im bewusst nicht initialisierten
Task-Worktree fehlen. Framework/MRTS-Initialisierung oder -Modifikation ist
nicht autorisiert.

## Verbleibende Risiken

`FND-PARENT-1085` wird nicht allein durch Source-Edits geschlossen. Sein
ursprünglicher Source-Fehler darf nicht mehr reproduzierbar sein, und der
aktuelle exakte PR-Head benötigt seine anwendbaren Hosted-Controls vor einer
verifizierten Integrationsbehauptung. Jeder fehlgeschlagene Hosted-Control muss
als neue Evidence triagiert werden. Ein Merge verlangt eine gesonderte
aktuelle Benutzerautorisierung und Exact-Head-Evidence; dieser statische
Source-Record liefert weder diese Autorisierung noch behauptet er ein späteres
Merge-Ergebnis.

## Nicht ausgeführte Prüfungen mit Begründung

Die Source-Validierungssuite ersetzt weder die CodeQL-Go-Analyse noch
anwendbare Hosted-PR-Controls. Diese Controls werden während des
Delivery-Lifecycles gegen den aktuellen exakten PR-Head geprüft; dieser
statische Record klassifiziert kein geplantes oder späteres Delivery-Ergebnis
als bestanden.

## Finaler Diff- und Review-Status

Die fokussierten lokalen Prüfungen und das frische Post-Patch-Sicherheitsreview
sind vollständig. Der finale Source-Diff-Readback ist vollständig.
Delivery-Branch-, PR-, Exact-Head-, Hosted-Check-, Review- und Merge-Fakten
werden erst nach Beobachtung im Delivery-Lifecycle festgehalten; dieser
Source-Record behauptet sie nicht vorweg.
