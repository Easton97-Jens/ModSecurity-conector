# FND-PARENT-0016 — SonarCloud wies die ursprüngliche Traefik-UDS-Härtung zurück, weil Public-Root-Allokation im PR-Pfad lag

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0016` |
| Kategorie | `sonarqube_finding` |
| Repository / Ownership | `parent` / `parent` |
| Priorität | `P1` |
| Severity / Confidence | `high` / `confirmed` |
| Status / Machbarkeit | `fixed` / `feasible_now` |
| Release-Blocker / Security-Relevanz | `true` / `true` |
| Connector / Protokoll / Profil | Traefik / AF_UNIX pathname / native-traefik-middleware |

## Zusammenfassung

Die erste SonarCloud-Analyse des Parent-Draft-PR #51 scheiterte am New-Code-
Security-Rating (D). Direkte rohe PR-Evidence klassifiziert Public-Root-UDS-
Allokation/Fallback-Code, einen generischen geerbten `TMPDIR`-Selector und eine
prozessglobale `umask` als Vulnerabilities. Scanner-sichtbare Test-Negativfälle
und Code-Smells sind task-owned, rechtfertigen jedoch keine Scanner-Suppression
oder automatische Risikoentscheidung. Die finale Implementierung verlangt die
explizite Private-Parent-Variable, und der exakte gepushte PR-Head bestand
SonarCloud ohne Suppression oder Risikoakzeptanz.

## Beobachtetes und erwartetes Verhalten

Check-Run `87922216387` für PR #51/Head
`48198b50357cf24fd59b1aad39d99ef407b3d890` scheiterte, weil
`new_security_rating=4` den A-Schwellenwert überschritt. Der direkte
Issue-Export enthält kritische/hohe `python:S5443`- und `c:S5443`-
Vulnerability-Issues, `c:S5849`, `python:S2612` und zugehörige task-owned
Maintainability-Issues. Runner, Shell-Harness und C-Engine müssen vor
Allokation oder Bind einen bestehenden, absoluten, kanonischen,
current-user-owned, exakt-`0700` und symlinkfreien Socket-Parent verlangen,
dessen vollständige Vorfahrenkette UID-übergreifende Ersetzung verhindert.
Kein Runtime- oder Selbsttestpfad darf still `/tmp` oder `/var/tmp` wählen. Der
Listener verwendet diese verifizierte Directory-Grenze statt einer
prozessglobalen `umask` oder einer Pathname-Berechtigungsbehauptung. Ein Rerun
auf dem aktualisierten exakten PR-Head muss den SonarCloud-New-Code-Security-
Rating-Schwellenwert ohne Suppression oder Risikoakzeptanz erfüllen.

Der erste Post-Remediation-Exact-Head-Check `87949565401` für
`56e35eb5e6ff52e0ec84f08807f767acc890ae9e` schloss 14 task-owned Issues.
Seine eine offene Vulnerability war `python:S5443` am geerbten `TMPDIR`-
Fallback des Python-Runners. Keine Scanner-Kontrolle wurde geändert; der
Source-Follow-up entfernte diesen Fallback.

Der nachfolgende Head `2ad97e0e4c7defd0d7d0aa30b8603d59dacbed85` zeigte
dreizehn task-owned `python:S5443`-Annotations ausschließlich in feindlichen
`/tmp`-Test-Fixture-Werten. Der fokussierte Follow-up leitet diese Werte aus
einem privaten `TemporaryDirectory` ab. Finaler Exact Head
`6e73dc97eba8b503d7d88f7feb3c43ef14132083` bestand SonarCloud-Check
`87978528103` mit null Annotations, null offenen PR-Issues und Quality-Gate-
Status `OK`.

Ein dokumentationsreiner Follow-up erzeugte anschließend den aktuellen
exakten Draft-PR-Head `ef2f5755c29c5bc8f452290a14389fe8822e0709`. Er ändert
nur die bilingualen Change-Record-Indizes, um die unabhängige CodeQL-Record-
Einfügung auf aktuellem `master` konfliktfrei zu halten. SonarCloud-Check
`87983807169` bestand mit Quality Gate `OK`, null ungelösten PR-Issues und
keinen zu prüfenden Hotspots. GitHub meldet diesen Head als Draft und
`MERGEABLE`/`CLEAN`; seine 33 erfolgreichen Check-Runs und sechs
workflow-deklarierten Skips enthalten keinen fehlgeschlagenen, abgebrochenen
oder ausstehenden Run.

Der native Runner akzeptiert nur einen expliziten
`TRAEFIK_ENGINE_SOCKET_PARENT`; er darf keine generische geerbte Temporary-
Directory-Variable wählen.

## Auswirkung

Der exakte Draft-PR-Head erfüllt nun sein externes Security-Gate, aber dieses
Finding bleibt `fixed` statt `verified` oder `closed`, weil keine Master-
Integration autorisiert oder durchgeführt ist. Im Vorzustand könnte ein
privilegierter oder anderweitig sensibler nativer
Runner, der ein angreiferkontrolliertes absolutes `TMPDIR` erbt, ein benanntes
UDS-Child außerhalb der beabsichtigten privaten Grenze erzeugen. Diese
Scanner-Evidence validiert nicht die separaten Same-UID-Endpoint-Umleitungs-
oder Final-Cleanup-Races; sie bleiben `FND-PARENT-0013`, `FND-PARENT-0014`
und `FND-PARENT-0015`.

## Betroffene Dateien und Symbole

- `connectors/traefik/scripts/runtime_native_smoke.py` —
  `resolve_engine_socket_parent`, vollständige Vorfahrenvalidierung.
- `connectors/traefik/src/traefik_engine_service.c` — Selbsttest-Parent,
  Listener-Setup, globaler `umask`-Wrapper.
- `connectors/traefik/build/test-engine-service-runtime.sh` und
  `connectors/traefik/build/build-engine-service.sh` — Test-Parent-Vertrag.
- `tests/test_traefik_native_local_plugin.py` — negative und legitime
  Private-Parent-Kontrollen.
- `ci/runtime/lifecycle/run-connector-stage.sh` und
  `ci/runtime/lifecycle/run-remaining-connector-target.sh` — erhalten den
  vom Aufrufer gelieferten Parent durch den kanonischen nativen Lifecycle-Pfad.
- `connectors/traefik/Makefile` und
  `tests/test_no_crs_selected_runner_wiring.py` — reichen den exakten
  Aufruferwert weiter bzw. prüfen ihn, ohne einen Runtime-Root-Parent zu erzeugen.
- `common/scripts/modsecurity_targeted_eval.cc` — isolierte C++17-
  Maintainability-Anpassung.

## Voraussetzungen und Reproduktion

1. SonarCloud analysiert PR #51 am aufgezeichneten Head.
2. Der Vorzustands-Runner hat keinen ausgewählten privaten Parent, oder der
   C-Selbsttest erbt ein ungeeignetes absolutes `TMPDIR`.
3. Check-Run-Annotations und SonarCloud-Issues-/Quality-Gate-JSON mit den
   exakten retained Befehlen abrufen.
4. Die ehemaligen Public-Fallback/Standard- und globalen-`umask`-Pfade sowie
   anschließend die festen Immediate-Parent- und Vorfahrenkontrollen verfolgen.

## Evidence

- Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`, GitHub-
  Annotationsexport `evidence/draft-pr-51-sonar-annotations.json`, SHA-256
  `96885558996384b6f17e83a5d4452413ef6c2c2ff04b19441f1753aae4cbb2c8`, Log
  `089-draft-pr-51-sonar-annotations.log`, Exit `0`, beobachtet
  `2026-07-17T15:27:12Z`.
