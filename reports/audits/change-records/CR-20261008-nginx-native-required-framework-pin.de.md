# Change Record: CR-20261008-nginx-native-required-framework-pin

**Sprache:** [English](CR-20261008-nginx-native-required-framework-pin.md) | Deutsch

Separates Framework-Gitlink-Update; dieser Nachweis bestätigt keinen nativen Lauf.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-required-framework-pin |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `767de5bf4e901f256dffbca76547af4ee6b54757` |

## Motivation und Problemstellung

Der integrierte Selected-Native-Dispatch des Parents benötigt die geschlossenen
Operationsdeskriptoren, Original-Evidence-Authority und strikte Canonical-Zuordnung
des Frameworks. Sein alter Gitlink enthielt diese abgestimmten Verträge nicht.

## Akzeptanzkriterien

Den veröffentlichten, sauberen Framework-Commit
`61b9f33ad44fa92b916059d2f3e1944c6a4f1bf3` separat pinnen. Alle 97 selektierten
Required-Identitäten und den MRTS-Gitlink erhalten. Evidence-Prüfungen nicht
abschwächen; weder der Pin noch bestandene Source-Tests schließen die 45
fehlenden Nachweise eines frischen Runtime-Laufs.

## Implementierungsentscheidung und Begründung

Den regulär veröffentlichten Framework-Folgecommit nach erfolgreichem vollständigem
nativen Lint und No-CRS-Vertragstest verwenden. Das Framework ergänzt 42 explizite
native Routen, strikte Originalbyte-Authority-/Receipt-Prüfung und die freigegebenen
Konfigurationsverträge; der aktuelle Plan enthält 42 native, 10 Konfigurations-,
31 abgeleitete und 14 YAML-Aufrufe. Für diesen Pin ist kein zusätzlicher
Parent-Dispatch-Fix nötig.

## Geänderte Dateien

Nur `modules/ModSecurity-test-Framework` und dieses EN/DE-Change-Record-Paar.
`tools/MRTS` im Framework bleibt
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`; beide `.gitmodules` bleiben unverändert.

## Ausgeführte Befehle

Framework `make test-no-crs-contract` über RTK: 385 Tests, Exit 0.
Framework `make lint` über RTK: Exit 0, einschließlich Provenienz-, Workflow-,
Katalog- und Dokumentationsprüfungen. Parent `make lint` an der Basisrevision:
Exit 0. Tatsächlicher Framework-Git-HEAD, sauberer Arbeitsbaum, Gitlink und
reguläre Dateien wurden geprüft; regulärer Push, `git ls-remote` und PR-API-
Readback stimmen beim neuen Framework-SHA überein. PR #137 bleibt OPEN/DRAFT
mit unveränderter Basis.

## Security-Auswirkung

Selektierte Required-Records benötigen weiterhin echte Evidence. Fehlende
Caller-Authority oder Aufrufdeskriptoren, fremde Identitäten, widersprüchliche
native Fakten und veränderte aufbewahrte Bytes werden weiter abgewiesen. Kein
geschützter Runner, keine Trusted Base, kein HostGate, Validator und keine
Namespace-Schutzprüfung wird ersetzt oder abgeschwächt.

## Runtime-Evidence

Dieses Update behauptet keine frische integrierte native Ausführung. Der
ursprüngliche Canonical-Status bleibt NOT_EXECUTED. Frühere Diagnoseartefakte
werden nicht zu Evidence dieses neuen Parent-/Framework-Tupels umetikettiert.

## Bekannte Einschränkungen

Die finalen vertrauensabhängigen Parent-Tests müssen nach dem committed Gitlink
und dem passenden sauberen lokalen Framework-Checkout laufen. Frische
revisionsgebundene PR-CI-/Sonar-Ergebnisse bleiben von erfolgreichen lokalen
Make-Prüfungen getrennt. Ruff ist nicht verfügbar; sein separater Lint lief nicht.

## Verbleibende Risiken

Tatsächliche native Artefaktprovenienz, sämtliche Required-Request-/Konfigurations-/
Fault-Beobachtungen, Cleanup und finale Canonical-Prüfung benötigen weiter den
frischen integrierten Runtime-Lauf. Die unabhängige Basis und administrativen
Runner-Voraussetzungen des geschützten Workflows bleiben offen; ein lokaler
Candidate-Lauf kann sie nicht erfüllen.

## Nicht ausgeführte Prüfungen mit Begründung

Parent-Fokusprüfungen nach dem Pin und der vollständige native Lifecycle liefen
vor diesem Pin-Commit nicht, da sie dessen sauberes exaktes Gitlink-Tupel benötigen.
Bei fehlenden Trusted-Base-Voraussetzungen wird kein geschützter Lauf ausgelöst.

## Finaler Diff- und Review-Status

Der Umfang bleibt auf den Gitlink und diesen zweisprachigen Nachweis begrenzt.
Framework-Historie und MRTS bleiben unverändert. Der Review prüft den exakten
veröffentlichten SHA und trennt Source-Integration, lokale Runtime und geschützte
Attestierung ausdrücklich.
