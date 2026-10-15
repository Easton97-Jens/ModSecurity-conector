# Change Record: CR-20261015-i12-nginx-native-evidence

**Sprache:** [English](CR-20261015-i12-nginx-native-evidence.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-nginx-native-evidence |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation und Problemstellung

NGINX-spezifische I12-Nachweise aus PR #410 erhalten und ergänzen; ursprüngliche Hostausführung, Fixturefehler, Oracle-Konflikte und vollständig qualifizierte Lifecycle-Ergebnisse getrennt halten.

## Akzeptanzkriterien

Exakt 140 ursprüngliche ausgewählte IDs, unveränderte ausgewählte Verträge und historische Revisionen; unabhängige physische Belege je ID; kein PASS aus Aliasen, Kandidaten oder ungelösten Oracles. Neue Nachweise und verbleibende Lücken sind in beiden Sprachen zu berichten.

## Implementierungsentscheidung und Begründung

NGINX-spezifische Capture-/Harness- und Ledger-/Berichtsgeneratoren ergänzen Nachweise ohne Änderungen an gemeinsamer Source-Capture-Infrastruktur, gemeinsamem Oracle-Generator, zentraler Matrix oder produktivem Connectorcode. Der Bericht prüft unveränderliche Basis-SHA256 und Originalzeilen; Kandidatenbeobachtungen können keinen Lifecycle freigeben.

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

Finale RTK-vermittelte AST-, JSON-, Exakt-140-ID-, Ergebniszählungs- und EN/DE-Überschriften-/Tabellenstrukturprüfungen bestanden. Mutationen mit fehlendem beziehungsweise zusätzlichem Schlüssel der 69-ID-Lückenzuordnung wurden abgewiesen. Die begrenzte Prüfung `git diff --check` bestand. Finale repositoryweite Dokumentations-/Linkprüfungen verantwortet weiterhin die integrierende Aufgabe.

Das versionierte Artefakt bettet nur projizierte öffentliche Zusammenfassungen und ursprüngliche ausgewählte Verträge ein. Vollständige Kandidatenlisten, fallbezogene Entscheidungen/Bodyprüfungen und Verifikations-Umgebungszuordnungen bleiben extern und sind durch Eingabepfad/SHA256/Größe gebunden. Eine rekursive Prüfung bricht bei Body-Hexwerten, Umgebungszuordnungen und sensiblen Schlüsselnamen ab; Befehle, Status, Logdigests, Zähler und Oracle-Korrekturgründe bleiben prüfbar.

## Bekannte Einschränkungen

Ein ausgewählter Fall benötigt sein eigenes geprüftes vollständiges Lifecycle-Paket. Kandidatenbeobachtungen, Builds, Konfigurationsprüfungen und native Tests allein können ihn nicht qualifizieren. Client-EOF und Nullbyte-Append ersetzen kein natives EOS. HTTP/1-Nachweise behaupten kein HTTP/2-Resetverhalten. SDK-3.0.14-MIME-Fixture09 wird nicht stillschweigend durch Fixture08 oder erfundenen Clear-Reset ersetzt.

## Verbleibende Risiken

Alle Zeilen ohne vollständige Lifecycle-Qualifikation bleiben unvollständig. Die Body-Null-Fixture erreicht P1 trotz ihres ursprünglichen P2-Oracles; die HTTP-500-Statuskorrektur löst diesen Phasenkonflikt nicht. Der separat bestätigte Produktfehler für leere Requests lehnt NGINX' gültigen leeren Terminalbuffer vor P2 ab; das reguläre Modul reproduziert ihn. Sein produktiver Fix gehört separat zu #382. Master-Merge und Release gehören nicht zu dieser Aufgabe.

## Nicht ausgeführte Prüfungen mit Begründung

Finale Hosted-CI-/Sonar- und Lieferstatus sind durch lokale Nachweise nicht festgestellt. Ruff war in der ausgewählten Parent-`.venv` nicht verfügbar (`No module named ruff`); kein Paket wurde installiert. Berichtssyntax und Verhaltens-/Negativprüfungen bestanden. Fehlende fallbezogene Lifecycle-Messungen bleiben im generierten Bericht und Ledger explizit. Lokale Dokumentations-/Linkprüfungen führt die integrierende Aufgabe separat aus; hier wird kein Ergebnis abgeleitet.

## Finaler Diff- und Review-Status

Änderungen beschränken sich auf NGINX-spezifische I12-Tests/Harness/Fixtures und diesen Nachweis-/Berichtsumfang. Die integrierende Aufgabe verantwortet finale Diffprüfung, normale Commits und Draft-PR-Lieferung gegen `work/pr382-i12-host-evidence-20261011`; dieser Record behauptet keinen Commit, keine PR-Nummer und keinen Merge.
