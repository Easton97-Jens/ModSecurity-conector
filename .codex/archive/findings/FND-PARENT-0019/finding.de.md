# FND-PARENT-0019 — Das native Traefik-Make-Rezept wertete aufrufergesteuerten Socket-Parent-Text vor der Runner-Validierung aus

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0019 |
| Kategorie | security_validated |
| Repository / Ownership | parent / parent |
| Priorität | P1 |
| Severity / Confidence | medium / confirmed |
| Status / Machbarkeit | fixed / feasible_now |
| Release-Blocker / Security-Relevanz | true / true |
| Connector / Protokoll / Profil | Traefik / GNU-Make-zu-POSIX-Shell-Weiterleitung vor AF_UNIX-Pathname-Validierung / native-traefik-middleware |

## Zusammenfassung und Auswirkung

Die erste Implementierung der expliziten Private-Parent-Weiterleitung setzte
aufrufergesteuerte Werte in Shell-Assignment-Text des nativen Traefik-Make-
Rezepts ein. Ein Quote-und-Kommentar-Socket-Parent-Payload brach die
Assignment-Quotierung und wurde vor runtime-native-middleware.sh sowie dem
Python-Private-Parent-Validator ausgeführt.

Dies demonstriert lokale/direkte oder Automation-Caller-Codeausführung im
sicherheitsrelevanten nativen Target. Es wurde kein Repository-Workflow
nachgewiesen, der eine nicht vertrauenswürdige Remote-Anfrage in diese
Variablen abbildet; Remote-Ausnutzung und weitergehende Privilegienauswirkung
werden daher nicht behauptet.

## Beobachtetes und erwartetes Verhalten

Vor der Reparatur erzeugte das Rezept ein Socket-Parent-Shell-Assignment aus
einer Make-Variablen. Das kontrollierte Payload /tmp/unsafe"; printf
MAKE_INJECTION_REACHED; # führte printf aus und verhinderte den Wrapper-Aufruf.
Direkte Make-Kommandozeilenwerte mit $(shell ...) benötigen ebenfalls
Raw-Transport, damit Make sie nicht vor dem Child-Prozess auswerten kann.

TRAEFIK_BIN, TRAEFIK_NATIVE_RUNTIME_ROOT, TRAEFIK_ENGINE_SOCKET_PARENT,
PYTHON, BUILD_ROOT, MODSECURITY_INCLUDE_DIR, MODSECURITY_LIB_DIR und
MODSECURITY_PREFIX müssen die betroffenen Grenzen als rohe Prozess-Environment-
Daten passieren. Ein gültiger ausgewählter privater Parent bleibt unverändert.
Ein ungültiger oder bösartiger Parent erreicht den Python-Runner als Literal
und scheitert vor Runtime-Root-Setup oder UDS-Allokation fail closed.

## Betroffene Dateien und Symbole

- connectors/traefik/Makefile — runtime-smoke-traefik-native, test-engine-
  service und Raw-Export-Grenze für benannte betroffene Werte.
- ci/runtime/lifecycle/run-connector-stage.sh — explizite Socket-Parent-
  Environment-Weiterleitung in den Remaining-Target-Runner.
- ci/runtime/lifecycle/run-remaining-connector-target.sh — Grenze von
  run_remaining_connector und des run_make_target-Aufrufs.
- connectors/traefik/scripts/runtime-native-middleware.sh — nativer Wrapper,
  der das rohe Environment empfängt.
- connectors/traefik/build/test-engine-service-runtime.sh — fokussiertes
  Engine-Service-Skript, das das rohe PYTHON-Environment empfängt.
- connectors/traefik/scripts/runtime_native_smoke.py — strikte Private-
  Parent-Validierung vor Runtime-Root-Setup.
- tests/test_no_crs_selected_runner_wiring.py — statische und echte Make-
  Forwarding-Controls.

Betroffene Symbole sind runtime-smoke-traefik-native, run_remaining_connector,
run_make_target, TRAEFIK_ENGINE_SOCKET_PARENT, TRAEFIK_BIN,
TRAEFIK_NATIVE_RUNTIME_ROOT, PYTHON, BUILD_ROOT, MODSECURITY_INCLUDE_DIR,
MODSECURITY_LIB_DIR, MODSECURITY_PREFIX und test-engine-service.

## Voraussetzungen und Reproduktion

1. Ein direkter lokaler Aufrufer oder Automation-Kontext kann
   TRAEFIK_ENGINE_SOCKET_PARENT oder eine andere Native-Target-Make-Variable
   setzen.
2. Das verwundbare native Make-Rezept läuft vor dem nachgelagerten Python-
   Validator.
3. Das Pre-Fix-Target mit einem Quote/Kommentar-Socket-Parent-Payload
   ausführen; Logs 154 und 155 bewahren die gerenderte und tatsächliche
   kontrollierte Ausführungs-Evidence.
4. Das reparierte Target mit literalen Make-Function-Werten für jeden benannten
   betroffenen Wert und mit dem Quote/Kommentar-Control ausführen;
   kein Marker oder Sentinel darf laufen und der Runner muss sein BLOCKED-
   Ergebnis liefern.

