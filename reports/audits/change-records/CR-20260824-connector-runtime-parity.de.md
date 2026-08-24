# Change Record CR-20260824: Connector-Runtime-Paritätsbaseline

**Sprache:** [English](CR-20260824-connector-runtime-parity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260824-connector-runtime-parity` |
| Datum (UTC) | `2026-08-24` |
| Basis-Revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Scope | Nur Parent-Repository: fünf Connector-Source-/Testdateien und dieser gekoppelte Change Record. Keine Framework-/MRTS-/Gitlink-, Workflow-, Branch-Rule-, Required-Check-, CI-, Dependency- oder globalen Toolchain-Änderungen. |

## Motivation und Problemstellung

Die Connector-Matrix verlangte eine belegte lokale Baseline für Apache, NGINX,
HAProxy HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy ext_proc, Traefik
forwardAuth, Traefik Native UDS, Stock-lighttpd und Patched-lighttpd. Die
Stock-lighttpd-Source versteckte fälschlich einen gemeinsamen Response-Helper
hinter dem gepatchten Stream-Hook-ABI-Guard, obwohl Stock diesen Helper aus
seinem normalen Response-Start-Pfad aufruft. Der NGINX-Harness verlangte zudem
einen realen lokalen Master-/Worker-Lifecycle-Nachweis, statt den Sandbox-
Single-Process-Modus als produktionsgleich zu behandeln. Das HAProxy-Cleanup
musste seine task-eigenen Runtime-Marker nach bestätigter Kindprozessbeendigung
entfernen.

## Akzeptanzkriterien

- Stock-lighttpd-Referenzen auf APIs beschränken, die von seiner Stock-ABI
  deklariert werden; Patched-only-Streamfunktionen hinter dem Compile-Time-ABI-
  Guard belassen.
- Stock und Patched lighttpd getrennt mit dem gelockten Host `1.4.85` bauen;
  ihre unterschiedlichen Allow- und Block-Connectorpfade erhalten.
- Einen normalen NGINX-Master-/Worker-Lifecycle mit einem nicht privilegierten
  Worker, Readiness, Connector-Allow- und -Block-Traffic, Reload-Ersetzung,
  geordnetem Shutdown und Artefakt-Cleanup verlangen. Sandbox-Sondermodus ist
  kein normaler Worker-Nachweis.
- Jeden der zehn Connectorpfade getrennt für Source-Identität, Build,
  Konfigurationsvalidierung, Start, Readiness, Allow, Block, Shutdown und
  Cleanup belegen.
- CI und deren Konfiguration unverändert erhalten.

## Implementierungsentscheidung und Begründung

- Gemeinsame Lighttpd-Response-Header-Helper einschließlich
  `mod_msconnector_emit_host_transaction_id` werden außerhalb von
  `LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION` kompiliert; nur gepatchte
  Stream-Body-Hooks bleiben innerhalb dieses Guards. Dies ist eine ABI-korrekte
  Scope-Änderung, keine Warnungsunterdrückung und kein Stock-Stub.
- Ein fokussierter statischer Vertragstest prüft die Trennung zwischen
  gemeinsamen und nur gepatchten Lighttpd-Helpern.
- Der HAProxy-Smoke-Harness löscht nur seine expliziten PID- und Readiness-
  Dateien und erst nach seinen Kindprozess-Shutdown-Prüfungen.
- Der NGINX-Lifecycle-Harness behandelt deaktivierten Lifecycle-Modus in einem
  normalen Lauf als ungültig, erfasst erwartete initiale und Ersatz-Worker und
  schlägt fail closed fehl, wenn nach Shutdown verfolgte Prozesse, Listener,
  UDS-Pfade oder Runtime-Artefakte verbleiben.

## Security-Auswirkung

Diese Arbeit betrifft nicht vertrauenswürdige HTTP-Requestpfade und lokale
Prozessgrenzen. Die Änderungen erhalten reale Policy-Entscheidungen: Ein
legitimer Request erreicht den Connector und wird erlaubt, während ein eine
Regel auslösender Request denselben Connectorpfad erreicht und geblockt wird.
Kein Mock ersetzt einen Host oder Agent. Die Änderungen schwächen weder
Autorisierung, Request-Validierung, Compilerdiagnostik, Isolation,
Cleanup-Prüfungen noch CI-Controls. Verbleibende P1--P4-Feature-Arbeit wird
durch diese Baseline nicht als abgeschlossen behauptet.

## Geänderte Dateien

- `connectors/lighttpd/module/mod_msconnector.c`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `connectors/haproxy/harness/run_haproxy_smoke.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `connectors/nginx/tests/test_master_worker_lifecycle_contract.py`
- `reports/audits/change-records/CR-20260824-connector-runtime-parity.md`
- `reports/audits/change-records/CR-20260824-connector-runtime-parity.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Getrennter Stock-lighttpd Strict-C17-Module-Build gegen gelocktes `lighttpd-1.4.85` | Bestanden; Modul im isolierten Stock-Buildroot erzeugt. |
| Getrennter Patched-lighttpd Strict-C17-Module-Build gegen gelocktes `lighttpd-1.4.85` | Bestanden; Modul im isolierten Patched-Buildroot erzeugt. |
| `python3 -m unittest connectors.lighttpd.tests.test_patched_host_contract` | Bestanden: 36 Tests, 2 übersprungen. |
| `sh -n connectors/haproxy/harness/run_haproxy_smoke.sh` | Bestanden. |
| Finaler Stock-lighttpd-Hostlauf | Bestanden: Konfigurationsvalidierung, Allow `200`, Block `403` / Regel `1000001`, Connector-Event, geordneter Foreground-Host-Shutdown und Cleanup. Eine opt-in-Allow-Response trug `X-Msconnector-Host-Transaction-Id`. |
| Finaler Patched-lighttpd-Hostlauf | Bestanden: Konfigurationsvalidierung, Allow `200`, Block `403` / Regel `1000001`, Connector-Event, geordneter Foreground-Host-Shutdown und Cleanup. Der gepatchte Host exportiert weiterhin beide Entity-Body-Hook-Symbole; dieser Lauf beansprucht kein P4. |
| Finaler HAProxy-HTX-Lauf | Bestanden: realer Overlay-Host mit Konfigurations-/Readinessprüfung, Allow `200`, Block `403` und `processes_stopped=yes`. |
| Finale HAProxy-SPOE/SPOP-Läufe | Getrennt bestanden: realer HAProxy `-db` + SPOA-Agent + Python-Backend Allow `200` und Block `403`; alle vier task-eigenen PID-/Readiness-Marker waren nach jedem Lauf abwesend. |
| `python3 -m unittest connectors.nginx.tests.test_master_worker_lifecycle_contract` | Bestanden: 7 Tests. |
| `sh -n connectors/nginx/harness/run_nginx_smoke.sh` | Bestanden. |
| Finale NGINX-Transient-Service-Läufe | Bestanden: getrennte Allow-`200`-, Block-`403`- und forced-quit/`TERM`-fallback-Allow-`200`-Läufe; jeder config-testete, erreichte Readiness, nutzte root-Master plus `nobody:nogroup`-Worker, reloadete zu einem anderen Worker und beendete Cleanup mit Exit `0`. |
| Lifecycle-disabled-NGINX-Negativkontrolle | Bestanden: Normaler Lauf endete vor Hoststart mit Exit `1`. |
| `git diff --check` auf dem finalen Delivery-Diff | Bestanden. |

## Runtime-Evidence

Die versiegelte Hauptmatrix wird unter
`/var/tmp/codex/ModSecurity-conector/task-connector-runtime-parity-20260824/runs/20260824T103505Z-connector-runtime-parity-61be62e2`
aufbewahrt. Ihre Manifest-SHA-256 ist
`cdfaaab244fd580f97f876de190c4a6d4c809ef56a839f96808a54e42fe9e2e4`.
Die getrennt aufbewahrte Traefik-Native-UDS-Evidence liegt unter
`/var/tmp/codex/ModSecurity-conector/t.aeQFSv/runs/20260824T122139Z-traefik-native-uds-41fdda3c`.

Der finale Exact-Source-NGINX-Receipt wird unter
`/var/tmp/codex/ModSecurity-conector/connector-runtime-parity-delivery-20260824/evidence/final-nginx-master-worker-verification.md`
mit SHA-256
`64dfe67c16c6b6b6b49fb9c921b2a689fa43ca0b5319148ee8d092d0376703f4`
aufbewahrt. Seine Harness-SHA-256 ist
`301323aa66255ae04e7be1d2e2620c285371a8039f2c9d18039c984cab7d8af9`
und die Lifecycle-Test-SHA-256 ist
`df3dfe851459258897389b4df442afbc8c33331f99d51c1897c67f2137bee561`.
Der aktuelle Changed-Connector-Rerun-Receipt wird daneben als
`final-changed-connector-reruns.md` mit SHA-256
`d0e291b695ca605a8670e36493bb1472deca91227d5839d6d0b985297ffcde2c`
aufbewahrt.

Die gelockten Hostversionen sind Apache HTTP Server `2.4.68`, NGINX `1.31.4`,
HAProxy `3.2.22`, Envoy `1.39`, Traefik `3.7.11` und lighttpd `1.4.85`.
Die Runtime-Receipts zeigen für alle zehn genannten Pfade getrennte reale
Host-Allow- (`200`, Regel `2103`) und -Block- (`403`, Regel `2101`) Requests,
Readiness, Shutdown und Cleanup; NGINX zeigt zusätzlich Master/root,
Worker/non-root, Reload-Ersetzung, Lifecycle-disabled-Ablehnung und
Fallback-Cleanup-Verhalten.

## Nicht ausgeführte Prüfungen mit Begründung

- CI, Hosted-Checks, SonarCloud, Workflow-Ausführung und Required-Check-
  Änderungen wurden absichtlich weder ausgeführt noch verändert, weil sie
  außerhalb des autorisierten Scopes liegen.
- Es wurde keine globale Dependency-Installation und kein mutable Host-Source-
  Fallback verwendet.
- `make check-bilingual-docs` und `make check-doc-links` wurden nach der
  Korrektur der Change-Record-Überschriften ausgeführt. Beide bleiben in diesem
  frischen Parent-Worktree blockiert, weil sein gepinnter Framework-Gitlink
  absichtlich uninitialisiert ist und bestehende Repository-Links daher kein
  lokales Ziel haben. Weder Framework-Checkout noch Source-Änderung,
  Gitlink-Update oder Link-Workaround waren autorisiert. Die Checks meldeten
  keinen verbleibenden Change-Record-Überschriftenfehler.

## Bekannte Einschränkungen

Die Evidence-Roots sind aufbewahrte lokale Evidence, keine versionierten
Source-Dateien. Der finale NGINX-Receipt nennt die exakten finalen Harness-
und Test-Hashes; ältere POSIX-Receipts bleiben nur historische Evidence. Dieser
Record beansprucht auch nicht den Abschluss zukünftiger P1--P4-Connector-
Arbeit.

## Verbleibende Risiken

Die isolierten Testhosts beweisen keine deploymentspezifischen
Produktionsrichtlinien, Namespace-Einschränkungen oder Operator-Konfiguration.
Die Aufgabe behält absichtlich fail-closed Lifecycle- und Cleanup-Prüfungen,
damit eine nicht verfügbare normale NGINX-Worker-Umgebung nicht als
erfolgreiches Produktionsmodell falsch berichtet werden kann.
Die beiden repositoryweiten Dokumentationschecks verlangen einen befüllten
gepinnten Framework-Gitlink und bleiben daher environment-blocked, nicht
abgewählt.

## Finaler Diff- und Review-Status

Der Nutzer autorisierte nur einen frischen task-eigenen Branch, normalen
Commit, Push und Draft-PR. Weder Merge noch direkter `master`-Push,
Framework-/MRTS-Modifikation, Gitlink-Update, CI-Aktion oder Protected-Check-
Ergebnis ist autorisiert oder wird behauptet.
