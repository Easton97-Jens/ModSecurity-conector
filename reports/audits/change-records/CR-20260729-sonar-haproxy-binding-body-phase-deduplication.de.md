# Change Record: Parent-HAProxy-Binding-Body-Phase-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-haproxy-binding-body-phase-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-binding-body-phase-deduplication |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | Zwei aktuelle SonarQube-Cloud-CPD-Paare im HAProxy-Binding: Phase-2- und Phase-4-Chunk-Append-/Finalisierungspfade (68 gemeldete Duplikatzeilen). |
| Grenze | Parent-HAProxy-Binding-Source und gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Das Binding duplizierte Lifecycle-Guards und Accounting in der Request-Body-Phase 2 und der Response-Body-Phase 4. Die Reduktion muss unterschiedliche Phasennummern, Transaction-State-Felder, libmodsecurity-Einstiegspunkte, Diagnostik und Intervention-Erfassungszeitpunkt ohne connector-eigenen Body-Buffer erhalten.

## Akzeptanzkriterien

- Gemeinsame Append- und Finish-Helper erhalten die früheren Null-, Header-vor-Body-, Post-EOS-, Pointer/Längen-, Library-Fehler-, Accounting- und Decision-Pfade.
- Explizite Request- und Response-Wrapper behalten ihre öffentlichen APIs und nutzen ausschließlich ihre bestehenden `msc_append_*_body`- und `msc_process_*_body`-Funktionen.
- Der native Binding-Selbsttest besteht unter GCC und Clang im C17-Modus mit `-Wall -Wextra -Werror`.
- Exact-Head-Hosted-Checks und SonarQube Cloud müssen vor jeder Merge-Betrachtung null New Issues, null New-Code-Duplikatzeilen, null New-Code-Duplikatdichte und eine niedrigere Gesamtduplikatanzahl beweisen.

## Implementierungsentscheidung und Begründung

Ein typisierter Descriptor pro Aufruf übergibt Transaction-Felder, Meldungen, Phasennummer und passende libmodsecurity-Einstiegspunkte an zwei kleine Helper. Die öffentlichen Funktionen bleiben explizite Wrapper, einschließlich der `transaction == 0`-Diagnostik, die vor der Descriptor-Konstruktion erforderlich ist. Damit verschwinden die zwei duplizierten Paare, ohne Phase-Ownership oder die externe API zu verändern.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_modsecurity_binding.c` — typisierte gemeinsame Body-Append-/Finalisierungs-Helper und vier explizite Phasen-Wrapper.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| GCC-C17-nativer Binding-Build | bestanden mit `-std=c17 -Wall -Wextra -Werror` gegen den temporären vorhandenen libmodsecurity-Prefix. |
| GCC-C17-`self-test-modsecurity-binding` | bestanden; Request-Body-Disruptive-Rule-Selbsttest meldete Status 403. |
| Clang-C17-nativer Binding-Build | bestanden mit `-std=c17 -Wall -Wextra -Werror` gegen denselben temporären Prefix. |
| Clang-C17-`self-test-modsecurity-binding` | bestanden mit demselben Self-Test-only-Scope. |
| `python3 ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | bestanden; Lifecycle-, Borrowed-Slice-, EOS-Callsite-, Host-Action- und No-Unsupported-Claim-Kontrollen bestanden. |
| `python3 ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | bestanden. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Dieser Code verarbeitet HTTP-abgeleitete Body-Chunks an einer Host-Protokoll-Grenze. Die Refaktorierung erhält die Source-to-Sink-Invariante: Eine Länge ungleich null benötigt weiter einen nicht-null Borrowed Pointer; jede Phase erreicht nur ihre passende libmodsecurity-Funktion; Post-EOS-Input bleibt abgewiesen; und nur der Phasen-Finisher erfasst die Intervention dieser Phase. Der native Request-Body-Rule-Selbsttest bestand durch die echte libmodsecurity-C-API. Keine Validierungs-, Isolations-, Logging-, Late-Intervention- oder Quality-Gate-Kontrolle wird gelockert.

## Runtime-Evidence

Die kompilierten Selbsttests nutzen den temporären vorhandenen libmodsecurity-Prefix und bestätigen den Phase-1- und Request-Body-Rule-Pfad. Sie führen keine Live-HAProxy-Runtime, keine CRS-Regeln und kein Response-Body-Enforcement aus. Der statische HTX-Contract prüft die Source-Invarianten von Phase-4-Dispatch und Finalisierung direkt, ist jedoch keine Host-Runtime-Behauptung.

## Bekannte Einschränkungen

- Eine Live-HAProxy-3.2.21-plus-libmodsecurity-Runtime und CRS-Fixture waren in diesem Task-Worktree nicht verfügbar.
- Die vollständige Codex-Security-Diff-Scan-Fähigkeit ist in dieser Runtime nicht verfügbar: Ihr verpflichtender Delegated-Worker-Preflight ist unvollständig. Dieser Record behauptet keinen vollständigen Scanner-Report.
- Hosted-Checks und eine frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

- Künftige Descriptor-Nutzer müssen auf kompatible Body-Append-/Finish-Funktionen und passende Transaction-Felder begrenzt bleiben; eine neue Phase oder ein neuer Ownership-Vertrag benötigt eine Lifecycle-Prüfung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-/libmodsecurity-Runtime, kein Response-Body-Enforcement-Test, kein CRS-Selbsttest, keine vollständige Connector-Matrix und kein vollständiger Codex-Security-Diff-Scan liefen. Die externen Source-/Runtime-Fixtures fehlen in dieser temporären Task-Umgebung und die verpflichtende Delegated-Worker-Fähigkeit des Scanners ist hier nicht verfügbar. Native C17-Binding-Selbsttests und der statische HTX-Contract sind die stärksten verfügbaren Kontrollen.

## Finaler Diff- und Review-Status

Der Kandidat ist auf das Parent-HAProxy-Binding und bilinguale Traceability begrenzt. Er entfernt zwei bestätigte 17-Zeilen-CPD-Paare, die als 68 Duplikatzeilen gemeldet waren. Lokale Compile-, Selbsttest-, statische Contract- und Whitespace-Prüfung sind abgeschlossen. Ein Draft-PR und Exact-Head-Hosted-Verifikation bleiben vor jeder Delivery- oder Merge-Behauptung erforderlich.
