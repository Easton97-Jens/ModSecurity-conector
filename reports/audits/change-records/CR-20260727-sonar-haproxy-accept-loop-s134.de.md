# Change Record: Parent-HAProxy-Accept-Loop-Fehlerpfadbereinigung für SonarQube Cloud C:S134

**Sprache:** [English](CR-20260727-sonar-haproxy-accept-loop-s134.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-haproxy-accept-loop-s134 |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-Code-Smell-Receipt `AZ7HxAr7_i61V0DF6_H2` für `c:S134` in `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` in `accept_loop(...)`. |
| Grenze | Parent-HAProxy-Quelltext, sein fokussierter Parent-Reliability-Contract-Test sowie dieses englisch/deutsche Change-Record-Paar mit seinen Indizes. Framework, MRTS, Gitlinks, Workflow-Konfiguration, Scanner-Konfiguration, Quality Gates, Suppressions und der externe SonarQube-Cloud-Issue-Status bleiben unverändert. |
| Kandidatenstatus | Lokal und uncommittet. Es gab kein Staging, keinen Commit, Push, Pull Request oder Merge sowie keine Framework- oder MRTS-Änderung und kein Gitlink-Update. |

## Motivation und Problemstellung

Receipt `AZ7HxAr7_i61V0DF6_H2` kennzeichnet die verschachtelte Fehlerbehandlung
in der `accept_loop(...)`-Funktion der HAProxy-Diagnose-Runtime als `c:S134`.
Die Korrektur beschränkt sich darauf, die bestehende Unterscheidung im
Fehlerpfad explizit zu machen, ohne den erfolgreichen
Verbindungsverarbeitungspfad zu ändern:

- ein nicht-`EINTR`-`accept()`-Fehler muss `accept failed errno=%d` loggen und
  `1` zurückgeben;
- ein `EINTR`-Fehler muss bei angeforderter Beendigung abbrechen, anderenfalls
  erneut versuchen;
- ein erfolgreich angenommener Deskriptor muss in derselben Reihenfolge durch
  `handle_connection(...)`, `close(...)` und die bestehende Aktualisierung des
  Handled-Zählers laufen.

## Akzeptanzkriterien

- Das nicht-`EINTR`-Log-and-Return-Verhalten exakt erhalten.
- Das Break bei `EINTR` plus angeforderter Beendigung und den Retry ohne
  angeforderte Beendigung erhalten.
- Ein fehlgeschlagenes `accept()`-Ergebnis weder durch die
  Verbindungsverarbeitung noch durch `close(...)` oder die Aktualisierung des
  Handled-Zählers schicken.
- Die Reihenfolge der Verarbeitung erfolgreicher Deskriptoren erhalten.
- Die dokumentierte Validation-Evidence und ihre Autoritätsgrenzen korrekt
  halten; vorläufige Default-Root-Prüfungen sind keine autoritative Evidence.

## Implementierungsentscheidung und Begründung

Der Kandidat macht den terminalen Fehlerfall zur äußeren Bedingung:
`errno != EINTR` loggt die bestehende Diagnose und gibt `1` zurück. Der
verbleibende Interrupted-Call-Pfad behandelt dann nur noch den Shutdown-Break
oder Retry. Damit verschwindet die von `c:S134` beanstandete vermeidbare
Verschachtelung, während jede Fehlerdisposition erhalten bleibt und die
erfolgreiche Verbindungsverarbeitung unverändert bleibt.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — Kandidat für
  die Abflachung des `accept_loop(...)`-Fehlerpfads.
- `tests/test_sonar_reliability_contract.py` — fokussierte
  Source-Contract-Regression für die drei Fehlerdispositionen und den
  unveränderten Erfolgspfad.
- `reports/audits/change-records/CR-20260727-sonar-haproxy-accept-loop-s134.md`
  und `.de.md` — dieses bilinguale Change-Record-Paar.
- `reports/audits/change-records/README.md` und `README.de.md` — gepaarte
  Indexeinträge.

## Ausgeführte Befehle

| Ausgeführte Kontrolle oder dokumentierte Validierung | Beobachtetes Ergebnis |
| --- | --- |
| Fokussiertes Parent-Unit-Modul `tests.test_sonar_reliability_contract` | bestanden: 7 Unit-Tests. |
| HAProxy-Common-Adoption-Kontrolle | bestanden. |
| HAProxy-C-Standard-Wiring-Kontrolle | bestanden. |
| Autoritative isolierte GCC-15.2-C17-Kompilierung | bestanden mit einem task-eigenen externen Root; dieser Root wurde nach der Validierung bereinigt. |
| Autoritative isolierte Clang-21.1-C17-Kompilierung | bestanden mit einem task-eigenen externen Root; dieser Root wurde nach der Validierung bereinigt. |
| Vorläufige Default-Root-Prüfungen | nicht autoritativ und aus der Akzeptanz-Evidence ausgeschlossen. |
| Fokussierte Ausführung der Change-Record-Strukturparitätsroutinen aus `ci/checks/documentation/check-bilingual-docs.py` | bestanden: erforderliche Überschriften, Sprachumschalter, Identitätsfelder, Überschriftenebenen, Tabellenblöcke und Fenced-Block-Struktur stimmen überein. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | bestanden nach ausschließlich lesender Initialisierung der im Parent festgeschriebenen Framework-Revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`: `bilingual docs ok`, `repository path references: PASS` und `doc links ok`. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Es wurde kein neuer reportbarer Sicherheitsbefund identifiziert. Dies ist eine
Maintainability-Code-Smell-Remediation, kein nachgewiesener
angreiferkontrollierter Pfad und keine Änderung einer Vertrauensgrenze. Die
relevante Fehlerpfadinvariante wurde geprüft: Ein fehlgeschlagenes
`accept()`-Ergebnis darf `handle_connection(...)`, `close(...)` oder die
Aktualisierung des Handled-Zählers nicht erreichen; ein nicht-`EINTR`-Fehler
loggt und kehrt zurück, während nur `EINTR` erneut versuchen kann und eine
angeforderte Beendigung die Schleife abbricht. Der Kandidat erhält diese
Invariante und führt kein Parsing-, Authentifizierungs-, Autorisierungs-,
Privilegien- oder Datenflussverhalten ein.

## Runtime-Evidence

Es wird kein Live-HAProxy-Network-Runtime-Ergebnis beansprucht. Die sieben
fokussierten Unit-Tests prüfen den Source Contract, und die isolierten GCC-15.2-
und Clang-21.1-C17-Prüfungen liefern Kompilierungs-Evidence. Diese Prüfungen
ersetzen weder eine Live-Connector-Runtime noch eine gehostete
SonarQube-Cloud-Analyse.

## Bekannte Einschränkungen

- Der SonarQube-Cloud-Receipt ist an die angegebene Basis-Revision gebunden;
  es wird keine Exact-Head-gehostete Analyse und kein Issue-Abschluss
  beansprucht.
- Für diesen Kandidaten lief keine Live-HAProxy-Runtime und keine vollständige
  Connector-Matrix.
- Die task-eigenen externen Compiler-Roots wurden nach den autoritativen
  isolierten Prüfungen bereinigt; vorläufige Default-Root-Prüfungen werden
  bewusst nicht als autoritative Evidence verwendet.

## Verbleibende Risiken

Der fokussierte Contract und die zwei isolierten C17-Compiler-Prüfungen
reduzieren das Risiko einer Änderung der drei Fehlerdispositionen, üben aber
keine Betriebssystem-Signal-Timings in einem Live-HAProxy-Prozess aus. Eine
künftige Exact-Head-SonarQube-Cloud-Analyse kann den Receipt weiterhin
melden, bis sie einen ausgelieferten Kandidaten analysiert; dieser Record
beansprucht keine Änderung des externen Status.

## Nicht ausgeführte Prüfungen mit Begründung

Es liefen keine Live-HAProxy-Runtime, keine vollständige Connector-Matrix,
keine gehostete GitHub-CI, keine gehostete SonarQube-Cloud-Analyse, keine
Delivery-Aktion sowie keine Framework- oder MRTS-Aktion. Der Task ist nur ein
lokaler Parent-Kandidat mit Dokumentationsrecord; diese getrennten Kontrollen
und Repositories liegen außerhalb dieses autorisierten Umfangs.

## Finaler Diff- und Review-Status

Der Worktree enthält einen lokalen, uncommitteten Kandidaten aus dem
HAProxy-Source-Refactor, seinem fokussierten Test und diesem bilingualen
Dokumentationspaar mit Indizes. Es wurde kein Git-Staging, Commit, Push, Pull
Request, Merge, Framework- oder MRTS-Source-Change und kein Gitlink-Update
vorgenommen. Der fokussierte Change-Record-Strukturparitätscheck, die
vollständigen Dokumentations-/Link-Checks und der Whitespace-Diff-Check
bestanden. Das im Parent festgeschriebene Framework wurde nur für diese
Dokumentationschecks lesend initialisiert; sein Source, sein Gitlink und sein
verschachtelter MRTS-Status bleiben unverändert.
