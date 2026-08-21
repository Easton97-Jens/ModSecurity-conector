# Change Record: CRS-Runtime für Envoy, Traefik und Lighttpd aktivieren

**Sprache:** [English](CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260820-enable-crs-runtime-envoy-traefik-lighttpd` |
| Datum (UTC) | 2026-08-20 |
| Basis-Revision | `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Beobachteter aktueller `origin/master` | `aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf` |
| Parent → Framework Pin | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| Framework → MRTS Pin | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery-Status | Draft-[PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309) für `agent/crs-runtime-envoy-traefik-lighttpd-master-20260820` vorhanden. Der zuletzt gehostet geprüfte exakte Head ist `75c3be54a4855e0c34ffeb30d0895c0fd840f313`; Hosted-Lauf `32433856340` ist nicht erfolgreich und dieses Follow-up wartet auf einen frischen Exact-Head-Lauf. Kein Merge und kein Auto-Merge sind autorisiert. |

Der Task-Worktree wurde von der aufgezeichneten Task-Basis erstellt.
`origin/master` ist anschließend auf den separat aufgezeichneten aktuellen Wert
weitergelaufen. Dieser Record behauptet nicht, dass die spätere Basis enthalten
ist; diese Entscheidung und jede erforderliche Revalidierung bleiben
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
- Nur Parent-Dateien ändern sich. Framework, MRTS, Gitlinks,
  Dependency-Manifeste, Lockfiles und Toolchain-Auswahlen bleiben unverändert.
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
  `ci/runtime/lifecycle/run-with-crs-no-mrts.sh` und
  `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`;
- Envoy-ext-proc-Runtime-Code, Harness und fokussierte Tests unter
  `connectors/envoy/`;
- Traefik-Native-Middleware, Runtime-Smoke und fokussierte Tests unter
  `connectors/traefik/`;
- Lighttpd-Modul, Lifecycle-Harness, vertrauenswürdiger Namespace-Runner,
  Namespace-/Descriptor-I/O-Helfer, fokussierte Tests und zugehörige EN/DE-
  Dokumentation unter `connectors/lighttpd/` und `docs/`;
- fokussierte Parent-Test-Contracts unter `tests/` sowie das Repository-
  `Makefile`;
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
| `test_collect` unter dem Framework-Override | bestanden: 42 Tests; 3 Framework-gated Skips |
| Python-Dependency-Validierung | `pip check` bestanden |
| Shell-/Python-/YAML-Validierung | Shell-Syntax, Python-Kompilierung, YAML-Parsing und Diff-Checks bestanden |
| Cppcheck | bestehende Style-Diagnosen außerhalb geänderter Hunks; kein Befund im geänderten Hunk gemeldet |
| Nicht-root-User-Namespace-Probe | blockiert: `unshare --user --map-root-user` scheiterte mit `write /proc/self/uid_map: Operation not permitted` |

## Runtime-Evidence

Der Draft-[PR #309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309)
wurde beim gepushten exakten Head
`75c3be54a4855e0c34ffeb30d0895c0fd840f313` durch den Hosted-Lauf `32433856340`
geprüft. Envoy und Traefik beendeten ihre Runtime-Jobs erfolgreich. Lighttpd
erreichte und beendete seinen Lifecycle, aber der Post-Run-Normalizer lehnte
die Curl-8.18-Schreibweise `Connected` ab; seine beförderte Zelle ist daher
noch nicht verifiziert. Apache verlor seine frisch erworbenen CRS-Roots über
den Runtime-Snapshot. HAProxy war vor der Runtime durch die read-only-
Framework-Reihenfolge blockiert, die `verify_build_target` vor
`prepare_build_worktree` aufruft. Diese Fehler verhindern einen Full-Matrix-
oder verified-PR-Claim.

Die Follow-up-Parent-Behebungen sind eng begrenzt: die exakt
dokumentierte Curl-Schreibweise akzeptieren; Apaches frische CRS-Roots über
`GITHUB_ENV` mit einem expliziten finalen Environment-Override weiterreichen;
und die PR-ausgelöste Lighttpd-Namespace-Suite so erzwingen, dass fehlende
User-, Mount- oder PID-Namespace-Unterstützung fehlschlägt. Die Suite prüft den
exakten PR-Head aus und testet ihn. Die lokale Suite bleibt capability-gated
und überspringt ihre Integrationsfälle, weil der verschachtelte Kernel den
User-Namespace mit `EPERM` ablehnt; Hosted-Evidence für diese erforderliche
Suite steht noch aus. Es wurden keine rohen CI-Logs oder Trace-Artefakte
exportiert.

Der fehlgeschlagene Lighttpd-Job auf dem exakten Head erreichte CRS-Akquisition
und den gepinnten `1.4.85`-Host-Build, bevor sein privater Curl-Trace-Parser
eine sonst nicht klassifizierte strukturelle Zeile ablehnte. Der eng begrenzte
Follow-up akzeptiert ausschließlich Curls dokumentierten Übergang
`<= Recv header, <decimal> bytes (0x<hex>)` als alternative
Request-Abschlussgrenze. Empfangene Daten, generische Diagnosen, fehlerhafte
Datensätze und beliebige Star-Zeilen bleiben abgelehnt; Outgoing-
Offset-/Längenprüfungen und die unabhängige Raw-Response-Header-Validierung
bleiben verpflichtend. Diese Änderung wartet auf frische Exact-Head-
Runtime-Evidence.

Dieser Lauf ist keine finale Runtime-Evidence für alle drei beförderten Zellen.
Frühere Hosted-Läufe und ihre Ergebnisse bleiben nur als historischer Kontext
erhalten und werden nicht für Exact-Head-Behauptungen wiederverwendet.

Dieser Record behauptet keine finale Runtime-Evidence. Insbesondere besitzt
der Follow-up-Head noch keinen abgeschlossenen Hosted-Workflow, keine
SonarQube-Cloud-Analyse und kein Required-Check-Ergebnis. Vorläufige
Connector-Arbeit und Static-Validierung ersetzen keine reale Host-Runtime-
Evidence für die drei beförderten Matrixzellen.

## Nicht ausgeführte Prüfungen mit Begründung

Folgendes bleibt ausstehend oder war lokal nicht verfügbar: vollständige
Drei-Connector-Lokal-Runtime-Validierung in einer Namespace-Umgebung mit
Nicht-root-Capability (die reale Nicht-root-Namespace-Integration wartet auf
einen Hosted-Runner); Full-Matrix-Workflow-Validierung; GitHub-Hosted-
Required-Checks; actionlint, zizmor, Ruff und Pyright waren in der lokalen
Umgebung nicht verfügbar; SonarQube Cloud sowie finale PR-Exact-Head-
Validierung. CodeQL, Secret Scanning, OSV und zizmor wurden nur für den
früheren PR-Head beobachtet und nicht als Evidence für den ausstehenden
Follow-up-Head wiederverwendet.

## Bekannte Einschränkungen

Die beobachtete Nicht-root-Probe `unshare --user --map-root-user` scheitert mit
`write /proc/self/uid_map: Operation not permitted` und verhindert die
Ausführung des capability-geprüften Lighttpd-Namespace-Einstiegspfads mit
seinem vorgesehenen Nicht-root-Aufrufer. Die reale Nicht-root-Namespace-
Integration wartet auf einen Hosted-Runner. Das ist ein Umgebungsblocker für
diesen Integrationstest, kein Nachweis, dass die Kontrolle unnötig ist oder ein
schwächerer Cleanup-Pfad erlaubt wäre. Das bilinguale Dokumentationsziel ist
außerdem durch den uninitialisierten Framework-Gitlink blockiert. Die aktuelle
Task-Basis unterscheidet sich zudem vom beobachteten `origin/master`; der PR
bleibt Draft und die Delivery erfordert eine erneute Exact-Head-Validierung
gemäß der aktuellen Basisstrategie. Keine Framework-, MRTS- oder Gitlink-
Änderung ist Teil dieser Arbeit.

## Verbleibende Risiken

Bis die erforderlichen Nicht-root-Namespace-Integrationstests und adversarial
Lifecycle-Tests bestehen, ist die P1-Behebung nicht für einen
verified-PR-Claim geeignet. Die Implementierung muss weiter fail-closed sein,
statt auf pfadbasierte Löschung zurückzufallen. Die Runtime-Promotion hängt
außerdem von realer CRS-Regel-Evidence, No-MRTS-Nachweis, Cleanup-Evidence,
Exact-Head-Hosted-Checks und den erforderlichen Qualitäts-/Security-Gates ab.
Die Framework-Abhängigkeit der HAProxy-Reihenfolge blockiert derzeit die
Vervollständigung der Matrix.

## Finaler Diff- und Review-Status

Status: in Arbeit; Draft-PR #309 vorhanden, Exact-Head-Hosted-Validierung
ausstehend. Dieser Record dokumentiert eine autorisierte Parent-only-
Implementierungsarbeit und ihre aktuellen Blocker. Er behauptet keinen
Ready-for-Review-Übergang, erfolgreichen Hosted-Check, Merge, CI-Erfolg,
SonarQube-Erfolg, vollständige Matrix oder Risikoakzeptanz.
