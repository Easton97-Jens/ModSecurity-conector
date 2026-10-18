## Change Record: CR-20261015-i12-traefik-host-evidence — Fortschreibung vom 18. Oktober 2026

**Sprache:** [English](CR-20261015-i12-traefik-host-evidence.md) | Deutsch

## Aktuelle Fortschreibung — 18. Oktober 2026

Der aktuelle [Traefik-Evidence-Bericht](../../../docs/i12-traefik-evidence-20261015.de.md) und sein englischer Partner beginnen jetzt mit der Fortsetzung vom 18. Oktober. Die vollständigen Berichte/Anhänge vom 15. Oktober und dieser ursprüngliche Change Record bleiben unter historischen Überschriften wortgetreu erhalten. Ursprüngliche Change-ID/Datum/Basis bleiben historische Identität.

Die aktuelle Qualifikation bleibt **6 historische Lifecycle-PASS,1 historischer qualifizierter FAIL,273 unqualifizierte Pflicht-IDs**; Root hat keine Runtime-Promotions vorgenommen. Quellreview löst 56/124 Originalerwartungen auf: Native 30/55, Request 15/39, Companion 11/30; offen 25/24/19 ergeben 68. Die aktuelle Abstimmung liegt unter `R18/root-source52-reconciliation-20261018`, mit `R18=/var/tmp/codex/ModSecurity-conector/runs/i12-traefik-acceptance-20261015`. Quellreview und Lifecycle-Qualifikation bleiben getrennt.

Die Produktkorrekturen für Telemetrie/Originalmethode kommen jetzt über #382 → #410 (`f8ce4c1342e29a20070029738663f86716488ccf`) → #413-Revision `782f31ed78353b59a0dcd63978638ae5b107f8cf`; korrigierte Telemetriebeobachtungen löschen den historischen FAIL nicht. `root-sdk-review-20261018-v3` ersetzt ausschließlich zehn unbegründete native P2-Backend0-Erwartungen, bei weiterhin verpflichtender unabhängiger Backendmessung und unveränderten benannten Auth-Ausschlusspflichten. V2-/Originaldatensätze bleiben unveränderlich.

Die Berichte trennen ältere versiegelte Native-v4-/v5-/v7- und Auth-v12-Quellen/Deltas von der veröffentlichten 782f-Revision. Native v4 enthält 118 Versuchszeilen; Auth v12 enthält 93+69 Original-IDs/179 physische Verzeichnisse mit zwei Companion-Producer-Timeouts. Native v5 schloss ausgewählte 41 IDs/54 Ausführungen mit Exit0/timeoutfalse ab;12 SDK-Kontrollen vor Hoststart bestehen, Sink-Erwartungen entsprechen physischen Belegen, vollständiger Root-Review bleibt offen. Native v7 hat zwei Producerfehler, keine Short-write-/EAGAIN-/Resume-Belege und keine Produktfehlerbehauptung. Root-Prüfung der35-Felder-Pakete, kanonische Fixture-Varianten und ursprüngliche File-/API-Pflichten bleiben offen.

TLS-Quelle31 Kontrollen und42 Dokumentationsprüfungen bestehen. Tatsächlicher 782f-Hostversuch1792321692553561516 endete mit Controller0/timeoutfalse,15 Client-Exits0 und Observer-Abbruch Exit1/null Bytes; Allokation/Logging/Free jeweils15, finale Pending-/Live-Mappings0 sowie Socket-/Prozess-Cleanup sind beobachtet. Tatsächliche HTTPS-/CA-/Hostnamenprüfung und 32768-/32769-Kapazitätspfade sind geprüft; kein16-Fall-All-PASS oder Lifecycle-Aufstieg wird behauptet. `maxResponseBodySize=32768` bleibt Authorization-Response-Kapazität; private Schlüssel bleiben aus öffentlichen Artefakten/Manifesten ausgeschlossen. Exakter782f-Sonar-GateOK/SecurityA ist von fünf offenen Strict-zero-S1192-Befunden getrennt. Die lokale Korrektur besteht31 vorhandene TLS-/Auth-Kontrollen; die gehostete Auflösung am nächsten veröffentlichten Head bleibt offen. Aufbewahrter Hosted-Readback:28Checks,1Sonar erfolgreich,2übersprungen,25offen. Dauerhafte Veröffentlichung bleibt offen; kein All-green oder vollständiger Abschluss.

Diese begrenzte Fortschreibung ändert ausschließlich das Evidence-Berichtspaar und dieses Change-Record-Paar. Die Validierung verwendet bestehende EN-/DE-Struktur-, Change-Record- und Diffprüfungen; keine neuen Tests nur für Prosa, Hoststarts, Git-Delivery, Produktänderung oder zusätzliche tiefe Sicherheitsprüfung gehören dazu. Die unten erhaltenen historischen Befehle/Ergebnisse behaupten keine frische Ausführung am neuesten Head.

