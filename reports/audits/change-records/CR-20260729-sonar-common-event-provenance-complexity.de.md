# Change Record: Parent-Common-Event-Provenance-Serialisierungszerlegung für SonarQube Cloud c:S3776

**Sprache:** [English](CR-20260729-sonar-common-event-provenance-complexity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-event-provenance-complexity |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 |
| Tracking | SonarQube-Cloud-Regel `c:S3776` in `common/src/event.c:382`: Cognitive Complexity von 32 auf die erlaubten 25 reduzieren. Die offene PR [#174](https://github.com/Easton97-Jens/ModSecurity-conector/pull/174) begann am initialen Head `8baef24192ccaaa39e38e89238b8d2e8e90baec9`; der spätere Remote-Head war `b92084c523498978b55de9068240752314bbedc3` vor seiner erforderlichen normalen Master-Synchronisierung. Historische Actions-/Sonar-Beobachtungen des initialen Heads verifizieren keinen synchronisierten Kandidaten. Sein exakter Head, Reviews, Actions und SonarQube-Cloud-Evidence müssen vor der Integration frisch verifiziert werden. Ein Merge wird nicht behauptet. |
| Grenze | Parent-`common`-Event-JSON-Provenance-Serialisierung, fokussierte Common-Helper-Smoke-Assertions und dieses englisch/deutsche Change-Record-Paar mit seinen Indizes. Framework, MRTS, Gitlinks, Workflows, Scanner-Policy, generierte Artefakte und `master` werden nicht verändert. |

## Motivation und Problemstellung

`msconnector_event_write_json_ex` serialisiert escapte Metadaten und begrenzte Protocol-Provenance in ein Audit-JSON-Event. SonarQube Cloud meldet dafür eine Cognitive Complexity von 32 und damit mehr als die erlaubten 25. Der bisherige Source nutzte eine lange Short-Circuit-Kette sowohl zum Ermitteln von Protocol-Daten als auch zum Anhängen aller Protocol-Strings und Boolean-Felder.

Diese Maintainability-Änderung liegt an einer sicherheitsrelevanten Audit-Grenze. Sie muss die Prüfbarkeit verbessern, ohne rohe Transport-Identifier, unbegrenzte Werte, partielle Provenance oder verändertes Truncation-Verhalten in den JSON-Sink gelangen zu lassen.

## Akzeptanzkriterien

- Den `c:S3776`-Befund in begrenzte Helper zerlegen, ohne Event-JSON-Feldnamen oder -reihenfolge zu verändern.
- Escaping, Transport-Case-Validierung, Transport-Value-Filterung und QUIC-CID-Redaktion vor jedem tabellengesteuerten Provenance-Append ausführen.
- Leere Werte auslassen, erlaubte Werte und Flags geordnet bewahren und bei Append-Kapazitätsfehlern weiterhin fail-closed bleiben.
- GCC- und Clang-C17-Common-Helper-Controls mit `-Wall -Wextra -Werror` bestehen. Der C23-Advisory-Control darf C17-Evidence nicht ersetzen.
- Befüllte Protocol-Werte sowie vorhandene Negativ-Controls für Raw-CID, Invalid-Token und Truncation testen.
- Ein äquivalentes englisch/deutsches Change-Record-Paar pflegen. Gehostete PR-Evidence erst nach ihrem Vorliegen dokumentieren.

## Implementierungsentscheidung und Begründung

Feste C17-Arrays deklarieren nun die etablierten Protocol-String- und Boolean-Feldnamen. `append_event_provenance` behält `run_id` und `transport_case_id` bei und delegiert die verbleibenden geordneten Protocol-Felder an `append_protocol_metadata`. Der Presence-Check und die Append-Schleife verwenden dieselben bereits escapten und validierten lokalen Werte wie die frühere Kette.

Die Arrays halten die Reihenfolge an einer Stelle sichtbar, ohne einen Helper mit vielen Parametern oder einen großen veränderlichen State-Struct einzuführen. Es wird keine C23-Sprach- oder Bibliotheksfunktionalität verwendet. Der Smoke asserted nun jeden befüllten Protocol-String dieses Pfades zusätzlich zu vorhandenen Boolean-, Raw-CID-, Invalid-Token- und Truncation-Prüfungen.

## Security-Auswirkung

Kontrollierte Inputs sind request-nahe Protocol-Metadaten und Transportdiagnosen. Das Asset ist die Integrität des Audit-Events, der Sink ist das JSON-Provenance-Fragment, und die Trust Boundary wird erst überschritten, nachdem die bestehenden `escape_field`-, Transport-Token-Validierungs- und QUIC-CID-Nichtreversibilitätsprüfungen die lokalen Arrays befüllt haben.

Der Refactor übergibt diese gefilterten lokalen Werte an den Append-Helper und keine Source-Felder direkt. Vorhandene Negativ-Controls bestätigen, dass rohe QUIC-CIDs und ungültige Transportdaten fehlen, während der legitime Control die vorhandenen erlaubten Felder bestätigt. Der Fehlerpfad bleibt fail-closed: Jeder Protocol-Append-Fehler setzt `was_truncated` und leert `provenance_json`. Keine Autorisierungs-, Validierungs-, Redaktions-, Integritäts-, Logging-, Scanner- oder Quality-Gate-Control wird geschwächt.

## Geänderte Dateien

- `common/src/event.c`
- `ci/checks/common/check-common-helpers.sh`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260729-sonar-common-event-provenance-complexity.md`
- `reports/audits/change-records/CR-20260729-sonar-common-event-provenance-complexity.de.md`

## Ausgeführte Befehle

| Befehl | Tatsächliches Ergebnis |
| --- | --- |
| `make check-common-helpers CC=gcc MSCONNECTOR_C_STD=c17 MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"` | bestanden; der Common-Helper-Smoke wurde mit GCC im C17-Modus kompiliert und ausgeführt. |
| `make check-common-helpers CC=clang MSCONNECTOR_C_STD=c17 MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"` | bestanden; der Common-Helper-Smoke wurde mit Clang im C17-Modus kompiliert und ausgeführt. |
| `make check-common-helpers-c23` | als Advisory für neuere C-Version bestanden; er ersetzt nicht die C17-Evidence. |
| `make check-common-security-contract check-common-sdk-contract check-common-flow-integrity` | bestanden. |
| `git diff --check` | vor Hinzufügen dieses Records bestanden; wird vor Delivery erneut für den finalen Kandidaten-Diff ausgeführt. |
| `gh pr view 174` und SonarQube-Cloud-PR-APIs für den initialen Head `8baef24192ccaaa39e38e89238b8d2e8e90baec9` | erfolgreiche/erwartet übersprungene Actions-Checks, Quality Gate `OK`, 0 offene PR-Issues, 0 neue Violations und 0,0 % New-Code-Duplikation beobachtet. |

## Tests und tatsächliche Ergebnisse

| Control | Ergebnis |
| --- | --- |
| Befüllter-Protocol-Common-Helper-Control | bestanden: asserted `run_id`, `transport_case_id`, alle befüllten Protocol-Strings, alle Flags, Reset-Daten und Lifecycle-Diagnostik. |
| Raw-QUIC-CID-Negativ-Control | bestanden: `raw-quic-cid` bleibt nach Serialisierung eines Protocol-enthaltenden Events abwesend. |
| Controls für ungültige Transport-Metadaten | bestanden: ungültige Metadaten fehlen, das Ergebnis ist als truncated markiert und betroffene Provenance-Felder werden nicht ausgegeben. |
| Output-Capacity-Control | bestanden: ein zu kleiner Buffer erzeugt ein NUL-begrenztes Ergebnis und meldet Truncation. |
| Fokussierter Security-Review | bestanden: Werte erreichen die Tabellen erst nach Escape-, Validierungs- und CID-Redaktionszweigen; geordneter Append und fail-closed Cleanup wurden gegen die frühere Kette geprüft. Es wurde keine reportbare Regression festgestellt. |

## Runtime-Evidence

Es wurde keine Connector-, Host-, Framework- oder MRTS-Runtime gestartet. Der Common-Helper-Smoke ist nur fokussierte Source-/Build-Evidence und belegt keine Deployment- oder Host-Runtime-Kompatibilität.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine reale Connector-Runtime und die vollständige Connector-Matrix wurden nicht ausgeführt: Die Änderung beschränkt sich auf Common-Event-Serialisierung, und repository-native Common-Helper-, Security-, SDK- und Flow-Controls prüfen diese Grenze.
- Framework- und MRTS-Prüfungen wurden nicht ausgeführt, weil sie außerhalb der gewählten Parent-`common`-Grenze liegen und keines der Repositories verändert wurde.
- Ein vollständiger Repository-Security-Scan wurde nicht ausgeführt: Der fokussierte Security-Review und der Common-Security-Contract decken den geänderten Serialisierungspfad ab; dieser Record behauptet keine repository-weite Coverage.
- Historische Hosted-Evidence wurde nur für `8baef24192ccaaa39e38e89238b8d2e8e90baec9` beobachtet. Der spätere Remote-Head und jeder normal Master-synchronisierte Kandidat benötigen frische GitHub-Actions-, SonarQube-Cloud-PR-Analyse-, Review-Status- und Exact-Head-Evidence, bevor der PR als verifiziert dargestellt wird.

## Bekannte Einschränkungen

Der lokale Helper-Smoke validiert repräsentative Metadaten-, Redaktions- und Truncation-Verhalten, ist aber kein Connector-Host-Integrationstest. Die offene PR #174 besitzt noch keinen Merge, keine Freigabe und keine finale synchronisierte-Head-Hosted-Evidence.

## Verbleibende Risiken

Künftige Ergänzungen müssen Name-Arrays, Value-Arrays und Negativ-Controls synchron halten; ein nicht übereinstimmender Index könnte Provenance auslassen oder falsch kennzeichnen. Feste Enum-Dimensionen, geordnete Tabellen-Review, Assertions für befüllte Felder, C17-Controls und fail-closed Append-Verhalten mindern dieses Risiko. Eine Exact-Head-Hosted-Analyse bleibt nötig, um die tatsächliche Sonar-Behebung zu verifizieren.

## Finaler Diff- und Review-Status

Der scoped Kandidat verändert nur die Common-Event-Provenance-Zerlegung, seine fokussierten Smoke-Assertions und die gekoppelten Change-Record-/Index-Dokumente. Der initiale Commit `8baef24192ccaaa39e38e89238b8d2e8e90baec9` öffnete PR #174, und der spätere Remote-Head `b92084c523498978b55de9068240752314bbedc3` enthält diesen Dokumentations-Follow-up. Eine normale Synchronisierung erzeugt einen neuen unverifizierten Kandidaten. Es wird keine Framework-, MRTS-, Gitlink-, Workflow-, SonarQube-Regel-, Default-Branch- oder Merge-Aktion behauptet. Finale Dokumentationsprüfungen und Exact-Head-Hosted-Verifikation stehen noch aus.
