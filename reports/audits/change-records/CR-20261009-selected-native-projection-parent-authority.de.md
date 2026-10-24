# Change Record: CR-20261009-selected-native-projection-parent-authority

**Sprache:** [English](CR-20261009-selected-native-projection-parent-authority.md) | Deutsch

Nur Dispatcher: Korrektur der Projection-Parent-Autorität für ausgewählte Native-Cases.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-selected-native-projection-parent-authority |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Der tatsächliche f639-Dispatcher erzeugte private 0700-Zwischenparents trotz explizitem Shared-Parent des Wrappers. Der unveränderte Projection-Helper lehnt diese worker-unzugängliche Topologie korrekt ab. Eine neue kontrollierte Dispatcher-Reproduktion bestätigt den falschen an den Driver übergebenen Parent.

## Akzeptanzkriterien

Den exakten expliziten Parent jedem Nicht-RAW-Driver übergeben, ohne ihn zu erzeugen/ändern, private Zwischenparents oder Run-ID-Änderungen. Tatsächliche Helper-Guards nutzen und privaten Output-Modus, geschlossene42-Auswahl, Pflicht-Fixtures, originale Source-Receipts und NOT_EXECUTED erhalten. Unsichere/überlappende Authorities vor Host-Dispatch ablehnen.

## Implementierungsentscheidung und Begründung

Bestehenden Projection-Helper über festen Pfad laden. Tatsächlichen Root-Koordinator, expliziten absoluten traversalfreien Parent und VERIFIED_RUN_ROOT verlangen. Component-NOFOLLOW, bestehende Ownership-/Non-Enumerability-/Traversal-Guards und Overlap-Prädikat gegen Checkout-/Build-/Results-/Verified-/Cache-/Evidence-/Log-/Run-Authorities anwenden. Der Projection-Pfad ist nicht auf SOURCE.STORAGE beschränkt: der genehmigte Shared-Parent darf außerhalb des verifizierten ProjektstorageRoots liegen. Runtime-Outputs behalten ihre External-/Private-Prüfungen. RAW-only-Auswahl braucht keine Projection.

## Geänderte Dateien

Nur `ci/runtime/lifecycle/run-selected-nginx-native-operations.py`, neu `tests/test_nginx_selected_native_projection.py` und dieses generierte EN/DE-Paar im neuen isolierten Worktree.

## Ausgeführte Befehle

RTK-Unit-Befehle/Logs stehen extern in `D-selected-native-projection-parent-results.md`. RED: vier Tests, Exit 1, bisheriger falscher Parent und fehlende Guard. Zwischenlauf scheiterte am neuen kontrollierten Receipt-Fixture mit falschem Envelope; auf das tatsächliche Input-Fault-Source-Envelope korrigiert, ohne Consumer-Änderung. Finale vier vollständige Module: 35 Tests, Exit 0, keine Skips. `git diff --check` bestand. Paar mit Repository-Generator erzeugt; Strukturprüfung separat gespeichert.

## Security-Auswirkung

Keine Guard-Lockerung, chmod/chown des übergebenen Parents, Symlink-Folge, Entfernung, Wiederverwendung oder öffentliche Freigabe privater Outputs. Echte Helper-Prüfungen lehnen alte 0700-Topologie und wiederverwendete direkte Kinder ab. Tests erhalten originale Receipt-Hashbindung und exakte globale Run-IDs; Source-Zeilen bleiben NOT_EXECUTED.

## Runtime-Evidence

Zwei tatsächliche Projection-Vorbereitungen über kontrollierte Dispatcher-Kollaboratoren, echte Reuse-Ablehnung und unverändertes separates FirstByte-Seed. Kopien verwenden die Gruppe des Testprozesses; kein nobody-UID-/65534-Rollen- oder Native-NGINX-Hostnachweis. Kein Native-Server/Build ausgeführt. Parent Required bleibt 97.

## Bekannte Einschränkungen

Bestehende Phase4-/MIME-Kindnamen verwenden nur run_id und kollidieren im Shared-Parent. Der Koordinator hat Case-/Variant-Kindableitung und Framework-Reader-Bindung separat zugewiesen; dieser Dispatcher-Patch behauptet keine All-Group-Freshness. Kombinierte Integrations-/Native-Prüfungen bleiben erforderlich.

## Verbleibende Risiken

Root besitzt Integration mit parallelem Dispatcher-Quality-Patch und muss den tatsächlichen bestehenden externen Parent außerhalb VERIFIED_RUN_ROOT bereitstellen. Bestehender Check/Create-Lebenszyklus des Produkthelpers bleibt unverändert. Neue Source-/Build-/Authority-Bindung folgt nach Integration.

## Nicht ausgeführte Prüfungen mit Begründung

Keine Native-Runtime, Root-/nobody-Transition, Build, Protected-Gate, volle CI/Sonar, API-Schreibzugriffe, MRTS-Initialisierung, Git-Stage/Commit/Push oder Änderungen alter/gemeinsamer Worktrees: außerhalb dieses engen Auftrags. Dokumentationsprüfungen mit initialisierten Submodules bleiben Koordinatoraufgabe.

## Finaler Diff- und Review-Status

Begrenzten Diff gegen aktuelle Producer und unveränderten Helper-Contract geprüft; ungestagte Lieferung in `parent-native-projection-parent-20261009`. Keine Änderung fertiger CI-/Sequence-Quality-Slices. Integration und Native-Rerun liegen bei Root.