- SonarCloud-Issue-Export `evidence/draft-pr-51-sonar-issues.json`, SHA-256
  `361370c72e7d4e965695c823cdac616a3404dcf3fa2f3441d3446fe850317d7c`, Log
  `090-draft-pr-51-sonar-issues.log`, Exit `0`, beobachtet
  `2026-07-17T15:29:31Z`.
- SonarCloud-Quality-Gate-Export
  `evidence/draft-pr-51-sonar-quality-gate.json`, SHA-256
  `b6348c561174b598ec56ec596a106179cb12f4e8c75654fb61b0f7143538debe`, Log
  `091-draft-pr-51-sonar-quality-gate.log`, Exit `0`, beobachtet
  `2026-07-17T15:32:26Z`.
- Finaler fokussierter Python-Contract-Lauf
  `logs/120-private-parent-ancestor-python-contracts-final.log`, SHA-256
  `1bf27a75961e8aec742448899c4e2e648ad1ea4bf6af1fdc9b33440c9d4620f2`,
  16 Tests, Exit `0`, beobachtet `2026-07-17T16:19:10Z`–`16:19:11Z`.
- Clang- und GCC-C17-Selbsttest-Builds (`logs/121` und `122`) bestanden,
  ebenso Mutable-Ancestor-Rejection (`logs/123`), gültige Allow/Blocking-
  Runtime-Kontrolle (`logs/125`), Hardened-Diagnostic-Build (`logs/126`),
  ASan+UBSan-Runtime (`logs/128`) und GCC `-fanalyzer` (`logs/129`). Ihre
  exakten Command-/CWD-/Zeit-/Exit-Records und SHA-256-Werte liegen im aktuellen
  Run und im zugehörigen Record `FND-PARENT-0017` vor.
