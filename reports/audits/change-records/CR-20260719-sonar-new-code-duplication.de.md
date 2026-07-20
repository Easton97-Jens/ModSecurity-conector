# Change Record: Behebung der SonarQube-Cloud-New-Code-Duplizierung

**Sprache:** [English](CR-20260719-sonar-new-code-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260719-sonar-new-code-duplication` |
| Datum (UTC) | `2026-07-19` |
| Basis-Revision | `79d224a1c20d648974923630c7746d4b6511f9be` |
| Tracking | Behebung der New-Code-Duplizierung für SonarQube-Cloud-Draft-PR #61; es wurde kein eigenständiger Finding-Eintrag angelegt. |
| Grenze | Nur Parent-`common`-Event-JSON-Serialisierung und ihr fokussierter Smoke-Test; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

Die Exact-Head-Analyse von SonarQube Cloud für Draft-PR #61 meldete 106 neue
Zeilen, zwei neue duplizierte Zeilen, zwei neue duplizierte Blöcke und eine
New-Code-Duplizierungsdichte von `1.8867924528301887%` (angezeigt als 1,9%).
Beide Blöcke lagen in `common/src/event.c`: im gemeinsamen Validierungsrumpf
für erforderliche Transport-Case-IDs und optionale Transport-Metadatenwerte.

## Akzeptanzkriterien

- Die vorhandene Unterscheidung zwischen erforderlichen und optionalen
  Leerwerten bleibt erhalten.
- Die vorhandene Längen- und Zeichensatzvalidierung für nichtleere
  Transport-Token bleibt erhalten.
- Bei ungültigen optionalen Transport-Metadaten bleiben Auslassung und
  Trunkierung erhalten, während ein gültiger Kontrollfall weiterhin
  serialisiert wird.
- Der gemeldete duplizierte Validierungsrumpf wird ohne SonarQube-Einstellung,
  Suppression, Exclusion oder Quality-Gate-Workaround entfernt.
- Nach dem Follow-up-Commit wird ein frischer SonarQube-Cloud-Readback für den
  exakten PR-Head eingeholt.

## Implementierungsentscheidung und Begründung

Ein privates `is_bounded_transport_token(const char *value, int allow_empty)`
besitzt jetzt die vorhandene `strlen`-Grenze und das ASCII-Token-
Zeichenprädikat. `is_bounded_transport_case_id` ruft es mit `0` auf; der
Wrapper für optionale Werte ruft es mit `1` auf. Damit bleiben alle vorhandenen
Aufrufer und ihre Verträge unverändert, es gibt keine Änderung einer
öffentlichen API, und nur die duplizierte Implementierung entfällt.

Der fokussierte Common-Helper-Smoke-Test ergänzt einen ungültigen
`reset_by`-Wert mit einem Leerzeichen. Er prüft `truncated`, die Auslassung
beider optionalen Provenance-Felder und das Fehlen des abgewiesenen Werts. Ein
getrennter gültiger `reset_by`/`reset_code`-Kontrollfall prüft die normale
Serialisierung und `truncated:false`.

## Security-Auswirkung

Die geänderten Validatoren kontrollieren Transport-/Korrelationsmetadaten,
bevor diese in das Event-JSON-Provenance-Fragment gelangen. Das Refactoring
erhält die Regel für erforderliche Case-IDs, die Null-/Leerwert-Erlaubnis für
optionale Werte, die 128-Byte-Grenze, den Token-Zeichensatz und das gemeinsame
Leeren aller fünf optionalen Werte. Eine unabhängige fokussierte Prüfung fand
bei Erhalt dieser Invarianten keinen plausiblen Security-Kandidaten.

## Geänderte Dateien

- `common/src/event.c`
- `ci/checks/common/check-common-helpers.sh`
- `reports/audits/change-records/README.md` und `README.de.md`
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `rtk env BUILD_ROOT=<task-owned run>/build/gcc-c17 TMPDIR=<task-owned run>/tmp CC=gcc make check-common-helpers-c17` | bestanden mit GCC 15.2.0 und `-std=c17 -Wall -Wextra -Werror`. |
| `rtk env BUILD_ROOT=<task-owned run>/build/clang-c17 TMPDIR=<task-owned run>/tmp CC=clang make check-common-helpers-c17` | bestanden mit Clang 21.1.8 und `-std=c17 -Wall -Wextra -Werror`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-common-security-contract` | bestanden: `common security contract: ok`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-common-flow-integrity` | bestanden: `common flow integrity: ok`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-bilingual-docs` | durch fehlende Framework-Linkziele im Sparse-Worktree blockiert; nach Korrektur der Change-Record-Überschriften meldete die Prüfung keinen Fehler für dieses Paar. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned run>/tmp make check-doc-links` | durch dieselben fehlenden Framework-Linkziele blockiert; kein geänderter Parent-Link wurde gemeldet. |
| `rtk git diff --check` | nach den Dokumentationsergänzungen bestanden. |

## Runtime-Evidence

Nicht anwendbar. Dies ist ein privates Common-Validierungsrefactoring mit
Smoke-Test-Ergänzung; es startet keinen Connector-Host und behauptet keine
Runtime-Kompatibilität.

## Nicht ausgeführte Prüfungen mit Begründung

- `make check-common-helpers-c23` ist beratend und wurde nicht ausgewählt, weil
  der geänderte C-Code kein C23-spezifisches Verhalten besitzt; die erforderlichen
  C17-Prüfungen bestanden mit beiden verfügbaren Compilern.
- Vollständige Connector-Builds, Host-Runtime-Harnesses, Framework-Prüfungen
  und MRTS-Prüfungen wurden nicht ausgeführt, weil sich kein Connector-,
  Framework- oder MRTS-Verhalten änderte.
- Frische Exact-Head-SonarQube-Cloud- und GitHub-PR-Prüfungen sind
  Delivery-Evidence, keine lokale Evidence; sie müssen vor jedem
  Verified-PR-Claim beobachtet werden.

## Bekannte Einschränkungen

Dieser Record hält die SonarQube-Cloud-Metrik vor der Behebung fest. Das finale
Ergebnis ohne New-Code-Duplizierung wird nicht behauptet, bevor die PR-Analyse
des neuen Commits beobachtet und an dessen exakte SHA gebunden ist.

## Verbleibende Risiken

Ein invertiertes `allow_empty`-Argument könnte entweder leere Case-IDs
akzeptieren oder legitime leere optionale Werte abweisen. Die erforderlichen/
optionalen Wrapper-Aufrufe und die neue negative plus kontrollierte
Smoke-Abdeckung mindern dieses Risiko. Dieser Record enthält keine rohe
Transportkennung und keinen request-abgeleiteten Payload.

## Finaler Diff- und Review-Status

Die begrenzte Implementierung, die unabhängige Sicherheitsprüfung, die
C17-Smoke-Prüfungen, die Common-Sicherheits-/Datenflussverträge und
`git diff --check` bestanden. Die Dokumentationsbefehle sind nur durch bereits
fehlende Framework-Linkziele in diesem Sparse-Worktree blockiert und melden
keinen Fehler für dieses Change-Record-Paar. Begrenzter Diff-Review, Commit/
Push und Exact-Head-SonarQube-Cloud-Evidence werden über die PR-Delivery
bewertet; dieser Record autorisiert keinen Merge.
