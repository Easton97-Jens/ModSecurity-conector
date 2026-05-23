# Template Evaluation

Status: reviewed

Template-Bewertung: teilweise geeignet

Begründung: `connectors/_template` enthält eine vorsichtige Scaffold-Struktur
mit README, TODO, Architektur-, Build-, Validation-, Harness- und
Source-Platzhaltern. Es ist als Ausgangspunkt geeignet, aber nur teilweise:
konkrete Herkunfts-/Metadatenanforderungen, Build-Nachweise und
Runtime-Nachweise sind im Template nicht vollständig belegt. Der lokale
Template-Tests-Ordner wurde entfernt; ausführbare Template-Tests werden nicht
connector-lokal gepflegt. Die Scaffold-Entscheidungen fuer neue Connectoren
sind in `connector-scaffold-decisions.md` dokumentiert. Die aktuelle
`/src`-Runtime-Evidenz fuer Apache und NGINX in `verified-runtime-run.md`
promotet das generische Template nicht zu einer Implementierung.

## Bewertung

| Bereich | Status | Begründung | Beleg/Pfad |
| --- | --- | --- | --- |
| README | OK | Datei vorhanden; beschreibt Template als generisch und nicht produktiv. | `connectors/_template/README.md` |
| TODO | OK | Datei vorhanden und auf GitHub-Checkboxen mit Statuswerten umgestellt. | `connectors/_template/TODO.md` |
| Grundstruktur | OK | README listet README, TODO, docs, harness und src; lokaler Testordner ist entfernt. | `connectors/_template/README.md` |
| Architektur | OK | Beschreibt adapter-owned Prinzip und server-spezifische Grenzen. | `connectors/_template/docs/architecture.md` |
| Build | Teilweise | Build-Themen sind benannt, konkrete Build-Regeln bleiben fuer Connectoren offen. | `connectors/_template/docs/build.md` |
| Validation | OK | Stellt klar, dass Runtime-Evidenz erforderlich ist. | `connectors/_template/docs/validation.md` |
| Coverage Matrix | OK | Generische Matrix trennt Framework-Coverage von Runtime-Verifikation und setzt Template-Defaults auf `not-verified`. | `connectors/_template/docs/coverage-decision-matrix.md` |
| Scaffold-Entscheidungen | OK | Status-Vokabular, externe Testpfade, RESPONSE_BODY-Mindest-Evidenz und `partial`-Grenzen sind dokumentiert. | `reports/template-verification-nginx-apache/connector-scaffold-decisions.md` |
| Aktuelle Runtime-Evidenz | Nicht anwendbar | `verified-runtime-run.md` dokumentiert Apache/NGINX-Runtime-Ergebnisse, aber keine Template-Runtime. | `reports/template-verification-nginx-apache/verified-runtime-run.md` |
| Harness | Teilweise | Erwartete Hooks sind benannt, aber nicht implementiert. | `connectors/_template/harness/README.md` |
| Source | OK | Enthält keine produktiven C-Claims und warnt vor ungeprueftem Kopieren. | `connectors/_template/src/README.md` |
| Lokaler Template-Testordner | OK | `connectors/_template/tests` wurde entfernt. | `connectors/_template/README.md` |
| Ausführbare Template-Tests | Nicht verifiziert | Ausführbare Template-Tests werden nicht connector-lokal gepflegt. | `connectors/_template/README.md` |
| Externer Testmodulpfad | Teilweise | Externer Testmodulpfad: `modules/ModSecurity-test-Framework` ist im Repository belegt; das Template definiert ihn nicht als lokalen Testordner. | `README.md`, `Makefile` |
| ORIGIN/Lizenz | Offen | Nur als TODO fuer konkrete Connectoren benannt; keine Template-Datei vorhanden. | `connectors/_template/TODO.md` |
| Metadaten | Offen | Nur als TODO fuer konkrete Connectoren benannt; keine `metadata.*`-Datei im Template. | `connectors/_template/TODO.md` |
| RESPONSE_BODY blocking | Nicht verifiziert | Keine ausreichende Repo-Evidenz gefunden. | `connectors/_template/docs/validation.md` |

## Checkbox-Zusammenfassung

- [x] README vorhanden.
- [x] Grundstruktur ohne lokalen Template-Testordner vorhanden.
- [x] Keine produktive Funktionsbehauptung im Template gefunden.
- [x] Validation-Dokument fordert Runtime-Evidenz.
- [x] Coverage-Decision-Matrix vorhanden.
- [ ] Status: teilweise - Harness ist dokumentiert, aber nicht implementiert.
- [x] Lokaler Template-Testordner entfernt.
- [ ] Status: nicht verifiziert - Ausführbare Template-Tests werden nicht
      connector-lokal gepflegt.
- [ ] Status: teilweise - Externer Testmodulpfad ist im Repository belegt, aber
      nicht als lokaler Template-Testordner Teil des Templates.
- [ ] Status: offen - ORIGIN-/Lizenzanforderungen fuer konkrete Connectoren
      noch zu belegen.
- [ ] Status: offen - Metadatenanforderungen fuer konkrete Connectoren noch zu
      belegen.
- [ ] Status: nicht verifiziert - RESPONSE_BODY blocking. Nicht verifiziert -
      keine ausreichende Repo-Evidenz gefunden.
- [ ] Status: not-verified - Phasen 1 bis 4 sind im Template ohne konkreten
      Connector nicht runtime-verifiziert.

## Fehlende Punkte

- Konkrete Anforderungen an `ORIGIN.md`, `SOURCE_MAP.json` oder `metadata.*`
  fuer neue Connectoren.
- Kriterien, wann ein Template-Connector von Scaffold zu Runtime-validiert
  wechseln darf, bleiben an die dokumentierte Mindestmatrix und künftige
  Runtime-Evidenz gebunden.

## Entscheidung

Das Template ist teilweise geeignet. Es ist als vorsichtige Startstruktur
nutzbar, aber nicht vollständig genug, um ohne zusätzliche connector-spezifische
Bewertung als fertige Implementierungsgrundlage zu gelten.
