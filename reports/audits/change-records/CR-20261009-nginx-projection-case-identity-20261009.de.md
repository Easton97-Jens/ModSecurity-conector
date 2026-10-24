# Change Record: CR-20261009-nginx-projection-case-identity-20261009

**Sprache:** [English](CR-20261009-nginx-projection-case-identity-20261009.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-projection-case-identity-20261009 |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | f63996290925f4b0c04d286506171825de9dc2ff |

## Motivation und Problemstellung

Zwei Cases desselben Runs kollidierten im gemeinsamen Projection-Kind.

## Akzeptanzkriterien

Case-/Run-Identität und strikte Pfadprüfung bleiben erhalten.

## Implementierungsentscheidung und Begründung

phase4- plus24 SHA256-Hexzeichen aus run_id:case_id; tatsächliche E-Child-Run-ID, kein Altformat.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-phase4-cases.py und gezielter neuer Test; EN/DE-Record.

## Ausgeführte Befehle

Unittest-Fokus:17 Tests, Exit0. Roter Originalpfad: TypeError beziehungsweise bestehendes Projection-Kind. Diff-Check:0.

## Security-Auswirkung

Keine Guard-, Authority-, Status- oder Seal-Abschwächung.

## Runtime-Evidence

Keine. Kontrollierter Configtest stoppt vor Native-Start; NOT_EXECUTED bleibt erhalten.

## Bekannte Einschränkungen

Dateisystem kann gid65534 nicht abbilden; nur fchown kontrolliert, erwartete65534 geprüft. Exklusive Erstellung, Kopieren und Modi bleiben real.

## Verbleibende Risiken

Integrierte Native-Prüfung und Veröffentlichung bleiben Root vorbehalten.

## Nicht ausgeführte Prüfungen mit Begründung

Native-Build/Runtime nicht autorisiert; Archive-Checker0 und scoped Record-Pfade0; vollständige Parent-Dokumentationsprüfung scheitert an unbefülltem Framework-Gitlink (18 Pfad-/22 Bilingual-Ziele).

## Finaler Diff- und Review-Status

Enger unstaged Diff geprüft, keine Git-Schreibaktionen.
