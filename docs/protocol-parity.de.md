# Workstream zur HTTP/2- und HTTP/3-Protokollparität

**Sprache:** [English](protocol-parity.md) | Deutsch

Dies ist ein unabhängiger laufender Parent-Workstream. Er dokumentiert die
aktuelle Evidence für HTTP/2- und HTTP/3-Lifecycle-Parität über die sechs
ausgewählten Connectoren. Dies ist keine Abschlussbehauptung. HTTP/1.1 bleibt
die Regressions-Baseline.

## Aktualisierung am 2026-11-02: Fixture-Integration, keine Protokollpromotion

[Framework #153](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/153)
wurde am `2026-11-02T06:11:26Z` regulär per Squash in
`f11d4617ff98ad615c72c1b6672fc386394db41e` integriert. Sein vollständiger Baum entspricht
geprüftem PR-Head `64e53d3a9c850711493f1349b44c1290d6486e1f`, einschließlich
unabhängigem #152. Alle fünf vorhandenen Mapper-Methoden bestanden beide
V3-Modi mit strengem C17, 14 beobachteten Probes/zehn benannten Unterfällen je
Modus und ohne Skips; angrenzende Verträge, native Generatoren, Docs/Secrets,
Head-CI/CodeQL/Sonar bestanden. Dies sind Fixture-/Vertragsergebnisse, keine
Live-H2-/H3-/TLS-Qualifikation.

Der aktuelle Benutzer autorisiert separat geordnete reguläre Integration von
#153 und bestehendem #348. Parent übernimmt mastere6b36f7 normal und pinnt den
tatsächlichen Framework-Merge-SHA mit nativen Werkzeugen. Framework-Masterprüfungen,
neues Commitpaar, frische Parent-Gates/-Provenienz/-Reviews, exakter Parent-Merge
und tatsächliche Parent-Master-/Baumprüfungen bleiben an diesem
Vorbereitungspunkt verpflichtend. Frühere Mergeverbote/offene Schritte unten
sind datierte Snapshots, nicht aktuelle Freigabe oder Pin. MRTS unverändert;
keine vollständige Protokollqualifikation behauptet. Den gepaarten
Fixture-Pin-Change-Record beachten.

## Aktualisierung am 2026-11-01: migrierte Tests und Framework-Integration

Die Testverantwortung ist ins Framework umgezogen. Parent-PR #348 übernimmt
Parent-Master `a6001a09`, zunächst mit Framework-Pin `d503ddbe`. Fünfzehn
veraltete Parent-Pfade werden entfernt statt wiederhergestellt; die 13
zugeordneten Prüfer-/Testdeltas erhalten 24 Definitionen (19 Go, fünf Python)
im Framework und bleiben aus Parent-Historie `db431efa` wiederherstellbar.

[Framework-PR #148](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/148)
integriert diese Ports und die Transferabschluss-/NGINX-QUIC-Fixes aus #143/#144.
Sein regulärer Squash-Merge erfolgte um `2026-11-01T19:09:19Z`; der remote
verifizierte Framework-Master an diesem Checkpoint war
`91f5370c7eddcebdc7e49d2099c58054ec2d5d5d`.
Der finale PR-Head bestand 15 Hosted-Prüfungen bei drei vorgesehenen Skips.
Die direkte Sonar-Rücklesung für genau diesen Head ergab ein OK-Gate mit allen
fünf Bedingungen und null offenen PR-Issues. Getrennt davon bestanden alle
sieben Workflows auf Master `91f5370c`; dessen direkte Sonar-Analyse um
`2026-11-01T19:26:02Z` bestand alle fünf Bedingungen (Ratings 1 <= 1,
Duplikation 0 <= 3%, Hotspots 100 >= 100%). PRs #143/#144 wurden ungemergt
mit Verweis auf #148 geschlossen; ihre Branches auf `b7d643f` / `9e49913`
bleiben erhalten.

Die finale native Parent-Validierung deckte weitere Migrationsintegritätsfehler
auf. Der Produktgenerator `scripts/generate_compiler_guides.py` bildet nun den
öffentlichen `source_path` des NGINX-Preparers ab statt dessen gelöschten
Parent-Pfad zu referenzieren und korrigiert die tatsächlich migrierten Apache-/
HAProxy-Harnesslinks. Alle 18 generierten Guide-Ausgaben bleiben byteidentisch
zu ihren versionierten Fassungen. Die ausgewählte Parent-Projektions-/Revisions-/
Kandidatensuite bestand 55 Tests. Apache bestand zunächst 21 Tests und
scheiterte an einer veralteten vollständigen AST-Golden-Erwartung.

Separater [Framework-Draft #150](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/150),
erster veröffentlichter Head `e1b4f8b24ab95749d685db3e6581e26da302dd57`
auf Basis `91f5370c`,
repariert zwei bestehende Testmodule: Compilererwartungen/tatsächlich
weitergeleitete Make-Targets und das unabhängig auditierte vollständige
AST-Golden. Sechs Migrationskontext-Transformationen rekonstruieren den Prüfer
seit #142 bytegenau und erhalten alle Prädikate, Meldungen, Reihenfolge und
Kontrollen. Die kombinierten 44 Methoden bestanden in 27.660 Sekunden;
acht tatsächliche Target-Kontrollen und 26 isolierte Parserkontrollen bestanden
ebenfalls. Native Apache-Targets mit #150 sowie NGINX und Common C17 bestanden.
Native Generierungs-, Bindungs- und Zulassungszahlen bleiben unverändert
(526 feste Framework-Bindungen / 235 Produktpfade); 350 Dokumentationspaare und
vier kanonische Checks bestanden. #150 führt keine neuen Methoden, Selektoren,
Versionen oder abgeschwächten Gates ein.

Framework #147 setzte Master danach mit Host-Ausführungskontext-Preflights auf
`5ef57603a4933f18c988f1f9f32b93f478182440`. #150 integriert diesen Master
normal auf seinem neuen veröffentlichten Head
`af6997be5c5cee38e3feb9274c3269d52784bbe1` und ersetzt den ersten Kandidaten.
Native Regenerierung löst den Inventarkonflikt unter Erhalt zweier neuer
Preflight-Bindungen und fünf Standardverbraucher; gegenüber `5ef57603`
unterscheidet sich im Inventar nur der beabsichtigte Compiler-Testhash.
Aktuelle Zulassung umfasst 528 feste Framework-Bindungen / 235 Produktpfade;
100/80 Standard, 2586/1140 optional und 1993 Basis-IDs bleiben unverändert.
Inventar-SHA-256:
`147ebacc795c634bd9d4b21cfbcd408e635dd55de8b757be2671d3b056ac1cb8`.
Frische 44-Methoden-Validierung bestand in 26.138 Sekunden; native Generierung/
Checks, öffentliche Zulassung, 354 bilinguale Checks, 2159 Pfadchecks ohne
veraltete Pfade, Record-/Linkchecks und vier kanonische Checks bestanden.
Unabhängiges Review bestätigte beide Testfixes unverändert und keinen EN/DE-
oder Inventarblocker. Der frühere #150-Compiler-Guide-Einstieg bestand außerdem
22 Tests in 0.848 Sekunden bei 18 byteidentischen Guides. Diese Ergebnisse
starten keine Hostkampagne.

Framework #150 wurde tatsächlich mit Exact-SHA-Guard um
`2026-11-01T20:11:25Z` per Squash gemergt; offizieller Master ist
`b85280278310f4034af78149ac13671438965c7b`. Sein vollständiger Tree entspricht
`af6997be`. Dieser PR-Head bestand 12 Checks / drei vorgesehene Skips;
direkte Sonar-Analyse um `2026-11-01T20:03:53Z` bestand alle fünf Bedingungen
(Ratings 1 <= 1, Duplikation 0 <= 3%, Hotspots 100 >= 100%), die vollständige
OPEN/CONFIRMED-Abfrage ergab null Issues. Drei CodeQL-Analyze-/Post-Analyze-
Konfigurationen bestanden im begrenzten Modus ohne Upload. Neue `b8528027`-
Master-CI steht aus und wird nicht vom PR übernommen. GitHubs konfiguriertes
Auto-Delete entfernte den Remote-Branch von #150; lokaler Branch/Worktree und
die ausdrücklich behaltenen #143/#144-Branches bleiben unverändert erhalten.

Unabhängiger Parent #435 wurde um `2026-11-01T19:49:13Z` in Master
`2abad408cae7e5a103d12a9a9e432129bfe0468f` gemergt, mit geerbtem Framework-
Pin `e628`, nicht `91f5370c`. Ein sauberer normaler Merge erzeugte lokalen Parent
`5b5a4a89aa9cb55b0b95b485611aadb78f276185`; nur die eingehenden zwölf
Middleware-Zeilen werden mit den Paritätsänderungen verbunden. Unabhängiges
Quell-/Security-Review fand keine P3-/EOS-/Protokollregression. 23 Pinprojektionen
entsprechen Master; MRTS-/Versionswerte bleiben unverändert. Frühere generierte
Zwischenansichten wurden vor dem Merge extern gesichert; Aufgabenquellen und
Dokumentation blieben erhalten.

Begrenzte Merge-Interaktions-Unitvalidierung bestand mit 16 Paritäts- plus sechs
informativen Selektoren: 22 Top-Level-Tests, 53 erfolgreiche Test-/Subtest-
Abschlüsse plus Paket-Pass, 48 Leaves einschließlich aller 31 informativen
Leaves, null Fehler/Skips und kein Race-Report. Dies verwendete den gemergten
Worktree vor dem lokalen Merge-Commit, keine Qualifikation des gesamten
committeten Heads. Sein Middleware-SHA-256 bleibt nach Commit
`b8df119f43332c00e7308478cae3f84a5f2d015a96e8d4e9c18d74261e73884b`.
Dies ist echte httptest-Unit-Evidence, keine Native-Host-, private Common-Dienst-,
TLS-/H2-/H3- oder MRTS-Ausführung.

Finaler lokaler Pin-Abgleich ist implementiert, noch nicht committet/gepusht:
Verschachteltes Framework und gestagter Gitlink sind exakt `b8528027`; nativer
Lock und 22 Workflow-Ansichten sind synchronisiert. Native Pre-Candidate-
`e628` → `b8528027`-, 23-Dateien-Sync-, No-Drift- und Post-Candidate-
`b8528027`-Checks bestanden, beide mit NGINX `release-1.31.6`. Der unveränderliche
Common-Helferblob entspricht exakt Framework-`b8528027:ci/lib/common.sh`.
Kombinierte finale Pin-Pythonvalidierung bestand alle 99 bestehenden Methoden
in 60.799 Sekunden (7 Projektion, 19 Revision, 29 Kandidat, 22 Compiler,
22 Apache), mit Parent `5b5a4a89` plus Aufgabenänderungen und Framework
`b8528027`. Absichtliche negative SHA-Diagnosen in Unittest-Ausgabe sind kein
nativer Kandidatenfehler. Native NGINX-Adoption und Common-C17-Helferchecks
bestanden mit `-std=c17 -Wall -Wextra -Werror`. Öffentliche Inventarzulassung
bestand mit SHA-256
`147ebacc795c634bd9d4b21cfbcd408e635dd55de8b757be2671d3b056ac1cb8`,
100 Standard- / 2686 Gesamt- / 2586 optionalen Fällen und wahrheitsgemäß
schmutzigem Parent-Worktree; Zulassung ist keine Testausführung. Gestagte/
ungestagte Whitespace-Checks bestanden. Finaler Guide-Byte-Diff bestätigt alle
18 Ausgaben unverändert; native Parent-Zweisprachigkeits-, Repositorypfad- und
Dokumentationslinkprüfungen bestanden. Commit/Push und neue Head-CI/Sonar stehen
bei diesem Vorbereitungssnapshot aus.

Framework-`b8528027`-Master-Workflows CodeQL/Common/Scorecard bestanden;
Lint/Sonar laufen. Genau fünf Master-Workflows wurden ausgelöst. Security-Python-
und Fünf-Connector-Vertragsworkflows sind nicht anwendbar: Keiner der elf
geänderten Pfade passt zu ihren eingecheckten Push-Filtern. Sie zählen nicht
als bestanden, übersprungen oder fehlend.
MRTS bleibt uninitialisiert/schreibgeschützt; strikte lokale Prüfung tatsächlicher
Materialisierung ist daher nicht verfügbar. Immutable-Chain-/native Pinchecks
sind getrennt von frischer gehosteter Actual-Checkout-Evidence. Parent #348
bleibt ein ungemergter Draft auf veröffentlichtem `db431efa`; lokaler
`5b5a4a89` plus finale Pinänderungen ist unveröffentlicht. Kein Parent-Master-
Merge ist freigegeben.

Native Generierung erhält 100 Standardfälle / 80 Ausführungen und 1993
Basis-IDs; der optionale Katalog enthält 2586 Fälle / 1140 Ausführungen. Die
frühere Framework-Stufe hatte 526 Bindungen, nach #147 ersetzt durch 528.
Deren fokussierte Framework-Prüfungen bestanden mit 12
Python-Methoden, 43 Protokollmethoden, vier QUIC-Helfermethoden, 348
Dokumentationspaaren und kanonischen Checks. Die Traefik-Paritätsauswahl nach
#146 bestand mit Race-Detector: 16 Tests / 18 Abschlüsse. Der frühere volle
Traefik-Lauf (173 erfolgreiche Abschlüsse, ein Echtdienst-Skip) liegt vor #146
und qualifiziert dessen neue Leaves nicht. Vor der späteren `2abad408`-Master-
Integration waren alle 31 informativen Leaves kompiliert, aber NOT_RUN, weil
dem gewählten Parent `b43faa78` der separate Produktfix fehlte und #435 damals
ungemergt geschlossen war. Diese historische Grenze ist durch die begrenzte
Merge-Interaktions-Unit-Evidence oben überholt, nicht durch eine vollständige
Host-/TLS-/H2-/H3-Laufzeitqualifikation.

Die datierten Snapshots unten bewahren ihre ursprüngliche Evidence und
Inventarzahlen; sie beschreiben nicht die aktuelle Testverantwortung, das
aktuelle Inventar oder den Submodulzustand. Die Protokollmatrix bleibt ein
unqualifizierter historischer Snapshot. Dieses Migrations- und
Integritäts-Increment belegt weder eine neue TLS-/H2-/H3-Qualifikationskampagne
noch neue Host-Runtime-Ergebnisse. MRTS bleibt außerhalb des Änderungsumfangs.

## Historische Aktualisierung am 2026-10-30: anschließender Master-Pin-Abgleich

Der geprüfte Parent-Head `096170f7ab0ba19537546ce861f818fbab6e1772`
bestand 59 Hosted-Prüfungen bei fünf vorgesehenen Skips. Master rückte danach
durch Submodul-Update #433 auf
`ee1345f17c5390fd2341751e88fc510c7e7b580c` vor. Dieser Nachtrag integriert
die Revision normal und erzeugt den einzigen Archivkonflikt neu. Framework-Pin
und Projekt-Lock stimmen jetzt auf
`d3b47aec9410f7adc3bb40df1ea413c00c438e89` überein; diese Revision enthält
die zuvor fehlenden Paket-/Ergebnis-APIs. MRTS bleibt unverändert gepinnt.
API-Verfügbarkeit belegt keine neue Host- oder Protokoll-Runtime-Qualifikation.

Keine neuen Tests oder Selektoren werden geschrieben. Die aktive Fallauswahl
bleibt 100; das Inventar übernimmt nur die Formatierung von Requirement-Strings
und den aktualisierten Lock-Digest. Vorhandene Upstream-Framework-Tests werden
mit dessen Pin übernommen, nicht hier neu angelegt. Connector-Produktcode und
Issue-#401-Integration bleiben unverändert. Separater Framework-Draft
[PR #143](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/143)
verschärft die Integrität der Transferabschlüsse in Protokollartefakten; sein
Commit `78b103f8` ist nicht im Parent-Pin enthalten. CI/Sonar des aktuellen Heads
wird nach Veröffentlichung separat geprüft. Der vollständige H1-/H2-/H3-
Workstream bleibt offen.

## Historische Aktualisierung am 2026-10-30: Integrität der Integration

Der gesicherte Kandidat `1dca1c8eabd17d71a3327ccf3f828c3c5cb8fa01`
hat alle 59 ausgeführten Hosted-Prüfungen einschließlich Sonar bestanden;
fünf Prüfungen wurden übersprungen. Dieses Increment integriert aktuellen
Master `ec18f9e92286379a2410e917f76e6a5502675804` durch einen normalen
Merge. Sein einziger Konflikt liegt im generierten Spezialistenarchiv, das aus
den Quellen beider Branches neu erzeugt wird. Die aktuelle Master-Auswahl und
der Apache-Harness-Digest bleiben neben den neun Source-Digest-Aktualisierungen
des PR erhalten. Alle Source-Digests stimmen; aktive Auswahl und Selektoren
ändern sich nicht. Das Archiv enthält 6228 On-demand-Definitionen, getrennt
von den unveränderten 100 aktiven Fällen.

In diesem Increment werden keine neuen Tests angelegt. Masters vorhandene
Tests zur privaten Paketübergabe werden unverändert übernommen. Connector-
Produktquellcode und Issue-#401-Mapping bleiben ebenso erhalten wie Masters
Paket-/Ergebnis-Integritätsprüfungen. Die dokumentierte Abhängigkeit von einer
späteren Framework-Paket-API bleibt eine Einschränkung; dieser Merge ändert
weder Framework-/MRTS-Quellcode noch einen ihrer Gitlinks. CI-/Sonar-Verifikation
für den neuen Head steht bei Vorbereitung noch aus. Die früheren Prüfungen
beweisen weder den neuen Merge noch vollständige H1-/H2-/H3-Laufzeitqualifikation.

## Historische Aktualisierung am 2026-10-28: aktueller Master und CI-Reparatur

Dieses Increment übernimmt `master`-Revision
`c5993ed9a7b59fc0bd58f105595ec79f596c88d6` durch einen normalen Merge
mit erhaltener veröffentlichter PR-Historie. Apaches ausgehandeltes P3-Protokoll
verwendet jetzt die Native-Phase-Erfolgsprüfung aus Master. NGINX erhält die
typisierten Mapper-Fehler und zählt den synthetischen HTTP/3-Host gegen
dasselbe Limit für empfangene Header. Traefik verbindet Incomplete-Response- und
EOS-Behandlung mit Masters geprüftem Close, terminalem Fehlerzustand und
`http.ErrAbortHandler`-Verhalten.

Die fünf fehlgeschlagenen Struktur-/Lint-Jobs auf `ab3d4d27` teilten eine
veraltete Apache-Checker-Erwartung. Der Checker verlangt jetzt ausgehandeltes
Protokoll und Native-Erfolgsprüfung; negative Mutationen prüfen Umgehungen.
NGINX-Checker und Mutationen erzwingen ebenfalls das gemeinsame Limit für rohe
und synthetische Header. Sonar-Issue `AaF3fXFNfuQxuJn35iQJ` (`c:S859`) wird
durch ein lokales veränderbares Host-Namensarray statt des Casts behoben, der
`const` entfernt.

Frische lokale Validierung bestand: beide Adoption-Checker, 21 ausgewählte
Python-Szenarien und 44 ausgewählte Traefik-Fälle mit Race-Detector. Eine
veraltete Source-Assertion schlug zunächst fehl und bestand nach Abgleich mit
der zusammengeführten Limit-Prüfung. Die Auswahl der 100 aktiven Testfälle ist
bis auf Source-Digests unverändert; Admission-Prüfung und Konsistenzprüfung des
neu generierten Archivs bestanden. Die Python-Prüfungen verwendeten das
vorhandene lokale Python 3.14.4; Hosted-CI verwendet den Interpreter-Vertrag
des Repositorys. Unabhängiges Quellreview fand kein neues validiertes
Sicherheitsproblem. Hosted-CI und Sonar für den aktuellen Head stehen an dieser
Revision noch aus. Die frühere Testzurückstellung ist für CI-Reparaturen
aufgehoben; vollständige H1-/H2-/H3-Laufzeitqualifikation bleibt unvollständig.

Auf dem ersten veröffentlichten Kandidaten `2a6089c3` bestehen der erforderliche
C++17-Sonar-Job und alle fünf zuvor fehlgeschlagenen Struktur-/Lint-Jobs; der
Const-Cast-Befund fehlt. Zwei neue `python:S1192`-Checker-Literale sind jetzt
gemeinsame Konstanten; dieselben acht positiven/negativen Apache-Szenarien
bestehen erneut. Die unverbindliche C++20-Analyse meldet eine lighttpd-
Null-Dereferenz, obwohl ihre eigene Quellansicht den expliziten Null-Return
enthält; unabhängiges Review findet keinen erreichbaren Nullpfad. Die
redundanten Fehler-Guards werden ohne Verhaltensänderung zu einer NULL-first-
Kurzschlussprüfung verbunden. Beide bestehenden nativen Null-/Normalabschluss-
Fälle bestehen. Dies ergänzt zwei Szenarien (insgesamt 67 mit der früheren
Auswahl) und eine Source-Digest-Erneuerung; die Auswahl von 100 Fällen bleibt
unverändert. Nach Framework-Setup bestehen auch Bilingual-/Pfad-/Link-Prüfungen.
Hosted-Validierung dieses Follow-ups steht noch aus; kein Sonar-Serverzustand,
keine Regel und kein Gate werden geändert.

## Historische Aktualisierung am 2026-10-24: Master-Abgleich und NGINX-Issue #401

PR #348 übernimmt `master`-Revision
`42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3` durch einen normalen Merge.
Envoy erhält die aktuelle Pflichtvalidierung für Host/Authority zusammen mit
den strengeren Pseudo-Header- und modernen Protokollprüfungen dieses
Workstreams. Traefik erhält das aktuelle begrenzte Leeren des Request-Bodys
und Connection-Cleanup zusammen mit den Incomplete-Response-/EOS-Kontrollen.
Testdefinitionen und Change-Record-Einträge beider Branches bleiben nach der
Konfliktauflösung erhalten.

Für [ModSecurity-nginx-Issue #401](https://github.com/owasp-modsecurity/ModSecurity-nginx/issues/401)
ergänzt der NGINX-Adapter genau einen Inspection-only-`Host` aus einer
empfangenen HTTP/3-`:authority`, wenn kein Host-Eintrag unabhängig von seiner
Groß-/Kleinschreibung existiert. Mapper, Request-Hostname, native P1-Header-
Übergabe und Header-Anzahl-/Byte-Erfassung verwenden dieselbe Authority-
Auswahl. Ein expliziter Host, auch ein leerer, unterdrückt diesen Fallback.
Der Adapter verändert weder die NGINX-Headerliste noch leitet er einen Host
aus der Konfiguration ab. Er erhält Port und geklammerte IPv6-Form der
ursprünglichen Authority wie der Raw-Authority-Host-Shim von NGINX für HTTP/2.
Native H3-Versionsmetadaten sind ausdrücklich `3.0`.

Diese Aktualisierung ist im Quellcode geprüft, aber
`implemented_not_runtime_verified`. Funktionstests, Builds, Protokollverkehr
und CI-Grünstatus sind auf Benutzerwunsch zurückgestellt. Alle folgenden
Ergebnisse und Umgebungsproben sind historische Evidenz von 2026-08 und keine
frische Validierung der zusammengeführten Revision. Der gesamte Workstream
und die H1-/H2-/H3-Laufzeitmatrix bleiben unvollständig.

## Evidence-Grenze

Das neutrale Common-Modell stellt die Protokollzustände `unknown`, H1, H2 und
H3, Stream-Identität, Commit- und EOS-Zustand sowie die Auswahl eines
Stream-Resets dar. H2-Stream-ID 0 und ein frei gesetztes `STREAM_RESET` werden
konservativ nicht als Stream-Reset ausgegeben. Dieses Modell beweist nicht,
dass jeder Adapter es verwendet.

Im ursprünglichen Umgebungssnapshot von 2026-08 war das Framework-Submodul
nicht initialisiert und wurde nicht geändert. MRTS wurde nicht angefasst.
Das damalige curl hatte HTTP/2, aber kein HTTP/3; `curl --http3` beendete sich
mit `2`. Daher lautet der H3-Runtime-Status
`runtime_skipped_missing_client`; H3-Runtime ist nicht verifiziert.

## Connector-Statusmatrix

Die Statuswerte sind unabhängig. `not_run` bedeutet, dass für diese Dimension
keine Evidence geliefert wurde; `blocked` bezeichnet eine beobachtete
Voraussetzungsbeschränkung. `source-level fixed` und
`implemented_not_runtime_verified` beschreiben nur Source-Evidence und sind
keine Runtime-Pässe.

| Connector | H1 baseline | H2 code | H2 runtime | H3 code/capability | H3 runtime | P1 | P2 | P3 | P4 | Late intervention | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | contract_verified (source only) | configured_not_exercised | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | contract_verified (source only; protocol from `ap_get_protocol(r->connection)` plus canonical HTTP/1 `r->proto_num`; unknown fails closed) | not_run | not_run | source-level fixed / runtime not verified |
| NGINX | contract_verified (historical source only) | implemented_not_asserted | not_run | implemented_not_runtime_verified (authority-to-Host mapping) | runtime_not_verified (deferred) | implemented_not_runtime_verified | not_run | not_run | not_run | not_run | source-level fixed / runtime not verified |
| HAProxy | not_run | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |
| Envoy | not_run | configured_not_exercised | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | source-level configured / runtime not verified |
| Traefik | contract_verified (source only) | not_implemented | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | contract_verified (source only) | source-level fixed / runtime not verified |
| lighttpd | not_run | unsupported_by_host_model | not_run | not_implemented | runtime_skipped_missing_client / runtime_not_verified | not_run | not_run | not_run | not_run | not_run | not_implemented |

Die Apache-P3-Änderung leitet das Protokoll jetzt aus
`ap_get_protocol(r->connection)` plus kanonischem HTTP/1-`r->proto_num` ab und
schlägt bei unbekanntem Protokoll fail closed fehl. NGINX erzeugt für H2-Streams
kein `Transfer-Encoding` mehr und besitzt einen geschützten H3-Pfad. Traefik
markiert einen initialen nicht-EOF-`ReadFrom`-Source-Fehler (mit oder ohne Bytes) als
unvollständig und verhindert, dass ein Response-Body-Engine-Fehler nach Commit
ein synthetisches EOS auslöst. Die ursprüngliche direkte Post-Commit-
Engine-Error-Reproduktion und die neue Initial-ReadFrom-Source-Error-
Reproduktion schlugen vor der Reparatur fehl; die fokussierte Post-Patch-Go-
Auswahl bestand. Es wird keine H2/H3-Traffic-Behauptung aufgestellt und die
tatsächliche Traefik-H2/H3-Runtime wurde nicht ausgeführt. Sein
`responseIncomplete`-Zustand unterdrückt falsches EOS und normales FINISH bei
Host-, Engine-, Commit- und Source-Fehlern. `finish()` markiert einen nach
Commit fehlgeschlagenen EOS-Callback als `responseIncomplete`; fehlgeschriebene
oder nicht bestätigte Pre-Commit-Deny-/Fehlerantworten werden ebenfalls als
unvollständig markiert. Ein initiales `(0,nil)` ReaderFrom delegiert nicht vor
Pre-Commit-Kontrollen. Es wird kein falsches EOS- oder normales FINISH-Verhalten
behauptet. Ein Pre-Commit-EOS-Enginefehler markiert den Abschluss trotz eines
sichtbaren Fallbacks als unvollständig. Fehlende Applied- oder Late-Log-Only-
Acknowledgements markieren den Abschluss ebenfalls als unvollständig, sodass
kein normales FINISH behauptet wird. Bei Late-Log-Only-Ack-Fehlern erzeugt auch
der delegierte ReaderFrom-EOF-Pfad kein synthetisches EOS.

Envoy besitzt jetzt getrennt materialisierte Downstream-Profile `http1` und
`h2`: `http1` wählt ausschließlich ALPN `http/1.1` und den HTTP/1-HCM-Codec,
während `h2` ALPN `h2`, den HTTP/2-HCM-Codec und
`http2_protocol_options` wählt. Der Materializer weist jeden anderen Wert
zurück, statt zurückzufallen. Sein vorhandener Python-Runtime-Helper bleibt
ausdrücklich HTTP/1.1-only. Fokussierte Go-Contract-Tests für den
`ext_proc`-Request-Header-Adapterpfad bewahren einen von Envoy gelieferten
Metadatenwert `HTTP/2` und weisen doppelte, großgeschriebene oder nicht
unterstützte Request-Pseudo-Header, CR/LF/NUL-Headerwerte,
Connection-spezifische Header für moderne Protokolle und ungültige `TE`-Werte
zurück, wenn das gelieferte Protokoll HTTP/2 oder HTTP/3 ist. Dies sind ausschließlich Source-/Konfigurations- und
Adaptergrenzprüfungen: Es wurde weder ein Envoy-Binary-/Config-Load noch
Client-ausgehandelter H2-Traffic ausgeführt.

Die Matrix bewahrt die getrennten Angaben aus
`connectors/*/capabilities.json`: Apache H2 ist
`configured_not_exercised` und sein H3-Host-Pfad ist `not_implemented`; NGINX
H2 und H3 sind `implemented_not_asserted`; HAProxy und Traefik sind für die
ausgewählten nativen Modern-Protocol-Profile `not_implemented`; Envoy
Downstream-H2 und TLS/ALPN sind `configured_not_exercised`; lighttpd H2 ist
`unsupported_by_host_model` und H3 ist `not_implemented`.

Kein Security-Finding ist vollständig verifiziert. Die zutreffende
Klassifizierung für die obigen Änderungen ist source-level fixed / runtime not
verified.

## Neutrales Lifecycle-Contract

Der Common-Contract hält Protokoll- und Lifecycle-Entscheidungen von
Connector-spezifischen Host-Typen getrennt. Er umfasst:

- die Protokollauswahl `unknown`, H1, H2 und H3;
- Stream-Identität und Transaktionskorrelation;
- Commit-Zustand und terminale EOS-Behandlung;
- Stream-Reset-Auswahl für ein Multiplexing-Protokoll; sowie
- Safe- und Strict-Entscheidungen für späte Interventionen.

Adapter müssen weiterhin nachweisen, dass sie dieses Modell abbilden und
durchsetzen. Die Matrix erhebt daher Common-Modell-Abdeckung nicht zu
Connector-Runtime-Abdeckung.

## Historische Regressions- und Capability-Evidence

- 28 ausgewählte Python-Tests bestanden (Apache/NGINX/C/C++-Gruppe).
- Der kombinierte Python-Befehl jener Revision bestand mit 98 Tests und 1 erwarteten
  Framework-Identity-Skip.
- Frühere Baselines waren 20 passed/3 skipped und 39 passed/2 skipped.
- Capability-Gruppe 93 hatte einen erwarteten Environment-Fehler, weil der
  Framework-Validator fehlte, während das Framework-Submodul nicht initialisiert
  war.
- Common C17 bestand.
- Common C17 helper bestand.
- Common SDK/adapter/security checks bestanden.
- Apache C17 bestand.
- Apache statischer Test bestand.
- Traefik-Pakettest bestand.
- Vier fokussierte Go-Regressionen schlugen absichtlich vor dem Fix fehl und
  bestanden danach.
- Drei test-first Go-Regressionen schlugen absichtlich vor dem Fix fehl und
  bestanden danach.
- Ein neuer test-first ReaderFrom-Regressionsfall schlug vor dem Guard fehl und
  besteht danach.
- Für die Matrix wurde kein H2-Runtime-Traffic geliefert.
- H3-Runtime ist `runtime_skipped_missing_client` und nicht verifiziert.

Während des Workstreams wurde eine versehentliche anfängliche Ausgabe in einem
gemeinsamen Build-Verzeichnis beobachtet. Dies ist nur eine lokale
Storage-Beschränkung; es ist keine Protokoll- oder Runtime-Evidence und stützt
keine weitergehende Behauptung.

## Historischer initialer Delivery-Status

Commit `5e7b34d1887984f74d061872d7652a3f71d87856` ist als
`feature/http2-http3-protocol-parity` gepusht und durch Draft-PR
[#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348)
vertreten. Bei der initialen Delivery-Verifikation stimmten lokaler, Remote- und
PR-Head-SHA überein. CI-Prüfungen waren in Warteschlange oder in Ausführung und
werden nicht als bestanden behauptet. Bei dieser initialen Delivery hatte kein
Merge stattgefunden. Framework-Submodul und MRTS waren zu diesem Zeitpunkt
unverändert. Die Aktualisierung vom 2026-11-01 beschreibt den aktuellen
Integrationsumfang und die noch ausstehende Delivery-Evidence.
