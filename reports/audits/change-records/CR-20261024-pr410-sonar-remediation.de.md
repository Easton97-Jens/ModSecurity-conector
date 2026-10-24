# Change Record: CR-20261024-pr410-sonar-remediation

**Sprache:** [English](CR-20261024-pr410-sonar-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261024-pr410-sonar-remediation |
| Datum (UTC) | 2026-10-24 |
| Basis-Revision | `30d50a181278904a552e295d9a2c1ae1265e8b87` |

## Motivation und Problemstellung

Der exakte Head von PR #410 verfehlte das Sonar Quality Gate, weil die Security
Rating des New Codes E statt A war. Die vollständige Analyse enthielt 231
offene Issues und 21 duplizierte Blöcke. Der größte Teil des scheinbaren Codes
war unveränderliches historisches I12-Quellmaterial mit ausführbaren Endungen;
der Rest betraf Live-Pfad-/Prozessbehandlung, Generator-Komplexität und echte
Native-Testduplikation. Gefordert waren ursächliche Reparatur, ein lokaler Lauf
im gemeinsamen Budget und genau eine Veröffentlichung ohne Wiedereröffnung der
historischen I12-Kampagne.

## Akzeptanzkriterien

- Vollständiges Issue-/Messwert-/Duplikationsinventar an Ausgangsanalyse und
  Revision binden.
- Scanner-ausführbare historische Quellablage entfernen, ohne rekonstruiertes
  Byte, Ergebnis, Profil, Delta oder Revisionsidentität zu ändern.
- Live-Security-/Maintainability-Ursachen ohne Ausschlüsse, Unterdrückungen,
  schwächere Validierung oder geänderte Qualifikationssemantik reparieren.
- Echte Native-Testduplikation bei Erhalt unterschiedlicher Fälle konsolidieren.
- Eine importfrei vorgeprüfte Auswahl innerhalb der gemeinsamen 100-Fall-Grenze
  einfrieren und exakt einmal ohne Retry ausführen.
- Framework-/MRTS-Gitlinks und reduzierten I12-Abschluss unverändert lassen.
- EN/DE-Dokumentation aktualisieren, einmal auf den bestehenden PR-Branch
  veröffentlichen und automatische Exact-Head-CI/Sonar terminal rücklesen.
- `verified_pr` nur bei vollständig erfolgreichen Ergebnissen behaupten. Ein
  fehlgeschlagener lokaler Lauf bleibt fehlgeschlagen, auch wenn Provider später
  grün sind.

## Implementierungsentscheidung und Begründung

Die Arbeit erfolgte in einem isolierten Worktree auf
`30d50a181278904a552e295d9a2c1ae1265e8b87`. 61 historische Klartextobjekte und
ein historischer Observer-Repository-Snapshot wurden in die vorhandene
verlustfreie JSON-Form `text_lines` des Archivs überführt. Damit ändert sich
ihre Analysegrenze, nicht ihr Inhalt:
346.634 Bytes werden exakt rekonstruiert und behalten ihre SHA-256-Identitäten.

Gepflegte Envoy-Parser ersetzen transitive Imports historischer Helfer, mit
getrennten aktuellen und historischen Identitäten. Das gemeinsame Modul
`i12_path_safety` erzwingt begrenzte deskriptorgebundene Lesezugriffe, explizite
geschützte Ausgabe-Roots sowie Traversal-/Symlink-/Privatpfad-/Modus-/Checkout-
Kontrollen. Ein gemeinsames Prozessbeobachtungsmodul ersetzt aktive Imports aus
dem Archiv. Report-Generatoren, NGINX-Prüfung, Native-C-Finalisierung und Tests
wurden entlang der vorhandenen Kontrollgrenzen zerlegt.
`.sonarcloud.properties` ergänzt ausschließlich Python-/Testklassifizierung und
enthält keinen Ausschluss.

Der Einmallauf-Plan zählt jede Schleifen-/Subtest-Variante und jeden materiell
unterschiedlichen Assertion-Pfad konservativ. Er wählte 79 aktive Szenarien und
behielt die historische 21-Fall-Reserve bei: zusammen exakt 100. Die
automatischen Standardpfade sind nicht vollständig an dieses Inventar gebunden;
eine globale technische Cap-Durchsetzung wird daher nicht behauptet.

## Geänderte Dateien

- `.sonarcloud.properties` liefert Sprach-/Testklassifizierung.
- `ci/lib/i12_path_safety.py` und `i12_process_observation.py` liefern gepflegte
  gemeinsame Evidence-/Pfad-/Prozesskontrollen.
- `ci/runtime/lifecycle/i12/manifest.json`, 61 Klartextumstellungen plus eine
  Repository-Snapshot-Umstellung,
  Capture-Validierung, aktuelle Pins, gepflegte Envoy-Parser und EN/DE-I12-/
  Envoy-Dokumentation bilden die verlustfreie Code-/Datengrenze.
- Parent-Evidence-Generatoren sowie Apache-, lighttpd-, NGINX-, Envoy-, HAProxy-,
  Traefik- und Native-Lifecycle-Code nutzen gepflegte Kontrollen und kleinere
  ursachenkohärente Funktionen.
- Fokussierte Regressionstests erhalten unterschiedliche Fälle und ergänzen
  Pfad-/Archiv-Negativkontrollen; der Native-Observer-Test teilt seine zuvor
  duplizierte Compile-Fixture.
- `docs/pr-410-sonar-remediation-20261024*.md`, die drei maschinenlesbaren
  Datensätze unter `reports/testing/pr410-sonar-remediation-20261024/` und dieses
  EN/DE-Change-Record dokumentieren Ausgangsstand, Plan und tatsächlichen Fehler.
- Framework bleibt `99a7985c1be92a2297b1b59208f64df6768f2cbf`; MRTS bleibt
  `8a6bb546c4c81d8ffc7be801dceac60c6925685f`.

## Ausgeführte Befehle

- Sonar-CLI-/API-Lesezugriffe über den Pflichtwrapper holten alle 231 offenen
  Issues, Facetten/Regeln, Gate und Messwerte, alle 15 Duplikatdateien samt
  Blöcken, Compute-Task-Metadaten/-Warnungen und alle 50 GitHub-Annotationen.
- RTK-verpackte Git-/GitHub-Lesezugriffe bestimmten exakte PR-/Base-/Master-
  Heads, Draft-/Checkstatus, Branch-Berechtigung und isolierte Worktree-Basis.
- Der externe statische Prüfer rekonstruierte alle Zeilenobjekte, prüfte alle
  Objekt-/Delta-Hashes und Manifestübergänge, parste 61 geänderte Python-Dateien,
  validierte 64 JSON-Dateien/aktuelle Pins/keine Ausschlüsse und bestand.
- `git diff --check` bestand. Strikte C17-Prüfungen mit
  `-Wall -Wextra -Werror -fsyntax-only` bestanden für
  `native-lifecycle-observer.c` und `apache_header_semantics_probe.c`.
- Der importfreie Testplan-Preflight löste 30 Selektoren in 39 Methoden auf und
  bestand den Guard `79 + 21 = 100` ohne Imports, Builds oder Tests.
- Eine RTK-verpackte `python -m unittest -v`-Ausführung startete die eingefrorene
  Auswahl mit expliziten Roots/Toolchain-/SDK-/Fixture-Identitäten und ohne
  Retry. Sie lief 11,431 Sekunden und endete mit fünf Failures und einem Error.
  Sie wurde nicht wiederholt.

## Security-Auswirkung

Der Patch verengt Vertrauensgrenzen: Nicht vertrauenswürdige Evidence-Pfade
können genehmigte Roots nicht verlassen, Symlinks/Privatkonfiguration nutzen,
Create-only-Datensätze überschreiben oder unsichere Eltern verwenden; Lesezugriffe
sind größenbegrenzt und deskriptorgebunden. Historischer Programmtext ist
inertes authentifiziertes Datum und nimmt nicht mehr an aktiven Imports teil.
Vorhandene Identitäts-, Provenienz-, Physical-Producer-, Lifecycle- und
Negativ-Event-Anforderungen bleiben erhalten.

Eine frische beratende Rücklesung bestätigte den verfügbaren TAC1-Status des
Benutzers; sie erweiterte keine Repository-/Plattformberechtigung. Ein
fokussierter defensiver statischer Patch-Review fand keinen verbleibenden
konkreten Security-Befund. Es gab keinen tiefen Repository-Scan, kein Credential,
keine Unterdrückung, Gate-Abschwächung oder serverseitige Befunddisposition.

## Runtime-Evidence

Der eine lokale Funktionslauf ist in
`reports/testing/pr410-sonar-remediation-20261024/run-result.json` festgehalten.
Von 79 expandierten aktiven Szenarien bestanden 65, fünf schlugen fehl, eines
lief in einen Fehler und acht wurden nach dem ersten Companion-Schleifenfehler
nicht erreicht. Die unittest-Zusammenfassung über 39 Methoden lautete
`FAILED (failures=5, errors=1)`.

Der Envoy-Error war eine Fixture-Root-Bindungsabweichung vor der beabsichtigten
Assertion gegen transitive Imports. Alle fünf Native-Fehler stoppten in der
gemeinsamen C++-SDK-Hilfsvoraussetzung, weil `-isystem /usr/include` die
GCC-15-libstdc++-Auflösung von `#include_next <stdlib.h>` verhinderte. Kein
fehlgeschlagenes Szenario wurde erneut ausgeführt; nach dem Lauf wurde kein
ausführbares Verhalten geändert.

Das 21.256 Byte große Rohlog liegt unter
`/var/tmp/codex/ModSecurity-conector/pr410-sonar-final-20261024.0T0N9T/functional-run.log`
mit SHA-256
`4015acc961e1af01a1d88884a2960ae349230f44a001c4d93841521ea6fcdaa3`.

## Bekannte Einschränkungen

- Aktuelle Runtime-Akzeptanz und lokale Abschlussverifikation fehlen, weil der
  einzige erlaubte Lauf scheiterte und acht ausgewählte Varianten nicht erreicht
  wurden.
- Automatisches globales Standard-Suite-Inventar und technischer 100-Fall-Guard
  bleiben `not_verified`; nur der eingefrorene Aufgabenplan besaß einen
  bestandenen Guard.
- Sonar lieferte keinen PR-Coverage-Messwert; es wird kein Prozentsatz behauptet.
- Statische Quelltextevidenz prognostiziert Issue-/Duplikatschließung, ersetzt
  aber nicht die automatische Analyse des exakt veröffentlichten Heads.
- Der vorhandene 21-Fall-Abschluss bleibt historisch und wird nicht auf diesen
  neuen Head übertragen.

## Verbleibende Risiken

Fixture-Root-Abweichung und C++-Include-Pfad benötigen eine künftig ausdrücklich
autorisierte Reparatur samt neuem Lauf; der No-Retry-Vertrag dieser Aufgabe
verhindert Reparatur und Wiederholung hier. Automatische CI kann weitere Fehler
zeigen. Jeder offene Sonar-Befund, rote/ausstehende Pflichtcheck, Review-Blocker
oder Head-Unterschied hält den PR ebenfalls auf `remediation_required` oder
`checks_pending`.

## Nicht ausgeführte Prüfungen mit Begründung

Kein zweiter Funktionslauf, keine Vollsuite und weder `make lint`, `quick-check`
noch `codex-check` wurden ausgeführt, weil diese Pfade Funktionsfälle enthalten
und die eingefrorene Auswahl wiederholen oder überschreiten würden. Keine
historische I12-Host-/Matrixkampagne, Oracle-Reconciliation, PASS-Aktualisierung,
Framework-/MRTS-Ausführung, Release, Deployment oder Merge war autorisiert. Es
gab keinen lokalen Sonar-Scanner-Upload; die verbindliche automatische Analyse
gehört zum einmal veröffentlichten Head.

## Finaler Diff- und Review-Status

Statische Integrationsbefunde zu `CODEX_PROJECT_STATE`, aktuellen Quell-Pins,
altem Native-Observer-Objekt und aktiven Archivverbrauchern wurden vor dem Lauf
korrigiert. Der fokussierte Security-Review hatte keinen konkreten Befund.
Archividentität, Framework-Gitlink, JSON-/Python-/C-Statik und Diff-Whitespace
bestanden.

Der funktionale Prüfpunkt scheiterte; dieses Change Record behauptet daher
weder `verified_pr` noch Reviewbereitschaft. Der finale veröffentlichte Commit
und terminale automatische CI-/Sonar-Identitäten werden nach dem einzigen Push
in PR #410 eingetragen; sie können die fehlgeschlagene lokale Evidenz nicht
rückwirkend ändern.
