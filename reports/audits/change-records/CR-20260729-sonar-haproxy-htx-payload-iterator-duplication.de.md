# Change Record: Parent-HAProxy-HTX-Payload-Iterator-Deduplizierung

**Sprache:** [English](CR-20260729-sonar-haproxy-htx-payload-iterator-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-haproxy-htx-payload-iterator-duplication |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Tracking | Ein aktuelles SonarQube-Cloud-CPD-Paar: zwei 35-Zeilen-HTX-Request-/Response-Body-Slice-Iteratoren. |
| Grenze | Parent-HAProxy-HTX-Overlay-Source und gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der HTX-Filter enthielt zwei strukturell identische Schleifen für Request- und
Response-Payload-Slices. Beide müssen HAProxys Borrowing-Regel für den
aktuellen Buffer, Offset-Trimming, Unsigned-Size-Grenzen, Non-Data-Block-
Accounting und vollständigen `remaining`-Verbrauch erhalten. Der einzige
beabsichtigte Unterschied ist der bestehende Binding-Einstiegspunkt für die
Request- beziehungsweise Response-Phase.

## Akzeptanzkriterien

- Ein gemeinsamer Iterator erhält jeden Input-Guard, Offset, Bound,
  Borrowed-Pointer-, Block-Accounting- und Return-Value-Pfad der früheren
  Schleifen.
- Explizite Request- und Response-Wrapper behalten ihre bestehenden Namen und
  wählen ausschließlich ihre jeweilige Binding-Funktion.
- Der statische HTX-Lifecycle-Contract besteht, ohne Precommit-Deny,
  Phase-Finalisierung oder Forward-first-Verhalten zu schwächen.
- Exact-Head-Hosted-Checks und SonarQube Cloud müssen weiterhin null New
  Issues, null New-Code-Duplikatzeilen und eine niedrigere Gesamtduplikatanzahl
  beweisen.

## Implementierungsentscheidung und Begründung

Der gemeinsame Iterator akzeptiert einen typisierten Callback, der zu den zwei
bestehenden Binding-APIs passt. Der Callback wird vor dem Parsing validiert und
erst nach derselben vorhandenen HTX-Slice-Validierung aufgerufen. Die Request-
und Response-Wrapper übergeben direkt ihre bestehende Phasenfunktion. Damit
verschwindet die Duplizierung, ohne einen Body-Buffer einzuführen, Ownership zu
ändern oder die unterschiedlichen Phasen zusammenzuführen.

## Geänderte Dateien

- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c` — ein
  typisierter gemeinsamer Payload-Iterator und zwei explizite Phasen-Wrapper.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| `make check-haproxy-htx-overlay` | bestanden; alle statischen HTX-Lifecycle-, Borrowed-Slice-, Phase-Finalisierungs-, Host-Action- und Build-Boundary-Kontrollen bestanden. |
| `git diff --check` | bestanden. |
| Fokussierter Codex-Security-Diff-Scan | bestanden mit null reportbaren Befunden; der versiegelte Report liegt unter `/var/tmp/codex/ModSecurity-conector/security-scans/ModSecurity-conector/dbbc9c6-haproxy-htx-payload-20260729T052500Z/report.md`. |

## Security-Auswirkung

Dieser Source verarbeitet HTTP-abgeleitete Body-Chunks an einer nicht
vertrauenswürdigen Host-Protokoll-Grenze. Die Refaktorierung erhält die
vorhandene Borrowed-Pointer-Regel, weist dieselben ungültigen Offsets und
Längen zurück, behält keine Body-Bytes und ruft weiter getrennte Request- und
Response-Binding-APIs auf. Keine Autorisierungs-, Validierungs-, Isolations-,
Late-Intervention-Policy- oder Quality-Gate-Kontrolle wird gelockert.

## Runtime-Evidence

Der statische HTX-Lifecycle-Contract prüft den version-pinned Overlay-Source
direkt. Er ist keine Live-HAProxy-plus-libmodsecurity-Runtime. Es wird keine
Host-Runtime-Promotion oder Phasenbehauptung gemacht.

## Bekannte Einschränkungen

- Der lokale Worktree enthält keinen gebauten HAProxy-3.2.21-Source-Tree,
  daher ist keine vollständige Overlay-Kompilierung oder Runtime-Smoke
  verfügbar.
- Hosted-Checks und eine frische Exact-Head-SonarQube-Cloud-Analyse stehen aus.

## Verbleibende Risiken

- Der generische Callback muss auf die zwei semantisch kompatiblen
  Body-Chunk-Binding-Funktionen begrenzt bleiben; eine künftige Nutzung für
  andere Phasen benötigt eine neue Lifecycle-Prüfung.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Live-HAProxy-/libmodsecurity-HTX-Runtime und keine vollständige
Connector-Matrix liefen, weil die version-festgeschriebene externe Source und
Runtime-Fixtures fehlen. Der Source-Contract ist die stärkste verfügbare lokale
Kontrolle.

## Finaler Diff- und Review-Status

Der Kandidat ist auf das Parent-HAProxy-Overlay und bilinguale Traceability
begrenzt. Er entfernt ein bestätigtes Duplikatpaar mit 70 Zeilen. Die lokale
Prüfung ist abgeschlossen; ein separater Draft-PR und Exact-Head-Hosted-
Verifikation bleiben vor jeder Delivery- oder Merge-Behauptung erforderlich.
