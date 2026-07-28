# Change Record: Parent-Compiler-Guide-Literal-Deduplizierung für SonarQube Cloud S1192

**Sprache:** [English](CR-20260727-sonar-compiler-guides-literal-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-compiler-guides-literal-deduplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-python:S1192-Code-Smells: 43 aktuelle OPEN-Receipt-Keys in scripts/generate_compiler_guides.py. |
| Grenze | Parent-Compiler-Guide-Generator, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Generierte Guide-Dateien, Connector- oder Runtime-Verhalten, Framework, MRTS, Gitlinks, Workflows, SonarQube-Cloud-Konfiguration, Quality Gates, Suppressions, externer Issue-Status, Push, Pull Request und Merge bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle SonarQube-Cloud-Receipt-Inventur meldet 43 offene
python:S1192-Befunde im Parent-Compiler-Guide-Generator. Wiederholte statische
Guide-Metadaten, Befehlsfragmente, Quellbeschreibungen und
Verifikationszeichenketten verdecken die Herkunft der gerenderten Werte und
machen spätere Änderungen fehleranfällig.

## Akzeptanzkriterien

- Genau die 43 Receipt-basierten python:S1192-Vorkommen im
  Compiler-Guide-Generator durch Wiederverwendung semantisch identischer
  Modulkonstanten bearbeiten.
- Die generierten englischen und deutschen Compiler-Guides bytegenau erhalten.
- Die native Compiler-Guide-Verifikation, die Receipt-basierte statische
  Prüfung, den Whitespace-Review und die Repository-Dokumentationschecks
  bestehen.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar pflegen und keinen
  SonarQube-Cloud-Issue vor einer neuen exakten Kandidaten-Head-Analyse als
  geschlossen behaupten.

## Implementierungsentscheidung und Begründung

Die wiederholten Werte werden durch modul-lokale Konstanten dargestellt, deren
Werte mit den vorherigen Literalen identisch sind. Bestehende Datenstrukturen,
Render-Reihenfolge, Branch-Auswahl, generierte Pfade und Befehlstext bleiben
unverändert. Der Generator bleibt die einzige Quelle für das gesamte
gerenderte Guide-Material; keine generierte Datei wird direkt bearbeitet.

## Geänderte Dateien

- scripts/generate_compiler_guides.py
- reports/audits/change-records/CR-20260727-sonar-compiler-guides-literal-deduplication.md
- reports/audits/change-records/CR-20260727-sonar-compiler-guides-literal-deduplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

- rtk proxy make check-compiler-guides
- Receipt-basierte AST-Literalprüfung für die 43 aktuellen python:S1192-Keys
- rtk proxy git diff --check
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links

Der isolierte Task-Worktree initialisierte den vom Parent festgeschriebenen
Framework-Gitlink auf 47e50e7bc43ba7a3b5bad1a9448111794f664cc0 ausschließlich
als Dokumentationscheck-Abhängigkeit. Weder Framework-Quellen, Parent-Gitlink,
Framework-Branch noch Framework-Pull-Request wurden geändert.

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Compiler-Guide-Verifikation | bestanden: make check-compiler-guides schloss 21 Tests ab, einschließlich idempotenter Generierung und bytegenauem Vergleich der generierten Guides. |
| Receipt-basierte AST-Literalprüfung | bestanden: sonar_receipt_issues=43 und issue_literals_still_duplicated=0. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| Direkter Source-Diff-Review | bestanden: nur semantisch identische modul-lokale Konstanten und ihre direkten Verwendungen im Generator änderten sich. |
| make check-bilingual-docs | bestanden: bilingual docs ok. |
| make check-doc-links | bestanden: repository path references: PASS und doc links ok. |

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet not_applicable. Dies ist ein
ausgabeäquivalenter Refactor eines Dokumentationsgenerators; er ändert keine
Runtime-Pfadvalidierung, kein Netzwerk, keinen Subprozess, keinen Connector,
keine Credentials, Berechtigungen oder Sicherheitskontrollen. Es wird kein
Security-Befund als behoben behauptet.

## Dokumentationsstatus

Die Generatorverifikation bestätigt, dass der erzeugte englisch/deutsche
Guide-Inhalt unverändert ist. Dieses gepaarte Change Record dokumentiert die
reine Source-Deduplizierung. Die abgeschlossenen
Repository-Dokumentationschecks melden bilingual docs ok, repository path
references PASS und doc links ok.

## Runtime-Evidence

Es wurde kein Connector-, Host-, Protokoll- oder Produktions-Runtime-Verhalten
geändert oder behauptet. Die Generatorverifikation ist Source- und
Dokumentations-Evidence, keine Runtime-Evidence.

## Bekannte Einschränkungen

SonarQube Cloud hat diesen Kandidaten-Head noch nicht analysiert. Die 43
aktuellen Befunde können erst nach einer frischen Analyse des exakten
ausgelieferten Commits verschwinden.

## Verbleibende Risiken

Eine fehlerhafte Ersetzung könnte einen generierten Guide-Wert oder Befehl
ändern. Der native Generatorcheck führt einen bytegenauen Output-Vergleich
aus, und der Source-Diff ist auf die von der aktuellen Receipt belegten Werte
begrenzt.

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

Der Task-Worktree-Kandidat enthält ausschließlich die Compiler-Guide-Literal-
Deduplizierung und das erforderliche bilinguale Traceability-Material. Der
autoritative Parent-Checkout, Framework-Quellen, MRTS-Quellen, Parent-Gitlink,
Scanner-Kontrollen und externe SonarQube-Cloud-Issue-Status bleiben unverändert.
