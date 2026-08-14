# FND-PARENT-0129 — Gepatchter Lighttpd-Core-Build verlangt manuellen Autotools-Bootstrap, wenn dem verifizierten 1.4.84-Release configure fehlt

| Feld | Wert |
| --- | --- |
| ID / Source-Input | `FND-PARENT-0129` / `F-GS-002` |
| Kategorie | `build_defect` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Severity | `P1` / `not_applicable` |
| Confidence / Status | `validated` / `in_progress` |
| Machbarkeit | `blocked_external_dependency` |
| Release-Blocker / Candidate-Integration-Blocker | ja / nein |
| Security-relevant | ja; Source-/Bootstrap-Ausführungsgrenze, kein Exploit behauptet |

## Zusammenfassung

Dem gepinnten, verifizierten Lighttpd-`1.4.84`-Release kann ein generiertes
ausführbares `configure` fehlen. Der bisherige gepatchte Core-Builder stoppte
vor der Konfiguration, obwohl die aufbewahrte Analyse zeigte, dass ein
task-lokales `sh autogen.sh` den realen Core- und Host-Build ermöglichte. Die
Source-Korrektur fügt dieselbe Entscheidung dem Builder hinzu: ausführbares
`configure` weiterverwenden; andernfalls nur die disponierbare gepatchte
Source-Kopie bootstrappen und danach ein ausführbares Ergebnis verlangen. Sechs
Real-Skript-Contract-Szenarien und generierte englische/deutsche Guide-Checks
bestehen. Das Finding bleibt `in_progress`: Der zugelassene Speicher enthält
keinen verifizierten `1.4.84`-Tree und kein Archiv für den erforderlichen
finalen sauberen Core-/Host-Nachweis, und kein Netzwerk-Workaround ist
autorisiert.

## Beobachtetes und erwartetes Verhalten

Der analysis-only-Record
`.codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/`
zeichnet den ursprünglichen blockierten Build aus einer verifizierten Source,
gefolgt von erfolgreichem task-lokalem `sh autogen.sh`, Core-Build und Host-
Build auf. Der alte Builder besaß nur eine Sperre für ausführbares `configure`.

Nach bestehender Source-Validierung und Patch-Anwendung muss vorhandenes
ausführbares `configure` weiterverwendet werden. Andernfalls muss `autogen.sh`
in der gepatchten Kopie vorhanden sein und dort laufen. Ein ausführbares Skript
läuft direkt; ein nicht ausführbares Skript wird nur mit exakter erster Zeile
`#!/bin/sh` oder `#!/usr/bin/env sh` durch `sh` akzeptiert. Fehlendes Skript,
nicht unterstützter Interpreter, Bootstrap-Fehler oder nicht ausführbares
generiertes `configure` stoppen vor Core-Build-Output mit präziser Exit-77-
Diagnose.

## Auswirkung und Security-Bewertung

Der frische gepatchte Lighttpd-Core-/Host-Build war ohne manuellen Eingriff
nicht reproduzierbar. Dies ist eine P1-Release-Build-Grenze, kein nachgewiesener
Exploit. Der geänderte Pfad führt ein Upstream-gepflegtes Bootstrap-Skript aus
und ist deshalb sicherheitsrelevant: Bootstrap bleibt auf die gepatchte
disponierbare Kopie begrenzt; die originale verifizierte Source wird nicht
verändert; es wurden keine Paketinstallation, Netz-Aktion, Hash-Änderung,
Modus-Änderung oder ignorierten Fehler eingeführt.

Security-Invariante: Nach bestehender Source-Validierung und Patch-Anwendung
läuft Bootstrap nur innerhalb des disponierbaren gepatchten Trees; er muss die
Original-Source bewahren, darf keinen Installer-/Netzwerkschritt ausführen,
muss Fehler sichtbar machen und ausführbares `configure` vor Erzeugung von
Core-Output produzieren.

