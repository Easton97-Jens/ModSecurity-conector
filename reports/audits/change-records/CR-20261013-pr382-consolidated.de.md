# Change Record: PR #382 konsolidierte Historie und Review-Remediation

**Sprache:** [English](CR-20261013-pr382-consolidated.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261013-pr382-consolidated` |
| Datum (UTC) | `2026-10-13` |
| Basis-Revision | `4639f982a8125f4150394e4d4f2e8af4e690f494` |
| Pull Request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation und Problemstellung

Der Nutzer wünscht einen kompakten Gesamtnachweis für PR #382 statt 244
hinzugefügter Change-Record-Dateien (122 EN/DE-Paare; 1,480,067 Bytes). Dieses
Paar erhält Identitäten und unveränderliche Originale; alle 176 Records aus
master bleiben unverändert. Es dokumentiert auch aktuelle Review-Korrekturen
und das Go-Sicherheitsupdate ohne zusätzliche Change Records.

## Akzeptanzkriterien

Alle historischen Identitäten, Basen und Ergebnisse erhalten; die drei geprüften
Produktpfade und acht Sonar-Quellbefunde beheben, ohne I09/I10/I11, Engine-eigene
Body-Limits, Tests oder Gates zu schwächen. Vier Go-Module und begrenzten Updater
mit Go 1.27.2 validieren. Finale Lieferung erfordert revisionsgenaue CI, strenge
Sonar-Gates und frische Reviews. Der unabhängige historische Secret-Scan-Fehler
verhindert weiterhin vollständige Abnahme und READY_FOR_I12.

## Implementierungsentscheidung und Begründung

Die Originaltexte bleiben bei `4639f982a8125f4150394e4d4f2e8af4e690f494`. Jeder
nummerierte Indexlink erhält ursprüngliche Sprachdatei und Change-ID. Basen sind
wörtlich kopiert, einschließlich historischer kurzer/ungültiger Werte; weder
Basen noch R16/R17-Ergebnisse werden an diese Korrektur gebunden.

Historische Arbeit umfasst native Result-/Fehler-/Event-Ownership, vierzehn
Adapter-Legs und physische Sinks, NGINX-Nachweise und Integration/Qualität.
Detaillierte Fehler, Skips, Timeouts, Baselines und Folgekorrekturen bleiben in
den Originalen. I09/I10/I11-Implementierungsakzeptanz bleibt von I12-Live-Host-
Nachweisen getrennt. Native Inspection-Limits der Engine bleiben wirksam;
Connector-Ressourcenfehler bleiben technische Fehler statt erfundener
Regel-/BODY_LIMIT-Events.

Aktuelle Änderungen beheben diese konkreten Auslöser:

- Stock-lighttpd-Profile wählen jetzt explizite private Spool-Pfade. Ein Launcher
  wählt ausschließlich ein geliefertes Profil und startet die fest installierte
  native Komponente über einen geprüften Descriptor, ohne beliebige Binary-/
  Argv-Dateieingaben. Er validiert/erstellt service-eigene 0700-Verzeichnisse. Zulassung verwendet ein
  gemeinsames 256-MiB-Spool-Budget und 64 MiB freien Dateisystemreserve, vollständige
  Allokation und geprüfte Arithmetik; Erschöpfung liefert technische 503 vor
  Upstream-Kontakt. Reservierungen gelten bis zum Schließen des entlinkten
  0600-Deskriptors. Zwei Sidecars im selben Verzeichnis können das Budget nicht umgehen.
- Traefik speichert tatsächlichen Response-Commit und ersten Write-Fehler vor
  der fehleranfälligen Bestätigung. Deren Fehlschlag erzeugt weder eine zweite
  Antwort noch überschreibt er die erste Ursache.
- Benannte private C-Feldgruppen und begrenzte Diagnosebuffer-Parameter beheben
  acht Sonar-Quellbefunde bei unveränderten geprüften opaken Layouts, Offsets
  und Ownership. Der unbenutzte Runtime-Smoke-Helperparameter entfällt.
- Envoy bindet den Socket unter dem gepinnten privaten Verzeichnisdeskriptor,
  pinnt seinen eigenen Socket und veröffentlicht ohne bestehende Pfade zu
  ersetzen. Einmaliges Cleanup erhält Ersatzdateien/-Sockets/-Symlinks.
  Deterministische Austausch-, Deskriptor-/Fehler- und wiederholte Race-Tests
  sichern diese Grenze. Synchronisierung des Capacity-Tests und Join beim
  Traefik-Fake-Observer-Abschluss beheben Testraces bei erhaltenen Fehlerassertions.
- Die zentrale Go-Version ist 1.27.2; alle vier Modulminima sind 1.26.9. Envoy
  verwendet `golang.org/x/net` 0.61.0, `golang.org/x/sys` 0.49.0 und
  `golang.org/x/text` 0.43.0. `google.golang.org/grpc` 1.83.2 und
  `google.golang.org/protobuf` 1.36.11 bleiben unverändert. Der Updater repariert
  freigegebene Sicherheitsrequirements auch ohne grpc-Bump, prüft Checksums und
  begrenzte Dateideltas und erhält vertrauenswürdige Veröffentlichung nur aus
  master. Ein separater PR-Kandidatenworkflow mit Leserechten validiert vier Module.

## Geänderte Dateien

Die 244 indexierten PR-eigenen Records werden durch dieses Paar ersetzt;
Archiv-README und aktuelle Dokumentationslinks werden abgeglichen. Produktänderungen
liegen in `connectors/lighttpd`, `connectors/traefik`, `connectors/envoy`, `common`,
`connectors/haproxy` und `connectors/nginx` mit fokussierten Tests/Fixtures.
Go-Änderungen betreffen zentralen Lock, `.go-version`, vier `go.mod`, Envoy-`go.sum`,
Updater und Kandidatenworkflows/-Tests. Konfigurationsreferenzen und Compilerguides
werden durch ihre Quellgeneratoren erneuert; zugehörige EN/DE-Connector-, Build-
und PR-Dokumente werden aktualisiert. Framework-/MRTS-Quelle und beide Gitlinks
bleiben unverändert.

## Ausgeführte Befehle

Die folgenden Belege gelten für Parent-Ausgangspunkt
`4639f982a8125f4150394e4d4f2e8af4e690f494` plus Aufgaben-Workingtree-Änderungen.
Sie sind lokale Nachweise, keine Bestätigung einer noch nicht abgerufenen finalen
Remote-SHA. Exakte gewrappte Befehle, Umgebungen, Logs und Exits bleiben unter
`/var/tmp/codex/ModSecurity-conector/runs/pr382-review-20261013` erhalten.

`rtk proxy python3 ci/tools/new-change-record.py create --name pr382-consolidated --base-revision 4639f982a8125f4150394e4d4f2e8af4e690f494 --date 2026-10-13` endete mit Exit 0.

### Aktuelle Review-Remediation-Evidence

| Prüfung / Nachweis | Beobachtetes Ergebnis und Grenze |
| --- | --- |
| Vier Module: `rtk proxy go mod tidy -diff`; `go mod verify`; `go test -mod=readonly -count=1 ./...`; `go test -race -mod=readonly -count=1 ./...`; `go vet -mod=readonly ./...`; `go build -mod=readonly ./...`; `govulncheck ./...` (jeweils durch `rtk proxy`) | Alle 28 Prüfungen mit Go 1.27.2 Exit 0; `go-final/*.json` erhält modulspezifische Befehle. |
| Updater-/Versions-/Workflow-Unitsuite; actionlint für beide Go-Workflows | 71 Tests bestehen; beide Workflowchecks Exit 0; `go-updater/validation-summary.json`. |
| `rtk proxy make quick-check`; native Traefik-Targets; native Event-/Body-Suite | Exit 0; `root-validation/{quick-check,traefik-native,native-events-body}.json`. |
| `rtk proxy make check-i09-native-routes check-i10-adapter-errors check-apache-event-sink check-haproxy-spop-event-sink check-apache-native-response-limit check-common-helpers-c17 check-http-authorization-service-timeout`; `rtk proxy make -C connectors/envoy test-envoy-ext-proc` | Beide finalen Läufe Exit 0; Parent-Python und externe Build-/Cache-/kurze Socketpfade wie im Runner protokolliert. |
| Stock-Sidecar-Suite | Follow-up mit geschlossenem Launcher: 44 PASS, echter Nonroot-Start wegen UID-Namespace-Mapping `0 0 1` einmal BLOCKED; daraus folgt kein Nonroot-Runtime-PASS. |
| Konfigurationsreferenz-/All-Example-Tests und generierte Referenzprüfung; Compilerguide-Verträge | Exit 0; 22 Compilerguide-Tests bestehen; Generatorausgabe ist aktuell. |
| Kompilierte C-/Routen-/Mutationstests und privater Layoutvergleich | Fokussierte Akzeptanz besteht; opake Größe/Alignment/Offsets unverändert, einschließlich NGINX-Sanity-Konfigurationen; Nachweise in `sonar/`. Finale native Gesamt-/Envoy-Wiederholungen bestehen: `root-validation/{native-i09-i10-sinks,envoy-native}.json`, Exit 0 (234.759 / 14.283 Sekunden). |
| Unabhängiger Gitleaks-8.30.1-Scan des PR-Commitbereichs | Exit 1, zwei historische Prosa-False-Positives; Scan des aktuellen docs-Verzeichnisses Exit 0. Keine Unterdrückung oder verengter PR-Scan. |
| Offizieller OSV-Graphvergleich | Alter Head: 25 Modul-/Advisory-Paare; aktuell drei Paare, 22 entfernt, null neue. Verbleibende Paare betreffen unbenutzte OpenTelemetry-SDK-Exporter- und `x/crypto/openpgp`-Pfade; vier govulncheck-Läufe melden keine erreichbaren Schwachstellen. Keine Behauptung von null OSV-Befunden. |

Frühere Gesamtfehler und Folgekorrekturen bleiben getrennte Laufversuche;
sie werden nicht als PASS umetikettiert. Finale CI des gepushten Heads,
Sonar-Nullbefund-/Duplikationsabruf und Codex-/Security-Review stehen hier aus.

Die erste Lieferung `34b396875876d2d52e09bf44722e55d13bd9ab28` schloss die ursprünglichen
acht Sonar-Befunde, führte jedoch zwölf Befunde in neuen Tests, Launcher und
Referenztext ein. Dieses Follow-up entfernt beliebige Launcher-Eingaben, zieht
zusammengehörige Test-/Pfadhelfer heraus und erhält jede ursprüngliche Assertion.
Die CI-Registrierung ergänzt ausschließlich den neuen Go-Kandidatenworkflow in
der vorhandenen exakten Publisher-/Kopier-/Staging-Liste.
Action-Pins und Berechtigungsgrenzen bleiben gleich. Aktuelle Quellprüfung liegt
vor einer neuen normalen Lieferung; Remote-Ergebnisse der ersten Lieferung
belegen das Follow-up nicht.

Das Follow-up `f96714c5470f9148dd6971871cff688b81cc36a9` änderte einen bestehenden
Self-Repository-Workflow-Verweis fälschlich nach direktem Aufruf eines älteren
actionlint. Der unabhängige zizmor-Check zeigte den Fehler. Originalverweis `$/`
und exakte Assertion sind wiederhergestellt; der vorhandene native Wrapper
normalisiert nur validierte Verweise im Speicher für das ältere Tool,
während Security-Audits weiterhin Originalquellen prüfen.

An `8a36baac97b7a0eb177a2fb31e7b6f9f6288c338` bestanden Sonar und beide strengen
Gates ohne Befunde/Annotationen/Duplikation. Native Envoy-CI zeigte danach eine
umask-Annahme im Fixture: Erzeugung mit 0640 ergibt unter umask 077 den Modus0600.
Das Fixture stellt nun 0640 vor dem Listener-Aufruf ausdrücklich her;
die unveränderte Assertion verlangt weiterhin Erhalt dieses fremden Dateimodus.
Der Fehler ist unter 077 reproduzierbar; Wiederholungen/Race und Modulprüfungen
werden mit dieser Maske erneut ausgeführt. Das korrigiert Setup ohne schwächeres Cleanup.

## Security-Auswirkung

Spool-Zulassung schlägt geschlossen fehl und erhält Reservierungen bis zum
tatsächlichen Cleanup. Service-Administratoren müssen vertrauenswürdige private
Parent-Pfade bereitstellen; reguläre Dateiallokation ist durch Socket-Deadlines
nicht abbrechbar, fremde Dateisystemschreiber benötigen dediziertes Dateisystem/
Quota zur Isolation. Envoy benötigt Linux-procfs und atomare Veröffentlichung;
die private UID-Grenze setzt vertrauenswürdige Schreiber derselben UID voraus.
Linux bietet kein bedingtes Inode-Unlink; eine absolute Garantie gegen einen
böswilligen gleichzeitig schreibenden Prozess derselben UID wird nicht behauptet.

Gitleaks findet weiterhin `generic-api-key`-Prosa in veröffentlichten Commits
`492663334d89428dce084792145ef94e91579788` (`docs/pr-382-i09-route-audit.de.md:55`)
und `91f07e124fe09056dc46dc59d65693f406b4b1a1` (`docs/pr-382-event-contract.md:138`).
Der aktuelle Wortlaut ist korrigiert; angehängte Commits entfernen historische
Treffer nicht. Credential-Werte werden nicht wiedergegeben. History-Rewrite und
Scanner-Ausnahmen sind in dieser Aufgabe verboten; eine separate Entscheidung
ist erforderlich. Validierung, Authentifizierung, Action-Pins, Redaction,
Warnings und Gates werden nicht geschwächt.

## Runtime-Evidence

Lokale native/CGo-, Socket-, Spool-Admission- und physische Sinktests belegen ihre
beobachteten Ebenen. R16/R17 bleiben historische ausgewählte NGINX-H1-Läufe, kein
Nachweis dieses Heads, aller zehn Profile oder vierzehn Routenteile. Der echte
Service-UID-Starttest ist lokal blockiert; injizierte Ownership-/Read-only-
Kontrollen und Root-Profil-Readiness sind getrennte Nachweise.

## Bekannte Einschränkungen

Gesamtstatus: **BLOCKED_FOR_I12**. Die vollständige revisionsgenaue Delivery-
Abnahme bleibt offen, weil der historische PR-Secret-Check unter den aktuellen
Vorgaben nicht bestehen kann. Strenger finaler Sonar-Status und neue Reviews
benötigen weiterhin Remote-Abruf. Bekannte OSV-Befunde nur im Abhängigkeitsgraph
bleiben erhalten statt versteckt zu werden.

## Verbleibende Risiken

Die [I12-Übergabe](../../../docs/pr-382-i12-handoff.de.md) beschreibt Host-
Voraussetzungen, #410-Konflikte, routespezifische Client-/Reset-/Nachbar-/Log-
Belege und erneute historische Fehlertests. I09/I10/I11-Abschluss schließt
I12/V08–V10 nicht. Post-Return-Budgets brechen keine hängende Engine ab;
Late-Abort zieht bereits gelieferte Bytes nicht zurück.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständige I12-Matrix, #410-Integration, master-Merge und Deployment sind NOT RUN
und außerhalb dieser Aufgabe. Der reparierte master-Go-Updater ist nach
Integration **NOT_EXECUTED**: Fehllauf `38370968157` bleibt historischer Nachweis.
Lokale/PR-Kandidatenvalidierung beweist **MASTER_WORKFLOW_VERIFIED** nicht; dafür
ist eine spätere freigegebene vertrauenswürdige master-Ausführung erforderlich.
`GO_UPDATER_FIXED_IN_PR` wird an diesem Checkpoint nicht behauptet;
dafür ist die noch ausstehende finale PR-Verifikation erforderlich.

## Finaler Diff- und Review-Status

Alle 122 Identitäten und Originalbasen bleiben im unveränderlichen Index erhalten.
Finale normale Commit-IDs, vollständige lokale/Remote-/PR-Head-SHA-Bindung und
beobachtete Remotechecks gehören in die [aktuelle PR-Beschreibung](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
und das externe Lieferprotokoll. Historische grüne CI/Sonar werden nicht auf die
aktuelle Revision übertragen. Dieser Record erlaubt keinen Merge.

### I12-Native-Regressionen, 2026-10-13

Produkt-Ausgangsstand `8c574cdf86f10af976297c31d31485b042eba73b` bleibt die
Quelle dieser Komponentenbeobachtungen. Die alte Companion-Assertion behandelte
ein reversibel escaptes Byte als verlustbehaftet und scheiterte mit
SIGABRT/Exit134. Die korrigierte Fixture prüft verlustfreies Escaping getrennt
von echtem Escape-Feldüberlauf; physische No-write-/Hashketten-/Erstursachen-
Assertions und explizite native Request-/Response-Policies bleiben erhalten.
Produktiver Serializer-/Runtime-Code bleibt unverändert.

`make check-native-engine-body-inspection` führt die echte Companion-C-Regression
jetzt in der nativen Suite und dem bestehenden Envoy-Runtime-Components-CI-
Schritt aus. Externe SDK-Include-/Bibliotheksauswahl wird berücksichtigt;
ungültige Auswahl scheitert geschlossen. Vierzehn native Methoden bestehen mit
Systembibliothek und explizit gewählter externer Bibliothek ohne Skips;
der Companion besteht separat mit Prefix-Auswahl. Neunzehn Protokoll-/Sinktests
bestehen.

Stocks aktuelle RST-Kontrolle besteht bereits. Verstärkte Tests korrelieren
produktive P2-Entscheidung und technischen Schreibfehler und weisen danach
Deny418/Backend0 sowie Allow200/Backend1 nach. Sechs native Komponentencontrols
bestehen; ihr UID0-Scope belegt keinen Nonroot- oder Stock-Host-Abschluss.
Eine optionale echte Traefik-UDS-Regression prüft Reject/ProcessPartial,
getrennten/kombinierten EOS, beide Richtungen, geprüfte Finish-/Destroy-
Bestätigungen und Verbindungsfreigabe:
18 native Subcases bestehen mit Race-Detector; die EOS-Verlustmutation scheitert
erwartet. Kein produktiver Appendfehler ist reproduziert; die Klassifizierung
des echten Traefik-Host-Protokollfehlers bleibt offen. Diese Checks zählen
physisches natives Cleanup nicht unabhängig. Der optionale Test
benötigt den privaten echten C-Service; gewöhnliche Go-Unit-Läufe überspringen
diese zusätzliche Integration ausdrücklich.

Lokale Receipts liegen unter
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/{common-lossy,stock-rst,traefik-repair,native-wiring}`.
Dies sind lokal erhaltene Artefakte, keine hochgeladenen Downloadlinks.
`tests/README.md` und die deutsche Begleitfassung dokumentieren das neue native
Target. Framework-/MRTS-Quellen und Gitlinks, Dependencies, Gates und
Runtime-Guards bleiben unverändert. Vollständiges Live-Host-I12, finale
Head-CI/Sonar/Reviews und das unabhängige historische Secret-Gate werden durch
diese Komponentenergebnisse nicht belegt.

Die breitere Prüfung reproduzierte außerdem einen separaten Fixturefehler im
Optional-Prerequisite-Test: geerbte GNU-Make-Kommandozuweisungen überschreiben
das absichtlich fehlende Framework und private Buildpfade der Child-Fixture.
Die fünf synthetischen Nested-Make-Aufrufe entfernen jetzt nur `MAKEFLAGS`,
`MAKEOVERRIDES`, `MFLAGS` und `GNUMAKEFLAGS`. Produktive Make-/Skriptpfade,
Compilerflags und sämtliche Fehlerassertionen bleiben unverändert. Der alte
Missing-Framework-Fall scheitert mit geerbten Zuweisungen; das korrigierte
vollständige20-Testmodul besteht über das normale äußere Make-Target mit
expliziten Python-/Framework-Zuweisungen. Receipts: `optional-fixture/` im
gleichen lokalen Run. Breitere Verifikation und finale Head-Liefernachweise
bleiben getrennt.

### Übernommener historischer I12-Nachweis aus PR #410

Der normale Merge von Parent `8c574cdf86f10af976297c31d31485b042eba73b` in den
bestehenden #410-Branch erhält dessen alten Head
`511c4ac4515f0e515f68b3bbc38274c5a230d903` in der Historie.
Der zusätzliche historische Change-ID `CR-20261011-pr382-i12-host-evidence`
wird hier konsolidiert; sein [unveränderliches Original](https://github.com/Easton97-Jens/ModSecurity-conector/blob/511c4ac4515f0e515f68b3bbc38274c5a230d903/reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.de.md)
bleibt erreichbar. Der [historische I12-Bericht](../../../docs/pr-382-i12-host-evidence-20261011.de.md)
behält alle Beobachtungen; ausschließlich der historische Change-Record-Link
zeigt jetzt auf die unveränderliche Originalrevision statt die entfernte Datei.
Run `20261011T063350Z-0df51024008f-i12` testete Parent
`0df51024008fc84f0a6820f3b011055b69c3a3e2`, Framework
`99a7985c1be92a2297b1b59208f64df6768f2cbf`, MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`: 79 ausgewählte Records,
9 PASS, 6 FAIL, 53 BLOCKED, 11 NOT_EXECUTED; 13 Pflichtteile mit
0 vollständigen PASS, 2 FAIL, 11 BLOCKED. Ergänzende Stock-native-Kontrolle
separat NOT_EXECUTED. Die Zahlen sind keine vollständige Pflichtfallmatrix und
keine Ergebnisse des neuen Parents. I12/V08–V10 bleiben offen. Originale
Rohbelege und Prüfsummen werden unverändert erhalten; neue Runs haben eigene
Source-/Config-/Hostbindungen. Keine entfernten redundanten Records werden
wiederhergestellt; I09/I10/I11 und die 122 ursprünglichen Indexeinträge bleiben erhalten.

### Korrektur des Stock-Real-Backend-Evidence-Producers, 2026-10-13

Der historische physische Stock06-Log bleibt bytegleich. Seine kanonische
Engine-Entscheidung hat vor Hostbeobachtung zulässig leeres `actual_action`;
der alte Validator lehnte dies ab. Der korrigierte Validator erlaubt diesen
Contract nur für unbeobachtete Engine-/Error-Events und verlangt separat ein
beobachtetes natives Deny451 derselben Transaktion. Falsche Korrelation oder
fehlender Hostnachweis scheitert geschlossen; keine Engine-Aktion wird erfunden.

Der sieben Fälle umfassende Real-Backend-Harness erhält jeden Versuch,
physisches Stderr, Launch-/Exit-/Cleanupreceipts, direkt gewartete Clientheader,
Body/Hash/Framing und unabhängige Backend-Fehler-/Endzähler. Fehlgeschlagene Fälle
laufen nach erfolgreichem Cleanup weiter; ein Cleanupfehler stoppt weitere
Starts. Verifizierte Receipts werden erst nach Cleanup veröffentlicht.
Achtzehn fokussierte Harness-Tests bestehen, einschließlich unvollständigem
Framing trotz Client-Exit0, fehlendem Hostnachweis, falscher Korrelation und
Launch-/Cleanupfehlern. Roots echte aktuelle Stock-Host-Wiederholung bleibt
erforderlich. Lokale Receipts:
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/stock-harness/resumed-01`.
Nur der hostspezifische Harness und seine Tests ändern sich; Produktquellen,
Framework-/MRTS-Gitlinks, Scanner und native Runtime-Guards bleiben unverändert.

### Native Test-Quality-Gate-Nachprüfung, 2026-10-13

Der Sonar-Check für exakt `b982c6f35abc47eccddcfded2bfd920f92516d90` hat null
neue/akzeptierte Issues und Hotspots; der strenge Duplikationscheck meldet
jedoch 13 neue duplizierte Zeilen in
`tests/transaction_phase_runtime_companion_test.c`. Ein gemeinsamer
Eventdatei-Lesehelfer erhält dieselben Open-/Read-/Error-/Close- und
Terminierungsassertionen an vier Aufrufstellen. Die gezielte echte
libModSecurity-Companion-Regression besteht mit C17 und
`-Wall -Wextra -Werror`; `git diff --check` besteht. Der vorherige Refactor
des Traefik-Body-Policy-Tests erhält alle Fälle und besteht Modultests mit
Race-Detector sowie Vet. Beide Änderungen betreffen ausschließlich Testcode.
Remote-Sonar/CI müssen für die gelieferte Folgerevision zurückgelesen werden;
das historische Secret-Range-Gate bleibt unabhängig fehlgeschlagen.

### HAProxy-Native-Companion-Outcome-Reparatur, 2026-10-13

Echter Combined-Hostversuch `1791917296154368188` lieferte erwartete
P3-Deny403 und P4-Safe200; physische Logs zeigten jedoch gescheiterte
Outcomebestätigung/Terminal-Cleanup und Protokollfehler. Das Binding lehnte
jeden terminalen Common-Zustand ab, einschließlich erfolgreicher nativer
Blockentscheidungen. Es erlaubt jetzt das beobachtete Hostoutcome nach einer
gültigen terminalen Entscheidung; technische Fehler und Completed-/Cleaned-
Zustände bleiben gesperrt. Native Body-Limit-Reject ist Policy; Outcome und
Finish müssen BODY_LIMIT erhalten, ohne erfolgreiche Enforcement als
technischen Protokollfehler zu behandeln. Native Loggingfehler lassen Finish
weiterhin scheitern. Claim, Phase, Korrelation, Duplikat-, Größen- und
Erstursachenbehandlung bleiben durchgesetzt. Das Hostoutcome überschreibt
die Engineentscheidung nicht.

Der echte a30-Neubau/-Retest (`1791918602525320691`) zeigt danach eine zweite
Ursache: Nach erfolgreichem P3-OUTCOME verwendet der HTX-Caller eine typisierte
Connector-Error-CANCEL, weil normales MRC1-RELEASE bisher P4-EOS verlangte.
Der bestehende RELEASE-Opcode akzeptiert jetzt auch ein bestätigtes,
passendes disruptives P3-Outcome vor Commit. Client und Server teilen den
Matching-Prädikat; CLAIM-only, Allow/log_only, fehlendes Outcome und falscher
Status bleiben unzulässig. HTX verwendet bei Erfolg OUTCOME -> RELEASE ->
close; explizite technische CANCEL bleiben erhalten. Kein künstlicher EOS,
neuer Opcode oder Fehlerunterdrückung. Die Clientstruktur ändert sich;
Consumer benötigen echte Neubauten. Alte Hostinputs behalten ihre originale
Revisionsidentität.

Echte libModSecurity-/Client-/Servertests und Standalone-Clienttests bestehen.
Vier kopierte Originalguard-/Outcomevalidierungs-Controls kompilieren und
scheitern an den beabsichtigten Assertions. Receipts:
`haproxy-precommit-native-validation.json`, SHA256
`73ccabd26af1514570e9f7327812e71c825be858067aed5ce9a47599bf6d2454`,
im Task-Run. Die echte Transportregression ist in die bestehende native
Body-Suite integriert; der Overlaybuild kopiert ihren neuen privaten
Helperheader. Fokussierte Host-/Build- und Response-Handle-Contracts bestehen;
die veraltete Test-Cleanup-Signatur folgt dem tatsächlichen Integer-Return
ohne abgeschwächte Checks.

Gezielte P3-/P4-/Native-Limit-Fälle scheitern am Originalguard und bestehen
nach Korrektur. Bestehende Full-Binding-/Common-Caller-, Native-Result-,
Phasen-, Technikfehler-/Reentry- und Mutationsregressionen werden wiederholt:
Acht finale Callertests und 18 Native-/Phasencontracts bestehen; alle 26
bestehenden Zero-Argument-Transaktionscontractchecks bestehen durch expliziten
Direktaufruf, weil der gewählte Interpreter kein pytest hat. Loggingfehler-
und Originalguard-Mutationen werden erkannt.
Die native API-Naht steuert Interventionen und Cleanupzähler; diese
Komponententests sind keine Live-Hostevidenz. Externes Taskverzeichnis
`hosts-haproxy-postfix-01/` erhält echte neu gebaute Binaries und frische
Hostretests nach Abschluss; keine alte Binary wird umetikettiert. Exakte
finale Prüfungs- und Lieferergebnisse stehen im aktuellen Bericht/PR-
Lieferprotokoll.

### SPOP-Phasenmetadaten und Caller-Qualitätsfolgeprüfung, 2026-10-13

HAProxy-Versuch `1791920706986259057` mit echt neu gebauten6175Binaries
besteht8direkteHTX-Controls, scheitert aber beim regulären Combined-P3-Deny-
Cleanup. Die produktive SPOP-Konvertierung verwendet Common-Entscheidungs-
konstruktoren, setzt dadurch die Phase auf CONNECTION zurück und verliert
nativeP3/P4. Der RELEASEguard verlangt korrekt P3 und wird nicht abgeschwächt.
Die Bridge bildet jetzt native1–5 nach Allow- und disruptiven Konstruktoren
explizit auf benannte Common-Phasen ab. Produktive Ccaller-Regressionen prüfen
P3/P4 Allow/Deny/Redirect sowie Originalauslassung und numerischen Cast.
Originalfehler/-logs bleiben in `hosts-haproxy-postfix-01/retry-02` erhalten.
Gemeinsame Common-/Envoy-Quellen bleiben bei diesem Folgefix unverändert.

Hosted-Sonar des exakten6175Heads meldet einen neuen Ctest-Befund zur
kognitiven Komplexität28>25 in `check_precommit`. Unveränderte Release-/Close-
Fehlerassertions stehen jetzt im zusammengehörigen Helper
`check_precommit_cleanup_failure`. Die tatsächliche Off/Safe/Strict-Callermatrix
und ihre15Mutationskontrollen bestehen mit Exit0 in18,816Sekunden. Keine
Assertion, Compilerwarnung, Scannerregel oder Prüfung wird unterdrückt.

Der nächste Sonarcheck des exakten Heads beanstandet einen geschachtelten
Status-Ternary in der neuen SPOP-Regression. Eine Statuswerttabelle erhält
genau dieselben Allow-/Deny-/Redirect-Testinputs200/403/302 ohne Schachtelung.
Produktquellen ändern sich nicht; echte e2445-Host-/Buildidentitäten bleiben.

### Aktueller I12-Kampagnenstatus, 2026-10-13

Der [aktuelle zweisprachige Hostbericht](../../../docs/pr-382-i12-host-evidence-20261013.de.md)
ersetzt frühere Liefer-/Checkpointaussagen in diesem Record. Ergebnis ist
**I12_PARTIAL**; alle13Pflichtteile und die separate Stock-native-Diagnose
sind bewertet. Finaler Parent: `a9d48bb58aa948aea7d79e20cdf09d3f239b7808`.
Der bestehende #410 mergt den Parent normal und erhält den alten #410-Head
`511c4ac4515f0e515f68b3bbc38274c5a230d903` in der Ancestry. Kein master-Merge,
History-Rewrite, neuer PR oder Framework-/MRTS-Gitlinkwechsel erfolgte.

Die Auswahl bleibt1.406Pflicht-IDs plus78Diagnose-IDs; der
[generierte Missing-Case-Index](../../../docs/pr-382-i12-missing-case-index-20261013.de.md)
erhält jede fehlende Pflicht samt Grund. Smoke-/Driver-Exit0 wird nicht zur
vollständigen I12-/V08–V10-Abnahme aufgewertet. Historische79Records,
Fehlversuche, physische Rawlogs und originale Quell-/Buildidentitäten bleiben
erhalten; alle85.108historischen Manifesteinträge wurden unverändert nachgehasht.

Echte Apache-Sink-/Recoveryprobes, direkte/Combined-HAProxyprobes, Envoy-
Request-/Responseprobes und lighttpd-Stock-/Patched-/Kontrollbeobachtungen
bleiben in runspezifischen Paketen erhalten. Zwei reproduzierte HAProxy-
Terminal-Cleanupfehler und Phasenmetadaten sind im Parent mit nativen Negativ-/Mutationschecks
repariert; SPOP/HTX aus e2445 und Envoy aus 6175 wurden wirklich neu gebaut
und getestet. Begrenzte Inputvergleiche binden unveränderte Produktinputs
an finalen a9, ohne tatsächliche Build-/Runidentitäten umzuetikettieren. Verbleibende NGINX-/Traefik-/Patched-Launchervoraussetzungen
und physische Lifecycle-/Transport-/Korrelationsproducerlücken sind explizit
benannt. Fehlende Felder bleiben null. Harnesskorrekturen erhalten native403-
Policyergebnisse, gültige leere unbeobachtete Aktionen und Cleanupreceipts;
physische HAProxyfehler in Normalfällen verhindern jetzt PASS-Veröffentlichung.

Die spätere Sicherheitsscope-Anweisung wird umgesetzt: Advisory-Freigabe
wurde geprüft, kein weiterer Deep-Scan-/Review-Trigger erfolgt. Der bereits
belegte historische Gitleaks-Rangefehler bleibt ein unabhängiges Release-Gate.
Finale lokale Prüfungen geänderter Pfade und Hosted-Ergebnisse des exakten
Heads stehen im aktuellen Bericht und Lieferprotokoll. Beide PRs bleiben Draft.

### Begrenzte PR410-Sonar-Reparatur, 2026-10-14

Der aktuelle Auftrag erlaubt ausdrücklich Analyse und Reparatur der echten
PR410-Befunde. Die authentifizierte Abfrage über den kanonischen Sonar-Wrapper
liefert zehn offene Issues am Ausgangshead
`1a40c9109f7aef3373ec24019000eb9ebe4dc27b`: drei HIGH-Security-Auswirkungen
und sieben Wartbarkeitsbefunde. Der revisionsgenaue GitHub-Check `115518660334`
scheitert ausschließlich an `new_security_rating`, C statt A. Der fehlgeschlagene
Providertext enthält keine Befundzähler; beide strengen Scaffold-Prüfungen
scheitern deshalb korrekt fail-closed. Kein Parser wurde geändert und kein
fehlender Zähler als null interpretiert.

Die beiden `pythonsecurity:S8707`-Pfade wurden mit synthetischen Bytes und
privatem Loopback-Listener reproduziert: Der interne Client-CLI konnte eine
beliebige Datei lesen und Ausgabe außerhalb seines Fallverzeichnisses anlegen.
Sein einziger normaler Aufrufer öffnet feste Artefaktnamen jetzt exklusiv über
den bestehenden deskriptorbasierten `PrivateRuntimeRoot` und übergibt dem Kind
nur eigene reguläre Dateideskriptoren. Exakt 0600, ein Link, unterschiedliche
Identitäten, passende Zugriffsmodi und frische Ausgabe bleiben geprüft.
Binäre/partielle Antwortbytes, Zeitlimits, bestehende Antwortgrenze und
Exit77 bleiben erhalten.

Der `pythonsecurity:S8705`-Git-Aufruf nutzt feste Argumente ohne Shell; eine
Optionsinjektion wurde nicht nachgewiesen. Die echte ungeprüfte Auswahl eines
fremden Checkouts wird durch Bindung an den eigenen kanonischen Quellroot
geschlossen. Git erhält feste Argumente und diesen vertrauenswürdigen cwd.
Beide Artefaktprobes haben zehn Sekunden Deadline; Hash-, Versions- und
Quellgleichheitsprüfungen bleiben verpflichtend. S108, zweimal S3776, S9154
und dreimal S5778 werden ohne Unterdrückungen korrigiert.

Eine unabhängige begrenzte Voruntersuchung und Kandidatenprüfung fanden keinen
konkreten verbleibenden Bypass oder Kompatibilitätsfehler. Root führte 79
fokussierte Tests beider Harnesses, nativer Spool-Verträge und strenger Sonar-
Parserkontrollen mit dem ausgewählten SDK erneut aus: Exit0, keine Skips.
Whitespace besteht. Exakte RTK-Befehle, Quellhashes, Exits und Original-Logs
bleiben unter
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/`
erhalten; die ursprüngliche synthetische Reproduktion liegt unter `sonar-stock/`
dieses Runs. Am Reparaturhead `4f59d1632322a78676e224ef40c0ab7c8e96286c`
bestätigt die Cloud Security Rating A und Quality Gate OK. Sieben neue
Wartbarkeitsbefunde bleiben von den behobenen Sicherheitsbefunden getrennt:
S1192 für den wiederholten Request-Artefaktnamen und sechs S5778-Ausnahmetests.
Der Folgepatch verwendet eine Dateinamenkonstante und ermittelt Deskriptorwerte
vor der Ausnahmeprüfung; alle Negativfälle bleiben erhalten. Root wiederholte
dieselben 79 Tests mit ausgewähltem SDK: Exit0, keine Skips; zweiter Receipt
`verification/focused-02/`. Vollständiges quick-check samt EN/DE-, Link- und
Variablenprüfung Exit0 in 197,163 Sekunden. Revisionsgenaues strenges Null-Issue-
und Scaffold-Readback des neuen Heads ist noch offen; kein Parser oder Gate
wurde abgeschwächt.

Am exakten Folgehead `71ba09f0a695c333c2c10d3a0db46d2dc956ec40` besteht
Sonar-Check `115688597895` mit null neuen/akzeptierten Issues, Hotspots und
Annotationen. Authentifiziertes Cloud-Readback bestätigt Rating A/Gate OK und
null duplizierte Zeilen, Blöcke und Dichte. Scaffold-lint-Job `115687673149`
besteht ohne Parseränderung. Diese Fakten gelten für diesen Head; spätere
Lieferung erfordert erneut frisches Readback.

### NGINX-Ownership-Handoff mit begrenzten Rechten, 2026-10-14

Der ursprüngliche Harness reproduziert chmod-EPERM nach Worker-chown unter
Maske `0xc1`. Die Reparatur erstellt den vollständigen Unterbaum und setzt
exakt0700 vor Übergabe erst der Kinder, dann der Eltern. Wiederholter Handoff
prüft alle acht vorhandenen Pfade unter aufgelöster Workeridentität ohne
Inode-/ctime-Änderung. Symlink-, UID/GID- und Modusabweichungen bleiben
abgewiesen. Die Wrong-Owner-P4-Negativfixture setzt ebenfalls0600 vor chown;
ihr Ablehnungsvertrag bleibt erhalten. Nur NGINX-Harness und Ownershiptests
werden geändert.

Sieben echte Root/nobody-Tests einschließlich realem Framework-Materializer
bestehen in 2,487 Sekunden. Der erste Aufruf im Command-Sandbox hatte nur
UID0 abgebildet und konnte weder Bounding-Set reduzieren noch chown65534
ausführen; dieser Umgebungsfehler bleibt erhalten. Der autorisierte Outside-
Rerun nutzt echte UID-Abbildung; die fünf Capability-Regressionen reduzieren
ausdrücklich auf `0xc1`. Receipts liegen unter `nginx-handoff/` des Task-Runs.

Frische Offline-NGINX1.31.6-/Modulbuilds kompilieren 33 aktuelle Parentinputs
aus `a9d48bb58aa948aea7d79e20cdf09d3f239b7808` mit C17/GCC15.2.0 und echtem
libModSecurity3.0.14. Build-/Versions-/Linkage-Exit0 ist keine Hostabnahme.
Der ausschließlich private Namespace-Worker-Alias0711 erhält Host-Attempt/
Data0700. Zwei harmlose echte Admissions reproduzieren fehlendes runuser-PAM
und Master-EACCES auf worker-privaten Logs. Private gesperrte Fixturekonten
mit PAM-Root-/Unix-Prüfungen beheben Ersteres; Letzteres braucht separat
explizite DAC-Admission und nativen Hosttest. Setup-Probes behaupten keinen
HTTP-Request oder I12-PASS. Originale Controller-/Quell-/Specs und Outside-
Cleanup-Receipts ihrer einzelnen Attempts bleiben unverändert erhalten.

### Physischer Lifecycle-Observer und privates Traefik-Staging, 2026-10-14

Der GNU-Linker-Observer ausschließlich für Tests erhält tatsächliche Argumente,
Rückgaben und errno. Er erfasst Aufrufpaare, getrennte Host-/kanonische IDs und
den öffentlichen Common-Zustand an jeder Aufrufkante. Wiederholte erfolgreiche
Finish-Aufrufe im Terminalzustand bleiben Versuche, keine erfundenen Übergänge.
Zwölf Wrapper erfassen externe Linkreferenzen; interne Aufrufe desselben Objekts
können sie umgehen. Privater geerbter Append-Ausgabedeskriptor, Fork-gemeinsames
Bytebudget, Invalidierungskontrollen und finale Belege begrenzen die Beobachtung.
Fehlende Abschlussbelege oder offene Zuordnungen verhindern Qualifikation;
native MIME-Auswahl und tatsächliches Host-EOS bleiben null. Releaseartefakte
bleiben ohne Instrumentierung.

Kontrollen mit ausdrücklich ausgewähltem SDK und der additive NGINX-Modul-Relink
bestehen. Baseline-Modul und Objekte bleiben unverändert. Das neue ausdrückliche
Make-Target blockiert fehlende Ausgabe-/SDK-Konfiguration. Diese Komponenten-/
Linkergebnisse belegen keinen Host-PASS. Belege liegen im aktuellen externen Run
unter `native-observer-root/`, `native-observer/`, `nginx-observed-build/` und
`verification/harness-02/`.

Die ersten echten isolierten Traefik-Versuche erhalten Compilerfehler und
verweigertes Cleanup der privaten Kopie. Ein falscher Fixture-GCC_EXEC_PREFIX
verlegte die Bibliothekssuche des vorhandenen Compilers; Entfernen reproduziert
unabhängig FAIL/PASS. Der native Harness normalisiert ausschließlich seinen
frisch kopierten Plugin-Workspace auf Verzeichnisse0700/Dateien0600 und erhält
versiegelte Quelle sowie Cleanup-Identität. Eine Regression belegt Quellerhalt,
private Kopie und sichere Entfernung bei erhaltenen Logs. Der veraltete Inventar-
Test prüft acht aktive Steuerfelder und beide abgewiesenen Decoder-Tombstones
getrennt; dokumentierte UDS-Chunk-Grenzen bleiben32768. Kein Connector-eigenes
Gesamt-Inspection-Limit wird wieder eingeführt.

Revisionsgenaue e5c02189-Checks sind terminal:22 erfolgreich/zwei bedingte Skips;
SonarGateOK/RatingA, null neue/akzeptierte/Hotspot-/Annotationsbefunde und null
neue Duplikationsblöcke/-zeilen/-dichte; scaffold-lint besteht ohne Änderung des
strengen Parsers. Dies attestiert ausschließlich e5. Spätere Commits benötigen
eigene Abrufe. Echte Host-Retakes und die Qualifikation sämtlicher1484 Fälle
stehen an diesem Zwischenstand weiterhin aus.

### Unveränderlicher Originalindex

Jeder nummerierte Link identifiziert eine Original-Change-ID durch ihren Dateinamen.
Die entsprechende Zeile des Sprachpartners verlinkt das ursprüngliche Gegenstück.

| Original | Ursprüngliche Basis-Revision |
| --- | --- |
| [001](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.de.md) | `b779167ff979aa73cdd9321a829f9c693d943760` |
| [002](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md) | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| [003](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-chain-link.de.md) | `3730eaa03b2f76ccac3baebfc862d8a8417c99ef` |
| [004](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-context-accounting.de.md) | `96c41eb287778e807daeba5b28f97bd5d86fbc0a` |
| [005](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-decision-errors.de.md) | `1301a4e30f04cb82dd0546607bfaab1461671b7b` |
| [006](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-envoy-bridge.de.md) | `57d42c575372edca0149465038d8a683a11d494d` |
| [007](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-native-intervention.de.md) | `7a52a55cfa4eb4c4c85ed44396e7137ef013f5aa` |
| [008](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-native-logging.de.md) | `1ce569e1afce55e17c767e1e06b0266874fe8c3e` |
| [009](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-nginx-result-tail.de.md) | `81e53a943fb149a92eb4214091f81a217c567f8b` |
| [010](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-nonrule-observation.de.md) | `7fe606c56a423f05454fe200f07a1c03d007ea3f` |
| [011](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-profile-errors.de.md) | `97d3ea10d526f8ab306bc1cc24fa63f573f36bc9` |
| [012](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-route-completion.de.md) | `68f78e079d88c80f82d1297c651f0e38e9624308` |
| [013](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-runtime-sink-errors.de.md) | `0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9` |
| [014](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-sonar-counts.de.md) | `e8d5e5081f166e8a9b01bbb84ce4baf6530109d9` |
| [015](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-apache-adoption.de.md) | `cac867da7292f6ca82fc76fee3b974382881c5b1` |
| [016](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-apache-native-lifecycle.de.md) | `ad22918e92849a10483439d72ac9a50154ec00be` |
| [017](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-envoy-native-verification.de.md) | `ee33afc5bbb961f2d0d612c5ff591eb073fd02ce` |
| [018](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-envoy-test-boundaries.de.md) | `3c29004b060b461649383cdb0db9996feab51b05` |
| [019](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260927-nginx-first-byte-safe.de.md) | `1bf1dcd46d25ba5b22f8a7d5915b5f72b4daa4da` |
| [020](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260927-nginx-lifecycle-output-root.de.md) | `57b0ed6a72ff7c7235037a59f008164be673e7a5` |
| [021](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260927-nginx-projection-invocations.de.md) | `9fbaa70227b17d71c11005bc45984a11b9dd5dce` |
| [022](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260930-nginx-no-crs-native-event-sink.de.md) | `3de8043c2482b52debc6f6e2d9ca609adf257eab` |
| [023](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260930-nginx-port-cleanup.de.md) | `91fce858acea9273d649e0bca1a5c2faadd28f9a` |
| [024](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260930-nginx-redirect-location.de.md) | `0fe4c7b8cf4b021663985d895064e56cd2c63410` |
| [025](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-audit-result-pointer.de.md) | `2634d821acd80ad208a8e1cd3e4f49fd7e80c628` |
| [026](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-configtest-collection.de.md) | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |
| [027](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-configtest-receipt.de.md) | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |
| [028](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-empty-header-driver.de.md) | `e9d022ed16d9df469baa9b12070786468706ced7` |
| [029](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-h1-request-binding.de.md) | `75e2a24bcdc3ee97dab0d6f5a0e52e76b0b542c4` |
| [030](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-framework-sonar-gitlink.de.md) | `209e6f003282695e62876332a4b916eb3e170969` |
| [031](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-nginx-configtest-path-authority.de.md) | `acefed5c81a56f636610601edcc447a257b9e947` |
| [032](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-nginx-size-configtest.de.md) | `b1dd58a1289a84f15903fa0bb46474cf776e67db` |
| [033](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-pr355-pr396-integration.de.md) | `ac4c746f6a4c07006f25b078f660e31b16341479` |
| [034](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261007-pr396-ci-fixture-contracts.de.md) | `1f68c3742bd29b23a6938b36816adff4524944c7` |
| [035](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261007-protected-nginx-1316.de.md) | `60034d48dcee4ae5225bfaff012c48413cc0acd8` |
| [036](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-common-mapper-body-pointer-invariant.de.md) | `85397f4d621c568316566faccac6c217fc5315d8` |
| [037](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-harness-explicit-content-type-omission.de.md) | `5788ba5ced597106911785a5407b2024c68bbaf2` |
| [038](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-hostruntime-binary-artifact-hash.de.md) | `810a9b5621b04c79d58b1429c3182f1668e672c9` |
| [039](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-baseline-shell-environment.de.md) | `461bcd62a3cb2159ec9750db6ad64f0ab6053cc3` |
| [040](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-first-byte-shell-environment.de.md) | `8c19e31a21f0388b7b1417f0d25bb6530f496fae` |
| [041](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-unit-fixture-boundaries.de.md) | `06df37a5fc8963bdc8c9c5577d602b9861e4bb4d` |
| [042](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-uri-budget-cleanup-20261008.de.md) | `7c169f5bbe946650431f8e0cdbe2ddc63d3e85c1` |
| [043](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-admitted-native-begin-ledger.de.md) | `20478534e305a35c7f92fd80e8303a92121a5a3a` |
| [044](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-adoption-timing-dependency-boundaries.de.md) | `2ee41e347b8d6c7ac3eabc91aa3aa05f1690b279` |
| [045](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-bounded-native-uri.de.md) | `68bf814e0d850f68f20bd26da59ed7a351e3633d` |
| [046](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-cleanup-observation.de.md) | `201c6194a0061efe49e854a02f8626170ddee3b1` |
| [047](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-common-input-fault-driver.de.md) | `48243d5f77a6ae52b52729b6d6a2447229f6fab6` |
| [048](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-config-three-native-contracts.de.md) | `45754c0a0f0ae3dbd04f63a028d342bdac61220a` |
| [049](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-event-boundary-driver.de.md) | `bc9587f086b1e4ff558a870f2d5020aa22f72b64` |
| [050](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-event-boundary-serialized-callback.de.md) | `1940c1dbda6b371248a37f257c19df9b60fd836d` |
| [051](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-lifecycle-sequence-driver.de.md) | `b7403e30111688da00d8e7ce376ea91ced1c6145` |
| [052](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-merge-c17-unused-context.de.md) | `fe43865c03e89c0e8b0e1ae7dfbd5a9e11a7b602` |
| [053](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-missing-rules-filename-quality.de.md) | `8004340da887d143bc5e850822ac122eb5ce8b59` |
| [054](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-authority-baseline.de.md) | `6b069af4c2c87cdbddd7efc8867f642b1dd03098` |
| [055](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-authority-mrts-root.de.md) | `603e84493dcb51ab72eadb5a7102c4977cab631c` |
| [056](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-authority-producer.de.md) | `9ecd63fce94d424526fe6a70da1021c8f0d02681` |
| [057](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-cleanup-and-technical-faults.de.md) | `f0aa2fe099837d44d760012d28bd247729c73120` |
| [058](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-dispatch-overrides.de.md) | `9dcd35c7e380c1fc46d12bfd1fa53cfacb999775` |
| [059](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-fixture-followup-framework-pin.de.md) | `ca8ac4b0598da65b178f670652047052cda7a531` |
| [060](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-mime-driver.de.md) | `70bfce7f6e776f49ae3f8160b18fed6b8fe4779a` |
| [061](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-operation-collection.de.md) | `63d2f9a38c506e5122ace9ba36927add7f47e377` |
| [062](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-required-framework-pin.de.md) | `767de5bf4e901f256dffbca76547af4ee6b54757` |
| [063](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-response-limit-classification.de.md) | `8b575c094140f3a92bb030a83f27b4c44b00127e` |
| [064](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-p3-technical-source.de.md) | `ec632b50d439385859113f9667fcbddb29cde357` |
| [065](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-phase4-bounded-host.de.md) | `b7403e30111688da00d8e7ce376ea91ced1c6145` |
| [066](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-phase4-completion-observation.de.md) | `0981e437968a3d0df5cd6200f4d55b0128e4874e` |
| [067](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-phase4-native-body-observations.de.md) | `764402f47b7d2db941e5002485b205b4d4563cbd` |
| [068](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-pointer-protocol-cleanup-selection.de.md) | `bcb02b6b20c2e0697be3c0cd8013ce9b28aa1afa` |
| [069](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-post-return-engine-budget.de.md) | `49e2011b21893d1d30fdeedbe177deb48af0e4ce` |
| [070](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-projected-jsonl-source-guard.de.md) | `8004340da887d143bc5e850822ac122eb5ce8b59` |
| [071](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-protocol-fixture-executor-contract.de.md) | `708e15aa4623b2b039d333e8f654753a027a554d` |
| [072](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-raw-h1-native-invocation.de.md) | `883693506efa4ce64a016e2a440ac20ace367efd` |
| [073](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-response-limit-signature.de.md) | `91625ef984dcff914ea3a631dc738645d78abf45` |
| [074](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-selected-native-host-wiring.de.md) | `b7f3bb22a8ee5ebfe78a0f3b4fb3b32238200f91` |
| [075](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-seven-contract-hostoperations.de.md) | `a44d276b37f4ba1ce2c57af2f016d4cf96af43b6` |
| [076](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-source-p1-completion.de.md) | `9cfae553e7e69b1db8211f1a4ce0afc986b88604` |
| [077](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-standard-h1-forwarding.de.md) | `e3fcd1c7d5a9ce09abde7c9593a15690d7ed08f0` |
| [078](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-startup-quality-refactor.de.md) | `54877d2824c402a3912c71755bac7fcc884da5f4` |
| [079](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-response-fixture-content-type-omission.de.md) | `b7403e30111688da00d8e7ce376ea91ced1c6145` |
| [080](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-scheduler-lock-reuse-fixture-control.de.md) | `5e22a9f0cc9b688ddc271012467b053bca8d1bfb` |
| [081](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-scheduler-refill-causal-barrier.de.md) | `d76cb01c84350dbaeb380929bcc80a9c7719789e` |
| [082](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-selected-nginx-native-operations.de.md) | `4a28d86fa0d052397e74f0843ca6931e3dd17cae` |
| [083](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-sonar-s5778-release-test.de.md) | `3ddeb8f6bfab3c619e6db50c2b0621dc0a504c19` |
| [084](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-native-input-ledger-fd.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [085](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-native-python-quality-sink.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [086](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-body-buffer-event-scope.de.md) | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |
| [087](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-ci-terminal-fixture-seams.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [088](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-cleanup-pool-lifetime.de.md) | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |
| [089](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-driver-contract-construction.de.md) | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |
| [090](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-driver-quality-boundaries.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [091](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-early-mapper-event-selection.de.md) | `407b647ce007daae5340cb87d2ead57f7ab4a730` |
| [092](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-exception-test-isolation.de.md) | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |
| [093](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-fresh-raw-run-mode.de.md) | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |
| [094](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-input-fault-inherited-fd-20261009.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [095](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-native-collection-authority.de.md) | `cf95e1e2519909d498a4a6fdb0e21db16b2ae3c4` |
| [096](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-native-readers-pin.de.md) | `e319c932db7da011feca54fcb1fc5d2ab5d6018f` |
| [097](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-native-receipt-single-write.de.md) | `e5e8569eaf0f0ce1cdc8b56e3181d872d03eb9a8` |
| [098](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-phase4-path-input-adapter-20261009.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [099](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-phase4-reject-header-flush.de.md) | `75686a47ba971d33c46f4f40a844bbe53d7465f1` |
| [100](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-projection-case-identity-20261009.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [101](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-ruleid-adoption-delegation.de.md) | `c09480ff9b5b83b52883f5cf116266f1da5ca4d1` |
| [102](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sequence-driver-quality-phases.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [103](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sequence-prefix-publication-barrier.de.md) | `fabc2b7b436cf1fe276a4fc681e8edc1221145b7` |
| [104](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sequence-static-probe-cleanup.de.md) | `b884c6653a72dc490c4ae472dd3cbf5a1ee646b8` |
| [105](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sonar-c-quality-20261009.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [106](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-upstream-header-reader.de.md) | `c57e6b0a930161e83cb59bf5905a6db00311dc91` |
| [107](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-selected-native-projection-parent-authority.de.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [108](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-apache-adoption-check-batching.de.md) | `ff162ecb11217320a81829169a72ca4a5a4081f9` |
| [109](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-nginx-ab-cognitive-followup.de.md) | `2686b07aaf64b0541d743b53970008bd86caa91f` |
| [110](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-nginx-first-byte-snapshot-binding.de.md) | `b0d75ef6bbc33228423aef65d8ea3409387ab30f` |
| [111](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-nginx-intervention-outcome-projection.de.md) | `dca17fd5690c2ec2b8806024d1061744db8c3ad8` |
| [112](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-pr382-nginx-system-reference.de.md) | `2a5704f82fdae4ba75902eb3f4244225838e1747` |
| [113](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-r17-pr382-nginx-system-evidence.de.md) | `b2622a5d6ca746485c08f4789208299a111f47c7` |
| [114](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-r17-strict-client-full97.de.md) | `2f02370b07149265841411894f1a2cf7f1e978ff` |
| [115](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-remove-phase4-body-limit.de.md) | `b4044d10682cb2881c218fe84cebe41e61b235c2` |
| [116](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-i09-native-route-reconciliation.de.md) | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |
| [117](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-b09-secret-scan-followup.de.md) | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| [118](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-i10-adapter-errors.de.md) | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| [119](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-i11-physical-sink-parity.de.md) | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| [120](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr406-i09-i11-conflict-resolution.de.md) | `6a79efe7d571d9fc980f970a08073d6334c36a7a` |
| [121](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-response-limit-policy-removal.de.md) | `2619b20b9d2e70fa07cbe71f664b48ff3c105380` |
| [122](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261012-pr409-base-refresh.de.md) | `1e7f7c8405ddcc7fc4a5ff117ef45c5bf0686707` |
