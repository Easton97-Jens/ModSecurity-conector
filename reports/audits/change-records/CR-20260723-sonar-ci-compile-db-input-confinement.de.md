# Change Record: CI-Compile-Database-Capture-Input-Begrenzung für SonarQube Cloud

**Sprache:** [English](CR-20260723-sonar-ci-compile-db-input-confinement.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-ci-compile-db-input-confinement |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | FND-SONAR-0016 und FND-SONAR-0018; SonarQube Cloud `AZ9dWiALxi9ITghe3pzq` (`pythonsecurity:S8707`), `AZ9dWiALxi9ITghe3pzp` (`python:S3516`), `AZ9dWiALxi9ITghe3pzo` sowie PR-Follow-up `AZ-QC5_F7_w-jke5-e7_` (`python:S3776`). |
| Grenze | Parent-CI-Compile-Database-Tool, seine zwei Bear-Wrapper, direkte Regressionstests sowie dieses englisch/deutsche Change-Record-Paar und die Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und der Default-Branch bleiben unverändert. |

## Motivation und Problemstellung

Der Nicht-Verify-Compile-Database-Befehl akzeptierte `--input`, konstruierte
einen `Path` und übergab ihn an `load_database`, die ihn nach nur einer
Dateiprüfung mit `read_text` las. Das Tool erzwingt eine externe Output-
Begrenzung, aber keine entsprechende Input-Capture-Grenze. Ein
aufrufergesteuerter Wert konnte deshalb eine unbeabsichtigte Datei für JSON-
Parsing und spätere Verarbeitung auswählen.

Dieselbe Source enthielt außerdem die ausgewählten Befunde zu einem
redundanten Success-Return und zur kognitiven Komplexität. Sie werden behoben,
ohne Capture-, Source- oder Output-Validierung zu schwächen.

Die erste exakte Draft-PR-Analyse entfernte die drei ursprünglichen Target-
Keys und hielt das Quality Gate bei `OK`, meldete aber einen frischen
`python:S3776`-Befund in `main` (kognitive Komplexität 24/15). Dieser Befund
ist ein erforderliches Follow-up im selben Draft-PR, keine akzeptierte Quality-
Gate-Ausnahme.

## Akzeptanzkriterien

- Ein Nicht-Verify-`--input` erfordert einen expliziten `--capture-root`;
  Verify-only weist beide inputseitigen Argumente zurück.
- Der Root ist absolut, existierend, kein Symlink, außerhalb des Checkouts,
  ein sicherer Runtime-Pfad, dem effektiven Benutzer gehörend und weder
  gruppenschreibbar noch für andere Benutzer zugänglich.
- Die aufgelöste Eingabe ist absolut, außerhalb des Checkouts, unterhalb dieses
  Roots enthalten und eine reguläre Datei, bevor sie `load_database` erreicht.
- Relative, Checkout-enthaltene, Symlink-ausbrechende, unsichere-Root- und
  Symlink-Root-Controls scheitern vor dem Lesen; ein gültiger privater
  Bear-artiger Capture wird weiterhin veröffentlicht.
- Beide Bear-Wrapper übergeben ihr eigenes `mktemp`-Capture-Verzeichnis.
  Bestehendes Filtering, Merge, atomare Veröffentlichung und Verify-only-
  Verhalten bleiben abgedeckt.
- Frische Exact-Head-SonarQube-Cloud- und Hosted-Check-Evidence ist
  erforderlich, bevor alle vier ausgewählten Keys als behoben gelten.

## Implementierungsentscheidung und Begründung

`compile_database.py` importiert jetzt die vorhandene Parent-Runtime-Path-
Policy und nutzt sie zur Validierung eines expliziten Capture-Roots. Es
kanonisiert diesen Root mit strikter Auflösung, weist einen direkten Root-
Symlink zurück, weist Checkout- und unsichere Runtime-Roots zurück und prüft
Owner-/Mode-Metadaten. Danach wird die Eingabe strikt aufgelöst; sie muss
außerhalb des Checkouts und unterhalb des validierten Roots bleiben. Nur diese
kanonische Eingabe wird an `load_database` übergeben.

Die zwei vorhandenen Bear-Aufrufer erstellen bereits private externe Capture-
Verzeichnisse. Sie übergeben jetzt genau dieses Verzeichnis über
`--capture-root`, was ihr Artefaktlayout erhält und zugleich die Trust-Grenze
am Read-Sink explizit macht.

`collect_entries` delegiert Parse- und Filterentscheidungen an schmale
Hilfsfunktionen. Dieselben akzeptierten Entries, Filtermeldungen,
Duplicate-Behandlung, Source-Tracking und Output-in-Checkout-Ablehnung bleiben
erhalten, während die kognitive Komplexität der ausgewählten Funktion sinkt.
`main` hat statt separater äquivalenter Returns nur noch einen gemeinsamen
Success-Return.

Die initiale Branch-Anordnung machte `main` selbst zu komplex. Das Follow-up
extrahiert Verify-only-Argumentvalidierung, bestehende-Datenbank-Validierung,
Capture-Laden und Veröffentlichung in explizite Hilfsfunktionen. `main`
bleibt ein flacher Orchestrator und erhält die zuvor getestete Argument-
Priorität, Read-Sink-Containment, Merge-Verhalten, atomaren Output, Filtering
und Success-Meldungen.

## Geänderte Dateien

- ci/checks/analysis/compile_database.py
- ci/checks/analysis/compile-db-nginx-c17.sh
- ci/checks/analysis/compile-db-cpp17.sh
- tests/test_c_cpp_diagnostics.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Security-Auswirkung

Der reparierte Source-to-Sink-Pfad ist `args.input` zu `Path(args.input)` zu
`load_database` und `read_text`. Vor diesem Sink etabliert der Code jetzt eine
kanonische externe Capture-Root-Invariante. Der Regressions-Control platziert
absichtlich ungültige Nicht-JSON-Daten außerhalb des Roots hinter einem
Symlink; der neue Fehler ist die Root-Containment-Verletzung und zeigt damit,
dass Parsing nicht stattfindet.

Es werden keine Rule, kein Quality Gate, keine Suppression, Exclusion, Issue-
Disposition oder Scanner-Konfiguration geändert. Keine Authentisierung,
Isolation, Validierung, Logging- oder CI-Protection wird geschwächt.

## Ausgeführte Befehle

- Fokussiertes `tests.test_c_cpp_diagnostics`: bestanden (7 Tests),
  einschließlich legitimem Capture und aller genannten negativen Controls.
- Fokussiertes `tests.test_bilingual_docs`: bestanden (11 Tests).
- `make check-ci-security-contract` mit der Parent-Virtual-Environment:
  bestanden (16 Workflow-Security-Tests und drei installierte Tool-
  Validation-Checks).
- In-Memory-Syntaxkompilierung der geänderten Python-Source und des Tests,
  `sh -n` für beide geänderten Bear-Wrapper und `git diff --check`: für den
  finalen lokalen Kandidaten bestanden.
- `make check-bilingual-docs`: nur durch bereits vorhandene Links unterhalb des
  absichtlich nicht initialisierten Framework-Gitlinks blockiert; für dieses
  Change-Record-Paar wird kein fehlender Abschnitt oder Equivalence-Fehler
  gemeldet.
- Follow-up-Helper-Extraktion: fokussierte C/C++-Diagnostik und ausgewählte
  Syntax bestanden lokal; finale Exact-Head-SonarCloud- und Hosted-Evidence
  steht nach dem gezielten Push noch aus.

## Runtime-Evidence

Das direkte Regressionsmodul startet die echte Compile-Database-CLI gegen
temporäre externe Verzeichnisse. Sein legitimer Control veröffentlicht eine
echte JSON-Compile-Datenbank aus einem privaten Capture-Root. Sein Nicht-JSON-
Symlink-Ziel liegt außerhalb dieses Roots und scheitert mit Containment-
Validierung vor dem Parsing. Es wird kein Live-Bear-, NGINX- oder C++-Build als
ausgeführt dargestellt.

## Validierungsstatus

Für den finalen lokalen Kandidaten besteht die fokussierte Parent-Suite
`tests.test_c_cpp_diagnostics` alle sieben Tests, darunter Controls für
gültigen Capture, fehlenden Root, relative Eingabe, Checkout-Eingabe,
Symlink-Ausbruch, Symlink-Schleife, unsicheren Root, Symlink-Root und
Verify-only. Ausgewählte Syntax-, Shell-Syntax-, Diff- und fokussierte
bilinguale Checks bestehen. Exact-Head-Delivery-Checks werden erst nach ihrer
tatsächlichen Ausführung nach dem Push festgehalten.

## Bekannte Einschränkungen und Follow-up

Kanonische Pfadvalidierung ist kein Descriptor-Level-Schutz gegen ein
gleichberechtigtes Umbenennen nach der Validierung. Die produktiven Wrapper
erzeugen private `mktemp`-Roots, was dieses Risiko wesentlich reduziert; diese
Änderung beansprucht jedoch keinen race-freien Descriptor-Open.

FND-SONAR-0017 hält einen getrennten plausiblen externen `--output`-Read/
Write-Path-Kandidaten fest. Er wurde nicht reproduziert oder als konkrete
Vulnerabilität klassifiziert, und diese inputfokussierte Änderung beansprucht
nicht, ihn zu beheben.

## Verbleibende Risiken

Ein konkurrierender Prozess mit derselben effektiven Benutzerberechtigung kann
Dateien nach der kanonischen Validierung und vor `read_text` weiterhin
umbenennen; Descriptor-begrenztes Öffnen wäre eine getrennte Härtungsänderung.
Das vorhandene externe Output-Argument wird durch diesen PR absichtlich nicht
als sicher umklassifiziert und bleibt bis zur direkten Validierung in
FND-SONAR-0017 nachverfolgt.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine Live-Bear-/NGINX-/C++-Compile-Database-Generierung: Sie erfordert
  Bear, Compiler, NGINX- und ModSecurity-Voraussetzungen sowie ein externes
  Artefakt-Setup; die direkte Python-Grenze und beide Caller-Verträge sind
  ohne diese Abhängigkeiten deterministisch abgedeckt.
- Kein Framework- oder MRTS-Test und keine -Änderung: Beide liegen außerhalb
  dieses Parent-only-Batches.
- `make check-bilingual-docs` wurde ausgeführt, ist aber nur durch fehlende
  Targets im absichtlich nicht initialisierten Framework-Gitlink blockiert und
  wird nicht als bestanden dargestellt. Der gezielte bilinguale Change-Record-
  Test besteht.
- Hosted-Checks, Exact-Head-SonarQube-Cloud-Analyse und Quality Gate stehen
  aus, bis der ungemergte Draft-PR-Branch gepusht ist.

## Delivery-Status

Der Kandidat ist auf einem isolierten Parent-Task-Branch basierend auf aktuellem
master vorbereitet. Er wird nur als ungemergter Draft-PR committed, gepusht
und geöffnet. Kein Merge, Default-Branch-Update oder Framework-/MRTS-Change
ist autorisiert.

## Finaler Diff- und Review-Status

Ein unabhängiges read-only Security-Review bewertete die ausgewählte Input-
Source-to-Sink-Schließung und Caller-Kompatibilität als stimmig und empfahl nur
einen fail-closed `RuntimeError`-Catch für die strikte Path-Resolution; diese
Empfehlung ist enthalten. Der finale lokale Diff und alle benannten lokalen
Validierungsbefehle wurden nach diesem Record-Update erneut geprüft und
bestanden, abgesehen vom getrennt dokumentierten Framework-Gitlink-
Dokumentationsblocker. SonarCloud, Hosted-Checks, PR-Nummer und Quality Gate
stehen aus, bis der exakte Branch-Head gepusht ist.
Die initiale PR-#98-Analyse lief bereits und fand das erforderliche Follow-up
`AZ-QC5_F7_w-jke5-e7_`; das finale Clean-Head-Ergebnis muss nach Push dieses
Refactorings eingeholt werden.
