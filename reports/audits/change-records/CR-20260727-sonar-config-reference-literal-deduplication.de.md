# Change Record: Parent-Connector-Config-Reference-Literal-Deduplizierung für SonarQube Cloud S1192

**Sprache:** [English](CR-20260727-sonar-config-reference-literal-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-config-reference-literal-deduplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-python:S1192-Code-Smells: 69 aktuelle OPEN-Receipt-Keys in ci/checks/documentation/connector_config_reference.py. |
| Grenze | Parent-Konfigurationsreferenz-Generator/Checker, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Generierte Konfigurationsreferenz-Dateien, Connector- oder Runtime-Verhalten, Framework, MRTS, Gitlinks, Workflows, SonarQube-Cloud-Konfiguration, Quality Gates, Suppressions, externer Issue-Status, Push, Pull Request und Merge bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Receipt-Inventur meldet 69 offene
python:S1192-Befunde im Parent-Konfigurationsreferenz-Generator. Wiederholte
Schema-Labels, Quellpfade, Erläuterungstexte und Optionskennungen erschweren
die Wartung der Quelle, ohne unterschiedliches Verhalten zu tragen.

## Akzeptanzkriterien

- Genau die 69 Receipt-basierten python:S1192-Vorkommen in
  connector_config_reference.py durch semantisch identische modul-lokale
  Konstanten bearbeiten.
- Schema, Optionsreihenfolge, JSON- oder Markdown-Rendering und jede
  generierte Konfigurationsreferenz-Datei erhalten.
- Den nativen Konfigurationsreferenz-Generator-/Checker-Vertrag, die
  Receipt-basierte statische Prüfung, den Whitespace-Review und die
  Repository-Dokumentationschecks bestehen.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar pflegen und keinen
  SonarQube-Cloud-Issue vor einer neuen exakten Kandidaten-Head-Analyse als
  geschlossen behaupten.

## Implementierungsentscheidung und Begründung

Nur wiederholte, byte-identische Werte werden einmal auf Modulebene benannt
und an ihren bestehenden Call-Sites verwendet. Extraktion, YAML-Verarbeitung,
Renderer-Reihenfolge, Default-Werte, Diagnostik und Generator-Output-Verträge
bleiben unverändert. Keine generierte Dokumentation wird direkt bearbeitet.

## Geänderte Dateien

- ci/checks/documentation/connector_config_reference.py
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.md
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

- rtk proxy make check-connector-config-reference
- Receipt-basierte AST-Literalprüfung für die 69 aktuellen python:S1192-Keys
- rtk proxy git diff --check
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links

Der isolierte Task-Worktree initialisiert den vom Parent festgeschriebenen
Framework-Gitlink ausschließlich als Dokumentationscheck-Abhängigkeit. Weder
Framework-Quellen, Parent-Gitlink, Framework-Branch noch Framework-Pull-
Request ändern sich.

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Konfigurationsreferenz-Generation/Checker | bestanden: 21 generierte Dateien sind aktuell; der Checker bestand mit apache=14, nginx=18, haproxy=41, envoy=141, traefik=71, lighttpd=19, common=25, engine=12. |
| Receipt-basierte AST-Literalprüfung | bestanden: receipt_issues=69 und all_literals_singleton. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| Direkter Source-Diff-Review | bestanden: nur byte-identische modul-lokale Konstanten und direkte Verwendungen im abgegrenzten Generator änderten sich. |
| make check-bilingual-docs | bestanden: bilingual docs ok. |
| make check-doc-links | bestanden: repository path references: PASS und doc links ok. |

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet not_applicable. Dies ist ein
ausgabeäquivalenter Refactor eines Konfigurationsdokumentations-Generators; er
ändert keine Runtime-Pfadvalidierung, kein Netzwerk, keinen Subprozess, keinen
Connector, keine Credentials, Berechtigungen oder Sicherheitskontrollen. Es
wird kein Security-Befund als behoben behauptet.

## Dokumentationsstatus

Der native Konfigurationsreferenz-Check bestätigt, dass alle 21 generierten
Dateien aktuell bleiben. Dieses gepaarte Change Record dokumentiert die reine
Source-Deduplizierung. Die abgeschlossenen
Repository-Dokumentationschecks melden bilingual docs ok, repository path
references PASS und doc links ok.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll- oder Produktions-Runtime-Verhalten
geändert oder behauptet. Die Generator-/Checker-Verifikation ist Source- und
Dokumentations-Evidence, keine Runtime-Evidence.

## Bekannte Einschränkungen

SonarQube Cloud hat diesen Kandidaten-Head noch nicht analysiert. Die 69
aktuellen Befunde können erst nach einer frischen Analyse des exakten
ausgelieferten Commits verschwinden.

## Verbleibende Risiken

Eine fehlerhafte Extraktion könnte eine gerenderte Option oder Diagnostik
ändern. Die native Generation/der Checker validiert jede versionierte
Konfigurationsreferenz-Datei, und der Source-Diff ist auf die von der aktuellen
Receipt belegten Werte begrenzt.

## Nicht ausgeführte Prüfungen mit Begründung

- Gehostete SonarQube-Cloud-Analyse und GitHub-CI sind für diesen
  uncommitteten lokalen Kandidaten noch nicht verfügbar.
- Connector-Builds, Host-Konfigurationschecks, Runtime-Smokes,
  Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar,
  weil keine Connector-/Runtime-Implementierung oder Cross-Repository-Quelle
  geändert wurde.
- Zum Zeitpunkt dieses Records gab es keinen Commit, Push, Pull Request oder
  Master-Merge; spätere Delivery-Evidence wird ausschließlich aus beobachteten
  Ergebnissen aufgenommen.

## Finaler Diff- und Review-Status

Der Task-Worktree-Kandidat enthält ausschließlich die
Konfigurationsreferenz-Literal-Deduplizierung und das erforderliche bilinguale
Traceability-Material. Der autoritative Parent-Checkout, Framework-Quellen,
MRTS-Quellen, Parent-Gitlink, Scanner-Kontrollen und externe
SonarQube-Cloud-Issue-Status bleiben unverändert.
