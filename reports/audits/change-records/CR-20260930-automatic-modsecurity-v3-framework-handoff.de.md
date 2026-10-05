# Change Record: automatische ModSecurity-v3-Framework-Übergabe

**Sprache:** [English](CR-20260930-automatic-modsecurity-v3-framework-handoff.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-automatic-modsecurity-v3-framework-handoff |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `d75d36d6118714e6d92c3e498c500783c3fd028e` |

## Motivation und Problemstellung

GitHub-Actions-Lauf 36728825605 löste den Framework-Kandidaten `bc8217d325809b9aba9a1d8c16964d71a01933ee` auf, die Validierung stoppte jedoch, weil dieser Kandidat den offiziellen ModSecurity-v3-Pin von v3.0.16 auf v3.0.17 anhebt. Der bisherige Strukturhash deckte absichtlich jede ModSecurity-Zuweisung ab, sodass der Submodule-Updater ein geprüftes stabiles ModSecurity-Wartungstupel nicht über seinen normalen begrenzten Projektionspfad mitziehen konnte.

## Akzeptanzkriterien

Nur das offizielle ModSecurity-v3-Repository, einen stabilen `v3.x.y`-Tag und einen exakten kleingeschriebenen SHA-1-Commit als registrierte Framework-Quelldaten beweglich machen. Ausschließlich die zwei Dokumentations-Kommando-Konstanten projizieren, die dieses Tupel konsumieren, die vorhandenen Compiler-Guides im Publisher neu erzeugen, die geschlossene Update-Pfad-Allowlist erhalten und NGINX sowie jedes andere ModSecurity-Feld strukturell geprüft lassen. Automatischer Merge bleibt deaktiviert.

## Implementierungsentscheidung und Begründung

Die bestehende geschlossene Quellregistry wird exakt um `MODSECURITY_V3_APPROVED_REPO_URL`, `MODSECURITY_V3_APPROVED_COMMIT` und `MODSECURITY_V3_RELEASE_TAG` erweitert. Der Repository-Wert bleibt fest auf das offizielle OWASP-ModSecurity-Repository gebunden, der Release ist auf stabile v3-Tags beschränkt und der Commit muss aus vierzig kleingeschriebenen Hexadezimalzeichen bestehen. Der Verifier normalisiert beim geprüften Framework-Strukturhash nur genau diese drei Zuweisungen.

Der Compiler-Guide-Generator und seine Regression-Fixture stellen zwei explizite verwaltete Kommando-Konstanten bereit. Der Synchronisierer darf nur diese Konstanten aktualisieren; anschließend erzeugt der vorhandene Generator die zweisprachige Dokumentation. Publisher-Allowlist und Raw-Diff-Gate registrieren die beiden Quelldateien explizit statt ein Verzeichnis oder Wildcard freizugeben.

## Geänderte Dateien

Framework-Quelldaten-Synchronisierer und Candidate-Verifier; Reviewed-Version-Handoff-Checker; Compiler-Guide-Generator und Tests; Submodule-Update-Workflow und dessen Security-Contract-Tests; fokussierte Synchronisierer-/Verifier-Regressionen; sowie dieses zweisprachige Change Record.

## Ausgeführte Befehle

Repository-Zustand, fehlgeschlagene Actions-Logs und der exakte Framework-Candidate-Commit wurden über die GitHub-Verbindung geprüft. Die Implementierung wird als Draft Pull Request ausgeliefert, damit die Repository-native CI den vollständig konfigurierten Test- und Security-Workflow-Satz auf dem finalen Head ausführen kann. In diesem Record wird kein ausstehender Hosted-Check als bestanden bezeichnet.

## Security-Auswirkung

Die Änderung sourced oder führt Candidate-`common.sh` nicht aus. Sie akzeptiert weder beliebige `MODSECURITY_*`-Namen noch veränderliche Repositories, Moving Branches, NGINX-Pins, Shell-Ausdrücke, neue Schreibverzeichnisse oder breitere Workflow-Rechte. Bestehende Pfad-, Raw-Diff-, Candidate-Lineage-, Read-only-Namespace-, App-Token- und No-Auto-Merge-Kontrollen bleiben erhalten.

## Runtime-Evidence

Die Änderung ermöglicht einem Wartungstupel, die bestehenden Runtime-Validierungsgates zu erreichen; sie zertifiziert selbst weder ABI noch WAF-Verhalten oder Connector-Kompatibilität von ModSecurity v3.0.17. Solche Claims benötigen die vorhandenen Hosted-/Runtime-Checks des Repositorys für den erzeugten Candidate-PR.

## Bekannte Einschränkungen

Automatisiert wird nur das aktuelle offizielle ModSecurity-v3-Provenance-Tupel. Ein zukünftiger Major-Release, Repository-Wechsel, anderes Pin-Format oder zusätzliches Framework-ModSecurity-Feld bleibt fail-closed und verlangt eine separate Prüfung.

## Verbleibende Risiken

Auch ein syntaktisch gültiger Upstream-Wartungsrelease kann API-, ABI-, Build-, Dependency- oder Verhaltensänderungen enthalten. Der Updater erzeugt deshalb weiterhin einen Draft PR und verlässt sich auf die bestehenden Candidate- und Runtime-Gates statt automatisch zu mergen.

## Nicht ausgeführte Prüfungen mit Begründung

Vor Erstellung des Draft-PR werden keine Hosted-Final-Head-Checks als bestanden berichtet. Es wird nicht allein daraus abgeleitet, dass v3.0.17 native Connector-Runtime-Validierung besteht, weil Tag und Commit den begrenzten Quelldatenvertrag erfüllen.

## Finaler Diff- und Review-Status

Als Draft PR gegen `master` ausliefern. Exakten finalen Diff und Hosted-Checks vor jedem Merge prüfen. Kein direkter Master-Schreibvorgang und kein automatischer Merge sind autorisiert.
