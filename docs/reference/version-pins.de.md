# Projekt-Versionspins

**Sprache:** [English](version-pins.md) | Deutsch

## Kanonische Parent-Konfiguration

Gewöhnliche Parent-Revisions- und Toolchain-Auswahl wird in
[`ci/tooling/project-versions.lock.json`](../../ci/tooling/project-versions.lock.json)
gepflegt. Das geschlossene Schema hat genau fünf Schlüssel:

| Schlüssel | Bedeutung |
| --- | --- |
| `schema_version` | Ganzzahliger Schema-Bezeichner |
| `framework_sha` | Exakte gewöhnliche Framework-Revision |
| `mrts_sha` | Exakte verschachtelte MRTS-Revision |
| `python_version` | Stabile Python-3.14-Patch-Toolchain |
| `go_version` | Stabile Go-Toolchain |

Die ausgewählten Werte werden direkt aus dem verlinkten JSON-Datensatz gelesen;
diese Referenz pflegt keine weitere Kopie davon.
[`.python-version`](../../.python-version) und
[`.go-version`](../../.go-version) sind generierte Ansichten für Setup-Actions
und bestehende Consumer. Sie werden nicht als unabhängige Konfiguration gepflegt.
Jedes Go-Modul behält seine getrennte Kompatibilitätsuntergrenze in `go.mod`;
diese Untergrenze und die ausgewählte Build-Toolchain erfüllen verschiedene Zwecke.

## Revisionsprovenienz

Der gewöhnliche Workflow-Reader validiert begrenztes, ausschließlich als Daten
behandeltes JSON und weist doppelte/unbekannte Schlüssel, ungültige oder
Nicht-ASCII-Werte und symlinkbasierte Eingaben zurück. Er verlangt unabhängig,
dass die Lock-Bytes dem regulären Git-Blob des exakten Parent-Commits entsprechen,
der Framework-Gitlink des Parents zu `framework_sha` passt und der MRTS-Gitlink
des Frameworks zu `mrts_sha` passt. Initialisierte, unabhängige Framework-/MRTS-
Repositorys müssen genau diese materialisierten HEADs besitzen. Git-Replacement-
Objekte sind bei Provenienzprüfungen deaktiviert. Die Änderung eines Lock-Felds
allein kann keinen widersprüchlichen Gitlink oder Checkout überschreiben.

Der geschützte NGINX-Root-Broker behält sein getrenntes geprüftes unveränderliches
Broker-/Framework-Tupel in seinem dedizierten Caller-Vertrag. Gewöhnliche Lock-Änderungen aktivieren
oder pinnen diesen privilegierten Caller nicht neu. Siehe den
[Broker-Vertrag](../security/trusted-nginx-root-broker.de.md).

## Zuständigkeit für Komponenten und Sicherheitswerkzeuge

Komponentenversionen, offizielle Quell-URLs, Prüfsummen und genehmigte Release-
Tupel bleiben kanonisch in der
[`ci/lib/common.sh`](../../modules/ModSecurity-test-Framework/ci/lib/common.sh)
des ausgewählten Frameworks. Die Parent-Lockdatei wählt diese vollständige
unveränderliche Framework-Quelle aus; sie kopiert nicht jede Komponentendefinition
in eine zweite Autorität. Framework-Komponentenupdates gehören zu diesem
Repository. Der geprüfte Parent-Submodul-Updater wählt anschließend den neuen
Framework-Gitlink samt Lock und synchronisiert seine expliziten Parent-
Projektionen. Keine MRTS-Quelländerung folgt implizit.

Action-Pins und Release-/Digest-Einträge für Sicherheitswerkzeuge bleiben in der
getrennten
[`ci/tooling/security-tools.lock.yml`](../../ci/tooling/security-tools.lock.yml)
unter ihrem eingeschränkten Workflow-/Tool-Updater. Dedizierte geschützte Release-
Verträge behalten ihre eigene Review-Grenze. Die Zentralisierung gewöhnlicher
Auswahl vereint diese Autoritäten nicht und erweitert keine Publisher-
Schreibberechtigungen.

## Aktualisieren und prüfen

Nach einer autorisierten Toolchain-Auswahländerung in der JSON-Lockdatei werden
ihre beiden Ansichten mit den Repository-eigenen Zielen neu erzeugt und geprüft:

```sh
make sync-project-versions
make check-project-versions
```

Lokale Arbeitsvereinbarungen können einen Ausführungswrapper um diese nativen
Befehlspayloads verlangen. `ci/tools/sync-project-versions.py --sync` und `--check`
implementieren diese Ziele. `--check` meldet Drift und scheitert, statt ihn still
zu reparieren. Die exakte committete Revisionsprovenienz ist eine eigene Prüfung:
Der gewöhnliche Workflow-Reader führt nach dem Materialisieren der ausgewählten
Repositorys
`ci/tools/read-framework-revisions.py --parent-sha <exact-parent-sha>` aus.

Die Python- und Go-Updater ändern nur ihr eigenes Lock-Feld und die zugehörige
Ansicht; sie erhalten bestehende Metadaten-, monotone Versions- und
Veröffentlichungsschutzbedingungen. Der Go-Updater darf außerdem sein getrennt
begrenztes Envoy-Modul-Bundle synchronisieren. Publisher-Schutzbedingungen prüfen
den Feldumfang der zentralen Lockdatei für bestehende Branches und neue
Kandidaten. Der Framework-Updater ändert die genehmigte gewöhnliche Framework-
Auswahl und ihre registrierten Projektionen und erhält Toolchain-/MRTS-Felder.

Writer teilen einen `flock` auf dem Verzeichnis `ci/tooling`, prüfen Dateiidentität
und Inhalt vor dem Ersetzen und erfassen Ersetzungen vor dem Directory-fsync,
damit sie einen betrieblichen Fehler sicher zurückrollen können. Rollback erhält
unabhängige gleichzeitige Änderungen. Einzelne Dateiersetzungen machen eine
Transaktion über mehrere Dateien nicht crash-atomar; ein Crash kann erkennbaren
Ansichtsdrift hinterlassen. Vor der Veröffentlichung die Prüfungen wiederholen
und ausschließlich Task-eigenen Drift reparieren.

## Evidence-Grenzen

Eine synchronisierte Ansicht, Provenienzprüfung oder bestandene Unit-Prüfung
belegt ihre eigene Ebene. Echte Connector-Runtime- und Sonar-Ergebnisse müssen
an den ausgelieferten exakten Head gebunden sein. Framework-, Parent- und MRTS-
Auslieferung bleiben getrennt; eine Parent-Revisionsänderung mergt weder einen
Framework-PR noch autorisiert sie eine privilegierte Broker-Aktivierung.
