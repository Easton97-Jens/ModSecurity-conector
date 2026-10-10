# Change Record: CR-20261009-native-input-ledger-fd

**Sprache:** [English](CR-20261009-native-input-ledger-fd.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-native-input-ledger-fd |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Unabhängiges Review identifizierte eine bedingte Fixture-Ledger-Identitätslücke: erneutes Pfadöffnen bindet den Writer nicht allein an den zugelassenen privaten Inode. Erreichbarkeit über die gewöhnliche geschlossene CLI oder einen unprivilegierten Angreifer wurde nicht nachgewiesen.

## Akzeptanzkriterien

Nur vorgeöffneten frischen root-eigenen0600 regulären leeren Single-Link-Schreibdeskriptor an den tatsächlichen eigenen Native-Master übergeben. Configtest nie aktivieren; bei jedem Exit fsync und schließen.

## Implementierungsentscheidung und Begründung

MSCONNECTOR_OWNED_INPUT_LEDGER durch MSCONNECTOR_OWNED_INPUT_FD ersetzen. Unverändertes Raw-Leaf exklusiv mit NOFOLLOW über bestehende Private-Root-Autorität öffnen, FD>=3 behalten und exakt diesen Deskriptor an Native-Popen übergeben. Configtest ohne pass_fds lassen; sämtliche INPUT_-Variablen und Preload aus curl entfernen. Verschachteltes finally schließt auch bei Cleanup-/fsync-Ausnahmen.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-common-input-fault.py und tests/test_nginx_common_input_fault_driver.py. Das C-Fixture-Gegenstück ist eine separat besessene koordinierte Änderung; hier wurde kein C-Fixture editiert.

## Ausgeführte Befehle

Kontrollierte FD-Tests scheiterten vor Migration (Exit1), danach bestand das Pointer-Driver-Modul7 Tests (Exit0). Finaler aktueller Sechs-Modul-Fokus58 Tests/48.211s/Exit0 ohne Skips enthält Configtest-Ausnahme-Cleanup. Evidenz: python-sonar-ledger-red.log, python-sonar-ledger-green.log und python-sonar-slice-final-focus-r2.log. Tests nutzen echte Dateideskriptoren mit gemocktem Prozessstart, keinen Native-Prozess.

Unabhängiges Kandidatenreview identifizierte eine begrenzte Acquisition-Cleanup-Lücke bei Ausnahme während Private-Root-Kontextende nach Ledger-Erstellung. Der kontrollierte Kontextende-Test scheiterte zunächst (1 Test, Exit1: Deskriptor blieb offen). Erweiterung des bestehenden Deskriptor-Cleanup-try um Kontexteintritt/Acquisition/Ende schließt diesen Deskriptor. RTK-gewrapptes Parent Python -m unittest tests.test_nginx_common_input_fault_driver -v mit externem TMPDIR und explizitem FRAMEWORK_ROOT bestand danach9 Tests/0.804s/Exit0 ohne Skips. Keine Änderung an pass_fds oder Receipt-Verhalten; kein nachgewiesener Exploit.

## Security-Auswirkung

Fixture-Ressourcenintegrität wiederherstellen, ohne zugelassene Faults zu erweitern, Common-Mapping zu ändern oder native Events zu erfinden. Bedingtes Fixture-Risiko ist kein nachgewiesener gewöhnlicher CLI-Exploit.

## Runtime-Evidence

Keine Native-Runtime oder geladener Interposer ausgeführt. Tatsächliche lokale Inode-/FD-Beobachtungen in Unit-Tests belegen nur Producer-Verhalten.

## Bekannte Einschränkungen

Driver und separat besessenes C-Fixture müssen zusammen mit identischem FD-Umgebungsnamen und Konstruktorvalidierung integriert werden. Raw-Ledger-Basename, Originalbytes und SHA-Retention bleiben unverändert.

## Verbleibende Risiken

Frische integrierte Native-Ausführung und unabhängiges Source-/Security-Review bleiben erforderlich; Unit-FD-Tests beweisen keine native Fault-Zustellung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, Native-E2E, neuer Scan, Authentifizierungs-/Konfigurationsmutation, Git-Schreibzugriff oder Veröffentlichung. Integration und Runtime durch Koordinator.

## Finaler Diff- und Review-Status

Isolierten uncommitteten Kandidaten auf exakte pass_fds, unbewaffneten Configtest und Finally-Cleanup geprüft. Security-Record getrennt von verhaltenserhaltenden Qualitätsänderungen.
