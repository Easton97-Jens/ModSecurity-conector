# Change Record: CR-20261011-pr382-i12-host-evidence

**Sprache:** [English](CR-20261011-pr382-i12-host-evidence.md) | Deutsch

Manuelle Dokumentations-/Nachweisänderung. I12 NOT COMPLETE; kein vollständiger erforderlicher Routenteil-PASS.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261011-pr382-i12-host-evidence |
| Datum (UTC) | 2026-10-11 |
| Basis-Revision | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |

## Motivation und Problemstellung

Historisches R17 und kompilierte Tests belegten I12 am getesteten PR-#382-Sourcetupel nicht. Unabhängige Host-/Client-/Backend-/Transport-/physische Log-/Cleanup-Nachweise, echte Fehler und genaue Lücken erfassen.

## Akzeptanzkriterien

Run `20261011T063350Z-0df51024008f-i12` an getesteten Parent `0df51024008fc84f0a6820f3b011055b69c3a3e2`, Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` und MRTS `8a6bb546c4c81d8ffc7be801dceac60c6925685f` binden. Dreizehn Pflichtteile plus eine ergänzende Diagnosekontrolle trennen, R17 erhalten, vollständige EN/DE-Parität pflegen und I12 bei Fehlern oder fehlendem Pflichtnachweis unabgehakt lassen. Vollständige Routenteil-PASS sind 0; breite I12-Kriterien nicht erfüllt.

## Implementierungsentscheidung und Begründung

Nur Dokumentation: externe private Fixtures, unveränderliche Sources, Builds und Rohreceipts bleiben außerhalb des empfohlenen atomaren Acht-Dateien-Commits. Keine Produkt-/Test-/Dependency-/Gitlinkänderung. Offizielle bwrap-/AppArmor-Isolation und unprivilegierte Hostidentitäten erhalten; fehlende Beobachtungen null lassen und physische Sinkfehler von Transportfehlern trennen.

## Geänderte Dateien

Vier Paare: `docs/pr-382-checklist.md` / `docs/pr-382-checklist.de.md`; `docs/pr-382-i09-i12-rest-matrix.md` / `docs/pr-382-i09-i12-rest-matrix.de.md`; `docs/pr-382-i12-host-evidence-20261011.md` / `docs/pr-382-i12-host-evidence-20261011.de.md`; `reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.md` / `reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.de.md`. Historisches I12b/R17 und die 56 Source-Matrixzeilen bleiben unverändert.

## Ausgeführte Befehle

RTK umschließt alle Shellbefehle. `make test-hostruntime-preflight`: Exit 0, 27 Tests. `make check-common-helpers-c17`: Exit 0. `make check-ci-security-contract`: Exit 2, 177 Tests, drei Importfehler, sechs Skips. `make check-bounded-smoke-runtime-contract`: Exit 2, 119 Tests, vier Assertion-/Subtestfehler, 12 Errors. Native Event-/Sink-/Lifecycle-Batch: Exit 1, 74 Tests, 15 Assertion-/Subtestfehler, zwei Errors. actionlint 1.7.12: Exit 0 für 32 Workflows plus Permissionfixtures. zizmor 1.29.0 offline: Workflows/sichere Kontrollen Exit 0, unsichere Kontrollen erwarteter Exit 14. Explizites Parent-Python ist `/usr/local/bin/python3` 3.14.7; exakte Befehle/Ergebnisse bleiben in `verification/results.json`. `rtk gain`: Exit 0. Finale native Bilingual-, Link-, Change-Record- und Diffchecks Exit 0; Receipts bleiben in document-mount-checks-02/results.json erhalten.

## Security-Auswirkung

Kein Produktsicherheitsverhalten geändert. Physische Apache-Sinkweitergabefehler und historischer fokussierter Traefik-Native-/UDS-`protocol_error` bleiben sichtbar. Jüngste Native-/UDS-Vollbeobachtungen haben normales Allow und bleiben wegen fehlenden Receipts BLOCKED. Keine Isolations-/Validierungsschwächung, Paket-/Toolchaininstallation, sensible Payloadveröffentlichung oder Produktionsdeployment. Fremde Hauptcheckoutänderungen erhalten. Kontrollierte APR-FD-Fehler beweisen keine natürliche Dateisystemerschöpfung oder jeden parallelen FD-Schedule.

## Runtime-Evidence

Der [Hostbericht](../../../docs/pr-382-i12-host-evidence-20261011.de.md) erfasst Provenienz, dreizehn Pflichtteile und Lücken. Lokaler Aufbewahrungsroot: `/var/tmp/codex/ModSecurity-conector/runs/e2e/20261011T063350Z-0df51024008f-i12`; kein herunterladbares GitHub-Artefakt. Geschlossener Apache-Bestand: 21 Fälle, 9 Vollvertrags-PASS, 5 physische Sink-FAIL, 7 Vollvertrags-NOT_EXECUTED. Echte direkte curl-Exits/Bytes, Backendzählungen, native committed actions, echte Recoverylogs und unabhängiges Cleanup beobachtet. Kein vollständiger Pflichtfallbestand. NGINX-Identitätszulassung BLOCKED. libModSecurity-3.0.14-SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`.

