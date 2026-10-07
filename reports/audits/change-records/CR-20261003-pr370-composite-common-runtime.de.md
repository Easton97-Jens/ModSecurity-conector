# Change Record: CR-20261003-pr370-composite-common-runtime

**Sprache:** [English](CR-20261003-pr370-composite-common-runtime.md) | Deutsch

Parent-Nachfolger mit NGINX-Ausschluss aus der Reife-B-Qualifikation: Common-/Connector-Korrekturen, Qualifikationsverträge und begrenzte beobachtete Lifecycle-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261003-pr370-composite-common-runtime |
| Datum (UTC) | 2026-10-03 |
| Basis-Revision | `c58de8e534463f56875e6f038380d342fcb1fea4` |

## Motivation und Problemstellung

Der Go-Composite-Dienst von PR #370 wählte die direkte Envoy-ext_proc-Identität und den Streaming-Requestmodus für gepufferte Autorisierungsrequests. Start oder ein vorzeitiger P2-Abschluss konnten fehlschlagen. Die Korrektur behebt zudem native Claim-, Ablauf- und Cleanup-Ownership-Defekte und ersetzt Surrogat-Folgeanfragebelege durch unabhängige Request-/Response-Beobachtungen. Der aktuelle Nachfolger korrigiert und prüft zusätzlich ausgewähltes Apache-, Envoy-, HAProxy- und Traefik-Verhalten und entwickelt bei fehlender Evidenz sperrende Qualifikationsverträge für beide lighttpd-Profile. NGINX-Änderungen aus aktuellem Master dürfen integriert werden; NGINX bleibt jedoch aus Reife-B-Qualifikation und Runtime-Anrechnung ausgeschlossen.

## Akzeptanzkriterien

Geschlossene Composite-Modi wählen kanonische Identitäten und gepufferte Request-/gestreamte Response-Modi. Header-Start verschiebt P2 bis zum expliziten EOS; gewöhnliches Begin bleibt kompatibel. Ungültige Claims können keinen nativen Zustand übernehmen. Echte Body-Limits liefern 413 mit Host-Aktionsmetadaten und erlauben eine Folgeanfrage derselben Engine. Konsumiertes Cleanup darf freigegebenen Zustand nicht erneut verwenden; unaufgelöstes Cleanup sperrt die Aufnahme. Qualifikationsrunner bewahren hostspezifische Phasen-, Limit-, Recovery-, Identitäts- und Cleanup-Beobachtungen und melden fehlende unabhängige Evidenz ausdrücklich. Diese Kriterien gelten für die implementierten Korrekturen und Verträge; vollständige G1–G9-Abnahme aller neun Nicht-NGINX-Profile bleibt offen.

## Implementierungsentscheidung und Begründung

`msconnector_runtime_transaction_begin_request_headers()` hinzufügen, das ausschließlich BUFFERED mit `body.data == NULL` und `body.size == 0` akzeptiert; explizites Append und Finish bei EOS verlangen. Gewöhnliches Begin verarbeitet weiterhin die vollständige gepufferte Entity einschließlich einer leeren Entity. Terminales Host-413-Cleanup protokolliert ohne erfundenes EOS oder P2.

`envoy / ext_authz / envoy-ext-authz` oder `traefik / forwardAuth / traefik-forwardauth` wählen. Die direkte Common-Engine `envoy / ext_proc / envoy-ext-proc` behält gestreamte Request-/Response-Callbacks; der Host-Renderer unterstützt zusätzlich `PROFILE=buffered-admission` mit BUFFERED-Requesttransport. Go-Claim, Kontext und Deadline vor dem nativen Claim prüfen und Lease-Laufzeit koppeln. Erfolgreiches Close, konsumierten Fehler und unaufgelöstes Cleanup unterscheiden; den nativen Zustand einmalig stilllegen, Entry-Ownership bis zum terminalen Cleanup behalten und Cleanup-Fehler in einen dauerhaften Coordinator-Fehlerzustand und ein fehlgeschlagenes terminales Event übernehmen. Der Envoy-Harness erfasst getrennte begrenzte eigentümerexklusive Request- und Response-Belege.

