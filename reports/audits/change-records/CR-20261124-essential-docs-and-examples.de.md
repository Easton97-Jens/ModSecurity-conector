# Change Record: CR-20261124-essential-docs-and-examples

**Sprache:** [English](CR-20261124-essential-docs-and-examples.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261124-essential-docs-and-examples |
| Datum (UTC) | 2026-11-24 |
| Basis-Revision | `48c4672dc07458411288570515bb8357f1e9e581` |

## Motivation und Problemstellung

Wiederholte Einstiegsbefehle, Erklärungen zu Modi und Hinweise zur Validierung erschwerten das Auffinden der hostspezifischen Optionen und Befehle. Alte PR- und Analyseaufzeichnungen standen neben den aktuellen Anleitungen.

## Akzeptanzkriterien

Leser können jedes der zehn Profile auswählen, seine Konfigurationslayouts und Prüfanleitungen erreichen und die aktuellen Voraussetzungen in beiden Sprachen finden. Historische Aufzeichnungen bleiben erreichbar. Aktive Beispieldirektiven und generierte Referenzen behalten ihre bisherige Bedeutung.

## Implementierungsentscheidung und Begründung

Die Indizes für Dokumentation und Beispiele dienen zur Navigation. Der Einstieg erläutert die Einrichtung. Hostspezifische Voraussetzungen stehen bei den passenden Beispielen. Die Checkliste zu Response-Limits und zwei SonarQube-Aufzeichnungen zu PR #421 liegen im Audit-Archiv. Kurze Verweise bleiben an den bisherigen Pfaden. Die Envoy-Anleitung wählt die eingecheckte Vorlage explizit aus. Ein veralteter NGINX-Kommentar zur nativen Ereignisprotokollierung entfällt.

## Geänderte Dateien

- `docs/README{,.de}.md` und `docs/getting-started{,.de}.md`
- `examples/README{,.de}.md` und die sechs Host-README-Paare unter `examples/`
- Kommentare in `examples/nginx/safe/nginx.conf`
- `docs/response-limit-stack-checklist{,.de}.md` und `docs/sonarqube-pr421-{closeout,triage}{,.de}.md` mit ihren Inhalten unter `reports/audits/documentation-history/`
- Dieses Change-Record-Paar

## Ausgeführte Befehle

- `make check-bilingual-docs`, `make check-doc-links` und `make check-variable-documentation` bestanden für die bearbeiteten Anleitungen mit dem gepinnten Framework-Checkout und Python `3.15.2`.
- `git diff --check` bestand. Ein gezielter Vergleich bestätigte identische Layout-Links für alle zehn Profile und identische aktive NGINX-Direktiven gegenüber der Basis-Revision.
- Der Befehlsblock im Envoy-README lief mit einem temporären `BUILD_ROOT`. Er erzeugte lokale TLS-Dateien und renderte die gewählte Vorlage als einlesbares YAML.

## Security-Auswirkung

Die Änderung betrifft Dokumentation und Beispielkommentare. Die jeweiligen Anleitungen beschreiben weiterhin die Grenzen für Hosts, private Sockets, Zertifikate, Logs und Richtlinien. Die temporären TLS-Dateien dienten ausschließlich zur Vorbereitung der Konfiguration.

## Runtime-Evidence

Für das Envoy-Beispiel wurde die Erzeugung der Konfiguration geprüft. Das belegt ausschließlich die Verarbeitung der Vorlage und das Einlesen des YAML.

## Bekannte Einschränkungen

Die Linkprüfung des Repositorys deckt eingecheckte relative Links ab. Externe Ziele und historische Laufzeitaussagen behalten ihren ursprünglichen Geltungsbereich.

## Verbleibende Risiken

Verweise von außerhalb des Repositorys auf archivierte Abschnitte benötigen unter Umständen die entsprechende Archiv-URL.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese redaktionellen Änderungen wurden keine Connector-Hosts oder Lifecycle-Kampagnen gestartet. Das Framework-Beispielmodul ist archiviert und die Standard-Testzulassung lehnte den Aufruf ab. Der gezielte Vergleich und die Konfigurationserzeugung oben decken die geänderten Beispielinhalte ab.

## Finaler Diff- und Review-Status

Die Prüfung umfasst die englischen und deutschen Anleitungen, archivierte Aufzeichnungen, ihre Verweise und eine reine Kommentaränderung an einer Konfiguration. Veröffentlichung und CI sind im Pull Request nachvollziehbar.
