# Vorgeschlagene Master-Prüfungen

**Sprache:** [English](rules-review.md) | Deutsch

Status: vorgeschlagen, nicht angewendet. Administrative Änderungen benötigen eine gesonderte Benutzerfreigabe. Die lokale Sonar-Ausnahme ändert weder GitHub-Workflows noch allgemeine Regeln.

[Vorher-Snapshot](rules-before.json) und [Nachher-Vorlage](rules-after-proposal.json) enthalten die vollständigen sichtbaren Konfigurationen. [Connector-Anlagevorlage](connector-ruleset-create-proposal.json) und [Framework-Anlagevorlage](framework-ruleset-create-proposal.json) sind eigenständige API-Request-Bodys. Bestehende Rulesets bleiben unverändert, einschließlich Archivzweigen, strikten Prüfungen, Review-Vorgaben, Lösch-/Force-Push-Schutz und fehlenden Bypass-Akteuren. Pro Repository wird ausschließlich ein zusätzliches Master-Ruleset vorgeschlagen.

## Bestehende Schutzmaßnahmen

Connector-Ruleset 19138299 verlangt sechs Kontexte: actions, bounded-c-cpp, envoy-go, traefik-go, actionlint, zizmor. Framework-Ruleset 19700778 enthält keine required_status_checks-Regel. Klassische Branch-Protection-Abfragen liefern für beide Repositories HTTP 403 Resource not accessible by integration; zusätzliche klassische Vorgaben bleiben unbekannt. Dies ist eine Lesezugriffsgrenze und kein Nachweis fehlenden Schutzes.

Quellen: [Connector-Ruleset](https://api.github.com/repos/Easton97-Jens/ModSecurity-conector/rulesets/19138299), [Framework-Ruleset](https://api.github.com/repos/Easton97-Jens/ModSecurity-test-Framework/rulesets/19700778).

## Vorgeschlagene Pflichtprüfungen

Die zusätzliche Connector-Liste enthält 15 exakte Kontexte, die Framework-Liste 6, jeweils an GitHub-Actions-Integration 15368 gebunden. Zusammen mit bestehenden Regeln ergeben sich 21 sichtbare Connector-Kontexte. Die Quellenprüfung ergab kontinuierliche Master-PR-Ausführung ohne Pfad-/Fork-Jobausschlüsse für diese Kontexte. Maßgeblich sind GitHub-Prüfungen des aktuellen Heads; ein Anzeigename allein belegt weder Runtime noch Befundfreiheit.

| Repository | Zusätzliche Prüfungen |
| --- | --- |
| Connector | scaffold-lint; common-structure; apache-autotools-bootstrap; apache-structure; nginx-structure; nginx-exact-head; haproxy-structure; envoy-contract; lighttpd-contract; traefik-contract; quick-check; report-governance; protocol-contract; apr-util-provenance; pull-request-range |
| Framework | scaffold-lint; common-structure; CodeQL PR (actions); CodeQL PR (python); CodeQL PR (c-cpp); pull-request-range |

nginx-exact-head führt echte gehostete Functional-A-H1-Tests einschließlich Adapter-Provisionierung und nginx-hosted-Gruppe aus. Er unterscheidet sich von manuellen geschützten Broker-Jobs und qualifiziert H2/H3 nicht. Framework-CodeQL-PR-Jobs verwenden upload: never; ihre Verbindlichkeit sichert die Analyseausführung, nicht null Befunde. Alle ausgewählten Workflows haben kein merge_group; vor einer Merge-Queue ist erneut zu prüfen.

## Prüfungen mit weiterem Vorbereitungsbedarf

| Prüfungen | Grund für den Verbleib außerhalb dieser Vorlage |
| --- | --- |
| Framework actionlint-and-contract, zizmor, python-ci-security-quality, check-action-versions, portable-contract | PR-Pfadfilter verhindern universelle Ausführung; Filter entfernen und Dokumentations-PR-Ausführung vor Verbindlichkeit prüfen. Bestehende Wartungs-PRs werden nicht geändert. |
| Parent go-candidate-Varianten, nginx-b09-regression, fünfzelliger CRS-Aggregator | PR-Pfadfilter; echte Tests erhalten und Ausführung des exakten Heads vor Hochstufung qualifizieren. |
| Framework OSV und Scorecard | Doppelte pull-request-head-Identitäten; zuerst explizite eindeutige Jobnamen und Ausführung qualifizieren. |
| Parent OSV pull-request-diff | Fork-SARIF-Upload/Berechtigungen benötigen Qualifikation; Erfolg im eigenen Repository genügt nicht. |
| Gehostetes Sonar und externe SonarCloud-Prüfungen | Bei Forks übersprungene Jobs oder fehlende externe Ausführung; bestehende CI bleibt erhalten. |
| C++20/23, geplante Scans, Wartungsjobs | Ausdrücklich beratend oder operativ statt universeller PR-Pflichtprüfungen. |
| Manuelle Host-/Broker-Jobs und H2/H3-Preflight | Keine kontinuierliche Runtime-Abnahme; keine unimplementierte Kampagne verlangen oder Aggregaterfolg vortäuschen. |

## Nachweise und Grenzen

Aktuelle Parent-/Framework-Workflow- und Composite-Quellen am 2026-11-02 sowie Live-Rulesets und gelieferte Check-Metadaten geprüft. Kein Fork-PR und keine administrative Änderung ausgeführt. Vor Anwendung den Vorher-Snapshot erneuern, die unzugängliche klassische Schutzebene klären und die Ausführung am aktuellen PR-Head prüfen. Bestehende Schutzmaßnahmen dürfen niemals reduziert werden.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