## Betroffene Dateien und Symbole

- `connectors/lighttpd/build/build_patched_core.sh`: `run_autogen` und
  `ensure_configure`.
- `connectors/lighttpd/tests/test_patched_host_contract.py`: sechs
  Real-Skript-Bootstrap-Szenarien.
- `scripts/generate_compiler_guides.py` sowie generierte
  `docs/build/compilers/lighttpd.md` / `.de.md`: dieselbe explizite Entscheidung.
- `tests/test_compiler_guides.py`: Regression der generierten Dokumentation.

## Voraussetzungen und Reproduktion

1. Der Aufrufer stellt absolute externe `LIGHTTPD_SOURCE_DIR` mit verifizierter
   Lighttpd-`1.4.84`-Source bereit.
2. Die bestehende Patch-Anwendung kopiert diese Source in den verwalteten
   externen gepatchten Root.
3. Der Upstream-Tree enthält ausführbares `configure` oder ein `autogen.sh`,
   das es mit seinen deklarierten Werkzeugen erzeugen kann.
4. `make -C connectors/lighttpd check-lighttpd-patched-host` mit sauberem
   privatem `BUILD_ROOT` ausführen. Vor dieser Korrektur blockiert die Source
   ohne configure; danach bootstrappt die gepatchte Kopie und Core/Host sind
   erfolgreich.

## Nachweise

- Ursprünglicher Fehler und manueller Bootstrap-Erfolg:
  `.codex/analysis/general-state/20260814T083829Z-ea3b48a/findings/F-GS-002/artifacts/build-observation.json`,
  SHA-256 `ccb6ed179d61f716e5035fbed0376469432a98233da96966621c7f310cbd117c`.
- Lokales Remediation-Receipt:
  `.codex/runs/20260814T115110Z-f-gs-002-autogen-bootstrap/evidence/validation.md`,
  SHA-256 `e4e16d93f787ef22e954abf33051ca72e60446662d8aa5d0f4751726fe796cbc`.
  Es dokumentiert die aktuellen 26 Patched-Host-Contract-Tests, vier
  Lighttpd-Guide-Controls, die vollständige 21-Test-Compiler-Guide-Suite,
  bilinguale Dokumentation, Doc-Links, Shell-Checks, JSON-Parsing und den
  Diff-Check als bestanden. `LIGHTTPD_SOURCE_DIR` ist nicht gesetzt; der
  frühere Target-Versuch stoppte fail closed an der fehlenden Eingabe (Make
  Exit `2`, zugrunde liegender Builder Exit `77`), nicht an einem realen
  Source-Core-/Host-Ergebnis.

## Root Cause und Remediation

Der bisherige Builder setzte generiertes `configure` in der kopierten,
gepatchten Source voraus, obwohl das gepinnte Release es auslassen kann. Die
Korrektur ergänzt einen engen Bootstrap-Schritt nach bestehender Patch-/Stamp-
Verifikation und vor dem ersten Configure-Aufruf. Bei Fehler schreibt sie
begrenzte `autogen.log`-Ausgabe und verlangt ausführbares `configure`, bevor
`mkdir` das Core-Build-Verzeichnis erzeugt. Sie rät keine Autotools-
Subcommands: Upstream-`autogen.sh` bleibt maßgeblich.

## Akzeptanzkriterien und Validierungsplan

1. Vorhandenes ausführbares `configure` überspringt `autogen.sh`.
2. Fehlendes `configure` bootstrappt nur die gepatchte Kopie, einschließlich
   eines nicht ausführbaren Skripts mit exaktem POSIX-Shebang.
3. Fehlendes Skript, fehlgeschlagener Bootstrap, nicht unterstützter
   Interpreter und fehlendes generiertes `configure` stoppen fail closed,
   bevor Core-Output existiert.
4. Original-Source, Patch-/Hash-Controls und No-Install-/No-Network-Policy
   bleiben erhalten; englische/deutsche Anweisungen bleiben synchron.