## Geänderte Dateien

Der aktuelle Nachfolger umfasst diese Gruppen geänderter Dateien; dieser Record ist nicht mehr auf den früheren Composite-Subdiff begrenzt:

- Common-Runtime-API/Implementierung, EN/DE-Phasenvertragsdokumentation und C-Companion-Tests.
- Apache-Host-Qualifikationsharness und Tests einschließlich Response-Limit-Framing, kontrolliertem Neustart, Ressourcen- und Cleanup-Evidence.
- Envoy-Composite-/ext_proc-Produktcode, Common-Bridge, Coordinator-/Claim-/Cleanup-Tests, Receipt-Observer, echte Host-Qualifikationsharnesses und Tests sowie EN/DE-Dokumentation.
- HAProxy-HTX-/SPOP-Produktintegration, Qualifikationsharnesses und Tests einschließlich Origin-Dispatch-Zählung und begrenztem Receipt-Abgleich.
- lighttpd-Stock-Sidecar-Produkt/Tests und Stock-/Patched-Qualifikationsverträge/Tests. Der aktuelle Stock-Vertrag besteht 27 Tests und unterscheidet blockierte Voraussetzungen (77), Runtime- oder Cleanup-Fehler (1) und Aufruffehler (2); ein Qualifikationshostlauf wird nicht behauptet.
- Traefik-Native-Middleware und forwardAuth-Integration, Qualifikationsharnesses/Tests sowie EN/DE-Dokumentation.
- Connector-/Common-Workflows, Regressionstests, leserorientierte EN/DE-Dokumentation, dieses Change-Record-Paar und der EN/DE-Archivindex.

Nach der Branch-Integration dürfen NGINX-Änderungen aus aktuellem Master vorhanden sein; sie gehören nicht zur Reife-B-Qualifikation oder Runtime-Evidence dieses Records. Framework- und MRTS-Source liegen außerhalb des Schreibscopes dieses Nachfolgers.

## Ausgeführte Befehle

Die tatsächlich gewrappten Befehle und effektiven Inputs bleiben in den externen `execution.json`-Dateien und Runnern erhalten. Payload-Zusammenfassungen unten lassen externe Compiler-/Linkerpfade und Laufkonfiguration weg; sie sind keine impliziten Defaults.

~~~sh
rtk proxy go mod verify
rtk proxy go test -mod=readonly -count=1 ./cmd/msconnector-composite ./internal/processor ./internal/composite ./internal/compositeenvoy ./internal/compositetraefik
rtk proxy make -C connectors/envoy build-envoy-ext-proc
rtk proxy env CGO_ENABLED=1 go test -mod=readonly -tags libmodsecurity -count=1 -timeout=3m -json ./...
rtk proxy make -C connectors/envoy test-envoy-ext-proc
rtk proxy make -C connectors/envoy build-envoy-composite
rtk proxy make -C connectors/envoy runtime-smoke-envoy-ext-proc
rtk proxy sh connectors/envoy/harness/run_envoy_composite_matrix.sh
rtk proxy go test -mod=readonly -count=1 ./...
rtk proxy /usr/local/bin/python3.14 -B connectors/traefik/harness/test_composite_config.py
rtk proxy /usr/local/bin/python3.14 -B connectors/traefik/harness/test_composite_harness_paths.py
rtk proxy /bin/sh connectors/traefik/harness/run_traefik_composite_matrix.sh
~~~

