# Change Record: CR-20261015-traefik-companion-method-metadata

**Sprache:** [English](CR-20261015-traefik-companion-method-metadata.md) | Deutsch

Komponentenregressionen für zwei begrenzte Traefik-Fixes. Die integrierte Hostabnahme bleibt eine eigene Verpflichtung von PR #413.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-traefik-companion-method-metadata |
| Datum (UTC) | 2026-10-15 |
| Basis-Revision | `9980eb049dde0643da6a4f04e3b6712801b670b3` |

## Motivation und Problemstellung

Das qualifizierte historische Companion-P4-Safe-Event forderte deny403 an und wendete nach Commit korrekt log_only an, enthielt aber keine Late-Intervention-Metadaten. Unabhängig davon verwendet die gepinnte Traefik-forwardAuth-Implementierung standardmäßig GET für die Autorisierung; die eingecheckten Vorlagen aktivierten keinen Methodenerhalt.

## Akzeptanzkriterien

Validierte disruptive P4-OUTCOME-Events nach Commit behalten ihr Late-Flag und den tatsächlich konfigurierten Policy-Modus. Allow, Precommit, fehlerhafte/doppelte OUTCOME-Frames und technische Fehler bleiben getrennt. ForwardAuth erhält die Originalmethode und erzeugt mit `trustForwardHeader: false` vertrauenswürdige Forwarding-Metadaten neu. Die Authorization-Response-Kapazität bleibt unverändert.

## Implementierungsentscheidung und Begründung

Die gespeicherte MRC1-Entscheidung erst nach Prüfung von OUTCOME-Reihenfolge und Payload annotieren, anhand des tatsächlichen Commit-, Response-EOS-, P4- und disruptiven Entscheidungszustands. Die Runtime bestimmt weiterhin den Policy-Modus. Natives MSE1 liefert einen unabhängigen Vergleich. `preserveRequestMethod: true` in beiden Vorlagen und im Runtime-Konfigurationsproducer aktivieren; fehlende, deaktivierte oder mehrdeutige Methoden-/Trust-Einstellungen im Validator zurückweisen. Gepinnte Upstream-Implementierung: Traefik 3.7.13, Commit `fc92cc118a0557a029c7019d5ee06665127b0f13`, `pkg/middlewares/auth/forward.go`.

## Geänderte Dateien

`common/runtime/response_companion_transport.c`; beide dynamischen forwardAuth-Vorlagen; `runtime_smoke.py` und `start-smoke.sh`; Traefik-README-Paar; `test_traefik_forwardauth_p2_contract.py`; neuer Python-Test für Companion-Metadaten und drei C-Proben; dieser EN/DE-Bericht. Keine Framework-/MRTS-Dateien oder Gitlinks ändern sich.

## Ausgeführte Befehle

`rtk proxy env CODEX_RUN_ROOT=<external-run>/product python3 -B -m unittest -v tests.test_traefik_i12_companion_metadata`: 11 PASS. Die öffentliche MRC1-/Real-SDK-Regression scheiterte vor dem Fix in Safe und Off; drei Metadaten-/Policy-Mutationen sowie eine Annotation-vor-Admission-Mutation wurden erkannt. Achtzehn angrenzende MRC1-/I10-/Native-Event-Verträge bestanden. `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_traefik_forwardauth_p2_contract tests.test_traefik_runtime_smoke_security`: 35 PASS, zwei optionale echte Hostloader-Tests übersprungen, weil ihre explizite Hostvoraussetzung fehlte. Der neue Methodenvertrag scheiterte in sieben Teilfällen am bisherigen Helper. Exakte Befehle, Exits, Quellhashes und Ausgaben sind in den Laufbelegen erhalten. Die integrierte Root-Prüfung wird separat erfasst.

## Security-Auswirkung

Keine Änderung von Protokoll, Enforcement, Capability oder öffentlicher API. Die bestehende Frame-Admission erfolgt vor der Annotation. Client-Forwarding-Header bleiben nicht vertrauenswürdig; `trustForwardHeader: false`, Request-Sample-Limits und `maxResponseBodySize=32768` bleiben erhalten. Strict-Profil-Admission wird nicht gelockert. Worker-Ownership und Cleanup bleiben unverändert.

## Runtime-Evidence

Der unveränderliche historische FAIL und die physischen JSONL-/Audit-Belege bleiben mit ihrer ursprünglichen Revision erhalten. Frische Komponentenproben führen das tatsächliche SDK, MRC1-Client/-Server und den JSONL-Recorder aus; sie belegen die Metadatenregression und keinen Live-Traefik-Lifecycle. Externer Lauf: `i12-traefik-acceptance-20261015`, `product/companion-metadata-final-manifest.json` und `method-uri/{before,after}.json`. Ein neuer integrierter Hostlauf muss dieselbe Original-ID nach regulärer Synchronisierung #382 → #410 → #413 qualifizieren.

## Bekannte Einschränkungen

Dieser Produktpatch qualifiziert nicht die 280 Traefik-Original-IDs. Hostzustellung, natives EOS, Finalisierung/Free und Konfigurationsanwendbarkeit benötigen eigene physische Belege. Die Kompatibilität des Methodenerhalts mit älteren Traefik-Releases ist nicht nachgewiesen.

## Verbleibende Risiken

Auch die Root-Prüfung bestand: alle drei Go-Module mit `go test -mod=readonly -count=1 -race ./...` und `go vet -mod=readonly ./...`; 53 gezielte Tests (zwei optionale Hostloader-Skips), 59 breitere Native-/Security-/Fehlerverträge (zwei Capability-Skips), native Engine-Service-/UDS-Tests, Common-Security-/SDK-/Flow-Prüfungen, Change-Record-Struktur und EN/DE-/Linkprüfungen mit privatem schreibgeschütztem Framework-Mount. Anfängliche Fehler durch lange Socketpfade und fehlende explizite SDK-Pfadangaben bleiben separat erhalten; Wiederholungen mit kurzen privaten Pfaden und installiertem SDK bestanden. Exakte Belege: `checks/product-*.json` im externen Abnahmelauf.

Die endgültige integrierte Hostmatrix und CI-/Sonar-Ergebnisse des exakten Heads bleiben eigene Abnahmeanforderungen. Das historische Gitleaks-Problem von #382 bleibt unabhängig; weder History-Umschreibung noch Ausnahme werden eingeführt.

## Nicht ausgeführte Prüfungen mit Begründung

Die zwei optionalen Hostloader-Tests benötigen die zugelassene private Nonroot-Hostumgebung und werden dort wiederholt. Vollständige Traefik-I12-Qualifikation, finale gehostete Analyse und dauerhafte Veröffentlichung der Rohbelege gehören zur fortgesetzten Arbeit an #413 und werden durch diesen Komponentenbericht nicht behauptet.

## Finaler Diff- und Review-Status

Eine unabhängige Read-only-Quellprüfung fand nach Verlagerung der Annotation hinter die Admission keinen handlungsrelevanten Befund. `rtk proxy git diff --check` bestand. Normaler Commit/Push und Integration sind autorisiert; PR-Merge, Force-Push, Rebase oder Master-Änderung sind weder autorisiert noch behauptet.
