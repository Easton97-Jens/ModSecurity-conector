# Aktualisierung der Root-READMEs

**Sprache:** [English](CR-20260921-root-readme-refresh.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260921-root-readme-refresh` |
| Datum (UTC) | 2026-09-21 |
| Basis-Revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |

## Motivation und Problemstellung

Das Root-README-Paar enthielt weiterhin korrekte, aber stark Evidence-interne
Sprache und bot neuen Lesern keinen kompakten Projektüberblick mehr. Es
beschrieb außerdem nur die sechs ausgewählten Hostfamilien-Routen, obwohl die
kanonische Connector-Dokumentation zehn logische Profile unterscheidet, und
stellte den aktuellen Phase-4-Vertrag `off` / `safe` / `strict` nicht als
erstklassigen Einstiegspunkt dar.

Der Benutzer hat eine vollständige Aktualisierung von `README.md` und
`README.de.md` auf den aktuellen Repository-Stand angefordert.

## Akzeptanzkriterien

Die englische und deutsche Root-README müssen strukturell gleichwertig bleiben,
die sechs Hostfamilien und zehn logischen Profile erklären, die aktuelle
Phase-4-Modusgrenze ohne Erweiterung von Runtime-Claims beschreiben, einen
nutzbaren Schnellstart und eine Übersicht häufiger Targets bieten, auf die
kanonische Detaildokumentation verweisen, die Parent-/Framework-Ownership-
Grenze erhalten und explizite Evidence-/Security-Einschränkungen beibehalten.

Durch diese reine Dokumentationsänderung dürfen weder Connector-Verhalten,
Build-Target, Konfigurationsstandard, Workflow, Dependency, Submodule-Pointer
noch Runtime-/Evidence-Ergebnis geändert oder hochgestuft werden.

## Implementierungsentscheidung und Begründung

Das Root-README-Paar wird als Onboarding- und Navigationsschicht neu geschrieben,
statt jeden detaillierten Connector-Guide zu duplizieren. Stabile Fakten werden
direkt genannt; volatile Details wie exakte Python-/Go-Patchversionen werden auf
ihre eingecheckten Source-Dateien verwiesen, statt in Prosa kopiert zu werden.

Die README unterscheidet nun Core-Routen der Hostfamilien von logischen
Profilen, ergänzt das gemeinsame P1-P4-Phasenmodell und die aktuellen
Phase-4-Budgetmodi, hält Run-/Evidence-Grenzen explizit und gruppiert
Repository-Aufbau, Schnellstart, häufige Workflows, Konfiguration, Sicherheit,
Entwicklungsregeln, Dokumentation und Provenienz in eigene Abschnitte.

## Geänderte Dateien

- `README.md`
- `README.de.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.de.md`

## Ausgeführte Befehle

Es wurde kein repository-nativer Shell-Befehl ausgeführt, weil diese Änderung
über den GitHub-Connector ohne lokalen Repository-Checkout vorbereitet wurde.
Repository-Stand, aktuelle Dokumentationsverträge, Targetnamen, aktuelle
Phase-4-Semantik, Toolchain-Source-Dateien und die aktuelle `master`-Revision
wurden vor der Bearbeitung aus GitHub gelesen.

## Security-Auswirkung

Nur Dokumentation. Source, Runtime-Verhalten, Validierungsregel, Standardwert,
Credential-Flow, Berechtigung, Workflow, Dependency, Netzwerkexposition,
Logging-Pfad und Evidence-Aufbewahrungsverhalten werden nicht verändert. Die
neue README verstärkt die bestehende Warnung, keine Secrets oder sensiblen
Traffic-Daten in Run-IDs, Befehlszeilen, eingecheckte Konfiguration, Logs oder
Review-Evidence zu schreiben.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Aus dieser
Dokumentationsänderung wird kein Host-, Protokoll-, CRS-, Production-Readiness-,
Strict-Intervention- oder Deployment-Ergebnis abgeleitet.

## Bekannte Einschränkungen

Die Root-README fasst das Repository bewusst zusammen. Connectorspezifische
Syntax, Compatibility-Routen, Capability-Status, Host-Voraussetzungen,
Protokollgrenzen und aktuelle Run-Ergebnisse bleiben in den verlinkten
Connector-, Konfigurations-, Build-, Test-/Evidence-, Operations-/Security- und
Report-Dokumenten maßgeblich.

## Verbleibende Risiken

Das wesentliche Restrisiko ist zukünftiger Dokumentationsdrift, wenn die
Root-Navigation bei Änderungen an Targetnamen, Profilidentitäten oder
Policy-Verträgen nicht nachgezogen wird. Repository-Dokumentations-/Linkchecks
und die Prüfung des exakten PR-Heads bleiben die geeigneten Kontrollen.

## Nicht ausgeführte Prüfungen mit Begründung

`make check-bilingual-docs`, `make check-doc-links`, `git diff --check` und
`git status --short` wurden nicht ausgeführt, weil der GitHub-Connector keinen
lokalen Shell-Checkout bereitstellt. Hosted Checks, falls sie durch den
Draft-PR ausgelöst werden, sind getrennte Exact-Head-Evidence und werden hier
nicht vorab als erfolgreich behauptet.

Build, Config-Load, Unit-/Integrationstest, Host-Runtime, CRS-Run, Sanitizer,
SonarQube-Check und Protokollmatrix wurden nicht ausgeführt, weil die Änderung
rein dokumentarisch ist und kein solches Ergebnis benötigt wird, um eine nicht
vorhandene Runtime-Änderung zu beschreiben.

## Finaler Diff- und Review-Status

Die eingegrenzte Änderung beschränkt sich auf das englische/deutsche
Root-README-Paar und dieses erforderliche englische/deutsche Change-Record-Paar.
Der Inhalt wurde vor der Branch-Veröffentlichung mit der aktuellen
`master`-Dokumentation und dem aktuellen Phase-4-Vertrag abgeglichen. Es werden
kein Merge, keine Produktionsfreigabe, kein erfolgreicher Hosted Check und
keine Runtime-Verifikation behauptet.
