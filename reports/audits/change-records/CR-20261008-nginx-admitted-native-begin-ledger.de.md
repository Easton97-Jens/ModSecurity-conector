# Change Record: CR-20261008-nginx-admitted-native-begin-ledger

**Sprache:** [English](CR-20261008-nginx-admitted-native-begin-ledger.md) | Deutsch

Versuchsgebundene BEGIN-Allocation-Evidenz, keine native Runtime-Promotion.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-admitted-native-begin-ledger |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `20478534e305a35c7f92fd80e8303a92121a5a3a` |

## Motivation und Problemstellung

Die begrenzte native Allocation-Fixture lieferte zuvor still NULL und hatte keinen geerbten Evidenzdeskriptor-Guard. Der Treiber hielt keine nativen BEGIN-Beobachtungen fest und schloss gewöhnliche/Fault-/Finish-Events aus seiner vollständigen Sourceprojektion aus.

## Akzeptanzkriterien

Ein tatsächlicher eigener Child-/Exact-TX-Injection-NULL-Record vor Rückkehr, privater rootgehörender anfangs leerer Deskriptor-Guard, Wrong-TX-/No-FD-/Invalid-FD-Kontrollen, vollständige Originalevent-Erhaltung und Roh-SHA. Kein nativer NGINX-Lauf oder Produktmodul-Build; begrenzte C17-Fixture-Prüfung ausdrücklich erlaubt.

## Implementierungsentscheidung und Begründung

Root-Konstruktor verlangt exakten Modus/TX und geerbtes MSCONNECTOR_OWNED_BEGIN_FD dezimal >=3, schreibbares reguläres rootgehörendes privates0600/Single-Link/leeres File. Der tatsächliche Nobody-Child dieses Masters schreibt vor NULL-Rückkehr eine Zeile: native_operation msc_new_transaction_with_id, observed_return null, tatsächliche worker_pid/worker_uid65534/master_pid, transaction_id, injected true. Fehlende/ungültige Deskriptoren armieren nicht; fehlgeschlagene Writes injizieren nicht. Keine Phasen/Rules/Events werden erfunden. Der Treiber öffnet das Ledger vorab, übergibt das bestehende Deskriptortupel nur dem tatsächlichen Master, fsynct und schließt in verschachteltem finally, erfasst originale native_begin und native_begin_sha256 und erhält jedes originale Phase1-Event für alle Sequenzfälle.

## Geänderte Dateien

Nur eigene tests/fixtures/nginx_transaction_fault.c und ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py, neue tests/test_nginx_native_begin_ledger.py und test_nginx_begin_driver_evidence.py sowie dieser gepaarte Record. Root genehmigte normale Cherry-pick-Materialisierung von sieben vorherigen Sequenztreibercommits; deren gepaarter Record-Konflikt erhielt beide alten Transport-/Finish-Fakten. Keine neuen Source-/Gitlink-/Framework-/MRTS-/Shared-Collector-Änderungen.

## Ausgeführte Befehle

RTK-gewrapte Parent-Unittest-Befehle verwenden `${PARENT_PYTHON}`, PYTHONNOUSERSITE=1/PYTHONDONTWRITEBYTECODE=1. `-m unittest discover -s tests -p test_nginx_native_begin_ledger.py`: Sandbox-Exit1 wegen Setuid-Einschränkung (kein Produkt-RED); eskalierte alte Fixture Exit1/zehn gezielte Fehler; geänderte Fixture Exit0/drei Tests, dreizehn begrenzte Fake-Engine-/Harness-Aufrufe. Jeweils kompiliert mit cc -std=c17 -Wall -Wextra -Werror (nur versuchsgebundene Shared-Fixture/Stub/Harness). `-p test_nginx_begin_driver_evidence.py`: drei Tests0; `-p test_nginx_sequence_driver.py`: neun0; `-p test_nginx_sequence*.py`: fünfzehn0; Dispatcher-Regression acht0. Scaffold lehnte zuerst abgekürzten Basis-SHA ab Exit2, danach Full-SHA create0. Finale AST-/Record-/Paar-/Diffchecks im Handoff.

## Security-Auswirkung

Geschlossene eigene Root-Master-/Nobody-Child-/Transaktionsgrenze; kein globaler Fehler oder fremde Prozessmutation. Deskriptor-Guards werden verstärkt, nicht gelockert. Nur geerbte Root-Capability hält Metadaten ohne native Payload-, Phasen- oder Rule-Prämisse fest. Negative Fixture-Kontrollen prüfen Identität, fehlenden/ungültigen Deskriptor, Rechte, Linkzahl, Ausgangsinhalte, Readonly-Zugriff, UID und Elternscope.

## Runtime-Evidence

Keine native NGINX-Ausführung oder Modul-Build. Der C17-Harness ruft den tatsächlichen Versuchsinterposer über ein gefaktes originales Engine-Symbol auf, forkt tatsächlich credentialbegrenzte Children und validiert sein Ledger; dies ist nur Fixture-Verhalten, keine Engine-/Host-/Common-Integrationsevidenz. Root-Moduländerungen an Admission/Error/Cleanup dienten nur readonly Kontext und bleiben separat zu authentifizieren.

## Bekannte Einschränkungen

Root muss die tatsächliche ausgewählte Fault-Bibliothek neu bauen und ihre unveränderliche Digestauthority liefern. C-Sourcehash ist kein kompilierter Bibliotheksnachweis. Die Child-Credential-Fixture braucht Root/Compiler und Erlaubnis zum Senken von Subprozess-Credentials; strikte Umgebungsfehler werden nicht als grün umgedeutet.

## Verbleibende Risiken

Tatsächlich zugelassener Common-before-native-allocation-Error und Cleanup(native0) sowie vollständige Source-Phase1-Zeilen benötigen Roots neues Modul und Reader-Laufzeitvalidierung. D stimmte exakten BEGIN-Receipt-Feldern/native_begin_sha256 zu und bleibt Reader-Eigentümer. Alle vorherigen nativen Laufzeitlücken bleiben offen.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Lauf/full E2E/Produktbuild, Framework-/MRTS-Mutation oder Scanner/Publish/Push. Parent-Ruff zuvor nicht verfügbar; kein Install. Root besitzt finale integrierte Source-/Bibliotheks-/Modul-/Reader-Prüfungen.

## Finaler Diff- und Review-Status

Nur neues BEGIN-Ledger und vollständige Source-Eventerfassung gegen exakte delegierte Grenzen geprüft. Gewöhnliche WRITE-/FINISH-/BUDGET-Modi und Host-FD-Guards bleiben unverändert oder erhalten garantiertes Close-on-fsync-error-Cleanup. Keine Runtime-Promotion oder Lockerung zentraler Validierung.