## Historischer Change Record — 15. Oktober 2026, wortgetreu erhalten


# Change Record: CR-20261015-i12-traefik-host-evidence

**Sprache:** [English](CR-20261015-i12-traefik-host-evidence.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-traefik-host-evidence |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation und Problemstellung

Getrennte Native-/UDS-, forwardAuth-Request- und Response-Companion-I12-Nachweise vom PR410-Head f27eb59b erweitern. Alle280 ursprünglichen Pflicht-IDs und124 ursprünglichen offenen Erwartungen erhalten; funktionalen Smoke nicht als vollständige Qualifikation behandeln.

## Akzeptanzkriterien

Isolierte Quell-/Konfigurations-/Laufidentitäten, echte Host-/Client-/Backend-/Native-/EOS-/Finish-/Free-/Cleanup-Belege und ursprüngliche Oracles erhalten. Go/Race/Vet-, UDS-/Observer-/Security-Contract-Prüfungen ausführen. EN/DE-Evidence mit ausdrücklich offenen IDs sowie Draft-PR gegen work/pr382-i12-host-evidence-20261011 liefern. Vollständige I12-Abnahme bleibt partiell:6PASS/1FAIL/273unqualifiziert; von124 Originalerwartungen sind4aufgelöst/120ungelöst.

## Implementierungsentscheidung und Begründung

Die vorhandenen zentralen Varianten traefik-native und traefik-forwardauth unverändert verwenden. Ausschließlich Traefik-spezifische versiegelte Quellkopie-Producer, strenge Client-Framing-Prüfung, explizite synthetische Fehlerfixtures und separates Ledger mit vorhandenen Validatoren ergänzen. Gesamtes Originalinventar pinnen, damit keine bisherigen PASS/Oracle-Auflösungen injiziert werden. Nichtphysische, Symlink-, Checkout- und externe Fremdziele für native Ausgaben vor Schreibzugriffen ablehnen; frische Followup-Ziele prüfen. Leere Host-Captures und TCP-EOF-Ersatz ablehnen. Commonfinish2 idempotent getrennt von einmaliger nativer Finalisierung/Freigabe erhalten. maxResponseBodySize=32768 bleibt Autorisierungsresponse-Kapazität.

## Geänderte Dateien

connectors/traefik/harness/i12/native/ und i12_auth/: Hostproducer, Clients/Backends, Fehlerpeers, Reviewer, Paketvorschläge und EN/DE-READMEs. connectors/traefik/harness/i12_ledger.py plus fixtures/i12_original_inventory.json: separates Traefik-Ledger/Eingabe. Drei tests/test_traefik_i12_*-Module: Evidence-Integritätskontrollen. connectors/traefik/build/test-engine-service-runtime.sh: sofortigen BrokenPipe/Reset bei absichtlich gesättigter Workerzulassung behandeln. docs/i12-traefik-evidence-20261015.md und .de.md sowie dieses Change-Record-Paar. Produktquellen, Common, zentrale I12-Matrix/gemeinsame Generatoren, Abhängigkeiten und Framework/MRTS/Gitlinks bleiben unverändert.

## Ausgeführte Befehle

Alle Shellbefehle liefen über RTK. Frische modulweise rtk proxy /usr/local/go/bin/go test -count=1 ./..., test -count=1 -race ./... und vet ./... bestehen für drei Traefik-Module. rtk proxy make -C connectors/traefik test-engine-service besteht nach begrenzter Testkorrektur; natives Protokoll/Self-Test,64nichtlesende Peers/Deadline/Folgerequest/Socketersetzung wurden tatsächlich ausgeführt. RTK-gewrappte Parent-Unittests und make check-common-security-contract bestehen; anfängliche Pfad-/Setupfehler bleiben erhalten. Zentrale Capture-Prüfung und15Guards sowie31Ledger-/Oracle-/Berichtsregressionen bestehen. Exakte argv/CWD/Exits/Ausgabe-SHA256 liegen extern unter i12-traefik-20261015/verification. Abschließende fokussierte I12-Tests:23PASS. Sprachparität und lokale Links bestehen mit dem unveränderten Framework als temporärem Read-only-Mount im privaten Namespace; der Change-Record-Check besteht. Separate terminale Belege: i12-final-unit-tests-v3, final-docs-publication und change-record-publication.

## Security-Auswirkung

Kein Enforcement-Control, Hostlimit, Warning, Authentifizierungs-/Peercheck oder Gate wird abgeschwächt. Kandidatencode läuft ohne Root/Capabilities in unabhängig geprüften Namespaces mit versiegelten Bindings. Synthetische MSE1-/MRC1-Fehler und Same-UID-Peers bleiben explizite Testeingaben. Vollständiges Sample/Hostablehnung, native Entscheidung und technischer Fehler bleiben getrennt. Native Strict wird vom aktuellen Profil abgelehnt; nicht unterstütztes Verhalten wird nicht positiv behauptet.

## Runtime-Evidence

Externe Wurzel /var/tmp/codex/ModSecurity-conector/runs/i12-traefik-20261015 erhält physische Logs, rohe synthetische Client-/Backendbytes, geladene Image-Mappings, Quell-/Konfigurationshashes, Prozess-/FD-/UDS-Beobachtungen und Cleanup. Drei korrigierte native Matrizen21Austausche, getrennte Request14-/Companion14-Austausche und Autorisierungskapazität3 ergeben52aktuelle gemessene Austausche; ältere Fehl-/Teilversuche bleiben getrennt. Root-geprüfte35-Felder-Pakete qualifizieren Native NEED-request-streaming, Request allow_without_marker und Companion phase4_rule_observed. Dieselbe Companion-P4-Transaktion FAILT phase4_deny_after_commit_log_only_safe wegen late_intervention=false und fehlendem Modus. Connectorfreies direktes SDK-Streaming-Oracle begründet die eine neue Originalerwartung unabhängig.

## Bekannte Einschränkungen

I12 ist nicht vollständig geschlossen:6qualifiziertePASS,1qualifizierterFAIL,273unqualifizierte Pflicht-IDs und120ungelöste Original-Oracles bleiben routenweise ausdrücklich erhalten. Native Strict ist laut Quelle/Profil und realer Startablehnung nicht unterstützt. Historische Allow-/Client-cancel-/EOS-Evidence bleibt erhalten. Charset-Fixtures verwenden ASCII und belegen keine Nicht-ASCII-Umkodierung. Native Autorisierungsereignisse nennen GET beim ursprünglichen POST-Client. Unbekannte gültige64hex-Korrelationshandles, H2/H3, ursprüngliche dateibasierte Fälle und ungeprüfte Sinkfehlerpflichten bleiben unqualifiziert.

## Verbleibende Risiken

Unabhängig bestätigter Companion-Telemetriefehler: physisch vollständiger Late-Intervention-Event besitzt falsches Late-Flag und keinen Modus trotz committed Deny-zu-LogOnly. Zwei unabhängige Hostläufe reproduzieren ihn; Quellenprüfung schließt Capture-Eingriff aus. Kein Enforcement-Fehler nachgewiesen. Die Producer-/Quittungs-/Quellkette ist [an Produkt-PR382 übergeben](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194758198); kein Produktionsfix in diesem Evidenzbranch. Ursprüngliche Strict-/v4-Namespace-Cleanupfehler bleiben Fehler trotz späterer exakter PID-Abwesenheit. Neueste erfolgreiche Controller haben keine Überlebenden/Mount-Leaks und finale native Mappings0.

## Nicht ausgeführte Prüfungen mit Begründung

Keine breite All-Connector-Matrix, Framework-/MRTS-Ausführung, H2/H3-Prüfung, zusätzlicher Deep-Security-Scan, Produktreparatur, Merge oder Deployment: außerhalb dieser Traefik-Evidence-Aufgabe. Zwei optionale Legacy-Hostloadertests haben kein TRAEFIK_BIN im portablen Contract-Aufruf; getrennte echte Host-Namespace-Tests laden tatsächliche private Plugins. Gehostete Checks/Reviews/Quality Gate gelten erst nach Veröffentlichung und werden nicht von PR410 übernommen.

## Finaler Diff- und Review-Status

Begrenzte lokale Gegenprüfung umfasst unabhängigen Ledger-Tamper-Audit und unabhängige Quell-/physische Logvalidierung des Companion-Fehlers. Root erhält Ursprungsstatus/Historie und prüft neue Pakete unabhängig gegen alle35Messrollen. Ausschließlich explizite aufgabeneigene Dateien werden gestaged. Draft #413 ist gegen die gewünschte Base veröffentlicht; Sonar am ersten Head scheitert mit Security-Rating E/A und15Meldungen, unabhängig ohne validierte erreichbare Schwachstelle unter dem versiegelten Controller triagiert; keine Remote-Status-/Gate-Änderung. Spätere aktuelle Head-Checks stehen in externen Delivery-Belegen; kein Force-Push, Merge oder master-Wechsel autorisiert.