- Der Follow-up-Exact-Head-Issue-Export
  `evidence/pr-51-head-56e35eb-sonar-issues.json`, SHA-256
  `5561b1461984c8b7375def710bfaca9ac31bf466b24fad750f0c7b1c348e78da`, zeigt
  14 `CLOSED/FIXED` task-owned Issues und die eine verbleibende
  `python:S5443` vor dieser finalen Source-Änderung.
- Die Follow-up-Python-Validierung mit 16 Contracts liegt als
  `logs/144-explicit-private-parent-python-contracts.log`, SHA-256
  `712fa2f1ac323a17d9c569fd8f8396eafceda7f6e28b18df61a6a502580dbc37`, Exit
  `0`, beobachtet `2026-07-17T17:34:11Z`, vor. Die geänderten English/German-
  Paare bestanden die checker-äquivalente fokussierte Dokumentationsvalidierung
  in `logs/148-explicit-private-parent-targeted-bilingual-docs.log`, SHA-256
  `a26471edca192db542c117efe00e6aaae1ed44ea2518e5b2b3d59b6aaa17bdf8`, Exit
  `0`, beobachtet `2026-07-17T17:42:13Z`.
- Die frühere Explicit-Parent-Forwarding-Validierung liegt als
  `logs/150-explicit-parent-forwarding-final-validation.log`, SHA-256
  `139dba675ef96bf6c8c3e0bb2b0624949f208ba5cd14f982933fde80fb244221`,
  Exit `0`, beobachtet `2026-07-17T18:18:17Z`–`18:18:18Z`, vor. Sie
  dokumentiert nur gewöhnliches Explicit-Parent-Forwarding und liegt vor dem
  separat reproduzierten Make-/Shell-Interpretationsdefekt in
  `FND-PARENT-0019`; sie ist keine finale Hostile-Input-Evidence.
- Der synchronisierte Change Record bestand anschließend eine finale Changed-
  Pair-Dokumentationsvalidierung in
  `logs/152-change-record-forwarding-docs-validation.log`, SHA-256
  `2199e4d1cdffede8f66e3a19dabbf3806e5afbddd25719c4d87c59705d878d6b`,
  Exit `0`, beobachtet `2026-07-17T18:26:44Z`–`18:26:45Z`.
- Die Raw-Make-/Environment-Forwarding-Closure ist in
  `logs/159-final-make-raw-forwarding-security-validation.log`, SHA-256
  `faab9a431c6964e40f0aab0731884dd049b22a998935fffa2ff436a05f63e51d`,
  Exit `0`, beobachtet `2026-07-17T18:56:13Z`, erhalten. Sie beweist literale
  direkte Make-Function-Werte für alle vier weitergereichten Variablen, keinen
  Quote/Kommentar-Shell-Sentinel, Python-Rejection vor Runtime-Root-Setup und
  22 fokussierte Contracts. Der getrennte Pre-Validation-Interpretationspfad
  wird als `FND-PARENT-0019` nachverfolgt und repariert.
