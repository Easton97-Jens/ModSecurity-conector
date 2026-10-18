# Change Record: CR-20261015-lighttpd-terminal-delivery-eos

**Sprache:** [English](CR-20261015-lighttpd-terminal-delivery-eos.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-lighttpd-terminal-delivery-eos |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `9980eb049dde0643da6a4f04e3b6712801b670b3` |

## Motivation und Problemstellung

Unabhängige I12-Hostaufzeichnungen zeigten vier lighttpd-Lifecyclefehler: Reset setzte nach einer angewandten terminalen P3-Aktion eine Bodyphase fort; einer echten leeren Upstreamantwort fehlte natives EOS; der Responsehook verwarf eine bereits ausgewählte technische 500; und Stock/Bodymodus=none meldete vor dem Logging die tatsächliche Auslieferung nicht.

## Akzeptanzkriterien

Terminale Entscheidungen und erste Ursache erhalten; eine bestätigte technische Antwort ohne erneuten Engineaufruf ausliefern; tatsächlichen Header-/Bodycommit des Hosts melden; CL0-EOS einmal an der echten Headerfinalisierung liefern. Unvollständige positive Content-Length behält fehlendes EOS. Cleanup bleibt einmalig, native Limits bleiben Eigentum der Engine.

## Implementierungsentscheidung und Begründung

Drei Resetguards verwenden die vorhandene terminale Markierung host_response_attempted. Das neue failure_response_selected wird erst nach erfolgreicher Auswahl und Bestätigung der Hostfehlerantwort gesetzt, auch bei zuvor gesetztem api_failed. Reset synchronisiert echte write_queue.bytes_out/resp_header_len über die geprüfte Common-API nur nach regulärer P3-Verarbeitung. Der gepatchte Core schließt die Entitybrücke bei tatsächlicher CL0-Finalisierung; Reset erfindet kein EOS.

## Geänderte Dateien

connectors/lighttpd/module/mod_msconnector.c; der lighttpd-Streamhookpatch; neue kompilierte test_terminal_response_reset.py, test_empty_response_eos.py und test_tech_delivery_commit.py; vorhandene I09/I10-Fixtures sowie zwei veraltete Quellvertragsassertionen. Die P2-Assertion prüft die vorhandene native Limitzuständigkeit statt eines veralteten Connector-Bytelimitliterals. Dieser Record ist die zweisprachige Verhaltensdokumentation.

## Ausgeführte Befehle

Alle Befehle verwenden RTK. Kompilierte terminale Resetkontrollen: 2 PASS, Guardentfernungsmutationen scheitern für Stock- und Patched-ABI. CL0-Coreregression: Baseline scheitert mit EOS0; korrigierter Test PASS einschließlich Callbackfehler und unvollständiger positiver Länge. Technische Delivery-/Commitkontrollen: 4 PASS, vier gezielte Mutationen scheitern. Finale I10-Adapterfehlersuite: 8 PASS. Ausgewählte Patched-/P2-Quellverträge: 51 Tests, 49 PASS, 2 Namespace-Skips. Der erste breitere Lauf mit 206 Tests enthält zwei später korrigierte veraltete Assertions; der finale breite Lauf besteht mit 212 Tests (199 PASS, 12 Namespace-Skips, 1 SDK-Loopback-Klassenskip ohne ausgewählte SDK-Umgebung). Die explizite SDK3.0.14-Stock-Sidecar-Suite besteht45 Tests (44 PASS, 1 Sandbox-Skip für eine getrennte UID).

## Security-Auswirkung

Keine Namespace-, UID-, Quellvertrauens-, Berechtigungs-, Warnungs- oder Gategrenze wird gelockert. Eine Fehlerantwort überspringt den erneuten Engineaufruf erst nach ausdrücklich erfolgreicher Fehlerauswahl. Fehlende Bestätigung liefert weiterhin HANDLER_ERROR. Ein gescheitertes geprüftes Commitupdate stoppt die Finalisierung, erhält die erste Ursache und räumt einmal auf.

## Runtime-Evidence

Run i12-lighttpd-412-completion-20261015 erhält ursprüngliche Fehleraufzeichnungen und getrennte Korrekturen. Der vorläufige echte Nonroot-Patched-CL0-Lauf1792078514962046469 beobachtet EOS1, append0, P4/Logging/Finish/Free einmal und gesunde Nachbarn; kurze Content-Length behält EOS0 und abnormalen Clientexit. Dieser vorläufige Lauf liegt vor der final integrierten Produktidentität und ergänzt keine finale Qualifikation. Der gepinnte lighttpd1.4.85-Corebuild besteht; der neue Hunk wird ohne Fuzz angewendet. Drei bereits vorhandene Fuzzanforderungen des Patches bleiben unverändert.

## Bekannte Einschränkungen

Kompilierte Callbacktests verwenden begrenzte Hostseams; sie sind Regressionsbelege und keine vollständigen Host-Lifecycle-PASS. Hostwiederholungen und erforderliche CI/Sonar am aktuellen Head stehen nach Integration über #410 nach #412 aus. Stock-native bleibt eine Diagnoseroute ohne native Entityhooks; Patched Strict-Clientabort bleibt nicht unterstützt.

## Verbleibende Risiken

Die tatsächlichen Ausgabecounter müssen an der Hostresetgrenze gültig bleiben. Die neuen Tests decken Headercommit, Bodycommit, gescheiterte geprüfte Synchronisierung, Auslieferung bei API-Fehler und fehlgeschlagene Bestätigung der Fehleraktion ab. Finale Hostwiederholungen müssen die integrierten Binaries bestätigen.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Masterintegration, Veröffentlichung, Bereitstellung, Framework/MRTS- oder andere Connector-Matrix. Unprivilegierte Namespacetests werden in der eingeschränkten Shell übersprungen; separat autorisierte kontrollierte echte Nonroot-Hostläufe erhalten den ursprünglichen Isolationsvertrag. Der historische Gitleaks-Blocker von #382 bleibt ein unabhängiger Releaseblocker.

## Finaler Diff- und Review-Status

Root prüfte den minimalen Produktdiff und die gezielten Regressionen. Normale Commits im bestehenden #382 und normale Integration #382→#410→#412 sind autorisiert; keine Historienumschreibung oder Masterintegration. Finale leserorientierte Qualifikation und abrufbare Rohbelege gehören zum bestehenden Folgeauftrag #412.
