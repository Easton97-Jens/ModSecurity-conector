# Change Record: CR-20261015-i12-apache-native-evidence

**Sprache:** [English](CR-20261015-i12-apache-native-evidence.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261015-i12-apache-native-evidence |
| Datum (UTC) | 2026-10-15 |
| Evidence-Branch | `codex/i12-apache-410-20261015` |
| Basis-Revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |
| Draft-PR-Ziel | `work/pr382-i12-host-evidence-20261011` |
| Tatsächliche versiegelte Produktquellbasis | `02754040bced960cfc1857416cd7101bb3116ef4` |

## Motivation und Problemstellung

Die Apache-I12-Baseline enthält 155 Pflichtfälle, 25 historische Ausführungen, neun Config-PASS und einen vollständigen Lifecycle-PASS. Config-/Client-Erfolg allein schließt fehlende native, physische Event-, EOS-/Commit- oder Freigabebeobachtungen nicht.

## Akzeptanzkriterien

Alle 155 Original-IDs einzeln bewerten, fehlende Werte als `null` erhalten, Oracles unabhängig abgleichen und ursprüngliche Fehler bewahren. Bestehende Apache-Lifecycle-Pakete erweitern; Apache-Evidence auf einem isolierten Branch gegen den Branch von #410 liefern. Kein `I12_COMPLETE` und keine Release-Freigabe.

## Implementierungsentscheidung und Begründung

Versiegelte source-v5/artifacts-v3 und bestehende Capture-/Native-/Host-Observer wiederverwenden. Neue Fixture-Vorbereitung, abgewartete Client-Aufzeichnung, Kandidatenprüfung, Ledger und Paketierung bleiben Apache-spezifisch. Duplicate-Header-Normalisierung ist an bestätigte Apache-Core-/APR-Semantik und native SDK-Beweise gebunden. Response-Regel-Deduplizierung benötigt echte SDK-Äquivalenz für die exakten Fixture-Payloads. Physische Descriptor-Fehler reichen echte APR-Ergebnisse unverändert weiter.

## Geänderte Dateien

Apache-Harness-Erweiterungen: `ci/runtime/lifecycle/apache-i12/`; gezielte Apache-Tests: `tests/test_apache_i12_*.py`; begrenzte Evidence: `reports/audits/apache-i12-20261015/`; [Apache-Bericht](../../../docs/i12-apache-native-evidence-20261015.de.md) und dieses Change-Record-Paar. Für genaue Dateinamen ist der abschließende Git-Diff maßgeblich.

## Ausgeführte Befehle

RTK-gekapselte native/fokussierte Prüfungen, private Controller-Hostläufe, unabhängige SDK-Proben, Capture-Validierung, Mutationstests und `git diff --check` stehen in den [Evidence-Belegen](../apache-i12-20261015/). Die Launcher-Prüfung `rtk proxy python3 -m unittest discover -s tests -p test_apache_i12_launch.py` bestand mit drei Tests. Frische Aufgabensuiten erfassten 122 fokussierte Tests plus fünf Paketierungs-Qualifikationstests, 76 native Regressionen sowie Capture-Verifikation plus 15 Capture-Tests. Mapper-/Sink-Mutationen wurden erkannt: fünf Tests mit 14 fehlgeschlagenen Assertions beziehungsweise acht Tests mit zwei Fehlern. Das sind erwartete Negativergebnisse.

Dokumentations-/Change-Record-/Pfadprüfungen bestanden mit Exit0 nach Nutzung eines privaten read-only Framework-Mounts für den isolierten Worktree. Der anfängliche Fehler wegen fehlendem Framework/Link bleibt dokumentiert; kein nativer Checker wurde umgangen.

## Security-Auswirkung

Kein Produktfix und keine abgeschwächte Kontrolle. Hosts behalten private Namespaces, UID/GID `65534`, keine Capabilities, `NoNewPrivs`, Ressourcenlimits und schreibgeschützte versiegelte Eingaben. Der APR-Interposer ist explizit aktiviert und auf privaten Marker/Zielpfad begrenzt; echte EBADF-/ENOSPC-Rückgaben bleiben erhalten. Framework, MRTS, zentrale Manifeste/Observer, andere Connectoren und Workflows bleiben unverändert.

## Runtime-Evidence

Das [Fallledger](../apache-i12-20261015/case-ledger.json) enthält die Einzelqualifikation. Bei Berichtserstellung gibt es acht neue vollständige Host-PASS (sieben Request-Fälle plus begrenzter Duplicate-Header-Abgleich), neun eindeutige vollständige Fälle einschließlich Baseline; von 54 Original-Oracles sind acht gelöst und 46 offen. Fünf physische Fehler liefern 500/571 Bytes mit Client-Exit 0, Backendzahlen 0/1/1 und erfolgreiche Folge-/Nachbarrequests mit 200/200. Geschlossener Descriptor liefert echt APR 9/0 Bytes; physisches ENOSPC 28/0 Bytes. Drei frühere Ablehnungen liegen vor APR, dessen Open `null` bleibt. Die fehlerfreie Kontrolle liefert 403/239 Bytes und physische Common-Regeln `120001`, `120016`. Alle 18 beobachteten Sink-/Kontrolltransaktionen räumen genau einmal auf; sechs Controller enden sauber. Fehlerpakete bleiben unvollständig qualifiziert.

## Bekannte Einschränkungen

Die Quellbasis der instrumentierten Runtime unterscheidet sich von der Basis des Evidence-Branches und wird mit Komponentenhashes offengelegt. Natives Audit und Commit-Bindung des Standardfehlerrenderers bleiben für Sinkfehler unvollständig. Response-MIME-/Limit- und Phase-3-Pakete werden nicht aufgrund ihres Status zu PASS. `phase2_truncated` ist ein vollständig gerahmter ProcessPartial-Request, keine HTTP-Trunkierung. Ein literales Kommafeld bleibt hinter Apache-Merging mehrdeutig. Der deduplizierte Reject-Hostversuch endet mit Driver 78/Controller 77 ohne HTTP, weil die ursprüngliche NGINX-Fixture mit `runtime_materializable:false` nicht materialisiert wird; belegt ist nur die native SDK-Reject-Probe. Fehlende Beobachtungen bleiben `null`.

## Verbleibende Risiken

Im dokumentierten Stand bleiben 46 Original-Oracles offen. Erste Exit-78-Fehler durch fehlendes Preamble, doppelte Regeln, unmögliche Fixture-Marker-Erwartungen und ein vorübergehender Controller-Cleanup-Fehler bleiben erhalten. Native disruptive 403 in Fehlerfällen belegt keine unabhängige Audit-Regelzuordnung. Produktbefunde benötigen separat freigegebene Behebung auf #382.

## Nicht ausgeführte Prüfungen mit Begründung

Diese Apache-Änderung führt keine fremden Connector-/Framework-/MRTS-Lieferungen aus und behauptet keinen repositoryweiten Runtime-Durchlauf. Nicht ausgeführte Pflichtfälle stehen ausdrücklich im Ledger. PR-CI-, Review- und Merge-Ergebnisse werden nicht aus lokalen Tests abgeleitet.

## Finaler Diff- und Review-Status

Lokale Prüfbelege und abschließender Diff definieren den geprüften Umfang. Normale Commits/Pushes und Draft-PR-Lieferung sind nur auf dem isolierten Branch gegen den Branch von #410 autorisiert; kein Force-Push oder automatischer Merge. Dieser Record erfindet keine Liefer-SHA, PR-Nummer, CI-Ergebnisse oder Abschlussfreigabe. I12 bleibt insgesamt unvollständig.
