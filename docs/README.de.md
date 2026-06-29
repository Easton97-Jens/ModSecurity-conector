# Dokumentationsindex

**Sprache:** [English](README.md) | Deutsch

Status: umgesetzt

Dieses Verzeichnis ist nach Themen gruppiert, damit connector-eigene
Architektur-, Roadmap- und Source-Attribution-Dokumente auch dann navigierbar
bleiben, wenn der framework-eigene Case-Korpus und die generierten Reports
wachsen.

## Hauptabschnitte

| Abschnitt | Zweck |
| --- | --- |
| `architecture/` | Gemeinsames C-first-Modell, Adaptergrenzen, Status-/Capability-Modelle und Refactoring-Pläne |
| `connectors/` | Apache-/NGINX-Direktiven, Rule-Load-Dokumentation und Planung zukünftiger Connectoren |
| `testing/` | Verified-Run-Runtime-Umgebung, Worker-Zugriffs-Preflights und Workflow-Hinweise für generierte Reports |
| `roadmap/` | Aktuelle Connector-Roadmap |
| `licensing/` | Lizenz- und Herkunftsrichtlinie für importierte Connector-Quellen |
| `../reports/testing/` | Connector-eigene generierte Evidence, Real-World-Validierungsnotizen, Case Matrix und PR-/Source-Evidence |
| `../modules/ModSecurity-test-Framework/docs/` | Framework-eigenes YAML-Schema, Fixtures, Case-Korpus, Importanalysen, TODO-Inventar und wiederverwendbare Testdokumente |

## Quellenangaben

| Repository | Repo-lokaler Zweck | Upstream | Beobachtete Version / Tag | Lizenz |
| --- | --- | --- | --- | --- |
| ModSecurity v2 | Nur historische Source-/Vergleichsreferenz | https://github.com/owasp-modsecurity/ModSecurity | `v2.9.13` | Apache-2.0 |
| ModSecurity v3 | libmodsecurity-Runtime-/API-Referenz | https://github.com/owasp-modsecurity/ModSecurity | `v3.0.15` | Apache-2.0 |
| ModSecurity-apache | Referenz für Apache-Adapter-Verhalten und Source-Attribution | https://github.com/owasp-modsecurity/ModSecurity-apache | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |
| ModSecurity-nginx | Referenz für NGINX-Adapter-Verhalten und Source-Attribution | https://github.com/owasp-modsecurity/ModSecurity-nginx | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

CI, lokale Entwicklung und Report-Refreshes sollten repository-relative Pfade,
Submodule und Umgebungsvariablen verwenden, nicht maschinenspezifische
Source-Orte.

## Erste Lesungen

- Architekturgrenze: `architecture/architecture.md`
- Fähigkeitsmodell: `architecture/capability-model.md`
- Statusmodell: `architecture/status-model.md`
- Real-World-Connector-Proof-Modus: `../reports/testing/real-world-connector-validation.md`
- Testing-Report-Index: `../reports/testing/README.md`
- Verified-Run-Umgebung: `testing/verified-run-environment.md`
- Zusammenführungsbereitschaft: `../reports/testing/generated/canonical/final-consistency-audit.generated.md`
- Aktueller Kompatibilitätsnachweis: `../reports/testing/test-coverage-overview.md`
- Case Matrix: `../reports/testing/case-matrix.md` und
`../reports/testing/generated/coverage/case-matrix.generated.md`
- Roadmap und offene Arbeit: `roadmap/roadmap.md` und
`../modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`
- YAML-Schema und gemeinsam genutzte Fixtures:
`../modules/ModSecurity-test-Framework/docs/imports/common/schema.md` und
`../modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md`
- PR-/Source-Evidence: `../reports/testing/evidence/pr-evidence-summary.md`
und `../reports/testing/evidence/raw-args-pr3564.md`
- Lizenz und Herkunft: `licensing/license-and-origin.md` und `../licenses/README.md`
