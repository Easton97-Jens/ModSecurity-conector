# CR-20260820 — Geschlossener no-CRS/with-MRTS-Runtimepfad

**Sprache:** [English](CR-20260820-no-crs-with-mrts-runtime.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260820-no-crs-with-mrts-runtime |
| Datum (UTC) | 2026-08-20 |
| Basis-Revision | `7c403fada21de4547259fef1dc4a1b079cb0cb25` |
| Parent-Grenze | Nur Parent; aktuelle Framework- und MRTS-Gitlinks read-only verwendet |
| Framework-Gitlink | `c40e924ec5c341032908e0082feba1d37ed1dfda` |
| MRTS-Gitlink | `615b13bacbd008562c17408246c41ab27dca3104` |
| Lieferstatus | Der Task-Branch ist auf den beobachteten aktuellen Master rebased; Draft-Delivery darf ohne Behauptung von Host-Runtime-, Hosted-Check- oder Sonar-Erfolg erfolgen; kein Merge, Auto-Merge oder Default-Branch-Write ist autorisiert |

## Motivation und Problemstellung

Der aktuelle `master` benötigt einen geschlossenen, modusspezifischen Pfad für
echte `no-crs/with-mrts`-Ausführung durch Envoy, Traefik und lighttpd. Der alte
Stand von PR #279 wird nicht als Implementierungsbasis verwendet. Die drei
`with-crs/with-mrts`-Ziele müssen weiterhin unsupported bleiben; fremdes
Connector-Verhalten darf nicht erweitert werden.

## Akzeptanzkriterien

- Nur Envoy, Traefik und lighttpd werden zum neuen Target-Pfad zugelassen.
- Die exakte Parent-/Framework-/MRTS-Gitlink-Kette wird aufgezeichnet und geprüft.
- Das vom Framework erzeugte MRTS-Inventar und die Load-Datei werden von einem
  echten Host-Executor mit Kontroll-, Detection- und gutartigem Bypass-Case
  verwendet.
- Laufzeitergebnisse korrelieren Request, Transaktion, Case und beobachtete
  Events; Resultate werden begrenzt und atomar im privaten Run-Root geschrieben.
- CRS-Pfade und CRS-Includes werden zurückgewiesen; OWASP CRS wird in diesem
  Profil nicht beschafft, geladen, gecacht oder wiederverwendet.
- Echte Host-, Cleanup-, Exact-Head-CI-, Required-Check- und Sonar-Evidence
  wird nur bei tatsächlicher Beobachtung aufgezeichnet.
- `with-crs/with-mrts` für die drei Ziele und NGINX bleiben unverändert.
- Keine Framework- oder MRTS-Quelländerung ist erforderlich.

## 2026-08-23 Branch-Abgleich und Job-Isolation

Der Task-Branch wurde normal auf das frisch abgerufene
`origin/master` `7c403fada21de4547259fef1dc4a1b079cb0cb25` rebased; er basiert
weder auf PR #279 noch wird er über diesen PR ausgeliefert. Der Parent zeichnet
Framework `c40e924ec5c341032908e0082feba1d37ed1dfda` auf, dessen veröffentlichter
MRTS-Gitlink `615b13bacbd008562c17408246c41ab27dca3104` ist. Der lokale
verschachtelte Framework-Checkout wird nicht verwendet, um diesen Gitlink
umzuschreiben.

Der no-CRS/with-MRTS-Workflow leitet Vorbereitung und Ausführung jetzt aus
einem geschlossenen Connector-Zweig pro Job ab. Apache erhält nur die
Apache-Komponente und seinen Runtimepfad; HAProxy erhält nur die
HAProxy-Komponente und seinen Runtimepfad; Envoy, Traefik und lighttpd
verwenden jeweils ihren eigenen literalen versiegelten Target-Aufruf. NGINX
ist nicht enthalten. Kein von der Matrix bereitgestelltes Komponenten-Target
oder Kommando erreicht `make`, eine Shell, einen Pfad oder einen Runner.

Alle joblokalen Pfade werden aus denselben expliziten Runner-, Run-, Attempt-
und Connector-Koordinaten statt aus einer gleichrangigen Workflow-
Umgebungsvariable expandiert. Der Traefik-MRTS-Host bindet seine native
Middleware an `X-MRTS-Transaction-ID`; der normale Hostpfad behält
`X-Request-Id`.

Jeder Job schreibt nach dem Evidence-Upload eine sichere GitHub Step Summary
mit festen Stage-Outcomes, Zählungen, der ersten nicht bestandenen Stufe und
einem `PASS`/`FAIL`/`MISSING`/`CANCELLED`-Runtime-Bundle-Status. Sie liest keine
rohe Evidence und befördert eine fehlende, übersprungene oder fehlgeschlagene
Runtime nicht zum Erfolg.

Die Korrektur verwendet nun für beide Connector-Workflowprofile einen
gemeinsamen sicheren Step-Summary-Helper. Dadurch gibt es keine doppelten
Summary-Implementierungen und die Pfadvalidierung bleibt identisch. Der
Target-Runner verwendet den vor dem Dispatch angelegten privaten Build-Root
sicher wieder, statt ihn aus einem Umgebungs-Fallback neu zu bestimmen. Traefik
legt sein kurzes AF_UNIX-Socket-Verzeichnis mit `tempfile.mkdtemp` sicher an;
nur der Traefik-Aufruf erhält `TMPDIR=/tmp`, während der private Run-Root für
Pläne, Logs, Ergebnisse und aufbewahrte Evidence maßgeblich bleibt. Envoys
MRTS-HTTPS prüft das versiegelte, run-lokale Zertifikat an der Peer-Grenze;
eine unsichere TLS-Option oder Umgehung der Zertifikatsprüfung ist nicht
vorhanden.

Repository und gehosteter Workflow behalten `.go-version` `1.26.7`. Die lokale
Binary ist `go1.26.6`; auf Grundlage der aktuellen Benutzeranweisung ist diese
Differenz eine dokumentierte lokale Validierungseinschränkung, kein Download,
Upgrade, Vertragswechsel oder Exact-Hosted-Nachweis.

## Implementierungsentscheidung und Begründung

Parent besitzt Hostadapter und geschlossene Dispatch-Grenze. Das neue
`ci/runtime/lifecycle/run-no-crs-with-mrts-target.py` materialisiert die
exakte Framework-MRTS-Runtime, wählt portable Phase-1-GET-ARGS-Cases aus,
ergänzt explizite Kontroll- und Bypass-Cases und ruft den bestehenden echten
Hostpfad auf. `execute-no-crs-mrts-cases.py` sendet Live-Requests und prüft
DetectionOnly-HTTP-200 sowie Event-Korrelation, bevor ein frischer Receipt
geschrieben wird. Die Hostadapter bleiben Envoy ext-proc, Traefik native
Middleware und der gepatchte native lighttpd-Pfad.

Der Pfad ist über `MSCONNECTOR_MRTS_RUNTIME=1` opt-in und verwendet private,
symlinkgeprüfte Runtimepfade. Er weist Plan-/Result-Wiederverwendung,
JSON-Duplikatschlüssel, Traversal, CRS-Referenzen und Connectornamen außerhalb
der geschlossenen Menge zurück. Der Plan wird durch den SHA-256-Digest seiner
exakten Bytes versiegelt; dieser Digest ist an jeder Hostadapter- und
Executor-Grenze erforderlich. Aus dem exakten Framework-Checkout rekonstruierte
Case-Hashes und der ausgewählte Inventar-Hash müssen mit dem versiegelten Plan
übereinstimmen. Rule-Match-Evidence verwendet einen typisierten nativen
`RuleMessage`-Observer, standardmäßig deaktiviert und nur für das versiegelte
MRTS-Profil aktiviert; er erzeugt begrenzte Metadaten-JSONL und prüft native
Integrität sowie zusammenhängende Verkettung. Der Parent-Go-
Versionsvertragschecker entspricht dem aktuellen CodeQL-`awk`-Guard und
bewahrt die exakte stabile `1.26.x`-Grammatik. Die lokale Go-Validierung
verwendete `/usr/local/go/bin/go` `go1.26.6` mit `GOTOOLCHAIN=local`.

Das Lifecycle-Follow-up erzeugt `NO_CRS_RUN_ID` im geschlossenen Target-Runner
als `mrts-<32 lowercase hexadecimal characters>`. Es weist einen ambient
gesetzten Wert zurück, reicht den erzeugten Wert durch die `env -i`-Grenze und
setzt den readonly-Snapshot-Wert vor dem Start jedes nativen Hosts erneut. Der
Workflow setzt daher keine von GitHub bereitgestellte Identität vor. Das stellt
Traefik und lighttpd dieselbe begrenzte Lifecycle-Identität bereit, ohne einen
vom Aufrufer kontrollierten Wert zu akzeptieren.

Traefiks native Engine benötigt einen kurzen AF_UNIX-Socket-Parent, während
der versiegelte Runtime-Root das Socket-Pfadlängenlimit der Plattform
überschreiten kann. Nur für diesen Host reserviert der Target-Runner ein
eindeutiges `/var/tmp/msct-*`-Child, prüft jede Pfadkomponente auf Symlinks,
erzwingt den exakten Owner-Modus `0700` und begrenzt den vollständigen nativen
Socket-Kandidaten auf 100 Byte. Der native Host muss zuerst sein eigenes Child
entfernen; Parent entfernt nur den anschließend leeren exakten Parent und
schlägt bei jedem unerwarteten Artefakt fail-closed fehl. Pläne, Logs,
Ergebnisse und aufbewahrte Evidence bleiben unterhalb des privaten Run-Roots.
Die versiegelte MRTS-`env -i`-Grenze reicht nur diesen berechneten Parent für
Traefik weiter; ein fehlender Wert lässt den nativen Runner weiterhin
fail-closed fehlschlagen.

Zu den aktuellen Implementierungscommits gehören das versiegelte
Run-Identity-/Socket-Parent-Follow-up (`602d88e3`) und seine geschlossene
Traefik-`env -i`-Weitergabekorrektur (`14f453d7`). Keiner der Commits ändert
den Framework- oder MRTS-Gitlink.

Der erste frische Traefik-`r2`-Targetlauf stoppte anschließend fail-closed vor
der Host-Erzeugung: Seine Hilfsprüfung des Loadfiles verwendete einen breiten
textuellen CRS-Treffer und bewertete `mrts-no-crs-*` im legitimen privaten Root
als CRS-Material. Das erzeugte Loadfile enthielt selbst nur die 15 gepinnten
`MRTS_*.conf`-Includes; der zentrale versiegelte Validator verlangt weiterhin
kanonische Include-Syntax, das private generierte Regelverzeichnis, die
vollständige kanonische Include-Menge und bytegenaue Hashes. Der enge lokale
Guard erkennt jetzt nur echte CRS-Pfadkomponenten; fokussierte Controls weisen
`crs`- und `owasp-crs`-Komponenten ab und akzeptieren einen `no-crs`-Parent.
`FND-PARENT-0201` bewahrt die Diagnose und hält die Release-Hochstufung bis zu
zwei frischen Traefik-Receipts auf dem exakten Head blockiert.

Der frische Traefik-`r3` auf Parent `27b7e5a5` bestand diesen Guard, baute die
gepinnte Traefik-Runtime und erreichte den echten nativen Host. Sein erster
legitimer MRTS-GET-Kontrollfall erhielt danach HTTP 501 vom lokalen
Upstream-Fixture: Der versiegelte Executor sendet absichtlich GET-Cases, das
Fixture implementierte aber nur `do_POST`. Dies ist eine task-eigene
Fixture-Capability-Lücke, keine CRS-, Regel- oder Host-Middleware-Evidence.
Es wurde kein MRTS-Receipt geschrieben; das Host-Cleanup schloss dennoch ab.
Das Fixture führt body-freie GET- und bestehende POST-Requests jetzt durch
denselben begrenzten Response-Pfad und weist GET-Body-Framing ab;
ein direkter GET-Control-Contract verhindert eine Wiederholung des 501. Vor
einer Hochstufung bleiben zwei frische Receipts auf dem neuen Candidate-Head
erforderlich.

## Security-Auswirkung

Die relevanten Grenzen sind nicht vertrauenswürdige Connector-/Case-Auswahl,
generierte MRTS-Konfiguration, Subprozess- und Host-Lifecycle, HTTP-
Request-Korrelation und private Evidence-Dateien. Traversal,
Symlink-Komponenten, nicht passende oder veränderliche Gitlinks,
CRS-Referenzen, alte Resultate, doppelte JSON-Schlüssel und unbekannte
Connectoren werden fail-closed validiert. Dieser Record dokumentiert außerdem
den diagnostizierten Parent-Interpreterauflösungsfehler `FND-PARENT-0194`: Der
letzte Symlink der genehmigten venv muss erhalten bleiben, symlinkte
übergeordnete Verzeichnisse müssen zurückgewiesen werden, und der Shell-
Dispatch muss denselben genehmigten Interpreter durch seine geschlossene
Grenze weiterreichen. Der Framework-Generator verwendet die explizite
`PYTHON`-Auswahl; dieser Record behauptet nicht, dass der Produktpfad den
aufrufenden `PATH` umschreibt. Die Behebung ist in der aktuellen Quelle und
den fokussierten Contracts enthalten; das Finding
bleibt jedoch bis zur frischen Runtime-Validierung release-blockierend. Dieser
Record behauptet keinen abgeschlossenen gehosteten Security-Scan; weitere
Security-Ergebnisse sind bis zum Implementierungs- und Validierungslauf offen.

## Geänderte Dateien

Die aktuelle Parent-Implementierung umfasst vorbehaltlich des finalen
Diff-Reviews:

- `ci/runtime/lifecycle/run-no-crs-with-mrts-target.py`
- `ci/runtime/lifecycle/execute-no-crs-mrts-cases.py`
- `ci/runtime/lifecycle/run-connector-stage.sh`
- `ci/runtime/lifecycle/run-remaining-connector-target.sh`
- `ci/checks/common/check-go-version-contract.py` sowie fokussierte Common-
  Security-, Adapter- und Remaining-Connector-Wiring-Checks
- `common/include/msconnector/config.h`
- `common/include/msconnector/event.h`
- `common/runtime/msconnector_runtime.c`
- `common/runtime/msconnector_rule_match_observer.cc`
- `common/runtime/msconnector_rule_match_observer.h`
- `common/src/config.c`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- Envoy-Build-/Konfigurations-/Harness-Skripte sowie ext-proc-Go-Quelle/-Tests
- `connectors/traefik/scripts/runtime_native_smoke.py`
- Traefik-Build-Skripte, MRTS-Input-Tests und
  `tests/test_traefik_transport_hardening_contract.py`
- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `connectors/lighttpd/harness/run_patched_lifecycle_smoke.sh`
- Lighttpd-Build-/Konfigurationspfade und Host-Contract-Tests
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- `ci/runtime/lifecycle/summarize-no-crs-with-mrts-workflow.py`
- fokussierte `tests/test_no_crs_with_mrts_*.py`, einschließlich
  Workflow-Isolations- und sicherer Summary-Contracts, Envoy-Transport- und
  Selected-Runner-Contracts
- `tests/test_go_version_contract.py`
- `docs/testing-and-evidence.md` und `docs/testing-and-evidence.de.md`
- dieser gepaarte Change Record und sein Archive-Index-Eintrag

Framework- und MRTS-Quelldateien werden nicht geändert.

## Ausgeführte Befehle

Bei der Erstellung dieses Records wurden folgende Repository-Inspektionsbefehle
ausgeführt: `rtk proxy find`, `rtk proxy sed`, `rtk proxy rg` und `rtk proxy git
status --short`. Die beobachtete lokale Validierung bestand: 97 fokussierte
Python-Contract-Tests, Shell-Syntaxprüfungen für geänderte Runner,
Python-Kompilierung, `check-common-security-contract.py`,
`check-adapter-contracts.py`, `check-remaining-connectors-build-wiring.py`,
`git diff --check`, der C17-Check für die übrigen Connectoren sowie C/C++-
Syntaxprüfungen. Die aktuelle Traefik-GET-Upstream-Korrektur bestand 106
fokussierte Selected-Runner-, versiegelte Target-, Dispatch-, Workflow-,
Traefik-Input-/Plugin- und Transport-Contract-Tests mit `TMPDIR=/var/tmp` und
deaktiviertem Bytecode-Schreiben. Envoy- und Traefik-Go-Checks verwendeten
`/usr/local/go/bin/go` `go1.26.6` mit `GOTOOLCHAIN=local`: `gofmt`,
`go mod verify`, `go list -deps ./...`, `go test ./...`, `go vet ./...` und
`govulncheck ./...` bestanden. Das Traefik-Modul wurde aus
`connectors/traefik/native_middleware` ausgeführt; sein erster längerer
temporärer Socket-Pfad wurde durch einen privaten kurzen Test-Root ersetzt.
Der Scanner behielt die ursprüngliche C/H-Baseline bei und ergänzte nur
`common/runtime/msconnector_rule_match_observer.cc`; vier vorbestehende
ShellCheck-SC1007-Warnungen verbleiben im Envoy-Konfigurationshelfer. Die
Dokumentationsvertragsprüfungen bestanden: `rtk proxy make
check-bilingual-docs` (`bilingual docs ok`), `rtk proxy make check-doc-links`
(`repository path references: PASS`; `doc links ok`) und `rtk proxy git
diff --check` (Exit 0).
Nach dem diagnostischen Envoy-`r10`-Header-Mismatch bestand das fokussierte
Envoy-/Lighttpd-Contract-Paar 50 Tests; `sh -n` bestand für
`connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` und
`connectors/lighttpd/harness/run_patched_lifecycle_smoke.sh`. Diese Checks
validieren nur die engen Source-Dispatch-Änderungen.
Die fokussierte Target-Runner-Suite für die r11-Phasenreihenfolgenkorrektur
bestand 28 Tests, und ihr Security-Review fand keinen konkreten Blocker. Dies
bleibt reine Source-Level-Validierung.
Das aktuelle Socket-Parent- und Run-Identity-Follow-up bestand Shell-Syntax,
ShellCheck, `git diff --check`, 107 fokussierte Python-Contracts und die
breitere Parent-Suite mit 160 Tests. Diese breitere Suite verwendete den kurzen
AF_UNIX-fähigen `TMPDIR=/var/tmp`: Ein zuvor langer privater temporärer Pfad
ließ den Testhelfer seinen eigenen Socket-Kandidaten zurückweisen, und der
unveränderte Envoy-Phase-4-Barrier-Test lief unter Suite-Last einmal ab. Beide
Tests bestanden danach isoliert und der vollständige Wiederholungslauf
bestand; dies wird als Umgebungs-/Testpfadgrenze dokumentiert, nicht als
Produkt-Erfolgsabkürzung. Ein fokussierter Security-Diff-Scan der sechs
Follow-up-Dateien meldete keinen konkreten Befund. Er bleibt Source-Level-
Review und ersetzt weder frische Host-Receipts noch Exact-Head-Hosted-Checks.
Die fokussierte Suite nach der Forwarding-Korrektur bestand 94 Tests,
einschließlich Selected-Runner-, versiegelter Target-, Dispatch-, Workflow-,
Traefik-MRTS-Input- und Traefik-Native-Plugin-Contracts. Die drei
Final-Candidate-Realhost-Wiederholungen, der gehostete Fünf-Connector-
Workflow, Exact-Head-Required-Checks und die SonarQube-Cloud-Analyse sind
aktuell `NOT EXECUTED`. Kein statisches Vertrags- oder Inventarergebnis wird
zu Runtime-`PASS` befördert.
Die enge Traefik-Load-Guard-Korrektur bestand 56 fokussierte Target- und
Traefik-Input-Contracts sowie `git diff --check`; sie wurde noch nicht in einem
Hostlauf verwendet. Ihr fokussiertes unabhängiges Security-Review fand keinen
konkreten Bypass; sie schwächt die zentrale versiegelte No-CRS-
Korpusvalidierung nicht ab.

Das Connector-Isolations-Update vom 2026-08-23 bestand 188 ausgewählte
Parent-Tests (vier erwartete Skips, weil das lokal ausgecheckte verschachtelte
Framework nicht dem vom Parent aufgezeichneten Gitlink entspricht), 125
fokussierte CI-Security-Tests (fünf erwartete Skips),
`check-common-security-contract`, `check-common-memory-safety`,
`check-common-flow-integrity`, `check-adapter-contracts`, checksum-verifiziertes
actionlint und offline ausgeführtes zizmor. Dies sind ausschließlich Source-,
Workflow- und Security-Contract-Ergebnisse. Es wurde keine lokale Go-Version
beschafft oder geändert: Das verfügbare `go1.26.6` ist als nicht äquivalent zum
vom Repository verlangten gehosteten Vertrag `1.26.7` dokumentiert.

## Runtime-Evidence

Ein aufbewahrter Envoy-Receipt vor dem Dokumentationsabgleich wird jetzt nur
als diagnostische Runtime-Evidence behauptet: `r15` auf Parent `14f453d7`
verwendete die exakt aufgezeichneten Framework- und MRTS-Gitlinks, bestand
realen Envoy-ext-proc-Start/Readiness, führte zehn Live-DetectionOnly-MRTS-
Cases mit HTTP 200 aus, erzeugte korrelierte native Rule-Match-Evidence und
meldete Cleanup bestanden. Er belegt den aktuellen Hostpfad, ist aber keine
Final-Candidate-Evidence, weil dieser Record erst danach abgeglichen wird.
Eine finale Beförderung erfordert weiterhin zwei frische, unabhängige Receipts
für jeden Zielconnector auf dem Candidate-Head.

Zwei spätere unabhängige Envoy-Receipts, `r16` und `r17`, schlossen auf Parent
`e7316caa` mit echtem ext-proc-Hoststart/Readiness, zehn HTTP-200-
DetectionOnly-Cases, korrelierter metadata-only Rule-Match-Evidence und
bestandenem Cleanup ab. Sie bleiben nur Verhaltens-Evidence, weil die aktuelle
Traefik-Guard-Korrektur diesem Head folgt; jeder Zielconnector muss aus
frischen Roots auf dem finalen Candidate-Head wiederholt werden.

Traefik `r2` ist nur Diagnose-Evidence: Der Lauf stoppte am Hilfs-Loadfile-
Guard vor der nativen Host-Erzeugung, Readiness, Request-Verarbeitung,
Case-Ausführung oder einem Runtime-Receipt. Sein Fehler ist kein Nachweis
eines CRS-Ladens und kann nicht als Runtime-Ergebnis verwendet werden.

Auch Traefik `r3` ist nur Diagnose-Evidence: Er bestand den korrigierten
No-CRS-Guard und startete den echten Host, aber sein erster MRTS-GET-
Kontrollfall erhielt HTTP 501 vom nur POST-fähigen lokalen Upstream, bevor
Case-Ergebnis, Event-Korrelation oder Receipt erzeugt werden konnten. Er
bestätigte sauberes Host-Teardown, darf aber nicht als Runtime-Ergebnis
verwendet werden.

Evidence muss im privaten Run-Root bleiben und Plan-/Result-/Event-Pfade,
exakte Parent-/Framework-/MRTS-Identitäten, Case- und Request-Korrelation,
No-CRS-Ergebnis, Evidence-Hashes und Cleanup-Status enthalten. Roh-Payloads,
Secrets, private Schlüssel und lokale absolute Pfade dürfen nicht in diesen
Record kopiert werden.

Das vollständige versiegelte `mrts.load` kann für einen ausgewählten Request
legitim mehr als einen nativen DetectionOnly-Treffer erzeugen. Der
Parent-Executor verwendet daher das kanonische Apache-/HAProxy-Subset-Orakel:
Jede vom Case deklarierte erwartete ID muss in der vollständig validierten,
exakt transaktions- und phasenkorrelierten Evidence vorhanden sein;
zusätzliche IDs derselben Phase bleiben nur bei Mitgliedschaft im erneut
validierten gepinnten Regel-ID-Inventar im Receipt. Sie ersetzen keine
erwartete ID, eine erwartete ID in einer anderen Phase schlägt fail-closed
fehl, und jeder korrelierte Treffer lässt weiterhin einen Kontroll- oder
Bypass-Case fehlschlagen.

Envoy `r10` wird nur als Diagnose-Evidence aufbewahrt: Der Lauf erreichte
echten Hoststart und Readiness, schlug aber mit HTTP 500 vor der MRTS-
Case-Ausführung fehl, weil der versiegelte Evidence-Modus
`x-mrts-transaction-id` verlangt, während der Readiness-Probe
`X-Request-Id` sendete. Es werden kein Case-Ergebnis, kein versiegelter
MRTS-Receipt und kein Runtime-Erfolg behauptet. Die aktuelle lokale Korrektur
wählt den geschlossenen MRTS-Readiness-Header nur im MRTS-Modus und erhält
`x-request-id` im Normalmodus. Unabhängig davon wählt der Lighttpd-MRTS-
Dispatcher nun den versiegelten Full-Lifecycle-Executor statt in den Legacy-
Kompatibilitäts-Smoke zu fallen. Beide Korrekturen benötigen weiterhin frische
Host-Validierung.

Commit `6e63fb52` zeichnet die Korrekturen für Readiness-Header und Lighttpd-
Dispatcher auf. Frisches Envoy `r11` erreichte echten Envoy-/ext-proc-Start und
den korrigierten Readiness-Pfad, stoppte aber vor MRTS-Case-Receipts: Gültige
unabhängige Readiness-Events wurden vor Transaktions-/URI-Korrelation auf ihre
Phase geprüft. Die gültige Transaktion `envoy-ext-proc-readiness-1` enthält
`request_body`, `response_headers` und `response_body`. Dies ist nur
diagnostische Realhost-Evidence, kein Runtime-Ergebnis. `FND-PARENT-0198`
verfolgt den Parent-Executor-Reihenfolgenfehler. Die enge Korrektur erhält
Duplicate-safe-Parsing, exaktes Schema, native Hash- und globale Chain-
Validierung für jede Event-Zeile; sie verwendet eine endliche native
Phasenzuordnung, ignoriert nur vollständig gültige unabhängige Transaktions-/
URI-Records nach der Validierung und behält eine relevante falsche Phase
fail-closed.

Frisches Envoy `r12c` erreichte danach den gepinnten Build, echten ext-proc-
Hoststart, Readiness und einen DetectionOnly-Request, scheiterte jedoch vor
jedem gültigen MRTS-Receipt. Die relevante Request-Transaktion enthielt die
ausgewählte Request-Body-Regel und gültige `response_headers`-/`response_body`-
Records derselben Transaktion. Diese nicht erwarteten Response-Phasen als
ungültig zu behandeln, ist ein zweiter Executor-Klassifikationsfehler. Sie
müssen integritätsvalidiert bleiben und danach außerhalb des ausgewählten
Request-Body-Akzeptanzprofils liegen. Eine erwartete Regel-ID in falscher Phase
sowie alle Kontroll-/Bypass-Erwartungen bleiben fail-closed. `r12c` ist nur
diagnostisch und kann die Zelle nicht befördern.

## Nicht ausgeführte Prüfungen mit Begründung

- Final-Candidate-Echt-Hostausführung für Envoy, Traefik und lighttpd:
  `NOT EXECUTED`; Envoy `r15` ist ein erfolgreicher Receipt vor dem
  Dokumentationsabgleich und ersetzt die geforderten frischen Wiederholungen
  nicht.
- Gehostete GitHub Actions und Exact-Head-Prüfungen: bei diesem Record-Update
  `NOT EXECUTED`; ein Draft-PR darf erstellt werden, aber ohne beobachtete
  Exact-Head-Evidence wird kein Erfolg abgeleitet.
- SonarQube-Cloud-Analyse und Quality Gate für diesen Task-Head:
  `NOT EXECUTED`; es wurde keine Exact-Head-Analyse eines Task-PR beobachtet.
- Framework-/MRTS-Quelltests: `NOT APPLICABLE`; dieses Parent-Task ändert keine
  Quelldatei dieser Repositories.

## Bekannte Einschränkungen

Der Task-Branch basiert auf aktuellem `master`, nicht auf PR #279. Die
Implementierung und ihre lokalen Verträge können sich nach den Hostläufen noch
ändern, wenn connector-spezifische Probleme sichtbar werden. Die lokale
Evidence enthält einen echten Envoy-Receipt, belegt aber nicht die
Drei-Connector-Final-Candidate-Hostmatrix. Die Dokumentation beschreibt den
vorgesehenen geschlossenen Pfad und die aktuelle Evidence-Grenze; sie begründet
nicht `verified_pr`.

## Verbleibende Risiken

Die finalen Hostadapter können Capability-, Readiness- oder Cleanup-Fehler
zeigen. `FND-PARENT-0194` ist durch lokale Interpreter-Contract-Tests allein
nicht geschlossen; frische Private-Root-Hostversuche müssen bestätigen, dass
die MRTS-Erzeugung die genehmigte venv verwendet und bei fehlender Dependency
kein falsches Runtime-Receipt erzeugt. Der finale Workflow kann Umgebungs- oder
Required-Check-Fehler zeigen.
Envoy `r15`, `r16` und `r17` belegen den aktuellen Hostpfad, gehen aber der
Traefik-Guard-Korrektur voraus und sind keine Final-Candidate-Evidence. Zwei
frische Final-Candidate-Receipts pro Zielconnector müssen MRTS-Cases,
No-CRS-Evidence und Cleanup belegen. Weder ein Legacy-Lighttpd-Smoke-Ergebnis
noch ein statischer Contract kann als Runtime-Evidence dienen.
Bis diese Exact-Head-Ergebnisse beobachtet wurden, bleiben die drei Zielzellen
für die Lieferung `PENDING`.

## Finaler Diff- und Review-Status

`PARTIAL — der Task-Branch ist auf den aktuellen Master rebased und ergänzt
enge Connector-Isolations- und GitHub-Summary-Verträge, während frische
Candidate-Head-Runtime-, Exact-Head-CI-, Required-Check- und Sonar-Evidence
offen bleibt.` Ein normaler Draft-PR darf erstellt werden; kein Merge,
Auto-Merge oder Default-Branch-Write ist autorisiert oder behauptet.
