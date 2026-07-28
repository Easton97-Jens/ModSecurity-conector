# Change Record: Parent-Common-Event-Provenance-Short-Circuit-Refaktorierung für SonarQube Cloud c:S1066

**Sprache:** [English](CR-20260728-sonar-common-event-s1066.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-common-event-s1066 |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Tracking | SonarQube-Cloud-Issue `AZ9cRy9OHhV2CayPTP4Z`, Regel `c:S1066`, in `common/src/event.c:547`. Der Task-Kontext bezeichnet PR #153 als Kandidaten; hier werden kein gehosteter Issue-, Quality-Gate-, Workflow-, Review- oder Exact-Head-Status behauptet. |
| Grenze | Parent-`common`-Event-JSON-Provenance-Serialisierung und ihre fokussierten Common-Helper-Smoke-Assertions sowie dieses englisch/deutsche Change-Record-Paar und die beiden Change-Record-Indizes. Diese Dokumentationsaufgabe greift nicht auf Framework, MRTS, Gitlinks, Workflows, Scanner-Policy, generierte Artefakte oder gehosteten PR-Status zu und verändert sie nicht. |

## Motivation und Problemstellung

Der gemeldete `c:S1066`-Issue kennzeichnet eine verschachtelte Bedingung in
`common/src/event.c:547`. Der äußere `protocol_present`-Guard umschloss zuvor
die bestehende Fehlerkette für Protocol-Appends. Der Kandidat entfernt nur
diese redundante Verschachtelung; das Event-JSON-Provenance-Fragment darf bei
einem Fehlschlag eines seiner Append-Helper weiterhin kein partielles Ergebnis
ausgeben.

Dies ist eine Maintainability-Refaktorierung an einer Audit-/Provenance-Grenze.
Sie muss das bestehende Auslassungsverhalten bei fehlenden Protocol-Daten und
die bestehende fail-closed Bereinigung bei einem nicht abschließbaren
Protocol-Append bewahren.

## Akzeptanzkriterien

- Der `protocol_present`-Guard und die vollständige vorhandene
  Append-Fehlerkette bleiben durch C-Short-Circuit-Auswertung semantisch
  äquivalent.
- Wenn keine Protocol-Provenance vorhanden ist, wird kein Protocol-Append-
  Helper ausgewertet und kein Protocol-Provenance-Feld ausgegeben.
- Wenn Protocol-Provenance vorhanden ist, behalten die Append-Aufrufe ihre
  Reihenfolge; jeder fehlgeschlagene Append setzt weiterhin `was_truncated`
  und leert `provenance_json`.
- Der fokussierte Smoke behält einen No-Protocol-Negativ-Control und einen
  befüllten Protocol-Provenance-Control einschließlich Assertions für
  `requested_protocol` und `connection_reused`.
- Das englisch/deutsche Change-Record-Paar und beide Indizes halten die lokale
  Evidence korrekt fest und behandeln gehostete SonarQube-Cloud- und
  PR-Evidence als ausstehend.

## Implementierungsentscheidung und Begründung

Der Kandidat ändert die verschachtelte Form zu einer Bedingung:

```c
if (protocol_present && (/* unchanged append-failure OR chain */)) {
    was_truncated = 1;
    provenance_json[0] = '\0';
}
```

In C wertet `&&` die rechte Seite nicht aus, wenn `protocol_present` false
ist. Das ist dasselbe No-Append-Verhalten wie beim früheren äußeren `if`. Ist
es true, ruft die unveränderte parenthesierte `||`-Kette dieselben
`append_protocol_string`- und `append_protocol_bool`-Aufrufe in derselben
Reihenfolge auf und behält ihr bestehendes Short-Circuit-bei-Fehler-Verhalten.
Ein Fehler führt weiterhin die unveränderte fail-closed Bereinigung aus,
anstatt ein partielles Protocol-Provenance-Fragment zu veröffentlichen.

Die Refaktorierung verändert weder `protocol_present`, einen der Append-Helper,
die Feldreihenfolge, die bestehende Auslassung leerer Strings noch den
umgebenden Event-JSON-Writer. Der Smoke ergänzt direkte Assertions für fehlende
Protocol-Felder im Negativ-Control und erwartete Felder im befüllten Control.

## Security-Auswirkung

Protocol-Provenance wird in ein Event-/Audit-JSON-Fragment serialisiert. Die
bestehenden Schutzvorkehrungen bleiben erhalten: Der `protocol_present`-Guard
unterdrückt das Protocol-Fragment, wenn es fehlt, die Append-Helper behalten
ihr bestehendes Validierungs- und Kapazitätsfehlerverhalten bei, und ein
fehlgeschlagener Append markiert das Event als truncated und leert das gesamte
Protocol-Provenance-Fragment. Dieser reine Control-Flow-Refactor führt keinen
neuen Input, Sink, Trust Boundary, keine Suppression und keine geschwächte
Security Control ein.

Dieser Record behauptet weder ein neu validiertes Security-Finding noch ein
gehostetes Security-Ergebnis. Er hält nur das bewahrte fail-closed Verhalten
des Kandidaten und die verfügbare fokussierte Source-Level-Evidence fest.

## Geänderte Dateien

- `common/src/event.c`
- `ci/checks/common/check-common-helpers.sh`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260728-sonar-common-event-s1066.md`
- `reports/audits/change-records/CR-20260728-sonar-common-event-s1066.de.md`

## Ausgeführte Befehle

| Befehl | Tatsächliches Ergebnis |
| --- | --- |
| `make check-common-sdk-contract check-common-security-contract check-common-flow-integrity` mit `/root/git/ModSecurity-conector/.venv/bin/python` | bestanden, wie vom Main Agent beobachtet. |
| `make CC=gcc check-common-helpers-c17` | bestanden, wie vom Main Agent beobachtet; dies entspricht dem bereitgestellten GCC-C17-Common-Helper-Worker-Ergebnis. |
| `make CC=clang check-common-helpers-c17` | bestanden, wie vom Main Agent beobachtet; dies entspricht dem bereitgestellten Clang-C17-Common-Helper-Worker-Ergebnis. |
| `git diff --check` | bestanden, wie vom Main Agent beobachtet, und für dieses Dokumentationsupdate erneut über `rtk proxy -- git diff --check` ausgeführt. |

## Tests und tatsächliche Ergebnisse

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Main-Agent-Common-SDK-/Security-/Flow-Contracts und GCC-/Clang-C17-Common-Helper-Smokes | bestanden; ihre einzelnen Befehle und Ergebnisse stehen oben. Dieser reine Dokumentations-Scope führte die Source-Validierungsbefehle nicht erneut aus. |
| Enge englisch/deutsche Record-Paritäts- und Index-Link-Review | bestanden: Beide Begleitfassungen enthalten dieselbe Change-ID, Basis-Revision, Sonar-Issue-ID, Regel, Source-Location, Validierungsgrenze und Hosted-Evidence-Einschränkung; beide Indizes verlinken ihre passende Begleitfassung. |
| `rtk proxy -- git diff --no-index --check` für jeden neuen Record gegen `/dev/null` | es wurde kein Whitespace-Fehler gemeldet. Exit `1` ist erwartet, weil jeder Befehl eine neue Datei mit `/dev/null` vergleicht. |

## Runtime-Evidence

Es wurde keine Connector-, Host-, Framework- oder MRTS-Runtime gestartet. Die
Common-Helper-Smokes sind fokussierte Source-/Build-Evidence; sie belegen keine
Deployment- oder Host-Runtime-Kompatibilität.

## Nicht ausgeführte Prüfungen mit Begründung

- Die GCC- und Clang-Common-Helper-Smokes wurden von dieser reinen
  Dokumentationsaufgabe nicht erneut ausgeführt; ihr bestandener Status ist
  als bereitgestellte beobachtete Kandidaten-Evidence festgehalten.
- Repository-weite Bilingual-Dokumentations- und Dokumentationslink-Prüfungen
  wurden nicht ausgeführt, weil die aktuelle Aufgabe nur enge
  Dokumentations-/Diff-Validierung erlaubt, die Framework oder MRTS weder
  aufruft noch verändert.
- Gehostete SonarQube-Cloud-Issue-/Quality-Gate-Readbacks, PR-Workflows,
  Review-Status und Exact-Head-Verifikation bleiben externe ausstehende
  Evidence für PR #153 und wurden von dieser Aufgabe nicht abgefragt.
- Vollständige Connector-Builds, Runtime-Matrizen, Framework-Prüfungen,
  MRTS-Prüfungen und ein breiter Security-Scan liegen außerhalb dieses
  fokussierten Control-Flow- und Dokumentations-Scopes.

## Bekannte Einschränkungen

Dieser Record besitzt keine gehostete Exact-Head-SHA-, SonarQube-Cloud-
Quality-Gate-, PR-Workflow- oder Review-Evidence. Er behauptet auch kein
vollständiges Connector- oder Deployment-Runtime-Ergebnis. Die lokale Evidence
ist auf die Main-Agent-Common-SDK-/Security-/Flow-Contracts und GCC-/Clang-
C17-Common-Helper-Smokes, den scoped Source-Review, die Record-Parität und die
Whitespace-Prüfung begrenzt.

## Verbleibende Risiken

Die Source-Änderung ist bewusst klein, aber eine spätere Änderung der
Append-Kette könnte ihre Fehlerreihenfolge oder ihr Short-Circuit-Verhalten
ändern. Die negativen und befüllten Protocol-Smoke-Controls, der scoped
Diff-Review und die bewahrte Bereinigung mindern dieses Risiko. Eine frische
gehostete Analyse für den exakten PR-Head ist weiterhin erforderlich, bevor
`AZ9cRy9OHhV2CayPTP4Z` als behoben behandelt oder PR #153 als verifiziert
dargestellt wird.

## Finaler Diff- und Review-Status

Der scoped Source-Diff führt nur die verschachtelte Bedingung zusammen und
bewahrt den bestehenden Fehler-Body. Die Helper-Smoke-Änderungen dokumentieren
beide Controls für fehlende und vorhandene Protocol-Provenance. Dieses
englisch/deutsche Record-Paar, seine beiden Indizes und `git diff --check`
erhielten die oben festgehaltene enge lokale Review. Gehostete SonarQube-Cloud-
und PR-Evidence bleibt ausstehend; diese Dokumentationsaufgabe führte kein
Staging, keinen Commit, Push, PR-Update, Merge oder `master`-Aktion aus.
