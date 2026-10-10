# Change Record: CR-20261008-nginx-native-authority-mrts-root

**Sprache:** [English](CR-20261008-nginx-native-authority-mrts-root.md) | Deutsch

Explizite Read-only-MRTS-Quellauswahl; Unit-Wiring-Evidence.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-authority-mrts-root |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `603e84493dcb51ab72eadb5a7102c4977cab631c` |

## Motivation und Problemstellung

Ein isolierter Framework-Worktree kann tools/MRTS uninitialisiert lassen. Git meldet dann das übergeordnete Framework statt eines unabhängigen MRTS-Repositories; der Authority-Producer lehnt dies korrekt ab.

## Akzeptanzkriterien

Explizites MRTS_ROOT unverändert durchreichen, ohne Angabe den bisherigen Standard Framework/tools/MRTS erhalten und Producer-Identitäts-/Pin-/Sicherheitsvalidierung unverändert lassen.

## Implementierungsentscheidung und Begründung

Das Producer-Argument der Baseline nutzt jetzt ${MRTS_ROOT:-$FRAMEWORK_ROOT/tools/MRTS}, wie das vorhandene run-mrts-native-full.sh. Der Aufrufer wählt ein tatsächliches initialisiertes Read-only-Repository; keine Root-Entdeckung oder historische SHA-Ausweichlogik.

## Geänderte Dateien

Ein Baseline-Argument, eine fokussierte Kontrolle in test_no_crs_native_authority_wiring.py und dieser zweisprachige Record.

## Ausgeführte Befehle

Die Assertion für den expliziten Override scheiterte vor der Änderung (RED). Danach bestanden alle neun begrenzten extrahierten Shell-Wiring-Kontrollen in 4,408 Sekunden. Shell-Syntax, Archiv und abschließende Whitespace-Prüfungen sind im Handoff dokumentiert.

## Security-Auswirkung

Kein MRTS-Checkout, Pin oder Quellcode wird geändert. Explizites MRTS_ROOT durchläuft weiterhin Producer-Prüfungen für unabhängigen Top-Level, aktuellen HEAD40, sauberen Status und Gleichheit zum aktuellen Framework-Gitlink. Ein Receipt liefert keine SHA.

## Runtime-Evidence

Kein nativer Runtime-/Build-Lauf. Der Argumenttest verwendet ein Producer-Unit-Double und ein leeres ausgewähltes Verzeichnis; er belegt Durchreichen und ausbleibende Quellschreibzugriffe, nicht Repository-Autorität oder Host-Verhalten.

## Bekannte Einschränkungen

Read-only-Inspektion bestätigte ein initialisiertes sauberes MRTS mit aktuellem HEAD 8a6bb546c4c81d8ffc7be801dceac60c6925685f; der inspizierte Framework-Gitlink entsprach ihm. Das ist eine Momentaufnahme, keine fest codierte erwartete SHA oder aufbewahrte Build-Autorität.

## Verbleibende Risiken

Aktuelle saubere Parent-/Framework-Pins, vorbereitete Release-/Engine-Bereitschaft und alle fünf kompilierten Fault-Libraries bleiben Koordinator-Voraussetzungen. Der Authority-Producer prüft tatsächliche Identitäten erneut.

## Nicht ausgeführte Prüfungen mit Begründung

Build, native Runtime, MRTS-Änderungen und Quellpin-Updates lagen außerhalb dieses Slice. Keine Cache-/Build-/Release-Semantik geändert.

## Finaler Diff- und Review-Status

Der finale Diff beschränkt sich auf expliziten Override, begrenzte Regression und zweisprachigen Record. Producer-Quelle/Sicherheit, originales release-1.31.6-Verhalten und vorhandene Commits bleiben erhalten.