Envoy-Go-Befehle liefen unter `connectors/envoy/ext_proc`; das zweite `go test ./...` lief unter `connectors/traefik/composite_middleware`. Normale Stufen endeten mit 0. Die Tagged-Suite hatte 344 benannte Passes und keine Skips. C17-Companion-Kompilierung mit `-Wall -Wextra -Werror -pedantic` und dessen Executable bestanden. Der Traefik-Harness lief je Fall; P4 Strict endete absichtlich mit 1 und `NON_PASS`. Der native Vorlagengenerator erstellte dieses Paar mit obigen Identitätswerten. Dokumentationsvalidierung steht im finalen Review-Abschnitt.

Spätere Nachfolgerprüfung bestand offline unter `p370finalregress.20261003a`: Der Envoy-ext_proc-Build kompilierte Common als striktes C17, verifizierte Go-Module und bestand alle acht mit libmodsecurity getaggten Packages; die vollständige Traefik-Native-Middleware-Prüfung `go test -mod=readonly -count=1 ./...` bestand. Der breite Python-Lauf bestand 368 Tests mit zwei erwarteten echten libmodsecurity-Stock-Skips, weil die SDK-Umgebung fehlte. Ein separater Stock-Lauf mit der exakten SDK-Umgebung bestand alle 52 Tests ohne Skips. Der Patched-Qualifikationsvertrag bestand 18 Tests; kein vertrauenswürdiger Qualifikationsexecutor war verfügbar. Ein historischer Stock-Qualifikationslauf bestand 21 Tests ohne Hostlauf. Der aktuelle Vertrag mit 27 Tests einschließlich der Exitcode-Unterscheidungen bestand am 2026-10-07 erneut innerhalb einer Qualifikationssuite mit 463 Tests. Dies sind lokale Prüfungen, keine gehosteten Nachfolger-CI- oder Sonar-Ergebnisse; historische lokale Ergebnisse belegen keine Abnahme der mit aktuellem Master integrierten Nachfolgerrevision.

## Security-Auswirkung

Limits schließen mit hostbestätigtem Status. Ungültige/abgelaufene Claims können keinen lebenden nativen Zustand übernehmen. Unaufgelöstes Cleanup verhindert weitere Aufnahme; konsumierte Fehler verwenden niemals freigegebene Pointer erneut. Unabhängige Belege verhindern falsche Folgeanfragebehauptungen. Linux-Peer-Credentials und eigentümerexklusive UDS-/Dateiprüfungen bleiben erforderlich. Authentifizierung, Tests, Warnungen, Quality Gate und Capability-Grenzen werden nicht abgeschwächt.

## Runtime-Evidence

Alle Roots liegen unter `/var/tmp/codex/ModSecurity-conector/runs/`.

| Lauf | Beobachtetes Ergebnis und Grenze |
| --- | --- |
| `p370efix.LLQmPm7g` | Erfolgreicher nativer Build, 344 Tagged-Passes, C17-Companion, direkter echter Envoy-Verkehr für allow/block/413/P3/Safe und Go-Composite-Matrix. `stage_status=0`, `cleanup_ok=true`, keine Cleanup-Probleme, unverändertes Source-Manifest. Frühere Versuche bleiben historisch. |
| `p370efu.Ggj72Jct` | Unabhängige begrenzte Request-/Response-Belege: deny403, dann allow200 im selben Dienstprozess; 19 Receipt-/Projection-Tests bestanden. Allow-Response-SHA256 `81f2257e4b0c2040e12b9116ac86279aead533c7a4357fba96dbece040a9288b`, Modus `0600`. Keine vollständige G5-/G6-Behauptung. |
| `p370t.T4wJJ8kA` | Echter Traefik: zehn `LIFECYCLE_ONLY`-Fälle (P1/P2 allow/deny, P2 oversize, P3 deny/redirect, P4 Safe, metadata omitted, P2-to-P3-Timeout). P4 Strict liefert 200 und erwartetes `NON_PASS`. `stage_status=0`, `cleanup_ok=true`, unverändertes Source-Manifest, keine Cleanup-Probleme und temporäre Testschlüssel entfernt. |

