# Berichte

**Sprache:** [English](README.md) | Deutsch

Berichte sind nach ihrer Evidence-Rolle organisiert. Sie ersetzen nicht die
lauflokalen Artefakte, aus denen ein Claim validiert wurde.

| Bereich | Inhalt | Source of Truth |
| --- | --- | --- |
| [`current/`](current/) | Aktuelle manuell gepflegte Sechs-Connector-Status- und Readiness-Berichte | Aktueller ausgewählter HTTP/1.1-Kern und seine verlinkte Evidence-Grenze |
| [`audits/`](audits/) | Vertrags-, Runtime-Root-, Promotion-, Transport- und Organisationsaudits | Benannte Audit-Eingaben und Datum |
| [`evidence/`](evidence/) | Lesbare Zusammenfassungen ausgewählter No-CRS-Evidence | Kanonische Result-/Event-Artefakte, nicht rohe lokale Läufe |
| [`archive/`](archive/README.de.md) | Ersetzte Planung, Readiness und historische Analysen | Banner am Beginn jedes Berichts |
| [`testing/`](testing/) | Bestehender detaillierter Testing-Index und Generated-Report-Layout | Generator-Registry und Framework-Quellen |

`testing/generated/` bleibt der etablierte Ort für generierte Berichte, weil
Report-Registry, Pfadsicherheitsprüfungen und Generatoren ihn als Vertrag
verwenden. Mit `make refresh-all-reports` neu erzeugen; Generated-Markdown nie
manuell bearbeiten.

## Portable Pfadangaben

Versionierte Berichte hängen nie von der Verzeichnisstruktur einer bestimmten
Workstation ab. Wenn ein aufbewahrter Nachweis einen Runtime-Ort benennen muss,
nutzt er eine der folgenden reinen Anzeigeangaben; Run-ID, Hashes und
Repository-relative Artefaktnamen bleiben der Provenance-Vertrag.

| Referenz | Bedeutung |
| --- | --- |
| `<repository-root>` | Der Checkout, der diesen Bericht enthält. |
| `<verified-run-root>` | Konfigurierter Root eines verifizierten Runtime-Laufs; enthält `build/`, Logs und den Komponenten-Cache dieses Laufs. |
| `BUILD_ROOT:<relative-path>` | Ein Pfad unter der konfigurierten Umgebungsvariablen `BUILD_ROOT`. |
| `<historical-run-root:run-id>` | Aufbewahrter historischer Workspace mit der Kennung `run-id`; kein Pfad, den Leser nachbilden sollen. |
| `<local-state-root>` | Nichtvertraglicher, entwicklerlokaler Zustand, der nur in historischen Evidence-Beschreibungen erhalten bleibt. |
| `<temporary-work-root>` | Wegwerfbarer temporärer Workspace während eines Befehls oder Vergleichs. |
| `<local-home-root>` | Home-Verzeichnis-relativer Ort, dessen konkreter Benutzer- oder Hostpfad absichtlich ausgelassen wird. |
| `<external-source-root>` | Extern bereitgestellter Source-Checkout, nie ein erforderlicher Ort dieses Repositorys. |

Das Phase-1-Organisationsinventar und der Plan bleiben am Berichts-Root:
[Inventar](repository-organization-inventory.json) und
[Plan](repository-organization-plan.de.md). Sie dokumentieren den Vor-Move-
Stand und sind keine aktuelle Runtime-Evidence.