- Die finale Named-Make-/Environment-Forwarding-Closure ist in
  `logs/160-final-named-make-forwarding-security-validation.log`, SHA-256
  `8be26ef3b432fc17c6bb8a6b6127c7199ebe114d8b5bc0a668fd7b10dcee4d7a`,
  Exit `0`, beobachtet `2026-07-17T19:29:10Z`, erhalten. Sie verifiziert
  literale Behandlung der benannten lifecycle-weitergereichten BUILD_ROOT-,
  MODSECURITY- und Traefik-Werte, keine Marker-Ausführung, Syntax-/Diff-Checks
  und 22 fokussierte Contracts.
- Die finale Exact-Head-Delivery- und SonarCloud-Validierung ist in
  `logs/164-final-exact-pr-head-delivery-and-sonar.log`, SHA-256
  `1a70d77d83673c68017fc466f0fbf8c57bd91fe3145c806568fc908bcd63b7d3`, Exit
  `0`, beobachtet `2026-07-17T19:49:34Z`, erhalten. Sie erfasst den gleichen
  lokalen/Remote-/PR-Head `6e73dc9…`, alle anwendbaren GitHub-Checks,
  SonarCloud-Check `87978528103` mit null Annotations und offenen Issues sowie
  Quality-Gate `OK`.
- Die finale konfliktfreie Draft-PR-Delivery- und SonarCloud-Validierung ist
  in `logs/167-final-conflict-free-draft-pr-delivery-and-sonar.log`, SHA-256
  `22c69a59ee5a962354f360fd1a02ac099d148c5e76a3ccb248761a379b8e1aa7`, Exit
  `0`, beobachtet `2026-07-17T20:18:08Z`, erhalten. Sie erfasst denselben
  lokalen, Remote- und Draft-PR-#51-Head `ef2f575…`, GitHub
  `MERGEABLE`/`CLEAN`, 33 erfolgreiche und sechs workflow-deklarierte
  übersprungene Exact-Head-Runs, SonarCloud-Check `87983807169`, Quality Gate
  `OK`, null ungelöste PR-Issues und keine zu prüfenden Hotspots. Sie bewahrt
  zudem das read-only konfliktfreie Dreiweg-Ergebnis für die bilingualen
  Change-Record-Indizes.

## Grundursachenanalyse und vorgeschlagene Remediation

Der ehemalige Python-Runner behielt automatische `/var/tmp`-Allokation; der
C-Selbsttest akzeptierte geerbtes `TMPDIR` nach einer absoluten Pfadprüfung
und fiel danach auf `/var/tmp` zurück; eine temporäre globale `umask` wurde
für eine Grenze verwendet, deren wirksamer UID-übergreifender Schutz ein
privater Pathname-Parent ist. Die erste Remediation-Review zeigte zusätzlich,
dass Immediate-Parent-only-Validierung ein `0700`-Kind unter einem nicht-sticky
veränderbaren Vorfahren akzeptierte (`FND-PARENT-0017`). Test-Negativfälle und
wiederholte Literale erzeugten zusätzliche Scanner-Befunde. Die erste Exact-
Head-Reanalyse bewies, dass der generische Python-`TMPDIR`-Fallback die einzige
verbleibende aktive Vulnerability war; der finale Source-Follow-up entfernt
daher diesen optionalen Selector statt sich auf eine spätere manuelle
Validierung zu stützen. Der Gate-Fehler ist bestätigt; ob jede Scanner-Issue
eine separat ausnutzbare Produktvulnerability darstellt, bleibt durch die
benannte Source-/Runtime-Evidence begrenzt.

Sobald der Runner strikt wurde, musste auch die unterstützte Dispatcher- und
Make-Aufrufkette diese vom Aufrufer gelieferte Grenze erhalten. Einen neuen
Parent unter dem kanonischen Runtime- oder Temporary-Root abzuleiten würde das
100-Byte-UDS-Pfadbudget überschreiten und ist deshalb weder ein sicherer
Fallback noch eine kompatible Reparatur.

