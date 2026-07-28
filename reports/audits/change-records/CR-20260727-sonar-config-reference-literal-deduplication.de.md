# Change Record: Parent-Connector-Config-Reference-Literal-Deduplizierung und SonarQube-Cloud-S3358-Follow-up

**Sprache:** [English](CR-20260727-sonar-config-reference-literal-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-config-reference-literal-deduplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-PR #131: SonarQube-Cloud-python:S1192-Code-Smells: 69 aktuelle OPEN-Receipt-Keys in ci/checks/documentation/connector_config_reference.py; seine initiale Exact-PR-Head-Analyse meldete Quality Gate `OK` mit keiner neuen Duplizierung und einem neuen task-owned `python:S3358`-Issue bei ci/checks/documentation/connector_config_reference.py:3495. |
| Grenze | Parent-Konfigurationsreferenz-Generator/Checker, dieses englisch/deutsche Change-Record-Paar, seine Indizes und das lokale `python:S3358`-Follow-up. Generierte Konfigurationsreferenz-Dateien, Connector- oder Runtime-Verhalten, Framework, MRTS, Gitlinks, Workflows, SonarQube-Cloud-Konfiguration, Quality Gates, Suppressions und externer Issue-Status bleiben unverändert. PR #131 bleibt Draft; es gab keinen Merge. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Receipt-Inventur meldet 69 offene
python:S1192-Befunde im Parent-Konfigurationsreferenz-Generator. Wiederholte
Schema-Labels, Quellpfade, Erläuterungstexte und Optionskennungen erschweren
die Wartung der Quelle, ohne unterschiedliches Verhalten zu tragen.

Der initiale exakte Head des Draft-PR #131 erhielt ein SonarQube-Cloud-Quality
Gate `OK` mit keiner neuen Duplizierung, meldete jedoch einen neuen
task-owned-`python:S3358`-Issue bei
ci/checks/documentation/connector_config_reference.py:3495. Die gemeldete
verschachtelte Bedingung ist ein erforderliches lokales Follow-up, keine
akzeptierte Quality-Gate-Ausnahme. Das initiale Remote-Ergebnis kann den Status
des später lokal korrigierten Kandidaten nicht belegen.

## Akzeptanzkriterien

- Genau die 69 Receipt-basierten python:S1192-Vorkommen in
  connector_config_reference.py durch semantisch identische modul-lokale
  Konstanten bearbeiten.
- Die als `python:S3358` bei
  ci/checks/documentation/connector_config_reference.py:3495 gemeldete
  verschachtelte Bedingung durch äquivalente normale bedingte Logik ohne
  Suppression oder Änderung der Scanner-Konfiguration ersetzen.
- Schema, Optionsreihenfolge, JSON- oder Markdown-Rendering und jede
  generierte Konfigurationsreferenz-Datei erhalten.
- Den nativen Konfigurationsreferenz-Generator-/Checker-Vertrag, die
  Receipt-basierte statische Prüfung, den Whitespace-Review und die
  Repository-Dokumentationschecks bestehen.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar pflegen und keinen
  SonarQube-Cloud-Issue oder ein sauberes Post-Correction-Ergebnis vor einer
  neuen exakten Analyse des geänderten Kandidaten-Heads als geschlossen
  behaupten.

## Implementierungsentscheidung und Begründung

Nur wiederholte, byte-identische Werte werden einmal auf Modulebene benannt
und an ihren bestehenden Call-Sites verwendet. Extraktion, YAML-Verarbeitung,
Renderer-Reihenfolge, Default-Werte, Diagnostik und Generator-Output-Verträge
bleiben unverändert. Keine generierte Dokumentation wird direkt bearbeitet.

Nach der initialen PR-#131-Analyse gibt das lokale Follow-up dem Quellpfad und
dem lokalisierten Label explizite Namen, wählt mit einem normalen `if`/`else`
einen Link oder einen code-formatierten Pfad und setzt danach dieselbe
Source-Example-Zeile zusammen. Es ersetzt die gemeldete verschachtelte
Bedingung ohne SonarQube-Cloud-Suppression, Quality-Gate-Änderung oder Änderung
der Scanner-Konfiguration. Für diesen lokal geänderten Kandidaten wurde keine
neue Remote-Analyse beobachtet.

## Geänderte Dateien

- ci/checks/documentation/connector_config_reference.py
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.md
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

Die folgenden lokalen Befehle sind bestätigte Evidence für den initialen
S1192-Kandidaten vor dem `python:S3358`-Follow-up. Sie werden nicht als
Source-Validation nach der Korrektur dargestellt.

- rtk proxy make check-connector-config-reference
- Receipt-basierte AST-Literalprüfung für die 69 aktuellen python:S1192-Keys
- rtk proxy git diff --check
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links

Die dokumentationsspezifische Validation für dieses Record-Update verwendete:

- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy git diff --check

Der isolierte Task-Worktree initialisiert den vom Parent festgeschriebenen
Framework-Gitlink ausschließlich als Dokumentationscheck-Abhängigkeit. Weder
Framework-Quellen, Parent-Gitlink, Framework-Branch noch Framework-Pull-
Request ändern sich.

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Konfigurationsreferenz-Generation/Checker (initialer S1192-Kandidat) | bestanden: 21 generierte Dateien sind aktuell; der Checker bestand mit apache=14, nginx=18, haproxy=41, envoy=141, traefik=71, lighttpd=19, common=25, engine=12. Dies wird nicht als Evidence nach der `python:S3358`-Korrektur behauptet. |
| Receipt-basierte AST-Literalprüfung (initialer S1192-Kandidat) | bestanden: receipt_issues=69 und all_literals_singleton. Dies wird nicht als Evidence nach der `python:S3358`-Korrektur behauptet. |
| git diff --check (initialer S1192-Kandidat) | bestanden: kein Whitespace-Fehler. Dies wird nicht als Evidence nach der `python:S3358`-Korrektur behauptet. |
| Direkter Source-Diff-Review (initialer S1192-Kandidat) | bestanden: nur byte-identische modul-lokale Konstanten und direkte Verwendungen im abgegrenzten Generator änderten sich. Dies ging der späteren normalen bedingten Korrektur voraus. |
| make check-bilingual-docs (initialer S1192-Kandidat) | bestanden: bilingual docs ok. Dies wird nicht als Evidence nach der `python:S3358`-Korrektur behauptet. |
| make check-doc-links (initialer S1192-Kandidat) | bestanden: repository path references: PASS und doc links ok. Dies wird nicht als Evidence nach der `python:S3358`-Korrektur behauptet. |
| Dokumentationsspezifisches make check-bilingual-docs (dieses Record-Update) | bestanden: bilingual docs ok. Dies validiert nur die gepaarte Dokumentation; es validiert weder die lokale `python:S3358`-Source-Korrektur noch einen geänderten Remote-SonarQube-Cloud-Head. |
| Dokumentationsspezifisches git diff --check (dieses Record-Update) | bestanden: kein Whitespace-Fehler im Kandidaten-Diff. Dies ist keine Source- oder Remote-Analyse-Evidence. |
| Initiale exakte Draft-PR-#131-SonarQube-Cloud-Analyse | beobachtet: Quality Gate `OK` mit keiner neuen Duplizierung, jedoch ein neuer task-owned `python:S3358`-Issue bei ci/checks/documentation/connector_config_reference.py:3495. Dies ist kein sauberes Exact-Head-Ergebnis. |
| Lokales `python:S3358`-Follow-up | lokal angewendet: Die verschachtelte Bedingung wurde durch die oben beschriebene normale bedingte Konstruktion ersetzt; es ist keine Remote-Analyse nach der Korrektur dokumentiert. |
| SonarQube-Cloud-Analyse nach der Korrektur | not_run: Es wurde keine Analyse für den geänderten Kandidaten-Head beobachtet. |

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet not_applicable. Dies ist ein
ausgabeäquivalenter Refactor eines Konfigurationsdokumentations-Generators; er
ändert keine Runtime-Pfadvalidierung, kein Netzwerk, keinen Subprozess, keinen
Connector, keine Credentials, Berechtigungen oder Sicherheitskontrollen. Es
wird kein Security-Befund als behoben behauptet.

## Dokumentationsstatus

Der initiale native Konfigurationsreferenz-Check bestätigt, dass alle 21
generierten Dateien vor dem `python:S3358`-Follow-up aktuell waren. Dieses
gepaarte Change Record trennt jetzt diese initiale S1192-Evidence von der
lokalen normalen bedingten Korrektur. Die abgeschlossenen initialen
Repository-Dokumentationschecks meldeten bilingual docs ok, repository path
references PASS und doc links ok; sie werden nicht für den geänderten
Kandidaten-Head behauptet.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll- oder Produktions-Runtime-Verhalten
geändert oder behauptet. Die Generator-/Checker-Verifikation ist Source- und
Dokumentations-Evidence, keine Runtime-Evidence.

## Bekannte Einschränkungen

SonarQube Cloud analysierte den initialen exakten Draft-PR-#131-Head, aber
diese Analyse meldete trotz Quality Gate `OK` und keiner neuen Duplizierung das
task-owned-`python:S3358`-Follow-up. Der später lokal korrigierte Kandidat
erhielt keine Analyse seines geänderten Heads. Die 69 aktuellen Befunde und
der S3358-Status können erst durch eine frische Analyse des exakten
ausgelieferten Heads als behoben gelten.

## Verbleibende Risiken

Eine fehlerhafte Extraktion oder die normale bedingte Umschreibung könnte eine
gerenderte Option, Diagnostik, einen Link oder ein Label ändern. Die initiale
native Generation/der Checker mindert das Extraktionsrisiko, jedoch bleiben
eine frische Exact-Head-Analyse und Source-Validation nach der Korrektur
erforderlich, bevor ein sauberes Ergebnis behauptet wird.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine frische SonarQube-Cloud-Analyse und ein GitHub-CI-Ergebnis für den lokal
  geänderten Kandidaten nach `python:S3358` sind not_run: Es wurde keine
  Remote-Analyse des geänderten Heads beobachtet. Das initiale Draft-PR-#131-
  Ergebnis gilt nur für seinen initialen exakten Head.
- Connector-Builds, Host-Konfigurationschecks, Runtime-Smokes,
  Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar,
  weil keine Connector-/Runtime-Implementierung oder Cross-Repository-Quelle
  geändert wurde.
- Es gab keinen Merge und kein Parent-`master`-Update. PR #131 bleibt Draft;
  spätere Delivery-Evidence wird ausschließlich aus beobachteten Ergebnissen
  für seinen geänderten Head aufgenommen.

## Delivery-Status

PR #131 bleibt Draft. Sein initialer exakter Head hat das oben festgehaltene
SonarQube-Cloud-Ergebnis: Quality Gate `OK`, keine neue Duplizierung und ein
task-owned-`python:S3358`-Follow-up. Die normale Korrektur der verschachtelten
Bedingung ist lokal; eine anschließende Remote-Analyse wurde nicht beobachtet.
Es wird kein Merge oder Parent-`master`-Update behauptet.

## Finaler Diff- und Review-Status

Die Draft-PR-#131-Historie enthält die Konfigurationsreferenz-Literal-
Deduplizierung und das erforderliche bilinguale Traceability-Material; der
lokale Kandidat enthält zusätzlich die normale `python:S3358`-Korrektur der
Bedingung und dieses synchronisierte Record-Update. Das einzige beobachtete
Remote-SonarQube-Cloud-Ergebnis gehört zum initialen exakten PR-Head und darf
nicht als Evidence für den geänderten Kandidaten gelten. Der autoritative
Parent-Checkout, Framework-Quellen, MRTS-Quellen, Parent-Gitlink,
Scanner-Kontrollen und die externe SonarQube-Cloud-Konfiguration bleiben
unverändert; PR #131 ist Draft und ungemergt.
