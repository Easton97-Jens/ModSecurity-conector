# Change Record: CR-20261015-i12-nginx-native-evidence

**Sprache:** [English](CR-20261015-i12-nginx-native-evidence.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-nginx-native-evidence |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |
| Neueste integrierte PR-#410-Revision | `61e45cf6dd211f21835709a014fe6884d4bcda62` |

## Motivation und Problemstellung

NGINX-spezifische I12-Nachweise aus PR #410 erhalten und ergänzen; ursprüngliche Hostausführung, Fixturefehler, Oracle-Konflikte und vollständig qualifizierte Lifecycle-Ergebnisse getrennt halten.

## Akzeptanzkriterien

Exakt 140 ursprüngliche ausgewählte IDs, unveränderte ausgewählte Verträge und historische Revisionen; unabhängige physische Belege je ID; kein PASS aus Aliasen, Kandidaten oder ungelösten Oracles. Neue Nachweise und verbleibende Lücken sind in beiden Sprachen zu berichten.

## Implementierungsentscheidung und Begründung

NGINX-spezifische Capture-/Harness- und Ledger-/Berichtsgeneratoren ergänzen Nachweise ohne Änderungen an gemeinsamer Source-Capture-Infrastruktur, gemeinsamem Oracle-Generator, zentraler Matrix oder produktivem Connectorcode. Der Adapter für die aktuellen Quellen exportiert den exakten Git-Baum, prüft sein vollständiges Inventar und rekonstruiert nur die gepinnten historischen NGINX-Observerquellen mit einer unveränderten privaten Kopie des gemeinsamen Registry. Historisches Staging ist als nicht aktuell markiert und kann keine Laufzeitnachweise qualifizieren. Der Bericht prüft die unveränderliche Basis-SHA256 und Originalzeilen; Kandidatenbeobachtungen können keinen Lifecycle freigeben.

## Geänderte Dateien

- `ci/runtime/lifecycle/i12/nginx/build_capture.py`
- `ci/runtime/lifecycle/i12/nginx/config_controls.py`
- `ci/runtime/lifecycle/i12/nginx/host_state.h`
- `ci/runtime/lifecycle/i12/nginx/invalid_return.c`
- `ci/runtime/lifecycle/i12/nginx/ledger.py`
- `ci/runtime/lifecycle/i12/nginx/qualify.py`
- `ci/runtime/lifecycle/i12/nginx/report.py`
- `ci/runtime/lifecycle/i12/nginx/review_observations.py`
- `ci/runtime/lifecycle/i12/nginx/run_cases.py`
- `ci/runtime/lifecycle/i12/nginx/scenarios.py`
- `ci/runtime/lifecycle/i12/nginx/wire_client.py`
- `tests/test_nginx_native_cleanup_bridge.py`
- `tests/test_i12_nginx_invalid_return.py`
- `tests/test_i12_nginx_ledger.py`
- `tests/test_i12_nginx_qualify.py`
- `tests/test_i12_nginx_security_boundaries.py`
- `tests/test_i12_nginx_wire_client.py`

Neuer Bericht: [Deutsch](../../../docs/pr-410-i12-nginx-evidence-20261015.de.md); das englische Pendant ist über dessen Sprachumschalter erreichbar. Kompaktes Maschinenartefakt: `ci/runtime/lifecycle/i12/nginx/evidence-20261015.json`. Dieses Change-Record-Paar.

## Ausgeführte Befehle

`rtk proxy python3 ci/tools/new-change-record.py create --name i12-nginx-native-evidence --base-revision f27eb59b53beff6f65384fc2e5037881a3052c01 --date 2026-10-15`: Vorlagenpaar erstellt. RTK-vermittelte Berichts-AST- und Basis-/Negativprüfungen bestanden: 140 eindeutige IDs, Basis-Lifecycle-PASS 1, verbleibende ursprünglich offene Oracles 42; verändertes Original-Oracle und doppelte ID abgewiesen. Build-/Native-/Adoption-/Security-/Mutationsbefehle und tatsächliche Exit-Ergebnisse stehen im generierten Bericht und seinen hashgebundenen Verifikationseingaben; anfängliche fehlgeschlagene Setups bleiben erhalten.

## Security-Auswirkung

Produktivcode und Sicherheitskontrollen sind unverändert. Hostidentität, physische Clientbytes, native Beobachtungen und Cleanup werden an ihren jeweiligen Grenzen geprüft. Bestehender Release-Secret-Blocker bleibt ungelöst; keine Releasefreigabe wird impliziert.

## Runtime-Evidence

Externer Run-Root: `/var/tmp/codex/ModSecurity-conector/runs/i12-nginx-410-20261015`. Generierter Bericht und kompaktes Ledger binden jede übergebene Ledger-/Beobachtungs-/Verifikationseingabe durch SHA256. Ursprüngliche 42 native und 14 kanonische Ausführungen behalten ihre Originalrevisionen; 31 abgeleitete Zeilen und wiederverwendete YAML sind keine zusätzlichen Requests. Historische 60-Fall-Batches behalten zwei Konfigurationsfehler und ein veraltetes Oracle unabhängig.

Das finale Ledger enthält exakt 140 ursprüngliche IDs: 71 vollständige Lifecycle-Qualifikationen (67 PASS, vier FAIL), 69 ohne vollständige Qualifikation sowie zehn historische Config-PASS auf ihrer eigenen Nachweisebene. Es gibt 70 neu qualifizierte ursprüngliche IDs und einen erneuten Test. Von 43 ursprünglich offenen Oracle-Erwartungen war eine an der Basis aufgelöst und 33 sind neu aufgelöst; neun bleiben offen. Alle 93 neuen Hostfälle behalten direkte Client-PID-/Wait-Bindung, echte Root-Master-/Nobody-Worker-Identität und verifiziertes Cleanup; Kandidatenabdeckung allein qualifiziert nicht alle 93 Fälle.

Die vier qualifizierten FAIL-Ergebnisse sind der ursprüngliche P2-/beobachtete P1-Konflikt der Body-Null-Fixture, der separat bestätigte Produktfehler für leere Requests und beide Timeoutfälle mit fehlenden ursprünglichen Eventmetadaten `run_id`/`transport_case_id`/`connection_id`. Korrekturen erhalten die ursprünglichen verpflichtenden Eventfelder; `phase4_body_reject` besteht mit diesen Feldern. Request-ProcessPartial erfasst native Append-Rückgaben 0/0 und native Process-Request-Body-Rückgabe 1.

Die Berichtsgenerierung verwendete `rtk proxy python3 ci/runtime/lifecycle/i12/nginx/report.py` mit `ledger/nginx-140-final.json`, `review-suite04-v2/candidate-summary.json`, `final-provenance.json`, `verification-native/verification-summary.json` und `sdk-mime/receipt.json` aus diesem Run-Root. Exit 0 erzeugte Maschinenartefakt und beide Sprachberichte. Der Generator bricht ab, wenn die geprüfte Zuordnung verbleibender Lücken nicht exakt die unqualifizierten ursprünglichen IDs abdeckt.

Finale RTK-vermittelte AST-, JSON-, Exakt-140-ID-, Ergebniszählungs- und EN/DE-Überschriften-/Tabellenstrukturprüfungen bestanden. Mutationen mit fehlendem beziehungsweise zusätzlichem Schlüssel der 69-ID-Lückenzuordnung wurden abgewiesen. Die begrenzte Prüfung `git diff --check` bestand. Finale repositoryweite Prüfungen für Variablendokumentation, Zweisprachigkeit, Repository-Referenzen und Links bestanden gegen die gepinnte Framework-Revision.

Das NGINX-I12-Harness weist nun vor Lesezugriffen, Veröffentlichung, Konfigurationsausführung und Hashing geladener Images fremde, für Gruppe oder andere beschreibbare, verlinkte, nicht reguläre, traversierende oder außerhalb der Grenzen liegende Nachweispfade ab. Build-Ausgaben entstehen frisch und privat; Worker-Scratchverzeichnisse erhalten innerhalb ihrer zugelassenen Speichergrenze zusätzlich unvorhersagbare Namen. Die Berichtsveröffentlichung bleibt auf die drei aufgabeneigenen versionierten Dateien begrenzt. 70 fokussierte I12-Tests einschließlich 18 dauerhafter Grenzregressionen bestanden. Der ursprüngliche gehärtete Replay schlug alle 93 aufbewahrten Kandidaten ohne Freigabe vor und materialisierte alle 71 geprüften Datensätze mit 71 eindeutigen physischen Requestpfaden erneut.

PR #410 wurde zuerst auf `a2d545ac7ec4abce23595e1c033f094104617201` und danach auf `61e45cf6dd211f21835709a014fe6884d4bcda62` fortgeschrieben; beide Heads wurden mit normalen Merge-Commits integriert, zuletzt `571a80ac402dc55f42be3370892765b9bd2eff3a`. Der exakte Build der aktuellen Quellen auf diesem Merge exportierte 2.141 reguläre Parent-Dateien sowie den Framework-Gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf`. Sein Git-Baum lautet `6119d6510ef503ffba7cdbba490c429508579efa` und sein Quellmanifest `9c94a861886f2814531637179f9365447baf13401c3d10f3abf750291a9e7927`; die SHA256-Werte des regulären und des beobachteten Moduls lauten `6d58a540bb364461905748a50792b0158685655d60f1f078ca55b47e1628e304` und `e8d4ff973a3d921cef0cf9ce39e9b823ac7addd967ebd4bddc96829907b4d047`. Das aktuelle gemeinsame Registry verifiziert 155 Objekte und neun Profile; gemeinsame Verifikation und Anwendung endeten auch innerhalb des eingefrorenen unveränderten Registry jeweils mit null. Die aktuellen Quellen blieben current-v2; die historische Kompatibilitätsstufe war ausdrücklich von Laufzeitqualifikation ausgeschlossen. Frische Konfigurationskontrollen erhielten beide erwarteten historischen Ladefehler und akzeptierten die unterstützten Safe- und Strict-Konfigurationen.

Ein frischer versiegelter Kompatibilitäts-Retest, `attempt-1792079470951070559`, führte `NEED-request-file` und `NEED-response-file` mit dem aktuellen Harness aus: Controller und Treiber beendeten sich mit null, Root-Master und Nobody-Worker wurden beobachtet, alle vier ausgewählten beziehungsweise nachfolgenden Clients beendeten sich mit null und vollständigem Framing, beide eigenen Master wurden mit bestätigtem Cleanup abgewartet, und der Controller meldete weder Timeout, Ressourcenverletzung, überlebenden Namespaceprozess noch Mount-Leak. Jede ausgewählte beziehungsweise nachfolgende Allokation erfasste P1, P2, P3 und P4 genau einmal mit nativer Rückgabe 1 sowie je einen Aufruf von Common-Finish, nativem Logging und nativem Cleanup; der Request nutzte einen 65.553 Byte großen temporären Dateibody und die Response einen tatsächlichen Dateibuffer bis Byte 36. Frühere blockierte Packaging-Versuche und eine Controller-Beobachtung eines Cleanup-Rennens bleiben erhalten und zählen nicht als erfolgreicher Hostnachweis.

Ein zweiter versiegelter Retest nach `a2d545ac`, `attempt-1792315527242854317`, band sein exaktes beobachtetes Modul und das NGINX-Binary `0d2287b344a1af4c6cc986dd915c09c60f3c942ec8ae76f8bdc5456506939746`. Controller und Treiber endeten mit null ohne Timeout, Ressourcenverletzung, Überlebende oder Mount-Leaks. Alle drei Fälle mit Root-Master/Nobody-Worker hatten direkt abgewartete ausgewählte und benachbarte Clients, vollständiges HTTP/1.1-Framing, Nullsignale, verifiziertes Listener-/Prozess-Cleanup sowie Observer-Finalzustände mit null ausstehenden Aufrufen und lebenden Zuordnungen. `NEED-request-file` hängte 32.768 + 32.768 + 17 Bytes aus einer echten temporären Datei von 65.553 Bytes an; `NEED-response-file` beobachtete einen echten Dateibuffer von Offset 0 bis 36. Beide erreichten P1-P4 einmal mit nativer Rückgabe 1, genau einer Terminal-zu-P2-/P4-Kopplung, HTTP 200 sowie je einem Common-Finish-, nativen Logging- und nativen Cleanup-Aufruf. `NEED-request-empty` erhielt erneut eine gültige leere Terminalkette, lieferte jedoch nach P1 und vor P2/P3/P4 oder einem nativen Body-Append HTTP 500; der erste physische Connectorfehler blieb `invalid request body buffer range`, und der nachfolgende Request lieferte HTTP 200. Dieser Retest bestätigt den separaten Produktfehler für #382, ohne einen Lifecycle-PASS hinzuzufügen.

Der neueste versiegelte Retest, `attempt-1792316268398778779`, bindet die exakten Quellen von `571a80ac` und das beobachtete Modul `e8d4ff973a3d921cef0cf9ce39e9b823ac7addd967ebd4bddc96829907b4d047`. Auch sein Controller und Treiber endeten mit null ohne Timeout, Ressourcenverletzung, Überlebende oder Mount-Leaks. Der aktuelle Reviewer erzeugte drei physische Kandidaten ohne unbekannte Felder oder Lücken und ohne Qualifikation. Die beiden Dateifälle erreichten erneut P1-P4 mit nativer Rückgabe 1, genau einer echten Terminal-zu-P2-/P4-Kopplung, HTTP 200, 36 Responsebytes und vollständigem Framing; der Request nutzte die temporäre Datei mit 65.553 Bytes, die Response den Dateibereich 0..36. Der leere Request erreichte erneut nur P1 und lieferte HTTP 500/177 Bytes vor nativem P2/P3/P4 oder nativem EOS; sein erster physischer Fehler war ein Requestbody-Connectorfehler vor Commit mit `eos_seen=false`. Jeder ausgewählte und benachbarte Client endete mit null ohne Signal, jeder Nachbar lieferte HTTP 200, Finish/Logging/Free erfolgten je einmal, Master endeten mit null, Observer-Finalzustände hatten null ausstehende Aufrufe/lebende Zuordnungen, und Listener-/Prozess-Cleanup war vollständig. Dies bleibt Regressionsnachweis für #382 und ergänzt keinen Ledger-PASS.

Die aufbewahrte Kandidatenzusammenfassung und die geprüften Entscheidungen werden mit dem aktuellen Qualifier weiterhin als exakt 71 Datensätze reproduziert, und die deterministische Berichtserzeugung bleibt byteidentisch. Eine neue Prüfung des alten 93-Fall-Hostlaufs weist die aktuelle Identität geladener Images korrekt ab, weil `/usr/lib/x86_64-linux-gnu/libcurl-gnutls.so.4.8.0` auf dem Host nach der Erfassung ersetzt wurde (Inode und SHA256 geändert). Der ursprüngliche Identitätsnachweis zur Prüfzeit bleibt hashgebunden; diese spätere Hostmutation wird als Grenze des historischen Replays erfasst und weder umgangen noch in PASS umgedeutet. Beide frischen Drei-Fall-Retests oben validieren geladene Images gegen den jeweiligen Hostzustand zur Erfassungszeit. Auf dem neuesten exakten Merge bestanden 70 NGINX-I12-, 17 Mapper-/Cleanup-, 48 gemeinsame Capture-, 48 Oracle-/Ledger-/Berichts- und 34 Native-Observer-Tests: 217 fokussierte Tests ohne Skip oder Fehler.

Das versionierte Artefakt bettet nur projizierte öffentliche Zusammenfassungen und lesbare Projektionen ursprünglicher ausgewählter Verträge ein. Vollständige Kandidatenlisten, fallbezogene Entscheidungen/Bodyprüfungen, Verifikations-Umgebungszuordnungen sowie pfadbezogene Eingabe- und Quellhash-Inventare bleiben extern und sind durch Eingabepfad/SHA256/Größe gebunden. Die öffentlichen Projektionen behalten jeweils die Inventaranzahl und einen kanonischen SHA256 für die vollständige Zuordnung; jede ausgewählte Anforderung behält außerdem den kanonischen Hash des unprojizierten Vertrags und einen externen Basis-Locator. Eine rekursive Prüfung bricht bei Body-Hexwerten, Umgebungszuordnungen und sensiblen Schlüsselnamen ab; Befehle, Status, Logdigests, Zähler und Oracle-Korrekturgründe bleiben prüfbar. Öffentliche Befehlszusammenfassungen ersetzen lokale Entwickler-Checkoutpfade deterministisch, während das referenzierte rohe Verifikations-Receipt den exakten Aufruf behält.

## Bekannte Einschränkungen

Ein ausgewählter Fall benötigt sein eigenes geprüftes vollständiges Lifecycle-Paket. Kandidatenbeobachtungen, Builds, Konfigurationsprüfungen und native Tests allein können ihn nicht qualifizieren. Client-EOF und Nullbyte-Append ersetzen kein natives EOS. HTTP/1-Nachweise behaupten kein HTTP/2-Resetverhalten. SDK-3.0.14-MIME-Fixture09 wird nicht stillschweigend durch Fixture08 oder erfundenen Clear-Reset ersetzt.

## Verbleibende Risiken

Alle Zeilen ohne vollständige Lifecycle-Qualifikation bleiben unvollständig. Die Body-Null-Fixture erreicht P1 trotz ihres ursprünglichen P2-Oracles; die HTTP-500-Statuskorrektur löst diesen Phasenkonflikt nicht. Der separat bestätigte Produktfehler für leere Requests lehnt NGINX' gültigen leeren Terminalbuffer vor P2 ab; das reguläre Modul reproduziert ihn. Sein produktiver Fix gehört separat zu #382. Master-Merge und Release gehören nicht zu dieser Aufgabe.

## Nicht ausgeführte Prüfungen mit Begründung

Finaler Hosted-CI-/Sonar-Status wird nach jedem Push getrennt von lokalen Nachweisen festgestellt. Ruff war in der ausgewählten Parent-`.venv` nicht verfügbar (`No module named ruff`); kein Paket wurde installiert. Berichtssyntax und Verhaltens-/Negativprüfungen bestanden. Fehlende fallbezogene Lifecycle-Messungen bleiben im generierten Bericht und Ledger explizit. Repositoryprüfungen für Variablendokumentation, Zweisprachigkeit, Referenzen und Links bestanden in einer externen unveränderlichen Ansicht mit dem exakten Parent-Baum und dem Framework-Pin `99a7985c1be92a2297b1b59208f64df6768f2cbf`; das absichtlich leere Submodul des Aufgaben-Worktrees kann diese Linkziele nicht direkt bereitstellen.

## Finaler Diff- und Review-Status

Änderungen beschränken sich auf NGINX-spezifische I12-Tests/Harness/Fixtures und diesen Nachweis-/Berichtsumfang. Draft-PR #416 zielt von `codex/i12-nginx-410-20261015` auf `work/pr382-i12-host-evidence-20261011`; die Lieferung verwendet ausschließlich normale Commits und normale Pushes. Ein Master-Merge gehört nicht zu diesem Record.
