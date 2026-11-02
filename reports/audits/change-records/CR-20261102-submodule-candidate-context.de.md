# Change Record: CR-20261102-submodule-candidate-context

**Sprache:** [English](CR-20261102-submodule-candidate-context.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261102-submodule-candidate-context |
| Datum (UTC) | 2026-11-02 |
| Basis-Revision | `a18ffca3b5bb54887c0b8859ece95478e83cf262` |

## Motivation und Problemstellung

Run 41495088844 / Job 125448091161 checkte Framework-Kandidat `1b0885a2aa9b91b3faad76de6df8250bf8147eef` aus, behielt jedoch die alte `FRAMEWORK_REVISION`. Die Workflow-Expansion löste `ContextError` aus. Der Publisher hatte nach dem Umschreiben der Parent-Pins die umgekehrte Inkonsistenz. Korrekte Quellauswahl zeigte anschließend NGINX 1.31.8 im Kandidaten gegen veraltete Action-/Producer-Projektionen für 1.31.6. Der Nutzer wählte die Reparatur dieses Versionskonflikts ausdrücklich aus.

## Akzeptanzkriterien

Alte/neue Parent-Pins unabhängig von Framework-Checkout/-Kontext prüfen; falsche Pins und fehlende Blobs ablehnen; nur den vertrauenswürdigen Parser des committeten Parent ausführen. Gewöhnliche NGINX-Übergaben an das kanonische 1.31.8-Tupel angleichen und den historischen geschützten 1.31.4-Brokervertrag erhalten. Separate Framework- und Parent-Draft-PRs ohne Merge liefern.

## Implementierungsentscheidung und Begründung

Begrenzte reguläre UTF-8-Git-Blobs aus der validierten Parent-Lock-Revision lesen. Parsercode getrennt aus dem Framework-Gitlink von committetem Parent HEAD beziehen und dessen geschlossenen Schema-Expander mit Git-Datenleser wiederverwenden. Updater-Prüfer mit isoliertem Python (`-I`) ausführen; bestehende geprüfte PyYAML-Abhängigkeit im separaten Publisherjob vor App-Zugangsdaten bereitstellen. Migrierte Producer bleiben Framework-eigen. Komponenten-/Voll-SHA-Verweise mit dem bestehenden Parent-Tool synchronisieren und Compiler-Anleitungen aus Quellen regenerieren. Framework-Abhängigkeit: [PR #165](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/165).

## Geänderte Dateien

Updater/Prüfer, direktes Full-Smoke-NGINX-Tupel, Framework-Gitlink, registrierte Komponenten-/Workflow-Pins, generierte EN/DE-Compiler-Anleitungen für Envoy/HAProxy/NGINX, `ci/README.md` / `ci/README.de.md` und dieses Change-Record-Paar. Framework-Quellen/-Tests haben einen separaten Commit und PR. MRTS ist unverändert.

## Ausgeführte Befehle

Alle Befehle verwendeten RTK. Der taskeigene Launcher `with-context.py` hält explizite Connector-/Framework-Roots und HEADs, Profil `h1`, externe Ausgaben/TMPDIR und Python-User-Site-Isolation fest. Aufbewahrter Evidence-Root: `/var/tmp/codex/ModSecurity-conector/runs/fix-submodule-candidate-context`.

- Ursprünglicher Prüfer: gepinnte Kontrolle Exit 0; Kandidaten-Checkout mit altem Kontext reproduzierte den gemeldeten `ContextError`, Exit 1.
- Korrigierter `python -I ci/tools/verify-framework-candidate-contract.py` mit kompatiblen geprüften Common-Daten: Exit 0 trotz altem Kontext.
- Die vier `VerifyFrameworkCandidateGitContextTests` plus vier ausgewählte `VerifyFrameworkCandidateContractTests`: 8 bestanden. Kontrollen prüfen alte/neue Auswahl, nicht ausgeführtes Kandidaten-Python, Vorrang migrierter Quellen, falschen Wrapper-SHA, fehlenden Blob, veralteten Lock, NGINX-Abweichung und Provenienzanforderungen.
- `python -I ci/tools/sync-framework-component-versions.py --sync` und `--check` mit extrahierten Kandidaten-Common-Daten und exakt ausgewähltem SHA: bestanden; abschließende Prüfung meldet keine Änderungen.
- `python -I ci/tools/verify-framework-candidate-contract.py` gegen synchronisierte Pins: Exit 0, `release-1.31.8` verifiziert.
- `python scripts/generate_compiler_guides.py`: Exit 0.
- Aktive Inventarzulassung: 100 aktive Fälle / Grenze 100; der gesamte Katalog wurde nicht ausgeführt.
- Python-AST-Parsing und `git diff --check`: bestanden.

Ein erster Synchronisierungsversuch lehnte korrekt eine Common-Datei außerhalb des erlaubten temporären Roots ab; Extraktion in den taskeigenen Runner-Root löste das Setup.

Abschließende integrierte Validierung mit Framework 965797c84142813e2992971fdf2add9a56170d5a: 8 gezielte Tests bestanden. RTK-gekapselte make check-bilingual-docs, make check-doc-links und python ci/tools/new-change-record.py check bestanden. Automatischer Abgleich bestätigt für alle übrigen Workflow-Änderungen ausschließlich den registrierten Voll-SHA-Austausch.

## Security-Auswirkung

Keine schwächeren Prüfungen, Privilegien oder Provenienzanforderungen. Der isolierte Prüfer importiert kein Kandidaten-Python. Action-/Producer-Daten verwenden den ausgewählten Pin; Parsercode verwendet den committeten vertrauenswürdigen Pin. Fehlende, übergroße, Symlink-, Nicht-UTF-8- und inkonsistente Quellen werden abgelehnt. Framework-Quellzuordnung hat Vorrang vor lokalen Schattenkopien. Historische Broker-Quelltupel bleiben unverändert.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Git-Objekt-Vertragstests und Quellsynchronisierung belegen weder gehosteten NGINX-Verkehr noch Runtime-Unterstützung.

## Bekannte Einschränkungen

Framework und Parent benötigen getrennte PR-Reviews/-Integrationen. Der Updater-Publisher der geschützten Basis kann den reparierten Branch vor Integration nicht ausführen. Es wurden weder Merge noch Workflow-Dispatch mit Publisher-Zugangsdaten durchgeführt.

## Verbleibende Risiken

Die Datenlese-Schnittstelle des vertrauenswürdigen Framework-Expanders bleibt eine explizite Kompatibilitätsabhängigkeit, abgesichert durch echte Git-Objekt-Regressionsfixtures. Host-Runtime-Qualifikation bleibt von dieser begrenzten Wartungsreparatur getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Connector-/I12-Matrix oder gehostete NGINX-Runtime-Kampagne: außerhalb dieser begrenzten Reparatur. Lokale Prüfungen verwenden verfügbares Python 3.14; GitHub CI wählt den Python-3.15-Patchvertrag des Repositories. Aktuelle GitHub-Head-Prüfungen und Reviews werden separat in PR/Taskplan verfolgt; lokale Ergebnisse implizieren keinen CI- oder Sonar-Erfolg.

## Finaler Diff- und Review-Status

Unabhängiges Read-only-Review identifizierte und korrigierte den Vorrang lokaler Schattenkopien, NUL-Ablehnung und Publisher-Abhängigkeitsbereitstellung. Abschließende Integrations-/Dokumentationsergebnisse bleiben in Taskplan und PR erhalten. Der ursprüngliche Nutzercheckout bleibt unverändert; taskeigene externe Checkouts/Evidence werden aufbewahrt. Es wird keine Master-Änderung beansprucht.
