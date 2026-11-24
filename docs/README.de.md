# Dokumentation

**Sprache:** [English](README.md) | Deutsch

## Erste Schritte

Den Checkout nach dem [Einstieg](getting-started.de.md) initialisieren und die
ersten Prüfungen ausführen. Vor einem Update die [Migration](migration.de.md)
lesen, insbesondere bei Konfigurationen mit Connector-Optionen für Body-Größen.

## Dokumentation nach Aufgabe finden

| Aufgabe | Anleitung |
| --- | --- |
| Host und Topologie wählen | [Connector-Profile](connectors/README.de.md) und [Beispielbundles](../examples/README.de.md) |
| Toolchain vorbereiten und bauen | [Build-Guide](build/README.de.md), [Compiler-Guides](build/compilers/README.de.md), [Versions-Pins](reference/version-pins.de.md) |
| Host oder Regeln konfigurieren | [Konfiguration](configuration.de.md) und [Variablenreferenz](reference/variables.de.md) |
| Body-Limits und Phase-4-Modus wählen | [Zuständigkeit für Body-Limits](phase4-mode-budget.de.md) und [Inspection-Grenzen je Profil](body-inspection-review-matrix.de.md) |
| Datenfluss verstehen | [Architektur](architecture.de.md) und [Repository-Konzept](repository-concept.de.md) |
| Connector betreiben | [Betrieb und Sicherheit](operations-and-security.de.md) und [Schwachstellen melden](../SECURITY.de.md) |
| An CI oder Analyse arbeiten | [CI-Einstiegspunkte](../ci/README.de.md), [Sicherheitswerkzeuge](security/ci-security-tooling.de.md), [SonarQube-Analyse](sonarqube-analysis.de.md) und [NGINX-Root-Broker](security/trusted-nginx-root-broker.de.md) |
| Änderung oder externe Quelle nachvollziehen | [Nachvollziehbarkeit](change-traceability.de.md) und [Herkunfts- und Lizenzreferenzen](../licenses/README.de.md) |
| Begriff nachschlagen | [Glossar](reference/glossary.de.md) |

## Connector-Guides

Der [Connector-Index](connectors/README.de.md) nennt alle zehn Profile und
verlinkt ihre hostspezifischen Voraussetzungen. Beim Anpassen eines
[Beispielbundles](../examples/README.de.md) den passenden Guide verwenden.

## Beispiele, Tests und Nachweise

[Tests und Nachweise](testing-and-evidence.de.md) erklärt die aktive Testauswahl
und die Aussagekraft jeder Prüfung. Unter [Reports](../reports/README.de.md)
liegen aufgezeichnete Laufzeitprüfungen und historische Nachweise.

## Zuständigkeit für Dokumentation

Englische und deutsche Begleitdateien gemeinsam pflegen.
`make check-bilingual-docs` und `make check-doc-links` ausführen.
Compiler-Guides und generierte Referenzen über ihre Quellen und Generatoren aktualisieren.
