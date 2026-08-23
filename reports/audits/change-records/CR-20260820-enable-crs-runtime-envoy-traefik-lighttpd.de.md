# Change Record: CRS-Runtime für Envoy, Traefik und Lighttpd aktivieren

**Sprache:** [English](CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd` |
| Datum (UTC) | 2026-08-20 |
| Basis-Revision | `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Beobachteter aktueller `origin/master` | `4e8560fdc8a2b737fca598522f8748a4d73857be` |
| Parent → Framework Pin | `c40e924ec5c341032908e0082feba1d37ed1dfda` |
| Framework → MRTS Pin | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery-Status | Draft-[PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309) für `agent/crs-runtime-envoy-traefik-lighttpd-master-20260820` vorhanden. Der Branch wurde per normalem Merge-Commit `0ae1ce0590f18b20a39903f2ce877d0280a6e5bd` mit aktuellem `origin/master` synchronisiert. Am Pre-Remediation-Head `fe74cb02876e9de16eaafc7b590f36b46348044a` identifizierte SonarQube Cloud noch einen neuen Code-Smell und 18 duplizierte New-Code-Zeilen; die Exact-Successor-Analyse steht aus. Der master-abgeleitete Framework-Pin bleibt read-only und löst auf den aufgezeichneten MRTS-Pin auf. Kein Merge und kein Auto-Merge sind autorisiert. |

Der Task-Worktree wurde von der aufgezeichneten Task-Basis erstellt und später
per normalem Merge mit separat aufgezeichneten aktuellen `origin/master`-
Revisionen synchronisiert, zuletzt mit
`4e8560fdc8a2b737fca598522f8748a4d73857be`. Frühere Hosted-Ergebnisse bleiben
ausschließlich historisch; alle erforderlichen Revalidierungen bleiben
Delivery-gesteuert.

## Motivation und Problemstellung

Das Parent-Repository muss die `with-crs/no-mrts`-Zellen von Envoy, Traefik und
Lighttpd von reiner Contract-Validierung in reale Host-Runtime-Ausführung
überführen, ohne Framework, MRTS, ihre Gitlinks, Dependencies oder Toolchains
zu ändern. Die Arbeit muss CRS-Provenance, No-MRTS-Evidence,
Request-zu-Entscheidung-Korrelation und fail-closed Cleanup erhalten.

Während der Analyse der Lighttpd-No-CRS-Fixture wurde ein P1-Same-UID-TOCTOU im
früheren Muster gefunden, das eine Fixture-Inode prüfte und denselben Pfad
später löschte. Ein Prozess mit derselben UID konnte den Pfad zwischen diesen
Schritten ersetzen. Die autorisierte Behebung macht die Namespace-Lebensdauer
statt einer abschließenden Löschung über einen angreiferbeschreibbaren Pfad zur
Cleanup-Grenze.

## Akzeptanzkriterien

- Envoy, Traefik und Lighttpd führen jeweils einen realen
  `with-crs/no-mrts`-Hostpfad mit erlaubtem Kontrollrequest, CRS-blockiertem
  Request, korrelierter Evidence, No-MRTS-Nachweis und Cleanup-Evidence aus.
- Der `with-crs/no-mrts`-Workflow klassifiziert diese drei Zellen als
  `runtime`; die sechs Envoy-/Traefik-/Lighttpd-MRTS-Zellen bleiben
  `expected_unsupported`.
- Erstellung und Nutzung der Lighttpd-No-CRS-Fixture erfolgen in einem
  capability-geprüften privaten Namespace mit privater Mount-Propagation und
  ohne unsicheren Fallback auf Cleanup über Pfadnamen.
- Same-UID-Angreiferersetzung sowie Erfolg, Fehler, Timeout, Signal,
  Helper-Fehler, teilweise Initialisierung, Capability-Fehler und Teardown
  besitzen fokussierte Regression-Abdeckung.
- Nur Parent-eigene Dateien ändern sich. Framework- und MRTS-Source,
  Dependency-Manifeste, Lockfiles und Toolchain-Auswahlen bleiben unverändert.
  Der normale Merge des aktuellen `master` enthält dessen Parent → Framework-
  Gitlink-Update, ohne daraus eine task-eigene Gitlink-Änderung zu machen.
- Ein separater Task-Branch und PR erhalten Exact-Head-Lokal- und
  Hosted-Validierung vor jeder Ready-for-Review-Behauptung. Kein Merge,
  Auto-Merge oder Risikoakzeptanz ist Teil dieser Änderung.

## Implementierungsentscheidung und Begründung

Das Parent besitzt Connector-Runtime-Implementierungen, Lifecycle-Skripte,
Normalisierung, Tests und Task-Dokumentation. Framework und MRTS bleiben
read-only Validierungsgrenzen. Die aufgezeichneten Parent → Framework- und
Framework → MRTS-Pins bleiben erhalten.

### Technische Entscheidungen

Die Runtime-Arbeit verwendet den bestehenden CRS-Akquisitions- und
Provenance-Vertrag des Repositorys. Sie fügt keine Dependency hinzu, lädt kein
ungepinntes Artefakt herunter, ändert kein Lockfile und aktualisiert keine
Compiler-, Go-, Python- oder System-Toolchain.

Für die Lighttpd-No-CRS-Fixture bilden vertrauenswürdige root-eigene
Setup-Programme die Grenze: `/usr/bin/unshare` startet den privaten Namespace
und `/usr/bin/unshare --propagation private` macht die Propagation explizit
privat; festes `/usr/bin/dash` und `/usr/bin/mount` erzeugen danach ein privates
`nosuid,nodev,noexec`-tmpfs; anschließend stellt `/usr/bin/bwrap` nur minimale
schreibgeschützte System-/Runtime-Binds und den exakten Task-eigenen Smoke-Root
als beschreibbar bereit. Der unprivilegierte Harness läuft erst nach Prüfungen
von Capability-Sets, `no_new_privs`, Mounts und fester Fixture-Root-Identität
weiter.

Der finale Namespace-State-Verifier prüft Capability-Sets, `no_new_privs`,
Mount-Zustand und die `dev:ino`-Identität des festen Fixture-Roots. Der
Descriptor-I/O-Cleanup-Befehl prüft separat das Allowlist-Inventar der Blätter,
behält alle Blätter und führt niemals eine Löschung über Pfadnamen oder relativ
zu einem Deskriptor aus. Der Abbau des privaten tmpfs-Namespace entfernt das
Fixture-Verzeichnis und seine Blätter.

Der descriptorgebundene Fixture-Server veröffentlicht jedes Steuerartefakt
jetzt über die verfügbare einmalige `write_text_fresh`-API. Das finale Blatt
wird mit `O_EXCL|O_NOFOLLOW` erzeugt; die Implementierung hängt nicht von der
zuvor fehlenden atomaren Schreibschnittstelle und nicht von einem temporären
Blatt ab, das bereinigt werden müsste.

## Follow-up vom 2026-08-21: Namespace-Gate, Workflow-Übersicht und Sonar-Befunde

Die Hosted-Lighttpd-Namespace-Integration bleibt bewusst fail-closed. Der
`ubuntu-latest`-Runner stellt die erforderliche Kombination aus
unprivilegiertem User-, Mount- und PID-Namespace nicht bereit; deshalb schlägt
der Test an seiner expliziten Availability-Assertion fehl, statt auf
pfadbasiertes Cleanup zurückzufallen. Für diese fehlende Kernel-Fähigkeit gibt
es keine sichere Parent-only-Workflow-Anpassung: `sudo`, ein privilegierter
Container, ein Setcap-Helper, das Abschalten des Gates oder ein
Check-then-`rmdir`-Fallback würden entweder veränderbaren PR-Code privilegiert
ausführen oder die P1-Kontrolle abschwächen. Kleinste Voraussetzung ist ein
isolierter, nicht-root Self-hosted-Linux-Runner mit aktivierten Namespaces,
vertrauenswürdigen root-eigenen Setup-Binaries, keinen Secrets, keinem Docker-
Socket, keinem persistenten Hostzugriff und einem dedizierten Label. Der
Draft-PR bleibt auf diese externe Runner-Fähigkeit blockiert.

Der CRS/no-MRTS-Workflow schreibt nun eine abschließende
`if: always()`-Connector-Übersicht. Sie meldet ausschließlich feste GitHub-
Step-Outcomes für Checkout, gesperrte Dependencies, Revisions-/Zellenprüfung,
private Roots, CRS-Vorbereitung, das reale Runtime-Target und die Evidence-
Veröffentlichung. Für jeden Connector werden bestandene, fehlgeschlagene,
übersprungene und abgebrochene Stages sowie die erste nicht bestandene Stage
sichtbar. Ein fehlgeschlagenes, übersprungenes oder abgebrochenes Runtime-
Target wird als solches dargestellt und niemals zu einem Connector-
Capability-Pass befördert. Der bestehende HAProxy-Ausschluss für den Raw-
Artifact-Upload wird separat als `skipped_by_security_policy` gezeigt; er wird
weder als Runtime-Erfolg noch als Runtime-Fehler versteckt. Der Summary-Writer
weist unbekannte Outcomes ab, verlangt `O_NOFOLLOW`, öffnet das vom Runner
bereitgestellte Parent-Verzeichnis einmal und hängt über dessen Directory-
Descriptor an.

Am PR-Head `6c1fe074b1d3027a00228b1517e29e08b064eca3` meldete die offizielle
SonarQube-Cloud-Issue-API trotz bestandenem Quality Gate elf offene neue
Befunde: fünf Regex-Style-Befunde und einen Cognitive-Complexity-Befund im
Parent-Normalizer sowie vier Exception-Assertion-Befunde in einem Lighttpd-
Contract-Test. Dieses Follow-up behebt jeden Befund ohne `NOSONAR`, Änderungen
an Regeln oder Quality Gate, Exclusions, Issue-Acceptance, Dependency-
Änderungen oder Testabschwächungen. Der Normalizer erhält seine ASCII-
Wire-Evidence-Einschränkung mit expliziter ASCII-Regex-Semantik; die
Komplexitätsaufteilung erhält dieselbe fail-closed Trace-Validierung. Die
nächste SonarQube-Analyse des exakten Heads muss weiterhin null neue Befunde
zeigen, bevor die Anforderung als erfüllt gilt.

## Follow-up vom 2026-08-22: Master-Aktualisierung, Traefik-Deduplizierung und Hosted-Grenze

Der Branch enthält jetzt den normalen Merge-Commit `101df216` des aktuellen
`origin/master` `423abcc130cf5d29ccf15dd7d82e4e7d89d495d3`. Der resultierende
Parent → Framework-Pin ist `c40e924ec5c341032908e0082feba1d37ed1dfda`; der
Framework → MRTS-Pin bleibt `615b13bacbd008562c17408246c41ab27dca3104`. Das
ist eine master-abgeleitete Revisionsaktualisierung und keine task-eigene
Framework- oder MRTS-Änderung; der veraltete lokale verschachtelte Checkout
wird weder gestaged noch als Autorität verwendet.

Die offizielle SonarQube-Cloud-Duplizierungs-API ordnete alle 20 duplizierten
New-Code-Zeilen zwei gleichartigen Traefik-Engine-/Host-Startblöcken zu. Sie
verwenden jetzt gemeinsam den Context-Manager `running_traefik_host`. Er erhält
Prozess-Ownership, Argumente, Arbeitsverzeichnis, Lebensdauer der
Log-Deskriptoren, Readiness-Diagnostik und das äußere Cleanup-Verhalten beider
CRS- und Nicht-CRS-Runtime-Pfade. Ein direkter Regressionstest prüft diese
Lifecycle-Eigenschaften; der bestehende CRS-Run-ID-Request-Test deckt weiter
die Request-Korrelation ab. Die frische SonarQube-Analyse des exakten Heads
muss `0,0 %` New-Code-Duplizierung melden, bevor diese Metrik als erfüllt
behauptet wird.

Die erforderliche Lighttpd-Namespace-Integration bleibt ein externer
Hosted-Runner-Blocker und kein sicher Parent-only behebbarer Workflowfehler.
Ihr echter Einstiegspfad verlangt eine unprivilegierte User-/Mount-/PID-
Namespace-Kette und weist Host-root- sowie Set-ID-Aufrufer zurück. `sudo`, ein
privilegierter Container oder ein Setcap-Helper würden diese Grenze nicht
erhalten. Kleinste sichere Abhilfe bleibt ein isolierter Nicht-root
Self-hosted-Linux-Runner mit den nötigen Namespaces, festen root-eigenen
Setup-Binaries, keinen Secrets, keinem Docker-Socket und dediziertem Label.

## Follow-up vom 2026-08-23: Sonar-Remediation für null New-Code-Befunde

Am exakten Predecessor-PR-Head `fe74cb02876e9de16eaafc7b590f36b46348044a`
meldete die öffentliche SonarQube-Cloud-API einen offenen New-Code-Befund,
`AaAqpBihH7VZS0qiY-cu` / `python:S8714`, in
`connectors/lighttpd/tests/test_no_crs_fixture_namespace.py:230`. Zusätzlich
meldete sie `new_duplicated_lines=18` und
`new_duplicated_lines_density=0.1573701696100717` (angezeigt als 0,2 %) aus
zwei überlappenden Envoy-Header-Tabellenblöcken in
`connectors/envoy/ext_proc/internal/processor/processor_test.go`.

Das Parent-only-Follow-up entfernt den unnötigen Exception-Wrapper aus dem
Lighttpd-Required-Identity-Vertrag, sodass fehlende oder fehlerhafte numerische
Pflicht-Environment-Werte natürlich fehlschlagen. Die Assertions für Nicht-
root, exakte UID/GID, leere Gruppen, `NoNewPrivs` und Docker-Socket bleiben
unverändert. Der Envoy-Test erzeugt die zwei Authority-/Host-
Reihenfolgevarianten nun aus einem Helper und behält alle feindlichen Fälle:
beide Reihenfolgen, doppeltes Host und doppelte Authority. Es unterdrückt
Sonar nicht, verändert keine Regel/kein Profil/keinen Schwellwert, schließt
keinen Pfad aus, akzeptiert keinen Befund, ändert keine Dependency und schwächt
keine Runtime- oder Security-Kontrolle ab.

Vor der Delivery bestand der fokussierte Lighttpd-Namespace-Contract-Test mit
sieben Contract-Tests und zehn erwarteten capability-gegateten
Integration-Skips; Envoy `go test ./...` und `go vet ./...` bestanden mit der
vorhandenen Go-1.26.6-Toolchain und einem privaten Task-Cache; Python-
Kompilierung und `git diff --check` bestanden. Der exakte Successor-PR-Head-
Readback der SonarQube-Cloud-Issues und Duplikation bleibt die finale
Akzeptanz-Evidence; bevor diese Analyse beendet ist, wird hier kein
Null-Ergebnis behauptet.

## Security-Auswirkung

Die betroffene Grenze umfasst nicht vertrauenswürdige HTTP-Eingaben,
Connector-zu-ModSecurity-Entscheidungspfade, CRS-Provenance, Evidence-Pfade,
Prozess-Lifecycle, Mounts und temporäre Fixtures. Das Same-UID-Angreifermodell
erlaubt Umbenennen, Ersetzen und Neuanlegen des Legacy-Fixture-Pfads.

Die Behebung entfernt die sicherheitsrelevante Operation aus Prüfung und
anschließendem `rmdir` aus dem Fixture-Lifecycle. Sie verwendet einen privaten
Mount-Namespace, explizit private Propagation, einen nicht
angreiferbeschreibbaren Fixture-Root, begrenzte vertrauenswürdige
Setup-Programme, Capability-Entzug und `no_new_privs`. Ein Fehlschlag beim
Erhalt oder der Prüfung einer nötigen Capability-, Namespace-, Mount- oder
Isolationseigenschaft ist fail-closed. Es gibt keine Risikoakzeptanz und keine
manuelle Cleanup-Anweisung als Ersatz für die technische Kontrolle.

## Geänderte Dateien

Task-eigene Implementierung und Tests umfassen derzeit die folgenden
Parent-Bereiche; das finale gestagte Inventar bleibt der verpflichtenden
finalen Diff-Prüfung vorbehalten:

- `ci/provisioning/components/prepare-runtime-components.py`,
  `ci/runtime/lifecycle/run-no-crs-baseline.sh`,
  `ci/runtime/lifecycle/run-remaining-connector-target.sh`,
  `ci/runtime/lifecycle/run-with-crs-no-mrts.sh`,
  `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py` und
  `ci/runtime/lifecycle/summarize-with-crs-no-mrts-workflow.py`;
- Envoy-ext-proc-Runtime-Code, Harness und fokussierte Tests unter
  `connectors/envoy/`;
- Traefik-Native-Middleware, Runtime-Smoke und fokussierte Tests unter
  `connectors/traefik/`;
- Lighttpd-Modul, Lifecycle-Harness, vertrauenswürdiger Namespace-Runner,
  Namespace-/Descriptor-I/O-Helfer, fokussierte Tests und zugehörige EN/DE-
  Dokumentation unter `connectors/lighttpd/` und `docs/`;
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`, fokussierte
  Parent-Test-Contracts unter `tests/` sowie das Repository-`Makefile`;
- dieses englische/deutsche Change-Record-Paar.

Keine Framework- oder MRTS-Quelldatei, kein Gitlink, kein Dependency-Manifest,
kein Lockfile und keine Toolchain-Auswahl liegen im autorisierten
Änderungsscope.

## Ausgeführte Befehle

Dieser Record hat unmittelbar seine eigenen Dokumentationsprüfungen beobachtet.
Die Task-Evidence enthält außerdem die folgenden aufgezeichneten lokalen
Kernvalidierungen; deren exakter Invocation-Text wird mit der Task-Evidence
aufbewahrt und hier nicht aus Erinnerung rekonstruiert:

- `make check-bilingual-docs` wurde vor und nach der Korrektur der
  Record-Überschriften ausgeführt. Die spätere Ausführung meldete keinen
  strukturellen Change-Record-Fehler mehr, blieb aber durch bereits bestehende
  fehlende Framework-Submodule-Dokumentationsziele blockiert. Dieser externe
  Missing-Target-Zustand wird durch den Record nicht geändert.
- `git diff --check -- reports/audits/change-records/CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.md reports/audits/change-records/CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.de.md`
  wurde ohne Ausgabe zu Diff-Whitespace ausgeführt.
- `rg '^## '` wurde für beide Records verwendet, um die Sequenz ihrer
  Top-Level-Überschriften zu vergleichen.

## Tests und tatsächliche Ergebnisse

Die Lighttpd-Integration des vertrauenswürdigen Namespace ist lokal
capability-gated. Die beobachtete Nicht-root-Probe
`unshare --user --map-root-user` scheiterte mit
`write /proc/self/uid_map: Operation not permitted`; daher kann der vollständige
vorgesehene Produktions-Einstiegspfad für Nicht-root in dieser Umgebung nicht
ausgeführt werden. Das erforderliche Verhalten ist daher hier nicht zu einem
lokal verifizierten Produktions-Runtime-Ergebnis befördert.

| Prüfung | Hier aufgezeichnetes tatsächliches Ergebnis |
| --- | --- |
| Change-Record-`git diff --check` | bestanden; keine Ausgabe zu Diff-Whitespace |
| Lighttpd-fokussierte Contracts | bestanden: 50 Tests im kombinierten fokussierten Lauf; Namespace-Integration bleibt lokal capability-gated |
| Workflow-Sicherheitstests | bestanden: 30 Tests |
| C-Modul-Build | bestanden mit `-Wall`, `-Wextra` und `-Werror` |
| Clang Static Analyzer | bestanden: 0 Diagnosen |
| Envoy- und Traefik-Go-Validierung | `go mod verify`, Dependency-Auflistung, Tests, Vet und `govulncheck` bestanden; keine Schwachstellen gefunden |
| Parent-Runtime-Tests | bestanden: 34 Tests; die task-lokalen Btrfs-Verzeichnis-Haltbarkeitsbarrieren waren langsam, endeten aber ohne Entfernung einer Atomicity-Kontrolle |
| Fokussierte CRS/no-MRTS-Normalizer-Regression | bestanden: 44 Tests, einschließlich semantischem Lighttpd-`status=blocked` plus strikter numerischer HTTP-Status-Validierung |
| `test_collect` unter dem Framework-Override | bestanden: 42 Tests; 3 Framework-gated Skips |
| Python-Dependency-Validierung | `pip check` bestanden |
| Shell-/Python-/YAML-Validierung | Shell-Syntax, Python-Kompilierung, YAML-Parsing und Diff-Checks bestanden |
| Cppcheck | bestehende Style-Diagnosen außerhalb geänderter Hunks; kein Befund im geänderten Hunk gemeldet |
| Nicht-root-User-Namespace-Probe | blockiert: `unshare --user --map-root-user` scheiterte mit `write /proc/self/uid_map: Operation not permitted` |

## Runtime-Evidence

Der Draft-[PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309)
wurde zuletzt beim Hosted-Exact-Head `e432b1e748dc8f49b98ed1a29e8d7277a40763a5` geprüft. Envoy und Traefik beendeten
ihre Runtime-Jobs erfolgreich. Apache scheiterte, weil die zeitliche Semantik
von `GITHUB_ENV` innerhalb desselben Steps die frisch erworbenen CRS-Roots für
den folgenden Step nicht verfügbar machte; diese Änderung fügt einen separaten
Vorbereitungsschritt für diese Übergabe hinzu. Lighttpd beendete seinen
Lifecycle sowie die Curl-Metadatenvalidierung erfolgreich, doch danach
versuchte die Parent-Attestierung, das semantische Action-Label
`status=blocked` von Lighttpd als Ganzzahl zu parsen, bevor sie die numerischen
Hostfelder `http_status=403` und `visible_http_status=403` berücksichtigte.
Das Follow-up akzeptiert dieses dokumentierte semantische Label nur, wenn
mindestens ein striktes JSON-Ganzzahl-HTTP-Feld vorhanden, im Bereich und
konsistent ist; fehlerhafte Strings, Booleans, Gleitkommazahlen, fehlende
numerische Evidence und Konflikte werden fail-closed abgewiesen. Eine
task-private Kopie der hochgeladenen Evidence validierte gegen das unveränderte
gepinnte Framework als `CONTRACT_VALIDATED`. Die vorausgehende Curl-Korrektur
akzeptiert ausschließlich die entsprechenden `Trying`-, `Established`- und
`Connected`-Schreibweisen mit literalem `127.0.0.1`, gültigen Source- und
Zielports, genau einem Marker jeder Art und übereinstimmenden
Versuch-/Verbindungs-Zielports. HAProxy war vor der Runtime durch die alte
read-only-Framework-Reihenfolge bei
`bd69ee96e0e7082317d4afe1232bee625665eb9a` blockiert, die
`verify_build_target` vor `prepare_build_worktree` aufrief. Der aktuelle
Parent-Pin ist `89881a1b33219fc18df3cf2f15dda53261d13443` und enthält die
Reihenfolgekorrektur aus Framework-PR #102. Eine frische Exact-Head-HAProxy-
Runtime-Validierung bleibt verpflichtend; dieser Record behauptet keinen
Erfolg.

Der erforderliche PR-ausgelöste P1-Namespace-Test schlug fail-closed fehl,
weil die Hosted-Umgebung die nötige User-, Mount- oder PID-Namespace-
Capability nicht bereitstellte. Das ist eine fehlgeschlagene Validierung und
kein erfolgreicher Fallback. Diese Beobachtungen verhindern einen Full-Matrix-
oder verified-PR-Claim. Es wird kein künftiges Testergebnis behauptet und es
wurden keine rohen CI-Logs oder Trace-Artefakte exportiert.

Dieser Lauf ist keine finale Runtime-Evidence für alle drei beförderten Zellen.
Frühere Hosted-Läufe und ihre Ergebnisse bleiben nur als historischer Kontext
erhalten und werden nicht für Exact-Head-Behauptungen wiederverwendet. Das
Statusnormalisierungs-Follow-up hat noch keinen Hosted-Exact-Head-Lauf erhalten.

Dieser Record behauptet keine finale Runtime-Evidence. Insbesondere ist die
Hosted-Validierung des neuesten exakten Task-Heads nicht erfolgreich; eine
erfolgreiche SonarQube-Cloud-Analyse oder ein erfolgreiches Required-Check-
Ergebnis wird nicht behauptet. Vorläufige Connector-Arbeit und
Static-Validierung ersetzen keine reale Host-Runtime-Evidence für die drei
beförderten Matrixzellen.

## Nicht ausgeführte Prüfungen mit Begründung

Folgendes bleibt ausstehend oder war lokal nicht verfügbar: vollständige
Drei-Connector-Lokal-Runtime-Validierung in einer Namespace-Umgebung mit
Nicht-root-Capability (der Hosted-Namespace-Test schlug fail-closed fehl);
Full-Matrix-Workflow-Validierung; GitHub-Hosted-
Required-Checks; actionlint, zizmor, Ruff und Pyright waren in der lokalen
Umgebung nicht verfügbar; SonarQube Cloud sowie finale PR-Exact-Head-
Validierung. CodeQL, Secret Scanning, OSV und zizmor wurden nur für den
früheren PR-Head beobachtet und nicht als Evidence für den ausstehenden
Follow-up-Head wiederverwendet.

## Bekannte Einschränkungen

Die beobachtete Nicht-root-Probe `unshare --user --map-root-user` scheitert mit
`write /proc/self/uid_map: Operation not permitted` und verhindert die
Ausführung des capability-geprüften Lighttpd-Namespace-Einstiegspfads mit
seinem vorgesehenen Nicht-root-Aufrufer. Der Hosted-Namespace-Test schlug
fail-closed fehl, weil der Runner die erforderliche Namespace-Capability nicht
bereitstellte. Das ist ein Umgebungsblocker für
diesen Integrationstest, kein Nachweis, dass die Kontrolle unnötig ist oder ein
schwächerer Cleanup-Pfad erlaubt wäre. Das bilinguale Dokumentationsziel
benötigt für seine repository-native Validierung weiterhin den exakten
gepinnten Framework-Checkout. Der Task-Branch ist jetzt per normalem Merge mit
dem beobachteten `origin/master` synchronisiert; der PR bleibt Draft und die
Delivery erfordert eine erneute Exact-Head-Validierung. Keine Framework-,
MRTS- oder task-erzeugte Gitlink-Änderung gehört zu dieser Arbeit.

## Verbleibende Risiken

Bis die erforderlichen Nicht-root-Namespace-Integrationstests und adversarial
Lifecycle-Tests bestehen, ist die P1-Behebung nicht für einen
verified-PR-Claim geeignet. Die Implementierung muss weiter fail-closed sein,
statt auf pfadbasierte Löschung zurückzufallen. Die Runtime-Promotion hängt
außerdem von realer CRS-Regel-Evidence, No-MRTS-Nachweis, Cleanup-Evidence,
Exact-Head-Hosted-Checks und den erforderlichen Qualitäts-/Security-Gates ab.
Die aktualisierte Framework-Revision entfernt den zuvor bekannten HAProxy-
Reihenfolgefehler, aber ein frischer Exact-Head-HAProxy-Lauf bleibt erforderlich,
bevor er kein Matrix-Blocker mehr ist.

## Finaler Diff- und Review-Status

Status: in Arbeit; Draft-PR #309 vorhanden, Exact-Head-Hosted-Validierung
ausstehend. Dieser Record dokumentiert eine autorisierte Parent-only-
Implementierungsarbeit und ihre aktuellen Blocker. Er behauptet keinen
Ready-for-Review-Übergang, erfolgreichen Hosted-Check, Merge, CI-Erfolg,
SonarQube-Erfolg, vollständige Matrix oder Risikoakzeptanz.

## Exact-Head-Remediation-Follow-up vom 2026-08-21

Der aktuelle Parent-`origin/master` ist
`c2e2c6a77edd0f1ccc3d41fc4e133974a630e518`; er pinnt Framework
`798bff0c921ab8c7f10b2ca949304d58e7f205a2` und MRTS
`615b13bacbd008562c17408246c41ab27dca3104`. Der Task-Branch wurde normal mit
diesem Parent-Master gemergt. Dies ist eine Basis-Synchronisierung und erzeugt
keinen task-eigenen Gitlink-Diff.

Der erste Exact-Head-Lauf nach dieser Synchronisierung brach für alle
`with-crs/no-mrts`-Connectoren vor dem Hoststart ab, weil der Workflow den
ausgecheckten Framework-Stand noch gegen den früheren Pin `89881a…` verglich.
Workflow-Vertrag und Regressionstest verwenden jetzt die vom Parent
eingetragene Revision `798bff…`. Das ist eine Konsistenzkorrektur und keine
Framework-Source-Änderung.

SonarQube Cloud meldete außerdem zwei `pythonsecurity:S8707`-Befunde im neuen
Connector-Summary-Helper: Ein per CLI übergebener Summary-Dateiname konnte
einen Dateisystem-Sink erreichen. Der Helper akzeptiert keinen Summary-
Dateipfad mehr per CLI. Er akzeptiert nur noch das runner-bereitgestellte
`GITHUB_STEP_SUMMARY`, verlangt genau eine reguläre `step_summary_*`-Datei
unter dem runner-owned Verzeichnis `RUNNER_TEMP/_runner_file_commands`,
durchläuft Verzeichnisse über Non-Symlink-Deskriptoren und prüft Owner,
nicht-schreibbare Verzeichnis-/Dateimodi sowie Link-Anzahl vor dem Anhängen.
Fehlende Capabilities, unsichere Pfade, Symlinks, fehlende Dateien oder falsche
Owner brechen fail-closed ab. Der neue Regressionstest belegt den legitimen
Runner-Fall und lehnt externe, Traversal- und Symlink-Ziele ab.

Die fokussierte Post-Fix-Validierung bestand: 49 CRS/no-MRTS-
Runtime-Contract-Tests, 30 CI-Workflow-Tests, die CI-Sicherheitsvertrags-Suite
mit 124 Tests und 5 erwarteten environment-gated Skips, actionlint, offline
zizmor, zweisprachige Dokumentation, Python-Syntaxkompilierung und
`git diff --check`. Neue Exact-Head-Hosted-Runtime- und SonarQube-Cloud-
Evidence bleibt erforderlich; dieser Record behauptet noch keinen Sonar-
Nullbefund und keine erfolgreichen Runtime-Zellen.

Die erste SonarQube-Cloud-Analyse für den exakten Head `263f8806…` bestand
zwar ihr Quality Gate und schloss die beiden Security-Befunde, die offizielle
PR-Issue-Abfrage enthielt jedoch noch einen task-eigenen `python:S1192`-
Code-Smell für das wiederholte Unsafe-Path-Fehlerliteral. Das Literal ist jetzt
eine Modulkonstante; das fail-closed Fehlerverhalten bleibt ohne Suppression
erhalten. Eine neue Exact-Head-Analyse muss den vom Benutzer geforderten
Null-Neu-Issues-Befund nachweisen.

## Exact-Head-Workflow-Revisionskorrektur vom 2026-08-22

Die frische SonarQube-Cloud-Analyse des PR-Heads
`93a007f7b858a09c5b527b5db4084e93add5da7b` meldet `0,0 %` New-Code-
Duplizierung und null duplizierte Zeilen. Der frische Runtime-Workflow
`32578172744` scheiterte dennoch in allen fünf Matrix-Jobs, bevor ein
Connector-Host startete. Jeder Job scheiterte bei `Verify pinned Parent,
Framework, and MRTS revisions`: Der normale Master-Merge änderte den Parent →
Framework-Gitlink auf `c40e924ec5c341032908e0082feba1d37ed1dfda`, während
dieser Workflow und sein Contract-Test weiter die frühere Revision
`798bff0c921ab8c7f10b2ca949304d58e7f205a2` erwarteten; MRTS bleibt
`615b13bacbd008562c17408246c41ab27dca3104`.

Die Korrektur aktualisiert ausschließlich diese erwartete Framework-Identität
im Workflow und synchronisierten Contract-Test. Sie behält den exakten
unveränderlichen Vergleich von Parent, Framework und MRTS bei; sie unterdrückt
weder das Gate noch erlaubt sie Runtime-Ausführung bei einem nicht passenden
Checkout. Artifact-Upload-Fehler in Envoy, Traefik und Lighttpd waren Folge der
übersprungenen Runtime und werden nicht als separater Runtime-Fehler behandelt.
Frische Exact-Head-Workflow- und Sonar-Evidence bleibt nach dieser Korrektur
erforderlich.

## Follow-up vom 2026-08-22: Voraussetzung eines vertrauenswürdigen Namespace-Dispatchers

Die frühere ausschließlich Self-hosted-Voraussetzung wird durch den separat
geprüften Bootstrap-Draft-PR #320 ersetzt. Er fügt einen ausschließlich
`workflow_dispatch`-Workflow zu geschütztem `master` hinzu; er ist nicht Teil
des `pull_request`-Workflows dieses PRs und fügt PR #309 weder `sudo`,
AppArmor-Setup, privilegierten Container noch Fallback hinzu.

Nach unabhängiger Prüfung und Merge von PR #320 muss der konfigurierte
Repository-Owner dessen vertrauenswürdigen Workflow manuell von `master` mit
der offenen kanonischen Nummer oder dem aktuellen vollständigen klein
geschriebenen Head-SHA von PR #309 starten. Der feste Dispatcher führt zuerst
nur root-owned Ubuntu-24.04-Systemsetup aus und bindet die Eingabe danach über
die öffentliche GitHub-API an genau einen offenen kanonischen master-PR und
dessen exakten Head-SHA. Er checkt nur diesen SHA ohne persistente Credentials
oder Hooks aus, entfernt `.git` und führt den Testquelltext dieses PRs nur als
frischen `ns-test` mit leeren Zusatzgruppen und Capability-Sets,
`NoNewPrivs`, `env -i`, privatem Temp-Root, Docker-Socket-Sperre und
fail-closed User-/Mount-/PID-Namespace- sowie Bubblewrap-Probes aus.

PR #309 enthält nur die passenden unprivilegierten Testassertions für diese
äußere Identität und den temporären Root. Er bleibt Draft: Namespace-
Runtime-Erfolg, Qualitätsergebnis, Ready-for-Review-Status und Merge werden
erst nach einem erfolgreichen manuellen Lauf des geschützten-master-Workflows
für den exakten Head beansprucht.

## Aktualisierung vom 2026-08-22: aktueller Master und Envoy-Authority-Kohärenz

Ein sauberer Task-Worktree hat das aktuelle `origin/master`
`4e8560fdc8a2b737fca598522f8748a4d73857be` regulär durch Merge-Commit
`0ae1ce0590f18b20a39903f2ce877d0280a6e5bd` übernommen. Der Parent →
Framework-Pin bleibt `c40e924ec5c341032908e0082feba1d37ed1dfda`, der Framework →
MRTS-Pin bleibt `615b13bacbd008562c17408246c41ab27dca3104`; in keinem der
verschachtelten Repositories gibt es eine task-eigene Source- oder
Gitlink-Änderung.

Der oben beschriebene vertrauenswürdige Namespace-Dispatcher auf geschütztem
`master` ist jetzt Teil des aktuellen Masters. Er muss weiterhin manuell gegen
den exakten finalen Head von PR #309 gestartet werden; der gewöhnliche
PR-Workflow bleibt unprivilegiert und dieser Draft beansprucht keinen
Namespace-Runtime-Erfolg, bevor dieser manuelle Lauf erfolgreich ist.

Die fokussierte Prüfung stellte fest, dass der Envoy-Request-Metadatenparser
`:authority` und einen gewöhnlichen `Host`-Header bisher unabhängig behielt.
Er weist jetzt einen Unterschied oder eine doppelte Authority-/Host-
Repräsentation ab, bevor die Transaktion geöffnet wird. Ein kanonisches,
case-insensitiv übereinstimmendes Paar bleibt erlaubt und verwendet den
ursprünglichen `:authority`-Wert. Fokussierte Go-Tests decken beide
Header-Reihenfolgen, doppelte Repräsentationen und den legitimen Matching-Fall
ab.
