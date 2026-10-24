# Change Record: CR-20261008-nginx-common-input-fault-driver

**Sprache:** [English](CR-20261008-nginx-common-input-fault-driver.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-common-input-fault-driver |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `48243d5f77a6ae52b52729b6d6a2447229f6fab6` |

## Motivation und Problemstellung

Zwei Required-Adapter-Input-Faults benötigen echte Requests am tatsächlichen Common-Guard, keine fehlerhafte Wire-Syntax oder Driver-Events.

## Akzeptanzkriterien

Exakte Worker-/native Transaktions-/POST-URI-Injektion, echter Mapper-Return0/Diagnose, tatsächlicher400/nativer Protokollfehler ohne Regel, begrenztes Cleanup und Wrong-Target-Kontrollen.

## Implementierungsentscheidung und Begründung

Attempt-lokalen Interposer ausschließlich in eigenen nativen Master laden. Echte Transaktionserstellung und Common-Validator delegieren; genau eine Request-Kopie am passenden exportierten Validator verändern.

## Geänderte Dateien

Neuer dedizierter Driver, nativer Interposer, kompilierte simulierte Scope-Fixture, zwei Fokustestmodule und dieses zweisprachige Paar.

## Ausgeführte Befehle

Driver-Datei fehlt RED, dann2GREEN; kompilierte Scope-Fixture fehlt RED, dann2GREEN mit sechs Wrong-Target-Kontrollen. C17Wall/Wextra/Werror-Build0; Common-Invarianten4GREEN. Isolierter alter Cache: Header echt400/Commonreturn0/nativ protocol_error und Driver0; WrongTX Driver1/405 ohne Ledger/Event; alter Body-Guard Return1/405 bleibt RED. Cleanup geprüft/keinNGX danach.

## Security-Auswirkung

Kein Produkthook, globaler Fault-Schalter, erfundenes Common-Event oder gelockerte Isolation. Nur Root-eigenes0600-Ledger; Fixture-Library gehasht und requestgebunden.

## Runtime-Evidence

Native Diagnose unter Task stream-a-input-r1/r2 mit Root/nobody/Maps/Config/Fault/Access/Events/Cleanup. Artefakt-Build b740/a904 getrennt von neuem Helper-Source48243/Framework210a33c. R1 erwartete phase1_error, Common-Protocol-View liefert protocol_error; strikter Helfer korrigiert und frischer Header-R2 erfolgreich. Prozesssimulation bleibt Unit-only; Body-Positiv/neues Modul und finale Coverage nicht behauptet.

## Bekannte Einschränkungen

Benötigt neu gebautes natives Modul mit separat committed Body-Pointer-Guard, Koordinator-Slot, Framework-Validator und zentrale geschlossene Receipt-Integration.

## Verbleibende Risiken

Native Events/Diagnosen und exakte rohe Artefakt-Hashes müssen übereinstimmen. Body-Akzeptanz des alten Cache ist RED-Kontrolle, keine umetikettierte neue Quelle.

## Nicht ausgeführte Prüfungen mit Begründung

Protected-Exact-Head, vollständiger E2E/Lint und Remote-Prüfungen fehlen. Body-Positiv benötigt neu gebauten Produkt-Guard; Header-Diagnose beweist keinen finalen Exact-Head-PASS.

## Finaler Diff- und Review-Status

Nur eigene neue Dateien. Separater Commit nach begrenztem nativen Fokus; kein Push, Merge, Amend, Gitlink- oder MRTS-Eingriff. Zentrale Receipt-Validierung bleibt beim Koordinator.
