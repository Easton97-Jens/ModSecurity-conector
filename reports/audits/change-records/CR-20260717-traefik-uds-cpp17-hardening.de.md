# Change Record: Traefik-UDS- und C++-Evaluator-Härtung

**Status:** Die lokale Remediation und die fokussierte Validierung sind
abgeschlossen. Die Delivery-Disposition bleibt ein Parent-only-Draft-PR ohne
Merge. SonarCloud lehnte den ersten Draft-PR-Head mit Security Rating D ab; die
abgegrenzte Folge-Revision wartet auf ihre eigene exakte Head-Analyse.

**Sprache:** [English](CR-20260717-traefik-uds-cpp17-hardening.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260717-traefik-uds-cpp17-hardening` |
| Datum (UTC) | `2026-07-17` |
| Basis-Revision | `02f9f98cdbbdd70bbc530ac1399974e53884f4e9` |
| Scope | Nur Parent-Repository |
| Zugehörige Findings | `FND-FRAMEWORK-0008`, `FND-PARENT-0012`, `FND-PARENT-0013`, `FND-PARENT-0014`, `FND-PARENT-0015`, `FND-PARENT-0016`, `FND-PARENT-0017` |

## Motivation und Problemstellung

Der native Traefik-Smoke-Runner konnte einen zu langen Unix-Domain-Socket-Pfad
erzwingen und bot keine validierte Auswahl eines kurzen Parents. Sein UDS-
Lebenszyklus benötigte außerdem explizite Kontrollen für Collision, Pfad,
Identity und Cleanup. Separat hatten interne gleich typisierte String-
Schnittstellen des C++-Targeted-Evaluators eine spätere Vertauschung von
Argumenten unnötig leicht gemacht.

## Akzeptanzkriterien

- Ein nativer Runner wählt einen kurzen task-owned UDS-Parent über einen
  expliziten Wert oder `TMPDIR` und scheitert vor dem Host-Setup geschlossen,
  wenn keine valide private Vorfahrenkette gegen UID-übergreifende Ersetzung
  bereitsteht.
- Fokussierte Tests decken Länge, relative Pfade, Symlinks, vorhandene Sockets,
  parallele Allokation, Setup-Fehler, YAML-Quoting und Cleanup-Refusal ab.
- Der C17-Service lehnt eine unsichere Private-Parent-Topologie sowie Pre-Bind-,
  Post-Bind- und Post-Probe-Pathname-Replacements ab, bevor Listener-Ownership
  erfasst wird.
- Der bestehende Protocol-Lifecycle behält Allow- und Blocking-Controls;
  gewöhnliches fokussiertes Cleanup ist abgedeckt, ohne Same-UID-Race-Proof-
  Deletion oder Live-Endpoint-Identity zu behaupten.
- Der Evaluator kompiliert mit C++17 `-Wall -Wextra -Werror` und erhält das
  direkte Allow/Block-Ergebnis bei weniger vertauschbaren internen Eingaben.

## Implementierungsentscheidung und Begründung

Der Python-Runner priorisiert `TRAEFIK_ENGINE_SOCKET_PARENT` vor `TMPDIR`. Er
validiert einen bestehenden absoluten, kanonischen, dem aktuellen Benutzer
gehörenden Parent mit exakt `0700` außerhalb des Checkouts, lehnt Symlink-
Komponenten und Steuerzeichen ab und prüft jeden Vorfahren bis root gegen UID-
übergreifende Ersetzung. Ein gruppen- oder weltbeschreibbarer Vorfahr ist nur
zulässig, wenn er sticky ist und sein nächster Kindeintrag der effektiven UID
gehört. Wenn keine Quelle diese Grenze liefert, scheitert der Runner vor dem
Host-Setup. Er JSON-quotiert die erzeugte YAML und speichert Directory-Identity
vor Cleanup-Checks. Diese Checks verweigern beobachtete Abweichung oder
Restinhalte; sie sind keine atomare Same-UID-Deletion-Garantie.

Der C-Service erzwingt unabhängig denselben Vertrag aus unmittelbarem privatem
Parent und UID-übergreifend sicherer Vorfahrenkette und benötigt daher keine
prozessglobale `umask` oder pfadbasierte Berechtigungsänderung. Vor der
Bereitschaft führt er unter Linux eine begrenzte nichtblockierende lokale UDS-
Probe aus und verlangt, dass der akzeptierte `SO_PEERCRED`-Peer der Engine-
Prozess ist. Er vergleicht `lstat()`-Identity unmittelbar vor und nach der
Probe. Deterministische Selbsttest-Hooks decken die Ablehnung unsicherer
Vorfahren sowie Replacement vor Bind, nach Bind und nach der Probe ab; der
C-Selbsttest verlangt einen expliziten privaten `--socket-parent`.

Der Evaluator verwendet `std::string_view` für unveränderliche
Bracket-Parser-Eingaben und einen benannten `DecisionLogInput`-Wert für den
Decision-Log-Aufruf. Dies ändert nur interne Schnittstellen, keine öffentliche
API und kein ausgegebenes Decision-Verhalten.

## Geänderte Dateien

- `common/scripts/modsecurity_targeted_eval.cc`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/build/build-engine-service.sh`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/README.md` und `connectors/traefik/README.de.md`
- `docs/connectors/README.md` und `docs/connectors/README.de.md`
- `docs/reference/variables.md` und `docs/reference/variables.de.md`
- Dieser bilinguale Change Record und seine bilingualen Indexeinträge in
  `reports/audits/change-records/README.md` und
  `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

Alle Befehle liefen aus `/root/git/ModSecurity-conector` mit task-owned Output
unter `/var/tmp/codex/ModSecurity-conector/runs/20260717T114213Z-feasibility-runtime-remediation-838d9adc/`.

- `make -C connectors/traefik test-engine-service` mit expliziten task-owned
  Build-/Socket-Roots und verifizierten lokalen libmodsecurity-Include-/Library-
  Pfaden bestand; die ursprüngliche doppelte Identity-Observation-Evidence
  liegt in `logs/056-traefik-engine-service-double-observation-race-regression.log`
  (SHA-256 `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`).
- `python -B -m unittest -v tests.test_traefik_native_local_plugin` bestand
  zunächst mit 13 Tests in `057` und nach einer Portabilitätskorrektur mit 14
  Tests in `073`. Das kanonische C++-Evidence-Manifest
  `evidence/cpp17-revalidation-evidence-manifest.json` enthält exakten Befehl,
  CWD, UTC-Start/-Ende, Exit, Rohlog-Pfad, SHA-256 und Zusammenfassung für
  C++17-Compilation (`074`), CDB (`075`), Diagnostics (`080`, fünf Tests) und
  Allow/Block (`081`). Die aktuelle Swappable-Parameter-Reanalyse wurde vom
  Storage-Gate gestoppt (`076`, Exit `77`) und nicht umgangen.
- Die Sonar-Remediation führte 14 Python-Runner-Contracts (`103`), C17-Build
  und expliziten Private-Parent-Selbsttest (`105`), lokale Engine-Allow/
  Blocking-Protokoll- und Replacement-Sentinel-Controls (`106`), Unsafe-Parent-
  Rejection (`107`) sowie C++17-Evaluator-Compile, Diagnostics und Allow/Block
  (`109`–`111`) aus. Der erste überlange Test-Parent (`094`) und die erste
  Pfadmodus-Annahme (`101`) wurden durch den `0700`-Parent-Vertrag korrigiert,
  nicht durch Wiedereinführung globaler `umask` oder Pathname-chmod.
- Die finale Vorfahren-Remediation-Evidence enthält die Pre-Fix-Lücke mit
  Immediate-Parent-Only-Akzeptanz (`119`, SHA-256
  `25a6728bca11448352bd922384e22749570e7d453e393f6dd1092cec1abfeee7`), 16
  Python-Contracts (`120`, SHA-256
  `1bf27a75961e8aec742448899c4e2e648ad1ea4bf6af1fdc9b33440c9d4620f2`),
  Clang- und GCC-C17-Build/Selbsttest (`121`/`122`, SHA-256
  `6d044ad0eb36b861fefe8e1d36b28ae6a59d91b48da5c14aca3b73e416612d80` und
  `8c6ff06096212dde3a1f272f00b9ed7492c33bef35cfc820f0df074910605156`),
  negative Controls über Python, Shell und C (`123`, SHA-256
  `0cc657a4a58763b44070215e7c354027c12688a1eb248e21cb9a76c9c4a2868c`) sowie
  gültige Runtime-Allow/Blocking- plus Cleanup-Sentinel-Controls (`125`,
  SHA-256 `c35d629326601b521feeb92953f7f43526cad2bc5b9d7e6c7316d22e85c0cb36`).
  Gehärteter Diagnosebuild (`126`), ASan+UBSan-Build/Runtime (`127`/`128`) und
  GCC `-fanalyzer` (`129`) bestanden. Die genannten Rohlogs enthalten jeweils
  exakten Befehl, CWD, UTC-Timing und Exit.

## Security-Auswirkung

Die Änderung stärkt Pfadvalidierung, YAML-Serialisierung, UDS-Collision-
Handling, Replacement-Detection und Cleanup-Refusal. Der modellierte
Pre-Capture-Post-`bind`-Identity-Race ist geschlossen: Ein Replacement vor,
während oder unmittelbar nach der Selbstprobe wird nicht als engine-owned
erfasst.

`FND-PARENT-0016` erfasst den bestätigten SonarCloud-Quality-Gate-Fehler am
ersten Draft-PR-Head. Die Remediation entfernt Public-Root-/Default-Allokation,
fordert validierte private Parents und sichere Vorfahrenketten an Python-,
Shell- und C-Grenzen und entfernt prozessglobalen `umask`-State. Sie behauptet
nicht, dass getrennte Same-UID-Endpoint- oder Cleanup-Races behoben sind.

`FND-PARENT-0017` erfasst die unabhängig reproduzierte Cross-UID-
Ancestor-Replacement-Lücke: Ein Kind mit exakt `0700` unter einem nicht-sticky
beschreibbaren Vorfahren wurde vor der Reparatur akzeptiert. Die task-owned
Reproduktion konnte wegen der Storage-Policy keinen Live-Foreign-UID-Prozess
unter einer öffentlichen Root verwenden; die akzeptierte Topologie und der
Source-to-`bind`-Pfad waren dennoch konkret. Die aktuellen Python-, Shell- und
C-Grenzen lehnen sie ab.

`FND-PARENT-0013` bleibt offen: POSIX/Linux besitzt keine atomare bedingte
Unlink-by-Expected-Inode-Operation. Ein bösartiger Prozess mit derselben
Service-UID und veränderbarem Verzeichnis kann weiterhin das finale
`lstat()`-zu-`unlink()`-Intervall rennen. Dieser Record behauptet nicht, dass
das finale Cleanup Same-UID-Race-proof ist.

`FND-PARENT-0014` erfasst getrennt das analoge finale Manifest-Leaf-
Validierungs-zu-Entfernungs-Intervall. `FND-PARENT-0015` ist für den nativen
Host-Pfad folgenreicher: Nach Bereitschaft kann ein Same-UID-Mutator den
Pathname vor einem späteren Middleware-Dial neu binden. Der Client öffnet für
jede Transaktion eine frische UDS-Verbindung und hat aktuell keine verifizierte
Peer-Identity-Bindung; ein gefälschter protokollgültiger Allow-Endpoint könnte
eine Transaktion umleiten. Das ist source-backed, aber ohne echte Host-
Reproduktion, deshalb P1/medium/probable statt High oder confirmed.

## Runtime-Evidence

Der kompilierte C17-Service bestand Protocol-Selbsttest, Selbsttest für
Safe-Ancestor-Socket-Ownership, normalen lokalen Protocol-Lifecycle und den
deliberate Replacement-Sentinel-Negativtest. Im Negativtest ist
`socket_cleanup` das erwartete Fail-Closed-Service-Ergebnis und der Test selbst
bestand. Getrennte Ancestor-Negativkontrollen bestätigten, dass ein expliziter
Test-Parent nun erforderlich ist und ein nicht-sticky beschreibbarer Vorfahr
vor Allokation oder bind abgelehnt wird.

Kein echter Traefik/libmodsecurity-Host-Lifecycle lief: die notwendigen
Host-Binär- und Runtime-Inputs waren nicht verfügbar. Diese Evidence bleibt
`blocked_environment`.

## Bekannte Einschränkungen

- Der Native-Pathname-Listener scheitert geschlossen außerhalb des verwendeten
  Linux-Peer-Credential-Mechanismus.
- `FND-PARENT-0013` blockiert eine strikte Same-UID-No-Foreign-Socket-Cleanup-
  Aussage.
- `FND-PARENT-0014` blockiert eine strikte Same-UID-No-Foreign-Manifest-Leaf-
  Deletion-Aussage.
- `FND-PARENT-0015` blockiert eine strikte Same-UID-Live-Client-to-Engine-
  Endpoint-Identity-Aussage; die bestehende Selbstprobe gilt nur vor
  Bereitschaft.
- `0700` schützt zwischen UIDs; es isoliert nicht bösartige Prozesse mit
  derselben Owner-UID.

## Verbleibende Risiken

Die finalen Pathname- und Manifest-Leaf-Deletion-Grenzen wurden nicht
risikoakzeptiert. Eine spätere Lösung muss entweder automatische Pathname-
Deletion vermeiden, getrennt vertrauenswürdige Cleanup-Grenzen einführen oder
einen kompatiblen atomaren Expected-Object-Deletion-Mechanismus beweisen. Die
Live-Endpoint-Redirection-Grenze benötigt zusätzlich ein verifiziertes End-to-
End-Client/Engine-Identity-Design; abstraktes AF_UNIX, Client-Peer-Credentials
und Descriptor-Handoff sind Zukunftskandidaten, keine aktuellen verifizierten
Fixes.

## Nicht ausgeführte Prüfungen mit Begründung

- Der echte native Traefik-Host-Lifecycle und seine volle CRS/MRTS-
  Profilmatrix liefen nicht, weil benötigte Host-/Runtime-Inputs fehlten; kein
  Download, keine Installation, kein Build und kein Retest wurden zu ihrer
  Erzwingung verwendet.
- NGINX-, Apache- und MRTS-blockierte Punkte bleiben in ihren eigenen
  Machbarkeits-Dispositionen; keine Framework- oder MRTS-Datei wurde geändert.
- Die Repository-CI-Lane nutzt Python 3.13, das auf diesem Host nicht verfügbar
  ist. Die fokussierten Python-Contracts bestanden mit dem vorhandenen
  Interpreter, werden aber nicht als Python-3.13-CI-Lane-Ergebnis behauptet.
- H3 was intentionally not investigated in this remediation task because no approved compatible client solution is currently available.

## Finaler Diff- und Review-Status

Die abgegrenzte lokale Source-/Test-/Dokumentations-Remediation ist
abgeschlossen; die gesamte Security-Posture wird absichtlich nicht als
abgeschlossen beschrieben: `FND-PARENT-0013`, `FND-PARENT-0014` und
`FND-PARENT-0015` bleiben ohne Risikoakzeptanz blockiert. Parent Draft PR #51
existiert und sein erster Head wurde vom SonarCloud-Security-Rating-D-Gate
abgelehnt; die Folge-Revision muss gepusht und an ihrem exakten SHA beobachtet
werden, bevor dieser Record Remote-CI als bestanden beschreiben kann. Die
Kompatibilitätsänderung des fokussierten Tests ist beabsichtigt:
`make -C connectors/traefik test-engine-service` verlangt jetzt einen
bestehenden `TRAEFIK_ENGINE_SOCKET_TEST_PARENT` und endet ohne ihn mit `77`.
Für dieses fokussierte Target wurde kein konfigurierter CI-Caller gefunden. Die
Delivery-Disposition bleibt ein Parent-only-Draft-PR ohne Merge-Autorität.
