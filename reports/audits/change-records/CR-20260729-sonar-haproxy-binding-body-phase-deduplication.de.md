# Change Record: Parent-HAProxy-Binding-Body-Phase-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-haproxy-binding-body-phase-deduplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-binding-body-phase-deduplication |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` (ursprünglicher ausgewählter PR-Head: `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`). |
| Tracking | Zwei aktuelle SonarQube-Cloud-CPD-Paare im HAProxy-Binding: Phase-2- und Phase-4-Chunk-Append-/Finalisierungspfade (68 gemeldete Duplikatzeilen). |
| Grenze | Parent-HAProxy-Binding-Source, sein lokaler Binding-Selbsttest/Fixture/Make-Ziel, Reader-Dokumentation und gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Das Binding duplizierte Lifecycle-Guards und Accounting in der Request-Body-Phase 2 und der Response-Body-Phase 4. Die Reduktion muss unterschiedliche Phasennummern, Transaction-State-Felder, libmodsecurity-Einstiegspunkte, Diagnostik und Intervention-Erfassungszeitpunkt ohne connector-eigenen Body-Buffer erhalten.

## Akzeptanzkriterien

- Gemeinsame Append- und Finish-Helper erhalten die früheren Null-, Header-vor-Body-, Post-EOS-, Pointer/Längen-, Library-Fehler-, Accounting- und Decision-Pfade.
- Explizite Request- und Response-Wrapper behalten ihre öffentlichen APIs und nutzen ausschließlich ihre bestehenden `msc_append_*_body`- und `msc_process_*_body`-Funktionen.
- Der Binding-Selbsttest übt beide öffentlichen Body-Wrapper-Lifecycle-Pfade:
  Null-Transaction, Nichtnull-Längen-/Nullpointer-Ablehnung, Response-Append
  vor Headern, gültiges Append/Finalisierung, Post-EOS-Append und doppelte
  Finalisierung.
- Der native Binding-Selbsttest besteht unter GCC und Clang im C17-Modus mit `-Wall -Wextra -Werror`.
- Exact-Head-Hosted-Checks und SonarQube Cloud müssen vor jeder Merge-Betrachtung null New Issues, null New-Code-Duplikatzeilen, null New-Code-Duplikatdichte und eine niedrigere Gesamtduplikatanzahl beweisen.

## Implementierungsentscheidung und Begründung

Ein typisierter Descriptor pro Aufruf übergibt Transaction-Felder, Meldungen, Phasennummer und passende libmodsecurity-Einstiegspunkte an zwei kleine Helper. Die öffentlichen Funktionen bleiben explizite Wrapper, einschließlich der `transaction == 0`-Diagnostik, die vor der Descriptor-Konstruktion erforderlich ist. Damit verschwinden die zwei duplizierten Paare, ohne Phase-Ownership oder die externe API zu verändern.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_modsecurity_binding.c` — typisierte gemeinsame Body-Append-/Finalisierungs-Helper und vier explizite Phasen-Wrapper.
- `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c`,
  `connectors/haproxy/Makefile` und
  `connectors/haproxy/harness/fixtures/modsecurity-binding-lifecycle.conf` —
  echte-libmodsecurity-Request-/Response-Wrapper-Lifecycle-Regression-Coverage.
- `connectors/haproxy/README.md` und `connectors/haproxy/README.de.md` —
  korrekt abgegrenzte Selbsttest-Coverage und Runtime-Einschränkungen.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| Frühere Kontrollen des ausgewählten PR-Heads | nur historisch; sie sind keine Evidenz für den synchronisierten Kandidaten. |
| Frische Exact-Candidate-GCC-/Clang-C17-Binding-Builds und Selbsttest | ausstehend; müssen `-std=c17 -Wall -Wextra -Werror` gegen den registrierten temporären libmodsecurity-Prefix verwenden. |
| Frische Exact-Candidate-HTX-/Common-Adoption-Contracts und Diff-Hygiene | ausstehend. |

## Security-Auswirkung

Dieser Code verarbeitet HTTP-abgeleitete Body-Chunks an einer Host-Protokoll-Grenze. Die Refaktorierung erhält die Source-to-Sink-Invariante: Eine Länge ungleich null benötigt weiter einen nicht-null Borrowed Pointer; jede Phase erreicht nur ihre passende libmodsecurity-Funktion; Post-EOS-Input bleibt abgewiesen; und nur der Phasen-Finisher erfasst die Intervention dieser Phase. Der native Request-Body-Rule-Selbsttest und die ergänzte Public-Wrapper-Lifecycle-Regression müssen auf dem exakten synchronisierten Kandidaten erneut laufen. Keine Validierungs-, Isolations-, Logging-, Late-Intervention- oder Quality-Gate-Kontrolle wird gelockert.

## Runtime-Evidence

Der erweiterte Selbsttest soll den temporären vorhandenen libmodsecurity-Prefix nutzen und den Phase-1-/Request-Body-Rule-Pfad sowie P2-/P4-Wrapper-Lifecycle-Guards bestätigen. Er führt keine Live-HAProxy-Runtime, keine CRS-Regeln und keine positive Response-Body-Enforcement-Rule aus. Der statische HTX-Contract prüft die Source-Invarianten von Phase-4-Dispatch und Finalisierung direkt, ist jedoch keine Host-Runtime-Behauptung.

## Bekannte Einschränkungen

- Eine Live-HAProxy-3.2.21-plus-libmodsecurity-Runtime und CRS-Fixture waren in diesem Task-Worktree nicht verfügbar.
- Ein frischer Exact-Candidate-Codex-Security-Diff-Scan, Hosted-Checks und eine SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

- Künftige Descriptor-Nutzer müssen auf kompatible Body-Append-/Finish-Funktionen und passende Transaction-Felder begrenzt bleiben; eine neue Phase oder ein neuer Ownership-Vertrag benötigt eine Lifecycle-Prüfung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-Runtime, kein Response-Body-Enforcement-Test, kein CRS-Selbsttest und keine vollständige Connector-Matrix sind für diese enge Binding-Lifecycle-Regression geplant. Frische Exact-Candidate-Binding-Builds/-Selbsttests, statische Contracts, ein vollständiger Security-Diff-Scan und Hosted-Checks bleiben vor der Delivery erforderlich.

## Finaler Diff- und Review-Status

Der synchronisierte Kandidat ist auf das Parent-HAProxy-Binding, seinen eng gekoppelten Selbsttest/Fixture/Make-Ziel und bilinguale Traceability begrenzt. Er entfernt zwei bestätigte 17-Zeilen-CPD-Paare, die als 68 Duplikatzeilen gemeldet waren. Frische lokale Compile-, Selbsttest-, statische-Contract-, Whitespace-, Security-Diff-Scan- und Exact-Head-Hosted-Verifikation bleiben vor jeder Delivery- oder Merge-Behauptung erforderlich.
