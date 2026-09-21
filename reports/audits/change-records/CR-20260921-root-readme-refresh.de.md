# Aktualisierung der Dokumentation und Beispiele für bessere Verständlichkeit

**Sprache:** [English](CR-20260921-root-readme-refresh.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260921-root-readme-refresh` |
| Datum (UTC) | 2026-09-21 |
| Basis-Revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |

## Motivation und Problemstellung

Der Benutzer hat eine vollständige Aktualisierung der englischen/deutschen
Root-READMEs angefordert und den Scope danach auf die Projektdokumentation und
den eingecheckten `examples/`-Baum erweitert, damit das Repository für neue
Benutzer leichter verständlich ist und dem aktuellen Implementierungsstand
entspricht.

Das vorhandene Material war technisch detailliert, begann aber häufig auf einer
Evidence-, Policy- oder Implementierungs-internen Ebene. Wichtige
Unterscheidungen wie sechs Hostfamilien gegenüber zehn logischen Profilen,
Konfigurationsebenen, Phase-4 `off` / `safe` / `strict`,
Beispielauswahl und der Unterschied zwischen Static-/Build-/Config-Checks und
Runtime-Evidence wurden nicht überall vor dem Detailmaterial eingeführt.

## Akzeptanzkriterien

Die Dokumentation muss einen klaren Weg vom Root-README über Einstieg,
Beispiele, Connector-Auswahl, Konfiguration, Build, Tests/Evidence und sicheren
Betrieb bieten. Englische und deutsche Begleitdateien müssen strukturell und
inhaltlich gleichwertig bleiben. Alle sechs Hostfamilien und zehn logischen
Lösungen müssen über Beispiele und Connector-Guides auffindbar sein.

Die Aktualisierung muss aktuelle Source-of-Truth-Grenzen erhalten und darf
Connector-Runtime-Verhalten, Konfigurationsstandards, Build-Targets, Workflows,
Dependencies, Submodule-Pointer, Verträge generierter Referenzen oder
Runtime-/Evidence-Ergebnisse nicht verändern. Technische Referenztiefe bleibt
erhalten und wird nicht durch vereinfachte, aber unvollständige Prosa ersetzt.

## Implementierungsentscheidung und Begründung

Die Dokumentation wird in zwei Ebenen organisiert. Leserorientierte
Einstiegsseiten und Host-Guides beginnen mit einer kurzen aufgabenbezogenen
Orientierung. Detaillierte quellenbasierte Referenzabschnitte bleiben dahinter
vollständig erhalten.

Root-README, Dokumentationsindex, Einstiegs-Guide, Beispielindex, zentrale
Konzept-Guides, Connector-Index und sechs Connector-Guides sowie alle sechs
Host-Beispiel-Guides erklären nun zuerst, was gelesen, welches Profil gewählt,
was die jeweilige Validierungsstufe beweist und wo Konfigurations-/
Security-Grenzen liegen. Source-Tree-READMEs für Common, Connectors, Config,
Reports und SECURITY verweisen Benutzer vor code-nahen Details auf das passende
leserorientierte Material.

Der erste PR-Head deckte außerdem einen echten Bilingual-Check-Fehler auf: Im
englischen Schnellstart stand `cd ModSecurity-connector`, während das
Repository-Verzeichnis `ModSecurity-conector` heißt. Diese Aktualisierung
korrigiert den englischen Befehl, sodass der EN/DE-Fenced-Command identisch ist.

## Geänderte Dateien

- `README.de.md`
- `README.md`
- `SECURITY.de.md`
- `SECURITY.md`
- `common/README.de.md`
- `common/README.md`
- `config/README.de.md`
- `config/README.md`
- `connectors/README.de.md`
- `connectors/README.md`
- `docs/README.de.md`
- `docs/README.md`
- `docs/architecture.de.md`
- `docs/architecture.md`
- `docs/build/README.de.md`
- `docs/build/README.md`
- `docs/build/compilers/README.de.md`
- `docs/build/compilers/README.md`
- `docs/build/compilers/apache.de.md`
- `docs/build/compilers/apache.md`
- `docs/build/compilers/envoy.de.md`
- `docs/build/compilers/envoy.md`
- `docs/build/compilers/haproxy.de.md`
- `docs/build/compilers/haproxy.md`
- `docs/build/compilers/libmodsecurity.de.md`
- `docs/build/compilers/libmodsecurity.md`
- `docs/build/compilers/lighttpd.de.md`
- `docs/build/compilers/lighttpd.md`
- `docs/build/compilers/nginx.de.md`
- `docs/build/compilers/nginx.md`
- `docs/build/compilers/overview.de.md`
- `docs/build/compilers/overview.md`
- `docs/build/compilers/traefik.de.md`
- `docs/build/compilers/traefik.md`
- `docs/change-traceability.de.md`
- `docs/change-traceability.md`
- `docs/configuration.de.md`
- `docs/configuration.md`
- `docs/connectors/README.de.md`
- `docs/connectors/README.md`
- `docs/connectors/apache.de.md`
- `docs/connectors/apache.md`
- `docs/connectors/envoy.de.md`
- `docs/connectors/envoy.md`
- `docs/connectors/haproxy.de.md`
- `docs/connectors/haproxy.md`
- `docs/connectors/lighttpd.de.md`
- `docs/connectors/lighttpd.md`
- `docs/connectors/nginx.de.md`
- `docs/connectors/nginx.md`
- `docs/connectors/runtime-failure-policy.de.md`
- `docs/connectors/runtime-failure-policy.md`
- `docs/connectors/traefik.de.md`
- `docs/connectors/traefik.md`
- `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.de.md`
- `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.md`
- `docs/decisions/README.de.md`
- `docs/decisions/README.md`
- `docs/getting-started.de.md`
- `docs/getting-started.md`
- `docs/operations-and-security.de.md`
- `docs/operations-and-security.md`
- `docs/phase4-mode-budget.de.md`
- `docs/phase4-mode-budget.md`
- `docs/reference/glossary.de.md`
- `docs/reference/glossary.md`
- `docs/reference/variables.de.md`
- `docs/reference/variables.md`
- `docs/reference/with-crs-no-mrts-profile-contract.de.md`
- `docs/reference/with-crs-no-mrts-profile-contract.md`
- `docs/repository-concept.de.md`
- `docs/repository-concept.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- `docs/security/trusted-nginx-root-broker.md`
- `docs/testing-and-evidence.de.md`
- `docs/testing-and-evidence.md`
- `examples/README.de.md`
- `examples/README.md`
- `examples/apache/README.de.md`
- `examples/apache/README.md`
- `examples/common/README.de.md`
- `examples/common/README.md`
- `examples/common/common-connector-configuration.de.md`
- `examples/common/common-connector-configuration.md`
- `examples/common/modsecurity-directives.de.md`
- `examples/common/modsecurity-directives.md`
- `examples/common/rule-examples.de.md`
- `examples/common/rule-examples.md`
- `examples/envoy/README.de.md`
- `examples/envoy/README.md`
- `examples/haproxy/README.de.md`
- `examples/haproxy/README.md`
- `examples/lighttpd/README.de.md`
- `examples/lighttpd/README.md`
- `examples/nginx/README.de.md`
- `examples/nginx/README.md`
- `examples/traefik/README.de.md`
- `examples/traefik/README.md`
- `reports/README.de.md`
- `reports/README.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.de.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.md`

## Ausgeführte Befehle

Es wurde kein repository-nativer lokaler Shell-Befehl ausgeführt, weil die
Änderung über den GitHub-Connector ohne lokalen Checkout vorbereitet wurde.

Für den ersten PR-Head `8e0086b2d194828144d303d8a887cfb285e00ec6`
meldeten GitHub Actions erfolgreiche Workflows für CodeQL, OpenSSF Scorecard,
Secret Scanning, Security Workflow Lint, protocol-contract, Envoy, HAProxy,
lighttpd, trusted NGINX exact-head und Report Governance. Die Workflows lint,
quick-framework-check, test-common, test-apache und test-nginx scheiterten am
gemeinsamen Bilingual-Dokumentationscheck mit der konkreten Meldung
`README.md: fenced code-block content differs from README.de.md`. Die Analyse
identifizierte den oben beschriebenen englischen Verzeichnisnamen-Tippfehler.
Diese Ergebnisse gelten nur für diesen früheren Head und sind keine
Current-Head-Ergebnisse des erweiterten Dokumentations-Commits.

Für den zweiten Dokumentations-Head `bb98e75da5bd472215a6194462e24fa7356da4b4`
war die Fenced-Command-Abweichung der Root-README nicht mehr der gemeldete
Blocker. Der gemeinsame No-CRS-Dokumentationskonsistenzcheck meldete stattdessen,
dass im Repository-Übersichtspaar die erforderlichen Literale
`minimal_runtime_smoke` und `capabilities.json` fehlten. Der Nachfolger
stellt beide Konzepte mit leserorientierten Erklärungen wieder her, anstatt den
Checker abzuschwächen. Auch diese Ergebnisse sind nur Evidence des früheren
Heads.

## Security-Auswirkung

Nur Dokumentation. Produkt-Source, Parser, Runtime-Policy, Standardwerte,
Berechtigungen, Workflows, Dependencies, Netzwerkexposition, Credential-Flows
und Evidence-Aufbewahrung werden nicht geändert.

Die überarbeitete Dokumentation macht bestehende Security-Grenzen deutlicher:
private Listener/UDS, soweit passend, begrenzte Ressourcen, externe
Build-/Runtime-/Evidence-Pfade, Least-Privilege-Dateisystem-/Service-Ownership
sowie das Verbot, Credentials, Cookies, Authorization-Werte, Private Keys,
sensible Bodies oder personenbezogene Daten in Run-IDs, versionierte Dateien,
Logs oder Review-Evidence zu schreiben.

## Runtime-Evidence

Es wurde keine neue Runtime-Evidence erhoben oder beansprucht. Diese
Dokumentationsänderung begründet keine Host-, Protokoll-, CRS-,
Production-Readiness-, Strict-Intervention- oder Deployment-Ergebnisse.

## Bekannte Einschränkungen

Generierte Dokumentation unter `docs/generated/` bleibt bewusst unverändert, weil die Repository-Policy Änderungen über Generator/Source-Vertrag verlangt. Compiler-spezifische Tiefenreferenzen, Decision Records und spezialisierte CI-/Security-Verträge bleiben technisch, beginnen nun aber mit Leserorientierung oder werden über klarere aufgabenbezogene Einstiege erreicht.

Die Beispiele bleiben Konfigurationsreferenzen und keine Produktions-
Deployment-Manifeste. Hostspezifische Installationspfade, Ports, Modul-ABI,
Service-Identität, TLS, Rules-Dateien, Sockets, Berechtigungen und
Logging/Retention benötigen weiterhin Operator-Review.

## Verbleibende Risiken

Künftige Source-, Target-, Profil- oder Policy-Änderungen können erneut
Dokumentationsdrift erzeugen, wenn die leserorientierte Navigation nicht
zusammen mit dem zuständigen technischen Vertrag aktualisiert wird.
Repository-Bilingual-/Link-Checks und Review der Exact-Head-CI bleiben die
wesentlichen Kontrollen.

## Nicht ausgeführte Prüfungen mit Begründung

Lokale `make check-bilingual-docs`, `make check-doc-links`, `git diff
--check` und `git status --short` wurden nicht ausgeführt, weil dieser
Connector-Workflow keinen lokalen Checkout bereitstellt. Builds,
Host-Runtime-Tests, CRS-Runs, Sanitizer und Protokollmatrizen wurden nicht
ausgeführt, weil die Änderung rein dokumentarisch ist.

Current-Head-Hosted-CI wird nicht vorab als erfolgreich behauptet. Sie muss den
erweiterten Dokumentations-Commit einschließlich des korrigierten Root-README-
Fenced-Commands bewerten.

## Finaler Diff- und Review-Status

Diese Arbeit erweitert Draft PR #383 auf Branch
`docs-refresh-root-readmes`. Die Änderung bleibt rein dokumentarisch und
autorisiert bzw. führt keinen Merge aus. Der CI-Fehler des früheren Heads wurde
geprüft; die README-Befehlsabweichung ist im vorbereiteten Nachfolger
korrigiert. Current-Head-Checks und Review bleiben getrennte Delivery-Evidence.