## Grundursache

Die erste Forwarding-Reparatur interpolierte Make-Variablen in Shell-Source,
sodass die Recipe-Shell Aufrufertext vor der Private-Parent-Validierung parste.
Direkte Make-Kommandozeilenassignments können ebenfalls eingebettete Make-
Syntax freilegen. Python-Validierung kann Daten nicht schützen, die Make oder
die Shell bereits interpretiert haben.

## Reparatur und Validierung

Das native Target friert jeden benannten betroffenen Wert mit GNU-Make-Raw-
Value-Transport ein, exportiert ihn und startet den Wrapper ohne Inline-Recipe-
Assignments. Der Lifecycle-Target-Runner exportiert seine Traefik-Binary- /
Runtime-Root- und MODSECURITY-Werte, statt sie als Make-Kommandozeilenassignments
zu übergeben. Das test-engine-service-Target startet sein Skript ebenfalls ohne
Inline-PYTHON-Assignment. Die bestehende strikte Python-Private-Parent-
Validierung bleibt die fail-closed Durchsetzungsgrenze.

Wenn kein Aufrufer TRAEFIK_NATIVE_RUNTIME_ROOT bereitstellt, wird das
repository-owned Suffix aus einem eingefrorenen rohen BUILD_ROOT-Wert
zusammengesetzt. Ein vom Aufrufer bereitgestellter Runtime-Root-Wert bleibt
dagegen literal, sodass die Security-Reparatur den gültigen Standard nicht in
einen unaufgelösten Make-Ausdruck verwandelt oder aktive Syntax in einem
BUILD_ROOT-Kommandozeilenwert auswertet.

- logs/154-make-parent-shell-injection-pre-fix-reproduction.log, SHA-256
  8a66165ca568d84aa5d7e9d923dc532c0ecde915bd276962ad5d6af321b1f1ee, Exit 0,
  beobachtet 2026-07-17T18:30:50Z: das Pre-Fix-Rezept zeigt die kontrollierte
  Quote/Kommentar-Injektion.
- logs/155-make-parent-shell-injection-controlled-runtime-reproduction.log,
  SHA-256 4e4b6b5c78456dbd201b25519c6ecce5d3ea870c83fb5d549379290cb8e820f7,
  Exit 0, beobachtet 2026-07-17T18:31:38Z: kontrollierte printf-Ausführung
  erfolgte vor Python-Validierung.
- logs/159-final-make-raw-forwarding-security-validation.log, SHA-256
  faab9a431c6964e40f0aab0731884dd049b22a998935fffa2ff436a05f63e51d, Exit 0,
  beobachtet 2026-07-17T18:56:13Z: alle vier literalen $(shell ...)-Werte
  blieben ohne Marker literal; ein Quote/Kommentar-Payload erzeugte keinen
  Sentinel, erreichte Python literal, lieferte BLOCKED/Make Error 77 und
  erzeugte keinen Runtime-Root; 22 fokussierte Native-/Lifecycle-Contracts
  bestanden.
- logs/160-final-named-make-forwarding-security-validation.log, SHA-256
  8be26ef3b432fc17c6bb8a6b6127c7199ebe114d8b5bc0a668fd7b10dcee4d7a, Exit 0,
  beobachtet 2026-07-17T19:29:10Z: alle acht benannten Werte (BUILD_ROOT, die
  drei MODSECURITY-Werte und die vier Traefik-Werte) blieben ohne Marker
  literal; der Standard-Runtime-Pfad blieb korrekt; der test-engine-service-
  Dry-Run renderte kein feindliches PYTHON-Assignment; Diff-/Shell-Checks und
  22 fokussierte Contracts bestanden.
- logs/164-final-exact-pr-head-delivery-and-sonar.log, SHA-256
  1a70d77d83673c68017fc466f0fbf8c57bd91fe3145c806568fc908bcd63b7d3, Exit 0,
  beobachtet 2026-07-17T19:49:34Z: Exact Draft PR #51 Head `6e73dc9…` stimmte
  mit lokalem und Remote-Stand überein; alle anwendbaren GitHub-Checks und
  SonarCloud-Check `87978528103` bestanden mit null Annotations, null offenen
  PR-Issues und Quality Gate `OK`.
- logs/167-final-conflict-free-draft-pr-delivery-and-sonar.log, SHA-256
  `22c69a59ee5a962354f360fd1a02ac099d148c5e76a3ccb248761a379b8e1aa7`, Exit
  `0`, beobachtet `2026-07-17T20:18:08Z`: der dokumentationsreine aktuelle
  Exact Draft PR #51 Head `ef2f575…` stimmte mit lokalem und Remote-Stand
  überein; GitHub meldet Draft `MERGEABLE`/`CLEAN`; 33 Exact-Head-Check-Runs
  bestanden und sechs deklarierte Runs wurden übersprungen. SonarCloud-Check
  `87983807169` bestand mit Quality Gate `OK`, null ungelösten PR-Issues und
  keinen zu prüfenden Hotspots.

