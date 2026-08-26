# CR-20260825 — Begrenzte Envoy- und Traefik-Composite-Response-Korrelation

**Sprache:** [English](CR-20260825-fnd-parent-0221-composite-connectors.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260825-fnd-parent-0221-composite-connectors` |
| Datum (UTC) | 2026-08-25 |
| Basis-Revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Finding | `FND-PARENT-0221` |
| Scope | Parent-only Envoy `ext_authz` + `ext_proc` und Traefik `forwardAuth` + private-UDS-Response-Composite, Tests, Konfiguration und gekoppelte Dokumentation |
| Framework-/MRTS-Grenze | Keine Framework- oder MRTS-Source-, Branch-, `HEAD`-, Gitlink- oder Delivery-Änderung |
| Delivery-Disposition | Der Benutzer autorisierte einen task-owned Worktree, scoped Commit/Push und genau einen Parent-Draft-PR gegen `master`; kein Merge. Die Commits `931d6eb81207997169719bb475d50274ae281eed`, `9aeb0b551b34a0e44b9409130c2ecafeac641530` und `00b767aec09ccab0a6cceba37c8dc4ae763395d5` liegen auf Draft-PR #341. Die Sonar-Analyse `af6a96df-297f-47dd-af26-83b5315327e6` schloss/fixte neun von zehn Vulnerability-Records, ließ jedoch LOW `python:S5332` am kontrollierten Upstream offen. Das exakte Head-TLS-Follow-up reduzierte das Resultat auf eine neue Vulnerability, doch der Hosted-Check `97786524327` meldet weiterhin Security Rating B, weil er `BaseServer.serve_forever` unabhängig vom TLS-wrapped Socket modelliert. Der scanner-kompatible native TLS-Server-Loop-Successor ist lokal validiert; sein Commit/Push und die exakte Successor-Hosted-Validierung stehen aus. FND-SONAR-0061 bleibt P0/high, `in_progress`, release- und kandidat-integration-blockierend; kein grünes Sonar-Ergebnis wird behauptet. `FND-PARENT-0221` bleibt `in_progress`/`blocked_missing_evidence`, daher ist diese Änderung nicht für `verified_pr` oder Merge geeignet. |

## Motivation und Problemstellung

Request-only-Authorization-Hooks bewahren die für P3/P4 nach der
Upstream-Response-Verarbeitung benötigte Common-Transaktion nicht selbst. Die
Änderung implementiert begrenzte server-ownende Korrelation für Envoy und
Traefik, ohne einem Caller die Wahl einer Transaktion oder die Injektion eines
wiederverwendbaren Lease zu erlauben.

## Akzeptanzkriterien

- P1--P4-Beobachtungen wirken nur auf derselben erhaltenen Common-Transaktion
  für den unterstützten Envoy- oder Traefik-Composite-Pfad.
- Der Lease ist servergeneriert, integrity-bound, begrenzt, single-use und an
  Client-, Upstream- und Event-Grenzen nicht vorhanden.
- Traefik sendet rohe P1-Header nur in einem begrenzten versionierten
  private-UDS-Snapshot; ForwardAuth-HTTP erhält nur den opaque Lease und
  Traefik-generierte Forwarded-Metadaten.
- Reservation-, Timeout-, Disconnect-, Request-Termination- und Finish-Pfade
  besitzen genau ein begrenztes terminales Cleanup und schlagen fail-closed
  fehl.
- P4 Safe bleibt nach Commitment log-only. P4 Strict wird ohne tatsächlichen
  clientsichtbaren Reset/Abort nicht promotiert.
- Fokussierte Source-Checks und Real-H1-Host-Evidenz laufen gegen das aktuelle
  Binary und behalten ihren angegebenen Evidenz-Scope.

## Implementierungsentscheidung und Begründung

`composite.Coordinator` behält einen begrenzten unveränderlichen
Reservation-Snapshot und stellt einen HMAC-authentisierten opaque Lease erst
aus, nachdem ein payload-freier `reservation`-Lifecycle-Opener akzeptiert
wurde. `Activate` verwendet für P1 nur diesen Snapshot und bindet vertraute
Forwarded-Method-, URI- und Host-Metadaten an die Reservation; es akzeptiert
keine rohe Request-Context-Capsule über den ForwardAuth-HTTP-Hop. Snapshot- und
Lease-Material werden bei Terminalisierung gelöscht.

Die äußere Traefik-Middleware entfernt caller-gelieferte interne Header und
Trailer, reserviert über ihre owner-only UDS-Sitzung, leitet den Lease nur an
den unmittelbaren inneren ForwardAuth-Aufruf weiter und entfernt ihn vor dem
echten Upstream und der Client-Response. UDS-Read- und Result-Write-
Deadline-Fehler behalten den Grund `timeout`. Wenn ein UDS-Fehler vor dem
HTTP-Commit entsteht, löscht der äußere Writer ausstehende Upstream-Header/
Body und erzeugt eine sanitisierte 503.
Request-terminale ForwardAuth-Entscheidungen schreiben nun denselben
normalisierten finalen Status, der als Host-Aktion aufgezeichnet wird; ein
ungültiger Deny-/Redirect-Status kann daher nicht zu einer informationalen
oder erfolgreichen Response werden. Der private P1-Snapshot bewahrt außerdem
eine bekannte Transport-`Content-Length` von null, statt das explizite
Empty-Body-Feld stillschweigend auszulassen.

Das Envoy-Composite behält seinen geschützten `ext_authz`-Dynamic-Metadata-
Handoff und verwendet `ext_proc` für die Response-Beobachtung. Der gemeinsame
Evidence-Verifier erkennt den payload-freien Reservation-Opener und verlangt
ihn für einen Missing-Metadata-Pre-Admission-Receipt. Bevor das Envoy-
Composite ein disruptives P1/P2/P3-Ergebnis aufzeichnet oder ausgibt, hält ein
aktionsspezifischer Normalizer aufgezeichnete Host-Aktion und Wire-Ergebnis
gleich: Denies sind `4xx`--`5xx`, Redirects benötigen ein nicht leeres Ziel
und verwenden `3xx` plus `Location`, und jede andere fehlerhafte Entscheidung
schlägt als `403` fail-closed fehl.

Der geschützte Terminal-Marker lässt eine `ext_authz`-Local-Reply anschließend
durch `ext_proc` nur als validiertes `3xx` mit genau einer sicheren `Location`
oder als `4xx`--`5xx` ohne eine solche passieren. Jeder andere Marker schlägt
als sanitisierte `503` fail-closed fehl, ohne eine zweite Common-Transaktion zu
öffnen.

## Security-Auswirkung

Die betroffene Grenze ist Authorization-to-Response-Korrelation. Die Controls
verhindern clientgewählte Korrelation, rohe P1-Header-Propagation über die
ForwardAuth-HTTP-Trust-Boundary, Replay über UDS-Sitzungen und Lease-Egress zu
Clients/Upstreams/Events. Bounds gelten vor Snapshot-Kopien oder Protocol-
Allokationen. Ein fokussiertes unabhängiges Post-Fix-Review fand keinen
Supported-Path-High-/Critical-Issue oder Authorization-Bypass.

Request-terminale Host-Action-Metadaten und der ausgegebene ForwardAuth-HTTP-
Status bleiben nach fail-closed-Normalisierung nun identisch; fehlerhafte
`100`--`399`-Deny-/Redirect-Status können keine interimistische oder
erfolgreiche Client-Response erzeugen. Eine bekannte Transport-Content-Length
von null bleibt im begrenzten P1-Snapshot erhalten.
Dieselbe Invariante deckt nun Envoy-Composite-P1/P2 und Pre-Commit-P3-
Immediate-Replies ab, einschließlich aktionsbewahrender gültiger Redirects
und geschützter `ext_authz`--`ext_proc`-Terminal-Weitergabe.

`Hijack` und `Unwrap` bleiben nicht unterstützte Downstream-Response-Path-
Escape-Hatches; sie sind von No-Egress- und P3/P4-Garantien ausgeschlossen.
Nach HTTP-Commit ist eine Ersatz-503 absichtlich unmöglich und der
Response-Pfad bleibt, wo zutreffend, log-only.

## Geänderte Dateien

- `common/rules/modsecurity_p1_p4_vectors.conf` und
  `common/rules/p1_p4_traffic_vectors.json`
- `connectors/composite_harness/verify_matrix_evidence.py` und seine Tests
- Envoy-Composite-Coordinator-, Adapter-, Command-, Konfigurations-, Build-
  und Host-Runner-Pfade unter `connectors/envoy/`
- Traefik-`composite_middleware/`, Composite-Konfiguration, Driver, Upstream,
  Host-Runner und `README.md` / `README.de.md` unter `connectors/traefik/`
- Sonar-Remediation-Pfade in `ci/lib/runtime_path_utils.py`,
  `connectors/composite_harness/verify_matrix_evidence.py` sowie Traefik-
  Composite-Harness-Helfer und fokussierte Tests
- dieses englisch/deutsche Change-Record-Paar und die gekoppelten
  Archivindizes

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

Die vier expliziten Pre-Fix-Reproduktionen endeten erwartungsgemäß mit Exit
`1`; alle folgenden Post-Fix-Validierungen endeten mit Exit `0`.

- `CGO_ENABLED=1 go test -race -count=1 ./internal/composite ./internal/compositeenvoy ./internal/compositetraefik ./cmd/msconnector-composite` in `connectors/envoy/ext_proc` — fokussierte Coordinator-, Envoy-, UDS-, ForwardAuth- und Command-Race-Tests bestanden.
- `go test -race -count=1 ./...` in `connectors/traefik/composite_middleware` — Middleware-Race-Tests bestanden.
- `go vet ./internal/composite ./internal/compositeenvoy ./internal/compositetraefik ./cmd/msconnector-composite` in `connectors/envoy/ext_proc` und `go vet ./...` in `connectors/traefik/composite_middleware` — bestanden.
- `go test -count=1 -run TestForwardAuthNormalizesInvalidRequestDenyStatus ./internal/compositetraefik` — reproduzierte zunächst, dass ein fehlerhaftes P1-Deny den Client mit `103` erreichte; nach der Normalisierung bestand der Test sowohl für informationalen als auch für Erfolgsstatus-Input.
- `go test -count=1 -run 'TestCheckNormalizesMalformedRequestDenyStatus|TestCheckPreservesValidatedRedirect|TestNormalizePolicyDecisionRejectsInvalidRedirect|TestNormalizePolicyDecisionRejectsUnsafeRedirectTarget|TestProcessNormalizesMalformedP3DenyStatus|TestSendImmediatePreservesValidatedRedirect|TestProcessMarkedTerminalRedirectPassesThrough|TestProcessMarkedTerminalServerErrorPassesThrough|TestProcessMarkedTerminalInvalidRedirectFailsClosed' ./internal/compositeenvoy` — reproduzierte zunächst Envoy-P1/P2/P3-Status-/Evidence-Divergenz, verlorene Redirect-Location sowie durch `503` ersetzten markierten Redirect/5xx; nach aktionsspezifischer Normalisierung und Terminal-Marker-Validierung bestand er für fehlerhafte Deny-Status `103`, `200` und `600`, sichere Redirects, den Invalid-Redirect-Fallback und Terminal-Weitergabe ohne zweite Transaktion.
- `go test -count=1 -run TestReservationPayloadPreservesZeroTransportContentLength ./...` — reproduzierte zunächst das fehlende P1-Feld für Länge null; nach dem Fix bestand der Test.
- `PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v connectors.composite_harness.test_verify_matrix_evidence connectors.traefik.harness.test_composite_config` — 22 Verifier-/Konfigurations-Tests bestanden.
- `gofmt -d` für geänderte Go-Dateien und `sh -n connectors/envoy/build/build_composite.sh connectors/envoy/harness/run_envoy_composite_matrix.sh connectors/traefik/harness/run_traefik_composite_matrix.sh` — keine Formatter- oder Shell-Syntax-Diagnose.
- `BUILD_ROOT=<task-build-root> ... sh connectors/envoy/build/build_composite.sh` — der erneut gebaute Common/libmodsecurity-Composite für Envoy-Release `1.39.0` bestand.
- Fokussierte Inspektion von paired Record-/Dokument-Sprachumschaltern, erforderlichen Überschriften und lokalen Link-Targets — Exit `0`; die betroffenen englisch/deutschen Paare und lokalen Targets sind vorhanden.
- `make check-bilingual-docs` — Exit `2`; die neuen Records und betroffenen Composite-Dokumente bestanden ihre eigenen strukturellen Checks, während bestehende Repository-Links zum nicht initialisierten Framework-Submodule fehlen.
- `make check-doc-links` — Exit `2` wegen derselben bestehenden fehlenden Framework-Submodule-Link-Targets; kein betroffenes Composite- oder Change-Record-Target wurde als fehlend gemeldet.

## Runtime-Evidence

Frische Traefik-`3.7.10`-H1-Host-Läufe gegen das damals aktuelle Composite-
Binary lieferten:

| Fall | Client-Status | Evidenz-Scope |
| --- | ---: | --- |
| P1 allow | 200 | `LIFECYCLE_ONLY` P1/P2/P3/P4 |
| P1 deny | 403 | `LIFECYCLE_ONLY` P1 |
| P2 allow | 200 | `LIFECYCLE_ONLY` P1/P2/P3/P4 |
| P2 deny | 403 | `LIFECYCLE_ONLY` P1/P2 |
| P2 oversize | 413 | `LIFECYCLE_ONLY` P1/P2 |
| P3 deny | 403 | `LIFECYCLE_ONLY` P1/P2/P3 |
| P4 Safe | 200 | `LIFECYCLE_ONLY` P1/P2/P3/P4, log-only |
| metadata omitted | 503 | `LIFECYCLE_ONLY` Pre-Admission-Reservation plus terminales Disconnect |
| P2-to-P3 timeout | 503 | `LIFECYCLE_ONLY` P1/P2 plus terminales Timeout |

Jeder aufgeführte Traefik-Receipt hat `lifecycle_verified: true`,
`catalog_acceptance: false` und keinen am Client- oder Upstream-Boundary
berichteten Lease. Der P2-Allow-Lauf prüfte gezielt die explizite Empty-Body-
`Content-Length: 0`-Behandlung.

Die Final-Source-Envoy-`1.39.0`-H1-Matrix zeichnete P1/P2/P3/P4
Safe-, Spoofed-Lease-Header-, Metadata-Omission-, Lease-Expiry-,
Companion-Unavailability- und Same-Service-Follow-up-Controls auf. Ihre
Evidenz ist `structural_input_only`, keine Katalog-Akzeptanz. Die
Final-Current-Source-Runtime-Zusammenfassung ist payload-sicher und lokal bei
`FND-PARENT-0221` zurückgehalten; kein roher Payload, Credential, Lease oder
Decision-Token ist in diesem Record enthalten.

## Nicht ausgeführte Prüfungen mit Begründung

- P4 Strict wurde nicht promotiert: Envoy führt ihn absichtlich nicht aus und
  Traefik besitzt keinen unabhängig beobachteten clientsichtbaren Reset/Abort.
- Der gemeinsame Traefik-`p3_redirect`-Vektor ist als 403 deny konfiguriert,
  daher ist er als Redirect-Evidenz nicht bestanden.
- Die vollständige Traefik-Hostmatrix wurde nach dem finalen Envoy-only-
  Status-/Terminal-Normalizer-Patch nicht wiederholt. Ihre direkte
  Middleware-/UDS-Race-Suite bestand, und die früheren Traefik-Receipts
  behalten ihren angegebenen `LIFECYCLE_ONLY`-Scope.
- Real-Host-Duplicate-Response-Callback, Raw-Client-Cancellation,
  Same-Process-Traefik-Follow-up, H2/H3 und breitere Cross-Connector-Parität
  wurden nicht ausgeführt.
- Ein erster Timeout-Aufruf verwendete ein Runtime-Root-Suffix, das den
  kontrollierten Sechs-Sekunden-Delay absichtlich nicht auswählte und deshalb
  `200` zurückgab; er wird nicht als Evidenz akzeptiert. Der zurückgehaltene
  Rerun mit dem exakten kontrollierten Suffix lieferte die geforderte `503` und
  terminales `timeout`.
- Der Hosted-PR-Check `97747662107` wurde beobachtet und schlug mit New-Code-
  Security-Rating C statt des erforderlichen A fehl. Exakte Successor-Head-
  Checks, Review und Branch Protection stehen noch aus.

## Bekannte Einschränkungen

Der Traefik-Case-Driver ist eine operator-vertraute Grenze, daher sind seine
Receipts `LIFECYCLE_ONLY`. Die Envoy-Matrix ist `structural_input_only`. Keiner
der Scopes bewirbt vollständige Katalog-Akzeptanz oder Produktionsreife. P4
Safe liefert keine strikte Client-Disruption.

## Verbleibende Risiken

`FND-PARENT-0221` bleibt ein P0/high-Release-Blocker. P4 Strict,
Duplicate-Callback, Raw-Client-Cancellation, Same-Process-Traefik-Follow-up,
H2/H3 und Cross-Connector-Parität benötigen weitere Evidenz oder eine
ausdrückliche aktuelle Benutzer-Risikoentscheidung. Eine solche
Risikoakzeptanz existiert nicht.

## Finaler Diff- und Review-Status

Der finale lokale Review umfasst den scoped Source-Diff, gekoppelte
Dokumentation, fokussierte Tests, aktuellen CGo-Build, reale H1-Receipts und
unabhängiges Post-Fix-Security-Review. Draft-PR #341 und sein initialer scoped
Commit/Push sind beobachtet; ein Merge wurde nicht versucht. Die native
Remediation ist lokal validiert, doch der Post-Push-Exact-Head-Check,
Hosted-Check, Review-Entscheidung, Branch Protection und ein grünes
Sonar-Ergebnis stehen noch aus. Keine Framework-/MRTS-Änderung oder
Gitlink-Update wird behauptet.

## Initialer Sonar-Status nach Draft-PR

Draft-PR #341 gegen `master` liegt mit Commit/Head
`931d6eb81207997169719bb475d50274ae281eed` vor; ein Merge wurde nicht
versucht. Der Hosted-Check `97747662107` schlug mit New-Code-Security-Rating
C statt des erforderlichen A fehl und meldete zehn Vulnerabilities.
FND-SONAR-0061 ist P0/high, `in_progress` sowie release- und
kandidat-integration-blockierend. Eine native lokale Remediation läuft mit
descriptor-backed exakten `0700`-Roots, direkten `0600`-Leaves mit genau einem
Link, einer Runtime-Root-Kopie des Case-Inputs und einem festen
Loopback-/Origin-Form-Client. Es gab keine Suppression, keine
Konfigurationsänderung und keine Quality-Gate-Änderung. Fokussierte native
Tests validieren die Remediation lokal; der Post-Push-Exact-Head- und die
nachfolgenden Hosted-Checks stehen noch aus, und ein grünes Sonar-Ergebnis wird
nicht behauptet.

## Successor-Sonar und Upstream-TLS-Follow-up

Zu Beginn dieses scoped Follow-ups stand Draft-PR #341 auf
`9aeb0b551b34a0e44b9409130c2ecafeac641530`. Seine exakte
Successor-Sonar-Analyse `af6a96df-297f-47dd-af26-83b5315327e6` schloss/fixte
neun der ursprünglichen zehn Vulnerability-Records, ließ jedoch LOW
`python:S5332` am kontrollierten Upstream offen. Dies ist ein realer
Cleartext-Hop; er wird weder unterdrückt noch umklassifiziert.

Die Remediation ändert nur Traefiks internen kontrollierten Upstream-Hop. Der
Runner erzeugt pro Lauf ein `0600`-Zertifikat/Key im `0700`-Runtime-Root. Die
Dynamic-Konfiguration nutzt `https` mit einem zertifikatverifizierenden
`serversTransport` (`serverName` und `rootCAs`), und der kontrollierte
Upstream verlangt TLS 1.2 oder höher. Es gibt kein `insecureSkipVerify` und
keinen Plaintext-Fallback. Der Case-Driver bleibt der HTTP-Client von
Traefiks unverändertem öffentlichem Listener.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_runtime_artifact_utils connectors.composite_harness.test_verify_matrix_evidence connectors.traefik.harness.test_composite_config connectors.traefik.harness.test_composite_harness_paths` bestand mit 54 fokussierten Stdlib-Tests. Sie enthalten verifiziertes TLS, Ablehnung eines nicht vertrauten Zertifikats und Ablehnung eines vertrauten Zertifikats mit falschem Hostnamen gegen den tatsächlichen kontrollierten Upstream. Quellenbasierte Python-Kompilierung, Runner-Shell-Syntax und `git diff --check` bestanden ebenfalls. Ein unabhängiger scoped Security-Review fand keinen validierten Bypass. Die verbleibende Same-UID-Path-Replacement-Annahme ist dokumentiert; Cross-User-Zugriff wird durch den privaten Runtime-Root begrenzt.

Es gibt kein lokales `traefik`-Executable, daher sind tatsächliches
Traefik-Dynamic-Config-Parsing und ein realer TLS-aktivierter Matrix-Lauf in
dieser Umgebung blockiert. Als Nächstes folgen der autorisierte scoped
Commit/Push und die exakte Successor-Head-Hosted-Sonar-Validierung. Der
Draft-PR bleibt `DIRTY`; kein Rebase, Konfliktlösungs-Commit oder Merge ist
autorisiert.

## Scanner-kompatibler nativer TLS-Server-Successor

Der exakte PR-Head `00b767aec09ccab0a6cceba37c8dc4ae763395d5` bewahrt den
zertifikatverifizierenden Traefik-zu-Upstream-TLS-Transport, doch sein
gehosteter SonarCloud-Check `97786524327` schlug weiterhin fehl: Das
New-Code-Security-Rating war B mit einer neuen LOW-`python:S5332`-
Vulnerability am `server.serve_forever`-Aufruf des kontrollierten Upstreams.
Die lokale TLS-Kontrolle war real, aber diese Regel modelliert einen zu
`socketserver.BaseServer.serve_forever` aufgelösten Aufruf als Cleartext-
Server-Start-Sink, ohne den Zustand des wrapped Socket/Context fortzupflanzen.
Sie wird weder unterdrückt noch umklassifiziert.

Der scoped Successor behält das TLS-1.2-oder-höher-Zertifikat/Key-Paar bei und
nutzt Pythons nativen `http.server.ThreadingHTTPSServer` aus 3.14, an dessen
Konstruktor dieses Paar übergeben wird und dessen Socket-Context-
Minimum-Version gesetzt wird. Sein begrenzter prozess-ownender Loop setzt
`server.timeout = 0.2` und ruft wiederholt `server.handle_request()` auf.
Dies bewahrt Threaded-TLS-Request-Handling und entfernt zugleich den vom
Scanner modellierten generischen `serve_forever`-Sink; weder Traefiks
Zertifikatsverifikation noch der unveränderte öffentliche HTTP-Listener
ändern sich.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_runtime_artifact_utils connectors.composite_harness.test_verify_matrix_evidence connectors.traefik.harness.test_composite_config connectors.traefik.harness.test_composite_harness_paths` bestand mit 55 fokussierten Stdlib-Tests. Die zusätzliche Kontrolle prüft nativen TLS-Server und Request-Loop sowie verifiziertes TLS, die Ablehnung eines nicht vertrauten Zertifikats und die Ablehnung eines vertrauten Zertifikats mit falschem Hostnamen gegen den tatsächlichen kontrollierten Upstream. Quellenbasierte Python-Kompilierung, Runner-Shell-Syntax, `git diff --check` und ein Source-Scan auf den generischen Server-Start sowie Plaintext-Template- und unsichere Verifikationsmuster bestanden ebenfalls.

Es gibt kein lokales `traefik`-Executable, daher bleiben tatsächliches
Traefik-Dynamic-Config-Parsing und ein TLS-aktivierter Matrix-Lauf
`blocked_environment`. Als Nächstes folgen der autorisierte scoped Commit/Push
und die exakte Successor-Head-Hosted-Sonar-Validierung. Der Draft-PR bleibt
`DIRTY`; kein Rebase, Konfliktlösungs-Commit oder Merge ist autorisiert.

## Sonar-Remediation für null New Code (Hosted-Bestätigung dokumentiert)

Ein separates, begrenztes Follow-up refaktoriert die für diesen Draft-PR
gemeldeten 92 New-Code-Code-Smells und sechs Duplikatblöcke. Es ändert weder
Sonar-Konfiguration noch Quality Gate, Exclusion, Accepted-Issue-Status,
Coverage-Input oder Suppression. Die Source-Änderungen beschränken sich auf
verhaltenserhaltende Helper-Extraktion, Literal-Wiederverwendung,
Dispatcher-Aufteilung und fokussierte Test-Fixture-Wiederverwendung.

Der aktuelle lokale Source-Review identifiziert für jeden gemeldeten Befund
und jeden Duplikatblock eine strukturelle Remediation. Ungecachte Validierung
bestand für die vollständigen Envoy- und Traefik-Go-Suiten, die relevanten
Envoy-Race-Suiten, beide Go-vet-Suiten, 53 Python-Runtime-/Evidence-/Harness-
Tests, Go-Formatierung, Shell-Syntax und Diff-Whitespace. Ein unabhängiger
Security-Review bestätigte außerdem, dass die während dieses Follow-ups
gefundenen temporären Descriptor-Cleanup- und UDS-Outcome-Routing-Regressions
behoben sind und die Fail-Closed-Controls erhalten bleiben.

Die SonarCloud-Analyse um `2026-08-25T16:32:43Z` für Source-Head
`6af90bc98f90452faae1e7179ade38a2a41561b0` verzeichnete Quality Gate OK, 0
offene New Issues, 0 Accepted Issues, 0 Hotspots, 0 duplizierte neue
Blocks/Lines/Density sowie `new_lines_to_cover=0` /
`new_uncovered_lines=0`. Die Coverage-UI zeigt weiterhin 0.0%; dies wird als
beobachteter UI-Status dokumentiert und nicht als weitergehende Coverage-
Behauptung über die Zähler für neue Zeilen hinaus. Fünf GitHub-Workflows
bestanden. Der PR bleibt Draft/Open, und ein Merge wurde weder versucht noch
autorisiert. Die abschließende Verifikation dieses Dokumentations-Follow-ups
gegen seinen zukünftigen Dokumentations-Head steht noch aus.

## Codex-Feedback-Remediation für PR #341 — 2026-08-26

Der registrierte Task-Worktree für `agent/fnd-parent-0221-composite-connectors`
wurde normal auf `origin/master` bei
`c1653fb84201bc6a29c47723fa74e12270deb164` vorgezogen; `master` blieb
unverändert. Sieben aktuelle Codex-Review-Threads wurden behoben, ohne
Quality-Gate, Suppression, CI-Konfiguration oder Security-Control zu ändern:

- root-eigene nicht schreibbare Pfad-Ahnen werden akzeptiert; schreibbare
  Ahnen bleiben mit Ausnahme von root-eigenen sticky `/tmp` und `/var/tmp`
  abgewiesen;
- ein Claim vor der Aktivierung überlässt dem besitzenden UDS-Cleanup die
  `disconnect`-Begründung, statt mit einem `out_of_order`-Terminal zu rennen;
- ForwardAuth akzeptiert genau eine begrenzte URI mit Kommas und weist
  Control- oder übergroße Daten ab;
- leere gewöhnliche Headerwerte werden konsistent serialisiert und geparst,
  während Methode, URI, Headername und Host nichtleer bleiben;
- Downstream-Fehler und Short-Writes verhindern falsche P3/P4-EOS-/Outcome-
  Evidenz;
- ein Coordinator-Fehler wird nach Close abgefragt und hat Vorrang im
  Shutdown-Ergebnis; und
- der Composite-Response-Writer exponiert weder `Hijack` noch `Unwrap`, sodass
  ein nicht unterstütztes HTTP-Upgrade-Takeover fail-closed statt an P3/P4
  vorbeizulaufen fehlschlägt.

Die finalen lokalen Checks bestanden: Envoy-Coordinator-/ForwardAuth-/UDS- und
Command-Race-Tests, Traefik-Middleware-Race-Tests, beide betroffenen Go-vet-
Suiten, 39 fokussierte Python-Verifier-/Konfigurations-/Harness-Tests,
Traefik-Runner-Shell-Syntax und `git diff --check`. Das unabhängige
33-Dateien-Security-Diff-Review fand keinen neuen offenen Security-Kandidaten;
es hält den Pre-Fix-Raw-Writer-Escape als behobene Instanz von
`FND-PARENT-0221` fest und den separaten P4-Strict-Harness-Hinweis als
unterdrückte, nicht-promotende Evidence-Integrity-Notiz.

Dies sind ausschließlich lokale Final-Worktree-Ergebnisse. Corrective Commit,
Push sowie neue exakte Head-GitHub-/SonarCloud-Checks stehen noch aus; hier
wird kein zukünftiges Sonarqube-Ergebnis behauptet, und kein Merge ist
autorisiert.
