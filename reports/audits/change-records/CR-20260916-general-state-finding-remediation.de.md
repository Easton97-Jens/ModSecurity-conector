# Change Record: Behebung validierter General-State-Findings

**Sprache:** [English](CR-20260916-general-state-finding-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260916-general-state-finding-remediation |
| Datum (UTC) | 2026-09-16 |
| Basis-Revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Benutzerautorisierung | Ursprünglicher Scope: „kümmere dich in dem bestehenden pr um die sichere behebung der sachen“. Delivery-Fortsetzung: „erstelle ein pr mit den änderung“. |
| Delivery-Status | Erweitert ausschließlich Parent-Draft-PR #369. Ein normaler inkrementeller Commit und Push auf seinen bestehenden Branch liegen im Scope; kein Merge, Auto-Merge, direkter `master`-Schreibvorgang, Framework-/MRTS-/Gitlink-Change oder Branch-Löschung ist autorisiert. Der aktualisierte exakte PR-Head und Hosted-Checks müssen nach dem Push noch beobachtet werden. |

## Motivation und Problemstellung

Der zurückbehaltene General-State-Lauf `20260913T142629Z-e475baa` vermischte
bestätigte Parent-Defekte mit Runtime-Evidenzlücken und Framework-eigenen
Beobachtungen. Diese Änderung repariert nur bestätigte Parent-eigene Grenzen
mit einem gezielten Regressionspfad:

- `FND-PARENT-1093`: Expat-Provenance ist in jedem Vorbereitungsmodus
  unveränderlich.
- `FND-PARENT-1096`: Der opt-in Envoy-Response-Phase-Smoke wählt passende
  P1/P3/P4-Regeln und weist doppelte Evidenz-Records ab.
- `FND-PARENT-1097`: Apache APXS erhält eine gestagte Profile-Registry
  außerhalb des kanonischen Parent-Checkouts, auch im Frischquell-
  Autotools-Bootstrap.
- `FND-PARENT-1095`: Das private NGINX-Build-Child ersetzt geerbtes
  `TAR_OPTIONS` durch `--no-same-owner`, bevor der Framework-Provisioner das
  gepinnte Source-Archiv extrahieren kann.
- `FND-PARENT-1099`: Eine statische NGINX-Harness-Regression bindet die
  Path-Authority-Validierung vor dem Root-zu-Worker-Ownership-Handoff; ihr
  nativer Runtime-Nachweis bleibt durch Host-`chown(...)=EINVAL` blockiert.
- `FND-SONAR-0084`: Die Parent-HAProxy-SPOP-Accept-Loop entfernt das gemeldete
  terminale `goto`, während Worker-Drain- sowie Error-/Restart-Pfade erhalten
  bleiben.

Die separat dokumentierte lighttpd-Endpunktmetadaten-Reparatur des bestehenden
PR bleibt unverändert. Dieser Record macht aus keiner blockierten
Runtime-Beobachtung eine Produktdiagnose und ändert weder Framework noch MRTS.

## Akzeptanzkriterien

- `EXPAT_GIT_REF` akzeptiert exakt eine 40- oder 64-stellige hexadezimale
  Objekt-ID und Expat löst niemals ein veränderliches Latest-Release auf.
- Der Standard-Envoy-P1-Smoke bleibt unverändert; ein separates Response-Target
  wählt `modsecurity_response_companion_smoke.conf`, aktiviert seine
  Response-Assertions und stellt nur seine pfadbezogenen P3/P4-Fixturedaten
  bereit.
- Response-Phase-Evidenz verlangt exakt einen korrelierten P3-Deny-Record und
  exakt einen korrelierten P4-Safe-Record ohne Response-Payload-Felder.
- APXS kompiliert ein gestagtes `connectors/profile_registry.c` und erhält einen
  gestagten Include-Root. Ein direkter oder über Symlink aufgelöster
  Staging-Ort im kanonischen Checkout schlägt fehl, bevor
  Profile-Registry-Artefakte entstehen.
- Gezielte Regressionstests und gleichgrenzige Negativkontrollen bestehen,
  ohne einen nativen Envoy-Service zu starten. Der lokale Frischquell-Apache-
  Build erreicht seine Modul-Output-Prüfung; seine spätere Runtime-Phase wird
  jedoch durch ein Host-Dateisystem blockiert, das `chown(...)=EINVAL`
  zurückgibt.
- Das NGINX-Build-Child übergibt immer `TAR_OPTIONS=--no-same-owner`; feindliche
  und fehlende geerbte Werte erreichen den tatsächlichen Build-Process-Sink
  weder für H1-, H2- noch H3-Profile.
- Der NGINX-Harness validiert beide Worker-eigenen Pfade vor der Root-Mutation
  und vor seinem Non-Root-Handoff, ohne statische Evidenz als native
  Runtime-Coverage auszugeben.
- HAProxy-terminale Accept-Fehler und STOP-Ergebnisse verlassen die Intake-Loop
  über ein explizites Loop-Prädikat, bewahren Counting-/Error-Semantik und
  erreichen weiterhin den einzelnen Worker-Drain-Pfad.

## Implementierungsentscheidung und Begründung

### Unveränderliche Expat-Provenance

`prepare_expat_git_component` delegiert nun immer an
`prepare_immutable_git_component`; `strict` steuert weiterhin nur die
gemeinsame Cache-/fsck-Policy. `required_runtime_component_sources` validiert
`EXPAT_GIT_REF`, bevor einer der Modi einen Git- oder Release-Resolution-Sink
erreichen kann. Das Full-Object-Prädikat akzeptiert nur exakt 40 oder exakt 64
hexadezimale Zeichen. Der vom Framework gelieferte Default ist der vollständige
40-stellige Commit `92810461043fce37e70079b37ab1f04490a8f039`. Die generischen
Release-Resolution-Pfade von `go-ftw` und `albedo` bleiben absichtlich
unverändert.

Dies entfernt eine veränderliche Upstream-Auswahl über `releases/latest` aus
der Expat-Build-Input-Grenze. Eine veränderliche Expat-Referenz schlägt nun vor
Git- oder Release-Lookup fail-closed fehl.

Das gezielte Follow-up entfernt das zuvor ungenutzte Argument
`expected_prompt_latest` aus diesem internen Expat-Helper und seinen Aufrufern
sowie das ungenutzte Argument `strict` aus der Source-Validierung.
`EXPAT_PROMPT_EXPECTED_LATEST` bleibt ein exportierter und dokumentierter
Kompatibilitätsinput; er beeinflusste die unveränderliche Vorbereitung nicht.
Der abgeleitete Strict-Wert bleibt im Runtime-Kontext und steuert weiterhin die
nachgelagerte Vorbereitung sowie Cache- und fsck-Verhalten.

## Security-Auswirkung

Die Reparatur verengt die Source-Provenance, bewahrt den Envoy-Testmodus als
Standard, verhindert, dass APXS Profile-Registry-Build-Artefakte in einem
kanonischen Source-Checkout ablegt, verhindert geerbten Archive-Owner-Restore
im NGINX-Child und erhält NGINX-Path-/Ownership- sowie HAProxy-Worker-Drain-
Controls. Sie lockert keinen Host-, Dateiberechtigungs-, UDS-, URI-,
Response-Payload-, Ownership-, ACL-, Symlink-, Mode- oder Capacity-Control.
Unbewiesene Runtime-Beobachtungen bleiben ungepatcht.

### Envoy-Response-Phase-Smoke-Evidenz

`response-phase-smoke-envoy` ist ein opt-in-Make-Target. Es wählt
`common/rules/modsecurity_response_companion_smoke.conf` und exportiert
`MSCONNECTOR_RESPONSE_PHASE_SMOKE=1`; normales `runtime-smoke-envoy` behält
sein P1-Standard-Regelfixture. Target-spezifische `override`-Zuweisungen
verhindern, dass eine Kommandozeilen-`RULES_FILE` oder
`MSCONNECTOR_RESPONSE_PHASE_SMOKE=0` dieses Target auf P1-only-Coverage
reduziert. Der Upstream-Helper emittiert `X-Modsec-Upstream: block` nur für
`/phase3-block` und den Response-Body-Marker nur für `/phase4-marker`.

Der Event-Verifier weist jetzt null, fehlende oder doppelte passende P3/P4-
Records ab. Er speichert keine Response-Payload-Daten. Dies korrigiert die
Test-Evidenzauswahl; es behauptet keine native Envoy-Response-Phase- oder
Original-URI-Korrelations-Evidenz.

### Apache-Profile-Registry-Staging

APXS/libtool kann Objektartefakte neben einem C-Input schreiben. Der Wrapper
löst nun den kanonischen Checkout und den angeforderten Staging-Parent auf,
bevor er das Staging-Verzeichnis erzeugt, weist Pfade im Checkout (auch über
einen Symlink) ab, löst den finalen Root erneut auf und kopiert dann
`connectors/profile_registry.c` und `.h` dorthin. APXS erhält nur die gestagte
Source und den gestagten Include-Root.

Normale Out-of-Tree-Builds bleiben unterstützt. Ein Profile-Registry-
Staging-Root im Checkout schlägt jetzt fail-closed fehl, statt `.o`, `.lo`,
`.slo` oder `.libs/*.o`-Artefakte im Source-Checkout zu erlauben.

Der Autotools-Bootstrap extrahiert seinen synthetischen Checkout unter
`$WORK_ROOT/source` und übergibt den Geschwisterpfad
`$WORK_ROOT/profile-registry` nur an seinen `make`-Aufruf. `WORK_ROOT` ist ein
privates `mktemp`-Verzeichnis, das nach `umask 077` unter dem konfigurierten
Test-Parent angelegt und durch das bestehende begrenzte Cleanup entfernt wird.
Damit erhält der Wrapper für diesen synthetischen Checkout einen externen
Stage-Root, ohne seine Canonical-Path- oder Symlink-Abweisung zu lockern.

### NGINX-Archiv-Owner-Grenze und Harness-Authority

Die NGINX-Build-Umgebung ersetzt `TAR_OPTIONS` jetzt, statt es zu erben, durch
`--no-same-owner`. Archivierte UID-/GID-Metadaten sind kein Build-Input, und ein
Aufrufer kann Owner-Restore nicht über seine Umgebung wieder aktivieren, bevor
der Framework-eigene Provisioner das gepinnte Archiv extrahiert. Die Regression
prüft feindliche und fehlende geerbte Werte am tatsächlichen `run_build`-Child-
Environment für H1, H2 und H3.

Die NGINX-Harness-Source bleibt absichtlich unverändert. Ihr neuer statischer
Contract bestätigt, dass beide abgeleiteten Worker-Pfade vor Root-eigener
Mutation und dem aufgelösten Non-Root-Mode-`0700`-Handoff an die generische
Path-Authority-Validierung übergeben werden. Das schützt die etablierte
Reihenfolge, macht aber ein Dateisystem, das das erforderliche `chown`
zurückweist, nicht fähig.

### HAProxy-SPOP-Accept-Loop-Wartung

`accept_loop` verwendet statt eines terminalen `goto` oder STOP-`break` ein
initialisiertes `loop_running`-Prädikat. Ein terminaler Accept-Fehler oder STOP
löscht dieses Prädikat und fährt mit der Bedingung fort; dadurch treten beide
Pfade in den bestehenden Post-Loop-Worker-Drain ein. Das Refactoring erhält
`loop_rc`, Capacity-Rejection, Handled-Count, Owner-Restart-Priorität,
Descriptor-Close und die Zerstörungsreihenfolge der Synchronisation.

## Geänderte Dateien

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `connectors/envoy/Makefile`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `tests/test_envoy_transport_hardening_contract.py`
- `connectors/apache/build/apxs-wrapper.in`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/_haproxy_spop_contract_helpers.py`
- `tests/test_nginx_harness_path_authority.py`
- `tests/test_sonar_reliability_contract.py`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.md`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.de.md`
- `reports/audits/change-records/CR-20260916-general-state-finding-remediation.md`
- `reports/audits/change-records/CR-20260916-general-state-finding-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Check | Ergebnis | Beobachtetes Ergebnis |
| --- | --- | --- |
| Verifiziertes Projekt-vEnv: `python -m unittest -v tests.test_prepare_runtime_components tests.test_envoy_transport_hardening_contract tests.test_apache_apxs_profile_registry_staging tests.test_apache_common_adoption` mit Bytecode- und temporären Ausgaben außerhalb des Checkouts | bestanden | 134 Tests bestanden; 5 bestehende Framework-abhängige Tests wurden übersprungen, weil der Framework-Test-Root nicht zum Parent-Gitlink passte. |
| Gezieltes Post-Sonar-Follow-up: `python -m unittest -v tests.test_prepare_runtime_components` mit Bytecode- und temporären Ausgaben außerhalb des Checkouts | bestanden | 90 Tests bestanden; 5 bestehende Framework-abhängige Tests wurden übersprungen, weil der Framework-Test-Root nicht zum Parent-Gitlink passte. |
| `sh -n ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh` und `sh -n connectors/apache/build/apxs-wrapper.in` | bestanden | Shell-Syntax akzeptiert. |
| `sh -n connectors/envoy/harness/run_envoy_connector_runtime.sh` | bestanden | Shell-Syntax akzeptiert. |
| `make -n -C connectors/envoy response-phase-smoke-envoy` | bestanden | Dry-Run zeigt die Companion-Regeldatei und `MSCONNECTOR_RESPONSE_PHASE_SMOKE=1`; kein Build oder Service lief. |
| `APACHE_AUTOTOOLS_TEST_PARENT=... APACHE_AUTOTOOLS_RUNTIME_PARENT=... make check-apache-autotools-bootstrap` | blocked_environment (make exit 2) | Der Frischquell-Snapshot absolvierte Autotools-Konfiguration, `make` und die Modul-Output-Prüfung; ein späteres Runtime-`chown` im kontrollierten `/var/tmp`-Root schlug mit `EINVAL` fehl. |
| `make check-bilingual-docs` | blocked_environment | Der Checker meldete keinen Fehler für einen der aktuellen Change Records, scheiterte aber an 20 bestehenden Links, deren Framework-Gitlink-Ziele in diesem Worktree fehlen. |
| `make check-doc-links` | blocked_environment | Die Repository-Link-Validierung scheiterte an denselben bestehenden fehlenden Framework-Gitlink-Zielen; kein geänderter Change-Record-Link wurde gemeldet. |
| `git diff --check` | bestanden | Keine Whitespace-Fehler vor der Delivery-Vorbereitung. |
| Aktuelle PR-Worktree-Focused-Suite: `python -m unittest tests.test_prepare_runtime_components tests.test_nginx_harness_path_authority tests.test_sonar_reliability_contract tests.test_haproxy_spop_peer_isolation_contract tests.test_haproxy_spop_sigpipe_peer_isolation_contract` | bestanden | 140 Tests bestanden; 5 bestehende Framework-Root-Tests wurden übersprungen. Dies umfasst NGINX-Child-Environment-/Process-Sink-, NGINX-Authority-Ordering- und HAProxy-Loop-Contracts. |
| `BUILD_ROOT=<private task root> make check-haproxy-c17` | bestanden | Die geänderte HAProxy-Source kompilierte mit dem Repository-C17-Profil. |
| `TMPDIR=<private task root> BUILD_ROOT=<private task root> make -C connectors/haproxy build-spoa-runtime self-test-spoa-runtime` | bestanden | Der isolierte SPOP-Selbsttest übte gültige/malformed Frames und eine disruptive ModSecurity-Entscheidung aus; er ist keine native HAProxy-Enforcement-Behauptung. |

Die Apache-Fake-APXS-Kontrolle beweist, dass erzeugte Profile-Registry-
Artefakte nur unter dem externen Stage-Root existieren. Ihre Negativkontrollen
weisen einen direkten In-Checkout-Root und einen in den Checkout aufgelösten
Symlink ab. Der Bootstrap-Contract bewahrt seine eine private
Geschwister-Stage-Zuweisung, während der partielle native Bootstrap-Lauf
beweist, dass der Build über den ursprünglichen CI-Fehlerpunkt hinauslief: Er
erreichte die Modul-Output-Prüfung vor der unabhängigen Host-Ownership-
Operation. Die Expat-Kontrollen weisen veränderliche, abgekürzte, 41-stellige
und 63-stellige Referenzen vor Git-/Release-Lookup ab; 40- und 64-stellige
Referenzen bleiben akzeptiert. Die Envoy-Kontrollen bewahren das
P1-Standard-Target und weisen doppelte P3/P4-Evidenz ab.

Die aktuellen NGINX-Controls beweisen außerdem, dass das erzeugte Child-
Environment feindliche/fehlende `TAR_OPTIONS`-Werte am Build-Process-Sink
ersetzt und dass beide Worker-Roots vor dem Non-Root-Handoff validiert werden.
Die HAProxy-Contracts decken die terminale Accept-Error- und STOP-
Exit-Reihenfolge ab, während der gemeinsame Drain erhalten bleibt. Die C17-
und isolierten SPOP-Checks liefern ausschließlich Kompilierungs- und
Protokoll-/Selbsttest-Evidenz.

## Runtime-Evidence

Das Envoy-Helper-Fixture wurde vom gezielten Python-Contract-Test ausgeführt,
nicht von einem nativen Envoy-Prozess. Der Apache-Fake-APXS-Test übte die
Wrapper-Argument- und Artefaktgrenze aus. Der lokale Apache-Bootstrap übte
zusätzlich seinen echten Autotools-/APXS-Modul-Build aus, aber keine
abgeschlossene Server-Runtime, weil das kontrollierte Host-Dateisystem eine
spätere Ownership-Änderung abwies. Dies sind ausschließlich begrenzte lokale
Evidenzpfade.

Der HAProxy-Runtime-Selbsttest ist ein isolierter Loopback-SPOP-Protokolltest.
Er übt Handshake, Malformed-Frame-Rejection und Typed-Disruptive-Decision-ACK-
Verhalten aus, jedoch keinen nativen HAProxy-Host-Enforcement-Pfad. Keine
native NGINX-Runtime lief, weil der erforderliche Worker-Ownership-Handoff
durch das Host-Dateisystem blockiert bleibt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Envoy-Build oder -Service, keine abgeschlossene Apache-Server-
Runtime-Prüfung, keine vollständige Connector-Matrix, keine SonarQube-Cloud-
Analyse und kein Hosted-PR-Check liefen am exakten Head dieses Follow-ups. Ein
nativer Envoy-Runtime-Lauf benötigt den separaten Runtime-Preflight und einen
kurzen privaten absoluten Runtime-Root für seinen UDS; beides wird nicht durch
die statischen Contract-Tests impliziert. Das Post-Build-Ownership-Problem des
lokalen Apache-Bootstraps ist eine Host-Dateisystemgrenze und keine Evidenz,
die eine Lockerung der Ownership-Logik erlauben würde. Keine Framework-Source
oder extern vorbereitete CRS-Inhalte wurden geändert oder getestet.

## Bekannte Einschränkungen

- `FND-PARENT-1091` bleibt durch seinen eigenen lighttpd-Change-Record
  abgedeckt. Sein Immediate-Client-Reset-Test ist ein nachgewiesener
  Scheduler-Race; ein deterministischer Broken-Peer-Harness gehört in eine
  separate, eng begrenzte Test-Stabilitätsänderung.
- `FND-PARENT-1092` (Traefik) bleibt `blocked_missing_evidence`: Die
  vorgeschlagene Empty-Body-P2-Ursache wird vom Common-Finish-Pfad
  widerlegt. Vor Änderungen am Lifecycle-Code ist eine gezielte Runtime-
  Body-A/B-Matrix erforderlich.
- `FND-PARENT-1096` ist lokal nur für Regel-/Fixture-/Evidenzauswahl
  repariert. Native Response-Phase-Ausführung und Original-URI-Korrelation
  bleiben unverifiziert.
- Die fünf übersprungenen Tests in der kombinierten Suite benötigen einen
  Framework-Test-Root, dessen Commit dem Parent-Gitlink entspricht.
- Der lokale Apache-Bootstrap benötigt ein ownership-fähiges Dateisystem, um
  seine Runtime-Phase abzuschließen. Sein isolierter `/var/tmp`-Root erreichte
  den Modul-Build, scheiterte aber später an `chown(...)=EINVAL`; für volle
  Runtime-Evidenz ist weiterhin der korrigierte Hosted-Rerun erforderlich.

## Verbleibende Risiken

- `FND-PARENT-1098` (Apache 403 gegenüber 413) bleibt
  `blocked_missing_evidence`; eine Änderung von `AP_FILTER_ERROR` vor der
  Nachverfolgung der initialen Terminalbedingung könnte einen fail-closed-Pfad
  regressieren.
- `FND-PARENT-1094` ist Framework-eigen und hat keine checked-in Standard-
  `t:hexDecode`-Reachability. Exakte externe CRS-Inhalte müssen in einer
  separat autorisierten Framework-Analyse geprüft werden, bevor ein
  Framework-Patch erfolgt.
- `FND-PARENT-1095` und `FND-PARENT-1099` bleiben Umgebungsblocker. Archive-
  Owner-Restore hat nun eine enge Child-Environment-Härtung und NGINX-
  Ordering eine statische Regression. Vollständige Archive-Extraktion und
  nativer NGINX-`chown(...)=EINVAL`-Nachweis benötigen weiterhin einen
  geeigneten Host; keine Owner-, ACL-, Symlink- oder Mode-Prüfung wurde
  gelockert.

## Finaler Diff- und Review-Status

Dieser Record dokumentiert lokale Evidenz für das aktuelle Update des
bestehenden Draft-PR. Vor/nach dem inkrementellen Push müssen lokale,
Remote-Branch- und PR-Head-SHAs exakt verglichen werden; Hosted-Checks,
SonarQube, Review-Status und ein späterer Merge bleiben getrennte beobachtete
Fakten. Insbesondere ist `FND-SONAR-0084` nur lokal fixed, bis SonarQube den
neuen exakten PR-Head liest, und native NGINX-Runtime bleibt
`blocked_environment`. Es wird kein Merge behauptet.