5. Mit bereitgestellter verifizierter Source bestehen ein frischer realer Core-
   und Host-Build sowie ein Wiederholungslauf mit Reuse, mit aufbewahrter Raw-
   Evidence.

Der nächste erforderliche Control ist ein sauberer externer Source-Build unter
neuem privatem `BUILD_ROOT`, der stdout, stderr, Exit-Code, `autogen.log`,
Patch-/Core-Manifeste, gestagtes Binary und Host-Manifest aufbewahrt.
Anschließend alle fokussierten Tests sowie Dokumentations-/Static-Checks erneut
ausführen.

## Regressionen und legitime Controls

Der fokussierte Builder-Test deckt vorhandenes configure, fehlendes configure
mit POSIX-nicht-ausführbarem autogen, nicht ausführbares configure, beide
fehlenden Dateien, Bootstrap-Fehler, fehlendes generiertes configure, nicht
unterstützten Interpreter und Repeat-Reuse ab. Die aktuellen vier gezielten
Lighttpd-Generator-Controls, die vollständige
`make check-compiler-guides`-Suite, Shell-Syntax, ShellCheck, bilinguale
Dokumentation, Doc-Links, JSON-Parsing und `git diff --check` bestanden. Eine
bereitgestellte reale Source muss weiterhin Patch-Identität, Binary-Version,
Hook-Symbole, Host-Konstruktion, Original-Source-Erhalt, keinen Netzwerkschritt
und keinen zweiten Bootstrap beim Reuse belegen.

## Abhängigkeiten, Blocker und Restrisiko

Der finale Nachweis hängt von einer vom Aufrufer bereitgestellten verifizierten
Lighttpd-`1.4.84`-Source oder einer separat genehmigten verifizierten Archiv-
Extraktion ab. Das versprochene absolute `LIGHTTPD_SOURCE_DIR` ist nicht
gesetzt, und die gezielte lokale Suche fand keinen passenden Tree/kein Archiv;
der Nutzer untersagte einen Netzwerk-Akquisitionsschritt. Dieses Finding nicht
als fixed, verified oder closed bezeichnen, bis der reale saubere
Core-/Host-/Reuse-Control besteht. `FND-PARENT-0090` zitiert ein anderes
historisches `F-GS-002` aus einer 2026-08-02-HAProxy/libModSecurity-
Abhängigkeitsgrenze; es ist kein Duplikat dieses Lighttpd-Records.

## Historie

- `2026-08-14T11:58:05Z`: Die Bootstrap-Entscheidung in der gepatchten Kopie,
  sechs Szenario-Controls und bilinguale generierte Dokumentation wurden
  implementiert. Das tatsächliche Host-Target begann seine Core-Voraussetzung,
  stoppte aber an der beabsichtigten Sperre fehlendes `LIGHTTPD_SOURCE_DIR`;
  kein unsicherer Workaround wurde verwendet.
- `2026-08-14T12:15:11Z`: Explizite Controls für nicht ausführbares
  `configure` und einen nicht unterstützten Interpreter wurden ergänzt. Alle
  26 fokussierten Contract-Tests, Shell-Syntax und ShellCheck bestanden; nur
  der zugelassene Real-Source-Core-/Host-Nachweis bleibt blockiert.
- `2026-08-14T12:48:43Z`: Die 26-Test-Contract-Suite, vier
  Lighttpd-spezifische Guide-Controls, vollständige Compiler-Guide-Suite,
  bilinguale Dokumentation, Doc-Links, Shell-Checks, JSON-Parsing und
  Diff-Check wurden erfolgreich wiederholt. Die erforderliche Source-Eingabe
  fehlte weiterhin; daher werden Fresh-/Core-/Host-/Reuse-E2E und der
  Original-Source-Fingerprint nicht behauptet und der Status bleibt
  `in_progress`.