Jüngster geschlossener Envoy-/Traefik-Bestand: 27 Fälle, 0 PASS, 0 FAIL, 27 BLOCKED. Späterer PR-#382-Head `498653c2a193d34b7b25b2903b1e4db1c45e7f73` hat nur Dokumentation/B09-Testdifferenz; Nachweis bleibt an getestetes `0df51024008fc84f0a6820f3b011055b69c3a3e2` gebunden, ohne PASS-Vererbung. Parent/Apache/native Wrapper verwenden Python 3.14.7; native Envoy-/Traefik-Helfer explizit `/usr/bin/python3` 3.14.4.

Nativer Review bis Stock full06 erhält 262 Hashreferenzen. HTX full02 hat acht echte Fälle; SPOP full03 sechs plus getrennt bewerteten Response-Companion-Nachweis; beide wegen unabhängigen Client-/Sink-/Transaktionscleanuplücken BLOCKED. Patched-Staticfile-focus02 ist begrenzter curl0/200/32 Bytes, full03 Trusteddirectory-ablehnung77. Stock06 erhält 16 geprüfte Rohdateien und echte Zwei-Allow-Backendlogs ohne /p1-block-Ankunft. Natives engine_decision actual_action="" scheitert am unveränderten Harnessenum; same-TX request_blocked ist actual_action=deny, HTTP451, transport_result=http_status, Rule9821001 mit Hashkette. Direkter Denyclientnachweis bleibt null; spätere vier Fälle NOT_EXECUTED. Stock05-Rohverlust bleibt historisch. Keine Produktregression oder unabhängiger Clientenforcementfehler abgeleitet. Finaler ausgewählter Bestand in `matrix.final.json`: 79 Records, 9 PASS, 6 FAIL, 53 BLOCKED, 11 NOT_EXECUTED; ergänzende Kontrolle ausgeschlossen. Ganze dreizehn Teile: 0 PASS, 2 FAIL, 11 BLOCKED. Keine vollständige Pflichtfallabdeckung. `normalized/` erhält originalgebundene Teilreceipts; keine physischen Events erfunden. Unabhängiger Rehash bestätigt 791 Referenzen (529 Apache + 262 native). Vorläufige Docchecks scheiterten wegen fehlenden Framework-/Gitmetadaten; finale echte Read-only-Mountchecks Exit 0 mit privaten nur lesbaren Gitpfadaliasen, unveränderten Originaldateien und unveränderten Validatoren.

## Bekannte Einschränkungen

Kein vollständiger Pflicht-Routenteil-PASS. Sieben begrenzte Apache-MIME-/EOS-Beobachtungen beweisen nicht den vollständigen Scope-/Genau-einmal-Vertrag. Fehlende Timestamp-/Sequenz-/Hashbeobachtungen bleiben unsynthetisiert. Driver-Exit ist kein Clientabschluss; Companion-Teile benötigen getrennte Receipts. Historisches R17 beweist weder dieses getestete Tupel noch H2/H3/CRS/Off/Produktion.

## Verbleibende Risiken

Pflichtroutenfälle und I11-Arbeit zur physischen Apache-/SPOP-Sinkweitergabe bleiben offen. Gescheiterte breitere Verifikation bleibt erhalten, wird nicht in grüne CI umgewandelt. Kein Sonar-, Protected-Exact-Head- oder Releasereifeanspruch. Lokale Rohaufbewahrung ist kein portabler veröffentlichter Nachweis.

## Nicht ausgeführte Prüfungen mit Begründung

Vollständige NGINX-Runtime durch erforderliche Root-Master-/nobody-Worker-Identitätsübergabe blockiert. Vollständige All-Route-Abnahme bleibt nicht verfügbar. Breitere Prüfungen treffen fehlendes PyYAML, hardcodierte uninitialisierte Worktree-Frameworkpfade, fehlenden `python`-Alias und Sandbox-UID-Grenzen; keine Schwächung oder Dependencyinstallation erzwingt einen PASS. Finale Bilingual-/Link-/Change-Record-Prüfungen bestehen; gehostete Liefer-CI/Sonar für den Veröffentlichungscommit bleiben ausstehend und erben keine lokalen Ergebnisse.

## Finaler Diff- und Review-Status

Ein atomarer Acht-Dokumente-Commit wird empfohlen. Scoped Diff, native fertige Bericht-/Recordchecks und unabhängiger nur lesender Dokumentationsreview bestanden; keine materiellen Reviewbefunde bleiben. Nutzerautorisierte Lieferung ist ein gestapelter Draft PR auf `fix/unified-native-results-events-20260921`; keine Veröffentlichung/PR-Nummer, Merge oder Deployment erfunden. I12 NOT COMPLETE.
