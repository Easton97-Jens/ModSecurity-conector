# Template Evaluation

Status: reviewed

Template status: suitable scaffold, not runtime-verified

Template-Bewertung: geeignet als Scaffold-Vorlage, nicht runtime-verifiziert

Begründung: `connectors/_template` enthält jetzt einen konkreteren
Connector-Ablauf mit README, TODO, Architektur-, Build-, Validation-,
Coverage-, Harness- und Source-Dokumentation. Es ist als Scaffold-Vorlage fuer
neue Connectoren geeignet. Es ist bewusst keine produktive
Connector-Implementierung und deshalb nicht runtime-verifiziert.
Herkunfts-/Metadatenanforderungen, Build-Nachweise, No-CRS/With-CRS-Ergebnisse
und Runtime-Nachweise sind verpflichtende Gates pro konkretem Connector, keine
Template-Fehler. Der lokale Template-Tests-Ordner wurde entfernt; ausführbare
Template-Tests werden absichtlich extern im Framework gepflegt. Die
Scaffold-Entscheidungen fuer neue Connectoren sind in
`connector-scaffold-decisions.md` dokumentiert. Die aktuelle `/src`-Runtime-
Evidenz fuer Apache und NGINX in `verified-runtime-run.md` promotet das
generische Template nicht zu einer Implementierung.

## Bewertung

| Bereich | Status | Begründung | Beleg/Pfad |
| --- | --- | --- | --- |
| README | OK | Datei vorhanden; beschreibt Purpose, Nutzung, anzulegende Dateien, Evidenzanforderungen, No-CRS/With-CRS, Matrix, Promotion-Gates und Nicht-Claims. | `connectors/_template/README.md` |
| TODO | OK | Datei vorhanden und in Phasen 0 bis 7 mit Checkboxen und Statuswerten gegliedert. | `connectors/_template/TODO.md` |
| Grundstruktur | OK | README listet README, TODO, docs, harness und src; lokaler Testordner ist entfernt. | `connectors/_template/README.md` |
| Architektur | OK | Beschreibt adapter-owned Prinzip, server-spezifische Grenzen und erforderliche Architektur-Evidenz. | `connectors/_template/docs/architecture.md` |
| Build | OK | Build-Evidenz, Include-/Library-Pfade, Artefakte, Logs und Makefile-Integration sind als Checkliste dokumentiert. | `connectors/_template/docs/build.md` |
| Validation | OK | Stellt klar, dass Runtime-Evidenz erforderlich ist, und nennt No-CRS, With-CRS, RESPONSE_BODY und Mindestmatrix. | `connectors/_template/docs/validation.md` |
| Coverage Matrix | OK | Generische Matrix trennt Framework-Coverage, No-CRS-Status, With-CRS-Status, Evidenzpfad und Entscheidung. | `connectors/_template/docs/coverage-decision-matrix.md` |
| CRS-Varianten | OK | Template-Doku fordert getrennte No-CRS/With-CRS-Dokumentation fuer konkrete Connectoren. | `connectors/_template/README.md`, `connectors/_template/docs/coverage-decision-matrix.md` |
| Scaffold-Entscheidungen | OK | Status-Vokabular, externe Testpfade, RESPONSE_BODY-Mindest-Evidenz und `partial`-Grenzen sind dokumentiert. | `reports/template-verification-nginx-apache/connector-scaffold-decisions.md` |
| Aktuelle Runtime-Evidenz | Nicht anwendbar | Not applicable to template. Runtime-Evidenz kann nur durch konkrete Connectoren erbracht werden. | `reports/template-verification-nginx-apache/verified-runtime-run.md` |
| Harness | Teilweise | Harness contract documented, implementation required per connector. | `connectors/_template/harness/README.md` |
| Source | OK | Enthält keine produktiven C-Claims und warnt vor ungeprueftem Kopieren. | `connectors/_template/src/README.md` |
| Lokaler Template-Testordner | OK | `connectors/_template/tests` wurde entfernt. | `connectors/_template/README.md` |
| Ausführbare Template-Tests | Intentionally external | Executable tests are framework-owned and must be referenced, not copied into `connectors/_template/tests`. | `connectors/_template/README.md` |
| Externer Testmodulpfad | OK | Externer Testmodulpfad: `modules/ModSecurity-test-Framework` ist im Repository belegt; das Template definiert ihn nicht als lokalen Testordner. | `README.md`, `Makefile` |
| ORIGIN/Lizenz | Required per connector | Jeder neue Connector muss `ORIGIN.md`, Lizenz-/Herkunftsnachweis und importierte Dateien dokumentieren. | `connectors/_template/TODO.md` |
| Metadaten | Required per connector | Jeder neue Connector muss `metadata.*` oder die im Repo vorgesehene Metadatenform anlegen. | `connectors/_template/TODO.md` |
| RESPONSE_BODY blocking | Runtime promotion gate | RESPONSE_BODY blocking darf bei konkreten Connectoren erst nach belegtem Runtime-Test als verified markiert werden. | `connectors/_template/docs/validation.md` |

