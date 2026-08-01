# Finding: Der Append-Fehlerpfad des nativen Oracle gibt einen Request-Body doppelt frei

**Sprache:** [English](finding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0036` |
| Kategorie | `sanitizer_finding` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P2` / `medium` / `confirmed` |
| Status | `fixed` |
| Release-Blocker / sicherheitsrelevant | nein / ja |

## Zusammenfassung, Verhalten und Auswirkung

Der historische Zweig für einen nichtleeren Body gab `body.data` frei, wenn
`msc_append_request_body(...) == 0` war, und erreichte dann gemeinsames Cleanup
mit weiterhin nicht-null Pointer. Das Cleanup gab ihn erneut frei. ASan gegen
echtes LibModSecurity 3.0.16 meldete `attempting double-free`, wenn ein enger
ein-symboliger Interposer diesen Library-Fehler erzwang. Dies beweist einen
Memory-Safety-/Availability-Defekt des kurzlebigen Oracle-Prozesses, nicht die
Reachability durch gewöhnlichen Remote-Input.

Erwartet ist, dass die Allokation einmal freigegeben und Pointer/Größe vor dem
gemeinsamen Cleanup-Guard geleert werden.

## Betroffener Umfang und Voraussetzungen

- Datei/Symbole: `ci/tools/native_modsecurity_oracle.c`,
  `msc_append_request_body`, `cleanup_error`, `cleanup_oracle` und `body.data`.
- Ein nichtleerer Body ist alloziert und `msc_append_request_body` liefert null.

## Reproduktion und Evidenz

1. Das historische Oracle mit ASan bauen und den erhaltenen ein-symboligen
   `LD_PRELOAD`-Interposer verwenden, der `msc_append_request_body` null
   zurückgeben lässt.
2. Einen nichtleeren Body ausführen und den historischen Double-Free
   beobachten; den patch-äquivalenten Zweig ohne ASan-Diagnose wiederholen.
3. Die erhaltene Evidenz hat den historischen Pfad
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/native-oracle-lifetime-revalidation.md`
   (nicht in diesem Reconciliation-Checkout verteilt),
   SHA-256 `5d676317ed37403f1eae272c23f3c93e744e1fad9cbc2366fdd67a832fb8a7b5`.
   Exact-PR-D-Head `5704905c5337f9dcfe8c08a78a7e482ecd72bbf7` bestand seinen
   fokussierten Regressionstest und Clang-/GCC-Statik-Kontrollen.
4. Der aktuelle Task-Run `ci-tools-sonar-remediation-20260730` refaktoriert
   aktuellen Teardown durch `cleanup_oracle`. Sein versiegelter fokussierter
   Security-Diff-Report besitzt SHA-256
   `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7`;
   C17-GCC/Clang- und Real-LibModSecurity-200/403/Setup-Error-Controls
   bestanden. Ein natürlicher `msc_append_request_body`-Fehler wurde nicht
   reproduziert, daher ist dies One-Owner-Source-/Control-Evidence statt neuer
   Reachability-Behauptung.

## Root Cause und Remediation

Das branch-lokale `free(body.data)` stellte die gemeinsame Cleanup-Invariante
nicht her. PR D setzt `body.data = NULL` und `body.size = 0` direkt nach dem
Append-Fehler-free und behält den bestehenden guarded Cleanup-Pfad plus
fokussierten Regressionstest bei. Das aktuelle ci/tools-Refactoring führt
zusätzlich aktuellen Teardown durch `cleanup_oracle`, sodass `body.data` einen
Owner besitzt, ohne einen natürlich reproduzierten Append-Fehler zu behaupten.

## Akzeptanz, Validierung und Kontrollen

- Der Append-Fehlerzweig leert Pointer/Größe vor gemeinsamem Cleanup.
- `tests/test_native_oracle_memory_safety.py` besteht.
- Der historische ASan-Replay unterscheidet den alten Double-Free vom
  patch-äquivalenten fehlerfreien Replay; C17-Clang-/GCC-fanalyzer-Kontrollen
  bestehen.
- Aktuelle C17-GCC/Clang-Warning-as-Error- und Real-LibModSecurity-200/403/
  Setup-Error-Controls bewahren Result- und Cleanup-Verhalten nach dem
  One-Owner-Refactoring.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Geschützter Squash-PR #200 lieferte das One-Owner-Refactoring auf resultierenden
Parent-Master `13890da56ad19a105629243349f39ea8c084f396`; Exact-Master-
Workflow- und Source-Identity-Evidence sind erhalten. `FND-PARENT-0035` ist
getrennte Regel-/Output-Autorität. Eine realistische nicht-synthetische Library-
Append-Failure ist nicht verfügbar; Produktions-/Remote-Reachability bleibt
unbestätigt und ist keine Exploit-Behauptung. Auch das aktuelle Refactoring
reproduzierte diesen natürlichen Fehler nicht. Die verbleibende Einschränkung
ist der nicht verfügbare stärkste historische ASan-/One-Symbol-Interposer-
Replay mit referenziertem Harness; es erfolgte keine Risikoakzeptanz.

## Historie

- `2026-07-18T14:46:42Z`: historischer ASan-Fehlerpfad bestätigt; Exact-PR-D-
  Head-Kontrolle bestand; Status auf `fixed` pending verified PR gesetzt.
- `2026-07-30T11:07:21Z`: aktuelles One-Owner-Cleanup-Refactoring mit
  versiegeltem Security-Review, Compiler-/Runtime-Controls und dem Exact-
  Draft-PR-#200-Hosted-Check-/SonarQube-Cloud-Receipt revalidiert. Kein
  natürlicher Append-Fehler wurde reproduziert, daher bleibt der Status `fixed`,
  nicht `verified`.
- `2026-07-30T11:33:48Z`: aufgefrischter exakter Draft-PR-#200-Head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` gegen Master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` bestand erforderliche GitHub-Checks und SonarQube-Cloud-Quality-Gate/Readbacks. Diese Delivery-Evidence reproduziert keinen natürlichen Append-Fehler neu; das historische Finding bleibt daher `fixed`, nicht `verified`.

## Resulting-Master-Disposition

Geschützter Squash-PR #200 vom exakten Head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` erzeugte Parent-Master
`13890da56ad19a105629243349f39ea8c084f396` am `2026-07-30T12:11:32Z`.
Der Native-Oracle-Blob entspricht dem geprüften Kandidaten und alle 14
Master-Workflows bestanden. Dies bestätigt die Auslieferung des One-Owner-
Source-Refactorings, erzeugt aber nicht den erforderlichen historischen
ASan-/One-Symbol-Interposer-Append-Failure-Replay erneut. Der referenzierte
stärkste Harness/Evidence fehlt in diesem Workspace; natürliche Reachability
wird nicht abgeleitet. Der Status bleibt `fixed`, nicht `verified` oder
`closed`. Receipt-SHA-256:
`69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