Die Regression-Suite besteht aus tests/test_no_crs_selected_runner_wiring.py
und tests/test_traefik_native_local_plugin.py. Legitime Controls erhalten
einen sicheren direkten Parent bytegenau und den normalen
Valid-Private-Parent-Pfad.

## Validierungsplan und Tests

1. Fokussierte Lifecycle-/Wiring-Tests mit Safe-Parent-, Quote/Kommentar- und
   Make-Function-Controls ausführen.
2. Einen echten nativen Make-Quote/Kommentar-Control ausführen und prüfen,
   dass kein Sentinel entsteht.
3. Direkte Make-Function-Controls für jeden benannten betroffenen Wert
   ausführen und prüfen, dass sie literal bleiben.
4. Prüfen, dass der Standard-Runtime-Root ohne Aufruferwert aus einem sicheren
   BUILD_ROOT aufgelöst wird und ein bösartiger BUILD_ROOT-Kommandozeilenwert
   literal bleibt; anschließend Exact-Head-Evidence für Draft PR #51 nach dem
   Push einholen.

## Akzeptanzkriterien, Abhängigkeiten und Restrisiko

- Keine aufrufergesteuerte Inline-Shell-Interpolation bleibt in einem
  gehärteten Traefik-Rezept.
- Jeder benannte betroffene Wert verwendet Raw-GNU-Make-Transport und
  Environment-Export.
- Literale $(shell ...)-Werte in benannten betroffenen Eingaben führen keine
  Make-Funktion aus.
- Ein Quote/Kommentar-Parent hat keinen Shell-Effekt und scheitert vor dem
  Runtime-Root-Setup in Python fail closed.
- Ohne aufruferbereitgestellten Runtime-Root wird der repository-owned
  BUILD_ROOT-Standard ohne Auswertung bösartiger Make-Syntax zum normalen
  Runtime-Pfad aufgelöst; ein aufruferbereitgestellter Root bleibt raw.
- Keine Scanner-Suppression, Risikoakzeptanz, Framework-/MRTS-Änderung, H3-
  Arbeit oder Merge wird eingeführt.

Exact-Head-Draft-PR-#51- und SonarCloud-Verifikation bestanden für
`6e73dc97eba8b503d7d88f7feb3c43ef14132083`, einschließlich der getrennten
Delivery-Abhängigkeit FND-PARENT-0016. Post-Merge-Master-Verifikation liegt
außerhalb der aktuellen Autorisierung. Verwandte Findings sind FND-PARENT-0016
und FND-PARENT-0017. Diese Reparatur löst nicht
die Same-UID-UDS-Pathname-Risiken in FND-PARENT-0013 bis FND-PARENT-0015; es
wird kein Risiko akzeptiert. Sie behauptet nicht, die GNU-Make-Behandlung
beliebiger nicht verwandter Kommandozeilenvariablen zu ändern.

Der aktuelle exakte Draft-PR-#51-Head ist
`ef2f5755c29c5bc8f452290a14389fe8822e0709`; sein dokumentationsreiner
Konflikt-Follow-up ist ohne Rebase oder Merge `MERGEABLE`/`CLEAN` und
wiederholte den Exact-Head-GitHub-/SonarCloud-Pass. Post-Merge-Master-
Verifikation liegt weiterhin außerhalb der aktuellen Autorisierung.

## Historie

- 2026-07-17T18:30:50Z: kontrollierte Pre-Fix-Recipe-Injektion beobachtet.
- 2026-07-17T18:31:38Z: kontrollierte Shell-Ausführung vor Python-
  Validierung bestätigt.
- 2026-07-17T18:56:13Z: Raw-Make-Transport, literale fail-closed-Behandlung
  und fokussierte Controls bestanden.
- 2026-07-17T19:29:10Z: Die benannten lifecycle-MODSECURITY-Werte, der
  BUILD_ROOT-Standard und das benachbarte test-engine-service-PYTHON-Rezept
  wurden gehärtet und durch finale Literal-Value-Controls abgedeckt.
- 2026-07-17T19:49:34Z: Exact Draft PR #51 Head `6e73dc9…` stimmte mit
  lokalem und Remote-Stand überein; alle anwendbaren GitHub-Checks und
  SonarCloud-Check `87978528103` bestanden mit null Annotations, null offenen
  PR-Issues und Quality Gate `OK`. Das Finding bleibt `fixed`, bis eine
  separat autorisierte Post-Merge-Master-Verifikation erfolgt.
- 2026-07-17T20:18:08Z: Der dokumentationsreine Konflikt-Follow-up erzeugte
  den exakten Draft-PR-#51-Head `ef2f575…` ohne Rebase oder Merge. GitHub
  meldet ihn als Draft `MERGEABLE`/`CLEAN`; 33 Checks bestanden mit sechs
  deklarierten Skips, und SonarCloud-Check `87983807169` lieferte Quality Gate
  `OK`, null ungelöste PR-Issues und keine zu prüfenden Hotspots. Das Finding
  bleibt `fixed` bis zur separat autorisierten Post-Merge-Master-Verifikation.