## Checkbox-Zusammenfassung

- [x] README vorhanden.
- [x] Grundstruktur ohne lokalen Template-Testordner vorhanden.
- [x] Keine produktive Funktionsbehauptung im Template gefunden.
- [x] Validation-Dokument fordert Runtime-Evidenz.
- [x] Coverage-Decision-Matrix vorhanden.
- [x] No-CRS/With-CRS getrennt als Regel fuer konkrete Connectoren
      dokumentiert.
- [ ] Status: per-connector gate - Harness contract documented,
      implementation required per connector.
- [x] Lokaler Template-Testordner entfernt.
- [x] Status: intentionally external - Ausführbare Template-Tests werden nicht
      connector-lokal gepflegt.
- [x] Status: OK - Externer Testmodulpfad ist im Repository belegt, aber nicht
      als lokaler Template-Testordner Teil des Templates.
- [ ] Status: per-connector gate - ORIGIN-/Lizenzanforderungen fuer konkrete
      Connectoren belegen.
- [ ] Status: per-connector gate - Metadatenanforderungen fuer konkrete
      Connectoren belegen.
- [ ] Status: runtime promotion gate - RESPONSE_BODY blocking fuer konkrete
      Connectoren erst nach belegtem Runtime-Test als verified markieren.
- [ ] Status: not applicable to template - Phasen 1 bis 4 sind im Template ohne
      konkreten Connector nicht runtime-verifiziert.

## Echte Template-Gaps

- Keine offenen Punkte blockieren die Bewertung als Scaffold-Vorlage.
- Harness bleibt absichtlich nur als Contract dokumentiert; die Implementierung
  ist pro Connector erforderlich.
- Keine produktive Connector-Implementierung und keine Template-Runtime-
  Verifikation sind beabsichtigt und werden nicht als Template-Fehler gewertet.

## Per-Connector Gates

- `ORIGIN.md`, Lizenz-/Herkunftsnachweis und importierte Dateien dokumentieren.
- `SOURCE_MAP.json` oder einen gleichwertigen Provenance-Nachweis pflegen.
- `metadata.*` oder die im Repo vorgesehene Metadatenform anlegen.
- Build-Command, Build-Artefakte, Include-/Library-Pfade und Logs belegen.
- No-CRS und With-CRS getrennt ausführen und dokumentieren.
- Coverage Matrix mit Evidenzpfaden ausfüllen.
- RESPONSE_BODY blocking nur nach belegtem Runtime-Test als verified markieren.
- Der Wechsel von Scaffold zu Runtime-validiert bleibt an die dokumentierte
  Mindestmatrix und künftige Runtime-Evidenz gebunden.

## Entscheidung

Das Template ist als Scaffold-Vorlage geeignet. Es ist bewusst nicht
runtime-verifiziert und enthält keine produktive Connector-Implementierung.
Neue Connectoren müssen die per-connector Gates für Origin, Metadata, Build,
No-CRS, With-CRS, Coverage Matrix und Runtime Evidence erfüllen, bevor sie über
partial hinaus bewertet werden können.
