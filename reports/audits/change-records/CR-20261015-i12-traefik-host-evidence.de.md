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

Alle Shellbefehle liefen über RTK. Frische modulweise rtk proxy /usr/local/go/bin/go test -count=1 ./..., test -count=1 -race ./... und vet ./... bestehen für drei Traefik-Module. rtk proxy make -C connectors/traefik test-engine-service besteht nach begrenzter Testkorrektur; natives Protokoll/Self-Test,64nichtlesende Peers/Deadline/Folgerequest/Socketersetzung wurden tatsächlich ausgeführt. RTK-gewrappte Parent-Unittests und make check-common-security-contract bestehen; anfängliche Pfad-/Setupfehler bleiben erhalten. Zentrale Capture-Prüfung und15Guards sowie31Ledger-/Oracle-/Berichtsregressionen bestehen. Exakte argv/CWD/Exits/Ausgabe-SHA256 liegen extern unter i12-traefik-20261015/verification. Abschließende fokussierte I12-Tests:23PASS. Sprachparität und lokale Links bestehen mit dem unveränderten Framework als temporärem Read-only-Mount im privaten Namespace; der Change-Record-Check besteht. Separate terminale Belege: i12-final-unit-tests-v2, final-docs-publication und change-record-publication.

## Security-Auswirkung

Kein Enforcement-Control, Hostlimit, Warning, Authentifizierungs-/Peercheck oder Gate wird abgeschwächt. Kandidatencode läuft ohne Root/Capabilities in unabhängig geprüften Namespaces mit versiegelten Bindings. Synthetische MSE1-/MRC1-Fehler und Same-UID-Peers bleiben explizite Testeingaben. Vollständiges Sample/Hostablehnung, native Entscheidung und technischer Fehler bleiben getrennt. Native Strict wird vom aktuellen Profil abgelehnt; nicht unterstütztes Verhalten wird nicht positiv behauptet.

## Runtime-Evidence

Externe Wurzel /var/tmp/codex/ModSecurity-conector/runs/i12-traefik-20261015 erhält physische Logs, rohe synthetische Client-/Backendbytes, geladene Image-Mappings, Quell-/Konfigurationshashes, Prozess-/FD-/UDS-Beobachtungen und Cleanup. Drei korrigierte native Matrizen21Austausche, getrennte Request14-/Companion14-Austausche und Autorisierungskapazität3 ergeben52aktuelle gemessene Austausche; ältere Fehl-/Teilversuche bleiben getrennt. Root-geprüfte35-Felder-Pakete qualifizieren Native NEED-request-streaming, Request allow_without_marker und Companion phase4_rule_observed. Dieselbe Companion-P4-Transaktion FAILT phase4_deny_after_commit_log_only_safe wegen late_intervention=false und fehlendem Modus. Connectorfreies direktes SDK-Streaming-Oracle begründet die eine neue Originalerwartung unabhängig.

## Bekannte Einschränkungen

I12 ist nicht vollständig geschlossen:6qualifiziertePASS,1qualifizierterFAIL,273unqualifizierte Pflicht-IDs und120ungelöste Original-Oracles bleiben routenweise ausdrücklich erhalten. Native Strict ist laut Quelle/Profil und realer Startablehnung nicht unterstützt. Historische Allow-/Client-cancel-/EOS-Evidence bleibt erhalten. Charset-Fixtures verwenden ASCII und belegen keine Nicht-ASCII-Umkodierung. Native Autorisierungsereignisse nennen GET beim ursprünglichen POST-Client. Unbekannte gültige64hex-Korrelationshandles, H2/H3, ursprüngliche dateibasierte Fälle und ungeprüfte Sinkfehlerpflichten bleiben unqualifiziert.

## Verbleibende Risiken

Unabhängig bestätigter Companion-Telemetriefehler: physisch vollständiger Late-Intervention-Event besitzt falsches Late-Flag und keinen Modus trotz committed Deny-zu-LogOnly. Zwei unabhängige Hostläufe reproduzieren ihn; Quellenprüfung schließt Capture-Eingriff aus. Kein Enforcement-Fehler nachgewiesen. Producer-/Quittungs-/Quellkette an Produkt-PR382 übergeben; kein Produktionsfix in diesem Evidenzbranch. Ursprüngliche Strict-/v4-Namespace-Cleanupfehler bleiben Fehler trotz späterer exakter PID-Abwesenheit. Neueste erfolgreiche Controller haben keine Überlebenden/Mount-Leaks und finale native Mappings0.

## Nicht ausgeführte Prüfungen mit Begründung

Keine breite All-Connector-Matrix, Framework-/MRTS-Ausführung, H2/H3-Prüfung, zusätzlicher Deep-Security-Scan, Produktreparatur, Merge oder Deployment: außerhalb dieser Traefik-Evidence-Aufgabe. Zwei optionale Legacy-Hostloadertests haben kein TRAEFIK_BIN im portablen Contract-Aufruf; getrennte echte Host-Namespace-Tests laden tatsächliche private Plugins. Gehostete Checks/Reviews/Quality Gate gelten erst nach Veröffentlichung und werden nicht von PR410 übernommen.

## Finaler Diff- und Review-Status

Begrenzte lokale Gegenprüfung umfasst unabhängigen Ledger-Tamper-Audit und unabhängige Quell-/physische Logvalidierung des Companion-Fehlers. Root erhält Ursprungsstatus/Historie und prüft neue Pakete unabhängig gegen alle35Messrollen. Ausschließlich explizite aufgabeneigene Dateien werden gestaged. Draft-Übergabe und Hosted-Checks des exakten Heads werden erst nach tatsächlicher Veröffentlichung dokumentiert; kein Force-Push, Merge oder master-Wechsel autorisiert.