Public-Root-/Standardallokation wird durch explizit bereitgestellte bestehende
private Parents ersetzt. Absolute, kanonische, current-user-owned, exakt-
`0700` und symlinkfreie Checks sowie eine UID-übergreifend sichere
Vorfahrenkette werden im Runner, C-Listener, C-Selbsttest und Shell-Harness
erzwungen. Globale `umask`-Abhängigkeit entfällt und Pathname-
Berechtigungsbehauptungen werden vermieden. Fail-Closed-Verhalten bleibt
erhalten und für zugehörige Maintainability-Punkte sind nur
verhaltensbewahrende task-owned Refactors zulässig.
Die finale Runner-Auswahl verlangt nur `TRAEFIK_ENGINE_SOCKET_PARENT` und
erbt kein `TMPDIR`. Der zentrale Dispatcher und das native Make-Target
reichen nur den exakten expliziten Wert des Aufrufers weiter; sie leiten keinen
Wert unter einem Runtime- oder Temporary-Root ab.

## Akzeptanzkriterien und Validierung

- Kein Produktions-Runner und kein C-Selbsttest allokiert still unter `/tmp`
  oder `/var/tmp`.
- Der Produktions-Runner akzeptiert keinen generischen geerbten Temporary-
  Directory-Fallback; er verlangt `TRAEFIK_ENGINE_SOCKET_PARENT` vor dem
  Host-Setup.
- Der kanonische Dispatcher und das native Make-Target erhalten nur den exakten
  expliziten Parent des Aufrufers; keiner leitet einen unter einem Runtime- oder
  Temporary-Root ab.
- Fehlende, relative, symlinkte, fremdbesessene oder nicht-`0700` Parents
  scheitern vor Allokation/Bind; ein gültiger privater Parent gelingt.
- Die verifizierte Immediate-Parent-/Vorfahren-Grenze ist die UID-
  übergreifende Kontrolle; kein globaler `umask`-Wrapper oder Pathname-
  Berechtigungsanspruch bleibt.
- Fokussierte Python-Contracts, C17-Build/Selbsttest/Runtime-Allow/Blocking-
  Controls und C++-Evaluator-Checks bestehen.
- Der aktualisierte exakte PR-Head erfüllt den SonarCloud-Security-
  Schwellenwert ohne Suppression, Konfigurationsänderung oder Risikoakzeptanz.

Die Validierung umfasst statische Assertions für den Private-Parent-Vertrag,
fokussierte Python-Controls, C17-Warnings-as-Errors, C-Selbsttest und native
UDS-Protokoll-Controls, C++17-Evaluator-Kompilierung/Diagnostics/Allow/
Blocking sowie die Roh-Issues und das Quality-Gate des gepushten exakten PR-
Heads. Relevante Tests sind `tests/test_traefik_native_local_plugin.py`, die
zwei Traefik-Build/Runtime-Skripte, `check-targeted-evaluator-cpp17.sh` und
`tests/test_c_cpp_diagnostics.py`. Legitime Kontrollen verlangen einen gültigen
privaten Parent mit sicherer Vorfahrenkette, SO_PEERCRED-Selbstprobe, Allow
`200` und Blocking `403`.

Zusätzlich prüfen Shell-Syntax, nativer Make-Dry-Run und Lifecycle-Wiring-
Controls die unveränderte Weitergabe des vom Aufrufer gelieferten Parents ohne
einen generierten Temporary-Root-Parent.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Der exakte gepushte PR-Head bestand seine SonarCloud-Analyse. Es gibt keinen
aktuellen Implementierungsblocker; Post-Merge-Master-Verifikation erfordert
separate Autorisierung. Verwandte Findings sind `FND-PARENT-0013`,
`FND-PARENT-0014`, `FND-PARENT-0015`,
`FND-PARENT-0017`, `FND-PARENT-0019` und `FND-SONAR-0001`. Diese Arbeit kann
die Same-UID-Pathname-Endpoint-Umleitungs- oder nichtatomaren Cleanup-Races
nicht allein lösen. Es wurde kein Risiko akzeptiert.

## Historie

Die frühere nicht feindliche Forwarding-Validierung liegt vor dem separat
reproduzierten Make-/Shell-Interpretationsfinding FND-PARENT-0019. Seine
Hostile-Input-Closure-Evidence ist Log 159: alle vier Raw-Make-Werte blieben
literal, der Quote/Kommentar-Sentinel fehlte, Python scheiterte fail closed,
und 22 fokussierte Contracts bestanden.

- `2026-07-17T15:35:00Z`: Direkte GitHub- und SonarCloud-Rohexporte
  bestätigten einen PR-Head-Security-Rating-D-Gate-Fehler. Aktive Remediation
  begann; weder Scanner-Regel noch Quality-Gate-Konfiguration oder
  Risikodisposition wurden geändert.