Beide Composite-Matrizen behalten `catalog_acceptance=false`; Strict wird nicht hochgestuft. Executable-/Bibliothekshashes, tatsächliche Mappings geladener libmodsecurity, begrenzte Ressourcenmessungen, effektive Konfigurationen und Upstream-Beobachtungen bleiben extern. Ressourcenüberwachung belegt die Laufbegrenzung, keine Parallelitäts-/Soak-Abnahme. Evidence gilt für Go `msconnector-composite`; beibehaltene Legacy-C-Status `implemented_not_asserted` / `configured_not_exercised` und Geschwisterprofile bleiben getrennt.

Die folgenden späteren Läufe erweitern ausgewählte Host-Evidence. Sie ändern Ergebnis oder Scope der obigen historischen Läufe nicht rückwirkend.

| Lauf | Beobachtetes Ergebnis und Grenze |
| --- | --- |
| `p370extprocqualbufferedcurrent.20261003a` | Envoy ext_proc PASS: drei Starts, verzögerte P2-/Body-Limit-Prüfungen, Response-Limit-Safe-Verhalten, Common-Abbruch/Recovery, Ausfall/Neustart, Vier-Client-Überlappung und verifiziertes Cleanup. `catalog_acceptance=false`; aggregierte G1-/G7-/G8-Abnahme bleibt extern. |
| `p370compositefinal.6BOXCIIW` | Envoy ext_authz und Traefik forwardAuth PASS: drei Starts, Timeout/Recovery, Keepalive, Vier-Client-Überlappung, P1-/P2-/Body-Limit-Origin-Ausschluss und Cleanup. Nur diagnostische Evidence. |
| `p370traefiknativequal4.PribNi` | Traefik native PASS: drei Starts, Origin-Ausschluss bei P1-/P2-/Keepalive-Deny und Abbruch, P3/P4 Safe, Recovery, Vier-Client-Überlappung, Ressourcen und Cleanup. Nur diagnostische Evidence. |
| `p370htxcampaigncurrent5.20261003a` | HAProxy HTX PASS: drei unterschiedliche Starts, Host-/Origin-Zählung, Vier-Client-Überlappung, Ressourcenmessungen, exakte Input-Pins und kontrolliertes Stop/Reap/Cleanup. Aggregiertes G1, vollständigeres G4, G7 und G8 bleiben offen. |
| `p370apachequalfinal3.20261003a/qualification-parent/campaign-06` | Apache PASS: 35 Fälle, keine fehlgeschlagenen Probes, drei Starts plus kontrollierter Neustart unter echter Nonroot-Identität, Vier-Client-Überlappung, Ressourcen- und Cleanup-Evidence. Response-Limit-Framing bestand den beobachteten BEFORE-Zweig. Late-Commit Safe/Strict, Engine-Fehlerinjektion und vollständige Security-/Fehlermatrix bleiben offen; `full_b_acceptance=false`. |
| `p370spopcampaigncurrent6.20261003a` | HAProxy SPOP liefert absichtlich Exit 77 / `BLOCKED`: drei unterschiedliche Starts; der erste Start besteht 44 Probes und G2–G7-/G9-Voraussetzungen, folgende Starts bestehen Allow/P1/P2. Phasen-/Limitgrenzen, fehlerhafter/abgeschnittener Verkehr, Abbruch, Agent-Neustart, Keepalive, Überlappung, Ressourcen und Cleanup sind beobachtet. Unabhängige G1-/G8-Abnahme bleibt blockiert. |

Die früheren HTX- und SPOP-Fehlläufe bleiben als Fehlläufe erhalten; erfolgreiche spätere Läufe deklarieren sie nicht um. NGINX-Runtime-Evidence wird nicht angerechnet.

## Bekannte Einschränkungen

