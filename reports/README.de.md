# Berichte

**Sprache:** [English](README.md) | Deutsch

Berichte sind nach ihrer aktuellen Evidence-Rolle organisiert. Sie ersetzen
nicht die lauflokalen Artefakte, aus denen ein Claim validiert wurde.

| Bereich | Kanonische Quelle | Zweck |
| --- | --- | --- |
| Aktuelle Kern-Evidence | [current/core-completion.de.md](current/core-completion.de.md) | Abgegrenzte ausgewählte Sechs-Connector-HTTP/1.1-Kern-Evidence. |
| Aktuelle Readiness | [current/readiness.de.md](current/readiness.de.md) | Aktueller Status, Grenzen und bewusst nicht erhobene Claims. |
| Architektur- und Evidence-Audit | [audits/architecture-and-evidence.de.md](audits/architecture-and-evidence.de.md) | Konsolidierter Architektur-, Runtime-Root-, Transport- und Evidence-Vertrag. |
| Change Records | [audits/change-records/README.de.md](audits/change-records/README.de.md) | Versionierte, manuell gepflegte Records für nicht triviale Änderungen. |
| Konfigurationsinventar | [connector-configuration-inventory.json](connector-configuration-inventory.json) | Generiertes quellenbasiertes Inventar für Connector-, Common-Runtime- und Engine-Optionen. |
| Testing- und Generated-Berichte | [testing/README.de.md](testing/README.de.md) | Generatorverwaltete Runtime-, Coverage-, Cache- und Evidence-Berichte. |

`testing/generated/` bleibt der etablierte Ort für Generated Reports, weil
Report-Registry, Pfadsicherheitschecks und Generatoren ihn als Source-Vertrag
verwenden. Mit `make refresh-all-reports` neu erzeugen; Generated Markdown
nicht manuell bearbeiten. Das Refresh-Manifest ist der kanonische Katalog der
Generated Reports; getrennte Dependency-, Lineage-, Path-Migration-, Roadmap-
und Generator-Summary-Ansichten werden bewusst nicht aufbewahrt.

Konfigurationsinventar und die zugehörigen Beispielreferenzen mit
`make generate-connector-config-reference` neu erzeugen; Source-/
Dokumentationsparität mit `make check-connector-config-reference` prüfen.

## Portable Pfadangaben

Versionierte Berichte hängen nie von der Verzeichnisstruktur einer bestimmten
Workstation ab. Wenn ein aufbewahrter Nachweis einen Runtime-Ort benennen muss,
nutzt er eine der folgenden reinen Anzeigeangaben; Run-ID, Hashes und
repository-relative Artefaktnamen bleiben der Provenance-Vertrag.

| Referenz | Bedeutung |
| --- | --- |
| `<repository-root>` | Der Checkout, der diesen Bericht enthält. |
| `<verified-run-root>` | Konfigurierter Root eines verifizierten Runtime-Laufs; enthält `build/`, Logs und den Komponenten-Cache für diesen Lauf. |
| `BUILD_ROOT:<relative-path>` | Ein Pfad unter der konfigurierten Umgebungsvariablen `BUILD_ROOT`. |
| `<historical-run-root:run-id>` | Aufbewahrter historischer Workspace mit der Kennung `run-id`; kein Pfad, den Leser nachbilden sollen. |
| `<local-state-root>` | Nichtvertraglicher, entwicklerlokaler Zustand, der nur in historischen Evidence-Beschreibungen erhalten bleibt. |
| `<temporary-work-root>` | Wegwerfbarer temporärer Workspace während eines Befehls oder Vergleichs. |
| `<local-home-root>` | Home-Verzeichnis-relativer Ort, dessen konkreter Benutzer- oder Hostpfad absichtlich ausgelassen wird. |
| `<external-source-root>` | Extern bereitgestellter Source-Checkout, nie ein erforderlicher Ort dieses Repositorys. |