- `2026-07-17T16:58:45Z`: Lokale Remediation ist nach fokussierten Python-,
  C17-, Shell-/Runtime-, Hardened-, ASan+UBSan- und GCC-Analyzer-Kontrollen
  fixed. Exakte Head-SonarCloud-Reanalyse bleibt vor Verifikation erforderlich.
- `2026-07-17T17:42:13Z`: Exact-Head-Check `87949565401` zeigte, dass nur der
  generische Python-`TMPDIR`-Selector offen blieb; der finale Source-Follow-up
  entfernte ihn. Sechzehn fokussierte Python-Contracts und die Changed-Pair-
  Bilingual-Validierung bestanden. Das Finding bleibt lokal `fixed`, bis eine
  neue Exact-Head-SonarCloud-Reanalyse vorliegt.
- `2026-07-17T18:18:18Z`: Der kanonische Stage-Dispatcher, Remaining-Target-
  Runner und das native Make-Target wurden auf die Weitergabe nur des
  aufrufergelieferten expliziten Parents verdrahtet. Die frische 22-Contract-/
  Syntax-/Dokumentations-/Make-Dry-Run-Validierung bestand; ein aus dem
  kanonischen Runtime- oder Temporary-Root abgeleiteter Parent wurde bewusst
  verworfen, weil er das UDS-Pfadbudget überschreiten würde.
- `2026-07-17T18:26:45Z`: Der bilinguale Change Record wurde mit der
  finalen Forwarding-Validierung synchronisiert, und sein ausgewählter Changed-
  Pair-Checker-Rerun bestand. Das Finding bleibt lokal `fixed`, bis eine
  neue Exact-Head-SonarCloud-Reanalyse vorliegt.
- `2026-07-17T18:56:13Z`: Das frühere Log 150 wurde als nur nicht feindliche
  Forwarding-Evidence reklassifiziert. `FND-PARENT-0019` dokumentiert den
  separat reproduzierten Make-/Shell-Interpretationsdefekt; Raw-Environment-
  Forwarding und fokussierte Hostile-Input-Controls bestanden in Log 159. Das
  Finding bleibt lokal `fixed`, bis eine Exact-Head-SonarCloud-Reanalyse
  vorliegt.
- `2026-07-17T19:29:10Z`: Die finalen benannten Make-/Environment-Controls
  deckten BUILD_ROOT, die lifecycle-weitergereichten MODSECURITY-Werte und die
  Traefik-Werte ohne Marker-Ausführung ab. Die gemeinsame Interpretationsgrenze
  bleibt durch `FND-PARENT-0019` nachverfolgt; dieses Finding bleibt lokal
  `fixed`, bis eine Exact-Head-SonarCloud-Reanalyse vorliegt.
- `2026-07-17T19:49:34Z`: Exact Draft PR #51 Head
  `6e73dc97eba8b503d7d88f7feb3c43ef14132083` bestand SonarCloud-Check
  `87978528103` mit null Annotations, null offenen PR-Issues und Quality-Gate
  `OK`. Der fokussierte `TemporaryDirectory`-Fixture-Follow-up entfernte die
  13 zwischenzeitlichen test-only-S5443-Annotations ohne Suppression oder
  Risikoakzeptanz. Das Finding bleibt `fixed`, bis eine separat autorisierte
  Post-Merge-Master-Verifikation erfolgt.
- `2026-07-17T20:18:08Z`: Der dokumentationsreine Konflikt-Follow-up erzeugte
  den exakten Draft-PR-#51-Head `ef2f5755c29c5bc8f452290a14389fe8822e0709`
  ohne Rebase oder Merge. Lokaler/Remote-/PR-Head stimmten überein, GitHub
  meldete `MERGEABLE`/`CLEAN`, alle 33 anwendbaren Checks bestanden mit sechs
  deklarierten Skips, und SonarCloud-Check `87983807169` lieferte Quality Gate
  `OK`, null ungelöste PR-Issues und keine zu prüfenden Hotspots. Das Finding
  bleibt `fixed` bis zur separat autorisierten Post-Merge-Master-Verifikation.