Vollständige G1–G9-Abnahme der neun Nicht-NGINX-Profile bleibt offen. Die ausgewählten späteren Läufe belegen wiederholte Starts, bestimmte Phasen-/Limitgrenzen, Recovery, Keepalive/Parallelität und RSS-/FD-Beobachtungen nur innerhalb ihrer dokumentierten Hostprofile. Stock-lighttpd benötigt eine unabhängige Operator-Attestierung; G1/G4/G8 bleiben blockiert und kein Qualifikationshostlauf ist erfolgt. Patched-lighttpd benötigt den vertrauenswürdigen Namespace-/noexec-Ausführungspfad sowie unabhängige Provenance und einen Qualifikationsexecutor; lokales Namespace-Setup scheiterte mit `uid_map` EPERM und ein gewöhnlicher bwrap-Lauf liefert keine gleichwertige Evidence. Die 27 Tests des Stock-Vertrags und die 18 Tests des Patched-Vertrags belegen weder Host-Runtime-Abnahme noch B. NGINX ist vom Benutzer ausgeschlossen. Die Evidence bestätigt weder vollständigen Katalog, CRS, HTTP/2/HTTP/3, strikten Post-Commit-Reset, Produktionsreife noch Nutztraffic-Freigabe.

## Verbleibende Risiken

Bereits laufende native Aufrufe können nicht in-place abgebrochen werden; unaufgelöstes Cleanup erfordert kontrollierten Prozessneustart. Ein Nachfolger-Delivery-Commit benötigt frische integrierte Prüfungen und gehosteten CI-/Sonar-Readback. Baseline-Sonar bestätigt weder Nachfolgerduplikation noch dessen Quality-Gate-Status. Aktueller Master delegiert Response-Inspection-Limits an libModSecurity; historische Apache- und ext_proc-Response-Limit-Läufe dürfen dem integrierten Nachfolger erst nach Anpassung und Wiederholung ihrer engine-eigenen Verträge angerechnet werden.

TAC-Advisory-Readback ist auf `tac1` freigegeben; dieser Zugang ersetzt weder Host-Runtime-Evidence noch fehlende lighttpd-Voraussetzungen oder Nachfolger-Sonar. Nachfolgerduplikation auf neuem Code mit exakt 0.0% steht noch aus; Reife B oder Master-Reife werden nicht behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

Die vollständige G1–G9-Kampagne der neun Profile ist durch diese ausgewählten Läufe nicht bestätigt. Produktionsverkehr, universelle Protokoll-/CRS-Abdeckung und unabhängige Strict-Host-Reset-Evidence wurden innerhalb dieser Korrektur nicht ausgeführt. Merge, direkter Master-Push, Deployment oder neue NGINX-Runtime-Arbeit werden nicht vorgenommen. Framework-/MRTS-Source bleibt unverändert.

## Finaler Diff- und Review-Status

Das frühere fokussierte Code- und Security-Review fand nach Cleanup- und Entry-Ownership-Korrekturen keinen verbleibenden Blocker in seinem Composite-/Common-Subdiff. Diese Aussage gibt nicht den gesamten aktuellen Nachfolger frei und schließt dessen Runtime-/Delivery-Voraussetzungen nicht. Bei diesem Review bestanden `rtk proxy make check-bilingual-docs check-doc-links`, `rtk proxy python3 ci/tools/new-change-record.py check`, `rtk proxy python3 -m unittest -v tests.test_change_record` (20 Tests) und `rtk proxy git diff --check`. Manueller Review des eigenen Diffs und EN/DE-Review bestätigten übereinstimmende technische Werte und Evidence-Grenzen. Eine anfängliche zusätzliche Testmodulauswahl scheiterte, weil dieses Modul nicht existiert; anschließend bestand die dokumentierte Archivsuite. Der verbreiterte aktuelle Nachfolger benötigt weiterhin finalen integrierten Review, vollständige angeforderte Abnahme und gehostete Prüfungen seiner veröffentlichten Revision. Merge oder Nachfolger-Sonar-Ergebnis werden nicht behauptet.
